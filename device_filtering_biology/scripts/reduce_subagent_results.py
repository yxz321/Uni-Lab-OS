#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


WORK_ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = WORK_ROOT / "work"
RESULT_DIR = WORK_ROOT / "subagent_results"

NORMALIZED_TAGS_PATH = WORK_DIR / "normalized_tags.jsonl"
MERGED_DECISIONS_PATH = WORK_DIR / "tag_decisions_merged.jsonl"
CONFLICTS_PATH = WORK_DIR / "tag_conflicts.json"
ALLOWED_RELATEDNESS = {"high", "medium", "low", "exclude"}


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def validate_result_payload(path: Path, payload: dict) -> list[dict]:
    if not isinstance(payload, dict):
        raise SystemExit(f"{path.name}: payload must be an object")
    batch_id = payload.get("batch_id")
    results = payload.get("results")
    if not isinstance(batch_id, str) or not batch_id:
        raise SystemExit(f"{path.name}: batch_id must be a non-empty string")
    if not isinstance(results, list):
        raise SystemExit(f"{path.name}: results must be a list")
    validated: list[dict] = []
    for index, row in enumerate(results, start=1):
        if not isinstance(row, dict):
            raise SystemExit(f"{path.name}: results[{index}] must be an object")
        tag_key = row.get("tag_key")
        tag_id = row.get("id")
        relatedness = row.get("relatedness")
        rationale = row.get("rationale")
        signals = row.get("signals")
        if not isinstance(tag_key, str) or not tag_key:
            raise SystemExit(f"{path.name}: results[{index}].tag_key must be a non-empty string")
        if not isinstance(tag_id, str) or not tag_id:
            raise SystemExit(f"{path.name}: results[{index}].id must be a non-empty string")
        if relatedness not in ALLOWED_RELATEDNESS:
            raise SystemExit(f"{path.name}: results[{index}].relatedness must be one of {sorted(ALLOWED_RELATEDNESS)}")
        if not isinstance(rationale, str):
            raise SystemExit(f"{path.name}: results[{index}].rationale must be a string")
        if not isinstance(signals, list) or any(not isinstance(item, str) for item in signals):
            raise SystemExit(f"{path.name}: results[{index}].signals must be a list of strings")
        validated.append({
            "tag_key": tag_key,
            "id": tag_id,
            "relatedness": relatedness,
            "rationale": rationale,
            "signals": signals,
            "batch_id": batch_id,
            "source_file": path.name,
        })
    return validated


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    normalized_tags = load_jsonl(NORMALIZED_TAGS_PATH)
    normalized_keys = {row["tag_key"] for row in normalized_tags}

    result_files = sorted(RESULT_DIR.glob("tag_batch_*.result.json"))
    if not result_files:
        raise SystemExit("No subagent result files found in subagent_results/")

    by_key: dict[str, list[dict]] = {}
    for path in result_files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        for entry in validate_result_payload(path, payload):
            if entry["tag_key"] not in normalized_keys:
                raise SystemExit(f"{path.name}: unknown tag_key {entry['tag_key']}")
            by_key.setdefault(entry["tag_key"], []).append(entry)

    conflicts: dict[str, list[dict]] = {}
    merged_rows: list[dict] = []
    for tag_key, entries in sorted(by_key.items()):
        relatedness_values = {entry["relatedness"] for entry in entries}
        if len(relatedness_values) > 1:
            conflicts[tag_key] = entries
            continue
        chosen = entries[0]
        merged_rows.append({
            "tag_key": chosen["tag_key"],
            "id": chosen["id"],
            "relatedness": chosen["relatedness"],
            "confidence": chosen["relatedness"],
            "keep": chosen["relatedness"] != "exclude",
            "rationale": chosen["rationale"],
            "signals": chosen["signals"],
            "batch_id": chosen["batch_id"],
            "source_file": chosen["source_file"],
        })

    if conflicts:
        CONFLICTS_PATH.write_text(json.dumps(conflicts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        raise SystemExit(f"Found conflicting relatedness labels for {len(conflicts)} tag ids; see {CONFLICTS_PATH}")

    merged_rows.sort(key=lambda row: row["id"])
    write_jsonl(MERGED_DECISIONS_PATH, merged_rows)
    summary = {
        "result_files": len(result_files),
        "unique_tag_keys": len(merged_rows),
        "kept_tags": sum(1 for row in merged_rows if row["keep"]),
        "excluded_tags": sum(1 for row in merged_rows if not row["keep"]),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
