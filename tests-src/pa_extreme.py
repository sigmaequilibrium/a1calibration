"""Sanity check that the printer obeys `M900 K` changes mid-print: same square tower as pa_tower.py but K alternates
between 0.00 and 0.50 every 2.4 mm. The corners must look very different (sharp/bulged at K 0, rounded/starved
at K 0.5) or the printer is ignoring M900 K.

Run:  .venv/Scripts/python -I tests-src/pa_extreme.py
Writes 3mf/0.2/R6x_matte-purple_pa-extreme_0.2.3mf.
"""

from __future__ import annotations

import sys
from pathlib import Path

import trimesh

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_3mf as b  # noqa: E402
import flow_ratio_coarse as c  # noqa: E402
import pa_tower as p  # noqa: E402

KS = [0.0, 0.5, 0.0, 0.5, 0.0, 0.5]
BAND_H = 2.4
Z0 = p.Z0


def main() -> int:
    height = Z0 + len(KS) * BAND_H
    m = trimesh.creation.box(extents=[p.SIDE, p.SIDE, height])
    m.apply_translation([0, 0, height / 2])
    out = b.STL / "0.2" / "pa_extreme_K0-0.5_0.2.stl"
    m.export(out)
    gcodes = [(round(Z0 + i * BAND_H + 0.1, 4), f"M900 K{k:.3f} L1000 M10") for i, k in enumerate(KS)]
    over = b.base_over("0.2", wall_loops=2, bottom_shell_layers=4, top_shell_layers=0, sparse_infill_density="0%",
                       brim_type="no_brim", seam_position="back", outer_wall_speed=f"{p.SPEED:g}",
                       inner_wall_speed=f"{p.SPEED:g}")
    fil = dict(c.FIL_OVER, filament_flow_ratio="1.03", filament_max_volumetric_speed="2.5",
               slow_down_for_layer_cooling="0")
    pr = b.Project("0.2", "R6x_matte-purple_pa-extreme_0.2", [b.Obj(out, out.stem, over)], fil_over=fil, gcodes=gcodes)
    prof = b.Profiles(b.find_profile_dir(None), b.TAG)
    dest = b.OUT / "0.2" / f"{pr.out_name}.3mf"
    rep = b.build_project(prof, pr, b.TAG.lstrip("v"), dest)
    errs = b.validate(dest, rep)
    print(dest.name, "OK" if not errs else errs, f"height {height:.1f} mm")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
