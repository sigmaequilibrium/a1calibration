"""R6 final pressure-advance tower for the 0.2 mm nozzle, ELEGOO Matte PLA purple reference.

A hollow square tower with sharp corners. Every BAND_H mm of height a custom `M900 K<k>` (the same command Orca
emits for the filament's own pressure_advance) steps K from K_MIN to K_MAX. At the right K the corners are sharp with
neither a bulge (K too low) nor a rounded, gappy corner (K too high). Slow-down for layer cooling is off so the
speed, and with it the corner behaviour, stays constant. Filament: 190 C, flow ratio 1.03 (R2, R4).

Run:  .venv/Scripts/python -I tests-src/pa_tower.py
Writes stl/0.2/pa_tower_K0.060-0.140_0.2.stl and 3mf/0.2/R6_matte-purple_pa-tower_0.2.3mf.
"""

from __future__ import annotations

import sys
from pathlib import Path

import trimesh

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_3mf as b  # noqa: E402
import flow_ratio_coarse as c  # noqa: E402

K_MIN, K_MAX, K_STEP = 0.060, 0.140, 0.005
BAND_H = 1.2                  # mm of height per K step (12 layers of 0.10)
Z0 = 0.4                      # solid bottom layers, below the first band
SIDE = 35.0
SPEED = 100.0                 # mm/s outer and inner wall


def bands():
    n = round((K_MAX - K_MIN) / K_STEP) + 1
    return [(round(Z0 + i * BAND_H + 0.1, 4), round(K_MIN + i * K_STEP, 3)) for i in range(n)]


def main() -> int:
    bs = bands()
    height = Z0 + len(bs) * BAND_H
    m = trimesh.creation.box(extents=[SIDE, SIDE, height])
    m.apply_translation([0, 0, height / 2])
    out = b.STL / "0.2" / f"pa_tower_K{K_MIN:.3f}-{K_MAX:.3f}_0.2.stl"
    out.parent.mkdir(parents=True, exist_ok=True)
    m.export(out)
    gcodes = [(z, f"M900 K{k:.3f} L1000 M10") for z, k in bs]
    over = b.base_over("0.2", wall_loops=2, bottom_shell_layers=4, top_shell_layers=0, sparse_infill_density="0%",
                       brim_type="no_brim", seam_position="back", outer_wall_speed=f"{SPEED:g}",
                       inner_wall_speed=f"{SPEED:g}")
    fil = dict(c.FIL_OVER, filament_flow_ratio="1.03", filament_max_volumetric_speed="2.5",
               slow_down_for_layer_cooling="0")
    pr = b.Project("0.2", "R6_matte-purple_pa-tower_0.2", [b.Obj(out, out.stem, over)], fil_over=fil, gcodes=gcodes)
    prof = b.Profiles(b.find_profile_dir(None), b.TAG)
    dest = b.OUT / "0.2" / f"{pr.out_name}.3mf"
    rep = b.build_project(prof, pr, b.TAG.lstrip("v"), dest)
    errs = b.validate(dest, rep)
    print(dest.name, "OK" if not errs else errs, f"height {height:.1f} mm")
    print("z band start -> K:", ", ".join(f"{z - 0.1:.1f}:{k}" for z, k in bs))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
