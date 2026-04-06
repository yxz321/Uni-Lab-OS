# Workflow v4 Benchmark Summary

## Usage

- `gpt-5.2-codex`: Pass A total 17487 tokens, Pass B total 29710 tokens, combined 47197 tokens
- `gpt-5.4`: Pass A total 21572 tokens, Pass B total 43890 tokens, combined 65462 tokens
- `gpt-5.4-mini`: Pass A total 22932 tokens, Pass B total 46825 tokens, combined 69757 tokens
- `gpt-5.4-nano`: Pass A total 21930 tokens, Pass B total 38695 tokens, combined 60625 tokens

## bio_shake

### Device Name

- `gpt-5.2-codex`: BioShake heater shaker
- `gpt-5.4`: BioShake Microplate Heater Shaker
- `gpt-5.4-mini`: BioShake Heater Shaker
- `gpt-5.4-nano`: BioShake Heater-Shaker

### Device Description

- `gpt-5.2-codex`: BioShake is a heater shaker for microplates, providing temperature control and orbital shaking for mixing, incubation, and temperature-controlled reactions.
- `gpt-5.4`: The BioShake microplate heater shaker is a laboratory device for temperature-controlled incubation and shaking of microplate samples. It can heat and shake plates, perform reset and homing operations, and on some models supports plate locking and active-cooling-related features.
- `gpt-5.4-mini`: A heated shaking device for microplates or plate-based samples, supporting temperature control, plate locking, and optional active cooling. It is commonly used for mixing, incubation, and reaction acceleration.
- `gpt-5.4-nano`: A heater-shaker device for biological samples. It supports setting shaking speed, acceleration, and deceleration, as well as temperature setpoints with active temperature control. It can lock the sample plate/holder for stable operation.

### Action: `auto-deactivate`

- `gpt-5.2-codex`: stop temperature control
- `gpt-5.4`: stop temperature control
- `gpt-5.4-mini`: Stop temperature control
- `gpt-5.4-nano`: Deactivate temperature control.

### Action: `auto-home`

- `gpt-5.2-codex`: home to the reference position
- `gpt-5.4`: move the device to its home position
- `gpt-5.4-mini`: Initialize the device to its home position
- `gpt-5.4-nano`: Move/initialize the shaker to its home position.

### Action: `auto-lock_plate`

- `gpt-5.2-codex`: lock the microplate
- `gpt-5.4`: lock the microplate
- `gpt-5.4-mini`: Lock the plate
- `gpt-5.4-nano`: Lock the sample plate/holder to secure the sample position.

### Action: `auto-reset`

- `gpt-5.2-codex`: reset the device
- `gpt-5.4`: reset the device
- `gpt-5.4-mini`: Reset the device
- `gpt-5.4-nano`: Reset the BioShake to restore it to a ready initial state.

### Action: `auto-set_temperature`

- `gpt-5.2-codex`: set the temperature setpoint
- `gpt-5.4`: set the target temperature and start temperature control
- `gpt-5.4-mini`: Set and start temperature control
- `gpt-5.4-nano`: Set a target temperature and start temperature control.

### Action: `auto-setup`

- `gpt-5.2-codex`: initialize the device
- `gpt-5.4`: perform initialization, including reset and homing
- `gpt-5.4-mini`: Reset, initialize, and home the device
- `gpt-5.4-nano`: Initialize the device and prepare it for operation (optionally reset first, then home).

### Action: `auto-shake`

- `gpt-5.2-codex`: start shaking and set speed/acceleration
- `gpt-5.4`: start shaking at the specified speed and acceleration
- `gpt-5.4-mini`: Set the shaking speed and start shaking
- `gpt-5.4-nano`: Start shaking with a specified speed and acceleration (according to the device command, with or without duration).

### Action: `auto-stop`

- `gpt-5.2-codex`: stop the device
- `gpt-5.4`: stop the device's current operation
- `gpt-5.4-mini`: Stop the device
- `gpt-5.4-nano`: Stop the device.

### Action: `auto-stop_shaking`

- `gpt-5.2-codex`: stop shaking and set deceleration
- `gpt-5.4`: stop shaking with optional deceleration
- `gpt-5.4-mini`: Stop shaking
- `gpt-5.4-nano`: Stop shaking, optionally with a specified deceleration.

### Action: `auto-unlock_plate`

- `gpt-5.2-codex`: unlock the microplate
- `gpt-5.4`: unlock the microplate
- `gpt-5.4-mini`: Unlock the plate
- `gpt-5.4-nano`: Unlock the sample plate/holder to allow loading or unloading samples.

### Action: `auto-supports_locking`

- `gpt-5.2-codex`: get whether plate locking is supported
- `gpt-5.4`: get whether plate locking is supported
- `gpt-5.4-mini`: Get whether the device supports plate locking
- `gpt-5.4-nano`: get whether plate-locking is supported.

### Action: `auto-supports_active_cooling`

- `gpt-5.2-codex`: get whether active cooling is supported
- `gpt-5.4`: get whether active cooling is supported
- `gpt-5.4-mini`: Get whether the device supports active cooling
- `gpt-5.4-nano`: get whether active cooling is supported for temperature control.

### Action: `auto-get_current_temperature`

- `gpt-5.2-codex`: get current temperature
- `gpt-5.4`: get the current temperature
- `gpt-5.4-mini`: Get the current temperature
- `gpt-5.4-nano`: get the current temperature.

### Tags

- `gpt-5.2-codex`: 实验执行&合成设备, 生命体系, 细胞生物学研究, 恒温摇床
- `gpt-5.4`: 器件/细胞设备, 生命体系, 细胞生物学研究, 恒温摇床
- `gpt-5.4-mini`: 器件/细胞设备, 生命体系, 细胞生物学研究, 恒温摇床
- `gpt-5.4-nano`: 器件/细胞设备 / Device / Cell Equipment, 生命体系 / Life Sciences, 细胞生物学研究 / Cell Biology Research, 恒温摇床 / Constant Temperature Shaker

## cc_core

### Device Name

- `gpt-5.2-codex`: QuTech Central Controller Core
- `gpt-5.4`: QuTech Central Controller
- `gpt-5.4-mini`: Central Controller Core
- `gpt-5.4-nano`: QuTech CC Control Core

### Device Description

- `gpt-5.2-codex`: A programmable central controller core for quantum experiments, running sequencers, calibrating digital I/O, and monitoring status to provide timing and trigger control.
- `gpt-5.4`: A central control electronics unit for quantum computing experiments, typically FPGA-based, used to execute timing and sequence programs, coordinate CCIO modules, digital I/O links, and timing delay settings, and provide synchronized control for qubit control and readout experiments.
- `gpt-5.4-mini`: QuTech central controller core module used in quantum experiments for pulse-sequence control, sequence loading and start/stop operation, digital I/O calibration, and status monitoring of related control modules.
- `gpt-5.4-nano`: A CC timing control core module for quantum experiments. It uploads/assembles sequence programs, starts/stops the CC sequencers, and supports DIO calibration, VSM delay parameter tuning, and status monitoring.

### Action: `auto-assemble`

- `gpt-5.2-codex`: assemble a sequence program
- `gpt-5.4`: assemble the sequence program
- `gpt-5.4-mini`: Assemble the pulse-sequence program.
- `gpt-5.4-nano`: Assemble/prepare a sequence program for uploading to the CC core.

### Action: `auto-assemble_and_start`

- `gpt-5.2-codex`: assemble and start sequencers
- `gpt-5.4`: assemble the sequence program and start the controller
- `gpt-5.4-mini`: Assemble and start the pulse-sequence program.
- `gpt-5.4-nano`: Assemble the sequence program and start the CC sequencers.

### Action: `auto-calibrate_dio`

- `gpt-5.2-codex`: calibrate digital I/O
- `gpt-5.4`: calibrate the digital I/O link
- `gpt-5.4-mini`: Calibrate the digital I/O interface.
- `gpt-5.4-nano`: Calibrate the DIO.

### Action: `auto-debug_get_ccio_reg`

- `gpt-5.2-codex`: read a CCIO register
- `gpt-5.4`: read a CCIO debug register
- `gpt-5.4-mini`: Read a CCIO register for debugging.
- `gpt-5.4-nano`: Read a specified CCIO register value (for debugging).

### Action: `auto-debug_get_ccio_trace`

- `gpt-5.2-codex`: read CCIO trace data
- `gpt-5.4`: read CCIO debug trace data
- `gpt-5.4-mini`: Read CCIO trace data for debugging.
- `gpt-5.4-nano`: Read CCIO trace data (for debugging).

### Action: `auto-debug_get_traces`

- `gpt-5.2-codex`: read multiple CCIO traces
- `gpt-5.4`: read debug trace data from multiple CCIOs
- `gpt-5.4-mini`: Read debug traces from multiple CCIO modules.
- `gpt-5.4-nano`: Get multiple CCIO trace data by mask (for debugging).

### Action: `auto-debug_marker_in`

- `gpt-5.2-codex`: set debug marker to input
- `gpt-5.4`: route the debug marker to an input bit
- `gpt-5.4-mini`: Insert a debug marker into the specified channel.
- `gpt-5.4-nano`: Set the debug marker to “in” (specified bit) (for debugging).

### Action: `auto-debug_marker_off`

- `gpt-5.2-codex`: turn off debug marker
- `gpt-5.4`: turn off the debug marker output
- `gpt-5.4-mini`: Turn off debug marker output.
- `gpt-5.4-nano`: Turn off the debug marker (specified bit) (for debugging).

### Action: `auto-debug_marker_out`

- `gpt-5.2-codex`: set debug marker to output
- `gpt-5.4`: route the debug marker to an output bit
- `gpt-5.4-mini`: Output a debug marker on the specified channel.
- `gpt-5.4-nano`: Set the debug marker to “out” (specified bit) (for debugging).

### Action: `auto-debug_set_ccio_trace_on`

- `gpt-5.2-codex`: enable CCIO trace
- `gpt-5.4`: enable CCIO debug tracing
- `gpt-5.4-mini`: Enable trace recording on the specified CCIO channel.
- `gpt-5.4-nano`: Enable CCIO tracing (specified trace index) (for debugging).

### Action: `auto-print_status_operation`

- `gpt-5.2-codex`: print operation status summary
- `gpt-5.4`: display operation status information
- `gpt-5.4-mini`: Display the combined operation status.
- `gpt-5.4-nano`: Print/display the operation status (combined CC core and CCIO status).

### Action: `auto-print_status_questionable`

- `gpt-5.2-codex`: print questionable status summary
- `gpt-5.4`: display questionable status information
- `gpt-5.4-mini`: Display the combined questionable-status summary.
- `gpt-5.4-nano`: Print/display the questionable status (combined CC core and CCIO status).

### Action: `auto-sequence_program_assemble`

- `gpt-5.2-codex`: set the sequence program to assemble
- `gpt-5.4`: set the sequence program to assemble
- `gpt-5.4-mini`: Upload and assemble the sequence program.
- `gpt-5.4-nano`: set sequence program for assembly.

### Action: `auto-set_q1_reg`

- `gpt-5.2-codex`: set Q1 register value
- `gpt-5.4`: set a Q1 register
- `gpt-5.4-mini`: Set the Q1 register value on a CCIO module.
- `gpt-5.4-nano`: set Q1 register value.

### Action: `auto-set_seqbar_cnt`

- `gpt-5.2-codex`: set sequence barrier count
- `gpt-5.4`: set the sequence barrier counter
- `gpt-5.4-mini`: Set the sequence-bar count on a CCIO module.
- `gpt-5.4-nano`: Set the sequence bar counter (SeqBar count).

### Action: `auto-set_status_operation_run_enable`

- `gpt-5.2-codex`: set operation run status enable
- `gpt-5.4`: set operation run status enable
- `gpt-5.4-mini`: Set the enable flag for the operation-run status.
- `gpt-5.4-nano`: set operation-run status reporting enable.

### Action: `auto-set_status_questionable_bplink_enable`

- `gpt-5.2-codex`: set questionable backplane link status enable
- `gpt-5.4`: set questionable backplane link status enable
- `gpt-5.4-mini`: Set the enable flag for the backplane-link questionable status.
- `gpt-5.4-nano`: set questionable bplink status reporting enable.

### Action: `auto-set_status_questionable_config_enable`

- `gpt-5.2-codex`: set questionable configuration status enable
- `gpt-5.4`: set questionable configuration status enable
- `gpt-5.4-mini`: Set the enable flag for the configuration questionable status.
- `gpt-5.4-nano`: set questionable config status reporting enable.

### Action: `auto-set_status_questionable_frequency_enable`

- `gpt-5.2-codex`: set questionable frequency status enable
- `gpt-5.4`: set questionable frequency status enable
- `gpt-5.4-mini`: Set the enable flag for the frequency questionable status.
- `gpt-5.4-nano`: set questionable frequency status reporting enable.

### Action: `auto-set_status_questionable_instrument_enable`

- `gpt-5.2-codex`: set questionable instrument status enable
- `gpt-5.4`: set questionable instrument status enable
- `gpt-5.4-mini`: Set the enable flag for the instrument questionable status.
- `gpt-5.4-nano`: set questionable instrument status reporting enable.

### Action: `auto-set_status_questionable_instrument_idetail_bplink_enable`

- `gpt-5.2-codex`: set questionable instrument detail backplane link status enable
- `gpt-5.4`: set questionable instrument detail backplane link status enable
- `gpt-5.4-mini`: Set the enable flag for the instrument backplane-link detailed questionable status.
- `gpt-5.4-nano`: set questionable instrument detailed bplink status reporting enable.

### Action: `auto-set_status_questionable_instrument_idetail_config_enable`

- `gpt-5.2-codex`: set questionable instrument detail configuration status enable
- `gpt-5.4`: set questionable instrument detail configuration status enable
- `gpt-5.4-mini`: Set the enable flag for the instrument configuration detailed questionable status.
- `gpt-5.4-nano`: set questionable instrument detailed config status reporting enable.

### Action: `auto-set_status_questionable_instrument_idetail_diocal_enable`

- `gpt-5.2-codex`: set questionable instrument detail DIO calibration status enable
- `gpt-5.4`: set questionable instrument detail digital I/O calibration status enable
- `gpt-5.4-mini`: Set the enable flag for the instrument DIO-calibration detailed questionable status.
- `gpt-5.4-nano`: set questionable instrument detailed diocal status reporting enable.

### Action: `auto-set_status_questionable_instrument_idetail_freq_enable`

- `gpt-5.2-codex`: set questionable instrument detail frequency status enable
- `gpt-5.4`: set questionable instrument detail frequency status enable
- `gpt-5.4-mini`: Set the enable flag for the instrument frequency detailed questionable status.
- `gpt-5.4-nano`: set questionable instrument detailed frequency status reporting enable.

### Action: `auto-set_status_questionable_instrument_isummary_enable`

- `gpt-5.2-codex`: set questionable instrument summary status enable
- `gpt-5.4`: set questionable instrument summary status enable
- `gpt-5.4-mini`: Set the enable flag for the instrument status summary.
- `gpt-5.4-nano`: set questionable instrument summary status reporting enable.

### Action: `auto-set_vsm_delay_fall`

- `gpt-5.2-codex`: set VSM fall delay
- `gpt-5.4`: set the VSM falling-edge delay
- `gpt-5.4-mini`: Set the VSM fall-edge delay.
- `gpt-5.4-nano`: set VSM fall-delay value.

### Action: `auto-set_vsm_delay_rise`

- `gpt-5.2-codex`: set VSM rise delay
- `gpt-5.4`: set the VSM rising-edge delay
- `gpt-5.4-mini`: Set the VSM rise-edge delay.
- `gpt-5.4-nano`: set VSM rise-delay value.

### Action: `auto-start`

- `gpt-5.2-codex`: start the controller sequencers
- `gpt-5.4`: start the controller sequencers
- `gpt-5.4-mini`: Start the control sequencers.
- `gpt-5.4-nano`: Start the CC sequencers.

### Action: `auto-status_preset`

- `gpt-5.2-codex`: preset status and enable event reporting
- `gpt-5.4`: enable the SCPI event status reporting preset
- `gpt-5.4-mini`: Enable the default status event reporting.
- `gpt-5.4-nano`: Preset/initialize the status reporting configuration.

### Action: `auto-stop`

- `gpt-5.2-codex`: stop the controller sequencers
- `gpt-5.4`: stop the controller sequencers
- `gpt-5.4-mini`: Stop the control sequencers.
- `gpt-5.4-nano`: Stop the CC sequencers.

### Action: `auto-get_sequence_program_assemble`

- `gpt-5.2-codex`: get the sequence program to assemble
- `gpt-5.4`: get the sequence program to assemble
- `gpt-5.4-mini`: Get the assembled sequence program.
- `gpt-5.4-nano`: get sequence program for assembly.

### Action: `auto-get_assembler_success`

- `gpt-5.2-codex`: get assembler success status
- `gpt-5.4`: get assembler success status
- `gpt-5.4-mini`: Get whether the assembler succeeded.
- `gpt-5.4-nano`: get assembler success status.

### Action: `auto-get_assembler_log`

- `gpt-5.2-codex`: get assembler log
- `gpt-5.4`: get the assembler log
- `gpt-5.4-mini`: Get the assembler log.
- `gpt-5.4-nano`: get assembler log.

### Action: `auto-get_q1_reg`

- `gpt-5.2-codex`: get Q1 register value
- `gpt-5.4`: get a Q1 register
- `gpt-5.4-mini`: Get the Q1 register value on a CCIO module.
- `gpt-5.4-nano`: get Q1 register value.

### Action: `auto-get_calibrate_dio_success`

- `gpt-5.2-codex`: get DIO calibration success status
- `gpt-5.4`: get digital I/O calibration success status
- `gpt-5.4-mini`: Get whether digital I/O calibration succeeded.
- `gpt-5.4-nano`: get DIO calibration success status.

### Action: `auto-get_calibrate_dio_status`

- `gpt-5.2-codex`: get DIO calibration status
- `gpt-5.4`: get digital I/O calibration status
- `gpt-5.4-mini`: Get the digital I/O calibration status.
- `gpt-5.4-nano`: get DIO calibration status.

### Action: `auto-get_calibrate_dio_read_index`

- `gpt-5.2-codex`: get DIO calibration read index
- `gpt-5.4`: get the digital I/O calibration read index
- `gpt-5.4-mini`: Get the digital I/O calibration read index.
- `gpt-5.4-nano`: get DIO calibration read index.

### Action: `auto-get_calibrate_dio_margin`

- `gpt-5.2-codex`: get DIO calibration margin
- `gpt-5.4`: get the digital I/O calibration margin
- `gpt-5.4-mini`: Get the digital I/O calibration margin.
- `gpt-5.4-nano`: get DIO calibration margin.

### Action: `auto-get_vsm_delay_rise`

- `gpt-5.2-codex`: get VSM rise delay
- `gpt-5.4`: get the VSM rising-edge delay
- `gpt-5.4-mini`: Get the VSM rise-edge delay.
- `gpt-5.4-nano`: get VSM rise-delay value.

### Action: `auto-get_vsm_delay_fall`

- `gpt-5.2-codex`: get VSM fall delay
- `gpt-5.4`: get the VSM falling-edge delay
- `gpt-5.4-mini`: Get the VSM fall-edge delay.
- `gpt-5.4-nano`: get VSM fall-delay value.

### Action: `auto-get_status_questionable_frequency`

- `gpt-5.2-codex`: get questionable frequency status
- `gpt-5.4`: get questionable frequency status
- `gpt-5.4-mini`: Get the frequency questionable status.
- `gpt-5.4-nano`: get questionable frequency status.

### Action: `auto-get_status_questionable_frequency_enable`

- `gpt-5.2-codex`: get questionable frequency status enable
- `gpt-5.4`: get questionable frequency status enable
- `gpt-5.4-mini`: Get the enable flag for the frequency questionable status.
- `gpt-5.4-nano`: get questionable frequency status reporting enable.

### Action: `auto-get_status_questionable_config`

- `gpt-5.2-codex`: get questionable configuration status
- `gpt-5.4`: get questionable configuration status
- `gpt-5.4-mini`: Get the configuration questionable status.
- `gpt-5.4-nano`: get questionable config status.

### Action: `auto-get_status_questionable_config_enable`

- `gpt-5.2-codex`: get questionable configuration status enable
- `gpt-5.4`: get questionable configuration status enable
- `gpt-5.4-mini`: Get the enable flag for the configuration questionable status.
- `gpt-5.4-nano`: get questionable config status reporting enable.

### Action: `auto-get_status_questionable_bplink`

- `gpt-5.2-codex`: get questionable backplane link status
- `gpt-5.4`: get questionable backplane link status
- `gpt-5.4-mini`: Get the backplane-link questionable status.
- `gpt-5.4-nano`: get questionable bplink status.

### Action: `auto-get_status_questionable_bplink_enable`

- `gpt-5.2-codex`: get questionable backplane link status enable
- `gpt-5.4`: get questionable backplane link status enable
- `gpt-5.4-mini`: Get the enable flag for the backplane-link questionable status.
- `gpt-5.4-nano`: get questionable bplink status reporting enable.

### Action: `auto-get_status_operation_run`

- `gpt-5.2-codex`: get operation run status
- `gpt-5.4`: get operation run status
- `gpt-5.4-mini`: Get the operation run status.
- `gpt-5.4-nano`: get operation-run status.

### Action: `auto-get_status_operation_run_enable`

- `gpt-5.2-codex`: get operation run status enable
- `gpt-5.4`: get operation run status enable
- `gpt-5.4-mini`: Get the enable flag for the operation run status.
- `gpt-5.4-nano`: get operation-run status reporting enable.

### Action: `auto-get_status_questionable_instrument`

- `gpt-5.2-codex`: get questionable instrument status
- `gpt-5.4`: get questionable instrument status
- `gpt-5.4-mini`: Get the instrument questionable status.
- `gpt-5.4-nano`: get questionable instrument status.

### Action: `auto-get_status_questionable_instrument_enable`

- `gpt-5.2-codex`: get questionable instrument status enable
- `gpt-5.4`: get questionable instrument status enable
- `gpt-5.4-mini`: Get the enable flag for the instrument questionable status.
- `gpt-5.4-nano`: get questionable instrument status reporting enable.

### Action: `auto-get_status_questionable_instrument_isummary`

- `gpt-5.2-codex`: get questionable instrument summary status
- `gpt-5.4`: get questionable instrument summary status
- `gpt-5.4-mini`: Get the instrument status summary questionable condition.
- `gpt-5.4-nano`: get questionable instrument summary status.

### Action: `auto-get_status_questionable_instrument_isummary_enable`

- `gpt-5.2-codex`: get questionable instrument summary status enable
- `gpt-5.4`: get questionable instrument summary status enable
- `gpt-5.4-mini`: Get the enable flag for the instrument status summary.
- `gpt-5.4-nano`: get questionable instrument summary status reporting enable.

### Action: `auto-get_status_questionable_instrument_idetail_freq`

- `gpt-5.2-codex`: get questionable instrument detail frequency status
- `gpt-5.4`: get questionable instrument detail frequency status
- `gpt-5.4-mini`: Get the instrument frequency detailed questionable condition.
- `gpt-5.4-nano`: get questionable instrument detailed frequency status.

### Action: `auto-get_status_questionable_instrument_idetail_freq_enable`

- `gpt-5.2-codex`: get questionable instrument detail frequency status enable
- `gpt-5.4`: get questionable instrument detail frequency status enable
- `gpt-5.4-mini`: Get the enable flag for the instrument frequency detailed questionable status.
- `gpt-5.4-nano`: get questionable instrument detailed frequency status reporting enable.

### Action: `auto-get_status_questionable_instrument_idetail_config`

- `gpt-5.2-codex`: get questionable instrument detail configuration status
- `gpt-5.4`: get questionable instrument detail configuration status
- `gpt-5.4-mini`: Get the instrument configuration detailed questionable condition.
- `gpt-5.4-nano`: get questionable instrument detailed config status.

### Action: `auto-get_status_questionable_instrument_idetail_config_enable`

- `gpt-5.2-codex`: get questionable instrument detail configuration status enable
- `gpt-5.4`: get questionable instrument detail configuration status enable
- `gpt-5.4-mini`: Get the enable flag for the instrument configuration detailed questionable status.
- `gpt-5.4-nano`: get questionable instrument detailed config status reporting enable.

### Action: `auto-get_status_questionable_instrument_idetail_bplink`

- `gpt-5.2-codex`: get questionable instrument detail backplane link status
- `gpt-5.4`: get questionable instrument detail backplane link status
- `gpt-5.4-mini`: Get the instrument backplane-link detailed questionable condition.
- `gpt-5.4-nano`: get questionable instrument detailed bplink status.

### Action: `auto-get_status_questionable_instrument_idetail_bplink_enable`

- `gpt-5.2-codex`: get questionable instrument detail backplane link status enable
- `gpt-5.4`: get questionable instrument detail backplane link status enable
- `gpt-5.4-mini`: Get the enable flag for the instrument backplane-link detailed questionable status.
- `gpt-5.4-nano`: get questionable instrument detailed bplink status reporting enable.

### Action: `auto-get_status_questionable_instrument_idetail_diocal`

- `gpt-5.2-codex`: get questionable instrument detail DIO calibration status
- `gpt-5.4`: get questionable instrument detail digital I/O calibration status
- `gpt-5.4-mini`: Get the instrument DIO-calibration detailed questionable condition.
- `gpt-5.4-nano`: get questionable instrument detailed diocal status.

### Action: `auto-get_status_questionable_instrument_idetail_diocal_enable`

- `gpt-5.2-codex`: get questionable instrument detail DIO calibration status enable
- `gpt-5.4`: get questionable instrument detail digital I/O calibration status enable
- `gpt-5.4-mini`: Get the enable flag for the instrument DIO-calibration detailed questionable status.
- `gpt-5.4-nano`: get questionable instrument detailed diocal status reporting enable.

### Tags

- `gpt-5.2-codex`: 实验执行&合成设备, 智慧表征与检测中心, 移液站产品, 移液工作站
- `gpt-5.4`: 实验执行&合成设备, 智慧表征与检测中心, 物化表征测试中心, 实验时序控制器
- `gpt-5.4-mini`: 实验执行&合成设备, 智慧表征与检测中心, 物化表征测试中心
- `gpt-5.4-nano`: 实验执行&合成设备 / Experiment Execution & Synthesis Equipment, 生命体系 / Life Sciences, 移液站产品 / Liquid Handling Station Products, 移液工作站 / Liquid Handling Workstation

## cryo_tel_gt

### Device Name

- `gpt-5.2-codex`: Sunpower CryoTel GT Cryocooler
- `gpt-5.4`: Sunpower CryoTel GT Cryocooler
- `gpt-5.4-mini`: CryoTel GT Cryocooler
- `gpt-5.4-nano`: Sunpower CryoTel GT Cryocooler

### Device Description

- `gpt-5.2-codex`: The Sunpower CryoTel GT is a closed‑cycle cryocooler for laboratory cryogenic cooling, providing a stable cold head temperature with temperature or power control for low‑temperature experiments.
- `gpt-5.4`: The Sunpower CryoTel GT is a laboratory cryocooler used to provide a stable low-temperature environment for samples, sensors, or small cold-stage assemblies. It supports temperature or power control and allows users to read current temperature, power, status, and error information, as well as set temperature targets, power limits, and thermostat-related parameters for cryogenic testing and low-temperature experimental setups.
- `gpt-5.4-mini`: The Sunpower CryoTel GT is a laboratory cryocooler used to provide and maintain low-temperature conditions, with readback of the current temperature and adjustable temperature or power setpoints.
- `gpt-5.4-nano`: The Sunpower CryoTel GT (generation 2) cryocooler is used in labs to provide and maintain cryogenic temperatures. It can be regulated via temperature or power setpoints and includes an at-temperature indication (green LED and an I/O “At Temperature” pin).

### Action: `auto-at_temperature_band`

- `gpt-5.2-codex`: Get/set the cryocooler at‑temperature band (K)
- `gpt-5.4`: Get/set the at-temperature band
- `gpt-5.4-mini`: get/set the temperature band threshold in Kelvin.
- `gpt-5.4-nano`: get/set temperature band (at-temperature range)

### Action: `auto-control_mode`

- `gpt-5.2-codex`: Get/set the control mode (power/temperature)
- `gpt-5.4`: Get/set the control mode
- `gpt-5.4-mini`: get/set the control mode (power or temperature).
- `gpt-5.4-nano`: get/set control mode (power/temperature)

### Action: `auto-ki`

- `gpt-5.2-codex`: Get/set the integral constant of the temperature control loop
- `gpt-5.4`: Get/set the temperature control loop integral constant
- `gpt-5.4-mini`: get/set the integral gain of the temperature control loop.
- `gpt-5.4-nano`: get/set integral constant of the temperature control loop (Ki)

### Action: `auto-kp`

- `gpt-5.2-codex`: Get/set the proportional constant of the temperature control loop
- `gpt-5.4`: Get/set the temperature control loop proportional constant
- `gpt-5.4-mini`: get/set the proportional gain of the temperature control loop.
- `gpt-5.4-nano`: get/set proportional constant of the temperature control loop (Kp)

### Action: `auto-power_max`

- `gpt-5.2-codex`: Get/set the maximum user power (W)
- `gpt-5.4`: Get/set the user-defined maximum power
- `gpt-5.4-mini`: get/set the user-defined maximum power limit in watts.
- `gpt-5.4-nano`: get/set maximum user-defined power limit

### Action: `auto-power_min`

- `gpt-5.2-codex`: Get/set the minimum user power (W)
- `gpt-5.4`: Get/set the user-defined minimum power
- `gpt-5.4-mini`: get/set the user-defined minimum power limit in watts.
- `gpt-5.4-nano`: get/set minimum user-defined power limit

### Action: `auto-power_setpoint`

- `gpt-5.2-codex`: Get/set the power setpoint (W)
- `gpt-5.4`: Get/set the power setpoint
- `gpt-5.4-mini`: get/set the power setpoint in watts for power control mode.
- `gpt-5.4-nano`: get/set power setpoint (used in power control mode)

### Action: `auto-query`

- `gpt-5.2-codex`: Send a query command to the cryocooler and read the response
- `gpt-5.4`: Send a query command to the cryocooler, optionally write a value, and return the response
- `gpt-5.4-mini`: send a query or set command and return the response.
- `gpt-5.4-nano`: send a query to the cooler and read the response

### Action: `auto-query_multiline`

- `gpt-5.2-codex`: Send a multi‑line query command and read the response
- `gpt-5.4`: Send a multiline query command to the cryocooler and return the response
- `gpt-5.4-mini`: send a query command that returns multiple lines of data.
- `gpt-5.4-nano`: send a multiline query to the cooler and retrieve the multiline response

### Action: `auto-reset`

- `gpt-5.2-codex`: Reset the cryocooler to factory defaults
- `gpt-5.4`: Reset the cryocooler to factory defaults
- `gpt-5.4-mini`: reset the cryocooler to factory defaults.
- `gpt-5.4-nano`: reset the cryocooler to factory defaults

### Action: `auto-save_control_mode`

- `gpt-5.2-codex`: Save the current control mode as the default
- `gpt-5.4`: Save the current control mode as the default control mode
- `gpt-5.4-mini`: save the current control mode as the default control mode.
- `gpt-5.4-nano`: save the current control mode as the default

### Action: `auto-sendcmd`

- `gpt-5.2-codex`: Send a control command to the cryocooler
- `gpt-5.4`: Send a command to the cryocooler
- `gpt-5.4-mini`: send a command to the cryocooler.
- `gpt-5.4-nano`: send a command to the cooler

### Action: `auto-stop`

- `gpt-5.2-codex`: Get/set the stop state (stop/start)
- `gpt-5.4`: Get/set the stop state
- `gpt-5.4-mini`: get/set the stop state (stop or start).
- `gpt-5.4-nano`: get/set stop (pause) state / start state

### Action: `auto-stop_mode`

- `gpt-5.2-codex`: Get/set the stop mode
- `gpt-5.4`: Get/set the stop mode
- `gpt-5.4-mini`: get/set the stop mode (host or digital input).
- `gpt-5.4-nano`: get/set stop mode (host/digio)

### Action: `auto-temperature_setpoint`

- `gpt-5.2-codex`: Get/set the temperature setpoint (K)
- `gpt-5.4`: Get/set the temperature setpoint
- `gpt-5.4-mini`: get/set the temperature setpoint in Kelvin for temperature control mode.
- `gpt-5.4-nano`: get/set temperature setpoint (used in temperature control mode)

### Action: `auto-thermostat`

- `gpt-5.2-codex`: Get/set the thermostat mode
- `gpt-5.4`: Get/set the thermostat mode
- `gpt-5.4-mini`: get/set the thermostat mode on or off.
- `gpt-5.4-nano`: get/set thermostat mode enable

### Action: `auto-errors`

- `gpt-5.2-codex`: Get the list of current error codes
- `gpt-5.4`: Get the active error codes
- `gpt-5.4-mini`: get the currently active error codes.
- `gpt-5.4-nano`: get the list of currently active error codes

### Action: `auto-power`

- `gpt-5.2-codex`: Get the current power (W)
- `gpt-5.4`: Get the current power
- `gpt-5.4-mini`: get the current output power in watts.
- `gpt-5.4-nano`: get the current power (watts)

### Action: `auto-power_current_and_limits`

- `gpt-5.2-codex`: Get the current power and power limits (W)
- `gpt-5.4`: Get the current power and power limits
- `gpt-5.4-mini`: get the current power and its allowable limits in watts.
- `gpt-5.4-nano`: get current power and power limits

### Action: `auto-serial_number`

- `gpt-5.2-codex`: Get the cryocooler serial number and revision
- `gpt-5.4`: Get the serial number and revision information
- `gpt-5.4-mini`: get the serial number and revision.
- `gpt-5.4-nano`: get the serial number and revision

### Action: `auto-state`

- `gpt-5.2-codex`: Get the list of major control parameters and states
- `gpt-5.4`: Get the list of control parameters and current state
- `gpt-5.4-mini`: get a list of controller state parameters.
- `gpt-5.4-nano`: get a list of control parameters and their current values

### Action: `auto-temperature`

- `gpt-5.2-codex`: Get the current temperature (K)
- `gpt-5.4`: Get the current temperature
- `gpt-5.4-mini`: get the current temperature in Kelvin.
- `gpt-5.4-nano`: get the current temperature (kelvin)

### Action: `auto-thermostat_status`

- `gpt-5.2-codex`: Get the current thermostat status
- `gpt-5.4`: Get the thermostat status
- `gpt-5.4-mini`: get the current thermostat status.
- `gpt-5.4-nano`: get the current thermostat status (on/off)

### Tags

- `gpt-5.2-codex`: 实验执行&合成设备, 智慧表征与检测中心, 物化表征测试中心, 深低温冰箱
- `gpt-5.4`: 实验执行&合成设备, 智慧表征与检测中心, 物化表征测试中心, 深低温冰箱
- `gpt-5.4-mini`: 物流/机械, 智慧表征与检测中心, 物化表征测试中心
- `gpt-5.4-nano`: 物流/机械 / Logistics / Machinery, 智慧表征与检测中心 / Intelligent Characterization & Testing Center, 稀土永磁与超导材料 / Rare Earth Permanent Magnet & Superconducting Materials, 深低温冰箱 / Ultra-Low Temperature Freezer

## cvd_control

### Device Name

- `gpt-5.2-codex`: CVD Process Control System
- `gpt-5.4`: Chemical Vapor Deposition System
- `gpt-5.4-mini`: Chemical Vapor Deposition Controller
- `gpt-5.4-nano`: CVD Gas & Temperature Control Panel

### Device Description

- `gpt-5.2-codex`: A process control system for chemical vapor deposition (CVD) experiments, used to manage recipes, gas flows, and temperature setpoints, with status display and trend monitoring during runs.
- `gpt-5.4`: A chemical vapor deposition (CVD) process system for controlling reactor temperature and multiple process-gas flows, running deposition recipes, and monitoring process trends. It is commonly used for thin-film growth and materials deposition experiments.
- `gpt-5.4-mini`: A process controller for chemical vapor deposition (CVD) experiments, used to manage gas flows, temperature setpoints, and recipe execution while monitoring process trends.
- `gpt-5.4-nano`: A control panel for chemical vapor deposition (CVD) experiments, used to manage time-varying flow profiles for three process gases and set a temperature setpoint; it supports saving/loading recipes and starting/stopping runs.

### Action: `auto-return_ui_fields`

- `gpt-5.2-codex`: Get the list of UI fields
- `gpt-5.4`: Return the current values of the recipe UI fields.
- `gpt-5.4-mini`: Return the current recipe field values from the interface.
- `gpt-5.4-nano`: Return the UI fields used for configuration.

### Action: `auto-save_recipe`

- `gpt-5.2-codex`: Save the process recipe
- `gpt-5.4`: Save the current process recipe.
- `gpt-5.4-mini`: Save the current process recipe file.
- `gpt-5.4-nano`: Save the current parameters as a recipe file (including metadata and gas settings) and prompt for the save path.

### Action: `auto-open_recipe`

- `gpt-5.2-codex`: Open a process recipe
- `gpt-5.4`: Open and load a process recipe.
- `gpt-5.4-mini`: Open and load a process recipe file.
- `gpt-5.4-nano`: Load parameters from a recipe file into the interface, display recipe metadata, and set the gas column labels.

### Action: `auto-update_plot`

- `gpt-5.2-codex`: Update the process plots
- `gpt-5.4`: Update the process monitoring plots.
- `gpt-5.4-mini`: Update the gas flow trend plot.
- `gpt-5.4-nano`: Update the plots for the three gas flow curves to reflect the time evolution.

### Action: `auto-start_recipe`

- `gpt-5.2-codex`: Start running the process recipe
- `gpt-5.4`: Start running the process recipe.
- `gpt-5.4-mini`: Start running the current process recipe.
- `gpt-5.4-nano`: Start the process according to the current recipe and begin updating the curves and run status.

### Action: `auto-stop_recipe`

- `gpt-5.2-codex`: Stop the process recipe
- `gpt-5.4`: Stop the process recipe.
- `gpt-5.4-mini`: Stop the current process recipe.
- `gpt-5.4-nano`: Stop the currently running recipe.

### Action: `auto-apply_setpoints`

- `gpt-5.2-codex`: Apply setpoints
- `gpt-5.4`: Apply the temperature and gas-flow setpoints.
- `gpt-5.4-mini`: Apply process setpoints such as temperature.
- `gpt-5.4-nano`: Apply setpoints such as the temperature value to the relevant control items and UI display.

### Tags

- `gpt-5.2-codex`: 实验执行&合成设备, 表面/薄膜体系, 涂层材料, 化学气相沉积设备
- `gpt-5.4`: 实验执行&合成设备, 表面/薄膜体系, 涂层材料, 化学气相沉积设备
- `gpt-5.4-mini`: 实验执行&合成设备, 表面/薄膜体系, 涂层材料
- `gpt-5.4-nano`: 实验执行&合成设备 / Experiment Execution & Synthesis Equipment, 表面/薄膜体系 / Surface / Thin Film System, 涂层材料 / Coating Materials, 化学气相沉积设备 / Chemical Vapor Deposition System

## cytomat_backend

### Device Name

- `gpt-5.2-codex`: Cytomat Automated Incubator/Storage System
- `gpt-5.4`: Cytomat automated microplate incubator storage system
- `gpt-5.4-mini`: Cytomat Automated Incubator
- `gpt-5.4-nano`: Cytomat automated storage and incubation workcell

### Device Description

- `gpt-5.2-codex`: The Cytomat is an automated incubator and microplate storage system with an internal handling mechanism, transfer station, and storage positions. It maintains controlled temperature and gas conditions while moving plates between storage, wait, transfer, and exposed positions, and can include shaking modules for incubation with agitation.
- `gpt-5.4`: Cytomat is an automated microplate incubation and storage system that stores and incubates plates under controlled temperature, CO2, O2, and humidity conditions, while moving plates between storage, transfer, wait, and exposed positions using an internal handling mechanism. It is commonly used for cell culture, drug screening, and plate storage within laboratory automation workflows.
- `gpt-5.4-mini`: An automated incubator and storage system for plate-based samples, with rack storage, a transfer station, door handling, and optional shaking, while monitoring and controlling temperature, CO2, humidity, and O2.
- `gpt-5.4-nano`: An automated incubation and storage workcell for plates/samples. It provides incubation control (temperature, CO₂, O₂, humidity), includes shaking capability, and uses an internal door plus transfer/shovel mechanisms to move plates between storage, waiting, and exposed positions, with barcode reading for storage locations.

### Action: `auto-action_exposed_to_storage`

- `gpt-5.2-codex`: Move a plate from the exposed position back to storage
- `gpt-5.4`: Move a microplate from the exposed position back to a storage site.
- `gpt-5.4-mini`: Move a plate from the exposed position back to the specified storage site.
- `gpt-5.4-nano`: Move items from the exposed position back to the storage position (including door/transfer steps).

### Action: `auto-action_exposed_to_wait`

- `gpt-5.2-codex`: Move a plate from the exposed position back to the wait position
- `gpt-5.4`: Move a microplate from the exposed position back to the wait position.
- `gpt-5.4-mini`: Move a plate from the exposed position back to the wait position.
- `gpt-5.4-nano`: Return items from the exposed position to the wait position (including closing the door).

### Action: `auto-action_read_barcode`

- `gpt-5.2-codex`: Read barcodes of storage locations
- `gpt-5.4`: Read the barcode of specified storage locations.
- `gpt-5.4-mini`: Read the barcode of the specified storage locations.
- `gpt-5.4-nano`: Read the barcode for the specified storage locations.

### Action: `auto-action_storage_to_exposed`

- `gpt-5.2-codex`: Retrieve a plate from storage and move it to the exposed position
- `gpt-5.4`: Move a microplate from a storage site to the exposed position outside the device.
- `gpt-5.4-mini`: Move a plate from the specified storage site to the exposed position.
- `gpt-5.4-nano`: Retrieve items from storage and transport them to the exposed position.

### Action: `auto-action_storage_to_transfer`

- `gpt-5.2-codex`: Retrieve a plate from storage and move it to the transfer station
- `gpt-5.4`: Move a microplate from a storage site to the transfer station.
- `gpt-5.4-mini`: Retrieve a plate from the specified storage site and move it to the transfer station.
- `gpt-5.4-nano`: Take items from storage and place them into the transfer area.

### Action: `auto-action_storage_to_wait`

- `gpt-5.2-codex`: Retrieve a plate from storage and move it to the wait position
- `gpt-5.4`: Move a microplate from a storage site to the wait position.
- `gpt-5.4-mini`: Retrieve a plate from the specified storage site and move it to the wait position.
- `gpt-5.4-nano`: Retrieve items from storage and move them to the wait position.

### Action: `auto-action_transfer_to_storage`

- `gpt-5.2-codex`: Retrieve a plate from the transfer station and place it into storage
- `gpt-5.4`: Move a microplate from the transfer station into a storage site.
- `gpt-5.4-mini`: Move a plate from the transfer station into the specified storage site.
- `gpt-5.4-nano`: Move items from the transfer area back into storage.

### Action: `auto-action_transfer_to_wait`

- `gpt-5.2-codex`: Retrieve a plate from the transfer station and move it to the wait position
- `gpt-5.4`: Move a microplate from the transfer station to the wait position.
- `gpt-5.4-mini`: Retrieve a plate from the transfer station and move it back to the wait position.
- `gpt-5.4-nano`: Move items from the transfer area to the wait position.

### Action: `auto-action_wait_to_exposed`

- `gpt-5.2-codex`: Move a plate from the wait position to the exposed position
- `gpt-5.4`: Move a microplate from the wait position to the exposed position.
- `gpt-5.4-mini`: Move a plate from the wait position to the exposed position outside the device.
- `gpt-5.4-nano`: Move items from the wait position to the exposed (outside) position.

### Action: `auto-action_wait_to_storage`

- `gpt-5.2-codex`: Move a plate from the wait position to storage
- `gpt-5.4`: Move a microplate from the wait position to a storage site.
- `gpt-5.4-mini`: Move a plate from the wait position into the specified storage site.
- `gpt-5.4-nano`: Move items from the wait position back to storage, unload, and return to the wait position.

### Action: `auto-action_wait_to_transfer`

- `gpt-5.2-codex`: Move a plate from the wait position to the transfer station
- `gpt-5.4`: Move a microplate from the wait position to the transfer station.
- `gpt-5.4-mini`: Move a plate from the wait position to the transfer station.
- `gpt-5.4-nano`: Move items from the wait position to the transfer area (including placing items and closing the door).

### Action: `auto-close_door`

- `gpt-5.2-codex`: Close the incubator door
- `gpt-5.4`: Close the device door.
- `gpt-5.4-mini`: Close the device door.
- `gpt-5.4-nano`: Close the door mechanism.

### Action: `auto-fetch_plate_to_loading_tray`

- `gpt-5.2-codex`: Fetch a specified plate to the loading tray
- `gpt-5.4`: Fetch a specified microplate to the loading tray.
- `gpt-5.4-mini`: Fetch a plate to the loading tray.
- `gpt-5.4-nano`: Fetch a plate from inside the device and place it onto the loading tray.

### Action: `auto-init_shakers`

- `gpt-5.2-codex`: Initialize the shaker modules
- `gpt-5.4`: Initialize the shaker modules.
- `gpt-5.4-mini`: Initialize the shakers.
- `gpt-5.4-nano`: Initialize the shaker units.

### Action: `auto-initialize`

- `gpt-5.2-codex`: Initialize the device
- `gpt-5.4`: Initialize the device.
- `gpt-5.4-mini`: Initialize the device.
- `gpt-5.4-nano`: Initialize the device for operation.

### Action: `auto-open_door`

- `gpt-5.2-codex`: Open the incubator door
- `gpt-5.4`: Open the device door.
- `gpt-5.4-mini`: Open the device door.
- `gpt-5.4-nano`: Open the door mechanism for transfer operations.

### Action: `auto-reset_error_register`

- `gpt-5.2-codex`: Reset the error status register
- `gpt-5.4`: Reset the error register.
- `gpt-5.4-mini`: Reset the error register.
- `gpt-5.4-nano`: Reset the device error register.

### Action: `auto-send_action`

- `gpt-5.2-codex`: Send an action command to the device and wait for completion
- `gpt-5.4`: Execute a low-level device action command and wait for the result.
- `gpt-5.4-mini`: Send a control action to the device.
- `gpt-5.4-nano`: Send an action command to the device to trigger execution and return the current overview state.

### Action: `auto-send_command`

- `gpt-5.2-codex`: Send a command to the device
- `gpt-5.4`: Send a low-level device command.
- `gpt-5.4-mini`: Send a command to the device.
- `gpt-5.4-nano`: Send a low-level command to the device and receive its reply.

### Action: `auto-serialize`

- `gpt-5.2-codex`: Serialize the device state
- `gpt-5.4`: Serialize device configuration or state information.
- `gpt-5.4-mini`: Serialize the device configuration and state.
- `gpt-5.4-nano`: Create a serialized representation of the device’s current status/configuration.

### Action: `auto-set_racks`

- `gpt-5.2-codex`: Set the storage rack configuration
- `gpt-5.4`: Define the rack configuration.
- `gpt-5.4-mini`: Define the rack layout.
- `gpt-5.4-nano`: Configure the rack layout and placement positions inside the device.

### Action: `auto-set_shaking_frequency`

- `gpt-5.2-codex`: Set the shaking frequency
- `gpt-5.4`: Define the shaking frequency.
- `gpt-5.4-mini`: Set the shaking frequency.
- `gpt-5.4-nano`: Set the shaking frequency (optionally for specific shaker(s)).

### Action: `auto-set_temperature`

- `gpt-5.2-codex`: Set temperature
- `gpt-5.4`: Set temperature.
- `gpt-5.4-mini`: Set the incubation temperature.
- `gpt-5.4-nano`: set temperature

### Action: `auto-setup`

- `gpt-5.2-codex`: Set up the device
- `gpt-5.4`: Set up the device for operation.
- `gpt-5.4-mini`: Configure the device.
- `gpt-5.4-nano`: Run the device setup/ready configuration procedure.

### Action: `auto-shovel_in`

- `gpt-5.2-codex`: Perform the shovel-in plate handling action
- `gpt-5.4`: Move the loading shovel inward into the device.
- `gpt-5.4-mini`: Move the shuttle inward into the device.
- `gpt-5.4-nano`: Use the shovel mechanism to move items/plates into the device.

### Action: `auto-shovel_out`

- `gpt-5.2-codex`: Perform the shovel-out plate handling action
- `gpt-5.4`: Move the loading shovel outward from the device.
- `gpt-5.4-mini`: Move the shuttle outward out of the device.
- `gpt-5.4-nano`: Use the shovel mechanism to move items/plates out of the device.

### Action: `auto-start_shaking`

- `gpt-5.2-codex`: Start shaking
- `gpt-5.4`: Start shaking.
- `gpt-5.4-mini`: Start shaking.
- `gpt-5.4-nano`: Start shaking.

### Action: `auto-stop`

- `gpt-5.2-codex`: Stop the device
- `gpt-5.4`: Stop device operation.
- `gpt-5.4-mini`: Stop device operation.
- `gpt-5.4-nano`: Stop the device and enter a safe idle state.

### Action: `auto-stop_shaking`

- `gpt-5.2-codex`: Stop shaking
- `gpt-5.4`: Stop shaking.
- `gpt-5.4-mini`: Stop shaking.
- `gpt-5.4-nano`: Stop the shaking process.

### Action: `auto-take_in_plate`

- `gpt-5.2-codex`: Take in a plate and store it at a specified position
- `gpt-5.4`: Take a microplate into the device and place it in a specified storage site.
- `gpt-5.4-mini`: Take in a plate from the specified site.
- `gpt-5.4-nano`: Take in a specified plate to a given position.

### Action: `auto-wait_for_task_completion`

- `gpt-5.2-codex`: Wait for the current task to complete
- `gpt-5.4`: Wait for the current task to complete.
- `gpt-5.4-mini`: Wait for the current task to complete.
- `gpt-5.4-nano`: Wait for the current task to complete (with timeout handling).

### Action: `auto-wait_for_transfer_station`

- `gpt-5.2-codex`: Wait for the transfer station to become occupied or unoccupied
- `gpt-5.4`: Wait for the transfer station to reach the specified occupied state.
- `gpt-5.4-mini`: Wait for the transfer station to become occupied or unoccupied.
- `gpt-5.4-nano`: Wait for the transfer station to reach the requested occupancy state (occupied/unoccupied).

### Action: `auto-get_overview_register`

- `gpt-5.2-codex`: Get overview status register
- `gpt-5.4`: Get the overview register.
- `gpt-5.4-mini`: get overview register state
- `gpt-5.4-nano`: get overview register

### Action: `auto-get_warning_register`

- `gpt-5.2-codex`: Get warning status register
- `gpt-5.4`: Get the warning register.
- `gpt-5.4-mini`: get warning register state
- `gpt-5.4-nano`: get warning register

### Action: `auto-get_error_register`

- `gpt-5.2-codex`: Get error status register
- `gpt-5.4`: Get the error register.
- `gpt-5.4-mini`: get error register state
- `gpt-5.4-nano`: get error register

### Action: `auto-get_action_register`

- `gpt-5.2-codex`: Get action status register
- `gpt-5.4`: Get the action register.
- `gpt-5.4-mini`: get action register state
- `gpt-5.4-nano`: get action register

### Action: `auto-get_swap_register`

- `gpt-5.2-codex`: Get swap status register
- `gpt-5.4`: Get the swap register.
- `gpt-5.4-mini`: get swap register state
- `gpt-5.4-nano`: get swap register

### Action: `auto-get_sensor_register`

- `gpt-5.2-codex`: Get sensor status register
- `gpt-5.4`: Get the sensor register.
- `gpt-5.4-mini`: get sensor register state
- `gpt-5.4-nano`: get sensor register

### Action: `auto-get_incubation_query`

- `gpt-5.2-codex`: Get incubation query status
- `gpt-5.4`: Get the incubation query result.
- `gpt-5.4-mini`: get incubation query status
- `gpt-5.4-nano`: get incubation query state

### Action: `auto-get_co2`

- `gpt-5.2-codex`: Get CO2 level
- `gpt-5.4`: Get CO2 level.
- `gpt-5.4-mini`: get CO2 level
- `gpt-5.4-nano`: get CO₂

### Action: `auto-get_humidity`

- `gpt-5.2-codex`: Get humidity
- `gpt-5.4`: Get humidity.
- `gpt-5.4-mini`: get humidity level
- `gpt-5.4-nano`: get humidity

### Action: `auto-get_o2`

- `gpt-5.2-codex`: Get O2 level
- `gpt-5.4`: Get O2 level.
- `gpt-5.4-mini`: get O2 level
- `gpt-5.4-nano`: get O₂

### Action: `auto-get_temperature`

- `gpt-5.2-codex`: Get temperature
- `gpt-5.4`: Get temperature.
- `gpt-5.4-mini`: get incubation temperature
- `gpt-5.4-nano`: get temperature

### Tags

- `gpt-5.2-codex`: 实验执行&合成设备, 生命体系, 细胞生物学研究, 微生物培养箱, 自动化耗材堆栈
- `gpt-5.4`: 器件/细胞设备, 生命体系, 细胞生物学研究, 微生物培养箱
- `gpt-5.4-mini`: 器件/细胞设备, 生命体系, 细胞生物学研究, 微生物培养箱
- `gpt-5.4-nano`: 器件/细胞设备 / Device / Cell Equipment, 生命体系 / Life Sciences, 细胞生物学研究 / Cell Biology Research, 微生物培养箱 / Microbial Incubator

