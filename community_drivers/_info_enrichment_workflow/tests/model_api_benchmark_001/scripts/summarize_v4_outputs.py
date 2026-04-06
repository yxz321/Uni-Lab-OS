#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections import defaultdict

import yaml


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def extract_device_entry(doc: dict):
    for k, v in doc.items():
        if k != 'auto_annotation_metadata':
            return k, v
    raise ValueError('No device entry found')


def collect_usage(model_dir: Path):
    totals = defaultdict(int)
    for p in model_dir.glob('*/02_device_profile_api.json'):
        data = load_json(p)
        usage = data.get('usage', {})
        totals['pass_a_input_tokens'] += int(usage.get('input_tokens', 0) or 0)
        totals['pass_a_output_tokens'] += int(usage.get('output_tokens', 0) or 0)
        totals['pass_a_total_tokens'] += int(usage.get('total_tokens', 0) or 0)
    for p in model_dir.glob('*/_batch_tag_api.json'):
        data = load_json(p)
        usage = data.get('usage', {})
        totals['pass_b_input_tokens'] += int(usage.get('input_tokens', 0) or 0)
        totals['pass_b_output_tokens'] += int(usage.get('output_tokens', 0) or 0)
        totals['pass_b_total_tokens'] += int(usage.get('total_tokens', 0) or 0)
    totals['all_total_tokens'] = totals['pass_a_total_tokens'] + totals['pass_b_total_tokens']
    return totals


def infer_model_label(model_dir: Path) -> str:
    for p in sorted(model_dir.glob('*/02_device_profile_api.json')):
        data = load_json(p)
        label = data.get('model')
        if isinstance(label, str) and label.strip():
            return label
    return model_dir.name


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--runs-dir', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--run-names', nargs='*', help='Optional specific run folder names to include')
    args = parser.parse_args()

    model_dirs = sorted([p for p in args.runs_dir.iterdir() if p.is_dir()])
    if args.run_names:
        wanted = set(args.run_names)
        model_dirs = [p for p in model_dirs if p.name in wanted]
    data = {}
    devices = set()

    for mdir in model_dirs:
        model = infer_model_label(mdir)
        usage = collect_usage(mdir)
        data[model] = {'usage': usage, 'devices': {}}
        for info_path in sorted(mdir.glob('*/info.txt')):
            device_dir = info_path.parent
            doc = load_yaml(info_path)
            device_key, entry = extract_device_entry(doc)
            meta = doc.get('auto_annotation_metadata', {})
            devices.add(device_key)
            actions = ((entry.get('class') or {}).get('action_value_mappings') or {})
            data[model]['devices'][device_key] = {
                'name': entry.get('name_en') or entry.get('name') or device_key,
                'description_en': entry.get('description_en', ''),
                'tags': entry.get('tags', []),
                'full_tags': (meta.get('existing_tags', []) or []) + (meta.get('proposed_new_tags', []) or []),
                'actions': {k: ((v or {}).get('schema') or {}).get('description_en', '') for k, v in actions.items()},
            }

    lines = ['# Workflow v4 Benchmark Summary', '']
    lines += ['## Usage', '']
    for model in sorted(data):
        u = data[model]['usage']
        lines.append(f"- `{model}`: Pass A total {u['pass_a_total_tokens']} tokens, Pass B total {u['pass_b_total_tokens']} tokens, combined {u['all_total_tokens']} tokens")
    lines.append('')

    for device in sorted(devices):
        lines += [f'## {device}', '']
        lines += ['### Device Name', '']
        for model in sorted(data):
            item = data[model]['devices'].get(device)
            if item:
                lines.append(f"- `{model}`: {item['name']}")
        lines.append('')

        lines += ['### Device Description', '']
        for model in sorted(data):
            item = data[model]['devices'].get(device)
            if item:
                lines.append(f"- `{model}`: {item['description_en']}")
        lines.append('')

        action_names = []
        seen = set()
        for model in sorted(data):
            for action_name in data[model]['devices'].get(device, {}).get('actions', {}):
                if action_name not in seen:
                    seen.add(action_name)
                    action_names.append(action_name)
        for action_name in action_names:
            lines += [f'### Action: `{action_name}`', '']
            for model in sorted(data):
                desc = data[model]['devices'].get(device, {}).get('actions', {}).get(action_name)
                if desc is not None:
                    lines.append(f"- `{model}`: {desc}")
            lines.append('')

        lines += ['### Tags', '']
        for model in sorted(data):
            item = data[model]['devices'].get(device)
            if item:
                lines.append(f"- `{model}`: {', '.join(item['tags'])}")
        lines.append('')

    args.out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'wrote {args.out}')


if __name__ == '__main__':
    main()
