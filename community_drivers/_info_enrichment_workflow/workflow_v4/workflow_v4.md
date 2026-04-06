# Workflow v4: Production Operational Guide

This file is the production overview for workflow `v4`.
It explains the real production information flow, file layout, agent split, and
update cycle without requiring anyone to inspect the scripts first.

## Active defaults

- main orchestrator agent: `GPT-5.4`
- device-reasoning subagent: `gpt-5.3-codex`
- semantic API model: `Vendor2/GPT-5.4`
- API reasoning effort: `medium`
- Pass A timeout: `240s`
- Pass A request fan-out: parallel, default `4` concurrent devices
- Pass B timeout: `240s`
- first production verification batch: `2` devices
- normal production batch size: `10`

## Core idea

Workflow `v4` separates the enrichment problem into five clean layers:

1. deterministic local extraction by script
2. per-device semantic interpretation by API (Pass A)
3. script-assisted comparison plus agent-side conflict resolution and optional web search
4. batch-level tag assignment by API (Pass B)
5. direct merge, render, and structural validation by script

Boundary rule:
- scripts perform deterministic extraction, transport-level response parsing,
  merge/render, and structural validation only
- scripts do not perform semantic repair
- if Pass A or Pass B semantic JSON does not match schema, the run fails and
  preserves trace artifacts

## Two-agent split

There are two different agents in production, and they must stay distinct.

### Main orchestrator agent

The main orchestrator reads:
- `_info_enrichment_workflow/README.md`
- `_info_enrichment_workflow/WORKFLOW_CHANGELOG.md`
- `_info_enrichment_workflow/production_state_v4.json`
- `_info_enrichment_workflow/workflow_v4/workflow_v4.md`
- `_info_enrichment_workflow/workflow_v4/production_starter_prompt_v4.md`
- `_info_enrichment_workflow/workflow_v4/agent_prompt_template_v4.md`

The main orchestrator is responsible for:
- selecting the next devices in sorted order
- creating batches under `_info_enrichment_workflow/batches/`
- generating the device-reasoning subagent prompt from the shared template
- dispatching subagents
- reading validator results and subagent reports
- updating workflow prompts/docs/scripts when needed
- appending next-cycle TODOs into `production_state_v4.json` before waiting,
  before dispatching the next normal batch, and before entering workflow-update mode

### Device-reasoning subagents

The device-reasoning subagent works on one batch folder only.
It performs deterministic extraction, Pass A, compare, optional web search,
Pass B, render, validation, tag proposal collection, and batch reporting.

For device semantics, the subagent may read only:
- `02_profile_registry_compare.json`
- optional `websearch_evidence.json`
- `_batch_tag_api.json`
- sampled final `info.txt`

The device-reasoning subagent must not read:
- raw `driver.py`
- raw `registry.yaml`
- full `02_device_profile_api.json`
- raw device sections of `01_local_signals.json`

The subagent is still allowed to run the extraction and API scripts; the file
restriction applies to semantic reading context, not to executing the workflow.

## Production file layout

Production source files live under:
- `_info_enrichment_workflow/workflow_v4/`

Batch-local working artifacts live under:
- `_info_enrichment_workflow/batches/<batch_id>/`

Each batch folder should contain:
- `manifest.json`
- `devices.txt`
- `agent_prompt.md`
- `report.md`
- one subfolder per device, containing intermediate artifacts and trace files
- optional validation-diff or trigger-validation artifacts

Final output always lives directly in:
- `community_drivers/<device>/info.txt`

No production `runs/`, `materials/`, or `reports/` subfolders are used under
`workflow_v4/`.

Batch-selection rule:
- batch-level scripts should resolve device artifact directories from the
  explicit batch metadata (`devices.txt`, or `manifest.json` as fallback) when
  present
- do not infer device inclusion by excluding directory names that begin with
  `_`, because valid device ids in this corpus may start with underscores

## State file

Production state is tracked at:
- `_info_enrichment_workflow/production_state_v4.json`

The state file should track at least:
- active workflow version
- current cursor / next device
- current batch id
- queued batch ids
- main orchestrator model
- subagent model
- API model
- current batch size
- active batches / active agents
- success streak
- parallelism target
- pending workflow candidate
- last completed batch
- last reviewed batch
- append-only TODO list / next actions
- an IDE todo stack synchronized with the same next-cycle actions

Control rule:
- append next-cycle TODOs before waiting on subagents
- append next-cycle TODOs before dispatching the next normal batch
- append next-cycle TODOs before entering workflow-update mode
- keep the IDE todo stack synchronized with those same next-cycle actions so the autonomous loop can resume reliably across turn boundaries

This rule applies whether or not a workflow update is needed.

## Information priority

For identity and description decisions, use this priority:

1. online search
2. Pass A driver-derived profile as surfaced in `02_profile_registry_compare.json`
3. extracted registry values as surfaced in `02_profile_registry_compare.json`

Registry reliability ranking:

More reliable:
- `class.action_value_mappings`
- `class.module`
- `class.status_types`

Less reliable, treat with caution:
- `description`
- `device_params`
- `manufacturer`
- `model`
- `name`
- `category`
- `tags`
- `scene`

## Production pass order

For a batch folder `<batch_dir>`:

```text
1. extract_info_raw.py                ->  <batch_dir>/<device>/01_local_signals.json
2. run_pass_a.py                      ->  <batch_dir>/<device>/02_device_profile_api.json
3. compare_profile_vs_registry.py     ->  <batch_dir>/<device>/02_profile_registry_compare.json
4. agent conflict check + web search  ->  optional edits to 02 + websearch_evidence.json
5. run_pass_b.py                      ->  <batch_dir>/<device>/_batch_tag_api.json
6. render_info_txt.py                 ->  <batch_dir>/<device>/03_enriched_payload.json
7. render_info_txt.py --write-info-txt -> community_drivers/<device>/info.txt
8. validate_info_txt.py               ->  structural validation
9. collect_proposed_tags.py           ->  optional append to tag_additions_proposed.csv
10. subagent report                   ->  <batch_dir>/report.md
```

## Step 1: Deterministic local extraction

Command:

```bash
python3 workflow_v4/extract_info_raw.py \
  --devices-file _info_enrichment_workflow/batches/<batch_id>/devices.txt \
  --output-dir _info_enrichment_workflow/batches/<batch_id>
```

Input:
- raw `registry.yaml`
- raw `driver.py`

Output:
- `<batch_dir>/<device>/01_local_signals.json`

What `01_local_signals.json` contains:
- `registry`
  - `name`
  - `category`
  - `manufacturer`
  - `model`
  - `description`
  - `module`
  - `status_types`
  - `tags`
  - `scene`
  - simplified registry `actions`
- `driver`
  - module docstring
  - all classes
  - focal class
  - focal methods
  - function type annotations
  - collected comments/docstrings

Important rule:
- the `driver` section is for Pass A only
- the device-reasoning subagent must not use the `driver` section as manual
  semantic reading context

## Step 2: Pass A semantic profile

Command:

```bash
python3 workflow_v4/run_pass_a.py \
  --signals-dir _info_enrichment_workflow/batches/<batch_id> \
  --model Vendor2/GPT-5.4 \
  --reasoning-effort medium
```

Pass A uses:
- driver-derived evidence from `01_local_signals.json`
- reliable action ids from the registry extraction

Pass A does not use unreliable registry identity fields as semantic input.

Output per device:
- `02_device_profile_api.json`
- `_02_device_profile_api_trace.json`

Parsed fields in `02_device_profile_api.json`:
- `name`
- `name_en`
- `manufacturer`
- `description`
- `description_en`
- `actions[]`
- `tag_hints[]`

Pass A contract:
- if manufacturer remains uncertain, return an empty string
- use `action_name`, not alternate keys
- describe the physical device, not a backend/wrapper
- if schema is violated, preserve the trace and fail the batch

## Step 3: Script-assisted compare artifact

Command:

```bash
python3 workflow_v4/compare_profile_vs_registry.py \
  --signals-dir _info_enrichment_workflow/batches/<batch_id>
```

Output per device:
- `02_profile_registry_compare.json`

This comparison artifact contains only:
- `name`
- `name_en`
- `manufacturer`
- `description`
- `description_en`

The compare artifact does not decide whether web search is needed.
It only presents the Pass A profile and extracted registry values side by side.

## Step 4: Agent conflict check and web search

The device-reasoning subagent reads only `02_profile_registry_compare.json`
when deciding whether conflict resolution is needed.

Web search is not triggered by script heuristics. Follow this sequence:

1. Pass A produces the driver-derived device profile.
2. The compare script produces `02_profile_registry_compare.json`.
3. The subagent compares Pass A output with the extracted registry values by
   reading only `02_profile_registry_compare.json`.
4. If there is significant unresolved identity conflict or important fields are
   still empty, the subagent triggers targeted web search.
5. Web search findings refine only:
   - `name`
   - `name_en`
   - `manufacturer`
   - `description`
   - `description_en`
   in `02_device_profile_api.json`.
6. If manufacturer remains uncertain after web search, leave it empty.

Interpretation rule:
- do not web search just because weak registry metadata disagrees with a
  coherent Pass A profile
- do not web search solely because registry wording looks like a backend or
  wrapper if Pass A already identifies a plausible physical device
- do not web search solely to fill manufacturer when the device family and
  description are already coherent; empty manufacturer is acceptable
- use web search mainly when the physical device identity is still unclear, the
  conflict would change the device family, or the key identity/description
  fields remain too uncertain to trust

Optional output per device:
- `websearch_evidence.json`

Important information-flow rule:
- registry and web findings are agent-side only
- they influence Pass B only indirectly through the updated
  `02_device_profile_api.json`
- they must not be passed directly into the Pass B API request

## Step 5: Pass B batch tag assignment

Command:

```bash
python3 workflow_v4/run_pass_b.py \
  --signals-dir _info_enrichment_workflow/batches/<batch_id> \
  --model Vendor2/GPT-5.4 \
  --reasoning-effort medium
```

Pass B input:
- only the conflict-resolved `02_device_profile_api.json`
- full tag list once per batch

Pass B uses:
- `name`
- `name_en`
- `manufacturer`
- `description`
- `description_en`
- `tag_hints`
- action descriptions

Pass B does not use:
- registry `category`
- registry `tags`
- registry `scene`
- registry `module`
- any other raw registry fields

Output per device:
- `_batch_tag_api.json`
- `_batch_tag_api_trace.json`

Tagging rules:
- the combined set of `existing_tags + proposed_new_tags` must include at least
  one tag of each type:
  - `experimental_step`
  - `experimental_domain`
  - `experimental_scene`
  - `device_template_tag`
- prefer existing tags when reasonably relevant
- include all relevant tags rather than exactly one per type
- a practical default is around 1-4 relevant tags per type when supported
- `experimental_step` may use existing tags only
- new proposals are allowed only for:
  - `experimental_domain`
  - `experimental_scene`
  - `device_template_tag`
- multiple proposals are allowed
- every selected or proposed tag must include a device-specific rationale

## Step 6: Merge and render

Command:

```bash
python3 workflow_v4/render_info_txt.py \
  --signals-dir _info_enrichment_workflow/batches/<batch_id> \
  --write-info-txt
```

Optional preview copy:

```bash
python3 workflow_v4/render_info_txt.py \
  --signals-dir _info_enrichment_workflow/batches/<batch_id> \
  --write-preview
```

Inputs:
- `01_local_signals.json`
- `02_device_profile_api.json`
- `_batch_tag_api.json`
- optional `websearch_evidence.json` via `websearch_evidence_path` or the
  batch-local default file name `websearch_evidence.json` when present

Outputs per device:
- `03_enriched_payload.json`
- final `community_drivers/<device>/info.txt`
- optional batch-local `info.txt` preview if requested

Rendering rules:
- device-entry `tags` comes from the combined set of `existing_tags + proposed_new_tags`
- device-entry `category` is derived from combined `device_template_tag` names,
  not from registry category
- device-entry `category` and `tags` are Chinese-preferred string lists
- metadata stores:
  - `existing_tags`
  - `proposed_new_tags`
  - `tag_hints`
  - optional `websearch_evidence`
- renderer does not perform semantic cleanup or repair

## Step 7: Validation

Command:

```bash
python3 workflow_v4/validate_info_txt.py \
  --manifest _info_enrichment_workflow/batches/<batch_id>/manifest.json
```

Validation is structural only.
It checks:
- YAML parses
- required top-level keys
- required device-entry fields
- required metadata fields
- combined tag-type coverage from `existing_tags + proposed_new_tags`
- required fields in each tag object
- action schema presence

Validation does not judge:
- rationale quality
- Chinese/English quality
- manufacturer confidence beyond field presence

## Step 8: Proposed tags

Command:

```bash
python3 workflow_v4/collect_proposed_tags.py \
  --signals-dir _info_enrichment_workflow/batches/<batch_id> \
  --append
```

This appends proposed tags to:
- `community_drivers/tag_additions_proposed.csv`

Encoding rule:
- the file should be written as UTF-8-safe mixed Chinese/English text

Current operational rule:
- duplicate ids or repeated signals may be introduced by parallel runs
- do not block production on deduping them now
- cleanup can happen later

## Batch report

The device-reasoning subagent writes one short batch report to:
- `_info_enrichment_workflow/batches/<batch_id>/report.md`

The report should include:
- devices processed
- what worked well
- what still needs fixing
- proposed new tags, whether appended or discarded
- for 2 sampled devices: only `name`, `description`, `tags`
- 3 sampled action summaries
- recommended prompt/workflow changes, if any

## Autonomous production loop

Normal continuation:
- append next-cycle TODOs to `production_state_v4.json`
- wait for subagent completion
- read validator result
- read subagent report
- if no workflow update is needed, append next-cycle TODOs again before
  dispatching the next normal batch and continue automatically

Workflow-update continuation:
- append next-cycle TODOs to `production_state_v4.json` before entering update mode
- commit locally before entering workflow-update mode
- start commit message with workflow version, for example `v4: tighten Pass B rationale wording`
- prefer updating:
  - Pass A prompt
  - Pass B prompt
  - device-reasoning subagent prompt
- minimize script-based semantic patching
- run trigger-device validation before adopting the update
- adopt the update only if the result is visibly better
- continue from the current cursor after adoption

Important rule:
- workflow updates after promotion should not change `info.txt` structure
- the only full-rerun exception is the initial `v4` promotion from `v3`

## Summary of the information flow

- deterministic extraction produces `01_local_signals.json`
- Pass A uses driver-derived evidence and action ids
- compare script extracts only the five identity/description fields into
  `02_profile_registry_compare.json`
- the subagent compares Pass A against extracted registry values by reading
  only `02_profile_registry_compare.json`, then optionally uses web evidence
- the subagent edits only the five identity/description fields in `02`
- Pass B uses only the conflict-resolved `02_device_profile_api.json`
- rendering combines tags and derives `category` from template tags
- validation checks structure and combined-tag coverage only
- batch-local artifacts stay in `_info_enrichment_workflow/batches/`
- final `info.txt` lives directly in each device folder
