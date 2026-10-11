"""R4 flow-ratio test plate (coarse pass) for the 0.2 mm nozzle, ELEGOO Matte PLA purple reference.

Reuses the nine numbered blocks of OrcaSlicer's own coarse flow-rate test (resources/calib/filament_flow/
flowrate-test-pass1.3mf, 40 x 30 x 2 mm for a 0.6 mm nozzle), scaled to 20 x 15 x 1.2 mm so a block is 12 layers
of 0.10 mm, and gives each block its own per-object flow ratio (print_flow_ratio, -20 % ... +20 % in 5 % steps).
The filament carries the reference settings so far: 190 C (R2), K = 0.10 (R3, provisional). First layer 210 C and a
2 mm brim: the first run (195 C, no brim) peeled -20, -15 and +10 off the plate.

Writes stl/0.2/flow_ratio_coarse/*.stl and 3mf/0.2/R4_matte-purple_flow-ratio-coarse_0.2.3mf.

Run:  .venv/Scripts/python -I tests-src/flow_ratio_coarse.py [path to flowrate-test-pass1.3mf]
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

SRC = Path("C:/Program Files/OrcaSlicer/resources/calib/filament_flow/flowrate-test-pass1.3mf")
PITCH = (26.0, 20.0)                  # block centres, mm (blocks are 20 x 15)
XY, Z = 0.5, 0.6                      # 40 x 30 x 2 mm -> 20 x 15 x 1.2 mm
DELTAS = {"m20": -20, "m15": -15, "m10": -10, "m5": -5, "0": 0, "5": 5, "10": 10, "15": 15, "20": 20}
FIL_OVER = {
    "nozzle_temperature": "190", "nozzle_temperature_initial_layer": "210",     # R2: 190 C; hotter first layer (195 C peeled)
    "textured_plate_temp": "60", "textured_plate_temp_initial_layer": "60",
    "filament_density": "1.26",
    "enable_pressure_advance": "1", "pressure_advance": "0.10",                  # R3: provisional K
}


def blocks(src: Path):
    t = zipfile.ZipFile(src).read("3D/3dmodel.model").decode()
    for m in re.finditer(r'<object id="\d+" name="flowrate_([^"]+)"(.*?)</object>', t, re.S):
        v = np.array(re.findall(r'<vertex x="([-\d.]+)" y="([-\d.]+)" z="([-\d.]+)"', m.group(2)), float)
        f = np.array(re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"', m.group(2)), int)
        yield m.group(1), v, f


def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else SRC
    out = b.STL / "0.2" / "flow_ratio_coarse"
    out.mkdir(parents=True, exist_ok=True)
    objs = []
    for key, v, f in sorted(blocks(src), key=lambda x: DELTAS[x[0]]):
        centre = (v.min(0) + v.max(0)) / 2
        v2 = v * np.array([XY, XY, Z])
        v2[:, 2] -= v2[:, 2].min()
        m = trimesh.Trimesh(v2, f, process=True)
        assert m.is_watertight and m.volume > 0, key
        stl = out / f"flowrate_{key}_0.2.stl"
        m.export(stl)
        col, row = round((centre[0] - 62.0) / 42.0), round((centre[1] - 47.0) / 32.0)   # source grid, 3 x 3
        at = (b.CX + col * PITCH[0], b.CY + row * PITCH[1])                             # wider: room for the brims
        d = DELTAS[key]
        over = b.base_over("0.2", wall_loops=3, top_shell_layers=4, bottom_shell_layers=1,
                           sparse_infill_density="35%", top_surface_pattern="monotonic",
                           brim_type="outer_only", brim_width="2", brim_object_gap="0", print_flow_ratio=f"{1 + d / 100:.2f}")
        objs.append(b.Obj(stl, f"flow {d:+d}%", over, at))
        print(f"  {stl.name}: {m.extents.round(2)} mm  flow x{1 + d / 100:.2f}")
    prof = b.Profiles(b.find_profile_dir(None), b.TAG)
    pr = b.Project("0.2", "R4_matte-purple_flow-ratio-coarse_0.2", objs, fil_over=FIL_OVER)
    dest = b.OUT / "0.2" / f"{pr.out_name}.3mf"
    rep = b.build_project(prof, pr, b.TAG.lstrip("v"), dest)
    errs = b.validate(dest, rep)
    print(dest.name, "OK" if not errs else errs)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
