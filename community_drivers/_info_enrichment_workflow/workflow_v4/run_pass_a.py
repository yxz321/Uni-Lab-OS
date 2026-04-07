#!/usr/bin/env python3
"""Pass A: per-device semantic profile via Responses API."""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from batch_devices import list_batch_device_dirs
from responses_compat import extract_output_text_compat


DEFAULT_BASE_URL = 'https://api.openai.com/v1'
SECRET_ENV_PATH = Path.home() / '.config' / 'unilabos' / 'openai.env'
API_READ_TIMEOUT_SECONDS = 300

SYSTEM_PROMPT = """\
You are interpreting extracted evidence about a lab-device driver.

Task:
- Infer a concise device name (Chinese) and name_en (English).
- Infer the manufacturer from driver evidence (class name, module path,
  docstrings, comments). If unclear, output empty string.
- Write a concise Chinese description and English description_en of the
  physical device and its lab use. Describe the physical device, not the
  software wrapper, backend, API, or driver implementation.
- Write bilingual descriptions for each action.
- For `actions[].action_name`, use the required action id exactly when one is
  provided in the user message under "Required output action ids".
- Some functions are annotated as status_getter or status_setter. These manage
  device properties. For these, the description should simply be
  "get/set/define <plain-text description of the property>".
- Produce tag_hints: a relevance-sorted list of short keyword phrases the
  device relates to (e.g., "cryogenic cooling", "PID temperature control").
  These will be used downstream for tag assignment. Aim for 3-8 hints.
  Prefer English for tag_hints, but Chinese is acceptable if needed.
- Do not invent capabilities unsupported by the evidence.
- If evidence is weak, stay generic rather than hallucinating.
- `name` and `description` must be natural Chinese.
- `name_en` and `description_en` must be natural English.
- Do not copy English text into the Chinese fields.
- Do not describe the result as a "backend", "driver", or "wrapper" unless the
  evidence truly supports only a software component and no physical device can
  be identified.
- Use module path, class name, action surface, and method comments to infer the
  device family when possible.
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
        'required': ['name', 'name_en', 'manufacturer', 'description', 'description_en', 'actions', 'tag_hints'],
    },
    'strict': True,
}


def log_progress(stage: str, message: str) -> None:
    timestamp = time.strftime('%H:%M:%S')
    print(f'[{timestamp}] [{stage}] {message}', flush=True)


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
        parts.append('\nRequired output action ids:')
        for a in registry['actions']:
            action_id = a.split(' (from ')[0].strip()
            parts.append(f"  {action_id}")

    return '\n'.join(parts)


def process_device(
    device_dir: Path,
    *,
    model: str,
    reasoning_effort: str,
    base_url: str,
    api_key: str,
    dry_run: bool,
) -> bool:
    signals_path = device_dir / '01_local_signals.json'
    if not signals_path.exists():
        print(f'skip {device_dir.name}: no 01_local_signals.json')
        return False

    signals = json.loads(signals_path.read_text(encoding='utf-8'))
    user_prompt = build_user_prompt(signals)

    payload = {
        'model': model,
        'reasoning': {'effort': reasoning_effort},
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
    trace_path = device_dir / '_02_device_profile_api_trace.json'

    if dry_run:
        trace_path.write_text(json.dumps({'request': payload}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'dry-run: wrote request to {trace_path}')
        return False

    req = urllib.request.Request(
        f'{base_url}/responses',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(req, timeout=API_READ_TIMEOUT_SECONDS) as resp:
            raw_response = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        trace_path.write_text(
            json.dumps({'request': payload, 'http_error': {'code': exc.code, 'reason': exc.reason, 'body': body}}, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )
        print(f'ERROR: HTTP {exc.code} for {device_dir.name}')
        return True
    except Exception as exc:
        trace_path.write_text(json.dumps({'request': payload, 'error': str(exc)}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'ERROR: request failed for {device_dir.name}: {exc}')
        return True

    text = extract_output_text_compat(raw_response)
    trace_doc = {'request': payload, 'response': raw_response, 'output_text': text}
    trace_path.write_text(json.dumps(trace_doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if not text:
        print(f'ERROR: no output_text for {device_dir.name}')
        return True

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        print(f'ERROR: invalid JSON for {device_dir.name}: {exc}')
        return True

    usage = raw_response.get('usage', {})
    out_path.write_text(
        json.dumps({'model': model, 'reasoning_effort': reasoning_effort, 'usage': usage, 'parsed': parsed}, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print(f'wrote {out_path}')
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', default='Vendor2/GPT-5.4')
    parser.add_argument('--signals-dir', type=Path, required=True, help='Directory containing per-device 01_local_signals.json')
    parser.add_argument('--reasoning-effort', default='medium')
    parser.add_argument('--max-concurrency', type=int, default=4, help='Maximum number of per-device Pass A requests to run in parallel')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--dry-run', action='store_true', help='Write request payloads only, do not call API')
    args = parser.parse_args()

    load_env_file(SECRET_ENV_PATH)
    api_key = os.environ.get('OPENAI_API_KEY', '').strip()
    base_url = os.environ.get('OPENAI_BASE_URL', DEFAULT_BASE_URL).rstrip('/')
    if not api_key and not args.dry_run:
        raise SystemExit(f'Missing OPENAI_API_KEY (checked env and {SECRET_ENV_PATH})')

    device_dirs = list_batch_device_dirs(args.signals_dir)
    if args.limit is not None:
        device_dirs = device_dirs[:args.limit]

    total = len(device_dirs)
    max_workers = max(1, min(args.max_concurrency, len(device_dirs) or 1))
    failures = 0
    completed = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures: dict[concurrent.futures.Future[bool], Path] = {}
        for index, device_dir in enumerate(device_dirs, start=1):
            log_progress('Pass A', f'开始设备 {index}/{total}: {device_dir.name}')
            future = executor.submit(
                process_device,
                device_dir,
                model=args.model,
                reasoning_effort=args.reasoning_effort,
                base_url=base_url,
                api_key=api_key,
                dry_run=args.dry_run,
            )
            futures[future] = device_dir
        for future in concurrent.futures.as_completed(futures):
            device_dir = futures[future]
            try:
                failed = future.result()
            except Exception as exc:
                failures += 1
                completed += 1
                log_progress('Pass A', f'异常失败 {completed}/{total}: {device_dir.name} ({exc})，累计失败 {failures}')
                continue
            if failed:
                failures += 1
                completed += 1
                log_progress('Pass A', f'失败 {completed}/{total}: {device_dir.name}，累计失败 {failures}')
            else:
                completed += 1
                log_progress('Pass A', f'完成 {completed}/{total}: {device_dir.name}，累计失败 {failures}')

    if failures:
        raise SystemExit(f'Pass A failed for {failures} device(s)')


if __name__ == '__main__':
    main()
