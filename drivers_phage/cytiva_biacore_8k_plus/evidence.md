Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Evidence Summary

## Device selected

Cytiva Biacore 8K+.

## Why this model won

- Cytiva publicly positions Biacore 8K+ as a high-capacity SPR system for screening, characterization, process optimization, and quality control.
- Public documentation includes the SPR systems page, launch article, operating instructions, and selection-guide specifications.
- The platform is built for high-throughput affinity/specificity work rather than only single-assay kinetics.

## Required functions vs capability

| Required function | Evidence |
|---|---|
| Measure binding affinity | SPR systems page and selection guide position Biacore 8K/8K+ for affinity/kinetics work. |
| Compare specificity panels | Launch article highlights thousands of binding experiments in a single run and high-throughput screening/characterization. |
| Export kinetics / response outputs | Cytiva evaluation/software content emphasizes screening and characterization data evaluation from Biacore systems. |

## Interfaces / automation notes

- Public evidence points to Cytiva’s dedicated Biacore software stack rather than an open public API.
- Biacore 8K+ supports high plate capacity and long unattended run times, which is useful for automated specificity panels.

## Outputs returned by the device

- Sensorgrams and derived affinity / kinetics / specificity outputs.
- Screening and characterization datasets through Biacore software.

## Footprint / integration constraints

- Official operating-instructions/specification content gives dimensions for the Biacore 8K/8K+ family around `902 x 875 x 616 mm` and weights around `128 kg` for 8K and `141 kg` for 8K+.
- Sample capacity in the selection guide is up to `12 x 96- or 384-well` plates for Biacore 8K+ with long unattended runs.

## Files found

- Official SPR systems page
- Official launch / news article for Biacore 8K+
- Official operating instructions
- Official selection-guide/specification content
- Biacore software/evaluation news item

## Pricing notes

- No public price found.

## Risks / unknowns

- Public documentation is very strong on assay capability, but public low-level automation APIs were not surfaced.
- This is a large specialized station with significant footprint and assay-development overhead compared with simpler plate assays.
