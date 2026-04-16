#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path("/home/xzye/projects/DPTech/device_filtering_biology")
DPTECH_ROOT = ROOT.parent
UNILAB_ROOT = DPTECH_ROOT / "community_drivers" / "Uni-Lab-OS"
INPUT_CSV = ROOT / "final" / "05_life_science_related_devices_refined_high_medium.csv"
OUTPUT_DIR = ROOT / "final" / "reformatted_info_yaml"
OVERRIDES_PATH = OUTPUT_DIR / "manual_name_overrides.yaml"
COMMUNITY_ROOT = UNILAB_ROOT / "community_drivers"
EXISTING_INFO_ROOT = UNILAB_ROOT / "existing_devices_info" / "info_extracted"
REGISTRY_ROOT = UNILAB_ROOT / "unilabos" / "registry" / "devices"
AUTO_META_KEY = "auto_annotation_metadata"


def load_yaml_file(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    return data if data is not None else {}


def as_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def as_list(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return list(value)
    return [value]


def as_dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def first_non_metadata_entry(data: Any) -> tuple[str, dict[str, Any]]:
    if not isinstance(data, dict):
        raise ValueError("YAML root is not a mapping")
    for key, value in data.items():
        if key == AUTO_META_KEY:
            continue
        if isinstance(value, dict):
            return key, value
    raise ValueError("No non-metadata device entry found")


def select_info_entry(data: Any, registry_key: str) -> tuple[str, dict[str, Any]]:
    if isinstance(data, dict):
        candidate = data.get(registry_key)
        if isinstance(candidate, dict):
            return registry_key, candidate
    return first_non_metadata_entry(data)


def select_registry_entry(data: Any, registry_key: str, *, exact_required: bool) -> tuple[str, dict[str, Any]]:
    if not isinstance(data, dict):
        raise ValueError("Registry YAML root is not a mapping")
    candidate = data.get(registry_key)
    if isinstance(candidate, dict):
        return registry_key, candidate
    if exact_required:
        raise KeyError(f"Registry key {registry_key!r} not found in registry file")
    return first_non_metadata_entry(data)


def build_registry_index() -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in sorted(REGISTRY_ROOT.glob("*.yaml")):
        data = load_yaml_file(path)
        if not isinstance(data, dict):
            continue
        for key, value in data.items():
            if key == AUTO_META_KEY or not isinstance(value, dict):
                continue
            if key in index and index[key] != path:
                raise SystemExit(f"Duplicate registry key {key!r} found in both {index[key]} and {path}")
            index[key] = path
    return index


def resolve_existing_registry_path(registry_key: str, registry_index: dict[str, Path]) -> Path:
    direct = REGISTRY_ROOT / f"{registry_key}.yaml"
    if direct.exists():
        return direct
    path = registry_index.get(registry_key)
    if path is None:
        raise FileNotFoundError(f"Unable to resolve registry YAML for {registry_key}")
    return path


def load_overrides() -> dict[str, dict[str, str]]:
    if not OVERRIDES_PATH.exists():
        OVERRIDES_PATH.write_text("{}\n", encoding="utf-8")
        return {}
    data = load_yaml_file(OVERRIDES_PATH)
    if not isinstance(data, dict):
        raise SystemExit(f"{OVERRIDES_PATH} must contain a mapping keyed by registry_key")
    normalized: dict[str, dict[str, str]] = {}
    for key, value in data.items():
        if not isinstance(value, dict):
            raise SystemExit(f"Override for {key!r} must be a mapping")
        normalized[key] = {name: as_str(val) for name, val in value.items() if name in {"name", "name_en"}}
    return normalized


def normalized_action_description(source_actions: dict[str, Any], registry_actions: dict[str, Any], action_name: str, field: str) -> str:
    source_schema = as_dict(as_dict(source_actions.get(action_name)).get("schema"))
    registry_schema = as_dict(as_dict(registry_actions.get(action_name)).get("schema"))
    value = as_str(source_schema.get(field))
    if value:
        return value
    value = as_str(registry_schema.get(field))
    return value


def normalize_device_entry(source_entry: dict[str, Any], registry_entry: dict[str, Any], registry_key: str, overrides: dict[str, dict[str, str]]) -> dict[str, Any]:
    source_actions = as_dict(as_dict(source_entry.get("class")).get("action_value_mappings"))
    registry_actions = as_dict(as_dict(registry_entry.get("class")).get("action_value_mappings"))

    normalized_actions: dict[str, Any] = {}
    for action_name in registry_actions:
        normalized_actions[action_name] = {
            "description": normalized_action_description(source_actions, registry_actions, action_name, "description"),
            "description_en": normalized_action_description(source_actions, registry_actions, action_name, "description_en"),
        }

    entry = {
        "name": as_str(source_entry.get("name")),
        "name_en": as_str(source_entry.get("name_en")),
        "manufacturer": as_str(source_entry.get("manufacturer")),
        "category": as_list(source_entry.get("category")),
        "tags": as_list(source_entry.get("tags")),
        "description": as_str(source_entry.get("description")),
        "description_en": as_str(source_entry.get("description_en")),
        "actions": normalized_actions,
    }

    override = overrides.get(registry_key, {})
    if "name" in override:
        entry["name"] = as_str(override["name"])
    if "name_en" in override:
        entry["name_en"] = as_str(override["name_en"])
    return entry


def source_paths_for_row(row: dict[str, str], registry_index: dict[str, Path]) -> tuple[str, Path, Path]:
    if row["source_file"] == "_aggregate_device_info_output.csv":
        info_path = COMMUNITY_ROOT / row["device"] / "info.txt"
        registry_path = COMMUNITY_ROOT / row["device"] / "registry.yaml"
        return "community_drivers", info_path, registry_path

    if row["source_file"] == "_aggregate_device_info_existing.csv":
        info_path = EXISTING_INFO_ROOT / f"{row['device']}_info.txt"
        registry_path = resolve_existing_registry_path(row["registry_key"], registry_index)
        return "existing_devices_info", info_path, registry_path

    raise SystemExit(f"Unsupported source_file {row['source_file']!r} for {row['registry_key']}")


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        yaml.safe_dump(payload, handle, allow_unicode=True, sort_keys=False)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in OUTPUT_DIR.glob("info_*.yaml"):
        path.unlink()

    overrides = load_overrides()
    registry_index = build_registry_index()

    with INPUT_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    written = 0
    summary_rows: list[dict[str, str]] = []
    for row in rows:
        source_family, info_path, registry_path = source_paths_for_row(row, registry_index)
        info_data = load_yaml_file(info_path)
        registry_data = load_yaml_file(registry_path)

        _, info_entry = select_info_entry(info_data, row["registry_key"])
        _, registry_entry = select_registry_entry(
            registry_data,
            row["registry_key"],
            exact_required=(source_family == "existing_devices_info"),
        )

        normalized_entry = normalize_device_entry(info_entry, registry_entry, row["registry_key"], overrides)
        output_path = OUTPUT_DIR / f"info_{row['registry_key']}.yaml"
        write_yaml(output_path, {row["registry_key"]: normalized_entry})
        written += 1
        summary_rows.append({
            "registry_key": row["registry_key"],
            "source_family": source_family,
            "info_path": str(info_path),
            "registry_path": str(registry_path),
            "output_path": str(output_path),
        })

    summary_path = OUTPUT_DIR / "_source_resolution_summary.json"
    summary_path.write_text(json.dumps(summary_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "input_csv": str(INPUT_CSV),
        "output_dir": str(OUTPUT_DIR),
        "written_files": written,
        "overrides_path": str(OVERRIDES_PATH),
        "summary_path": str(summary_path),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
