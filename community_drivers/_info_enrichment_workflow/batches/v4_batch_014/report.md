# v4_batch_014 Report

## Devices Processed

- ccl
- centrifuge
- cesar1312
- channel_client
- charge_coupled_device
- chemputersoftware__serial_device
- cito_plus1310
- clari_ostar_backend
- client
- client_async

## What Worked Well

- Deterministic extraction, Pass A, compare, Pass B, render, validate, and tag collection all completed without script failure.
- `validate_info_txt.py` passed for all 10 devices (`validated 10 files, no errors`).
- Targeted web search was used only for material identity conflicts (`cesar1312`, `cito_plus1310`) and recorded as compact `websearch_evidence.json` artifacts.
- Final `info.txt` files were written to all device folders listed in the manifest.

## What Still Needs Fixing

- Manufacturer ambiguity remains for mixed legacy/current branding cases (example: `cesar1312`, Dressler vs Advanced Energy ownership context).
- Several software-wrapper/client-type drivers still map into physical-device-oriented tag space; coverage is structurally valid but semantics can be improved further in prompts/taxonomy.

## Proposed New Tags

- Appended to `tag_additions_proposed.csv`: 4 rows.
- Proposed and appended IDs: `P-8001`, `P-8002`, `P-8003`, `P-8004`.
- No proposals were discarded in this batch.

## QA Samples (2 Devices)

### centrifuge

- name: 实验室离心机
- description: 实验室离心机利用离心力分离液体样品中的不同组分，常用于样品沉降、相分离和前处理。该设备具备舱门控制、转篮/吊篮位置切换，以及按设定离心力和时间执行离心循环的能力，可用于自动化样品处理流程。
- tags: 备料&前处理设备, 溶液配制与反应, 实验室自动化与仪器集成, 离心机, 液体样品离心分离与前处理

### client

- name: ARTIQ 固件构建服务客户端
- description: 用于连接 ARTIQ 固件构建服务的网络客户端，可通过 WebSocket 登录、提交指定版本和变体的构建请求，并读取文本或 JSON 格式的返回结果。该服务常用于为实验室中的 ARTIQ 控制硬件准备固件或相关构建产物。
- tags: 实验执行&合成设备, 实验室自动化与仪器集成, 实验控制固件构建与部署, 固件构建服务客户端

## Sampled Action Summaries (3)

- `centrifuge.auto-start_spin_cycle`: 按设定离心力和持续时间启动一次离心循环。
- `client.auto-build`: 提交指定版本、修订和变体的构建请求，并可附带日志或实验性功能选项。
- `ccl.auto-print_qisa_opcodes`: 读取并显示设备支持的 QISA 操作码。

## Recommended Prompt / Workflow Change

- In conflict-resolution guidance, add an explicit rule for legacy-vs-current manufacturer naming (for acquired product lines), e.g. preferred format/order when evidence supports both historic brand and current owner.
