# Workflow v4 Benchmark Summary

## Usage

- `Vendor2/GPT-5.2`: Pass A total 21593 tokens, Pass B total 61685 tokens, combined 83278 tokens
- `Vendor2/GPT-5.3-codex`: Pass A total 22110 tokens, Pass B total 59520 tokens, combined 81630 tokens
- `Vendor2/GPT-5.4`: Pass A total 23757 tokens, Pass B total 68260 tokens, combined 92017 tokens
- `gpt-5.4-mini`: Pass A total 22944 tokens, Pass B total 69985 tokens, combined 92929 tokens

## bio_shake

### Device Name

- `Vendor2/GPT-5.2`: BioShake microplate thermoshaker
- `Vendor2/GPT-5.3-codex`: BioShake microplate thermoshaker
- `Vendor2/GPT-5.4`: BioShake microplate thermoshaker
- `gpt-5.4-mini`: BioShake microplate thermoshaker

### Device Description

- `Vendor2/GPT-5.2`: BioShake is an integrated microplate heater shaker used to mix microplates by orbital shaking while controlling the plate temperature. It can clamp/lock the plate to prevent movement during shaking, and is commonly used for incubation, enzymatic reactions, mixing, and sample preparation workflows.
- `Vendor2/GPT-5.3-codex`: BioShake is a benchtop microplate heater shaker for temperature-controlled incubation and shaking/mixing of plate-based samples, with plate locking support. It is commonly used in molecular biology and biochemistry workflows for incubation, dissolution, reaction mixing, and sample preparation.
- `Vendor2/GPT-5.4`: This is a benchtop heater shaker for microplates or sample plates. It provides temperature control together with shaking for sample mixing, incubation, reaction setup, and automated laboratory workflows. Depending on the model, it may also support plate locking and active cooling.
- `gpt-5.4-mini`: BioShake is a benchtop microplate heater shaker for temperature-controlled incubation and shaking/mixing of plate-based samples, with plate locking support. It is commonly used in molecular biology and biochemistry workflows for incubation, dissolution, reaction mixing, and sample preparation.

### Action: `auto-deactivate`

- `Vendor2/GPT-5.2`: Deactivate temperature control (stop heating/temperature regulation)
- `Vendor2/GPT-5.3-codex`: Deactivate temperature control.
- `Vendor2/GPT-5.4`: Stop temperature control.
- `gpt-5.4-mini`: Stop temperature control.

### Action: `auto-home`

- `Vendor2/GPT-5.2`: Home the device to its reference position
- `Vendor2/GPT-5.3-codex`: Home the device to its initial reference position.
- `Vendor2/GPT-5.4`: Initialize the device and move it to the home position.
- `gpt-5.4-mini`: Home the device to its initial position.

### Action: `auto-lock_plate`

- `Vendor2/GPT-5.2`: Lock/clamp the microplate
- `Vendor2/GPT-5.3-codex`: Lock the microplate.
- `Vendor2/GPT-5.4`: Lock the plate.
- `gpt-5.4-mini`: Lock the plate.

### Action: `auto-reset`

- `Vendor2/GPT-5.2`: Reset the device (recover from an error or stuck state)
- `Vendor2/GPT-5.3-codex`: Reset the device to clear error or stuck states.
- `Vendor2/GPT-5.4`: Reset the device to return it to a ready state.
- `gpt-5.4-mini`: Reset the device to recover a ready state.

### Action: `auto-set_temperature`

- `Vendor2/GPT-5.2`: set the temperature setpoint (start/maintain temperature control)
- `Vendor2/GPT-5.3-codex`: Set and start temperature control to the target temperature.
- `Vendor2/GPT-5.4`: Set the target temperature and start temperature control.
- `gpt-5.4-mini`: Set the target temperature.

### Action: `auto-setup`

- `Vendor2/GPT-5.2`: Initialize the device (reset and home it to a ready-to-run state)
- `Vendor2/GPT-5.3-codex`: Run setup initialization (reset and home).
- `Vendor2/GPT-5.4`: Perform device setup, including reset and homing.
- `gpt-5.4-mini`: Reset first and then home the device to complete initialization.

### Action: `auto-shake`

- `Vendor2/GPT-5.2`: Start shaking at the specified speed (and acceleration)
- `Vendor2/GPT-5.3-codex`: Start shaking/mixing at the set speed (and acceleration).
- `Vendor2/GPT-5.4`: Start shaking at the specified speed.
- `gpt-5.4-mini`: Start shaking at the specified speed and acceleration.

### Action: `auto-stop`

- `Vendor2/GPT-5.2`: Stop the device (overall stop)
- `Vendor2/GPT-5.3-codex`: Stop current device operation.
- `Vendor2/GPT-5.4`: Stop the device's current operation.
- `gpt-5.4-mini`: Stop the current operation.

### Action: `auto-stop_shaking`

- `Vendor2/GPT-5.2`: Stop shaking (optionally with a specified deceleration)
- `Vendor2/GPT-5.3-codex`: Stop shaking with the specified deceleration.
- `Vendor2/GPT-5.4`: Stop shaking.
- `gpt-5.4-mini`: Stop shaking and decelerate to a halt.

### Action: `auto-unlock_plate`

- `Vendor2/GPT-5.2`: Unlock/release the microplate
- `Vendor2/GPT-5.3-codex`: Unlock the microplate.
- `Vendor2/GPT-5.4`: Unlock the plate.
- `gpt-5.4-mini`: Unlock the plate.

### Action: `auto-supports_locking`

- `Vendor2/GPT-5.2`: get whether plate locking is supported
- `Vendor2/GPT-5.3-codex`: Get whether plate locking is supported.
- `Vendor2/GPT-5.4`: Get whether plate locking is supported.
- `gpt-5.4-mini`: Get whether plate locking is supported.

### Action: `auto-supports_active_cooling`

- `Vendor2/GPT-5.2`: get whether active cooling is supported
- `Vendor2/GPT-5.3-codex`: Get whether active cooling is supported.
- `Vendor2/GPT-5.4`: Get whether active cooling is supported.
- `gpt-5.4-mini`: Get whether active cooling is supported.

### Action: `auto-get_current_temperature`

- `Vendor2/GPT-5.2`: get the current temperature
- `Vendor2/GPT-5.3-codex`: Get the current temperature.
- `Vendor2/GPT-5.4`: Get the current temperature.
- `gpt-5.4-mini`: Get the current temperature.

### Tags

- `Vendor2/GPT-5.2`: 实验执行&合成设备, 生命体系, 溶液配制与反应, 细胞生物学研究, 热混匀仪
- `Vendor2/GPT-5.3-codex`: 备料&前处理设备, 实验执行&合成设备, 生命体系, 溶液配制与反应, 基因编辑、分子生物学与育种, 细胞生物学研究, 恒温摇床, 热混匀仪
- `Vendor2/GPT-5.4`: 备料&前处理设备, 实验执行&合成设备, 生命体系, 溶液配制与反应, 热混匀仪, 微孔板孵育与混匀, 微孔板恒温振荡器
- `gpt-5.4-mini`: 备料&前处理设备, 实验执行&合成设备, 生命体系, 溶液配制与反应, 恒温摇床, 热混匀仪, 分子生物学与生化实验, 微孔板恒温振荡器

## cc_core

### Device Name

- `Vendor2/GPT-5.2`: Central Controller (CC)
- `Vendor2/GPT-5.3-codex`: Central Controller (CC)
- `Vendor2/GPT-5.4`: Central Controller (CC)
- `gpt-5.4-mini`: Central Controller (CC)

### Device Description

- `Vendor2/GPT-5.2`: A central timing and sequencing controller for quantum experiments. It runs hardware sequence programs and coordinates synchronized triggers and digital control via digital I/O modules (e.g., CCIO). It supports digital I/O link calibration, delay tuning, and status monitoring, commonly used for deterministic timing control and diagnostics in setups such as superconducting qubit experiments.
- `Vendor2/GPT-5.3-codex`: This is a central timing and sequence-control instrument for quantum experiments. It coordinates CCIO-type submodules, runs sequence programs, starts/stops real-time control flow, and provides digital I/O calibration, delay adjustment, and status monitoring. It is commonly used for real-time control and synchronization in superconducting-qubit labs.
- `Vendor2/GPT-5.4`: This is a programmable sequence and timing control instrument for qubit experiments. It is used to assemble and run control sequences, distribute digital trigger and synchronization signals, coordinate CCIO interface modules, and support DIO calibration, status monitoring, and timing delay adjustment. It is commonly used in superconducting quantum computing experiments for pulse sequence execution, system synchronization, and bring-up.
- `gpt-5.4-mini`: A central timing and sequencing controller for quantum experiments. It runs hardware sequence programs and coordinates synchronized triggers and digital control via digital I/O modules (e.g., CCIO). It supports digital I/O link calibration, delay tuning, and status monitoring, commonly used for deterministic timing control and diagnostics in setups such as superconducting qubit experiments.

### Action: `auto-assemble`

- `Vendor2/GPT-5.2`: Assemble a sequence program string.
- `Vendor2/GPT-5.3-codex`: Assemble the sequence program string.
- `Vendor2/GPT-5.4`: Assemble the sequence program
- `gpt-5.4-mini`: Assemble a sequence program into an executable control sequence.

### Action: `auto-assemble_and_start`

- `Vendor2/GPT-5.2`: Assemble the sequence program and start the sequencers.
- `Vendor2/GPT-5.3-codex`: Assemble the sequence program and start the sequencers.
- `Vendor2/GPT-5.4`: Assemble the sequence program and start the sequencers
- `gpt-5.4-mini`: Assemble a sequence program and start the control sequence immediately.

### Action: `auto-calibrate_dio`

- `Vendor2/GPT-5.2`: Calibrate digital I/O for a specified CCIO (using an expected bit pattern).
- `Vendor2/GPT-5.3-codex`: Run digital I/O calibration for the specified CCIO.
- `Vendor2/GPT-5.4`: Calibrate the digital I/O interface
- `gpt-5.4-mini`: Calibrate the digital I/O timing against an expected bit pattern.

### Action: `auto-debug_get_ccio_reg`

- `Vendor2/GPT-5.2`: Read a specified CCIO debug register value.
- `Vendor2/GPT-5.3-codex`: Read a CCIO debug register.
- `Vendor2/GPT-5.4`: Read a CCIO debug register
- `gpt-5.4-mini`: Read a specified CCIO register for debugging.

### Action: `auto-debug_get_ccio_trace`

- `Vendor2/GPT-5.2`: Get debug trace data from a specified CCIO.
- `Vendor2/GPT-5.3-codex`: Read CCIO debug trace data.
- `Vendor2/GPT-5.4`: Read a CCIO debug trace
- `gpt-5.4-mini`: Read debug trace data from a specified CCIO.

### Action: `auto-debug_get_traces`

- `Vendor2/GPT-5.2`: Get debug traces in bulk using a CCIO mask.
- `Vendor2/GPT-5.3-codex`: Read debug traces for multiple CCIOs by mask.
- `Vendor2/GPT-5.4`: Read debug traces
- `gpt-5.4-mini`: Read debug traces from multiple CCIOs selected by a mask.

### Action: `auto-debug_marker_in`

- `Vendor2/GPT-5.2`: Route a debug marker to a specified CCIO input bit.
- `Vendor2/GPT-5.3-codex`: Route debug marker to an input bit.
- `Vendor2/GPT-5.4`: Route a debug marker to an input bit
- `gpt-5.4-mini`: Inject a debug marker on a specified bit line.

### Action: `auto-debug_marker_off`

- `Vendor2/GPT-5.2`: Turn off the debug marker function for a specified CCIO.
- `Vendor2/GPT-5.3-codex`: Turn off debug marker output.
- `Vendor2/GPT-5.4`: Turn off the debug marker
- `gpt-5.4-mini`: Turn off debug marker output for a specified CCIO.

### Action: `auto-debug_marker_out`

- `Vendor2/GPT-5.2`: Route a debug marker to a specified CCIO output bit.
- `Vendor2/GPT-5.3-codex`: Route debug marker to an output bit.
- `Vendor2/GPT-5.4`: Route a debug marker to an output bit
- `gpt-5.4-mini`: Output a debug marker on a specified bit line.

### Action: `auto-debug_set_ccio_trace_on`

- `Vendor2/GPT-5.2`: Enable trace capture on a specified CCIO (selecting a trace unit index).
- `Vendor2/GPT-5.3-codex`: Enable trace capture for a CCIO timing unit.
- `Vendor2/GPT-5.4`: Enable CCIO debug tracing
- `gpt-5.4-mini`: Enable trace capture on a specified CCIO.

### Action: `auto-print_status_operation`

- `Vendor2/GPT-5.2`: Read and print the Operation status information (combined CC core and CCIO).
- `Vendor2/GPT-5.3-codex`: Print operation status information.
- `Vendor2/GPT-5.4`: Print operation status information
- `gpt-5.4-mini`: Print the operation status summary.

### Action: `auto-print_status_questionable`

- `Vendor2/GPT-5.2`: Read and print the Questionable status information (combined CC core and CCIO).
- `Vendor2/GPT-5.3-codex`: Print questionable status information.
- `Vendor2/GPT-5.4`: Print questionable status information
- `gpt-5.4-mini`: Print the questionable status summary.

### Action: `auto-sequence_program_assemble`

- `Vendor2/GPT-5.2`: set the sequence program (upload and assemble the program string).
- `Vendor2/GPT-5.3-codex`: set sequence program string for assembly
- `Vendor2/GPT-5.4`: Set the sequence program string to assemble
- `gpt-5.4-mini`: Define the sequence program string to upload.

### Action: `auto-set_q1_reg`

- `Vendor2/GPT-5.2`: set a Q1 register value (only allowed when the CC is stopped).
- `Vendor2/GPT-5.3-codex`: set Q1 register value
- `Vendor2/GPT-5.4`: Set the Q1 register value
- `gpt-5.4-mini`: Set the Q1 register of a specified CCIO.

### Action: `auto-set_seqbar_cnt`

- `Vendor2/GPT-5.2`: Set a sequence barrier/counter value for a specified CCIO (no need to stop the CC).
- `Vendor2/GPT-5.3-codex`: Set the sequence barrier count value.
- `Vendor2/GPT-5.4`: Set the sequence barrier counter
- `gpt-5.4-mini`: Set the sequence bar counter of a specified CCIO.

### Action: `auto-set_status_operation_run_enable`

- `Vendor2/GPT-5.2`: set the enable for Operation:RUN status reporting.
- `Vendor2/GPT-5.3-codex`: set operation run status enable
- `Vendor2/GPT-5.4`: Set the operation run status event enable
- `gpt-5.4-mini`: Define whether run status reporting is enabled.

### Action: `auto-set_status_questionable_bplink_enable`

- `Vendor2/GPT-5.2`: set the enable for Questionable status: backplane link (BPLINK) reporting.
- `Vendor2/GPT-5.3-codex`: set questionable bplink status enable
- `Vendor2/GPT-5.4`: Set the questionable backplane link status event enable
- `gpt-5.4-mini`: Define whether link questionable-status reporting is enabled.

### Action: `auto-set_status_questionable_config_enable`

- `Vendor2/GPT-5.2`: set the enable for Questionable status: configuration (CONFIG) reporting.
- `Vendor2/GPT-5.3-codex`: set questionable config status enable
- `Vendor2/GPT-5.4`: Set the questionable configuration status event enable
- `gpt-5.4-mini`: Define whether configuration questionable-status reporting is enabled.

### Action: `auto-set_status_questionable_frequency_enable`

- `Vendor2/GPT-5.2`: set the enable for Questionable status: frequency (FREQUENCY) reporting.
- `Vendor2/GPT-5.3-codex`: set questionable frequency status enable
- `Vendor2/GPT-5.4`: Set the questionable frequency status event enable
- `gpt-5.4-mini`: Define whether frequency questionable-status reporting is enabled.

### Action: `auto-set_status_questionable_instrument_enable`

- `Vendor2/GPT-5.2`: set the enable for Questionable status: instrument (INSTRUMENT) reporting.
- `Vendor2/GPT-5.3-codex`: set questionable instrument status enable
- `Vendor2/GPT-5.4`: Set the questionable instrument status event enable
- `gpt-5.4-mini`: Define whether instrument questionable-status reporting is enabled.

### Action: `auto-set_status_questionable_instrument_idetail_bplink_enable`

- `Vendor2/GPT-5.2`: set the enable for Questionable status: instrument detail—BPLINK reporting (per CCIO).
- `Vendor2/GPT-5.3-codex`: set instrument idetail bplink status enable
- `Vendor2/GPT-5.4`: Set the detailed questionable backplane link status event enable for a selected instrument
- `gpt-5.4-mini`: Define whether instrument bplink detail questionable-status reporting is enabled.

### Action: `auto-set_status_questionable_instrument_idetail_config_enable`

- `Vendor2/GPT-5.2`: set the enable for Questionable status: instrument detail—CONFIG reporting (per CCIO).
- `Vendor2/GPT-5.3-codex`: set instrument idetail config status enable
- `Vendor2/GPT-5.4`: Set the detailed questionable configuration status event enable for a selected instrument
- `gpt-5.4-mini`: Define whether instrument config detail questionable-status reporting is enabled.

### Action: `auto-set_status_questionable_instrument_idetail_diocal_enable`

- `Vendor2/GPT-5.2`: set the enable for Questionable status: instrument detail—DIO calibration (DIOCAL) reporting (per CCIO).
- `Vendor2/GPT-5.3-codex`: set instrument idetail diocal status enable
- `Vendor2/GPT-5.4`: Set the detailed questionable DIO calibration status event enable for a selected instrument
- `gpt-5.4-mini`: Define whether instrument DIO calibration detail questionable-status reporting is enabled.

### Action: `auto-set_status_questionable_instrument_idetail_freq_enable`

- `Vendor2/GPT-5.2`: set the enable for Questionable status: instrument detail—frequency (FREQ) reporting (per CCIO).
- `Vendor2/GPT-5.3-codex`: set instrument idetail freq status enable
- `Vendor2/GPT-5.4`: Set the detailed questionable frequency status event enable for a selected instrument
- `gpt-5.4-mini`: Define whether instrument frequency detail questionable-status reporting is enabled.

### Action: `auto-set_status_questionable_instrument_isummary_enable`

- `Vendor2/GPT-5.2`: set the enable for Questionable status: instrument summary (ISUMMARY) reporting (per CCIO).
- `Vendor2/GPT-5.3-codex`: set instrument isummary status enable
- `Vendor2/GPT-5.4`: Set the summary questionable status event enable for a selected instrument
- `gpt-5.4-mini`: Define whether instrument summary questionable-status reporting is enabled.

### Action: `auto-set_vsm_delay_fall`

- `Vendor2/GPT-5.2`: set the falling-edge delay for a specified CCIO bit (in 833 ps step counts).
- `Vendor2/GPT-5.3-codex`: set VSM fall delay count
- `Vendor2/GPT-5.4`: Set the VSM falling-edge delay
- `gpt-5.4-mini`: Define the VSM falling-edge delay for a specified bit.

### Action: `auto-set_vsm_delay_rise`

- `Vendor2/GPT-5.2`: set the rising-edge delay for a specified CCIO bit (in 833 ps step counts).
- `Vendor2/GPT-5.3-codex`: set VSM rise delay count
- `Vendor2/GPT-5.4`: Set the VSM rising-edge delay
- `gpt-5.4-mini`: Define the VSM rising-edge delay for a specified bit.

### Action: `auto-start`

- `Vendor2/GPT-5.2`: Start the CC sequencers (optionally block until start is complete).
- `Vendor2/GPT-5.3-codex`: Start the CC sequencers.
- `Vendor2/GPT-5.4`: Start the sequencers
- `gpt-5.4-mini`: Start the CC sequencers.

### Action: `auto-status_preset`

- `Vendor2/GPT-5.2`: Preset/initialize status reporting settings (enable event reporting that is off by default).
- `Vendor2/GPT-5.3-codex`: Apply status preset and enable SCPI event reporting.
- `Vendor2/GPT-5.4`: Enable standard status event reporting
- `gpt-5.4-mini`: Enable event reporting that is off by default.

### Action: `auto-stop`

- `Vendor2/GPT-5.2`: Stop the CC sequencers (optionally block until stop is complete).
- `Vendor2/GPT-5.3-codex`: Stop the CC sequencers.
- `Vendor2/GPT-5.4`: Stop the sequencers
- `gpt-5.4-mini`: Stop the CC sequencers.

### Action: `auto-get_sequence_program_assemble`

- `Vendor2/GPT-5.2`: get the sequence program (download the program string).
- `Vendor2/GPT-5.3-codex`: get sequence program string for assembly
- `Vendor2/GPT-5.4`: Get the sequence program string to assemble
- `gpt-5.4-mini`: Get the sequence program string to upload.

### Action: `auto-get_assembler_success`

- `Vendor2/GPT-5.2`: get whether the assembler succeeded.
- `Vendor2/GPT-5.3-codex`: get assembler success status
- `Vendor2/GPT-5.4`: Get whether assembly succeeded
- `gpt-5.4-mini`: Get whether sequence program assembly succeeded.

### Action: `auto-get_assembler_log`

- `Vendor2/GPT-5.2`: get the assembler log output.
- `Vendor2/GPT-5.3-codex`: get assembler log
- `Vendor2/GPT-5.4`: Get the assembler log
- `gpt-5.4-mini`: Get the sequence program assembly log.

### Action: `auto-get_q1_reg`

- `Vendor2/GPT-5.2`: get a Q1 register value (only allowed when the CC is stopped).
- `Vendor2/GPT-5.3-codex`: get Q1 register value
- `Vendor2/GPT-5.4`: Get the Q1 register value
- `gpt-5.4-mini`: Get the Q1 register value of a specified CCIO.

### Action: `auto-get_calibrate_dio_success`

- `Vendor2/GPT-5.2`: get whether DIO calibration succeeded (per CCIO).
- `Vendor2/GPT-5.3-codex`: get DIO calibration success status
- `Vendor2/GPT-5.4`: Get whether DIO calibration succeeded
- `gpt-5.4-mini`: Get whether DIO calibration succeeded.

### Action: `auto-get_calibrate_dio_status`

- `Vendor2/GPT-5.2`: get DIO calibration status (per CCIO).
- `Vendor2/GPT-5.3-codex`: get DIO calibration status
- `Vendor2/GPT-5.4`: Get the DIO calibration status
- `gpt-5.4-mini`: Get the DIO calibration status.

### Action: `auto-get_calibrate_dio_read_index`

- `Vendor2/GPT-5.2`: get the DIO calibration read index (per CCIO).
- `Vendor2/GPT-5.3-codex`: get DIO calibration read index
- `Vendor2/GPT-5.4`: Get the DIO calibration read index
- `gpt-5.4-mini`: Get the DIO calibration read index.

### Action: `auto-get_calibrate_dio_margin`

- `Vendor2/GPT-5.2`: get the DIO calibration margin (per CCIO).
- `Vendor2/GPT-5.3-codex`: get DIO calibration margin
- `Vendor2/GPT-5.4`: Get the DIO calibration margin
- `gpt-5.4-mini`: Get the DIO calibration margin.

### Action: `auto-get_vsm_delay_rise`

- `Vendor2/GPT-5.2`: get the rising-edge delay for a specified CCIO bit.
- `Vendor2/GPT-5.3-codex`: get VSM rise delay count
- `Vendor2/GPT-5.4`: Get the VSM rising-edge delay
- `gpt-5.4-mini`: Get the VSM rising-edge delay for a specified bit.

### Action: `auto-get_vsm_delay_fall`

- `Vendor2/GPT-5.2`: get the falling-edge delay for a specified CCIO bit.
- `Vendor2/GPT-5.3-codex`: get VSM fall delay count
- `Vendor2/GPT-5.4`: Get the VSM falling-edge delay
- `gpt-5.4-mini`: Get the VSM falling-edge delay for a specified bit.

### Action: `auto-get_status_questionable_frequency`

- `Vendor2/GPT-5.2`: get Questionable status: frequency (FREQUENCY).
- `Vendor2/GPT-5.3-codex`: get questionable frequency status
- `Vendor2/GPT-5.4`: Get the questionable frequency status
- `gpt-5.4-mini`: Get the frequency questionable status.

### Action: `auto-get_status_questionable_frequency_enable`

- `Vendor2/GPT-5.2`: get the enable for Questionable status: frequency (FREQUENCY) reporting.
- `Vendor2/GPT-5.3-codex`: get questionable frequency status enable
- `Vendor2/GPT-5.4`: Get the questionable frequency status event enable
- `gpt-5.4-mini`: Get whether frequency questionable-status reporting is enabled.

### Action: `auto-get_status_questionable_config`

- `Vendor2/GPT-5.2`: get Questionable status: configuration (CONFIG).
- `Vendor2/GPT-5.3-codex`: get questionable config status
- `Vendor2/GPT-5.4`: Get the questionable configuration status
- `gpt-5.4-mini`: Get the configuration questionable status.

### Action: `auto-get_status_questionable_config_enable`

- `Vendor2/GPT-5.2`: get the enable for Questionable status: configuration (CONFIG) reporting.
- `Vendor2/GPT-5.3-codex`: get questionable config status enable
- `Vendor2/GPT-5.4`: Get the questionable configuration status event enable
- `gpt-5.4-mini`: Get whether configuration questionable-status reporting is enabled.

### Action: `auto-get_status_questionable_bplink`

- `Vendor2/GPT-5.2`: get Questionable status: backplane link (BPLINK).
- `Vendor2/GPT-5.3-codex`: get questionable bplink status
- `Vendor2/GPT-5.4`: Get the questionable backplane link status
- `gpt-5.4-mini`: Get the link questionable status.

### Action: `auto-get_status_questionable_bplink_enable`

- `Vendor2/GPT-5.2`: get the enable for Questionable status: backplane link (BPLINK) reporting.
- `Vendor2/GPT-5.3-codex`: get questionable bplink status enable
- `Vendor2/GPT-5.4`: Get the questionable backplane link status event enable
- `gpt-5.4-mini`: Get whether link questionable-status reporting is enabled.

### Action: `auto-get_status_operation_run`

- `Vendor2/GPT-5.2`: get Operation status: RUN.
- `Vendor2/GPT-5.3-codex`: get operation run status
- `Vendor2/GPT-5.4`: Get the operation run status
- `gpt-5.4-mini`: Get the run status.

### Action: `auto-get_status_operation_run_enable`

- `Vendor2/GPT-5.2`: get the enable for Operation:RUN status reporting.
- `Vendor2/GPT-5.3-codex`: get operation run status enable
- `Vendor2/GPT-5.4`: Get the operation run status event enable
- `gpt-5.4-mini`: Get whether run status reporting is enabled.

### Action: `auto-get_status_questionable_instrument`

- `Vendor2/GPT-5.2`: get Questionable status: instrument (INSTRUMENT).
- `Vendor2/GPT-5.3-codex`: get questionable instrument status
- `Vendor2/GPT-5.4`: Get the questionable instrument status
- `gpt-5.4-mini`: Get the instrument questionable status.

### Action: `auto-get_status_questionable_instrument_enable`

- `Vendor2/GPT-5.2`: get the enable for Questionable status: instrument (INSTRUMENT) reporting.
- `Vendor2/GPT-5.3-codex`: get questionable instrument status enable
- `Vendor2/GPT-5.4`: Get the questionable instrument status event enable
- `gpt-5.4-mini`: Get whether instrument questionable-status reporting is enabled.

### Action: `auto-get_status_questionable_instrument_isummary`

- `Vendor2/GPT-5.2`: get Questionable status: instrument summary (ISUMMARY, per CCIO).
- `Vendor2/GPT-5.3-codex`: get instrument isummary status
- `Vendor2/GPT-5.4`: Get the summary questionable status for a selected instrument
- `gpt-5.4-mini`: Get the instrument summary questionable status.

### Action: `auto-get_status_questionable_instrument_isummary_enable`

- `Vendor2/GPT-5.2`: get the enable for Questionable status: instrument summary (ISUMMARY) reporting (per CCIO).
- `Vendor2/GPT-5.3-codex`: get instrument isummary status enable
- `Vendor2/GPT-5.4`: Get the summary questionable status event enable for a selected instrument
- `gpt-5.4-mini`: Get whether instrument summary questionable-status reporting is enabled.

### Action: `auto-get_status_questionable_instrument_idetail_freq`

- `Vendor2/GPT-5.2`: get Questionable status: instrument detail—frequency (per CCIO).
- `Vendor2/GPT-5.3-codex`: get instrument idetail freq status
- `Vendor2/GPT-5.4`: Get the detailed questionable frequency status for a selected instrument
- `gpt-5.4-mini`: Get the instrument frequency detail questionable status.

### Action: `auto-get_status_questionable_instrument_idetail_freq_enable`

- `Vendor2/GPT-5.2`: get the enable for Questionable status: instrument detail—frequency reporting (per CCIO).
- `Vendor2/GPT-5.3-codex`: get instrument idetail freq status enable
- `Vendor2/GPT-5.4`: Get the detailed questionable frequency status event enable for a selected instrument
- `gpt-5.4-mini`: Get whether instrument frequency detail questionable-status reporting is enabled.

### Action: `auto-get_status_questionable_instrument_idetail_config`

- `Vendor2/GPT-5.2`: get Questionable status: instrument detail—configuration (per CCIO).
- `Vendor2/GPT-5.3-codex`: get instrument idetail config status
- `Vendor2/GPT-5.4`: Get the detailed questionable configuration status for a selected instrument
- `gpt-5.4-mini`: Get the instrument config detail questionable status.

### Action: `auto-get_status_questionable_instrument_idetail_config_enable`

- `Vendor2/GPT-5.2`: get the enable for Questionable status: instrument detail—configuration reporting (per CCIO).
- `Vendor2/GPT-5.3-codex`: get instrument idetail config status enable
- `Vendor2/GPT-5.4`: Get the detailed questionable configuration status event enable for a selected instrument
- `gpt-5.4-mini`: Get whether instrument config detail questionable-status reporting is enabled.

### Action: `auto-get_status_questionable_instrument_idetail_bplink`

- `Vendor2/GPT-5.2`: get Questionable status: instrument detail—backplane link (per CCIO).
- `Vendor2/GPT-5.3-codex`: get instrument idetail bplink status
- `Vendor2/GPT-5.4`: Get the detailed questionable backplane link status for a selected instrument
- `gpt-5.4-mini`: Get the instrument bplink detail questionable status.

### Action: `auto-get_status_questionable_instrument_idetail_bplink_enable`

- `Vendor2/GPT-5.2`: get the enable for Questionable status: instrument detail—backplane link reporting (per CCIO).
- `Vendor2/GPT-5.3-codex`: get instrument idetail bplink status enable
- `Vendor2/GPT-5.4`: Get the detailed questionable backplane link status event enable for a selected instrument
- `gpt-5.4-mini`: Get whether instrument bplink detail questionable-status reporting is enabled.

### Action: `auto-get_status_questionable_instrument_idetail_diocal`

- `Vendor2/GPT-5.2`: get Questionable status: instrument detail—DIO calibration (per CCIO).
- `Vendor2/GPT-5.3-codex`: get instrument idetail diocal status
- `Vendor2/GPT-5.4`: Get the detailed questionable DIO calibration status for a selected instrument
- `gpt-5.4-mini`: Get the instrument DIO calibration detail questionable status.

### Action: `auto-get_status_questionable_instrument_idetail_diocal_enable`

- `Vendor2/GPT-5.2`: get the enable for Questionable status: instrument detail—DIO calibration reporting (per CCIO).
- `Vendor2/GPT-5.3-codex`: get instrument idetail diocal status enable
- `Vendor2/GPT-5.4`: Get the detailed questionable DIO calibration status event enable for a selected instrument
- `gpt-5.4-mini`: Get whether instrument DIO calibration detail questionable-status reporting is enabled.

### Tags

- `Vendor2/GPT-5.2`: 实验执行&合成设备, 量子测控与时序控制, 超导量子比特实验, 中央时序与序列控制器
- `Vendor2/GPT-5.3-codex`: 实验执行&合成设备, 量子信息与精密测控, 超导量子比特实验, 中央时序序列控制器
- `Vendor2/GPT-5.4`: 实验执行&合成设备, 量子信息与量子器件, 超导量子比特实验, 量子实验中央控制器
- `gpt-5.4-mini`: 物流/机械, 器件/细胞设备, 量子实验控制, 超导量子比特控制, 中央时序控制器

## cryo_tel_gt

### Device Name

- `Vendor2/GPT-5.2`: Sunpower CryoTel GT Cryocooler
- `Vendor2/GPT-5.3-codex`: Sunpower CryoTel GT Cryocooler
- `Vendor2/GPT-5.4`: Sunpower CryoTel GT Cryocooler
- `gpt-5.4-mini`: CryoTel GT Cryocooler

### Device Description

- `Vendor2/GPT-5.2`: The Sunpower CryoTel GT is a closed-cycle cryocooler (with controller) used in laboratories to provide cooling power for a cold stage/cryogenic assembly and stabilize it near a target temperature. It supports reading operating status such as temperature and power, and basic operation in temperature or power control modes including start/stop control.
- `Vendor2/GPT-5.3-codex`: The CryoTel GT is a laboratory cryocooler used to provide a stable low-temperature environment for experimental loads. It supports temperature-control or power-control operation, allows monitoring of current temperature and power, and lets users set temperature/power targets and limits for low-temperature testing and sample cooling.
- `Vendor2/GPT-5.4`: This is a mechanical cryocooler used in low-temperature laboratory experiments to provide cooling for sample stages, detectors, or other cryogenic components. It is typically used to read the current temperature, set a target temperature or power, and monitor operating status and fault conditions.
- `gpt-5.4-mini`: A Sunpower CryoTel GT closed-cycle cryocooler used in laboratories for low-temperature generation, sample cooling, and temperature maintenance.

### Action: `auto-at_temperature_band`

- `Vendor2/GPT-5.2`: get/set the “at-temperature” temperature band (K)
- `Vendor2/GPT-5.3-codex`: Get/set the at-temperature band (K).
- `Vendor2/GPT-5.4`: Get/set the at-temperature band.
- `gpt-5.4-mini`: define the temperature band threshold for the at-temperature indication/output.

### Action: `auto-control_mode`

- `Vendor2/GPT-5.2`: get/set the control mode (power mode / temperature mode)
- `Vendor2/GPT-5.3-codex`: Get/set the control mode (power mode or temperature mode).
- `Vendor2/GPT-5.4`: Get/set the control mode.
- `gpt-5.4-mini`: define the control mode (power mode or temperature mode).

### Action: `auto-ki`

- `Vendor2/GPT-5.2`: get/set the temperature control loop integral constant (Ki)
- `Vendor2/GPT-5.3-codex`: Get/set the temperature-loop integral constant (Ki).
- `Vendor2/GPT-5.4`: Get/set the integral constant of the temperature control loop.
- `gpt-5.4-mini`: define the integral gain of the temperature control loop.

### Action: `auto-kp`

- `Vendor2/GPT-5.2`: get/set the temperature control loop proportional constant (Kp)
- `Vendor2/GPT-5.3-codex`: Get/set the temperature-loop proportional constant (Kp).
- `Vendor2/GPT-5.4`: Get/set the proportional constant of the temperature control loop.
- `gpt-5.4-mini`: define the proportional gain of the temperature control loop.

### Action: `auto-power_max`

- `Vendor2/GPT-5.2`: get/set the user-defined maximum power limit (W)
- `Vendor2/GPT-5.3-codex`: Get/set the user-defined maximum power limit (W).
- `Vendor2/GPT-5.4`: Get/set the user-defined maximum power limit.
- `gpt-5.4-mini`: define the user-set maximum power limit.

### Action: `auto-power_min`

- `Vendor2/GPT-5.2`: get/set the user-defined minimum power limit (W)
- `Vendor2/GPT-5.3-codex`: Get/set the user-defined minimum power limit (W).
- `Vendor2/GPT-5.4`: Get/set the user-defined minimum power limit.
- `gpt-5.4-mini`: define the user-set minimum power limit.

### Action: `auto-power_setpoint`

- `Vendor2/GPT-5.2`: get/set the power setpoint (W)
- `Vendor2/GPT-5.3-codex`: Get/set the power setpoint (W).
- `Vendor2/GPT-5.4`: Get/set the power setpoint.
- `gpt-5.4-mini`: define the target power used in power control mode.

### Action: `auto-query`

- `Vendor2/GPT-5.2`: send a query/set command to the cryocooler controller and read the response
- `Vendor2/GPT-5.3-codex`: Send a query command, optionally set a value, and read the response.
- `Vendor2/GPT-5.4`: Send a query or setting command to the cryocooler and return the response.
- `gpt-5.4-mini`: send a query command to the cryocooler and read back the response.

### Action: `auto-query_multiline`

- `Vendor2/GPT-5.2`: send a query that returns multiple lines and read the response
- `Vendor2/GPT-5.3-codex`: Send a multiline query command and read multiline responses.
- `Vendor2/GPT-5.4`: Send a multiline query to the cryocooler and read multiple response lines.
- `gpt-5.4-mini`: send a multi-line query command and read the returned lines.

### Action: `auto-reset`

- `Vendor2/GPT-5.2`: reset the cryocooler controller to factory defaults
- `Vendor2/GPT-5.3-codex`: Reset the cryocooler to factory defaults.
- `Vendor2/GPT-5.4`: Reset the cryocooler to factory defaults.
- `gpt-5.4-mini`: reset the cryocooler to factory default settings.

### Action: `auto-save_control_mode`

- `Vendor2/GPT-5.2`: save the current control mode as the power-up default
- `Vendor2/GPT-5.3-codex`: Save the current control mode as the default mode.
- `Vendor2/GPT-5.4`: Save the current control mode as the default control mode.
- `gpt-5.4-mini`: save the current control mode as the default control mode.

### Action: `auto-sendcmd`

- `Vendor2/GPT-5.2`: send a command to the cryocooler controller (no response readback)
- `Vendor2/GPT-5.3-codex`: Send a raw command to the cryocooler.
- `Vendor2/GPT-5.4`: Send a command to the cryocooler.
- `gpt-5.4-mini`: send a control command to the cryocooler.

### Action: `auto-stop`

- `Vendor2/GPT-5.2`: get/set the stop state (stop/start)
- `Vendor2/GPT-5.3-codex`: Get/set the stop state (stop/start).
- `Vendor2/GPT-5.4`: Get/set the stop state.
- `gpt-5.4-mini`: define whether the cryocooler is stopped or running.

### Action: `auto-stop_mode`

- `Vendor2/GPT-5.2`: get/set the stop control source mode
- `Vendor2/GPT-5.3-codex`: Get/set the stop mode (host or digital I/O).
- `Vendor2/GPT-5.4`: Get/set the stop mode.
- `gpt-5.4-mini`: define the stop mode (host control or digital I/O control).

### Action: `auto-temperature_setpoint`

- `Vendor2/GPT-5.2`: get/set the temperature setpoint (K)
- `Vendor2/GPT-5.3-codex`: Get/set the temperature setpoint (K).
- `Vendor2/GPT-5.4`: Get/set the temperature setpoint.
- `gpt-5.4-mini`: define the target temperature used in temperature control mode.

### Action: `auto-thermostat`

- `Vendor2/GPT-5.2`: get/set the thermostat mode enable/disable
- `Vendor2/GPT-5.3-codex`: Get/set the thermostat mode on/off state.
- `Vendor2/GPT-5.4`: Get/set the thermostat mode.
- `gpt-5.4-mini`: define whether thermostat mode is enabled.

### Action: `auto-errors`

- `Vendor2/GPT-5.2`: get the list of currently active error codes
- `Vendor2/GPT-5.3-codex`: Get the list of currently active error codes.
- `Vendor2/GPT-5.4`: Get the currently active error codes.
- `gpt-5.4-mini`: read the currently active error codes.

### Action: `auto-power`

- `Vendor2/GPT-5.2`: get the current power (W)
- `Vendor2/GPT-5.3-codex`: Get the current power (W).
- `Vendor2/GPT-5.4`: Get the current power.
- `gpt-5.4-mini`: read the current output power.

### Action: `auto-power_current_and_limits`

- `Vendor2/GPT-5.2`: get the current power and the allowable power limits at the current temperature (W)
- `Vendor2/GPT-5.3-codex`: Get current power and power limit values (W).
- `Vendor2/GPT-5.4`: Get the current power and power limits.
- `gpt-5.4-mini`: read the current power and the allowable power limits.

### Action: `auto-serial_number`

- `Vendor2/GPT-5.2`: get the device serial number and revision information
- `Vendor2/GPT-5.3-codex`: Get the device serial number and revision information.
- `Vendor2/GPT-5.4`: Get the serial number and revision.
- `gpt-5.4-mini`: read the serial number and revision information.

### Action: `auto-state`

- `Vendor2/GPT-5.2`: get a list of controller control parameters and their current values
- `Vendor2/GPT-5.3-codex`: Get the controller parameter/state list.
- `Vendor2/GPT-5.4`: Get the list of control parameters and their current values.
- `gpt-5.4-mini`: read a list of control parameters and their current states.

### Action: `auto-temperature`

- `Vendor2/GPT-5.2`: get the current temperature (K)
- `Vendor2/GPT-5.3-codex`: Get the current temperature (K).
- `Vendor2/GPT-5.4`: Get the current temperature.
- `gpt-5.4-mini`: read the current temperature.

### Action: `auto-thermostat_status`

- `Vendor2/GPT-5.2`: get the current thermostat status (on/off)
- `Vendor2/GPT-5.3-codex`: Get the current thermostat status (on/off).
- `Vendor2/GPT-5.4`: Get the thermostat status.
- `gpt-5.4-mini`: read the current thermostat mode status.

### Tags

- `Vendor2/GPT-5.2`: 实验执行&合成设备, 低温制冷与低温实验支撑, 低温平台与冷台稳温, 闭循环低温制冷机
- `Vendor2/GPT-5.3-codex`: 表征设备, 备料&前处理设备, 智慧表征与检测中心, 物化表征测试中心, 冷热水机, 低温制冷机
- `Vendor2/GPT-5.4`: 实验执行&合成设备, 低温实验与低温工程, 样品台与探测器低温冷却, 低温制冷机
- `gpt-5.4-mini`: 物流/机械, 冷热水机, 低温实验与样品冷却, 低温制冷与温度维持, 低温制冷机

## cvd_control

### Device Name

- `Vendor2/GPT-5.2`: CVD Process Control System
- `Vendor2/GPT-5.3-codex`: Chemical Vapor Deposition (CVD) System Controller
- `Vendor2/GPT-5.4`: Chemical Vapor Deposition Process Control System
- `gpt-5.4-mini`: Chemical Vapor Deposition Controller

### Device Description

- `Vendor2/GPT-5.2`: A process control system for Chemical Vapor Deposition (CVD) experiments, typically integrating reactor temperature setpoint control, recipe (step) execution, and multi-gas flow setpoint/monitoring (commonly via mass flow controllers, MFCs). It supports starting/stopping a recipe and managing process setpoints and parameter trends during deposition runs.
- `Vendor2/GPT-5.3-codex`: A process control interface for a chemical vapor deposition (CVD) setup, typically handling temperature and multi-gas flow recipes for run control and monitoring. It is used in lab workflows to manage recipe files, apply setpoints, and view process trend plots during CVD thin-film growth experiments.
- `Vendor2/GPT-5.4`: A chemical vapor deposition (CVD) process control system used with a reactor chamber, heater or furnace, and multiple gas flow control components. It is used to define and run deposition recipes, adjust temperature and gas flow parameters, and monitor process trends during thin-film growth and materials synthesis experiments.
- `gpt-5.4-mini`: A control unit for chemical vapor deposition (CVD) processes, used to set gas flows and temperature, save/load process recipes, and start or stop operation.

### Action: `auto-return_ui_fields`

- `Vendor2/GPT-5.2`: Get the current recipe/setpoint fields from the control interface
- `Vendor2/GPT-5.3-codex`: Return the current process-parameter field values from the UI.
- `Vendor2/GPT-5.4`: Retrieve the currently configured parameter fields and setpoints for the CVD process.
- `gpt-5.4-mini`: Read and refresh the process parameter fields shown in the interface.

### Action: `auto-save_recipe`

- `Vendor2/GPT-5.2`: Save a process recipe to a file (including metadata and gas column information)
- `Vendor2/GPT-5.3-codex`: Save the current CVD process recipe to a file (including metadata and parameter table).
- `Vendor2/GPT-5.4`: Save the current deposition recipe for later reuse.
- `gpt-5.4-mini`: Save the current process parameters and metadata to a recipe file.

### Action: `auto-open_recipe`

- `Vendor2/GPT-5.2`: Open a process recipe from a file and load it into the control interface
- `Vendor2/GPT-5.3-codex`: Open a CVD process recipe file and load it into the control interface.
- `Vendor2/GPT-5.4`: Open and load a previously saved process recipe into the system.
- `gpt-5.4-mini`: Open a recipe file and load its process parameters.

### Action: `auto-update_plot`

- `Vendor2/GPT-5.2`: Update process trend plots (e.g., multi-gas flow vs. time)
- `Vendor2/GPT-5.3-codex`: Update the process trend plots (such as time-varying gas flow channels).
- `Vendor2/GPT-5.4`: Refresh the process trend plot, such as gas flow versus time.
- `gpt-5.4-mini`: Update the run trend plots for gas flow and related variables.

### Action: `auto-start_recipe`

- `Vendor2/GPT-5.2`: Start running a recipe and begin executing process steps
- `Vendor2/GPT-5.3-codex`: Start recipe execution and begin process monitoring.
- `Vendor2/GPT-5.4`: Start and execute the currently configured CVD process recipe.
- `gpt-5.4-mini`: Start recipe execution and show the running status.

### Action: `auto-stop_recipe`

- `Vendor2/GPT-5.2`: Stop the currently running recipe
- `Vendor2/GPT-5.3-codex`: Stop the current recipe run.
- `Vendor2/GPT-5.4`: Stop the process recipe that is currently running.
- `gpt-5.4-mini`: Stop recipe execution.

### Action: `auto-apply_setpoints`

- `Vendor2/GPT-5.2`: Apply current setpoints (e.g., temperature and gas flow setpoints) to process control
- `Vendor2/GPT-5.3-codex`: Apply process setpoints (e.g., temperature/flow) to the system.
- `Vendor2/GPT-5.4`: Apply the currently configured process setpoints, such as temperature and gas flow parameters.
- `gpt-5.4-mini`: Apply the current setpoints, such as temperature and gas parameters.

### Tags

- `Vendor2/GPT-5.2`: 实验执行&合成设备, 表面/薄膜体系, 二维材料, 有机光伏材料（OPV和OLED）, 化学气相沉积设备, CVD工艺控制系统
- `Vendor2/GPT-5.3-codex`: 实验执行&合成设备, 表面/薄膜体系, 涂层材料, 化学气相沉积设备
- `Vendor2/GPT-5.4`: 实验执行&合成设备, 表面/薄膜体系, 涂层材料, 化学气相沉积设备, 薄膜生长与CVD沉积, CVD工艺控制系统
- `gpt-5.4-mini`: 实验执行&合成设备, 表面/薄膜体系, 化学气相沉积设备, 化学气相沉积工艺, 化学气相沉积控制器

## cytomat_backend

### Device Name

- `Vendor2/GPT-5.2`: Cytomat automated incubator microplate storage system
- `Vendor2/GPT-5.3-codex`: Cytomat Automated Microplate Incubator-Storage System
- `Vendor2/GPT-5.4`: Cytomat automated microplate incubator
- `gpt-5.4-mini`: Cytomat Automated Incubator

### Device Description

- `Vendor2/GPT-5.2`: Cytomat is an incubator-style automated microplate storage system for storing and handling microplates (e.g., MTP/deep-well plates). It typically provides internal rack locations, an external transfer station, and an automated door mechanism, maintaining controlled incubation conditions (e.g., temperature, CO₂, O₂, humidity). An internal transport mechanism moves plates between storage, wait, and exposed/transfer positions for integration with robotic arms and automation workflows in cell culture, incubation steps, and plate staging.
- `Vendor2/GPT-5.3-codex`: This device is an automated microplate incubator and storage unit for laboratory workflows. It maintains controlled temperature, CO2, O2, and humidity conditions, and uses internal handling mechanics to move plates between storage, wait, transfer, and exposed positions. It also supports barcode reading and shaking incubation.
- `Vendor2/GPT-5.4`: The Cytomat automated microplate incubator is a plate storage and incubation unit with an internal robotic transport mechanism. It stores and incubates microplates under controlled temperature, CO2, O2, and humidity conditions. It is commonly used in cell culture, assay workflows, and high-throughput screening to automatically move plates between storage sites, wait positions, transfer stations, and external access positions, with support for shaking incubation and barcode reading.
- `gpt-5.4-mini`: An automated incubator and storage system for microplates and sample carriers, typically used with robotic handling; it supports rack management, a transfer station, door control, shaking, and environmental control of temperature, CO2, humidity, and O2 for cell culture and automated lab workflows.

### Action: `auto-action_exposed_to_storage`

- `Vendor2/GPT-5.2`: Return a microplate from the exposed external position and place it into the specified storage site.
- `Vendor2/GPT-5.3-codex`: Move a microplate from the exposed external position back to a storage position.
- `Vendor2/GPT-5.4`: Return a microplate from the exposed external position to a storage site
- `gpt-5.4-mini`: Move a plate from the exposed position back into storage.

### Action: `auto-action_exposed_to_wait`

- `Vendor2/GPT-5.2`: Return a microplate from the exposed external position to the wait position.
- `Vendor2/GPT-5.3-codex`: Return a microplate from the exposed position to the wait position.
- `Vendor2/GPT-5.4`: Return a microplate from the exposed external position to the wait position
- `gpt-5.4-mini`: Move a plate from the exposed position back to the wait position.

### Action: `auto-action_read_barcode`

- `Vendor2/GPT-5.2`: Read barcode information for specified storage locations (for plate/location identification).
- `Vendor2/GPT-5.3-codex`: Read barcode information from specified storage locations.
- `Vendor2/GPT-5.4`: Read the barcode of specified storage locations
- `gpt-5.4-mini`: Read the barcode at the specified storage locations.

### Action: `auto-action_storage_to_exposed`

- `Vendor2/GPT-5.2`: Retrieve a microplate from the specified storage site and move it to an exposed position outside the instrument.
- `Vendor2/GPT-5.3-codex`: Move a microplate from storage to the exposed external position.
- `Vendor2/GPT-5.4`: Move a microplate from storage to the exposed external position
- `gpt-5.4-mini`: Move a plate from storage to the exposed position.

### Action: `auto-action_storage_to_transfer`

- `Vendor2/GPT-5.2`: Retrieve a microplate from the specified storage site and deliver it to the transfer station.
- `Vendor2/GPT-5.3-codex`: Move a microplate from storage to the transfer station.
- `Vendor2/GPT-5.4`: Move a microplate from storage to the transfer station
- `gpt-5.4-mini`: Move a plate from storage to the transfer station.

### Action: `auto-action_storage_to_wait`

- `Vendor2/GPT-5.2`: Retrieve a microplate from the specified storage site and move it to the wait position.
- `Vendor2/GPT-5.3-codex`: Move a microplate from storage to the wait position.
- `Vendor2/GPT-5.4`: Move a microplate from storage to the wait position
- `gpt-5.4-mini`: Move a plate from storage to the wait position.

### Action: `auto-action_transfer_to_storage`

- `Vendor2/GPT-5.2`: Pick a microplate from the transfer station and place it into the specified storage site.
- `Vendor2/GPT-5.3-codex`: Move a microplate from the transfer station into storage.
- `Vendor2/GPT-5.4`: Move a microplate from the transfer station into storage
- `gpt-5.4-mini`: Move a plate from the transfer station back into storage.

### Action: `auto-action_transfer_to_wait`

- `Vendor2/GPT-5.2`: Pick a microplate from the transfer station and return it to the wait position.
- `Vendor2/GPT-5.3-codex`: Move a microplate from the transfer station to the wait position.
- `Vendor2/GPT-5.4`: Move a microplate from the transfer station to the wait position
- `gpt-5.4-mini`: Move a plate from the transfer station back to the wait position.

### Action: `auto-action_wait_to_exposed`

- `Vendor2/GPT-5.2`: Move a microplate from the wait position to an exposed position outside the instrument.
- `Vendor2/GPT-5.3-codex`: Move a microplate from the wait position to the exposed external position.
- `Vendor2/GPT-5.4`: Move a microplate from the wait position to the exposed external position
- `gpt-5.4-mini`: Move a plate from the wait position to the exposed position.

### Action: `auto-action_wait_to_storage`

- `Vendor2/GPT-5.2`: Move a microplate from the wait position back into the specified storage site and unload it.
- `Vendor2/GPT-5.3-codex`: Move a microplate from the wait position into storage.
- `Vendor2/GPT-5.4`: Move a microplate from the wait position back to storage
- `gpt-5.4-mini`: Move a plate from the wait position into storage.

### Action: `auto-action_wait_to_transfer`

- `Vendor2/GPT-5.2`: Move a microplate from the wait position to the transfer station for external pickup/placement.
- `Vendor2/GPT-5.3-codex`: Move a microplate from the wait position to the transfer station.
- `Vendor2/GPT-5.4`: Move a microplate from the wait position to the transfer station
- `gpt-5.4-mini`: Move a plate from the wait position to the transfer station.

### Action: `auto-close_door`

- `Vendor2/GPT-5.2`: Close the instrument door/transfer-port door.
- `Vendor2/GPT-5.3-codex`: Close the device door.
- `Vendor2/GPT-5.4`: Close the device door
- `gpt-5.4-mini`: Close the incubator door.

### Action: `auto-fetch_plate_to_loading_tray`

- `Vendor2/GPT-5.2`: Fetch the specified microplate and place it onto the loading tray/loading position.
- `Vendor2/GPT-5.3-codex`: Fetch a specified microplate to the loading tray.
- `Vendor2/GPT-5.4`: Fetch a specified microplate to the loading tray
- `gpt-5.4-mini`: Fetch a plate onto the loading tray.

### Action: `auto-init_shakers`

- `Vendor2/GPT-5.2`: Initialize the instrument’s internal shaker modules.
- `Vendor2/GPT-5.3-codex`: Initialize the shaker modules.
- `Vendor2/GPT-5.4`: Initialize the shaker modules
- `gpt-5.4-mini`: Initialize the shaker units.

### Action: `auto-initialize`

- `Vendor2/GPT-5.2`: Initialize the instrument mechanics and internal state.
- `Vendor2/GPT-5.3-codex`: Run device initialization.
- `Vendor2/GPT-5.4`: Initialize the device mechanisms
- `gpt-5.4-mini`: Initialize the incubator system.

### Action: `auto-open_door`

- `Vendor2/GPT-5.2`: Open the instrument door/transfer-port door.
- `Vendor2/GPT-5.3-codex`: Open the device door.
- `Vendor2/GPT-5.4`: Open the device door
- `gpt-5.4-mini`: Open the incubator door.

### Action: `auto-reset_error_register`

- `Vendor2/GPT-5.2`: Clear/reset the instrument error register.
- `Vendor2/GPT-5.3-codex`: Reset the error register.
- `Vendor2/GPT-5.4`: Reset the error register
- `gpt-5.4-mini`: Reset the error register.

### Action: `auto-send_action`

- `Vendor2/GPT-5.2`: Send an action command to the instrument and wait for completion.
- `Vendor2/GPT-5.3-codex`: Send an action command and wait for device execution.
- `Vendor2/GPT-5.4`: Send an action command to the device
- `gpt-5.4-mini`: Send an action command and wait for completion.

### Action: `auto-send_command`

- `Vendor2/GPT-5.2`: Send a low-level command to the instrument.
- `Vendor2/GPT-5.3-codex`: Send a command to the device controller.
- `Vendor2/GPT-5.4`: Send a low-level command to the device
- `gpt-5.4-mini`: Send a low-level command to the controller.

### Action: `auto-serialize`

- `Vendor2/GPT-5.2`: Export/record the instrument’s current configuration or state information.
- `Vendor2/GPT-5.3-codex`: Export current device configuration and state information.
- `Vendor2/GPT-5.4`: Serialize device configuration or state information
- `gpt-5.4-mini`: Serialize the current device configuration or state.

### Action: `auto-set_racks`

- `Vendor2/GPT-5.2`: Define/set the internal rack or storage layout.
- `Vendor2/GPT-5.3-codex`: Define the internal rack configuration.
- `Vendor2/GPT-5.4`: Define the rack configuration
- `gpt-5.4-mini`: Define the internal rack layout.

### Action: `auto-set_shaking_frequency`

- `Vendor2/GPT-5.2`: Set the shaker frequency.
- `Vendor2/GPT-5.3-codex`: Set the shaking frequency.
- `Vendor2/GPT-5.4`: Set the shaking frequency
- `gpt-5.4-mini`: Set the shaking frequency.

### Action: `auto-set_temperature`

- `Vendor2/GPT-5.2`: Set the temperature setpoint.
- `Vendor2/GPT-5.3-codex`: Set the temperature setpoint.
- `Vendor2/GPT-5.4`: Set the incubation temperature
- `gpt-5.4-mini`: Set the incubation temperature.

### Action: `auto-setup`

- `Vendor2/GPT-5.2`: Set up the instrument to reach a ready state (basic startup/communication preparation).
- `Vendor2/GPT-5.3-codex`: Perform device setup after power-up.
- `Vendor2/GPT-5.4`: Prepare the device for operation
- `gpt-5.4-mini`: Prepare the incubator for operation.

### Action: `auto-shovel_in`

- `Vendor2/GPT-5.2`: Retract the plate shuttle/pusher mechanism (move it into the instrument).
- `Vendor2/GPT-5.3-codex`: Shovel a tray/plate into the device interior.
- `Vendor2/GPT-5.4`: Retract the loading mechanism into the device
- `gpt-5.4-mini`: Shovel a plate into the incubator.

### Action: `auto-shovel_out`

- `Vendor2/GPT-5.2`: Extend the plate shuttle/pusher mechanism (move it toward the external access position).
- `Vendor2/GPT-5.3-codex`: Shovel a tray/plate out of the device.
- `Vendor2/GPT-5.4`: Extend the loading mechanism out of the device
- `gpt-5.4-mini`: Shovel a plate out of the incubator.

### Action: `auto-start_shaking`

- `Vendor2/GPT-5.2`: Start shaking operation (at the specified frequency).
- `Vendor2/GPT-5.3-codex`: Start shaking incubation.
- `Vendor2/GPT-5.4`: Start shaking incubation
- `gpt-5.4-mini`: Start shaking.

### Action: `auto-stop`

- `Vendor2/GPT-5.2`: Stop the instrument's current task/operation.
- `Vendor2/GPT-5.3-codex`: Stop current device operation.
- `Vendor2/GPT-5.4`: Stop device operation
- `gpt-5.4-mini`: Stop the device.

### Action: `auto-stop_shaking`

- `Vendor2/GPT-5.2`: Stop shaking operation.
- `Vendor2/GPT-5.3-codex`: Stop shaking.
- `Vendor2/GPT-5.4`: Stop shaking
- `gpt-5.4-mini`: Stop shaking.

### Action: `auto-take_in_plate`

- `Vendor2/GPT-5.2`: Take a microplate into the instrument and place it into the specified storage site.
- `Vendor2/GPT-5.3-codex`: Take a microplate into the device and place it at a specified site.
- `Vendor2/GPT-5.4`: Take a microplate into the device and place it in a specified storage site
- `gpt-5.4-mini`: Take in a plate from outside the device.

### Action: `auto-wait_for_task_completion`

- `Vendor2/GPT-5.2`: Wait for the instrument to finish the current task (until it is no longer busy).
- `Vendor2/GPT-5.3-codex`: Wait for the current task to complete.
- `Vendor2/GPT-5.4`: Wait for the current task to complete
- `gpt-5.4-mini`: Wait for the current task to complete.

### Action: `auto-wait_for_transfer_station`

- `Vendor2/GPT-5.2`: Wait until the transfer station becomes occupied or unoccupied.
- `Vendor2/GPT-5.3-codex`: Wait for the transfer station to become occupied or unoccupied.
- `Vendor2/GPT-5.4`: Wait for the transfer station to become occupied or unoccupied
- `gpt-5.4-mini`: Wait for the transfer station to become occupied or unoccupied.

### Action: `auto-get_overview_register`

- `Vendor2/GPT-5.2`: Get the instrument overview status register.
- `Vendor2/GPT-5.3-codex`: Get overview register status.
- `Vendor2/GPT-5.4`: Get overview register state
- `gpt-5.4-mini`: Get the overview register state.

### Action: `auto-get_warning_register`

- `Vendor2/GPT-5.2`: Get the instrument warning register.
- `Vendor2/GPT-5.3-codex`: Get warning register status.
- `Vendor2/GPT-5.4`: Get warning register state
- `gpt-5.4-mini`: Get the warning register state.

### Action: `auto-get_error_register`

- `Vendor2/GPT-5.2`: Get the instrument error register.
- `Vendor2/GPT-5.3-codex`: Get error register status.
- `Vendor2/GPT-5.4`: Get error register state
- `gpt-5.4-mini`: Get the error register state.

### Action: `auto-get_action_register`

- `Vendor2/GPT-5.2`: Get the instrument action status register.
- `Vendor2/GPT-5.3-codex`: Get action register status.
- `Vendor2/GPT-5.4`: Get action register state
- `gpt-5.4-mini`: Get the action register state.

### Action: `auto-get_swap_register`

- `Vendor2/GPT-5.2`: Get the instrument swap/transfer-related status register.
- `Vendor2/GPT-5.3-codex`: Get swap register status.
- `Vendor2/GPT-5.4`: Get swap register state
- `gpt-5.4-mini`: Get the swap register state.

### Action: `auto-get_sensor_register`

- `Vendor2/GPT-5.2`: Get the instrument sensor status register.
- `Vendor2/GPT-5.3-codex`: Get sensor register status.
- `Vendor2/GPT-5.4`: Get sensor register state
- `gpt-5.4-mini`: Get the sensor register state.

### Action: `auto-get_incubation_query`

- `Vendor2/GPT-5.2`: Get the value/status for an incubation-related query item.
- `Vendor2/GPT-5.3-codex`: Get incubation query results.
- `Vendor2/GPT-5.4`: Get incubation environment query value
- `gpt-5.4-mini`: Get the specified incubation query status.

### Action: `auto-get_co2`

- `Vendor2/GPT-5.2`: Get the CO₂ concentration reading.
- `Vendor2/GPT-5.3-codex`: Get CO2 level.
- `Vendor2/GPT-5.4`: Get CO2 concentration
- `gpt-5.4-mini`: Get the CO2 level.

### Action: `auto-get_humidity`

- `Vendor2/GPT-5.2`: Get the humidity reading.
- `Vendor2/GPT-5.3-codex`: Get humidity.
- `Vendor2/GPT-5.4`: Get humidity
- `gpt-5.4-mini`: Get the humidity.

### Action: `auto-get_o2`

- `Vendor2/GPT-5.2`: Get the O₂ concentration reading.
- `Vendor2/GPT-5.3-codex`: Get O2 level.
- `Vendor2/GPT-5.4`: Get O2 concentration
- `gpt-5.4-mini`: Get the O2 level.

### Action: `auto-get_temperature`

- `Vendor2/GPT-5.2`: Get the temperature reading.
- `Vendor2/GPT-5.3-codex`: Get temperature.
- `Vendor2/GPT-5.4`: Get temperature
- `gpt-5.4-mini`: Get the temperature.

### Tags

- `Vendor2/GPT-5.2`: 器件/细胞设备, 物流/机械, 生命体系, 细胞生物学研究, 移液站产品, 组织培养试验箱, 自动化耗材堆栈, 自动化培养箱式微孔板存储系统
- `Vendor2/GPT-5.3-codex`: 器件/细胞设备, 物流/机械, 生命体系, 细胞生物学研究, 组织培养试验箱, 自动化耗材堆栈, 恒温摇床, 自动化微孔板培养存储系统
- `Vendor2/GPT-5.4`: 器件/细胞设备, 物流/机械, 生命体系, 细胞生物学研究, 组织培养试验箱, 高通量筛选, 自动微孔板培养箱
- `gpt-5.4-mini`: 器件/细胞设备, 物流/机械, 生命体系, 细胞生物学研究, 组织培养试验箱, 细胞培养自动化, 自动化培养箱

