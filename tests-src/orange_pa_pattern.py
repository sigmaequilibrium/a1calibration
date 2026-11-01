"""R13 pressure-advance pattern for the 0.2 mm nozzle, ELEGOO Rapid PLA+ orange (225 C, 190 mm/s, 5000 mm/s^2).

One 90-degree chevron (3 walls thick, 1 mm tall) per K value. All chevrons are separate objects; after slicing,
tests-src/orange_pa_pattern_post.py inserts `M900 K<k>` after every "; printing object <name>" comment so each chevron
prints with its own K. The best K is the chevron whose apex is sharpest (no bulge, no rounded gap).

Run:  .venv/Scripts/python -I tests-src/orange_pa_pattern.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import trimesh

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_3mf as b  # noqa: E402
import flow_ratio_coarse as c  # noqa: E402

KS = [round(0.01 * i, 3) for i in range(9)]               # 0.00 ... 0.08 step 0.01
ARM, W, H = 14.0, 0.66, 1.0
SPEED, ACCEL = 190.0, 5000
PITCH_X = 25.0


def chevron() -> trimesh.Trimesh:
    """Two arms (W wide) leaving the apex at +-45 deg."""
    import manifold3d as md
    arm = md.Manifold.cube((ARM, W, H)).translate((0, -W / 2, 0))
    a1, a2 = arm.rotate((0, 0, 45)), arm.rotate((0, 0, 135))
    v = a1 + a2
    mesh = v.to_mesh()
    return trimesh.Trimesh(np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts))


def main() -> int:
    stl_dir = b.STL / "0.2" / "orange_pa_pattern"
    stl_dir.mkdir(parents=True, exist_ok=True)
    over = b.base_over("0.2", wall_loops=3, bottom_shell_layers=1, top_shell_layers=0, sparse_infill_density="0%",
                       brim_type="outer_only", brim_width="2", outer_wall_speed=f"{SPEED:g}", inner_wall_speed=f"{SPEED:g}",
                       default_acceleration=str(ACCEL), outer_wall_acceleration=str(ACCEL),
                       inner_wall_acceleration=str(ACCEL), seam_position="back")
    objs = []
    n = len(KS)
    for i, k in enumerate(KS):
        m = chevron()
        p = stl_dir / f"pa_K{k:.3f}.stl"
        m.export(p)
        x = b.CX + (i - (n - 1) / 2) * PITCH_X
        objs.append(b.Obj(p, p.stem, over, at=(x, b.CY)))
    fil = dict(c.FIL_OVER, nozzle_temperature="225", nozzle_temperature_initial_layer="225", fan_min_speed="100",
               fan_max_speed="100", filament_flow_ratio="1.03", filament_max_volumetric_speed="50",
               slow_down_for_layer_cooling="0", close_fan_the_first_x_layers="3",
               textured_plate_temp_initial_layer="65",
               initial_layer_speed="10", initial_layer_infill_speed="10", brim_width="2")
    pr = b.Project("0.2", "R13_orange-rapid_pa-pattern_0.2", objs, fil_over=fil)
    prof = b.Profiles(b.find_profile_dir(None), b.TAG)
    dest = b.OUT / "0.2" / f"{pr.out_name}.3mf"
    rep = b.build_project(prof, pr, b.TAG.lstrip("v"), dest)
    errs = b.validate(dest, rep)
    print(dest.name, "OK" if not errs else errs, "K:", KS)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
