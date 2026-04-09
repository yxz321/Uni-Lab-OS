Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Independent Capability Mapping

Availability classes used here:

- `(a)` available and well-suited
- `(b)` available but outclassed by a better unavailable product
- `(c)` no adequate available device

## Web-validated unavailable short list

The following products were selected using explicit web search because local availability was missing or materially incomplete:

- `Agilent BioTek 406 FX Washer Dispenser` for wash-heavy plate workflows: Agilent’s 2023 launch material positions 406 FX as the newer evolution of the EL406 concept, adding stronger dispensing flexibility while retaining integrated washing. Sources: `https://www.agilent.com/about/newsroom/presrel/2023/08jun-ca23026.html`, `https://www.agilent.com/en/product/cell-analysis/microplate-automation-detection/microplate-washers-dispensers/biotek-el406-washer-dispenser-1623255`
- `BD FACSMelody Cell Sorter` for gated fluorescence sorting: current BD brochure emphasizes simplified automation and cell sorting workflow. Source: `https://go.bd.com/rs/565-YXD-236/images/BD-FACSMelody-Brochure.pdf`
- `Tecan Resolvex A200` for automated positive-pressure filtration/SPE style workflows: official Tecan pages confirm positive-pressure processing, programmable pressure profiles, and up to `96` samples. Sources: `https://www.tecan.com/want-fast-and-reproducible-spe-sample-preparation`, `https://www.tecan.com/a200-brochure`
- `Molecular Devices QPix 400 Series / QPix 420` for colony picking: the product page explicitly covers colony imaging, selection, tracking, and transfer. Source: `https://www.moleculardevices.com/products/clone-screening/microbial-screening/qpix-400-series-microbial-colony-pickers`
- `QIAGEN QIAcube Connect` for automated plasmid extraction-class workflows: official product page confirms lysis/bind/wash/elute automation for up to `12` samples and broad protocol coverage. Source: `https://www.qiagen.com/us/products/discovery-and-translational-research/dna-rna-purification/instruments-equipment/qiacube-connect`
- `Applied Biosystems SeqStudio Genetic Analyzer` for clone-confirmation Sanger sequencing: official product page confirms low-throughput capillary sequencing and remote monitoring. Source: `https://www.thermofisher.com/us/en/home/life-science/sequencing/sanger-sequencing/genetic-analyzers/models/seqstudio.html`
- `Telesis Bio BioXp 3250` for automated construct assembly/cloning workflows: official fact sheet calls it an automated synthetic biology workstation for building DNA clones and libraries. Sources: `https://files.telesisbio.com/docs/45051_v1.4_BioXp%203250%20system_Fact%20sheet%20Effective%2005JAN2023.pdf`, `https://telesisbio.com/products/gene-synthesis/`
- `Cytiva ÄKTA pure` for automated protein purification: Cytiva’s protein-purification-systems page identifies ÄKTA pure as the research-focused automated purification platform. Sources: `https://www.cytivalifesciences.com/solutions/protein-research/products-and-technologies/protein-purification-systems`, `https://www.cytivalifesciences.com/en/us/news-center/unattended-protein-purification-10001`
- `Cytiva Biacore 8K+` for affinity/specificity measurement: Cytiva’s SPR-systems page and Biacore 8K+ launch material confirm high-throughput SPR screening and affinity/kinetics workflows. Sources: `https://www.cytivalifesciences.com/solutions/protein-research/products-and-technologies/spr-systems`, `https://www.cytivalifesciences.com/en/us/news-center/discover-more-with-maximized-capacity-10001`

## Front summary table

| Bundle | Suggested device | Class | Guessed driver needed? | Notes |
|---|---|---:|---|---|
| 1. Sample prep / liquid handling | `vantage_backend` | (a) | No | Strongest locally validated pipetting + integrated gripper |
| 2. Incubation / cooling / shaking | `cytomat_backend` | (a) | No | Best local match for temp + gas + shaking + plate hotel behavior |
| 3. Centrifugation | `centrifuge` | (a) | No | Best local generic centrifuge for mixed phage workflow carriers |
| 4. Seal / unseal / wash / bulk dispense | `Agilent BioTek 406 FX` | (b) | Yes | Local sealing exists, but washing does not |
| 5. Fluorescent staining / FACS | `BD FACSMelody` | (c) | Yes | Sorting/gating is a true local gap |
| 6. Phage recovery / infection / amplification | `vantage_backend` + `cytomat_backend` | (a) | No | Best served by combining already-validated local stations |
| 7. Sterile filtration | `Tecan Resolvex A200` | (c) | Yes | Local physical filtration station absent |
| 8. Colony picking / monoclonal screening | `Molecular Devices QPix 420` | (c) | Yes | Colony picking absent; downstream screening can reuse local readers |
| 9. ELISA plate reading | `molecular_devices_backend` | (a) | No | Strong locally validated multimode reader |
| 10. Plasmid extraction / DNA sequencing | `QIAcube Connect` + `SeqStudio Genetic Analyzer` | (c) | Yes | Extraction and sequencing are both true gaps |
| 11. Vector construction / transformation | `BioXp 3250` | (c) | Yes | Best web-backed automated construct-assembly station |
| 12. Protein expression / purification / validation | `ÄKTA pure` + `Biacore 8K+` | (c) | Yes | Purification and SPR analysis both missing locally |
| 13. Automation support | `vantage_backend` | (a) | No | Integrated gripper already covers most transport needs |

## Per-function capability matrix

| Function name | Bundle group | Class | Suggested device | Alternatives | Notes |
|---|---|---:|---|---|---|
| Cell/phage liquid transfer | 1 | (a) | `vantage_backend` | `star_backend`, `li_ha`, `liquid_handler.prcxi` | Best local combination of pipetting depth and gripper support |
| Resuspension and blocking mix | 1 | (a) | `vantage_backend` | `star_backend`, `li_ha` | Mix cycles can remain on liquid handler |
| Vessel reformatting | 1 | (a) | `vantage_backend` | `star_backend`, `li_ha` | Supports automation-first shift into plate/deep-well carriers |
| Plate/tube repositioning on deck | 1 | (a) | `vantage_backend` | `star_backend`, `li_ha` | Integrated gripper reduces need for a separate transport robot |
| Chilled incubation | 2 | (a) | `cytomat_backend` | `incubator`, `incubator_shaker_stack`, `bio_shake` | Chosen because its description explicitly includes environmental control |
| Gas-aware cell incubation | 2 | (a) | `cytomat_backend` | `heraeus_cytomat_backend`, `incubator` | Best local path for `CO2`-aware plate incubation |
| Scheduled shaking during binding | 2 | (a) | `cytomat_backend` | `incubator_shaker_stack`, `bio_shake` | Alternative is to split storage and shaking stations |
| Plate storage and recall | 2 | (a) | `cytomat_backend` | `incubator`, `hotel.thermo_orbitor_rs2_hotel` | Barcode/storage actions make it the best bundle lead |
| Load sample carrier | 3 | (a) | `centrifuge` | `v_spin_backend`, `access2_backend` | More generic than the plate-only VSpin variants |
| Controlled spin by `g` | 3 | (a) | `centrifuge` | `v_spin_backend` | Local action schema explicitly takes `g` and duration |
| Supernatant recovery handoff | 3 | (a) | `centrifuge` | `access2_backend` | Indexed bucket handling is explicit in the local driver |
| Door / interlock control | 3 | (a) | `centrifuge` | `v_spin_backend` | Explicit local open/close/lock/unlock actions |
| Seal plate | 4 | (a) | `sealer` | `a4_s_backend` | Already available locally |
| Peel plate | 4 | (a) | `peeler` | none local of similar quality | Already available locally |
| Wash cell or ELISA plate | 4 | (c) | `Agilent BioTek 406 FX` | `vantage_backend` plus manual wash logic | Local inventory has no credible dedicated washer |
| Bulk add PBS / antibody / wash buffer | 4 | (b) | `Agilent BioTek 406 FX` | `vantage_backend`, `star_backend`, `li_ha` | Local liquid handlers can do it, but a washer/dispenser is materially better for repetitive plate operations |
| Add fluorescent antibody stain | 5 | (a) | `vantage_backend` | `star_backend`, `li_ha` | Reagent addition is covered locally |
| Gate target population | 5 | (c) | `BD FACSMelody` | `BD FACSAria III`, `Sony SH800S` | No local flow-cytometer driver exists |
| Sort enriched fraction | 5 | (c) | `BD FACSMelody` | `BD FACSAria III`, `Sony SH800S` | Sorting is the key missing capability |
| Export sort counts / event files | 5 | (c) | `BD FACSMelody` | `BD FACSAria III` | Local readers cannot replace FCS/event export |
| Acid elution of bound phage | 6 | (a) | `vantage_backend` | `star_backend`, `li_ha` | Liquid manipulations stay on the workstation |
| Neutralization | 6 | (a) | `vantage_backend` | `star_backend`, `li_ha` | Same station as elution keeps traceability simple |
| Host infection setup | 6 | (a) | `vantage_backend` | `star_backend` | Liquid handler covers transfers and mixing |
| Amplification culture | 6 | (a) | `cytomat_backend` | `incubator_shaker_stack`, `bio_shake` | Requires protocol rewrite from flask to deep-well/plate format |
| Filter clarified supernatant through `0.22 um` membrane | 7 | (c) | `Tecan Resolvex A200` | manual syringe/vacuum filtration, `virtual_filter` | Chosen as the best automation-ready positive-pressure station among searched products |
| Colony imaging and ranking | 8 | (c) | `Molecular Devices QPix 420` | `Singer PIXL`, manual picking | No local colony-imaging picker exists |
| Pick and inoculate clones | 8 | (c) | `Molecular Devices QPix 420` | manual picking + `vantage_backend` | Picker remains the missing station |
| Clone rescreen by plate assay | 8 | (a) | `molecular_devices_backend` | `bio_tek_plate_reader_backend`, `clari_ostar_backend` | Local screening is possible after the missing picking step is solved |
| Load ELISA plate | 9 | (a) | `molecular_devices_backend` | `plate_reader`, `bio_tek_plate_reader_backend` | Strong local reader validation |
| Read `OD450` absorbance | 9 | (a) | `molecular_devices_backend` | `bio_tek_plate_reader_backend`, `clari_ostar_backend`, `plate_reader` | Well suited for ELISA confirmation |
| Optional fluorescence readback | 9 | (a) | `molecular_devices_backend` | `bio_tek_plate_reader_backend`, `clari_ostar_backend` | Useful when fluorescent reporters are retained |
| Extract plasmid from clones | 10 | (c) | `QIAcube Connect` | `Biomek` DNA purification protocol, manual miniprep | Local liquid-handler support exists, but no dedicated extraction station |
| Run clone-confirmation sequencing | 10 | (c) | `SeqStudio Genetic Analyzer` | external Sanger service, `SeqStudio Flex` | Current low-throughput benchtop match for clone verification |
| Assemble expression vector | 11 | (c) | `BioXp 3250` | `vantage_backend` plus manual Gibson/Golden Gate setup | Best web-backed automation station for construct generation |
| Transform expression host | 11 | (b) | `BioXp 3250` | `vantage_backend` + manual heat shock/electroporation | Local workstations can assist, but no finished transformation station exists |
| Expression culture induction | 12 | (a) | `cytomat_backend` | `bio_shake`, `incubator_shaker_stack` | Adequate after the workflow is shifted into automation-friendly culture format |
| Affinity purification | 12 | (c) | `ÄKTA pure` | manual chromatography, HPLC-adjacent local pieces | No local FPLC/AKTA-class station |
| Measure binding affinity | 12 | (c) | `Biacore 8K+` | outsourced assay service | No local SPR driver |
| Compare specificity panel | 12 | (c) | `Biacore 8K+` | ELISA-only surrogate assays | Specificity matrix work belongs on the SPR platform |
| Plate and carrier transport | 13 | (a) | `vantage_backend` | `star_backend`, CSV-only robot-arm entries | Integrated gripper beats adding a separate primary robot |
| Incubator / hotel storage | 13 | (a) | `cytomat_backend` | `incubator`, `hotel.thermo_orbitor_rs2_hotel` | Strongest validated local hotel behavior |
| Barcode and sample tracking | 13 | (a) | `cytomat_backend` | `QPix 420` for colony-specific tracking | Cytomat metadata explicitly mentions barcode reading |
| Consumable handling and tip replenishment | 13 | (a) | `vantage_backend` | `star_backend`, `li_ha` | Best overall local automation backbone |
