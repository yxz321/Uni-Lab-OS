# Model Selection Notes

Scope:
- plain API models for semantic interpretation of `info_raw.txt`
- not agentic orchestration models
- avoid `pro` tier models for cost reasons

## Official sources used

- GPT-5 pricing + benchmarks:
  - https://openai.com/index/introducing-gpt-5-for-developers/
- GPT-5.4 mini/nano pricing + benchmarks:
  - https://openai.com/index/introducing-gpt-5-4-mini-and-nano/
- current API pricing page:
  - https://openai.com/api/pricing/

## Selected candidate range

Recommended first-pass benchmark range:
- `gpt-5-nano`
- `gpt-5.4-nano`
- `gpt-5-mini`
- `gpt-5.4-mini`
- `gpt-5`

Rationale:
- all are visible to the current API key
- all are non-pro models
- they span a wide cost range without jumping straight to the most expensive options
- they are general reasoning/instruction models, which better match semantic interpretation than codex-specialized models

## Current price snapshot

| model | input / 1M | cached input / 1M | output / 1M | source |
|---|---:|---:|---:|---|
| gpt-5 | $1.25 | $0.125 | $10.00 | GPT-5 for developers |
| gpt-5-mini | $0.25 | not noted in article | $2.00 | GPT-5 for developers |
| gpt-5-nano | $0.05 | not noted in article | $0.40 | GPT-5 for developers |
| gpt-5.4-mini | $0.75 | $0.075 | $4.50 | API pricing / GPT-5.4 mini+nano |
| gpt-5.4-nano | $0.20 | $0.02 | $1.25 | API pricing / GPT-5.4 mini+nano |

Notes:
- the GPT-5 article explicitly lists prices for `gpt-5`, `gpt-5-mini`, and `gpt-5-nano`
- the current pricing page explicitly lists prices for `gpt-5.4-mini` and `gpt-5.4-nano`

## Relevant official benchmark signals

These are not task-identical, but they are the most relevant public proxies for our semantic interpretation workload:
- instruction following
- long-context reasoning
- factual reliability / low hallucination
- general reasoning on technical material

### GPT-5 family signals
From the GPT-5 for developers page:
- GPQA Diamond: `gpt-5 85.7`, `gpt-5-mini 82.3`, `gpt-5-nano 71.2`
- Internal API instruction-following eval (hard): `gpt-5 64.0`, `gpt-5-mini 65.8`, `gpt-5-nano 56.1`
- OpenAI MRCR 2-needle 128k: `gpt-5 95.2`, `gpt-5-mini 84.3`, `gpt-5-nano 43.2`
- LongFact / FActScore hallucination rates are also low for GPT-5 and GPT-5 mini, and worse for GPT-5 nano

### GPT-5.4 mini/nano signals
From the GPT-5.4 mini and nano page:
- GPQA Diamond: `gpt-5.4-mini 88.0`, `gpt-5.4-nano 82.8`
- HLE without tools: `gpt-5.4-mini 28.2`, `gpt-5.4-nano 24.3`
- OpenAI MRCR v2 64k-128k: `gpt-5.4-mini 47.7`, `gpt-5.4-nano 44.2`
- OpenAI recommends `gpt-5.4-nano` for classification, data extraction, and ranking
- OpenAI describes `gpt-5.4-mini` as the strongest mini model yet

## Estimated fit for our task

Our task is mostly:
- read moderately long structured evidence
- resolve identity conflicts
- compress action semantics faithfully
- stay literal and avoid hallucination
- return short JSON

Estimated quality ranking for this task:
1. `gpt-5`
2. `gpt-5.4-mini`
3. `gpt-5-mini`
4. `gpt-5.4-nano`
5. `gpt-5-nano`

Estimated cost-performance ranking:
1. `gpt-5.4-mini`
2. `gpt-5-mini`
3. `gpt-5.4-nano`
4. `gpt-5`
5. `gpt-5-nano`

Interpretation:
- `gpt-5.4-mini` is the most likely sweet spot if quality matters more than absolute lowest cost.
- `gpt-5-mini` may be surprisingly competitive because our task depends a lot on instruction following and long structured context.
- `gpt-5.4-nano` is especially interesting if we want cheap extraction/classification and are willing to accept weaker long-context handling.
- `gpt-5-nano` is worth testing only as a floor/baseline.
- `gpt-5` is the quality anchor, not the expected production default.

## Recommendation before running the benchmark

Use the 5-model range above, but keep tags disabled in the first pass so the benchmark isolates:
- description quality
- action-summary quality
- identity handling
- raw evidence faithfulness

Then, if one or two models look strong, run a second smaller benchmark with an optional tag-shortlist stage.
