# Dimensional and first-layer tests (Bambu Lab A1)

Generator: `tests-src/dimensional.py`. Run it with `.venv/Scripts/python -I tests-src/dimensional.py`. It rewrites every STL below, checks that each one is watertight, has positive volume and sits on z = 0, and prints its size and volume.

| File (stl/0.4/ and stl/0.2/) | Test | Size 0.4 / 0.2 version (mm) | PLA, approx. |
|---|---|---|---|
| `dim01_first-layer-squares_0.4n_h0.20.stl` / `..._0.2n_h0.10.stl` | First layer / auto-leveling | 220 x 220 x 0.20 / 220 x 220 x 0.10 | 1.4 g / 0.4 g |
| `dim02_xy-gauge-100-20_<n>.stl` | XY shrinkage, contour and hole offsets | 100 x 100 x 4 / 100 x 100 x 3 | 5.2 g / 3.4 g |
| `dim03_hole-peg-gauge_<n>.stl` | Round holes and pegs at nominal diameters | 71 x 36 x 9 / 54 x 24 x 6 | 10.3 g / 3.3 g |
| `dim04_fit-clearance-D6_0.4n.stl` / `dim04_fit-clearance-D3_0.2n.stl` | Fit and clearance series plus test pin | 63 x 38 x 12 / 42 x 26 x 7 | 8.1 g / 2.9 g |
| `dim05_elephant-foot_<n>.stl` | Elephant foot | 20 x 20 x 6 / 15 x 15 x 4 | 1.3 g / 0.5 g |

`<n>` is `0.4n` or `0.2n`. Each model is centred on the XY origin. The front of the printer is -Y. Bambu Studio puts an imported object at the plate centre. Keep dim01 there (position X = 128, Y = 128).

## Common conventions

- **Nozzle profiles assumed.** 0.4 nozzle: line width 0.42, layer 0.20, first layer 0.20 (process "0.20mm Standard @BBL A1"). 0.2 nozzle: line width 0.22, layer 0.10, first layer 0.10 (process "0.10mm Standard @BBL A1 0.2 nozzle"). All model heights are whole multiples of the layer height.
- **Wall thicknesses are whole multiples of the line width:**
  - dim02: 5 x 0.42 = 2.10 and 8 x 0.22 = 1.76.
  - dim05: 6 x 0.42 = 2.52 and 8 x 0.22 = 1.76.
  - Labels: 2-line strokes.

  Studio spaces wall loops at slightly less than the line width (spacing = w - h(1 - pi/4)). So N loops leave a thin strip, which gap fill closes. Check in the preview that each gauge wall is all perimeter and gap fill, with no sparse infill.
- **Order:**
  1. dim01 (first layer)
  2. dim05 (elephant foot)
  3. dim02 (shrinkage and contour)
  4. dim03 (holes)
  5. dim04 (final fit check)

  dim02, dim03 and dim05 fit on one plate together, which saves a print cycle.
- **Per filament.** Bambu's XY compensation and shrinkage are per-filament values. Run dim02, dim03 and dim05 for each of PLA, PLA+, Rapid PLA, budget PLA, PETG and Rapid PETG, on each nozzle you use. Do flow ratio, pressure advance and temperature first. Dry PETG first.
- **Speeds.** Print the gauges with the same process and speeds you will use for real parts: the profile defaults, or the Rapid profile speeds for Rapid PLA and Rapid PETG. Compensation values depend on speed, acceleration and wall order, so do not slow down only for calibration. Keep "Precise wall" and the wall generator (Classic or Arachne) as you normally print. No brim: brims interfere with elephant foot compensation.
- **Settings already active.** Note the X-Y hole compensation, X-Y contour compensation, elephant foot compensation and filament Shrinkage that were active when you printed. Every formula below gives a *change* to add to those values.
- **Measuring:**
  - Let parts cool at least 30 minutes after removal. PETG creeps longer.
  - Use calipers that read 0.01 mm. Take 3 readings per feature and average them.
  - Measure in the **upper half** of a wall, never at the first 1 mm, which has elephant foot.
  - Stay away from the seam. Use seam position "Aligned" or "Back", and measure round features 90 degrees from the seam.
  - Clear PETG is fine for calipers. For the first-layer visual check, light it at a low angle.
- **Where the settings are in Bambu Studio:**
  - Process > Quality > Precision: "X-Y hole compensation", "X-Y contour compensation", "Elephant foot compensation". Positive values make holes and contours larger. The value is per side.
  - Filament > Basic information: "Shrinkage (XY)", in % = measured / designed x 100.
- **Pass limits.** The pass limits below are suggestions, not Bambu specifications. Tighten them if your calipers and process allow.

---

## dim01 - First-layer squares

**Purpose.** Check A1 auto-leveling and first-layer squish across the whole bed. The file has 9 squares (25 mm for 0.4, 20 mm for 0.2) on a 220 mm grid. Each square is exactly one initial layer thick: 0.20 mm for 0.4, 0.10 mm for 0.2. Each square has a stencil digit cut through it in its back-left corner. Squares are numbered in reading order from the front: 1 2 3 is the back row, left to right, and 7 8 9 is the front row.

**Slicer settings:**

| | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Layer / initial layer | 0.20 / 0.20 | 0.10 / 0.10 |
| Walls | 2 | 2 |
| Bottom surface pattern | Monotonic (default) | Monotonic (default) |
| Infill | n/a (single layer is all bottom surface) | n/a |
| Speed | profile initial-layer speed (A1 default about 50 mm/s) | same |
| Plate type | must match the installed plate (textured PEI gets a Z offset in the start G-code) | same |
| Print options | Bed leveling ON | Bed leveling ON |

Check in the preview that the object is 1 layer.

**What to measure:**

1. **Visual, while printing and after.** Look for:
   - lines fused into a continuous sheet
   - no gaps between lines (too high)
   - no ridges, ploughing or rough, translucent-thin areas (too low)
   - the same look on all 9 squares
   - stencil digits with open, crisp corners
2. **Thickness.** Use a micrometer, or the flat jaws of the calipers. Peel each square and measure t at its centre and 4 corners. On the 0.2 version (0.10 mm) a micrometer is strongly preferred.

**Calculations:**

- Per-square mean t_i. Bed mean T = mean(t_i). Spread R = max(t_i) - min(t_i).
- Global first-layer height error: dZ = T - l0, where l0 = 0.20 or 0.10. Positive dZ means the nozzle is too high (under-squish).
- Tilt and leveling: compare columns (left vs right is the X tilt) and rows (back vs front is the Y tilt). A single bad square points to debris, plate warp or a leveling-probe point issue.

**Corrections.**
- **If dZ is outside the pass limit:**
  1. Clean the nozzle tip and the plate.
  2. Confirm the plate type in Studio matches the plate.
  3. Re-run auto-leveling.

  If dZ is still wrong, apply a software workaround. Use a Z offset if your Studio or firmware exposes one (offset = -dZ). Otherwise use the initial-layer flow ratio (see research/01). The A1 has no manual Z offset, so prefer fixing the cause.
- **If R is too large:** fix the hardware. Check plate flatness and debris, re-run full calibration, and check the heatbed. Do not compensate for it in the slicer.

**Pass:**

| | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| \|dZ\| | <= 0.04 mm | <= 0.03 mm |
| R | <= 0.04 mm | <= 0.03 mm |
| Visual | uniform on all squares | uniform on all squares |
| Sheet | each square peels as one sheet, no holes between lines | same |

---

## dim02 - XY dimensional / shrinkage gauge

**Purpose.** Separate three error sources:

1. Scale error (shrinkage, belts), which grows with size.
2. Outer-contour offset, which is constant.
3. Inner (hole) offset, which is constant.

Each is measured separately for X and Y.

The model is a square frame, 100 x 100 outside, with a 20 x 20 square island in the centre. Both have wall thickness w:

| | w | Frame inner | Island inner |
|---|---|---|---|
| 0.4 nozzle | 2.10 | 95.80 | 15.80 |
| 0.2 nozzle | 1.76 | 96.48 | 16.48 |

A low diagonal spoke at the front-left corner ties the island to the frame, so the axes stay identifiable. Low tabs carry a raised **X** at the front-right inner corner, the +X end, and a raised **Y** at the back-left inner corner, the +Y end. The letters read upright when you view from the printer front. Tabs and spoke are only 1 mm tall and sit in the corners, so they do not interfere with mid-span measurements.

**Slicer settings:**

| | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Layer / initial | 0.20 / 0.20 | 0.10 / 0.10 |
| Wall loops | 5 (whole wall is perimeter + gap fill) | 8 |
| Top/bottom shells | profile default | profile default |
| Infill | irrelevant (no infill region), leave 15% | same |
| Speed | profile defaults (your production speeds) | same |
| Placement | centred, rotation 0 (gauge X must be printer X) | same |

**What to measure.** Measure every value in both X and Y, at mid-span and in the top half of the wall.

| Symbol | Feature | Nominal (0.4 / 0.2) | Where |
|---|---|---|---|
| OB | frame outside | 100.00 / 100.00 | outside jaws, at y = 0 for X (x = 0 for Y). Jaws pass on either side of the island |
| IB | frame inside | 95.80 / 96.48 | inside jaws, at about 25 mm off-centre (clear of the island) |
| OS | island outside | 20.00 / 20.00 | outside jaws, mid-face |
| IS | island inside | 15.80 / 16.48 | inside jaws, mid-face |
| t | frame wall thickness (optional) | 2.10 / 1.76 | mid-wall |

**Calculations (per axis).** Let LB = 100, LS = 20, and NIB and NIS the inner nominals above (LB - LS = NIB - NIS = 80).

1. **Scale factor** from the slope between the two sizes, outer and inner:
   - kO = (OB - OS) / 80
   - kI = (IB - IS) / 80
   - k = (kO + kI) / 2

   Constant offsets cancel in the slope, so k is pure scaling.
   - Shrinkage % = (1 - k) x 100.
   - Studio "Shrinkage (XY)" = k x 100 %, for example 99.70 %. If a shrinkage value S_old was already set, the new value is S_old x k.
   - Apply it only if |1 - k| > 0.15 % on both axes. Use the mean of kX and kY, because Studio has one value for both axes.
2. **Outer contour offset** (per side), after removing scale:
   - eC = (OS - k x LS) / 2. You can also use (OB - k x LB) / 2. The two should agree within about 0.02.
   - Change to X-Y contour compensation: dC = -eC = (k x 20 - OS) / 2.
3. **Hole (inner) offset** (per side):
   - eH = (k x NIS - IS) / 2. Positive means the inner opening is too small.
   - Change to X-Y hole compensation: dH = +eH.
   - Treat this as a cross-check. Round holes usually print smaller than square openings, so take the hole compensation value from dim03.
4. **If you leave shrinkage at 100 %** (k close to 1), the formulas reduce to the Bambu wiki form: contour change = (20 - OS) / 2, and hole change = (NIS - IS) / 2.
5. **X vs Y:**
   - If |kX - kY| > 0.2 %, check the mechanics. On the A1, X is the toolhead belt and Y is the bed belt. Check belt tension and run vibration compensation.
   - Studio cannot scale X and Y separately. As a last resort, scale critical models per axis by 1/kX and 1/kY.
6. **Wall check (optional):** t should be about w + eC + eH. Both offsets thicken the wall when the contour is oversize or the opening is undersize. A t far from that points to flow ratio, not XY compensation.

Example (0.4, X): OB = 99.78, OS = 19.90, IB = 95.66, IS = 15.70.
- kO = 79.88 / 80 = 0.9985. kI = 79.96 / 80 = 0.9995. k = 0.9990, which is 0.10 % shrinkage, below 0.15 %, so leave shrinkage at 100 %.
- dC = (19.98 - 19.90) / 2 = +0.04.
- dH = (15.784 - 15.70) / 2 = +0.042.

**Pass (after applying corrections and reprinting):**

| | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| OS, IS | within ±0.08 mm of nominal | within ±0.05 mm |
| OB, IB | within ±0.15 mm | within ±0.15 mm |
| \|1 - k\| | <= 0.1 % | <= 0.1 % |
| \|kX - kY\| | <= 0.1 % | <= 0.1 % |

---

## dim03 - Hole / peg gauge (nominal diameters)

**Purpose.** Measure round holes (inner contours) and round pegs (outer contours) at several diameters. Large diameters give the X-Y hole compensation value. Small diameters show the smallest reliable feature size for each nozzle.

The gauge is one plate:
- Back row: through-holes.
- Middle row: raised diameter labels.
- Front row: pegs of the same diameters.

| | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Diameters (mm) | 2, 3, 4, 5, 6, 8, 10 | 1, 1.5, 2, 2.5, 3, 4, 5 |
| Plate thickness | 3.0 | 2.0 |
| Peg height above plate | 6.0 | 4.0 |

Circles are modelled as fine polygons (chord about 0.05 mm) whose mean radius is the nominal. The mesh error is under 0.001 mm.

**Slicer settings:**

| | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Layer / initial | 0.20 / 0.20 | 0.10 / 0.10 |
| Wall loops | 3 | 4 |
| Infill | 15% gyroid or grid | 15% |
| Top / bottom shells | profile default | profile default |
| Seam | Aligned (note its side) | Aligned |
| Speed | production speeds | production speeds |

**What to measure:**
- **Holes, Dh:**
  - For Dh >= 3 mm, use the inside jaws from the top face, in X and in Y, away from the seam.
  - For smaller holes, use drill-bit shanks or pin gauges. Record the largest that passes freely.
- **Pegs, Dp:** use the outside jaws, upper half of the peg, in X and in Y.

**Calculations** (d = nominal, per diameter):
- Hole error per side: eH(d) = (d - Dh) / 2. Positive means the hole is too small.
- Peg error per side: eP(d) = (Dp - d) / 2. Positive means the peg is too big.
- **X-Y hole compensation change:** dH = mean of eH(d) over the reliable sizes. Use d >= 4 mm for 0.4 and d >= 2 mm for 0.2. The new value is the old value + dH.
- **X-Y contour compensation cross-check:** dC = -mean(eP) over the same sizes. It should agree with dim02 within about 0.03 mm. If it does not, trust dim02 for flat contours. Pegs that print oversize while flat walls do not usually means a pressure advance or seam problem.
- **Smallest reliable feature:** the smallest d where |Dh - d| and |Dp - d| are both within the pass limit. Note it as a design rule for that filament and nozzle.
- If small holes are much tighter than large ones (eH rises as d shrinks), that is normal polygon and flow behaviour. Do not raise hole compensation to fix small holes. Upsize those holes in the CAD model instead.

**Pass (after correction):**

| | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Holes and pegs within ±0.10 mm in diameter | d >= 3 mm | d >= 1.5 mm |
| X vs Y diameter differ by (roundness) | <= 0.05 mm | <= 0.05 mm |

---

## dim04 - Fit / clearance series

**Purpose.** Find the practical clearance for slip, running and press fits with this filament and nozzle, after compensation. It also validates dim02 and dim03 together.

The plate has 8 holes in 2 rows of 4, labelled 1 to 8 with raised digits. The pin is printed standing on a flange, with a 45-degree lead-in chamfer at the tip. Hole diameter = D + 2g, where g is the **radial (per-side) clearance**.

0.4 version: pin D = 6.00, plate 4.0 thick, pin length 10.

| Label | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| g (mm) | 0.05 | 0.10 | 0.15 | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 |
| hole d | 6.10 | 6.20 | 6.30 | 6.40 | 6.50 | 6.60 | 6.70 | 6.80 |

0.2 version: pin D = 3.00, plate 3.0 thick, pin length 6.

| Label | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| g (mm) | 0.025 | 0.050 | 0.075 | 0.100 | 0.125 | 0.150 | 0.175 | 0.200 |
| hole d | 3.05 | 3.10 | 3.15 | 3.20 | 3.25 | 3.30 | 3.35 | 3.40 |

**Slicer settings.** Same as dim03: 3 walls (0.4) or 4 walls (0.2), 15% infill, production speeds. The pin is small, so the minimum layer time (slow-down for better cooling) will slow it, which is normal. For PETG, keep the part fan as in the profile.

**What to measure / do:**
1. Measure the pin diameter Dpin (upper half, X and Y).
2. Insert the pin from the **top** face of the plate. The bottom face of each hole is narrowed by elephant foot. Then try again from the bottom face.
3. For each hole, record one of:
   - press: needs force
   - slip: slides in by hand, no visible play
   - running: rotates and slides freely, little wobble
   - loose: visible wobble

**Calculations:**
- Effective clearance (per side) = g - (Dpin - D) / 2 - eH_round, where eH_round is the residual hole error from dim03 at this diameter. After good compensation the effective clearance is about g.
- Design rules for this filament and nozzle: g_press = largest g that still needs force. g_slip = smallest g that slides by hand. g_run = smallest g that rotates freely.
- If the step from press to slip happens at a g much larger than expected, re-check hole compensation (dim03) before widening design clearances. Expected: 0.10 to 0.15 for 0.4, 0.05 to 0.10 for 0.2.

**Pass** (well-tuned PLA, suggested):

| | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| g_slip | <= 0.15 mm | <= 0.10 mm |
| g_run | <= 0.25 mm | <= 0.15 mm |

PETG and budget PLA often need about 0.05 mm more. Top-face and bottom-face insertion should differ by at most one step. More than one step means elephant foot is under-compensated (see dim05).

---

## dim05 - Elephant foot check

**Purpose.** Measure how far the first layers bulge beyond the wall, outward on outer contours and inward on holes, and set "Elephant foot compensation".

The part is a square ring:

| | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Size | 20 x 20 x 6 | 15 x 15 x 4 |
| Wall | 2.52 (6 lines) | 1.76 (8 lines) |
| Inner opening | 14.96 | 11.48 |
| Front (-Y) chamfer | 0.4 | 0.2 |
| Back (+Y) chamfer | 0.8 | 0.4 |

The left and right outer faces and all four inner faces have **sharp 90-degree bottom edges**. The front and back bottom edges have **45-degree chamfers** as visual references.

**Slicer settings:**

| | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Layer / initial | 0.20 / 0.20 | 0.10 / 0.10 |
| Wall loops | 6 (solid walls) | 8 |
| Infill | n/a | n/a |
| Brim | **off** | **off** |
| Elephant foot comp. | note the current value. The A1 0.20 Standard default is 0.075. Check the 0.2 nozzle profile value | same |
| Speed / temperature | production | production |

**What to measure:**
- XB: X outer width at the very bottom. Stand the part on a flat surface and lower the outside jaws until they touch the surface, so the jaws read the first layers.
- XT: X outer width at mid-height or above (z >= 3 for 0.4, z >= 2 for 0.2).
- IB and IT: inner X and Y opening at the bottom face (inside jaw tips just in the bottom edge, part flipped) and at the top.
- Visual, with a loupe or a 10x macro photo:
  - Is there a lip on the sharp sides you can feel with a fingernail?
  - Are both chamfers still clean bevels down to the bed?
  - Or is the opposite true: an inward step (undercut) at the bottom of the sharp sides?

**Calculations:**
- Outer elephant foot per side: EFo = (XB - XT) / 2.
- Inner elephant foot per side: EFi = (IT - IB) / 2, from X and Y averaged.
- Residual: EF = mean(EFo, EFi).
- New elephant foot compensation = current value + EF. A negative EF means over-compensation, so the value goes down.
- Adjust in 0.025 to 0.05 mm steps, and only after dim01 passes. Squish is the root cause.

**Reading the chamfers:**
- The small chamfer (0.4 or 0.2) is filled flush or shows a lip at the bed: residual EF is about the chamfer size or more.
- The large chamfer (0.8 or 0.4) is also filled: there is a gross first-layer squish problem. Go back to dim01.

**Pass:**

| | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| \|EFo\| and \|EFi\| | <= 0.05 mm | <= 0.03 mm |
| Lip on sharp edges | none you can feel with a fingernail | same |
| Undercut | none visible | same |
| Small chamfer | clean and uniform | same |

---

## Recording

For each filament and nozzle, record the following in the saved user presets:
- first-layer dZ and R
- k (X and Y)
- dC, dH
- elephant foot value
- the smallest reliable hole and peg
- g_slip and g_run

Rerun dim02, dim03 and dim05 after any nozzle swap, filament brand or lot change, or profile speed change.
