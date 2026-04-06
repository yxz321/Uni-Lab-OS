#!/usr/bin/env python3
"""Prepare one production v4 batch under _info_enrichment_workflow/batches/."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


COMMUNITY_DIR = Path(__file__).resolve().parent.parent.parent
WORKFLOW_ROOT = COMMUNITY_DIR / '_info_enrichment_workflow'
BATCH_ROOT = WORKFLOW_ROOT / 'batches'
STATE_FILE = WORKFLOW_ROOT / 'production_state_v4.json'
WORKFLOW_DOC = WORKFLOW_ROOT / 'workflow_v4' / 'workflow_v4.md'
TEMPLATE = WORKFLOW_ROOT / 'workflow_v4' / 'agent_prompt_template_v4.md'
WORKFLOW_VERSION = 'v4'
DEFAULT_BATCH_PREFIX = 'v4_batch'


def list_devices() -> list[str]:
    devices = []
    for path in sorted(COMMUNITY_DIR.iterdir()):
        if not path.is_dir():
            continue
        if path.name == '_info_enrichment_workflow':
            continue
        if (path / 'driver.py').exists() and (path / 'registry.yaml').exists():
            devices.append(path.name)
    return devices


def parse_devices(raw_devices: list[str], devices_file: Path | None) -> list[str]:
    device_names: list[str] = []
    for item in raw_devices:
        for part in item.split(','):
            name = part.strip()
            if name:
                device_names.append(name)
    if devices_file is not None:
        for line in devices_file.read_text(encoding='utf-8').splitlines():
            name = line.strip()
            if name and not name.startswith('#'):
                device_names.append(name)
    deduped: list[str] = []
    seen: set[str] = set()
    for name in device_names:
        if name not in seen:
            deduped.append(name)
            seen.add(name)
    return deduped


def load_state(path: Path) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return {}


def next_batch_name(prefix: str) -> str:
    pattern = re.compile(rf'^{re.escape(prefix)}_(\d+)$')
    numbers = []
    for path in BATCH_ROOT.iterdir() if BATCH_ROOT.exists() else []:
        if not path.is_dir():
            continue
        match = pattern.match(path.name)
        if match:
            numbers.append(int(match.group(1)))
    return f'{prefix}_{(max(numbers) + 1) if numbers else 1:03d}'


def choose_from_cursor(all_devices: list[str], state: dict[str, Any], batch_size: int) -> list[str]:
    next_device = state.get('next_device')
    if next_device in all_devices:
        start = all_devices.index(next_device)
    else:
        start = 0
    return all_devices[start:start + batch_size]


def build_manifest(batch_name: str, batch_dir: Path, devices: list[str], state_path: Path, subagent_model: str, api_model: str, reasoning_effort: str) -> dict[str, Any]:
    manifest_devices = []
    for name in devices:
        folder = COMMUNITY_DIR / name
        artifact_dir = batch_dir / name
        manifest_devices.append({
            'device': name,
            'device_folder': str(folder),
            'info_txt': str(folder / 'info.txt'),
            'artifact_dir': str(artifact_dir),
            'signals_json': str(artifact_dir / '01_local_signals.json'),
            'profile_json': str(artifact_dir / '02_device_profile_api.json'),
            'compare_json': str(artifact_dir / '02_profile_registry_compare.json'),
            'tag_json': str(artifact_dir / '_batch_tag_api.json'),
        })
    return {
        'batch_name': batch_name,
        'workflow_version': WORKFLOW_VERSION,
        'device_count': len(manifest_devices),
        'devices': manifest_devices,
        'paths': {
            'batch_dir': str(batch_dir),
            'devices_file': str(batch_dir / 'devices.txt'),
            'agent_prompt': str(batch_dir / 'agent_prompt.md'),
            'report': str(batch_dir / 'report.md'),
            'state_file': str(state_path),
            'workflow_doc': str(WORKFLOW_DOC),
        },
        'models': {
            'subagent_model': subagent_model,
            'api_model': api_model,
            'reasoning_effort': reasoning_effort,
        },
        'notes': {
            'batch_local_artifacts_live_under_root_batches': True,
            'final_info_txt_writes_to_device_folder': True,
            'main_orchestrator_reads_root_docs_and_state': True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch-name')
    parser.add_argument('--prefix', default=DEFAULT_BATCH_PREFIX)
    parser.add_argument('--batch-size', type=int, default=10)
    parser.add_argument('--devices', nargs='*', default=[])
    parser.add_argument('--devices-file', type=Path)
    parser.add_argument('--state-file', type=Path, default=STATE_FILE)
    parser.add_argument('--subagent-model', default='gpt-5.3-codex')
    parser.add_argument('--api-model', default='Vendor2/GPT-5.4')
    parser.add_argument('--reasoning-effort', default='medium')
    args = parser.parse_args()

    BATCH_ROOT.mkdir(parents=True, exist_ok=True)
    state = load_state(args.state_file)
    explicit_devices = parse_devices(args.devices, args.devices_file)
    if explicit_devices:
        selected = explicit_devices
    else:
        selected = choose_from_cursor(list_devices(), state, args.batch_size)
    if not selected:
        raise SystemExit('No devices selected for batch creation.')

    batch_name = args.batch_name or next_batch_name(args.prefix)
    batch_dir = BATCH_ROOT / batch_name
    batch_dir.mkdir(parents=True, exist_ok=True)
    for device in selected:
        (batch_dir / device).mkdir(parents=True, exist_ok=True)

    devices_path = batch_dir / 'devices.txt'
    manifest_path = batch_dir / 'manifest.json'
    devices_path.write_text('\n'.join(selected) + '\n', encoding='utf-8')
    manifest = build_manifest(batch_name, batch_dir, selected, args.state_file, args.subagent_model, args.api_model, args.reasoning_effort)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print(f'Prepared batch: {batch_name}')
    print(f'Batch directory: {batch_dir}')
    print(f'Devices: {len(selected)}')
    print(f'Manifest: {manifest_path}')


if __name__ == '__main__':
    main()
