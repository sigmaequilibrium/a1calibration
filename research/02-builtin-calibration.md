# Bambu Lab A1: built-in machine calibration

Scope: A1 (not mini), Bambu Studio, PLA default. Researched 2026-10-06.

**Source caveat.** wiki.bambulab.com returned HTTP 402 to my fetcher for every page (e.g. https://wiki.bambulab.com/en/general/printer-calibration), so I could not read the official wiki directly. Findings come from Bambu store/product pages (via search summaries), the Bambu forum, a Bambu Studio GitHub issue, and third-party guides (some are low-authority blogs). Items marked [UNVERIFIED] are from those or from general knowledge; check them against the wiki and the printer's own screen. Menu wording varies by firmware and Studio version.

## 1. What each calibration does

| Item | What it does | Automatic? |
|---|---|---|
| Auto bed leveling (ABL) | Nozzle-contact/force sensing builds a bed height mesh that is compensated during the print. Bambu marketing says the A1 calibrates "Z-offset, bed-level, vibration resonance and nozzle pressure for EVERY print job". | Yes, per print, optional via checkbox in the Studio Print dialog. |
| Z offset / nozzle height | Determined as part of the same bed-touch routine. | Yes, with ABL. |
| Vibration compensation (input shaping / resonance) | Toolhead and bed vibrate at various frequencies; the accelerometer measures resonance and sets input shaping to cut ringing/ghosting. Can also flag belt tension changes. | Yes, at the start of prints (forum: "executes at the start of every print"); also a manual routine. Can be disabled via print dialog option (version-dependent) or by editing start G-code ("mech mode fast check", per forum). |
| Motor noise cancellation (MNC) | Calibrates per-motor drive parameters to reduce stepper whine. Essentially a one-off per machine. | Manual / setup wizard. |
| Flow dynamics (pressure advance, K value) | Per filament. A1 uses a toolhead pressure sensor to measure extrusion pressure and compute K automatically (no printed pattern in Auto mode). Saved to a filament profile. | Not per print for filaments with a stored K; run it per new filament. |
| Flow rate | Print-based, per filament. A filament-level calibration, covered in other docs. | No. |

Nozzle offset / toolhead camera: the A1 has a single nozzle, so there is no nozzle-offset calibration. I found no source indicating a toolhead camera built in. [UNVERIFIED; absence of evidence only.]

Disagreement on sensors: BabaBuilds says ABL uses "force sensors under the bed" and calls the flow sensor "eddy-current". Bambu's marketing text also says eddy-current for the nozzle-pressure sensor. Sensor-physics claims in blogs are uncertain, but do not change the procedure.

## 2. Recommended order

Machine-level first (filament-independent), then filament-level.

1. Mechanical sanity: belts, rods, bolts, nozzle clean, plate clean and seated (BabaBuilds says sensor readings depend on this).
2. Run the setup/startup calibration once: vibration compensation + motor noise cancellation + bed leveling/Z offset. A third-party source says about 8-12 minutes [UNVERIFIED].
3. Load PLA, run Flow Dynamics Auto calibration for that PLA.
4. Optional: flow rate and other fine-tuning (other research docs).

Disagreement: BabaBuilds lists vibration, MNC, flow dynamics, flow rate, then ABL last. Since ABL also runs each print, its position matters little. 3DBite gives a filament-tuning order (first layer, temperature, flow rate, pressure advance, max volumetric speed), not a machine order. All agree machine-level precedes filament-level.

## 3. How to run

### On the printer screen
- First boot: the setup wizard runs startup calibration (bed leveling, vibration compensation, motor noise cancellation). Make sure each is ticked.
- Later: Settings/Calibration > Calibration wizard > choose Bed leveling / Vibration compensation / Motor noise cancellation / Flow dynamics > Start. 3DBite cites "Calibration > Calibration Wizard > Bed Levelling". Exact labels vary [UNVERIFIED].
- Clear the bed and surroundings first; the toolhead and bed make large sweeps.

### In Bambu Studio
- Device tab (printer connected) > Calibration (or top toolbar Calibration) > pick the item.
- Flow Dynamics: Calibration > Flow Dynamics > Automatic Calibration (A1 only), select nozzle size, plate type and the loaded filament, Calibrate, then save the K value to that filament profile (BabaBuilds). Manual mode (pattern/line) is the alternative; 3DBite suggests Pattern over Line for textured plates.
- Per print: the Print dialog has checkboxes for Bed leveling, Flow dynamics calibration, and on the A1 vibration compensation / motor noise options. GitHub issue https://github.com/bambulab/BambuStudio/issues/4347 shows the vibration checkbox was missing in some Studio versions, so availability depends on version.

## 4. When to re-run

| Calibration | Re-run when |
|---|---|
| Bed leveling / Z offset | Default: every print (leave on). Always after nozzle change, plate swap, toolhead/bed repair, or first-layer problems. May be skipped when reprinting the same plate repeatedly to save time. |
| Vibration compensation | Setup; after moving/transporting, belt changes, replacing rods/hotend/toolhead parts, added weight, or when ringing/ghosting appears. Forum: temperature, toolhead weight and mechanical setup change the profile. One forum user disables it per print (saves roughly 8-10 minutes) but runs it occasionally to verify belts. |
| Motor noise cancellation | Setup; after replacing a motor or if whine returns. |
| Flow dynamics | New filament brand/type; nozzle size change or nozzle swap; hotend changes; corner bulging/gaps; major firmware update. Use dry filament (BabaBuilds, 3DBite). |

Disagreement: one source says the A1 runs ABL, Z offset, vibration compensation and flow dynamics before every print. The forum and other guides indicate per-print runs apply to bed leveling and vibration, while flow dynamics is per filament profile. Treat "all four every print" as marketing simplification. Another guide (3DBite) says to only touch machine-level calibrations manually after a nozzle change or plate swap, while the forum treats vibration compensation as worth re-running after mechanical changes. Reconcile by running manually after any hardware change.

## 5. Ordered step-by-step procedure (PLA)

1. Inspect and clean: tighten loose bolts, check belts and nozzle, wipe the plate, seat it correctly.
2. Clear the bed and surroundings; power on and finish the setup wizard, or open the Calibration menu.
3. Run Vibration compensation to completion.
4. Run Motor noise cancellation (once; skip if the setup wizard already did it).
5. Run Bed leveling (includes Z offset).
6. Load dry PLA and make sure it is primed.
7. In Studio: Calibration > Flow Dynamics > Automatic; select nozzle, plate, PLA; Calibrate; save K to the PLA profile.
8. Print a test with Bed leveling and Vibration compensation ticked and check the first layer.
9. Keep per-print ABL on; re-run others per section 4.

## 6. Open uncertainties
- Exact screen menu names and whether MNC is a Print-dialog checkbox on current firmware.
- Whether any toolhead camera or nozzle-offset calibration exists: none found.
- Time estimates come from low-authority sources.
- Verify against the official wiki (https://wiki.bambulab.com/en/general/printer-calibration), which I could not fetch.

## Sources
- https://bambulab.com/tr/a1 and https://uk.store.bambulab.com/en/products/A1 (product claims, via search summary)
- https://forum.bambulab.com/t/can-you-turn-off-the-vibration-test/187699
- https://github.com/bambulab/BambuStudio/issues/4347
- https://bababuilds.com/blog/bambu-lab-calibration-guide/
- https://bababuilds.com/blog/bambu-lab-flow-dynamics-calibration-k-value/
- https://3dbite.com/best-3d-printer-calibration-routine-bambu-a1-a2l/
- https://all3dp.com/4/bambu-labs-latest-update-brings-motor-noise-cancellation-to-the-x1-p1-series/ (search result only)
