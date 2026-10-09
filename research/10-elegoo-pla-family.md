# 10 — ELEGOO PLA family on Bambu Lab A1 (0.2 mm and 0.4 mm)

Scope: ELEGOO **PLA** (standard, sometimes called "PLA Basic"), ELEGOO **PLA+ / PLA Plus**, and ELEGOO **Rapid PLA+** (high-speed PLA). Printer: Bambu Lab A1 with AMS lite, Bambu Studio, firmware 01.08.01.00 or later.

Tags used below:
- **[S#]**: taken from a source in the list at the bottom.
- **[I]**: my inference or engineering judgement, not quoted from a source.
- **[C]**: the sources conflict. See "Conflicts" near the end.

Researched 2026-10-06.

---

## 0. TL;DR starting presets

| | Elegoo PLA | Elegoo PLA+ | Elegoo Rapid PLA+ |
|---|---|---|---|
| Bambu Studio base | `Generic PLA` [I] | `Generic PLA` [I] | `Generic PLA High Speed` [I] |
| Mfr nozzle range | 190–230 °C [S1] | 200–230 °C [S2] | 200–230 °C [S3] |
| Start nozzle 0.4 | 210 °C [I, S5] | 220 °C [I, S4] | 225 °C [I] |
| Start nozzle 0.2 | 210 °C [I] | 220 °C [I] | 220 °C [I] |
| Temp tower (0.4) | 230→190, 5 °C | 235→200, 5 °C | 240→205, 5 °C |
| Bed: Textured PEI | 60 (keep A1 default 65 if adhesion is marginal) | 60–65 | 60–65 |
| Bed: Smooth PEI / Cool plate | 55–60 / 35 | 55–60 / 35–40 | 55–60 / 35–40 |
| MVS start, 0.4 | 15 mm³/s | 15 mm³/s | 18 mm³/s |
| MVS expected, 0.4 | 16–20 | 15–22 | 20–26 |
| MVS start, 0.2 | 2.0 mm³/s | 1.8 mm³/s | 2.2 mm³/s |
| MVS expected, 0.2 | 2.0–3.2 | 1.8–3.0 | 2.2–3.5 |
| Flow ratio start / expected | 0.98 / 0.97–1.02 | 0.98 / 0.93–1.00 | 0.98 / 0.96–1.00 |
| K, 0.4 (expected) | 0.020–0.045 | 0.025–0.050 | 0.015–0.035 |
| K, 0.2 (expected) | 0.05–0.15 | 0.06–0.18 | 0.05–0.14 |
| Fan min/max, first layer | 60/80 %, off | 60/80 %, off | 70/100 %, off |
| Retraction 0.4 / 0.2 | 0.8 mm @30 (test 0.4–1.6) / 0.6 mm (test 0.3–1.2) | same | same |
| Dry | 50 ± 5 °C, 8 h [S1] | 50 ± 5 °C, 8 h [S2] | 50 ± 5 °C, 8 h [S3] |

Each value is justified and tagged in the sections below. The table shows starting points only. The calibration tests decide the final values.

---

## 1. What Elegoo officially publishes

Elegoo's EU store embeds a structured spec JSON in each product page. The US product pages show the same data as images. I pulled the JSON from the raw HTML with `curl` [S1–S3].

| Field (verbatim from Elegoo) | PLA [S1] | PLA Plus [S2] | Rapid PLA Plus [S3] |
|---|---|---|---|
| Nozzle Temperature | **190 – 230 °C** | **200 – 230 °C** | **200 – 230 °C** |
| Bed Temperature (depends on printer & plate) | 35 – 65 °C | 35 – 65 °C | 35 – 65 °C |
| Chamber Temperature | 20 – 45 °C | 20 – 45 °C | 20 – 45 °C |
| Printing Speed | < 300 mm/s | < 280 mm/s | < 600 mm/s |
| Drying before printing | 50 ± 5 °C for 8 h ("Recommended") | 50 ± 5 °C for 8 h ("Recommended") | 50 ± 5 °C for 8 h ("Recommended") |
| Build plate | Textured/Smooth PEI or other | same | same |
| Glue | Not required | Not required | Not required |
| Enclosure | Not required | Not required | Not required |
| Recommended nozzle | ≥ 0.2 mm | ≥ 0.2 mm | ≥ 0.2 mm |
| Print/store humidity | ≤ 20 % RH | ≤ 20 % RH | ≤ 20 % RH |
| Density | 1.26 g/cm³ | 1.30 g/cm³ | 1.23 g/cm³ |
| **Melt Index** | **8.1 ± 1.5 g/10 min** | **6.9 ± 1.3 g/10 min** | **10.7 ± 1.5 g/10 min** |
| Melting temp | 158 °C | 161 °C | 160 °C |
| Vicat / HDT (0.45 MPa) | 62 / 57 °C | 63 / 56 °C | 62 / 57 °C |
| Elongation at break X-Y / Z | 10.5 % / 6.7 % | 7.9 % / 5.9 % | 8.5 % / 7.9 % |
| Impact strength X-Y / Z | 66.2 / 12.5 kJ/m² | 65.5 / 7.6 kJ/m² | 50.4 / 6.7 kJ/m² |

Other official claims:
- The Elegoo PLA US page says it "prints smoothly between 190 – 230 °C" [S1b].
- Rapid PLA+ is marketed as "enhanced fluidity … printing speed of up to 600 mm/s". Elegoo's own demonstration ran at 250 mm/s on a Neptune 4 [S3b].
- PLA+ is marketed with "lower printing temperature" and a "better cooling effect" for overhangs [S2b].
- Older PLA+ listings say the material is NatureWorks 4032D [S2b]. Newer listings dropped that wording.
- Rapid PLA+ HDT, confirmed by Elegoo support in a product Q&A: 57 °C [S3b].

Interpretation [I]:
- The **melt index** is the most useful published number. It ranks how easily each material flows: **Rapid PLA+ (10.7) > PLA (8.1) > PLA+ (6.9)**.
- That ranking predicts volumetric limits in the same order: PLA+ lowest, Rapid highest.
- It also predicts that PLA+ needs the most heat and the most K. The community data in §3 agrees.
- The density values differ (1.23–1.30). Set density per filament so the slicer's weight and cost estimates are right. Density does not affect extrusion.

---

## 2. Elegoo's own slicer profiles

Elegoo does not ship profiles inside **Bambu Studio** [S6]: the BambuStudio repo only has `Generic PLA @Elegoo` for Elegoo printers. Elegoo does maintain filament profiles in **OrcaSlicer** (`resources/profiles/Elegoo/filament`) [S7]. They are written for Elegoo printers, but they are the closest thing to a manufacturer slicer profile.

| Orca profile | MVS (mm³/s) | Nozzle °C | PA | Fan min/max | Bed hot/textured |
|---|---|---|---|---|---|
| `Elegoo PLA @base` (inherits `fdm_filament_pla`) | 16 | 220 (inherited) | — | 50/100 (inherited) | 60/60 |
| `Elegoo PLA+ @base` | 16 (inherits PLA base) | 220 | — | — | — |
| `Elegoo Rapid PLA+ @base` | 16 (inherits PLA base) | 220 | — | — | — |
| `Elegoo PLA @ECC` (Centauri Carbon) | 21 | **210** | 0.024 | — | — |
| `Elegoo PLA+ @ECC` | **20** | 220 | 0.024 | — | — |
| `Elegoo Rapid PLA+ @ECC` | 21 | 220 | 0.024 | **60/100** | 60/60 |
| `… @ECC2` / `… @EC2` (Centauri Carbon 2 / Centauri 2) | 21 / 20 / 21 | 210 / 220 / 220 | **0.04** | Rapid: 60/100 | 60 |
| `… @EN4 Series` (Neptune 4) | 16 / 20 / 21 | 220 | — | 100/100 | 60 |
| **`Elegoo PLA / PLA+ / Rapid PLA+ @0.2 nozzle`** (Neptune) | **3.2** (all three) | 220 | — | — | — |

Takeaways:
- Elegoo runs **PLA at 210 °C** and **PLA+ and Rapid at 220 °C** on its own fast CoreXY printers [S7].
- Elegoo's own 0.4 MVS is about **20–21** for all three on CoreXY machines and **16** as a conservative base [S7].
- Elegoo's 0.2-nozzle MVS is **3.2** [S7]. That is higher than Bambu's A1 0.2 presets (1.6–2.0, see §4) [C].
- Elegoo's K values (0.024 and 0.04) come from different printers and extruders. Do not carry them over to the A1. Use them only to confirm the order of magnitude [I].

---

## 3. Community data on Bambu A1

| Source | Filament | Nozzle | Temp | Flow ratio | PA (K) | MVS | Bed | Fan |
|---|---|---|---|---|---|---|---|---|
| MakerWorld "Fully Calibrated Profile" by oohhddaanngg [S8] | Rapid PLA+ White | A1, 0.4 HS steel, OrcaSlicer | 230/230 | 0.9898 | 0.022 | **40** [C] | Textured/Smooth PEI 62, SuperTack 45, Cool 35 | 100/100, first layer off, overhang 100 % |
| Same author [S9] | PLA+ White | A1, 0.4 HS | 230/230 | **0.9405** | **0.04** | 22 | PEI 62 | 100/100 |
| MakerWorld Elegoo PLA sample-card profiles [S10] | Elegoo PLA (various) | — | 205 (less stringing; some colours under-melt) / **215 consistent for all colours** | ~1.00 (0.98–1.02) | — | — | — | — |
| Bambu forum, "I'm Impressed – Elegoo Rapid PLA Plus" [S11] | Rapid PLA+ | A1 and others | per spool label | — | — | — | — | Base: Generic PLA. One user reports "black Rapid PLA+ just won't stick" on A1. Some report weak layer adhesion. |
| Search snippet, single A1 user (not verified at primary source) [S12] | Rapid PLA+ | A1 | 230 | — | — | 18 | — | — |
| Bambu forum, "Elegoo PLA+ stringing on P2S" [S13] | PLA+ | P2S / A1 | 220 → 190 did not fix stringing | — | — | — | — | Thread unresolved; drying to 8 % RH did not help |

Reading this [I]:
- **230 °C** is the practical setting experienced A1 users land on for both PLA+ and Rapid PLA+. That is the top of Elegoo's range.
- PLA+ in particular under-flows at Bambu's 220 °C default when printing fast. This fits its low melt index.
- The **0.94 flow ratio** for PLA+ White is notable. Expect PLA+ to calibrate a few percent lower than Bambu's 0.98 default.
- The **MVS 40** for Rapid PLA+ on an A1 is not credible as a quality limit. Bambu's own spec for the A1 hotend is **28 mm³/s max flow, measured with ABS at 280 °C** [S14]. 40 is probably a "never limit me" cap: the author's real wall speeds would rarely demand it. Do not copy it [C].

---

## 4. Bambu Studio reference presets for the A1 (BambuStudio repo)

[S6] = `resources/profiles/BBL/filament/*.json`

| Preset | MVS 0.4 | MVS 0.2 (`@BBL A1 0.2 nozzle`) | Flow | Fan min/max | Bed textured/hot | Other |
|---|---|---|---|---|---|---|
| `Bambu PLA Basic` | 21 | **2.0** | 0.98 | 60/80 | 65/65 | `filament_long_retractions_when_cut` = 1, 18 mm; `slow_down_layer_time` 6 |
| `Generic PLA` | 12 (inherited) | **1.6** | 0.98 | 60/80 | 65/65 | `slow_down_layer_time` 8 |
| `Generic PLA High Speed` | 18 | **2.0** | 0.98 | 60/80 | 65/65 | `slow_down_layer_time` 6 |
| `eSUN PLA+` (closest PLA+ analogue) | 16 | **1.8** | 0.98 | 60/80 | 65/65 | `slow_down_layer_time` 8 |
| `fdm_filament_pla` (root) | 12 | — | — | 100/100 | 55/55 | 220 °C nozzle, cool plate 35 °C, first layer fan off (`close_fan_the_first_x_layers` 1), aux fan 70 % |

---

## 5. Per-filament recommendations

### 5.1 ELEGOO PLA (standard)

**Base profile:** `Generic PLA` → save as user preset "Elegoo PLA" for each nozzle (`@BBL A1` and `@BBL A1 0.2 nozzle`) [I].
- Why not `Bambu PLA Basic`? It has the same flow (0.98) and fans. Its only practical advantages are MVS 21 and the 18 mm long-retraction-on-cut [S6], and you can set both by hand.
- Basing a non-Bambu filament on the Bambu Basic preset hides the fact that the MVS was never validated for this material [I].
- Turn on "Long retraction when cut" with 18 mm in the user preset to cut AMS-lite purge waste. Bambu does this for PLA Basic on the A1 [S6].

**Temperatures**
- Manufacturer range: 190–230 °C [S1].
- **0.4 start: 210 °C.** This matches Elegoo's CC/CC2 profile at 210 [S7], and 205–215 is the community sweet spot [S10]. If some colours under-melt or look matte at speed, use 215 [S10].
- **0.4 tower: 230 → 190, 5 °C steps** (9 blocks). This covers the full official range [I].
- **0.2 start: 210 °C. Tower: 225 → 195, 5 °C steps** [I].
  - At 0.2 the volumetric demand is about 10× lower, so melt capacity is not the limit and you can run cooler for less stringing and oozing on fine detail.
  - Do not go below about 200 °C. A 0.2 orifice has high back-pressure and clogs more readily with partly melted pigment.
- **Bed:**
  - Textured PEI: 60 °C. The A1 Bambu default is 65 [S6], which is within Elegoo's 35–65 [S1]. Drop to 55–60 if the bottom shows elephant foot or the bed is at the upper limit.
  - Smooth PEI (High Temp Plate): 55–60 °C [I].
  - Cool plate / SuperTack: 35 °C (Bambu root default) [S6]. SuperTack: 45 [S8].

**Max volumetric speed**
- **0.4:** start **15 mm³/s**. Test **10 → 24 mm³/s, step 1** [I].
  - Expected result: **16–20** [I]. Elegoo publishes 16 (conservative) and 21 (CoreXY) [S7]. The A1 hotend's absolute ceiling is 28 mm³/s with ABS at 280 °C [S14], so a PLA at 210–215 °C should run out of melt well before that.
  - Set the final value about 10 % below the first visible failure point.
- **0.2:** start **2.0 mm³/s** (Bambu PLA Basic @A1 0.2) [S6]. Test **1.0 → 5.0 mm³/s, step 0.25** [I]. Expected: **2.0–3.2** [I]. The upper end is Elegoo's own 0.2 profile at 3.2 [S7].
  - Reasoning [I]: at 0.2 the limit is pressure drop across the small orifice, not melt capacity. Typical 0.2 jobs (0.08–0.12 mm layers, about 0.22 mm lines) need only 0.1 × 0.22 × 100 mm/s ≈ **2.2 mm³/s** at 100 mm/s walls. A higher MVS mostly matters for infill.
  - If the test gives more than 3.5, keep the preset at 3.0–3.2. The extra pressure raises the needed K and makes corners worse.

**Flow ratio**
- Start at **0.98** (Bambu Generic default) [S6].
- Expected **0.97–1.02** [S10]. Colour-dependent; calibrate per colour if you care about top-surface quality.
- 0.2 nozzle: same start. Expected 0.95–1.02 [I]. Small lines are more sensitive, so give the fine pass priority.

**PA / K**
- **0.4:** expected **0.020–0.045** [I].
  - A1 manual calibration on plain PLA typically gives 0.035–0.040, while A1 auto calibration overestimated (0.059) for the same filament [S15].
  - Elegoo's own printers use 0.024–0.04 [S7].
  - Manual test range: **0 → 0.08, step 0.002** (pattern method) [I].
- **0.2:** expected **0.05–0.15** [I, S16]. Use **manual** calibration (per the background note).
  - Forum: the A1 auto routine caps at 0.060 on 0.2. Manual results came in at 0.086 and "0.1–0.2" [S16].
  - Test range: **0 → 0.20, step 0.005** [I]. If the best line is at the top of the range, extend to 0.3.

**Cooling**
- **60 % min / 80 % max** fan (A1 PLA default) [S6].
- First layer fan off (`close_fan_the_first_x_layers` = 1) [S6].
- Overhang/bridge fan 100 %.
- Slow-down layer time 6–8 s [S6]. On 0.2, use 8 s or more for tiny parts [I].

**Retraction**
- A1 default **0.8 mm**. Speed **30 mm/s** (the A1 machine value shown in [S8]'s screenshots).
- Test **0.4 → 1.6 mm, step 0.2** on 0.4 [I]. On 0.2: test **0.3 → 1.2 mm**. Start at 0.6 [I], because a smaller melt chamber holds less residual pressure.
- Keep wipe on. Long-retraction-on-cut: 18 mm [S6].

### 5.2 ELEGOO PLA+ (PLA Plus)

**Base profile:** `Generic PLA` [I].
- `eSUN PLA+` exists in Bambu Studio (MVS 16; 0.2 nozzle 1.8) [S6]. It works as a reference point, but basing an Elegoo preset on another brand's preset is confusing.
- Recommendation: Generic PLA → user preset "Elegoo PLA+". Set MVS by hand.

**Temperatures**
- Manufacturer range: 200–230 °C [S2]. Third-party listings quote "200–230 (recommended 215)" [S17].
- **0.4 start: 220 °C** (Elegoo's own Orca profiles) [S7]. Expect the winner to be **220–230 °C**. A1 users who calibrated landed on 230 [S9].
- **0.4 tower: 235 → 200, 5 °C steps** [I]. Going 5 °C above the official max is deliberate: it shows whether 230 is still improving or already over the knee.
- Only use 235 if the tower proves it is clearly better [I]. It is outside Elegoo's stated max (230).
- **0.2 start: 220 °C. Tower: 230 → 205** [I].
- **Bed:**
  - Textured PEI: 60–65 °C [S6, S9]. The community A1 profile uses 62.
  - Smooth PEI: 55–60 °C.
  - Cool plate: 35–40 °C [S6, S9].

**Max volumetric speed**
- PLA+ has the lowest melt index (6.9) [S2] and the lowest official speed cap (< 280 mm/s) [S2].
- **0.4:** start **15 mm³/s** at 220–230 °C. Test **10 → 25, step 1** [I]. Expected **15–22**:
  - Elegoo's own value is 20 [S7].
  - An A1 user got 22 at 230 °C [S9].
  - If you settle at 220 °C, expect the lower end (about 15–17) [I].
- **Run the MVS test at the temperature you picked.** MVS for this material moves noticeably with temperature [I].
- **0.2:** start **1.8 mm³/s** (Bambu's eSUN PLA+ @A1 0.2 value) [S6]. Test **1.0 → 4.5, step 0.25**. Expected **1.8–3.0** [I].

**Flow ratio**
- Start at 0.98 [S6]. Expected **0.93–1.00**.
- A1 community calibration: **0.9405** on White [S9]. PLA+ often runs a few percent under 1.0 because the filament swells slightly more out of the nozzle and its density differs (1.30) [I].
- 0.2: expected 0.93–1.00 [I].

**PA / K**
- Higher viscosity means more pressure lag, so expect slightly higher K than plain PLA [I].
- **0.4:** **0.025–0.050** [I]. The A1 community value is 0.04 [S9]. Test 0 → 0.08, step 0.002.
- **0.2:** **0.06–0.18** [I, S16]. Test 0 → 0.20, step 0.005, manual.

**Cooling**
- 60/80 % [S6], first layer off.
- Elegoo says PLA+ has a "better cooling effect" for overhangs [S2b]. The community uses 100/100 [S9].
- Recommendation: keep 60/80 for strength (PLA+ is chosen for toughness, and more fan lowers layer adhesion). Raise max to 100 only if overhangs curl [I].

**Retraction**
- Same as PLA: 0.8 mm @ 30 mm/s, test 0.4–1.6 on 0.4, and 0.3–1.2 (start 0.6) on 0.2 [I].
- Elegoo PLA+ has an unresolved **stringing** thread on P2S/A1. Dropping temperature to 190 °C did not fix it [S13].
- If stringing persists, try in this order [I]:
  1. Dry the filament (50 °C, 8 h) [S2].
  2. Test longer retraction (1.0–1.2 mm) with wipe on.
  3. Lower temperature 5 °C at a time while watching MVS.
  4. Accept a light heat-gun pass.

**Drying:** 50 ± 5 °C, 8 h [S2].

### 5.3 ELEGOO Rapid PLA+ (high-speed PLA)

**Base profile:** `Generic PLA High Speed` [I, S6].
- It is Bambu's generic high-flow PLA: MVS 18 at 0.4 and 2.0 at 0.2 on the A1. The other values match Generic PLA.
- One forum user just used Generic PLA [S11]. That works, but MVS 12 throttles this filament.

**Temperatures**
- Manufacturer range: 200–230 °C [S3]. Some third-party pages say "recommended 220" [S18].
- **0.4 start: 225 °C** [I]. Elegoo's own profiles use 220 [S7]. A1 users who push speed use 230 [S8, S12].
- **0.4 tower: 240 → 205, 5 °C steps** [I].
- High-speed PLAs need heat at speed. A tower printed at modest speed can mislead you. **Print the tower at your real wall speed** (for example 200 mm/s outer walls), or confirm the winner with an MVS test at that temperature [I].
- **0.2 start: 220 °C. Tower: 230 → 205** [I].
  - At 0.2 you will never be flow-limited, so the high-flow chemistry gives no benefit.
  - Rapid PLA's lower viscosity (MFI 10.7) can mean **more oozing and stringing** on a 0.2. Favour the cooler end [I].
- **Bed:**
  - Textured PEI: 60–65 °C. Elegoo sets 60 in its Rapid profiles [S7]. The A1 community uses 62 [S8].
  - Smooth PEI: 55–60 °C.
  - Cool plate: 35–40 °C. SuperTack: 45 [S8].
  - **Black Rapid PLA+ has a reported A1 plate-adhesion problem** [S11]. If you see it, wash the plate with dish soap, use 65 °C, and slow the first layer.

**Max volumetric speed**
- **0.4:** start **18 mm³/s** (Generic PLA HS) [S6]. Test **14 → 30, step 1** [I]. Expected **20–26** [I].
  - Elegoo's value is 21 [S7]. One A1 user reports 18 at 230 [S12].
  - Hardware ceiling: 28 mm³/s with ABS at 280 °C [S14]. At about 230 °C PLA the realistic knee is a little below that.
  - The 40 mm³/s figure on MakerWorld [S8] is above the hotend spec. Treat it as a cap, not a measured limit [C].
- **0.2:** start **2.2 mm³/s**. Test **1.0 → 5.0, step 0.25**. Expected **2.2–3.5**. Bambu Generic PLA HS @A1 0.2 = 2.0 [S6]. Elegoo 0.2 = 3.2 [S7].

**Flow ratio**
- Start 0.98 [S6]. Expected **0.96–1.00**. A1 community result: 0.9898 [S8].
- 0.2: expected 0.95–1.00 [I].

**PA / K**
- Lower viscosity means less pressure build-up, so expect slightly lower K than PLA/PLA+ [I].
- **0.4:** **0.015–0.035**. A1 community: **0.022** [S8]. Test 0 → 0.06, step 0.002.
- **0.2:** **0.05–0.14** [I, S16]. Manual.
- If you print the same model at 100 mm/s and at 300 mm/s, consider separate presets or Orca's adaptive PA. A single K is a compromise across speeds [I].

**Cooling**
- **70 % min / 100 % max** [I], first layer off. Elegoo's own Rapid profile is 60/100 [S7]. The community uses 100/100 [S8].
- Fast printing gives short layer times, and the low-viscosity melt sags more on overhangs. Allow the fan to reach 100 %.
- Rapid PLA+ Z impact strength is the lowest of the three (6.7 kJ/m²) [S3]. For functional parts that load across layers, prefer PLA+ or a slower, hotter, less-cooled print [I].

**Retraction**
- 0.8 mm @ 30 mm/s. Test 0.4 → 1.6 on 0.4.
- On 0.2, start at 0.6 and test 0.3 → 1.2 [I]. Expect Rapid to need the **upper** half of the range because the melt is runnier [I].

**Drying:** 50 ± 5 °C, 8 h [S3].

---

## 6. Drying, storage, AMS lite

- **Drying: 50 ± 5 °C for 8 h** for all three, per Elegoo [S1–S3].
  - Elegoo marks it "Recommended", not required. New spools are vacuum-sealed with desiccant [S2b, S3b].
  - Bambu's generic PLA root profile stores AMS-dryer defaults of 45 °C / 12 h [S6]. Those apply to Bambu's drying AMS units. **The AMS lite cannot dry.** Use an external dryer or the A1 bed-drying trick (the bed-drying parameter is 70 °C in the root profile [S6]).
- **Storage:** ≤ 20 % RH [S1–S3]. The AMS lite is open to room air, so long PLA+ prints in humid rooms can pick up moisture. Stringing on PLA+ is the first symptom [I].
- **Cardboard spools in the AMS lite**
  - Cardboard spools "work perfectly on the AMS lite" per forum reports. Elegoo has been moving to plastic spools [S19].
  - The AMS lite rewinds by turning the spool on its rollers. Cardboard rims can slip or shed fibres. A wrap of masking tape on the rim helps [S20].
  - **Elegoo publishes a "Filament Ring" STL** to fit over the cardboard rim. Their stated purpose: "adapt to AMS (because AMS will rub the bottom paper tray, causing the paper tray to easily delaminate)". Elegoo's tips: print it in PETG, and set X-Y hole/contour compensation to 0.1 if it is too tight [S3b].
  - Empty spool weight: 154 ± 10 g [S1–S3]. Enter it if you track remaining filament by weight.
- **RFID:** Elegoo's newer "PLA (RFID)" spools use tags for Elegoo's CANVAS system [S1b]. The AMS lite will not recognise them as a known filament. You must assign the preset manually per slot [I].
- **End of spool:** a sharp hook at the spool core caused AMS-lite feed failures for some Elegoo users [S20]. Straighten or cut the last tail before runout [I].

---

## 7. Known quirks and differences

1. **PLA+ is not a hotter-but-otherwise-identical PLA.**
   - It has the lowest melt index (6.9 vs 8.1) [S1, S2]. That means lower MVS at a given temperature, higher K, and usually a flow ratio below 1.0 [S9].
   - Elegoo's marketing says "lower printing temperature" [S2b], but its own spec and slicer profiles point the other way: min 200 vs 190, and 220 vs 210 [S2, S7]. Calibrated A1 users run 230 [S9] [C].
2. **Rapid PLA+ trades toughness for flow.**
   - It has the highest MFI (10.7) [S3], but X-Y impact is lower than PLA/PLA+ (50.4 vs about 66 kJ/m²) [S1–S3].
   - It needs higher temperature at high speed; users settle at 230 [S8, S12].
   - The "600 mm/s" claim is not reachable on an A1, because 28 mm³/s at 0.4 × 0.2 mm lines is about 350 mm/s max [I, S14]. Even the MakerWorld author backed off to 400/500 mm/s [S8], and Elegoo itself demonstrated 250 mm/s [S3b].
3. **Elegoo standard PLA varies by colour.** A tester calls it "not the most consistent filament". Some colours do not fully melt at 205 °C, while 215 is reliable for all [S10]. Run a temperature tower per colour family (at least dark/pigmented vs. light) [I].
4. **Black Rapid PLA+ adhesion on A1** [S11]. **Weak layer adhesion** with Rapid PLA+ is also reported [S11]. Both point to running it hotter (225–230) and not over-cooling on load-bearing prints [I].
5. **Stringing with PLA+** is not cured by temperature alone [S13]. Drying, retraction length and travel settings matter more [I].
6. **0.2 nozzle:**
   - Auto Flow Dynamics is not reliable on 0.2 (it caps at 0.06) [S16]. Use the manual PA pattern.
   - Keep MVS modest (2–3) even if a test passes higher [I].
   - Use the `@BBL A1 0.2 nozzle` variant of the base preset so the MVS and slow-down defaults load [S6].

---

## 8. Conflicts [C]

| Topic | Source A | Source B | Resolution [I] |
|---|---|---|---|
| Rapid PLA+ MVS on A1 0.4 | MakerWorld A1 profile: **40** [S8] | Bambu A1 hotend spec: **28 mm³/s** max (ABS, 280 °C) [S14]. Elegoo profile: 21 [S7]. Single A1 user: 18 [S12]. | Measure it. Expect 20–26. Never set the MVS above the measured knee. |
| 0.2 nozzle MVS | Elegoo Neptune 0.2 profiles: **3.2** [S7] | Bambu A1 0.2 presets: **1.6–2.0** [S6] | Start at Bambu's value. Test up to about 5. Settle at 2–3.2. |
| PLA+ temperature | Elegoo marketing: "lower printing temperature" [S2b] | Elegoo spec 200–230 and slicer 220 [S2, S7]. A1 users: 230 [S9]. | Treat PLA+ as the *hottest* of the three. |
| 0.2 nozzle K magnitude | One forum user: 0.2–0.45 [S16] | Others: 0.086 and 0.1–0.2 [S16] | Expect 0.05–0.15. Extend the test range only if the pattern shows the optimum at the edge. The 0.2–0.45 report probably reflects a different method or units, or a worn nozzle. |
| A1 auto K, 0.4 | Auto: 0.059 [S15] | Manual: 0.035–0.040 for the same PLA [S15] | Prefer manual PA, or check the auto result with one manual pattern. |
| Fan for PLA+/Rapid | Elegoo/community: 100 % min (N4) or 60/100 [S7, S8, S9] | Bambu A1 PLA: 60/80 [S6] | Strength parts: 60/80. Overhang- or speed-heavy parts: raise max to 100. |
| Bed temperature | Bambu A1 default 65 °C, textured and smooth [S6] | Elegoo 35–65 [S1–S3]. Elegoo profiles 60 [S7]. Community 62 [S8, S9]. | Use 60–62 textured. 65 is the ceiling. |

---

## 9. Sources

- **[S1]** ELEGOO PLA, EU store (spec JSON embedded in page): https://eu.elegoo.com/en-es/products/pla-filament-1-75mm-colored-1kg
- **[S1b]** ELEGOO PLA, US store ("prints smoothly between 190 – 230 °C"; RFID/CANVAS): https://us.elegoo.com/products/pla-filament-1-75mm-colored-1kg
- **[S2]** ELEGOO PLA Plus, EU store (spec JSON): https://eu.elegoo.com/en-es/products/elegoo-pla-plus-3d-printer-filament-1-75mm-colored-1kg
- **[S2b]** ELEGOO PLA Plus, US store (marketing text; NatureWorks 4032D wording on bundle listings): https://us.elegoo.com/products/elegoo-pla-plus-3d-printer-filament-1-75mm-colored-1kg and https://us.elegoo.com/products/elegoo-pla-plus-filament-1-75mm-4-colors-10kg
- **[S3]** ELEGOO Rapid PLA Plus, EU store (spec JSON): https://eu.elegoo.com/en-es/products/elegoo-rapid-pla-plus-filament-1-75mm-colored-1kg
- **[S3b]** ELEGOO Rapid PLA Plus, US store (600 mm/s claim, 250 mm/s on Neptune 4, HDT 57 °C Q&A, Filament Ring note): https://us.elegoo.com/products/elegoo-rapid-pla-plus-filament-1-75mm-colored-1kg. Filament Ring STL: https://download.elegoo.com/06%20FDM%20Printer/02%20ELEGOO%20Neptune%20Series%20Files/6.%20Model%20Gallery/1.%20Practical%20modification%20devices/Elegoo_Filament_Ring.stl
- **[S4]** (see S7: Elegoo's 220 °C default for PLA+)
- **[S5]** (see S7: Elegoo's 210 °C for PLA on CC/CC2)
- **[S6]** BambuStudio system filament presets: https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament. Files used: `Bambu PLA Basic @BBL A1(.json| 0.2 nozzle.json)`, `Generic PLA @BBL A1…`, `Generic PLA High Speed @BBL A1…`, `eSUN PLA+ @BBL A1…`, `fdm_filament_pla.json`.
- **[S7]** OrcaSlicer, Elegoo vendor filament profiles: https://github.com/SoftFever/OrcaSlicer/tree/main/resources/profiles/Elegoo/filament. Folders used: `BASE`, `ECC`, `ECC2`, `EC2`, `EN4SERIES`, `ELEGOO_02_NOZZLE`, plus `fdm_filament_pla.json`.
- **[S8]** MakerWorld, "Fully Calibrated Profile – Elegoo Rapid PLA+ White" (A1, 0.4 HS). Values read from the author's settings screenshots via the MakerWorld design API: https://makerworld.com/en/models/1132085 (Black variant: https://makerworld.com/en/models/1125246)
- **[S9]** MakerWorld, "Fully Calibrated Profile for Elegoo PLA+ White" (A1, 0.4 HS). Values from screenshots: https://makerworld.com/en/models/1085293
- **[S10]** MakerWorld, "Elegoo PLA Filament Sample Card & Profiles": https://makerworld.com/en/models/1217612
- **[S11]** Bambu forum, "I'm Impressed – Elegoo Rapid PLA Plus": https://forum.bambulab.com/t/im-impressed-elegoo-rapid-pla-plus/130523
- **[S12]** Web-search summary attributing "230 °C, 18 mm³/s, A1" to an A1 user of Rapid PLA+. **Not verified at the primary page**; treat as weak.
- **[S13]** Bambu forum, "Elegoo PLA+ stringing on P2S": https://forum.bambulab.com/t/elegoo-pla-stringing-on-p2s/216547
- **[S14]** Bambu Lab A1 spec sheet (max hotend flow 28 mm³/s @ ABS, 280 °C): https://cdn.shopify.com/s/files/1/0635/8247/0318/files/A1_Spec_EN_1.pdf
- **[S15]** Bambu forum, "A1 Automatic Pressure Advance Calibration Produces Incorrect K Values": https://forum.bambulab.com/t/a1-automatic-pressure-advance-calibration-produces-incorrect-k-values/217723
- **[S16]** Bambu forum, "Calibrating 0.2mm nozzle": https://forum.bambulab.com/t/calibrating-0-2mm-nozzle/89574
- **[S17]** Third-party summaries of PLA+ "200–230, recommended 215" (e.g. https://filamentcat.com/en/filament/elegoo/elegoo-pla-plus-175). Secondary source.
- **[S18]** Third-party Rapid PLA+ "200–230, recommended 220, bed 40–60" (e.g. https://www.spoolscout.com/data-sheets/elegoo/pla-rapid-pla). Secondary source.
- **[S19]** Bambu forum, "AMS Lite Compatible PLA Filament": https://forum.bambulab.com/t/ams-lite-compatible-pla-filament/101783
- **[S20]** Bambu forum, AMS-lite cardboard-spool and end-of-spool-hook threads: https://forum.bambulab.com/t/polymaker-cardboard-spools/3236?page=2 and https://forum.bambulab.com/t/end-of-spool-hook-causes-issues/139024 (via search summary)

Not accessible: MakerWorld HTML pages (HTTP 403, worked around with the MakerWorld API) and 3dfilamentprofiles.com (HTTP 429).
