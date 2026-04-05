#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections import defaultdict


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--outputs-dir', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()

    model_dirs = sorted([p for p in args.outputs_dir.iterdir() if p.is_dir()])
    devices = set()
    data = {}
    for mdir in model_dirs:
        model = mdir.name
        data[model] = {}
        for p in sorted(mdir.glob('*/semantic.json')):
            device = p.parent.name
            devices.add(device)
            data[model][device] = load_json(p)

    lines = ['# Side-by-Side Semantic Comparison', '']
    for device in sorted(devices):
        lines += [f'## {device}', '']
        lines += ['### Device Description', '']
        for model in sorted(data.keys()):
            item = data[model].get(device)
            if item:
                lines.append(f'- `{model}`: {item.get("description_en", "")}'.rstrip())
        lines.append('')

        action_names = []
        seen = set()
        for model in sorted(data.keys()):
            for action in data[model].get(device, {}).get('actions', []):
                name = action.get('name')
                if name and name not in seen:
                    seen.add(name)
                    action_names.append(name)
        for action_name in action_names:
            lines += [f'### Action: `{action_name}`', '']
            for model in sorted(data.keys()):
                action_map = {a.get('name'): a.get('description_en', '') for a in data[model].get(device, {}).get('actions', [])}
                if action_name in action_map:
                    lines.append(f'- `{model}`: {action_map[action_name]}')
            lines.append('')

        any_tags = False
        for model in sorted(data.keys()):
            if 'selected_tags' in data[model].get(device, {}):
                any_tags = True
                break
        if any_tags:
            lines += ['### Tags', '']
            for model in sorted(data.keys()):
                tags = data[model].get(device, {}).get('selected_tags', [])
                if tags:
                    lines.append(f'- `{model}`: ' + ', '.join(t.get('name_en', t.get('id', '')) for t in tags))
            lines.append('')

    args.out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'wrote {args.out}')


if __name__ == '__main__':
    main()
