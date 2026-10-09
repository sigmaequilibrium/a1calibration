# 03 - Filament Prep and Profiles (Bambu Lab A1, Bambu Studio, default PLA)

Research date: 2026-10-06. Method: web search plus page fetches. Note: wiki.bambulab.com pages returned HTTP 402 to the fetch tool, so Bambu wiki facts below come from search-result excerpts, not full pages (flagged "excerpt"). Verify against the live wiki before relying on exact numbers.

## 1. Drying: temperature and time

| Material | Bambu (blast oven, excerpt) | Bambu (A1 heatbed, excerpt) | Third-party guides | Notes |
|---|---|---|---|---|
| PLA | 50 C / 8 h | 65-75 C / 12 h, flip every 6 h | 40-50 C / 4-6 h (PrintPal); 45 C / 6 h; 45-55 C | Stay low; PLA softens above ~55-60 C and spools can fuse |
| PETG | 65 C / 8 h | 75-85 C / 12 h | 60-70 C / 4-6 h; 65 C / 6 h | |
| TPU (95A) | 70 C / 8 h | 80-90 C / 12 h | 50-60 C / 6-12 h (PrintPal) | Big disagreement on temp (50-90 C); keep to the low-middle end (~55-65 C) unless the spool says otherwise |
| ABS | 80 C / 8 h | 90-100 C / 12 h | 65-80 C / 2-4 h | |
| ASA | 80 C / 8 h | 90-100 C / 12 h | 65-80 C / 2-4 h | |

Disagreement and uncertainty:
- Bambu heatbed temperatures are far above generic guides because the bed is much hotter than the air around the spool. They are not equal to dryer-box temps. The A1 is open-frame, so the heatbed method (covered with a box) is weaker and less repeatable than a real filament dryer. Prefer a dryer.
- Always check the manufacturer spool label for third-party filament; it overrides this table.
- Do not dry PLA in a kitchen oven (poor temperature control).
- Bambu numbers lean longer (8 h); generic guides say 4-6 h. Longer at low temperature is safe; hotter is the risk.

## 2. Storage

- Keep dried or fresh spools in a sealed bag or box with desiccant; target humidity below ~15-20% (PrintPal says under 15%).
- PLA is slow to absorb (about 2-4 weeks unsealed in normal indoor humidity per PrintPal); PETG and TPU absorb faster, so seal them first.
- Put a small hygrometer inside the box.
- Re-dry desiccant when its indicator changes.

## 3. How to tell filament is wet

- Hissing, popping or crackling at the nozzle; steam or tiny bubbles in the extruded bead.
- Stringing and oozing worse than usual, rough or matte surface, inconsistent extrusion, weak or brittle layer bonds.
- Caveat: these symptoms also come from too-high temperature or poor retraction/PA, so dry first, then judge.

## 4. Choosing a base profile for third-party filament

- Bambu Studio "Create Filament" asks for vendor, type, name and a base filament; the new preset is named "Vendor Type Serial @Printer" and appears under user presets (excerpt of Bambu wiki).
- Start from the Bambu or Generic profile of the same material type (PLA for PLA). Forum opinion differs: one thread says start from Bambu own profile; another notes Bambu PLA uses 22 mm3/s max volumetric speed vs about 12 mm3/s for Generic PLA. Generic is the conservative choice; Bambu PLA Basic is the faster starting point. Pick one and then verify.
- Special PLA types (Silk, Matte, Wood, CF/GF) should use a matching base where one exists, because they run hotter/slower (my general knowledge, not from a cited page).
- "Copy Current Filament Preset" keeps the same settings as a system preset and saves it as a user preset (excerpt).
- Create it for the A1 with the correct nozzle (0.4 mm) so it shows under the A1 0.4 nozzle.

## 5. Filament settings that matter (Filament tab)

| Setting | What it does | Practical guidance |
|---|---|---|
| Nozzle temperature (initial layer and others) | Melt quality, layer adhesion, stringing | Start mid-range from the spool label; refine with a temperature tower |
| Max volumetric speed (mm3/s) | Caps speed so the hotend can melt enough plastic | Generic PLA about 12; Bambu PLA 22; community says most third-party PLA is fine at 20-22 on 0.4 mm, PETG about 20 with seam issues above; TPU much lower. Measure with the Max Flow Rate calibration |
| Flow ratio | Fine-tunes extrusion amount for the specific spool | Calibrate per filament; start from the base profile value |
| Pressure advance (Flow Dynamics, K) | Corrects bulging corners and seams | Calibrate per filament, see section 6 |
| Cooling (fan min/max, layer-time slow-down, overhang fan) | Overhangs, bridging, layer bonding | PLA wants high cooling; PETG moderate; ABS/ASA minimal; TPU low-moderate (general knowledge) |
| Bed temperature | First-layer adhesion | Follow base profile and plate type |
| Retraction | Stringing | Mostly printer/filament profile; TPU needs little |

## 6. Pressure advance on the A1: disagreement

- The A1 supports automatic Flow Dynamics calibration (firmware 01.04.00.00 and later) and manual calibration (Bambu wiki excerpt).
- One forum thread reports A1 auto-calibration giving inflated K (about 0.059 vs 0.035-0.04 manually) and recommends manual calibration. Single-user report, not official. Treat auto results as a starting point and verify with a manual pattern, especially for third-party filament.
- If you want a stored K to be used, untick "Flow Dynamics Calibration" in the print dialog; if ticked, auto-calibration overrides stored K values.
- Calibrated K values are stored per filament via the Calibration tab (Flow Dynamics, Manage Results) and the filament swatch edit in the Device tab, not only in the preset. Check both places.

## 7. Creating and saving a custom filament profile

1. Dry the spool first (section 1) so calibration is done on dry filament.
2. In Bambu Studio, open the Prepare tab, click the filament Settings icon, then Custom Filaments, then Create New.
3. Enter vendor, type, name; choose the base filament (section 4) and the A1 0.4 nozzle printer; confirm.
4. Edit settings in the Filament tab (temps, max volumetric speed, flow ratio, cooling) and click the save icon; give the preset a clear name.
5. Run calibrations in the Calibration tab: temperature tower, max volumetric speed (needs developer mode), flow rate, flow dynamics. Write results back into the preset.
6. Save again. Confirm it appears in user presets; keep Cloud sync on for backup.
7. Export presets (File, Export, Export Presets Bundle) as a backup (menu path from memory; verify).

Known issues (forum): no direct way to rename a custom filament, no vendor folders, sync inconsistencies, hard to keep several profiles per filament. Bambu wiki also has a page on custom filament creation issues. Choose names carefully; workaround is save as a new name and delete the old.

## 8. Naming and organizing

Suggested scheme (matches the Studio auto-name "Vendor Type Serial @Printer"):
- `<Vendor> <Material> [variant] <colour> vN @BBL A1`
- Examples: `Sunlu PLA Meta Black v1`, `Polymaker PETG Teal v2`
- Add a version suffix when recalibrating.
- Make separate profiles per colour only when colour changes behavior (white, transparent, silk often differ).
- Keep an external log (vendor, material, nozzle temp, max flow, flow ratio, K, calibration date, drying settings), since Studio lacks folders and notes.

## 9. Ordered procedure (default PLA)

1. Read the spool label (temp range, drying advice, bed temp).
2. Check for wetness; dry PLA at about 45-50 C for 6-8 h if it has been open for weeks or pops.
3. Store sealed with desiccant; print from a dry box if humid.
4. Create the custom filament from a PLA base (Generic PLA or Bambu PLA Basic) for the A1 0.4 nozzle.
5. Set nozzle temp at the label midpoint; run a temperature tower and pick the best temp.
6. Run the max volumetric speed test; back off 2-3 layers worth; if unsure cap near 20 mm3/s.
7. Run Flow Dynamics (manual preferred if auto looks odd); save K.
8. Run flow rate calibration; set flow ratio.
9. Tune cooling if overhangs or layer adhesion are poor.
10. Save, name with version, export bundle, update log.

## 10. Sources

- Bambu wiki, drying (excerpt only): https://wiki.bambulab.com/en/filament-acc/filament/dry-filament
- Bambu wiki, create filament (excerpt only): https://wiki.bambulab.com/en/bambu-studio/create-filament
- Bambu wiki, custom filament issues: https://wiki.bambulab.com/en/software/bambu-studio/custom-filament-issue
- Bambu wiki, PA calibration: https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa
- PrintPal drying guide: https://printpal.io/wiki/filament-drying-guide
- MatterHackers wet filament: https://www.matterhackers.com/about/wet-filament-heres-how-to-fix-it
- 3DPrintBeginner drying: https://3dprintbeginner.com/how-to-dry-your-filament/
- Forum, volumetric speed for third-party filament: https://forum.bambulab.com/t/volumetric-speed-for-3rd-party-filaments/205714
- Forum, build a filament profile from scratch: https://forum.bambulab.com/t/how-to-build-a-filament-profile-from-scratch/258524
- Forum, A1 auto PA wrong K: https://forum.bambulab.com/t/a1-automatic-pressure-advance-calibration-produces-incorrect-k-values/217723
- Forum, custom filament management issues: https://forum.bambulab.com/t/better-fixed-custom-filament-profile-management/256185
- Forum, K factor from auto-calibration: https://forum.bambulab.com/t/use-k-factor-from-auto-calibration/144411

Gaps: Bambu wiki pages could not be read in full; cooling-by-material, flow-ratio starting values and the export menu path are general knowledge, not verified from a cited page. ABS/ASA need an enclosure, which the A1 lacks.
