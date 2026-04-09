Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Evidence Summary

## Device selected

Cytiva ÄKTA pure 25.

## Why this model won

- Cytiva positions ÄKTA pure as its flexible research-oriented automated purification system.
- Public documentation is strong: product family page, product documentation, and operating instructions are all available.
- The system is a clean fit for Ni-NTA / affinity bind-wash-elute workflows in research settings.

## Required functions vs capability

| Required function | Evidence |
|---|---|
| Bind / wash / elute affinity purification | Cytiva’s purification-system page positions ÄKTA pure for routine research purification and method flexibility. |
| Fraction collection | ÄKTA pure ecosystem includes fraction collectors and product docs for the pure 25 configuration. |
| Method programming | Operating instructions and Cytiva content emphasize automated purification methods and unattended workflows. |
| Run metadata / processed outputs | Standard chromatography outputs include chromatograms, fractions, detector traces, and method states. |

## Interfaces / automation notes

- Public materials show external equipment linkage via I/O box in Cytiva application/news content.
- Cytiva’s main public story is instrument software and chromatography workflow control rather than a public SDK/API.

## Outputs returned by the device

- Chromatograms and detector traces.
- Fraction collection outputs.
- Method/run metadata suitable for downstream purification review.

## Footprint / integration constraints

- Public product documentation lists dimensions for ÄKTA pure 25 components, including main-system dimensions around `390 x 585 x 320 mm` for F9-C and `320 x 400 x 250 mm` for F9-R modules, depending configuration.
- Integration depends on detector, mixer, fraction collector, and column configuration choices.

## Files found

- Official protein purification systems page
- Official ÄKTA pure product documentation PDF
- Official operating instructions PDF
- Cytiva unattended-purification and external-equipment integration articles

## Pricing notes

- No public list price found.

## Risks / unknowns

- Exact automation hooks beyond Cytiva software and optional I/O integration are not clearly public.
- Workcell integration will vary substantially with configuration and fraction-collector selection.
