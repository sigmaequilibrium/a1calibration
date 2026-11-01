# Filament settings: starting values, test ranges and run order (A1, 0.2 + 0.4 nozzles)

Printer: Bambu Lab A1 (full size) + AMS lite, Bambu Studio, firmware 01.08.01.00+. Reviewed 2026-10-06.
This file consolidates `research/10`, `11` and `12` after an independent fact-check (section 8 lists every change).
The test procedure itself is `research/07-review-and-master-procedure.md`, Phases A–E. Test models: `docs/README-tests.md`.

> **Reference-filament strategy (added 2026-10-06).** Calibrate **ELEGOO Matte PLA (purple)** fully on both nozzles first (section 0). Then derive the other filaments as offsets from those measured values and confirm each one with short checks: [reference-offset-method.md](reference-offset-method.md). Sections 1–6 still hold. They give the fallback start values and test ranges for any filament that fails its confirmation check, and the full procedure for both PETGs, which always get a full calibration.

**Tags.** **[V]** verified today: read from the Bambu Studio source or its stock presets on GitHub (master), from a Bambu wiki page, or from the manufacturer's own product page. **[S]** sourced, not verified at a primary source: a retailer copy of the manufacturer's spec, a search-engine extract, Elegoo's OrcaSlicer profiles (written for Elegoo printers), or a community/forum report. **[I]** inferred: engineering judgement. The calibration tests decide the final value. These are starting points.

**Common to every row (A1 machine profile, [V]):** retraction 0.8 mm @ 30 mm/s, deretraction 30 mm/s, wipe on (2 mm), Z-hop 0.4 mm "Auto Lift", elephant-foot compensation 0.075 mm (both `0.20mm Standard @BBL A1` and `0.10mm Standard @BBL A1 0.2 nozzle`). Process for tests: `0.20mm Standard @BBL A1` (0.42 lines) and `0.10mm Standard @BBL A1 0.2 nozzle` (0.22 lines, outer/inner wall 120/150 mm/s).

**Plates.** The A1 ships with the Textured PEI plate. In Bambu Studio "Smooth PEI" is the *High Temp Plate* (`hot_plate_temp`). Selecting the right plate also changes first-layer Z on the A1 (Textured PEI gets `G29.1 Z-0.02`) [V]. Bambu's PETG presets set the Cool Plate to 0, meaning "not allowed" [V].

**How to use a row.**
1. Pick the printer preset for the nozzle (`Bambu Lab A1 0.4 nozzle` / `Bambu Lab A1 0.2 nozzle`).
2. Pick the base filament preset named in the row, change the values in the row, and **save as a user preset** (e.g. `ELEGOO PLA+ White @A1 0.4`). Never edit system presets.
3. Run the tests in section 7 and overwrite the "start" values with the measured ones.

---

## 0. ELEGOO Matte PLA, purple (REFERENCE): label 190–230 °C, bed 35–65 °C, dry 50 ± 5 °C 8 h [S: retailer copies of Elegoo's spec (Memory Express, 3DJake: 190–230 °C, bed 50–65 °C); Elegoo's own stores returned HTTP 429 today]; melt index 9.4 ± 1.2 g/10 min, density 1.26 g/cm³, melting point 163 °C [S]

| Setting | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Base preset to inherit | `Generic PLA @BBL A1` [V], then set MVS 15, "long retraction when cut" on with 18 mm, slow-down layer time 6 s, density 1.26. Those values come from `Bambu PLA Matte @BBL A1` [V: 220 °C, MVS 22, flow 0.98, fan 60/80, plates 65/65, long retraction 18 mm, slow-down 6 s]. Why Generic: ELEGOO PLA, PLA+ and Keytek use the same parent, so each derived preset is a "Save as" copy of this one with only its deltas changed | `Generic PLA @BBL A1 0.2 nozzle` [V]; set MVS 2.0 (`Bambu PLA Matte @BBL A1 0.2 nozzle` = 2.0 [V]; Elegoo's own `PLA Matte @0.2 nozzle` = 2 [V for the profile]) |
| Start nozzle temp (first / other) | 215 / 215 [I]. Bambu PLA Matte runs at 220 [V]. Elegoo's matte Orca profiles inherit 220 [V for the profile]. One retailer says "recommended 220" [S]. Starting 5 °C lower keeps the matte look, because matte PLA turns glossier when hotter [I] | 210 / 210 [I] |
| Temp tower file | `stl/0.4/temp_tower_230-190_0.4.stl` (project `3mf/0.4/temp_tower_230-190_0.4.3mf`): the full label range | `stl/0.2/temp_tower_compact_230-190_0.2.stl` (compact, 36.6 mm tall, about 1 h 10 min; project `3mf/0.2/R2_matte-purple_temp_tower_compact_230-190_0.2.3mf`): the full range on purpose, because every offset is anchored on this result. The standard `stl/0.2/temp_tower_230-190_0.2.stl` (54.6 mm, about 1 h 50 min) also works |
| Bed: Textured PEI / Smooth PEI / Cool (SuperTack) | 60 / 60 / 35 (45) [I, inside the label; Bambu Matte 65 / 65 [V]; Elegoo matte profiles textured 65 / smooth 60 [V for the profile]] | same |
| Max volumetric speed: start / test / expected | 15 / 10→24 step 1 / 15–20 [S: Elegoo's own matte profiles use **16** on every 0.4 printer, against 21 for its plain PLA; Bambu PLA Matte 22 [V]]. Run the test at the chosen temperature, and optionally again at +10 °C (gives the MVS-vs-temperature slope used for offsets) | 2.0 [V] / 1.0→5.0 step 0.25 / 2.0–3.0 [I] |
| Flow ratio: start / expected | 0.98 [V] / 0.95–1.00 [I]. Do not judge the matte top by gloss. Use the pencil-rub + raking-light method in `reference-offset-method.md` §2.3 | 0.98 [V] / 0.95–1.02 [I] |
| K (pressure advance): expected / method | 0.020–0.045 [S: Elegoo matte profiles 0.024 (Centauri Carbon) / 0.04 (CC2), on other extruders; I] / **auto** Flow Dynamics, plus one optional manual pattern 0→0.08 step 0.002 to record the auto-vs-manual ratio | 0.05–0.15 [I] / **manual**: 0→0.20 step 0.01, then ±0.03 step 0.005 |
| Fan min / max / overhang / first layers off | 60 / 80 / 100 % above 50 % overhang / 1 [V: Bambu PLA Matte; Elegoo matte profiles also 60/80] | same; slow-down layer time 6 s [V Bambu Matte 0.2] |
| Retraction: start / test | 0.8 mm [V] / run the full coupon series 0.4→1.2 even if it does not string. This gives the PLA-family baseline [I] | 0.8 mm [V] / 0.3→1.2 [I] |
| Z-hop | 0.4 Auto Lift [V] | same |
| Drying | 50 ± 5 °C, 8 h [S]; storage ≤ 20 % RH [S]; long retraction when cut 18 mm [V Bambu Matte] | same |

Notes [I unless tagged]:
- Matte PLA is PLA with a mineral filler. Elegoo does not say which; talc or CaCO₃ is typical.
  - Expect slightly weaker layer bonding and lower Z impact strength than plain PLA. Bambu's matte preset records Z impact 6.6 kJ/m² [V].
  - Expect less stringing; Elegoo markets it that way [S].
  - The filler is mildly abrasive. The stock stainless nozzle is fine, but check it for wear after several kg.
- Hotter prints turn glossier. If the tower winner looks shiny, take the next cooler block that still bonds.
- Colour matters. Elegoo's matte range is pastel ("macaron") colours, so pigment and filler loading differ per colour. **Record the exact colour name and lot number.** Every offset in `reference-offset-method.md` is relative to this spool.
- Sources disagree on print speed: "< 300 mm/s" (Memory Express copy), "up to 250 mm/s" (Elegoo marketing snippet), "60–150 mm/s" (a retailer page). Elegoo's own MVS of 16 is the most useful of these. Measure it.

## 1. ELEGOO PLA (standard) — label 190–230 °C [V], bed 35–65 °C [V], dry 50 ± 5 °C 8 h "Recommended" [V]

| Setting | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Base preset to inherit | `Generic PLA @BBL A1` (MVS 12, flow 0.98) [V] | `Generic PLA @BBL A1 0.2 nozzle` (MVS 1.6) [V] |
| Start nozzle temp (first / other) | 210 / 210 [S: Elegoo's own Orca profile 210; community 205–215] | 210 / 210 [I] |
| Temp tower file | `stl/0.4/temp_tower_230-190_0.4.stl` | `stl/0.2/temp_tower_225-195_0.2.stl` |
| Bed: Textured PEI / Smooth PEI / Cool (SuperTack) | 60 / 60 / 35 (45) [I inside label; Bambu default 65 / 65 / 35 (45) [V]] | same |
| Max volumetric speed: start / test / expected | 15 / 10→24 step 1 / 16–20 [S: Elegoo Orca 16 base, 21 CoreXY] | 2.0 / 1.0→5.0 step 0.25 / 2.0–3.2 [start V: Bambu PLA Basic 0.2 = 2.0; expected S: Elegoo 0.2 profile 3.2] |
| Flow ratio: start / expected | 0.98 [V] / 0.97–1.02 [S] | 0.98 [V] / 0.95–1.02 [I] |
| K (pressure advance): expected / method | 0.020–0.045 [S/I] / **auto** Flow Dynamics (Calibration tab) [V] | 0.05–0.15 [S forum] / **manual** [V wiki] — range 0→0.20 step 0.01, then ±0.03 step 0.005 |
| Fan min / max / overhang / first layers off | 60 / 80 / 100 % above 50 % overhang / 1 layer [V] | same; slow-down layer time 8 s [V] |
| Retraction: start / test | 0.8 mm [V] / 0.4→1.6 step 0.2 [I] | 0.8 mm [V] / 0.3→1.2 step 0.1–0.2 [I] |
| Z-hop | 0.4 Auto Lift [V] | 0.4 Auto Lift [V] |
| Drying | 50 ± 5 °C, 8 h [V]; also set "long retraction when cut" 18 mm to save AMS-lite purge (Bambu does this for PLA Basic) [V] | same |

Notes: colour-dependent; some colours under-melt at 205 and 215 works for all [S]. Run one tower per colour family (dark vs light) [I].

## 2. ELEGOO PLA+ — label 200–230 °C [S: Elegoo EU store spec JSON, via research/10; re-fetch rate-limited today], bed 35–65 °C, dry 50 ± 5 °C 8 h

| Setting | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Base preset to inherit | `Generic PLA @BBL A1` [V] (reference: `eSUN PLA+ @BBL A1` MVS 16 [V]) | `Generic PLA @BBL A1 0.2 nozzle` [V] (reference: `eSUN PLA+` 0.2 MVS 1.8 [V]) |
| Start nozzle temp | 220 / 220 [S: Elegoo Orca 220]; expect 220–230 [S: A1 community 230] | 220 / 220 [I] |
| Temp tower file | `stl/0.4/temp_tower_235-200_0.4.stl` | `stl/0.2/temp_tower_230-200_0.2.stl` |
| Bed: Textured / Smooth / Cool (SuperTack) | 60 / 60 / 35 (45) [I; community 62] | same |
| MVS: start / test / expected | 15 / 10→25 step 1 / 15–22 [S: Elegoo 20, A1 user 22 @230] — run it at the chosen temperature | 1.8 [V eSUN PLA+ 0.2] / 1.0→4.5 step 0.25 / 1.8–3.0 [I] |
| Flow ratio: start / expected | 0.98 [V] / 0.93–1.00 [S: A1 community 0.94] | 0.98 / 0.93–1.00 [I] |
| K: expected / method | 0.025–0.050 [S: A1 community 0.04] / auto | 0.06–0.18 [S/I] / manual, 0→0.20 step 0.01 then fine |
| Fan min / max / overhang / first layers off | 60 / 80 / 100 / 1 [V]; raise max to 100 only if overhangs curl [I] | same |
| Retraction: start / test | 0.8 [V] / 0.4→1.6 [I] | 0.8 [V] / 0.3→1.2 [I] |
| Z-hop | 0.4 Auto Lift [V] | same |
| Drying | 50 ± 5 °C 8 h [S]. Stringing on PLA+ is reported not to respond to temperature alone [S]: dry first | same |

## 3. ELEGOO Rapid PLA+ — label 200–230 °C [V: Elegoo EU store, fetched today], bed 35–65 °C [V], dry 50 ± 5 °C 8 h [V]

| Setting | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Base preset to inherit | `Generic PLA High Speed @BBL A1` (MVS 18) [V] | `Generic PLA High Speed @BBL A1 0.2 nozzle` (MVS 2.0) [V] |
| Start nozzle temp | 225 / 225 [I]; Elegoo's profiles 220 [S]; A1 users running fast settle at 230 [S] | 220 / 220 [I] (favour the cool end: the runny melt oozes on a 0.2) |
| Temp tower file | `stl/0.4/temp_tower_235-200_0.4.stl` (use `240-205` only if you print near the MVS limit) | `stl/0.2/temp_tower_230-200_0.2.stl` |
| Bed: Textured / Smooth / Cool (SuperTack) | 60 / 60 / 35 (45) [S: Elegoo 60, community 62]; black Rapid PLA+ has a reported A1 adhesion issue: wash plate, 65 °C [S] | same |
| MVS: start / test / expected | 18 [V] / 14→30 step 1 / 20–26 [S/I] (Elegoo 21; A1 hotend spec 28 mm³/s with ABS @ 280 °C [S]; ignore the "40" MakerWorld cap) | 2.0 [V] / 1.0→5.0 step 0.25 / 2.2–3.5 [I] |
| Flow ratio: start / expected | 0.98 [V] / 0.96–1.00 [S: A1 community 0.99] | 0.98 / 0.95–1.00 [I] |
| K: expected / method | 0.015–0.035 [S: A1 community 0.022] / auto | 0.05–0.14 [I] / manual, 0→0.20 step 0.01 then fine |
| Fan min / max / overhang / first layers off | 60 / 100 / 100 / 1 [S: Elegoo Orca Rapid 60/100; base has 60/80 V] | 60 / 80 / 100 / 1 [V] (0.2 layers cool easily) |
| Retraction: start / test | 0.8 [V] / 0.4→1.6 [I] | 0.8 [V] / 0.3→1.2 [I]; expect the upper half [I] |
| Z-hop | 0.4 Auto Lift [V] | same |
| Drying | 50 ± 5 °C 8 h [V] | same |

## 4. Keytek PLA (Kmart AU, standard PLA line — user confirmed) — label 220–240 °C, bed 50–60 °C [S: kmart.com.au listing text via search extracts; Kmart blocks direct fetches]; no drying spec published

| Setting | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Base preset to inherit | `Generic PLA @BBL A1` (MVS 12) [V] | `Generic PLA @BBL A1 0.2 nozzle` (MVS 1.6) [V] |
| Start nozzle temp | 220 / 220 [S: bottom of label] | 215 / 215 [I] |
| Temp tower file | `stl/0.4/temp_tower_240-205_0.4.stl` | `stl/0.2/temp_tower_230-200_0.2.stl` |
| Bed: Textured / Smooth / Cool (SuperTack) | 60 / 55 / 35 (45) [S label 50–60; I] | same |
| MVS: start / test / expected | 12 [V] / 8→24 step 1 / 12–18 [I] (≥ 20 → consider the High Speed base) | 2.0 / 1.0→5.0 step 0.25 / 2–4 [S forum ceiling 5.25 on a 0.2; I] |
| Flow ratio: start / expected | 0.98 [V] / 0.93–1.00 [I] | 0.98 / 0.92–1.00 [I] |
| K: expected / method | 0.015–0.05 [I] / auto | 0.05–0.15 [I] / manual, 0→0.20 step 0.01 then fine |
| Fan min / max / overhang / first layers off | 60 / 80 / 100 / 1 [V] | same |
| Retraction: start / test | 0.8 [V] / 0.4→1.6 [I] | 0.8 [V] / 0.3→1.2 [I] |
| Z-hop | 0.4 Auto Lift [V] | same |
| Drying | 50 °C, 6–8 h [I] (budget spools are often poorly sealed). Measure filament diameter (10 points) and spool hub (AMS lite: 53–58 mm ID, 40–68 mm width [V]) | same |

Notes: 220–240 °C is hot for a standard PLA; the tower decides [I]. Calibrate per colour.

## 5. ELEGOO PETG PRO (blue) — label 230–260 °C, bed 65–75 °C, dry 60 ± 5 °C 8 h [S: Elegoo spec via research/12 and retailer copies today; Elegoo store rate-limited]; glue "Recommended" [S]

| Setting | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Base preset to inherit | `Generic PETG @BBL A1` (255 °C, MVS 8, flow 0.95, fan 40/90, bed 80) [V] | `Generic PETG @BBL A1 0.2 nozzle` (MVS 1) [V] |
| Start nozzle temp | 240 / 245 [S: Elegoo's own Orca PETG PRO 240] | 245 / 245 [I] (Bambu raises PETG Basic to 255 on 0.2 [V]) |
| Temp tower file | `stl/0.4/temp_tower_260-230_0.4.stl` | `stl/0.2/temp_tower_260-230_0.2.stl` |
| Bed: Textured / Smooth (glue!) / Cool | **70** / 70 with glue stick / not allowed [S label 65–75; Elegoo profile 70]; the Generic preset's 80 is above the label. Go 75 only if corners lift [I] | same |
| MVS: start / test / expected | **8** [V Generic; S Elegoo's own PETG PRO profile 8] / 4→16 step 0.5 / 8–12 [I] | **1.0** [V Bambu; S Elegoo PETG PRO 0.2 = 1] / 0.5→3.0 step 0.25 / 1.0–2.0 [I] |
| Flow ratio: start / expected | 0.95 [V] / 0.92–0.98 [S/I] | 0.95 [V] / 0.92–1.00 [I] |
| K: expected / method | 0.02–0.06 [I] / auto | unknown range on A1 0.2 [S forum 0.05–0.45] / manual, coarse 0→0.30 step 0.02, then ±0.03 step 0.005 |
| Fan min / max / overhang / first layers off | 30 / 50 / 90 % above 10 % / 3 [V: Bambu PETG Basic @A1] (Generic's 40/90 is high for PETG layer bonding) | 20 / 35 / 90 % above 25 % / 3 [V: Bambu PETG Basic @A1 0.2] |
| Retraction: start / test | 0.6 [I] (Bambu PETG Basic 0.4 [V]) / 0.2→1.4 step 0.2 | 0.6 [I] / 0.2→1.0 step 0.2 |
| Z-hop | 0.4 Spiral Lift [V: Bambu PETG Basic @A1] | 0.4 Spiral Lift |
| Drying | **required**: 60–65 °C, 8–12 h [S]; AMS lite cannot dry [V] — do not leave PETG in it for days | same |

## 6. ELEGOO Rapid PETG (clear / Transparent) — label 240–270 °C, bed 65–75 °C [S: retailer copies of Elegoo spec, today], dry 60 ± 5 °C 8 h, glue recommended [S]

| Setting | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Base preset to inherit | **`Generic PETG HF @BBL A1`** (MVS 16, fan 20/40, retraction 0.4, bed 70) [V] — closest stock analogue to a high-flow PETG; research/12 used Generic PETG | `Generic PETG HF @BBL A1 0.2 nozzle` (MVS 1, fan 20/40) [V] |
| Start nozzle temp | **250 / 250** [S: Elegoo's own Rapid PETG profiles 250] — the HF base's 220 is below the label minimum, change it | 250 / 250 [I] |
| Temp tower file | `stl/0.4/temp_tower_270-240_0.4.stl` | `stl/0.2/temp_tower_270-240_0.2.stl` |
| Bed: Textured / Smooth (glue!) / Cool | 70 / 70 with glue stick / not allowed [V base; S label] | same |
| MVS: start / test / expected | 16 [V] / 8→26 step 1 / 14–20 [S: Elegoo 18 @250; community 16–24] | 1.0 [V] / 0.5→3.5 step 0.25 / 1.2–2.5 [I] |
| Flow ratio: start / expected | 0.95 [V] / 0.93–1.00 [S community 0.95] | 0.95 / 0.93–1.00 [I] |
| K: expected / method | 0.02–0.05 [S: community 0.030] / auto | manual, coarse 0→0.30 step 0.02, then fine [I] |
| Fan min / max / overhang / first layers off | functional: 20 / 40 / 90 / 3 [V HF base]; clear look: 10 / 30 / 90 / 3 [V: Bambu PETG Translucent @A1] | 10 / 30 / 90 / 3 [V Translucent 0.2] |
| Retraction: start / test | 0.4 [V HF base; Translucent 0.3] / 0.2→1.2 step 0.2 | 0.4 / 0.2→1.0 step 0.2 [I] |
| Z-hop | 0.4 Spiral Lift [I] | same |
| Drying | **required**: 60–65 °C, 8–12 h; re-dry before every clarity print [S] | same |

Clarity variant (0.4 only, separate filament + process preset): 270 °C, flow 1.01, all fans 0, 0.1 mm layers, 0.5 mm lines, 1 wall, 0 top/bottom shells, 100 % aligned rectilinear infill, all speeds 20 mm/s, K 0.02 [S: Bambu wiki transparent-PETG 3MF]. Purge blue → clear generously (flush multiplier ≥ 1.5) [I].

---

## 7. Run order per filament

Do once per nozzle before any filament: Phase A (machine calibration from the screen) and Phase B of `research/07`, then `dim01_first-layer-squares_<n>` and, optionally, `min_feature_<n>` with your best-calibrated PLA.

Turn on **Developer mode** (Preferences) for the temperature, MVS and retraction tools. **After every developer-menu test, start a new project before saving a preset** (the test overrides leak into presets otherwise) [V].

**Print-dialog policy:** "Flow Dynamics Calibration" = **Off** when you want your saved K values. With a **0.2 nozzle keep it Off always**: On would run the automatic calibration that the wiki says is unreliable on 0.2 mm hotends, and Studio itself warns on i3 (A1) printers that auto calibration with a < 0.3 mm nozzle "may have a high probability of failure" [V].

| # | Step | Tool / file | 0.4: approx time | 0.2: approx time |
|---|---|---|---|---|
| 0 | Dry (PETG always; PLA if opened > 2 weeks or strings) | dryer | 8 h | — |
| 1 | Create user preset from the base in the table; set start temp and bed | Studio | 5 min | 5 min |
| 2 | Temperature tower + `M104` per the table in `docs/tests-temp-stringing.md` | `temp_tower_<range>_<n>.stl` | 1.5–2.5 h | 2–4 h |
| 3 | Flow Dynamics (provisional) | 0.4: Calibration tab > Flow Dynamics > **Auto** (no plate print). 0.2: Calibration tab > Flow Dynamics > **Manual**, custom range from the table (Studio's default for direct drive is only 0→0.05 step 0.005 [V], too narrow for 0.2) | 5 min | 20–30 min |
| 4 | Flow ratio coarse (80–120 %) then fine (91–100 %) | Calibration tab > Flow Rate > Manual | 30–45 min | 45–90 min |
| 5 | Max volumetric speed (optional on 0.4 if you print slowly; recommended on 0.2, where the stock caps of 1.0–2.0 mm³/s throttle the 120–150 mm/s default wall speeds) | Developer menu > Calibration > More > Max flowrate, range from the table; MVS = start + height × step, use 90 % | 20–30 min | 20–30 min |
| 6 | Flow Dynamics again if steps 2 or 5 changed temp or MVS; assign K to the AMS-lite slot (Device tab) | as step 3 | 5 min | 20–30 min |
| 7 | Stringing check; retraction only if it strings | `stringing_pins_<n>.stl`; then `retraction_coupon_<n>.stl` per value (or dev-menu Retraction test on 0.4) | 20 min (+10 min per coupon) | 30 min (+15 per coupon) |
| 8 | Cooling / overhang / bridge (one PLA and one PETG at least; every filament if you print overhangs) | `overhang_angles_<n>.stl`, `bridge_spans_<n>.stl` | 45–60 + 30–40 min | 1.5–2 h + 40 min |
| 9 | Dimensional (shrinkage, XY compensation, elephant foot), one plate | `dim02` + `dim03` + `dim05` | 1–1.5 h | 2–3 h |
| 10 | Fit check | `dim04_fit-clearance-*` | 40 min | 1 h |
| 11 | Final verification with the saved presets unchanged | `verify_combo_<n>.stl` | 20–35 min | 30–45 min |

Times are rough (slice to confirm). Suggested filament order:
1. **ELEGOO Matte PLA (reference, section 0):** every step above, plus the reference extras in `reference-offset-method.md` §2.
2. The derived PLAs (ELEGOO PLA, PLA+, Rapid PLA+, Keytek): predicted values plus the confirmation checks in `reference-offset-method.md` §4. Run the full order only for a filament that fails.
3. PETG PRO, then Rapid PETG: full order always.

Do the 0.4 nozzle for all filaments before swapping to the 0.2. Each swap means setting the nozzle on the printer, machine calibration, and the first-layer test again.

Per-filament shortcuts:
- **ELEGOO Matte PLA (reference):** full order on both nozzles, with no shortcuts. Also run the retraction coupon series and steps 8–10 even if nothing looks wrong. The other filaments inherit these results.
- **ELEGOO PLA, PLA+, Rapid PLA+, Keytek:** full order. Rapid PLA+: run step 5 at the chosen temperature, and redo step 2 at your real wall speed if you print fast.
- **PETG PRO (blue), Rapid PETG (clear):** dry first; textured PEI at 70 °C, or smooth PEI **with glue** only (PETG can tear smooth PEI). Do step 8 for at least one of them (PETG needs its own fan values).

---

## 8. Fact-check of research 10 / 11 / 12 (what changed)

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 1 | 0.2-nozzle MVS in Bambu presets: PLA Basic 2.0, Generic PLA 1.6, Generic PLA HS 2.0, eSUN PLA+ 1.8; every PETG 0.2 preset 1.0 (research 10, 12) | **Verified** | BambuStudio `resources/profiles/BBL/filament/*@BBL A1 0.2 nozzle.json` |
| 2 | Research 11: "Bambu's stock 0.2 PLA profiles cap MVS at 2"; Keytek 0.2 start 3 mm³/s | **Partly wrong / changed** | Generic PLA 0.2 (Keytek's base) is 1.6, not 2. Start lowered to 2.0 (Bambu's highest PLA 0.2 value); test range kept up to 5 |
| 3 | Research 12: PETG 0.2 MVS start 1.5–2, expected 2–3.5 | **Changed** | Both Bambu (all PETG 0.2 presets) and Elegoo's own `Elegoo PETG PRO @0.2 nozzle` use **1.0**. Start 1.0, expect 1–2 (PETG PRO), 1.2–2.5 (Rapid) |
| 4 | Research 12: PETG PRO 0.4 MVS start 10, test 5–20 | **Changed** | Elegoo's own PETG PRO profiles: 8 (base, Centauri Carbon) and 5 (CC2); Bambu Generic PETG A1 = 8. Start 8, test 4→16, expect 8–12 |
| 5 | Research 12 base for Rapid PETG: Generic PETG | **Changed** | Bambu Studio has `Generic PETG HF @BBL A1` (MVS 16, fan 20/40, retraction 0.4, bed 70; 0.2 variant MVS 1). Closer to a high-flow PETG; but its 220 °C default is below Rapid PETG's 240 minimum — set 250 (Elegoo's own Rapid PETG profiles: 250 °C, MVS 18, fan 30/80) |
| 6 | Blue PETG line unknown | **Resolved by user** | PETG PRO (230–260 °C, bed 65–75). Tower 260→230 on both nozzles; the union-range notes are dropped |
| 7 | 0.2 K ranges: research 10 0.05–0.15; research 11 0.03–0.10 (test to 0.12); research 12 coarse 0–0.30 | **Unified** | All forum-sourced. PLA family: test 0→0.20 step 0.01 then fine; PETG: coarse 0→0.30 step 0.02. Studio's Calibration-tab manual PA default for direct drive is **0→0.05 step 0.005** [V `CalibrationWizardPresetPage.cpp`]; widen it by hand. The developer-menu PA Pattern default is 0→0.08 step 0.005, PA Line/Tower 0→0.1 step 0.002 [V `calib_dlg.cpp`] (research/07 quoted step 0.002 for the pattern) |
| 8 | Auto Flow Dynamics on 0.2 | **Verified, stronger** | Bambu wiki: "all series of printers using 0.2mm hotend have a high probability of causing inaccurate automatic flow calibration results or calibration failure". Studio shows a < 0.3 mm warning for i3 (A1) printers. Consequence added: print-dialog Flow Dynamics = Off on 0.2 |
| 9 | PLA+ temps 200–230, start 220 | **Sourced** (Elegoo store rate-limited today) | Elegoo's Orca profiles 220 [V for the profile]; same label range as Rapid PLA+, which was fetched today |
| 10 | Rapid PLA+ 200–230, dry 50 ± 5 8 h | **Verified** | Elegoo EU store spec JSON, fetched 2026-10-06. ELEGOO PLA 190–230 / 35–65 / 50 °C 8 h also verified (AU store) |
| 11 | Rapid PLA+ tower 240→205 (research 10) | **Changed to 235→200** | 240 is 10 °C over the label; the tower prints slowly, so the speed argument applies to the MVS test, not the tower. 240-205 is still generated |
| 12 | Rapid PETG 240–270, bed 65–75 | **Sourced** | Retailer copies of the Elegoo spec (e.g. arvutitark.ee, masterfoto.lv), consistent with research/12 |
| 13 | Keytek PLA 220–240 °C, bed 50–60 | **Sourced only** | Kmart listing text via search-engine extracts (several SKUs agree); kmart.com.au returns HTTP 403 to scripts. Check the spool label |
| 14 | PETG bed: Bambu Generic 80 vs label 65–75 | **Verified conflict** | `Generic PETG @BBL A1` textured/smooth 80 [V]; PETG Basic/HF/Translucent and Generic PETG HF 70 [V]; Elegoo profiles 70. Use 70 |
| 15 | PETG fan presets (Basic 30/50, Basic 0.2 20/35 @25 %, Translucent 10/30, HF 30/50) and PETG Basic retraction 0.4 + Spiral Lift | **Verified** | BambuStudio presets |
| 16 | Studio temperature test defaults | **Verified, added** | PLA 230→190, PETG 250→230, ABS/ASA 270→230 (`calib_dlg.cpp`). Our towers replace these because they use 0.4-sized geometry and fixed 10 mm blocks |
| 17 | 0.2 process elephant-foot value (dimensional doc said "check") | **Verified** | 0.075 mm, same as the 0.4 process |
| 18 | Hotend limit 28 mm³/s (ABS, 280 °C) | Sourced (A1 spec sheet PDF, research/10) | not re-fetched |
