Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

Target device type: high-speed refrigerated laboratory centrifuge with automation potential

Required phage-workflow functions:

- run repeated low-speed cell pelleting steps around `500 x g` at room temperature
- run a refrigerated clarification step at `8000 x g` and `4 C`
- support the carrier formats implied by the draft protocol: `15 mL` tubes early, `1.5 mL` tubes after amplification recovery
- ideally support enough automation readiness or documented integration to justify a guessed driver

Bundle / protocol context:

- Bundle 3: centrifugation
- draft protocol uses multiple `500 x g` steps for cell handling and one `8000 x g`, `4 C` step before `0.22 um` filtration
- need to determine whether one high-speed refrigerated centrifuge can replace both the generic `centrifuge` recommendation and the existing `v_spin_backend`, or whether two separate centrifuges are still justified

Task:

1. Use explicit web search only.
2. Identify the best specific product/model for this device type, ranking by:
   - function coverage for both `500 x g` and `8000 x g` use cases
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
   - rotor / adapter compatibility for `15 mL` and `1.5 mL` tubes
   - pricing ballpark if public
   - suitability for the phage workflow functions above
4. Explicitly answer:
   - Is one high-speed refrigerated centrifuge enough for the draft protocol?
   - Or do we still need a second lower-speed / plate-oriented centrifuge such as `v_spin_backend`?
5. Write results into:
   - `Uni-Lab-OS/drivers_phage/high_speed_refrigerated_centrifuge/evidence.md`
   - `Uni-Lab-OS/drivers_phage/high_speed_refrigerated_centrifuge/sources.json`

Minimum `evidence.md` structure:

- Device selected
- Why this model won
- Required functions vs device capability
- Rotor / adapter fit for protocol vessels
- Interfaces / automation notes
- Outputs returned by the device
- Footprint / integration constraints
- Files found
- Pricing notes
- Verdict: one centrifuge vs two
- Risks / unknowns
