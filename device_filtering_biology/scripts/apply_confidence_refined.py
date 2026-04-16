#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/xzye/projects/DPTech/device_filtering_biology")
CSV_PATH = ROOT / "final" / "04_life_science_related_devices.csv"
RESULT_DIR = ROOT / "work" / "confidence_refined" / "results"
ALLOWED = {"high", "medium", "low", "exclude"}


def load_results() -> dict[int, dict[str, str]]:
    result_files = sorted(RESULT_DIR.glob("refine_batch_*.result.json"))
    if not result_files:
        raise SystemExit("No refine_batch result files found.")

    merged: dict[int, dict[str, str]] = {}
    for path in result_files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
            raise SystemExit(f"Invalid payload in {path}")
        for item in payload["results"]:
            if not isinstance(item, dict):
                raise SystemExit(f"Invalid result row in {path}")
            row_index = item.get("row_index")
            device = item.get("device")
            confidence_refined = item.get("confidence_refined")
            if not isinstance(row_index, int):
                raise SystemExit(f"row_index must be int in {path}")
            if not isinstance(device, str) or not device:
                raise SystemExit(f"device must be non-empty string in {path}")
            if confidence_refined not in ALLOWED:
                raise SystemExit(f"confidence_refined must be one of {sorted(ALLOWED)} in {path}")
            if row_index in merged:
                raise SystemExit(f"Duplicate row_index {row_index} across result files")
            merged[row_index] = {
                "device": device,
                "confidence_refined": confidence_refined,
            }
    return merged


def main() -> None:
    merged = load_results()
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys()) if rows else []

    if "confidence_refined" not in fieldnames:
        fieldnames.append("confidence_refined")

    review_count = 0
    for idx, row in enumerate(rows):
        if row.get("confidence") in {"high", "medium"}:
            review_count += 1
            result = merged.get(idx)
            if result is None:
                raise SystemExit(f"Missing refined result for row_index={idx} device={row.get('device')}")
            if result["device"] != row.get("device"):
                raise SystemExit(
                    f"Device mismatch for row_index={idx}: csv={row.get('device')} result={result['device']}"
                )
            row["confidence_refined"] = result["confidence_refined"]
        else:
            row["confidence_refined"] = row.get("confidence_refined", "")

    if review_count != len(merged):
        raise SystemExit(f"Expected {review_count} refined results, found {len(merged)}")

    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps({
        "updated_csv": str(CSV_PATH),
        "reviewed_rows": review_count,
        "result_files": len(list(RESULT_DIR.glob('refine_batch_*.result.json'))),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
