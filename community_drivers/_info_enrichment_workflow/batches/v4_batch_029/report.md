# v4_batch_029 Report

## Devices processed
- ftp_base_wrapper
- ftp_wrapper
- func_gen
- function_generator
- furnace
- fw102_b
- g2_v_sunbrick
- galil
- gamepad6_dof_teleop
- gamry

## What worked well
- Full v4 pipeline completed end to end for all 10 devices: extraction, Pass A, compare, Pass B, render, validate, and proposed-tag collection.
- Pass A and Pass B both completed with 0 failures and produced all required artifacts.
- Structural validation passed for all rendered files (`validated 10 files, no errors`).
- Compare artifacts were coherent enough to resolve conflicts without targeted web search; no unresolved device-family ambiguity remained.

## What still needs fixing
- Several registry-side identity fields are clearly weak/noisy (wrapper/backend wording, mismatched manufacturer/model), which still creates large diffs in compare artifacts.
- Pass B execution is quiet for long periods between batch request start and completion; this is operationally safe but reduces observability for long-running batches.

## Proposed new tags
- Kept and appended (4 rows) via `collect_proposed_tags.py --append`:
  - `P-0209` 管式炉 / Tube Furnace (`device_template_tag`) for `furnace`
  - `P-0210` 电动滤光片转轮 / Motorized Filter Wheel (`device_template_tag`) for `fw102_b`
  - `P-0211` 可调光谱照明与光照实验 / Tunable Spectral Illumination Experiments (`experimental_scene`) for `g2_v_sunbrick`
  - `P-0212` 多通道可调光谱LED光源 / Multi-Channel Tunable Spectrum LED Light Source (`device_template_tag`) for `g2_v_sunbrick`

## QA samples (2 devices: name, description, tags)
- gamry
  - name: Gamry电化学工作站
  - description: 一种用于电化学实验的台式电化学工作站（恒电位/恒电流仪），可施加设定的电位扫描并采集电流等响应信号，常用于循环伏安、线性扫描和电位斜坡类测试。
  - tags: 表征设备, 电化学测试与分析, 电化学表征与阻抗谱测量, 电化学工作站
- fw102_b
  - name: 电动滤光片转轮
  - description: 一款多工位电动滤光片转轮，可在多个滤光片位置之间快速切换。常用于显微成像、荧光实验和光学测量中，以选择不同波段或不同类型的光学滤片。
  - tags: 表征设备, 光学与光谱实验, 显微成像与光学显微实验, 电动滤光片转轮

## QA samples (3 action summaries)
- gamry / `auto-potential_cycle`: 执行循环电位扫描测量，在设定电位范围内往返扫描多个循环并记录响应。
- galil / `auto-motor_move`: 按指定轴、距离/位置、速度和模式移动电机。
- g2_v_sunbrick / `auto-set_channel_value`: 设置指定节点的LED通道输出值。

## Recommended adjustments before next batch
- Add periodic heartbeat/progress logging in `run_pass_b.py` while waiting for batch API completion (for example every 15-30s) to improve runtime observability without changing semantics.
