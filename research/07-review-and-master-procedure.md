# 07 - Independent review and master calibration procedure (Bambu Lab A1 + PLA, Bambu Studio)

Review date: 2026-10-06. Scope: fact-check of notes 01-06, cross-file contradictions, gaps, and one consolidated procedure.

## 0. How this review was sourced (read first)

- **The official wiki is readable.** WebFetch gets HTTP 402 from wiki.bambulab.com, but plain `curl` with a normal browser User-Agent got HTTP 200 on 2026-10-06. I downloaded and read these wiki pages in full:
  - A1 belt tension: https://wiki.bambulab.com/en/a1/maintenance/belt_tension
  - Printer calibration: https://wiki.bambulab.com/en/general/printer-calibration
  - Flow Dynamics: https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa
  - Flow Rate: https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate
  - Developer-mode calibration menu: https://wiki.bambulab.com/en/bambu-studio/Calibration
  - XY hole/contour compensation: https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation
  - Shrinkage: https://wiki.bambulab.com/en/knowledge-sharing/3d-prints-shrinkage
  - Drying: https://wiki.bambulab.com/en/filament-acc/filament/dry-filament
  - A1 firmware history: https://wiki.bambulab.com/en/a1/manual/a1-firmware-release-history
  - A1 hotend: https://wiki.bambulab.com/en/a1/maintenance/replace-hotend
  - AMS lite FAQ: https://wiki.bambulab.com/en/ams-lite/manual/faq
  - Cold pull (X1 page): https://wiki.bambulab.com/en/x1/maintenance/what-is-cold-pull-and-how-to-perform-it
- **Bambu Studio source code** (GitHub `bambulab/BambuStudio`, master branch, fetched 2026-10-06) was used to check menus, dialog defaults and formulas: `src/slic3r/GUI/MainFrame.cpp`, `calib_dlg.cpp`, `Plater.cpp`, `CalibrationPanel.cpp`, `CalibrationWizardStartPage.cpp`, `SelectMachine.cpp`, plus the stock profiles under `resources/profiles/BBL/` (filament, machine, process, and the A1 start G-code template). Master can be ahead of the release you have installed, so UI wording may differ slightly.
- Status labels used below:
  - **VERIFIED**: confirmed in a full wiki page or in Studio source/profiles.
  - **PARTIAL**: the main point is confirmed but a detail is not, or the evidence is forum-only but consistent.
  - **UNVERIFIED**: author's general knowledge, or a single forum or blog claim.

## 1. Fact-check of the priority claims

| # | Claim (file) | Verdict | Evidence |
|---|---|---|---|
| 1 | Belt target 110-150 Hz for X and Y (01) | **WRONG / UNSUPPORTED. Remove it.** | The official A1 belt page has no Hz target. It says the A1 "performs a frequency sweep during the preparation process... If re-tensioning is confirmed to be necessary, the printer will display a relevant prompt." BambuHub says outright "There is no frequency target to hit." The search-summary text behind the Hz figure also describes the Y axis as having "two belts, one per side", which is not the A1 design. The figure looks like a mix-up with other printers or an AI summary. |
| 2 | Belt menu path "Maintenance > Belt" vs "Maintenance > Calibration" (01) | **RESOLVED** | Wiki printer-calibration page, A Series: "Settings > Maintenance > Calibration", which shows three options. After tensioning, the belt page says: "select Vibration Compensation in the calibration menu". I found no separate "Belt" menu. |
| 3 | Belt adjustment: loosen 1 turn, move axis 3 times, retighten; Z belt "bambuhub only" (01) | **VERIFIED, including Z.** | The official A1 belt page covers X (screw at the back of the toolhead), Y (two screws under the front cap), and Z (two screws near the right column; Home, move Z up and down once, retighten). All use an H2.0 key. The tensioners self-set, so you loosen and retighten rather than "tighten more". |
| 4 | Firmware 1.8 problems; downgrade to 01.07.02.00 (01) | **PARTIAL, and outdated** | Forum thread 249215 (April 2026) does report 01.08.00.00 issues: slowness, SD card, bed leveling, UI freezes, ghosting. Users fixed them by downgrading to 01.07.02.00, with no staff reply. **But 01.08.01.00 was released on 2026-06-03.** It also fixes "an intermittent extrusion anomaly during the Flow Dynamics Calibration process in print jobs" (wiki firmware history). Recommendation: run 01.08.01.00 or newer. Downgrade only if one specific regression reproduces. Downgrade path: Bambu Handy > device > Firmware > "I want to downgrade" (forum), or the SD-card offline update. I did not confirm the "missing auto-calibrate button" claim. |
| 5 | A1 Z-offset: automatic, no user knob (01, 02) | **PARTIAL; important nuance** | The A1 stock start G-code (Studio profile) runs ABL (`G29`) when the bed-leveling flag is set. It then applies `G29.1 Z{-0.02}` **only when the plate type is "Textured PEI Plate"**, because the nozzle homes on the top of the texture. **So choosing the correct plate in Studio directly changes first-layer height.** The wiki has no user Z-offset in the A1 UI. The only lever is editing that `G29.1` line in a *copied* printer profile (community practice; more negative = nozzle closer). That carries a real risk of nozzle or plate damage. |
| 6 | Auto Flow Dynamics exists on A1; needs firmware 01.04.00.00 (03, 05) | **VERIFIED** | Wiki calibration_pa: "The A1 series printer only supports auto-flow dynamic calibration from firmware version 01.04.00.00." Method: it purges at the wiper and reads extrusion force with the toolhead eddy-current sensor. The wiki says results have about 10% jitter. The Studio source (`CalibrationWizardStartPage.cpp`) shows the Auto button for X1 and for i3-architecture (A1) printers. |
| 7 | Print-dialog "Flow Dynamics Calibration" overrides saved K (03, 05) | **VERIFIED** | Wiki: "If you check 'Flow Dynamics Calibration' before initiating each printing... this printing task will use the calibrated K value instead of the manually set K value." Current Studio shows it as a dropdown. It is Auto/On/Off on printers that report support for "Auto" (Auto = skip if this filament and nozzle were calibrated recently), otherwise On/Off. The wiki describes the 3-state behaviour only for H2D/H2C. Check which options your A1 shows. |
| 8 | Print-time FD on A1 calibrates only the first filament (05) | **WRONG for A1** (this is X1 behaviour) | Wiki: "For the A series... a flow calibration will be performed when each filament of this printing task is replaced for the first time, so all materials used in this printing task will be calibrated (supported since version 01.03.00.00)". The "first filament only" rule applies to the X1. The 2024 forum post in 05 predates this. |
| 9 | A1 auto K is "inflated" vs manual; treat it as wrong and use manual (03) | **REFRAMED** | Wiki: "The automatic calibration value (K value)... may sometimes be significantly higher than the manual calibration value, which is normal. This design is intended to avoid filament pile-up problems at the corners." **Do not "correct" auto K down to the manual value just because it is higher.** Use manual only when corners actually show a problem, with a 0.2 mm nozzle (wiki recommends manual there), or with a third-party hotend. |
| 10 | Flow ratio formula: new = old x (100 + modifier)/100 (05) | **VERIFIED** | Wiki (developer-mode page) plus Studio source: `print_flow_ratio = 1 + modifier/100` is applied on top of the filament flow ratio. The modifier is **signed**, so -6 gives x0.94. The wiki's pass-2 example writes "(100-6)" for modifier -6. It means the same thing, but the notation is inconsistent, which is the source of the "conflict" noted in 05. |
| 11 | Pass ranges (05: "-9 to 0" vs "+/-20" unverified) | **VERIFIED** | Calibration-tab wizard (wiki calibration_flow_rate): Coarse = 80-120% in 5% steps (9 blocks, -20 to +20). Fine = 91-100% in 1% steps (10 blocks, -9 to 0). **Consequence:** fine can only lower the ratio. In coarse, if two blocks look equally smooth, pick the **higher** one. |
| 12 | Flow ratio is manual-only on A1 (05) | **VERIFIED** | Wiki: "Only X1 series support Auto calibration" (it uses lidar). |
| 13 | Temperature tower procedure / defaults (04) | **VERIFIED (with corrections)** | Studio source: PLA preset 230 -> 190 C, 5 C per 10 mm block, **hottest at the bottom**. Input rules: start <= 350, end >= 180, start >= end + 5. **The Temperature, Retraction, Max flowrate and VFA tools are only in the top-bar Calibration menu, which for Bambu printers appears only with Developer Mode on** (`MainFrame::update_calibration_button_status`: `show_calibration = !isBBL \|\| developer_mode`). The wiki page says the same. Note 04 implies these sit in the normal Calibration tab. They do not. |
| 14 | Max volumetric speed procedure / formula (04) | **VERIFIED** | Dialog defaults: start 5, end 20, step 0.5 mm3/s. Formula (wiki + source): **MVS = start + measured height (mm) x step**. Example from the wiki: 10 + 14 x 1 = 24. Margin: wiki says "reduce by 5-10%". The test forces `slow_down_layer_time = 0`, spiral mode, layer height 0.8 x nozzle (0.32 mm) and line width 1.75 x nozzle (0.70 mm). So the cooling-slowdown caveat in 04 is already handled for the test print. The current Calibration-tab wizard has MVS commented out (`CalibrationPanel.cpp`), so on A1 the test is developer-mode only (03 was right about this). |
| 15 | Retraction test exists in Studio for A1? (06: "aimed at third-party printers, may be absent") | **EXISTS (developer mode)** | Studio source has "Retraction test" in the same developer-mode menu (defaults: start 0, end 2, step 0.1 mm per mm of height). Wiki: if a PLA tower is clean from the start, "setting the retraction length to 0.2mm - 0.4mm" is suggested. If it strings at the top, dry the filament and check the nozzle for leaks. |
| 16 | VFA test is OrcaSlicer-only (06) | **WRONG** | Bambu Studio has "VFA" under Calibration > More... (developer mode). Defaults: 40-200 mm/s, step 10. 06 is still right that Studio has no "resonance avoidance" field, and that the result is mainly used to choose wall speed. |
| 17 | XY compensation = (nominal - measured)/2; Process > Quality (06) | **VERIFIED** | Wiki: the setting is at **Process > Quality > Precision**. "The hole diameter will increase by twice the compensation value". Contour example: (55 - measured)/2. Positive values enlarge. The wiki says to fix shrinkage, elephant foot, moisture and Flow Dynamics first, and that the value is **per filament**. |
| 18 | Shrinkage setting path (06, "uncertain") | **VERIFIED** | Wiki: Filament Settings > Basic Information > "Shrinkage". Formula: (measured / designed) x 100%. It scales only the outer XY size. Holes are handled by XY hole compensation afterwards. |
| 19 | PLA drying temps (01, 03) | **PARTIAL; 03's A1 heatbed figure is not current** | Current wiki table, PLA Basic/Matte: forced-air oven **50 C / 8 h**; AMS 2 Pro / AMS HT 45 C / 12 h; heated-bed method **60-70 C / 12 h, flip every 6 h, covered**. That bed method is now listed for "H Series / X Series / P2S / P1S", **not A1**. Drying before use is "Recommended". I found no current wiki support for 03's "A1 heatbed 65-75 C". Use a filament dryer at about 45-50 C. |
| 20 | A1 PLA default fan / volumetric / flow values (03, 04) | **VERIFIED from Studio profiles** | **Bambu PLA Basic @BBL A1:** MVS **21** (03 said 22, which is wrong). Flow ratio 0.98. Fan min 60% / max 80%. Fan layer-time threshold 80 s. Slow-down layer time 6 s. Plate 65 C. **Generic PLA @BBL A1:** MVS 12, flow 0.98, fan 60/80, threshold 80 s, slow-down 8 s, nozzle 220 C. **Common to both:** overhang fan 100%, part fan off for the first layer, retraction 0.8 mm at 30 mm/s, Z-hop 0.4 mm "Auto Lift". **0.20mm Standard @BBL A1:** elephant-foot 0.075 mm, bridge flow 1.0, XY hole/contour 0. |
| 21 | Per-print vibration compensation is a Print-dialog checkbox on A1 (02) | **OUTDATED for current Studio** | The current `SelectMachine.cpp` print options are Timelapse, Auto Bed Leveling, Flow Dynamics Calibration and Nozzle Offset (multi-nozzle only). There is no vibration or MNC option. The A1 stock start G-code runs a "mech mode fast check" (`M970.3/M970.2` resonance check on X and Y) **unconditionally every print**. The full Vibration Compensation and MNC routines are run from the printer screen. |
| 22 | Elephant foot: "A1 mini default 0; start 0.1-0.15 on A1" (06) | **CORRECTED** | The A1 0.20 Standard profile already sets **0.075 mm**. Start from that, and change in 0.025-0.05 mm steps only if a lip remains. |
| 23 | AMS lite spool limits and CF compatibility (01) | **VERIFIED / RESOLVED** | Wiki FAQ: width 40-68 mm, inner diameter 53-58 mm. Third-party CF/GF is not recommended; **Bambu PLA-CF and PETG-CF are compatible.** TPU 95A and softer must not go through the AMS lite. |
| 24 | Cold pull PLA 70-100 C (01) | **PARTIAL** | Taken from the X1 wiki page (the wiki suggests 70 C for a first attempt). I found no A1 page. The A1 toolhead disassembly steps differ, so use the temperatures only, not the X1 steps. |
| 25 | When to redo FD (02, 05) | **VERIFIED, with one addition** | Wiki: new brand/model of filament, worn or replaced nozzle, **"When the maximum volumetric speed or print temperature is changed in the filament settings."** That addition drives the step order below. Also: firmware 01.07.02.00 added Z-axis motor noise cancellation, so re-run MNC once if you came from an older firmware. |

## 2. Contradictions between files, and how they are resolved

1. **Order of temp / flow / PA / MVS.**
   - 04 says flow -> PA -> temp -> MVS.
   - 05 says FD -> flow -> MVS, with temp only "if clearly wrong".
   - 03 says temp -> MVS -> FD -> flow.
   - 02 says machine -> FD.

   **Resolution**, based on official dependencies:
   - The FD wiki says to redo FD when temperature or MVS changes.
   - The flow-rate wiki says to do FD before flow rate.
   - The MVS test scales its flow targets by the filament flow ratio (`Plater.cpp`).

   So the order is: **temperature -> FD (auto, provisional) -> flow ratio coarse/fine -> MVS -> FD again (final) -> verify.** Auto FD on the A1 takes minutes and prints nothing on the plate, so running it twice costs little. If you leave temperature and MVS at the profile defaults, run FD once.
2. **Where the tests live.** 04 and 06 describe a "Calibration menu" with Temperature, MVS and Retraction. 02 and 05 describe the Calibration *tab*. **Both exist:**
   - The **Calibration tab** has Flow Dynamics (Auto/Manual) and Flow Rate (Manual). No developer mode is needed. It saves results into the printer or preset for you.
   - The **top-bar Calibration menu** has Temperature, Flow rate Coarse/Fine, Pressure advance, Retraction test, and More > Max flowrate / VFA. For Bambu printers it appears only after **Preferences > Developer mode**. In this menu you compute and type in the values yourself.
3. **Flow-rate pass naming.** "Pass 1/Pass 2" (old wiki, developer menu), "Coarse/Fine" (developer menu in the current source) and "Complete calibration / Fine calibration based on flow ratio" (Calibration-tab wizard) are the same pair of tests.
4. **Manual vs auto K.** 03 prefers manual and 05 prefers auto. **Resolution:** auto by default, because the wiki says the higher auto K is intended. Use manual pattern (step 0.002) only for a 0.2 mm nozzle, a third-party hotend, or visible corner defects.
5. **First-filament-only (05) vs all filaments.** The A1 calibrates every filament on first use in the job. See section 1, item 8.
6. **Max volumetric speed for Bambu PLA.** 03 says 22, 04 says ~21. The profile is **21**.
7. **Retraction.** 06 says keep 0.8 mm; the wiki suggests 0.2-0.4 mm when the PLA tower is clean. **Resolution:** keep 0.8 mm unless you have a reason to change it. Shortening is optional and low-value on a direct-drive A1. Never go above about 2 mm.
8. **Machine calibration order.** 02 lists vibration, MNC, ABL; BabaBuilds puts ABL last. Order does not matter much, because ABL also runs per print. Use the screen's "Calibration" with all three ticked.
9. **Drying.** 01 says 45-55 C; 03 gives four different sets of numbers. **Resolution:** dryer at 45-50 C for 6-8 h (wiki oven figure is 50 C / 8 h). Do not use the A1 bed method as an official route.

## 3. Problems found in the source notes

### Likely wrong or risky (fix or ignore)
- **01: 110-150 Hz belt target.** No official basis. Chasing an Hz number by over-tightening risks bearing and motor wear. The A1 tensioners self-set when you loosen and retighten.
- **01/02: "downgrade to 01.07.02.00".** Now superseded by 01.08.01.00. Downgrading also removes the 01.08 fix for PA parameters being overwritten after a power loss.
- **03: A1 heatbed drying at 65-75 C.** Not in the current wiki for the A1. On an open-frame moving bed it is also less controlled. At 60-70 C PLA spools can deform (the wiki itself warns about third-party spools).
- **05: "first filament only"** is wrong for the A1 (see section 1, item 8).
- **06: "VFA is OrcaSlicer only"** is wrong (see section 1, item 16).
- **06: elephant foot starting at 0.1-0.15 mm.** The A1 profile already uses 0.075. Raising it blindly can undersize the bottom layers.
- **04, 05, 06 (gap): forgetting that calibration projects modify the edited presets.** For example, the MVS test sets the filament max volumetric speed to **200** and slow-down to 0. The temperature test writes the start temperature into the filament preset. **Do not save presets while a calibration project is open.** The wiki says: "After completing the calibration process, remember to create a new project to exit the calibration mode."
- **01, step 7 (G29.1 / Z-offset hacks).** Present them only as a last resort, in a *copied* printer profile, in 0.01-0.02 mm steps. A defective hotend is the more common cause of over-squish (forum 85426).

### Unsupported but harmless
- 02: time estimates (8-12 min), and the sensor-physics claims from blogs. The wiki names an **eddy-current sensor** for A1 flow dynamics.
- 03: Studio menu path "File > Export > Export Presets Bundle" (from memory; check it).
- 04: cooling-tuning heuristics and PETG fan values (general knowledge).
- 05: "16 results per nozzle" K history limit (forum 144411 only).
- 06: bridge tuning numbers. The A1 defaults are bridge flow 1.0 and bridge speed 50 mm/s.

### Gaps (missing steps)
- **Plate type selection affects Z on the A1.** Textured PEI gets -0.02 mm in the start G-code, so selecting the wrong plate in Studio shifts the first layer.
- **Developer mode** is a prerequisite for the temperature, MVS, retraction and VFA tests. None of the notes say clearly that it is required for Bambu printers.
- **Exiting calibration mode** (start a new project) before saving presets.
- **Assigning K values to AMS lite slots** in the Device tab (05 covers this). It also matters that the print-time FD option should be **Off** if you want saved K values used.
- **Re-running MNC** after updating from firmware older than 01.07.02.00 (Z-motor MNC was added then).
- **Nozzle information** must be set on the printer (Settings > Maintenance > Nozzle) after a swap. Since Studio V02.01.01.52 it cannot be edited in Studio.
- **High-flow hotend:** the wiki lists one for the A1. If one is fitted, the PLA defaults and MVS above do not apply.
- **For Bambu PLA on stock hardware, most filament calibration can be skipped.** The wiki says flow-rate calibration is only needed if defects persist after FD, and the stock profiles are pre-tuned. Several notes say this, but none puts it first.

## 4. Master procedure (A1 + PLA, 0.4 mm stock hotend)

Legend: [V] verified, [P] partially verified, [U] unverified. Use the "fast path" for Bambu-brand PLA. Use the full path for third-party PLA.

### Phase A - Hardware and software baseline (once, and after any hardware change)

1. **Placement and mechanics.** Use a rigid, level surface and remove all shipping restraints. With the printer off, move X, Y and Z by hand: they should move smoothly. Check that cables are seated and the wiper is clean. [U, general practice]
2. **Firmware and Studio.** Update Bambu Studio. Update the A1 to **01.08.01.00 or newer** (released 2026-06-03). Record both versions. Downgrade only if a specific regression reproduces. [V] firmware history: https://wiki.bambulab.com/en/a1/manual/a1-firmware-release-history ; [P] 01.08.00.00 issues: https://forum.bambulab.com/t/firmware-update-problems-april-2026/249215
3. **Hotend.** Work with the printer off and cold. Seat the hotend: tilt it slightly toward the back, the magnet aligns it, the heatsink sits flush, the buckle locks. If you swapped nozzles, set the nozzle size and type **on the printer**: Settings > Maintenance > Nozzle. Clean the tip. Do a cold pull (PLA, about 70 C pull) only if you see clicking or inconsistent extrusion. [V] https://wiki.bambulab.com/en/a1/maintenance/replace-hotend ; [P] cold pull temperatures from the X1 page: https://wiki.bambulab.com/en/x1/maintenance/what-is-cold-pull-and-how-to-perform-it
4. **Belts (only when the printer prompts, or after transport/repair, or if you see ghosting or layer shifts).** Use an H2.0 key. For X, Y and Z: loosen the tension screw(s) one turn (do not remove them), move the axis by hand (X three times end to end; Y three times; Z: Home, then jog up and down once), and retighten. **There is no Hz target.** [V] https://wiki.bambulab.com/en/a1/maintenance/belt_tension
5. **Plate.** Wash with warm water and dish soap, dry it, and do not touch the surface. Check the magnetic bed and the plate underside for debris. [P] (the soap-and-water method is from wiki snippets cited in 01)
6. **Machine calibration from the screen.** Clear the bed area, then Settings > Maintenance > Calibration. Tick all three: bed leveling, vibration compensation, motor noise cancellation. Let it finish without errors. Re-run after moving the printer, a firmware update, belt work or any part change. [V] https://wiki.bambulab.com/en/general/printer-calibration
7. **AMS lite path.** Spool width must be 40-68 mm and inner diameter 53-58 mm. Put heavier spools in slots 2/3. Avoid tight PTFE bends. Set each slot's material in Studio (RFID spools are read automatically). [V] https://wiki.bambulab.com/en/ams-lite/manual/faq

**Gate A:** machine calibration completes with no belt prompt, filament loads and unloads cleanly in every slot you use, and the purge line is consistent.

### Phase B - First layer

8. **Select the correct plate type in Studio.** This is not cosmetic: the A1 start G-code applies `G29.1 Z-0.02` only for Textured PEI. Keep **Auto Bed Leveling** on in the print dialog (or Auto, if offered). [V] Studio profile `Bambu Lab A1 0.4 nozzle template machine_start_gcode.json`
9. **Print a single-layer test** across the plate, for example https://makerworld.com/en/models/1007393. Pass: lines are flat, fused and uniform, with no gaps and no ridging. [P]
10. **If it fails:** clean the nozzle and plate, re-run step 6, and dry the filament. If it is still over- or under-squished, contact Support (a defective hotend is a known cause). As a last resort only, edit the `G29.1` value in a **copied** printer profile in 0.01-0.02 mm steps. More negative means the nozzle sits closer. [P] https://forum.bambulab.com/t/a1-z-offset-appears-to-be-too-low/85426 ; https://forum.bambulab.com/t/z-offset-and-textured-plate/115088

### Phase C - Filament preparation and profile

11. **Dry the PLA** if the spool has been open for weeks, or if it pops or strings: filament dryer at 45-50 C for 6-8 h. The wiki oven value is 50 C / 8 h. Store it sealed with desiccant. [V for the oven value] https://wiki.bambulab.com/en/filament-acc/filament/dry-filament
12. **Create a user filament preset** for the "Bambu Lab A1 0.4 nozzle" printer. Base it on Bambu PLA Basic (MVS 21) for good PLA, or Generic PLA (MVS 12) to be conservative. Never edit system presets: RFID reloads overwrite them. [V for defaults] Studio profiles `Bambu PLA Basic @BBL A1.json`, `Generic PLA @BBL A1.json`; [P] create-filament wiki excerpt in 03.
13. **Fast path (Bambu-brand PLA):** skip to step 17 (auto FD), then step 23 (verify). The wiki says flow-rate calibration is only needed if defects remain after FD. [V] https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate

### Phase D - Filament calibration (third-party PLA)

14. **Enable Developer Mode** (Preferences > Developer mode). This adds the top-bar Calibration menu. [V] https://wiki.bambulab.com/en/bambu-studio/Calibration ; Studio source `MainFrame.cpp`
15. **Temperature tower.** Calibration > Temperature > PLA. Default 230 -> 190 C, 5 C per 10 mm block, hottest at the bottom. Pick the coolest block that still has good layer bonding, clean bridges and overhangs, and acceptable stringing. Enter it as nozzle temperature (first layer the same, or +5 C) in your preset. **Start a new project before you save the preset.** [V for mechanics; U for the judging heuristic] Studio source `calib_dlg.cpp`, `Plater.cpp::calib_temp`
16. **Temporary-change check:** after any developer-menu test, start a new project (File > New) so the test's overrides do not end up in your saved presets. [V] wiki Calibration page note.
17. **Flow Dynamics (provisional).** Calibration tab > Flow Dynamics > Auto-Calibration. Choose the 0.4 nozzle, the plate and the filament or slot, then Calibrate. The printer purges at the wiper; no plate print. Save the result and name it. A1 auto K can be higher than a manual K by design, and repeat runs vary by about 10%. Use Manual > Pattern, step 0.002, instead if you have a 0.2 mm nozzle, a third-party hotend, or corner defects. [V] https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa
18. **Flow ratio.** Calibration tab > Flow Rate > Manual > Complete calibration.
    - **Coarse:** 80-120% in 5% steps. Judge the top surfaces under low-angle light. If two blocks tie, pick the higher one.
    - **Fine:** 91-100% of the coarse result in 1% steps. Pick the smoothest block with no hint of gaps.
    - The wizard computes the ratio and saves it to a preset. Hand formula: new = old x (100 + signed modifier)/100.
    - A correction above about 10% points to a hardware or moisture problem.

    [V] https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate ; formula: https://forum.bambulab.com/t/what-formula-does-bambu-use-for-flow-rate-calibration/197570 ; Studio source `Plater.cpp::calib_flowrate`
19. **Max volumetric speed (optional, only if you print fast or with thick layers).** Developer menu > More... > Max flowrate. Defaults: start 5, end 20, step 0.5. For a fast PLA, raise the end to about 25-30. Measure the height of the first bad layer and compute MVS = start + height x step. You can confirm in Preview > Flow colour scheme. Enter 90-95% of that value. The test prints at 0.32 mm layers and 0.70 mm lines. Start a new project before saving. [V] wiki Calibration page; Studio source `Plater.cpp::calib_max_vol_speed`
20. **Flow Dynamics (final).** If you changed temperature or MVS in steps 15 or 19, re-run auto FD (wiki: recalibrate when these change). Assign the K value to each AMS lite slot: Device tab > slot > edit (eye icon) > choose the PA profile. If the list is full (forum: about 16 per nozzle), delete old entries first. [V for the trigger; P for the limit] https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa ; https://forum.bambulab.com/t/use-k-factor-from-auto-calibration/144411
21. **Print-dialog policy.**
    - To use your saved K values, set **Flow Dynamics Calibration = Off**.
    - With **On**, the A1 recalibrates every filament on its first use in the job and ignores the saved K.
    - **Auto**, if offered, skips filaments calibrated recently.

    [V] same wiki page; Studio source `SelectMachine.cpp`
22. **Cooling (only if overhangs, bridges or small features are poor).**
    - The A1 PLA defaults are fan 60-80% with an 80 s threshold, overhang fan 100%, part fan off for the first layer, and slow-down at 6 s (Bambu) or 8 s (Generic).
    - Change one variable at a time.
    - If the part is otherwise good, leave retraction at **0.8 mm**. If stringing persists after drying and a 5 C lower temperature, run the developer-menu Retraction test (0-2 mm, 0.1 mm/mm). Pick the shortest clean length and set it under Filament > Setting Overrides.

    [V for defaults] Studio profiles; [P] https://wiki.bambulab.com/en/bambu-studio/Calibration ; [U] cooling heuristics in 04.

### Phase E - Dimensional accuracy and verification

23. **Verification print** with the final saved presets and the normal process (0.20mm Standard @BBL A1): a 20 mm cube plus a corner/overhang/bridge test. Pass criteria:
    - corners have no bulge and no gap;
    - top surfaces are smooth;
    - no stringing;
    - a 20 mm bridge does not sag;
    - 60-degree overhangs are clean.

    [U for the thresholds, which are suggested by the reviewer and the authors]
24. **Shrinkage**, if the error grows with part size: Filament > Basic Information > Shrinkage = measured / designed x 100%. PLA usually needs none. [V] https://wiki.bambulab.com/en/knowledge-sharing/3d-prints-shrinkage
25. **XY hole and contour compensation**, if a fixed offset remains:
    - It is per filament and process, under Process > Quality > Precision.
    - Value = (nominal - measured)/2. Positive enlarges a hole or the outer size.
    - Measure above the first layers. Reprint once to confirm.

    [V] https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation
26. **Elephant foot.** The A1 default is 0.075 mm. Adjust in 0.025-0.05 mm steps only after the first layer (Phase B) is right. [V for the default] Studio profile `0.20mm Standard @BBL A1.json`; [P for the method] 06 sources.
27. **Optional VFA** (developer menu > More... > VFA, 40-200 mm/s). Use it only to choose an outer-wall speed that avoids a visible ripple band. [V that the tool exists; U whether it is useful on the A1]
28. **Save and log.** Save the user filament preset with a version suffix (e.g. `Sunlu PLA Black v1 @BBL A1`). Log the temperature, flow ratio, K, MVS, firmware version and date. Turn Developer mode off if you like.

### Re-run triggers (summary)
| Event | Re-run |
|---|---|
| Printer moved, firmware update, belt or part change | Step 6 (machine calibration). After a firmware update from older than 01.07.02.00, also run MNC. |
| Nozzle swap | Set the nozzle on the printer (step 3), then steps 6, 9 and 17/20, plus flow ratio if it is third-party filament. |
| New filament brand or type | Phase C/D steps 11-22 (fast path for Bambu PLA) |
| Temperature or MVS changed in the preset | Step 20 (FD) |
| Plate swapped or changed type | Step 8 (select the plate in Studio), step 9 |

## 5. Open questions to check on the real printer

1. What the **Settings > Maintenance > Calibration** screen on your firmware lists. Expect bed leveling, vibration compensation and motor noise cancellation. Check whether Z-motor MNC appears.
2. Whether your A1 print dialog shows **Auto/On/Off** or only **On/Off** for Flow Dynamics Calibration and Auto Bed Leveling, and what the defaults are.
3. Whether a belt-tension prompt ever appears after the preparation frequency sweep. There is no Hz value to read; confirm you don't see one either.
4. Which firmware is installed. If it is 01.08.00.00, update to 01.08.01.00+ and check whether the April 2026 symptoms (slowness, ghosting, load/unload UI freezes) are present.
5. Whether a high-flow hotend is fitted. If so, the stock PLA MVS and K do not apply.
6. Whether Developer mode in your installed Studio version shows Calibration > Temperature / Flow rate / Pressure advance / Retraction test / More (Max flowrate, VFA). I verified this against master source, which may be newer than your build.
7. Whether the Calibration-tab Flow Rate wizard shows "Complete calibration" and "Fine calibration based on flow ratio" for the A1, and whether it writes the ratio into a new preset.
8. The Device-tab K-profile list limit (forum says 16 per nozzle) and whether new results save when the list is full.
9. The exact menu path for exporting a presets bundle (03 wrote it from memory).
10. Your plate's actual type and condition (textured vs smooth) and that Studio matches it, since it changes Z.
11. Your auto-FD K for the PLA versus a manual pattern. Expect auto to be somewhat higher; act only if corners show a defect.

## 6. Note to the authors
- The wiki is reachable with `curl -A "<browser UA>" https://wiki.bambulab.com/en/...`. Pages are Wiki.js; their content sits inside `<template slot="contents">`.
- The Studio stock profiles at `raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/` are the authoritative source for default values.
