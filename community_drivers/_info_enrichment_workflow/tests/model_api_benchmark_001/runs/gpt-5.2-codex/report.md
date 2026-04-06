# Benchmark Report — gpt-5.2-codex (workflow v4)

## Devices processed
- bio_shake
- cc_core
- cryo_tel_gt
- cvd_control
- cytomat_backend

## What worked well
- Pass A completed for all 5/5 devices with coherent `name/name_en`, bilingual descriptions, and action coverage aligned to registry action ids.
- Pass B completed for all 5/5 devices and produced valid per-device `_batch_tag_api.json`.
- Rendering + validation succeeded (`validated 5 files, no errors`).

## What still needs fixing
- `cc_core` remains semantically tricky: generated profile is coherent, but registry-side category/scene priors appear potentially mismatched to quantum-control context and can bias downstream tags.
- `cryo_tel_gt` tag mapping selected `深低温冰箱` as closest existing template; acceptable under current tag inventory but not ideal for a cryocooler-specific device template.

## Proposed new tags (added/discarded)
- Proposed by model in this run: none (`proposed_new_tags: []` for all devices).
- Added to tag catalog from this run: none.
- Discarded: none.

## QA samples (2 final info.txt)
1. `runs/gpt-5.2-codex/cryo_tel_gt/info.txt`
- Identity and description are consistent with cryocooler behavior.
- Action descriptions correctly follow get/set style for control/status properties.
- Tag set is usable but template specificity is limited by available tag list.

2. `runs/gpt-5.2-codex/cvd_control/info.txt`
- CVD process-control interpretation is stable and action descriptions are concise and faithful.
- Tag assignment is coherent (`化学气相沉积设备` selected, no unnecessary new tags).

## Prompt/script/workflow adjustments recommended before next batch
- Validation command robustness: documented command `python3 ../../validate_info_txt.py runs/<model>/*/info.txt` did not expand wildcard in this shell invocation context; explicit file expansion via `find ... -name info.txt` was reliable.
- Consider adding a guardrail in Pass B prompt for "controller/core module" devices (e.g., quantum control systems) to reduce bias from potentially stale registry category/scene fields.
- Consider enriching device_template tags for cryogenic controllers/cryocoolers to avoid fallback to freezer-centric templates.
