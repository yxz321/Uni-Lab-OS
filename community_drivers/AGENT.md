# CLAUDE.md — Info Enrichment Workflow

Follow the monorepo-level rules in `../../AGENTS.md`.

## What this folder is

A large-scale AI-assisted enrichment pipeline that generates structured `info.txt`
metadata files for ~1008 community device drivers. The active version is **workflow v4**.

This is a **database-like folder** — `batches/` and `outputs/` contain many
repetitive per-device artifacts. Do not read them exhaustively; sample when needed.

## Key documentation (read these first)

- `README.md` — design principles, architecture, autonomy rules, file layout
- `WORKFLOW_CHANGELOG.md` — version history from prototypes through v4
- `workflow_v4/workflow_v4.md` — detailed operational guide for v4
- `workflow_v4/production_starter_prompt_v4.md` — bootstrap prompt for the main orchestrator
- `workflow_v4/agent_prompt_template_v4.md` — template prompt for device-reasoning subagents
- `production_state_v4.json` — persistent state: cursor, active batches, TODO queue

## Architecture

Two-agent split:

1. **Main orchestrator** — selects devices, creates batches, dispatches subagents,
   reviews results, decides on workflow updates
2. **Device-reasoning subagents** — execute the enrichment pipeline per batch

## Pipeline steps (per batch)

1. `extract_info_raw.py` — deterministic extraction from `driver.py` + `registry.yaml`
2. `run_pass_a.py` — semantic API call to interpret driver evidence
3. `compare_profile_vs_registry.py` — side-by-side comparison of Pass A vs registry
4. Agent conflict resolution + optional web search
5. `run_pass_b.py` — batch tag assignment API call
6. `render_info_txt.py` — merge all signals into final `info.txt`
7. `validate_info_txt.py` — structural YAML validation
8. `collect_proposed_tags.py` — append proposed tags to CSV
9. Subagent writes `report.md`

All scripts live in `workflow_v4/`. Run them from the repo root with paths like:
```bash
python3 workflow_v4/extract_info_raw.py --devices-file batches/<batch_id>/devices.txt --output-dir batches/<batch_id>
```

## File layout

- `workflow_v4/` — production scripts and prompt templates (source of truth)
- `batches/<batch_id>/` — per-batch working artifacts, one subfolder per device
- `production_state_v4.json` — persistent orchestration state
- Final output: `community_drivers/<device>/info.txt`

Batch naming: v4 batches use `v4_batch_###`. Legacy v1-v3 batches and prototype
batches also exist in `batches/` — do not modify them.

## Semantic boundary

- Scripts are **deterministic only** — extraction, transport parsing, merge/render, structural validation
- Scripts do **not** perform semantic repair
- If Pass A or Pass B JSON violates schema, the run fails and preserves trace artifacts
- All semantic reasoning happens in the AI agent or API calls, not in scripts

## Current production state

- Last completed batch: `v4_batch_011` (~110 devices processed)
- Next device cursor: `broadcast_udp_port_mapper_client` (device #104 of ~1008)
- Batch size: 10 devices per normal batch
- Success streak: 10

## Important rules

- Do not modify workflow docs/scripts unless performing an explicit workflow-update cycle
- Commit locally before any workflow-update cycle; prefix message with `v4:`
- Prefer prompt changes over script-based semantic patching
- Web search is agent-triggered, not script-triggered
- Append next-cycle TODOs before waiting, dispatching, or entering workflow-update mode
- Quality bar: structural validation + report review + manual sampling (not just PASS/FAIL)

## API credentials

Keep outside this repo. See `README.md` for the recommended secret file location.
