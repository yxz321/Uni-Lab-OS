#!/usr/bin/env python3
"""Aggregate device information from registry.yaml, driver.py, and info.txt
into a single CSV (UTF-8 with BOM for Excel / multi-language compatibility).

Usage:
    python _aggregate_device_info.py                    # all devices → _aggregate_device_info_output.csv
    python _aggregate_device_info.py pump camera        # specific devices
    python _aggregate_device_info.py --test             # test on a few devices (letter < u)
    python _aggregate_device_info.py --stdout           # write to stdout instead of file
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from typing import Any

import yaml

COMMUNITY_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = COMMUNITY_DIR / "_aggregate_device_info_output.csv"

CSV_FIELDS = [
    "name",
    "name_en",
    "device",
    "registry_key",
    "action_count",
    "function_count",
    "atom_actions",
    "description",
    "description_en",
    "categories",
    "tags",
]


# ---------------------------------------------------------------------------
# Per-device extraction
# ---------------------------------------------------------------------------

def _pick_registry_entry(device_name: str, data: Any) -> tuple[str, dict]:
    """Return (registry_key, entry_dict) from parsed registry.yaml."""
    if not isinstance(data, dict):
        return device_name, {}
    if device_name in data and isinstance(data[device_name], dict):
        return device_name, data[device_name]
    first_key = next(iter(data), None)
    if first_key and isinstance(data.get(first_key), dict):
        return first_key, data[first_key]
    return device_name, {}


def _extract_registry(device_dir: Path, device_name: str) -> dict:
    """Extract fields from registry.yaml."""
    reg_path = device_dir / "registry.yaml"
    if not reg_path.exists():
        return {"registry_key": device_name, "action_count": 0, "atom_actions": ""}

    data = yaml.safe_load(reg_path.read_text(encoding="utf-8"))
    reg_key, entry = _pick_registry_entry(device_name, data)

    mappings = ((entry.get("class") or {}).get("action_value_mappings")) or {}
    if not isinstance(mappings, dict):
        mappings = {}
    action_names = sorted(mappings.keys())

    return {
        "registry_key": reg_key,
        "action_count": len(action_names),
        "atom_actions": "|".join(action_names),
    }


def _count_functions(device_dir: Path) -> int:
    """Count function definitions in driver.py."""
    driver_path = device_dir / "driver.py"
    if not driver_path.exists():
        return 0
    content = driver_path.read_text(encoding="utf-8", errors="replace")
    return len(re.findall(r"^\s*(?:async\s+)?def\s+", content, re.MULTILINE))


def _extract_info_txt(device_dir: Path, device_name: str) -> dict:
    """Extract description, description_en, categories, tags from info.txt."""
    info_path = device_dir / "info.txt"
    result = {"name": "", "name_en": "", "description": "", "description_en": "", "categories": "", "tags": ""}
    if not info_path.exists():
        return result

    data = yaml.safe_load(info_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return result

    # info.txt top-level key is usually the registry_key
    entry = data.get(device_name)
    if not isinstance(entry, dict):
        first_key = next(iter(data), None)
        entry = data.get(first_key) if isinstance(data.get(first_key), dict) else {}

    result["name"] = entry.get("name", "") or ""
    result["name_en"] = entry.get("name_en", "") or ""
    result["description"] = entry.get("description", "") or ""
    result["description_en"] = entry.get("description_en", "") or ""

    cats = entry.get("category", [])
    if isinstance(cats, list):
        result["categories"] = "|".join(str(c) for c in cats)

    tags = entry.get("tags", [])
    if isinstance(tags, list):
        result["tags"] = "|".join(str(t) for t in tags)

    return result


def extract_device_info(device_dir: Path) -> dict:
    """Extract all aggregated fields for one device directory."""
    device_name = device_dir.name

    reg = _extract_registry(device_dir, device_name)
    info = _extract_info_txt(device_dir, device_name)
    func_count = _count_functions(device_dir)

    return {
        "name": info["name"],
        "name_en": info["name_en"],
        "device": device_name,
        "registry_key": reg["registry_key"],
        "action_count": reg["action_count"],
        "function_count": func_count,
        "atom_actions": reg["atom_actions"],
        "description": info["description"],
        "description_en": info["description_en"],
        "categories": info["categories"],
        "tags": info["tags"],
    }


# ---------------------------------------------------------------------------
# Device discovery
# ---------------------------------------------------------------------------

def discover_device_dirs() -> list[Path]:
    """Return sorted list of device directories (those containing registry.yaml)."""
    dirs = []
    for child in sorted(COMMUNITY_DIR.iterdir()):
        if child.is_dir() and (child / "registry.yaml").exists():
            dirs.append(child)
    return dirs


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = set(sys.argv[1:])
    use_stdout = "--stdout" in args
    args.discard("--stdout")

    # Decide which devices to process
    if "--test" in args:
        args.discard("--test")
        all_dirs = discover_device_dirs()
        test_names = {"pump", "camera", "bronkhorst_elflow", "cobolt_laser", "plate_reader"}
        device_dirs = [d for d in all_dirs if d.name in test_names]
        if not device_dirs:
            device_dirs = [d for d in all_dirs if d.name < "u"][:5]
    elif args:
        device_dirs = [COMMUNITY_DIR / n for n in sorted(args) if (COMMUNITY_DIR / n).is_dir()]
    else:
        device_dirs = discover_device_dirs()

    # Open output: file (utf-8-sig for Excel compat) or stdout
    if use_stdout:
        sys.stdout.reconfigure(encoding="utf-8")
        sink = sys.stdout
        close_sink = False
    else:
        sink = open(OUTPUT_PATH, "w", encoding="utf-8-sig", newline="")
        close_sink = True

    try:
        writer = csv.DictWriter(sink, fieldnames=CSV_FIELDS)
        writer.writeheader()

        success, failed = 0, 0
        for device_dir in device_dirs:
            try:
                row = extract_device_info(device_dir)
                writer.writerow(row)
                success += 1
            except Exception as exc:
                failed += 1
                print(f"[ERROR] {device_dir.name}: {exc}", file=sys.stderr)
                writer.writerow({f: "" for f in CSV_FIELDS} | {"device": device_dir.name})
    finally:
        if close_sink:
            sink.close()

    dest = "stdout" if use_stdout else str(OUTPUT_PATH)
    print(f"# Processed {success + failed} devices: {success} ok, {failed} failed → {dest}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
