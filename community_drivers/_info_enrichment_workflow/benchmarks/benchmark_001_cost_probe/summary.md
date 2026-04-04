# Benchmark 001 Summary

Devices:
- `bio_shake`
- `cc_core`

Baseline:
- existing production `gpt-5.3` outputs (`gold/`)

Tested cheaper candidates:
- `gpt-5.4-mini`
- `gpt-5.1-codex-mini`
- `gpt-5.2-codex`

Caveat:
- This is a staged benchmark on already-processed devices, so it measures practical replacement behavior in the current workflow, not fully blind first-pass generation.

## Result

### 1. gpt-5.4-mini
- Validator: pass
- Quality: closest to production `gpt-5.3`
- Drift from gold: extremely low
- Identity handling: correct on `cc_core`
- Recommendation: best drop-in cheaper replacement from this test

### 2. gpt-5.2-codex
- Validator: pass
- Quality: often richer than baseline on action summaries
- Drift from gold: high
- Identity handling: correct on `cc_core`
- Recommendation: strongest alternative if we want more proactive code-grounded summaries and can tolerate more variation

### 3. gpt-5.1-codex-mini
- Validator: pass
- Quality: viable, but tends to be more verbose and more inferential than desired for stable large-scale metadata
- Drift from gold: moderate
- Identity handling: correct on `cc_core`
- Recommendation: acceptable budget option, but less consistent than `gpt-5.4-mini`

## Quantitative comparison

| model | validator | bio_shake drift vs gold | cc_core drift vs gold | total drift | note |
|---|---|---:|---:|---:|---|
| gpt-5.4-mini | pass | 2 | 0 | 2 | Near-identical to production baseline |
| gpt-5.1-codex-mini | pass | 70 | 23 | 93 | More verbose, more rewritten phrasing |
| gpt-5.2-codex | pass | 73 | 265 | 338 | Most proactive rewrite behavior |

## Practical recommendation

- For production replacement or parallel help on this workflow: use `gpt-5.4-mini` first.
- If later we want a second lane optimized for richer action summaries on harder devices, `gpt-5.2-codex` is worth a targeted trial on a fresh unseen batch.
- `gpt-5.1-codex-mini` is usable, but not my first choice for metadata stability.
