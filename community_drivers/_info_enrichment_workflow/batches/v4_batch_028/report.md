# v4_batch_028 Report

## Devices processed
- filter_wheel
- fire_sting
- flash_firmware
- flask_service
- flow_controller
- flow_meter
- fluke3000
- folder_capture
- frame_grabber
- fridge__monitor

## What worked well
- Deterministic extraction completed for all 10 devices and generated `01_local_signals.json`.
- Pass A / compare / Pass B all completed without schema failures.
- Render wrote all target `community_drivers/<device>/info.txt`.
- Validator passed: `validated 10 files, no errors`.
- Conflict resolution with targeted web search was applied to 4 devices (`flash_firmware`, `flow_controller`, `flow_meter`, `fridge__monitor`) and corresponding `websearch_evidence.json` files were saved.

## What still needs fixing
- The profile editable identity fields in `02_device_profile_api.json` are nested under `parsed`. Manual conflict-resolution edits can be mistakenly applied at top level and silently ignored by downstream steps. This was corrected in this batch by rewriting `parsed.{name,name_en,manufacturer,description,description_en}` and rerunning Pass B/render/validate.
- Proposed tag append currently allows repeated rows across reruns/parallel runs by design; dedupe remains a known follow-up item.

## Proposed new tags (append/discard decision)
- Append executed successfully.
- Rows appended in this run:
  - First append: 11 rows (`P-12001` to `P-12011`)
  - Final append after corrected profile rerun: 1 row (`P-13001`, `flash_firmware`)
- Discarded: none

## QA sample: 2 final device entries
- flash_firmware
  - name: 固件烧录服务
  - description: 用于通过串口等接口将编译后的固件写入嵌入式设备的烧录软件服务组件，常见于 ESP32 等微控制器开发流程。该组件负责组织烧录参数、端口连接与写入流程，不对应单一硬件厂商设备。
  - tags: 备料&前处理设备, 实验室自动化与仪器集成, 实验控制固件构建与部署, 固件烧录服务
- flow_controller
  - name: 质量流量控制器
  - description: 质量流量控制器（MFC）用于精确调节气体或液体的质量流量，常见于气体配比、工艺供气和实验流程控制。该驱动上下文显示可能覆盖多家厂商型号，厂商信息不唯一时保持空值。
  - tags: 实验执行&合成设备, 气体输送与过程控制, 气体供给与混气控制, 气体质量流量控制器

## QA sample: 3 action summaries
- fire_sting: `auto-measure` -> 测量设备所有通道的氧信号及相关补偿参数。
- frame_grabber: `auto-run` -> 启动帧采集。
- fridge__monitor: `auto-snapshot` -> 获取当前监测参数快照

## Recommended prompt/workflow adjustment before next batch
- In the subagent prompt and/or workflow doc, explicitly state that the five editable profile fields must be edited under `02_device_profile_api.json.parsed.*` (not top-level keys), and optionally add a lightweight script check before Pass B to detect misplaced top-level edits.
