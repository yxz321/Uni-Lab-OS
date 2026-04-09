Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

Target device type: Agilent BioTek 406 FX class plate washer / dispenser

Required phage-workflow functions:

- wash bound-cell plates after incubation
- wash ELISA plates
- bulk dispense PBS, blocking buffer, antibody, or wash buffer
- fit robotic plate workflows used around local `sealer`, `peeler`, and liquid handlers

Bundle / protocol context:

- Bundle 4: sealing, unsealing, plate washing, bulk dispensing
- used after positive-selection washes, fluorescent staining clean-up, and ELISA validation

Task:

1. Use explicit web search only.
2. Confirm whether `Agilent BioTek 406 FX` is the best current choice for this workflow and clearly note any backward compatibility with the older EL406 line.
3. Find the best specific model for this workflow.
4. Write:
   - `Uni-Lab-OS/drivers_phage/agilent_biotek_406_fx/evidence.md`
   - `Uni-Lab-OS/drivers_phage/agilent_biotek_406_fx/sources.json`

Focus especially on:

- wash-cycle programming
- dispense manifold options
- plate formats
- automation interfaces / software hooks
- outputs or logs available to automation
- physical footprint and robotic access constraints
