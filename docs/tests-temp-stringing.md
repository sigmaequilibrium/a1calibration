# Temperature and stringing / retraction tests (A1, Bambu Studio)

Generator: `tests-src/temp_stringing.py`. To rebuild every STL in this document and print the height tables:

```
.venv/Scripts/python -I tests-src/temp_stringing.py
```

The script checks every mesh: it must be watertight, have consistent winding and positive volume, be a single body, fit the 256 mm bed, and have a total height that is a whole number of layers.

| File | Size X x Y x Z (mm) | Purpose |
|---|---|---|
| `stl/0.4/temp_tower_230-190_0.4.stl` | 63.9 x 18.0 x 91.0 | Temperature tower 230 → 190 °C, 9 blocks |
| `stl/0.4/temp_tower_225-195_0.4.stl` | 63.9 x 18.0 x 71.0 | Temperature tower 225 → 195 °C, 7 blocks |
| `stl/0.4/temp_tower_235-200_0.4.stl` | 63.9 x 18.0 x 81.0 | Temperature tower 235 → 200 °C, 8 blocks |
| `stl/0.4/temp_tower_230-200_0.4.stl` | 63.9 x 18.0 x 71.0 | Temperature tower 230 → 200 °C, 7 blocks |
| `stl/0.4/temp_tower_240-205_0.4.stl` | 63.9 x 18.0 x 81.0 | Temperature tower 240 → 205 °C, 8 blocks |
| `stl/0.4/temp_tower_260-220_0.4.stl` | 63.9 x 18.0 x 91.0 | Temperature tower 260 → 220 °C, 9 blocks |
| `stl/0.4/temp_tower_260-230_0.4.stl` | 63.9 x 18.0 x 71.0 | Temperature tower 260 → 230 °C, 7 blocks |
| `stl/0.4/temp_tower_270-240_0.4.stl` | 63.9 x 18.0 x 71.0 | Temperature tower 270 → 240 °C, 7 blocks |
| `stl/0.4/stringing_pins_0.4.stl` | 69.0 x 9.0 x 25.6 | Stringing check of the final settings |
| `stl/0.4/retraction_coupon_0.4.stl` | 52.0 x 10.0 x 12.6 | Short coupon, one print per retraction value |
| `stl/0.4/retraction_tower_devmode_0.4.stl` | 39.0 x 8.0 x 21.4 | Optional, experimental: retraction tower for Bambu's developer-mode rule |
| `stl/0.2/temp_tower_230-190_0.2.stl` | 40.2 x 12.0 x 54.6 | Temperature tower 230 → 190 °C, 9 blocks |
| `stl/0.2/temp_tower_225-195_0.2.stl` | 40.2 x 12.0 x 42.6 | Temperature tower 225 → 195 °C, 7 blocks |
| `stl/0.2/temp_tower_235-200_0.2.stl` | 40.2 x 12.0 x 48.6 | Temperature tower 235 → 200 °C, 8 blocks |
| `stl/0.2/temp_tower_230-200_0.2.stl` | 40.2 x 12.0 x 42.6 | Temperature tower 230 → 200 °C, 7 blocks |
| `stl/0.2/temp_tower_240-205_0.2.stl` | 40.2 x 12.0 x 48.6 | Temperature tower 240 → 205 °C, 8 blocks |
| `stl/0.2/temp_tower_260-220_0.2.stl` | 40.2 x 12.0 x 54.6 | Temperature tower 260 → 220 °C, 9 blocks |
| `stl/0.2/temp_tower_260-230_0.2.stl` | 40.2 x 12.0 x 42.6 | Temperature tower 260 → 230 °C, 7 blocks |
| `stl/0.2/temp_tower_270-240_0.2.stl` | 40.2 x 12.0 x 42.6 | Temperature tower 270 → 240 °C, 7 blocks |
| `stl/0.2/stringing_pins_0.2.stl` | 42.4 x 6.4 x 15.4 | Stringing check of the final settings |
| `stl/0.2/retraction_coupon_0.2.stl` | 36.0 x 7.0 x 8.4 | Short coupon, one print per retraction value |

Which tower to print for which filament and nozzle: see **Which tower for which filament** in section 1.

The STLs are centred on the origin and sit on Z = 0. Every height in them is a whole multiple of that nozzle's layer height (0.20 mm for the 0.4 nozzle, 0.10 mm for the 0.2 nozzle).

---

## What Bambu Studio can and cannot change by height

I checked this against the BambuStudio source on GitHub (`MainFrame.cpp`, `Plater.cpp`, `libslic3r/GCode.cpp`).

- **Height range modifiers** (right-click the object, then *Height range Modifier*) can only change **process** settings, such as layer height, walls, infill and speed. Nozzle temperature is a filament setting, and retraction length is a filament or printer setting, so a modifier can change neither.
- **Temperature by height works.** Use custom G-code on the layer slider (`M104 S<temp>`). The towers below are built for this.
- **Retraction by height does not work with your own model.** Bambu Studio writes retractions as explicit extruder moves, so a G-code command inserted at a layer cannot change their length. The only per-height retraction feature is the built-in **Calibration > Retraction test**. Its menu is shown for Bambu printers only when Developer Mode is on. That test loads Bambu's own model and forces 0.2 mm layers, 2 walls, 0 top layers and 0 % infill. It sets
  `retraction length = start + floor(max(0, Z - 0.4)) * step`
  which means the value changes **every 1 mm of height** above Z = 0.4. The model is cut to a height of `1.4 + (end - start) / step` mm.
- The built-in **Calibration > Temperature** test (also Developer Mode only) uses fixed 10 mm blocks and 5 °C steps (`temp = start - floor(Z / 10.001) * 5`), on Bambu's own 0.4-sized model.

So the plan is:
- **Temperature:** use our towers plus `M104` at the layer heights listed below.
- **Retraction:** print `retraction_coupon` once for each retraction value (main method), or run the built-in developer-mode Retraction test. The `retraction_tower_devmode_0.4.stl` swap is optional and has not been tested.

---

## 1. Temperature towers

### Geometry (each block)

```
   45° overhang       label core         bridge window           pillar   60° overhang
      /|  ┌──────────┐┌═════════════════ bridge deck ════════════┐┌──────┐|\
     / |  │  2 3 0   ││    ^pin            ^pin                 ││      │| \
       |  │(engraved)││   /  \            /  \   (open in Y)     ││      │|
       └──┴──────────┘└──────────────────────────────────────────┘└──────┘┘
```

- **Left side of the label core:** a 45° overhang wedge.
- **Right side of the pillar:** a 60° overhang wedge, measured from vertical, so it is the harder one.
- **Window:** a through-window (open front to back). Its bridge deck forms the roof, and its floor is the previous block's deck.
- **Stringing pins:** two tapered pins stand on the window floor. Their tips stop below the bridge, so the bridge stays a true bridge. The nozzle travels core → pin → pin → pillar on every layer, so strings form in the window, where you can see them from the front.
- **Label:** the temperature is engraved on the front face (the −Y side, facing you on the plate). Keep the label facing the front when you place the tower.

| Dimension | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Layer height | 0.20 | 0.10 |
| Base plate | 1.0 mm (5 layers) | 0.6 mm (6 layers) |
| Block height | 10.0 mm (50 layers) | 6.0 mm (60 layers) |
| Block depth (Y) | 12 mm | 8 mm |
| Bridge span / deck | 24 mm / 1.0 mm | 14 mm / 0.6 mm |
| 45° wedge | 5 mm tall, 5 mm out | 3 mm tall, 3 mm out |
| 60° wedge | 4 mm tall, 6.9 mm out | 2.4 mm tall, 4.2 mm out |
| Pins | Ø3 → Ø1, 6 mm tall, 12 mm apart | Ø2 → Ø0.6, 3.5 mm tall, 7 mm apart |
| Engraved digits | 6 mm tall, 0.8 stroke, 0.6 deep | 4 mm tall, 0.6 stroke, 0.4 deep |

### Which tower for which filament

Every range is generated for both nozzles, so a spare range is always available. The towers assigned to your filaments are below. Ranges come from the manufacturer label (checked on 2026-10-06 where the store page was reachable) and from `research/10`–`12`, with the review changes noted. Full per-filament settings: `docs/filament-settings.md`.

| Filament | Label range (°C) | 0.4 nozzle tower | 0.2 nozzle tower | Notes |
|---|---|---|---|---|
| ELEGOO PLA | 190–230 | `temp_tower_230-190_0.4.stl` | `temp_tower_225-195_0.2.stl` | 0.4 tower = Bambu Studio's own PLA default range |
| ELEGOO PLA+ | 200–230 | `temp_tower_235-200_0.4.stl` | `temp_tower_230-200_0.2.stl` | top block 5 °C over the label max, on purpose (shows whether 230 is past the knee) |
| ELEGOO Rapid PLA+ | 200–230 | `temp_tower_235-200_0.4.stl` | `temp_tower_230-200_0.2.stl` | research/10 proposed 240→205; the review cut it to 235→200 (the tower prints slowly, 240 is 10 °C over the label). Use `240-205` only if you print near your MVS limit |
| Keytek PLA (Kmart, standard line) | 220–240 (label) | `temp_tower_240-205_0.4.stl` | `temp_tower_230-200_0.2.stl` | label is unusually hot for standard PLA; the tower extends 15 °C below it |
| ELEGOO PETG PRO (blue) | 230–260 | `temp_tower_260-230_0.4.stl` | `temp_tower_260-230_0.2.stl` | covers the label range exactly |
| ELEGOO Rapid PETG (clear) | 240–270 | `temp_tower_270-240_0.4.stl` | `temp_tower_270-240_0.2.stl` | covers the label range exactly |
| (spare) any PETG of unknown line | — | `temp_tower_260-220_0.4.stl` | `temp_tower_260-220_0.2.stl` | not assigned |

### Height → temperature tables

**How to read the tables.** "Block Z" is the block's bottom and top in mm. The slider in the Preview tab shows each layer's **top** Z. Add the `M104` on the **first layer of the block**: the layer whose top Z is the block bottom plus one layer height. That is the "Insert at layer (top Z)" column.

The base plate and block 1 print at the filament preset temperature, so block 1 needs no G-code.

#### 0.4 nozzle: `temp_tower_230-190_0.4.stl` (9 blocks, layer 0.20, base 0–1.00, height 91.00 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 1.00 – 11.00 | 230 | — (preset 230) | — |
| 2 | 11.00 – 21.00 | 225 | 11.20 | `M104 S225` |
| 3 | 21.00 – 31.00 | 220 | 21.20 | `M104 S220` |
| 4 | 31.00 – 41.00 | 215 | 31.20 | `M104 S215` |
| 5 | 41.00 – 51.00 | 210 | 41.20 | `M104 S210` |
| 6 | 51.00 – 61.00 | 205 | 51.20 | `M104 S205` |
| 7 | 61.00 – 71.00 | 200 | 61.20 | `M104 S200` |
| 8 | 71.00 – 81.00 | 195 | 71.20 | `M104 S195` |
| 9 | 81.00 – 91.00 | 190 | 81.20 | `M104 S190` |

#### 0.4 nozzle: `temp_tower_225-195_0.4.stl` (7 blocks, layer 0.20, base 0–1.00, height 71.00 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 1.00 – 11.00 | 225 | — (preset 225) | — |
| 2 | 11.00 – 21.00 | 220 | 11.20 | `M104 S220` |
| 3 | 21.00 – 31.00 | 215 | 21.20 | `M104 S215` |
| 4 | 31.00 – 41.00 | 210 | 31.20 | `M104 S210` |
| 5 | 41.00 – 51.00 | 205 | 41.20 | `M104 S205` |
| 6 | 51.00 – 61.00 | 200 | 51.20 | `M104 S200` |
| 7 | 61.00 – 71.00 | 195 | 61.20 | `M104 S195` |

#### 0.4 nozzle: `temp_tower_235-200_0.4.stl` (8 blocks, layer 0.20, base 0–1.00, height 81.00 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 1.00 – 11.00 | 235 | — (preset 235) | — |
| 2 | 11.00 – 21.00 | 230 | 11.20 | `M104 S230` |
| 3 | 21.00 – 31.00 | 225 | 21.20 | `M104 S225` |
| 4 | 31.00 – 41.00 | 220 | 31.20 | `M104 S220` |
| 5 | 41.00 – 51.00 | 215 | 41.20 | `M104 S215` |
| 6 | 51.00 – 61.00 | 210 | 51.20 | `M104 S210` |
| 7 | 61.00 – 71.00 | 205 | 61.20 | `M104 S205` |
| 8 | 71.00 – 81.00 | 200 | 71.20 | `M104 S200` |

#### 0.4 nozzle: `temp_tower_230-200_0.4.stl` (7 blocks, layer 0.20, base 0–1.00, height 71.00 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 1.00 – 11.00 | 230 | — (preset 230) | — |
| 2 | 11.00 – 21.00 | 225 | 11.20 | `M104 S225` |
| 3 | 21.00 – 31.00 | 220 | 21.20 | `M104 S220` |
| 4 | 31.00 – 41.00 | 215 | 31.20 | `M104 S215` |
| 5 | 41.00 – 51.00 | 210 | 41.20 | `M104 S210` |
| 6 | 51.00 – 61.00 | 205 | 51.20 | `M104 S205` |
| 7 | 61.00 – 71.00 | 200 | 61.20 | `M104 S200` |

#### 0.4 nozzle: `temp_tower_240-205_0.4.stl` (8 blocks, layer 0.20, base 0–1.00, height 81.00 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 1.00 – 11.00 | 240 | — (preset 240) | — |
| 2 | 11.00 – 21.00 | 235 | 11.20 | `M104 S235` |
| 3 | 21.00 – 31.00 | 230 | 21.20 | `M104 S230` |
| 4 | 31.00 – 41.00 | 225 | 31.20 | `M104 S225` |
| 5 | 41.00 – 51.00 | 220 | 41.20 | `M104 S220` |
| 6 | 51.00 – 61.00 | 215 | 51.20 | `M104 S215` |
| 7 | 61.00 – 71.00 | 210 | 61.20 | `M104 S210` |
| 8 | 71.00 – 81.00 | 205 | 71.20 | `M104 S205` |

#### 0.4 nozzle: `temp_tower_260-220_0.4.stl` (9 blocks, layer 0.20, base 0–1.00, height 91.00 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 1.00 – 11.00 | 260 | — (preset 260) | — |
| 2 | 11.00 – 21.00 | 255 | 11.20 | `M104 S255` |
| 3 | 21.00 – 31.00 | 250 | 21.20 | `M104 S250` |
| 4 | 31.00 – 41.00 | 245 | 31.20 | `M104 S245` |
| 5 | 41.00 – 51.00 | 240 | 41.20 | `M104 S240` |
| 6 | 51.00 – 61.00 | 235 | 51.20 | `M104 S235` |
| 7 | 61.00 – 71.00 | 230 | 61.20 | `M104 S230` |
| 8 | 71.00 – 81.00 | 225 | 71.20 | `M104 S225` |
| 9 | 81.00 – 91.00 | 220 | 81.20 | `M104 S220` |

#### 0.4 nozzle: `temp_tower_260-230_0.4.stl` (7 blocks, layer 0.20, base 0–1.00, height 71.00 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 1.00 – 11.00 | 260 | — (preset 260) | — |
| 2 | 11.00 – 21.00 | 255 | 11.20 | `M104 S255` |
| 3 | 21.00 – 31.00 | 250 | 21.20 | `M104 S250` |
| 4 | 31.00 – 41.00 | 245 | 31.20 | `M104 S245` |
| 5 | 41.00 – 51.00 | 240 | 41.20 | `M104 S240` |
| 6 | 51.00 – 61.00 | 235 | 51.20 | `M104 S235` |
| 7 | 61.00 – 71.00 | 230 | 61.20 | `M104 S230` |

#### 0.4 nozzle: `temp_tower_270-240_0.4.stl` (7 blocks, layer 0.20, base 0–1.00, height 71.00 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 1.00 – 11.00 | 270 | — (preset 270) | — |
| 2 | 11.00 – 21.00 | 265 | 11.20 | `M104 S265` |
| 3 | 21.00 – 31.00 | 260 | 21.20 | `M104 S260` |
| 4 | 31.00 – 41.00 | 255 | 31.20 | `M104 S255` |
| 5 | 41.00 – 51.00 | 250 | 41.20 | `M104 S250` |
| 6 | 51.00 – 61.00 | 245 | 51.20 | `M104 S245` |
| 7 | 61.00 – 71.00 | 240 | 61.20 | `M104 S240` |

#### 0.2 nozzle: `temp_tower_230-190_0.2.stl` (9 blocks, layer 0.10, base 0–0.60, height 54.60 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 0.60 – 6.60 | 230 | — (preset 230) | — |
| 2 | 6.60 – 12.60 | 225 | 6.70 | `M104 S225` |
| 3 | 12.60 – 18.60 | 220 | 12.70 | `M104 S220` |
| 4 | 18.60 – 24.60 | 215 | 18.70 | `M104 S215` |
| 5 | 24.60 – 30.60 | 210 | 24.70 | `M104 S210` |
| 6 | 30.60 – 36.60 | 205 | 30.70 | `M104 S205` |
| 7 | 36.60 – 42.60 | 200 | 36.70 | `M104 S200` |
| 8 | 42.60 – 48.60 | 195 | 42.70 | `M104 S195` |
| 9 | 48.60 – 54.60 | 190 | 48.70 | `M104 S190` |

#### 0.2 nozzle: `temp_tower_225-195_0.2.stl` (7 blocks, layer 0.10, base 0–0.60, height 42.60 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 0.60 – 6.60 | 225 | — (preset 225) | — |
| 2 | 6.60 – 12.60 | 220 | 6.70 | `M104 S220` |
| 3 | 12.60 – 18.60 | 215 | 12.70 | `M104 S215` |
| 4 | 18.60 – 24.60 | 210 | 18.70 | `M104 S210` |
| 5 | 24.60 – 30.60 | 205 | 24.70 | `M104 S205` |
| 6 | 30.60 – 36.60 | 200 | 30.70 | `M104 S200` |
| 7 | 36.60 – 42.60 | 195 | 36.70 | `M104 S195` |

#### 0.2 nozzle: `temp_tower_235-200_0.2.stl` (8 blocks, layer 0.10, base 0–0.60, height 48.60 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 0.60 – 6.60 | 235 | — (preset 235) | — |
| 2 | 6.60 – 12.60 | 230 | 6.70 | `M104 S230` |
| 3 | 12.60 – 18.60 | 225 | 12.70 | `M104 S225` |
| 4 | 18.60 – 24.60 | 220 | 18.70 | `M104 S220` |
| 5 | 24.60 – 30.60 | 215 | 24.70 | `M104 S215` |
| 6 | 30.60 – 36.60 | 210 | 30.70 | `M104 S210` |
| 7 | 36.60 – 42.60 | 205 | 36.70 | `M104 S205` |
| 8 | 42.60 – 48.60 | 200 | 42.70 | `M104 S200` |

#### 0.2 nozzle: `temp_tower_230-200_0.2.stl` (7 blocks, layer 0.10, base 0–0.60, height 42.60 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 0.60 – 6.60 | 230 | — (preset 230) | — |
| 2 | 6.60 – 12.60 | 225 | 6.70 | `M104 S225` |
| 3 | 12.60 – 18.60 | 220 | 12.70 | `M104 S220` |
| 4 | 18.60 – 24.60 | 215 | 18.70 | `M104 S215` |
| 5 | 24.60 – 30.60 | 210 | 24.70 | `M104 S210` |
| 6 | 30.60 – 36.60 | 205 | 30.70 | `M104 S205` |
| 7 | 36.60 – 42.60 | 200 | 36.70 | `M104 S200` |

#### 0.2 nozzle: `temp_tower_240-205_0.2.stl` (8 blocks, layer 0.10, base 0–0.60, height 48.60 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 0.60 – 6.60 | 240 | — (preset 240) | — |
| 2 | 6.60 – 12.60 | 235 | 6.70 | `M104 S235` |
| 3 | 12.60 – 18.60 | 230 | 12.70 | `M104 S230` |
| 4 | 18.60 – 24.60 | 225 | 18.70 | `M104 S225` |
| 5 | 24.60 – 30.60 | 220 | 24.70 | `M104 S220` |
| 6 | 30.60 – 36.60 | 215 | 30.70 | `M104 S215` |
| 7 | 36.60 – 42.60 | 210 | 36.70 | `M104 S210` |
| 8 | 42.60 – 48.60 | 205 | 42.70 | `M104 S205` |

#### 0.2 nozzle: `temp_tower_260-220_0.2.stl` (9 blocks, layer 0.10, base 0–0.60, height 54.60 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 0.60 – 6.60 | 260 | — (preset 260) | — |
| 2 | 6.60 – 12.60 | 255 | 6.70 | `M104 S255` |
| 3 | 12.60 – 18.60 | 250 | 12.70 | `M104 S250` |
| 4 | 18.60 – 24.60 | 245 | 18.70 | `M104 S245` |
| 5 | 24.60 – 30.60 | 240 | 24.70 | `M104 S240` |
| 6 | 30.60 – 36.60 | 235 | 30.70 | `M104 S235` |
| 7 | 36.60 – 42.60 | 230 | 36.70 | `M104 S230` |
| 8 | 42.60 – 48.60 | 225 | 42.70 | `M104 S225` |
| 9 | 48.60 – 54.60 | 220 | 48.70 | `M104 S220` |

#### 0.2 nozzle: `temp_tower_260-230_0.2.stl` (7 blocks, layer 0.10, base 0–0.60, height 42.60 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 0.60 – 6.60 | 260 | — (preset 260) | — |
| 2 | 6.60 – 12.60 | 255 | 6.70 | `M104 S255` |
| 3 | 12.60 – 18.60 | 250 | 12.70 | `M104 S250` |
| 4 | 18.60 – 24.60 | 245 | 18.70 | `M104 S245` |
| 5 | 24.60 – 30.60 | 240 | 24.70 | `M104 S240` |
| 6 | 30.60 – 36.60 | 235 | 30.70 | `M104 S235` |
| 7 | 36.60 – 42.60 | 230 | 36.70 | `M104 S230` |

#### 0.2 nozzle: `temp_tower_270-240_0.2.stl` (7 blocks, layer 0.10, base 0–0.60, height 42.60 mm)

| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |
|---|---|---|---|---|
| 1 | 0.60 – 6.60 | 270 | — (preset 270) | — |
| 2 | 6.60 – 12.60 | 265 | 6.70 | `M104 S265` |
| 3 | 12.60 – 18.60 | 260 | 12.70 | `M104 S260` |
| 4 | 18.60 – 24.60 | 255 | 18.70 | `M104 S255` |
| 5 | 24.60 – 30.60 | 250 | 24.70 | `M104 S250` |
| 6 | 30.60 – 36.60 | 245 | 30.70 | `M104 S245` |
| 7 | 36.60 – 42.60 | 240 | 36.70 | `M104 S240` |

**Short form.** For every 0.4 tower, insert at `11.2 + 10·(k−2)` for blocks k = 2…n. For every 0.2 tower, insert at `6.7 + 6·(k−2)`. The temperature for block k is `T_hot − 5·(k−1)`, where T_hot is the first number in the file name and n = (T_hot − T_cold)/5 + 1.

**If you only want part of the range,** for example PLA 215 → 195, keep the whole tower and simply ignore the other blocks. Or cut the tower with the Cut tool at a block boundary and recompute the heights.

### Slicer settings

| Setting | 0.4 nozzle | 0.2 nozzle |
|---|---|---|
| Printer preset | Bambu Lab A1 0.4 nozzle | Bambu Lab A1 0.2 nozzle |
| Process | 0.20 mm Standard | 0.10 mm Standard |
| Layer height / initial layer height | 0.20 / 0.20 | 0.10 / 0.10 |
| Line width | 0.42 (defaults) | 0.22 (defaults) |
| Walls | 2–3 | 2–3 |
| Sparse infill | 15 % (default is fine) | 15 % |
| Seam position | **Back**, so the label and front faces stay clean | Back |
| Supports | **Off** (the overhangs and bridge are the test) | Off |
| Brim | Off for PLA. PETG: optional 3–5 mm outer brim if the bed is marginal | same |
| Avoid crossing walls | Off (default), so travel crosses the gaps | Off |
| Variable / adaptive layer height | Off (it would break the height table) | Off |

**Filament preset.** Set *Nozzle temperature* and *Initial layer* to the **hottest** value (the first number in the file name, e.g. 235 for `temp_tower_235-200`), because the base and block 1 print at the preset temperature.

- Leave bed temperature, fan settings and the max volumetric speed at your normal values for that filament. Change one variable only.
- For PETG, keep the PETG fan settings. The bridge result depends a lot on fan speed.

### Applying the temperature changes in Bambu Studio (step by step)

1. Load the STL for your nozzle and material. Check that the engraved label faces the front (−Y), then pick the printer, process and filament presets listed above.
2. In the filament preset, set Nozzle temperature and Initial layer to the hottest value of the tower.
3. Click **Slice plate**. Bambu Studio switches to the Preview tab.
4. Drag the **vertical layer slider** on the right until its readout shows the first insert height. For every 0.4 tower that is **11.20** (layer 56); for every 0.2 tower it is **6.70** (layer 67). Use the arrow keys (↑/↓) for single-layer steps. The readout shows the layer number and its top Z.
5. Right-click the slider handle (or the small **+** icon next to it) and choose **Add Custom G-code**. Type `M104 S225` and confirm. A marker appears on the slider.
   - Use **M104** (set without waiting), **not M109**. M109 would make the nozzle sit and wait while oozing onto the part, leaving a blob.
6. Repeat step 5 for every row in the table: 21.20 → `M104 S220`, 31.20 → `M104 S215`, and so on up to the last block.
7. Hover over each marker to check its text and height. If one is on the wrong layer, delete it with right-click and add it again.
8. Slice again if asked, then print. The custom G-code markers are saved in the project (.3mf), so save the project once. Next time, just change the filament and the hottest temperature. Keep one saved project per tower file, because the S values differ between ranges.

**Check while printing.** In the printer screen or Bambu Handy, the target nozzle temperature should step down by 5 °C each time a new block starts.

Note: the A1 hotend cools by 5 °C within a few layers, so the bottom 0.5–1 mm of each block is a transition zone. Judge each block by its **upper two thirds**. The bridge and the wedges are placed there on purpose.

### What to look at (per block)

1. **Stringing:** look for strings and hairs in the window, between the two pins and between the pins and the walls. Hold the tower against a dark background.
2. **Bridge:** look at the underside of the deck (the window roof). Check for sagging strands, gaps and droop. Hotter usually means more sag.
3. **Overhangs:** check the underside of the 45° wedge (left) and the 60° wedge (right) for curl, rough "fur", and drooping edges.
4. **Label:** the engraved digits should be crisp. Bulging or blobby strokes mean too hot, and gappy walls mean too cold.
5. **Surface:** look at gloss and smoothness. Matte, rough or under-extruded walls point to too cold, especially on PETG and on the 0.2 nozzle.
6. **Layer adhesion:** after you finish looking, try to snap blocks apart by hand, or flex the pillar. Blocks that crack cleanly along a layer line are too cold.

### How to pick the temperature

- Discard the blocks with poor layer adhesion or a rough, under-extruded surface. That gives you the **minimum** usable temperature.
- From the blocks that remain, choose the **coolest** one whose bridge and 60° overhang are still clean, and whose stringing is acceptable. When two blocks look equal, take the cooler.
- Treat the result as ±5 °C. The tower prints slowly with small layers, while real prints run at higher flow.
  - **ELEGOO Rapid PLA / Rapid PETG** (high-speed filaments): if you print fast, near your maximum volumetric speed, add **+5 to +10 °C** to the tower result for those fast prints.
  - **0.2 nozzle:** flow is very low, so the best value is often **5 °C lower** than on the 0.4. Calibrate each nozzle separately.
- Typical results to expect:
  - PLA / PLA+: 200–215 °C
  - Budget PLA (Keytek): may need +5 °C for adhesion
  - PETG: 235–250 °C
- If stringing is still bad at the coolest acceptable temperature: **dry the filament** (especially PETG), then tune retraction (section 2).
- **Save the result:** Filament preset > *Nozzle temperature* (and Initial layer, which can be +5 °C). Save it as a user preset per filament and nozzle, for example "ELEGOO PLA+ @A1 0.4 – 210".

---

## 2. Stringing and retraction

The A1 stock retraction is about 0.8 mm. PLA usually strings very little on the A1. Run these tests only if you see stringing at the chosen temperature, and only on dry filament.

### 2a. `stringing_pins_<n>.stl`: check the final settings

- **Shape:** three tapered pins on a thin strip. The two gaps are different (0.4: 20 mm and 40 mm between centres; 0.2: 12 mm and 24 mm), so you see short and long travel at the same time. The tapered tips make each layer very short, and therefore make oozing during travel stand out.
  - 0.4: Ø7 → Ø2 pins, 25 mm tall on a 0.6 mm strip.
  - 0.2: Ø4.4 → Ø1.2 pins, 15 mm tall on a 0.4 mm strip.
- **Settings:** the same process as for the tower (0.20 / 0.10 mm layers), with your **final** temperature and retraction. Wall loops 2, infill does not matter, supports off, Avoid crossing walls off, all retraction and Z-hop settings at your normal values.
- **What to look at:**
  - Strings or "spider web" between the pins.
  - Blobs or zits on the pins where the nozzle arrives.
  - Hairs on the long (40 / 24 mm) gap compared with the short one.
- **Pass:** no strings at all, or only a few fine hairs that brush off.

### 2b. `retraction_coupon_<n>.stl`: separate prints, one per retraction value (main method)

Retraction length cannot change with height on your own model in Bambu Studio, and it cannot change per object on one plate either. So use one short coupon per value.

- **Shape:** two tapered pins, 30 mm apart (0.4) or 20 mm apart (0.2).
  - 0.4: 12 mm tall. Prints in about 5–8 minutes.
  - 0.2: 8 mm tall.
- **Marker tab:** there is a flat tab at one end. Write the retraction value on it with a marker after printing.

**Steps:**
1. Set the temperature from section 1, using dry filament.
2. Filament preset > **Setting Overrides** > tick **Retraction length** and enter the value. Leave Retraction speed at its default for now.
3. Print the coupon, then write the value on its tab.
4. Change only the retraction length and print again.
   - **PLA family (0.4):** 0.4, 0.6, 0.8, 1.0, 1.2 mm.
   - **PETG (0.4):** 0.6, 0.8, 1.0, 1.2, 1.5 mm.
   - **0.2 nozzle:** use the same lengths. Stringing is usually lower there, so start at 0.4–0.8.
   - Tip: keep one project with one plate. For each value, edit the override and send the job again.
5. Line up the coupons. Pick the **smallest** length where the strings disappear, then add 0.1–0.2 mm margin.
   - Do not go above about 2 mm on the A1 direct drive. Too much retraction causes gaps at the start of each pin layer, and can cause jams with PLA.
6. If nothing gets rid of the strings, change the temperature or dry the filament instead. Then try a higher **Retraction speed** (for example 30 → 40 mm/s) at the best length.
7. **Save:** keep the override in the filament user preset, so other filaments keep their own values.

### 2c. Built-in developer-mode Retraction test (alternative, one print)

1. Turn on Developer Mode: **Preferences** > **Develop mode**. A **Calibration** menu appears in the top bar.
2. Choose **Calibration > Retraction test**. Enter Start, End and Step, for example 0, 1.5, 0.1 for PLA, or 0, 2.0, 0.1 for PETG.
3. Bambu Studio opens a new project with its own tower, cut to `1.4 + (End − Start)/Step` mm tall, and slices it at 0.2 mm layers.
   - Use the 0.4 nozzle. The test forces 0.2 mm layers, which is too coarse for the 0.2 nozzle, so for the 0.2 nozzle use the coupons from section 2b.
4. **Reading the result:** measure the height of the lowest point where the strings stop, Z in mm from the bed. Then
   `length = Start + floor(Z − 0.4) × Step`.
   - Example: start 0, step 0.1, strings stop at Z = 8.7 mm → floor(8.3) = 8 → **0.8 mm**.
5. Save the value as in 2b.

### 2d. `retraction_tower_devmode_0.4.stl` (optional, experimental)

This is a replacement model for the developer-mode test in 2c. It has two Ø5 mm posts 30 mm apart, so the 25 mm gap gives longer travel than Bambu's tower. It is 0.4 mm base + posts to Z = 21.4 mm, which is exactly 21 retraction steps. A 0.4 mm groove ring sits on both posts at Z = 5.4, 10.4, 15.4 and 20.4 (after steps 5, 10, 15, 20) to help you count.

| Z range (layer tops) | Step index k | Length (Start 0, Step 0.1) |
|---|---|---|
| 0.4 – 1.4 | 0 | 0.0 |
| 1.4 – 2.4 | 1 | 0.1 |
| … | k = floor(Z − 0.4) | Start + k·Step |
| 5.4 (1st groove) | 5 | 0.5 |
| 10.4 (2nd groove) | 10 | 1.0 |
| 15.4 (3rd groove) | 15 | 1.5 |
| 20.4 – 21.4 (4th groove → top) | 20 | 2.0 |

How to use it. This method is **not tested**. It relies on the calibration mode staying active after you swap the model.
1. Run **Calibration > Retraction test** with Start 0, End 2.0, Step 0.1.
2. Import `retraction_tower_devmode_0.4.stl` into that project (Add / Ctrl+I), then delete Bambu's tower object.
3. Set the new object's layer height to 0.20, and initial layer to 0.20.
4. Slice and export the G-code. Search the G-code for `; Calib_Retraction_tower: Z_HEIGHT`. Those comments appear only when the per-mm retraction rule is active.
5. If the comments are missing, the mode was reset. Do not print it; use 2b or 2c instead.

---

## Order of use (per filament and nozzle)

1. Dry the filament if needed, especially PETG and the budget PLA.
2. Print the temperature tower → save the temperature. (The temperature comes first: the Bambu wiki says to redo Flow Dynamics whenever the temperature or max volumetric speed changes. See `research/07`, section 2, item 1, and `docs/filament-settings.md`, section 7.)
3. Run the built-in calibrations at that temperature: Flow Dynamics (PA; manual on the 0.2 nozzle), flow ratio, and optionally max volumetric speed.
4. Print `stringing_pins` at that temperature with the stock retraction.
5. Only if it strings: print retraction coupons (2b) or run the developer-mode test (2c) → save the retraction override.
6. Print `stringing_pins` again with the final values to confirm.
