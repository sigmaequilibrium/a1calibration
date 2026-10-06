# 12 - ELEGOO PETG family (blue PETG + clear Rapid PETG) on Bambu A1, 0.2 / 0.4 nozzles

Scope: Bambu Lab A1 (open frame) + AMS lite, Bambu Studio, FW 01.08.01.00+, hotends 0.2 mm and 0.4 mm.
Filaments: **ELEGOO PETG (blue)** and **ELEGOO Rapid PETG (Transparent/clear)**.

Tags: **[S]** = sourced (URL in Sources), **[S-BBL]** = value read directly from Bambu Studio's system profile JSON on GitHub (master, fetched 2026-10-06), **[C]** = community report (single user / forum), **[I]** = my inference / engineering judgement. Conflicts are marked **CONFLICT**.

---

## 0. Identify your "ELEGOO PETG (blue)" spool first (CONFLICT / ambiguity)

Elegoo has sold several PETG lines and the label matters because the specs differ:

| Line | Nozzle | Bed | Speed | Melt index | Notes |
|---|---|---|---|---|---|
| Legacy "ELEGOO PETG" (no suffix) | 220-250 °C, "recommended 230 °C" [S: retailer copy of Elegoo listing] | **75-90 °C** [S] | "30-600 mm/s" (retailer copy; implausible for legacy PETG) | 13-15 g/10 min | No longer on Elegoo's own store (handle 404s) [S] |
| ELEGOO **PETG PRO** (current "standard" PETG, has Blue) | **230-260 °C** [S] | **65-75 °C** [S] | < 270 mm/s [S] | 8.2 ± 3.2 | Dry 60 ± 5 °C 8 h; glue "Recommended" [S] |
| ELEGOO **Rapid PETG** (has Blue *and* Transparent) | **240-270 °C** [S] | **65-75 °C** [S] | < 600 mm/s [S] | 13.4 ± 3.8 | Dry 60 ± 5 °C 8 h; glue "Recommended"; storage ≤ 20 % RH [S] |
| (for reference) ELEGOO PETG Translucent | 230-260 °C | 65-75 °C | < 220 mm/s | 16.3 ± 1.7 | not one of the user's spools |
| (for reference) ELEGOO PETG HF | 230-260 °C | 65-75 °C | < 600 mm/s | 20.5 ± 1.2 | not one of the user's spools |

- Rapid PETG product page lists both a **"Blue"** and a **"Transparent"** variant [S]. The user's clear spool = Rapid PETG Transparent. The blue spool could be legacy PETG, PETG PRO, or even Rapid PETG Blue - **check the spool label/box** before using the numbers below. This doc assumes blue = legacy PETG / PETG PRO ("standard PETG") and gives the union range where they differ.
- Melt index (higher = runnier): standard PETG PRO 8.2 vs Rapid 13.4 [S] -> Rapid should reach a noticeably higher max volumetric speed and wets out more easily (good for clarity) [I].
- Elegoo publishes no official Bambu Studio profile that I could find; MakerWorld community profiles exist (e.g. "Elegoo Rapid PETG - Optimized Profile", model 1125246) but MakerWorld returned 403 to fetching, so their values are not used here.

---

## 1. Bambu Studio base profile to inherit

| Spool | Recommended base | Why |
|---|---|---|
| ELEGOO PETG / PETG PRO (blue) | **Generic PETG** [I] | Neutral PETG base, flow 0.95, conservative. PETG PRO is not a high-flow resin (MI 8.2), so PETG HF's 18 mm³/s would be too optimistic. Community X1C profile for PETG PRO was built on generic-style values (flow 0.95, 40-90 % fan, 18 mm³/s) [C]. |
| ELEGOO Rapid PETG (clear) | **Generic PETG** [S/C] (the main Bambu-forum Rapid PETG recipe started from "Generic PETG Settings" [C]) | Then pull specific values (lower fan, 0.3 mm retraction) from **Bambu PETG Translucent @BBL A1** [S-BBL] and, for pure-clarity prints, from Bambu's transparent-PETG 3MF [S]. Alternative for speed-oriented opaque work: Bambu PETG HF base (Rapid is a "high-speed" PETG) [I]. |

Bambu system values worth knowing when you inherit (all **[S-BBL]**):

| Preset (A1) | Nozzle °C (first/other) | Textured & Smooth PEI bed °C | Max vol. speed mm³/s | Flow | Fan min/max % | Overhang fan | Fan off 1st layers | Retraction (filament override) | Other |
|---|---|---|---|---|---|---|---|---|---|
| Generic PETG @BBL A1 (0.4) | 255/255 | 80 | **8** | 0.95 | 40/90 | 90 % @ ≥10 % overhang | 3 | none -> printer 0.8 mm | range 220-270, min layer time 12 s |
| Generic PETG @BBL A1 **0.2 nozzle** | 255/255 | 80 | **1** | 0.95 | 40/90 | 90 % | 3 | none | same |
| Bambu PETG HF @BBL A1 (0.4) | 230/240 | 70 | 18 | 0.94 | 30/50 | 100 % | 3 | none | min layer time 7 s |
| Bambu PETG HF @BBL A1 0.2 | 230/240 | 70 | 1 | 0.94 | 30/50 | 100 % | 3 | none | |
| Bambu PETG Basic @BBL A1 (0.4) | 245/245 | 70 | 13 | 0.94 | 30/50 | 50 % | 3 (first-layer fan 0) | **0.4 mm**, Spiral Lift, wipe 1 mm | |
| Bambu PETG Basic @BBL A1 0.2 | **255**/255 | 70 | 1 | 0.94 | **20/35** | 90 % @ ≥25 % | 3 | none | Bambu raises temp and lowers fan for 0.2 |
| Bambu PETG Translucent @BBL A1 (0.4 and 0.2) | 250/245 | 70 | 6 (0.4) / 1 (0.2) | 0.95 | **10/30** | 90 % | 3 | **0.3 mm** | |

A1 printer defaults (machine profile, inherited by both 0.2 and 0.4) [S-BBL]: retraction 0.8 mm @ 30 mm/s, deretraction 30 mm/s, retraction minimum travel 1 mm, wipe on, wipe distance 2 mm, **z-hop 0.4 mm "Auto Lift"**. 0.2 nozzle machine profile: layer height 0.04-0.14 mm.
Generic/Bambu PETG profiles also carry AMS-dryer metadata 65 °C / 12 h [S-BBL] (relevant to AMS 2 Pro/HT, **not** the AMS lite, which cannot dry).

Note: Bambu's **1 mm³/s** cap on all 0.2-nozzle PETG presets is very conservative (a 0.2 nozzle, 0.1 mm layer, 0.22 mm line at 40 mm/s ≈ 0.9 mm³/s) - it effectively slows every 0.2 print to ~40-50 mm/s. Raise it only after a flow test [I].

---

## 2. Per-filament, per-nozzle starting values and test ranges

### 2A. ELEGOO PETG / PETG PRO (blue) - 0.4 mm nozzle

| Item | Value | Tag |
|---|---|---|
| Base | Generic PETG @BBL A1 -> save as "ELEGOO PETG Blue 0.4" | [I] |
| Manufacturer range | legacy 220-250 °C (230 rec.); PETG PRO 230-260 °C | [S] |
| Start nozzle | **240 °C** (first layer 245) | [I]; community PETG PRO on X1C 240/245 [C] |
| Temp tower | **255 -> 225 °C, 5 °C steps** (Bambu Studio Temperature cali, PETG preset) | [I] (covers both label ranges) |
| Bed | Textured PEI **70 °C** (first layer 70-75). Legacy label says 75-90 -> if corners lift go 75-80 | [S] ranges; start [I] |
| Max vol. speed | start **10 mm³/s**; test **5 -> 20, step 1** | [I] (Generic=8 [S-BBL]; PETG PRO community 18 on X1C [C]; MI 8.2 suggests below Rapid) |
| Flow ratio | start **0.95**; expect **0.92-0.98** | 0.95 [S-BBL]/[C]; range [I] |
| PA (K) | expect **0.02-0.06**; run Flow Dynamics auto-cali, verify with PA pattern/line 0-0.08 | [I]/[C] (PETG PRO community 0.02 on X1C; A1 extruder usually lands a bit higher) |
| Fan | min 30 / max 50 %, overhang 90 %, off for first 3 layers | [I] based on PETG Basic/HF A1 [S-BBL]; Generic 40/90 is high for PETG layer adhesion |
| Retraction | start **0.6 mm @ 30-40 mm/s**; test 0.2 -> 1.4 mm step 0.2 | A1 default 0.8 [S-BBL], PETG Basic 0.4 [S-BBL]; test [I] |
| Z-hop | 0.4 mm; try **Spiral Lift 0.2-0.4** (PETG Basic A1 uses Spiral) | [S-BBL]/[I] |
| Wipe | on, 1-2 mm; "wipe while retracting" | [S-BBL]/[I] |

### 2B. ELEGOO PETG / PETG PRO (blue) - 0.2 mm nozzle

| Item | Value | Tag |
|---|---|---|
| Base | Generic PETG @BBL A1 **0.2 nozzle** (separate preset; do not reuse the 0.4 one) | [S-BBL] |
| Start nozzle | **245 °C** (Bambu bumps PETG Basic to 255 for 0.2) | [S-BBL] trend; value [I] |
| Temp tower | **260 -> 230, step 5** (0.1 mm layers; small tower) | [I] |
| Bed | Textured PEI 70 °C | [S]/[I] |
| Max vol. speed | start **1.5 mm³/s**; test **0.5 -> 4.0, step 0.25** (expect usable 2-3.5) | Bambu preset 1 [S-BBL]; range [I] |
| Flow ratio | start 0.95; expect 0.92-1.00. Background tests (coarse 80-120 %, fine 91-100 %) apply; if the fine test lands on 100 % the true value may be > 1.00 -> rerun coarse | [I] |
| PA (K) | **manual** (auto-cali not reliable/available for 0.2). **CONFLICT**: forum reports for 0.2 nozzles range from 0.05 (PETG) to 0.1-0.45 (X1C/P1, mostly PLA). Do a **coarse PA line/pattern 0 -> 0.30 step 0.02**, then fine ±0.03 step 0.005 | [C]/[I] |
| Fan | min 20 / max 35 %, overhang 90 % (copy PETG Basic 0.2) | [S-BBL] |
| Retraction | 0.4-0.6 mm @ 30 mm/s (less melt volume in a 0.2 nozzle) ; test 0.2 -> 1.0 step 0.2 | [I] |
| Z-hop | 0.2-0.4 mm Spiral | [I] |
| Other | 0.2 nozzle + PETG partial clogs are common if filament is wet or temp too low; keep slow (outer wall ≤ 60 mm/s) | [I] |

### 2C. ELEGOO Rapid PETG Transparent - 0.4 mm nozzle

Two use-cases: **(a) functional/opaque-looking parts** and **(b) maximum clarity**. Calibrate (a) first; derive (b) as a process+filament variant.

| Item | (a) Functional | (b) Max clarity | Tag |
|---|---|---|---|
| Base | Generic PETG @BBL A1 | copy of (a) | [C]/[I] |
| Manufacturer range | 240-270 °C | 240-270 °C | [S] |
| Start nozzle | **250 °C** | **265-270 °C** (Bambu transparent 3MF: 270 °C) | [I] / [S] |
| Temp tower | **270 -> 240, step 5** | n/a (use top of the passing window) | [I] |
| Bed | Textured PEI 70 °C (first layer 70-75) | same; for glossy clear bottom use smooth PEI **with glue** | [S]/[I] |
| Max vol. speed | start **14 mm³/s**; test **8 -> 26, step 2** | irrelevant: all speeds 20 mm/s (~1 mm³/s) | community 16 (post-cal) to 24 [C]; Bambu transparent 3MF 13 [S] |
| Flow ratio | start **0.95**; expect 0.93-1.00 | **+3-6 % over calibrated** (Bambu: 1.01) | 0.95 [C]; 1.01 [S]; 1.05-1.07 used by one X1C user for strength at 265-270 °C [C] |
| PA (K) | expect **0.02-0.05** (community A1-mini/X1 Rapid: **0.030**) | 0.02 (Bambu 3MF) - low importance at 20 mm/s | [C]/[S] |
| Fan | min 10-20 / max 30-40 %, overhang 90 %, off first 3 layers | **0 %** (all fans off) | Translucent preset 10/30 [S-BBL]; Rapid users 30 % max [C], 30-40 % [C]; 0 % [S] |
| Retraction | start **0.4 mm** (Translucent preset 0.3) @ 30-45 mm/s; test 0.2 -> 1.2 step 0.2 | same | [S-BBL]/[C] (45 mm/s [C]) |
| Z-hop | 0.4 Auto/Spiral | 0 or minimal (few travels anyway) | [I] |
| Process | normal | 0.1 mm layers, 0.5 mm line width, **1 wall**, **0 top/0 bottom shells**, **100 % aligned rectilinear infill at 0° (or 90°)**, all speeds **20 mm/s**; Bambu recommends a 0.8 nozzle for best clarity | [S] (Bambu wiki + 3MF) |

### 2D. ELEGOO Rapid PETG Transparent - 0.2 mm nozzle

| Item | Value | Tag |
|---|---|---|
| Base | Generic PETG @BBL A1 0.2 nozzle; copy fan 10/30 and retraction 0.3 from Bambu PETG Translucent @BBL A1 0.2 | [S-BBL] |
| Start nozzle | **250-255 °C**; tower **270 -> 240 step 5** | [I] |
| Bed | Textured PEI 70 °C | [I] |
| Max vol. speed | start **2 mm³/s**; test **0.5 -> 4.5 step 0.25** (Rapid's higher MI may allow ~0.5 more than blue) | Bambu 1 [S-BBL]; rest [I] |
| Flow ratio | 0.95 start, expect 0.93-1.00 | [I] |
| PA (K) | manual, coarse 0 -> 0.30 step 0.02 then fine (same CONFLICT as 2B) | [C]/[I] |
| Fan | 10-30 % | [S-BBL] |
| Retraction | 0.3-0.5 mm @ 30 mm/s | [S-BBL]/[I] |
| Clarity note | a 0.2 nozzle is the **worst** choice for transparency (many thin lines = many interfaces). Use 0.2 + clear only for fine detail; for clarity use 0.4 (or 0.6/0.8) | [S] (Bambu: larger nozzle -> fewer seams) |

---

## 3. Bed / build plate

- **Textured PEI preferred** for both. Bambu: textured PEI needs no glue for PETG; smooth PEI needs glue stick/liquid glue [S - Bambu forum summarising Bambu guidance]. Elegoo lists "Textured/Smooth PEI or Other Plates" with **glue "Recommended"** [S].
- **WARNING - Smooth PEI:** PETG can bond to smooth PEI so strongly that it **tears chunks out of the PEI** on removal. Always use glue stick (Bambu glue) as a release layer on smooth PEI; let the plate cool fully before removal [S]. Even textured PEI can over-bond with PETG; wipe with dish soap/water (not just IPA) and let it cool, or use glue there too if it leaves residue [S]/[C].
- Bed temp: Elegoo 65-75 °C (PETG PRO / Rapid) vs legacy PETG 75-90 °C vs Bambu Generic 80 °C vs Bambu Basic/HF 70 °C. **CONFLICT** resolved by starting at 70 °C and raising to 75-80 only for warping on large parts (one A1 user reported real bed ~10 °C under target and needed 80 °C) [C]. A1 is open-frame -> large flat PETG parts may need a brim [I].

---

## 4. Drying and storage (both spools)

- Elegoo: **60 ± 5 °C for 8 h** before use; "Drying before Use: Required"; print/store at **≤ 20 % RH** sealed with desiccant [S].
- Bambu profile metadata: 65 °C / 12 h [S-BBL]. Bambu transparency guide: dry first, moisture -> bubbles/voids that kill clarity [S].
- Forum: Rapid PETG users dried 10 h, 12-24 h; one still got "zits" after 24 h and gave up on the brand [C]. Another got "very little stringing right out of the package" [C] -> batch variation.
- Recommended: 65 °C x 8-12 h in a dryer (not above ~70 °C; Vicat 70 °C [S]); re-dry clear spool before every clarity print [I].

## 5. AMS lite notes

- AMS lite is open to room air with **no drying**; PETG left in it for days re-absorbs moisture -> stringing, zits, cloudy clear prints. For long or clarity prints, feed from a dry box or keep spool in AMS lite only during the job [I].
- Rapid PETG ships on a **cardboard/paper spool** (retailer listings, 1 kg) [S]; AMS lite generally tolerates cardboard spools but they can shed fibres/slip - check rotation, or respool [I].
- Colour swaps **blue -> clear** need very large purge: any blue residue tints clear parts. Increase flush volume (flush multiplier >= 1.5 or manually raise blue->clear cells) and/or use a prime tower [I].
- One user reported Rapid PETG continuing to extrude/ooze after colour change, leaving material hanging from the hotend [C] - PETG ooze during the A1 purge/cut sequence; keep nozzle clean, consider lowering temp a few °C [I].

## 6. Quirks

**Clear (Rapid PETG Transparent)**
- Clarity recipe (Bambu wiki, 0.4 3MF values): dry filament; 270 °C; flow 1.01; all fans 0; 0.1 mm layers; 0.5 mm line width; 1 wall; no top/bottom shells; 100 % aligned-rectilinear infill at fixed 0°/90°; all speeds 20 mm/s; PA 0.02; sand/polish afterwards [S]. PETG (amorphous) is inherently clearer than PLA [S].
- **CONFLICT** fan: 0 % for clarity [S] vs one X1C user who found fan 0 made Rapid PETG **brittle** and insists overhang fan is critical [C]. Use 0 % only for clarity showpieces with no overhangs; 10-40 % for functional parts.
- **CONFLICT** temperature: Elegoo spec 240-270 °C, but community A1 users run 230-235 °C [C] while others run 255-280 °C [C]. 280 °C is above spec. Let the temp tower decide; clear tends to look best near the top of the window.
- **CONFLICT** flow: community 0.95 [C] vs 1.05-1.07 for strong parts [C] vs Bambu's 1.01 for clarity [S]. Calibrate first (expect ~0.95), then overextrude only the clarity variant.
- Clear makes every defect visible (bubbles = wet, haze = too fast/too cold, lines = flow gaps) [I].

**Blue (pigmented)**
- Pigment/colour changes rheology slightly; Rapid PETG users report different colours behaving differently (e.g. one colour reached 350 mm/s where another topped at 250 mm/s) [C]. Do **not** copy clear-spool numbers to blue (or vice versa) - calibrate each spool [I].
- Opaque blue hides internal voids, so prioritise surface/stringing rather than clarity [I].

**Blobbing, zits, nozzle buildup (both)**
- PETG sticks to the nozzle, collects and drops blobs. Mitigations: dry filament; lower nozzle temp 5-10 °C if stringing (one A1 user fixed stringing by going 250 first layer / 240 others [C]); enable wipe + "wipe while retracting"; Spiral z-hop; "avoid crossing walls"; scarf seam or aligned seams to reduce zits; reduce outer-wall acceleration (one A1 user eliminated start-point spikes by cutting acceleration heavily [C]); brush the hot nozzle with brass between prints; keep the A1 wiper/purge area clean [I].
- Rapid PETG "zits" reported persistent despite drying and higher temp by one user; line width 0.48 gave early improvement [C].
- Ironing PETG often drags/blobs - avoid or test separately [I].

---

## 7. Summary table (starting points)

| | Blue PETG 0.4 | Blue PETG 0.2 | Rapid Clear 0.4 | Rapid Clear 0.2 |
|---|---|---|---|---|
| Base preset | Generic PETG @BBL A1 | Generic PETG @BBL A1 0.2 | Generic PETG @BBL A1 (+Translucent fan/retract) | Generic PETG @BBL A1 0.2 (+Translucent) |
| Mfr range | 220-250 (legacy) / 230-260 (PRO) [S] | same | 240-270 [S] | 240-270 [S] |
| Start nozzle | 240 [I] | 245 [I] | 250 (clarity 265-270 [S]) | 250-255 [I] |
| Temp tower | 255->225 /5 | 260->230 /5 | 270->240 /5 | 270->240 /5 |
| Bed (textured PEI) | 70 (75-80 if lifting) | 70 | 70 | 70 |
| Max vol. start / test | 10 / 5-20 step 1 | 1.5 / 0.5-4 step 0.25 | 14 / 8-26 step 2 | 2 / 0.5-4.5 step 0.25 |
| Flow start / expect | 0.95 / 0.92-0.98 | 0.95 / 0.92-1.00 | 0.95 / 0.93-1.00 (clarity +3-6 %) | 0.95 / 0.93-1.00 |
| PA expect | 0.02-0.06 | manual, coarse 0-0.30 | 0.02-0.05 (community 0.030) | manual, coarse 0-0.30 |
| Fan min/max/overhang | 30/50/90 | 20/35/90 | 10-20/30-40/90 (clarity 0) | 10/30/90 |
| Retraction | 0.6 @ 30-40; test 0.2-1.4 | 0.4-0.6 @ 30 | 0.4 @ 30-45; test 0.2-1.2 | 0.3-0.5 @ 30 |
| Z-hop | 0.4 Spiral | 0.2-0.4 Spiral | 0.4 | 0.2-0.4 |
| Dry | 60-65 °C 8-12 h | same | same, re-dry before clarity prints | same |

## Sources

- ELEGOO Rapid PETG product page (spec JSON: 240-270 °C, bed 65-75, dry 60 ± 5 °C 8 h, glue recommended, ≤ 20 % RH, < 600 mm/s, MI 13.4, Blue + Transparent variants): https://us.elegoo.com/products/rapid-petg-filament-1-75mm-colored-1kg
- ELEGOO PETG PRO product page (230-260 °C, bed 65-75, < 270 mm/s, MI 8.2): https://us.elegoo.com/products/petg-pro-filament-1-75mm-colored-1kg
- ELEGOO PETG Translucent: https://us.elegoo.com/products/petg-translucent ; ELEGOO PETG HF: https://us.elegoo.com/products/petg-hf
- Legacy ELEGOO PETG Blue listing (220-250 °C, rec. 230, bed 75-90): https://woodartsupply.com/collections/3d-printer-filaments/products/elegoo-petg-filament-1-75mm-blue-1kg-3d-printer-filament-dimensional-accuracy-0-02-mm-1kg-spool2-2lbs-fits-for-most-fdm-3d-printers
- Rapid PETG paper spool listing: https://audicoonline.co.za/elegoo-rapid-petg-black-175mm-1000g-paper-spool
- Bambu Studio system profiles (GitHub, master): https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament (Generic PETG @BBL A1 [0.2 nozzle], Bambu PETG HF/Basic/Translucent @BBL A1 [0.2 nozzle]) and machine profiles https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/machine (fdm_bbl_3dp_001_common, Bambu Lab A1 0.2 nozzle)
- Bambu wiki - Transparent PETG guide + preset 3MF (270 °C, flow 1.01, fans 0, PA 0.02, 0.1 mm layer, 20 mm/s, 1 wall, 100 % aligned rectilinear): https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg ; 3MF: https://wiki.bambulab.com/filament-acc/filament/petg_-_transparent_parameters_-_0.4_mm_nozzle.3mf
- Bambu forum - ELEGOO Rapid PETG thread (flow 0.95, K 0.03, 24 mm³/s, Generic PETG base, 230 °C/70 °C/30 % fan on A1 mini, 255 °C, zits, ooze after colour change): https://forum.bambulab.com/t/elegoo-rapid-petg-filament/48209 , ?page=5 , ?page=6
- Bambu forum - "Elegoo Rapid PETG Settings - Mine are not normal" (265-270 °C, flow 1.05-1.07, fan 30-40 %, retraction 45 mm/s, glue): https://forum.bambulab.com/t/elegoo-rapid-petg-settings-mine-are-not-normal/143664
- Bambu forum - Elegoo PETG Pro with PETG HF settings (240/245, bed 80/82, flow 0.95, 18 mm³/s, PA 0.02, fan 40-90): https://forum.bambulab.com/t/rough-texture-using-elegoo-petg-pro-using-bambu-petg-hf-settings/98923
- Bambu forum - 0.2 nozzle K values (0.1-0.45 manual; auto-cal capped 0.06): https://forum.bambulab.com/t/calibrating-0-2mm-nozzle/89574 ; https://forum.bambulab.com/t/supertack-0-2-nozzle-issue/155239
- Bambu forum - A1 PETG stringing (240 °C fix): https://forum.bambulab.com/t/a1-struggling-with-petg-printing-stringing/172551 ; A1 combo PETG (textured plate, bed 80, accel cut): https://forum.bambulab.com/t/petg-problems-on-a1-combo/44602/16
- Bambu forum - PETG over-bonding / smooth PEI + glue: https://forum.bambulab.com/t/petg-cf-sticks-too-aggressively-to-the-pei-bed/76241 ; https://forum.bambulab.com/t/glue-stick-is-needed/16544 ; https://forum.bambulab.com/t/bambu-petg-s-stick-to-plate-too-well-and-leave-residue/101563
- Not fetchable: MakerWorld Rapid PETG profile https://makerworld.com/en/models/1125246 (403).
