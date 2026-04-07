# v4_batch_087 Report

## Devices processed
- tcp_port_mapper_client
- tcp_raw_driver
- tcp_sampler
- tcp_serve_value
- tcpip_connection
- tcpip_instr_vicp
- tds1002b
- tds1012
- tds2024
- tek_dpo4104

## What worked well
- Completed the full v4 workflow for all 10 devices with `Vendor2/GPT-5.4` and `reasoning_effort=medium`.
- Pass A, compare, Pass B, render, and validation all succeeded without schema/runtime failures.
- Physical identities for Tektronix oscilloscopes were coherent and consistent; software/network components were kept as non-physical components.

## What still needs fixing
- Some software communication components retain broad step-level tags due to current tag inventory and matching behavior.
- `manufacturer` remains empty for generic/open software components where vendor certainty is low.

## Proposed new tags
- No proposed new tags were generated in this batch.
- `collect_proposed_tags.py --append`: no rows appended.

## Sampled final device entries (2)
- device: `tds1012`
  - name: 泰克 TDS1012 数字存储示波器
  - description: 一款 100 MHz、2 通道数字存储示波器，用于采集和观察电信号波形，并进行频率、均值、最小值、最大值等基础测量。该设备支持触发、自动设置、自动校准和波形数据读取，适合电子实验与信号调试。
  - tags: [表征设备, 电子与电气测试, 射频与电子电路测试, 瞬态信号采集与同步触发测量, 通用电学参数测量, 数字存储示波器]
- device: `tcp_raw_driver`
  - name: TCP原始通信组件
  - description: 这是一个非物理的软件通信组件，用作通过 TCP 与实验室仪器建立网络连接的通用基类。它负责初始化和关闭套接字连接、检查连接是否打开，以及发送和接收原始字节数据，适合为基于网络协议的仪器驱动提供底层通信能力。
  - tags: [实验执行&合成设备, 实验室自动化与仪器集成, 实验仪器通信与驱动集成, 实验仪器数据采集与联机控制, 通用字节流仪器通信接口]

## Sampled action summaries (3)
- `tds1012` / `auto-acquire_curve`: 采集示波器波形数据。
- `tcp_raw_driver` / `auto-raw_send`: 通过 TCP 向仪器发送原始字节数据。
- `tek_dpo4104` / `auto-force_trigger`: 强制示波器产生一次触发事件。

## Recommended adjustments before next batch
- Add a stronger prompt note for software-only transport/helper components to prefer infrastructure-oriented taxonomy and reduce broad step-tag overlap when no physical instrument is represented.
