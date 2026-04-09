Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Phage Protocol Device Update

## 1. Concise Summary Table

| Bundle | Suggested device | Availability class | Alternatives | Required actions | Follow-up needed |
|---|---|---:|---|---|---|
| Sample preparation and liquid handling | `vantage_backend` | (a) | `star_backend`, `li_ha`, `liquid_handler.prcxi` | `pick_up_tips`, `aspirate`, `dispense`, `mix`, `move_plate` | No |
| Incubation, cooling, and shaking | `cytomat_backend` | (a) | `incubator_shaker_stack`, `bio_shake`, `incubator` | `set_temperature`, `fetch_plate`, `shake`, storage/hotel actions | No |
| Centrifugation | `centrifuge` | (a) | `v_spin_backend`, `access2_backend` | `load`, `spin`, `unload`, door interlocks | No |
| Sealing, unsealing, plate washing, bulk dispensing | `Agilent BioTek 406 FX` | (b) | `sealer`, `peeler`, `vantage_backend` | `seal`, `peel`, `wash_plate`, `bulk_dispense` | Deep search + guessed driver |
| Fluorescent staining and flow cytometry | `BD FACSMelody` | (c) | `BD FACSAria III`, `Sony SH800S` | `set_gate`, `sort_cells`, `record_sort_count`, `export_fcs` | Deep search + guessed driver |
| Phage recovery: acid elution, infection, amplification | `vantage_backend` + `cytomat_backend` | (a) | `star_backend`, `bio_shake` | `dispense`, `mix`, chilled hold, `shake`, warm incubation | No |
| Sterile filtration (`0.22 um`) | `Tecan Resolvex A200` | (c) | manual sterile filtration, `virtual_filter` | `filter`, pressure profile control, endpoint handling | Deep search + guessed driver |
| Colony picking and monoclonal screening | `Molecular Devices QPix 420` | (c) | manual picking, `molecular_devices_backend` for readout | `image_plate`, `select_colony`, `pick_colony`, `inoculate_clone` | Deep search + guessed driver |
| ELISA plate reading | `molecular_devices_backend` | (a) | `bio_tek_plate_reader_backend`, `clari_ostar_backend`, `plate_reader` | `read_absorbance`, `read_fluorescence`, tray control | No |
| Plasmid extraction and DNA sequencing | `QIAcube Connect` + `SeqStudio Genetic Analyzer` | (c) | Biomek DNA purification, external Sanger | `extract_plasmid`, `run_sequence`, `export_sequence` | Deep search + guessed drivers |
| Vector construction and transformation | `BioXp 3250` | (c) | `vantage_backend` + manual cloning/transformation | `assemble_vector`, `track_construct`, `transform_cells` | Deep search + guessed driver |
| Protein expression, purification, affinity/specificity validation | `ÄKTA pure` + `Biacore 8K+` | (c) | manual chromatography, outsourced affinity testing | `load_sample`, `wash_column`, `elute_fraction`, `measure_binding`, `compare_binding` | Deep search + guessed drivers |
| Automation support | `vantage_backend` | (a) | `star_backend`, `cytomat_backend`, CSV-only robot arms | plate transfer, consumables, hotel handoff | No |

## 2. Protocol Overview

The protocol should be executed as an automation-first station chain rather than as a literal replay of the draft tube/flask layout:

1. Preprocess positive and negative cells plus the phage library on the liquid handler, then shift into chilled plate/deep-well incubation.
2. Run negative and positive selections in plate-compatible carriers so incubator, shaker, and centrifuge handoffs stay robotic.
3. Perform fluorescent staining on the liquid handler; only move into a sorter-compatible carrier at the final staging step.
4. Sort the highest-binding cell fraction on a dedicated FACS station and recover the sorted material into chilled collection carriers.
5. Elute, neutralize, infect, and amplify using the existing liquid-handler and incubator stack; rewrite the flask amplification step into deep-well or automation-friendly culture blocks where possible.
6. Sterile-filter recovered phage through a dedicated filtration station before deciding whether another enrichment loop is required.
7. Plate for clone isolation, pick monoclonal colonies automatically, and rescreen them with local plate-reader support and, when needed, the same FACS station.
8. Extract plasmids, sequence inserts, assemble expression constructs, purify the protein product, and validate affinity/specificity on dedicated downstream stations that are currently missing locally.

## 3. Per-Bundle Analysis

### Bundle 1: Sample preparation and liquid handling

`vantage_backend` wins because it combines deep pipetting support with integrated gripper operations in a locally validated driver. `star_backend` and `li_ha` remain credible alternatives, but Vantage gives the cleanest single backbone for both fluid work and deck logistics.

### Bundle 2: Incubation, cooling, and shaking

`cytomat_backend` is the strongest local fit because its metadata explicitly includes temperature, `CO2`, humidity, `O2`, shaking, barcode, and storage/exposed-position moves. That is a closer match to the chilled cell-binding stages than a simple thermoshaker. `incubator_shaker_stack` and `bio_shake` remain useful alternates for stripped-down plate incubation.

### Bundle 3: Centrifugation

The generic `centrifuge` driver is better suited than the plate-only VSpin variants because the phage workflow still contains mixed carriers even after the automation-first rewrite. Its action surface explicitly supports `g`-based timed spins, load/unload, and door safety operations.

### Bundle 4: Sealing, unsealing, plate washing, bulk dispensing

Local coverage is asymmetric: `sealer` and `peeler` are present, but a real plate washer is not. That is why the bundle recommendation shifts to `Agilent BioTek 406 FX` as the best unavailable upgrade, while keeping the local sealer/peeler and liquid handler as fallback pieces.

### Bundle 5: Fluorescent staining and flow cytometry

Only the reagent-addition part is locally covered. Real gating, sorting, and event export are absent, so the bundle needs a dedicated sorter. `BD FACSMelody` was chosen as the web-backed recommendation because it squarely covers the missing sorting workflow and is backed by strong vendor documentation.

### Bundle 6: Phage recovery, infection, amplification

No new station is required here if we accept an automation-first vessel rewrite. `vantage_backend` handles the liquid chemistry, and `cytomat_backend` handles the incubation and shaking side. This bundle is therefore available, but only as a deliberate multi-device workflow rather than as a single magic instrument.

### Bundle 7: Sterile filtration

The local inventory only exposes a virtual filter, so physical sterile filtration remains a real gap. `Tecan Resolvex A200` is the recommended unavailable station because it is purpose-built for automated positive-pressure processing and is easier to integrate into robotic plate/deep-well workflows than manual syringe filtering.

### Bundle 8: Colony picking and monoclonal screening

Automated colony picking is missing. `Molecular Devices QPix 420` closes that gap directly by handling colony imaging, selection, transfer, and tracking. Local plate readers still help with downstream screening, but they do not solve the picking bottleneck.

### Bundle 9: ELISA plate reading

This is one of the healthier local areas. `molecular_devices_backend` gives the best readout coverage and also exposes temperature/shaking functions that make it more versatile for follow-up clone assays. The main ELISA weakness sits upstream at plate washing, not at detection.

### Bundle 10: Plasmid extraction and DNA sequencing

The repo only partially hints at plasmid purification through protocol-capable liquid handlers, and it has no sequencer driver. The best clean split is `QIAcube Connect` for automated extraction and `SeqStudio Genetic Analyzer` for clone confirmation.

### Bundle 11: Vector construction and transformation

No local construct-assembly station exists. `BioXp 3250` is the best unavailable candidate because it directly targets automated construct generation and cloning-class workflows rather than acting as a generic liquid handler.

### Bundle 12: Protein expression, purification, and affinity/specificity validation

Local incubation hardware can support expression culture in an automation-friendly format, but the purification and binding-validation instruments are missing. The clean downstream pair is `ÄKTA pure` for purification and `Biacore 8K+` for SPR-based affinity/specificity validation.

### Bundle 13: Automation support

The workflow does not need to lead with a standalone robot arm because `vantage_backend` already provides strong integrated transport capabilities. `cytomat_backend` fills the hotel/storage side, and that combination is sufficient for the current staging plan.

## 4. Unavailable Devices Summary

The following unavailable devices need deep search folders and guessed drivers:

- `agilent_biotek_406_fx`
- `bd_facsmelody`
- `tecan_resolvex_a200`
- `molecular_devices_qpix_420`
- `qiagen_qiacube_connect`
- `applied_biosystems_seqstudio_genetic_analyzer`
- `telesis_bio_bioxp_3250`
- `cytiva_akta_pure`
- `cytiva_biacore_8k_plus`
