# Model API Benchmark 001: Final Report

## Scope

Workflow: `v4`

Devices:
- `bio_shake`
- `cryo_tel_gt`
- `cc_core`
- `cvd_control`
- `cytomat_backend`

Agent orchestrator:
- `gpt-5.3-codex`
- reasoning effort: `medium`

API models benchmarked:
- `gpt-5.4`
- `gpt-5.4-mini`
- `gpt-5.4-nano`
- `gpt-5.2-codex`
- reasoning effort: `medium`

## Validation status

- `gpt-5.4`: passed (`validated 5 files, no errors`)
- `gpt-5.2-codex`: passed (`validated 5 files, no errors`)
- `gpt-5.4-nano`: passed (`validated 5 files, no errors`)
- `gpt-5.4-mini`: failed on 3/5 devices
  - failure type: missing `device_template_tag` in final `tags`
  - root cause: the model put the template choice only in `proposed_new_tags`

## Estimated API cost for this 5-device batch

Based on official OpenAI pricing and measured token usage in the run artifacts.

- `gpt-5.4-nano`: about `$0.0395`
- `gpt-5.4-mini`: about `$0.1871`
- `gpt-5.2-codex`: about `$0.2490`
- `gpt-5.4`: about `$0.5528`

## Quality summary

### `gpt-5.4`
Strengths:
- best overall semantic quality
- strongest identity inference
- best handling of tricky devices like `cc_core`
- clean validation pass
- good bilingual descriptions with strong physical-device framing

Weaknesses:
- highest cost in this set
- still inherits ontology gaps such as mapping cryocoolers to freezer-like template tags when the tag catalog is weak

Best use:
- quality anchor
- small high-value batches
- difficult devices or adjudication runs

### `gpt-5.2-codex`
Strengths:
- best price/performance among the models that fully validated
- concise, stable action descriptions
- clean validation pass
- strong technical compression on control-oriented devices

Weaknesses:
- weaker on taxonomy conflicts
- `cc_core` still drifted into liquid-handling-style tagging because of registry priors
- less rich than `gpt-5.4` on descriptions

Best use:
- likely production default if cost matters but we still want reliable full-batch completion

### `gpt-5.4-mini`
Strengths:
- strong Pass A semantics
- attractive cost
- good device descriptions on straightforward devices

Weaknesses:
- failed validation on 3 devices
- more likely to propose a new template tag without also supplying a valid existing one in `tags`
- under the current workflow, this makes it less dependable for unattended production

Best use:
- only after tightening Pass B contract or adding deterministic promotion logic for proposed template tags

### `gpt-5.4-nano`
Strengths:
- by far the cheapest
- surprisingly decent device/action descriptions
- clean validation pass after script fixes

Weaknesses:
- weaker taxonomy alignment
- more likely to produce awkward tag/domain choices on tricky devices
- more variable manufacturer/identity quality

Best use:
- ultra-cheap exploratory runs
- maybe acceptable for Pass A-only experiments, not ideal for the full current workflow

## Recommendation

### Recommended quality anchor
- `gpt-5.4`

### Recommended production candidate under current workflow
- `gpt-5.2-codex`

Reason:
- It passed validation cleanly.
- It was much cheaper than `gpt-5.4`.
- It was materially more dependable than `gpt-5.4-mini` under the current Pass B/tag contract.
- It produced better semantics and better overall fit than `gpt-5.4-nano` on the tricky devices.

### Not recommended as current default
- `gpt-5.4-mini`
- `gpt-5.4-nano`

## Workflow notes from this benchmark

Issues fixed during the benchmark:
- isolated all outputs inside the benchmark folder
- replaced `info_raw.txt` flow with `01_local_signals.json`
- split sanitized API outputs from raw trace files
- fixed Responses API parsing to read message content, not just `output_text`
- fixed action-id mapping between Pass A method names and registry action ids

Important non-blocking workflow findings:
- validator command should use explicit file expansion rather than relying on shell wildcard passing in some contexts
- Pass B still needs better protection against stale registry taxonomy priors on devices like `cc_core`
- tag inventory still lacks ideal template coverage for cryocoolers and some controller/core devices

## Output artifacts

- side-by-side summary:
  - `reports/model_comparison.md`
- cost summary:
  - `reports/cost_summary.json`
- per-model run folders:
  - `runs/gpt-5.4/`
  - `runs/gpt-5.4-mini/`
  - `runs/gpt-5.4-nano/`
  - `runs/gpt-5.2-codex/`
