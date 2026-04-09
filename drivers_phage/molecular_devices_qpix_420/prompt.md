Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

Target device type: automated microbial colony picker

Required phage-workflow functions:

- image agar plates
- rank/select candidate colonies
- pick colonies into `96`-well culture plates
- preserve colony identity and sample tracking

Bundle / protocol context:

- Bundle 8: colony picking and monoclonal screening
- used after phage amplification, plating, and clone isolation

Task:

1. Use explicit web search only.
2. Verify whether `Molecular Devices QPix 420` is the best choice within the QPix line or whether another model/vendor is superior.
3. Write:
   - `Uni-Lab-OS/drivers_phage/molecular_devices_qpix_420/evidence.md`
   - `Uni-Lab-OS/drivers_phage/molecular_devices_qpix_420/sources.json`

Focus especially on:

- colony imaging and phenotype selection modes
- picking throughput
- destination plate handling
- tracking / audit trail exports
- sterilization features and integration footprint
