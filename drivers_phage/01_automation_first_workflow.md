Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Automation-First Workflow

This file is the authoritative function source for the rest of the phage-driver staging work. The original draft protocol is preserved in `draft_inputs/_phage_protocol_draft_original.md`, but the execution model below intentionally rewrites vessel choices and step groupings so the workflow maps onto automation-friendly plate/deep-well modules.

## Design assumptions introduced here

- Convert most tube-only manipulations into 96-well plate, deep-well plate, or robotic tube-rack operations wherever assay integrity is preserved.
- Keep the cell-binding and staining stages plate-centric until the final transfer into a sorter-compatible carrier.
- Replace the draft `25 cm^2` culture flask amplification step with deep-well plate or automation-compatible culture block amplification unless yield studies later prove the flask is mandatory.
- Treat the FACS sorter, colony picker, plasmid-prep instrument, sequencer, and protein-analysis instruments as modular downstream stations, not as part of one monolithic workstation.

## Stage A: Positive/negative cell and phage library preprocessing

1. Load positive and negative cell suspensions into automation-compatible tubes or deep-well wells.
2. Use a liquid handler to add PBS, resuspend, and normalize working volumes.
3. Centrifuge in a robot-loadable centrifuge; remove supernatant.
4. Add blocking solution and resuspend with repeatable mix cycles instead of manual pipette agitation.
5. Hold cells in a chilled incubator or plate incubator at `4 C`; maintain gas control only where living-cell viability requires it.
6. In parallel, dilute the phage library with blocking solution on the liquid handler and incubate it in the same chilled, automation-controlled environment.
7. After incubation, centrifuge washed cells again, remove supernatant, and resuspend in BSA/PBS working buffer.

## Stage B: Negative selection against off-target cells

1. Use the liquid handler to combine blocked phage library with the negative-cell suspension.
2. Normalize the mixture into a microplate or deep-well format that the incubator and centrifuge can both accept.
3. Incubate at chilled temperature with scheduled shaking or agitation pulses to prevent settling.
4. Centrifuge and recover only the clarified supernatant that contains the negatively depleted phage pool.
5. Discard pellet material and record transfer provenance.

## Stage C: Positive selection against target cells

1. Add the depleted phage pool to the prepared positive-cell suspension using the liquid handler.
2. Incubate in plate/deep-well format under chilled conditions with periodic shaking.
3. Perform repeated wash cycles:
   - centrifuge
   - remove supernatant
   - add PBS
   - resuspend
4. After the final wash, resuspend the bound-cell pellet in sorter-compatible buffer.
5. Transfer the final bound-cell suspension into FACS-compatible tubes or a plate-loader format.

## Stage D: Fluorescent staining

1. Add fluorescent anti-phage antibody with the liquid handler.
2. Mix gently and incubate under chilled, light-protected conditions.
3. Wash away excess antibody by centrifugation and buffer replacement.
4. Resuspend in final sorter buffer and log the final cell concentration and carrier positions.

## Stage E: Flow analysis and sorting

1. Use a sorter-capable flow cytometer to gate the cell population on FSC/SSC and the PE signal.
2. Select the top `1% to 5%` binding population.
3. Sort into chilled recovery tubes or a chilled collection plate.
4. Export sort counts, gate metadata, and event files for traceability.

## Stage F: Phage recovery, infection, and amplification

1. Transfer sorted cells to a recovery rack or microcentrifuge-compatible robot position.
2. Centrifuge and remove supernatant.
3. Add acidic elution buffer, resuspend, and incubate for the defined elution window.
4. Clarify and transfer eluate.
5. Add neutralization buffer on the liquid handler.
6. Combine eluate with log-phase `F+` host cells.
7. Hold the infection mix under low-temperature conditions for attachment, then shift to `37 C` culture conditions.
8. Amplify in deep-well plates or automation-compatible culture blocks with controlled shaking.
9. Clarify harvested culture by centrifugation.
10. Sterile-filter supernatant through a `0.22 um` membrane device or automation-compatible filter module.
11. Measure titer externally or through a later assay step to decide whether the enrichment loop repeats.

## Stage G: Single-clone isolation and screening

1. Plate dilution series on agar using either automated plating support or a liquid-handler plus plate-transfer workflow.
2. Incubate plates until discrete colonies appear.
3. Use an automated colony picker to image, rank, and pick candidate monoclonal colonies into `96`-well growth plates.
4. Expand clones in plate format.
5. Split aliquots for clone re-screening:
   - flow-based rebinding assay if cell-format confirmation remains necessary
   - ELISA or plate-reader assay for plate-compatible confirmation
6. Select the strongest clones for downstream plasmid preparation and sequencing.

## Stage H: Sequence confirmation, expression, purification, and binding validation

1. Run automated plasmid extraction on selected clones.
2. Sequence the inserts with an automated sequencer or sequencing station.
3. Move verified sequences into expression-vector construction and host-transformation workflows.
4. Express target protein in an automation-compatible culture format when possible.
5. Purify the target protein on an automated chromatography system with affinity capture.
6. Measure affinity and specificity on a dedicated binding-analysis instrument.
7. Release only clones meeting both affinity and specificity thresholds.

## Manual-to-automation gaps intentionally surfaced

- The draft protocol mixes `15 mL` tubes, `1.5 mL` tubes, `96`-well plates, and a `25 cm^2` flask. The automation-first version collapses most of this into plate/deep-well-friendly formats.
- The protocol assumes a FACS sorter, colony picker, plasmid-prep device, sequencer, protein purifier, and SPR analyzer exist as downstream stations. Those remain the main driver gaps.
- Automated `0.22 um` sterile filtration is not covered by the current local driver pool and remains an explicit missing station.
