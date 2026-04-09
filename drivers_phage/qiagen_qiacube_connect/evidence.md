Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Evidence Summary

## Device selected

QIAGEN QIAcube Connect.

## Why this model won

- Official resource coverage is excellent: product page, user manual, protocol files, software release notes, and technical information are all public.
- QIAcube Connect is clearly positioned as the current QIAGEN automation platform beyond the older QIAcube Classic.
- It matches the phage workflow need for low-to-moderate throughput clone preparation better than high-throughput batch systems.

## Required functions vs capability

| Required function | Evidence |
|---|---|
| Automated plasmid-prep style chemistry | Product page and promotional material describe fully automated spin-column sample preparation and broad protocol support. |
| Minimal-manual clone processing | QIAcube Connect automates protocol execution and accepts standardized protocol files. |
| Return run status and reports | QIAsphere/QIAcube resources describe generated report files with sample count, measured liquid volumes, and run time. |

## Interfaces / automation notes

- Public documents show protocol-file loading, USB transfer, QIAsphere connectivity, cloud/app notifications, and downloadable standard/custom protocols.
- This is a strong software-managed instrument, but a vendor-public low-level API was not surfaced.

## Outputs returned by the device

- Sample eluates ready for downstream sequencing.
- Run reports containing sample count, measured liquid volumes during load check, and run time.
- Instrument/protocol state through QIAsphere connectivity.

## Footprint / integration constraints

- Official specifications list dimensions (hood closed) as `65 x 58 x 62 cm`.
- Operating temperature `18 to 28 C`; indoor use only.
- Requires QIAGEN kits/protocol ecosystem, so consumable lock-in is a real integration factor.

## Files found

- Official product/resource page
- Official user manual
- Official technical information PDF
- QIAsphere / web resource with operational and notification details
- Promotional workflow PDF

## Pricing notes

- No public list price found.

## Risks / unknowns

- Strong protocol and cloud features are public, but open automation APIs are not.
- Kit dependence narrows reagent flexibility.
