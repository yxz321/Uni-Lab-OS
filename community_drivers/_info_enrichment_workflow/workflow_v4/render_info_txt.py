#!/usr/bin/env python3
"""Merge intermediate artifacts and render production info.txt files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


COMMUNITY_DIR = Path(__file__).resolve().parent.parent.parent


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def load_optional_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return load_json(path)


def dedupe_tags(tags: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for tag in tags:
        if not isinstance(tag, dict):
            continue
        key = (str(tag.get('id', '')).strip(), str(tag.get('name', '')).strip(), str(tag.get('type', '')).strip())
        if key in seen:
            continue
        seen.add(key)
        out.append(tag)
    return out


def merge_payload(signals: dict[str, Any], profile: dict[str, Any], tag_result: dict[str, Any] | None, device_dir: Path) -> dict[str, Any]:
    registry = signals['registry']
    parsed = profile.get('parsed', {})

    action_descs = {a['action_name']: a for a in parsed.get('actions', []) if isinstance(a, dict) and 'action_name' in a}
    action_mappings: dict[str, Any] = {}

    for action_str in registry.get('actions', []):
        action_name = action_str.split(' (from ')[0].strip()
        schema: dict[str, Any] = {}
        desc = action_descs.get(action_name)
        if desc is not None:
            schema['description'] = desc.get('description', '')
            schema['description_en'] = desc.get('description_en', '')
        action_mappings[action_name] = {'schema': schema}

    if not action_mappings:
        driver = signals.get('driver', {})
        for m in driver.get('focal_methods', []):
            func_name = m['function'].split('(')[0]
            action_name = f'auto-{func_name}'
            schema = {}
            desc = action_descs.get(action_name)
            if desc is not None:
                schema['description'] = desc.get('description', '')
                schema['description_en'] = desc.get('description_en', '')
            action_mappings[action_name] = {'schema': schema}

    existing_tags: list[dict[str, str]] = []
    proposed_new_tags: list[dict[str, str]] = []
    if tag_result:
        existing_tags = [tag for tag in tag_result.get('existing_tags', []) if isinstance(tag, dict)]
        proposed_new_tags = [tag for tag in tag_result.get('proposed_new_tags', []) if isinstance(tag, dict)]

    combined_tags = dedupe_tags(existing_tags + proposed_new_tags)
    tag_names_cn = list(dict.fromkeys(t.get('name', '') for t in combined_tags if t.get('name')))
    category_names_cn = list(dict.fromkeys(t.get('name', '') for t in combined_tags if t.get('name') and t.get('type') == 'device_template_tag'))

    websearch_evidence = None
    if profile.get('websearch_evidence_path'):
        evidence_path = Path(profile.get('websearch_evidence_path', ''))
        if not evidence_path.is_absolute():
            evidence_path = device_dir / evidence_path.name
        websearch_evidence = load_optional_json(evidence_path)

    return {
        'device': signals['device'],
        'device_entry': {
            'name': parsed.get('name', ''),
            'name_en': parsed.get('name_en', ''),
            'manufacturer': parsed.get('manufacturer', ''),
            'category': category_names_cn,
            'tags': tag_names_cn,
            'description': parsed.get('description', ''),
            'description_en': parsed.get('description_en', ''),
            'class': {'action_value_mappings': action_mappings},
        },
        'auto_annotation_metadata': {
            'registry_key': signals['device'],
            'annotation_workflow_version': 'v4',
            'tag_hints': parsed.get('tag_hints', []),
            'existing_tags': existing_tags,
            'proposed_new_tags': proposed_new_tags,
            'websearch_evidence': websearch_evidence or {'used': False, 'findings': []},
            'processing_pass_order': [
                'deterministic_local_extraction',
                'per_device_semantic_profile',
                'agent_conflict_check_and_web_search',
                'batch_tag_pass',
                'payload_merge',
                'render_info_txt',
                'validate_and_review',
            ],
        },
    }


def render_info_txt(payload: dict[str, Any]) -> str:
    device_key = payload['device']
    info = {device_key: payload['device_entry'], 'auto_annotation_metadata': payload['auto_annotation_metadata']}
    return yaml.dump(info, default_flow_style=False, allow_unicode=True, sort_keys=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--signals-dir', type=Path, required=True, help='Batch directory containing per-device artifact dirs')
    parser.add_argument('--write-info-txt', action='store_true', help='Write info.txt to community_drivers/<device>/info.txt')
    parser.add_argument('--write-preview', action='store_true', help='Also write info.txt into the batch-local device artifact dir')
    args = parser.parse_args()

    device_dirs = sorted([p for p in args.signals_dir.iterdir() if p.is_dir() and not p.name.startswith('_')])
    for device_dir in device_dirs:
        signals_path = device_dir / '01_local_signals.json'
        profile_path = device_dir / '02_device_profile_api.json'
        if not signals_path.exists() or not profile_path.exists():
            print(f'skip {device_dir.name}: missing 01 or 02')
            continue

        signals = load_json(signals_path)
        profile = load_json(profile_path)
        tag_result = None
        batch_tag_path = device_dir / '_batch_tag_api.json'
        if batch_tag_path.exists():
            batch_data = load_json(batch_tag_path)
            tag_result = batch_data.get('device_result')

        payload = merge_payload(signals, profile, tag_result, device_dir)
        (device_dir / '03_enriched_payload.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        info_yaml = render_info_txt(payload)
        if args.write_preview:
            (device_dir / 'info.txt').write_text(info_yaml, encoding='utf-8')
            print(f'wrote preview {device_dir / "info.txt"}')
        if args.write_info_txt:
            info_path = COMMUNITY_DIR / payload['device'] / 'info.txt'
            info_path.write_text(info_yaml, encoding='utf-8')
            print(f'wrote {info_path}')


if __name__ == '__main__':
    main()
