# 01 - Hardware prep before calibrating a Bambu Lab A1 (PLA, Bambu Studio, AMS lite)

Research date: 2026-10-06. Confidence note: wiki.bambulab.com returned HTTP 402 to direct fetch, so wiki claims below come from search-result snippets and third-party mirrors, not full-page reads. Verify numbers against the live wiki before relying on them.

## Ordered checklist

### 0. Safety / baseline
- Power the printer OFF and let it cool before any hands-on work on the toolhead, wires or hotend (Bambu wiki hotend page, via search snippet).
- PASS: printer cold, powered off for hardware work.

### 1. Mechanical inspection (do first; a faulty frame ruins every later calibration)
- Place the printer on a flat, rigid, vibration-free surface. Feet should not rock.
- Remove all shipping material/foam/clips. With power off, check X gantry, Y bed and Z move by hand without binding or grinding.
- Check toolhead cable bundle and bed cable are seated and not snagged.
- Check the rear nozzle wiper is present and not coated in debris.
- PASS: smooth travel on all axes, no rocking, no stuck debris, no loose toolhead screws. FAIL: any grinding, rattling, wobble - fix before proceeding.
- Unsure: this step is general knowledge, not taken from a fetched page.

### 2. Firmware and software
- Update Bambu Studio to the current release and the printer firmware (printer screen, Bambu Handy or Studio).
- DISAGREEMENT/RISK: forum reports (April 2026) say A1 firmware 1.8 caused slowness, filament load/unload UI freezes, ghosting, SD card drop-outs and a missing auto-calibrate button for some users; the workaround was downgrading to 01.07.02.00 via Bambu Handy. Other threads show earlier firmware that "broke" calibration and was later fixed. Newest firmware is generally recommended, but check the forum and release notes before updating, and record the version you calibrated on.
- Calibration results (flow dynamics etc.) are tied to printer, filament and nozzle; re-run after a firmware update if behaviour changes (inference, not explicitly sourced).
- PASS: printer and Studio connected, versions recorded. FAIL: update stuck - power cycle and retry; downgrade if a known regression applies.
- Sources: https://forum.bambulab.com/t/firmware-update-problems-april-2026/249215 ; https://forum.bambulab.com/t/a1-a1-mini-firmware-v01-07-01-09-now-in-public-beta/222840 ; https://forum.bambulab.com/t/latest-01-05-00-00-firmware-broke-calibration-from-bambu-studio/46303

### 3. Belt tension (X, Y and Z belts)
- The A1 has 3 timing belts (toolhead X, bed Y, Z). It runs a frequency scan during calibration and prompts if re-tensioning is needed.
- Built-in check: Settings > Maintenance > Belt / Calibration, then Vibration Compensation. Target per a search summary of the official wiki: 110-150 Hz for X and Y. Sources disagree on the menu path ("Maintenance > Belt" vs "Maintenance > Calibration"); it may vary by firmware.
- Adjust with an H2.0 Allen key (wiki summary and bambuhub agree):
  - X: raise gantry to mid Z, loosen the tension screw at the toolhead back by ONE turn (do not remove), move toolhead along X 3 times by hand, retighten.
  - Y: remove the small cap at front-bottom of the base, loosen both tension screws one turn, move bed back and forth 3 times, retighten.
  - Z: (bambuhub only) loosen the two screws near the right column one turn, home, move Z up/down once, retighten.
- Then rerun Vibration Compensation.
- Pluck-the-belt test is community lore only; prefer the built-in test.
- PASS: X and Y within 110-150 Hz (verify on live wiki) and no tension warning. FAIL: out of range or warning persists after one re-tension - inspect belts for fraying/tooth wear, pulleys and screw seating; contact Support if unresolved.
- Sources: https://wiki.bambulab.com/en/a1/maintenance/belt_tension ; https://bambuhub.net/guides/belt-tensioning ; https://forum.bambulab.com/t/issue-with-a1-x-axis-tension-warning/104831/1

### 4. Nozzle / hotend condition
- Inspect nozzle tip: no burnt-on plastic, blobs or bent tip. Heat to about 200-220 C (PLA) and remove residue with a brass brush or tweezers (not bare hands).
- A1 nozzles are tool-less swappable (0.2/0.4/0.6/0.8 mm). After a swap: insert at a slight rearward tilt (magnet aids alignment), press the heatsink flush against the heating assembly, and sync nozzle diameter on the printer/Studio.
- For a suspected partial clog (clicking extruder, thin/uneven extrusion): cold pull. PLA cold pull temperature 70-100 C per wiki snippet (X1 wiki page; no A1-specific page confirmed).
- PASS: clean tip, smooth purge line of consistent width, no clicking. FAIL: irregular extrusion after a cold pull - replace the hotend.
- Forum reports of A1 "Z offset too low/over-squished" found a defective hotend assembly was the most common cause; support replaced it. Treat persistent over-squish after calibration as a possible hardware defect.
- Sources: https://wiki.bambulab.com/en/a1/maintenance/replace-hotend ; https://wiki.bambulab.com/en/x1/maintenance/what-is-cold-pull-and-how-to-perform-it ; https://forum.bambulab.com/t/a1-z-offset-appears-to-be-too-low/85426?page=2

### 5. Build plate type and cleaning
- Identify the installed plate (textured PEI, smooth PEI, Engineering Plate) and make sure Studio's selected plate type matches (affects temps and first layer; reasonable, not source-confirmed).
- Wash with warm water and dish soap, dry with a lint-free cloth, then do not touch the surface. IPA is common community practice on smooth PEI; the wiki snippet only cites soap and water.
- Let the plate cool a few minutes before removing prints; do not bend it.
- Check the magnetic bed and plate underside for debris (a speck causes uneven first layers); plate must sit flat.
- PASS: plate flat, evenly clean, no gouges. FAIL: dents, warp or stubborn grease - re-wash; replace if damaged.
- Sources: https://forum.bambulab.com/t/issues-with-the-a1-pei-build-plate/145778 ; first-layer/bed-cleaning test model https://makerworld.com/en/models/1007393

### 6. Filament and AMS lite path
- AMS lite spool limits: width 40-68 mm, inner diameter 53-58 mm (search summary of wiki FAQ). Avoid warped or cracked spools.
- One AMS lite per A1, 4 slots. Avoid TPU/TPE/PVA and generally CF/GF-filled filaments. Disagreement: Bambu PLA-CF/PETG-CF are listed as compatible in one snippet while third-party CF/GF is listed as unsupported; check the current wiki.
- Route the PTFE tube from AMS lite to the toolhead without sharp kinks; the spool must turn freely with no tangles or crossed loops.
- Assign each slot's material and colour in Studio (Bambu RFID spools auto-read; third-party spools must be set manually). A wrong type gives wrong temperatures and flow profile.
- Dry the filament (PLA roughly 45-55 C for several hours is common practice, not wiki-sourced here); wet filament causes stringing and bubbles that mimic calibration faults.
- Option: use the external spool holder for calibration prints if AMS lite path friction is suspected, then re-test via AMS.
- PASS: filament loads and unloads cleanly in every slot you will use, no grinding. FAIL: repeated load failures - check tube, kinks, spool fit.
- Sources: https://wiki.bambulab.com/en/ams-lite/manual/faq ; https://wiki.bambulab.com/en/a1-mini/manual/first-print-with-ams-lite (A1 mini page; closest found)

### 7. Z-offset / first-layer check
- The A1 probes the bed with the nozzle and sets absolute Z automatically per print (no paper method, no user Z-offset knob in the stock UI). Print-start options in Studio include bed leveling, vibration compensation and flow dynamics.
- Run the full machine calibration from the printer screen (Settings > Maintenance > Calibration) after steps 1-6 and note any errors.
- Print a first-layer test (e.g. wide single-layer square across the plate, community model https://makerworld.com/en/models/1007393).
- PASS: lines slightly flattened and fused with no gaps, no ridges or rough over-squish, uniform across the bed. FAIL: first clean nozzle and plate, rerun full calibration, dry filament. Then temporary software compensation (initial layer height, or initial-layer flow ratio; a forum user cites about 0.90; a G29.1 offset G-code was also mentioned - community, unsure). If it persists, suspect a defective hotend and contact Bambu Support.
- Sources: https://bambulab.com/tr/a1 ; https://forum.bambulab.com/t/first-layer-issues-a1-combo/216786 ; https://forum.bambulab.com/t/first-layer-issue-z-offset/243740 ; https://forum.bambulab.com/t/brand-new-a1-first-layer-issue/86853

### 8. Common mechanical faults that invalidate calibration
- Printer on a wobbly/soft surface or touching walls (ghosting, bad vibration compensation).
- Loose or over-tight belts; ignored tension warning.
- Loose toolhead/heatsink or hotend not fully seated after a nozzle swap (Z-offset errors).
- Debris or filament under the plate, on the nozzle, or at the wiper.
- Wet or poor-quality filament; tangled spool; AMS tube friction.
- Warped or dirty plate; wrong plate type selected in Studio.
- Not re-running calibration after belt, nozzle or plate changes.

## Gate before moving on to calibration
All of: belts in range with no warning; clean nozzle with smooth purge; clean flat plate with correct type selected; dry filament that loads cleanly; known-good firmware; full machine calibration completes without error; first-layer test passes. Otherwise stop and fix.

## Unsure / open items
- Belt Hz target (110-150) and menu path come from a search summary, not a fetched wiki page.
- PLA-CF AMS lite compatibility: sources conflict.
- Latest recommended firmware: conflicting forum reports (1.8 issues); verify at update time.
- Z-belt adjustment appears only in bambuhub, not confirmed in the official wiki.
- No A1-specific cold-pull page confirmed; X1 page used. Some A1 mini pages stood in for A1 (differences not verified).
