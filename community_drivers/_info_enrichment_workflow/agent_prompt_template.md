# Device Info Enrichment Batch Prompt

You are working on a prototype batch for `community_drivers`.

## Scope

Only work on the devices listed in `devices.txt` and `manifest.json`.
Do not touch the full corpus.
Do not rely on `_device_capability_summary.csv` as a normal input; use the
device-local files and batch manifest as the source of truth.

## Goal

Improve `info.txt` for each device in this batch so that it is more useful for
downstream structured parsing and later device-space analysis.

Quality target: good enough and consistent with the accepted prototype
examples. Do not optimize for perfection at the expense of batch-scalable
throughput or honesty.

## Required pass order

1. Description extraction pass
2. Action summary pass
3. Driver function summary pass
4. Tag determination pass
5. Final formatting and validation pass

The description pass must happen before the tag pass. The extracted
description is one of the inputs for tag determination.

## Description rules

- Default to English.
- Prefer vendor/manual/web retrieval when it gives a materially better device
  description.
- Summarize what the device is and what it does in lab use.
- If web evidence is weak, infer from local signals:
  - registry metadata
  - driver docstrings
  - action names
  - function names and nearby code
- Avoid generic descriptions like "professional laboratory equipment".

## Tag rules

- Add all relevant existing tags supported by evidence.
- Prefer mitigating false negatives over false positives.
- Existing subject, domain, and scene tags are important and should be added
  when plausible from the evidence, not only when they are explicitly named in
  the registry.
- Use all available signals:
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
- If a useful tag appears to be missing from `tag 标签列表.csv`, do not add it
  automatically during prototype batches. Record it in the report with a short
  rationale.

## Action and function summary rules

- Prefer evidence in this order:
  - docstring
  - leading inline comment block attached to the method body
  - nearby code comments tied to the operation
  - method/action name plus parameters
- Compress the best available evidence into a few words.
- If only naming evidence is available, use a concise heuristic and do not make
  unsupported claims.
- Prefer short stable summaries over clever phrasing.
- Keep the structure easy to convert into JSON later.

For `driver_functions`, keep the section concise by default. Most semantic
detail should live in `atom_actions`. Only add richer function summaries when
they contribute evidence not already obvious from the action section or
signature.

## Formatting guidance

Keep `info.txt` readable and future-JSON-friendly. A YAML-like or labeled
section format is fine as long as the structure is consistent across devices.

Suggested sections:

- `device`
- `registry_key`
- `device_identity`
- `description`
- `description_evidence`
- `related_tags`
- `tag_evidence`
- `atom_actions`
- `driver_functions`
- `schema_version`
- `processing_pass_order`
- `stats`

For `atom_actions` and `driver_functions`, include:

- name
- short description
- parameters
- optional evidence source such as `docstring`, `code`, or `web`

## Report

Write one short batch report that includes:

- files changed
- what worked well
- what still needs fixing
- proposed new tags or tag gaps
- any prompt adjustments recommended before the next batch

## Constraints

- Do not revert unrelated changes.
- Do not edit devices outside this batch.
- Prefer concise English descriptions.
- Do not include a `categories` section in the final `info.txt`.
- Do not introduce a tag-confidence scoring system during this stage unless the
  batch explicitly asks for it.
