#!/usr/bin/env python3
"""Structural validator for v4 enriched info.txt files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


# ─── Device entry required fields ───
DEVICE_ENTRY_REQUIRED = [
    "name",
    "name_en",
    "manufacturer",
    "category",
    "tags",
    "description",
    "description_en",
    "class",
]

# ─── auto_annotation_metadata required fields ───
METADATA_REQUIRED = [
    "registry_key",
    "annotation_workflow_version",
    "tag_hints",
    "existing_tags",
    "proposed_new_tags",
    "processing_pass_order",
]

# ─── Tag types that must each have >= 1 entry ───
REQUIRED_TAG_TYPES = [
    "experimental_step",
    "experimental_domain",
    "experimental_scene",
    "device_template_tag",
]

TAG_REQUIRED_FIELDS = ["id", "name", "name_en", "type", "rationale"]


def validate_tag_list(path: Path, key_name: str, tags: object) -> list[str]:
    errs: list[str] = []
    if tags is None:
        return errs
    if not isinstance(tags, list):
        return [f"{path}: {key_name}_not_list"]

    for i, tag in enumerate(tags):
        if not isinstance(tag, dict):
            errs.append(f"{path}: {key_name}[{i}]_not_mapping")
            continue
        for field in TAG_REQUIRED_FIELDS:
            if field not in tag:
                errs.append(f"{path}: {key_name}[{i}]_missing:{field}")
    return errs


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

    # ── Must have exactly 2 top-level keys: <device_key> and auto_annotation_metadata ──
    if "auto_annotation_metadata" not in data:
        errs.append(f"{path}: missing_key:auto_annotation_metadata")

    device_keys = [k for k in keys if k != "auto_annotation_metadata"]
    if len(device_keys) == 0:
        errs.append(f"{path}: missing_device_entry")
        return errs
    if len(device_keys) > 1:
        errs.append(f"{path}: multiple_device_entries:{device_keys}")

    device_key = device_keys[0]
    entry = data[device_key]

    # ── Device key should come first ──
    if keys[0] == "auto_annotation_metadata":
        errs.append(f"{path}: device_entry_should_precede_metadata")

    # ── Validate device entry ──
    if not isinstance(entry, dict):
        errs.append(f"{path}: device_entry_not_mapping")
        return errs

    for req in DEVICE_ENTRY_REQUIRED:
        if req not in entry:
            errs.append(f"{path}: device_entry_missing:{req}")

    if "category" in entry and not isinstance(entry["category"], list):
        errs.append(f"{path}: category_not_list")
    elif isinstance(entry.get("category"), list):
        for i, item in enumerate(entry["category"]):
            if not isinstance(item, str):
                errs.append(f"{path}: category[{i}]_not_string")

    if "tags" in entry:
        if not isinstance(entry["tags"], list):
            errs.append(f"{path}: device_tags_not_list")
        elif not all(isinstance(t, str) for t in entry["tags"]):
            errs.append(f"{path}: device_tags_items_not_strings")

    # ── Validate class.action_value_mappings ──
    cls = entry.get("class")
    if isinstance(cls, dict):
        avm = cls.get("action_value_mappings")
        if avm is not None and not isinstance(avm, dict):
            errs.append(f"{path}: action_value_mappings_not_mapping")
        elif isinstance(avm, dict):
            for action_name, action_spec in avm.items():
                if not isinstance(action_spec, dict):
                    continue
                schema = action_spec.get("schema")
                if not isinstance(schema, dict):
                    errs.append(f"{path}: action:{action_name}:missing_schema")
                    continue
                if "description" not in schema:
                    errs.append(f"{path}: action:{action_name}:schema_missing_description")

    # ── Validate auto_annotation_metadata ──
    meta = data.get("auto_annotation_metadata")
    if isinstance(meta, dict):
        for req in METADATA_REQUIRED:
            if req not in meta:
                errs.append(f"{path}: metadata_missing:{req}")

        # ── Validate tag_hints ──
        hints = meta.get("tag_hints")
        if hints is not None and not isinstance(hints, list):
            errs.append(f"{path}: tag_hints_not_list")
        elif isinstance(hints, list):
            for i, hint in enumerate(hints):
                if not isinstance(hint, str):
                    errs.append(f"{path}: tag_hints[{i}]_not_string")

        existing_tags = meta.get("existing_tags")
        proposed_new_tags = meta.get("proposed_new_tags")
        errs.extend(validate_tag_list(path, "existing_tags", existing_tags))
        errs.extend(validate_tag_list(path, "proposed_new_tags", proposed_new_tags))

        combined_tags: list[dict] = []
        if isinstance(existing_tags, list):
            combined_tags.extend([t for t in existing_tags if isinstance(t, dict)])
        if isinstance(proposed_new_tags, list):
            combined_tags.extend([t for t in proposed_new_tags if isinstance(t, dict)])

        type_counts = {}
        for tag in combined_tags:
            t = tag.get("type", "")
            type_counts[t] = type_counts.get(t, 0) + 1
        for req_type in REQUIRED_TAG_TYPES:
            if type_counts.get(req_type, 0) < 1:
                errs.append(f"{path}: combined_tags_missing_type:{req_type}")

        # ── Reject removed fields ──
        for removed in ["action_function_links", "useful_registry_metadata", "tags"]:
            if removed in meta:
                errs.append(f"{path}: metadata_unexpected_key:{removed}")

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

    print(f"validated {len(paths)} files, no errors")


if __name__ == "__main__":
    main()
