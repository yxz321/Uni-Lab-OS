# v4_batch_094 Report

## Devices processed
- usb4000_2000_plus
- usb_class
- usb_comm_obp
- usb_comm_ooi
- usb_communicator
- usb_device
- usb_device_description
- usb_driver
- usb_port
- usb_train_id

## What worked well
- Completed full v4 workflow for all 10 devices with `Vendor2/GPT-5.4` and `reasoning_effort=medium`.
- Pass A and Pass B completed without schema/runtime failure.
- Rendering and structural validation succeeded for all output `info.txt` files.
- Physical spectrometer identity (`usb4000_2000_plus`) remained clear while USB middleware components were kept as non-physical software components.

## What still needs fixing
- Some registry manufacturer fields appear noisy for USB communication-layer components (e.g., ABB/Open Standard), while driver-derived identity indicates generic middleware roles.
- Several USB communication helpers retain broad `experimental_step` tags due to current tag inventory overlap.

## Proposed new tags
- No proposed new tags were generated in this batch.
- `collect_proposed_tags.py --append`: no rows appended.

## Sampled final device entries (2)
- device: `usb4000_2000_plus`
  - name: USB4000/USB2000+光谱仪
  - description: Ocean Insight 的 USB4000/USB2000+ 系列光谱仪，用于实验室中的光谱采集与光学信号测量。该设备通过 USB 通信，可读取光谱数据、设置积分时间，并查询采集请求与光谱就绪状态，适用于吸收、发射或一般光谱分析实验。
  - tags: [表征设备, 光学与光谱实验, 智慧表征与检测中心, 光谱采集与检测, 光谱仪]
- device: `usb_driver`
  - name: USBTMC 通信组件
  - description: 用于通过 USB Test and Measurement Class（USBTMC）协议与实验仪器通信的软件组件，并非具体物理设备。它负责封装与解析 USBTMC 报文、发送命令、接收响应以及管理底层 USB 文本通信，适合连接支持 USBTMC 的测试测量仪器。
  - tags: [实验执行&合成设备, 表征设备, 实验室自动化与仪器集成, 电子与电气测试, 实验仪器通信与驱动集成, 实验仪器数据采集与联机控制, USB仪器通信接口, 通用字节流仪器通信接口]

## Sampled action summaries (3)
- `usb4000_2000_plus` / `auto-getSpectrumData`: 获取当前采集完成后的光谱数据。
- `usb_driver` / `auto-send`: 向 USBTMC 设备发送命令或文本数据。
- `usb_port` / `auto-readData`: 从指定端点读取指定长度的原始数据。

## Recommended adjustments before next batch
- Add clearer Pass B guidance for USB middleware families to prioritize communication-layer template tags and avoid step-tag over-assignment when the component is explicitly non-physical.
