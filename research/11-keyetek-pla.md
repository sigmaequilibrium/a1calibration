# 11 — "Keyetek" PLA: brand identification and per-nozzle starting values (A1 + AMS lite)

Research date: 2026-10-06. Printer: Bambu Lab A1 (full size) + AMS lite, Bambu Studio, firmware 01.08.01.00+. Nozzles: 0.2 mm and 0.4 mm.

Legend: **[S]** = sourced (URL given), **[I]** = inference / general practice (not specific to this filament), **[V]** = verify in Bambu Studio on your install (value from memory of stock presets; may differ by Studio version).

---

## 1. Brand identification

**Most likely match: KEYTEK, the Kmart Australia in-house 3D-filament brand** (spelled "Keytek", no second "e"). Searches for "Keyetek"/"KEYETEK" on Amazon and the web return only Keytek pages from kmart.com.au. I found no Amazon brand called "Keyetek". **[S]**

- Product lines sold under Keytek at Kmart AU **[S]**:
  - **Keytek PLA 3D Printer Filament** (newer SKUs `110166xxx`, e.g. Navy Blue 110166356, Teal 110166300, Lavender 110166333, Anthracite 110166327; ~AU$19). https://www.kmart.com.au/product/keytek-pla-3d-printer-filament-navy-blue-110166356/
  - **Keytek PLA+ 3D Filament** (SKUs `110077xxx`, e.g. Black 110077194, Ivory White 110077199; ~AU$22). https://www.kmart.com.au/product/keytek-pla+-3d-filament-ivory-white-110077199/
  - **Keytek Silk PLA** (~AU$24). https://www.kmart.com.au/product/keytek-pla-silk-3d-printer-filament-plum-110159929/
  - **Keytek PLA Transparent** https://www.kmart.com.au/product/keytek-pla-transparent-3d-printer-filament-clear-110159840/
  - **Keytek PLA Gradient** (e.g. 110167189) and Keytek PETG.
- **Do not confuse with "Keytech"**, a separate French filament maker (3dprint.com/16656/keytech-3d-printing-filament/). It is unrelated. **[S]**
- **Action for the user:** check the label for the product line (PLA / PLA+ / Silk / Transparent / Gradient). The temperature ranges differ by line (see below). If the spool is not from Kmart AU, this identification is wrong and you should use the generic budget-PLA guidance below, which every number in this doc already falls back to.

### What the manufacturer publishes (Kmart listing text, read via search-engine snippets; direct fetch of kmart.com.au returned HTTP 403)

| Line | Nozzle temp | Bed temp | "Print speed" | Spool | Source |
|---|---|---|---|---|---|
| PLA | **220–240 °C** | 50–60 °C | 300 mm/s | 1 kg | [S] Navy Blue / Teal listings above |
| PLA+ | **220–240 °C** | 50–60 °C | 300 mm/s | 1 kg | [S] PLA+ listings above |
| Silk PLA | **210–230 °C** | 50–60 °C | 300 mm/s | 1 kg | [S] Silk listings above |
| Transparent PLA | **210–230 °C** | 50–60 °C | n/a in snippet | 1 kg | [S] Transparent listings above |

**Not published (could not find):** diameter tolerance, spool material (cardboard or plastic), spool dimensions, drying recommendation, Bambu/AMS compatibility statement, melt-flow data. **No independent reviews** turned up on Reddit, the Bambu forum, OzBargain or MakerWorld (Reddit's JSON endpoint blocked scripted access). Everything on quality and tolerance below is **generic budget-PLA guidance [I]**.

### Conflicts / red flags
1. **Plain PLA listed at 220–240 °C** is high for standard PLA; typical is 190–220 °C. The identical range on the "PLA" and "PLA+" listings looks like copy-pasted marketing, or the PLA may be a high-flow/"high-speed" formulation. Either way, **the temp tower decides, not the label.** [I]
2. **"300 mm/s"** is a marketing line speed. It says nothing about volumetric limits and is meaningless for a 0.2 nozzle (see §3). [I]
3. Bambu's PLA Basic default MVS is 21 mm³/s and Generic PLA is 12 (from verified background). Assume the lower Generic value until the flow test proves otherwise.

---

## 2. Settings common to both nozzles

| Item | Value | Basis |
|---|---|---|
| Base profile family | **Generic PLA @BBL A1** (pick the variant for the matching nozzle). Do not inherit Bambu PLA Basic: its 21 mm³/s MVS assumes Bambu's own resin. | [I]; Generic MVS 12 from background |
| Alternative base for "PLA+" or high-speed variants | Generic PLA is still fine. Bambu Studio also ships "Generic PLA High Speed". Only use it if the flow test shows ≥18 mm³/s on the 0.4 nozzle. | [I][V] |
| Bed, Textured PEI | **55–60 °C** (stay inside the 50–60 °C label range; 60 °C if corners lift). If Studio's Generic PLA textured-plate default is 65 °C, drop it to 60. | [S] label 50–60; [I] |
| Bed, Smooth PEI (High Temp / Engineering plate slot) | **55 °C** (50 °C if you get elephant foot; elephant foot compensation is 0.075 per background) | [S] label; [I] |
| Fan | Keep the A1 Generic PLA fan curve (60/80 % per background), overhang/bridge fan 100 %. Silk/transparent: same. Raise min fan only if small features slump. | background; [I] |
| Drying | Not specified by Keytek. Generic PLA: **50–55 °C for 6–8 h** (food dehydrator, filament dryer, or bed-top box). Dry before calibrating if the spool was opened or stored humid (popping, steam, fuzzy strings). Budget PLA is often not vacuum-sealed well. | [I] |
| Storage | Sealed bag with desiccant. The AMS lite is open-air, so do not leave a spool loaded for weeks in humid weather. | [I] |

### Spool / AMS lite compatibility
- AMS lite accepts spool **width 40–68 mm, inner (hub) diameter 53–58 mm**, and Bambu lists cardboard spools as supported thanks to its spring-loaded hub. https://wiki.bambulab.com/en/ams-lite/manual/faq (via search snippet; direct fetch returned 402) **[S]**
- **Keytek spool material and dimensions are unknown [I].** The Kmart listing says only "1 kg spool". **Measure before loading:** outer flange width, hub ID, outer diameter (typical 1 kg is 195–200 mm OD).
  - Hub ID < 53 mm or > 58 mm: use an external spool holder, or print an adapter (MakerWorld/Printables have many).
  - **Cardboard spool:** works on the AMS lite. Watch for frayed flange edges and paper dust near the hub. If the edge is soft or out of round, print snap-on rims (e.g. https://www.printables.com/model/251028-cardboard-spool-ring-for-bambu-lab-ams-parametric) **[S]**. The AMS lite has no roller-drive dust issue like the enclosed AMS, so cardboard is less of a concern here. [I]
  - Check that the filament end is not wound under or crossed. Budget spools tangle more often, and a tangle in the AMS lite looks like an extruder clog. [I]

### Diameter tolerance and budget-PLA quality concerns [I]
- Keytek publishes no tolerance. Assume ±0.03–0.05 mm until measured. Measure with calipers at about 10 points over 2–3 m, rotating 90° each time to check ovality. Average 1.73–1.77 is fine. Note the average. If it's far from 1.75, the flow ratio will absorb it, but **large swings (>±0.03 within a few metres) cannot be calibrated out**: they show up as banding, varying top-surface fill and run-to-run flow-test scatter.
- Batch and colour variation: calibrate **per colour** (pigment changes flow and temp). Don't reuse a flow ratio from one colour across all of them without a quick check.
- Contamination/particles: a bigger risk with a **0.2 nozzle** (partial clogs). Silk, gradient and translucent lines are fine in principle, but silk usually wants slower outer walls.
- Moisture on arrival is common. Dry first if any doubt.

---

## 3. 0.2 mm nozzle

| Setting | Start | Test range / expected | Basis |
|---|---|---|---|
| Base profile | **Generic PLA @BBL A1 0.2 nozzle** (select the 0.2 printer preset first, then the Generic PLA filament) | — | [I][V] |
| Nozzle temp (manufacturer) | 220–240 °C (PLA/PLA+); 210–230 °C (Silk/Transparent) | — | [S] |
| Starting nozzle temp | **215 °C** (PLA/PLA+), **210 °C** (Silk/Transparent) | Temp tower **230 → 200 °C, step 5 °C**. Low flow on a 0.2 nozzle means the plastic sits in the melt zone longer, so the best temp is usually 5–10 °C below the 0.4 result. Start at the bottom of the label range or a bit under. | label [S]; offset [I] |
| Max volumetric speed | **3 mm³/s** | Test **1.5 → 6 mm³/s, step 0.5**. Expect a usable cap of **3–5 mm³/s**. | see reasoning |
| Flow ratio | 0.98 (Generic default) [V] | Coarse 80–120 %, fine 91–100 % passes (background). Expect **0.92–1.00**. Calibrate separately from the 0.4 nozzle; don't copy. | [I] |
| Pressure advance (K) | Manual (auto cal is unreliable on 0.2; background) | Expected **≈0.03–0.10**, test **0.00–0.12** (pattern or line method, step 0.005). | [I] |
| Fan | A1 Generic PLA curve; consider 100 % for tiny features; keep a minimum layer time so small parts can cool | [I] |
| Retraction | 0.8 mm (A1 default) | Test **0.4–1.2 mm, step 0.2**. Lower pressure in a 0.2 nozzle often allows 0.5–0.8. | [I] |

**MVS reasoning for 0.2:**
- Bambu's stock 0.2 nozzle PLA profiles cap MVS at **2 mm³/s**, set conservatively to avoid clogs. https://forum.bambulab.com/t/max-volumetric-speed-with-0-2-nozzle/62804 **[S]**
- Same thread: one user ran Orca's max-flowrate test (1–6 mm³/s, step 0.5) and got a **5.25 mm³/s** ceiling. Another (X-series) reports extrusion "up to just under 25 mm³/s" without clogs, but with **cosmetic defects above ~9.5 mm³/s / 200 mm/s**. **[S]** **Conflict:** the 25 mm³/s figure is an outlier. Treat it as "won't clog instantly", not as a quality limit.
- Arithmetic: 0.1 mm layer × 0.22 mm line × 150 mm/s = **3.3 mm³/s**. That is already plenty of speed for the detail work a 0.2 nozzle is for. So a 3–4 mm³/s cap costs almost nothing in print time and leaves margin for an unknown budget resin. [I]
- Set the final MVS at about **80 %** of the test's failure point. [I]

---

## 4. 0.4 mm nozzle

| Setting | Start | Test range / expected | Basis |
|---|---|---|---|
| Base profile | **Generic PLA @BBL A1** (0.4 nozzle) | — | [I][V] |
| Nozzle temp (manufacturer) | 220–240 °C (PLA/PLA+); 210–230 °C (Silk/Transparent) | — | [S] |
| Starting nozzle temp | **220 °C** (PLA/PLA+), **215 °C** (Silk/Transparent) | Temp tower **240 → 205 °C, step 5 °C** (silk/transparent: 230 → 200). Pick the coolest temp with good bridges and layer bonding. A truly standard PLA will probably land at 210–220 despite the label. A "PLA+"/high-flow resin may want 225–230 for high flow. | label [S]; [I] |
| Max volumetric speed | **12 mm³/s** (Generic PLA default; background) | Test **8 → 24 mm³/s, step 1** (Studio's Max flowrate test, run at your chosen temp). Expect **12–18 mm³/s** for budget PLA. If it shows ≥20, consider the high-speed base. Final = ~80–90 % of failure point. Re-test if you raise the temp. | background; [I] |
| Flow ratio | 0.98 (Generic default) [V] | Coarse 80–120 %, fine 91–100 % (background). Expect **0.93–1.00**. | [I] |
| Pressure advance (K) | Auto (Flow Dynamics) is OK on 0.4. Confirm with a manual pattern. | Expected **≈0.015–0.05** (A1 PLA, 0.4), test **0.00–0.08 step 0.002**. | [I] |
| Fan | A1 Generic PLA (60/80 %, overhang 100 %) | — | background |
| Retraction | 0.8 mm | Test **0.4–1.6 mm, step 0.2**. Raise only if stringing persists after the temp is tuned. | background; [I] |

---

## 5. Recommended order for this filament
1. Identify the line on the label. Measure spool hub/width and filament diameter. Dry if in doubt.
2. 0.4 nozzle: temp tower → MVS test → flow ratio coarse/fine → PA → retraction. Save as `Keytek PLA <colour> @A1 0.4`.
3. 0.2 nozzle: repeat with the 0.2 ranges above; manual PA. Save as `Keytek PLA <colour> @A1 0.2`. Don't share values between the nozzles.
4. Spot-check flow and PA for each new colour or batch.

## Sources
- Kmart AU Keytek PLA (Navy Blue): https://www.kmart.com.au/product/keytek-pla-3d-printer-filament-navy-blue-110166356/
- Kmart AU Keytek PLA (Teal): https://www.kmart.com.au/product/keytek-pla-3d-printer-filament-teal-110166300/
- Kmart AU Keytek PLA+ (Ivory White / Black): https://www.kmart.com.au/product/keytek-pla+-3d-filament-ivory-white-110077199/ , https://www.kmart.com.au/product/keytek-pla+-3d-filament-black-110077194/
- Kmart AU Keytek Silk PLA (Plum): https://www.kmart.com.au/product/keytek-pla-silk-3d-printer-filament-plum-110159929/
- Kmart AU Keytek PLA Transparent (Clear): https://www.kmart.com.au/product/keytek-pla-transparent-3d-printer-filament-clear-110159840/
- Unrelated "Keytech": https://3dprint.com/16656/keytech-3d-printing-filament/
- Bambu AMS lite FAQ (spool limits): https://wiki.bambulab.com/en/ams-lite/manual/faq
- Bambu forum, 0.2 nozzle MVS: https://forum.bambulab.com/t/max-volumetric-speed-with-0-2-nozzle/62804
- Cardboard spool ring: https://www.printables.com/model/251028-cardboard-spool-ring-for-bambu-lab-ams-parametric

Note: kmart.com.au blocks direct fetches (HTTP 403 for WebFetch, curl and a reader proxy). The listing values above come from search-engine extracts of those pages and agree across many SKUs. Check them against the printed label on your spool.
