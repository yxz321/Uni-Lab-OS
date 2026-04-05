#!/usr/bin/env python3
"""
Collect all proposed_new_tags from batch tag results for agent review.

Scans _batch_tag_api.json files in the outputs directory and prints
a summary of proposed new tags with the devices that triggered them.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


COMMUNITY_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
TAG_PROPOSED_PATH = COMMUNITY_DIR / 'tag_additions_proposed.csv'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--signals-dir', type=Path, required=True)
    parser.add_argument('--append', action='store_true',
                        help='Append accepted tags to tag_additions_proposed.csv')
    args = parser.parse_args()

    # Collect all proposed tags across devices
    proposals: dict[str, dict] = {}  # keyed by name to dedup
    device_map: dict[str, list[str]] = {}  # tag name -> list of devices

    for device_dir in sorted(args.signals_dir.iterdir()):
        if not device_dir.is_dir() or device_dir.name.startswith('_'):
            continue
        batch_tag = device_dir / '_batch_tag_api.json'
        if not batch_tag.exists():
            continue
        data = json.loads(batch_tag.read_text(encoding='utf-8'))
        result = data.get('device_result', {})
        for tag in result.get('proposed_new_tags', []):
            name = tag.get('name', '')
            if not name:
                continue
            proposals[name] = tag
            device_map.setdefault(name, []).append(device_dir.name)

    if not proposals:
        print('No proposed new tags found in this batch.')
        return

    # Print summary for agent review
    print(f'=== {len(proposals)} proposed new tag(s) ===\n')
    for name, tag in sorted(proposals.items()):
        print(f'  id:        {tag.get("id", "")}')
        print(f'  name:      {tag.get("name", "")}')
        print(f'  name_en:   {tag.get("name_en", "")}')
        print(f'  type:      {tag.get("type", "")}')
        print(f'  rationale: {tag.get("rationale", "")}')
        print(f'  devices:   {", ".join(device_map.get(name, []))}')
        print()

    if not args.append:
        print('Run with --append to write accepted tags to tag_additions_proposed.csv')
        return

    # Load existing proposed ids to avoid duplicates
    existing_ids: set[str] = set()
    if TAG_PROPOSED_PATH.exists():
        with open(TAG_PROPOSED_PATH, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                existing_ids.add(row.get('id', '').strip())

    new_rows = []
    for tag in sorted(proposals.values(), key=lambda t: t.get('id', '')):
        if tag.get('id', '') in existing_ids:
            print(f'skip {tag["id"]} {tag["name"]}: already in CSV')
            continue
        new_rows.append(tag)

    if not new_rows:
        print('All proposed tags already exist in CSV.')
        return

    write_header = not TAG_PROPOSED_PATH.exists()
    with open(TAG_PROPOSED_PATH, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'name_en', 'type', 'rationale', 'status'])
        if write_header:
            writer.writeheader()
        for tag in new_rows:
            writer.writerow({
                'id': tag.get('id', ''),
                'name': tag.get('name', ''),
                'name_en': tag.get('name_en', ''),
                'type': tag.get('type', ''),
                'rationale': tag.get('rationale', ''),
                'status': 'proposed',
            })
            print(f'appended: {tag["id"]} {tag["name"]}')


if __name__ == '__main__':
    main()
