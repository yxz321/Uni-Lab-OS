# Phage Device Investigation And Driver-Staging Plan (Revised)

## 0. Context And Goal

The phage display library screening protocol (`_phage_protocol.md`) describes an 8-stage
wet-lab workflow from cell/phage prep through protein purification and validation.
The goal of this plan is to:

1. Determine which protocol functions can be served by **available** device drivers.
2. Identify functions requiring **unavailable** devices and recommend specific products.
3. Produce a final integrated report with per-function device recommendations.
4. For each unavailable suggested device, **dispatch a search agent**, wait for its
   evidence, then write a `driver_guessed.py` stub from that evidence.

---

## 1. Source Definitions (Non-Negotiable Throughout)

| Label | Path | Role |
|-------|------|------|
| Draft protocol | `community_drivers/_phage_protocol.md` | Workflow steps source. Copy to working folder for traceability. |
| Screenshot layout | (attached images in conversation) | Draft device suggestions only — **not** proof of availability. |
| Available CSV 1 | `community_drivers/_aggregate_device_info_existing.csv` | Available device inventory (equal weight with CSV 2). |
| Available CSV 2 | `community_drivers/_aggregate_device_info_output.csv` | Available device inventory (equal weight with CSV 1). |
| Repo drivers (community) | `community_drivers/<device>/` containing `registry.yaml`, `driver.py`, `info.txt` | Validation layer — search first, read targeted snippets only. |
| Repo drivers (existing infos) | `community_drivers/existing_device_infos/` | Additional info files for existing/packaged devices. |
| Repo drivers (unilab) | `unilabos/devices/` | Unilab built-in device implementations. |
| Repo drivers (packaged) | `packaged_drivers/` | Packaged community drivers. |
| Independent assessment | `community_drivers/_device_availability_assessment.md` | **Do not read until Step 6.** Used for reconciliation only. |
| Decorator reference | `unilabos/devices/virtual/workbench.py` lines 112-150, 293-310 | Canonical `@device`/`@action` pattern for `driver_guessed.py`. |
| Decorator source | `unilabos/registry/decorators.py` lines 237+ (device), 325+ (action) | Decorator implementation if decorator API details are needed. |
| Online universe | Full web search | Source for unavailable device product recommendations. **Must** use explicit web search; model knowledge alone is insufficient. |

### Access Rules

- **CSVs are large.** Never read them in full. Use `grep` / search on `name`, `name_en`,
  `description_en`, `categories`, `tags`, `atom_actions` columns. Merge hits by `registry_key` across both CSVs.
- **Repo driver directories** — search first (grep for keywords in `info.txt` or `registry.yaml`),
  then read only the matched file sections. Do not read entire `driver.py` files.
- **Write findings to intermediate markdown files** as you go. Do not re-open the same
  source files repeatedly. This is the primary context-control mechanism for this large task.

---

## 2. Working Folder And File Layout

Working folder: **`Uni-Lab-OS/drivers_phage/`** (create if not exists).

```
drivers_phage/
├── 00_project_rules.md                        # Shared rules repeated at top of every intermediate file
├── draft_inputs/
│   ├── _phage_protocol_draft_original.md      # Verbatim copy of community_drivers/_phage_protocol.md
│   └── layout_draft_from_screenshots.md       # Transcribed screenshot suggestions, labelled as DRAFT ONLY
├── 01_automation_first_workflow.md             # Normalized protocol with automation-first rewrites
├── 02_capability_bundles.md                    # Tier-0 bundles + per-function rows
├── 03_csv_search_notes.md                      # All CSV search results, merged across both files
├── 04_repo_driver_validation.md                # Targeted repo snippet findings
├── 05_independent_mapping.md                   # Full independent capability matrix and recommendations
├── 06_reconciliation.md                        # Diff with _device_availability_assessment.md
├── _phage_protocol_update.md                   # ★ FINAL REPORT
├── _agent_deep_search_prompt_template.md       # Reusable prompt template
├── <device_slug>/                              # One folder per unavailable suggested device
│   ├── prompt.md                               # Instantiated search prompt
│   ├── evidence.md                             # Agent-collected evidence summary
│   └── sources.json                            # URLs and references
└── (driver_guessed.py files go into community_drivers/<device_slug>/)
```

---

## 3. Step-by-Step Execution

### Step 1: Setup Working Folder And Copy Inputs

1. Create `drivers_phage/` and all subdirectories.
2. Copy `_phage_protocol.md` → `drivers_phage/draft_inputs/_phage_protocol_draft_original.md`.
3. Transcribe screenshot device/layout suggestions into `drivers_phage/draft_inputs/layout_draft_from_screenshots.md`. Label every item as "draft suggestion — not confirmed available."
4. Write `drivers_phage/00_project_rules.md` with these rules:
   - Automation-first: assay goals outrank draft layout; vessel format, step grouping, and module boundaries may change to improve automation.
   - Search-first access for all large files.
   - Both CSVs are equal availability sources.
   - Screenshot devices are draft suggestions only.
   - Unavailable recommendations require explicit web search verification.
   - Write findings to intermediate files; do not re-open sources.

### Step 2: Normalize Protocol Into Automation-First Workflow

1. Read `_phage_protocol.md` (already read above — 48 lines).
2. Write `drivers_phage/01_automation_first_workflow.md`:
   - Rewrite each protocol stage as an automation-friendly sequence.
   - Note where the draft protocol assumes manual steps or suboptimal vessel formats.
   - Allow regrouping steps or changing vessel types if it improves device availability and automation quality while preserving the assay goal.
   - This file becomes the authoritative function source for all subsequent steps.

### Step 3: Build Capability Bundles And Function List

1. **Read 20 lines** from `_aggregate_device_info_existing.csv` to calibrate the granularity of actions (what level of specificity the existing drivers use for action names).
2. Write `drivers_phage/02_capability_bundles.md` containing:
   - **Tier-0 Bundle Index** — group closely related functions that are normally served by one physical device. Sort so related bundles are adjacent. Bundles:
     1. Sample preparation and liquid handling (pipetting, mixing, transfer)
     2. Incubation, cooling, and shaking
     3. Centrifugation
     4. Sealing, unsealing, plate washing, bulk dispensing
     5. Fluorescent staining and flow cytometry (analysis + FACS sorting)
     6. Phage recovery: acid elution, infection, amplification
     7. Sterile filtration (0.22 um membrane)
     8. Colony picking and monoclonal screening
     9. ELISA plate reading
     10. Plasmid extraction and DNA sequencing
     11. Vector construction and transformation
     12. Protein expression, purification, and affinity/specificity validation
     13. Automation support: robot arms, plate transfer, storage, consumable handling
   - **Per-function rows** under each bundle — the specific actions the workflow needs, written at the same granularity as `atom_actions` observed in the CSV sample.

### Step 4: Search Available Devices (CSV Union + Repo Validation)

For each function row in the bundle list:

1. **Search both CSVs** using semantic keywords (not exact device names). Search columns: `name`, `name_en`, `description_en`, `categories`, `tags`, `atom_actions`. Record all hits in `drivers_phage/03_csv_search_notes.md`, noting which CSV each hit came from.

2. Only if CSV entry data appears weak or contradictory, **validate promising hits against repo sources.** For the top candidates from CSV search:
   - Search `community_drivers/<device>/info.txt` for the specific action/capability.
   - If needed, search `community_drivers/<device>/registry.yaml` to confirm action signatures.
   - Check `existing_device_infos/` for additional info on existing/packaged devices.
   - Check `unilabos/devices/` for built-in implementations.
   - Check `packaged_drivers/` if relevant.
   - Record findings in `drivers_phage/04_repo_driver_validation.md`.

3. **For functions where no available device is adequate**, use explicit **web search** to identify the best unavailable product. Criteria for "best" (ranked by importance):
   - **Function coverage** — covers all required actions for this bundle
   - **Online information richness** — manuals, documentation, specs publicly available
   - **Automation readiness** — has SDK, API, serial/TCP interface, or known driver ecosystem
   - **Product quality and reliability** — established vendor, good reviews

### Step 5: Independent Capability Mapping

Write `drivers_phage/05_independent_mapping.md` with:

1. **Per-function capability matrix** — one row per function, grouped by Tier-0 bundle. Columns:
   - Function name
   - Bundle group
   - Availability class: `(a)`, `(b)`, or `(c)` as defined below
   - Suggested device (registry_key or product name)
   - Alternatives
   - Notes

2. **Availability classification**:
   - **(a) Available and well-suited.** Multiple available devices may match; pick the one that is most reliable, best optimized for our purpose, and covers the most functions in its bundle without leaving actions hanging. List it as `suggest`, others as `alternatives`.
   - **(b) Available but outclassed.** An available device can partially cover the function, but a specific unavailable device would cover it materially better. List the unavailable device as `suggest`, available devices as `alternatives`.
   - **(c) No available device.** Pick the best unavailable device as `suggest`, other unavailable options as `alternatives`.

3. **Front summary table** — one row per Tier-0 bundle showing the suggested device, class, and whether a guessed driver is needed.

### Step 6: Reconciliation With Independent Assessment

1. **Now and only now**, read `community_drivers/_device_availability_assessment.md`.
2. Write `drivers_phage/06_reconciliation.md`:
   - Side-by-side comparison of the independent mapping (Step 5) vs the assessment file.
   - Note agreements, disagreements, and any devices or capabilities mentioned in one but not the other.
   - Where the assessment provides useful additional detail, fold it into the final recommendations.

### Step 7: Final Integrated Report

Write `drivers_phage/_phage_protocol_update.md`:

- **Section 1: Concise Summary Table** — one row per Tier-0 bundle, columns: Bundle, Suggested Device, Availability Class, Alternatives, Required Actions, Follow-Up Needed (guessed driver? deep search?).
- **Section 2: Protocol Overview** — the automation-first normalized workflow from Step 2, updated with final device assignments.
- **Section 3: Per-Bundle Analysis** — for each bundle, explain why the suggested device was chosen over alternatives, what functions it covers, and what gaps remain.
- **Section 4: Unavailable Devices Summary** — list of all `(b)`-suggested and `(c)`-suggested unavailable devices that need deep search and guessed drivers.

### Step 8: Deep Search Prompt Template And Per-Device Prompts

1. Write `drivers_phage/_agent_deep_search_prompt_template.md` containing a reusable prompt template with these placeholders:
   - `{device_name}` — the target device type
   - `{required_functions}` — the specific actions this device must serve in the phage workflow
   - `{bundle_context}` — which protocol stages use this device

   The template must instruct the search agent to find:
   - **Best specific product/model** — ranked by: function coverage > online info richness > automation readiness > quality/reliability
   - Official product pages and datasheets
   - Manuals (PDF links if available)
   - SDK / API / driver documentation / communication interface (serial, TCP, REST, etc.)
   - Expected processed outputs (what data the instrument returns to the automation system)
   - Physical dimensions and integration constraints
   - CAD/STL/STEP/xacro/URDF models for movable parts and interaction points, if available
   - Pricing ballpark if publicly available
   - Suitability assessment for the specific phage workflow actions listed in `{required_functions}`

   The template must instruct the agent to write its findings to:
   - `evidence.md` — structured summary
   - `sources.json` — list of URLs with titles

2. For **each unavailable suggested device** from Step 7 Section 4, instantiate the template into `drivers_phage/<device_slug>/prompt.md`.

### Step 9: Dispatch Deep Search Agents And Wait For Results

**This is a critical execution step, not just a planning note.**

For each unavailable suggested device:

1. Create the device subfolder `drivers_phage/<device_slug>/`.
2. Write the instantiated `prompt.md` from Step 8.
3. **Dispatch one GPT-5.4 Agent** (subagent_type: `general-purpose`) with the prompt content.
   - The agent prompt must include:
     - The full instantiated search prompt
     - Instruction to write `evidence.md` and `sources.json` into `drivers_phage/<device_slug>/`
     - The specific functions this device must serve
   - Run agents **in parallel** where possible (multiple Agent tool calls in one message).
4. **Wait for all agents to complete.** Change wait_agent timeout to 30 minutes as web search takes time. Do not proceed to Step 10 until every agent has returned its evidence.
   - If a shell command is quiet, keep polling the session until the process exits or a concrete failure is observed.
   - Do not interrupt quiet runs merely because they are silent.
   - Only react early to **concrete failures**: HTTP/API errors, explicit timeouts, schema failures, missing required output artifacts.
   - you are **NOT DONE** after dispatching agent or after agent complete, **DO NOT** emit task completion signal and continue with step 10.
5. Read each `evidence.md` to confirm the agent found substantive information.

### Step 10: Write Guessed Drivers From Agent Evidence

For each unavailable suggested device where no existing Uni-Lab-compatible driver was found:

1. Read `drivers_phage/<device_slug>/evidence.md` for the specific product, interface, and capabilities discovered.
2. Create `community_drivers/<device_slug>/driver_guessed.py` following this exact pattern:

```python
"""
Guessed driver for <DeviceName> — <one-line description>.
Generated from deep-search evidence; not tested against real hardware.
"""
from unilabos.registry.decorators import device, action

@device(
    id="<device_slug>",
    category=["<category>"],
    description="<description from evidence>",
)
class <DeviceClassName>:
    def __init__(self, device_id=None, config=None, **kwargs):
        self.device_id = device_id or "<device_slug>"
        self.config = config or {}

    @action()
    def <action_name>(self, <params with type hints>) -> dict:
        """<Docstring describing the desired function, specific to phage workflow.>"""
        print(f"[{self.device_id}] <Realistic log message describing what the device is doing>")
        return {"success": True}

    # ... one @action method per required function from the protocol ...
```

   **Key requirements for each guessed driver:**
   - Uses `@device` and `@action` decorators from `unilabos.registry.decorators` (NOT the legacy `registry.yaml` style).
   - Reference pattern: `unilabos/devices/virtual/workbench.py` lines 112-150 for `@device`, lines 293-310 for `@action` with handles.
   - Every action required by the phage workflow for this device must be present.
   - Action bodies contain only: a docstring describing the intended real behavior, and a `print()` with a realistic-looking log message. No actual implementation.
   - The `print()` messages should look like real instrument communication (e.g., `"[facs_sorter] Setting gate: FSC/SSC → PE channel, threshold=500 RFU"`, not `"[facs_sorter] TODO: implement sorting"`).
   - After all guessed drivers are written, run `python -c "import ast; ast.parse(open('<path>').read())"` on each to verify syntax.

### Step 11: Registry Scan Sanity Check

- Confirm that each `driver_guessed.py` file would be discovered by the `@device` decorator AST scanner by verifying:
  - The file imports `device` and `action` from `unilabos.registry.decorators`.
  - The `@device(...)` decorator is applied to a class.
  - Each `@action()` is applied to a method.
- Note: the file is named `driver_guessed.py` (not `driver.py`), which is intentional. Confirm in the decorator scanner source (`unilabos/registry/`) whether it scans all `*.py` files or only `driver.py`. If the latter, document this as a known limitation and note that renaming or adding a registry path entry may be needed.

---

## 4. Context Management Strategy

This task is large enough to overwhelm a context window. Mandatory mitigations:

1. **Write-as-you-go**: Every search result, repo finding, or web search outcome is written to the corresponding intermediate markdown file immediately. Do not accumulate findings in working memory.
2. **Search-first**: For CSVs, use grep/search with keywords. For repo files, search before reading. For web, use targeted queries not broad exploration.
3. **Parallel agents**: Deep search agents (Step 9) run in parallel to avoid serializing web research.
4. **Snippet reads**: When validating a device in the repo, read only the relevant 20-40 lines of `info.txt` or `registry.yaml`, not the whole file.
5. **Bundle-at-a-time**: Process the capability matrix one bundle at a time rather than loading all bundles simultaneously.

---

## 5. Test / Verification Checklist

- [ ] Both CSVs searched with equal weight; no hits privileged by source file.
- [ ] Screenshot device list used only as draft context, never as availability proof.
- [ ] Independent mapping covers every Tier-0 bundle and every function row.
- [ ] Reconciliation step clearly separates independent findings from assessment file findings.
- [ ] Every intermediate markdown starts with a reference to `00_project_rules.md`.
- [ ] Every unavailable suggested device has:
  - [ ] A dispatched agent that completed and returned evidence
  - [ ] `evidence.md` and `sources.json` in its subfolder
  - [ ] Web search was used (not just model knowledge)
- [ ] Every `driver_guessed.py`:
  - [ ] Passes `ast.parse()` syntax check
  - [ ] Uses `@device` and `@action` decorators
  - [ ] Exposes all actions required by the phage workflow for that device
  - [ ] Contains realistic `print()` log messages (not TODO stubs)
  - [ ] Models integrated instruments as single devices returning processed outputs
- [ ] Final report `_phage_protocol_update.md` has concise summary table before detailed analysis.
