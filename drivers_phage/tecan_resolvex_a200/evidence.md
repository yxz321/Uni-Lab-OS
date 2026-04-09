Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Evidence Summary

## Device selected

Tecan Resolvex A200 Automated Positive Pressure Processor.

## Why this model won

- It is one of the clearest automation-first products in the sterile-filtration / pressure-processing class with strong official documentation.
- Official materials confirm programmable pressure profiles and support for either 1 mL columns or 96-well plates, which fits an automation-first reformat of the phage recovery stage.
- Tecan provides both a brochure and an operating manual publicly.

## Required functions vs capability

| Required function | Evidence |
|---|---|
| Automated membrane/plate filtration workflow | Brochure confirms automated positive-pressure processing. |
| Automation-friendly multi-sample format | Brochure states support for 1 mL columns or 96-well (1 mL) plates. |
| Controlled pressure program | Brochure and manual both mention programmable pressure profiles. |
| Logged method execution | Manual confirms instrument-method operation, though public summaries do not expose detailed exported file formats. |

## Interfaces / automation notes

- Primary public interface evidence is the onboard touch-screen and method programming.
- Tecan’s public pages emphasize workflow automation and reproducibility, but a public open API/SDK was not surfaced in this pass.

## Outputs returned by the device

- Processed filtered samples.
- Method completion/status information and instrument state rather than analytical data files.

## Footprint / integration constraints

- Benchtop instrument according to official brochure.
- Public search results did not expose a simple spec page with external dimensions in the snippet set reviewed; those likely live inside the full manual.
- Integration still depends on carrier and filter-consumable choices.

## Files found

- Official brochure page
- Official operating-manual landing page
- Direct PDF operating manual
- Application page around reproducible automated sample processing

## Pricing notes

- No public price found in the rapid pass.

## Risks / unknowns

- The product is optimized around SPE/positive-pressure sample prep, so compatibility with the exact sterile `0.22 um` consumable stack for phage supernatant must be confirmed during selection.
- Public-facing API details are limited.
