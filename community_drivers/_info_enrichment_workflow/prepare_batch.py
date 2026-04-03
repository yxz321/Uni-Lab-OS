#!/usr/bin/env python3
"""Prepare a reusable batch manifest and prompt for info.txt enrichment."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from string import Template


REPO_ROOT = Path(__file__).resolve().parent.parent
SUMMARY_CSV = REPO_ROOT / "_device_capability_summary.csv"
TAG_CSV = REPO_ROOT / "tag 标签列表.csv"
PROMPT_TEMPLATE = Path(__file__).resolve().parent / "agent_prompt_template.md"
BATCH_ROOT = Path(__file__).resolve().parent / "batches"


def load_summary_rows() -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    with SUMMARY_CSV.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows[row["device"]] = row
    return rows


def parse_device_args(raw_devices: list[str], devices_file: Path | None) -> list[str]:
    device_names: list[str] = []
    for item in raw_devices:
        for part in item.split(","):
            name = part.strip()
            if name:
                device_names.append(name)

    if devices_file is not None:
        for line in devices_file.read_text(encoding="utf-8").splitlines():
            name = line.strip()
            if name and not name.startswith("#"):
                device_names.append(name)

    deduped: list[str] = []
    seen: set[str] = set()
    for name in device_names:
        if name not in seen:
            deduped.append(name)
            seen.add(name)
    return deduped


def build_manifest(batch_name: str, devices: list[str], summary_rows: dict[str, dict[str, str]]) -> dict:
    manifest_devices = []
    missing = []

    for name in devices:
        folder = REPO_ROOT / name
        if name not in summary_rows or not folder.exists():
            missing.append(name)
            continue

        row = summary_rows[name]
        manifest_devices.append(
            {
                "device": name,
                "folder": str(folder),
                "driver_py": str(folder / "driver.py"),
                "registry_yaml": str(folder / "registry.yaml"),
                "info_txt": str(folder / "info.txt"),
                "current_categories": [x for x in row["categories"].split("|") if x],
                "current_tags": [x for x in row["tags"].split("|") if x],
                "action_count": int(row["action_count"]),
                "function_count": int(row["function_count"]),
                "current_short_description": row["short_description"],
            }
        )

    return {
        "batch_name": batch_name,
        "device_count": len(manifest_devices),
        "devices": manifest_devices,
        "missing_devices": missing,
        "supporting_files": {
            "tag_csv": str(TAG_CSV),
        },
        "notes": {
            "description_pass_before_tag_pass": True,
            "prototype_only": True,
        },
    }


def render_prompt(batch_name: str, manifest_path: Path, devices_path: Path) -> str:
    template_text = PROMPT_TEMPLATE.read_text(encoding="utf-8")
    suffix = (
        "\n\n## Batch paths\n\n"
        f"- batch name: `{batch_name}`\n"
        f"- manifest: `{manifest_path}`\n"
        f"- devices list: `{devices_path}`\n"
    )
    return Template(template_text).safe_substitute() + suffix


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-name", required=True, help="Short batch identifier")
    parser.add_argument(
        "--devices",
        nargs="*",
        default=[],
        help="Device names, optionally comma-separated",
    )
    parser.add_argument(
        "--devices-file",
        type=Path,
        help="Optional text file with one device name per line",
    )
    args = parser.parse_args()

    devices = parse_device_args(args.devices, args.devices_file)
    if not devices:
        raise SystemExit("No devices provided. Use --devices or --devices-file.")

    summary_rows = load_summary_rows()
    manifest = build_manifest(args.batch_name, devices, summary_rows)

    BATCH_ROOT.mkdir(parents=True, exist_ok=True)
    batch_dir = BATCH_ROOT / args.batch_name
    batch_dir.mkdir(parents=True, exist_ok=True)

    devices_path = batch_dir / "devices.txt"
    manifest_path = batch_dir / "manifest.json"
    prompt_path = batch_dir / "agent_prompt.md"

    devices_path.write_text("\n".join(devices) + "\n", encoding="utf-8")
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    prompt_path.write_text(
        render_prompt(args.batch_name, manifest_path, devices_path),
        encoding="utf-8",
    )

    print(f"Prepared batch: {args.batch_name}")
    print(f"Batch directory: {batch_dir}")
    print(f"Devices listed: {len(devices)}")
    print(f"Devices resolved: {manifest['device_count']}")
    if manifest["missing_devices"]:
        print("Missing devices: " + ", ".join(manifest["missing_devices"]))


if __name__ == "__main__":
    main()
