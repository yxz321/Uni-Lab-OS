# batch_007

Updated files:
- virtual_device.virtual_filter_info.txt
- virtual_device.virtual_gas_source_info.txt
- virtual_device.virtual_heatchill_info.txt
- virtual_device.virtual_multiway_valve_info.txt
- virtual_device.virtual_rotavap_info.txt
- virtual_device.virtual_separator_info.txt
- virtual_device.virtual_solenoid_valve_info.txt

Uncertain tag choices:
- `virtual_gas_source` lacked a precise existing device-template tag, so a new broad `气体源` template tag was proposed.
- `virtual_separator` lacked an existing generic separator template tag, so a new broad `分离器` template tag was proposed.
- `virtual_solenoid_valve` lacked an existing solenoid-valve template tag, so a new broad `电磁阀` template tag was proposed.

Newly proposed tags:
- P-2601 `气体源`
- P-2604 `温度控制与冷热循环`
- P-2606 `流路切换与通道选择`
- P-2607 `蒸发浓缩与溶剂去除`
- P-2608 `液液分离与相分离`
- P-2609 `分离器`
- P-2610 `流路通断与开关控制`
- P-2611 `电磁阀`
- P-2612 `过滤与杂质去除`
- P-2613 `协议测试与流程验证`

Taxonomy gaps noticed:
- The current shared taxonomy does not have several common process-control templates for virtual or generic flow-path hardware, especially gas sources, separators, and solenoid valves.
