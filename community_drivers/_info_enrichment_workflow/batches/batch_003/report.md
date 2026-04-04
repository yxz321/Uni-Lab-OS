# Batch 003 Report

## Scope
Processed exactly 10 devices from `batch_003` manifest.

## Files changed
- /home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/acq1102/info.txt
- /home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/acq2106/info.txt
- /home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/acq2106__mgtdram8/info.txt
- /home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/acq2106_tiga/info.txt
- /home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/acq400e/info.txt
- /home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/acquisition_stage/info.txt
- /home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/ad_roi_stat/info.txt
- /home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/address_space_builder/info.txt
- /home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/adn_xpt/info.txt
- /home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/ads_symbol/info.txt
- /home/xzye/projects/DPTech/community_drivers/Uni-Lab-OS/community_drivers/_info_enrichment_workflow/batches/batch_003/report.md

## Compatibility drift corrected
- Normalized outputs to `schema_version: v2`.
- Preserved structure compatibility (`device_identity` + `description` first, metadata later).
- Removed `categories` section from final files.
- Kept `driver_functions` in concise `compact_signatures` form.
- Refined device descriptions to avoid backend-style wording and keep device-first readability.

## Sampled descriptions
- `acq1102`: D-TACQ ACQ1102 data-acquisition unit driver for streaming, channel scaling, trigger-state monitoring, and waveform-pattern loading.
- `acq2106`: D-TACQ ACQ2106 host proxy for ACQ400 systems, exposing trigger, clock, and synchronization-routing controls.
- `acq2106__mgtdram8`: D-TACQ ACQ2106 MGTDRAM8 host proxy for ACQ400 systems, focused on MGT DRAM pull-client creation and run control.
- `acq2106_tiga`: D-TACQ ACQ2106 TIGA host proxy for ACQ400 digital-output workflows, including DIO482 pattern loading and DO setting.
- `acq400e`: D-TACQ ACQ400 EPICS-oriented control interface for PV read/write, monitoring, and stream-to-disk operations.

## Sampled action/function summaries
- `acq1102` / `chan2volts`: returns calibrated volts for channel.
- `acq2106` / `auto-set_MR`: Set mr using enable, evsel0, evsel1, MR10DEC.
- `acq2106__mgtdram8` / `auto-create_mgtdram_pull_client`: Execute create mgtdram pull client.
- `acq2106_tiga` / `auto-load_dio482pg`: Execute load dio482pg with site, stl, trace.
- `acq400e` / `auto-caget`: Execute caget with pvname.

## Workflow-level issues before batch_004
- No blocking issues found.
- Non-blocking: run the lightweight structure validator after each batch for automatic drift checks.
