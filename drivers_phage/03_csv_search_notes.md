Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# CSV Search Notes

Method:

- Searched both `community_drivers/_aggregate_device_info_existing.csv` and `community_drivers/_aggregate_device_info_output.csv`.
- Used semantic keywords against `name`, `name_en`, `registry_key`, `description_en`, `categories`, `tags`, and `atom_actions`.
- Merged hits mentally by `registry_key`; neither CSV was treated as authoritative over the other.
- The 20-row calibration sample from `_aggregate_device_info_existing.csv` showed action names at roughly the level of `aspirate`, `dispense`, `mix`, `move_plate`, `set_temperature`, `spin`, `seal`, `read_absorbance`.

## 1. Sample preparation and liquid handling

Search terms: `pipet`, `liquid handling`, `transfer`, `mix`, `aspirate`, `dispense`, `plate handling`

Top hits from `_aggregate_device_info_existing.csv`:

- `liquid_handler` with `aspirate`, `dispense`, `mix`, `transfer`, `move_plate`
- `liquid_handler.prcxi` with pipetting plus `auto-heater_action`, `auto-shaker_action`
- `liquid_handler.laiyu` with `aspirate`, `dispense`, `mix`, `pick_up_tips`
- `liquid_handler.biomek` as a protocol-oriented liquid handler

Top hits from `_aggregate_device_info_output.csv`:

- `li_ha` with strong score on `aspirate`, `dispense`, tip handling, plate movement
- `star_backend` with aspiration, dispensing, gripper-based plate moves, CoRe 96 support
- `vantage_backend` with aspiration, dispensing, CoRe96 operations, gripper handling
- `hamilton_tcp_backend` as a lower-level Hamilton transport/control layer

Conclusion:

- Bundle is well covered locally.
- The best automation-ready matches are the Hamilton/Tecan workstations in the output CSV, especially `vantage_backend`, `star_backend`, and `li_ha`.

## 2. Incubation, cooling, and shaking

Search terms: `incubator`, `shaker`, `cooling`, `temperature`, `thermoshaker`, `cytomat`, `orbitor`

Top hits from `_aggregate_device_info_existing.csv`:

- `hotel.thermo_orbitor_rs2_hotel`
- `liquid_handler.prcxi` because its action set references integrated heater/shaker behavior
- `chiller`

Top hits from `_aggregate_device_info_output.csv`:

- `cytomat_backend`
- `heraeus_cytomat_backend`
- `incubator_shaker_stack`
- `inheco_incubator_shaker_stack_backend`
- `inheco_incubator_shaker_unit`
- `bio_shake`
- `bioshake_driver`
- `hamilton_heater_shaker_backend`

Conclusion:

- Plate-format incubation and shaking are strongly covered.
- `cytomat_backend` is the strongest cell-oriented incubator/storage candidate because the CSV description explicitly mentions temperature, `CO2`, humidity, `O2`, shaking, and barcode support.
- `incubator_shaker_stack` and `bio_shake` are strong alternatives for simpler plate/deep-well agitation without the full storage/hotel feature set.

## 3. Centrifugation

Search terms: `centrifuge`, `spin`, `bucket`, `g-force`

Top hits from `_aggregate_device_info_existing.csv`:

- `virtual_centrifuge`
- generic workflow-level `workstation` references

Top hits from `_aggregate_device_info_output.csv`:

- `centrifuge`
- `v_spin_backend`
- `access2_backend`

Conclusion:

- Physical centrifuge coverage exists in the output CSV and is stronger than the legacy CSV sample.
- `centrifuge` is the best generic fit for tube/deep-well phage workflow steps; `v_spin_backend` and `access2_backend` look more microplate-specialized.

## 4. Sealing, unsealing, plate washing, bulk dispensing

Search terms: `sealer`, `peeler`, `washer`, `wash_plate`, `bulk dispense`, `dispenser`

Top hits from `_aggregate_device_info_existing.csv`:

- no convincing washer hits
- only incidental liquid-handler and solid-dispenser matches

Top hits from `_aggregate_device_info_output.csv`:

- `sealer`
- `peeler`
- `vantage_backend` as an alternative route for bulk dispense
- no credible dedicated plate washer in the local inventory search pass

Conclusion:

- Sealing and de-sealing are locally covered.
- Plate washing is the missing local function.
- Bulk dispensing can be done by a liquid handler, but a dedicated washer/dispenser would materially improve ELISA and wash-heavy steps.

## 5. Fluorescent staining and flow cytometry

Search terms: `facs`, `flow cytometer`, `sorter`, `cytometry`, `fluorescent stain`

Top hits from `_aggregate_device_info_existing.csv`:

- no genuine FACS/flow cytometer hits

Top hits from `_aggregate_device_info_output.csv`:

- no genuine FACS/flow cytometer hits
- plate-reader and imaging systems appeared as false positives when searching on `fluorescence`

Conclusion:

- The repo has no available driver for a real flow cytometer or sorter.
- Only the reagent-addition part of the staining workflow is locally covered via liquid handlers.

## 6. Phage recovery: acid elution, infection, amplification

Search terms: `phage`, `elution`, `infection`, `amplification`, `culture`, `incubator`, `shaker`

Top hits from `_aggregate_device_info_existing.csv`:

- only weak incidental matches

Top hits from `_aggregate_device_info_output.csv`:

- `vantage_backend` and `star_backend` remain the strongest liquid-manipulation candidates
- `cytomat_backend`, `incubator_shaker_stack`, `bio_shake` cover incubation/shaking pieces

Conclusion:

- This bundle is best served by combining available liquid handling and incubation devices rather than by introducing a unique standalone recovery instrument.

## 7. Sterile filtration (`0.22 um`)

Search terms: `filter`, `filtration`, `membrane`, `sterile`

Top hits from `_aggregate_device_info_existing.csv`:

- `virtual_filter`

Top hits from `_aggregate_device_info_output.csv`:

- no convincing physical sterile-filtration station
- several optical filter or unrelated hits were discarded as false positives

Conclusion:

- Physical `0.22 um` sterile filtration is effectively missing from the local driver pool.

## 8. Colony picking and monoclonal screening

Search terms: `colony`, `picker`, `clone`, `monoclonal`, `screening`

Top hits from `_aggregate_device_info_existing.csv`:

- none

Top hits from `_aggregate_device_info_output.csv`:

- no real colony picker
- plate readers and generic robotic arms surfaced as weak/indirect matches only

Conclusion:

- Automated colony picking is missing locally.
- Downstream monoclonal screening can reuse plate readers or the FACS station, but the actual colony-picker station is absent.

## 9. ELISA plate reading

Search terms: `elisa`, `plate reader`, `absorbance`, `fluorescence`, `luminescence`

Top hits from `_aggregate_device_info_existing.csv`:

- no strong reader-specific matches beyond generic noise

Top hits from `_aggregate_device_info_output.csv`:

- `molecular_devices_backend`
- `bio_tek_plate_reader_backend`
- `clari_ostar_backend`
- `plate_reader`
- `byonoy_absorbance96_automate_backend`
- `cytation_backend`

Conclusion:

- Readout itself is strongly covered.
- The main missing piece for end-to-end ELISA automation is plate washing, not the reader.

## 10. Plasmid extraction and DNA sequencing

Search terms: `plasmid`, `dna extraction`, `sequencing`, `sequencer`

Top hits from `_aggregate_device_info_existing.csv`:

- none

Top hits from `_aggregate_device_info_output.csv`:

- no dedicated plasmid-prep or sequencing station
- some unrelated `sequencer` false positives from control electronics

Conclusion:

- This bundle is not adequately covered by current local drivers.
- The only partial local signal is that some liquid handlers can host DNA-purification protocols, but there is no dedicated extraction instrument or sequencer driver in the CSV union.

## 11. Vector construction and transformation

Search terms: `vector construction`, `cloning`, `transformation`, `transfection`

Top hits from both CSVs:

- no convincing dedicated construct-design or transformation station
- liquid handlers can assist manually designed workflows but do not solve the bundle as a finished station

Conclusion:

- No good available device in the CSV union.

## 12. Protein expression, purification, and affinity/specificity validation

Search terms: `protein purification`, `affinity`, `spr`, `biacore`, `chromatography`, `expression`

Top hits from `_aggregate_device_info_output.csv`:

- weak chromatography-adjacent hits such as `mx_valve`
- no dedicated AKTA/Biacore style station

Conclusion:

- Protein purification and SPR-style affinity validation are not truly covered by the available device union.

## 13. Automation support

Search terms: `robot arm`, `gripper`, `agv`, `hotel`, `plate mover`, `storage`, `warehouse`

Top hits from `_aggregate_device_info_existing.csv`:

- `robotic_arm.UR`
- `robotic_arm.elite`
- `robotic_arm.SCARA_with_slider.moveit.virtual`
- `agv.SEER`
- `hotel.thermo_orbitor_rs2_hotel`

Top hits from `_aggregate_device_info_output.csv`:

- `experimental_scara`
- `li_ha`
- `star_backend`
- `cytomat_backend`
- several robotic-arm and AGV entries

Conclusion:

- Local automation support is broad enough for plate transport, hotel-style storage, and consumable handling.
- The integrated gripper moves already exposed by `vantage_backend` and `star_backend` reduce the need to lead with a standalone robot arm for this phage workflow.
