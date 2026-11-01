# A1 + Bambu Studio (PLA): Retraction, VFA, Bridging, Dimensional Accuracy, Verification

Research caveat: wiki.bambulab.com pages returned HTTP 402 to the fetch tool, so their content is known only from search-result snippets (marked "snippet"). Anything labeled "general knowledge" is not from a fetched source. Verify numbers against the live wiki before relying on them.

## Key findings / flags up front

1. **Bambu Studio has a built-in Calibration menu, but it is aimed at third-party printers.** The wiki says the Calibration page is "for advanced users, not recommended for beginners" and is about third-party printers ([wiki Calibration](https://wiki.bambulab.com/en/bambu-studio/Calibration), snippet). On a Bambu A1 the retraction test and the VFA test may be absent or limited. UNCERTAIN. Check the Calibration menu in your installed version. If they are missing, use OrcaSlicer's calibration menu or a MakerWorld test model (links below).
2. **The VFA test is an OrcaSlicer feature.** I found no source showing Bambu Studio has one. Docs: [OrcaSlicer VFA](https://www.orcaslicer.com/wiki/calibration/vfa_calib). Its output (resonance avoidance speed range) has no Bambu Studio equivalent. The A1 firmware does its own input shaping and resonance compensation. For the A1, VFA is therefore low priority (general knowledge). Use it only to pick an outer-wall speed.
3. **The A1 default retraction is about 0.8 mm** in the stock profile ([forum](https://forum.bambulab.com/t/stringing-the-never-ending-story/46371)). Users report clean PLA/PETG with defaults. Retune only if you see stringing.
4. **Radius vs diameter for XY compensation:** the XY hole and contour values are per-side (radius). If a hole is 0.1 mm too small in diameter, enter 0.05 ([forum summary, snippet](https://forum.bambulab.com/t/adjusting-the-hole-diameter/69468)). The Bambu wiki formula is (nominal - actual) / 2 ([XY compensation wiki](https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation), snippet).
5. **Disagreement on elephant foot values:** the P1S 0.2 mm profile defaults to 0.15 mm. The A1 mini default is 0, and users report 0.15 did not work well there ([forum, snippet](https://forum.bambulab.com/t/bottom-layers-lip/179917)). Typical suggested range is 0.1-0.2 mm. Another thread reports elephant foot persisting even at 0.25 ([forum](https://forum.bambulab.com/t/elephant-foot-even-with-0-25mm-compensation/149836)). Treat the value as empirical for your plate and bed temperature.

## Ordered procedure

Do these in order. The earlier steps (flow, PA, temperature, first layer) are assumed done by other research notes.

### Step 1: Retraction test (only if you see stringing)

- **Run it:** In Bambu Studio, use Calibration > Retraction Test (if present for your printer), then Adjust Parameters. Typical settings are start 0, end 2, step 0.1 mm ([wiki Calibration](https://wiki.bambulab.com/en/bambu-studio/Calibration), snippet; [MakerWorld retraction tower](https://makerworld.com/en/models/613254-retraction-tower)). Direct drive and PLA need small values, so end at about 1.5-2 mm.
- **Fallback:** Print a MakerWorld retraction tower, or use OrcaSlicer's Retraction test, which varies retraction length by height.
- **Read it:** Find the lowest tower height where the strings between pillars disappear. Convert that height to a retraction length (height / total height x range). Pick that value plus a small margin, about +0.1-0.2 mm. Avoid over-retracting: it causes under-extrusion and clogs, especially with the A1's reverse-Bowden-free direct drive but with a fast-heating hotend.
- **Note:** PLA often shows no stringing at any setting ([snippet](https://makerworld.com/en/models/613254-retraction-tower)). If so, keep the default 0.8 mm.
- **Apply:** Filament settings > Setting Overrides > Retraction length, and speed. This is saved in the filament preset. Alternatively set it in Printer settings > Extruder > Retraction (printer-wide). Prefer the filament override so other filaments keep their values.
- **Pass criteria:** no visible strings on the tower and no gaps or under-extrusion at the pillar starts.
- **Also consider:** if stringing remains, try lowering nozzle temperature 5 C or drying the filament before increasing retraction (general knowledge). Z-hop on the A1 has had reported issues ([forum](https://forum.bambulab.com/t/a1-and-bambu-studio-issues-z-hop-retractions-and-axis-limits/48872)).

### Step 2: VFA test (optional)

- **Run it:** OrcaSlicer: Calibration > VFA. Set speed range 20-200 mm/s, step 10 ([OrcaSlicer VFA](https://www.orcaslicer.com/wiki/calibration/vfa_calib)). Print the tower.
- **Read it:** Look for speed bands where the wall surface shows fine vertical ripples. Note the bands.
- **Apply:** OrcaSlicer applies the result in the printer profile as the Resonance Avoidance Speed Range. In Bambu Studio there is no such field, so the practical use is to set the outer wall speed (Process > Speed) outside the bad band.
- **Uncertainty:** whether this is meaningful on the A1 is unverified. Skip it if surfaces already look clean.

### Step 3: Bridging and overhang tuning

- **Settings in Bambu Studio:** Process > Quality has "Bridge flow" and "Thick bridges". Thick bridges extrude the bridge line at nozzle diameter. It applies only to external bridges. Internal bridges always use it ([wiki bridge, snippet](https://wiki.bambulab.com/en/software/bambu-studio/parameter/bridge)). Bridge speed is under Process > Speed.
- **Guidance from sources:** spans of 12-25 mm can be printed unsupported with good quality ([Fab Academy test](https://fabacademy.org/2025/labs/chaihuo/docs/week5/chaihuo/week05_group_assignment_3d_printer_test_en/)). Fan at 100% on bridges. Slow bridge speed to about 20-40 mm/s. Lower temperature 5-10 C. Add supports beyond about 50 mm ([3dprintingspace](https://3dprintingspace.com/t/how-to-fix-sagging-bridges-and-poor-bridging-settings-for-clean-overhangs-bambu-lab-ender-prusa/10449)). Forum tips: [3 ways to improve bridging](https://forum.bambulab.com/t/3-ways-to-improve-bridging-in-flat-roof-structures/192127).
- **Run it:** Print a bridge/overhang test from MakerWorld (e.g. [model 1916063](https://makerworld.com/en/models/1916063), unverified content) or the "Overhang test" model. Test spans of 10, 20, 30, 40 mm and overhang angles 45/60/70 degrees.
- **Read it:** Sag on the underside (rough and drooping lines), and gaps. Change one variable at a time: bridge flow in steps of 0.05 (for example 1.0 to 0.95), then thick bridges on/off, then bridge speed.
- **Apply:** edit the process preset. Save as a user preset.
- **Disagreement:** the sources' temperature and speed advice is generic, and not Bambu-specific. The Bambu default bridge flow is 1.0 with the profile's own speeds; defaults are generally good. Change them only if the test shows a problem.
- **Pass criteria:** 20 mm bridge with no visible sag and no broken lines; overhangs to 60 degrees clean.

### Step 4: Dimensional accuracy

1. **Prepare:** PLA has the lowest shrinkage, so calibrate with PLA ([wiki shrinkage, snippet](https://wiki.bambulab.com/en/knowledge-sharing/3d-prints-shrinkage)). Use a stable plate temperature and let parts cool fully before measuring.
2. **Print the test:** a calibration cube or the [X-Y Compensation Tool](https://makerworld.com/en/models/129893-x-y-compensation-tool) (page could not be fetched; content unverified), or a [tolerance test](https://makerworld.com/en/models/2236614-tolerance-test). Print with your normal production process preset, not a special one.
3. **Measure:** use calipers, measure several times, and measure from the top surface to avoid the elephant foot ([snippet](https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation)). Measure outer dimensions (X and Y) and hole diameters separately.
4. **Compute:** deviation = nominal - actual. Contour or hole compensation = deviation / 2 (per side).
   - Example: a 20.00 mm outer measures 19.90, so deviation = +0.10, compensation = +0.05 on the contour.
   - Example: a 10.00 mm hole measures 9.85, so enter hole compensation +0.075.
5. **Apply:** Process > Quality > "X-Y hole compensation" and "X-Y contour compensation" (positive grows, negative shrinks) ([snippet](https://forum.bambulab.com/t/adjusting-the-hole-diameter/69468)). Suggested PLA starting hole value is 0.05 mm (0.1 PETG/ABS, 0.15 nylon). Reprint and iterate once.
6. **Shrinkage:** PLA shrinkage is small (about 0.2-0.5%, general knowledge, not verified). Bambu Studio has a per-filament "Shrinkage" setting (Filament > Basic, as a percentage). It is useful for ABS/ASA, but for PLA you can leave it at 100% and use XY compensation. UNCERTAIN: this path is from general knowledge, so check your version.
7. **Elephant foot:** Process > Quality > Elephant foot compensation. Start at 0.1-0.15 mm on the A1 and adjust by 0.05 mm. Pass: bottom edge flush with the wall at 10x magnification, with no lip you can feel with a fingernail. Elephant foot is mainly caused by first layer squish and bed temperature, so fix first layer Z offset and flow first, then compensate ([forum](https://forum.bambulab.com/t/bottom-layers-lip/179917), [3dprintingspace](https://3dprintingspace.com/t/how-to-fix-elephants-foot-on-3d-prints-7-fixes-for-a-clean-base-bambu-lab-ender/10426)). Beware: brims can interact with elephant foot compensation ([forum](https://forum.bambulab.com/t/potential-bug-with-brims-and-elephant-foot-compensation/232772)).
8. **Caveats:** XY compensation applied to the contour can distort mating parts, so apply it to the global preset only when your prints are generally accurate. Round sections are often smaller than square ones ([forum](https://forum.bambulab.com/t/square-section-is-good-but-round-section-is-small/168189)); this is why holes get a separate value.

### Step 5: Final verification

Print with the final saved presets (all tuning applied, nothing changed between prints):

| Test | Model | Pass criteria |
|---|---|---|
| Dimensions | calibration cube 20 mm, or XY tool | each axis within +/-0.1 mm (a reasonable target; +/-0.05 is achievable on a tuned printer); hole error within +/-0.1 mm |
| Fit | [tolerance test](https://makerworld.com/en/models/2236614-tolerance-test) | the intended clearance tier fits as designed, with no fusing at the tighter gaps |
| Stringing | retraction tower or a two-pillar test | no strings |
| Bridges/overhangs | bridge and overhang test (see Step 3) | 20 mm bridge clean; 60 degree overhang clean |
| First layer / elephant foot | any model with a flat base | uniform first layer, no lip |
| Real-world check | a part from your actual use | assembles; no visible defects |

Record all final values (retraction, bridge flow, XY hole/contour, elephant foot) in a saved user preset, and re-measure after any filament change or nozzle swap.

## Source reliability

- Official Bambu wiki pages: relevant but not directly readable here (snippets only).
- Forum, MakerWorld and blog sources: community knowledge, varied quality.
- The numeric defaults (retraction 0.8 mm, elephant foot 0.15 on P1S, hole compensation 0.05 PLA) come from snippets or forum posts. The shrinkage percent and the +/-0.1 mm pass thresholds are my own suggestions.
