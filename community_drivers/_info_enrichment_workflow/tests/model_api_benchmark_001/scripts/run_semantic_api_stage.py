#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import urllib.request
from pathlib import Path

from responses_compat import extract_output_text_compat


DEFAULT_BASE_URL = 'https://api.openai.com/v1'
SECRET_ENV_PATH = Path.home() / '.config' / 'unilabos' / 'openai.env'


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True)
    parser.add_argument('--materials-dir', type=Path, required=True)
    parser.add_argument('--outputs-dir', type=Path, required=True)
    parser.add_argument('--system-prompt', type=Path, required=True)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--reasoning-effort', default='medium')
    args = parser.parse_args()

    load_env_file(SECRET_ENV_PATH)
    api_key = os.environ.get('OPENAI_API_KEY', '').strip()
    base_url = os.environ.get('OPENAI_BASE_URL', DEFAULT_BASE_URL).rstrip('/')
    if not api_key:
        raise SystemExit(f'Missing OPENAI_API_KEY in {SECRET_ENV_PATH}')

    schema = {
        'name': 'semantic_output',
        'schema': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'device': {'type': 'string'},
                'description_en': {'type': 'string'},
                'actions': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'additionalProperties': False,
                        'properties': {
                            'name': {'type': 'string'},
                            'description_en': {'type': 'string'},
                        },
                        'required': ['name', 'description_en'],
                    },
                },
            },
            'required': ['device', 'description_en', 'actions'],
        },
        'strict': True,
    }

    system_prompt = args.system_prompt.read_text(encoding='utf-8')
    device_dirs = sorted([p for p in args.materials_dir.iterdir() if p.is_dir()])
    if args.limit is not None:
        device_dirs = device_dirs[:args.limit]

    for device_dir in device_dirs:
        device = device_dir.name
        info_raw = (device_dir / 'info_raw.txt').read_text(encoding='utf-8')
        out_dir = args.outputs_dir / args.model / device
        out_dir.mkdir(parents=True, exist_ok=True)

        payload = {
            'model': args.model,
            'reasoning': {'effort': args.reasoning_effort},
            'text': {'format': {'type': 'json_schema', 'name': schema['name'], 'schema': schema['schema'], 'strict': True}},
            'input': [
                {'role': 'system', 'content': [{'type': 'input_text', 'text': system_prompt}]},
                {'role': 'user', 'content': [{'type': 'input_text', 'text': info_raw}]},
            ],
        }

        req = urllib.request.Request(
            f'{base_url}/responses',
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
            method='POST',
        )

        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = json.loads(resp.read().decode('utf-8'))

        (out_dir / 'response_raw.json').write_text(json.dumps(raw, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        text = extract_output_text_compat(raw)
        if not text:
            raise RuntimeError(f'No output_text for {device} using {args.model}')
        parsed = json.loads(text)
        (out_dir / 'semantic.json').write_text(json.dumps(parsed, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'wrote {out_dir / "semantic.json"}')


if __name__ == '__main__':
    main()
