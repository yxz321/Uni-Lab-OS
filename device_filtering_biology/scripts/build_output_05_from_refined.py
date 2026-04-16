#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/xzye/projects/DPTech/device_filtering_biology")
INPUT_CSV = ROOT / "final" / "04_life_science_related_devices.csv"
OUTPUT_CSV = ROOT / "final" / "05_life_science_related_devices_refined_high_medium.csv"
KEEP = {"high", "medium"}
CONFIDENCE_ORDER = {"high": 0, "medium": 1}


def main() -> None:
    with INPUT_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys()) if rows else []

    filtered = [row for row in rows if row.get("confidence_refined") in KEEP]
    filtered.sort(
        key=lambda row: (
            CONFIDENCE_ORDER[row["confidence_refined"]],
            row.get("name_en", ""),
            row.get("device", ""),
        )
    )

    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered)

    print(
        json.dumps(
            {
                "input_csv": str(INPUT_CSV),
                "output_csv": str(OUTPUT_CSV),
                "filtered_rows": len(filtered),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
