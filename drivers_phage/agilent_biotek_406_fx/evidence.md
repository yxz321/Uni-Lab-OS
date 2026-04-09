Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Evidence Summary

## Device selected

Agilent BioTek 406 FX Washer Dispenser, with EL406 documentation used as predecessor-line support where public 406 FX integration details are sparse.

## Why this model won

- It directly covers the missing local functions: plate washing plus bulk reagent dispensing.
- Agilent announced the 406 FX on June 8, 2023, so it is the better date-grounded recommendation for new procurement than the older EL406.
- Agilent provides unusually strong automation-facing documentation across the EL406/406 FX line, including a VWorks device-driver guide and ELISA automation notes.
- The instrument family is explicitly described as suitable for benchtop or integrated automated systems.

## Required functions vs capability

| Required function | Evidence |
|---|---|
| Wash bound-cell plates | Agilent positions 406 FX as the current washer/dispenser in this line, while predecessor EL406 documentation explicitly shows full-plate washing and Dual-Action gentle cell washing. |
| Wash ELISA plates | Agilent ELISA application note centers on repeated ELISA wash and reagent-addition cycles. |
| Bulk dispense buffers/reagents | Product page and ELISA note both describe up to three reagent dispensers. |
| Fit robotic workflows | VWorks device-driver guide explicitly targets integrators configuring BioTek washers/dispensers in automated systems. |

## Interfaces / automation notes

- Publicly documented software path: Agilent VWorks plus BioTek Liquid Handling Control software.
- The VWorks device guide names the EL406 as a supported device and describes setup for integrators; this remains a useful proxy for 406 FX-class software integration.
- Public sources did not expose a simple open API; the strongest evidence points to software-mediated integration rather than a vendor-advertised REST/SDK model.

## Outputs returned by the device

- Operational outputs are primarily run status, configured wash/dispense methods, and software-level completion/error states.
- This is a process station, not an analytical detector, so the main automation outputs are completion state and method traceability rather than assay data files.

## Footprint / integration constraints

- Compact benchtop format is repeatedly emphasized by Agilent, but the quick official pages surfaced in this pass did not publish full mechanical dimensions.
- For workcell design, the installation/integration guide should be treated as the authoritative source.

## Files found

- Official 406 FX launch page
- Official EL406 product page
- Official datasheet PDF
- VWorks BioTek Liquid Handler Device Driver Guide PDF
- EL406 ELISA automation application note PDF
- 406 FX launch announcement

## Pricing notes

- No public list price found in the rapid official-source pass; Agilent routes this product through quote requests.

## Risks / unknowns

- Public integration documents remain easier to find for EL406 than for 406 FX, so some automation assumptions still rely on predecessor-line documentation.
- Public automation documentation is software-centric; a low-level communications interface was not surfaced in this pass.
- Mechanical dimensions were not clearly exposed on the public product pages reviewed.
