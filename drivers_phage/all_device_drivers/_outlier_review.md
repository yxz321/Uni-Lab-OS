# Outlier Review

## access2_backend

- Chosen decorated class: `Access2Backend`
- Final staged id: `access2_backend`
- Final staged folder: `access2_backend`
- `_backend` suffix: retained

| Action | Current location | Implementation action |
| --- | --- | --- |
| `close` | declared on chosen class | decorate in place |
| `load` | declared on chosen class | decorate in place |
| `open` | declared on chosen class | decorate in place |
| `park` | declared on chosen class | decorate in place |
| `send_command` | declared on chosen class | decorate in place |
| `serialize` | declared on chosen class | decorate in place |
| `setup` | declared on chosen class | decorate in place |
| `stop` | declared on chosen class | decorate in place |
| `unload` | declared on chosen class | decorate in place |
| `get_status` | declared on chosen class | decorate in place |
| `bucket_1_remainder` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `set_bucket_1_position_to_current` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `get_bucket_1_position` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `get_position` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `get_tachometer` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `get_home_position` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `get_bucket_locked` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `get_door_open` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `get_door_locked` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `configure_and_initialize` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `set_configuration_data` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `initialize` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `open_door` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `close_door` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `lock_door` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `unlock_door` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `lock_bucket` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `unlock_bucket` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `go_to_bucket1` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `go_to_bucket2` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `go_to_position` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `g_to_rpm` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |
| `spin` | sibling/helper class `VSpinBackend` | add helper-forwarding wrapper |

## li_ha

- Chosen decorated class: `LiHa`
- Final staged id: `li_ha`
- Final staged folder: `li_ha`
- `_backend` suffix: removed

| Action | Current location | Implementation action |
| --- | --- | --- |
| `parse_response` | sibling/helper class `TecanLiquidHandler` | add helper-forwarding wrapper |
| `send_command` | sibling/helper class `TecanLiquidHandler` | add helper-forwarding wrapper |
| `num_channels` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `liha_connected` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `roma_connected` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `pnp_connected` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `mca_connected` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `serialize` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `setup_arm` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `aspirate` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `dispense` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `pick_up_tips` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `drop_tips` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `pick_up_tips96` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `drop_tips96` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `aspirate96` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `dispense96` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `pick_up_resource` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `move_picked_up_resource` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `drop_resource` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `can_pick_up_tip` | sibling/helper class `EVOBackend` | add helper-forwarding wrapper |
| `position_initialization_x` | inherited | add super() wrapper |
| `report_x_param` | inherited | add super() wrapper |
| `report_y_param` | inherited | add super() wrapper |
| `initialize_plunger` | declared on chosen class | decorate in place |
| `report_z_param` | declared on chosen class | decorate in place |
| `report_number_tips` | declared on chosen class | decorate in place |
| `position_absolute_all_axis` | declared on chosen class | decorate in place |
| `position_valve_logical` | declared on chosen class | decorate in place |
| `set_end_speed_plunger` | declared on chosen class | decorate in place |
| `move_plunger_relative` | declared on chosen class | decorate in place |
| `set_detection_mode` | declared on chosen class | decorate in place |
| `set_search_speed` | declared on chosen class | decorate in place |
| `set_search_retract_distance` | declared on chosen class | decorate in place |
| `set_search_submerge` | declared on chosen class | decorate in place |
| `set_search_z_start` | declared on chosen class | decorate in place |
| `set_search_z_max` | declared on chosen class | decorate in place |
| `set_z_travel_height` | declared on chosen class | decorate in place |
| `move_detect_liquid` | declared on chosen class | decorate in place |
| `set_slow_speed_z` | declared on chosen class | decorate in place |
| `set_tracking_distance_z` | declared on chosen class | decorate in place |
| `move_tracking_relative` | declared on chosen class | decorate in place |
| `move_absolute_z` | declared on chosen class | decorate in place |
| `set_stop_speed_plunger` | declared on chosen class | decorate in place |
| `get_disposable_tip` | declared on chosen class | decorate in place |
| `discard_disposable_tip_high` | declared on chosen class | decorate in place |
| `report_r_param` | sibling/helper class `RoMa` | add helper-forwarding wrapper |
| `report_g_param` | sibling/helper class `RoMa` | add helper-forwarding wrapper |
| `set_smooth_move_x` | sibling/helper class `RoMa` | add helper-forwarding wrapper |
| `set_fast_speed_x` | sibling/helper class `RoMa` | add helper-forwarding wrapper |
| `set_fast_speed_y` | sibling/helper class `RoMa` | add helper-forwarding wrapper |
| `set_fast_speed_z` | sibling/helper class `RoMa` | add helper-forwarding wrapper |
| `set_fast_speed_r` | sibling/helper class `RoMa` | add helper-forwarding wrapper |
| `set_vector_coordinate_position` | sibling/helper class `RoMa` | add helper-forwarding wrapper |
| `action_move_vector_coordinate_position` | sibling/helper class `RoMa` | add helper-forwarding wrapper |
| `position_absolute_g` | sibling/helper class `RoMa` | add helper-forwarding wrapper |
| `set_gripper_params` | sibling/helper class `RoMa` | add helper-forwarding wrapper |
| `grip_plate` | sibling/helper class `RoMa` | add helper-forwarding wrapper |
| `set_target_window_class` | sibling/helper class `RoMa` | add helper-forwarding wrapper |

## star_backend

- Chosen decorated class: `STARBackend`
- Final staged id: `star_backend`
- Final staged folder: `star_backend`
- `_backend` suffix: retained

| Action | Current location | Implementation action |
| --- | --- | --- |
| `additional_time_stamp` | declared on chosen class | decorate in place |
| `aspirate` | declared on chosen class | decorate in place |
| `aspirate96` | declared on chosen class | decorate in place |
| `aspirate_core_96` | declared on chosen class | decorate in place |
| `aspirate_pip` | declared on chosen class | decorate in place |
| `can_pick_up_tip` | declared on chosen class | decorate in place |
| `can_reach_position` | declared on chosen class | decorate in place |
| `channel_dispensing_drive_move_to_volume_position` | declared on chosen class | decorate in place |
| `channel_dispensing_drive_request_position` | declared on chosen class | decorate in place |
| `channel_request_y_minimum_spacing` | declared on chosen class | decorate in place |
| `channels_sense_tip_presence` | declared on chosen class | decorate in place |
| `check_fw_string_error` | declared on chosen class | decorate in place |
| `check_type_is_hhc` | declared on chosen class | decorate in place |
| `clld_probe_x_position_using_channel` | declared on chosen class | decorate in place |
| `clld_probe_y_position_using_channel` | declared on chosen class | decorate in place |
| `clld_probe_z_height_using_channel` | declared on chosen class | decorate in place |
| `collapse_gripper_arm` | declared on chosen class | decorate in place |
| `configure_node_names` | declared on chosen class | decorate in place |
| `core_check_resource_exists_at_location_center` | declared on chosen class | decorate in place |
| `core_get_plate` | declared on chosen class | decorate in place |
| `core_move_picked_up_resource` | declared on chosen class | decorate in place |
| `core_move_plate_to_position` | declared on chosen class | decorate in place |
| `core_open_gripper` | declared on chosen class | decorate in place |
| `core_pick_up_resource` | declared on chosen class | decorate in place |
| `core_put_plate` | declared on chosen class | decorate in place |
| `core_read_barcode_of_picked_up_resource` | declared on chosen class | decorate in place |
| `core_release_picked_up_resource` | declared on chosen class | decorate in place |
| `define_tip_needle` | declared on chosen class | decorate in place |
| `disable_cover_control` | declared on chosen class | decorate in place |
| `discard_tip` | declared on chosen class | decorate in place |
| `discard_tips_core96` | declared on chosen class | decorate in place |
| `dispense` | declared on chosen class | decorate in place |
| `dispense96` | declared on chosen class | decorate in place |
| `dispense_core_96` | declared on chosen class | decorate in place |
| `dispense_pip` | declared on chosen class | decorate in place |
| `drain_dual_chamber_system` | declared on chosen class | decorate in place |
| `drop_resource` | declared on chosen class | decorate in place |
| `drop_tips` | declared on chosen class | decorate in place |
| `drop_tips96` | declared on chosen class | decorate in place |
| `empty_tip` | declared on chosen class | decorate in place |
| `empty_tips` | declared on chosen class | decorate in place |
| `enable_cover_control` | declared on chosen class | decorate in place |
| `ensure_can_reach_position` | declared on chosen class | decorate in place |
| `fill_selected_dual_chamber` | declared on chosen class | decorate in place |
| `halt` | declared on chosen class | decorate in place |
| `head96_dispensing_drive_and_squeezer_driver_initialize` | declared on chosen class | decorate in place |
| `head96_dispensing_drive_move_to_home_volume` | declared on chosen class | decorate in place |
| `head96_dispensing_drive_move_to_position` | declared on chosen class | decorate in place |
| `head96_dispensing_drive_request_position_mm` | declared on chosen class | decorate in place |
| `head96_dispensing_drive_request_position_uL` | declared on chosen class | decorate in place |
| `head96_move_to_coordinate` | declared on chosen class | decorate in place |
| `head96_move_to_z_safety` | declared on chosen class | decorate in place |
| `head96_move_x` | declared on chosen class | decorate in place |
| `head96_move_y` | declared on chosen class | decorate in place |
| `head96_move_z` | declared on chosen class | decorate in place |
| `head96_park` | declared on chosen class | decorate in place |
| `head96_request_firmware_version` | declared on chosen class | decorate in place |
| `head96_request_position` | declared on chosen class | decorate in place |
| `head96_request_tip_presence` | declared on chosen class | decorate in place |
| `head96_request_type` | declared on chosen class | decorate in place |
| `initialize_auto_load` | declared on chosen class | decorate in place |
| `initialize_autoload` | declared on chosen class | decorate in place |
| `initialize_core_96_head` | declared on chosen class | decorate in place |
| `initialize_dual_pump_station_valves` | declared on chosen class | decorate in place |
| `initialize_hhc` | declared on chosen class | decorate in place |
| `initialize_iswap` | declared on chosen class | decorate in place |
| `initialize_pip` | declared on chosen class | decorate in place |
| `initialize_pipetting_channels` | declared on chosen class | decorate in place |
| `iswap_close_gripper` | declared on chosen class | decorate in place |
| `iswap_dangerous_release_break` | declared on chosen class | decorate in place |
| `iswap_get_plate` | declared on chosen class | decorate in place |
| `iswap_initialize_z_axis` | declared on chosen class | decorate in place |
| `iswap_minimum_traversal_height` | declared on chosen class | decorate in place |
| `iswap_move_picked_up_resource` | declared on chosen class | decorate in place |
| `iswap_open_gripper` | declared on chosen class | decorate in place |
| `iswap_put_plate` | declared on chosen class | decorate in place |
| `iswap_reengage_break` | declared on chosen class | decorate in place |
| `iswap_rotate` | declared on chosen class | decorate in place |
| `iswap_rotation_drive_request_y` | declared on chosen class | decorate in place |
| `load_carrier` | declared on chosen class | decorate in place |
| `load_carrier_from_autoload_belt` | declared on chosen class | decorate in place |
| `load_carrier_from_tray_and_scan_carrier_barcode` | declared on chosen class | decorate in place |
| `lock_cover` | declared on chosen class | decorate in place |
| `move_96head_to_coordinate` | declared on chosen class | decorate in place |
| `move_all_channels_in_z_safety` | declared on chosen class | decorate in place |
| `move_all_pipetting_channels_to_defined_position` | declared on chosen class | decorate in place |
| `move_auto_load_to_z_save_position` | declared on chosen class | decorate in place |
| `move_autoload_to_safe_z_position` | declared on chosen class | decorate in place |
| `move_autoload_to_save_z_position` | declared on chosen class | decorate in place |
| `move_autoload_to_slot` | declared on chosen class | decorate in place |
| `move_autoload_to_track` | declared on chosen class | decorate in place |
| `move_channel_x` | declared on chosen class | decorate in place |
| `move_channel_x_relative` | declared on chosen class | decorate in place |
| `move_channel_y` | declared on chosen class | decorate in place |
| `move_channel_y_relative` | declared on chosen class | decorate in place |
| `move_channel_z` | declared on chosen class | decorate in place |
| `move_channel_z_relative` | declared on chosen class | decorate in place |
| `move_core_96_head_to_defined_position` | declared on chosen class | decorate in place |
| `move_core_96_head_x` | declared on chosen class | decorate in place |
| `move_core_96_head_y` | declared on chosen class | decorate in place |
| `move_core_96_head_z` | declared on chosen class | decorate in place |
| `move_core_96_to_safe_position` | declared on chosen class | decorate in place |
| `move_iswap_x` | declared on chosen class | decorate in place |
| `move_iswap_x_relative` | declared on chosen class | decorate in place |
| `move_iswap_y` | declared on chosen class | decorate in place |
| `move_iswap_y_relative` | declared on chosen class | decorate in place |
| `move_iswap_z` | declared on chosen class | decorate in place |
| `move_iswap_z_relative` | declared on chosen class | decorate in place |
| `move_left_x_arm_to_position_with_all_attached_components_in_z_safety_position` | declared on chosen class | decorate in place |
| `move_picked_up_resource` | declared on chosen class | decorate in place |
| `move_plate_to_position` | declared on chosen class | decorate in place |
| `move_right_x_arm_to_position_with_all_attached_components_in_z_safety_position` | declared on chosen class | decorate in place |
| `occupy_and_provide_area_for_external_access` | declared on chosen class | decorate in place |
| `open_not_initialized_gripper` | declared on chosen class | decorate in place |
| `park_autoload` | declared on chosen class | decorate in place |
| `park_iswap` | declared on chosen class | decorate in place |
| `pick_up_core_gripper_tools` | declared on chosen class | decorate in place |
| `pick_up_resource` | declared on chosen class | decorate in place |
| `pick_up_tip` | declared on chosen class | decorate in place |
| `pick_up_tips` | declared on chosen class | decorate in place |
| `pick_up_tips96` | declared on chosen class | decorate in place |
| `pick_up_tips_core96` | declared on chosen class | decorate in place |
| `pierce_foil` | declared on chosen class | decorate in place |
| `plld_probe_z_height_using_channel` | declared on chosen class | decorate in place |
| `position_channels_in_y_direction` | declared on chosen class | decorate in place |
| `position_channels_in_z_direction` | declared on chosen class | decorate in place |
| `position_components_for_free_iswap_y_range` | declared on chosen class | decorate in place |
| `position_left_x_arm_` | declared on chosen class | decorate in place |
| `position_max_free_y_for_n` | declared on chosen class | decorate in place |
| `position_right_x_arm_` | declared on chosen class | decorate in place |
| `position_single_pipetting_channel_in_y_direction` | declared on chosen class | decorate in place |
| `position_single_pipetting_channel_in_z_direction` | declared on chosen class | decorate in place |
| `pre_initialize_instrument` | declared on chosen class | decorate in place |
| `prepare_for_manual_channel_operation` | declared on chosen class | decorate in place |
| `prepare_iswap_teaching` | declared on chosen class | decorate in place |
| `probe_liquid_heights` | declared on chosen class | decorate in place |
| `probe_liquid_volumes` | declared on chosen class | decorate in place |
| `put_core` | declared on chosen class | decorate in place |
| `query_whether_temperature_reached_at_hhc` | declared on chosen class | decorate in place |
| `release_all_occupied_areas` | declared on chosen class | decorate in place |
| `release_occupied_area` | declared on chosen class | decorate in place |
| `request_additional_timestamp_data` | declared on chosen class | decorate in place |
| `request_auto_load_slot_position` | declared on chosen class | decorate in place |
| `request_autoload_initialization_status` | declared on chosen class | decorate in place |
| `request_autoload_track` | declared on chosen class | decorate in place |
| `request_autoload_type` | declared on chosen class | decorate in place |
| `request_core_96_head_channel_tadm_error_status` | declared on chosen class | decorate in place |
| `request_core_96_head_channel_tadm_status` | declared on chosen class | decorate in place |
| `request_core_96_head_initialization_status` | declared on chosen class | decorate in place |
| `request_cover_open` | declared on chosen class | decorate in place |
| `request_deck_data` | declared on chosen class | decorate in place |
| `request_device_serial_number` | declared on chosen class | decorate in place |
| `request_download_date` | declared on chosen class | decorate in place |
| `request_eeprom_data_correctness` | declared on chosen class | decorate in place |
| `request_electronic_board_type` | declared on chosen class | decorate in place |
| `request_error_code` | declared on chosen class | decorate in place |
| `request_extended_configuration` | declared on chosen class | decorate in place |
| `request_firmware_version` | declared on chosen class | decorate in place |
| `request_installation_data` | declared on chosen class | decorate in place |
| `request_instrument_initialization_status` | declared on chosen class | decorate in place |
| `request_iswap_in_parking_position` | declared on chosen class | decorate in place |
| `request_iswap_initialization_status` | declared on chosen class | decorate in place |
| `request_iswap_position` | declared on chosen class | decorate in place |
| `request_iswap_rotation_drive_orientation` | declared on chosen class | decorate in place |
| `request_iswap_rotation_drive_position_increments` | declared on chosen class | decorate in place |
| `request_iswap_version` | declared on chosen class | decorate in place |
| `request_iswap_wrist_drive_orientation` | declared on chosen class | decorate in place |
| `request_iswap_wrist_drive_position_increments` | declared on chosen class | decorate in place |
| `request_left_x_arm_last_collision_type` | declared on chosen class | decorate in place |
| `request_left_x_arm_position` | declared on chosen class | decorate in place |
| `request_machine_configuration` | declared on chosen class | decorate in place |
| `request_master_status` | declared on chosen class | decorate in place |
| `request_maximal_ranges_of_x_drives` | declared on chosen class | decorate in place |
| `request_name_of_last_faulty_parameter` | declared on chosen class | decorate in place |
| `request_node_names` | declared on chosen class | decorate in place |
| `request_number_of_presence_sensors_installed` | declared on chosen class | decorate in place |
| `request_parameter_value` | declared on chosen class | decorate in place |
| `request_pip_channel_validation_status` | declared on chosen class | decorate in place |
| `request_pip_channel_version` | declared on chosen class | decorate in place |
| `request_pip_height_last_lld` | declared on chosen class | decorate in place |
| `request_plate_in_iswap` | declared on chosen class | decorate in place |
| `request_position_of_core_96_head` | declared on chosen class | decorate in place |
| `request_presence_of_carriers_on_deck` | declared on chosen class | decorate in place |
| `request_presence_of_carriers_on_loading_tray` | declared on chosen class | decorate in place |
| `request_presence_of_single_carrier_on_loading_tray` | declared on chosen class | decorate in place |
| `request_present_wrap_size_of_installed_arms` | declared on chosen class | decorate in place |
| `request_probe_z_position` | declared on chosen class | decorate in place |
| `request_pump_settings` | declared on chosen class | decorate in place |
| `request_right_x_arm_last_collision_type` | declared on chosen class | decorate in place |
| `request_right_x_arm_position` | declared on chosen class | decorate in place |
| `request_single_carrier_presence` | declared on chosen class | decorate in place |
| `request_supply_voltage` | declared on chosen class | decorate in place |
| `request_tadm_status` | declared on chosen class | decorate in place |
| `request_technical_status_of_assemblies` | declared on chosen class | decorate in place |
| `request_tip_bottom_z_position` | declared on chosen class | decorate in place |
| `request_tip_len_on_channel` | declared on chosen class | decorate in place |
| `request_tip_presence` | declared on chosen class | decorate in place |
| `request_tip_presence_in_core_96_head` | declared on chosen class | decorate in place |
| `request_verification_data` | declared on chosen class | decorate in place |
| `request_volume_in_tip` | declared on chosen class | decorate in place |
| `request_x_pos_channel_n` | declared on chosen class | decorate in place |
| `request_xl_channel_validation_status` | declared on chosen class | decorate in place |
| `request_y_pos_channel_n` | declared on chosen class | decorate in place |
| `request_z_pos_channel_n` | declared on chosen class | decorate in place |
| `reset_output` | declared on chosen class | decorate in place |
| `return_core_gripper_tools` | declared on chosen class | decorate in place |
| `rotate_iswap_rotation_drive` | declared on chosen class | decorate in place |
| `rotate_iswap_wrist` | declared on chosen class | decorate in place |
| `save_all_cycle_counters` | declared on chosen class | decorate in place |
| `save_download_date` | declared on chosen class | decorate in place |
| `save_pip_channel_validation_status` | declared on chosen class | decorate in place |
| `save_technical_status_of_assemblies` | declared on chosen class | decorate in place |
| `save_xl_channel_validation_status` | declared on chosen class | decorate in place |
| `search_for_teach_in_signal_using_pipetting_channel_n_in_x_direction` | declared on chosen class | decorate in place |
| `send_hhs_command` | declared on chosen class | decorate in place |
| `set_1d_barcode_type` | declared on chosen class | decorate in place |
| `set_barcode_type` | declared on chosen class | decorate in place |
| `set_carrier_monitoring` | declared on chosen class | decorate in place |
| `set_cover_output` | declared on chosen class | decorate in place |
| `set_deck_data` | declared on chosen class | decorate in place |
| `set_instrument_configuration` | declared on chosen class | decorate in place |
| `set_loading_indicators` | declared on chosen class | decorate in place |
| `set_minimum_channel_traversal_height` | declared on chosen class | decorate in place |
| `set_minimum_iswap_traversal_height` | declared on chosen class | decorate in place |
| `set_minimum_traversal_height` | declared on chosen class | decorate in place |
| `set_not_stop` | declared on chosen class | decorate in place |
| `set_single_step_mode` | declared on chosen class | decorate in place |
| `set_x_offset_x_axis_core_96_head` | declared on chosen class | decorate in place |
| `set_x_offset_x_axis_core_nano_pipettor_head` | declared on chosen class | decorate in place |
| `set_x_offset_x_axis_iswap` | declared on chosen class | decorate in place |
| `setup` | declared on chosen class | decorate in place |
| `slow_iswap` | declared on chosen class | decorate in place |
| `spread_pip_channels` | declared on chosen class | decorate in place |
| `start_temperature_control_at_hhc` | declared on chosen class | decorate in place |
| `step_off_foil` | declared on chosen class | decorate in place |
| `stop` | declared on chosen class | decorate in place |
| `stop_temperature_control_at_hhc` | declared on chosen class | decorate in place |
| `store_installation_data` | declared on chosen class | decorate in place |
| `store_verification_data` | declared on chosen class | decorate in place |
| `take_carrier_out_to_autoload_belt` | declared on chosen class | decorate in place |
| `trigger_next_step` | declared on chosen class | decorate in place |
| `unload_carrier` | declared on chosen class | decorate in place |
| `unload_carrier_after_carrier_barcode_scanning` | declared on chosen class | decorate in place |
| `unlock_cover` | declared on chosen class | decorate in place |
| `verify_and_wait_for_carriers` | declared on chosen class | decorate in place |
| `ztouch_probe_z_height_using_channel` | declared on chosen class | decorate in place |
| `num_arms` | declared on chosen class | decorate in place |
| `head96_installed` | declared on chosen class | decorate in place |
| `unsafe` | declared on chosen class | decorate in place |
| `num_channels` | declared on chosen class | decorate in place |
| `iswap_traversal_height` | declared on chosen class | decorate in place |
| `module_id_length` | declared on chosen class | decorate in place |
| `extended_conf` | declared on chosen class | decorate in place |
| `iswap_parked` | declared on chosen class | decorate in place |
| `core_parked` | declared on chosen class | decorate in place |
| `get_iswap_version` | declared on chosen class | decorate in place |
| `get_id_from_fw_response` | declared on chosen class | decorate in place |
| `setup_done` | declared on chosen class | decorate in place |
| `get_core` | declared on chosen class | decorate in place |
| `get_logic_iswap_position` | declared on chosen class | decorate in place |
| `mm_to_y_drive_increment` | declared on chosen class | decorate in place |
| `y_drive_increment_to_mm` | declared on chosen class | decorate in place |
| `mm_to_z_drive_increment` | declared on chosen class | decorate in place |
| `z_drive_increment_to_mm` | declared on chosen class | decorate in place |
| `dispensing_drive_vol_to_increment` | declared on chosen class | decorate in place |
| `dispensing_drive_increment_to_volume` | declared on chosen class | decorate in place |
| `dispensing_drive_mm_to_increment` | declared on chosen class | decorate in place |
| `dispensing_drive_increment_to_mm` | declared on chosen class | decorate in place |
| `dispensing_drive_vol_to_mm` | declared on chosen class | decorate in place |
| `dispensing_drive_mm_to_vol` | declared on chosen class | decorate in place |
| `channel_id` | declared on chosen class | decorate in place |
| `get_channels_y_positions` | declared on chosen class | decorate in place |
| `get_channels_z_positions` | declared on chosen class | decorate in place |
| `get_temperature_at_hhc` | declared on chosen class | decorate in place |
| `put_in_hotel` | sibling/helper class `UnSafe` | add helper-forwarding wrapper |
| `get_from_hotel` | sibling/helper class `UnSafe` | add helper-forwarding wrapper |
| `violently_shoot_down_tip` | sibling/helper class `UnSafe` | add helper-forwarding wrapper |

## v_spin_backend

- Chosen decorated class: `VSpinBackend`
- Final staged id: `v_spin_backend`
- Final staged folder: `v_spin_backend`
- `_backend` suffix: retained

| Action | Current location | Implementation action |
| --- | --- | --- |
| `close_door` | declared on chosen class | decorate in place |
| `configure_and_initialize` | declared on chosen class | decorate in place |
| `go_to_bucket1` | declared on chosen class | decorate in place |
| `go_to_bucket2` | declared on chosen class | decorate in place |
| `go_to_position` | declared on chosen class | decorate in place |
| `initialize` | declared on chosen class | decorate in place |
| `lock_bucket` | declared on chosen class | decorate in place |
| `lock_door` | declared on chosen class | decorate in place |
| `open_door` | declared on chosen class | decorate in place |
| `set_bucket_1_position_to_current` | declared on chosen class | decorate in place |
| `set_configuration_data` | declared on chosen class | decorate in place |
| `setup` | declared on chosen class | decorate in place |
| `spin` | declared on chosen class | decorate in place |
| `stop` | declared on chosen class | decorate in place |
| `unlock_bucket` | declared on chosen class | decorate in place |
| `unlock_door` | declared on chosen class | decorate in place |
| `send_command` | sibling/helper class `Access2Backend` | add helper-forwarding wrapper |
| `serialize` | sibling/helper class `Access2Backend` | add helper-forwarding wrapper |
| `get_status` | sibling/helper class `Access2Backend` | add helper-forwarding wrapper |
| `park` | sibling/helper class `Access2Backend` | add helper-forwarding wrapper |
| `load` | sibling/helper class `Access2Backend` | add helper-forwarding wrapper |
| `unload` | sibling/helper class `Access2Backend` | add helper-forwarding wrapper |
| `bucket_1_remainder` | declared on chosen class | decorate in place |
| `get_bucket_1_position` | declared on chosen class | decorate in place |
| `get_position` | declared on chosen class | decorate in place |
| `get_tachometer` | declared on chosen class | decorate in place |
| `get_home_position` | declared on chosen class | decorate in place |
| `get_bucket_locked` | declared on chosen class | decorate in place |
| `get_door_open` | declared on chosen class | decorate in place |
| `get_door_locked` | declared on chosen class | decorate in place |
| `g_to_rpm` | declared on chosen class | decorate in place |
