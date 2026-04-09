Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

Target device type: automated protein purification system

Required phage-workflow functions:

- bind / wash / elute affinity purification of expressed protein
- fraction collection
- method programming suitable for Ni-NTA or similar affinity workflows
- expose run metadata and processed outputs to automation

Bundle / protocol context:

- Bundle 12: protein expression, purification, and affinity/specificity validation
- used after expression culture harvest and before binding validation

Task:

1. Use explicit web search only.
2. Verify whether `ÄKTA pure` is the best current recommendation for this phage workflow.
3. Write:
   - `Uni-Lab-OS/drivers_phage/cytiva_akta_pure/evidence.md`
   - `Uni-Lab-OS/drivers_phage/cytiva_akta_pure/sources.json`

Focus especially on:

- affinity chromatography workflow fit
- inline detectors and outputs
- fraction collector support
- software / automation interfaces
- physical footprint and lab integration constraints
