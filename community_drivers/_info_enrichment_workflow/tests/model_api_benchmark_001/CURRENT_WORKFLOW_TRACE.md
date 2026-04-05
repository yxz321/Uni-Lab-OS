# Current Production Workflow Trace

This note traces what the current production workflow `v3` actually uses so the
API-benchmark design stays aligned with it instead of drifting away.

## Source artifacts checked

- `_info_enrichment_workflow/README.md`
- `_info_enrichment_workflow/agent_prompt_template.md`
- `_info_enrichment_workflow/prepare_batch.py`
- `_info_enrichment_workflow/validate_info_txt.py`
- `_info_enrichment_workflow/batches/batch_019/agent_prompt.md`

## What local information the current workflow uses

The production agent is told that these are the normal local signals:

- `registry.yaml`
- `driver.py`
- current `info.txt`
- `tag 标签列表.csv`
- `tag_additions_proposed.csv`

From `registry.yaml`, the workflow explicitly treats these as useful signals:

- `category`
- `tags`
- `manufacturer`
- `model`
- `name`
- `description`
- `class.module`
- `class.action_value_mappings`

From `driver.py`, the workflow explicitly treats these as useful signals:

- AST-style function and method signatures
- docstrings
- nearby code comments
- module/class naming
- source-origin comments

The batch manifest also injects some precomputed metadata from
`_device_capability_summary.csv`:

- `current_categories`
- `current_tags`
- `action_count`
- `function_count`
- `current_short_description`

Important nuance:

- the prompt says device-local files are the source of truth
- but the batch manifest still carries summary-derived hints
- so the current workflow is not purely raw-file driven

## How that information is extracted today

The current production workflow does not have a dedicated checked-in
`info_raw.txt` extractor in the main workflow folder.

Instead, the production agent performs the "local evidence collection pass" by
reading the device-local files directly and summarizing them under prompt
control.

So today the extraction is mostly:

- prompt-defined
- agent-executed
- not normalized into one reusable intermediate file

That is exactly the gap this benchmark can help close.

For the benchmark test folder, `scripts/extract_info_raw.py` is an explicit
deterministic substitute for that first production pass. It currently extracts:

- selected top-level registry key
- sibling top-level registry keys
- registry metadata fields
- registry action mappings
- module docstring
- class names and bases
- class docstrings
- method names, lines, async flag, and signatures
- method docstrings
- leading comments immediately above methods
- top-level functions with the same fields

## Basis for tag assignment in the current workflow

Tag assignment is currently driven by prompt policy, not by a separate scoring
script.

The prompt tells the agent to:

- add all relevant existing tags supported by evidence
- prefer mitigating false negatives over false positives
- include subject, domain, and scene tags when plausible
- use all available signals together, including:
  - registry tags
  - registry category
  - name
  - model
  - manufacturer
  - module path
  - description
  - atom action names and summaries
  - driver function names and summaries
  - docstrings

The prompt also says:

- do not auto-add missing new tags during production
- record missing tags in the batch report instead
- do not use a tag-confidence scoring system at this stage

So the current tag logic is:

- recall-first
- prompt-guided
- evidence-aggregating
- human-reviewed between batches

## What prompts are the basis for tag assignment

The main basis is the production batch prompt itself:

- `_info_enrichment_workflow/agent_prompt_template.md`
- realized in each batch, for example:
  - `_info_enrichment_workflow/batches/batch_019/agent_prompt.md`

There is no separate standalone "tag prompt" in the production workflow yet.

## Web-search trigger logic in the current workflow

The current workflow does use web search, but the trigger is qualitative rather
than scripted.

The prompt says web retrieval is preferred when it gives a materially better
device description, especially for:

- weak or generic registry descriptions
- device-identity conflicts
- cases where vendor/manual pages can materially improve specificity

Web evidence is also part of the allowed evidence for identity overrides.

So in `v3`, web search is integrated mainly into:

- device identity pass
- description extraction pass

It is not currently a separate deterministic pass with a logged trigger file or
formal threshold.

## Category handling in the current workflow

Category is still used as an input signal, but not as a final output field.

Specifically:

- `registry.category` is available to the agent
- `current_categories` also appears in the batch manifest
- the prompt says category is redundant once richer descriptions and tags exist
- `validate_info_txt.py` explicitly rejects a top-level `categories` field

So there is no longer a category-assignment pass for final `info.txt`.

## What the benchmark should mirror vs intentionally change

What we should mirror:

- use registry metadata and action mappings
- use driver signatures, docstrings, and comments
- use the same pass ordering logic
- use the same recall-first semantics for capabilities
- preserve the same final minimal semantic targets:
  - device identity
  - description
  - action descriptions

What we should intentionally change:

- replace prompt-only local evidence collection with deterministic
  `info_raw.txt`
- exclude current `info.txt` from API context to avoid contamination from prior
  processed outputs
- keep tags out of the first API benchmark so we isolate semantic extraction
  quality first
- defer web search to a later phase or only trigger it on flagged cases
