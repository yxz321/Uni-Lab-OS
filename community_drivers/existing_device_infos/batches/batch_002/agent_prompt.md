# Existing Registry Refinement Subagent Prompt

You are refining extracted registry summaries for exactly one assigned batch under `existing_device_infos`.

## Scope

- Work only on the info files listed in `entries.txt` and `manifest.json`.
- You are not alone in the codebase. Other workers are editing other batch files at the same time.
- Do not revert or rewrite files outside your assigned batch, and do not touch shared scripts or manifests unless your batch instructions explicitly require it.

## Goal

Improve only the `category` and `tags` fields in the assigned `*_info.txt` files.

Preserve these fields exactly unless a formatting fix is unavoidable:
- top-level registry key
- `name`
- `description`
- `class.action_value_mappings`
- every `schema.description`

## Evidence Rules

- Use only the assigned `*_info.txt` files plus the reference CSVs:
  - `category_list.csv`
  - `tag 标签列表.csv`
  - `tag_additions_proposed.csv`
- Do not read the raw source YAML registry files.
- Do not use web search.
- Base your refinement only on:
  - device `name`
  - `description`
  - action names
  - action `schema.description`

## Category Rules

- `category` must remain a YAML list of strings.
- Prefer exact Chinese names from `category_list.csv` when they fit.
- Keep categories Chinese-preferred.
- Use a short, conservative list. Most devices should have 0-3 categories.
- If the evidence is weak, keep the current value or leave the list empty rather than inventing a speculative category.

## Tag Rules

- `tags` must remain a YAML list of strings.
- Prefer exact Chinese `name` values from `tag 标签列表.csv` when they fit.
- You may also reuse clearly relevant names from `tag_additions_proposed.csv`.
- Keep tags Chinese-preferred.
- Prefer broad, reusable lab tags over overly narrow one-off phrases.
- Use only evidence-supported tags. If unsure, leave a tag out.
- A practical target is roughly 2-8 tags when the evidence supports them.

## Editing Rules

- Keep the file structure simple and stable.
- Do not add English mirror fields.
- Do not add comments.
- Do not change the filename.
- Do not rename the top-level registry key.
- Only the `category` and `tags` values should materially change.

## Report

Write a short `report.md` in the assigned batch folder that includes:
- the files you updated
- any category or tag choices that were especially uncertain
- any taxonomy gaps you noticed

Keep the report concise.

## Assigned Batch

- batch_name: `batch_002`
- batch_dir: `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/batches/batch_002`
- entries_file: `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/batches/batch_002/entries.txt`
- manifest: `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/batches/batch_002/manifest.json`
- report_path: `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/batches/batch_002/report.md`
- category_list_csv: `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/category_list.csv`
- tag_list_csv: `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/tag 标签列表.csv`
- proposed_tags_csv: `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/tag_additions_proposed.csv`
- assigned_model: `gpt-5.4`

### Assigned Entry IDs

- `chinwe.separator.chinwe`
- `coin_cell_workstation.coincellassemblyworkstation_device`
- `gas_handler.gas_source.mock`
- `gas_handler.vacuum_pump.mock`
- `hotel.hotel.thermo_orbitor_rs2_hotel`
- `laiyu_liquid_test.xyz_stepper_controller`
- `liquid_handler.liquid_handler`
- `liquid_handler.liquid_handler.biomek`
