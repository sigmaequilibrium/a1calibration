"""Independent QA of every STL under stl/ (Bambu Lab A1, 256 x 256 x 256 mm bed).

Run from the project root:
    .venv/Scripts/python -I tests-src/qa_check.py

Generic checks (every file):
  - watertight, consistent winding, positive volume, manifold (loads into manifold3d)
  - number of separate bodies (1, except dim01 = 9 squares and dim04 = plate + pin)
  - fits the bed with a 5 mm margin on every side (XY <= 246 mm) and Z <= 256 mm
  - base on z = 0
  - every horizontal face sits on the layer grid of its nozzle (0.20 / 0.10 mm)
  - placement note: footprint, when centred on the plate (128, 128), against the two
    on-plate areas the A1 start/timelapse G-code uses (front-edge extrusion-test lines
    and the back-right head-wrap detection zone)

Spot checks against the claims in docs/*.md (measured on the mesh, not taken from
the generators):
  - temp towers: block count, block heights, M104 insert heights and temperatures in
    docs/tests-temp-stringing.md; the bridge deck closes each block and the window is
    open below it; 45 / 60 deg wedges
  - overhang fins: the set of overhang angles (20..75 deg, from vertical)
  - bridge spans: clear gaps between pillar pairs
  - min-feature: thin-wall widths = multiples of line width, pin diameters, holes
  - dim02 / dim05: wall thickness = N x line width, outer sizes
  - dim03 / dim04: hole and peg diameters
  - dim01: thickness = one first layer, square size
  - verify_combo: vertical hole diameters

Exit code 0 if everything passes, 1 otherwise.
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import numpy as np
import trimesh
from manifold3d import CrossSection, Manifold, Mesh

ROOT = Path(__file__).resolve().parent.parent
BED = 256.0
MARGIN = 5.0
LAYER = {"0.4": 0.20, "0.2": 0.10}
LW = {"0.4": 0.42, "0.2": 0.22}
TOL = 0.01          # mm, geometric tolerance for spot checks (float32 mesh + polygon facets)
PLA_DENSITY = 1.24

# A1 plate areas touched by the stock G-code (BambuStudio master, 2026-10):
#  - start G-code "extrude cali test" lines at Y = -0.5 and Y = 1.0, X 108..158, and the
#    "remove waste by touching" at X 108..148, Y -0.5 (front edge, centre)
#  - head_wrap_detect_zone 226x224 .. 256x256 (machine profile). Objects there make the
#    timelapse G-code skip the G39.3 head-wrap check; it is not a collision.
FRONT_STRIP = (104.0, 0.0, 162.0, 3.0)
HEAD_WRAP = (226.0, 224.0, 256.0, 256.0)

EXPECTED_BODIES = {"dim01_": 9, "dim04_": 2}

results: list[tuple[str, str, str]] = []   # (file, level, message)


def log(f, level, msg):
    results.append((f, level, msg))


# --------------------------------------------------------------------------- helpers
def to_manifold(t: trimesh.Trimesh) -> Manifold:
    return Manifold(Mesh(vert_properties=np.asarray(t.vertices, np.float32),
                         tri_verts=np.asarray(t.faces, np.uint32)))


def strip_x(y, half=0.01, span=600.0):
    return CrossSection.square((span, 2 * half)).translate((-span / 2, y - half))


def strip_y(x, half=0.01, span=600.0):
    return CrossSection.square((2 * half, span)).translate((x - half, -span / 2))


def pieces(cs: CrossSection):
    return [(p.bounds(), p.area()) for p in cs.decompose()]


def holes_of(cs: CrossSection):
    """Inner openings of a section: complement inside the bounding box, minus the
    pieces that touch the bounding box (outside region)."""
    x0, y0, x1, y1 = cs.bounds()
    box = CrossSection.square((x1 - x0 + 2, y1 - y0 + 2)).translate((x0 - 1, y0 - 1))
    out = []
    for p in (box - cs).decompose():
        b = p.bounds()
        if b[0] <= x0 - 0.5 or b[1] <= y0 - 0.5 or b[2] >= x1 + 0.5 or b[3] >= y1 + 0.5:
            continue
        out.append((b, p.area()))
    return out


def eq_diam(area):
    return 2.0 * math.sqrt(area / math.pi)


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def nozzle_of(path: Path) -> str:
    return path.parent.name


def check_list(f, what, measured, expected, tol=TOL):
    measured = sorted(measured)
    expected = sorted(expected)
    ok = len(measured) == len(expected) and all(close(m, e, tol) for m, e in zip(measured, expected))
    log(f, "PASS" if ok else "FAIL",
        f"{what}: measured {', '.join(f'{v:.3f}' for v in measured)}"
        + ("" if ok else f"  expected {', '.join(f'{v:.3f}' for v in expected)}"))
    return ok


# --------------------------------------------------------------------------- generic
def generic(path: Path, t: trimesh.Trimesh, m: Manifold):
    f = path.relative_to(ROOT).as_posix()
    nz = nozzle_of(path)
    lh = LAYER[nz]
    ext = t.extents
    bodies = len(m.decompose())
    exp_bodies = next((n for k, n in EXPECTED_BODIES.items() if path.name.startswith(k)), 1)
    problems = []
    if m.status().name != "NoError":
        problems.append(f"manifold status {m.status()}")
    if not t.is_watertight:
        problems.append("not watertight")
    if not t.is_winding_consistent:
        problems.append("inconsistent winding")
    if t.volume <= 0:
        problems.append(f"volume {t.volume:.3f}")
    if bodies != exp_bodies:
        problems.append(f"{bodies} bodies (expected {exp_bodies})")
    if ext[0] > BED - 2 * MARGIN or ext[1] > BED - 2 * MARGIN:
        problems.append(f"XY {ext[0]:.1f} x {ext[1]:.1f} exceeds {BED - 2 * MARGIN:.0f} (5 mm margin)")
    if ext[2] > BED:
        problems.append(f"Z {ext[2]:.1f} exceeds {BED}")
    if abs(t.bounds[0][2]) > 1e-4:
        problems.append(f"z min {t.bounds[0][2]:+.4f} (not on bed)")
    # horizontal faces on the layer grid
    n = t.face_normals
    horiz = np.abs(n[:, 2]) > 0.9999
    zs = np.unique(np.round(t.triangles_center[horiz, 2], 4))
    off = [z for z in zs if abs(z / lh - round(z / lh)) > 1e-3]
    if off:
        problems.append(f"horizontal faces off the {lh} mm layer grid at z = "
                        + ", ".join(f"{z:.3f}" for z in off[:8]))
    mass = t.volume / 1000 * PLA_DENSITY
    summary = (f"{ext[0]:7.2f} x {ext[1]:6.2f} x {ext[2]:6.2f} mm  vol {t.volume / 1000:6.2f} cm3"
               f" (~{mass:5.1f} g PLA)  bodies {bodies}")
    log(f, "FAIL" if problems else "PASS", summary + ("" if not problems else "  <- " + "; ".join(problems)))

    # placement when centred on the plate (Bambu Studio's default for one imported object)
    x0, y0 = 128 - ext[0] / 2, 128 - ext[1] / 2
    x1, y1 = 128 + ext[0] / 2, 128 + ext[1] / 2

    def hits(z):
        return x0 < z[2] and x1 > z[0] and y0 < z[3] and y1 > z[1]
    notes = []
    if hits(FRONT_STRIP):
        notes.append("overlaps the front-edge extrusion-test lines when centred")
    if hits(HEAD_WRAP):
        notes.append("reaches the back-right head-wrap detection zone when centred "
                     "(harmless: the head-wrap check is skipped for that print)")
    if notes:
        log(f, "NOTE", "; ".join(notes))
    return ext


# --------------------------------------------------------------------------- temp towers
def parse_tower_table(doc: str, fname: str):
    m = re.search(r"^####[^\n]*`" + re.escape(fname) + "`", doc, re.M)
    if not m:
        return None
    i = m.start()
    rows = []
    for line in doc[i:].splitlines()[1:]:
        if line.startswith("####") or line.startswith("## "):
            break
        mm = re.match(r"\|\s*(\d+)\s*\|\s*([\d.]+)\s*–\s*([\d.]+)\s*\|\s*(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|", line)
        if mm:
            k, z0, z1, t, ins, g = mm.groups()
            ins = ins.strip()
            ins_z = float(ins) if re.fullmatch(r"[\d.]+", ins) else None
            gm = re.search(r"M104 S(\d+)", g)
            rows.append((int(k), float(z0), float(z1), int(t), ins_z, int(gm.group(1)) if gm else None))
    return rows


def check_tower(path, t, m, doc):
    f = path.relative_to(ROOT).as_posix()
    nz = nozzle_of(path)
    lh = LAYER[nz]
    hot, cold = map(int, re.match(r"temp_tower_(?:compact_)?(\d+)-(\d+)_", path.name).groups())
    compact = path.name.startswith("temp_tower_compact_")
    if compact:   # no doc table: the table is computed by tests-src/temp_tower_compact.py (used by build_3mf.py)
        sys.path.insert(0, str(ROOT / "tests-src"))
        import temp_tower_compact as tc
        rows = [(k, z0, z1, temp, ins, None if ins is None else temp)
                for k, z0, z1, temp, ins in tc.tower_table_compact(hot, cold)]
    else:
        rows = parse_tower_table(doc, path.name)
    if not rows:
        log(f, "FAIL", "no height table for this file in docs/tests-temp-stringing.md")
        return
    nblk = (hot - cold) // 5 + 1
    problems = []
    if len(rows) != nblk:
        problems.append(f"doc has {len(rows)} rows, range needs {nblk}")
    for i, (k, z0, z1, temp, ins, g) in enumerate(rows):
        if temp != hot - 5 * i:
            problems.append(f"block {k} temp {temp} != {hot - 5 * i}")
        if i == 0:
            if ins is not None or g is not None:
                problems.append("block 1 must use the preset temperature")
        else:
            if ins is None or not close(ins, z0 + lh, 1e-6):
                problems.append(f"block {k} insert {ins} != {z0 + lh:.2f}")
            if g != temp:
                problems.append(f"block {k} M104 S{g} != {temp}")
            if not close(z0, rows[i - 1][2], 1e-6):
                problems.append(f"block {k} does not start where block {k - 1} ends")
        if abs(z0 / lh - round(z0 / lh)) > 1e-6:
            problems.append(f"block {k} bottom {z0} not on layer grid")
    if not close(t.extents[2], rows[-1][2], 1e-3):
        problems.append(f"mesh height {t.extents[2]:.3f} != table top {rows[-1][2]:.2f}")

    # geometry: window centre is open mid-block, closed by the deck at the block top
    sys.path.insert(0, str(ROOT / "tests-src"))
    import temp_stringing as ts  # tower dimensions only (deck thickness, window position)
    p = tc.COMPACT_02 if compact else ts.TOWER[nz]
    gx_min = -p.ho45 - p.margin
    gx_max = p.Wc + p.Lb + p.Wp + p.ho60 * math.tan(math.radians(60)) + p.margin
    xc = (p.Wc + p.Lb / 2) - (gx_min + gx_max) / 2
    for k, z0, z1, *_ in rows:
        mid = m.slice(z0 + 0.6 * p.H) ^ strip_y(xc)
        deck = m.slice(z1 - lh / 2) ^ strip_y(xc)
        if mid.area() > 1e-6:
            problems.append(f"block {k}: window not open at z={z0 + 0.6 * p.H:.2f}")
        if deck.area() < 1e-6:
            problems.append(f"block {k}: no bridge deck at z={z1 - lh / 2:.2f}")
        else:
            dz = deck.bounds()
            if not close(dz[3] - dz[1], p.D, 0.02):
                problems.append(f"block {k}: deck depth {dz[3] - dz[1]:.2f} != {p.D}")
    # overhang wedge angles (from vertical): faces pointing down and sideways in X
    n = t.face_normals
    down = (n[:, 2] < -0.05) & (n[:, 2] > -0.99) & (np.abs(n[:, 1]) < 1e-3)
    ang = sorted(set(float(a) for a in np.round(np.degrees(np.arcsin(-n[down, 2])), 1)))
    if ang != [45.0, 60.0]:
        problems.append(f"wedge angles {ang} != [45, 60]")
    log(f, "FAIL" if problems else "PASS",
        f"tower {hot}->{cold}: {len(rows)} blocks match the {'computed' if compact else 'doc'} table (heights, M104 S/Z), "
        f"decks close every block, wedges 45/60 deg" if not problems else "; ".join(problems))


# --------------------------------------------------------------------------- overhang / bridge / detail
def check_overhang(path, t, m):
    f = path.relative_to(ROOT).as_posix()
    n = t.face_normals
    sel = (n[:, 2] < -0.05) & (n[:, 1] > 0.05)
    ang = sorted(set(float(a) for a in np.round(np.degrees(np.arcsin(-n[sel, 2])), 2)))
    check_list(f, "overhang angles from vertical (deg)", ang, list(range(20, 80, 5)), tol=0.05)


DOC_SPANS = {"0.4": [5, 10, 20, 30, 40, 50], "0.2": [3, 5, 8, 12, 16, 20]}
DOC_BRIDGE_HB = {"0.4": 8.0, "0.2": 5.0}


def check_bridge(path, t, m):
    f = path.relative_to(ROOT).as_posix()
    nz = nozzle_of(path)
    cs = m.slice(DOC_BRIDGE_HB[nz] / 2)
    pil = sorted(b for b, _ in pieces(cs))
    spans = [pil[i + 1][0] - pil[i][2] for i in range(0, len(pil) - 1, 2)]
    check_list(f, "bridge spans (mm)", spans, DOC_SPANS[nz])
    # slab underside height
    under = m.slice(DOC_BRIDGE_HB[nz] + LAYER[nz] / 2)
    ok = len(pieces(under)) == len(DOC_SPANS[nz])
    log(f, "PASS" if ok else "FAIL", f"each bridge is one closed slab at z={DOC_BRIDGE_HB[nz]} "
        f"({len(pieces(under))} slabs)")


DETAIL = {  # from docs/tests-overhang-bridge-detail.md section 3
    "0.4": dict(zb=1.6, block_h=3.0, mult=[0.5, 0.75, 1, 1.5, 2, 3, 4], pins=[0.5, 0.8, 1.0, 1.5, 2.0, 3.0],
                holes=[0.5, 0.8, 1.0, 1.5, 2.0, 3.0], gaps=[0.1, 0.2, 0.3, 0.4, 0.6, 0.8], wall_len=8.0),
    "0.2": dict(zb=1.0, block_h=2.0, mult=[0.5, 0.75, 1, 1.5, 2, 3, 4], pins=[0.3, 0.5, 0.8, 1.0, 1.5, 2.0],
                holes=[0.3, 0.5, 0.8, 1.0, 1.5, 2.0], gaps=[0.05, 0.1, 0.15, 0.2, 0.3, 0.4], wall_len=5.0),
}


def check_detail(path, t, m):
    f = path.relative_to(ROOT).as_posix()
    nz = nozzle_of(path)
    d = DETAIL[nz]
    cs = m.slice(d["zb"] + d["block_h"] + 1.0)        # above the hole/gap blocks
    walls, pins = [], []
    for b, a in pieces(cs):
        dx, dy = b[2] - b[0], b[3] - b[1]
        if close(dy, d["wall_len"], 0.02):
            walls.append(dx)
        else:
            pins.append(eq_diam(a))
    check_list(f, f"thin walls (mm) = k x {LW[nz]}", walls, [k * LW[nz] for k in d["mult"]], tol=0.002)
    check_list(f, "pin diameters (mm)", pins, d["pins"], tol=0.01)
    cs = m.slice(d["zb"] / 2)                          # holes go through the base
    check_list(f, "through-hole diameters (mm)", [eq_diam(a) for _, a in holes_of(cs)], d["holes"], tol=0.01)
    # slots run out of the comb block in Y; measure the gaps along X through the comb
    cs = m.slice(d["zb"] + d["block_h"] / 2)
    comb = max((p.bounds() for p in cs.decompose()), key=lambda b: b[1])   # back-most row
    segs = sorted(b for b, _ in pieces(cs ^ strip_x((comb[1] + comb[3]) / 2)))
    slot_w = [segs[i + 1][0] - segs[i][2] for i in range(len(segs) - 1)]
    check_list(f, "slot widths (mm)", slot_w, d["gaps"], tol=0.005)


def check_verify(path, t, m):
    f = path.relative_to(ROOT).as_posix()
    nz = nozzle_of(path)
    s = 1.0 if nz == "0.4" else 0.6
    cs = m.slice(8.5 * s)   # main block above the horizontal hole (centre 5.5, d 4, scaled)
    hs = [eq_diam(a) for b, a in holes_of(cs) if (b[2] - b[0]) < 6 * s]
    check_list(f, "vertical hole diameters (mm)", hs, [3 * s, 5 * s], tol=0.02)


# --------------------------------------------------------------------------- dimensional
DIM = {  # from docs/tests-dimensional.md
    "0.4": dict(xy_w=2.10, xy_h=4.0, ef_w=2.52, ef_L=20.0, ef_h=6.0, hp=[2, 3, 4, 5, 6, 8, 10], hp_T=3.0, hp_peg=6.0,
                fit_holes=[6.10, 6.20, 6.30, 6.40, 6.50, 6.60, 6.70, 6.80], fit_T=4.0, fit_pin=6.0, fit_F=1.6,
                fl_sq=25.0, l0=0.20),
    "0.2": dict(xy_w=1.76, xy_h=3.0, ef_w=1.76, ef_L=15.0, ef_h=4.0, hp=[1, 1.5, 2, 2.5, 3, 4, 5], hp_T=2.0, hp_peg=4.0,
                fit_holes=[3.05, 3.10, 3.15, 3.20, 3.25, 3.30, 3.35, 3.40], fit_T=3.0, fit_pin=3.0, fit_F=1.0,
                fl_sq=20.0, l0=0.10),
}


def check_dim(path, t, m):
    f = path.relative_to(ROOT).as_posix()
    nz = nozzle_of(path)
    d = DIM[nz]
    lw = LW[nz]
    name = path.name
    if name.startswith("dim01_"):
        ok = close(t.extents[2], d["l0"], 1e-4)
        sizes = sorted({round(b[2] - b[0], 3) for b, _ in pieces(m.slice(d["l0"] / 2))})
        log(f, "PASS" if ok and sizes == [d["fl_sq"]] else "FAIL",
            f"thickness {t.extents[2]:.3f} (one first layer {d['l0']}), square size {sizes}")
    elif name.startswith("dim02_"):
        cs = m.slice(d["xy_h"] / 2)
        for axis, line in (("X", strip_x(0.0)), ("Y", strip_y(0.0))):
            segs = sorted(b for b, _ in pieces(cs ^ line))
            i0, i1 = (0, 2) if axis == "X" else (1, 3)
            widths = [b[i1] - b[i0] for b in segs]
            check_list(f, f"{axis} wall widths (mm) = {d['xy_w'] / lw:.0f} x {lw}", widths, [d["xy_w"]] * 4, tol=0.002)
            outer = segs[-1][i1] - segs[0][i0]
            island = segs[2][i1] - segs[1][i0]
            ok = close(outer, 100.0, 0.002) and close(island, 20.0, 0.002)
            log(f, "PASS" if ok else "FAIL", f"{axis} outer {outer:.3f} / island {island:.3f} (100 / 20)")
    elif name.startswith("dim05_"):
        cs = m.slice(d["ef_h"] / 2)
        segs = sorted(b for b, _ in pieces(cs ^ strip_x(0.0)))
        check_list(f, f"ring wall widths (mm) = {d['ef_w'] / lw:.0f} x {lw}", [b[2] - b[0] for b in segs],
                   [d["ef_w"]] * 2, tol=0.002)
        log(f, "PASS" if close(segs[-1][2] - segs[0][0], d["ef_L"], 0.002) else "FAIL",
            f"outer size {segs[-1][2] - segs[0][0]:.3f} ({d['ef_L']})")
    elif name.startswith("dim03_"):
        holes = [eq_diam(a) for _, a in holes_of(m.slice(d["hp_T"] / 2))]
        check_list(f, "hole diameters (mm)", holes, d["hp"], tol=0.005)
        pegs = [eq_diam(a) for _, a in pieces(m.slice(d["hp_T"] + d["hp_peg"] / 2))]
        check_list(f, "peg diameters (mm)", pegs, d["hp"], tol=0.005)
    elif name.startswith("dim04_"):
        cs = m.slice(d["fit_T"] / 2)
        holes = [eq_diam(a) for _, a in holes_of(cs)]
        check_list(f, "clearance hole diameters (mm)", holes, d["fit_holes"], tol=0.005)
        pin = [eq_diam(a) for _, a in pieces(m.slice(d["fit_T"] + 1.0))]
        check_list(f, "test pin diameter (mm)", pin, [d["fit_pin"]], tol=0.005)


# --------------------------------------------------------------------------- main
def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    doc_ts = (ROOT / "docs" / "tests-temp-stringing.md").read_text(encoding="utf-8")
    files = sorted((ROOT / "stl").glob("*/*.stl"))
    if not files:
        print("no STL files found")
        return 1
    for path in files:
        t = trimesh.load(path, force="mesh")
        m = to_manifold(t)
        generic(path, t, m)
        n = path.name
        try:
            if n.startswith("temp_tower_"):
                check_tower(path, t, m, doc_ts)
            elif n.startswith("overhang_angles_"):
                check_overhang(path, t, m)
            elif n.startswith("bridge_spans_"):
                check_bridge(path, t, m)
            elif n.startswith("min_feature_"):
                check_detail(path, t, m)
            elif n.startswith("verify_combo_"):
                check_verify(path, t, m)
            elif n.startswith("dim0"):
                check_dim(path, t, m)
        except Exception as e:  # a spot check that cannot run is a failure, not a crash
            log(path.relative_to(ROOT).as_posix(), "FAIL", f"spot check error: {e!r}")

    cur = None
    for f, level, msg in results:
        if f != cur:
            print(f"\n{f}")
            cur = f
        print(f"  [{level}] {msg}")
    nfail = sum(1 for _, lv, _ in results if lv == "FAIL")
    print(f"\n{len(files)} files, {sum(1 for _, lv, _ in results if lv == 'PASS')} checks passed, "
          f"{nfail} failed, {sum(1 for _, lv, _ in results if lv == 'NOTE')} notes")
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main())
