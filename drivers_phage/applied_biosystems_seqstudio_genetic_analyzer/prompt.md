Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

Target device type: benchtop clone-confirmation DNA sequencer

Required phage-workflow functions:

- run sequence confirmation on selected plasmid clones
- expose run status and export sequence results suitable for automation handoff

Bundle / protocol context:

- Bundle 10: plasmid extraction and DNA sequencing
- used after automated plasmid prep of top phage-derived clones

Task:

1. Use explicit web search only.
2. Verify whether `Applied Biosystems SeqStudio Genetic Analyzer` is the best low-throughput recommendation or whether another currently sold model is better.
3. Write:
   - `Uni-Lab-OS/drivers_phage/applied_biosystems_seqstudio_genetic_analyzer/evidence.md`
   - `Uni-Lab-OS/drivers_phage/applied_biosystems_seqstudio_genetic_analyzer/sources.json`

Focus especially on:

- sequencing modality and output files
- run monitoring and data export
- instrument software / connectivity
- cartridge / consumable constraints
- dimensions and operator touchpoints relevant to automation
