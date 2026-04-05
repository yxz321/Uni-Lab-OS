# Workflow v4: Operational Guide

## Pass order

```
1. extract_info_raw.py    →  01_local_signals.json     (script)
2. run_pass_a.py          →  02_device_profile_api.json (API, per device)
3. Agent conflict check   →  optional web search        (agent)
4. run_pass_b.py          →  _batch_tag_api.json        (API, per batch)
5. render_info_txt.py     →  03_enriched_payload.json + info.txt (script)
6. validate_info_txt.py   →  validation report          (script)
7. Agent QA               →  final review               (agent)
```

## Setup

Scripts are in
`_info_enrichment_workflow/tests/model_api_benchmark_001/scripts/`.

Outputs go to `_info_enrichment_workflow/outputs/<device>/`.

API credentials: `~/.config/unilabos/openai.env` with `OPENAI_API_KEY` and
optionally `OPENAI_BASE_URL`.

## Step 1: Local extraction

```bash
python3 scripts/extract_info_raw.py --devices-file devices.txt
```

Reads `registry.yaml` and `driver.py` per device. Produces
`01_local_signals.json` containing:

- Registry fields (category, module, status_types, tags, scene, actions)
- Driver AST (module docstring, all class names/bases/docstrings, focal-class
  methods with function_type and comments)

Focal class is identified from the last segment of `class.module` after `:`.
Each method is annotated as `status_getter`, `status_setter`, or `command`
by checking against `status_types`.

## Step 2: Per-device semantic profile

```bash
python3 scripts/run_pass_a.py --signals-dir ../../outputs
# Add --dry-run to write request payloads without calling API
# Add --model gpt-4o to change model (default: o4-mini)
```

Sends driver evidence only (no unreliable registry fields) to the API.
Returns: `name`, `name_en`, `manufacturer`, `description`, `description_en`,
per-action bilingual descriptions, `tag_hints`.

For `status_getter`/`status_setter` methods, the prompt instructs the model
to write simple "get/set <property>" descriptions.

## Step 3: Agent conflict check

Compare Pass A output with registry entry. If significant conflict between
LLM-derived and registry-derived identity (name, manufacturer, model), or if
combining both sources still leaves fields empty, trigger web search and
refine.

This step is agent-driven, not scripted.

## Step 4: Batch tag assignment

```bash
python3 scripts/run_pass_b.py --signals-dir ../../outputs
```

Loads the full tag list once. Sends per-device summaries (tag_hints, name,
description from Pass A + scene, module, tags, category from registry).

Requirements per device:
- >= 1 `experimental_step` tag (choose from existing only)
- >= 1 `experimental_domain` tag (choose from existing only)
- >= 1 `experimental_scene` tag (choose from existing only)
- >= 1 `device_template_tag` (may propose new if no existing tag fits)

Proposed new tags use id format `"P-xxxx"` and must be broad enough for
multiple real-world devices.

## Step 5: Merge and render

```bash
# Render to output dir for review
python3 scripts/render_info_txt.py --signals-dir ../../outputs

# Render to production community_drivers/<device>/info.txt
python3 scripts/render_info_txt.py --signals-dir ../../outputs --write-info-txt
```

Merges 01 + 02 + batch tags into `03_enriched_payload.json`, then renders
`info.txt` YAML.

## Step 6: Validate

```bash
python3 ../../validate_info_txt.py ../../outputs/*/info.txt
```

Checks:
- Two top-level keys: `<device_key>` and `auto_annotation_metadata`
- Device entry has: name, name_en, manufacturer, category, tags, description,
  description_en, class
- Tags in device entry is a list of Chinese name strings
- Each action has `schema.description`
- Metadata has: registry_key, annotation_workflow_version, tag_hints, tags,
  processing_pass_order
- Full tags cover all 4 required types

## Step 7: Agent QA

Review proposed new tags:

```bash
python3 scripts/collect_proposed_tags.py --signals-dir ../../outputs
```

This prints all proposed new tags with their rationale and which devices
triggered them. The agent reviews each:

- If it makes sense, run with `--append` to add to `tag_additions_proposed.csv`
- If it doesn't make sense, note why and skip

```bash
# After review, append accepted tags
python3 scripts/collect_proposed_tags.py --signals-dir ../../outputs --append
```

Then review a sample of rendered info.txt files across the batch. Check:
- Description quality and accuracy
- Tag coverage and relevance
- Action description quality
- Proposed new tags validity

## info.txt structure

```yaml
<device_key>:
  name: <Chinese name>
  name_en: <English name>
  manufacturer: <manufacturer>
  category:          # from registry.yaml, as-is
    - <category>
  tags:              # short Chinese names from assigned tags
    - <tag_name_cn>
  description: <Chinese description>
  description_en: <English description>
  class:
    action_value_mappings:
      <action_name>:
        schema:
          description: <Chinese action description>
          description_en: <English action description>

auto_annotation_metadata:
  registry_key: <device_key>
  annotation_workflow_version: v4
  tag_hints:
    - <keyword phrase>
  tags:              # full tag objects with rationale
    - id: "<tag_id>"
      name: <Chinese name>
      name_en: <English name>
      type: <experimental_step|experimental_domain|experimental_scene|device_template_tag>
      rationale: <why this tag was assigned>
  proposed_new_tags: # same structure as tags, id like "P-xxxx"
    - id: "P-xxxx"
      name: <Chinese name>
      name_en: <English name>
      type: device_template_tag
      rationale: <why this tag is needed>
  websearch_evidence:
    used: <true|false>
    findings: []
  processing_pass_order:
    - deterministic_local_extraction
    - per_device_semantic_profile
    - agent_conflict_check_and_web_search
    - batch_tag_pass
    - payload_merge
    - render_info_txt
    - validate_and_review
```

## Artifact layout

```
_info_enrichment_workflow/
  outputs/
    <device>/
      01_local_signals.json        (Step 1)
      02_device_profile_api.json   (Step 2)
      _batch_tag_api.json          (Step 4)
      03_enriched_payload.json     (Step 5)
      info.txt                     (Step 5, preview)
```

## Key design decisions

- **Only driver evidence goes to Pass A.** Unreliable registry fields (name,
  description, manufacturer, model) are excluded to avoid biasing the LLM.
- **Tags are batch-level.** The tag list is sent once per batch, not per
  device. This saves tokens and improves cross-device consistency.
- **Category is passthrough.** Pulled from registry.yaml, not assigned by LLM.
- **Web search is agent-triggered.** No script heuristics. The agent compares
  Pass A output with registry and decides.
- **Function types guide descriptions.** `status_getter`/`status_setter`
  methods get simple "get/set <property>" descriptions. `command` methods get
  richer descriptions.
