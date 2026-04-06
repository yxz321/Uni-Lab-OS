# Model API Benchmark Orchestrator Prompt

You are orchestrating one benchmark run of workflow `v4` for exactly one API model.

## Scope

Work only inside this benchmark folder:
- `_info_enrichment_workflow/tests/model_api_benchmark_001/`

Do not edit any files under `community_drivers/<device>/`.
Do not write benchmark outputs outside this benchmark folder.

## Goal

Run the benchmark workflow for one API model using the provided scripts and local API credentials.
The objective is to produce a self-contained run folder for later cross-model comparison.

Important boundary:
- scripts perform deterministic extraction, transport-level response parsing,
  merge/render, and structural validation only
- scripts do not perform semantic repair
- if Pass A or Pass B semantic JSON does not match the required schema, treat
  that as a benchmark failure and preserve the trace artifacts

## Required workflow

1. If `01_local_signals.json` is missing or stale, run deterministic local extraction with `extract_info_raw.py`.
2. Seed or reseed the assigned run folder from `materials/` if needed.
3. Confirm the model run folder contains `01_local_signals.json` per device.
4. Run Pass A with the assigned API model and reasoning effort `medium`.
5. Run the comparison script to produce `02_profile_registry_compare.json` per device.
6. Read `02_profile_registry_compare.json` and compare the Pass A profile with the extracted registry entry side by side.
7. Trigger web search only if there is significant conflict or important fields are still empty.
8. If web search is used, save compact `websearch_evidence.json` files and manually update only the five identity/description fields in `02_device_profile_api.json`.
9. Run Pass B with the same API model and reasoning effort `medium`.
10. Render `03_enriched_payload.json` and preview `info.txt` into the same run folder.
11. Validate all rendered `info.txt` files.
12. Sample at least 2 final `info.txt` files for QA.
13. Write one short batch report.

## Information priority

When resolving identity or description conflicts, use this priority:
- online search
- Pass A driver-derived profile as surfaced in `02_profile_registry_compare.json`
- extracted registry comparison in `02_profile_registry_compare.json`

## Web search trigger policy

Web search is **not** triggered by script heuristics. Follow this logic strictly:

1. Pass A produces the device profile from driver evidence only.
2. The comparison script produces `02_profile_registry_compare.json`.
3. The agent compares the Pass A output with the registry entry by reading
   only `02_profile_registry_compare.json`.
4. If there is significant conflict or important fields are still empty, the
   agent triggers targeted web search.
5. Web search results refine `name`, `name_en`, `manufacturer`,
   `description`, and `description_en` in `02_device_profile_api.json`.
6. If manufacturer is still uncertain after web search, leave it empty rather
   than using placeholders like `Unknown`.

Registry reliability ranking:
- More reliable:
  - `class.action_value_mappings`
  - `class.module`
  - `class.status_types`
- Less reliable, treat with caution:
  - `description`
  - `device_params`
  - `manufacturer`
  - `model`
  - `name`
  - `category`
  - `tags`
  - `scene`

## Allowed device-specific inputs

The ONLY device-specific information you may read is:
- the side-by-side comparison artifact: `02_profile_registry_compare.json`
- optional web search result files created during this run
- collected tags in `_batch_tag_api.json`
- sampled final `info.txt`

Reading raw `registry.yaml` and `driver.py` is NOT allowed.
Reading the `driver` section of `01_local_signals.json` is NOT allowed.
Reading the `registry` section of `01_local_signals.json` directly is NOT allowed.
Reading full `02_device_profile_api.json` is NOT allowed.
Do not use prior production `info.txt` as context.

## Pass B guardrail

Pass B must use only the conflict-resolved `02_device_profile_api.json`.
Do not pass registry-derived fields directly into Pass B.
Registry and web findings are for agent-side conflict resolution only.

## Tagging expectations

- Encourage multiple relevant tags, not exactly one tag per type.
- `tag_hints` may be English or Chinese, but English is preferred.
- In tag objects, `name` should be Chinese-preferred and `name_en` should be English.
- Final device-entry `category` and `tags` should be Chinese string lists.
- These language preferences are enforced by prompt/QA, not by renderer
  heuristics.
- The combined set of `existing_tags` and `proposed_new_tags` must cover:
  - `experimental_step`
  - `experimental_domain`
  - `experimental_scene`
  - `device_template_tag`
- Prefer existing tags, but allow multiple proposals for:
  - `experimental_domain`
  - `experimental_scene`
  - `device_template_tag`

## Report

Write one short batch report that includes:
- devices processed
- what worked well (very concise)
- what still needs fixing
- proposed new tags, whether added or discarded
- 2 sampled final `info.txt` from the batch
- any prompt/script/workflow adjustments recommended before the next batch

## Output placement

Write all outputs into the assigned run folder only.
Keep any temporary analysis files in that run folder.

## Comparison discipline

Use the same benchmark scripts and same workflow steps as the other model runs.
Do not make model-specific prompt changes unless you document them clearly in the report.
