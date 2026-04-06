#!/usr/bin/env python3
"""Collect and optionally append proposed tags from one production batch."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


COMMUNITY_DIR = Path(__file__).resolve().parent.parent.parent
TAG_PROPOSED_PATH = COMMUNITY_DIR / 'tag_additions_proposed.csv'
FIELDNAMES = ['id', 'name', 'name_en', 'type', 'rationale', 'status']


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--signals-dir', type=Path, required=True)
    parser.add_argument('--append', action='store_true', help='Append proposed tags to tag_additions_proposed.csv')
    args = parser.parse_args()

    proposals: list[tuple[str, dict]] = []
    for device_dir in sorted(args.signals_dir.iterdir()):
        if not device_dir.is_dir() or device_dir.name.startswith('_'):
            continue
        batch_tag = device_dir / '_batch_tag_api.json'
        if not batch_tag.exists():
            continue
        data = json.loads(batch_tag.read_text(encoding='utf-8'))
        result = data.get('device_result', {})
        for tag in result.get('proposed_new_tags', []):
            if isinstance(tag, dict):
                proposals.append((device_dir.name, tag))

    if not proposals:
        print('No proposed new tags found in this batch.')
        return

    print(f'=== {len(proposals)} proposed new tag row(s) ===\n')
    for device_name, tag in proposals:
        print(f'device:    {device_name}')
        print(f"  id:        {tag.get('id', '')}")
        print(f"  name:      {tag.get('name', '')}")
        print(f"  name_en:   {tag.get('name_en', '')}")
        print(f"  type:      {tag.get('type', '')}")
        print(f"  rationale: {tag.get('rationale', '')}")
        print()

    if not args.append:
        print('Run with --append to write proposed tags to tag_additions_proposed.csv')
        return

    write_header = not TAG_PROPOSED_PATH.exists() or TAG_PROPOSED_PATH.stat().st_size == 0
    with open(TAG_PROPOSED_PATH, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        for _, tag in proposals:
            writer.writerow({
                'id': tag.get('id', ''),
                'name': tag.get('name', ''),
                'name_en': tag.get('name_en', ''),
                'type': tag.get('type', ''),
                'rationale': tag.get('rationale', ''),
                'status': 'proposed',
            })
    print(f'appended {len(proposals)} row(s) to {TAG_PROPOSED_PATH}')


if __name__ == '__main__':
    main()
