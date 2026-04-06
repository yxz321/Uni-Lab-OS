# Workflow v4 Benchmark Summary

## Usage

- `Vendor2/GPT-5.2`: Pass A total 21593 tokens, Pass B total 61685 tokens, combined 83278 tokens
- `Vendor2/GPT-5.3-codex`: Pass A total 22110 tokens, Pass B total 59520 tokens, combined 81630 tokens

## bio_shake

### Device Name

- `Vendor2/GPT-5.2`: BioShake microplate thermoshaker
- `Vendor2/GPT-5.3-codex`: BioShake microplate thermoshaker

### Device Description

- `Vendor2/GPT-5.2`: BioShake is an integrated microplate heater shaker used to mix microplates by orbital shaking while controlling the plate temperature. It can clamp/lock the plate to prevent movement during shaking, and is commonly used for incubation, enzymatic reactions, mixing, and sample preparation workflows.
- `Vendor2/GPT-5.3-codex`: BioShake is a benchtop microplate heater shaker for temperature-controlled incubation and shaking/mixing of plate-based samples, with plate locking support. It is commonly used in molecular biology and biochemistry workflows for incubation, dissolution, reaction mixing, and sample preparation.

### Action: `auto-deactivate`

- `Vendor2/GPT-5.2`: Deactivate temperature control (stop heating/temperature regulation)
- `Vendor2/GPT-5.3-codex`: Deactivate temperature control.

### Action: `auto-home`

- `Vendor2/GPT-5.2`: Home the device to its reference position
- `Vendor2/GPT-5.3-codex`: Home the device to its initial reference position.

### Action: `auto-lock_plate`

- `Vendor2/GPT-5.2`: Lock/clamp the microplate
- `Vendor2/GPT-5.3-codex`: Lock the microplate.

### Action: `auto-reset`

- `Vendor2/GPT-5.2`: Reset the device (recover from an error or stuck state)
- `Vendor2/GPT-5.3-codex`: Reset the device to clear error or stuck states.

### Action: `auto-set_temperature`

- `Vendor2/GPT-5.2`: set the temperature setpoint (start/maintain temperature control)
- `Vendor2/GPT-5.3-codex`: Set and start temperature control to the target temperature.

### Action: `auto-setup`

- `Vendor2/GPT-5.2`: Initialize the device (reset and home it to a ready-to-run state)
- `Vendor2/GPT-5.3-codex`: Run setup initialization (reset and home).

### Action: `auto-shake`

- `Vendor2/GPT-5.2`: Start shaking at the specified speed (and acceleration)
- `Vendor2/GPT-5.3-codex`: Start shaking/mixing at the set speed (and acceleration).

### Action: `auto-stop`

- `Vendor2/GPT-5.2`: Stop the device (overall stop)
- `Vendor2/GPT-5.3-codex`: Stop current device operation.

### Action: `auto-stop_shaking`

- `Vendor2/GPT-5.2`: Stop shaking (optionally with a specified deceleration)
- `Vendor2/GPT-5.3-codex`: Stop shaking with the specified deceleration.

### Action: `auto-unlock_plate`

- `Vendor2/GPT-5.2`: Unlock/release the microplate
- `Vendor2/GPT-5.3-codex`: Unlock the microplate.

### Action: `auto-supports_locking`

- `Vendor2/GPT-5.2`: get whether plate locking is supported
- `Vendor2/GPT-5.3-codex`: Get whether plate locking is supported.

### Action: `auto-supports_active_cooling`

- `Vendor2/GPT-5.2`: get whether active cooling is supported
- `Vendor2/GPT-5.3-codex`: Get whether active cooling is supported.

### Action: `auto-get_current_temperature`

- `Vendor2/GPT-5.2`: get the current temperature
- `Vendor2/GPT-5.3-codex`: Get the current temperature.

### Tags

- `Vendor2/GPT-5.2`: 实验执行&合成设备, 生命体系, 溶液配制与反应, 细胞生物学研究, 热混匀仪
- `Vendor2/GPT-5.3-codex`: 备料&前处理设备, 实验执行&合成设备, 生命体系, 溶液配制与反应, 基因编辑、分子生物学与育种, 细胞生物学研究, 恒温摇床, 热混匀仪

## cc_core

### Device Name

- `Vendor2/GPT-5.3-codex`: Central Controller (CC)

### Device Description

- `Vendor2/GPT-5.3-codex`: This is a central timing and sequence-control instrument for quantum experiments. It coordinates CCIO-type submodules, runs sequence programs, starts/stops real-time control flow, and provides digital I/O calibration, delay adjustment, and status monitoring. It is commonly used for real-time control and synchronization in superconducting-qubit labs.

### Action: `auto-assemble`

- `Vendor2/GPT-5.3-codex`: Assemble the sequence program string.

### Action: `auto-assemble_and_start`

- `Vendor2/GPT-5.3-codex`: Assemble the sequence program and start the sequencers.

### Action: `auto-calibrate_dio`

- `Vendor2/GPT-5.3-codex`: Run digital I/O calibration for the specified CCIO.

### Action: `auto-debug_get_ccio_reg`

- `Vendor2/GPT-5.3-codex`: Read a CCIO debug register.

### Action: `auto-debug_get_ccio_trace`

- `Vendor2/GPT-5.3-codex`: Read CCIO debug trace data.

### Action: `auto-debug_get_traces`

- `Vendor2/GPT-5.3-codex`: Read debug traces for multiple CCIOs by mask.

### Action: `auto-debug_marker_in`

- `Vendor2/GPT-5.3-codex`: Route debug marker to an input bit.

### Action: `auto-debug_marker_off`

- `Vendor2/GPT-5.3-codex`: Turn off debug marker output.

### Action: `auto-debug_marker_out`

- `Vendor2/GPT-5.3-codex`: Route debug marker to an output bit.

### Action: `auto-debug_set_ccio_trace_on`

- `Vendor2/GPT-5.3-codex`: Enable trace capture for a CCIO timing unit.

### Action: `auto-print_status_operation`

- `Vendor2/GPT-5.3-codex`: Print operation status information.

### Action: `auto-print_status_questionable`

- `Vendor2/GPT-5.3-codex`: Print questionable status information.

### Action: `auto-sequence_program_assemble`

- `Vendor2/GPT-5.3-codex`: set sequence program string for assembly

### Action: `auto-set_q1_reg`

- `Vendor2/GPT-5.3-codex`: set Q1 register value

### Action: `auto-set_seqbar_cnt`

- `Vendor2/GPT-5.3-codex`: Set the sequence barrier count value.

### Action: `auto-set_status_operation_run_enable`

- `Vendor2/GPT-5.3-codex`: set operation run status enable

### Action: `auto-set_status_questionable_bplink_enable`

- `Vendor2/GPT-5.3-codex`: set questionable bplink status enable

### Action: `auto-set_status_questionable_config_enable`

- `Vendor2/GPT-5.3-codex`: set questionable config status enable

### Action: `auto-set_status_questionable_frequency_enable`

- `Vendor2/GPT-5.3-codex`: set questionable frequency status enable

### Action: `auto-set_status_questionable_instrument_enable`

- `Vendor2/GPT-5.3-codex`: set questionable instrument status enable

### Action: `auto-set_status_questionable_instrument_idetail_bplink_enable`

- `Vendor2/GPT-5.3-codex`: set instrument idetail bplink status enable

### Action: `auto-set_status_questionable_instrument_idetail_config_enable`

- `Vendor2/GPT-5.3-codex`: set instrument idetail config status enable

### Action: `auto-set_status_questionable_instrument_idetail_diocal_enable`

- `Vendor2/GPT-5.3-codex`: set instrument idetail diocal status enable

### Action: `auto-set_status_questionable_instrument_idetail_freq_enable`

- `Vendor2/GPT-5.3-codex`: set instrument idetail freq status enable

### Action: `auto-set_status_questionable_instrument_isummary_enable`

- `Vendor2/GPT-5.3-codex`: set instrument isummary status enable

### Action: `auto-set_vsm_delay_fall`

- `Vendor2/GPT-5.3-codex`: set VSM fall delay count

### Action: `auto-set_vsm_delay_rise`

- `Vendor2/GPT-5.3-codex`: set VSM rise delay count

### Action: `auto-start`

- `Vendor2/GPT-5.3-codex`: Start the CC sequencers.

### Action: `auto-status_preset`

- `Vendor2/GPT-5.3-codex`: Apply status preset and enable SCPI event reporting.

### Action: `auto-stop`

- `Vendor2/GPT-5.3-codex`: Stop the CC sequencers.

### Action: `auto-get_sequence_program_assemble`

- `Vendor2/GPT-5.3-codex`: get sequence program string for assembly

### Action: `auto-get_assembler_success`

- `Vendor2/GPT-5.3-codex`: get assembler success status

### Action: `auto-get_assembler_log`

- `Vendor2/GPT-5.3-codex`: get assembler log

### Action: `auto-get_q1_reg`

- `Vendor2/GPT-5.3-codex`: get Q1 register value

### Action: `auto-get_calibrate_dio_success`

- `Vendor2/GPT-5.3-codex`: get DIO calibration success status

### Action: `auto-get_calibrate_dio_status`

- `Vendor2/GPT-5.3-codex`: get DIO calibration status

### Action: `auto-get_calibrate_dio_read_index`

- `Vendor2/GPT-5.3-codex`: get DIO calibration read index

### Action: `auto-get_calibrate_dio_margin`

- `Vendor2/GPT-5.3-codex`: get DIO calibration margin

### Action: `auto-get_vsm_delay_rise`

- `Vendor2/GPT-5.3-codex`: get VSM rise delay count

### Action: `auto-get_vsm_delay_fall`

- `Vendor2/GPT-5.3-codex`: get VSM fall delay count

### Action: `auto-get_status_questionable_frequency`

- `Vendor2/GPT-5.3-codex`: get questionable frequency status

### Action: `auto-get_status_questionable_frequency_enable`

- `Vendor2/GPT-5.3-codex`: get questionable frequency status enable

### Action: `auto-get_status_questionable_config`

- `Vendor2/GPT-5.3-codex`: get questionable config status

### Action: `auto-get_status_questionable_config_enable`

- `Vendor2/GPT-5.3-codex`: get questionable config status enable

### Action: `auto-get_status_questionable_bplink`

- `Vendor2/GPT-5.3-codex`: get questionable bplink status

### Action: `auto-get_status_questionable_bplink_enable`

- `Vendor2/GPT-5.3-codex`: get questionable bplink status enable

### Action: `auto-get_status_operation_run`

- `Vendor2/GPT-5.3-codex`: get operation run status

### Action: `auto-get_status_operation_run_enable`

- `Vendor2/GPT-5.3-codex`: get operation run status enable

### Action: `auto-get_status_questionable_instrument`

- `Vendor2/GPT-5.3-codex`: get questionable instrument status

### Action: `auto-get_status_questionable_instrument_enable`

- `Vendor2/GPT-5.3-codex`: get questionable instrument status enable

### Action: `auto-get_status_questionable_instrument_isummary`

- `Vendor2/GPT-5.3-codex`: get instrument isummary status

### Action: `auto-get_status_questionable_instrument_isummary_enable`

- `Vendor2/GPT-5.3-codex`: get instrument isummary status enable

### Action: `auto-get_status_questionable_instrument_idetail_freq`

- `Vendor2/GPT-5.3-codex`: get instrument idetail freq status

### Action: `auto-get_status_questionable_instrument_idetail_freq_enable`

- `Vendor2/GPT-5.3-codex`: get instrument idetail freq status enable

### Action: `auto-get_status_questionable_instrument_idetail_config`

- `Vendor2/GPT-5.3-codex`: get instrument idetail config status

### Action: `auto-get_status_questionable_instrument_idetail_config_enable`

- `Vendor2/GPT-5.3-codex`: get instrument idetail config status enable

### Action: `auto-get_status_questionable_instrument_idetail_bplink`

- `Vendor2/GPT-5.3-codex`: get instrument idetail bplink status

### Action: `auto-get_status_questionable_instrument_idetail_bplink_enable`

- `Vendor2/GPT-5.3-codex`: get instrument idetail bplink status enable

### Action: `auto-get_status_questionable_instrument_idetail_diocal`

- `Vendor2/GPT-5.3-codex`: get instrument idetail diocal status

### Action: `auto-get_status_questionable_instrument_idetail_diocal_enable`

- `Vendor2/GPT-5.3-codex`: get instrument idetail diocal status enable

### Tags

- `Vendor2/GPT-5.3-codex`: 实验执行&合成设备, 量子信息与精密测控, 超导量子比特实验, 中央时序序列控制器

## cryo_tel_gt

### Device Name

- `Vendor2/GPT-5.3-codex`: Sunpower CryoTel GT Cryocooler

### Device Description

- `Vendor2/GPT-5.3-codex`: The CryoTel GT is a laboratory cryocooler used to provide a stable low-temperature environment for experimental loads. It supports temperature-control or power-control operation, allows monitoring of current temperature and power, and lets users set temperature/power targets and limits for low-temperature testing and sample cooling.

### Action: `auto-at_temperature_band`

- `Vendor2/GPT-5.3-codex`: Get/set the at-temperature band (K).

### Action: `auto-control_mode`

- `Vendor2/GPT-5.3-codex`: Get/set the control mode (power mode or temperature mode).

### Action: `auto-ki`

- `Vendor2/GPT-5.3-codex`: Get/set the temperature-loop integral constant (Ki).

### Action: `auto-kp`

- `Vendor2/GPT-5.3-codex`: Get/set the temperature-loop proportional constant (Kp).

### Action: `auto-power_max`

- `Vendor2/GPT-5.3-codex`: Get/set the user-defined maximum power limit (W).

### Action: `auto-power_min`

- `Vendor2/GPT-5.3-codex`: Get/set the user-defined minimum power limit (W).

### Action: `auto-power_setpoint`

- `Vendor2/GPT-5.3-codex`: Get/set the power setpoint (W).

### Action: `auto-query`

- `Vendor2/GPT-5.3-codex`: Send a query command, optionally set a value, and read the response.

### Action: `auto-query_multiline`

- `Vendor2/GPT-5.3-codex`: Send a multiline query command and read multiline responses.

### Action: `auto-reset`

- `Vendor2/GPT-5.3-codex`: Reset the cryocooler to factory defaults.

### Action: `auto-save_control_mode`

- `Vendor2/GPT-5.3-codex`: Save the current control mode as the default mode.

### Action: `auto-sendcmd`

- `Vendor2/GPT-5.3-codex`: Send a raw command to the cryocooler.

### Action: `auto-stop`

- `Vendor2/GPT-5.3-codex`: Get/set the stop state (stop/start).

### Action: `auto-stop_mode`

- `Vendor2/GPT-5.3-codex`: Get/set the stop mode (host or digital I/O).

### Action: `auto-temperature_setpoint`

- `Vendor2/GPT-5.3-codex`: Get/set the temperature setpoint (K).

### Action: `auto-thermostat`

- `Vendor2/GPT-5.3-codex`: Get/set the thermostat mode on/off state.

### Action: `auto-errors`

- `Vendor2/GPT-5.3-codex`: Get the list of currently active error codes.

### Action: `auto-power`

- `Vendor2/GPT-5.3-codex`: Get the current power (W).

### Action: `auto-power_current_and_limits`

- `Vendor2/GPT-5.3-codex`: Get current power and power limit values (W).

### Action: `auto-serial_number`

- `Vendor2/GPT-5.3-codex`: Get the device serial number and revision information.

### Action: `auto-state`

- `Vendor2/GPT-5.3-codex`: Get the controller parameter/state list.

### Action: `auto-temperature`

- `Vendor2/GPT-5.3-codex`: Get the current temperature (K).

### Action: `auto-thermostat_status`

- `Vendor2/GPT-5.3-codex`: Get the current thermostat status (on/off).

### Tags

- `Vendor2/GPT-5.3-codex`: 表征设备, 备料&前处理设备, 智慧表征与检测中心, 物化表征测试中心, 冷热水机, 低温制冷机

## cvd_control

### Device Name

- `Vendor2/GPT-5.3-codex`: Chemical Vapor Deposition (CVD) System Controller

### Device Description

- `Vendor2/GPT-5.3-codex`: A process control interface for a chemical vapor deposition (CVD) setup, typically handling temperature and multi-gas flow recipes for run control and monitoring. It is used in lab workflows to manage recipe files, apply setpoints, and view process trend plots during CVD thin-film growth experiments.

### Action: `auto-return_ui_fields`

- `Vendor2/GPT-5.3-codex`: Return the current process-parameter field values from the UI.

### Action: `auto-save_recipe`

- `Vendor2/GPT-5.3-codex`: Save the current CVD process recipe to a file (including metadata and parameter table).

### Action: `auto-open_recipe`

- `Vendor2/GPT-5.3-codex`: Open a CVD process recipe file and load it into the control interface.

### Action: `auto-update_plot`

- `Vendor2/GPT-5.3-codex`: Update the process trend plots (such as time-varying gas flow channels).

### Action: `auto-start_recipe`

- `Vendor2/GPT-5.3-codex`: Start recipe execution and begin process monitoring.

### Action: `auto-stop_recipe`

- `Vendor2/GPT-5.3-codex`: Stop the current recipe run.

### Action: `auto-apply_setpoints`

- `Vendor2/GPT-5.3-codex`: Apply process setpoints (e.g., temperature/flow) to the system.

### Tags

- `Vendor2/GPT-5.3-codex`: 实验执行&合成设备, 表面/薄膜体系, 涂层材料, 化学气相沉积设备

## cytomat_backend

### Device Name

- `Vendor2/GPT-5.3-codex`: Cytomat Automated Microplate Incubator-Storage System

### Device Description

- `Vendor2/GPT-5.3-codex`: This device is an automated microplate incubator and storage unit for laboratory workflows. It maintains controlled temperature, CO2, O2, and humidity conditions, and uses internal handling mechanics to move plates between storage, wait, transfer, and exposed positions. It also supports barcode reading and shaking incubation.

### Action: `auto-action_exposed_to_storage`

- `Vendor2/GPT-5.3-codex`: Move a microplate from the exposed external position back to a storage position.

### Action: `auto-action_exposed_to_wait`

- `Vendor2/GPT-5.3-codex`: Return a microplate from the exposed position to the wait position.

### Action: `auto-action_read_barcode`

- `Vendor2/GPT-5.3-codex`: Read barcode information from specified storage locations.

### Action: `auto-action_storage_to_exposed`

- `Vendor2/GPT-5.3-codex`: Move a microplate from storage to the exposed external position.

### Action: `auto-action_storage_to_transfer`

- `Vendor2/GPT-5.3-codex`: Move a microplate from storage to the transfer station.

### Action: `auto-action_storage_to_wait`

- `Vendor2/GPT-5.3-codex`: Move a microplate from storage to the wait position.

### Action: `auto-action_transfer_to_storage`

- `Vendor2/GPT-5.3-codex`: Move a microplate from the transfer station into storage.

### Action: `auto-action_transfer_to_wait`

- `Vendor2/GPT-5.3-codex`: Move a microplate from the transfer station to the wait position.

### Action: `auto-action_wait_to_exposed`

- `Vendor2/GPT-5.3-codex`: Move a microplate from the wait position to the exposed external position.

### Action: `auto-action_wait_to_storage`

- `Vendor2/GPT-5.3-codex`: Move a microplate from the wait position into storage.

### Action: `auto-action_wait_to_transfer`

- `Vendor2/GPT-5.3-codex`: Move a microplate from the wait position to the transfer station.

### Action: `auto-close_door`

- `Vendor2/GPT-5.3-codex`: Close the device door.

### Action: `auto-fetch_plate_to_loading_tray`

- `Vendor2/GPT-5.3-codex`: Fetch a specified microplate to the loading tray.

### Action: `auto-init_shakers`

- `Vendor2/GPT-5.3-codex`: Initialize the shaker modules.

### Action: `auto-initialize`

- `Vendor2/GPT-5.3-codex`: Run device initialization.

### Action: `auto-open_door`

- `Vendor2/GPT-5.3-codex`: Open the device door.

### Action: `auto-reset_error_register`

- `Vendor2/GPT-5.3-codex`: Reset the error register.

### Action: `auto-send_action`

- `Vendor2/GPT-5.3-codex`: Send an action command and wait for device execution.

### Action: `auto-send_command`

- `Vendor2/GPT-5.3-codex`: Send a command to the device controller.

### Action: `auto-serialize`

- `Vendor2/GPT-5.3-codex`: Export current device configuration and state information.

### Action: `auto-set_racks`

- `Vendor2/GPT-5.3-codex`: Define the internal rack configuration.

### Action: `auto-set_shaking_frequency`

- `Vendor2/GPT-5.3-codex`: Set the shaking frequency.

### Action: `auto-set_temperature`

- `Vendor2/GPT-5.3-codex`: Set the temperature setpoint.

### Action: `auto-setup`

- `Vendor2/GPT-5.3-codex`: Perform device setup after power-up.

### Action: `auto-shovel_in`

- `Vendor2/GPT-5.3-codex`: Shovel a tray/plate into the device interior.

### Action: `auto-shovel_out`

- `Vendor2/GPT-5.3-codex`: Shovel a tray/plate out of the device.

### Action: `auto-start_shaking`

- `Vendor2/GPT-5.3-codex`: Start shaking incubation.

### Action: `auto-stop`

- `Vendor2/GPT-5.3-codex`: Stop current device operation.

### Action: `auto-stop_shaking`

- `Vendor2/GPT-5.3-codex`: Stop shaking.

### Action: `auto-take_in_plate`

- `Vendor2/GPT-5.3-codex`: Take a microplate into the device and place it at a specified site.

### Action: `auto-wait_for_task_completion`

- `Vendor2/GPT-5.3-codex`: Wait for the current task to complete.

### Action: `auto-wait_for_transfer_station`

- `Vendor2/GPT-5.3-codex`: Wait for the transfer station to become occupied or unoccupied.

### Action: `auto-get_overview_register`

- `Vendor2/GPT-5.3-codex`: Get overview register status.

### Action: `auto-get_warning_register`

- `Vendor2/GPT-5.3-codex`: Get warning register status.

### Action: `auto-get_error_register`

- `Vendor2/GPT-5.3-codex`: Get error register status.

### Action: `auto-get_action_register`

- `Vendor2/GPT-5.3-codex`: Get action register status.

### Action: `auto-get_swap_register`

- `Vendor2/GPT-5.3-codex`: Get swap register status.

### Action: `auto-get_sensor_register`

- `Vendor2/GPT-5.3-codex`: Get sensor register status.

### Action: `auto-get_incubation_query`

- `Vendor2/GPT-5.3-codex`: Get incubation query results.

### Action: `auto-get_co2`

- `Vendor2/GPT-5.3-codex`: Get CO2 level.

### Action: `auto-get_humidity`

- `Vendor2/GPT-5.3-codex`: Get humidity.

### Action: `auto-get_o2`

- `Vendor2/GPT-5.3-codex`: Get O2 level.

### Action: `auto-get_temperature`

- `Vendor2/GPT-5.3-codex`: Get temperature.

### Tags

- `Vendor2/GPT-5.3-codex`: 器件/细胞设备, 物流/机械, 生命体系, 细胞生物学研究, 组织培养试验箱, 自动化耗材堆栈, 恒温摇床, 自动化微孔板培养存储系统

