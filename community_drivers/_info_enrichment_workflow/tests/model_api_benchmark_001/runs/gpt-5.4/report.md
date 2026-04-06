# Workflow v4 Benchmark Report (`gpt-5.4`)

## Devices processed
- bio_shake
- cc_core
- cryo_tel_gt
- cvd_control
- cytomat_backend

## What worked well
- Pass A completed for all 5 devices with coherent bilingual name/description/action mappings.
- Pass B produced complete tag sets (all required types present per device).
- Render step produced `03_enriched_payload.json` + `info.txt` for all devices.
- Validation passed: `validated 5 files, no errors`.

## What still needs fixing
- `cc_core` appears semantically quantum-control oriented, while registry category/legacy tag context points to liquid-handling style taxonomy; this mismatch still affects downstream tag/domain alignment.
- `cryo_tel_gt` currently maps to existing template `深低温冰箱`; this is workable but not ideal for a cryocooler-specific ontology.
- `cvd_control` and `cytomat_backend` manufacturers remain empty (no confident evidence from allowed artifacts).

## Proposed new tags (added vs discarded)
- Proposed by Pass B:
  - `P-NEW-001` / `实验时序控制器` / `Experimental Timing Controller` / `device_template_tag`
  - Source device: `cc_core`
- Decision in this run:
  - Kept in run outputs (`_batch_tag_api.json` + rendered metadata) for comparison.
  - Not appended to global `tag_additions_proposed.csv` in this benchmark run.
- Discarded proposals:
  - None.

## Sampled final `info.txt` (QA)

### Sample 1: `bio_shake/info.txt`
- Name: `BioShake微孔板加热振荡器` / `BioShake Microplate Heater Shaker`
- Manufacturer: `QInstruments`
- Tags: `器件/细胞设备`, `生命体系`, `细胞生物学研究`, `恒温摇床`
- Description quality: matches microplate shaking + temperature-control use case; no obvious identity conflict.

### Sample 2: `cvd_control/info.txt`
- Name: `化学气相沉积系统` / `Chemical Vapor Deposition System`
- Manufacturer: empty
- Tags: `实验执行&合成设备`, `表面/薄膜体系`, `涂层材料`, `化学气相沉积设备`
- Description quality: concise and aligned with CVD process-control behavior (`recipe`, `setpoints`, `plot/update`).

## Prompt/script/workflow adjustments before next batch
- Add a small helper command in docs for validation using explicit file expansion (e.g., `$(find ... -name info.txt)`), since wildcard passing can fail depending on invocation context.
- Add a lightweight post-pass QA check that flags likely taxonomy conflicts between inferred device family and legacy registry category/tag hints.
- Consider adding guidance for when to keep `manufacturer` empty vs infer from strong model-name clues to improve consistency.

## Web search usage
- No targeted web search was needed for this batch (no critical identity/description conflicts after Pass A review).
