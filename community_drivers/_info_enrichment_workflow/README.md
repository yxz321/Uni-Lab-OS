# Device Info Enrichment Workflow

This folder documents the reusable batch workflow for improving `info.txt`
files in `community_drivers`.

The prototype phase has been completed. The active workflow below is now the
approved production workflow for batch-by-batch execution.

Current active workflow/schema version: `v3`

## Local API secret setup

If we use plain model API calls for semantic substeps, keep credentials outside
the repo and prefer the OS keyring.

Recommended keyring entry:

- service: `unilabos-openai`
- username: `default`

Store it locally with:

```bash
keyring set unilabos-openai default
```

A lightweight connectivity helper is available at:

- `community_drivers/_info_enrichment_workflow/test_openai_api.py`

It reads credentials from the current environment first, then falls back to the
OS keyring.

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

In autonomous production mode, a workflow update is part of the loop, not the
end of the loop:

- if review triggers a workflow update, enter the workflow-update cycle
- validate the candidate on trigger devices
- adopt the update only if the result is visibly better
- then immediately append the next production tasks and continue at reduced
  parallelism until the new workflow proves stable
- do not wait for additional user approval after a validated workflow update
  unless the change has unusual risk beyond the normal batch policy

If a workflow rule is changed because of a concrete device-level issue, rerun
the device or small batch that triggered the change and only keep the workflow
update if it produces a visible improvement.

Those trigger devices may therefore advance to a newer workflow version earlier
than the main batch queue. That is acceptable, as long as the batch queue still
continues in strict order for normal production processing.

## Success criteria for scaling

A batch counts as successful only if all of the following are true:

- the lightweight validator passes
- the agent report does not surface a blocking or workflow-changing issue
- sampled descriptions look readable and device-first
- sampled action/function summaries are acceptable for the current quality bar
- my own review does not identify a workflow change that should be made before
  continuing

Passing validation alone is not enough.

If a review suggests a workflow change, enter the workflow-update cycle and
reset the scaling success streak after the change is adopted.

## Pass order

Each batch should follow this order:

1. Local evidence collection pass
2. Atom action summary pass
3. Driver function summary pass
4. Description extraction pass
5. Tag determination pass
6. Final formatting and validation pass

Why this order:

- Local evidence collection still happens first.
- Description should be written after action and function summaries, because
  those summaries often expose device semantics more clearly than raw metadata.
- Tagging should happen after action and function summaries, because those
  summaries often expose device semantics more clearly than raw method names.
- The extracted description is therefore one input to tag determination, not
  the only semantic input.

## Device identity pass

`device_identity` should usually start from registry metadata, but it does not
have to remain registry-bound when the registry is clearly wrong.

Identity rules:

- Prefer registry manufacturer/model/name when they are broadly consistent with
  driver module, docstrings, actions, and web evidence.
- If registry identity is clearly contradicted by stronger evidence, override
  `device_identity` with the corrected identity.
- Stronger evidence can include:
  - driver module/class naming
  - class docstrings
  - source-origin comments
  - action surface that clearly matches another device family
  - vendor/manual/product pages
- If identity is overridden, add an optional
  `registry_identity_conflict` section after `description_evidence` to preserve
  traceability.
- Keep the conflict note concise. It should capture the registry identity,
  chosen identity, and a short rationale.

## Description pass

For each device, extract a better English description by combining:

- metadata collection from local files
- search-and-infer using web search plus semantic summarization when helpful
- fallback inference from local evidence when web evidence is weak

Avoid generic descriptions like "professional laboratory equipment".

Description rules:

- Describe the device first, not the software wrapper.
- Avoid phrasing like `device backend` or `pump-control backend` unless that is
  genuinely the most accurate device identity available.
- The final description should be at least as readable and specific as the best
  local source available.
- Do not let an action-list heuristic produce a description worse than
  `registry.description`.
- If local evidence is sparse, prefer a short plain device description over a
  verbose pseudo-summary built from action names.

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

## Policy-update validation runs

When testing a workflow change on trigger devices:

- prefer writing candidate outputs to temp or staged files first
- compare old vs new result
- only replace the live `info.txt` if the new workflow produces a visible
  improvement

This helps avoid keeping weaker outputs from experimental policy changes.

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
  - sampled final descriptions
  - sampled action or function summaries for review

## Preferred `info.txt` layout

Keep device identity and description first for readability. Put workflow
metadata later in the file.

Recommended section order:

1. `device`
2. `registry_key`
3. `device_identity`
4. `description`
5. `description_evidence`
6. optional `registry_identity_conflict`
7. `related_tags`
8. `tag_evidence`
9. `atom_actions`
10. `driver_functions`
11. `schema_version`
12. `processing_pass_order`
13. `stats`

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

## Identity conflict handling

When a device lands in the wrong product family because of noisy registry
metadata, it is better to emit the corrected identity than to preserve a
misleading one.

Examples of valid overrides:

- spectroscopy instrument registry text on a robotics Blockly tool
- flow-cytometer registry text on a microplate-reader backend
- pipette registry text on a quantum-control controller

This is a meaningful workflow improvement, not perfectionist cleanup. The goal
is to prevent obviously wrong `device_identity` fields from propagating through
the corpus.

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

The prototype phase and the production phase must stay clearly separated.

- Historical prototype versions use `prototype_vX.Y`.
- Active production versions use `vN`.
- `schema_version` in `info.txt` should match the active workflow changelog
  version one-to-one.
- Batch folders in production should use names like `batch_001`,
  `batch_002`, and so on.

Example:

- historical prototype run: `prototype_v0.3`
- current production workflow: `v2`
- current production batch: `batch_001`
