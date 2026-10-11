"""R4 flow-ratio test plate, fine pass, 0.2 mm nozzle, ELEGOO Matte PLA purple reference.

Same recipe as flow_ratio_coarse.py but with OrcaSlicer's fine-pass blocks (flowrate-test-pass2.3mf, labels 0 ... -9).
The labels are relative: a block's real print_flow_ratio is 1 + (BASE + label) / 100 with BASE = coarse best + 4,
the shift used by Orca's own fine pass (docs/reference-offset-method.md). Coarse best was +5 %, so BASE = 9 and the
plate covers 0 ... +9 % in 1 % steps, label -4 being +5 %.

Run:  .venv/Scripts/python -I tests-src/flow_ratio_fine.py
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import trimesh

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_3mf as b  # noqa: E402
import flow_ratio_coarse as c  # noqa: E402

SRC = Path("C:/Program Files/OrcaSlicer/resources/calib/filament_flow/flowrate-test-pass2.3mf")
COARSE_BEST = 5
BASE = COARSE_BEST + 4


def main() -> int:
    out = b.STL / "0.2" / "flow_ratio_fine"
    out.mkdir(parents=True, exist_ok=True)
    objs = []
    for key, v, f in sorted(c.blocks(SRC), key=lambda x: -int(x[0].replace("m", "-"))):
        label = int(key.replace("m", "-"))
        centre = (v.min(0) + v.max(0)) / 2
        v2 = v * np.array([c.XY, c.XY, c.Z])
        v2[:, 2] -= v2[:, 2].min()
        m = trimesh.Trimesh(v2, f, process=True)
        assert m.is_watertight and m.volume > 0, key
        stl = out / f"flowrate_fine_{key}_0.2.stl"
        m.export(stl)
        col, row = round((centre[0] - 62.0) / 42.0), (centre[1] - 63.0) / 32.0       # 3 columns x 4 rows
        at = (b.CX + col * c.PITCH[0], b.CY + row * c.PITCH[1])
        pct = BASE + label
        over = b.base_over("0.2", wall_loops=3, top_shell_layers=4, bottom_shell_layers=1,
                           sparse_infill_density="35%", top_surface_pattern="monotonic",
                           brim_type="outer_only", brim_width="2", brim_object_gap="0",
                           print_flow_ratio=f"{1 + pct / 100:.2f}")
        objs.append(b.Obj(stl, f"label {label} = {pct:+d}%", over, at))
        print(f"  {stl.name}: label {label:+d} -> flow x{1 + pct / 100:.2f}  at {at[0]:.0f},{at[1]:.0f}")
    prof = b.Profiles(b.find_profile_dir(None), b.TAG)
    pr = b.Project("0.2", "R4b_matte-purple_flow-ratio-fine_0.2", objs, fil_over=c.FIL_OVER)
    dest = b.OUT / "0.2" / f"{pr.out_name}.3mf"
    rep = b.build_project(prof, pr, b.TAG.lstrip("v"), dest)
    errs = b.validate(dest, rep)
    print(dest.name, "OK" if not errs else errs)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
