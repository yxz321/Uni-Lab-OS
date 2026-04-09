Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

Target device type: automated sterile filtration / positive-pressure processing workstation

Required phage-workflow functions:

- pass clarified phage supernatant through a `0.22 um` sterile filtration stage
- support automation-friendly plate or multi-sample workflows
- expose enough control/state information for automation logging

Bundle / protocol context:

- Bundle 7: sterile filtration
- used immediately after amplification culture clarification and before downstream titer / screening loop decisions

Task:

1. Use explicit web search only.
2. Verify whether `Tecan Resolvex A200` is the strongest recommendation for this use case.
3. Write:
   - `Uni-Lab-OS/drivers_phage/tecan_resolvex_a200/evidence.md`
   - `Uni-Lab-OS/drivers_phage/tecan_resolvex_a200/sources.json`

Focus especially on:

- positive-pressure vs vacuum operation
- plate / filter consumable compatibility
- automation interface details
- endpoint detection or pressure logging
- footprint / robotic loading constraints
