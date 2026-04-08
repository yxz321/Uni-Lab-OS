# v4_batch_095 Report

## Devices processed
- usbctr
- usbtmc_communicator
- usbtmc_device
- usbtmc_driver
- usbtmclight
- ux_rxxx2_a
- ux_rxxx4_a
- uxbus_cmd
- uxbus_cmd_ser
- uxbus_cmd_tcp

## What worked well
- Full v4 workflow completed in required order with `Vendor2/GPT-5.4` and `reasoning_effort=medium`.
- Pass A and Pass B both completed for all 10 devices.
- Pass B auto-retry handled one non-structured first response and recovered cleanly.
- Rendering and validation passed for all devices.

## What still needs fixing
- No blocking workflow/script issues in this batch.
- No compare-stage identity conflict required web search.

## Proposed new tags
- Status: appended.
- Appended rows: 2 (to `tag_additions_proposed.csv`).
- usbtmclight / `P-700101` / `实验照明与光激发` / `experimental_scene`
- usbtmclight / `P-700102` / `实验室可控光源` / `device_template_tag`

## QA samples (2 device entries)
- usbtmclight
  - name: USB-TMC实验光源
  - description: 通过 USB-TMC 通信控制的实验室光源，可进行开关、光强设定、运行时长设定、状态查询、温度读取和预设配方激活，适用于实验中的照明、激发或定时曝光场景。
  - tags: [实验执行&合成设备, 光学与光谱实验, 实验照明与光激发, 实验室可控光源]
- usbctr
  - name: USB-CTR04/08 多通道标度计数器
  - description: Measurement Computing 的 USB-CTR04/USB-CTR08 多通道标度计数器，用于对脉冲或计数通道进行定时采集。该设备支持内部/外部模式、连续采集、标量采集、阵列采集和 ROI 模式，可启动、停止、清除并读取 MCS/MCA 数据，常用于步进扫描或连续扫描实验中的计数信号采集。
  - tags: [表征设备, 智慧表征与检测中心, 同步计数与探测器通道监测, 瞬态信号采集与同步触发测量, 标量计数器]

## QA samples (3 action summaries)
- usbtmclight / auto-set_intensity: 设置光强百分比。
- usbctr / auto-ScalerMode: 设置为标量模式，用于步进扫描采集。
- uxbus_cmd / auto-move_joint: 执行关节运动。

## Recommended adjustments before next batch
- Keep prompts/scripts unchanged; this batch executed stably.
- Optional: add more reusable existing tags for USB-TMC light-source style components to reduce repeated proposal generation.
