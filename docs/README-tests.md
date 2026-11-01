# Test models: index

Every STL in `stl/`, what it is for, and which document explains it. Settings per filament: [filament-settings.md](filament-settings.md). Overall procedure: `research/07-review-and-master-procedure.md`.

Rebuild and check everything from the project root:

```
.venv/Scripts/python -I tests-src/dimensional.py
.venv/Scripts/python -I tests-src/temp_stringing.py            # add --markdown to print the M104 tables
.venv/Scripts/python -I tests-src/overhang_bridge_detail.py
.venv/Scripts/python -I tests-src/qa_check.py                  # independent QA of every STL, exit 1 on failure
```

`qa_check.py` checks each mesh (watertight, consistent winding, positive volume, expected body count, fits the 256 mm bed with a 5 mm margin, base on z = 0, every horizontal face on the nozzle's layer grid) and measures the features the docs describe (tower block heights and M104 tables, overhang angles, bridge spans, wall widths as multiples of the line width, hole/peg/pin diameters).

**Conventions.** Front of the printer = −Y. Keep each model where Bambu Studio puts it (plate centre) and do not rotate it. Use the files in `stl/0.4/` with the 0.4 nozzle (0.20 mm layers, 0.42 mm lines) and `stl/0.2/` with the 0.2 nozzle (0.10 mm layers, 0.22 mm lines). Heights are whole numbers of layers, so do not use a different layer height or adaptive layers.

**Placement on the A1.** The A1 purges and wipes off the plate (left of X 0 and behind the plate), so there is no front-left exclusion zone as on X1/P1 printers. The stock start G-code draws short extrusion-test lines on the front edge (Y −0.5 to 1.0, X 108–158), so keep models away from the front edge. `dim01` (220 mm) reaches the back-right head-wrap detection zone (X ≥ 226, Y ≥ 224); that only makes the printer skip its head-wrap check for that print.

Mass is approximate solid volume x 1.24 g/cm³; the printed part weighs less (15 % infill).

| File | Purpose | Nozzle | Size X x Y x Z (mm) | Solid mass (g) | Doc |
|---|---|---|---|---|---|
| `stl/0.4/dim01_first-layer-squares_0.4n_h0.20.stl` | First layer: 9 single-layer squares across the bed (9 separate bodies) | 0.4 | 220.0 x 220.0 x 0.2 | 1.4 | [tests-dimensional.md](tests-dimensional.md) |
| `stl/0.4/dim02_xy-gauge-100-20_0.4n.stl` | XY gauge: 100 mm frame + 20 mm island (shrinkage, contour/hole offsets) | 0.4 | 100.0 x 100.0 x 4.0 | 5.2 | [tests-dimensional.md](tests-dimensional.md) |
| `stl/0.4/dim03_hole-peg-gauge_0.4n.stl` | Hole and peg gauge at nominal diameters (X-Y hole compensation) | 0.4 | 71.0 x 36.0 x 9.0 | 10.3 | [tests-dimensional.md](tests-dimensional.md) |
| `stl/0.4/dim04_fit-clearance-D6_0.4n.stl` | Fit / clearance series + test pin (2 bodies) | 0.4 | 63.2 x 37.6 x 11.6 | 8.1 | [tests-dimensional.md](tests-dimensional.md) |
| `stl/0.4/dim05_elephant-foot_0.4n.stl` | Elephant-foot ring | 0.4 | 20.0 x 20.0 x 6.0 | 1.3 | [tests-dimensional.md](tests-dimensional.md) |
| `stl/0.4/temp_tower_225-195_0.4.stl` | Temperature tower 225 → 195 °C (7 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.4 | 63.9 x 18.0 x 71.0 | 29.8 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.4/temp_tower_230-190_0.4.stl` | Temperature tower 230 → 190 °C (9 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.4 | 63.9 x 18.0 x 91.0 | 37.9 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.4/temp_tower_230-200_0.4.stl` | Temperature tower 230 → 200 °C (7 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.4 | 63.9 x 18.0 x 71.0 | 29.8 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.4/temp_tower_235-200_0.4.stl` | Temperature tower 235 → 200 °C (8 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.4 | 63.9 x 18.0 x 81.0 | 33.8 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.4/temp_tower_240-205_0.4.stl` | Temperature tower 240 → 205 °C (8 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.4 | 63.9 x 18.0 x 81.0 | 33.8 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.4/temp_tower_260-220_0.4.stl` | Temperature tower 260 → 220 °C (9 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.4 | 63.9 x 18.0 x 91.0 | 37.9 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.4/temp_tower_260-230_0.4.stl` | Temperature tower 260 → 230 °C (7 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.4 | 63.9 x 18.0 x 71.0 | 29.8 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.4/temp_tower_270-240_0.4.stl` | Temperature tower 270 → 240 °C (7 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.4 | 63.9 x 18.0 x 71.0 | 29.8 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.4/bridge_spans_0.4.stl` | Bridges of increasing span (bridge flow, speed, cooling) | 0.4 | 228.6 x 16.0 x 9.0 | 9.6 | [tests-overhang-bridge-detail.md](tests-overhang-bridge-detail.md) |
| `stl/0.4/min_feature_0.4.stl` | Thin walls, pins, holes, slots scaled to line width | 0.4 | 66.0 x 56.6 x 7.6 | 9.6 | [tests-overhang-bridge-detail.md](tests-overhang-bridge-detail.md) |
| `stl/0.4/overhang_angles_0.4.stl` | Overhang fins 20–75° from vertical, 5° steps (cooling / overhang tuning) | 0.4 | 130.0 x 21.0 x 16.0 | 12.4 | [tests-overhang-bridge-detail.md](tests-overhang-bridge-detail.md) |
| `stl/0.4/retraction_coupon_0.4.stl` | One print per retraction length (2 pins + marker tab) | 0.4 | 52.0 x 10.0 x 12.6 | 0.7 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.4/retraction_tower_devmode_0.4.stl` | Optional, untested: replacement model for the developer-mode Retraction test | 0.4 | 39.0 x 8.0 x 21.4 | 1.2 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.4/stringing_pins_0.4.stl` | Stringing check of the final temperature and retraction (3 pins, two travel gaps) | 0.4 | 69.0 x 9.0 x 25.6 | 2.0 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.4/verify_combo_0.4.stl` | Final check of a saved profile: corners, top, holes, overhangs, bridge, seam | 0.4 | 56.0 x 35.0 x 20.0 | 9.4 | [tests-overhang-bridge-detail.md](tests-overhang-bridge-detail.md) |
| `stl/0.2/dim01_first-layer-squares_0.2n_h0.10.stl` | First layer: 9 single-layer squares across the bed (9 separate bodies) | 0.2 | 220.0 x 220.0 x 0.1 | 0.4 | [tests-dimensional.md](tests-dimensional.md) |
| `stl/0.2/dim02_xy-gauge-100-20_0.2n.stl` | XY gauge: 100 mm frame + 20 mm island (shrinkage, contour/hole offsets) | 0.2 | 100.0 x 100.0 x 3.0 | 3.3 | [tests-dimensional.md](tests-dimensional.md) |
| `stl/0.2/dim03_hole-peg-gauge_0.2n.stl` | Hole and peg gauge at nominal diameters (X-Y hole compensation) | 0.2 | 53.8 x 23.5 x 6.0 | 3.3 | [tests-dimensional.md](tests-dimensional.md) |
| `stl/0.2/dim04_fit-clearance-D3_0.2n.stl` | Fit / clearance series + test pin (2 bodies) | 0.2 | 41.6 x 26.3 x 7.0 | 2.9 | [tests-dimensional.md](tests-dimensional.md) |
| `stl/0.2/dim05_elephant-foot_0.2n.stl` | Elephant-foot ring | 0.2 | 15.0 x 15.0 x 4.0 | 0.5 | [tests-dimensional.md](tests-dimensional.md) |
| `stl/0.2/temp_tower_225-195_0.2.stl` | Temperature tower 225 → 195 °C (7 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.2 | 40.2 x 12.0 x 42.6 | 7.9 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.2/temp_tower_230-190_0.2.stl` | Temperature tower 230 → 190 °C (9 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.2 | 40.2 x 12.0 x 54.6 | 10.0 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.2/temp_tower_230-200_0.2.stl` | Temperature tower 230 → 200 °C (7 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.2 | 40.2 x 12.0 x 42.6 | 7.9 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.2/temp_tower_235-200_0.2.stl` | Temperature tower 235 → 200 °C (8 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.2 | 40.2 x 12.0 x 48.6 | 9.0 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.2/temp_tower_240-205_0.2.stl` | Temperature tower 240 → 205 °C (8 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.2 | 40.2 x 12.0 x 48.6 | 9.0 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.2/temp_tower_260-220_0.2.stl` | Temperature tower 260 → 220 °C (9 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.2 | 40.2 x 12.0 x 54.6 | 10.0 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.2/temp_tower_260-230_0.2.stl` | Temperature tower 260 → 230 °C (7 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.2 | 40.2 x 12.0 x 42.6 | 7.9 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.2/temp_tower_270-240_0.2.stl` | Temperature tower 270 → 240 °C (7 blocks, 5 °C each); bridge, 45/60° overhangs and stringing window per block | 0.2 | 40.2 x 12.0 x 42.6 | 7.9 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.2/bridge_spans_0.2.stl` | Bridges of increasing span (bridge flow, speed, cooling) | 0.2 | 110.9 x 10.2 x 5.6 | 2.0 | [tests-overhang-bridge-detail.md](tests-overhang-bridge-detail.md) |
| `stl/0.2/min_feature_0.2.stl` | Thin walls, pins, holes, slots scaled to line width | 0.2 | 40.0 x 39.4 x 5.0 | 2.5 | [tests-overhang-bridge-detail.md](tests-overhang-bridge-detail.md) |
| `stl/0.2/overhang_angles_0.2.stl` | Overhang fins 20–75° from vertical, 5° steps (cooling / overhang tuning) | 0.2 | 84.5 x 14.7 x 11.7 | 4.2 | [tests-overhang-bridge-detail.md](tests-overhang-bridge-detail.md) |
| `stl/0.2/retraction_coupon_0.2.stl` | One print per retraction length (2 pins + marker tab) | 0.2 | 36.0 x 7.0 x 8.4 | 0.2 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.2/stringing_pins_0.2.stl` | Stringing check of the final temperature and retraction (3 pins, two travel gaps) | 0.2 | 42.4 x 6.4 x 15.4 | 0.5 | [tests-temp-stringing.md](tests-temp-stringing.md) |
| `stl/0.2/verify_combo_0.2.stl` | Final check of a saved profile: corners, top, holes, overhangs, bridge, seam | 0.2 | 33.6 x 21.0 x 12.0 | 2.0 | [tests-overhang-bridge-detail.md](tests-overhang-bridge-detail.md) |

## Which temperature tower for which filament

| Filament | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| ELEGOO Matte PLA (purple, reference) | `temp_tower_230-190_0.4.stl` | `temp_tower_compact_230-190_0.2.stl` (4 mm blocks, 28.8 x 9 x 36.6 mm, about 1 h 10 min; generator `tests-src/temp_tower_compact.py`) |
| ELEGOO PLA | `temp_tower_230-190_0.4.stl` | `temp_tower_225-195_0.2.stl` |
| ELEGOO PLA+ | `temp_tower_235-200_0.4.stl` | `temp_tower_230-200_0.2.stl` |
| ELEGOO Rapid PLA+ | `temp_tower_235-200_0.4.stl` | `temp_tower_230-200_0.2.stl` |
| Keytek PLA | `temp_tower_240-205_0.4.stl` | `temp_tower_230-200_0.2.stl` |
| ELEGOO PETG PRO (blue) | `temp_tower_260-230_0.4.stl` | `temp_tower_260-230_0.2.stl` |
| ELEGOO Rapid PETG (clear) | `temp_tower_270-240_0.4.stl` | `temp_tower_270-240_0.2.stl` |
| spare: PETG of unknown line | `temp_tower_260-220_0.4.stl` | `temp_tower_260-220_0.2.stl` |

The remaining ranges (for example `240-205_0.2`) are spares. Matte PLA is the reference filament; see [reference-offset-method.md](reference-offset-method.md). Height → `M104` tables for every tower: [tests-temp-stringing.md](tests-temp-stringing.md), section 1.
