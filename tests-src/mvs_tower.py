"""R5 max volumetric speed test for the 0.2 mm nozzle, ELEGOO Matte PLA purple reference.

A single-wall spiral-vase cylinder. The outer wall is sliced at a speed that gives Q_MAX (3.0 mm^3/s) and every
BAND_H mm of height a custom G-code `M220 S<pct>` scales the feed rate so the flow steps from Q_MIN to Q_MAX in
Q_STEP steps. Slow-down for layer cooling is off (a spiral layer is under 1 s at these speeds) and the filament's
volumetric cap is lifted so the slicer does not clamp the speed. Read the height where the wall goes thin, ridged
or gappy and convert with the table printed here.

Run:  .venv/Scripts/python -I tests-src/mvs_tower.py [BASE_SPEED_MM_S]
Writes stl/0.2/mvs_tower_Q1.0-3.0_0.2.stl and 3mf/0.2/R5_matte-purple_mvs-tower_0.2.3mf.
"""

from __future__ import annotations

import sys
from pathlib import Path

import trimesh

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_3mf as b  # noqa: E402
import flow_ratio_coarse as c  # noqa: E402

Q_MIN, Q_MAX, Q_STEP = 1.0, 3.0, 0.1
BAND_H = 1.0                  # mm of height per flow step
Z0 = 0.5                      # bottom solid layers + first spiral layer, below the first band
DIAM = 30.0
BASE_SPEED = 150.0            # mm/s outer wall at 100 %; tune so the printed flow at 100 % is Q_MAX


def bands():
    n = round((Q_MAX - Q_MIN) / Q_STEP) + 1
    return [(round(Z0 + i * BAND_H + 0.1, 4), round(Q_MIN + i * Q_STEP, 2)) for i in range(n)]


def main() -> int:
    base = float(sys.argv[1]) if len(sys.argv) > 1 else BASE_SPEED
    bs = bands()
    height = Z0 + len(bs) * BAND_H
    m = trimesh.creation.cylinder(radius=DIAM / 2, height=height, sections=180)
    m.apply_translation([0, 0, height / 2])
    out = b.STL / "0.2" / f"mvs_tower_Q{Q_MIN:.1f}-{Q_MAX:.1f}_0.2.stl"
    out.parent.mkdir(parents=True, exist_ok=True)
    m.export(out)
    gcodes = [(0.2, f"M220 S{round(100 * Q_MIN / Q_MAX)}")] + [(z, f"M220 S{round(100 * q / Q_MAX)}") for z, q in bs]
    over = b.base_over("0.2", wall_loops=1, bottom_shell_layers=4, top_shell_layers=0,
                       sparse_infill_density="0%", brim_type="no_brim", outer_wall_speed=f"{base:g}",
                       internal_solid_infill_speed="60", bottom_surface_speed="60", sparse_infill_speed="60")
    fil = dict(c.FIL_OVER, filament_flow_ratio="1.03", filament_max_volumetric_speed="50",
               slow_down_for_layer_cooling="0", spiral_mode="1")   # spiral_mode is plate-wide: only honoured in the project settings
    pr = b.Project("0.2", "R5_matte-purple_mvs-tower_0.2", [b.Obj(out, out.stem, over)], fil_over=fil, gcodes=gcodes)
    prof = b.Profiles(b.find_profile_dir(None), b.TAG)
    dest = b.OUT / "0.2" / f"{pr.out_name}.3mf"
    rep = b.build_project(prof, pr, b.TAG.lstrip("v"), dest)
    errs = b.validate(dest, rep)
    print(dest.name, "OK" if not errs else errs, f"height {height:.1f} mm, base {base:g} mm/s")
    print("z band start -> Q mm^3/s:", ", ".join(f"{z - 0.1:.1f}:{q}" for z, q in bs))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
