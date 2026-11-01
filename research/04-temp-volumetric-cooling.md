# Bambu Lab A1: Temperature Tower, Max Volumetric Speed, Cooling/Fan Tuning (Bambu Studio, PLA default)

Research date: 2026-10-06. Confidence legend: [S] = directly supported by a fetched source; [K] = general community/slicer knowledge not verified in this session; [?] = uncertain or disagreeing.

Source caveat: the official Bambu wiki pages (wiki.bambulab.com) returned HTTP 402 to the fetch tool and the OrcaSlicer wiki pages returned only navigation indexes. Step-level menu details below therefore come from secondary sources plus general knowledge. Verify the exact dialog fields on your installed Bambu Studio version.

## Recommended order
1. Do these after flow rate and pressure advance (PA), as in the community-consensus order flow, PA, temperature, max volumetric speed [S: forum thread below]. Some users say flow and PA are mostly independent and order is flexible [S].
2. Optional: many users stop after flow and PA. Temperature towers "often require no adjustments" unless the filament is problematic, and the max volumetric speed (MVS) test is optional unless you are optimizing for speed [S].
3. Cooling is not a calibration-menu item. It is tuned by changing settings and judging overhangs, bridges, and layer lines.

Preconditions: dry filament, clean nozzle, textured/smooth PEI cleaned, same filament spool and profile you will actually use. Save results into a **custom filament preset** (see Common mistakes).

## 1. Temperature tower

### Procedure (Bambu Studio: Calibration menu > Temperature)
- Select your printer (A1), the filament, and the process. Open Calibration > Temperature [S].
- Choose a filament type preset in the dialog; it fills a start/end range and a 5 C step. Typical ranges: PLA 190-220 C, PETG 225-245 C, ABS 230-250 C [S: eolasprints]. Bambu/Orca built-in PLA ranges are about 190-230 C [K]. Orca's tower steps 5 C per block, each block labeled [K].
- Slice and print. The tower prints hottest at the bottom in Orca/Bambu implementations and cools as it goes up [K][?: confirm on the preview; the labels are on the tower, so just read them].
- Do not change the printed-in-the-gcode temperatures by hand; the slicer inserts the temperature changes.

### Judging results
Per block, look for [S: eolasprints, Bambu wiki summary in search result]:
- Stringing between the tower spires (less is better).
- Bridging quality and overhang sharpness.
- Surface smoothness/gloss, layer adhesion (try to snap or flex a block, or break the tower at the weakest layers).
- Warping/curling of corners.
Choose the **lowest** temperature that still gives good layer adhesion and clean bridges/overhangs; when two are equal, prefer the cooler [K]. Lower temperature reduces stringing, and higher gives stronger layers and better flow.

### What to enter
- Filament profile > Filament tab > Nozzle temperature (range for printing and "initial layer" fields). Set the normal and first-layer values to your best temperature (first layer can be 5 C higher for adhesion) [K].
- Keep the recommended nozzle min/max range in the profile reasonable, since the MVS limit interacts with temperature [K].

### Notes
- Pre-tuned vendor profiles (Bambu PLA etc.) are usually already near-optimal; the test is most useful for generic, third-party, or problem filament [S].
- The tower is small and quick so cooling per block is different from a real print. Treat it as a +/-5 C guide, not exact [K].
- Faster printing needs a higher temperature (more melt capacity); if you later raise speed, rerun or bump 5-10 C [K].
- Typical PLA result: 200-220 C. PETG: 230-250 C [K, consistent with ranges above].

## 2. Max volumetric speed (MVS)

### What it measures
The maximum mm^3/s your hotend can melt and push before under-extrusion. Formula: speed x layer height x line width = volumetric flow [S: Bambu forum thread]. Example in that thread: 476 mm/s x 0.20 x 0.42 is about 40 mm^3/s [S].

### Procedure (Bambu Studio: Calibration > Max Volumetric Speed)
Defaults in the Orca/Bambu dialog: start 5, end 20 mm^3/s, step 0.5 [K][?]. A1 stock hotend and PLA are typically good for about 12-21 mm^3/s, so end at 20-25 for PLA [K]. A quick-test model on MakerWorld ("maximum volume speed quick test") is a 15 mm tall model starting at 8 mm^3/s and increasing 2 mm^3/s per mm height up to 38 mm^3/s [S: search snippet; page itself returned 403].
1. Set the target filament and its already-tuned temperature (from step 1) and flow ratio/PA first [K].
2. Open Calibration > Max Volumetric Speed, set start/end/step, send. It prints a vase-mode (spiral) tower where flow rises with height [K].
3. Watch/inspect for the height where the walls turn rough, gappy, thin, glossy-then-matte, or the extruder clicks or skips [S: under-extrusion shows as gaps; K].
4. Measure from the bed to the first bad layer in mm, then compute: flow = start + (height_mm - first layer height... ) x step per mm. In Orca's formulation: MVS = start + height x step, where step is the per-mm rise; the dialog's step is per mm of height [K][?: confirm against the dialog's help text, because the units differ between the Bambu quick-test and Orca's calibration].
5. Take the last good height and apply a safety margin: **use about 90% of the failing value** [S: eolasprints]. Some users use 85% [K].

### What to enter
- Filament profile > Filament tab > "Max volumetric speed" (mm^3/s). This caps speed in the slicer for that filament so fast/large-layer features self-limit [S/K].
- Stock Bambu PLA Basic is set around 21 mm^3/s on A1 (profile default; verify in your profile) [K]. Typical ranges for 0.4 mm nozzle: standard PLA 12-18, high-speed PLA 20-30, PETG 8-14, ABS 10-16, ASA 8-14, TPU 2-5 [S: eolasprints]. Treat these as ranges for generic printers; the A1 stock hotend sits at the lower end for fast PLA [?].

### Caveats / known bugs [S: Bambu forum thread]
- "Slow printing down for better layer cooling" (cooling override) can override the MVS limit. Disable it for the test.
- Removing infill or using vase mode with modifiers can produce wrong flow values; check the Preview tab, Flow color scheme, to see the real calculated flow per height.
- Profile syncing issues can make the calculated flow wrong; one user works around it by creating a separate printer profile (adding a non-Bambu printer then switching back). This is an unconfirmed workaround [?].
- The Bambu Studio calibration menu is described as more limited than Orca's [S]. If the Bambu Studio dialog lacks fields, use the MakerWorld test model plus the formula, or OrcaSlicer.
- Judging by eye is subjective; sound (clicking), under-extruded gaps, and weak walls should all agree before you trust the height.
- Do not set MVS to a value that causes loss of layer adhesion; real parts with thick layers and wide lines hit the limit before thin ones, so test at the layer height you actually use [K].

## 3. Cooling / fan tuning

### Defaults for A1 [S: makers101]
- A1/A1 mini/A2L PLA: min fan 60%, max fan 80% (compare P1S/X1C 100/100). Bambu PLA Basic A1 mini: 60% at layer time 80 s, 80% at 6 s [S: search snippet].
- Fan interpolates between min and max by layer time ("Fan speed" thresholds at layer-time bounds). If min equals max, layer-time logic does nothing [S].
- PETG on A1 is set to about 10% more fan than P1S per forum report (so P1S has 10% less) [S: search snippet; garbled, treat as [?]]. PETG usually runs about 40-60% cooling in general practice [K].

### Procedure (no calibration-menu item; iterate on test prints)
1. Print a cooling/overhang test: an overhang angle test, a bridge test, and a small tall tower (layer-time test) on the same filament [K].
2. Judge:
   - Drooping overhangs, sagging bridges, curling edges: too little cooling. Raise fan, enable overhang fan 100%, lower bridge speed/ensure bridge fan.
   - Visible banding/layer lines, weak layers, delamination (especially PETG): too much cooling. Reduce min fan, or lengthen slow-down time [S: forum PSA discusses layer lines from over-strong cooling].
   - Tiny features melting/blobbing: layer time too short. Raise "Slow down for better layer cooling" threshold or minimum layer time (e.g. 4-8 s) [K].
3. Change one variable at a time [S: makers101 warns against changing multiple advanced options at once].

### Values to try (Filament tab > Cooling)
- PLA (A1): keep 60-80% as the baseline; raise min toward 80-100% for sharper overhangs, lower toward 40-60% for stronger parts [S/K]. Overhang fan 100% (A1 default). Keep **first-layer part fan at 0%** [S: makers101].
- PETG: min 30-40%, max 50-60%; overhang 70-100% if needed [K]; reduce if layer lines/delamination appear.
- Example of an H2D user lowering cooling to reduce layer lines: 60% at 100 s layer time, overhang 80%, aux fan 10%, bridge 100 mm/s, outer wall 60 mm/s [S]. Note this is for H2D, which has stronger cooling than A1; do not copy directly [S].
- Another user improved PETG-HS overhangs by raising min 10% to 40% and max 40% to 90% and disabling "slow down for overhangs" [S: search snippet; low detail].
- The A1 has an auxiliary fan; the A1 mini and A1 have a different cooling duct design than the P1/X1 series [K], so values from P1S guides are not directly transferable [S: makers101 table].

### Common mistakes [S unless marked]
- Copying tutorial values like 200% fan (impossible) [S].
- Enabling first-layer part cooling [S].
- Changing several advanced options simultaneously without a baseline [S].
- Editing the system profile: AMS RFID loading restores factory profiles and your edits vanish. Save as a custom filament preset [S].
- Disagreement: more cooling is not simply better; cooling is a balance between overhang/bridging and layer-line/warp problems [S].

## Common mistakes across all three
- Running the temperature tower before dry filament (wet filament skews stringing results) [K].
- Setting MVS from the first visible flaw without safety margin, or setting it too high and then wondering why the profile "makes" fast prints under-extrude [S/K].
- Forgetting that the temperature tower, MVS and cooling interact: higher flow needs higher temp and more cooling; retest if you change speed significantly [K].
- Editing the built-in profile instead of a custom copy [S].

## Points of uncertainty / disagreement
- Exact Bambu Studio dialog fields/defaults for Temperature and Max Volumetric Speed could not be confirmed (wiki blocked). Verify in the app.
- Tower ordering (hot at bottom or top) and exact MVS height-to-flow formula depend on the tool; read the dialog/preview.
- Safety margin: 90% (eolasprints) vs. 85% (commonly cited elsewhere, unverified).
- Whether the A1 stock hotend sustains the typical 12-18 for PLA or more: sources give generic ranges; A1 profile default is reportedly higher (about 21) [?].
- Order of calibration: flow then PA then temp then MVS is consensus but not mandatory [S].

## Sources
- Bambu Wiki calibration page (blocked, 402; cited via search snippets): https://wiki.bambulab.com/en/bambu-studio/Calibration
- Eolas Prints, Bambu Studio calibration guide: https://eolasprints.com/blogs/advanced-3d-printing/bambu-studio-calibration-guide-getting-perfect-prints-every-time
- Bambu forum, order of calibrations: https://forum.bambulab.com/t/order-of-calibrations-bambu-lab-x1-carbon/32349 (page fetched 402 for the first attempt; summary taken from the second fetch via the search result)
- Bambu forum, max volumetric flow for high flow nozzle: https://forum.bambulab.com/t/max-volumetric-flow-calculations-for-high-flow-nozzle/177422
- MakerWorld max volume speed quick test (403; snippet only): https://makerworld.com/en/models/944709-maximum-volume-speed-quick-test
- Makers101, PLA cooling settings: https://makers101.com/bambu-studio-pla-cooling-settings/
- Bambu forum PSA on cooling for layer lines: https://forum.bambulab.com/t/psa-tune-your-cooling-settings-for-pla-petg-to-reduce-layer-lines/168975
- Bambu forum, PLA filament profiles and fan speed: https://forum.bambulab.com/t/pla-filament-profiles-fan-speed/123036 (snippet only)
- Bambu forum, eSUN PETG-HS overhang settings: https://forum.bambulab.com/t/esun-petg-hs-my-settings-improvments-for-overhangs/96740 (snippet only)
- Polymaker cooling guide: https://wiki.polymaker.com/the-basics/3d-slicers/cooling (snippet only)
