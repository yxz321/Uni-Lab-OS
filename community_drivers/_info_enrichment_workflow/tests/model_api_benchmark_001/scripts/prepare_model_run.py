#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATERIALS = ROOT / 'materials'
RUNS = ROOT / 'runs'


def sanitize_model_name(model: str) -> str:
    return re.sub(r'[^A-Za-z0-9._-]+', '__', model).strip('_') or 'model_run'


def main() -> None:
    parser = argparse.ArgumentParser(description='Seed a model-specific run folder from materials/')
    parser.add_argument('--model', required=True)
    parser.add_argument('--run-name', help='Optional filesystem-safe run folder name; defaults to sanitized model id')
    parser.add_argument('--clear', action='store_true', help='Delete existing model run folder before seeding')
    args = parser.parse_args()

    run_name = args.run_name or sanitize_model_name(args.model)
    run_root = RUNS / run_name
    if args.clear and run_root.exists():
        shutil.rmtree(run_root)
    run_root.mkdir(parents=True, exist_ok=True)

    count = 0
    for device_dir in sorted(MATERIALS.iterdir()):
        if not device_dir.is_dir():
            continue
        src = device_dir / '01_local_signals.json'
        if not src.exists():
            continue
        dst_dir = run_root / device_dir.name
        dst_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst_dir / '01_local_signals.json')
        count += 1

    print(f'seeded {count} devices into {run_root} for model {args.model}')


if __name__ == '__main__':
    main()
