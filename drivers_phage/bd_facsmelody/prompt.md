Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

Target device type: automated fluorescence-activated cell sorter

Required phage-workflow functions:

- gate target cells using FSC/SSC and PE fluorescence
- sort the top `1% to 5%` binding population
- collect sorted cells into chilled tubes or plates
- report sort counts and export event / result files to automation

Bundle / protocol context:

- Bundle 5: fluorescent staining and flow cytometry
- used after antibody staining of target-bound cells and before phage recovery

Task:

1. Use explicit web search only.
2. Verify whether `BD FACSMelody` is the best practical recommendation or whether another sorter with stronger automation evidence should replace it.
3. Write:
   - `Uni-Lab-OS/drivers_phage/bd_facsmelody/evidence.md`
   - `Uni-Lab-OS/drivers_phage/bd_facsmelody/sources.json`

Focus especially on:

- gating/sorting workflow support
- output files and run metadata
- instrument control / automation interfaces
- consumables and chilled collection options
- physical integration constraints
