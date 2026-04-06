#!/usr/bin/env python3
"""
Create a side-by-side identity/description comparison artifact for agent review.

Reads:
  01_local_signals.json
  02_device_profile_api.json

Writes:
  02_profile_registry_compare.json

This script is intentionally simple. It does not decide whether web search is
needed. It only presents the key profile and registry fields side by side so
the agent can make that decision consistently.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from batch_devices import list_batch_device_dirs

FIELDS = [
    'name',
    'name_en',
    'manufacturer',
    'description',
    'description_en',
]


def normalize(value: Any) -> str:
    if value is None:
        return ''
    if not isinstance(value, str):
        value = str(value)
    return ' '.join(value.strip().split())


def build_row(field: str, profile: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    profile_value = normalize(profile.get(field, ''))
    registry_value = normalize(registry.get(field, ''))
    return {
        'field': field,
        'profile_value': profile_value,
        'registry_value': registry_value,
        'profile_empty': profile_value == '',
        'registry_empty': registry_value == '',
        'exact_match': profile_value == registry_value and profile_value != '',
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--signals-dir',
        type=Path,
        required=True,
        help='Directory containing per-device run folders with 01_local_signals.json and 02_device_profile_api.json',
    )
    parser.add_argument('--limit', type=int)
    args = parser.parse_args()

    device_dirs = list_batch_device_dirs(args.signals_dir)
    if args.limit is not None:
        device_dirs = device_dirs[:args.limit]

    count = 0
    for device_dir in device_dirs:
        signals_path = device_dir / '01_local_signals.json'
        profile_path = device_dir / '02_device_profile_api.json'
        if not signals_path.exists() or not profile_path.exists():
            continue

        signals = json.loads(signals_path.read_text(encoding='utf-8'))
        profile_doc = json.loads(profile_path.read_text(encoding='utf-8'))
        registry = signals.get('registry', {})
        profile = profile_doc.get('parsed', {})

        comparison_rows = [build_row(field, profile, registry) for field in FIELDS]

        out = {
            'device': signals.get('device', device_dir.name),
            'target_profile_path': str(profile_path.name),
            'editable_profile_fields': FIELDS,
            'comparison_basis': (
                'Side-by-side comparison only. This artifact does not decide whether '
                'web search is needed.'
            ),
            'information_priority': [
                'online search',
                'Pass A driver-derived profile in 02_device_profile_api.json',
                'registry entry in 01_local_signals.json',
            ],
            'profile': {field: normalize(profile.get(field, '')) for field in FIELDS},
            'registry': {field: normalize(registry.get(field, '')) for field in FIELDS},
            'rows': comparison_rows,
        }

        out_path = device_dir / '02_profile_registry_compare.json'
        out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        count += 1

    print(f'wrote comparison artifacts for {count} devices into {args.signals_dir}')


if __name__ == '__main__':
    main()
