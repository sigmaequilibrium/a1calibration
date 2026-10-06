# Reference-filament offset method (A1, 0.4 + 0.2 nozzles)

**Idea.** Calibrate one filament fully: **ELEGOO Matte PLA, purple**, on both nozzles. Every other filament then starts from that filament's *measured* values plus a delta or ratio, and short checks confirm the result. A filament that fails a check falls back to the full calibration in `filament-settings.md` sections 1–6.

**Be clear about what this saves.** It saves temperature towers, coarse flow passes, wide PA sweeps and dimensional plates for the PLA family. It does **not** remove per-filament measurement of flow ratio and K. Those depend on the actual spool: its diameter, density, die swell and pigment. The offsets only narrow those tests. The two PETGs share nothing with the reference except the machine-level values (§1), so they always get a full calibration.

Tags as in `filament-settings.md`: **[V]** read today from Bambu Studio presets/source or a manufacturer page, **[S]** sourced (retailer copy, Elegoo's OrcaSlicer profiles, community), **[I]** engineering judgement. Written 2026-10-06.

Related files:
- `filament-settings.md` section 0: the reference's start values.
- `README-tests.md`: what each STL is.
- `3mf-projects.md`: the ready-made projects.
- `tests-temp-stringing.md`, `tests-dimensional.md`, `tests-overhang-bridge-detail.md`: how to judge each test.
- `research/07-review-and-master-procedure.md`: Phases A–E.

---

## 1. What carries over: machine, family, filament

| Value | Where Studio stores it | Class | Carry to other PLAs | Carry to PETG | Reasoning |
|---|---|---|---|---|---|
| Machine calibration: ABL, vibration compensation, motor-noise cancellation; belts | printer | **MACHINE** | yes | yes | Mechanics only. Re-run after a move, a firmware update or a nozzle swap |
| Plate type selection and first-layer Z (`G29.1 Z-0.02` on Textured PEI) | printer start G-code | **MACHINE** | yes | yes | No per-filament Z offset exists on the A1. On the first PETG print, check that the first layer is not over-squished. PETG dislikes a heavy squish [I] |
| First-layer squares result (`dim01`) | none (a pass/fail check) | **MACHINE** (per nozzle) | yes | yes | Same reasoning. Re-run per nozzle |
| Elephant-foot compensation (0.075 default) | **process** | **MACHINE** (process) | yes | yes, but check `dim05` once | It depends on first-layer squish and bed temperature. PETG at 70 °C bed can bulge more [I]. It is a process setting, so a per-filament value would need its own process preset |
| X-Y hole / contour compensation | **process** | **MACHINE** (process) | yes | yes, but check `dim03` once | Mostly line width, seam, PA and cornering, so machine and process. Filament changes it a little through die swell and shrinkage. The Bambu wiki calls it per-filament, but Studio stores it in the process. Keep one value per nozzle unless a filament proves otherwise |
| Speeds, accelerations, line widths, wall order, seam, VFA / outer-wall speed | process | **MACHINE** | yes | yes | Not filament properties. MVS caps them per filament |
| Nozzle temperature | filament | **FAMILY** (offset) | as **T_ref + Δ** | **no**: tower | Within PLA the melt behaviour is similar, so a label- and profile-based delta is predictive. PETG is a different polymer |
| Bed temperature | filament | **FAMILY** | same value | no (70 °C) | PLA Tg about 55–60 °C, PETG about 80 °C |
| Fan min/max, overhang fan, first-layer fan off, slow-down layer time | filament | **FAMILY** | same (Rapid PLA+: max 100) | no (PETG presets) | Cooling need is set by Tg and viscosity, which PLAs share. PETG needs far less fan for layer bonding |
| Retraction length/speed, Z-hop type, wipe | filament override / printer | **FAMILY** | same baseline, then a stringing check | no (PETG test) | PLAs string similarly on a direct drive. PETG strings and oozes much more |
| Max volumetric speed | filament | **FAMILY** (ratio, low confidence) | as **MVS_ref × r** | no (test) | It scales with melt viscosity and temperature, but the sources disagree on the ratios (§3). Too low only slows prints, so use the conservative end |
| Pressure advance K | Device tab / filament | **FILAMENT-SPECIFIC** (seeded by a ratio) | auto FD on 0.4 always; on 0.2 a manual PA in a range narrowed by **K_ref × r** | no (test) | It depends on viscosity, compressibility and temperature of the actual spool. Auto FD on 0.4 costs 5 min and no plate, so measure it; never predict it on 0.4 |
| Flow ratio | filament | **FILAMENT-SPECIFIC** (seeded by a delta and a diameter correction) | fine pass always, centred on the prediction | no (coarse + fine) | It depends on true diameter (squared), density and die swell, which differ per spool and colour. A 0.02 mm diameter error alone is about ±2.3 % flow |
| Shrinkage (XY) | filament | **FILAMENT-SPECIFIC** | the reference value is acceptable for non-precision parts; run `dim02` for precision parts | no (`dim02`) | It depends on the polymer, crystallinity and filler. A matte filler lowers shrinkage, so the reference may shrink *less* than plain PLA [I]. PETG differs |
| Density, cost, spool weight | filament | data entry | per spool | per spool | From the label: PLA 1.26, PLA+ 1.30, Rapid PLA+ 1.23 [V Elegoo spec via research/10] |
| Drying | — | **FAMILY** | 50 ± 5 °C 8 h | 60–65 °C 8–12 h | Elegoo spec per line |

**PETG gets only the MACHINE rows.** Do not offset PETG temperature, flow, K, MVS, fan or retraction from PLA numbers.

---

## 2. Reference calibration: ELEGOO Matte PLA (purple)

### 2.1 Before you start (both nozzles)
1. Phase A and Phase B of `research/07` on the installed nozzle: machine calibration with all three ticked, the correct plate type, the nozzle set on the printer.
2. Preferences > **Developer mode** on. It is needed for the Temperature, MVS and Retraction tests and the PA pattern.
3. Dry the spool at 50 °C for 8 h [S]. Record the **colour name, lot number and spool weight**.
4. **Measure the filament diameter**: 10 points over about 5 m, both axes, and write down the mean d_ref. Every derived flow ratio uses it (§3.3).
5. Create the user preset from `filament-settings.md` section 0, for example `ELEGOO Matte PLA Purple REF @A1 0.4`.
6. After **every** developer-menu test, start a new project (File > New) before saving a preset [V wiki].

Project files are `3mf/<n>/<stl name>.3mf` (for example `3mf/0.4/temp_tower_230-190_0.4.3mf`). The dimensional combo plate is `3mf/<n>/dim-combo_02-03-05_<n>n.3mf`. Open each one as a project, then switch filament 1 to the reference preset (`3mf-projects.md`, "Using your own filament preset"). If a project is missing, slice the STL from `stl/<n>/` with the per-object settings listed in `3mf-projects.md`.

### 2.2 Order: 0.4 nozzle first, then 0.2

| # | Step | 0.4 file / tool | 0.2 file / tool | Record |
|---|---|---|---|---|
| R1 | First layer | `dim01_first-layer-squares_0.4n_h0.20` | `dim01_first-layer-squares_0.2n_h0.10` | pass / notes |
| R2 | Temperature tower (set the preset temp to 230 before slicing) | `temp_tower_230-190_0.4` | `temp_tower_compact_230-190_0.2` (project `R2_matte-purple_temp_tower_compact_230-190_0.2`: 28.8 x 9 x 36.6 mm, about 1 h 10 min, same 230 → 190 range) | **T_ref** and the usable window **T_min…T_max** (coldest block that bonds, hottest with acceptable bridge, overhang and gloss) |
| R3 | Flow Dynamics, provisional | Calibration tab > Flow Dynamics > **Auto** | Calibration tab > Flow Dynamics > **Manual**, range 0→0.20 step 0.01 | K (provisional) |
| R4 | Flow ratio, coarse then fine (read the matte surface as in §2.3) | Calibration tab > Flow Rate > Manual | same | **FR_ref** |
| R5 | Max volumetric speed at T_ref (MVS = start + height × step; use 90 %) | Dev menu > Calibration > More > Max flowrate, 10→24 step 1 | same, 1.0→5.0 step 0.25 | **MVS_ref** |
| R5b | *Reference extra:* MVS again at T_ref + 10 °C | same | optional | **s = (MVS₊₁₀ − MVS_ref)/10** in mm³/s per °C (used to correct derived MVS for temperature) |
| R6 | Flow Dynamics, final, at the final temperature and MVS. Assign it to the AMS-lite slot | Auto → **K_ref,auto** | Manual: first 0→0.20 step 0.01, then ±0.03 step 0.005 → **K_ref,0.2** | K |
| R6b | *Reference extra:* one manual PA pattern | Dev menu > Pressure advance > Pattern, 0→0.08 step 0.002 → **K_ref,man** | — | the auto/manual ratio. Shows how much auto inflates K on this printer |
| R7 | Stringing, plus the *reference extra*: the full retraction coupon series | `stringing_pins_0.4`, then `retraction_coupon_0.4` at 0.4 / 0.6 / 0.8 / 1.0 / 1.2 mm | `stringing_pins_0.2`, coupons at 0.3 / 0.4 / 0.6 / 0.8 / 1.0 / 1.2 | **R_min** (shortest clean length) and the chosen length (R_min + 0.1–0.2) |
| R8 | Cooling baseline | `overhang_angles_0.4`, `bridge_spans_0.4` | `overhang_angles_0.2`, `bridge_spans_0.2` | the steepest clean overhang, the longest clean bridge, the fan values used |
| R9 | Dimensional plate (dim02 + dim03 + dim05) | `dim-combo_02-03-05_0.4n` | `dim-combo_02-03-05_0.2n` | shrinkage k, contour change dC, hole change dH, elephant foot. Put dC, dH and EF in a **user process preset** (for example `0.20mm Standard @A1 – cal`). Put shrinkage in the filament preset |
| R10 | Fit check | `dim04_fit-clearance-D6_0.4n` | `dim04_fit-clearance-D3_0.2n` | g_slip, g_run |
| R11 | Optional detail | `min_feature_0.4` | `min_feature_0.2` | smallest wall, pin and hole |
| R12 | Verification, presets unchanged | `verify_combo_0.4` | `verify_combo_0.2` | pass on every row (`tests-overhang-bridge-detail.md` §4) |

Rough time: 0.4 about 7–9 h of printing, 0.2 about 10–14 h. Between the two blocks, swap the nozzle, set it on the printer, re-run machine calibration, and print `dim01` again.

**Before the 0.2 block, finish §4 for every derived PLA on the 0.4**, and the PETG full runs too if you want. Then you swap nozzles only once. Their *measured* 0.4 deltas also improve the 0.2 predictions (§5).

### 2.3 Reading flow ratio on a matte top surface
Bambu's wiki method compares gloss and smoothness under raking light. A matte filler scatters light, so over- and under-extruded blocks look equally dull, and a pastel purple shows little shadow. Instead:
1. **Raking light, very low.** Hold a phone torch at about 5–10° above the surface, **at right angles to the top-infill lines**, in a dark room. Look for dark gaps between lines (too low) and bright ridges or a ploughed edge at the far side of each line (too high). Rotate the plate 90° and look again.
2. **Pencil rub.** Rub a soft pencil (2B) flat and lightly across each block in one direction. Graphite marks only the high points.
   - Pale lines between grey stripes: under-extruded.
   - Even grey: correct.
   - Heavy grey ridges and smearing along the wall edge: over-extruded.
   - Graphite wipes off PLA with a damp cloth or isopropyl alcohol.
3. **Edges.** Check with a loupe or phone macro where the top infill meets the walls. A gap there means the flow is low. A raised lip along the wall means the flow is high.
4. **Touch.** Run a fingernail across the lines. Ridges catch.
5. **Tie rule.** In the coarse pass, if two blocks tie, take the **higher** one, because the fine pass can only go lower [V wiki].

### 2.4 Reference results log (fill in once, keep with the presets)

| Quantity | Symbol | 0.4 measured | 0.2 measured | Notes |
|---|---|---|---|---|
| Colour / lot / date / firmware / Studio version | — | | | |
| Filament diameter, mean of 10 | d_ref | | (same spool) | |
| Nozzle temp, chosen | T_ref | | | |
| Usable window | T_min…T_max | | | |
| Bed temp (plate) | — | | | |
| Flow ratio | FR_ref | | | coarse result → fine result |
| Max volumetric speed (90 % value) | MVS_ref | | | raw knee: |
| MVS at T_ref + 10 | MVS₊₁₀, slope s | | | |
| K, auto (0.4) / manual (0.2) | K_ref | | | |
| K, manual pattern (0.4) | K_ref,man | | — | auto/manual = |
| Retraction: shortest clean / chosen | R_min / R_ref | | | |
| Fan min/max/overhang used, verdict | — | | | |
| Steepest clean overhang / longest clean bridge | — | | | |
| Shrinkage (XY) | k | | | |
| X-Y contour compensation | dC | | | process preset |
| X-Y hole compensation | dH | | | process preset |
| Elephant foot | EF | | | process preset |
| Fit: slip / running clearance | g_slip / g_run | | | |
| verify_combo | pass/fail | | | |

---

## 3. Offset table: predicted start values for the derived filaments

Symbols are the reference results from §2.4 for the **same nozzle**. Clamp every temperature to the filament's label range. "Use" is the value to type into the preset before the confirmation checks. The range is the band the prediction is expected to fall in, and it doubles as the acceptance band in §4.

### 3.1 0.4 nozzle

| Filament (label °C) | Nozzle temp | Max volumetric speed | Flow ratio (before the fine-pass shift in §4) | K (auto FD band to accept) | Fan / retraction / bed | Base for "Save as" |
|---|---|---|---|---|---|---|
| **ELEGOO PLA** (190–230 [V]) | **T_ref + 0** (−5…+5); medium confidence | **MVS_ref × 0.9** (0.85–1.3); low | **FR_ref × (d_ref/d)²** ±0.02; medium-low | K_ref × 1.0 (0.75–1.3) | same as ref | copy of the ref preset |
| **ELEGOO PLA+** (200–230 [S]) | **T_ref + 10** (+5…+15, max 230); medium | **MVS_ref × 0.75 + s × ΔT** (0.73–1.25); low. Measure it | **FR_ref × (d_ref/d)² − 0.03** (−0.05…0); low | K_ref × 1.25 (1.0–1.6) | same as ref; dry first (stringing) | copy of the ref preset |
| **ELEGOO Rapid PLA+** (200–230 [V]) | **T_ref + 10** (+5…+15, max 230), plus 5 for fast prints; medium | **MVS_ref × 1.15 + s × ΔT** (1.14–1.5); low. Measure it | **FR_ref × (d_ref/d)²** ±0.02; medium | K_ref × 0.8 (0.6–1.0) | fan max **100**; retraction same as ref | copy of the ref preset (MVS overridden anyway; Generic PLA High Speed differs from Generic PLA mainly in MVS [V]) |
| **Keytek PLA** (220–240 [S]) | **max(T_ref + 15, 220)** (+10…+25); **low**: run a tower | **MVS_ref × 0.9** (0.7–1.2); low | **FR_ref × (d_ref/d)²** ±0.03; low | K_ref × 1.0 (0.7–1.4) | same as ref; dry first | copy of the ref preset |
| **ELEGOO PETG PRO** (230–260 [S]) | **not offset**: section 5 start 240 + tower | not offset | not offset | not offset | PETG presets | `Generic PETG @BBL A1` (section 5) |
| **ELEGOO Rapid PETG** (240–270 [S]) | **not offset**: section 6 start 250 + tower | not offset | not offset | not offset | PETG presets | `Generic PETG HF @BBL A1` (section 6) |

ΔT is the derived temperature minus T_ref. s is the MVS-per-°C slope from step R5b. Without R5b, use s ≈ 0 and accept the bias toward low MVS.

### 3.2 Basis and confidence of each delta

**Temperature.** It combines three independent signals.

| Filament | Label midpoint vs Matte (210) | Elegoo's own Orca profiles vs Matte (220, inherited) | A1 community | → Δ used |
|---|---|---|---|---|
| ELEGOO PLA | 210 → 0 | 210 → −10 | 205–215 (215 for all colours) [S] | **0** |
| PLA+ | 215 → +5 | 220 → 0 | 230 [S] | **+10** |
| Rapid PLA+ | 215 → +5 | 220 → 0 | 230 [S] | **+10** |
| Keytek | 230 → +20 | none | none | **+15**, floor 220 (label minimum) |

- Elegoo's matte profiles never set a temperature. They inherit 220 from the Orca root, so that column is weak evidence.
- PLA+ has the lowest melt index of the group (6.9 vs Matte 9.4), so it needs more heat at the same flow.
- Confidence:
  - Medium for the ELEGOO PLAs: same manufacturer, same label floor or 10 °C higher.
  - Low for Keytek: retailer label only, 220–240 is unusually hot for a standard PLA, and there is no profile data.

**Max volumetric speed.** Two sources point in opposite directions, so the ratios are low confidence.

| Filament | Melt index ratio vs Matte (9.4) [S] | Elegoo Orca MVS ratio vs Matte (16) [V profile] |
|---|---|---|
| PLA | 8.1 → 0.86 | 21 → 1.31 |
| PLA+ | 6.9 → 0.73 | 20 → 1.25 |
| Rapid PLA+ | 10.7 → 1.14 | 21 → 1.31 |

- Bambu's own matte preset (22) is *higher* than its PLA Basic (21) [V], which contradicts Elegoo's 16 vs 21. The filler effect on MVS is not established.
- The "use" column sits at the conservative end of each band. An MVS that is too low only slows the print; one that is too high under-extrudes walls.
- MVS rises with temperature. A derived filament printed 10 °C hotter than the reference gets the `s × ΔT` term.
- Keytek has no data, so it gets 0.9 [I].

**Flow ratio.** The flow ratio corrects the volume the slicer assumes (1.75 mm nominal) to what actually comes out.
- The diameter term `(d_ref/d)²` is physics. With both spools measured on the same calipers, it carries the reference's correction over exactly. Example: d_ref 1.74, d 1.76 gives ×0.977.
- The remaining delta covers die swell, density and pigment. These are filament-specific:
  - PLA+ −0.03: an A1 community calibration gave 0.94 on PLA+ White vs the usual 0.97–0.98 [S]. That is a single source, so confidence is low.
  - Rapid PLA+ 0: community 0.99 [S].
  - ELEGOO PLA 0: community 0.98–1.02 [S].
  - Keytek ±0.03: budget diameter tolerance [I].
- **The flow ratio is always confirmed with a fine pass.**

**K.**
- Higher melt viscosity gives more pressure lag and therefore a higher K.
- The ratios come from the A1 community values relative to typical plain PLA on the A1 (manual about 0.035, auto higher):
  - PLA+ about 0.04 → ×1.25
  - Rapid PLA+ about 0.022 → ×0.8 [S, single sources]
- On the 0.4, auto FD measures K directly in 5 minutes. The ratio is only used to **flag a suspicious auto result**, a value outside the band.

**Fan, retraction, bed.** These are family values [V]: every Bambu and Elegoo PLA preset involved uses 60/80 fan, 0.8 mm retraction and 60–65 °C plates. The exception is Rapid PLA+, where Elegoo's own profile uses max 100 [S]. Confidence is high that they are adequate. A stringing check confirms them.

**Shrinkage, XY compensation, elephant foot.**
- Shrinkage: use the reference value. If the reference measured k within 0.15 % of 100, leave all derived filaments at 100 % (`tests-dimensional.md` rule).
- X-Y and elephant-foot compensation live in the process preset, so every filament shares them automatically.

---

## 4. Confirmation checks per derived filament

### 4.1 The core check (every derived PLA, 0.4): about 1.5 h, 4 prints
1. **Diameter:** 10 points (5 min). Compute FR_pred from §3.1.
2. **Auto Flow Dynamics** at the predicted temperature (5 min, nothing printed on the plate). **Accept** if K is inside the §3.1 band. If it is outside, re-run once. If it is still outside, run a manual PA pattern, 0→0.08 step 0.002.
3. **Flow ratio, fine pass only**: Calibration tab > Flow Rate > "Fine calibration based on flow ratio".
   - The fine pass only tests 91–100 % of the preset value, so it can only *lower* the ratio. Set the preset to **FR_pred + 0.04** before running it. The ten blocks then cover about FR_pred − 0.05 … FR_pred + 0.04.
   - **Accept** if the best block is not at either end and the result is within the §3.1 band of FR_pred.
   - If the best block is at an end, run the coarse pass.
4. **`stringing_pins_0.4`** at the predicted temperature and the reference retraction. **Accept:** no strings, or only a few fine hairs that brush off (`tests-temp-stringing.md` §2a).
5. **`verify_combo_0.4`** with the saved presets unchanged. **Accept** if every row of the table in `tests-overhang-bridge-detail.md` §4 passes. Add a layer-bond check: snap the cylinder off by hand. A ragged break or a break at the base is fine. A clean split along a layer line means the temperature is too low.

### 4.2 Extras per filament
| Filament | Extra checks (0.4) | Skip |
|---|---|---|
| ELEGOO PLA | none. Repeat steps 2–3 for each new colour; this line is colour-sensitive [S] | tower, MVS (unless you print fast) |
| PLA+ | **MVS test** at the chosen temperature (dev menu, 10→25 step 1), 25 min. Dry before testing (stringing) | tower, unless the snap check or the overhangs fail |
| Rapid PLA+ | **MVS test** (14→30 step 1), always: high flow is the reason to buy it. If you print fast, run `verify_combo` with your fast process too, and add +5 °C if walls look under-melted | tower |
| Keytek PLA | **Temperature tower `temp_tower_240-205_0.4`** (the label is the weakest data). Dry first | coarse flow, unless the fine pass hits an end |
| PETG PRO / Rapid PETG | no shortcut: dry, then steps 2–11 of `filament-settings.md` §7 (tower `260-230` / `270-240`, FD, coarse + fine flow, MVS, stringing and retraction, overhang/bridge for fans, `dim-combo`, `dim04`, verify). From the reference they inherit only the MACHINE rows of §1. `dim05` and `dim03` in the combo confirm elephant foot and XY compensation at 70 °C bed | — |

### 4.3 When to fall back to the full calibration
- Two or more of the core checks fail → run the full `filament-settings.md` §7 order for that filament.
- The flow fine pass lands at an end twice, or differs from FR_pred by more than 0.05 → the coarse + fine pass. Also check the diameter readings and whether the spool is dry.
- The auto K is outside its band on two runs, and a manual pattern agrees with the auto value → keep the measured K (the prediction was wrong, not the filament). Note it in §6.
- `verify_combo` fails on adhesion, the 60° overhang or the bridge → temperature tower for that filament.
- Strings after drying → retraction coupon series.
- Precision or fit parts → `dim-combo_02-03-05` and `dim04` for that filament. Shrinkage and fit are not predicted to better than about ±0.2 %.
- New brand, new line, or a lot whose diameter differs from the old lot by more than 0.02 mm → treat it as a new filament.

---

## 5. How the 0.2 values relate to the 0.4 values

| Value | Transfers 0.4 → 0.2? | How |
|---|---|---|
| Machine calibration, plate, first layer | **no** | re-run after the swap (machine calibration + `dim01_…_0.2n_h0.10`) |
| Elephant foot, X-Y hole/contour compensation | **no** | separate process preset per nozzle (line width 0.22 vs 0.42). Measure with the reference on `dim-combo_02-03-05_0.2n` |
| Nozzle temperature | **as an offset** | Tower doc: the 0.2 usually runs about 5 °C lower. The reference measures it (T_ref,0.2). Derived: **T_x,0.2 = T_ref,0.2 + (T_x,0.4 − T_ref,0.4)**, using the *measured* 0.4 temperatures |
| Bed temperature, fan % | **yes** | same values. The 0.2 slow-down layer time stays 6–8 s |
| Flow ratio | **partly** | The diameter and material part carries over, the line-geometry part does not. **FR_x,0.2 ≈ FR_ref,0.2 + (FR_x,0.4 − FR_ref,0.4)**, then a fine pass (§4.1 step 3) on every filament |
| K | **as a ratio only** | Absolute K is 2–5× higher on a 0.2 [S forum], and auto FD is unreliable on the 0.2 [V wiki]. **K_x,0.2 ≈ K_ref,0.2 × (K_x,0.4,auto / K_ref,0.4,auto).** Using the ratio of two auto values cancels most of the auto-inflation. Then run a manual pattern over **K_pred ± 40 %, step 0.005** instead of the full 0→0.20 sweep. Print-dialog Flow Dynamics stays **Off** on the 0.2 |
| MVS | **weakly** | The 0.2 is limited by pressure drop, not melt capacity, so ratios compress. **MVS_x,0.2 ≈ MVS_ref,0.2 × r^0.5** (r from §3.1) [I], capped at 3.0 (`filament-settings.md`: more MVS raises the needed K). Run the test only if you print 0.2 infill fast |
| Retraction | **no** | the reference measures R_min,0.2. Derived PLAs use it plus `stringing_pins_0.2`. Rapid PLA+ is expected in the upper half [I] |
| Shrinkage | **yes, mostly** | It is a material property. Check with the 0.2 reference `dim02`. Derived filaments inherit it |
| PETG anything | **no** | full calibration on the 0.2 as well (manual PA, coarse 0→0.30 step 0.02). The reference's K_0.2/K_0.4 ratio may centre the coarse sweep, but do not narrow it |

0.2 confirmation per derived PLA:
1. Diameter is already known.
2. Manual PA over the narrowed range.
3. Flow fine pass with the +0.04 shift.
4. `stringing_pins_0.2`.
5. `verify_combo_0.2`.

The acceptance rules are the same as §4.1, with K accepted if the pattern's best line is inside the narrowed range and not at its edge.

---

## 6. Worksheet (copy one block per filament and nozzle)

```
Filament: ____________________  Colour/lot: ____________  Nozzle: 0.4 / 0.2   Date: ________
Diameter (mean of 10): d = ______   (reference d_ref = ______)   Dried: ___ °C ___ h
```

| Quantity | Reference value (§2.4) | Rule (§3 / §5) | Predicted / start | Check used | Measured | In band? | Saved value |
|---|---|---|---|---|---|---|---|
| Nozzle temp (°C) | | T_ref + Δ | | verify_combo snap / tower | | | |
| Bed temp (°C) | | same | | first layer | | | |
| Max vol. speed (mm³/s) | | MVS_ref × r + s·ΔT | | MVS test / none | | | |
| Flow ratio | | FR_ref·(d_ref/d)² + δ | | fine pass from FR_pred + 0.04 | | | |
| K | | K_ref × r | | auto FD (0.4) / manual ±40 % (0.2) | | | |
| Fan min/max/overhang | | same (Rapid: max 100) | | verify_combo overhang/bridge | | | |
| Retraction (mm) | | R_ref | | stringing_pins | | | |
| Shrinkage (%) | | same | | dim02 (precision only) | | | |
| XY contour / hole / EF | | process preset (same) | | dim-combo (PETG once) | | | |
| verify_combo | — | — | — | all rows | pass / fail | | |
| Outcome | | | | | | | **accepted** / **fallback: ______** |

Summary table, one line per filament (fill in as you go):

| Filament | Nozzle | T | FR | K | MVS | Retraction | Checks passed | Fell back on | Date |
|---|---|---|---|---|---|---|---|---|---|
| ELEGOO Matte PLA purple (REF) | 0.4 | | | | | | full | — | |
| ELEGOO Matte PLA purple (REF) | 0.2 | | | | | | full | — | |
| ELEGOO PLA | 0.4 | | | | | | | | |
| ELEGOO PLA | 0.2 | | | | | | | | |
| ELEGOO PLA+ | 0.4 | | | | | | | | |
| ELEGOO PLA+ | 0.2 | | | | | | | | |
| ELEGOO Rapid PLA+ | 0.4 | | | | | | | | |
| ELEGOO Rapid PLA+ | 0.2 | | | | | | | | |
| Keytek PLA | 0.4 | | | | | | | | |
| Keytek PLA | 0.2 | | | | | | | | |
| ELEGOO PETG PRO blue | 0.4 | | | | | | full | — | |
| ELEGOO PETG PRO blue | 0.2 | | | | | | full | — | |
| ELEGOO Rapid PETG clear | 0.4 | | | | | | full | — | |
| ELEGOO Rapid PETG clear | 0.2 | | | | | | full | — | |

**Refine the offsets as you go.** After each confirmed filament, write its *measured* Δ or ratio against the reference into a copy of §3.1. Over time those replace the literature-based numbers. If a filament keeps failing its band, the band was wrong, not the filament.

---

## 7. Sources for the ELEGOO Matte PLA values
- Bambu Studio presets (GitHub `bambulab/BambuStudio`, master, read 2026-10-06), `resources/profiles/BBL/filament/`:
  - `Bambu PLA Matte @base.json`, `@BBL A1.json`, `@BBL A1 0.2 nozzle.json`: density 1.32, flow 0.98, MVS 22 / 2, fan 60/80, plates 65, long retraction when cut 18 mm, slow-down 6 s; temperature 220 inherited from `fdm_filament_pla.json`.
  - Also present: `Overture Matte PLA @BBL A1` (MVS 16 / 0.2: 1.8) and `SUNLU PLA Matte @BBL A1` (MVS 21 / 0.2: 2). No Elegoo matte preset exists in Bambu Studio. [V]
- OrcaSlicer, Elegoo vendor profiles (`SoftFever/OrcaSlicer`, main), `resources/profiles/Elegoo/filament/`:
  - `BASE/Elegoo PLA Matte @base.json` (inherits `Elegoo PLA @base`, MVS 16, no temperature set).
  - `ECC`, `ECC2`, `EC2`, `EN4SERIES` matte profiles: MVS 16, fan 60/80, textured 65 / smooth 60, slow-down 6, PA 0.024 (ECC) / 0.04 (ECC2, EC2), density 1.25.
  - `ELEGOO_02_NOZZLE/Elegoo PLA Matte @0.2 nozzle.json`: MVS 2.
  - For comparison, `ECC/Elegoo PLA @ECC.json`: MVS 21, 210 °C. [V for the profiles]
- Spec copies of Elegoo's datasheet: Memory Express listings (for example https://www.memoryexpress.com/Products/MX00136265, search extract: 190–230 °C, bed 35–65 °C, dry 50 ± 5 °C 8 h, ≤ 20 % RH, MI 9.4 ± 1.2 g/10 min, 1.26 g/cm³, melting 163 °C, Vicat 63 °C, < 300 mm/s); 3DJake https://www.3djake.ch/de-CH/elegoo/pla-matte-navy-blue-1 (fetched: 190–230 °C, bed 50–65 °C); printer-hub.ru https://printer-hub.ru/materials/elegoo-pla-matte (fetched: 190–230 °C, bed 50–60 °C, 60–150 mm/s). [S]
- Elegoo product page https://eu.elegoo.com/products/pla-matte-filament-1-75mm-colored-1kg: HTTP 429 on every Elegoo domain today. Re-check the label values against it, or against the spool label.
- No A1-specific community profile for ELEGOO Matte PLA was found (MakerWorld, Bambu forum and Reddit searches). The other filaments' sources are in `research/10`, `11`, `12`.
