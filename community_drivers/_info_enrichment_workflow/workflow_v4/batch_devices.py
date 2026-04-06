#!/usr/bin/env python3
"""Helpers for resolving explicit batch device directories."""
from __future__ import annotations

import json
from pathlib import Path


def _load_devices_from_text(devices_file: Path) -> list[str]:
    devices: list[str] = []
    for raw_line in devices_file.read_text(encoding='utf-8').splitlines():
        name = raw_line.strip()
        if name and not name.startswith('#'):
            devices.append(name)
    return devices


def _load_devices_from_manifest(manifest_file: Path) -> list[str]:
    manifest = json.loads(manifest_file.read_text(encoding='utf-8'))
    devices = manifest.get('devices', [])
    return [
        str(item.get('device', '')).strip()
        for item in devices
        if isinstance(item, dict) and str(item.get('device', '')).strip()
    ]


def list_batch_device_dirs(batch_dir: Path) -> list[Path]:
    devices_file = batch_dir / 'devices.txt'
    manifest_file = batch_dir / 'manifest.json'

    device_names: list[str] | None = None
    if devices_file.exists():
        device_names = _load_devices_from_text(devices_file)
    elif manifest_file.exists():
        device_names = _load_devices_from_manifest(manifest_file)

    if device_names is None:
        return sorted([path for path in batch_dir.iterdir() if path.is_dir()])

    device_dirs: list[Path] = []
    missing: list[str] = []
    for name in device_names:
        path = batch_dir / name
        if path.is_dir():
            device_dirs.append(path)
        else:
            missing.append(name)

    if missing:
        missing_text = ', '.join(missing)
        raise FileNotFoundError(f'Missing batch device directories listed in batch metadata: {missing_text}')

    return device_dirs
