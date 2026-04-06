# Workflow Changelog

Versioning rule:

- Historical prototype versions use `prototype_vX.Y`.
- Major production versions use `vN`.
- Generated `info.txt` should carry the active workflow version exactly in
  `auto_annotation_metadata.annotation_workflow_version`.
- Because `_info_enrichment_workflow/batches/` already contains historical
  production batches, the new major `v4` rerun uses `v4_batch_###` naming to
  avoid ambiguity.

## v4

- Promoted the benchmark-proven `v4` workflow into the real production layout.
- `info.txt` structure changed materially from `v3`, so all devices must be
  rerun under `v4`.
- Added the two-agent production split:
  - main orchestrator: `GPT-5.4`
  - device-reasoning subagents: `gpt-5.3-codex`
  - semantic API default: `Vendor2/GPT-5.4`
- Moved production source-of-truth scripts and prompts into:
  - `_info_enrichment_workflow/workflow_v4/`
- Kept all batch-local artifacts under:
  - `_info_enrichment_workflow/batches/<batch_id>/`
- Final rendered output now writes directly to:
  - `community_drivers/<device>/info.txt`
- Duplicated `validate_info_txt.py` into `workflow_v4/` because workflow
  structure can evolve across major versions.
- Increased Pass A / Pass B request timeout to `240s`.
- Kept the `v4` semantic boundary intact:
  - scripts do deterministic extraction, transport compatibility, merge/render,
    and structural validation only
  - scripts do not perform semantic repair
  - schema drift is a batch failure with preserved traces
- Clarified the strict web-search trigger flow:
  - Pass A derives the profile from driver evidence
  - compare script produces side-by-side five-field comparison
  - agent decides whether to web search by reading only that compare artifact
  - web findings refine only the five identity/description fields in `02`
- Clarified autonomous continuation rules:
  - append next-cycle TODOs before waiting, before dispatching the next normal
    batch, and before entering workflow-update mode
- Promotion defaults:
  - verification batch size: `2`
  - normal production batch size: `10`
  - reasoning effort: `medium`

## v3

- Promoted the validated identity-conflict fix into the active production
  workflow.
- `device_identity` may now override registry manufacturer/model/name when the
  registry is clearly contradicted by stronger driver or web evidence.
- Added optional `registry_identity_conflict` trace metadata after
  `description_evidence` to document registry-vs-chosen identity differences.
- Kept the output structure backward-compatible while improving identity
  fidelity on noisy registry entries.
- Validation trigger set:
  - `blockly_tool` from `batch_010`
  - `bio_tek_plate_reader_backend` from `batch_010`
  - `cc_core` from `batch_013`

## v2

- Promoted the validated description-generation fix into the active production
  workflow.
- Active workflow now writes descriptions after action and driver summaries.
- Added a description quality floor: final description must not be worse than
  the best readable local source.
- Explicitly prefer device-first wording over software-wrapper wording such as
  `backend`.
- Batch reports should now include sampled final descriptions and sampled
  action/function summaries for review.
- Clarified that trigger-device validation runs may advance a few devices ahead
  of the main production queue.
- Added guidance to prefer temp/staged outputs during policy-update validation
  runs, replacing the live file only when the new result is visibly better.
- Clarified that scaling decisions must consider validator status, agent
  feedback, and manual sampled review together; validator PASS alone does not
  define batch success.

## v1

- Promoted the approved prototype workflow into production naming.
- Production outputs should now use `schema_version: v1`.
- Production batches should use `batch_###` naming instead of
  `prototype_batch_###`.
- Prototype entries below are retained only as historical development record.

## Historical prototype lineage

### prototype_v0.3

- Added explicit summary evidence priority:
  - docstring
  - leading inline comment block
  - nearby code comments
  - name plus parameters heuristic
- Clarified that name-only fallback is acceptable when no better source exists,
  but unsupported semantics must not be invented.
- Documented that `driver_functions` can stay concise by default because
  `atom_actions` usually carry the richer exposed semantics.
- Added a recommendation for a lightweight structural schema validator.
- Explicitly chose not to add a tag-confidence scoring system at this stage.

### prototype_v0.2

- Reordered the recommended pass sequence to:
  - description extraction
  - atom action summary
  - driver function summary
  - tag determination
  - final formatting and validation
- Clarified that description extraction is an independent first pass.
- Changed tag policy to prefer higher recall over stricter precision.
- Explicitly encouraged assignment of subject, domain, and scene tags when
  plausible from the evidence.
- Removed `categories` from the preferred final `info.txt` layout.
- Moved `schema_version` and `processing_pass_order` to later positions in the
  preferred `info.txt` structure.
- Demoted `_device_capability_summary.csv` from normal workflow context to an
  optional debug or batch-preparation artifact.
- Documented that full-scale execution should wait until prototype batches are
  reviewed and approved.
