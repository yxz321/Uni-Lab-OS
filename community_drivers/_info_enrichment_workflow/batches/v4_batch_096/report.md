# v4_batch_096 Report

## Devices processed
- uxr
- v_spin_backend
- vantage_backend
- vcn
- vdipm5_b
- vertical_mirror
- vfl
- video_file_capture
- view2_d
- viewer1_d

## What worked well
- Completed the full v4 sequence for all 10 devices using `Vendor2/GPT-5.4` with `reasoning_effort=medium`.
- Pass A and Pass B both completed without schema/runtime failures.
- Render and structural validation succeeded for all target `info.txt` files (`validated 10 files, no errors`).
- Physical instruments and software simulation/viewer components were separated coherently.

## What still needs fixing
- Some registry manufacturer fields appear noisy for several devices, but driver-derived identities were more coherent and had to be preferred.
- Taxonomy coverage for simulation/viewer software components is still sparse, leading to multiple new template-tag proposals.

## Proposed new tags
- Proposed tags were kept and appended (`6` rows):
  - `P-970002` 样品分离与前处理 / Sample Separation & Pre-processing (`experimental_domain`)
  - `P-970003` 可调针阀 / Adjustable Needle Valve (`device_template_tag`)
  - `P-970004` 光学反射镜运动学模拟器 / Optical Mirror Kinematics Simulator (`device_template_tag`)
  - `P-970005` 视频文件采集源 / Video File Capture Source (`device_template_tag`)
  - `P-970006` 二维科学数据查看器 / 2D Scientific Data Viewer (`device_template_tag`)
  - `P-970007` 一维科学数据查看器 / 1D Scientific Data Viewer (`device_template_tag`)

## Sampled final device entries (2)
- device: `v_spin_backend`
  - name: 安捷伦 VSpin 离心机
  - description: 用于实验室样品离心处理的自动化离心机，可进行转子位置控制、开关门、门锁与桶锁控制，并按设定的相对离心力或转速执行离心程序。
  - tags: [备料&前处理设备, 实验室自动化与仪器集成, 液体样品离心分离与前处理, 离心机, 样品分离与前处理]
- device: `view2_d`
  - name: 二维数据视图组件
  - description: 一个用于实验软件中的非物理二维数据显示组件，用于绘制和操作图像数据。它支持图像显示、ROI 区域、十字光标、线剖面、直方图、图例、坐标轴标签与缩放，常用于相机图像或扫描成像结果的实时可视化与分析。
  - tags: [表征设备, 实验数据可视化与分析, 多维实验数据可视化, 科学图像区域标注与感兴趣区分析, 感兴趣区图形标注器, 二维科学数据查看器]

## Sampled action summaries (3)
- `uxr` / `auto-measureStatistics`: 读取当前统计测量窗口中的测量统计结果。
- `v_spin_backend` / `auto-spin`: 按设定离心力、时长、加速度和减速度执行离心。
- `view2_d` / `auto-display_images`: 显示二维图像数据。

## Recommended adjustments before next batch
- For simulation and visualization components, add stronger prompt guidance to prefer software-component template tags early, reducing ambiguity between “instrument-like” and “software-tool” categorization.
