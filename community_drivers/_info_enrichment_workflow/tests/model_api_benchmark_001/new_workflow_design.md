# New Workflow Design: `v4`

## Updated goal

The enrichment workflow should produce:

1. a human-scannable, valid-YAML `info.txt`
2. per-device deterministic intermediate artifacts
3. raw Responses API request/response traces
4. enough structured output to update the current registry YAML shape with
   little or no manual re-parsing

The final outputs should support both:

- the current registry generation logic in `Uni-Lab-OS/generate_community_yamls.py`
- future downstream uses that want bilingual metadata, action semantics, and
  evidence traces

## Key downstream findings

### 1. What the current YAML generator actually needs

`Uni-Lab-OS/generate_community_yamls.py` reads:

- public methods from `community_drivers/<device>/driver.py`
- the matching entry from `community_drivers/<device>/registry.yaml`
- then writes normalized YAML entries like
  `unilabos/registry/devices/community_ba_<folder>.yaml`

Relevant fields it carries or writes:

- `name`
- `category`
- `description`
- `manufacturer`
- `model`
- `tags`
- `scene`
- `device_params`
- `init_param_schema`
- `class.action_value_mappings`
- `class.module`
- `class.status_types`

So the new `info.txt` should stay close to this shape.

### 2. Focal class identification

The enrichment workflow anchors on the **focal class** from the registry
`module` field (the segment after `:`, e.g. `CryoTelGT` from
`unilabos.devices.cryocooler.sunpower_cryotel_gt_cryocooler:CryoTelGT`).

Only focal-class methods are extracted with full detail. If `module` is
missing, the first class in `driver.py` is used as fallback.

### 3. Registry field reliability

**More reliable** (use directly): `category`, `class.action_value_mappings`,
`class.module`, `tags`, `scene`, `class.status_types`

**Less reliable** (treat with caution): `description`, `device_params`,
`manufacturer`, `model`, `name`

The enrichment workflow derives less-reliable fields from driver evidence via
LLM, not from registry.

### 4. Function type annotation

Each focal-class method is annotated as `status_getter`, `status_setter`, or
`command` by checking if the method name (with `get_`/`set_` prefix stripped)
appears in `status_types`. This helps the LLM generate appropriate
descriptions.

## Category handling

Category is pulled from `registry.yaml` as-is. The enrichment workflow does
**not** attempt to assign, improve, or validate category values.

## Tag system design

### Tag types and requirements

Each device must have at least one tag from each of these four types:

- `experimental_step` (6 available, do not propose new ones)
- `experimental_domain` (9 available)
- `experimental_scene` (38 available)
- `device_template_tag` (63 available, may propose new ones)

This is because the downstream panorama view lists `device_template_tag`
values in a grid of `experimental_scene` (grouped under `experimental_domain`)
crossed with `experimental_step`.

### Tag assignment strategy: hybrid with enrichment (Option C)

**Pass A (per-device API call):** produces `tag_hints` — a relevance-sorted
list of keyword phrases. Kept in `info.txt` throughout.

**Pass B (batch-level API call):** receives per-device `tag_hints`, `name`,
`description` from info.txt, plus `scene`, `module`, `tags`, `category` from
registry, plus the full tag list once. Outputs final tags per device.

### New tag proposals

Proposed new tags must be `device_template_tag` type only. A proposed tag must
be broad enough that multiple real-world devices would fall under it.

Proposed tags use the same structure as regular tags (with `id` like
`"P-xxxx"`) and are appended to `tag_additions_proposed.csv`.

## Recommended output model

### Final `info.txt`

Two top-level YAML keys: `<device_key>` (device entry) and
`auto_annotation_metadata`.

```yaml
digital_io:
  name: National Instruments 数字IO
  name_en: National Instruments Digital IO
  manufacturer: National Instruments
  category:
    - 实验执行&合成设备
  tags:
    - 实验执行&合成设备
    - 电子天平
  description: National Instruments 数字输入输出设备，用于配置数字线方向并读写数字线状态。
  description_en: >
    A National Instruments digital input/output device for configuring digital
    line direction and reading or writing digital line states.
  class:
    action_value_mappings:
      auto-get_num_lines:
        schema:
          description: 获取设备可用的数字线数量。
          description_en: Return the number of digital IO lines exposed by the device.
      auto-set_IO_state:
        schema:
          description: 设置指定数字线为输入或输出模式。
          description_en: Set one digital line to input or output mode.

auto_annotation_metadata:
  registry_key: digital_io
  annotation_workflow_version: v4
  tag_hints:
    - digital IO control
    - line read/write
    - NI instrument
  tags:
    - id: "4313"
      name: 实验执行&合成设备
      name_en: Experiment Execution & Synthesis Equipment
      type: experimental_step
      rationale: Existing registry category maps directly to this step tag.
    - id: "4318"
      name: 生命体系
      name_en: Life Sciences
      type: experimental_domain
      rationale: Example placeholder.
  proposed_new_tags:
    - id: "P-0005"
      name: 数字IO
      name_en: Digital IO
      type: device_template_tag
      rationale: Multiple NI and generic DIO devices exist in the market.
  websearch_evidence:
    used: false
    findings: []
  processing_pass_order:
    - deterministic_local_extraction
    - per_device_semantic_profile
    - agent_conflict_check_and_web_search
    - batch_tag_pass
    - payload_merge
    - render_info_txt
    - validate_and_review
```

Conventions:

- Natural-language fields without `_en` suffix are Chinese-preferred
- `_en` suffix fields are English
- `category` is pulled from `registry.yaml` as-is (list), not assigned by LLM
- `tags` in device entry is a short list of Chinese tag names (strings)
- `auto_annotation_metadata.tags` holds full tag objects with id, name,
  name_en, type, and rationale
- `proposed_new_tags` has the same structure as `tags`, with `id` like
  `"P-xxxx"`

### Action handling in info.txt

If `registry.yaml` has `action_value_mappings`, keep exactly those actions in
`info.txt` (adding `schema.description` and `schema.description_en`).

If `registry.yaml` has no `action_value_mappings`, fall back to generating
`auto-*` entries for all non-private methods of the focal class.

## Intermediate artifacts

```text
_info_enrichment_workflow/
  outputs/
    <device>/
      01_local_signals.json
      02_device_profile_api.json
      _batch_tag_api.json
      03_enriched_payload.json
      info.txt              (preview, not final)
community_drivers/
  <device>/
    info.txt                (final, written with --write-info-txt)
```

### `01_local_signals.json`

Produced by `extract_info_raw.py`. No model output.

Contains:

1. **Registry fields**: name, category, manufacturer, model, description,
   module, status_types, tags, scene, actions (one-liner format like
   `"auto-reset (from reset())"`)

2. **Driver AST**: module docstring, all class names/bases/docstrings (focal
   class marked), focal-class methods with function_type, function signature,
   and collected comments (above-def comments, inline comments, embedded
   docstrings)

Example shape:

```json
{
  "device": "cryo_tel_gt",
  "registry": {
    "name": "CryoTel GT",
    "category": ["cryocooler"],
    "manufacturer": "",
    "model": {"name": "CryoTel GT", "type": "device"},
    "description": "",
    "module": "unilabos.devices.cryocooler.sunpower_cryotel_gt_cryocooler:CryoTelGT",
    "status_types": ["temperature", "power", "state"],
    "tags": [],
    "scene": {"domain": "General", "scene_name": "General", "step": "Control"},
    "actions": [
      "auto-temperature (from temperature())",
      "auto-reset (from reset())"
    ]
  },
  "driver": {
    "module_docstring": "...",
    "all_classes": [
      {"name": "CryoTelGT", "bases": ["Instrument"], "docstring": "...", "is_focal": true}
    ],
    "focal_class": "CryoTelGT",
    "focal_methods": [
      {
        "function_type": "status_getter",
        "function": "temperature(self)",
        "comments": ["Return current cold-tip temperature in Kelvin."]
      },
      {
        "function_type": "command",
        "function": "reset(self)",
        "comments": ["CryoCooler Methods"]
      }
    ]
  }
}
```

### `02_device_profile_api.json`

Produced by `run_pass_a.py`. One Responses API call per device.

Input: driver AST from `01_local_signals.json` only (no unreliable registry
fields). Includes function-type hints for status-type methods.

Contains `request`, `response` (raw API), and `parsed` (structured output):

```json
{
  "request": { "...": "raw payload" },
  "response": { "...": "raw API response" },
  "parsed": {
    "name": "Sunpower CryoTel GT 低温冷却器",
    "name_en": "Sunpower CryoTel GT Cryocooler",
    "manufacturer": "Sunpower",
    "description": "...",
    "description_en": "...",
    "actions": [
      {"action_name": "auto-temperature", "description": "获取当前温度", "description_en": "Get current cold-tip temperature in Kelvin."}
    ],
    "tag_hints": ["cryogenic cooling", "PID temperature control", "low-temperature physics"]
  }
}
```

### `_batch_tag_api.json`

Produced by `run_pass_b.py`. One API call per batch, results distributed to
each device directory.

Contains `request_model`, `response` (raw batch API response), and
`device_result` (this device's tags).

### `03_enriched_payload.json`

Produced by `render_info_txt.py`. Merges 01 + 02 + batch tags into the single
source of truth for rendering `info.txt`.

Contains `device`, `device_entry` (the final device block), and
`auto_annotation_metadata` (the final metadata block).

## Division of labor

### Done by script

- `extract_info_raw.py`: read registry and driver AST, annotate function
  types, produce `01_local_signals.json`
- `run_pass_a.py`: call Responses API per device, produce
  `02_device_profile_api.json`
- `run_pass_b.py`: call Responses API per batch for tags, produce
  `_batch_tag_api.json`
- `render_info_txt.py`: merge artifacts into `03_enriched_payload.json`,
  render `info.txt`
- `validate_info_txt.py`: validate final `info.txt` structure

### Done by agent orchestration

- Compare LLM-derived device profile with registry entry
- If significant conflict or missing data, trigger web search
- Refine info.txt fields based on web search results
- Review tag outliers and proposed new tags
- Sample QA across a batch

## Web evidence policy

Web search is **not** triggered by script heuristics. Instead:

1. Pass A produces the device profile from driver evidence only
2. The agent compares LLM output with the registry entry
3. If significant conflict or important fields still empty, the agent triggers
   web search
4. Web search results refine `name`, `manufacturer`, `description`,
   `description_en` in info.txt

Save only compact findings (URL, page title, short findings).

## API calling design

### Pass A: per-device semantic profile

Script: `run_pass_a.py`

Input: driver AST from `01_local_signals.json` (module docstring, focal class
methods with function type and comments). No full tag table. No unreliable
registry fields.

Output: `name`, `name_en`, `manufacturer`, `description`, `description_en`,
bilingual per-action descriptions, `tag_hints`.

### Pass B: batch-level tag pass

Script: `run_pass_b.py`

Input: per-device `tag_hints`, `name`, `description_en` from Pass A; `scene`,
`module`, `tags`, `category` from registry; full tag list once.

Output: final tags per device (>= 1 per type), proposed new
`device_template_tag` entries.

### Structured output

Both passes use Responses API with `text.format` strict JSON schema.

## Pass order

1. `deterministic_local_extraction` — `extract_info_raw.py`
2. `per_device_semantic_profile` — `run_pass_a.py`
3. `agent_conflict_check_and_web_search` — agent compares LLM vs registry
4. `batch_tag_pass` — `run_pass_b.py`
5. `payload_merge` — `render_info_txt.py`
6. `render_info_txt` — `render_info_txt.py --write-info-txt`
7. `validate_and_review` — `validate_info_txt.py` + agent QA

## Concrete implementation

Scripts in `_info_enrichment_workflow/tests/model_api_benchmark_001/scripts/`:

| Script | Purpose | Artifact |
|--------|---------|----------|
| `extract_info_raw.py` | Deterministic local extraction | `01_local_signals.json` |
| `run_pass_a.py` | Per-device semantic profile API | `02_device_profile_api.json` |
| `run_pass_b.py` | Batch-level tag assignment API | `_batch_tag_api.json` |
| `render_info_txt.py` | Merge + render | `03_enriched_payload.json`, `info.txt` |
| `collect_proposed_tags.py` | Collect + append proposed new tags | `tag_additions_proposed.csv` |

Validator: `_info_enrichment_workflow/validate_info_txt.py`

Usage:

```bash
# Step 1: extract local signals
python3 scripts/extract_info_raw.py --devices-file devices.txt

# Step 2: per-device semantic profile
python3 scripts/run_pass_a.py --signals-dir ../../outputs

# Step 3: agent reviews conflicts, optionally triggers web search

# Step 4: batch tag assignment
python3 scripts/run_pass_b.py --signals-dir ../../outputs

# Step 5: merge and render
python3 scripts/render_info_txt.py --signals-dir ../../outputs

# Step 6: validate
python3 ../../validate_info_txt.py ../../outputs/*/info.txt

# Step 7: review proposed new tags
python3 scripts/collect_proposed_tags.py --signals-dir ../../outputs
# If accepted:
python3 scripts/collect_proposed_tags.py --signals-dir ../../outputs --append

# Step 8: write to production
python3 scripts/render_info_txt.py --signals-dir ../../outputs --write-info-txt
```
