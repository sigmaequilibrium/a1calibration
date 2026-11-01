# Ready-to-open Bambu Studio projects (`3mf/`)

`3mf/0.4/` and `3mf/0.2/` hold one Bambu Studio project per test STL. Each project already has the printer, process and filament presets selected, the part placed on the plate, the per-test settings from `docs/tests-*.md` applied to the object, and, for the temperature towers, the `M104` temperature changes on the layer slider. Open the file, check the filament, slice, print.

Generator: `tests-src/build_3mf.py`. Rebuild everything after the STLs change:

```
.venv/Scripts/python -I tests-src/build_3mf.py
```

The script deletes and rewrites `3mf/0.2/*.3mf` and `3mf/0.4/*.3mf` from whatever STLs are in `stl/`. It picks up every `temp_tower_<hot>-<cold>_<n>.stl`, so new tower ranges get projects automatically. It takes the M104 heights from `tests-src/temp_stringing.py` (the same function that prints the `--markdown` tables) and checks them against that table. Any STL it has no rule for is listed as `skipped` at the end of the run.

Optional headless check, if Bambu Studio is installed: this also slices every tower project with the Bambu Studio command line and confirms each `M104` is on the right layer of the G-code.

```
.venv/Scripts/python -I tests-src/build_3mf.py --studio "C:/Program Files/Bambu Studio/bambu-studio.exe"
```

## What is in each project

| Project (per nozzle) | Filament preset | Per-object settings (the object's gear icon in the object list) |
|---|---|---|
| `dim01_first-layer-squares_*` | Generic PLA | walls 2, brim off. The part is one layer thick (0.20 / 0.10, same as the first layer) |
| `dim02_xy-gauge-100-20_*` | Generic PLA | walls 5 (0.4) / 8 (0.2), infill 15 %, brim off |
| `dim03_hole-peg-gauge_*` | Generic PLA | walls 3 / 4, infill 15 %, seam Aligned, brim off |
| `dim04_fit-clearance-*` | Generic PLA | walls 3 / 4, infill 15 %, brim off |
| `dim05_elephant-foot_*` | Generic PLA | walls 6 / 8, brim off |
| `dim-combo_02-03-05_*` | Generic PLA | dim02 + dim03 + dim05 on one plate, each with its own settings above |
| `overhang_angles_*`, `bridge_spans_*` | Generic PLA | supports off |
| `min_feature_*` | Generic PLA | **two copies**: "ARACHNE" (wall generator Arachne) and "CLASSIC thin-wall-off" (Classic, Detect thin wall off). X-Y hole and contour compensation are 0 on both |
| `verify_combo_*` | Generic PLA | none. Use your final presets unchanged |
| `stringing_pins_*`, `retraction_coupon_*` | Generic PLA | walls 2, supports off |
| `temp_tower_<hot>-<cold>_*` | Generic PLA if hot ≤ 240; Generic PETG for 260-220 and 260-230; Generic PETG HF for 270-240 (Rapid PETG, see `docs/filament-settings.md`) | walls 2, infill 15 %, seam Back, brim off, supports off. Filament nozzle temperature and initial-layer temperature = `<hot>`. `M104 S<t>` on the first layer of every block after block 1 |

On every object the layer height is set to 0.20 (0.4 nozzle) or 0.10 (0.2 nozzle) and supports are off, except `verify_combo`, which has no overrides.

The presets are the stock system ones:
- Printer: `Bambu Lab A1 0.4 nozzle` with process `0.20mm Standard @BBL A1`.
- Printer: `Bambu Lab A1 0.2 nozzle` with process `0.10mm Standard @BBL A1 0.2 nozzle`.
- Filament: `Generic PLA / PETG / PETG HF @BBL A1` (with ` 0.2 nozzle` for the 0.2 projects).
- Plate type: Textured PEI Plate (the plate the A1 ships with).

All parts are centred on the plate (X 128, Y 128). The combo plates are laid out side by side. The A1 purges and wipes off the plate, so nothing needs to stay clear of a front-left purge area.

`retraction_tower_devmode_0.4.stl` has **no project**. It only works inside Bambu Studio's developer-mode *Calibration > Retraction test*, which a project file cannot switch on. Use the steps in `docs/tests-temp-stringing.md` section 2d.

## Opening a project

1. In Bambu Studio choose **File > Open Project** (or drag the `.3mf` onto the window). If Studio asks how to open it, choose **Open as project**. "Import geometry only" throws the settings and the M104 changes away.
2. Check the printer in the top left. It must match the nozzle that is installed (folder `0.4` or `0.2`).
3. Check the plate type. Change it if you are not using the Textured PEI plate.
4. Check the filament (see the next section), then click **Slice plate**.
5. For a tower, check the layer slider in the Preview tab. Each block start has a marker. Hover over a marker to see its `M104 S…` text. The heights are the "Insert at layer (top Z)" column of the tables in `docs/tests-temp-stringing.md`.
6. When you print or send the job, map filament 1 to the AMS lite slot (or the external spool) that holds your filament.

## Using your own filament preset

The projects use Bambu's Generic presets so they open on any installation. To use your own preset:

1. In the left panel, pick your own preset in the filament 1 drop-down, for example "ELEGOO PLA+ @A1 0.4".
2. **For a tower:** open the filament settings and set *Nozzle temperature* (Initial layer **and** Other layers) to the hottest value of the tower, which is the first number in the file name. The project's own value is lost when you switch presets, because it belongs to the old preset. The base and block 1 print at this temperature.
3. Slice. The `M104` markers are still on the slider.

Switching filament keeps the layer changes. They are stored in the project with the plate (`Metadata/custom_gcode_per_layer.xml`), not in the filament preset. Per-object settings also stay, because they are stored with the object.

Things that **do** affect the M104 changes:
- **Another layer height or process.** The markers stay at their Z values. With a layer height that does not divide the block heights (for example 0.16 or 0.12 on the 0.4 tower), each change moves to the next layer above the marker. Keep 0.20 / 0.10.
- **Variable layer height / adaptive layers.** Leave them off.
- **Deleting and re-importing the tower,** or "Import geometry only". Both lose the markers. Re-open the project instead.
- **Another printer preset** with a different nozzle size. Use the project from the other nozzle folder instead.

You can also save the setup into your presets. Click the save icon next to the filament to store the temperature, but remember that the next tower range needs a different value.

## What Studio shows when it opens

- The filament may show as **modified** (an orange icon or a "*"). For towers that is expected: the only change is the nozzle temperature. You do not need to save it.
- The files were written for Bambu Studio **2.08.02.61**. A slightly older 2.x version may show a "this file was saved by a newer version" notice. Click through it; the project still loads. A much older version (1.x) will only import the geometry.
- Thumbnails are not included. Studio draws the plate preview itself after it opens or slices the project.

## How the files are built (for maintenance)

This was checked against the BambuStudio source at tag `v02.08.02.61` (`src/libslic3r/Format/bbs_3mf.cpp`, `src/slic3r/GUI/Plater.cpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/Preset.cpp`, `src/BambuStudio.cpp`) and against a project that the Bambu Studio 2.08.02.61 command line exported itself.

- **Project vs geometry.** Studio loads settings, per-object settings and `custom_gcode_per_layer.xml` only when `3D/3dmodel.model` has `<metadata name="Application">BambuStudio-…</metadata>`. Without it the file opens as geometry only.
- **Files written:** `[Content_Types].xml`, `_rels/.rels`, `3D/3dmodel.model` (objects as components), `3D/_rels/3dmodel.model.rels`, `3D/Objects/object_N.model` (meshes), `Metadata/model_settings.config` (object names, per-object settings, plate 1), `Metadata/project_settings.config` (presets), `Metadata/slice_info.config` (header only) and, for towers, `Metadata/custom_gcode_per_layer.xml`. Each M104 is entry type 4 ("Custom") with `top_z` = the layer's top Z.
- **Why the full preset values are written.** When Studio loads `project_settings.config`, any key that is missing gets the program's built-in default, **not** the value from the named system preset (`Plater::load_files`: `FullPrintConfig::defaults()` + loaded keys). A partial file would give, for example, an empty start G-code. So the script resolves the stock presets (the `inherits` and `include` chains of the BBL JSON profiles) and writes every value.
  - It also writes the preset names (`printer_settings_id`, `print_settings_id`, `filament_settings_id`), an empty `inherits_group` (meaning "this is the system preset itself") and `different_settings_to_system`. That list contains only the tower's nozzle temperatures.
  - On load, `PresetCollection::load_external_preset` replaces every value that is *not* in that list with the value of your installed system preset. So a newer profile version on your machine wins, and only the listed temperatures stay as a change.
- **Profile source.** The script reads the system profiles from `--profiles DIR`, `$BAMBU_PROFILES`, or `C:/Program Files/Bambu Studio/resources/profiles/BBL`. If none of these exists, it reads the cache `tests-src/bbl_profiles/v02.08.02.61/`, which it downloads from GitHub on first use. The cached files are identical to those in the 2.08.02.61 Windows release. Use `--tag` to fetch another release.

## Verification status

Checked by the script on every run:
- the zip file is intact and every XML file is well formed;
- every mesh has the same vertex and triangle count as its STL;
- every part sits on Z = 0 and lies inside the 256 × 256 plate;
- every M104 height lies on a layer boundary (first layer = layer height), lies inside the part, and equals the `temp_stringing.py --markdown` table.

Checked once with the **Bambu Studio 2.08.02.61 command line** (official Windows release, run headless, not installed):
- every project opens and slices without errors;
- in every tower's G-code, each `M104 S<t>` appears under `; CUSTOM_GCODE` on the layer whose `; Z_HEIGHT` is the table value, and the preset temperature is the hottest one;
- the per-object wall count takes effect: dim02 slices with no sparse infill.

**Not tested:** opening the projects in the Bambu Studio *GUI*. The GUI uses the same 3MF reader as the command line, but its preset handling (the "modified" filament and the sync to your installed presets) was only checked by reading the source. The first time you open a project, look at the filament temperature and the slider markers before you print.
