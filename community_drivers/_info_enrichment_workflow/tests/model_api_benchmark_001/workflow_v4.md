# Workflow v4: Operational Guide

This file is the human-readable overview of workflow `v4`.
It is intentionally more detailed than the minimal run commands so that we can
understand the information flow without having to inspect the scripts.

## Core idea

Workflow `v4` separates the problem into four distinct layers:

1. deterministic local extraction
2. driver-derived semantic interpretation by API
3. script-assisted comparison, followed by agent-side conflict resolution and optional web search
4. batch-level tag assignment from the conflict-resolved semantic profile

The key information-flow rule is:
- registry information may help the agent detect conflicts
- but registry-derived fields must not flow directly into Pass B
- Pass B should see only the conflict-resolved `02_device_profile_api.json`

Boundary rule:
- scripts do deterministic extraction, transport-level response parsing,
  direct merge/render, and structural validation only
- scripts do not perform semantic repair
- if Pass A or Pass B semantic JSON does not match the required schema, the
  run should fail and preserve trace artifacts

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

## Pass order

```
1. extract_info_raw.py    ->  materials/<device>/01_local_signals.json        (script)
2. prepare_model_run.py   ->  runs/<api_model>/<device>/01_local_signals.json  (script)
3. run_pass_a.py          ->  02_device_profile_api.json                      (API, per device)
4. compare_profile_vs_registry.py -> 02_profile_registry_compare.json         (script)
5. Agent conflict check   ->  optional web search + manual 02 update          (agent)
6. run_pass_b.py          ->  _batch_tag_api.json                             (API, per batch)
7. render_info_txt.py     ->  03_enriched_payload.json + info.txt             (script)
8. validate_info_txt.py   ->  validation report                               (script)
9. Agent QA               ->  final review + batch report                     (agent)
```

## Folder layout

All benchmark outputs stay inside this working folder:

- `_info_enrichment_workflow/tests/model_api_benchmark_001/materials/`
- `_info_enrichment_workflow/tests/model_api_benchmark_001/runs/<api_model>/`
- `_info_enrichment_workflow/tests/model_api_benchmark_001/reports/`

Do not write benchmark `info.txt` outputs into `community_drivers/<device>/info.txt`.

## Step 1: Local extraction

Command:

```bash
python3 scripts/extract_info_raw.py --devices-file devices.txt
```

Input:
- raw `registry.yaml`
- raw `driver.py`

Output:
- `materials/<device>/01_local_signals.json`

Purpose:
- produce deterministic local signals once
- identify the focal class from `class.module`
- annotate focal methods as `status_getter`, `status_setter`, or `command`
- preserve registry evidence for later conflict checking
- preserve driver evidence for Pass A only

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
- the orchestrator agent must not read the `driver` section

## Step 2: Seed a model run

Command:

```bash
python3 scripts/prepare_model_run.py --model gpt-5.4-nano
```

Purpose:
- copy `01_local_signals.json` into a model-specific run folder
- keep each model run self-contained and directly comparable

Output:
- `runs/<api_model>/<device>/01_local_signals.json`

## Step 3: Pass A semantic profile

Command:

```bash
python3 scripts/run_pass_a.py \
  --signals-dir runs/gpt-5.4-nano \
  --model gpt-5.4-nano \
  --reasoning-effort medium
```

Input to Pass A:
- driver-derived evidence from `01_local_signals.json`
- registry action ids

Pass A does not receive unreliable registry identity fields as semantic input.

Output:
- `02_device_profile_api.json`
- `_02_device_profile_api_trace.json`

What `02_device_profile_api.json` contains:
- sanitized metadata
- token usage
- parsed semantic result

Parsed fields:
- `name`
- `name_en`
- `manufacturer`
- `description`
- `description_en`
- `actions[]`
- `tag_hints[]`

Design intent:
- `02_device_profile_api.json` is the driver-derived semantic profile
- it is the main object the agent reasons over in conflict resolution
- after conflict resolution, it becomes the sole semantic input to Pass B
- if manufacturer remains uncertain, Pass A should return an empty string

## Step 4: Script-assisted profile vs registry comparison

Command:

```bash
python3 scripts/compare_profile_vs_registry.py --signals-dir runs/gpt-5.4-nano
```

Output:
- `02_profile_registry_compare.json`

The comparison artifact extracts only these fields side by side:
- `name`
- `name_en`
- `manufacturer`
- `description`
- `description_en`

Important rule:
- this script does not decide whether web search is needed
- it only presents Pass A output and registry values side by side for agent review

## Step 5: Agent conflict check and web search

The agent reads:
- side-by-side comparison in `02_profile_registry_compare.json`

The agent must not read full `02_device_profile_api.json`.

Web search is **not** triggered by script heuristics. Instead:

1. Pass A produces the device profile from driver evidence only.
2. The comparison script produces `02_profile_registry_compare.json`.
3. The agent compares the Pass A output with the registry entry by reading
   only `02_profile_registry_compare.json`.
4. If there is significant conflict or important fields are still empty, the
   agent triggers targeted web search.
5. Web search results refine `name`, `name_en`, `manufacturer`,
   `description`, and `description_en` in `02_device_profile_api.json`.
6. If manufacturer remains uncertain after web search, leave it empty.

If there is meaningful conflict or important missing information:
- do targeted web search
- save compact findings in `websearch_evidence.json`
- manually update the parsed fields in `02_device_profile_api.json`

Fields the agent may update in `02_device_profile_api.json`:
- `parsed.name`
- `parsed.name_en`
- `parsed.manufacturer`
- `parsed.description`
- `parsed.description_en`
- optional `websearch_evidence_path`

Important editing rule:
- the agent edits only those five parsed fields, plus `websearch_evidence_path`
- the agent performs those edits without using full `02_device_profile_api.json`
  as a reading context

Important information-flow rule:
- registry data and web findings are agent-side only
- they should influence Pass B only indirectly through the updated
  `02_device_profile_api.json`
- they must not be passed directly into the Pass B API request

## Step 6: Pass B batch tag assignment

Command:

```bash
python3 scripts/run_pass_b.py \
  --signals-dir runs/gpt-5.4-nano \
  --model gpt-5.4-nano \
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

Output:
- `_batch_tag_api.json`
- `_batch_tag_api_trace.json`

Device-level tag result fields:
- `existing_tags`
- `proposed_new_tags`

Pass B contract:
- each returned tag object must already include a device-specific `rationale`
- the script should preserve returned tag objects rather than normalizing them

## Tagging rules

The combined set of `existing_tags + proposed_new_tags` must contain at least
one tag of each type:

- `experimental_step`
- `experimental_domain`
- `experimental_scene`
- `device_template_tag`

Guidance:
- prefer existing tags when they are reasonably relevant
- include all relevant tags rather than exactly one tag per type
- a practical default is around 1-4 relevant tags per type when supported
- prefer mitigating false negatives over false positives

Proposal rules:
- `experimental_step`: existing tags only, no new proposals
- new proposals are allowed for:
  - `experimental_domain`
  - `experimental_scene`
  - `device_template_tag`
- multiple proposals are allowed

Proposal breadth requirements:
- `device_template_tag`: broad enough to cover multiple real-world devices
- `experimental_scene`: broad enough to cover multiple device templates
- `experimental_domain`: broad enough to cover multiple scenes

## Step 7: Merge and render

Command:

```bash
python3 scripts/render_info_txt.py --signals-dir runs/gpt-5.4-nano
```

Inputs:
- `01_local_signals.json`
- `02_device_profile_api.json`
- `_batch_tag_api.json`
- optional `websearch_evidence.json` (via path carried in `02`)

Outputs:
- `03_enriched_payload.json`
- `info.txt`

Rendering rules:
- device-entry `tags` is the one-line list from the combined set of
  `existing_tags + proposed_new_tags`
- device-entry `category` is derived scriptically from the combined
  `device_template_tag` names, not from registry category
- device-entry `category` and `tags` should be Chinese-preferred string lists
- `tag_hints` may be English or Chinese, but English is preferred
- language preference is enforced by prompt/QA, not renderer heuristics
- metadata now stores:
  - `existing_tags`
  - `proposed_new_tags`
- `websearch_evidence` is copied in only if available locally

## Final info.txt shape

Top-level structure:
- `<device_key>`
- `auto_annotation_metadata`

Device entry keeps:
- `name`
- `name_en`
- `manufacturer`
- `category`
- `tags`
- `description`
- `description_en`
- `class.action_value_mappings`

Metadata keeps:
- `registry_key`
- `annotation_workflow_version`
- `tag_hints`
- `existing_tags`
- `proposed_new_tags`
- `websearch_evidence`
- `processing_pass_order`

## Step 8: Validate

Preferred command:

```bash
python3 ../../validate_info_txt.py $(find runs/gpt-5.4-nano -name info.txt | sort)
```

Validation rules:
- top-level structure is correct
- required device-entry fields exist
- metadata uses `existing_tags` and `proposed_new_tags`
- required tag-type coverage is checked on the combined set:
  - `existing_tags + proposed_new_tags`
- device-entry `tags` remains a list of short strings
- validation is structural only; rationale quality and language quality are QA topics

## Step 9: Agent QA

Allowed device-specific inputs:
- `02_profile_registry_compare.json`
- optional `websearch_evidence.json`
- `_batch_tag_api.json`
- sampled rendered `info.txt`

Forbidden inputs:
- raw `driver.py`
- raw `registry.yaml`
- full `02_device_profile_api.json`
- the `driver` section of `01_local_signals.json`
- the `registry` section of `01_local_signals.json`

The agent must write a short batch report into the model run folder.

## Summary of the information flow

- `01_local_signals.json` contains both registry and driver evidence
- Pass A uses driver-derived evidence and action ids
- `compare_profile_vs_registry.py` extracts only the five identity/description
  fields into `02_profile_registry_compare.json`
- the agent compares Pass A against registry by reading only
  `02_profile_registry_compare.json`, then optionally uses web evidence
- the agent edits `02_device_profile_api.json` if conflict resolution is needed
- Pass B uses only the conflict-resolved `02_device_profile_api.json`
- rendering combines tags into final device-entry `tags` and derives
  `category` from template tags
- validation checks coverage on `existing_tags + proposed_new_tags`
