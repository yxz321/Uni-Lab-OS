# Device Availability Assessment

> Auto-generated 2026-04-08. Compares a target device list against drivers in
> `community_drivers/` (prefix **community/**) and `unilabos/devices/` (prefix **unilab/**).

## Legend

| Symbol | Meaning |
|--------|---------|
| :white_check_mark: | Full or near-full driver exists |
| :large_orange_diamond: | Partial — related drivers cover some functions |
| :x: | Not present — no driver in either codebase |

---

## Summary Table

| # | Target Device | Status | Best Existing Match(es) |
|---|--------------|--------|------------------------|
| 1 | Fully Automated Incubator | :white_check_mark: | community/incubator, community/cytomat_backend, community/heraeus_cytomat_backend |
| 2 | Fully Automated Shaking Incubator | :white_check_mark: | community/incubator_shaker_stack, community/inheco_incubator_shaker_stack_backend, community/inheco_incubator_shaker_unit |
| 3 | Centrifuge | :white_check_mark: | community/centrifuge, community/access2_backend, community/v_spin_backend, unilab/virtual/virtual_centrifuge |
| 4 | 0.22 um Membrane Filtration Device | :x: | (none) |
| 5 | Full Automated Liquid Handler | :white_check_mark: | community/li_ha, community/hamilton_tcp_backend, unilab/liquid_handling/ (Biomek, LaiYu, PRCXI) |
| 6 | Flow Cytometer (FACS) | :x: | (none) |
| 7 | Fully Automated Monoclonal Colony Picker | :x: | (none) |
| 8 | Fully Automated Flow Cytometer (Analysis) | :x: | (none) |
| 9 | Fully Automated ELISA Plate Reader | :large_orange_diamond: | community/byonoy_absorbance96_automate_backend, community/plate_reader, community/molecular_devices_backend, community/clari_ostar_backend, community/bio_tek_plate_reader_backend, community/cytation_backend |
| 10 | Fully Automated Plasmid Extraction System | :large_orange_diamond: | unilab/liquid_handling/biomek (DNA_purification protocol) |
| 11 | DNA Sequencer | :x: | (none) |
| 12 | Fully Automated Protein Purification System | :large_orange_diamond: | unilab/virtual/virtual_column, unilab/hplc/AgilentHPLC, unilab/zhida_hplc/, community/mx_valve |
| 13 | Biacore Affinity Analyzer | :x: | (none) |
| 14 | Expression Vector Construction System | :x: | (none) |

---

## Detailed Analysis

### 1. Fully Automated Incubator :white_check_mark:

**Existing drivers:**

| Driver | Source | Description |
|--------|--------|-------------|
| incubator | community/ | Generic automated microplate incubator (pylabrobot-based) |
| cytomat_backend | community/ | Thermo Cytomat — automated microplate incubator with robotic door/shuttle, CO2/O2/temp/humidity |
| heraeus_cytomat_backend | community/ | Thermo Heraeus Cytomat — door control, shaking, temperature setpoint |
| incubator_stx | community/ | STX automated microplate incubator |
| opentrons_temperature_module_usb_backend | community/ | Opentrons temperature module (simpler, no CO2) |

**Coverage:** Full. Multiple vendors, full temp/gas control.

---

### 2. Fully Automated Shaking Incubator :white_check_mark:

**Existing drivers:**

| Driver | Source | Description |
|--------|--------|-------------|
| incubator_shaker_stack | community/ | INHECO incubator/shaker stack |
| inheco_incubator_shaker_stack_backend | community/ | INHECO backend — combined incubation + shaking |
| inheco_incubator_shaker_unit | community/ | INHECO single incubator-shaker unit |
| inheco_thermoshake_backend | community/ | INHECO Thermoshake AC heater-shaker |
| bio_shake | community/ | BioShake microplate heater-shaker |
| bioshake_driver | community/ | BioShake thermoshaker driver |
| hamilton_heater_shaker_backend | community/ | Hamilton heater-shaker |

**Coverage:** Full. INHECO stack provides combined incubation + shaking in one unit.

---

### 3. Centrifuge :white_check_mark:

**Existing drivers:**

| Driver | Source | Description |
|--------|--------|-------------|
| centrifuge | community/ | Generic laboratory centrifuge |
| access2_backend | community/ | Agilent VSpin microplate centrifuge (automation-ready) |
| v_spin_backend | community/ | Agilent VSpin centrifuge backend |
| VirtualCentrifuge | unilab/virtual/ | Virtual centrifuge (100-15000 rpm, temp 4-40 C) |

**Coverage:** Full. Both physical (Agilent VSpin) and virtual implementations.

---

### 4. 0.22 um Membrane Filtration Device :x:

**Existing drivers:** None.

**Partially related:**

| Driver | Source | What it covers |
|--------|--------|---------------|
| VirtualFilter | unilab/virtual/ | Virtual filtration simulation (temp, stir speed, volume) — no physical device |
| pump | community/ | Syringe pump — could drive fluid through a filter |
| next_gen_pump | community/ | Next-gen syringe pump |
| masterflex_backend | community/ | Peristaltic pump — could provide filtration pressure |

**Still missing:**
- Dedicated 0.22 um membrane filtration controller (vacuum or pressure)
- Filter integrity testing (bubble point test)
- Filter cassette/holder positioning and clamping
- Filtrate volume monitoring and endpoint detection
- Sterile filtration protocol management

---

### 5. Full Automated Liquid Handler :white_check_mark:

**Existing drivers:**

| Driver | Source | Description |
|--------|--------|-------------|
| li_ha | community/ | Tecan Freedom EVO LiHa arm |
| hamilton_tcp_backend | community/ | Hamilton STAR/Vantage liquid handler |
| liquid_classes | community/ | Tecan liquid class definitions |
| LiquidHandlerBiomek | unilab/liquid_handling/ | Beckman Biomek (pipetting, incubation, DNA purification) |
| PRCXI9300Handler | unilab/liquid_handling/ | PRCXI 9300 liquid handler |
| TransformXYZHandler | unilab/liquid_handling/ | LaiYu XYZ liquid handler with pipette control |
| LiquidHandlerAbstract | unilab/liquid_handling/ | Abstract base (pylabrobot-compatible) |
| BioyondDispensingStation | unilab/workstation/ | Bioyond dispensing station |

**Coverage:** Full. Multiple vendors (Hamilton, Tecan, Beckman, LaiYu, PRCXI).

---

### 6. Flow Cytometer (FACS) :x:

**Existing drivers:** None.

**Partially related:**

| Driver | Source | What it covers |
|--------|--------|---------------|
| cytation_backend | community/ | BioTek Cytation — fluorescence detection + cell imaging (plate-based, not flow) |

**Still missing:**
- Flow cell control and fluidics (sheath fluid, sample injection)
- Laser excitation and multi-channel fluorescence detection
- Cell sorting (droplet deflection, collection tubes)
- Real-time scatter/fluorescence gating
- Sort purity and yield optimization
- FCS file export

---

### 7. Fully Automated Monoclonal Colony Picker :x:

**Existing drivers:** None.

**Still missing:**
- Colony imaging and recognition (plate camera + image analysis)
- XY(Z) picking head with sterile pin/tip
- Source plate scanning and colony identification
- Destination plate dispensing
- Picking protocol (agar → liquid media transfer)
- Colony counting and selection criteria

---

### 8. Fully Automated Flow Cytometer (Analysis) :x:

Same gap as #6 (FACS), minus the sorting subsystem:

**Still missing:**
- Flow cell and fluidics control
- Multi-laser excitation
- Multi-channel fluorescence + scatter detection
- Gating and compensation
- FCS data acquisition and export

---

### 9. Fully Automated ELISA Plate Reader :large_orange_diamond:

**Existing drivers (plate readers):**

| Driver | Source | Description |
|--------|--------|-------------|
| byonoy_absorbance96_automate_backend | community/ | 96-well absorbance reader, explicitly ELISA-suitable, automation-ready |
| plate_reader | community/ | Generic plate reader (absorbance, fluorescence, luminescence) |
| molecular_devices_backend | community/ | Molecular Devices multimode reader (absorbance, fluorescence, luminescence, TRF, FP) |
| clari_ostar_backend | community/ | BMG CLARIOstar multimode reader |
| bio_tek_plate_reader_backend | community/ | Agilent BioTek multimode reader |
| cytation_backend | community/ | BioTek Cytation (reader + cell imaging) |
| NivoDriver | unilab/platereader/ | PerkinElmer Nivo plate reader |

**What is covered:** Absorbance readout (the detection step of ELISA).

**Still missing for "fully automated ELISA":**
- Automated plate washing (wash/aspirate cycles) — no plate washer driver
- Reagent dispensing / liquid handling integration for ELISA protocol
- Incubation step orchestration
- End-to-end ELISA workflow controller

---

### 10. Fully Automated Plasmid Extraction System :large_orange_diamond:

**Existing drivers:**

| Driver | Source | What it covers |
|--------|--------|---------------|
| LiquidHandlerBiomek | unilab/liquid_handling/ | DNA_purification protocol type within Biomek |

**What is covered:** DNA purification as a protocol on the Biomek liquid handler.

**Still missing for dedicated system:**
- Magnetic bead handling (magnet engage/disengage)
- Lysis, binding, wash, elution step automation
- Dedicated plasmid extraction instrument driver (e.g., Qiagen QIAcube, Promega Maxwell, KingFisher)
- Eluate quality check (UV absorbance A260/A280)

---

### 11. DNA Sequencer :x:

**Existing drivers:** None.

**Still missing:**
- Sequencer instrument control (Illumina MiSeq/NextSeq, ONT MinION, PacBio, Sanger capillary)
- Library preparation integration
- Run monitoring and basecalling
- FASTQ/BAM output management

---

### 12. Fully Automated Protein Purification System :large_orange_diamond:

**Existing drivers:**

| Driver | Source | What it covers |
|--------|--------|---------------|
| VirtualColumn | unilab/virtual/ | Virtual column chromatography (solvent ratios, Rf, flow rate) |
| AgilentHPLC | unilab/hplc/ | Agilent HPLC via UI automation (pump, injector, detector, VWD) |
| zhida.py | unilab/zhida_hplc/ | Zhida HPLC system |
| mx_valve | community/ | Rheodyne MXII multiport valve (column/buffer switching) |

**What is covered:** HPLC chromatography (closely related), multiport valve switching, virtual column simulation.

**Still missing for dedicated protein purification (e.g., AKTA):**
- Multi-buffer gradient mixing (A/B/C lines)
- UV/conductivity/pH inline monitors
- Fraction collector integration
- Method programming (bind → wash → elute → regenerate)
- Dedicated FPLC instrument driver (AKTA pure/avant/go)

---

### 13. Biacore Affinity Analyzer :x:

**Existing drivers:** None.

**Still missing:**
- SPR (Surface Plasmon Resonance) sensor chip control
- Microfluidic flow cell and buffer delivery
- Real-time binding kinetics (ka, kd, KD) measurement
- Ligand immobilization and analyte injection cycles
- Sensorgram data acquisition and export

---

### 14. Expression Vector Construction System :x:

**Existing drivers:** None.

This is primarily a **software/bioinformatics** system rather than a hardware device:

**Still missing:**
- Restriction enzyme site analysis
- Gibson Assembly / Golden Gate design
- Primer design for cloning
- In-silico sequence verification
- Integration with DNA synthesis ordering
- Transformation protocol management (links to liquid handler + incubator)

---

## Gap Summary

| Category | Count |
|----------|-------|
| Fully covered | 5 (Incubator, Shaking Incubator, Centrifuge, Liquid Handler, Plate Reader readout) |
| Partially covered | 3 (ELISA workflow, Plasmid Extraction, Protein Purification) |
| Not covered at all | 6 (Membrane Filtration, FACS, Colony Picker, DNA Sequencer, Biacore, Vector Construction) |
