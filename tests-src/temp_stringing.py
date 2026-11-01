"""Generate temperature-tower and stringing/retraction test STLs for a Bambu Lab A1.

Outputs (per nozzle, in stl/0.2/ and stl/0.4/):
  temp_tower_<hot>-<cold>_<n>.stl    one tower per range in TOWER_RANGES, hottest
                                     block at the bottom, 5 C per block
  stringing_pins_<n>.stl             3 tapered pins, two travel spacings
  retraction_coupon_<n>.stl          short 2-pin coupon, one print per retraction value
  retraction_tower_devmode_0.4.stl   (0.4 only) 2 posts for Bambu's per-1-mm retraction rule

Every Z feature is an integer multiple of the nozzle's layer height. Labels are
engraved seven-segment numerals made from boxes (STLs carry no fonts).

Run:  .venv/Scripts/python -I tests-src/temp_stringing.py
      .venv/Scripts/python -I tests-src/temp_stringing.py --markdown   (also print the
      height -> M104 tables as Markdown, for docs/tests-temp-stringing.md)
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import trimesh
from manifold3d import Manifold

ROOT = Path(__file__).resolve().parent.parent
BED = 256.0
SEG = 48  # circular segments for pins


# --------------------------------------------------------------------------- helpers
def box(x0, x1, y0, y1, z0, z1) -> Manifold:
    return Manifold.cube((x1 - x0, y1 - y0, z1 - z0)).translate((x0, y0, z0))


def cone(cx, cy, z0, h, r_low, r_high) -> Manifold:
    return Manifold.cylinder(h, r_low, r_high, SEG).translate((cx, cy, z0))


def union(parts) -> Manifold:
    return Manifold.batch_boolean(list(parts), _op_add())


def _op_add():
    from manifold3d import OpType
    return OpType.Add


def to_trimesh(m: Manifold) -> trimesh.Trimesh:
    mesh = m.to_mesh()
    verts = np.asarray(mesh.vert_properties)[:, :3]
    faces = np.asarray(mesh.tri_verts)
    return trimesh.Trimesh(vertices=verts, faces=faces, process=True)


# Seven-segment layout: segment -> (x0, x1, z0, z1) in units of (w, h, s)
SEGMENTS = {
    "a": lambda w, h, s: (0, w, h - s, h),
    "b": lambda w, h, s: (w - s, w, h / 2, h),
    "c": lambda w, h, s: (w - s, w, 0, h / 2),
    "d": lambda w, h, s: (0, w, 0, s),
    "e": lambda w, h, s: (0, s, 0, h / 2),
    "f": lambda w, h, s: (0, s, h / 2, h),
    "g": lambda w, h, s: (0, w, h / 2 - s / 2, h / 2 + s / 2),
}
DIGITS = {
    "0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc",
    "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcdfg",
}


def numeral_cutters(text, x_left, z_bottom, w, h, s, gap, y_face, depth) -> list[Manifold]:
    """Boxes to subtract from a face at y=y_face (face normal -Y), engraving `text`."""
    cutters = []
    for i, ch in enumerate(text):
        ox = x_left + i * (w + gap)
        for seg in DIGITS[ch]:
            x0, x1, z0, z1 = SEGMENTS[seg](w, h, s)
            cutters.append(box(ox + x0, ox + x1, y_face - 1.0, y_face + depth,
                               z_bottom + z0, z_bottom + z1))
    return cutters


def text_width(n, w, gap):
    return n * w + (n - 1) * gap


# --------------------------------------------------------------------------- params
@dataclass(frozen=True)
class TowerP:
    nozzle: str
    lh: float          # layer height
    base_t: float      # base plate thickness
    H: float           # block height
    D: float           # block depth (Y)
    Wc: float          # core width (label carrier)
    Lb: float          # bridge span / window width
    Wp: float          # right pillar width
    tb: float          # bridge deck thickness
    ho45: float        # height of 45 deg overhang wedge
    ho60: float        # height of 60 deg overhang wedge
    pin_h: float
    pin_r0: float
    pin_r1: float
    pin_dx: tuple      # pin x offsets inside the window
    dig_w: float
    dig_h: float
    dig_s: float
    dig_gap: float
    eng: float         # engrave depth
    margin: float      # base margin around the footprint


TOWER = {
    "0.4": TowerP("0.4", 0.20, 1.0, 10.0, 12.0, 16.0, 24.0, 6.0, 1.0, 5.0, 4.0,
                  6.0, 1.5, 0.5, (6.0, 18.0), 3.6, 6.0, 0.8, 0.9, 0.6, 3.0),
    "0.2": TowerP("0.2", 0.10, 0.6, 6.0, 8.0, 11.0, 14.0, 4.0, 0.6, 3.0, 2.4,
                  3.5, 1.0, 0.3, (3.5, 10.5), 2.4, 4.0, 0.6, 0.6, 0.4, 2.0),
    # 0.2 digit stroke is 0.6, not 0.5: the centred middle bar spans h/2 +- s/2, and with
    # s = 0.5 its faces fell at x.35 / x.85 mm, off the 0.10 mm layer grid.
}

# (hottest, coldest) in C. Which filament uses which tower: docs/tests-temp-stringing.md
# and docs/filament-settings.md. Every range is generated for both nozzles.
TOWER_RANGES = [
    (230, 190),  # generic PLA / ELEGOO PLA 0.4 (Bambu Studio's own PLA default)
    (225, 195),  # ELEGOO PLA 0.2
    (235, 200),  # ELEGOO PLA+ and Rapid PLA+ 0.4
    (230, 200),  # ELEGOO PLA+ / Rapid PLA+ / Keytek PLA 0.2
    (240, 205),  # Keytek PLA 0.4 (label 220-240)
    (260, 220),  # generic PETG (any PETG of unknown line); not assigned to a user filament
    (260, 230),  # ELEGOO PETG PRO (blue, label 230-260), both nozzles
    (270, 240),  # ELEGOO Rapid PETG (clear, label 240-270), both nozzles
]
STEP_C = 5


def tower_name(hot: int, cold: int, nz: str) -> str:
    return f"temp_tower_{hot}-{cold}_{nz}.stl"


def tower_table(p: "TowerP", hot: int, cold: int):
    """Rows (block, z_bottom, z_top, temp, insert_top_z or None) for one tower."""
    rows = []
    for k, t in enumerate(range(hot, cold - 1, -STEP_C)):
        z0 = p.base_t + k * p.H
        rows.append((k + 1, z0, z0 + p.H, t, None if k == 0 else z0 + p.lh))
    return rows


def tower_markdown(p: "TowerP", hot: int, cold: int) -> str:
    rows = tower_table(p, hot, cold)
    out = [f"#### {p.nozzle} nozzle: `{tower_name(hot, cold, p.nozzle)}` "
           f"({len(rows)} blocks, layer {p.lh:.2f}, base 0–{p.base_t:.2f}, height {rows[-1][2]:.2f} mm)",
           "",
           "| Block | Block Z (mm) | Temp | Insert at layer (top Z) | Custom G-code |",
           "|---|---|---|---|---|"]
    for k, z0, z1, t, ins in rows:
        if ins is None:
            out.append(f"| {k} | {z0:.2f} – {z1:.2f} | {t} | — (preset {t}) | — |")
        else:
            out.append(f"| {k} | {z0:.2f} – {z1:.2f} | {t} | {ins:.2f} | `M104 S{t}` |")
    return "\n".join(out)


def tower_block(p: TowerP, z0: float, label: str) -> Manifold:
    H, D = p.H, p.D
    xw0 = p.Wc                       # window start
    xp0 = p.Wc + p.Lb                # pillar start
    xp1 = xp0 + p.Wp                 # pillar end
    o45 = p.ho45 * math.tan(math.radians(45))
    o60 = p.ho60 * math.tan(math.radians(60))
    zt = z0 + H

    parts = [
        box(0, p.Wc, 0, D, z0, zt),                 # core
        box(xp0, xp1, 0, D, z0, zt),                # right pillar
        box(xw0, xp0, 0, D, zt - p.tb, zt),         # bridge deck over the window
    ]
    # 45 deg wedge on the left of the core (grows outward toward block top).
    # The inner hull points sit 0.5 mm inside the solid, on the same slope line,
    # so the exposed underside leaves the wall at exactly z = top - ho.
    pts = []
    for y in (0.0, D):
        pts += [(0.5, y, zt - p.ho45 - 0.5 * p.ho45 / o45), (-o45, y, zt), (0.5, y, zt)]
    parts.append(Manifold.hull_points(np.array(pts)))
    # 60 deg (from vertical) wedge on the right of the pillar
    pts = []
    for y in (0.0, D):
        pts += [(xp1 - 0.5, y, zt - p.ho60 - 0.5 * p.ho60 / o60), (xp1 + o60, y, zt), (xp1 - 0.5, y, zt)]
    parts.append(Manifold.hull_points(np.array(pts)))
    # stringing pins standing on the window floor (previous deck / base)
    for dx in p.pin_dx:
        parts.append(cone(xw0 + dx, D / 2, z0, p.pin_h, p.pin_r0, p.pin_r1))
    block = union(parts)

    tw = text_width(len(label), p.dig_w, p.dig_gap)
    cut = numeral_cutters(label, (p.Wc - tw) / 2, z0 + (H - p.dig_h) / 2,
                          p.dig_w, p.dig_h, p.dig_s, p.dig_gap, 0.0, p.eng)
    return block - union(cut)


def temp_tower(p: TowerP, t_hot: int, t_cold: int):
    if (t_hot - t_cold) % STEP_C or t_hot <= t_cold:
        raise ValueError(f"bad range {t_hot}-{t_cold}")
    o45 = p.ho45
    o60 = p.ho60 * math.tan(math.radians(60))
    x_min = -o45 - p.margin
    x_max = p.Wc + p.Lb + p.Wp + o60 + p.margin
    parts = [box(x_min, x_max, -p.margin, p.D + p.margin, 0.0, p.base_t)]
    table = tower_table(p, t_hot, t_cold)
    for k, z0, z1, t, _ in table:
        parts.append(tower_block(p, z0, str(t)))
    return union(parts), table


# --------------------------------------------------------------------------- stringing / retraction
@dataclass(frozen=True)
class PinP:
    lh: float
    strip_t: float
    strip_w: float
    pin_h: float
    r0: float
    r1: float
    xs: tuple          # pin centre x positions
    tab: tuple         # marker tab (length, width) or None


PINS = {
    "0.4": PinP(0.20, 0.6, 6.0, 25.0, 3.5, 1.0, (0.0, 20.0, 60.0), None),
    "0.2": PinP(0.10, 0.4, 4.0, 15.0, 2.2, 0.6, (0.0, 12.0, 36.0), None),
}
COUPON = {
    "0.4": PinP(0.20, 0.6, 6.0, 12.0, 3.0, 1.0, (0.0, 30.0), (14.0, 10.0)),
    "0.2": PinP(0.10, 0.4, 4.0, 8.0, 2.0, 0.6, (0.0, 20.0), (10.0, 7.0)),
}


def pin_row(p: PinP) -> Manifold:
    x0 = p.xs[0] - p.r0 - 1.0
    x1 = p.xs[-1] + p.r0 + 1.0
    parts = [box(x0, x1, -p.strip_w / 2, p.strip_w / 2, 0.0, p.strip_t)]
    for x in p.xs:
        parts.append(Manifold.cylinder(p.strip_t, p.r0 + 1.0, p.r0 + 1.0, SEG).translate((x, 0, 0)))  # foot
        parts.append(cone(x, 0.0, p.strip_t, p.pin_h, p.r0, p.r1))
    if p.tab:
        tl, tw = p.tab
        parts.append(box(x1 - 0.5, x1 + tl, -tw / 2, tw / 2, 0.0, p.strip_t))  # write the value here
    return union(parts)


def retraction_tower_devmode() -> tuple[Manifold, float]:
    """Two posts for Bambu Studio's dev-mode rule: length = start + floor(max(0, z-0.4)) * step.
    0.2 mm layers (forced by Bambu's dialog). Base 0.4 mm, posts to z = 21.4 mm (21 steps).
    A 0.4 mm groove at every 5th step boundary (z = 5.4, 10.4, 15.4, 20.4) aids counting."""
    base_t, top, r, spacing = 0.4, 21.4, 2.5, 30.0
    parts = [box(-r - 2, spacing + r + 2, -4.0, 4.0, 0.0, base_t)]
    for x in (0.0, spacing):
        parts.append(Manifold.cylinder(top - base_t, r, r, SEG).translate((x, 0, base_t)))
    body = union(parts)
    grooves = []
    for k in (5, 10, 15, 20):
        z = 0.4 + k
        for x in (0.0, spacing):
            ring = (Manifold.cylinder(0.4, r + 1, r + 1, SEG) - Manifold.cylinder(0.4, r - 0.4, r - 0.4, SEG))
            grooves.append(ring.translate((x, 0, z)))
    return body - union(grooves), top


# --------------------------------------------------------------------------- validation / export
def finish(m: Manifold, path: Path, lh: float | None) -> trimesh.Trimesh:
    # put the part on the bed, centred on the plate origin in XY
    bb = m.bounding_box()
    m = m.translate((-(bb[0] + bb[3]) / 2, -(bb[1] + bb[4]) / 2, -bb[2]))
    t = to_trimesh(m)
    ext = t.extents
    bodies = len(m.decompose())
    problems = []
    if not t.is_watertight:
        problems.append("not watertight")
    if not t.is_winding_consistent:
        problems.append("inconsistent winding")
    if t.volume <= 0:
        problems.append(f"volume {t.volume:.3f}")
    if ext[0] > BED or ext[1] > BED or ext[2] > BED:
        problems.append(f"exceeds bed {ext}")
    if bodies != 1:
        problems.append(f"{bodies} bodies")
    if lh is not None:
        layers = ext[2] / lh
        if abs(layers - round(layers)) > 1e-4:
            problems.append(f"height {ext[2]:.4f} not a multiple of {lh}")
    path.parent.mkdir(parents=True, exist_ok=True)
    t.export(path)
    status = "OK" if not problems else "FAIL: " + "; ".join(problems)
    print(f"  {path.relative_to(ROOT).as_posix():<52} {ext[0]:7.2f} x {ext[1]:6.2f} x {ext[2]:6.2f} mm"
          f"  vol {t.volume / 1000:6.2f} cm3  tris {len(t.faces):6d}  {status}")
    if problems:
        raise SystemExit(f"validation failed for {path}")
    return t


def main() -> int:
    markdown = "--markdown" in sys.argv[1:]
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # en dashes in the Markdown tables
    except AttributeError:
        pass
    print("Generating temperature / stringing / retraction STLs")
    wanted = {tower_name(h, c, nz) for nz in TOWER for h, c in TOWER_RANGES}
    for nz, p in TOWER.items():
        out = ROOT / "stl" / nz
        # remove towers from older runs (other ranges or the old PLA_/PETG_ names)
        for old in out.glob("temp_tower_*.stl"):
            if old.name not in wanted:
                print(f"  removing stale {old.relative_to(ROOT).as_posix()}")
                old.unlink()
        for hot, cold in TOWER_RANGES:
            m, table = temp_tower(p, hot, cold)
            finish(m, out / tower_name(hot, cold, nz), p.lh)
            ins = ", ".join(f"{z:.2f}:S{t}" for _, _, _, t, z in table if z is not None)
            print(f"      preset {hot} C; M104 at layer-top Z {ins}")
        finish(pin_row(PINS[nz]), out / f"stringing_pins_{nz}.stl", PINS[nz].lh)
        finish(pin_row(COUPON[nz]), out / f"retraction_coupon_{nz}.stl", COUPON[nz].lh)
    m, _ = retraction_tower_devmode()
    finish(m, ROOT / "stl" / "0.4" / "retraction_tower_devmode_0.4.stl", 0.2)
    print("All meshes valid.")
    if markdown:
        for nz, p in TOWER.items():
            for hot, cold in TOWER_RANGES:
                print()
                print(tower_markdown(p, hot, cold))
    return 0


if __name__ == "__main__":
    sys.exit(main())
