Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Evidence Summary

## Device selected

Applied Biosystems SeqStudio Genetic Analyzer.

## Why this model won

- It is a currently sold benchtop instrument explicitly positioned for plasmid Sanger sequencing and related clone-confirmation tasks.
- Thermo Fisher exposes a product page, specification sheet, user guide, getting-started guide, and remote-monitoring documentation.
- Compared with larger Flex instruments, SeqStudio is a better scale match for the phage protocol’s `3 to 5` top-clone confirmation stage.

## Required functions vs capability

| Required function | Evidence |
|---|---|
| Run clone-confirmation sequencing | Product page explicitly names plasmid Sanger sequencing among supported applications. |
| Export sequence results | SeqStudio is a standard capillary-sequencing platform with instrument/software guide and application guides; sequence output export is core to the platform. |
| Remote run status | Thermo Fisher provides a SeqStudio Remote Monitoring App through its cloud platform. |

## Interfaces / automation notes

- Onboard software and instrument-resident data collection are public.
- Thermo Fisher Cloud remote monitoring is publicly documented.
- Optional security/audit features are called out on the product page.
- No public low-level API/SDK was surfaced in the rapid pass.

## Outputs returned by the device

- Sanger sequencing traces and associated run data.
- Remote monitoring status through Thermo Fisher Cloud.
- Audit/security features for data integrity.

## Footprint / integration constraints

- Official spec sheet lists dimensions as `49.5 x 64.8 x 44.2 cm`.
- Cartridge-based consumables simplify operation but create consumable dependence.

## Files found

- Official product page
- Official spec sheet PDF
- Official user guide PDF
- Official getting-started guide PDF
- Official remote monitoring help pages

## Pricing notes

- No public list price found in the reviewed materials.

## Risks / unknowns

- Public materials focus on software usability, cloud monitoring, and assays, not on open external control.
- If throughput requirements increase substantially, the SeqStudio Flex series may become the better target.
