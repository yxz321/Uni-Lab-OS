#!/usr/bin/env python3
"""Select the next production batch from sorted device folders."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BATCH_ROOT = Path(__file__).resolve().parent / "batches"


def production_batch_dirs() -> list[Path]:
    if not BATCH_ROOT.exists():
        return []
    return sorted(
        p for p in BATCH_ROOT.iterdir()
        if p.is_dir() and re.fullmatch(r"batch_\d+", p.name)
    )


def processed_devices() -> set[str]:
    done: set[str] = set()
    for batch_dir in production_batch_dirs():
        manifest = batch_dir / "manifest.json"
        report = batch_dir / "report.md"
        if not manifest.exists() or not report.exists():
            continue
        data = json.loads(manifest.read_text(encoding="utf-8"))
        for dev in data.get("devices", []):
            name = dev.get("device")
            if isinstance(name, str):
                done.add(name)
    return done


def all_device_dirs() -> list[str]:
    names = []
    for p in REPO_ROOT.iterdir():
        if not p.is_dir():
            continue
        if p.name == "_info_enrichment_workflow":
            continue
        if (p / "driver.py").exists() and (p / "registry.yaml").exists():
            names.append(p.name)
    return sorted(names)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, default=10, help="Batch size")
    parser.add_argument("--offset", type=int, default=0, help="Skip additional pending devices")
    args = parser.parse_args()

    done = processed_devices()
    pending = [name for name in all_device_dirs() if name not in done]
    selected = pending[args.offset:args.offset + args.size]

    for name in selected:
        print(name)


if __name__ == "__main__":
    main()
