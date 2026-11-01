"""Generate overhang, bridge, fine-detail and verification test STLs
for a Bambu Lab A1 with 0.2 mm and 0.4 mm nozzles.

Run from the project root:
    .venv/Scripts/python -I tests-src/overhang_bridge_detail.py

Outputs (per nozzle N in {0.2, 0.4}):
    stl/N/overhang_angles_N.stl   overhang fins 20-75 deg (from vertical), 5 deg steps
    stl/N/bridge_spans_N.stl      bridges of increasing span
    stl/N/min_feature_N.stl       thin walls, pins, holes, gaps scaled to line width
    stl/N/verify_combo_N.stl      quick profile sanity check

Conventions: Z up, part sits on Z=0, the "front" of every part is -Y.
All labels are engraved into top faces with a 7-segment font made from boxes.
"""

import math
import sys
from pathlib import Path

import numpy as np
import trimesh
from manifold3d import Manifold, OpType

ROOT = Path(__file__).resolve().parent.parent
BED = 256.0
SEG = 64  # circle segments

# ---------------------------------------------------------------- primitives


def box(x0, y0, z0, x1, y1, z1):
    return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])


def cyl_z(cx, cy, z0, z1, d, seg=SEG):
    return Manifold.cylinder(z1 - z0, d / 2.0, d / 2.0, seg).translate([cx, cy, z0])


def cyl_x(x0, x1, cy, cz, d, seg=SEG):
    # cylinder along +X from x0 to x1
    c = Manifold.cylinder(x1 - x0, d / 2.0, d / 2.0, seg)
    return c.rotate([0, 90, 0]).translate([x0, cy, cz])


def union(parts):
    parts = [p for p in parts if p is not None]
    return Manifold.batch_boolean(parts, OpType.Add)


# ---------------------------------------------------------------- 7-seg font

DIGITS = {
    "0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc",
    "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcdfg",
}


class Font:
    def __init__(self, h, w, stroke, depth, space):
        self.h, self.w, self.s, self.depth, self.space = h, w, stroke, depth, space

    def char_w(self, ch):
        return self.s if ch == "." else self.w

    def text_w(self, txt):
        return sum(self.char_w(c) for c in txt) + self.space * (len(txt) - 1)

    def _segs(self, ch, x):
        h, w, s = self.h, self.w, self.s
        if ch == ".":
            return [(x, 0, x + s, s)]
        r = []
        for seg in DIGITS[ch]:
            if seg == "a":
                r.append((x, h - s, x + w, h))
            elif seg == "g":
                r.append((x, h / 2 - s / 2, x + w, h / 2 + s / 2))
            elif seg == "d":
                r.append((x, 0, x + w, s))
            elif seg == "f":
                r.append((x, h / 2 - s / 2, x + s, h))
            elif seg == "e":
                r.append((x, 0, x + s, h / 2 + s / 2))
            elif seg == "b":
                r.append((x + w - s, h / 2 - s / 2, x + w, h))
            elif seg == "c":
                r.append((x + w - s, 0, x + w, h / 2 + s / 2))
        return r

    def engrave_cutter(self, txt, cx, cy, ztop):
        """Cutter solid for text centred at (cx, cy), cut `depth` down from ztop."""
        x = cx - self.text_w(txt) / 2.0
        y0 = cy - self.h / 2.0
        boxes = []
        for ch in txt:
            for (a, b, c, d) in self._segs(ch, x):
                boxes.append(box(a, y0 + b, ztop - self.depth, c, y0 + d, ztop + 1.0))
            x += self.char_w(ch) + self.space
        return union(boxes)


def fmt_mm(v):
    """0.5 -> '.5', 1.0 -> '1', 1.5 -> '1.5', 0.05 -> '.05'"""
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    if s.startswith("0."):
        s = s[1:]
    return s


# ---------------------------------------------------------------- nozzle presets

NOZ = {
    "0.4": dict(
        nozzle=0.4, lw=0.42, layer=0.20,
        label_font=Font(h=5.0, w=3.0, stroke=0.8, depth=0.6, space=0.8),
        small_font=Font(h=3.6, w=2.4, stroke=0.7, depth=0.4, space=0.45),
        # overhang
        oh=dict(w=8.0, gap=2.0, t=3.0, R=10.0, Hmax=12.0, base=2.0, clear=2.0, strip_pad=1.5),
        # bridge
        br=dict(spans=[5, 10, 20, 30, 40, 50], pw=4.0, D=8.0, Hb=8.0, slab=1.0,
                gap=3.0, base=1.6, strip_pad=1.5),
        # fine detail
        fd=dict(pitch=7.5, base=1.6, margin=3.0, feat_h=6.0, wall_len=8.0,
                wall_mult=[0.5, 0.75, 1, 1.5, 2, 3, 4],
                pins=[0.5, 0.8, 1.0, 1.5, 2.0, 3.0],
                holes=[0.5, 0.8, 1.0, 1.5, 2.0, 3.0],
                gaps=[0.1, 0.2, 0.3, 0.4, 0.6, 0.8],
                block_h=3.0, block_d=6.0, row_gap=2.0),
        vf_scale=1.0,
    ),
    "0.2": dict(
        nozzle=0.2, lw=0.22, layer=0.10,
        label_font=Font(h=3.2, w=2.0, stroke=0.45, depth=0.3, space=0.5),
        small_font=Font(h=2.4, w=1.5, stroke=0.36, depth=0.3, space=0.3),
        oh=dict(w=5.0, gap=1.5, t=2.5, R=7.0, Hmax=9.0, base=1.2, clear=1.5, strip_pad=1.0),
        br=dict(spans=[3, 5, 8, 12, 16, 20], pw=2.5, D=5.0, Hb=5.0, slab=0.6,
                gap=2.0, base=1.0, strip_pad=1.0),
        fd=dict(pitch=4.5, base=1.0, margin=2.0, feat_h=4.0, wall_len=5.0,
                wall_mult=[0.5, 0.75, 1, 1.5, 2, 3, 4],
                pins=[0.3, 0.5, 0.8, 1.0, 1.5, 2.0],
                holes=[0.3, 0.5, 0.8, 1.0, 1.5, 2.0],
                gaps=[0.05, 0.1, 0.15, 0.2, 0.3, 0.4],
                block_h=2.0, block_d=4.0, row_gap=1.2),
        vf_scale=0.6,
    ),
}


# ---------------------------------------------------------------- 1. overhang


def make_overhang(cfg):
    p = cfg["oh"]
    f = cfg["label_font"]
    angles = list(range(20, 80, 5))
    w, gap, t, R, Hmax = p["w"], p["gap"], p["t"], p["R"], p["Hmax"]
    zb = p["base"]
    ztop = zb + p["clear"] + Hmax
    pitch = w + gap
    strip = f.h + 2 * p["strip_pad"]
    x_start = pitch  # first pitch slot reserved for nozzle marker
    n = len(angles)
    total_x = x_start + n * pitch
    parts = [box(0, -strip, 0, total_x, 0.5, zb)]
    info = []
    for i, a in enumerate(angles):
        x0 = x_start + i * pitch + gap / 2
        x1 = x0 + w
        tan = math.tan(math.radians(a))
        H = min(Hmax, R / tan)
        reach = H * tan
        z0 = ztop - H
        parts.append(box(x0, 0, 0, x1, t, ztop))  # column
        pts = []
        for x in (x0, x1):
            pts += [[x, 0, z0], [x, t, z0], [x, t + reach, ztop], [x, 0, ztop]]
        parts.append(Manifold.hull_points(np.array(pts)))
        info.append((a, round(H, 2), round(reach, 2)))
    body = union(parts)
    cutters = [f.engrave_cutter(cfg_label(cfg), pitch / 2, -strip / 2, zb)]
    for i, a in enumerate(angles):
        cx = x_start + i * pitch + pitch / 2
        cutters.append(f.engrave_cutter(str(a), cx, -strip / 2, zb))
    body = body - union(cutters)
    return body, info


def cfg_label(cfg):
    return "." + str(cfg["nozzle"]).split(".")[1]


# ---------------------------------------------------------------- 2. bridge


def make_bridge(cfg):
    p = cfg["br"]
    f = cfg["label_font"]
    pw, D, Hb, slab, gap = p["pw"], p["D"], p["Hb"], p["slab"], p["gap"]
    zb = p["base"]
    strip = f.h + 2 * p["strip_pad"]
    marker_w = f.text_w(cfg_label(cfg)) + 2 * gap
    parts, centers = [], []
    x = marker_w
    for s in p["spans"]:
        a0, a1 = x, x + pw
        b0, b1 = x + pw + s, x + 2 * pw + s
        parts.append(box(a0, 0, 0, a1, D, Hb + slab))
        parts.append(box(b0, 0, 0, b1, D, Hb + slab))
        parts.append(box(a0, 0, Hb, b1, D, Hb + slab))  # bridge slab
        centers.append((x + pw + s / 2.0, s))
        x = b1 + gap
    total_x = x - gap
    parts.append(box(0, -strip, 0, total_x, 0.5, zb))
    body = union(parts)
    cut = [f.engrave_cutter(cfg_label(cfg), marker_w / 2, -strip / 2, zb)]
    for cx, s in centers:
        cut.append(f.engrave_cutter(str(s), cx, -strip / 2, zb))
    return body - union(cut)


# ---------------------------------------------------------------- 3. fine detail


def make_detail(cfg):
    p = cfg["fd"]
    f = cfg["small_font"]
    lw = cfg["lw"]
    P, zb, m = p["pitch"], p["base"], p["margin"]
    ncol = max(len(p["wall_mult"]), len(p["pins"]), len(p["holes"]), len(p["gaps"]) + 1)
    # one extra column at the left for row-type marker / nozzle marker
    width = (ncol + 1) * P + 2 * m
    lab_h = f.h + 1.0
    feats, cuts, holes = [], [], []
    y = m
    rows = []

    def col_x(i):
        return m + (i + 1) * P + P / 2

    # Row 1: thin walls (labels = multiple of line width)
    rows.append(("walls", y))
    fy0 = y + lab_h + 0.8
    for i, k in enumerate(p["wall_mult"]):
        t = k * lw
        cx = col_x(i)
        feats.append(box(cx - t / 2, fy0, zb - 0.01, cx + t / 2, fy0 + p["wall_len"], zb + p["feat_h"]))
        cuts.append(f.engrave_cutter(fmt_mm(k), cx, y + f.h / 2, zb))
    y = fy0 + p["wall_len"] + p["row_gap"]

    # Row 2: pins (labels = diameter mm)
    rows.append(("pins", y))
    fy0 = y + lab_h + 0.8
    dmax = max(p["pins"])
    for i, d in enumerate(p["pins"]):
        cx = col_x(i)
        feats.append(cyl_z(cx, fy0 + dmax / 2, zb - 0.01, zb + p["feat_h"], d))
        cuts.append(f.engrave_cutter(fmt_mm(d), cx, y + f.h / 2, zb))
    y = fy0 + dmax + p["row_gap"]

    # Row 3: vertical through-holes in a block (labels = diameter mm)
    rows.append(("holes", y))
    fy0 = y + lab_h + 0.8
    bx0, bx1 = col_x(0) - P / 2, col_x(len(p["holes"]) - 1) + P / 2
    feats.append(box(bx0, fy0, zb - 0.01, bx1, fy0 + p["block_d"], zb + p["block_h"]))
    for i, d in enumerate(p["holes"]):
        cx = col_x(i)
        holes.append(cyl_z(cx, fy0 + p["block_d"] / 2, -1, zb + p["block_h"] + 1, d))
        cuts.append(f.engrave_cutter(fmt_mm(d), cx, y + f.h / 2, zb))
    y = fy0 + p["block_d"] + p["row_gap"]

    # Row 4: gaps (slots) through a comb block, not through the base (labels = gap mm)
    rows.append(("gaps", y))
    fy0 = y + lab_h + 0.8
    ng = len(p["gaps"])
    gx = [col_x(i) for i in range(ng)]
    bx0, bx1 = gx[0] - P / 2, gx[-1] + P / 2
    feats.append(box(bx0, fy0, zb - 0.01, bx1, fy0 + p["block_d"], zb + p["block_h"]))
    for cx, g in zip(gx, p["gaps"]):
        holes.append(box(cx - g / 2, fy0 - 1, zb, cx + g / 2, fy0 + p["block_d"] + 1, zb + p["block_h"] + 1))
        cuts.append(f.engrave_cutter(fmt_mm(g), cx, y + f.h / 2, zb))
    y = fy0 + p["block_d"] + m

    depth = y
    base = box(0, 0, 0, width, depth, zb)
    # nozzle marker in left column, middle of plate
    cuts.append(f.engrave_cutter(cfg_label(cfg), m + P / 2, depth / 2, zb))
    body = union([base] + feats)
    body = body - union(holes)
    body = body - union(cuts)
    return body


# ---------------------------------------------------------------- 4. verification


def make_verify(cfg):
    s = cfg["vf_scale"]
    f = cfg["small_font"]
    S = lambda v: v * s  # noqa: E731
    # Base thickness must be a whole number of layers (0.6 x 1.2 = 0.72 was off-grid
    # on the 0.2 part, which left the slicer to round the base and the label depth).
    zb = round(S(1.2) / cfg["layer"]) * cfg["layer"]
    parts, cuts = [], []
    # base plate (front strip y<0 carries the nozzle label)
    parts.append(box(0, S(-6), 0, S(56), S(26), zb))
    # main block: top surface, sharp corners (PA), holes
    bx0, by0, bx1, by1, bz = S(3), S(3), S(23), S(23), S(10)
    parts.append(box(bx0, by0, 0, bx1, by1, bz))
    # overhang wedges off the back face (+Y): 45 deg and 60 deg from vertical
    R = S(6)
    for (x0, x1, a) in ((S(3), S(12), 45), (S(14), S(23), 60)):
        tan = math.tan(math.radians(a))
        H = min(bz - S(4), R / tan)
        reach = H * tan
        z0 = bz - H
        pts = []
        for x in (x0, x1):
            pts += [[x, by1 - 1, z0], [x, by1, z0], [x, by1 + reach, bz], [x, by1 - 1, bz]]
        parts.append(Manifold.hull_points(np.array(pts)))
    # bridge: pillars + slab, span 20 (x 30..50)
    pw, span, D, Hb, sl = S(4), S(20), S(8), S(8), S(1.0)
    px0 = S(26)
    parts.append(box(px0, S(3), 0, px0 + pw, S(3) + D, Hb + sl))
    parts.append(box(px0 + pw + span, S(3), 0, px0 + 2 * pw + span, S(3) + D, Hb + sl))
    parts.append(box(px0, S(3), Hb, px0 + 2 * pw + span, S(3) + D, Hb + sl))
    # cylinder for seam / Z-banding
    parts.append(cyl_z(S(40), S(19), 0, S(20), S(10), seg=128))
    body = union(parts)
    holes = [
        cyl_z(S(7.5), S(18), -1, bz + 1, S(3)),
        cyl_z(S(18), S(18), -1, bz + 1, S(5)),
        cyl_x(bx0 - 1, bx1 + 1, S(8), S(5.5), S(4)),
    ]
    body = body - union(holes)
    cuts.append(f.engrave_cutter(cfg_label(cfg), S(8), S(-3), zb))
    body = body - union(cuts)
    return body


# ---------------------------------------------------------------- export / validate


def to_trimesh(man):
    mesh = man.to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3]
    fcs = np.asarray(mesh.tri_verts)
    tm = trimesh.Trimesh(vertices=v, faces=fcs, process=True)
    tm.apply_translation(-tm.bounds[0])  # min corner at origin, on the bed
    return tm


def export(man, path):
    nbodies = len(man.decompose())
    tm = to_trimesh(man)
    path.parent.mkdir(parents=True, exist_ok=True)
    tm.export(path)
    chk = trimesh.load(path, force="mesh")
    ext = chk.extents
    ok = (chk.is_watertight and chk.is_winding_consistent and chk.volume > 0
          and all(e <= BED for e in ext) and abs(chk.bounds[0][2]) < 1e-6
          and nbodies == 1)
    print(f"{'OK ' if ok else 'BAD'} {path.relative_to(ROOT)}  "
          f"{ext[0]:.2f} x {ext[1]:.2f} x {ext[2]:.2f} mm  vol {chk.volume / 1000:.2f} cm3  "
          f"watertight={chk.is_watertight} bodies={nbodies}")
    return ok


def main():
    all_ok = True
    for name, cfg in NOZ.items():
        out = ROOT / "stl" / name
        oh, info = make_overhang(cfg)
        all_ok &= export(oh, out / f"overhang_angles_{name}.stl")
        print("     angle / overhang height / horizontal reach (mm):",
              ", ".join(f"{a}:{h}/{r}" for a, h, r in info))
        all_ok &= export(make_bridge(cfg), out / f"bridge_spans_{name}.stl")
        all_ok &= export(make_detail(cfg), out / f"min_feature_{name}.stl")
        all_ok &= export(make_verify(cfg), out / f"verify_combo_{name}.stl")
    print("ALL OK" if all_ok else "VALIDATION FAILED")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
