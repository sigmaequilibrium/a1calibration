"""R10 fit/clearance plate (dim04) for the 0.2 mm nozzle with the ELEGOO Matte PLA purple reference values so far:
190 C (first layer 210 C), flow ratio 1.03 (R4 coarse best +5 % on 0.98), K 0.10 (R3 provisional). One plate, no brim.

Writes 3mf/0.2/R10_matte-purple_dim04_fit-clearance-D3_0.2n.3mf

Run:  .venv/Scripts/python -I tests-src/r10_dim04_purple.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_3mf as b  # noqa: E402
import flow_ratio_coarse as c  # noqa: E402

FIL_OVER = dict(c.FIL_OVER, filament_flow_ratio="1.03")


def main() -> int:
    stl = b.STL / "0.2" / "dim04_fit-clearance-D3_0.2n.stl"
    over = b.base_over("0.2", wall_loops=4, sparse_infill_density="15%", brim_type="no_brim")
    pr = b.Project("0.2", "R10_matte-purple_dim04_fit-clearance-D3_0.2n", [b.Obj(stl, stl.stem, over)], fil_over=FIL_OVER)
    prof = b.Profiles(b.find_profile_dir(None), b.TAG)
    dest = b.OUT / "0.2" / f"{pr.out_name}.3mf"
    rep = b.build_project(prof, pr, b.TAG.lstrip("v"), dest)
    errs = b.validate(dest, rep)
    print(dest.name, "OK" if not errs else errs)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
