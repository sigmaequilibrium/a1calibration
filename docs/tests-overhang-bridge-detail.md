# Overhang, bridge, fine-detail and verification tests

Generator: `tests-src/overhang_bridge_detail.py`. To rebuild every STL and re-run the checks:

```
.venv/Scripts/python -I tests-src/overhang_bridge_detail.py
```

| File | Size X x Y x Z (mm) | Volume |
|---|---|---|
| `stl/0.4/overhang_angles_0.4.stl` | 130.0 x 21.0 x 16.0 | 9.96 cm3 |
| `stl/0.4/bridge_spans_0.4.stl` | 228.6 x 16.0 x 9.0 | 7.70 cm3 |
| `stl/0.4/min_feature_0.4.stl` | 66.0 x 56.6 x 7.6 | 7.76 cm3 |
| `stl/0.4/verify_combo_0.4.stl` | 56.0 x 35.0 x 20.0 | 7.54 cm3 |
| `stl/0.2/overhang_angles_0.2.stl` | 84.5 x 14.7 x 11.7 | 3.36 cm3 |
| `stl/0.2/bridge_spans_0.2.stl` | 110.95 x 10.2 x 5.6 | 1.64 cm3 |
| `stl/0.2/min_feature_0.2.stl` | 40.0 x 39.4 x 5.0 | 2.04 cm3 |
| `stl/0.2/verify_combo_0.2.stl` | 33.6 x 21.0 x 12.0 | 1.62 cm3 |

The generator checks every mesh after export. Each one is a single body, watertight, with consistent winding and positive volume. It sits on Z=0 and fits the 256 mm bed.

## Conventions

- **Front is -Y.** Every part has a label strip along its front edge, and the labels read correctly when you look at the part from the front. Labels are engraved, using 7-segment digits made from boxes.
- **Nozzle marker.** The leftmost label slot on each part, or the label on the front strip of the verification part, reads `.4` or `.2`. Use it to tell the two sets apart after printing.
- **Overhang angles are measured from vertical.** 0° is a vertical wall and 90° is a flat ceiling. A "45" fin has a 45° overhang. A "75" fin is only 15° above horizontal. Some guides measure from horizontal, so check which convention they use before you compare results.
- **Change one variable at a time.** Write the filament, preset, and the one changed setting on the part with a marker.
- **Turn supports off for every part here.** Bambu Studio: Process > Support > *Enable support* = off. If supports are on, they fill the overhangs and bridges you are trying to test.
- **Keep the default orientation.** Place each part as imported and do not rotate it. The A1 cools one side of the toolhead more than the other, so a fin's quality depends on where the fan sits. If you want to see that effect, print a second copy rotated 180° about Z.

### Base slicer settings per nozzle

| | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Printer preset | Bambu Lab A1 0.4 nozzle | Bambu Lab A1 0.2 nozzle |
| Process preset | 0.20mm Standard @BBL A1 | 0.10mm Standard @BBL A1 0.2 nozzle (the 0.2-nozzle "Standard" preset) |
| Layer height | 0.20 | 0.10 |
| Line widths | 0.42 | 0.22 |
| Walls / top / bottom | preset defaults | preset defaults |
| Sparse infill | 15% (preset default) | 15% (preset default) |
| Supports | **off** | **off** |
| Brim | Auto/none. The PETG bridge part may need a brim (see that section). | Auto/none |
| Filament | your tuned preset (flow ratio, PA, temperature, and max volumetric speed already calibrated) | same filament, with a 0.2-nozzle preset |

Do flow, pressure advance (PA), and temperature first, as described in `research/07-review-and-master-procedure.md`. These tests tune cooling, overhangs, bridges, and small features on top of those values.

The tables below map each fin label to how far that layer overhangs the one below, as a percentage of the line width. Use them to match the Bambu Studio overhang settings to specific fins. Those settings are the overhang speed bands and *Cooling overhang threshold*. Percentage = layer x tan(angle) / line width.

| Fin label (°) | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 | 65 | 70 | 75 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.4 (0.20 layer / 0.42 width) | 17% | 22% | 27% | 33% | 40% | 48% | 57% | 68% | 82% | 102% | 131% | 178% |
| 0.2 (0.10 layer / 0.22 width) | 17% | 21% | 26% | 32% | 38% | 45% | 54% | 65% | 79% | 97% | 125% | 170% |

Bambu Studio's overhang speed bands are *10%-25%*, *25%-50%*, *50%-75%* and *75%-100%* of the line width. So:

- 20-25° fins fall in the first band.
- 30-45° fins fall in the second.
- 50-55° fins fall in the third.
- The 60° fin falls in the fourth.
- At about 65° and above, each layer overhangs by a full line width or more. The slicer then treats those perimeters as unsupported, close to a bridge. Expect failure at 70-75° with any profile. Those fins are there to show the limit.

---

## 1. Overhang test: `overhang_angles_<nozzle>.stl`

**Purpose.** Tune cooling and overhang slow-down for each filament.

**Geometry.**
- 12 fins labelled 20 to 75 in 5° steps. Each fin has a vertical front face and an overhanging back face toward +Y.
- The overhang reaches 10 mm horizontally on the 0.4 part and 7 mm on the 0.2 part. Low-angle fins are capped at 12 mm high (0.4) or 9 mm high (0.2), so their reach is shorter.
- All fins finish at the same top height, which makes them easy to compare side by side.
- The base plate only covers the label strip and the fin roots. That leaves the overhang undersides clear, so you can inspect them from behind and below.
- Fin width is 8 mm (0.4) or 5 mm (0.2).

**Settings.** Use the base settings above. Print one copy per filament.

**What to look for.** View each fin from the side, and look at its underside with a light behind it.
- **Curl-up.** The edge of the overhang lifts and the nozzle may scrape it. This means not enough cooling, or the layer is not cooling before the next one goes down.
- **Droop/sag.** The underside is wavy, the lines hang down, and the overhang face looks stair-stepped and rough.
- **Rough or "spaghetti" underside.** Lines are not attached to the layer below.
- **Wall-quality changes at band boundaries.** For example, the surface finish changes between the 45 and 50 fins. That happens when the overhang slow-down speed jumps from one band to the next.

**What to adjust in Bambu Studio** (one change at a time; arrows show which direction to move):

| Symptom | Setting (location) | Direction |
|---|---|---|
| Droop, curl, rough underside at moderate angles | Filament > Cooling > *Fan speed for overhangs* (`overhang_fan_speed`) | Up, to 100% for PLA. Try 60-90% for PETG. |
| Overhang fan only starts at steeper fins | Filament > Cooling > *Cooling overhang threshold* (`overhang_fan_threshold`) | Down (for example 25% or 10%), so the fan turns on at lower overhang percentages. Check the result against the table above. |
| Overhang fan setting has no effect | Filament > Cooling > *Force cooling for overhangs and bridges* (`enable_overhang_bridge_fan`) | Turn it on |
| General droop on every fin, or soft layers on small fins | Filament > Cooling > *Fan min speed* / *Fan max speed* and *Layer time* thresholds | Raise the fan for PLA (min toward 80-100%). For PETG, raise it only until layer bonding gets weak. |
| Overhang quality drops at one band | Process > Speed > *Slow down for overhangs* (`enable_overhang_speed`) and the band speeds *10%-25%*, *25%-50%*, *50%-75%*, *75%-100%* | Turn slow-down on. Lower the speed of the band that matches the first poor fin, for example to 10-20 mm/s for 75-100%. |
| Edge curls up | Process > Speed > *Slow down for curled perimeters* (if your version has it) | Turn it on |
| Overhang wall quality | Process > Quality > *Detect overhang wall* | On (the default) |
| Overhang wall quality on newer Bambu Studio | Process > Quality > *Reverse on odd* / overhang reverse (version-dependent) | Try it on, and keep it only if the underside improves |
| Droop that cooling does not fix | Filament > *Nozzle temperature* | Down 5 °C (keep it within the range your temperature tower showed was good) |
| Clear PETG looks hazy or brittle at full fan | Lower overhang fan and fan max | Down. Accept a lower pass angle. |

**Pass criteria** (from vertical):

| Filament | 0.4 nozzle: clean up to | 0.2 nozzle: clean up to |
|---|---|---|
| PLA, PLA+, Rapid PLA | at least 55°, ideally 60° | at least 55°, ideally 60° |
| Budget PLA | at least 50° | at least 50° |
| PETG, Rapid PETG | at least 45-50° | at least 45-50° |

- **Clean** means no visible curl, an underside without loose loops, and a face that is only slightly rougher than the vertical side.
- **Usable** fins (5-10° steeper than the clean limit) may be a bit rough but must not curl. Record the steepest usable angle for each filament. Your support *Threshold angle* depends on it. Note that support thresholds in Bambu Studio are measured from horizontal: a 55° from-vertical limit equals a 35° threshold.

---

## 2. Bridge test: `bridge_spans_<nozzle>.stl`

**Purpose.** Tune bridge flow, bridge cooling, and bridge speed, and find the longest span that still bridges cleanly.

**Geometry.**
- Separate bridges, each made of two pillars and a slab.
- Labels give the span (the clear gap) in mm:
  - 0.4 part: spans 5, 10, 20, 30, 40, 50. Pillars are 4 mm wide and 8 mm deep (Y). The underside is 8 mm above the bed and the slab is 1.0 mm thick.
  - 0.2 part: spans 3, 5, 8, 12, 16, 20. Pillars are 2.5 mm wide and 5 mm deep. The underside is 5 mm above the bed and the slab is 0.6 mm thick.
- Each bridge is a separate slab, so the slicer picks the bridge direction for each one (across the gap, pillar to pillar).
- The front strip joins the pillars. The space under each bridge is open down to the bed.
- At 228.6 mm long, the 0.4 part nearly fills the bed. Place it along X, as it imports, and leave it centred (Bambu Studio's default). Reviewed against the stock A1 G-code (BambuStudio master, 2026-10): the A1 purges and wipes **off the plate** (X −48 to −28, and the steel strip behind the plate at Y 261), so there is no front-left exclusion zone as on the X1/P1. The only things drawn on the plate are the extrusion-test lines along the front edge (Y −0.5 to 1.0, X 108–158). Centred, the part spans X 13.7–242.3 and Y 120–136, more than 100 mm clear of those lines, so it was not shortened. Do not drag it to the front edge.

**Settings.** Use the base settings above with supports off. Check the slicer preview: the first slab layer in each gap must show as **Bridge** (a distinct colour in the line-type view) and run across the gap. If it shows as top or internal solid infill, the slab is not being treated as a bridge.
- The 0.4 pillars are thin, 9 mm tall, and spread over about 230 mm. On PETG, or on a smooth PEI plate, add a brim if the pillars lift: Process > Others > *Brim type* = Outer brim only, 3 mm.

**What to look for.**
- How far the underside sags in the middle of each span. Check it with a straightedge or calipers across the bottom of the slab.
- Broken or loose strands, and gaps between strands.
- Strands that pulled back and left the bridge edge ragged where it meets the pillar.
- The top surface above the bridge. Pillowing or holes there mean the internal layers above the bridge were also short of support.

**What to adjust in Bambu Studio:**

| Symptom | Setting (location) | Direction |
|---|---|---|
| Strands sag, look wide and droopy, or touch each other unevenly | Process > Quality > *Bridge flow* (`bridge_flow`, A1 default 1.0) | Down in steps of 0.05 (0.95, then 0.90; rarely below 0.85) |
| Gaps between strands, thin strands that snap | *Bridge flow* | Up in 0.05 steps |
| Long spans (30 mm or more on 0.4) break | Process > Quality > *Thick bridges* (`thick_bridges`) | On. Strands are printed at nozzle-diameter height and survive long spans better, but they are a little heavier. Off gives neater short bridges. |
| Sag on every span | Filament > Cooling > *Force cooling for overhangs and bridges* on, *Fan speed for overhangs* | Up (100% for PLA, 70-100% for PETG) |
| Sag, strands not stretched tight | Process > Speed > *Bridge* (`bridge_speed`, A1 default about 50 mm/s) | Try both directions in 10 mm/s steps. Slower helps on PETG. Somewhat faster can pull PLA strands tighter. Keep the change that reduces sag. |
| Sag even with full fan | Filament > *Nozzle temperature* | Down 5 °C |
| Holes or pillowing in the top above the bridge | Process > Strength > *Top shell layers* / *Top shell thickness*. Internal bridge settings (version-dependent, for example *Thick internal bridges*). | Raise top shells by 1-2. Turn thick internal bridges on. |

**Pass criteria.**

| | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| PLA family: clean (sag under 0.3 mm, no broken strands) | spans up to 20 mm, ideally 30 mm | spans up to 8 mm, ideally 12 mm |
| PLA family: survives (closed, sag under 1 mm) | 40 mm | 16 mm |
| PETG and Rapid PETG: clean | 10-20 mm | 5-8 mm |
| Budget PLA | as PLA, minus one step | as PLA, minus one step |

The 50 mm span (0.4) and the 20 mm span (0.2) are meant to show the limit. Expect sag there.

---

## 3. Fine-detail / minimum-feature test: `min_feature_<nozzle>.stl`

**Purpose.** Find the smallest feature each nozzle prints reliably: thin walls, pins, holes, and gaps. Use the result to decide when a model needs the 0.2 nozzle. Also check how Bambu Studio's wall generator handles walls thinner than one line.

**Geometry.** Four rows on one base plate, front to back. Each row has its own engraved labels in front of it. The `.4` or `.2` marker is in the empty left column.

| Row | Labels mean | 0.4 nozzle values | 0.2 nozzle values | Feature |
|---|---|---|---|---|
| 1. Thin walls | multiple of line width | .5 .75 1 1.5 2 3 4 x 0.42 = 0.21, 0.315, 0.42, 0.63, 0.84, 1.26, 1.68 mm | same multiples x 0.22 = 0.11, 0.165, 0.22, 0.33, 0.44, 0.66, 0.88 mm | free-standing walls running front to back. 0.4: 8 mm long, 6 mm tall. 0.2: 5 mm long, 4 mm tall. |
| 2. Pins | diameter, mm | .5 .8 1 1.5 2 3 | .3 .5 .8 1 1.5 2 | round pins. 0.4: 6 mm tall. 0.2: 4 mm tall. |
| 3. Holes | diameter, mm | .5 .8 1 1.5 2 3 | .3 .5 .8 1 1.5 2 | vertical holes through a block (0.4: 3 mm, 0.2: 2 mm) and through the base, so you can see light through them |
| 4. Gaps | slot width, mm | .1 .2 .3 .4 .6 .8 | .05 .1 .15 .2 .3 .4 | slots through a comb block, stopping at the base |

**Settings.** Use the base settings above. Print it **twice** if you can:
- once with Process > Quality > *Wall generator* = **Arachne**;
- once with *Wall generator* = **Classic** and *Detect thin wall* = off.

The difference between the two prints shows how each generator handles walls below one line width. Do not change *X-Y hole compensation* or *X-Y contour compensation* for the first print. Leave them at 0 so you see the raw result.

**What to look for and expected behaviour.** Check the slicer preview first, then the print.

- **Walls.**
  - Classic, with *Detect thin wall* off, usually drops any wall narrower than about one line width. On the 0.4 part, expect the .5 and .75 walls to be missing, and maybe the 1 wall too. With *Detect thin wall* on, they come back as a single line or gap fill.
  - Arachne keeps any wall wider than *Minimum feature size* (`min_feature_size`, default 25% of the nozzle diameter, which is 0.10 mm on 0.4 and 0.05 mm on 0.2). It prints such walls at least *Minimum wall width* (`min_bead_width`, default 85% of the nozzle diameter, which is 0.34 mm on 0.4 and 0.17 mm on 0.2). So the .5 and .75 walls print, but **wider than modelled**.
  - Measure the 2x, 3x and 4x walls with calipers.
- **Pins.** Look for pins that are missing, bent, melted into blobs, or knocked over by travel moves, and for strings between pins. Small pins have very short layer times. That tests the cooling slow-down settings.
- **Holes.** Note the smallest hole that is open all the way through: hold the part up to a light, or push a drill bit or wire through. Measure the larger holes with drill bits used as gauge pins, or with calipers.
- **Gaps.** Note the smallest slot that is open all the way down, so light passes through and a feeler gauge or paper slides in. Slots narrower than the extrusion squish tend to fuse.

**What to adjust in Bambu Studio:**

| Symptom | Setting (location) | Direction |
|---|---|---|
| Thin walls (below 1x) are missing, and you need them | Process > Quality > *Wall generator* = Arachne, **or** Classic with *Detect thin wall* on | Turn it on |
| Arachne prints thin walls too thick | Process > Quality > *Minimum wall width* (`min_bead_width`) | Down (for example 85% to 60%). Below about 50%, under-extrusion and weak walls are likely. |
| Arachne drops a wall you want | *Minimum feature size* (`min_feature_size`) | Down |
| Walls measure consistently too wide or too narrow at 2-4x | Re-check the filament *Flow ratio* first (do not compensate here) | Change the flow ratio to fix it |
| Pins melt or blob | Filament > Cooling > *Slow printing down for better layer cooling* on. *Layer time* (`slow_down_layer_time`): raise it. *Min print speed*: lower it. Fan: up. | Up/on. Or print a second, sacrificial copy next to it to lengthen the layer time. |
| Pins knocked over | Printer > Extruder > *Z hop type* = Slope or Spiral. Process > Others > *Avoid crossing wall* on. | On |
| Strings between pins | Filament > Setting Overrides > *Retraction length* and drying | See the retraction step in `research/06-retraction-dimensional-verify.md` |
| Holes undersized | Process > Quality > *X-Y hole compensation* (`xy_hole_compensation`) | Up, by half the measured diameter error, for example +0.05 mm if a 3.0 mm hole measures 2.9 mm |
| Outside dimensions wrong | *X-Y contour compensation* | In the direction that fixes the error, by half the error. Use the dimensional test for this, not this part. |
| Small gaps fused | Lower *Flow ratio* only if the walls also measure wide. Otherwise this is a physical limit. | |

**Pass criteria.**

| Feature | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Walls 1x and up | All present. 2x/3x/4x within ±0.05 mm of model. | All present. 2x/3x/4x within ±0.03 mm. |
| Walls below 1x | Present with Arachne (width at least `min_bead_width`). Missing with Classic and *Detect thin wall* off. (This is expected and only shows how each generator behaves.) | same |
| Pins | 1.0 mm and up standing, round, not blobbed. 0.8 mm acceptable. | 0.5 mm and up standing and round. 0.3 mm acceptable. |
| Holes | 1.0 mm and up open. 2-3 mm within -0.1 mm (after compensation, ±0.05). | 0.5 mm and up open. 1.5-2 mm within -0.05 mm. |
| Gaps | 0.3 mm and up open all the way down. 0.2 mm is a bonus. | 0.15 mm and up open. 0.1 mm is a bonus. |

The 0.2 nozzle should beat the 0.4 by roughly one to two columns on every row. If it does not, check the 0.2 flow ratio, PA, and max volumetric speed first. The 0.2 nozzle reaches its volumetric limit early, so PA and flow tuned on the 0.4 do not carry over.

---

## 4. Verification part: `verify_combo_<nozzle>.stl`

**Purpose.** A quick check of a finished filament + process profile, run after tuning or after a filament or nozzle change. The 0.2 version is the same design scaled to 0.6x, except that the base plate is rounded to 0.7 mm (7 layers) so it stays on the 0.10 mm layer grid. Both take roughly 20-35 min (slice to confirm).

**Geometry (0.4; multiply by 0.6 for 0.2).**
- **Main block.** 20 x 20 x 10 mm.
  - The top surface shows top-surface quality.
  - The four vertical edges show corners for PA.
  - Ø3 mm and Ø5 mm vertical holes check hole size. On 0.2 they are Ø1.8 and Ø3.0.
  - A Ø4 mm horizontal hole runs along X. Its roof is a natural overhang test. On 0.2 it is Ø2.4.
- **Two overhang wedges.** They hang off the back of the block, 45° (left) and 60° (right) from vertical, each reaching 6 mm.
- **Bridge.** A 20 mm bridge (12 mm on 0.2) between two pillars, 8 mm above the bed.
- **Cylinder.** Ø10 x 20 mm (Ø6 x 12 on 0.2), for checking the seam and Z-banding/wobble.
- **Base plate.** All of the above sit on a base plate. The `.4`/`.2` marker is engraved on the front strip.

**Settings.** Use the final saved filament and process presets **unchanged**. Note the seam setting: Process > Quality > *Seam position*, Aligned by default.

**What to look for, and what to adjust:**

| Area | Look for | If it fails, adjust |
|---|---|---|
| Block corners | Bulge or gap at the corners, and ringing next to them | PA (K value): bulge means K too low, gap or rounding means K too high. Re-run PA calibration rather than guessing. For ringing, lower the outer wall speed or acceleration. |
| Block top | Smooth, closed, no ridges or pinholes | Flow ratio. Process > Quality > *Top surface pattern* / *Ironing* (optional). For pinholes, more top layers. |
| Vertical holes | Ø3 and Ø5 within ±0.1 mm (0.4) or ±0.05 mm (0.2) | *X-Y hole compensation* |
| Horizontal hole | Round. A slight droop at the roof is fine, but a 0.2 mm+ step is not. | Overhang cooling (Section 1) |
| 45°/60° wedges | 45° clean. 60° clean on PLA and acceptable on PETG. | Section 1 |
| Bridge | 20 mm span (12 mm on 0.2) with no visible sag and no broken strands | Section 2 |
| Cylinder | Seam: a thin, even line with no blob or gap. Walls: no regular Z-banding, no wobble, round. | Seam blob means retraction, or *Wipe on loops* / scarf seam (Process > Quality > *Scarf joint seam*, version-dependent). Gap means PA too high or *Seam gap* too large. Banding usually means a mechanical issue (belts, Z axis, or a loose toolhead), or a temperature or flow that varies from layer to layer. |
| Everything | No stringing between the cylinder, pillars and block | Retraction, drying, temperature |

**Pass criteria.** Every row in the table passes. In short:
- sharp corners;
- smooth top;
- holes within tolerance;
- 45° clean (60° clean on PLA);
- bridge flat;
- seam unobtrusive;
- no strings.

If one area fails, fix it with the matching full test (Sections 1-3 or the PA/flow calibrations) rather than with the verification part.

---

## Notes

- Approximate print times are rough guesses until you slice. Expect the 0.4 overhang part to take about 45-60 min and the 0.4 bridge about 30-40 min. Prints with the 0.2 nozzle run at 0.10 mm layers and a much lower volumetric limit, so they take several times longer than their volume suggests.
- To change spans, angles, sizes or label sizes, edit the `NOZ` dictionary at the top of the generator and re-run it. The validation runs again automatically. The run fails (exit code 1) if any mesh is not a single watertight body, or if it does not fit the bed.
- Setting names follow Bambu Studio 1.9/2.x. Some options are marked version-dependent; if you cannot find one, use the search box in the settings panel (the magnifier).
