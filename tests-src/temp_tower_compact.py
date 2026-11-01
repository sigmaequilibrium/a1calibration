"""Compact temperature tower for the 0.2 mm nozzle.

Same block design as temp_stringing.py (45/60 degree overhangs, a bridge over a window with two
stringing pins, an engraved temperature) but with 4 mm blocks and a smaller footprint, so a
230 -> 190 C tower is 36.6 mm tall (366 layers at 0.10 mm) instead of 54.6 mm (546 layers).

Writes stl/0.2/temp_tower_compact_<hot>-<cold>_0.2.stl for each range in RANGES and prints the
M104 height table. build_3mf.py imports tower_table_compact() for the layer-slider G-code.

Run:  .venv/Scripts/python -I tests-src/temp_tower_compact.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import temp_stringing as ts  # noqa: E402

ROOT = ts.ROOT

# 0.10 mm layers, line width 0.22. Every height below is a whole multiple of 0.10 mm, and the
# digit stroke is 0.6 mm so the centred middle bar stays on the layer grid (see temp_stringing.py).
COMPACT_02 = ts.TowerP(
    "0.2", 0.10, 0.6, 4.0, 6.0, 8.0, 10.0, 3.0, 0.6, 2.0, 1.6,
    2.4, 0.8, 0.3, (2.5, 7.5), 1.8, 3.0, 0.6, 0.5, 0.4, 1.5)

RANGES = [(230, 190)]   # Matte PLA reference tower (docs/reference-offset-method.md, R2)


def name(hot: int, cold: int) -> str:
    return f"temp_tower_compact_{hot}-{cold}_0.2.stl"


def tower_table_compact(hot: int, cold: int):
    return ts.tower_table(COMPACT_02, hot, cold)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    for hot, cold in RANGES:
        m, table = ts.temp_tower(COMPACT_02, hot, cold)
        ts.finish(m, ROOT / "stl" / "0.2" / name(hot, cold), COMPACT_02.lh)
        print("      preset", hot, "C; M104 at layer-top Z",
              ", ".join(f"{z:.2f}:S{t}" for _, _, _, t, z in table if z is not None))
    return 0


if __name__ == "__main__":
    sys.exit(main())
