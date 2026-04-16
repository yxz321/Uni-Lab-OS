#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
from collections import OrderedDict
from pathlib import Path


WORK_ROOT = Path(__file__).resolve().parents[1]
DPTECH_ROOT = WORK_ROOT.parent
SOURCE_ROOT = DPTECH_ROOT / "community_drivers" / "Uni-Lab-OS" / "community_drivers"
FINAL_DIR = WORK_ROOT / "final"
WORK_DIR = WORK_ROOT / "work"
BATCH_DIR = WORK_ROOT / "batches"

DEVICE_SOURCES = [
    SOURCE_ROOT / "_aggregate_device_info_output.csv",
    SOURCE_ROOT / "_aggregate_device_info_existing.csv",
]
TAG_SOURCES = [
    SOURCE_ROOT / "tag 标签列表.csv",
    SOURCE_ROOT / "tag_additions_proposed.csv",
]

DEVICE_OUTPUT = FINAL_DIR / "01_concatenated_device_info.csv"
TAG_OUTPUT = FINAL_DIR / "02_concatenated_tags.csv"
NORMALIZED_TAGS_OUTPUT = WORK_DIR / "normalized_tags.jsonl"
TAG_CANDIDATES_OUTPUT = WORK_DIR / "tag_candidates.jsonl"

DEVICE_OUTPUT_FIELDS = [
    "name",
    "name_en",
    "device",
    "registry_key",
    "action_count",
    "function_count",
    "atom_actions",
    "description",
    "description_en",
    "categories",
    "tags",
    "source_file",
]

TAG_OUTPUT_FIELDS = [
    "id",
    "name",
    "name_en",
    "type",
    "rationale",
    "status",
    "source_file",
]

KEYWORD_FAMILIES = [
    ("life_domain", [
        "生命", "life science", "lifescience", "生物", "bio", "biology", "biological",
        "细胞", "cell", "cellular", "组织", "tissue", "微生物", "microbial", "菌",
    ]),
    ("molecular", [
        "基因", "gene", "genome", "genomic", "核酸", "nucleic", "dna", "rna", "pcr",
        "测序", "sequenc", "蛋白", "protein", "proteom", "分子", "molecular",
        "电穿孔", "electroporat", "文库", "library construction",
    ]),
    ("plate_workflow", [
        "微孔板", "plate", "酶标", "reader", "washer", "洗板", "封膜", "sealer",
        "撕膜", "desealer", "板", "孔板", "高通量", "throughput", "assay",
    ]),
    ("liquid_handling", [
        "移液", "liquid handling", "pipett", "配液", "dispens", "加液", "sample prep",
        "样品制备", "磁珠纯化", "bead purification",
    ]),
    ("incubation_storage", [
        "培养", "culture", "incubat", "孵育", "离心", "centrif", "冷冻", "freezer",
        "低温", "thermomix", "热混匀", "恒温振荡", "shake", "storage",
    ]),
    ("microscopy_imaging", [
        "显微", "microscop", "optical microscopy", "fluorescen", "成像", "imaging",
        "光学显微", "flow cyt", "流式细胞", "生理信号", "biosignal",
    ]),
    ("automation_support", [
        "实验室自动化", "laboratory automation", "自动化", "automation",
        "样品", "sample", "机械臂", "robot", "robotic", "plate handling",
        "handling module", "工作站", "workstation",
    ]),
]

TARGET_BATCHES = 6
MAX_BATCH_SIZE = 80
MIN_BATCH_SIZE = 40


def ensure_dirs() -> None:
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    BATCH_DIR.mkdir(parents=True, exist_ok=True)


def remove_existing_batches() -> None:
    for path in BATCH_DIR.glob("tag_batch_*.json"):
        path.unlink()


def iter_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def normalize_text(value: str) -> str:
    return " ".join(value.lower().split())


def make_tag_key(tag_id: str, name: str, name_en: str, tag_type: str) -> str:
    return "||".join([tag_id, tag_type, name, name_en])


def gather_devices() -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []
    for source in DEVICE_SOURCES:
        for row in iter_csv_rows(source):
            output_rows.append({field: row.get(field, "") for field in DEVICE_OUTPUT_FIELDS if field != "source_file"} | {
                "source_file": source.name,
            })
    write_csv(DEVICE_OUTPUT, DEVICE_OUTPUT_FIELDS, output_rows)
    return output_rows


def gather_tags() -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []
    for source in TAG_SOURCES:
        for row in iter_csv_rows(source):
            output_rows.append({
                "id": row.get("id", ""),
                "name": row.get("name", ""),
                "name_en": row.get("name_en", ""),
                "type": row.get("type", ""),
                "rationale": row.get("rationale", ""),
                "status": row.get("status", ""),
                "source_file": source.name,
            })
    write_csv(TAG_OUTPUT, TAG_OUTPUT_FIELDS, output_rows)
    return output_rows


def normalize_tags(tag_rows: list[dict[str, str]]) -> list[dict]:
    normalized: OrderedDict[tuple[str, str, str, str], dict] = OrderedDict()
    for row in tag_rows:
        key = (row["id"], row["name"], row["name_en"], row["type"])
        entry = normalized.setdefault(key, {
            "tag_key": make_tag_key(row["id"], row["name"], row["name_en"], row["type"]),
            "id": row["id"],
            "name": row["name"],
            "name_en": row["name_en"],
            "type": row["type"],
            "source_files": [],
            "rationale_examples": [],
        })
        if row["source_file"] and row["source_file"] not in entry["source_files"]:
            entry["source_files"].append(row["source_file"])
        rationale = " ".join((row.get("rationale") or "").split())
        if rationale and rationale not in entry["rationale_examples"] and len(entry["rationale_examples"]) < 3:
            entry["rationale_examples"].append(rationale)
    normalized_rows = list(normalized.values())
    write_jsonl(NORMALIZED_TAGS_OUTPUT, normalized_rows)
    return normalized_rows


def find_keyword_hits(text: str) -> list[tuple[str, str]]:
    lowered = normalize_text(text)
    hits: list[tuple[str, str]] = []
    for family, keywords in KEYWORD_FAMILIES:
        for keyword in keywords:
            if keyword in lowered:
                hits.append((family, keyword))
    return hits


def make_evidence_snippets(tag: dict, hits: list[tuple[str, str]]) -> list[str]:
    snippets: list[str] = []
    seen: set[str] = set()
    for field_name in ("name", "name_en"):
        value = tag.get(field_name, "")
        for family, keyword in find_keyword_hits(value):
            snippet = f"{field_name}: {value} [family={family}; keyword={keyword}]"
            if snippet not in seen:
                snippets.append(snippet)
                seen.add(snippet)
            if len(snippets) >= 3:
                return snippets
    for rationale in tag.get("rationale_examples", []):
        for family, keyword in find_keyword_hits(rationale):
            snippet = f"rationale: {rationale} [family={family}; keyword={keyword}]"
            if snippet not in seen:
                snippets.append(snippet)
                seen.add(snippet)
            if len(snippets) >= 3:
                return snippets
    if not snippets and hits:
        families = ", ".join(dict.fromkeys(family for family, _ in hits))
        snippets.append(f"matched families: {families}")
    return snippets[:3]


def shortlist_candidates(normalized_tags: list[dict]) -> list[dict]:
    candidates: list[dict] = []
    for tag in normalized_tags:
        combined_text = " | ".join([
            tag.get("name", ""),
            tag.get("name_en", ""),
            " | ".join(tag.get("rationale_examples", [])),
        ])
        hits = find_keyword_hits(combined_text)
        if not hits:
            continue
        matched_families = list(dict.fromkeys(family for family, _ in hits))
        candidates.append({
            "tag_key": tag["tag_key"],
            "id": tag["id"],
            "name": tag["name"],
            "name_en": tag["name_en"],
            "type": tag["type"],
            "source_files": tag["source_files"],
            "evidence_snippets": make_evidence_snippets(tag, hits),
            "matched_families": matched_families,
        })
    candidates.sort(key=lambda row: (
        row["matched_families"][0] if row["matched_families"] else "",
        row["type"],
        row["name"],
        row["id"],
    ))
    write_jsonl(TAG_CANDIDATES_OUTPUT, candidates)
    return candidates


def pick_batch_size(total_items: int) -> int:
    if total_items <= MAX_BATCH_SIZE:
        return total_items
    minimum_batch_count = max(TARGET_BATCHES, math.ceil(total_items / MAX_BATCH_SIZE))
    for batch_count in range(minimum_batch_count, total_items + 1):
        batch_size = math.ceil(total_items / batch_count)
        if MIN_BATCH_SIZE <= batch_size <= MAX_BATCH_SIZE:
            return batch_size
    return MAX_BATCH_SIZE


def shard_candidates(candidates: list[dict]) -> list[Path]:
    remove_existing_batches()
    if not candidates:
        return []
    batch_size = pick_batch_size(len(candidates))
    batch_paths: list[Path] = []
    for index in range(0, len(candidates), batch_size):
        batch_number = (index // batch_size) + 1
        batch_id = f"tag_batch_{batch_number:03d}"
        records = [{
            "tag_key": row["tag_key"],
            "id": row["id"],
            "name": row["name"],
            "name_en": row["name_en"],
            "type": row["type"],
            "source_files": row["source_files"],
            "evidence_snippets": row["evidence_snippets"],
        } for row in candidates[index:index + batch_size]]
        batch_path = BATCH_DIR / f"{batch_id}.json"
        payload = {
            "batch_id": batch_id,
            "record_count": len(records),
            "records": records,
        }
        batch_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        batch_paths.append(batch_path)
    return batch_paths


def main() -> None:
    ensure_dirs()
    device_rows = gather_devices()
    tag_rows = gather_tags()
    normalized_tags = normalize_tags(tag_rows)
    candidates = shortlist_candidates(normalized_tags)
    batch_paths = shard_candidates(candidates)
    summary = {
        "device_rows": len(device_rows),
        "tag_rows": len(tag_rows),
        "normalized_tags": len(normalized_tags),
        "candidate_tags": len(candidates),
        "batches": len(batch_paths),
        "batch_files": [path.name for path in batch_paths],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
