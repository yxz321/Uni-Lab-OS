# v4_batch_070 Report

## Devices processed

- raw_client
- reader
- readout
- real_usb_device
- recipe
- recipe_pusher
- recipe_rule
- recorder
- rectangle_type_graphic
- register_interface

## What worked well

- Deterministic extraction, Pass A, compare, Pass B, render, and validator all completed successfully for all 10 devices.
- Updated non-physical software/helper guardrail was effective for this batch: most devices were coherently identified as software/interface components without forcing physical-hardware identities.
- Final `info.txt` writing was limited to manifest-listed devices.

## What still needs fixing

- `03_enriched_payload.json` in this batch has empty top-level `actions` arrays, while action summaries are present in `info.txt` under `class.action_value_mappings`; this makes automated action-level QA less direct.
- Several software/helper devices still carry `experimental_step` tags that imply physical execution equipment (`实验执行&合成设备` / `表征设备`), which may be semantically broad for pure software components.

## Proposed new tags

- Proposed: `P-970001 | 实验配方规则引擎 | Experiment Recipe Rule Engine | device_template_tag` (from `recipe_rule`)
- Decision: kept and appended to `tag_additions_proposed.csv`

## Sampled final device entries (2)

1. `readout`
- name: SHFQA量子分析仪读出模块
- description: 用于苏黎世仪器 SHFQA 量子分析仪的读出功能模块，面向量子比特/多能级态测量。它可配置结果记录器、写入和读取加权积分权重、运行读出采集，并管理与测序器、波形存储器和触发相关的读出流程。
- tags: `实验执行&合成设备`, `表征设备`, `低温与量子测量`, `量子比特脉冲控制与读出`, `超导量子比特标定与时域测量`, `量子实验控制器`, `数字解调仪`

2. `recipe_rule`
- name: 配方规则组件
- description: 这是一个非物理的软件组件，用于定义并准备实验数据处理中的配方规则。它服务于集群或笔记本环境下的任务启动、组织与进度跟踪，而不是直接控制任何实验硬件。
- tags: `后处理设备`, `实验计算与数据处理`, `实验数据管理与记录`, `分布式实验数据处理`, `实验配方规则引擎`

## Sampled action summaries (3)

1. `raw_client.auto-read`: 从服务端口读取指定数量的原始数据元素。  
2. `raw_client.auto-get_blocks`: 以分块方式获取原始数据，便于连续传输或后处理。  
3. `register_interface.auto-write`: 向指定地址写入数值，以执行 FPGA 的底层寄存器写操作。  

## Recommended adjustments before next batch

- In `render_info_txt.py`, optionally mirror normalized action summaries into top-level `03_enriched_payload.json.actions` for easier machine QA and sampling.
- Consider tightening tag guidance for non-physical helper/software components to reduce assignment of hardware-like `experimental_step` tags when not required by evidence.
