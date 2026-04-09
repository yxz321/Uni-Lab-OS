Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Evidence Summary

## Device selected

Molecular Devices QPix 420 within the QPix 400 Series microbial colony pickers.

## Why this model won

- Official materials directly target microbial colony imaging, selection, picking, and sample tracking.
- Public documentation confirms throughput, phenotype-based selection, sterility features, and a complete audit trail.
- Molecular Devices also publishes pre-installation guidance with physical dimensions, which helps workcell planning.

## Required functions vs capability

| Required function | Evidence |
|---|---|
| Image agar plates | Product page/brochure describes colony imaging and phenotype selection. |
| Rank/select candidate colonies | Product materials explicitly list fluorescence, blue/white, size, proximity, and zone-of-inhibition selection modes. |
| Pick colonies into destination plates | Brochure states automated colony picking and transfer into downstream workflows. |
| Maintain identity / tracking | Product page says data is automatically recorded into the machine database for audit trail and sample tracking. |

## Interfaces / automation notes

- Software-guided workflow setup is a core public feature.
- Customer-facing application notes show QPix systems in robotic workcells with plate hotels, incubators, liquid handlers, centrifuges, sealers, and readers.
- A public open API was not surfaced, but the integration story is stronger than for many competing systems because Molecular Devices explicitly shows robot-linked workcells.

## Outputs returned by the device

- Colony images and selection metrics.
- Pick lists / audit trail / sample-tracking database outputs.
- Destination culture plates or picked-colony transfers.

## Footprint / integration constraints

- Pre-install guide and QPix XE comparison note that QPix 420 dimensions are roughly `57 x 29.5 x 30.7 in` and height/depth around `78 cm` / `79 cm`, with much larger width for the full system depending on holder/stacker configuration.
- Instrument receiving and clearance requirements are nontrivial and should be planned early.

## Files found

- Official product page for QPix 400 series
- Official brochure PDF
- Official sterility application note
- Official pre-installation guide with dimensions
- Official application note comparing QPix XE vs QPix 420 and showing robotic-workcell integration

## Pricing notes

- No public price found. Molecular Devices notes price and lead time vary with technical requirements.

## Risks / unknowns

- Public materials strongly support colony-picking automation, but low-level software control interfaces are not public.
- The QPix XE is smaller and cheaper, but the QPix 420 remains the stronger throughput-oriented recommendation for this workflow.
