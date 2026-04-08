# batch_005

Status: completed

Updated files:
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/robot_arm.robotic_arm.SCARA_with_slider.moveit.virtual_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/robot_arm.robotic_arm.UR_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/robot_arm.robotic_arm.elite_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/robot_gripper.gripper.misumi_rz_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/robot_gripper.gripper.mock_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/robot_linear_motion.linear_motion.grbl_info.txt`
- `/home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/existing_device_infos/robot_linear_motion.linear_motion.toyo_xyz.sim_info.txt`

Uncertain choices:
- `robot_arm.robotic_arm.elite` 的描述很短，主要依据设备名称和 Modbus 动作名补充为机械臂自动化与运动控制相关标签。
- `robot_gripper.gripper.mock` 同时保留了仿真调试场景标签和真实夹爪模板标签，以提高按夹爪类关键词检索时的召回率。
- `robot_linear_motion.linear_motion.grbl` 兼具 CNC 加工平台和多轴定位平台属性，因此同时使用了 `数控固件运动控制器` 与 `电动定位台` 模板标签。

Newly proposed tags used:
- none

Taxonomy gaps noticed:
- 现有标签中缺少比 `机械臂` 更贴近 `机械臂+滑轨一体化系统` 的通用设备模板。
- 现有模板也缺少比 `数控固件运动控制器` 更贴近 `三轴数控运动平台` 整机形态的通用标签。
