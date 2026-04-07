# v4_batch_079 Report

## Devices Processed

- servo_fiber_shaker
- sftp_wrapper
- shaker
- shaker_chatterbox_backend
- shared_serial
- shf_scope
- shfqa
- shfqc
- shfsg
- shutter

## What Worked Well

- Full v4 pipeline completed end-to-end for all 10 devices (extract -> Pass A -> compare -> Pass B -> render -> validate -> tag collect).
- Structural validation passed: `validated 10 files, no errors`.
- Web-search conflict handling was applied where needed (`shf_scope`) and constrained to `02_device_profile_api.json.parsed.{name,name_en,manufacturer,description,description_en}`.
- Final `info.txt` files were written successfully to all target device folders.

## What Still Needs Fixing

- Registry metadata quality remains noisy for some devices (software/helper components mislabeled as physical instruments), which still creates avoidable identity conflicts.
- Pass B latency is high for batch-level responses; no failure this run, but long quiet periods reduce observability.

## Proposed New Tags (Append Decision)

- Status: appended (kept), 5 rows appended to `tag_additions_proposed.csv`.
- `P-00001` / 光纤扰动与光路去相关 / `experimental_scene` (servo_fiber_shaker)
- `P-00002` / 实验设备模拟与流程调试 / `experimental_scene` (shaker_chatterbox_backend)
- `P-00003` / 振荡器模拟后端 / `device_template_tag` (shaker_chatterbox_backend)
- `P-00004` / 量子读出分析仪 / `device_template_tag` (shfqa)
- `P-00005` / 快门时序控制器 / `device_template_tag` (shutter)

## QA Samples (2 Devices)

- `shf_scope`
  - `name`: SHFQA示波采集组件
  - `description`: 用于 Zurich Instruments SHFQA 平台的示波采集软件组件（非独立硬件）。该组件对应 SHFQA 的 scope 节点/接口，负责采集配置、触发与数据读取，用于量子测量流程中的时域波形观测。
  - `tags`: 表征设备, 低温与量子测量, 量子比特脉冲控制与读出, 超导量子比特标定与时域测量, 数字存储示波器
- `shaker_chatterbox_backend`
  - `name`: Chatterbox振荡器模拟后端
  - `description`: 用于振荡器流程的非实体软件组件。它提供振荡、停止振荡以及夹板锁定/解锁等接口，主要用于测试、调试或在未连接具体硬件时模拟振荡器行为。
  - `tags`: 备料&前处理设备, 实验室自动化与仪器集成, 微孔板样品孵育与混匀, 实验设备模拟与流程调试, 振荡器模拟后端

## QA Samples (3 Action Summaries)

- `shfqa` / `auto-acquisition`: 执行一次完整采集流程，并返回测量结果。
- `shfqa` / `auto-configure_spectroscopy`: 配置连续或脉冲式谱学扫描实验序列。
- `shfqa` / `auto-push_to_device`: 将驱动中缓存的配置下发到实际仪器。

## Recommended Adjustments Before Next Batch

- Add a lightweight pre-Pass-B warning report for devices with likely software-node identities (e.g., `*_backend`, `*_wrapper`, `*_scope`) when compare artifacts show hardware-level conflicts, so reviewers can focus web-search effort quickly.
- Keep current semantic boundary unchanged (no script-side semantic auto-repair), but include an optional progress heartbeat in Pass B for long-running batch API calls.
