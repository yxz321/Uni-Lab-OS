#!/usr/bin/env python3
"""
Pass A: per-device semantic profile via OpenAI Responses API.

Reads 01_local_signals.json (driver section only — no unreliable registry
fields), sends to the API with function-type hints, writes
02_device_profile_api.json with raw request/response and parsed result.
"""
from __future__ import annotations

import argparse
import json
import os
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = 'https://api.openai.com/v1'
SECRET_ENV_PATH = Path.home() / '.config' / 'unilabos' / 'openai.env'

SYSTEM_PROMPT = """\
You are interpreting extracted evidence about a lab-device driver.

Task:
- Infer a concise device name (Chinese) and name_en (English).
- Infer the manufacturer from driver evidence (class name, module path,
  docstrings, comments). If unclear, output empty string.
- Write a concise Chinese description and English description_en of the
  physical device and its lab use. Describe the device, not the software.
- Write bilingual descriptions for each action.
- Some functions are annotated as status_getter or status_setter. These manage
  device properties. For these, the description should simply be
  "get/set/define <plain-text description of the property>".
- Produce tag_hints: a relevance-sorted list of short keyword phrases the
  device relates to (e.g., "cryogenic cooling", "PID temperature control").
  These will be used downstream for tag assignment. Aim for 3-8 hints.
- Do not invent capabilities unsupported by the evidence.
- If evidence is weak, stay generic rather than hallucinating.
- Output JSON only.
"""

RESPONSE_SCHEMA: dict[str, Any] = {
    'name': 'device_profile',
    'schema': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'name': {'type': 'string', 'description': 'Chinese device name'},
            'name_en': {'type': 'string', 'description': 'English device name'},
            'manufacturer': {'type': 'string'},
            'description': {'type': 'string', 'description': 'Chinese description'},
            'description_en': {'type': 'string', 'description': 'English description'},
            'actions': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'additionalProperties': False,
                    'properties': {
                        'action_name': {'type': 'string'},
                        'description': {'type': 'string', 'description': 'Chinese'},
                        'description_en': {'type': 'string', 'description': 'English'},
                    },
                    'required': ['action_name', 'description', 'description_en'],
                },
            },
            'tag_hints': {
                'type': 'array',
                'items': {'type': 'string'},
                'description': 'Relevance-sorted keyword phrases for downstream tagging',
            },
        },
        'required': ['name', 'name_en', 'manufacturer', 'description',
                      'description_en', 'actions', 'tag_hints'],
    },
    'strict': True,
}


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


def build_user_prompt(signals: dict[str, Any]) -> str:
    """Build the user prompt from driver section of 01_local_signals.json.

    Only includes driver evidence and registry action list (reliable).
    Excludes unreliable registry fields (name, description, manufacturer, model).
    """
    driver = signals['driver']
    registry = signals['registry']

    parts = [f"Device folder: {signals['device']}"]

    if driver.get('module_docstring'):
        parts.append(f"\nModule docstring:\n{driver['module_docstring']}")

    parts.append(f"\nModule path: {registry.get('module', '')}")

    for cls in driver.get('all_classes', []):
        label = '(focal)' if cls.get('is_focal') else ''
        parts.append(f"\nClass: {cls['name']} {label}")
        parts.append(f"  Bases: {cls.get('bases', [])}")
        if cls.get('docstring'):
            parts.append(f"  Docstring: {cls['docstring']}")

    if driver.get('focal_methods'):
        parts.append('\nFocal class methods:')
        for m in driver['focal_methods']:
            parts.append(f"  [{m['function_type']}] {m['function']}")
            if m.get('comments'):
                for c in m['comments']:
                    preview = c[:200] + '...' if len(c) > 200 else c
                    parts.append(f"    comment: {preview}")

    if registry.get('actions'):
        parts.append('\nRegistry actions:')
        for a in registry['actions']:
            parts.append(f"  {a}")

    return '\n'.join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', default='o4-mini')
    parser.add_argument('--signals-dir', type=Path, required=True,
                        help='Directory containing per-device 01_local_signals.json')
    parser.add_argument('--reasoning-effort', default='medium')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--dry-run', action='store_true',
                        help='Write request payloads only, do not call API')
    args = parser.parse_args()

    load_env_file(SECRET_ENV_PATH)
    api_key = os.environ.get('OPENAI_API_KEY', '').strip()
    base_url = os.environ.get('OPENAI_BASE_URL', DEFAULT_BASE_URL).rstrip('/')
    if not api_key and not args.dry_run:
        raise SystemExit(f'Missing OPENAI_API_KEY (checked env and {SECRET_ENV_PATH})')

    device_dirs = sorted([p for p in args.signals_dir.iterdir() if p.is_dir()])
    if args.limit is not None:
        device_dirs = device_dirs[:args.limit]

    for device_dir in device_dirs:
        signals_path = device_dir / '01_local_signals.json'
        if not signals_path.exists():
            print(f'skip {device_dir.name}: no 01_local_signals.json')
            continue

        signals = json.loads(signals_path.read_text(encoding='utf-8'))
        user_prompt = build_user_prompt(signals)

        payload = {
            'model': args.model,
            'reasoning': {'effort': args.reasoning_effort},
            'text': {
                'format': {
                    'type': 'json_schema',
                    'name': RESPONSE_SCHEMA['name'],
                    'schema': RESPONSE_SCHEMA['schema'],
                    'strict': True,
                },
            },
            'input': [
                {'role': 'system', 'content': [{'type': 'input_text', 'text': SYSTEM_PROMPT}]},
                {'role': 'user', 'content': [{'type': 'input_text', 'text': user_prompt}]},
            ],
        }

        out_path = device_dir / '02_device_profile_api.json'

        if args.dry_run:
            out_path.write_text(
                json.dumps({'request': payload}, ensure_ascii=False, indent=2) + '\n',
                encoding='utf-8',
            )
            print(f'dry-run: wrote request to {out_path}')
            continue

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
            raw_response = json.loads(resp.read().decode('utf-8'))

        text = raw_response.get('output_text')
        if not text:
            print(f'ERROR: no output_text for {device_dir.name}')
            continue
        parsed = json.loads(text)

        out_path.write_text(
            json.dumps({
                'request': payload,
                'response': raw_response,
                'parsed': parsed,
            }, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )
        print(f'wrote {out_path}')


if __name__ == '__main__':
    main()
