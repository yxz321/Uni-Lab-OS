# batch_002

Status: pending refinement
Updated files:
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/chinwe.separator.chinwe_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/coin_cell_workstation.coincellassemblyworkstation_device_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/gas_handler.gas_source.mock_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/gas_handler.vacuum_pump.mock_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/hotel.hotel.thermo_orbitor_rs2_hotel_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/laiyu_liquid_test.xyz_stepper_controller_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/liquid_handler.liquid_handler_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/liquid_handler.liquid_handler.biomek_info.txt`

Uncertain choices:
- `chinwe.separator.chinwe` spans pump, motor, sensor, and sequencing functions, so I kept multiple device-template tags and added one batch-local controller template.
- `hotel.hotel.thermo_orbitor_rs2_hotel` did not have a close existing scene/template tag for rotating sample storage, so I added one new scene and one new device template.
- `gas_handler.gas_source.mock` had a clear gas-control domain/scene fit but no sufficiently general existing device-template tag, so I added a new gas source template.

Newly proposed tags:
- `P-2101` 简易液路工作站控制器 / Benchtop Fluidic Workstation Controller
- `P-2102` 气体源模块 / Gas Source Module
- `P-2103` 样品存储与自动存取 / Sample Storage & Automated Retrieval
- `P-2104` 自动样品存储柜 / Automated Sample Storage Cabinet
- `P-2105` XYZ运动控制器 / XYZ Motion Controller

Taxonomy gaps noticed:
- Current taxonomy is strong for pumps, liquid handlers, and battery assembly, but weaker for generic gas sources, rotating sample hotels, and compact multi-actuator workstation controllers.
