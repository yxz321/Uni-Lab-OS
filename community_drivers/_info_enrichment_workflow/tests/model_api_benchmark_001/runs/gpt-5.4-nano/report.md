# Workflow v4 Benchmark Report (`gpt-5.4-nano`)

## Devices processed
- `bio_shake`
- `cc_core`
- `cryo_tel_gt`
- `cvd_control`
- `cytomat_backend`

## What worked well
- Pass A and Pass B both completed successfully for all 5 devices using `reasoning_effort=medium`.
- Render + validation completed cleanly (`validated 5 files, no errors`).
- No extra web search was required for this batch (no major identity/description failures).

## What still needs fixing
- `cc_core` remains semantically in a quantum-control context from Pass A, but final tags are strongly biology/liquid-handling aligned due registry priors; this is likely a data-prior conflict and should be handled in prompt/ranking logic.
- `cryo_tel_gt` gets a plausible template tag (`深低温冰箱`) but domain/scene mapping may still be taxonomy-driven rather than device-function-driven.

## Proposed new tags (added/discarded)
- Proposed by model in this batch: none.
- Added to tag list: none.
- Discarded: none.

## QA sample of final `info.txt` (2 devices)

### Sample 1: `bio_shake`
- File: `runs/gpt-5.4-nano/bio_shake/info.txt`
- Name: `BioShake 恒温振荡器`
- Name (EN): `BioShake Heater-Shaker`
- Manufacturer: `""`
- Device template tag: `恒温摇床 / Constant Temperature Shaker`
- Description quality: consistent with heater-shaker physical behavior and action set.

### Sample 2: `cryo_tel_gt`
- File: `runs/gpt-5.4-nano/cryo_tel_gt/info.txt`
- Name: `Sunpower CryoTel GT 低温制冷机`
- Name (EN): `Sunpower CryoTel GT Cryocooler`
- Manufacturer: `Sunpower`
- Device template tag: `深低温冰箱 / Ultra-Low Temperature Freezer`
- Description quality: consistent with cryocooler temperature/power control behavior and telemetry actions.

## Recommended adjustments before next batch
- In Pass B prompt/scoring, increase weight of Pass A semantic evidence (`name_en`, `description_en`, `tag_hints`) when it conflicts with registry category/scene priors.
- Add a lightweight conflict guard in Pass B: if selected tags imply a different domain than Pass A core semantics, require explicit rationale or fallback alternative tags.
- Keep current scripts unchanged for this run; no benchmark-local script bug blocked execution.
