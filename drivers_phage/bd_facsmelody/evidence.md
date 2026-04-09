Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Evidence Summary

## Device selected

BD FACSMelody Cell Sorter.

## Why this model won

- It is explicitly marketed as an automated 4-way cell sorter rather than only an analyzer.
- BD positions it as simple, automation-oriented, and suitable for users who need walk-away sorting rather than only expert-operated high-end custom sorting.
- The official brochure exposes the exact workflow areas the phage protocol needs: automated stream setup, steering into tubes or plates, continuous QC monitoring, and reduced hands-on time.

## Required functions vs capability

| Required function | Evidence |
|---|---|
| FSC/SSC + fluorescence gating | FACSMelody is a full cell sorter with multicolor workflow support in the official brochure and landing page. |
| Sort top `1% to 5%` binders | Official brochure emphasizes automated stream setup and walk-away sorting. |
| Collect into tubes or plates | Brochure explicitly says steering into tubes or plates is automated. |
| Record sort counts / export results | Standard sorter workflow implies FCS/result export; BD materials emphasize software-driven workflow and QC tracking, though file-format details were not public in the pages reviewed. |

## Interfaces / automation notes

- BD emphasizes user-friendly software, automated workflow, continuous QC monitoring, and optional index plate sorting in comparison materials.
- Publicly reviewed sources did not expose a formal open SDK/API; the available evidence suggests appliance-style instrument software rather than public low-level control docs.

## Outputs returned by the device

- Sorted cells into tubes or plates.
- Standard flow-cytometry run outputs such as event data, gating results, and QC/sort metadata are implied by the instrument class, though BD’s public landing materials do not spell out the exact file formats in detail.

## Footprint / integration constraints

- Public BD materials surfaced rich feature information but not an easily accessible official dimensions sheet in the rapid pass.
- A site-preparation guide or official spec sheet should be requested during procurement.

## Files found

- Official BD landing page
- Official BD brochure PDF
- Comparison page showing FACSMelody as an automation-oriented sorter with optional index plate sorting

## Pricing notes

- No public list price found; BD routes the product through demo/quote flows.

## Risks / unknowns

- Public docs are feature-rich but API-light.
- If deeper sort customization or more parameters are required, BD FACSAria III remains a stronger alternative, but FACSMelody is the cleaner automation-first recommendation for this workflow.
