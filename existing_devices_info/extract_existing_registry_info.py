#!/usr/bin/env python3
"""Extract, validate, materialize, and aggregate non-community registry entries."""
from __future__ import annotations

import argparse
import csv
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


WORK_DIR = Path(__file__).resolve().parent
COMMUNITY_DIR = WORK_DIR.parent
REGISTRY_DIR = COMMUNITY_DIR.parent / 'unilabos' / 'registry' / 'devices'
MANIFEST_PATH = WORK_DIR / 'entries_manifest.json'
AGGREGATE_CSV_PATH = COMMUNITY_DIR / '_aggregate_device_info_existing.csv'
TAG_CSV_PATH = COMMUNITY_DIR / 'tag 标签列表.csv'
TAG_PROPOSED_PATH = COMMUNITY_DIR / 'tag_additions_proposed.csv'

CSV_FIELDS = [
    'name',
    'name_en',
    'device',
    'registry_key',
    'action_count',
    'function_count',
    'atom_actions',
    'description',
    'description_en',
    'categories',
    'tags',
]

TAG_FIELDS = {'id', 'name', 'name_en', 'type', 'rationale'}
ALLOWED_TAG_TYPES = {
    'experimental_step',
    'experimental_domain',
    'experimental_scene',
    'device_template_tag',
}
PROPOSED_ALLOWED_TAG_TYPES = {
    'experimental_domain',
    'experimental_scene',
    'device_template_tag',
}
REQUIRED_TAG_TYPES = {
    'experimental_step',
    'experimental_domain',
    'experimental_scene',
    'device_template_tag',
}


def normalize_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if value is None:
        return ''
    return str(value).strip()


def normalize_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    items: list[str] = []
    for item in value:
        text = normalize_text(item)
        if text:
            items.append(text)
    return items


@lru_cache(maxsize=1)
def load_available_tag_ids() -> set[str]:
    tag_ids: set[str] = set()
    if TAG_CSV_PATH.exists():
        with open(TAG_CSV_PATH, encoding='utf-8-sig') as handle:
            for row in csv.DictReader(handle):
                tag_id = normalize_text(row.get('id'))
                if tag_id:
                    tag_ids.add(tag_id)
    if TAG_PROPOSED_PATH.exists():
        with open(TAG_PROPOSED_PATH, encoding='utf-8-sig') as handle:
            for row in csv.DictReader(handle):
                if normalize_text(row.get('status')) not in {'proposed', 'accepted'}:
                    continue
                tag_id = normalize_text(row.get('id'))
                if tag_id:
                    tag_ids.add(tag_id)
    return tag_ids


def discover_registry_files() -> list[Path]:
    return sorted(path for path in REGISTRY_DIR.glob('*.yaml') if not path.name.startswith('community'))


def iter_entry_specs(registry_path: Path) -> list[dict[str, Any]]:
    raw = yaml.safe_load(registry_path.read_text(encoding='utf-8'))
    yaml_stem = registry_path.stem

    if registry_path.name == 'balance.yaml' and raw == {}:
        return [{
            'yaml_name': registry_path.name,
            'yaml_stem': yaml_stem,
            'registry_key': 'balance',
            'entry': {},
            'is_placeholder': True,
        }]

    if not isinstance(raw, dict):
        raise RuntimeError(f'{registry_path.name} does not contain a mapping root')

    specs: list[dict[str, Any]] = []
    for registry_key, entry in raw.items():
        if not isinstance(entry, dict):
            continue
        specs.append({
            'yaml_name': registry_path.name,
            'yaml_stem': yaml_stem,
            'registry_key': str(registry_key),
            'entry': entry,
            'is_placeholder': False,
        })
    return specs


def extract_action_value_mappings(entry: dict[str, Any]) -> dict[str, Any]:
    raw_mappings = ((entry.get('class') or {}).get('action_value_mappings')) or {}
    if not isinstance(raw_mappings, dict):
        raw_mappings = {}

    mappings: dict[str, Any] = {}
    for action_name in sorted(str(name) for name in raw_mappings.keys()):
        raw_spec = raw_mappings.get(action_name) or {}
        raw_schema = raw_spec.get('schema') if isinstance(raw_spec, dict) else {}
        if not isinstance(raw_schema, dict):
            raw_schema = {}
        mappings[action_name] = {
            'schema': {
                'description': normalize_text(raw_schema.get('description')),
            },
        }
    return mappings


def build_info_payload(registry_key: str, entry: dict[str, Any]) -> dict[str, Any]:
    return {
        registry_key: {
            'name': normalize_text(entry.get('name')),
            'category': [],
            'tags': [],
            'existing_tags': [],
            'proposed_new_tags': [],
            'description': normalize_text(entry.get('description')),
            'class': {
                'action_value_mappings': extract_action_value_mappings(entry),
            },
        },
    }


def build_manifest_record(spec: dict[str, Any], info_path: Path) -> dict[str, Any]:
    payload = build_info_payload(spec['registry_key'], spec['entry'])
    action_mappings = payload[spec['registry_key']]['class']['action_value_mappings']
    action_names = sorted(action_mappings.keys())
    return {
        'entry_id': f"{spec['yaml_stem']}.{spec['registry_key']}",
        'yaml_name': spec['yaml_name'],
        'yaml_stem': spec['yaml_stem'],
        'registry_key': spec['registry_key'],
        'source_registry_path': str(REGISTRY_DIR / spec['yaml_name']),
        'output_info_path': str(info_path),
        'is_placeholder': bool(spec['is_placeholder']),
        'action_count': len(action_names),
        'action_names': action_names,
    }


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        yaml.dump(payload, allow_unicode=True, default_flow_style=False, sort_keys=False),
        encoding='utf-8',
    )


def run_extract() -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, Any]] = []
    registry_files = discover_registry_files()
    for registry_path in registry_files:
        specs = iter_entry_specs(registry_path)
        for spec in specs:
            entry_id = f"{spec['yaml_stem']}.{spec['registry_key']}"
            info_path = WORK_DIR / f'{entry_id}_info.txt'
            payload = build_info_payload(spec['registry_key'], spec['entry'])
            write_yaml(info_path, payload)
            records.append(build_manifest_record(spec, info_path))

    records.sort(key=lambda item: item['entry_id'])
    manifest = {
        'source_registry_dir': str(REGISTRY_DIR),
        'working_dir': str(WORK_DIR),
        'registry_file_count': len(registry_files),
        'entry_count': len(records),
        'entries': records,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'wrote manifest {MANIFEST_PATH}')
    print(f'extracted {len(records)} entry files from {len(registry_files)} registry YAML files')


def load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        raise SystemExit(f'Missing manifest: {MANIFEST_PATH}')
    return json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))


def load_info_entry(record: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    info_path = Path(record['output_info_path'])
    if not info_path.exists():
        raise RuntimeError(f'missing info file: {info_path}')
    payload = yaml.safe_load(info_path.read_text(encoding='utf-8'))
    if not isinstance(payload, dict):
        raise RuntimeError(f'info file is not a mapping: {info_path}')

    registry_key = record['registry_key']
    entry = payload.get(registry_key)
    if not isinstance(entry, dict):
        raise RuntimeError(f'missing top-level key `{registry_key}` in {info_path.name}')
    return payload, entry


def collect_structured_tags(entry: dict[str, Any]) -> list[dict[str, str]]:
    combined: list[dict[str, str]] = []
    for field_name in ('existing_tags', 'proposed_new_tags'):
        values = entry.get(field_name, [])
        if not isinstance(values, list):
            continue
        for value in values:
            if isinstance(value, dict):
                combined.append(value)
    return combined


def materialized_names(entry: dict[str, Any]) -> tuple[list[str], list[str]]:
    all_tags = collect_structured_tags(entry)

    tags: list[str] = []
    categories: list[str] = []
    seen_tags: set[str] = set()
    seen_categories: set[str] = set()

    for tag in all_tags:
        name = normalize_text(tag.get('name'))
        tag_type = normalize_text(tag.get('type'))
        if name and name not in seen_tags:
            seen_tags.add(name)
            tags.append(name)
        if tag_type == 'device_template_tag' and name and name not in seen_categories:
            seen_categories.add(name)
            categories.append(name)

    return tags, categories


def materialize_entry(entry: dict[str, Any]) -> None:
    tags, categories = materialized_names(entry)
    entry['tags'] = tags
    entry['category'] = categories


def write_materialized_record(record: dict[str, Any]) -> None:
    info_path = Path(record['output_info_path'])
    payload, entry = load_info_entry(record)
    materialize_entry(entry)
    write_yaml(info_path, payload)


def validate_tag_object(
    tag: Any,
    *,
    section_name: str,
    tag_index: int,
    available_tag_ids: set[str],
) -> str:
    if not isinstance(tag, dict):
        raise RuntimeError(f'{section_name}[{tag_index}] must be an object')
    if set(tag.keys()) != TAG_FIELDS:
        raise RuntimeError(
            f'{section_name}[{tag_index}] must contain exactly {sorted(TAG_FIELDS)}, got {sorted(tag.keys())}'
        )

    values = {field: normalize_text(tag.get(field)) for field in TAG_FIELDS}
    for field, value in values.items():
        if not value:
            raise RuntimeError(f'{section_name}[{tag_index}].{field} must be a non-empty string')

    tag_type = values['type']
    if tag_type not in ALLOWED_TAG_TYPES:
        raise RuntimeError(f'{section_name}[{tag_index}].type `{tag_type}` is not allowed')

    if section_name == 'existing_tags':
        if values['id'] not in available_tag_ids:
            raise RuntimeError(f'{section_name}[{tag_index}].id `{values["id"]}` is not in the available tag catalog')
    else:
        if tag_type not in PROPOSED_ALLOWED_TAG_TYPES:
            raise RuntimeError(
                f'{section_name}[{tag_index}] must not propose type `{tag_type}`; '
                f'allowed: {sorted(PROPOSED_ALLOWED_TAG_TYPES)}'
            )
        if not values['id'].startswith('P-'):
            raise RuntimeError(f'{section_name}[{tag_index}].id `{values["id"]}` must start with `P-`')
        if values['id'] in available_tag_ids:
            raise RuntimeError(f'{section_name}[{tag_index}].id `{values["id"]}` already exists in the tag catalog')

    return tag_type


def validate_record(record: dict[str, Any], *, require_materialized: bool = True) -> None:
    _, entry = load_info_entry(record)
    available_tag_ids = load_available_tag_ids()

    if not isinstance(entry.get('name', ''), str):
        raise RuntimeError(f"{record['entry_id']}: `name` must be a string")
    if not isinstance(entry.get('description', ''), str):
        raise RuntimeError(f"{record['entry_id']}: `description` must be a string")

    existing_tags = entry.get('existing_tags', [])
    if not isinstance(existing_tags, list):
        raise RuntimeError(f"{record['entry_id']}: `existing_tags` must be a list")

    proposed_new_tags = entry.get('proposed_new_tags', [])
    if not isinstance(proposed_new_tags, list):
        raise RuntimeError(f"{record['entry_id']}: `proposed_new_tags` must be a list")

    covered_types: set[str] = set()
    for tag_index, tag in enumerate(existing_tags):
        covered_types.add(
            validate_tag_object(
                tag,
                section_name='existing_tags',
                tag_index=tag_index,
                available_tag_ids=available_tag_ids,
            )
        )
    for tag_index, tag in enumerate(proposed_new_tags):
        covered_types.add(
            validate_tag_object(
                tag,
                section_name='proposed_new_tags',
                tag_index=tag_index,
                available_tag_ids=available_tag_ids,
            )
        )

    missing_types = sorted(REQUIRED_TAG_TYPES - covered_types)
    if missing_types:
        raise RuntimeError(
            f"{record['entry_id']}: combined existing/proposed tags must cover all required types, "
            f'missing {missing_types}'
        )

    category = entry.get('category', [])
    if not isinstance(category, list):
        raise RuntimeError(f"{record['entry_id']}: `category` must be a list")

    tags = entry.get('tags', [])
    if not isinstance(tags, list):
        raise RuntimeError(f"{record['entry_id']}: `tags` must be a list")

    cls = entry.get('class', {})
    if not isinstance(cls, dict):
        raise RuntimeError(f"{record['entry_id']}: `class` must be a mapping")

    action_value_mappings = cls.get('action_value_mappings', {})
    if not isinstance(action_value_mappings, dict):
        raise RuntimeError(f"{record['entry_id']}: `class.action_value_mappings` must be a mapping")

    for action_name, action_spec in action_value_mappings.items():
        if not isinstance(action_spec, dict):
            raise RuntimeError(f"{record['entry_id']}: action `{action_name}` must be a mapping")
        schema = action_spec.get('schema', {})
        if not isinstance(schema, dict):
            raise RuntimeError(f"{record['entry_id']}: action `{action_name}` schema must be a mapping")
        if 'description' not in schema or not isinstance(schema.get('description'), str):
            raise RuntimeError(f"{record['entry_id']}: action `{action_name}` missing string schema.description")

    if require_materialized:
        expected_tags, expected_categories = materialized_names(entry)
        if tags != expected_tags:
            raise RuntimeError(
                f"{record['entry_id']}: `tags` must equal the ordered names from existing_tags + proposed_new_tags"
            )
        if category != expected_categories:
            raise RuntimeError(
                f"{record['entry_id']}: `category` must equal the ordered device_template_tag names "
                f'from existing_tags + proposed_new_tags'
            )


def run_validate() -> None:
    manifest = load_manifest()
    records = manifest.get('entries', [])
    if not isinstance(records, list):
        raise SystemExit('Manifest `entries` is not a list')

    for record in records:
        validate_record(record)

    print(f'validated {len(records)} info files')


def build_csv_row(record: dict[str, Any]) -> dict[str, Any]:
    _, entry = load_info_entry(record)
    tags, categories = materialized_names(entry)

    return {
        'name': entry.get('name', ''),
        'name_en': '',
        'device': record['entry_id'],
        'registry_key': record['registry_key'],
        'action_count': record.get('action_count', 0),
        'function_count': '',
        'atom_actions': '|'.join(record.get('action_names', [])),
        'description': entry.get('description', ''),
        'description_en': '',
        'categories': '|'.join(categories if isinstance(categories, list) else []),
        'tags': '|'.join(tags if isinstance(tags, list) else []),
    }


def run_aggregate() -> None:
    manifest = load_manifest()
    records = manifest.get('entries', [])
    if not isinstance(records, list):
        raise SystemExit('Manifest `entries` is not a list')

    for record in records:
        validate_record(record)

    with open(AGGREGATE_CSV_PATH, 'w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for record in sorted(records, key=lambda item: item['entry_id']):
            writer.writerow(build_csv_row(record))

    print(f'wrote aggregate CSV {AGGREGATE_CSV_PATH}')
    print(f'aggregated {len(records)} rows')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'command',
        nargs='?',
        default='extract',
        choices=['extract', 'validate', 'aggregate'],
        help='Operation to run (default: extract)',
    )
    args = parser.parse_args()

    if args.command == 'extract':
        run_extract()
    elif args.command == 'validate':
        run_validate()
    else:
        run_aggregate()


if __name__ == '__main__':
    main()
