# High-Speed Refrigerated Centrifuge Evidence

## Device selected

**Selected model:** Eppendorf **Centrifuge 5910 Ri**

## Why this model won

I compared the most plausible explicit-search hits that surfaced strong first-party documentation:

1. **Eppendorf Centrifuge 5910 Ri**  
   Best overall balance of function coverage, public documentation depth, connectivity, rotor range, and public pricing. It reaches **22,132 x g**, runs at **-11 C to 40 C**, supports conical tubes and microtubes, and has the richest first-party digital stack through **VisioNize Lab Suite**.

2. **Eppendorf SpinPro 6 R**  
   Strongest automation-forward runner-up. It adds an **electric lid drive**, **LIMS and VisioNize integration**, RFID rotor recognition, and PDF run-log export. But it appears to have launched only in **March 2026**, so it has less public history and a thinner evidence trail than 5910 Ri.

3. **Eppendorf 5810 R**  
   Credible conservative fallback. It covers the speed and refrigeration requirements and even exposes an optional **RS-232 C** interface, but its public connectivity story is much weaker than 5910 Ri and it looks more like a traditional benchtop centrifuge than a digitally integrated one.

Why 5910 Ri wins:

- It fully covers both the low-speed and high-speed phage steps with headroom.
- It has first-party documentation for product specs, brochure, software, rotor family, and pricing.
- Its connectivity story is real but still realistic: networked monitoring, alerts, documentation, data export, and audit trail support through VisioNize.
- It is more mature than SpinPro 6 R while being much more connected than 5810 R.

## Required functions vs device capability

| Required phage function | Evidence for 5910 Ri | Fit |
| --- | --- | --- |
| Repeated low-speed pelleting around `500 x g` | Product page shows programmable speed / RCF control and a range up to **22,132 x g**; running at `500 x g` is well inside range. | Yes |
| Refrigerated clarification at `8000 x g`, `4 C` | Product page lists **-11 C to 40 C** temperature range and **22,132 x g** max with fixed-angle rotor. | Yes |
| Early `15 mL` tubes | Product page lists max conical capacity **68 x 15 mL / 36 x 50 mL**. Official package listings include S-4x750 and S-4xUniversal configurations with **5/15/50 mL** adapters. | Yes |
| Later `1.5 mL` tubes | Product page says fixed-angle rotors support tubes from **0.2 mL to 250 mL**. Rotor overview lists **FA-48x2** and **FA-30x2** for **1.5/2.0 mL** tubes. | Yes |
| Some automation potential | 7-inch VisioNize touch UI, user management, documentation, networked monitoring, event history, export, notifications, and audit trail via VisioNize Lab Suite. | Yes, but mostly monitoring/documentation rather than open run-control |

## Rotor / adapter fit for protocol vessels

### `15 mL` tubes

The strongest documented fits are the swing-bucket packages:

- **S-4x750** package with adapters for **5/15/50 mL conical tubes**
- **S-4xUniversal** package with adapters for **5/15/50 mL conical tubes and plates**

Those are useful for the repeated early tube-handling spins around `500 x g`.

### `1.5 mL` tubes

For the post-amplification high-speed clarification steps, the clearest fit is a fixed-angle microtube rotor:

- **FA-48x2** for **48 x 1.5/2.0 mL**
- **FA-30x2** for **30 x 1.5/2.0 mL**

These rotors are explicitly listed for the 5910 Ri rotor family and support the machine's high-speed mode.

### Practical implication

One 5910 Ri can cover both vessel families, but it likely does so with **two rotor setups**:

- swing-bucket rotor for `15 mL` conicals
- fixed-angle microtube rotor for `1.5 mL` tubes

That is operationally normal for a benchtop centrifuge, but it is still a **manual rotor change**, not an automated one.

## Interfaces / automation notes

### What is documented

- **7-inch VisioNize touch interface**
- **User management** with multiple authorization levels
- **Documentation features** supporting GLP/GxP-style environments
- Connection to **VisioNize Lab Suite** over local network + Internet
- Remote **monitoring**, **notifications**, **task management**, **booking**, and **audit trail**
- Device software updates can be scheduled and confirmed on-device

### Network / integration constraints

From the VisioNize Lab Suite manual:

- touch-enabled devices connect to a **local network with Internet connection**
- device should be near an **active network port**
- connection uses **Ethernet**
- firewall exception is documented as `*.eppendorf.com` over **443/TCP**, using **MQTT via web sockets**

### What I did not find

I did **not** find a public:

- command API
- SDK
- serial command reference
- OPC UA / SiLA / REST run-control spec

So the realistic automation story is:

- good **digital visibility and data capture**
- some compliance / operational integration
- **unclear public support for third-party start/stop programmatic control**

That last point is an inference from the official documents I found and did not find.

## Outputs returned by the device

Based on the VisioNize product and software documentation, the automation-visible outputs are mainly:

- device **status**
- run **parameters**
- **history chart**
- **event list**
- exported monitoring data in **Excel**
- **e-mail / SMS notifications**
- **time-stamped audit trail** entries
- downloadable **PDF** manuals and certificates associated with the device

For the newer SpinPro 6 R runner-up, the operating manual snippet also indicates that **run records can be exported as PDF**, and the product page explicitly mentions **LIMS and VisioNize integration**. That strengthens SpinPro 6 R as an automation-oriented alternative, but 5910 Ri still has the denser documentation set.

## Footprint / integration constraints

For **5910 Ri**:

- Dimensions: **72 x 68 x 37 cm**
- Footprint without front panel: **72 x 62 cm**
- Weight: **109 kg**
- Height with lid open: **85 cm**
- Refrigerated bench unit, so bench strength and service access matter
- Needs nearby Ethernet if VisioNize connectivity is desired

For comparison:

- **5810 R** is smaller at about **70 x 60.8 x 34.5 cm** and **99 kg**
- **SpinPro 6 R** is about **70.6 x 74.5 x 38.5 cm** and **100 kg**

So 5910 Ri is not the smallest option, but it remains benchtop-scale and does not require a floor centrifuge footprint.

## Files found

### Selected model: 5910 Ri

- Official product page: <https://www.eppendorf.com/us-en/Products/Centrifugation/Multipurpose-Centrifuges/Centrifuge-5910Ri-p-PF-963296>
- Official brochure PDF: <https://www.eppendorf.com/product-media/doc/en/990312/Centrifugation_Brochure_Centrifuge-5910-Ri_Accelerate-Your-Research.pdf>
- Official VisioNize Lab Suite manual PDF: <https://www.eppendorf.com/product-media/doc/en/972319/VisioNize_Software-manual_VisioNize-Lab-Suite.pdf>
- Official price list PDF: <https://www.eppendorf.com/product-media/doc/en/11245129/General_Catalog_Price-List-2024-IVD-prices-euros.pdf>
- Official rotor overview PDF: <https://www.eppendorf.com/product-media/doc/de/988706/Centrifugation_Overview_Rotors-S-4xUniversal_S-4xUniversal-Large_S-4x400_S-4x500-S-4x750-round-buckets-S-4x1000-high-capacity-buckets_S-4x1000-plate-tube-buckets_S-4x1000-round-buckets_FA.pdf>

### Runner-ups used for ranking

- 5810 R product page: <https://www.eppendorf.com/us-en/Products/Centrifugation/Multipurpose-Centrifuges/Centrifuge-5810-5810R-p-PF-240994>
- 5810 R operating manual: <https://www.eppendorf.com/product-media/doc/en/2283284/Centrifugation_Operating-manual_Centrifuge-5804-R_5810-R-compliant-2017-746-EC.pdf>
- SpinPro 6 R product page: <https://www.eppendorf.com/us-en/Products/Centrifugation/Multipurpose-Centrifuges/SpinPro6R-p-PF-14012022>
- SpinPro 6 R operating manual: <https://www.eppendorf.com/product-media/doc/en/17096809/Centrifugation_Operating-manual_SpinPro-6-R.pdf>
- SpinPro 6 R brochure: <https://www.eppendorf.com/product-media/doc/en/17082071/Centrifugation_Brochure_SpinPro-6-R-centrifuge_Effortless-Every-Time.pdf>
- SpinPro 6 R launch note: <https://corporate.eppendorf.com/en/09032026-eppendorf-introduces-spinpror-centrifuge-series-to-streamline-life-science-research/>

## Pricing notes

Public pricing for **5910 Ri** is unusually good:

- Official Eppendorf 2024 price list shows **11,246.60 EUR** for the refrigerated unit **without rotor**
- Official Eppendorf price list shows **13,038.00 EUR** for the **High Speed Solution**
- Official Eppendorf price list shows **14,861.20 EUR** for the **S-4xUniversal** package with adapters for `5/15/50 mL` conicals and plates

Interpretation:

- realistic capital budget is roughly **11k to 15k EUR** before local taxes, options, service, and regional pricing
- if both conical-tube and microtube work are needed, total spend will be higher once the second rotor set is included

## Verdict: one centrifuge vs two

**Verdict:** For the **draft protocol as written**, **one high-speed refrigerated centrifuge is enough**.

Reason:

- the draft protocol's centrifugation steps are all fundamentally **tube-oriented**
- the repeated early spins are only around **`500 x g`**
- the one special requirement is a refrigerated **`8000 x g` at `4 C`** clarification step
- 5910 Ri can do both on a single instrument with the appropriate rotor choices

### Do we still need `v_spin_backend`?

**Not for the current draft protocol.**

A second lower-speed / plate-oriented centrifuge such as `v_spin_backend` is only justified if you intentionally rewrite the workflow toward:

- microplate or deep-well processing
- robotic plate transport and batching
- minimizing rotor swaps on the high-speed centrifuge
- higher-throughput automation where a dedicated plate centrifuge removes a bottleneck

So the clean answer is:

- **draft protocol today:** one high-speed refrigerated centrifuge is enough
- **future automation-first plate rewrite:** a second plate centrifuge may become worthwhile, but it is not strictly required by the current protocol

## Risks / unknowns

- I did not find a public run-control API or open driver protocol for 5910 Ri.
- The best-documented digital outputs are monitoring, logging, documentation, and notifications rather than explicit external motion/control commands.
- Covering both `15 mL` and `1.5 mL` steps likely requires **manual rotor changes**.
- If the team wants true robotic walk-away operation, the newer **SpinPro 6 R** may deserve a second pass because its **electric lid drive** and explicit **LIMS integration** are better automation signals than 5910 Ri.
- If the team wants the most conservative, mature choice with lower cost, **5810 R** remains viable, but its connectivity story is weaker.
