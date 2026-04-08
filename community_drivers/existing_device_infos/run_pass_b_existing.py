#!/usr/bin/env python3
"""Prepare and collect refinement batches for existing registry info files."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import yaml


WORK_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = WORK_DIR / 'entries_manifest.json'
BATCH_ROOT = WORK_DIR / 'batches'
TEMPLATE_PATH = WORK_DIR / 'agent_prompt_template_existing.md'
CATEGORY_LIST_PATH = WORK_DIR.parent / 'category_list.csv'
TAG_LIST_PATH = WORK_DIR.parent / 'tag 标签列表.csv'
PROPOSED_TAGS_PATH = WORK_DIR.parent / 'tag_additions_proposed.csv'
DISPATCH_MANIFEST_PATH = WORK_DIR / 'dispatch_manifest.json'
COLLECTION_SUMMARY_PATH = WORK_DIR / 'batch_collection.json'
BATCH_SIZES = [8, 8, 8, 8, 7, 7, 7, 7]


def log_progress(stage: str, message: str) -> None:
    timestamp = time.strftime('%H:%M:%S')
    print(f'[{timestamp}] [{stage}] {message}', flush=True)


def load_entries_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        raise SystemExit(f'Missing manifest: {MANIFEST_PATH}')
    return json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))


def split_entries(records: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    expected = sum(BATCH_SIZES)
    if len(records) != expected:
        raise SystemExit(f'Expected {expected} entries but found {len(records)} in {MANIFEST_PATH}')

    sorted_records = sorted(records, key=lambda item: item['entry_id'])
    batches: list[list[dict[str, Any]]] = []
    cursor = 0
    for size in BATCH_SIZES:
        batches.append(sorted_records[cursor:cursor + size])
        cursor += size
    return batches


def build_agent_prompt(template: str, batch_name: str, batch_dir: Path, entries: list[dict[str, Any]]) -> str:
    entry_ids = '\n'.join(f'- `{entry["entry_id"]}`' for entry in entries)
    assigned = f"""
## Assigned Batch

- batch_name: `{batch_name}`
- batch_dir: `{batch_dir}`
- entries_file: `{batch_dir / 'entries.txt'}`
- manifest: `{batch_dir / 'manifest.json'}`
- report_path: `{batch_dir / 'report.md'}`
- category_list_csv: `{CATEGORY_LIST_PATH}`
- tag_list_csv: `{TAG_LIST_PATH}`
- proposed_tags_csv: `{PROPOSED_TAGS_PATH}`
- assigned_model: `gpt-5.4`

### Assigned Entry IDs

{entry_ids}
"""
    return template.rstrip() + '\n\n' + assigned.lstrip('\n')


def prepare_batches() -> None:
    manifest = load_entries_manifest()
    records = manifest.get('entries', [])
    if not isinstance(records, list):
        raise SystemExit('Manifest `entries` is not a list')

    template = TEMPLATE_PATH.read_text(encoding='utf-8')
    batches = split_entries(records)
    BATCH_ROOT.mkdir(parents=True, exist_ok=True)

    dispatch_batches: list[dict[str, Any]] = []
    for index, entries in enumerate(batches, start=1):
        batch_name = f'batch_{index:03d}'
        batch_dir = BATCH_ROOT / batch_name
        batch_dir.mkdir(parents=True, exist_ok=True)

        entries_file = batch_dir / 'entries.txt'
        entries_file.write_text('\n'.join(entry['entry_id'] for entry in entries) + '\n', encoding='utf-8')

        batch_manifest = {
            'batch_name': batch_name,
            'batch_index': index,
            'entry_count': len(entries),
            'paths': {
                'batch_dir': str(batch_dir),
                'entries_file': str(entries_file),
                'agent_prompt': str(batch_dir / 'agent_prompt.md'),
                'report': str(batch_dir / 'report.md'),
            },
            'references': {
                'entries_manifest': str(MANIFEST_PATH),
                'category_list_csv': str(CATEGORY_LIST_PATH),
                'tag_list_csv': str(TAG_LIST_PATH),
                'proposed_tags_csv': str(PROPOSED_TAGS_PATH),
            },
            'entries': [
                {
                    'entry_id': entry['entry_id'],
                    'registry_key': entry['registry_key'],
                    'yaml_name': entry['yaml_name'],
                    'info_path': entry['output_info_path'],
                    'is_placeholder': entry['is_placeholder'],
                }
                for entry in entries
            ],
        }

        (batch_dir / 'manifest.json').write_text(
            json.dumps(batch_manifest, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )
        (batch_dir / 'agent_prompt.md').write_text(
            build_agent_prompt(template, batch_name, batch_dir, entries),
            encoding='utf-8',
        )
        (batch_dir / 'report.md').write_text(
            f'# {batch_name}\n\nStatus: pending refinement\n',
            encoding='utf-8',
        )

        dispatch_batches.append({
            'batch_name': batch_name,
            'batch_dir': str(batch_dir),
            'entry_count': len(entries),
            'entry_ids': [entry['entry_id'] for entry in entries],
            'agent_prompt': str(batch_dir / 'agent_prompt.md'),
            'report': str(batch_dir / 'report.md'),
        })
        log_progress('Prepare', f'wrote {batch_name} with {len(entries)} entries')

    dispatch_manifest = {
        'working_dir': str(WORK_DIR),
        'batch_sizes': BATCH_SIZES,
        'batch_count': len(dispatch_batches),
        'entry_count': len(records),
        'batches': dispatch_batches,
    }
    DISPATCH_MANIFEST_PATH.write_text(
        json.dumps(dispatch_manifest, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print(f'wrote dispatch manifest {DISPATCH_MANIFEST_PATH}')


def validate_info_file(info_path: Path, registry_key: str) -> bool:
    payload = yaml.safe_load(info_path.read_text(encoding='utf-8'))
    if not isinstance(payload, dict):
        return False
    entry = payload.get(registry_key)
    if not isinstance(entry, dict):
        return False
    if not isinstance(entry.get('category', []), list):
        return False
    if not isinstance(entry.get('tags', []), list):
        return False
    mappings = ((entry.get('class') or {}).get('action_value_mappings')) or {}
    if not isinstance(mappings, dict):
        return False
    return True


def collect_batches() -> None:
    if not DISPATCH_MANIFEST_PATH.exists():
        raise SystemExit(f'Missing dispatch manifest: {DISPATCH_MANIFEST_PATH}')

    dispatch_manifest = json.loads(DISPATCH_MANIFEST_PATH.read_text(encoding='utf-8'))
    batch_summaries: list[dict[str, Any]] = []
    completed = 0
    invalid_files = 0

    for batch in dispatch_manifest.get('batches', []):
        batch_dir = Path(batch['batch_dir'])
        manifest_path = batch_dir / 'manifest.json'
        report_path = batch_dir / 'report.md'
        if not manifest_path.exists():
            raise SystemExit(f'Missing batch manifest: {manifest_path}')

        batch_manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        entry_results: list[dict[str, Any]] = []
        batch_valid = True
        for entry in batch_manifest.get('entries', []):
            info_path = Path(entry['info_path'])
            valid = info_path.exists() and validate_info_file(info_path, entry['registry_key'])
            if not valid:
                invalid_files += 1
                batch_valid = False
            entry_results.append({
                'entry_id': entry['entry_id'],
                'info_path': str(info_path),
                'valid': valid,
            })

        report_exists = report_path.exists()
        report_has_content = report_exists and bool(report_path.read_text(encoding='utf-8').strip())
        if batch_valid and report_has_content:
            completed += 1

        batch_summaries.append({
            'batch_name': batch_manifest['batch_name'],
            'entry_count': batch_manifest['entry_count'],
            'report_exists': report_exists,
            'report_has_content': report_has_content,
            'all_info_files_valid': batch_valid,
            'entries': entry_results,
        })
        log_progress('Collect', f"checked {batch_manifest['batch_name']}: valid={batch_valid} report={report_has_content}")

    summary = {
        'working_dir': str(WORK_DIR),
        'batch_count': len(batch_summaries),
        'completed_batches': completed,
        'invalid_info_files': invalid_files,
        'batches': batch_summaries,
    }
    COLLECTION_SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'wrote collection summary {COLLECTION_SUMMARY_PATH}')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'command',
        nargs='?',
        default='prepare',
        choices=['prepare', 'collect'],
        help='Operation to run (default: prepare)',
    )
    args = parser.parse_args()

    if args.command == 'prepare':
        prepare_batches()
    else:
        collect_batches()


if __name__ == '__main__':
    main()
