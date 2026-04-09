Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Evidence Summary

## Device selected

Telesis Bio BioXp 3250 system.

## Why this model won

- It is explicitly marketed as an automated synthetic biology workstation for building gene fragments, clones, and libraries.
- Telesis Bio provides a product page, fact sheet, specification sheet, and full user guide publicly.
- The system’s automation scope aligns more closely with construct assembly than a generic liquid handler does.

## Required functions vs capability

| Required function | Evidence |
|---|---|
| Assemble verified sequences into constructs | Product docs say the system builds gene fragments, clones, and libraries. |
| Track construct-building workflows | Instrument uses defined application protocols and user-guide workflow. |
| Reduce manual cloning setup | Product docs position it as hands-free / automated synthetic biology workstation. |

## Interfaces / automation notes

- Public docs show a self-contained instrument with onboard workflow rather than a public API-first device.
- Site-preparation material says the system requires power and internet connectivity.
- No public SDK/REST/serial command model was surfaced.

## Outputs returned by the device

- DNA fragments, clones, variant libraries, and mRNA depending application.
- Per-run yields, runtime, and protocol-defined construct outputs.

## Footprint / integration constraints

- Official specification sheet gives dimensions `69 x 77 x 53 cm` and weight `63.4 kg`.
- Format is `96`-well plate based, with up to `32` fragments or clones per run.
- Assembly runtimes are `6 to 21` hours depending application.

## Files found

- Official product page
- Official fact sheet
- Official specification sheet
- Official user guide
- Product pages for DNA cloning/gene synthesis workflows

## Pricing notes

- No public list price found, but Telesis Bio public financial statements describe the BioXp 3250 as the lower-priced instrument relative to BioXp 9600.

## Risks / unknowns

- Public materials emphasize assay/application throughput rather than external instrument-control hooks.
- Host-cell transformation is not clearly presented as a full end-to-end automated biological transformation step; downstream wet-lab handoff may still be needed.
