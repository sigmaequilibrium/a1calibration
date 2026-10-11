"""Dimensional & first-layer calibration STL generator (Bambu Lab A1).

Generates, for each nozzle (0.2 and 0.4 mm), into stl/<nozzle>/:
  dim01_first-layer-squares   3x3 single-layer squares spread across the bed
  dim02_xy-gauge              100 mm frame + 20 mm island: outer & inner spans in X and Y
  dim03_hole-peg-gauge        holes and pegs at nominal diameters
  dim04_fit-clearance         hole plate with a radial-clearance series + matching test pin
  dim05_elephant-foot         small ring with sharp bottom edges + reference chamfers

Coordinates: mm, Z up, front of printer = -Y, models centred on XY origin, z >= 0.
All geometry is built with manifold3d (guaranteed manifold booleans) and every
mesh is re-loaded from disk with trimesh and checked for watertightness.

Run:  .venv/Scripts/python -I tests-src/dimensional.py
"""

from __future__ import annotations

import math
import os
import sys

import numpy as np
import trimesh
from manifold3d import CrossSection, Manifold

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLA_DENSITY = 1.24  # g/cm^3, only for the printed mass estimate

# --------------------------------------------------------------------------
# Nozzle profiles
# --------------------------------------------------------------------------
NOZZLES = {
    "0.4": dict(
        tag="0.4n",
        lw=0.42,          # line width
        lh=0.20,          # layer height
        l0=0.20,          # initial layer height (A1 0.4 profiles)
        # 1 first-layer
        fl_square=25.0, fl_span=220.0, fl_digit_h=7.0, fl_digit_lines=3,
        # 2 xy gauge
        xy_big=100.0, xy_small=20.0, xy_wall_lines=5, xy_h=4.0,
        # labels (raised)
        txt_h=5.0, txt_lines=2, txt_raise=0.40,
        # 3 hole/peg gauge
        hp_diams=[2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0], hp_plate=3.0, hp_peg_h=6.0, hp_gap=4.0,
        # 4 fit/clearance
        fit_d=6.0, fit_clear=[0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        fit_plate=4.0, fit_gap=4.0, fit_pin_len=10.0, fit_flange=1.6, fit_flange_extra=6.0,
        # 5 elephant foot
        ef_size=20.0, ef_wall_lines=6, ef_h=6.0, ef_chamfers=(0.4, 0.8),
    ),
    "0.2": dict(
        tag="0.2n",
        lw=0.22,
        lh=0.10,
        l0=0.10,          # initial layer height (A1 0.2 profiles)
        fl_square=20.0, fl_span=220.0, fl_digit_h=6.0, fl_digit_lines=3,
        xy_big=100.0, xy_small=20.0, xy_wall_lines=8, xy_h=3.0,
        txt_h=3.5, txt_lines=2, txt_raise=0.30,
        hp_diams=[1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0], hp_plate=2.0, hp_peg_h=4.0, hp_gap=3.5,
        fit_d=3.0, fit_clear=[0.025, 0.05, 0.075, 0.10, 0.125, 0.15, 0.175, 0.20],
        fit_plate=3.0, fit_gap=3.5, fit_pin_len=6.0, fit_flange=1.0, fit_flange_extra=4.0,
        ef_size=15.0, ef_wall_lines=8, ef_h=4.0, ef_chamfers=(0.2, 0.4),
    ),
}

# --------------------------------------------------------------------------
# 2D helpers
# --------------------------------------------------------------------------


def poly(points) -> CrossSection:
    """CrossSection from one polygon, orientation-independent."""
    pts = np.asarray(points, dtype=float)
    x, y = pts[:, 0], pts[:, 1]
    area = 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)
    if area < 0:
        pts = pts[::-1]
    return CrossSection([pts])


def rect(x0, y0, x1, y1) -> CrossSection:
    return poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def bar(p0, p1, width) -> CrossSection:
    """Straight stroke of given width from p0 to p1 (square ends)."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = p1 - p0
    d /= np.linalg.norm(d)
    n = np.array([-d[1], d[0]]) * width / 2
    return poly([p0 - n, p1 - n, p1 + n, p0 + n])


def circle(d, segments=None) -> CrossSection:
    """Polygonal circle whose *mean* radius equals d/2 (vertices slightly outside,
    flats slightly inside), so the slicer sees the nominal diameter."""
    r = d / 2
    n = segments or max(96, int(math.ceil(2 * math.pi * r / 0.05)))  # ~0.05 mm chords
    rv = r * 2 / (1 + math.cos(math.pi / n))
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    return poly(np.c_[rv * np.cos(ang), rv * np.sin(ang)])


def union2d(parts) -> CrossSection:
    out = CrossSection()
    for p in parts:
        out = out + p
    return out


# --------------------------------------------------------------------------
# Segment font (7-segment digits + '.', plus X and Y)
# --------------------------------------------------------------------------
SEGS = {
    "0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc",
    "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcdfg",
}


def glyph(ch, h, s, stencil=0.0) -> tuple[CrossSection, float]:
    """Return (cross-section with lower-left at origin, advance width).
    stencil > 0 opens a stencil bridge of that width at the right-middle
    junction (middle bar shortened, right bars split) so no closed counters
    remain: cut-out digits then leave no loose islands inside 6, 8, 9."""
    w = 0.6 * h
    if ch in SEGS:
        st = stencil / 2
        r = {
            "a": rect(0, h - s, w, h), "d": rect(0, 0, w, s),
            "g": rect(0, (h - s) / 2, w - s - stencil if stencil else w, (h + s) / 2),
            "f": rect(0, h / 2, s, h), "e": rect(0, 0, s, h / 2),
            "b": rect(w - s, h / 2 + st, w, h), "c": rect(w - s, 0, w, h / 2 - st),
        }
        return union2d(r[k] for k in SEGS[ch]), w
    if ch == ".":
        return rect(0, 0, s, s), s
    if ch == "X":
        cs = bar((s / 2, s / 2), (w - s / 2, h - s / 2), s) + bar((s / 2, h - s / 2), (w - s / 2, s / 2), s)
        return cs ^ rect(0, 0, w, h), w
    if ch == "Y":
        cx, cy = w / 2, h * 0.45
        cs = (bar((s / 2, h), (cx, cy), s) + bar((w - s / 2, h), (cx, cy), s)
              + rect(cx - s / 2, 0, cx + s / 2, cy + s / 4))
        return cs ^ rect(0, 0, w, h), w
    raise ValueError(ch)


def text(s, h, stroke, cx=0.0, cy=0.0, stencil=0.0) -> CrossSection:
    """Text centred on (cx, cy)."""
    gap = max(1.5 * stroke, 0.22 * h)
    parts, x = [], 0.0
    for ch in s:
        g, adv = glyph(ch, h, stroke, stencil)
        parts.append(g.translate((x, 0)))
        x += adv + gap
    width = x - gap
    return union2d(parts).translate((cx - width / 2, cy - h / 2))


def text_width(s, h, stroke) -> float:
    return text(s, h, stroke).bounds()[2] - text(s, h, stroke).bounds()[0]


def ext(cs: CrossSection, z0, z1) -> Manifold:
    return cs.extrude(z1 - z0).translate((0, 0, z0))


def fmt(v):
    return ("%.2f" % v).rstrip("0").rstrip(".") if v != int(v) else str(int(v))


# --------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------


def first_layer(p):
    """3x3 single-layer squares across the bed, numbered 1..9 by cut-out digits
    (1 = back-left, reading order, 9 = front-right)."""
    a, span = p["fl_square"], p["fl_span"]
    c = (span - a) / 2
    dh, ds = p["fl_digit_h"], p["fl_digit_lines"] * p["lw"]
    parts = []
    k = 1
    for row, y in enumerate([c, 0.0, -c]):
        for col, x in enumerate([-c, 0.0, c]):
            sq = rect(x - a / 2, y - a / 2, x + a / 2, y + a / 2)
            # digit in the back-left corner of each square
            g = text(str(k), dh, ds, cx=x - a / 2 + 2.5 + 0.3 * dh, cy=y + a / 2 - 2.5 - dh / 2,
                     stencil=3 * p["lw"])
            parts.append(sq - g)
            k += 1
    return ext(union2d(parts), 0, p["l0"])


def xy_gauge(p):
    """Square frame (outer = big) with a square island (outer = small) in the
    centre. Gives, per axis: outer big, inner big, outer small, inner small.
    A low diagonal spoke ties the island to the frame (front-left corner) and
    low tabs carrying raised 'X' (front-right corner, +X end) and 'Y'
    (back-left corner, +Y end) keep the axis identity after removal."""
    lw, B, S, H = p["lw"], p["xy_big"], p["xy_small"], p["xy_h"]
    w = p["xy_wall_lines"] * lw
    b, s = B / 2, S / 2
    frame = rect(-b, -b, b, b) - rect(-b + w, -b + w, b - w, b - w)
    island = rect(-s, -s, s, s) - rect(-s + w, -s + w, s - w, s - w)
    body = ext(frame + island, 0, H)

    low_h = 5 * p["lh"] if p["lh"] >= 0.2 else 10 * p["lh"]  # 1.0 mm
    spoke = bar((-b + w - 0.5, -b + w - 0.5), (-s + 0.5, -s + 0.5), 3 * lw)
    tab = 10.0
    tab_x = rect(b - w - tab, -b + w - 0.01, b - w + 0.01, -b + w + tab)
    tab_y = rect(-b + w - 0.01, b - w - tab, -b + w + tab, b - w + 0.01)
    low = ext(spoke + tab_x + tab_y, 0, low_h)

    th, ts = 0.7 * tab, p["txt_lines"] * lw
    lx = text("X", th, ts, cx=b - w - tab / 2, cy=-b + w + tab / 2)
    ly = text("Y", th, ts, cx=-b + w + tab / 2, cy=b - w - tab / 2)
    labels = ext(lx + ly, low_h, low_h + p["txt_raise"])
    info = dict(wall=w, outer_big=B, inner_big=B - 2 * w, outer_small=S, inner_small=S - 2 * w)
    return body + low + labels, info


def hole_peg(p):
    """Plate: back row = through-holes, middle row = raised diameter labels,
    front row = pegs, one column per nominal diameter."""
    lw, diams, T = p["lw"], p["hp_diams"], p["hp_plate"]
    th, ts, gap = p["txt_h"], p["txt_lines"] * lw, p["hp_gap"]
    labels = [fmt(d) for d in diams]
    colw = [max(d, text_width(l, th, ts)) for d, l in zip(diams, labels)]
    xs, x = [], gap
    for cw in colw:
        xs.append(x + cw / 2)
        x += cw + gap
    width = x
    dmax = max(diams)
    y_peg = gap + dmax / 2
    y_lab = gap + dmax + 1.5 + th / 2
    y_hole = y_lab + th / 2 + 1.5 + dmax / 2
    depth = y_hole + dmax / 2 + gap
    ox, oy = width / 2, depth / 2  # centre
    plate = rect(0, 0, width, depth)
    holes = union2d(circle(d).translate((xc, y_hole)) for d, xc in zip(diams, xs))
    body = ext(plate - holes, 0, T)
    pegs = ext(union2d(circle(d).translate((xc, y_peg)) for d, xc in zip(diams, xs)), 0, T + p["hp_peg_h"])
    lab = ext(union2d(text(l, th, ts, cx=xc, cy=y_lab) for l, xc in zip(labels, xs)), T, T + p["txt_raise"])
    m = (body + pegs + lab).translate((-ox, -oy, 0))
    return m, dict(diameters=diams)


def fit_clearance(p):
    """Hole plate with holes D + 2*g (g = radial clearance per side), 2 rows of 4,
    labelled 1..8 (raised), plus a test pin of nominal D on a flange."""
    lw, D, T, gap = p["lw"], p["fit_d"], p["fit_plate"], p["fit_gap"]
    th, ts = p["txt_h"], p["txt_lines"] * lw
    clears = p["fit_clear"]
    hd = [D + 2 * g for g in clears]
    hmax = max(hd)
    lab_w = text_width("8", th, ts)
    cell_w = max(hmax, lab_w) + gap
    cell_h = hmax + 1.0 + th + gap
    ncol = 4
    nrow = math.ceil(len(clears) / ncol)
    width = ncol * cell_w + gap
    depth = nrow * cell_h + gap
    holes, labs = [], []
    for i, d in enumerate(hd):
        r, c = divmod(i, ncol)
        xc = gap + c * cell_w + cell_w / 2 - gap / 2
        yb = depth - gap - (r + 1) * cell_h + gap  # bottom of this cell
        y_lab = yb + th / 2
        y_hole = yb + th + 1.0 + hmax / 2
        holes.append(circle(d).translate((xc, y_hole)))
        labs.append(text(str(i + 1), th, ts, cx=xc, cy=y_lab))
    plate = ext(rect(0, 0, width, depth) - union2d(holes), 0, T)
    lab = ext(union2d(labs), T, T + p["txt_raise"])
    plate_m = (plate + lab).translate((-width / 2, -depth / 2, 0))

    # Test pin: flange + pin with a small 45 deg lead-in chamfer at the tip
    F, L = p["fit_flange"], p["fit_pin_len"]
    ch = 2 * p["lh"] if p["lh"] >= 0.2 else 3 * p["lh"]
    flange = ext(circle(D + p["fit_flange_extra"]), 0, F)
    pin = ext(circle(D), F - 0.01, F + L - ch)
    tip = Manifold.cylinder(ch, D / 2, D / 2 - ch, 256).translate((0, 0, F + L - ch))
    pin_m = (flange + pin + tip).translate((width / 2 + gap + (D + p["fit_flange_extra"]) / 2, 0, 0))
    m = (plate_m + pin_m).translate((-(gap + (D + p["fit_flange_extra"])) / 2, 0, 0))
    return m, dict(pin_d=D, clearances=clears, hole_diams=[round(h, 3) for h in hd])


def elephant_foot(p):
    """Square ring. Left/right outer faces and all inner faces have sharp 90 deg
    bottom edges (measure first-layer bulge). Front (-Y) bottom edge has a small
    45 deg chamfer, back (+Y) a larger one: visual reference."""
    lw, L, H = p["lw"], p["ef_size"], p["ef_h"]
    w = p["ef_wall_lines"] * lw
    h = L / 2
    ring = ext(rect(-h, -h, h, h) - rect(-h + w, -h + w, h - w, h - w), 0, H)
    c1, c2 = p["ef_chamfers"]

    def prism(y_face, c, sign):
        # triangle in YZ at the bottom edge of face y=y_face; sign=+1 for back face
        pts = []
        for x in (-h - 1, h + 1):
            pts += [(x, y_face + sign * 0.01, -0.01), (x, y_face - sign * c, -0.01), (x, y_face + sign * 0.01, c + 0.01)]
        # extend the corner beyond the face so the cut is clean
        pts2 = []
        for x in (-h - 1, h + 1):
            pts2 += [(x, y_face + sign * 1.0, -0.01), (x, y_face + sign * 1.0, c + 1.0 + 0.01)]
        return Manifold.hull_points(np.array(pts + pts2))

    m = ring - prism(-h, c1, -1) - prism(h, c2, +1)
    return m, dict(size=L, wall=w, inner=L - 2 * w, chamfer_front=c1, chamfer_back=c2)


# --------------------------------------------------------------------------
# Output & validation
# --------------------------------------------------------------------------


def to_trimesh(m: Manifold) -> trimesh.Trimesh:
    mesh = m.to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3]
    f = np.asarray(mesh.tri_verts)
    return trimesh.Trimesh(vertices=v, faces=f, process=True)


def save(m: Manifold, path: str, info=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    t = to_trimesh(m)
    t.export(path)
    r = trimesh.load(path, force="mesh")  # validate what is actually on disk
    ok = bool(r.is_watertight and r.is_winding_consistent and r.volume > 0)
    ext_ = r.extents
    bodies = len(m.decompose())
    zmin = r.bounds[0][2]
    print(f"{'OK ' if ok else 'BAD'} {os.path.relpath(path, ROOT):55s} "
          f"{ext_[0]:7.2f} x {ext_[1]:7.2f} x {ext_[2]:6.2f} mm  "
          f"vol {r.volume / 1000:7.3f} cm3 (~{r.volume / 1000 * PLA_DENSITY:5.2f} g PLA)  "
          f"bodies {bodies}  zmin {zmin:+.3f}")
    if info:
        print("     " + ", ".join(f"{k}={v}" for k, v in info.items()))
    if not ok or abs(zmin) > 1e-6:
        raise SystemExit(f"validation failed: {path}")
    return r


def main():
    for nz, p in NOZZLES.items():
        out = os.path.join(ROOT, "stl", nz)
        tag = p["tag"]
        print(f"\n=== nozzle {nz} mm  (line {p['lw']}, layer {p['lh']}, first layer {p['l0']}) ===")
        save(first_layer(p), os.path.join(out, f"dim01_first-layer-squares_{tag}_h{p['l0']:.2f}.stl"),
             dict(square=p["fl_square"], span=p["fl_span"], thickness=p["l0"]))
        m, info = xy_gauge(p)
        save(m, os.path.join(out, f"dim02_xy-gauge-100-20_{tag}.stl"), info)
        m, info = hole_peg(p)
        save(m, os.path.join(out, f"dim03_hole-peg-gauge_{tag}.stl"), info)
        m, info = fit_clearance(p)
        save(m, os.path.join(out, f"dim04_fit-clearance-D{fmt(p['fit_d'])}_{tag}.stl"), info)
        m, info = elephant_foot(p)
        save(m, os.path.join(out, f"dim05_elephant-foot_{tag}.stl"), info)
    print("\nall meshes watertight, positive volume, sitting on z=0")


if __name__ == "__main__":
    sys.exit(main())
