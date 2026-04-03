# Device Info Enrichment Workflow

This folder documents the reusable batch workflow for improving `info.txt`
files in `community_drivers`.

This workflow is for iterative prototyping first. Do not start full-scale
execution until the current prompt, format, and review loop have been approved
from small consecutive batches.

## Design principle

This is a large-scale enrichment task. The goal is useful, consistent, and
honest metadata, not perfection.

- A quality level comparable to the current accepted prototypes is good enough.
- Do not over-invest in polishing individual devices beyond the level needed to
  keep the corpus broadly useful.
- Prefer steady batch throughput and consistent rules over isolated
  high-effort edits.

## Why batches

The full corpus is large enough that enrichment quality should be validated in
small consecutive batches. After each batch, review:

- description quality
- tag assignment quality
- action/function summary quality
- formatting stability
- missing tag proposals

Then update the prompt or extraction rules before running the next batch.

The prompt and extraction rules should therefore be versioned and written to
this folder, alongside a changelog documenting:

- workflow version
- changes
- batch or devices processed under that version
- lessons learned

## Recommended workflow

1. Generate a batch manifest and agent prompt with `prepare_batch.py`.
2. Dispatch one agent for that batch only.
3. Review the changed `info.txt` files and the agent report.
4. Adjust the prompt/template/rules if needed.
5. Move on to the next batch.

If a workflow rule is changed because of a concrete device-level issue, rerun
the device or small batch that triggered the change and only keep the workflow
update if it produces a visible improvement.

## Pass order

Each batch should follow this order:

1. Description extraction pass
2. Atom action summary pass
3. Driver function summary pass
4. Tag determination pass
5. Final formatting and validation pass

Why this order:

- Description remains an independent first pass.
- Tagging should happen after action and function summaries, because those
  summaries often expose device semantics more clearly than raw method names.
- The extracted description is therefore one input to tag determination, not
  the only semantic input.

## Description pass

For each device, first extract a better English description by combining:

- metadata collection from local files
- search-and-infer using web search plus semantic summarization when helpful
- fallback inference from local evidence when web evidence is weak

Avoid generic descriptions like "professional laboratory equipment".

## Summary extraction priority

When summarizing atom actions or driver functions, prefer real evidence in this
order:

1. docstring
2. leading inline comment block attached to the method body
3. nearby code comments tied to the operation
4. method or action name plus parameters

If the only usable evidence is the name and parameters, it is acceptable to
fall back to a concise naming heuristic. Do not invent semantics that are not
supported by source evidence.

## Local signals available to the agent

- `registry.yaml`: category, tags, manufacturer, model, name, description
- `driver.py`: AST signatures, docstrings, nearby code comments
- current `info.txt`
- `tag 标签列表.csv`
- `tag_additions_proposed.csv`

## Optional debug artifacts

These are useful for batch preparation, QA, or corpus-wide diagnostics, but
they should not be treated as normal agent context during enrichment:

- `_device_capability_summary.csv`
- `_unmatched_categories_for_tags.csv`

## Tagging policy

- Assign multiple related tags when supported by evidence.
- Use all available signals:
  - registry tags
  - registry category
  - name
  - model
  - manufacturer
  - module path
  - extracted description
  - atom action names and summaries
  - driver function names and summaries
  - docstrings
- Prefer mitigating false negatives over false positives.
- It is acceptable if a few devices receive slightly broader tags than needed.
- Prioritize discoverability: users should be able to find devices by device
  type, subject/domain, and scene when the evidence is at least plausible.
- Existing subject/domain/scene tags in `tag 标签列表.csv` should be considered
  alongside device-template tags, not treated as optional extras.

`category` is still a useful input signal, but it should not be emitted as a
top-level section in the final `info.txt` because it is redundant once richer
tags and descriptions are present.

At this stage, explicit tag-confidence scoring is not required. The current
policy is recall-first tagging with human review between batches.

## Output expectations

- improved `info.txt` for the selected devices only
- one short report describing:
  - what worked
  - what still looks weak
  - proposed new tags or tagging gaps

## Preferred `info.txt` layout

Keep device identity and description first for readability. Put workflow
metadata later in the file.

Recommended section order:

1. `device`
2. `registry_key`
3. `device_identity`
4. `description`
5. `description_evidence`
6. `related_tags`
7. `tag_evidence`
8. `atom_actions`
9. `driver_functions`
10. `schema_version`
11. `processing_pass_order`
12. `stats`

Do not include a `categories` section in the final `info.txt`.

## Driver section redundancy

`registry.yaml` and `driver.py` are complementary, not interchangeable:

- `registry.yaml` describes the exposed device interface, metadata, and atom
  actions.
- `driver.py` provides implementation details, hidden helpers, docstrings, and
  operational comments.

For the final `info.txt`, the `atom_actions` section should carry most of the
semantic detail because it is closest to the exposed action space.

The `driver_functions` section can stay concise by default. A compact format is
preferred, especially when the function is already represented by an atom
action. For example:

```text
Driver Functions (16):
- IncubatorShakerStack.__init__(self, backend) (line 85)
- IncubatorShakerStack.num_units(self) (line 102)
- IncubatorShakerStack.setup(self, **backend_kwargs) [async] (line 145)
- IncubatorShakerStack.stop(self) [async] (line 195)
```

Only add richer function summaries when they provide extra evidence that is not
already obvious from the atom-action section or signature.

## Lightweight validator

A lightweight schema validator is recommended before scaling, but it should
only enforce structure, not meaning. It should check things like:

- required top-level sections exist
- `device` and description-related sections appear first
- `categories` is absent
- `related_tags` entries have the expected keys
- `atom_actions` entries have basic required fields
- `driver_functions` entries have basic required fields
- `schema_version` and `processing_pass_order` are present

This keeps the format stable without adding a high-overhead quality-scoring
system.

## Notes on new tags

Do not automatically edit `tag 标签列表.csv` during early prototype batches
unless the review explicitly approves it. During prototyping, record proposed
tags in the batch report first. After prototyping, stage new tags first in
`tag_additions_proposed.csv` rather than directly mutating `tag 标签列表.csv`,
but with the same format and compatible IDs to allow easy future merge.

## Versioning convention

Use an explicit `prototype_vX.Y` naming scheme during the prototype phase.

- `schema_version` in `info.txt` should match the workflow changelog version
  one-to-one.
- The changelog should use the same exact version string.
- Example: if the active workflow version is `prototype_v0.4`, then newly
  generated `info.txt` files should use `schema_version: prototype_v0.4`.

This avoids ambiguity about whether the leading `0` means prototype status.
