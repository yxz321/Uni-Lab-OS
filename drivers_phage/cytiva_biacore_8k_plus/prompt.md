Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

Target device type: SPR affinity and specificity analyzer

Required phage-workflow functions:

- measure binding affinity for purified phage-derived proteins
- compare specificity against negative / cross-reactive protein panels
- export kinetics / response outputs usable by the automation system

Bundle / protocol context:

- Bundle 12: protein expression, purification, and affinity/specificity validation
- used after purification of verified binders

Task:

1. Use explicit web search only.
2. Verify whether `Biacore 8K+` is the best high-throughput recommendation for this workflow.
3. Write:
   - `Uni-Lab-OS/drivers_phage/cytiva_biacore_8k_plus/evidence.md`
   - `Uni-Lab-OS/drivers_phage/cytiva_biacore_8k_plus/sources.json`

Focus especially on:

- sensorgram outputs and kinetics exports
- assay programming / injection cycles
- software / API or automation hooks
- chip / fluidics constraints
- footprint and integration requirements
