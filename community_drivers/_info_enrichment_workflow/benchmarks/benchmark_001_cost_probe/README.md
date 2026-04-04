# Benchmark 001: Cost Probe

Purpose:
- Compare cheaper agent candidates against existing gpt-5.3 production outputs.

Devices:
- bio_shake: straightforward biology lab device with useful code comments.
- cc_core: harder identity-conflict device with broader action surface.

Ground truth for practical comparison:
- Current production `info.txt` files produced/validated in the existing workflow.

Candidate models under test:
- gpt-5.4-mini
- gpt-5.1-codex-mini
- gpt-5.2-codex

All candidate outputs must be staged under `candidates/<model_slug>/` and must not overwrite live device files.
