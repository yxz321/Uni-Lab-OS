# batch_003

## Updated Files

- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/liquid_handler.liquid_handler.laiyu_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/liquid_handler.liquid_handler.prcxi_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/liquid_handler.liquid_handler.revvity_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/neware_battery_test_system.neware_battery_test_system_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/opcua_example.opcua_example_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/opsky_ATR30007.opsky_ATR30007_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/organic_miscellaneous.rotavap.one_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/organic_miscellaneous.separator.homemade_info.txt`

## Uncertain Choices

- `opcua_example` lacked a close existing `device_template_tag`, so I kept existing communication scenes and added one new proposed interface template.
- `separator.homemade` was mapped to `抽提萃取设备`; it fits the liquid-liquid extraction use case, but the taxonomy could eventually benefit from a more explicit liquid-liquid separator template.
- `neware_battery_test_system` was treated as `表征设备` because its evidence is dominated by monitoring and testing rather than assembly or synthesis.

## Newly Proposed Tags

- `P-2201` `OPC UA仪器通信接口` / `OPC UA Instrument Communication Interface` (`device_template_tag`)

## Taxonomy Gaps

- The current catalog appears to lack a direct existing `device_template_tag` for OPC UA protocol interface devices.
