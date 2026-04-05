#!/usr/bin/env python3
"""
Pass B: batch-level tag assignment via OpenAI Responses API.

Reads per-device 02_device_profile_api.json (for tag_hints, name, description)
and registry signals (scene, module, tags, category) from 01_local_signals.json.
Loads the full tag list once.  Outputs tag assignments into
03_enriched_payload.json per device.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import urllib.request
from pathlib import Path
from typing import Any


COMMUNITY_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
DEFAULT_BASE_URL = 'https://api.openai.com/v1'
SECRET_ENV_PATH = Path.home() / '.config' / 'unilabos' / 'openai.env'
TAG_CSV_PATH = COMMUNITY_DIR / 'tag 标签列表.csv'
TAG_PROPOSED_PATH = COMMUNITY_DIR / 'tag_additions_proposed.csv'

SYSTEM_PROMPT = """\
You are assigning tags to lab devices using extracted evidence and a provided
tag list.

Rules:
- Each device MUST receive at least 1 tag of each type:
  experimental_step, experimental_domain, experimental_scene, device_template_tag.
- For experimental_step: choose ONLY   from existing tags. Do NOT propose new ones.
- For experimental_domain, experimental_scene, device_template_tag: choose from 
  existing tags first. If no existing tag fits well, 
  you may propose ONE new device_template_tag. A proposed tag must
  be broad enough that multiple real-world devices would fall under it.
- Prefer recall over precision, but do not select obviously unrelated tags.
- Use all evidence: tag_hints, name, description, scene, module path, existing
  tags, category.
- Output JSON only.
"""


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('export '):
            line = line[len('export '):]
        if '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_tag_list() -> list[dict[str, str]]:
    """Load tags from CSV + proposed additions."""
    tags: list[dict[str, str]] = []
    if TAG_CSV_PATH.exists():
        with open(TAG_CSV_PATH, encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                tags.append({
                    'id': row.get('id', '').strip(),
                    'name': row.get('name', '').strip(),
                    'name_en': row.get('name_en', '').strip(),
                    'type': row.get('type', '').strip(),
                })
    if TAG_PROPOSED_PATH.exists():
        with open(TAG_PROPOSED_PATH, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                if row.get('status', '').strip() in ('proposed', 'accepted'):
                    tags.append({
                        'id': row.get('id', '').strip(),
                        'name': row.get('name', '').strip(),
                        'name_en': row.get('name_en', '').strip(),
                        'type': row.get('type', '').strip(),
                    })
    return tags


def build_batch_prompt(devices_data: list[dict[str, Any]],
                       tag_list: list[dict[str, str]]) -> str:
    parts = ['Available tags:']
    for t in tag_list:
        parts.append(f"  [{t['id']}] {t['name']} / {t['name_en']} ({t['type']})")

    parts.append('\n---\nDevices to tag:\n')
    for d in devices_data:
        parts.append(f"Device: {d['device']}")
        parts.append(f"  name: {d.get('name', '')}")
        parts.append(f"  description: {d.get('description_en', '')}")
        parts.append(f"  tag_hints: {d.get('tag_hints', [])}")
        parts.append(f"  category: {d.get('category', [])}")
        parts.append(f"  scene: {d.get('scene', {})}")
        parts.append(f"  module: {d.get('module', '')}")
        parts.append(f"  existing_tags: {d.get('existing_tags', [])}")
        parts.append('')

    return '\n'.join(parts)


def build_response_schema() -> dict[str, Any]:
    tag_obj = {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'id': {'type': 'string'},
            'name': {'type': 'string'},
            'name_en': {'type': 'string'},
            'type': {'type': 'string'},
            'rationale': {'type': 'string'},
        },
        'required': ['id', 'name', 'name_en', 'type', 'rationale'],
    }
    device_result = {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'device': {'type': 'string'},
            'tags': {'type': 'array', 'items': tag_obj},
            'proposed_new_tags': {'type': 'array', 'items': tag_obj},
        },
        'required': ['device', 'tags', 'proposed_new_tags'],
    }
    return {
        'name': 'batch_tag_results',
        'schema': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'devices': {'type': 'array', 'items': device_result},
            },
            'required': ['devices'],
        },
        'strict': True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', default='o4-mini')
    parser.add_argument('--signals-dir', type=Path, required=True)
    parser.add_argument('--reasoning-effort', default='medium')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    load_env_file(SECRET_ENV_PATH)
    api_key = os.environ.get('OPENAI_API_KEY', '').strip()
    base_url = os.environ.get('OPENAI_BASE_URL', DEFAULT_BASE_URL).rstrip('/')
    if not api_key and not args.dry_run:
        raise SystemExit(f'Missing OPENAI_API_KEY (checked env and {SECRET_ENV_PATH})')

    tag_list = load_tag_list()
    print(f'Loaded {len(tag_list)} tags')

    # Collect per-device summaries from 01 + 02
    devices_data: list[dict[str, Any]] = []
    device_dirs = sorted([p for p in args.signals_dir.iterdir() if p.is_dir()])

    for device_dir in device_dirs:
        signals_path = device_dir / '01_local_signals.json'
        profile_path = device_dir / '02_device_profile_api.json'
        if not signals_path.exists() or not profile_path.exists():
            print(f'skip {device_dir.name}: missing 01 or 02')
            continue

        signals = json.loads(signals_path.read_text(encoding='utf-8'))
        profile = json.loads(profile_path.read_text(encoding='utf-8'))
        parsed = profile.get('parsed', {})

        devices_data.append({
            'device': signals['device'],
            'name': parsed.get('name', ''),
            'description_en': parsed.get('description_en', ''),
            'tag_hints': parsed.get('tag_hints', []),
            'category': signals['registry'].get('category', []),
            'scene': signals['registry'].get('scene', {}),
            'module': signals['registry'].get('module', ''),
            'existing_tags': signals['registry'].get('tags', []),
        })

    if not devices_data:
        print('No devices with both 01 and 02 artifacts')
        return

    user_prompt = build_batch_prompt(devices_data, tag_list)
    schema = build_response_schema()

    payload = {
        'model': args.model,
        'reasoning': {'effort': args.reasoning_effort},
        'text': {
            'format': {
                'type': 'json_schema',
                'name': schema['name'],
                'schema': schema['schema'],
                'strict': True,
            },
        },
        'input': [
            {'role': 'system', 'content': [{'type': 'input_text', 'text': SYSTEM_PROMPT}]},
            {'role': 'user', 'content': [{'type': 'input_text', 'text': user_prompt}]},
        ],
    }

    if args.dry_run:
        dry_path = args.signals_dir / '_batch_tag_request.json'
        dry_path.write_text(
            json.dumps({'request': payload}, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )
        print(f'dry-run: wrote request to {dry_path}')
        return

    req = urllib.request.Request(
        f'{base_url}/responses',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )

    with urllib.request.urlopen(req, timeout=300) as resp:
        raw_response = json.loads(resp.read().decode('utf-8'))

    text = raw_response.get('output_text')
    if not text:
        raise RuntimeError('No output_text in batch tag response')
    parsed = json.loads(text)

    # Distribute results to per-device directories
    results_by_device = {d['device']: d for d in parsed.get('devices', [])}
    for device_dir in device_dirs:
        device_name = device_dir.name
        if device_name not in results_by_device:
            continue
        result = results_by_device[device_name]

        # Write batch tag trace
        (device_dir / '_batch_tag_api.json').write_text(
            json.dumps({
                'request_model': args.model,
                'response': raw_response,
                'device_result': result,
            }, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )
        print(f'wrote tag results for {device_name}')


if __name__ == '__main__':
    main()
