# gpt-5.4-mini benchmark report (workflow v4)

## Devices processed
- bio_shake
- cc_core
- cryo_tel_gt
- cvd_control
- cytomat_backend

## What worked well
- Pass A completed for all 5 devices with usable bilingual identity/description/action outputs.
- Pass B completed in one batch and produced per-device `_batch_tag_api.json` + traces.
- Render step produced `03_enriched_payload.json` and `info.txt` for all devices.
- Final validation passed for `bio_shake` and `cytomat_backend`.

## What still needs fixing
- Validation failed for 3 devices:
  - `cc_core/info.txt`: `tags_missing_type:device_template_tag`
  - `cryo_tel_gt/info.txt`: `tags_missing_type:device_template_tag`
  - `cvd_control/info.txt`: `tags_missing_type:device_template_tag`
- Root cause: Pass B returned `device_template_tag` only in `proposed_new_tags`, not in `tags`, while renderer only writes `tags` into final validation path.

## Proposed new tags (added/discarded)
- Proposed by Pass B (not added to global tag files in this run):
  - `N-cvd-controller` / `CVD控制器` / `CVD Controller` / `device_template_tag` (from `cvd_control`)
  - `N-cryo-cooler` / `低温制冷机` / `Cryocooler` / `device_template_tag` (from `cryo_tel_gt`)
  - `N-cc-core-controller` / `实验控制器` / `Experimental Controller` / `device_template_tag` (from `cc_core`)
- Status in this run: **discarded for now** (kept as proposals only; not appended/accepted).

## QA sample of final info.txt (2 files)
1. `runs/gpt-5.4-mini/bio_shake/info.txt`
   - Device identity: `BioShake 加热振荡器` / `BioShake Heater Shaker`
   - Description quality: clear physical-device description (heated shaker for microplates).
   - Tag coverage: includes all required tag types, validation passed.
2. `runs/gpt-5.4-mini/cytomat_backend/info.txt`
   - Device identity: `Cytomat 自动化培养箱` / `Cytomat Automated Incubator`
   - Description quality: clear physical-device description (automated incubator + plate logistics).
   - Tag coverage: includes all required tag types, validation passed.

## Recommended adjustments before next batch
- Pass B robustness: enforce output contract so each device always includes at least one `device_template_tag` in `tags` (not only `proposed_new_tags`).
- Add a deterministic post-check in `run_pass_b.py` or `render_info_txt.py`:
  - if `tags` lacks `device_template_tag` and a proposed one exists, promote one proposed template tag into `tags` for validation compatibility.
- Keep current prompt mostly unchanged; this is primarily a structured-output constraint/enforcement issue.

## Notes
- No web search evidence files were created in this run (not needed after Pass A review).
