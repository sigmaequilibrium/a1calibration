"""20 mm calibration cube STL generator (Bambu Lab A1).

Writes stl/0.4/cube_20mm_0.4.stl and stl/0.2/cube_20mm_0.2.stl. The geometry is the same
plain 20 x 20 x 20 mm cube for both nozzles (every dimension is a whole multiple of the
0.20 and 0.10 mm layer heights); the nozzle only changes the slicer settings.

Coordinates: mm, Z up, centred on the XY origin, sitting on z = 0.

Run:  .venv/Scripts/python -I tests-src/cube.py
"""

from __future__ import annotations

import os
import sys

import trimesh
from manifold3d import Manifold

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZE = 20.0


def main() -> int:
    m = Manifold.cube((SIZE, SIZE, SIZE), center=True).translate((0.0, 0.0, SIZE / 2))
    mesh = m.to_mesh()
    base = trimesh.Trimesh(vertices=mesh.vert_properties[:, :3], faces=mesh.tri_verts, process=True)
    bad = 0
    for nz in ("0.4", "0.2"):
        out = os.path.join(ROOT, "stl", nz)
        os.makedirs(out, exist_ok=True)
        path = os.path.join(out, f"cube_20mm_{nz}.stl")
        base.export(path)
        t = trimesh.load(path)
        ext = t.bounds[1] - t.bounds[0]
        ok = (t.is_watertight and t.is_winding_consistent and t.volume > 0
              and abs(t.bounds[0][2]) < 1e-9 and all(abs(e - SIZE) < 1e-6 for e in ext))
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {os.path.relpath(path, ROOT):40s} "
              f"{ext[0]:.1f} x {ext[1]:.1f} x {ext[2]:.1f} mm  volume {t.volume / 1000:.2f} cm3")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
