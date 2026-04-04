# Benchmark 002: Model Switch Probe

Purpose:
- Evaluate `gpt-5.4-mini` vs `gpt-5.2-codex` as a production workflow-update decision.

Unseen benchmark devices:
- `dexarm`
- `dl3000`
- `driver_socket`

Why these three:
- `dexarm`: hardware automation / robotic arm profile
- `dl3000`: test-and-measurement instrument profile
- `driver_socket`: software/protocol abstraction profile

Rule:
- staged outputs only, no live device files touched
- compare structure, identity quality, description quality, action-summary quality, and tagging usefulness
