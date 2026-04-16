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
MANIFEST_PATH = OUTPUT_DIR / "qc_manifest.csv"
COMMUNITY_ROOT = UNILAB_ROOT / "community_drivers"
EXISTING_INFO_ROOT = UNILAB_ROOT / "existing_devices_info" / "info_extracted"
REGISTRY_ROOT = UNILAB_ROOT / "unilabos" / "registry" / "devices"

MANIFEST_FIELDS = [
    "registry_key",
    "output_file_path",
    "source_family",
    "source_info_path",
    "source_registry_path",
    "name_blank",
    "name_en_blank",
    "description_blank",
    "description_en_blank",
    "action_count_written",
]


def load_yaml_file(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    return data if data is not None else {}


def build_registry_index() -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in sorted(REGISTRY_ROOT.glob("*.yaml")):
        data = load_yaml_file(path)
        if not isinstance(data, dict):
            continue
        for key, value in data.items():
            if not isinstance(value, dict):
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


def source_paths_for_row(row: dict[str, str], registry_index: dict[str, Path]) -> tuple[str, Path, Path]:
    if row["source_file"] == "_aggregate_device_info_output.csv":
        info_path = COMMUNITY_ROOT / row["device"] / "info.txt"
        registry_path = COMMUNITY_ROOT / row["device"] / "registry.yaml"
        return "community_drivers", info_path, registry_path
    if row["source_file"] == "_aggregate_device_info_existing.csv":
        info_path = EXISTING_INFO_ROOT / f"{row['device']}_info.txt"
        registry_path = resolve_existing_registry_path(row["registry_key"], registry_index)
        return "existing_devices_info", info_path, registry_path
    raise SystemExit(f"Unsupported source_file {row['source_file']!r}")


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def main() -> None:
    registry_index = build_registry_index()
    with INPUT_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    output_files = sorted(OUTPUT_DIR.glob("info_*.yaml"))
    errors: list[str] = []
    if len(output_files) != len(rows):
        errors.append(f"Expected {len(rows)} generated YAML files, found {len(output_files)}")

    manifest_rows: list[dict[str, str]] = []
    name_blank_count = 0
    name_en_blank_count = 0

    for row in rows:
        source_family, info_path, registry_path = source_paths_for_row(row, registry_index)
        output_path = OUTPUT_DIR / f"info_{row['registry_key']}.yaml"
        if not output_path.exists():
            errors.append(f"Missing output file {output_path}")
            continue

        data = load_yaml_file(output_path)
        if not isinstance(data, dict) or len(data) != 1 or row["registry_key"] not in data:
            errors.append(f"{output_path} must contain exactly one top-level entry keyed by {row['registry_key']}")
            continue

        entry = data[row["registry_key"]]
        if not isinstance(entry, dict):
            errors.append(f"{output_path} top-level entry is not a mapping")
            continue

        for forbidden_key in ("existing_tags", "proposed_new_tags", "auto_annotation_metadata"):
            if forbidden_key in entry:
                errors.append(f"{output_path} unexpectedly contains {forbidden_key}")

        actions = entry.get("actions", {})
        if not isinstance(actions, dict):
            errors.append(f"{output_path} actions must be a mapping")
            action_count = 0
        else:
            action_count = len(actions)

        name_blank = not bool(entry.get("name"))
        name_en_blank = not bool(entry.get("name_en"))
        description_blank = not bool(entry.get("description"))
        description_en_blank = not bool(entry.get("description_en"))
        if name_blank:
            name_blank_count += 1
        if name_en_blank:
            name_en_blank_count += 1

        manifest_rows.append({
            "registry_key": row["registry_key"],
            "output_file_path": str(output_path),
            "source_family": source_family,
            "source_info_path": str(info_path),
            "source_registry_path": str(registry_path),
            "name_blank": bool_str(name_blank),
            "name_en_blank": bool_str(name_en_blank),
            "description_blank": bool_str(description_blank),
            "description_en_blank": bool_str(description_en_blank),
            "action_count_written": str(action_count),
        })

    with MANIFEST_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(manifest_rows)

    if errors:
        raise SystemExit("QC structural errors:\n- " + "\n- ".join(errors))
    if name_blank_count:
        raise SystemExit(f"QC failed: {name_blank_count} file(s) have blank name. See {MANIFEST_PATH}")
    if name_en_blank_count:
        raise SystemExit(
            f"QC manual-translation blocker: {name_en_blank_count} file(s) have blank name_en. See {MANIFEST_PATH}"
        )

    print(json.dumps({
        "manifest_path": str(MANIFEST_PATH),
        "manifest_rows": len(manifest_rows),
        "generated_yaml_files": len(output_files),
        "name_blank": name_blank_count,
        "name_en_blank": name_en_blank_count,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
