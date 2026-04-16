#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


WORK_ROOT = Path(__file__).resolve().parents[1]
FINAL_DIR = WORK_ROOT / "final"
WORK_DIR = WORK_ROOT / "work"

DEVICE_INPUT = FINAL_DIR / "01_concatenated_device_info.csv"
TAG_OUTPUT = FINAL_DIR / "03_life_science_related_tags.csv"
DEVICE_OUTPUT = FINAL_DIR / "04_life_science_related_devices.csv"
NORMALIZED_TAGS_PATH = WORK_DIR / "normalized_tags.jsonl"
MERGED_DECISIONS_PATH = WORK_DIR / "tag_decisions_merged.jsonl"

TAG_OUTPUT_FIELDS = [
    "id",
    "name",
    "name_en",
    "type",
    "source_files",
    "rationale_examples",
    "confidence",
]

DEVICE_EXTRA_FIELDS = [
    "source_file",
    "matched_life_science_tags",
    "matched_tag_confidences",
    "confidence",
]

CONFIDENCE_ORDER = {"high": 0, "medium": 1, "low": 2}


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_tag_outputs(normalized_tags: list[dict], decisions: list[dict]) -> tuple[list[dict[str, str]], dict[str, str]]:
    tag_by_key = {tag["tag_key"]: tag for tag in normalized_tags}
    token_to_confidence: dict[str, str] = {}
    output_rows: list[dict[str, str]] = []

    for decision in decisions:
        if not decision.get("keep"):
            continue
        tag = tag_by_key[decision["tag_key"]]
        row = {
            "id": tag["id"],
            "name": tag["name"],
            "name_en": tag["name_en"],
            "type": tag["type"],
            "source_files": "|".join(tag["source_files"]),
            "rationale_examples": " || ".join(tag.get("rationale_examples", [])),
            "confidence": decision["confidence"],
        }
        output_rows.append(row)
        for token in (tag["name"], tag["name_en"]):
            if not token:
                continue
            previous = token_to_confidence.get(token)
            if previous is None or CONFIDENCE_ORDER[decision["confidence"]] < CONFIDENCE_ORDER[previous]:
                token_to_confidence[token] = decision["confidence"]

    output_rows.sort(key=lambda row: (
        CONFIDENCE_ORDER[row["confidence"]],
        row["type"],
        row["name"],
        row["id"],
    ))
    return output_rows, token_to_confidence


def build_device_outputs(device_rows: list[dict[str, str]], token_to_confidence: dict[str, str]) -> tuple[list[dict[str, str]], list[str]]:
    if not device_rows:
        return [], []
    fieldnames = list(device_rows[0].keys()) + [field for field in DEVICE_EXTRA_FIELDS if field not in device_rows[0]]
    output_rows: list[dict[str, str]] = []

    for row in device_rows:
        tokens = [token.strip() for token in (row.get("tags") or "").split("|") if token.strip()]
        matched_tags: list[str] = []
        matched_confidences: list[str] = []
        for token in tokens:
            confidence = token_to_confidence.get(token)
            if confidence is None:
                continue
            matched_tags.append(token)
            matched_confidences.append(confidence)
        if not matched_tags:
            continue
        device_confidence = min(matched_confidences, key=lambda item: CONFIDENCE_ORDER[item])
        output_rows.append(row | {
            "matched_life_science_tags": "|".join(matched_tags),
            "matched_tag_confidences": "|".join(matched_confidences),
            "confidence": device_confidence,
        })

    output_rows.sort(key=lambda row: (
        CONFIDENCE_ORDER[row["confidence"]],
        row.get("name", ""),
        row.get("device", ""),
    ))
    return output_rows, fieldnames


def main() -> None:
    normalized_tags = load_jsonl(NORMALIZED_TAGS_PATH)
    decisions = load_jsonl(MERGED_DECISIONS_PATH)
    device_rows = load_csv(DEVICE_INPUT)

    tag_rows, token_to_confidence = build_tag_outputs(normalized_tags, decisions)
    device_output_rows, device_fields = build_device_outputs(device_rows, token_to_confidence)

    write_csv(TAG_OUTPUT, TAG_OUTPUT_FIELDS, tag_rows)
    write_csv(DEVICE_OUTPUT, device_fields, device_output_rows)

    summary = {
        "life_science_tags": len(tag_rows),
        "life_science_devices": len(device_output_rows),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
