# Hettich ROTANTA 460 Robotic Evidence

## Device investigated

**Canonical manufacturer:** Andreas Hettich GmbH  
**Canonical product name:** Hettich ROTANTA 460 Robotic  
**Canonical id for this repo:** `hettich_rotanta_460_robotic`

## Existence and identity verification

The product clearly exists in current first-party Hettich materials.

- The official product page is titled **"ROTANTA 460 Robotic"** and places it under **Automated Centrifuges**.
- The Hettich automation overview page lists **ROTANTA 460 Robotic** as one of four current robotic centrifuge models.
- The English data sheet is titled **"ROTANTA 460 Robotic"** and identifies the legal manufacturer as **Andreas Hettich GmbH** in Tuttlingen, Germany.
- Hettich also publishes an **EU Declaration of Conformity** specifically for **ROTANTA 460 Robotic**.

So the canonical naming is not ambiguous: the commercial model name is **ROTANTA 460 Robotic**, under the **Hettich** brand, manufactured by **Andreas Hettich GmbH**.

## Why this model is relevant

This is a real automation-oriented centrifuge, not just a standard centrifuge with optional networking.

First-party Hettich sources describe it as:

- a **cooled, floorstanding centrifuge**
- a robotically operated model that has been part of laboratory automation systems for **several decades**
- a model used in **high-throughput screening**, biotechnology, and pharmaceutical environments
- a centrifuge with explicit robotic features such as a **loading and unloading hatch in the lid**, **fast and slow positioning modes**, and **RS232** interface

That makes it a strong automation candidate on paper. The limiting question is whether it also covers the exact phage protocol spin envelope.

## Required functions vs device capability

| Required phage function | Evidence for ROTANTA 460 Robotic | Fit |
| --- | --- | --- |
| Repeated low-speed tube spins around `500 x g` | Official max RCF is **`6,446 x g`**, so `500 x g` is comfortably inside range. | Yes |
| Refrigerated operation | Official product page lists **`-20 to +40 C` with pre-cooling function**. | Yes |
| Explicit recovery spin at `8000 x g`, `4 C` | Official max RCF is only **`6,446 x g`** on the robotic model. That is below the required `8000 x g`. | **No** |
| `15 mL` tube support | Data sheet shows a swing-out configuration for **`24 x 50 mL`** and explicitly lists **`15 mL`** tube compatibility at **`4,188 x g`** with the 2-place rotor setup. | Yes |
| `1.5 mL` microtube support for the recovery step | I did **not** find first-party robotic-specific evidence for `1.5 mL` microtube support in the sources used here. The published robotic documents focus on blood tubes, `15/50 mL` tubes, and plates. | Unclear / weak |
| Robotic loading / loader integration potential | Hettich explicitly documents a **robotic lid hatch**, **front or rear automated opening variants**, **RS232**, **positioning modes**, optional **light barriers**, and overview-page compatibility with **linear robots** and **cobots**. | Yes |

## Specs confirmed from manufacturer sources

- **Max RCF:** `6,446 x g`
- **Max RPM:** `6,200 rpm`
- **Temperature control:** `-20 to +40 C` with pre-cooling function
- **Refrigerant:** `R290`
- **Documented robotic features:** lid hatch for loading/unloading, hatch opening time `< 6 s`, fast/slow positioning mode, positioning time `5 s`, positioning accuracy `3 encoder steps out of 4096`, optional additional light barriers, automatic rotor recognition, powered lid lock, RS232

Important nuance on cooling:

- The product page gives the broad chamber-control range of **`-20 to +40 C`**.
- The robotic brochure/data sheet also publishes rotor-specific lowest temperatures at **max speed after precooling**, for example **`6 C`** on the `24 x 50 mL` swing-out setup and **`9 C`** on the `12-plate` setup.

My interpretation is:

- refrigeration is definitely present
- but the exact achievable sample temperature depends on rotor and speed
- this does **not** rescue the `8000 x g` requirement, because the machine still tops out at `6,446 x g`

## Interfaces / automation notes

The automation case for this model is stronger than for a typical benchtop centrifuge.

Authoritative Hettich signals:

- automation overview page says Hettich robotic centrifuges offer **continuous status communication**
- product page says ROTANTA 460 Robotic is already used in many leading automation systems
- data sheet says **interface via RS232**
- brochure/data sheet describe **automated opening** in the lid and show **front** and **rear** hatch variants
- Hettich says its **top-loading** robotic centrifuges are compatible with **linear robots** and **cobots**
- overview FAQ says the device can be switched to **manual mode** if automation malfunctions

What I did **not** find publicly:

- a serial command reference
- an SDK
- OPC UA / SiLA / REST documentation
- a public loader API

So the realistic conclusion is:

- **integration potential is strong**
- **public protocol detail is weak**

## Outputs returned by the device

The public Hettich pages do not expose a message schema, but they do point to likely automation-visible outputs:

- continuous **status communication**
- **error display**
- **automatic rotor recognition**
- hatch / positioning state sufficient for robotic handoff

That last line is an inference from the documented robotic positioning features rather than a published field list.

## Footprint / integration constraints

Official Hettich sources show a refrigerated floorstanding instrument:

- **Dimensions:** `554 x 697 x 654 mm` in the robotic brochure/data sheet
- **Weight:** about `154 kg`
- **Power:** `200-240 V 1~`, `50-60 Hz`, `1,800 VA`
- **Top-loading robotic access** through lid hatch

Important uncertainty:

- the product web page lists dimensions as **`554 x 697 x 684 mm`**
- the brochure and data sheet list **`554 x 697 x 654 mm`**

I would treat the footprint as confirmed but the exact published height as **inconsistent across Hettich sources** until checked with Hettich sales or integration support.

## Files found

- Official product page: <https://www.hettichlab.com/products/centrifuges/automated-centrifuges/rotanta-460-robotic/>
- Official automation overview page: <https://www.hettichlab.com/products/centrifuges/automated-centrifuges/>
- Official English data sheet PDF: <https://www.hettichlab.com/downloadcenter/Products/Datasheets/ROTANTA-460-Robotic_EN.pdf>
- Official automated centrifuges brochure PDF: <https://www.hettichlab.com/downloadcenter/Products/Catalogs_Brochures/Hettich_Robotic-Brochure_EN.pdf>
- Official EU Declaration of Conformity PDF: <https://www.hettichlab.com/downloadcenter/Products/EU_Declaration_of_conformity/ROTANTA_460_Robotic/DOC5680DEEN.pdf>
- Comparison source, Eppendorf 5910 Ri product page: <https://www.eppendorf.com/us-en/Products/Centrifugation/Multipurpose-Centrifuges/Centrifuge-5910Ri-p-PF-963296>

## Pricing notes

I did **not** find a first-party public price for ROTANTA 460 Robotic in the sources used here.

## Comparison vs Eppendorf 5910 Ri

### Where ROTANTA 460 Robotic is stronger

- Much stronger explicit **robotic integration story**
- Purpose-built **loader hatch** and robotic positioning behavior
- First-party **RS232** interface mention
- Explicit compatibility messaging for **linear robots** and **cobots**

### Where Eppendorf 5910 Ri is stronger

- Officially reaches **`22,132 x g`** and **`14,000 rpm`**
- Official temperature range **`-11 to 40 C`**
- Explicitly supports the protocol's `8000 x g` refrigerated recovery step
- Stronger first-party evidence for mixed tube families relevant to the draft protocol, including conical tubes and small high-speed rotor options

## Verdict on suitability

**Verdict:** `hettich_rotanta_460_robotic` is a **real, well-documented robotic centrifuge**, but it is **not a better primary fit than Eppendorf 5910 Ri** for the current draft phage protocol.

Reason:

- it can cover the repeated low-speed `500 x g` spins
- it has true robotic-integration evidence that is better than 5910 Ri's public automation story
- but its official max RCF is only **`6,446 x g`**, which fails the explicit **`8000 x g` at `4 C`** recovery requirement

So the clean recommendation is:

- **support the device as evidenced and draftable**
- **do not promote it above 5910 Ri as the primary centrifuge for the protocol as written**

It could become attractive as a **secondary automation-first centrifuge** if the workflow is rewritten around robotic tube/plate handling and the `8000 x g` recovery step is moved to another instrument or changed experimentally.

## Risks / unknowns

- I did not find a public command set for the documented **RS232** interface.
- I did not find first-party robotic-specific evidence for `1.5 mL` microtube support.
- Hettich's own product page and PDF sources disagree on the exact machine height.
- The product page claims the model is the market leader and only high-g high-capacity model in its segment; I treated that as vendor positioning, not as an independently verified market fact.
