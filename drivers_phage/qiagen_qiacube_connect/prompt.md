Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

Target device type: automated plasmid extraction station

Required phage-workflow functions:

- automate lysis / binding / wash / elution style plasmid-prep steps
- process clone-confirmation samples with minimal manual intervention
- return run status and sample-ready eluates to downstream sequencing

Bundle / protocol context:

- Bundle 10: plasmid extraction and DNA sequencing
- used after clone re-screening and before sequence confirmation

Task:

1. Use explicit web search only.
2. Verify whether `QIAcube Connect` is still the best recommendation for plasmid-prep automation in this context.
3. Write:
   - `Uni-Lab-OS/drivers_phage/qiagen_qiacube_connect/evidence.md`
   - `Uni-Lab-OS/drivers_phage/qiagen_qiacube_connect/sources.json`

Focus especially on:

- supported plasmid protocols
- throughput
- consumables / kit dependence
- connectivity and automation interfaces
- output files, logs, and physical footprint
