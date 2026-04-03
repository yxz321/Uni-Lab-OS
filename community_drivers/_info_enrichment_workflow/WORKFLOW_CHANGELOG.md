# Workflow Changelog

Versioning rule:

- During the prototype phase, use `prototype_vX.Y`.
- `schema_version` in generated `info.txt` should match this changelog version
  exactly.
- Example mapping: changelog `prototype_v0.3` <-> `schema_version:
  prototype_v0.3`

## prototype_v0.3

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

## prototype_v0.2

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
