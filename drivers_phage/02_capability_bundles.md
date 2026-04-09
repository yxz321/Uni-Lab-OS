Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Capability Bundles

The function names below are intentionally normalized toward the `atom_actions` granularity observed in the CSV sample, e.g. `aspirate`, `dispense`, `mix`, `set_temperature`, `spin`, `seal`, `read_absorbance`.

## Tier-0 Bundle Index

1. Sample preparation and liquid handling
2. Incubation, cooling, and shaking
3. Centrifugation
4. Sealing, unsealing, plate washing, bulk dispensing
5. Fluorescent staining and flow cytometry
6. Phage recovery: acid elution, infection, amplification
7. Sterile filtration (`0.22 um` membrane)
8. Colony picking and monoclonal screening
9. ELISA plate reading
10. Plasmid extraction and DNA sequencing
11. Vector construction and transformation
12. Protein expression, purification, and affinity/specificity validation
13. Automation support: robot arms, plate transfer, storage, consumable handling

## 1. Sample preparation and liquid handling

| Function row | Needed action granularity |
|---|---|
| Cell/phage liquid transfer | `pick_up_tips`, `aspirate`, `dispense` |
| Resuspension and blocking mix | `mix` |
| Vessel reformatting | `transfer`, `transfer_liquid` |
| Plate/tube repositioning inside the liquid handler deck | `move_plate`, `pick_up_resource`, `drop_resource` |

## 2. Incubation, cooling, and shaking

| Function row | Needed action granularity |
|---|---|
| Chilled incubation | `set_temperature`, `get_temperature` |
| Gas-aware plate hold for cells | `set_temperature`, `close_door`, `open_door` |
| Scheduled agitation during binding | `start_shaking`, `stop_shaking`, `shake` |
| Plate storage / recall | `fetch_plate_to_loading_tray`, `take_in_plate`, barcode/readback where available |

## 3. Centrifugation

| Function row | Needed action granularity |
|---|---|
| Load sample carrier | `load`, `open_door`, `close_door` |
| Controlled spin | `spin`, `start_spin_cycle` |
| Supernatant recovery workflow | `unload`, indexed bucket positioning |
| Safety / interlock state | `door_open`, `lock_door`, `unlock_door` |

## 4. Sealing, unsealing, plate washing, bulk dispensing

| Function row | Needed action granularity |
|---|---|
| Seal plate | `seal`, `set_temperature` |
| Peel plate | `peel` |
| Wash cell or ELISA plate | `wash_plate` or equivalent aspirate/dispense wash cycle |
| Bulk add PBS / antibody / wash buffer | `bulk_dispense`, plate-wide `dispense` |

## 5. Fluorescent staining and flow cytometry

| Function row | Needed action granularity |
|---|---|
| Add staining reagent | `aspirate`, `dispense`, `mix` |
| Gate target population | `set_gate`, `analyze_events` |
| Sort enriched fraction | `sort_cells`, `collect_sorted_fraction` |
| Export sort results | `record_sort_count`, `export_fcs` |

## 6. Phage recovery: acid elution, infection, amplification

| Function row | Needed action granularity |
|---|---|
| Acid elution | `dispense`, `mix`, timed hold |
| Neutralization | `dispense`, `mix` |
| Host infection setup | `transfer_liquid`, `mix`, chilled hold |
| Amplification culture | `set_temperature`, `shake`, `incubate` |

## 7. Sterile filtration (`0.22 um` membrane)

| Function row | Needed action granularity |
|---|---|
| Filter clarified supernatant | `filter`, pressure/vacuum control, endpoint detection |

## 8. Colony picking and monoclonal screening

| Function row | Needed action granularity |
|---|---|
| Colony imaging and ranking | `image_plate`, `select_colony` |
| Pick and inoculate | `pick_colony`, `inoculate_clone` |
| Clone plate setup | `dispense_media`, `transfer_colony` |
| Clone rescreen handoff | `plate_transfer`, assay-specific export |

## 9. ELISA plate reading

| Function row | Needed action granularity |
|---|---|
| Load plate | `open`, `assign_child_resource`, `close` |
| Read ELISA absorbance | `read_absorbance` |
| Optional fluorescent readback | `read_fluorescence` |

## 10. Plasmid extraction and DNA sequencing

| Function row | Needed action granularity |
|---|---|
| Automated plasmid prep | `extract_plasmid`, lysis/wash/elution orchestration |
| Sequence confirmation | `load_capillary_or_cartridge`, `run_sequence`, `export_sequence` |

## 11. Vector construction and transformation

| Function row | Needed action granularity |
|---|---|
| Assemble expression vector | `assemble_vector`, `program_protocol`, `track_construct` |
| Transform host cells | `transform_cells`, `heat_shock` or `electroporate`, recovery hold |

## 12. Protein expression, purification, and affinity/specificity validation

| Function row | Needed action granularity |
|---|---|
| Expression culture induction | `set_temperature`, `shake`, timed induction |
| Affinity purification | `equilibrate_column`, `load_sample`, `wash_column`, `elute_fraction` |
| Affinity measurement | `prime_flow_cell`, `inject_analyte`, `measure_binding`, `export_sensorgram` |
| Specificity comparison | `run_panel`, `compare_binding_responses` |

## 13. Automation support: robot arms, plate transfer, storage, consumable handling

| Function row | Needed action granularity |
|---|---|
| Plate and carrier transport | `pick_up_resource`, `move_picked_up_resource`, `drop_resource` |
| Incubator/hotel storage | `storage_to_exposed`, `exposed_to_storage`, barcode reads |
| Consumable handling | tip pick/drop, plate loading, carrier loading |
| Traceability | barcode, plate identity, state serialization |
