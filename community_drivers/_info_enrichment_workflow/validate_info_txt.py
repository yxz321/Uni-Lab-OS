#!/usr/bin/env python3
"""Lightweight structural validator for enriched info.txt files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


REQUIRED_TOP_LEVEL = [
    "device",
    "registry_key",
    "device_identity",
    "description",
    "description_evidence",
    "related_tags",
    "tag_evidence",
    "atom_actions",
    "driver_functions",
    "schema_version",
    "processing_pass_order",
    "stats",
]

IDENTITY_CONFLICT_KEYS = [
    "registry_manufacturer",
    "registry_model_name",
    "chosen_manufacturer",
    "chosen_model_name",
    "rationale",
]


def load_paths(manifest: Path | None, files: list[Path]) -> list[Path]:
    out = list(files)
    if manifest is not None:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        for dev in data.get("devices", []):
            path = dev.get("info_txt")
            if isinstance(path, str):
                out.append(Path(path))
    return out


def validate_file(path: Path) -> list[str]:
    errs: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{path}: yaml_parse_error: {exc}"]

    if not isinstance(data, dict):
        return [f"{path}: top_level_not_mapping"]

    keys = list(data.keys())
    for req in REQUIRED_TOP_LEVEL:
        if req not in data:
            errs.append(f"{path}: missing_key:{req}")

    if "categories" in data:
        errs.append(f"{path}: forbidden_key:categories")

    if keys[:4] != ["device", "registry_key", "device_identity", "description"]:
        errs.append(f"{path}: unexpected_key_order_prefix:{keys[:4]}")

    if "related_tags" in data and not isinstance(data["related_tags"], list):
        errs.append(f"{path}: related_tags_not_list")

    if "atom_actions" in data and not isinstance(data["atom_actions"], list):
        errs.append(f"{path}: atom_actions_not_list")

    if "driver_functions" in data and not isinstance(data["driver_functions"], dict):
        errs.append(f"{path}: driver_functions_not_mapping")

    if "registry_identity_conflict" in data:
        if not isinstance(data["registry_identity_conflict"], dict):
            errs.append(f"{path}: registry_identity_conflict_not_mapping")
        else:
            for key in IDENTITY_CONFLICT_KEYS:
                if key not in data["registry_identity_conflict"]:
                    errs.append(f"{path}: registry_identity_conflict_missing:{key}")
        if "description_evidence" in data and keys.index("registry_identity_conflict") < keys.index("description_evidence"):
            errs.append(f"{path}: registry_identity_conflict_wrong_order")

    return errs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("files", nargs="*", type=Path)
    args = parser.parse_args()

    paths = load_paths(args.manifest, args.files)
    errors: list[str] = []
    for path in paths:
        errors.extend(validate_file(path))

    if errors:
        for err in errors:
            print(err)
        raise SystemExit(1)

    print(f"validated {len(paths)} files")


if __name__ == "__main__":
    main()
