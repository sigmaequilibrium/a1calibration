# Flow Ratio and Pressure Advance / Flow Dynamics - Bambu Lab A1 (Bambu Studio, PLA)

Research date: 2026-10-06. Caveat: the official Bambu wiki pages (wiki.bambulab.com) returned HTTP 402 to the fetch tool, so wiki content below comes from search-result excerpts plus third-party/forum pages. Items marked [UNVERIFIED] should be checked against the live wiki or on-screen text in Bambu Studio.

## 1. Short answer

- A1 (no lidar) supports an AUTO Flow Dynamics calibration (purges at the wiper/purge area and reads a toolhead pressure sensor; no pattern to judge) and a MANUAL one (prints a pattern; you pick the best K). Auto needs A1 firmware >= 01.04.00.00 per forum summaries [UNVERIFIED version].
- Flow Ratio is manual only (visual, two passes) because the A1 has no lidar to automate it.
- Order: mechanical/first-layer/temp/dry filament -> Flow Dynamics (PA/K) -> Flow Ratio pass 1 -> pass 2 -> (optionally re-check PA) -> max volumetric speed. Sources disagree on PA vs flow order (see section 5).
- For Bambu-brand PLA the factory profiles are already tuned; calibration pays off mainly for third-party filament.

## 2. Pressure Advance / Flow Dynamics (K value)

### 2a. Auto (A1 default path)
Source: https://sparklab.unbc.ca/?p=682 ; https://forum.bambulab.com/t/flow-dynamic-calibration-runs-forever/44454
1. Bambu Studio -> Calibration tab -> Flow Dynamics -> Auto-Calibration.
2. Sync printer info; choose nozzle diameter (0.4), plate type, filament (AMS Lite / external spool: make sure the right source is selected).
3. Calibrate. Printer heats, purges filament at the wiper while the toolhead sensor measures flow/pressure.
4. Name and save the result as a profile (K factor). Typical PLA results reported on the forum: about 0.026-0.037 (https://forum.bambulab.com/t/use-k-factor-from-auto-calibration/144411).
5. Apply: Device tab -> click the eye/edit icon on the filament swatch -> pick the saved PA profile. If it is missing: Calibration tab -> Flow Dynamics -> Manage Results -> New. Printer stores limited history: forum reports 16 results per nozzle; a full list can silently drop new results, so delete old ones first.
6. Gotcha: the "Flow dynamics calibration" checkbox in the print dialog. If checked, the printer re-runs auto calibration at print start and uses THAT K, not your saved one. Uncheck it to use your saved K (https://forum.bambulab.com/t/use-k-factor-from-auto-calibration/144411; search summary of forum threads). Forum users also say it defaults OFF and only calibrates the first filament in multi-colour prints (https://forum.bambulab.com/t/questions-about-flow-dynamics-and-extrusion-multiplier-on-the-a1/47642).
7. Auto-calibration can occasionally hang ("runs forever" thread) - clean the nozzle/wiper area and retry.

### 2b. Manual (pattern or line)
Source: https://sparklab.unbc.ca/?p=682 ; https://forum.bambulab.com/t/pressure-advance-flow-dynamics/67454
1. Clean smooth PEI plate (easier to read), dry filament, load it.
2. Calibration tab -> Flow Dynamics -> Manual Calibration; Sync; nozzle 0.4; plate type; filament.
3. Method: Pattern method (recommended in the guide). Interval 0.002 for finer steps. Line method is the other option; tower method exists in older/other versions (tower: PA increases 0.002 per mm height, pick best corner height - search excerpt of wiki, [UNVERIFIED for A1 UI]).
4. Reading it:
   - Pattern: pick the cleanest, sharpest corner with no under-extrusion gaps. K too low = bulging/rounded corners; K too high = thin corners/gaps/divots (also https://3dbite.com/best-3d-printer-calibration-routine-bambu-a1-a2l/).
   - Line: pick the line with the most uniform width (forum).
   - The currently saved PA does not affect the test; every line/corner uses its own value (forum 67454).
5. Enter the chosen K value in the dialog, name the profile, Finish. Then assign it in Device tab as in 2a.
6. Starting values / sanity range for PLA: roughly 0.02-0.06, generic starting point 0.04 (https://eolasprints.com/blogs/advanced-3d-printing/bambu-studio-calibration-guide-getting-perfect-prints-every-time). Treat as third-party ballpark.

### 2c. Auto vs manual - uncertainty
- Forum thread "Manual calibration with A1 - does it work?" (https://forum.bambulab.com/t/manual-calibration-with-a1-does-it-work/101778) reports manual flow/PA functions flaky or non-functional on early firmware and in LAN mode; success came after cloud mode, new custom profiles, power cycles. This thread is older; current state unverified. Practical advice: try auto first; use manual as a cross-check or if auto result looks wrong (corner bulges).
- Users disagree on benefit: some see clear gains with third-party filament, others "prints look the same"; Bambu-brand filament comes pre-calibrated.
- Which K the printer actually uses is poorly surfaced in the UI (forum complaints, and an older firmware bug fixed in 01.03.01.00 where K edits were not applied). Verify after saving by checking the Device tab value and by printing a corner test.

### 2d. Per-nozzle / per-filament
- K is stored per printer + nozzle diameter (and nozzle type) + filament + (in the dialog) plate type. Recalibrate when you change nozzle diameter/type, filament brand/colour batch, or notably different drying state. PLA colours of the same brand often differ slightly; at minimum calibrate one per brand/type.
- Filament profiles are linked to a particular printer/nozzle (forum search summary).

## 3. Flow Ratio (Flow Rate calibration)

Source: https://sparklab.unbc.ca/?p=682 ; wiki excerpts via search (https://wiki.bambulab.com/en/bambu-studio/Calibration); formula confirmed at https://forum.bambulab.com/t/what-formula-does-bambu-use-for-flow-rate-calibration/197570
Prereqs: dry filament, clean nozzle/extruder gears, no partial clog, clean plate (smooth PEI), Flow Dynamics done first (per Spark Lab guide).

1. Calibration tab -> Flow Rate -> Manual Calibration. Choose Complete (pass 1) vs Fine (pass 2); Sync; nozzle; plate; filament.
2. Pass 1 (coarse): prints a set of blocks (one per flow modifier). Look at the TOP surface of each block. Over-extrusion = overlapping/ridged lines; under-extrusion = gaps between lines. Choose the smoothest block (the guide says choose from the middle of the range showing smooth consistent lines). Studio shows the modifier / resulting ratio. Save the new ratio into the filament preset.
3. Pass 2 (fine): remove samples, clean plate, run again (starts from the ratio you saved in pass 1 - save pass 1 first). Choose the smoothest block, name the preset, Finish.
4. Formula (to enter/verify by hand): new ratio = current ratio x (100 + modifier) / 100. E.g. 0.98 x (100+5)/100 = 1.029; 1.045 x 0.95 = 0.99275.
5. Where to enter: in the Studio filament settings (Filament -> flow ratio) of your custom/user filament preset and save the preset. It is a slicer-side preset value, not a printer-side K-like profile. Make a user preset per filament (do not edit the system Bambu preset; name it e.g. "Brand PLA colour date").
6. Modifier ranges: one search excerpt of the wiki says pass 2 modifiers run -9 to 0, while the wiki's own pass-2 formula example uses +5. These conflict; read the numbers printed on the blocks and use the formula with the sign shown. [UNCERTAIN] Pass 1 range is wider (about +/-20) [UNVERIFIED].
7. Sanity: calibrated values typically fall within about +/-5% of the starting ratio (Eolas guide). Large corrections (>~10%) usually indicate wet filament, clogged nozzle, or under-tensioned/dirty extruder - fix hardware instead.
8. Note: PA does not change the extrusion multiplier, but flow dynamics affects effective flow at speed changes (forum 47642), so do PA first, then flow.
9. Optionally verify with a hollow-cube wall thickness measurement using calipers/micrometer (forum 67454) - independent check of visual result.

## 4. Per-nozzle / per-filament considerations summary
- Redo both calibrations after: nozzle swap (size/material), new filament brand or type, big temperature change, moisture change.
- Flow ratio depends on filament diameter tolerance and temperature; K depends on filament stiffness, temperature, nozzle and plate type.
- Bambu-brand PLA: skip or only validate. Third-party PLA: do both.
- Multi-filament (AMS Lite) prints: auto flow-dynamics at print start covers only the first filament; saved per-filament K values are what applies to the others.

## 5. Recommended ordering
Sources:
- Spark Lab (UNBC) A1 guide: Flow Dynamics BEFORE Flow Rate.
- Eolas Prints and 3DBite: Flow Rate BEFORE Pressure Advance (https://eolasprints.com/blogs/advanced-3d-printing/bambu-studio-calibration-guide-getting-perfect-prints-every-time ; https://3dbite.com/best-3d-printer-calibration-routine-bambu-a1-a2l/).
Disagreement: community orders differ. Rationale for PA first on the A1: auto flow dynamics is quick, and flow-ratio blocks have many speed changes where PA mismatch can skew top-surface appearance. Rationale for flow first: PA patterns assume right extrusion amount. Pragmatic compromise: do auto FD -> flow pass 1/2 -> if corner quality is poor, redo FD (cheap on A1).

Ordered procedure:
1. Hardware: clean nozzle, extruder gears, wipe/inspect plate, check belts/tension; dry the PLA; update firmware.
2. First layer / z-offset (auto on A1 at print start) and filament profile selection (correct type, nozzle).
3. Temperature check only if the default is clearly wrong.
4. Flow Dynamics auto-calibration; save and assign K to the filament. (Manual pattern as cross-check if doubtful.)
5. Flow Rate pass 1 -> save ratio -> pass 2 -> save preset.
6. Re-run/verify FD if corners look off; print a test part.
7. Max volumetric speed (if wanting faster prints), then input shaping/other speed tuning.
8. Uncheck print-time "Flow dynamics calibration" if you want your saved K used; otherwise leave on to auto-calibrate each print (slower, first filament only).

## 6. Sources
- https://sparklab.unbc.ca/?p=682 (A1 extrusion calibration how-to; main step source)
- https://wiki.bambulab.com/en/bambu-studio/Calibration and https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa (official; only seen via search excerpts, fetch blocked 402)
- https://forum.bambulab.com/t/questions-about-flow-dynamics-and-extrusion-multiplier-on-the-a1/47642
- https://forum.bambulab.com/t/pressure-advance-flow-dynamics/67454
- https://forum.bambulab.com/t/what-formula-does-bambu-use-for-flow-rate-calibration/197570
- https://forum.bambulab.com/t/use-k-factor-from-auto-calibration/144411
- https://forum.bambulab.com/t/manual-calibration-with-a1-does-it-work/101778
- https://forum.bambulab.com/t/flow-dynamic-calibration-runs-forever/44454
- https://3dbite.com/best-3d-printer-calibration-routine-bambu-a1-a2l/
- https://eolasprints.com/blogs/advanced-3d-printing/bambu-studio-calibration-guide-getting-perfect-prints-every-time
