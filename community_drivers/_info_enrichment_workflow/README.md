# Device Info Enrichment Workflow

This folder documents the active production workflow for generating enriched
`info.txt` files in `community_drivers`.

Current active workflow/schema version: `v4`

## Local API secret setup

If we use plain model API calls for semantic substeps, keep credentials outside
this repo.

Recommended local secret file:
- `~/.config/unilabos/openai.env`

Contents:

```bash
export OPENAI_API_KEY='your_real_key_here'
# optional
export OPENAI_BASE_URL='https://api.openai.com/v1'
```

Connectivity helper:
- `community_drivers/_info_enrichment_workflow/test_openai_api.py`

## Design principle

This is a large-scale enrichment task. The goal is useful, consistent, and
honest metadata, not perfection.

- A quality level comparable to the accepted current examples is good enough.
- Do not over-invest in polishing individual devices beyond what is needed to
  keep the corpus broadly useful.
- Prefer steady throughput and consistent rules over isolated high-effort edits.

## Active architecture

Workflow `v4` has two distinct agent roles.

### Main orchestrator

The main orchestrator:
- reads the root workflow docs and state
- chooses the next devices in sorted order
- creates production batches under `_info_enrichment_workflow/batches/`
- generates the device-reasoning subagent prompt from the shared template
- dispatches subagents
- reads validator results and subagent reports
- decides whether a workflow update is needed
- appends next-cycle TODOs into `_info_enrichment_workflow/production_state_v4.json`

Default main orchestrator model:
- `GPT-5.4`

### Device-reasoning subagents

The device-reasoning subagent:
- works on one batch folder only
- runs deterministic extraction, Pass A, compare, optional web search,
  Pass B, render, validation, and reporting
- writes final `info.txt` to `community_drivers/<device>/info.txt`
- keeps all intermediate files in the assigned batch folder

Default device-reasoning model:
- `gpt-5.3-codex`

Default semantic API model:
- `Vendor2/GPT-5.4`

## Production file layout

Workflow source files live under:
- `_info_enrichment_workflow/workflow_v4/`

Persistent state lives at:
- `_info_enrichment_workflow/production_state_v4.json`

Batch-local artifacts live under:
- `_info_enrichment_workflow/batches/<batch_id>/`

Each batch folder should contain:
- `manifest.json`
- `devices.txt`
- `agent_prompt.md`
- `report.md`
- one subfolder per device for intermediate artifacts and trace files
- optional validation-diff or trigger-validation artifacts

Final outputs live directly in device folders:
- `community_drivers/<device>/info.txt`

## Normal production flow

1. Run a 2-device production verification batch first.
2. After the verification batch succeeds, continue with 10-device batches.
3. Use the first devices in sorted order.
4. Treat all devices as needing rerun because `v4` changes `info.txt`
   structure materially from `v3`.
5. Keep working state in batch folders and persistent state at the root.

Production helpers:
- `_info_enrichment_workflow/workflow_v4/prepare_batch_v4.py`
- `_info_enrichment_workflow/workflow_v4/build_agent_prompt.py`
- `_info_enrichment_workflow/workflow_v4/extract_info_raw.py`
- `_info_enrichment_workflow/workflow_v4/run_pass_a.py`
- `_info_enrichment_workflow/workflow_v4/compare_profile_vs_registry.py`
- `_info_enrichment_workflow/workflow_v4/run_pass_b.py`
- `_info_enrichment_workflow/workflow_v4/render_info_txt.py`
- `_info_enrichment_workflow/workflow_v4/collect_proposed_tags.py`
- `_info_enrichment_workflow/workflow_v4/validate_info_txt.py`

## Autonomy rules

The main orchestrator should continue autonomously through normal production.

Before waiting on subagents, before starting the next normal batch, and before
entering workflow-update mode, append the next-cycle TODOs into
`production_state_v4.json`.

This applies both when a workflow update is needed and when no workflow update
is needed.

API patience rule:
- do not interrupt slow Pass A or Pass B runs just because they are quiet
- only react to concrete failures such as HTTP errors, timeouts, schema
  failures, or missing output artifacts

## Policy-update validation runs

When testing a workflow change on trigger devices:

- commit locally before entering the workflow-update cycle
- start the commit message with the workflow version, for example `v4: ...`
- prefer prompt changes in Pass A, Pass B, and the subagent prompt over
  script-based semantic patching
- prefer writing candidate outputs to staged or temp files first
- compare old vs new result
- only adopt the update if the new result is visibly better
- append next-cycle TODOs before entering the update cycle so the autonomous
  loop does not stop
- after a validated update, continue from the current device cursor rather than
  restarting the corpus

The only full-rerun exception is the initial promotion from `v3` to `v4`,
because the `info.txt` structure changed materially.

## Success criteria for scaling

A batch counts as successful only if all of the following are true:

- the structural validator passes
- the subagent report does not surface a blocking or workflow-changing issue
- sampled `name`, `description`, `tags`, and 3 sampled action summaries in the
  report look acceptable for the current quality bar
- my own review of the report does not identify a workflow change that should
  be made before continuing

Passing validation alone is not enough.

If a review suggests a workflow change, enter the workflow-update cycle and
reset the scaling success streak after the change is adopted.

## Proposed tags

Proposed tags append to:
- `community_drivers/tag_additions_proposed.csv`

Operational rule:
- preserve mixed Chinese/English text correctly with UTF-8-safe handling
- parallel runs may introduce duplicate ids or repeated signals
- do not block production on cleanup now; clean them later in a separate pass

## Versioning convention

Versioning is now split across workflow lineage and batch lineage.

- Historical prototype versions use `prototype_vX.Y`.
- Major production workflow versions use `vN`.
- Generated `info.txt` should carry the active workflow version exactly in
  `auto_annotation_metadata.annotation_workflow_version`.
- Because `_info_enrichment_workflow/batches/` already contains historical
  production batches, new `v4` major-rerun batches should use `v4_batch_###`
  naming to avoid ambiguity.
- Prompt-only updates within `v4` keep the same output structure and continue
  from the current cursor.
