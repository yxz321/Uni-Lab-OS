#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path("/home/xzye/projects/DPTech/device_filtering_biology")
TARGET_DIR = ROOT / "final" / "reformatted_info_yaml"


def as_dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def flatten_entry(entry: dict[str, Any]) -> dict[str, Any]:
    class_data = as_dict(entry.get("class"))
    action_mappings = as_dict(class_data.get("action_value_mappings"))

    actions: dict[str, Any] = {}
    for action_name, action_data in action_mappings.items():
        schema = as_dict(as_dict(action_data).get("schema"))
        actions[action_name] = {
            "description": schema.get("description", "") or "",
            "description_en": schema.get("description_en", "") or "",
        }

    flattened: dict[str, Any] = {}
    inserted_actions = False
    for key, value in entry.items():
        if key == "class":
            flattened["actions"] = actions
            inserted_actions = True
            continue
        flattened[key] = value
    if not inserted_actions:
        flattened["actions"] = actions
    return flattened


def main() -> None:
    paths = sorted(TARGET_DIR.glob("info_*.yaml"))
    updated = 0

    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or len(data) != 1:
            raise SystemExit(f"{path} must contain exactly one top-level device entry")
        registry_key, entry = next(iter(data.items()))
        if not isinstance(entry, dict):
            raise SystemExit(f"{path} top-level entry must be a mapping")

        flattened = flatten_entry(entry)
        with path.open("w", encoding="utf-8", newline="") as handle:
            yaml.safe_dump({registry_key: flattened}, handle, allow_unicode=True, sort_keys=False)
        updated += 1

    print(json.dumps({
        "target_dir": str(TARGET_DIR),
        "updated_files": updated,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
