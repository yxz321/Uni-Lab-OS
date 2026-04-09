Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Deep Search Prompt Template

Use this template for one unavailable device at a time.

---

Target device type: `{device_name}`

Required phage-workflow functions:

`{required_functions}`

Bundle / protocol context:

`{bundle_context}`

Task:

1. Use explicit web search. Do not rely on memory alone.
2. Identify the best specific product/model for this device type, ranking by:
   - function coverage
   - online information richness
   - automation readiness
   - quality / reliability
3. Gather and summarize:
   - official product page(s)
   - datasheet(s)
   - manual(s), preferably PDF links
   - SDK / API / driver / communication interface information
   - expected processed outputs returned to an automation system
   - physical dimensions and integration constraints
   - CAD / STL / STEP / xacro / URDF files for movable parts and interaction points, if available
   - pricing ballpark, if publicly visible
   - suitability for the phage workflow functions listed above
4. Write results into:
   - `evidence.md` as a structured summary
   - `sources.json` as a JSON array of objects with at least `title` and `url`

Minimum `evidence.md` structure:

- Device selected
- Why this model won
- Required functions vs device capability
- Interfaces / automation notes
- Outputs returned by the device
- Footprint / integration constraints
- Files found (manuals, CAD, SDK, APIs)
- Pricing notes
- Risks / unknowns

Use official vendor sources first, then strong secondary sources only when official coverage is missing.
