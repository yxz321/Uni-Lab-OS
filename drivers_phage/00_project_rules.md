# Project Rules

These rules govern every intermediate file in `Uni-Lab-OS/drivers_phage/`.

1. Automation-first: assay goals outrank the draft layout; vessel format, step grouping, and module boundaries may change when that improves automation fit.
2. Search-first access for large files: the aggregate CSVs and repo driver trees are searched before any targeted snippet reads.
3. Both CSVs are equal availability sources. A hit in `_aggregate_device_info_existing.csv` is not privileged over `_aggregate_device_info_output.csv`, and vice versa.
4. Screenshot-derived device ideas are draft suggestions only and never count as proof of availability.
5. Any unavailable-device recommendation must be backed by explicit web search, not model memory alone.
6. Findings are written to intermediate files as soon as they are established so we do not need to repeatedly reopen large sources.
7. Repo validation is targeted: `info.txt` and `registry.yaml` snippets are preferred; whole `driver.py` files are avoided unless there is no alternative.
8. The phage workflow is allowed to move from tubes/flasks into plate or deep-well formats when that preserves assay intent and materially improves automation coverage.
