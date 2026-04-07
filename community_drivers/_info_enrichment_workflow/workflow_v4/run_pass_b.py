#!/usr/bin/env python3
"""Pass B: batch-level tag assignment via Responses API."""
from __future__ import annotations

import argparse
import csv
import json
import os
import socket
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from batch_devices import list_batch_device_dirs
from responses_compat import extract_output_text_compat


COMMUNITY_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_BASE_URL = 'https://api.openai.com/v1'
SECRET_ENV_PATH = Path.home() / '.config' / 'unilabos' / 'openai.env'
TAG_CSV_PATH = COMMUNITY_DIR / 'tag 标签列表.csv'
TAG_PROPOSED_PATH = COMMUNITY_DIR / 'tag_additions_proposed.csv'
API_READ_TIMEOUT_SECONDS = 300
MAX_API_ATTEMPTS = 2
RETRY_BACKOFF_SECONDS = 5

SYSTEM_PROMPT = """\
You are assigning tags to lab devices using extracted evidence and a provided full tag list.

Rules:
- The response MUST follow the requested JSON schema exactly.
- The top-level object must be: {"devices": [ ... ]}.
- Each device result object must contain exactly these keys:
  `device`, `existing_tags`, `proposed_new_tags`.
- Every tag object in both `existing_tags` and `proposed_new_tags` must contain exactly:
  `id`, `name`, `name_en`, `type`, `rationale`.
- The `type` field is mandatory on every tag object and must be one of:
  `experimental_step`, `experimental_domain`, `experimental_scene`, `device_template_tag`.
- The combined set of `existing_tags` and `proposed_new_tags` must contain at least one tag of each required type.
- Prefer existing tags when reasonably relevant.
- Include all relevant tags, not exactly one per type.
- A practical default is roughly 1-4 relevant tags per type when supported.
- For `experimental_step`: choose only from existing tags. Do not propose new ones.
- For `experimental_domain`, `experimental_scene`, and `device_template_tag`:
  choose from existing tags first, but you may propose multiple new tags if the existing list is insufficient.
- Proposed new tags are allowed only for:
  `experimental_domain`, `experimental_scene`, `device_template_tag`.
- A proposed tag must be broad enough that:
  - multiple real-world devices would fall under `device_template_tag`
  - multiple device templates would fall under `experimental_scene`
  - multiple scenes would fall under `experimental_domain`
- Every tag object's `id` must be a string.
- For existing tags, copy the provided tag id as a string.
- For proposed new tags, create a string id like `P-0001`, `P-0002`, etc.
- `name` should be Chinese-preferred and `name_en` should be English.
- Every selected or proposed tag must include a short, device-specific rationale.
- Do not output IDs only. Return full tag objects.
- Do not use bilingual mixed strings inside `name`.
- Prefer recall over precision, but do not select obviously unrelated tags.
- Use only the evidence provided in the device summaries. Do not assume hidden registry priors.
- Output JSON only.
"""


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


def load_tag_list() -> list[dict[str, str]]:
    tags: list[dict[str, str]] = []
    if TAG_CSV_PATH.exists():
        with open(TAG_CSV_PATH, encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                tags.append({
                    'id': row.get('id', '').strip(),
                    'name': row.get('name', '').strip(),
                    'name_en': row.get('name_en', '').strip(),
                    'type': row.get('type', '').strip(),
                })
    if TAG_PROPOSED_PATH.exists():
        with open(TAG_PROPOSED_PATH, encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                if row.get('status', '').strip() in ('proposed', 'accepted'):
                    tags.append({
                        'id': row.get('id', '').strip(),
                        'name': row.get('name', '').strip(),
                        'name_en': row.get('name_en', '').strip(),
                        'type': row.get('type', '').strip(),
                    })
    return tags


def build_batch_prompt(devices_data: list[dict[str, Any]], tag_list: list[dict[str, str]]) -> str:
    parts = ['Available tags:']
    for t in tag_list:
        parts.append(f"  [{t['id']}] {t['name']} / {t['name_en']} ({t['type']})")

    parts.append('\n---\nDevices to tag:\n')
    for d in devices_data:
        parts.append(f"Device: {d['device']}")
        parts.append(f"  name: {d.get('name', '')}")
        parts.append(f"  name_en: {d.get('name_en', '')}")
        parts.append(f"  manufacturer: {d.get('manufacturer', '')}")
        parts.append(f"  description_zh: {d.get('description', '')}")
        parts.append(f"  description_en: {d.get('description_en', '')}")
        parts.append(f"  tag_hints: {d.get('tag_hints', [])}")
        actions = d.get('actions', [])
        if actions:
            parts.append('  actions:')
            for action in actions:
                parts.append(f"    - {action.get('action_name', '')}: {action.get('description_en', '')}")
        parts.append('')

    return '\n'.join(parts)


def build_response_schema() -> dict[str, Any]:
    tag_obj = {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'id': {'type': 'string'},
            'name': {'type': 'string'},
            'name_en': {'type': 'string'},
            'type': {'type': 'string'},
            'rationale': {'type': 'string'},
        },
        'required': ['id', 'name', 'name_en', 'type', 'rationale'],
    }
    device_result = {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'device': {'type': 'string'},
            'existing_tags': {'type': 'array', 'items': tag_obj},
            'proposed_new_tags': {'type': 'array', 'items': tag_obj},
        },
        'required': ['device', 'existing_tags', 'proposed_new_tags'],
    }
    return {
        'name': 'batch_tag_results',
        'schema': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'devices': {'type': 'array', 'items': device_result},
            },
            'required': ['devices'],
        },
        'strict': True,
    }


def validate_parsed_response(parsed: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(parsed, dict):
        raise RuntimeError('Pass B response is not a JSON object')
    devices = parsed.get('devices')
    if not isinstance(devices, list):
        raise RuntimeError('Pass B response missing `devices` list')

    for index, device in enumerate(devices):
        if not isinstance(device, dict):
            raise RuntimeError(f'Pass B devices[{index}] is not an object')
        for field in ('device', 'existing_tags', 'proposed_new_tags'):
            if field not in device:
                raise RuntimeError(f'Pass B devices[{index}] missing `{field}`')
        for key in ('existing_tags', 'proposed_new_tags'):
            value = device[key]
            if not isinstance(value, list):
                raise RuntimeError(f'Pass B devices[{index}].{key} is not a list')
            for tag_index, tag in enumerate(value):
                if not isinstance(tag, dict):
                    raise RuntimeError(f'Pass B devices[{index}].{key}[{tag_index}] is not an object')
                for field in ('id', 'name', 'name_en', 'type', 'rationale'):
                    if field not in tag:
                        raise RuntimeError(f'Pass B devices[{index}].{key}[{tag_index}] missing `{field}`')
    return devices


def write_trace_root(path: Path, payload: dict[str, Any], attempts: list[dict[str, Any]]) -> None:
    trace: dict[str, Any] = {
        'request': payload,
        'attempts': attempts,
    }
    if attempts:
        last_attempt = attempts[-1]
        if 'response' in last_attempt:
            trace['response'] = last_attempt['response']
        if 'output_text' in last_attempt:
            trace['output_text'] = last_attempt['output_text']
        if 'error' in last_attempt:
            trace['error'] = last_attempt['error']
        if 'http_error' in last_attempt:
            trace['http_error'] = last_attempt['http_error']
    path.write_text(json.dumps(trace, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def request_pass_b_with_retry(
    request: urllib.request.Request,
    *,
    base_payload: dict[str, Any],
    trace_root: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    attempts: list[dict[str, Any]] = []

    for attempt in range(1, MAX_API_ATTEMPTS + 1):
        attempt_record: dict[str, Any] = {'attempt': attempt}
        try:
            with urllib.request.urlopen(request, timeout=API_READ_TIMEOUT_SECONDS) as resp:
                raw_response = json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode('utf-8', errors='replace')
            attempt_record['http_error'] = {
                'code': exc.code,
                'reason': exc.reason,
                'body': body,
            }
            attempts.append(attempt_record)
            write_trace_root(trace_root, base_payload, attempts)
            raise SystemExit(f'HTTP {exc.code} during Pass B; wrote {trace_root}')
        except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
            attempt_record['error'] = {
                'type': type(exc).__name__,
                'message': str(exc),
            }
            attempts.append(attempt_record)
            write_trace_root(trace_root, base_payload, attempts)
            if attempt < MAX_API_ATTEMPTS:
                log_progress(
                    'Pass B',
                    f'批量标签请求第 {attempt}/{MAX_API_ATTEMPTS} 次失败（{type(exc).__name__}），{RETRY_BACKOFF_SECONDS}s 后重试',
                )
                time.sleep(RETRY_BACKOFF_SECONDS)
                continue
            raise SystemExit(f'Pass B request failed after {MAX_API_ATTEMPTS} attempts; wrote {trace_root}') from exc

        output_text = extract_output_text_compat(raw_response)
        attempt_record['response'] = raw_response
        attempt_record['output_text'] = output_text

        if not output_text:
            attempt_record['error'] = {
                'type': 'empty_output_text',
                'message': 'No output_text in batch tag response',
            }
            attempts.append(attempt_record)
            write_trace_root(trace_root, base_payload, attempts)
            if attempt < MAX_API_ATTEMPTS:
                log_progress(
                    'Pass B',
                    f'批量标签请求第 {attempt}/{MAX_API_ATTEMPTS} 次返回空输出，{RETRY_BACKOFF_SECONDS}s 后重试',
                )
                time.sleep(RETRY_BACKOFF_SECONDS)
                continue
            raise RuntimeError(f'No output_text in batch tag response after {MAX_API_ATTEMPTS} attempts; wrote {trace_root}')

        try:
            parsed = json.loads(output_text)
            validate_parsed_response(parsed)
        except (json.JSONDecodeError, RuntimeError) as exc:
            attempt_record['error'] = {
                'type': type(exc).__name__,
                'message': str(exc),
            }
            attempts.append(attempt_record)
            write_trace_root(trace_root, base_payload, attempts)
            if attempt < MAX_API_ATTEMPTS:
                log_progress(
                    'Pass B',
                    f'批量标签请求第 {attempt}/{MAX_API_ATTEMPTS} 次返回非结构化结果，{RETRY_BACKOFF_SECONDS}s 后重试',
                )
                time.sleep(RETRY_BACKOFF_SECONDS)
                continue
            raise RuntimeError(f'Pass B response was not valid JSON/schema after {MAX_API_ATTEMPTS} attempts; wrote {trace_root}') from exc

        attempts.append(attempt_record)
        write_trace_root(trace_root, base_payload, attempts)
        return raw_response, attempts

    raise RuntimeError(f'Pass B request exhausted retry budget; wrote {trace_root}')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', default='Vendor2/GPT-5.4')
    parser.add_argument('--signals-dir', type=Path, required=True)
    parser.add_argument('--reasoning-effort', default='medium')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    load_env_file(SECRET_ENV_PATH)
    api_key = os.environ.get('OPENAI_API_KEY', '').strip()
    base_url = os.environ.get('OPENAI_BASE_URL', DEFAULT_BASE_URL).rstrip('/')
    if not api_key and not args.dry_run:
        raise SystemExit(f'Missing OPENAI_API_KEY (checked env and {SECRET_ENV_PATH})')

    tag_list = load_tag_list()
    print(f'Loaded {len(tag_list)} tags')

    devices_data: list[dict[str, Any]] = []
    device_dirs = list_batch_device_dirs(args.signals_dir)
    total = len(device_dirs)
    failures = 0

    for index, device_dir in enumerate(device_dirs, start=1):
        log_progress('Pass B', f'准备设备 {index}/{total}: {device_dir.name}')
        profile_path = device_dir / '02_device_profile_api.json'
        if not profile_path.exists():
            print(f'skip {device_dir.name}: missing 02')
            failures += 1
            log_progress('Pass B', f'跳过设备 {index}/{total}: {device_dir.name}，累计失败 {failures}')
            continue

        profile = json.loads(profile_path.read_text(encoding='utf-8'))
        parsed = profile.get('parsed', {})
        devices_data.append({
            'device': device_dir.name,
            'name': parsed.get('name', ''),
            'name_en': parsed.get('name_en', ''),
            'manufacturer': parsed.get('manufacturer', ''),
            'description': parsed.get('description', ''),
            'description_en': parsed.get('description_en', ''),
            'tag_hints': parsed.get('tag_hints', []),
            'actions': parsed.get('actions', []),
        })
        log_progress('Pass B', f'已收集设备 {index}/{total}: {device_dir.name}，累计失败 {failures}')

    if not devices_data:
        raise SystemExit('No devices with both 01 and 02 artifacts')

    user_prompt = build_batch_prompt(devices_data, tag_list)
    schema = build_response_schema()
    payload = {
        'model': args.model,
        'reasoning': {'effort': args.reasoning_effort},
        'text': {
            'format': {
                'type': 'json_schema',
                'name': schema['name'],
                'schema': schema['schema'],
                'strict': True,
            },
        },
        'input': [
            {'role': 'system', 'content': [{'type': 'input_text', 'text': SYSTEM_PROMPT}]},
            {'role': 'user', 'content': [{'type': 'input_text', 'text': user_prompt}]},
        ],
    }

    trace_root = args.signals_dir / '_batch_tag_request.json'
    if args.dry_run:
        trace_root.write_text(json.dumps({'request': payload}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'dry-run: wrote request to {trace_root}')
        return

    log_progress('Pass B', f'开始批量标签请求，设备数 {len(devices_data)}')
    req = urllib.request.Request(
        f'{base_url}/responses',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
        method='POST',
    )
    raw_response, attempts = request_pass_b_with_retry(req, base_payload=payload, trace_root=trace_root)
    final_output_text = attempts[-1].get('output_text', '')
    parsed = json.loads(final_output_text)
    device_results = validate_parsed_response(parsed)
    results_by_device = {d['device']: d for d in device_results}

    for index, device_dir in enumerate(device_dirs, start=1):
        device_name = device_dir.name
        if device_name not in results_by_device:
            failures += 1
            log_progress('Pass B', f'缺少结果 {index}/{total}: {device_name}，累计失败 {failures}')
            continue
        result = results_by_device[device_name]
        (device_dir / '_batch_tag_api.json').write_text(
            json.dumps({'request_model': args.model, 'reasoning_effort': args.reasoning_effort, 'usage': raw_response.get('usage', {}), 'device_result': result}, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )
        (device_dir / '_batch_tag_api_trace.json').write_text(
            json.dumps({'request': payload, 'response': raw_response, 'device_result': result}, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )
        print(f'wrote tag results for {device_name}')
        log_progress('Pass B', f'完成设备 {index}/{total}: {device_name}，累计失败 {failures}')

    if failures:
        raise SystemExit(f'Pass B failed for {failures} device(s)')


if __name__ == '__main__':
    main()
