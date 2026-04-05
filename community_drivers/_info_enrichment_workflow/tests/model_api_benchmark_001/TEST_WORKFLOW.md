# Test Workflow Design

Status:
- planning only
- do not dispatch agents yet

## Goal

Benchmark plain API models for semantic interpretation only.

This benchmark should stay close to the current production workflow `v3`.
We are not replacing the workflow wholesale; we are testing whether some
semantic substeps can be handed off from an agent to deterministic scripts plus
plain model API calls.

Deterministic/local steps:
- extract `info_raw.txt` from `driver.py` and `registry.yaml`
- manage device list, prompts, and output folders
- compare outputs side-by-side with scripts

LLM/API steps:
- stage 1: semantic interpretation from `info_raw.txt`
- optional stage 2: tag selection from a reduced shortlist

## Alignment with current production workflow

See:

- `CURRENT_WORKFLOW_TRACE.md`

Key alignment points:

- current production `v3` uses prompt-driven local evidence collection
- this benchmark replaces that first pass with deterministic `info_raw.txt`
- current production normally allows existing `info.txt` as context
- this benchmark intentionally excludes `info.txt` so we test raw-evidence
  interpretation only
- current production uses web search opportunistically for better descriptions
  and identity resolution
- this benchmark should start without web search in the API loop, then add it
  later only if needed

## Orchestrator

Planned orchestrator: `gpt-5.3-codex` worker agent.

Note:
- the request said `gpt-3.5-codex`, but the available orchestrator model in this environment is `gpt-5.3-codex`
- I am treating that as the intended orchestrator unless you want something else

## Selected benchmark devices

Prepared from devices that already passed through workflow v3:
- `bio_shake`
- `cool_led`
- `cryo_tel_gt`
- `cc_core`
- `cvd_control`
- `d435_rgb_stream`
- `cytomat_backend`

Coverage rationale:
- normal hardware device
- biology automation device
- identity-conflict device
- mixed-registry device
- service/stream wrapper
- sparse-action device

## Selected model range for API benchmarking

Recommended first-pass range along the cost/performance frontier:
- `gpt-5-nano`
- `gpt-5.4-nano`
- `gpt-5-mini`
- `gpt-5.4-mini`
- `gpt-5`

Why this range:
- all are visible to the current API key
- all are cheaper than `pro` models
- they span from very cheap extraction models to a high-quality anchor
- they are better fits for semantic interpretation than codex variants

## Stage outputs

Per model, per device:
- `outputs/<model>/<device>/semantic.json`
- optional `outputs/<model>/<device>/tags.json`
- optional merged `outputs/<model>/<device>/final_min.json`

Required minimum fields for stage 1:
- device
- description_en
- actions[].name
- actions[].description_en

Tags:
- disabled by default in the first benchmark
- reason: sending the full tag file on every call is wasteful and would confound the model-selection test
- optional second benchmark can add tags using a deterministic shortlist

## Summary generation

Use the local script:
- `scripts/summarize_model_outputs.py`

The summary markdown groups by device, then by field, and shows all model outputs side-by-side:
- device description
- each action description
- tags only if the optional tag stage is enabled

## Decision criteria

Primary:
- description quality
- action-description quality
- faithfulness to raw evidence
- stability / low hallucination
- cost

Secondary:
- output consistency across tricky devices
- whether the model is too terse or too rewrite-happy

## Discussion points before execution

1. Whether to keep tags disabled for the first benchmark
2. Whether 7 devices is the right test size, or shrink to 5 for faster iteration
3. Whether the top anchor should be `gpt-5` or `gpt-5.4`
