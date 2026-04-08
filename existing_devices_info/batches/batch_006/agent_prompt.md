# Existing Registry Structured Tagging Subagent Prompt

You are assigning structured tags for exactly one assigned batch under `existing_device_infos`.

## Scope

- Work only on the info files listed in `entries.txt` and `manifest.json`.
- You are not alone in the codebase. Other workers are editing other batch files at the same time.
- Do not revert or rewrite files outside your assigned batch, and do not touch shared scripts or manifests unless your batch instructions explicitly require it.

## Goal

Write structured tag evidence into the assigned `*_info.txt` files using these two sections:
- `existing_tags`
- `proposed_new_tags`

The flat fields:
- `tags`
- `category`

are derived later by the main workflow. Do not spend effort hand-curating them.

Preserve these fields exactly unless a formatting fix is unavoidable:
- top-level registry key
- `category`
- `tags`
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

## Structured Tag Output Rules

- You must write both sections:
  - `existing_tags`
  - `proposed_new_tags`
- Each tag object must contain exactly:
  - `id`
  - `name`
  - `name_en`
  - `type`
  - `rationale`
- `type` must be one of:
  - `experimental_step`
  - `experimental_domain`
  - `experimental_scene`
  - `device_template_tag`
- The combined set of `existing_tags` and `proposed_new_tags` must include at least one tag of each required type.
- Prefer existing tags when reasonably relevant.
- Encourage multiple relevant tags per required type when the evidence supports them.
- Prioritize discovery rate / recall over strict best-match ranking.
- Include broad parent tags together with more specific tags when both improve searchability.
- Do not omit a relevant tag just because another tag is more specific.
- Reject only obviously unrelated tags.
- A practical default is roughly 1-4 relevant tags per type when supported.
- `experimental_step` may appear only in `existing_tags`.
- `proposed_new_tags` may include only:
  - `experimental_domain`
  - `experimental_scene`
  - `device_template_tag`
- Proposed new tags must be broad enough that:
  - multiple real devices could fit the same `device_template_tag`
  - multiple templates could fit the same `experimental_scene`
  - multiple scenes could fit the same `experimental_domain`
- `name` should be Chinese-preferred.
- `name_en` should be English.
- Every selected or proposed tag must include a short, device-specific rationale.
- Treat tags from both `tag 标签列表.csv` and `tag_additions_proposed.csv` as available existing tags.
- If you create a new proposed tag, use only IDs from the assigned batch range in the batch instructions.

## Required YAML Shape

Write sections in this shape:

```yaml
existing_tags:
  - id: '4316'
    name: 表征设备
    name_en: Characterization Equipment
    type: experimental_step
    rationale: 该通道用于采集并标定多类传感器信号，核心用途是测量与表征。
proposed_new_tags:
  - id: P-2001
    name: 模拟输入数据采集模块
    name_en: Analog Input Data Acquisition Module
    type: device_template_tag
    rationale: 该设备是面向多类模拟传感器的输入采集单元，比通用接口标签更贴切。
```

## Editing Rules

- Keep the file structure simple and stable.
- Do not add English mirror fields.
- Do not add comments.
- Do not change the filename.
- Do not rename the top-level registry key.
- Only `existing_tags` and `proposed_new_tags` should be edited intentionally.
- Leave `category` and `tags` alone; the main workflow will recompute them later.

## Report

Write a short `report.md` in the assigned batch folder that includes:
- the files you updated
- any uncertain tag choices
- any newly proposed tags
- any taxonomy gaps you noticed

Keep the report concise.

## Assigned Batch

- batch_name: `batch_006`
- batch_dir: `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/batches/batch_006`
- entries_file: `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/batches/batch_006/entries.txt`
- manifest: `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/batches/batch_006/manifest.json`
- report_path: `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/batches/batch_006/report.md`
- category_list_csv: `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/category_list.csv`
- tag_list_csv: `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/tag 标签列表.csv`
- proposed_tags_csv: `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/tag_additions_proposed.csv`
- assigned_model: `gpt-5.4`
- new_proposed_tag_id_range: `P-2501` to `P-2600`

### Assigned Entry IDs

- `robot_linear_motion.motor.iCL42`
- `solid_dispenser.solid_dispenser.laiyu`
- `temperature.chiller`
- `temperature.heaterstirrer.dalong`
- `temperature.tempsensor`
- `virtual_device.virtual_centrifuge`
- `virtual_device.virtual_column`
