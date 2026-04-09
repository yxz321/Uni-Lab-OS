Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Reconciliation With `community_drivers/_device_availability_assessment.md`

The independent assessment file was read only after the local protocol rewrite, CSV union search, and repo validation were completed.

## High-level comparison

| Topic | Assessment file | Independent mapping in this folder | Reconciliation |
|---|---|---|---|
| Incubator coverage | Full | Full | Agreement. `cytomat_backend` is the best lead in both views. |
| Shaking incubator coverage | Full | Full | Agreement. The independent mapping prefers `cytomat_backend` as bundle lead and `incubator_shaker_stack` as alternate depending carrier format. |
| Centrifuge coverage | Full | Full | Agreement. |
| Liquid handler coverage | Full | Full | Agreement. Independent mapping is more specific in preferring `vantage_backend` because the local validation showed the broadest action surface plus integrated gripper handling. |
| FACS / flow cytometry | Not present | Not present | Agreement. |
| Colony picker | Not present | Not present | Agreement. |
| Filtration | Not present | Not present | Agreement. |
| ELISA | Partial | Readout available; workflow still partial | Mostly agreement. The independent mapping splits the problem into reader-available `(a)` functions and washer/dispenser-missing `(b)/(c)` functions. |
| Plasmid extraction | Partial via Biomek DNA purification | Dedicated station missing | Agreement in substance. The independent mapping accepts that a liquid handler can partially cover the chemistry, but still recommends `QIAcube Connect` as the dedicated unavailable device. |
| DNA sequencing | Not present | Not present | Agreement. |
| Protein purification | Partial via HPLC-adjacent pieces | Dedicated AKTA-class station missing | Agreement in substance. The independent mapping is simply more explicit about the target instrument family. |
| Biacore / SPR | Not present | Not present | Agreement. |
| Expression vector construction | Not present | Not present | Agreement. |

## Useful extra detail from the assessment file that was adopted

- The assessment explicitly calls out `heraeus_cytomat_backend` and `incubator_stx` as additional incubator-class alternatives.
- It surfaces `access2_backend` and `v_spin_backend` as useful centrifuge alternates, which aligns with the local search.
- It clarifies that the strongest local coverage for plasmid extraction is really protocol-level support on Biomek rather than a dedicated plasmid-prep instrument.
- It usefully separates `FACS` from `flow cytometer (analysis only)`, reinforcing that both analysis and sorting remain gaps.

## Differences worth preserving

### 1. The independent mapping is workflow-shaped, not device-list-shaped

The assessment compares a target device list to the repo. The independent mapping here instead decomposes the phage protocol into per-function rows. That is why:

- ELISA readout is marked locally available here, while the overall ELISA bundle still shows a missing washer/dispenser.
- Phage recovery is treated as a combination of already-available liquid handling plus incubation, not as a unique standalone device gap.
- Protein validation is split into expression, purification, and SPR measurement instead of being flattened into a single “protein purification system” row.

### 2. The independent mapping prefers locally validated devices over CSV-only matches

- `vantage_backend` is elevated because its `info.txt` and `registry.yaml` showed both pipetting and integrated gripper support.
- CSV-only robot-arm hits were deprioritized because the corresponding local driver folders were not present during targeted validation.

### 3. The independent mapping adds explicit unavailable product recommendations

The assessment stops at “missing” or “partial.” This staging folder continues to:

- pick a best unavailable product
- instantiate a deep-search prompt
- collect evidence
- generate a `driver_guessed.py` stub

## Final reconciliation judgment

There are no substantive contradictions that would force a change in the independent mapping. The assessment file mostly corroborates the local findings, and the main value it adds is a few extra alternative device names plus clearer wording around the difference between partial workflow coverage and dedicated instrument coverage.
