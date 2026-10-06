"""Build ready-to-open Bambu Studio project files (.3mf) for every calibration STL.

Output: 3mf/0.2/*.3mf and 3mf/0.4/*.3mf (one project per test, plus one dim02+dim03+dim05
combo plate per nozzle). Each project contains:

  - the mesh(es) from stl/<nozzle>/, centred on the A1 plate (or laid out side by side),
  - the stock system presets selected by name (printer "Bambu Lab A1 <n> nozzle", process
    "0.20mm Standard @BBL A1" / "0.10mm Standard @BBL A1 0.2 nozzle", filament "Generic ...")
    with their full, resolved values in Metadata/project_settings.config,
  - per-object overrides from docs/tests-*.md (walls, infill, seam, brim, supports, layer height),
  - for every temperature tower: filament nozzle temperature = hottest block, and
    Metadata/custom_gcode_per_layer.xml with `M104 S<t>` at the first layer of each block.

How the presets are written (checked against BambuStudio v02.08.02.61 source):
  Plater::load_files fills keys missing from project_settings.config with libslic3r's
  hard-coded defaults (FullPrintConfig::defaults), not with the system preset. So the script
  writes the complete resolved preset values (inherits + include chains of the BBL system
  JSON profiles). It also writes print/printer/filament_settings_id, inherits_group and
  different_settings_to_system; PresetCollection::load_external_preset then re-syncs every key
  that is NOT listed as different to the user's installed system preset, and keeps the listed
  ones (here only the tower nozzle temperatures) as an unsaved modification.

System profile JSONs are read from (first found):
  --profiles DIR | $BAMBU_PROFILES | a local Bambu Studio install (resources/profiles/BBL)
  | the cache tests-src/bbl_profiles/<tag>/ (filled from GitHub raw at --tag on first use).

Run:   .venv/Scripts/python -I tests-src/build_3mf.py
       .venv/Scripts/python -I tests-src/build_3mf.py --studio "C:/Program Files/Bambu Studio/bambu-studio.exe"
            (also slices every temperature-tower project headless with the Bambu Studio CLI and
             checks that each M104 lands on the expected layer of the G-code)
The script is rerunnable: it deletes and rewrites 3mf/0.2 and 3mf/0.4 from the current STLs.
"""

from __future__ import annotations

import argparse
import io
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import urllib.request
import uuid
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.dom import minidom
from xml.sax.saxutils import quoteattr

import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parent.parent
STL = ROOT / "stl"
OUT = ROOT / "3mf"
CACHE = ROOT / "tests-src" / "bbl_profiles"
TAG = "v02.08.02.61"            # BambuStudio release whose system profiles are embedded
BED = 256.0
CX = CY = BED / 2               # plate centre (A1 purges off-plate: no exclusion zone, see docs)
PLATE = "Textured PEI Plate"    # the plate the A1 ships with
ZIP_DATE = (2026, 1, 1, 0, 0, 0)

sys.path.insert(0, str(ROOT / "tests-src"))
import temp_stringing as ts
import temp_tower_compact as tc      # noqa: E402  (read-only: tower geometry + height tables)

NOZZLES = {
    # nozzle: (layer height, printer preset, process preset, filament suffix)
    "0.4": (0.20, "Bambu Lab A1 0.4 nozzle", "0.20mm Standard @BBL A1", "@BBL A1"),
    "0.2": (0.10, "Bambu Lab A1 0.2 nozzle", "0.10mm Standard @BBL A1 0.2 nozzle", "@BBL A1 0.2 nozzle"),
}
COLOURS = {"PLA": "#00AE42", "PETG": "#1F79E5"}


# --------------------------------------------------------------------------- system presets
META = {"name", "inherits", "from", "setting_id", "instantiation", "include", "type",
        "filament_id", "description", "renamed_from", "compatible_printers",
        "compatible_prints", "compatible_printers_condition", "compatible_prints_condition"}
SUBDIR = {"machine": "machine", "process": "process", "filament": "filament"}


class Profiles:
    def __init__(self, base: Path | None, tag: str):
        self.base, self.tag = base, tag
        self.cache = CACHE / tag
        self._raw: dict[str, dict] = {}

    def _read(self, sub: str, name: str) -> dict:
        key = f"{sub}/{name}"
        if key in self._raw:
            return self._raw[key]
        rel = Path(sub) / f"{name}.json"
        for d in ([self.base] if self.base else []) + [self.cache]:
            p = d / rel
            if p.is_file():
                break
        else:
            if self.base:
                raise SystemExit(f"profile {rel} not found under {self.base}")
            url = ("https://raw.githubusercontent.com/bambulab/BambuStudio/"
                   f"{self.tag}/resources/profiles/BBL/{rel.as_posix()}").replace(" ", "%20")
            print(f"  fetching {url}")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=60).read()
            p = self.cache / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("name") != name:
            raise SystemExit(f"{p}: name {d.get('name')!r} != {name!r}")
        self._raw[key] = d
        return d

    def resolve(self, sub: str, name: str) -> dict:
        """Same order as PresetBundle::load_vendor_configs_from_json: parent, includes, own keys."""
        d = self._read(sub, name)
        cfg = self.resolve(sub, d["inherits"]) if d.get("inherits") else {}
        for inc in d.get("include", []) or []:
            cfg.update({k: v for k, v in self._read(sub, inc).items() if k not in META})
        cfg.update({k: v for k, v in d.items() if k not in META})
        return cfg

    def filament_id(self, name: str) -> str:
        n = name
        while n:
            d = self._read("filament", n)
            if d.get("filament_id"):
                return d["filament_id"]
            n = d.get("inherits")
        return ""


def find_profile_dir(arg: str | None) -> Path | None:
    cands = [arg, os.environ.get("BAMBU_PROFILES")]
    for pf in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)")):
        if pf:
            cands.append(str(Path(pf) / "Bambu Studio" / "resources" / "profiles" / "BBL"))
    for c in cands:
        if c and (Path(c) / "machine").is_dir():
            return Path(c)
    return None


def project_settings(prof: Profiles, nozzle: str, filament: str, fil_type: str,
                     fil_over: dict[str, str], version: str) -> dict:
    lh, printer, process, _ = NOZZLES[nozzle]
    cfg: dict = {}
    cfg.update(prof.resolve("machine", printer))
    cfg.update(prof.resolve("process", process))
    fil = prof.resolve("filament", filament)
    for k, v in fil_over.items():
        fil[k] = [v] if isinstance(fil.get(k), list) else v
    cfg.update(fil)
    cfg.update({
        "name": "project_settings",
        "from": "project",
        "version": version,
        "printer_settings_id": printer,
        "print_settings_id": process,
        "filament_settings_id": [filament],
        "print_compatible_printers": [printer],
        # [print, filament 1, printer]; empty inherits = the selected preset IS the system preset
        "inherits_group": ["", "", ""],
        "different_settings_to_system": ["", ";".join(sorted(fil_over)), ""],
        "filament_colour": [COLOURS[fil_type]],
        "filament_ids": [prof.filament_id(filament)],
        "filament_map": ["1"],
        "filament_self_index": ["1"],
        "curr_bed_type": PLATE,
    })
    if abs(float(cfg["initial_layer_print_height"]) - lh) > 1e-9 or abs(float(cfg["layer_height"]) - lh) > 1e-9:
        raise SystemExit(f"{process}: layer heights differ from {lh}")
    return cfg


# --------------------------------------------------------------------------- projects
@dataclass
class Obj:
    stl: Path
    name: str
    overrides: dict[str, str] = field(default_factory=dict)
    at: tuple[float, float] = (CX, CY)   # plate position of the part's XY bbox centre


@dataclass
class Project:
    nozzle: str
    out_name: str
    objects: list[Obj]
    fil_type: str = "PLA"
    filament: str = ""                    # full preset name; derived from fil_type if empty
    fil_over: dict[str, str] = field(default_factory=dict)
    gcodes: list[tuple[float, str]] = field(default_factory=list)   # (top_z, gcode)


def base_over(nz: str, **kw) -> dict[str, str]:
    d = {"layer_height": f"{NOZZLES[nz][0]:.2f}", "enable_support": "0"}
    d.update({k: str(v) for k, v in kw.items()})
    return d


TOWER_RE = re.compile(r"^temp_tower_(?:[A-Za-z]+_)?(\d{3})-(\d{3})_(0\.[24])\.stl$")
SKIP = {"retraction_tower_devmode_0.4.stl"}   # only works inside Studio's dev-mode calibration


def tower_filament(hot: int, cold: int) -> tuple[str, str]:
    if hot <= 240:
        return "PLA", "Generic PLA"
    if (hot, cold) == (270, 240):
        return "PETG", "Generic PETG HF"     # ELEGOO Rapid PETG, docs/filament-settings.md
    return "PETG", "Generic PETG"


def tower_gcodes(nz: str, hot: int, cold: int, compact: bool = False) -> list[tuple[float, str]]:
    rows = tc.tower_table_compact(hot, cold) if compact else ts.tower_table(ts.TOWER[nz], hot, cold)
    return [(round(z, 4), f"M104 S{t}") for _, _, _, t, z in rows if z is not None]


def projects_for(nz: str) -> tuple[list[Project], list[str]]:
    d = STL / nz
    files = {f.name: f for f in sorted(d.glob("*.stl"))}
    used: set[str] = set()
    projs: list[Project] = []

    def pick(pattern: str) -> Path | None:
        m = [f for n, f in files.items() if re.fullmatch(pattern, n)]
        if len(m) > 1:
            raise SystemExit(f"ambiguous {pattern}: {m}")
        if m:
            used.add(m[0].name)
        return m[0] if m else None

    w = lambda a, b: a if nz == "0.4" else b    # noqa: E731
    dims = {
        "dim01": (r"dim01_.*\.stl", base_over(nz, wall_loops=2, brim_type="no_brim")),
        "dim02": (r"dim02_.*\.stl", base_over(nz, wall_loops=w(5, 8), sparse_infill_density="15%", brim_type="no_brim")),
        "dim03": (r"dim03_.*\.stl", base_over(nz, wall_loops=w(3, 4), sparse_infill_density="15%",
                                                seam_position="aligned", brim_type="no_brim")),
        "dim04": (r"dim04_.*\.stl", base_over(nz, wall_loops=w(3, 4), sparse_infill_density="15%", brim_type="no_brim")),
        "dim05": (r"dim05_.*\.stl", base_over(nz, wall_loops=w(6, 8), brim_type="no_brim")),
    }
    dim_files = {}
    for key, (pat, over) in dims.items():
        f = pick(pat)
        if f:
            dim_files[key] = (f, over)
            projs.append(Project(nz, f.stem, [Obj(f, f.stem, over)]))
    # ELEGOO Matte PLA purple reference run, R1 (docs/filament-settings.md section 0, docs/reference-offset-method.md 2.2)
    if "dim01" in dim_files:
        f1, o1 = dim_files["dim01"]
        t0 = {"0.4": "215", "0.2": "210"}[nz]
        projs.append(Project(nz, f"R1_matte-purple_{f1.stem}", [Obj(f1, f1.stem, o1)], fil_over={
            "nozzle_temperature": t0, "nozzle_temperature_initial_layer": t0,
            "textured_plate_temp": "60", "textured_plate_temp_initial_layer": "60",
            "filament_density": "1.26",
        }))
    # dim02 + dim03 + dim05 share one plate (docs/tests-dimensional.md)
    if all(k in dim_files for k in ("dim02", "dim03", "dim05")):
        f2, o2 = dim_files["dim02"]; f3, o3 = dim_files["dim03"]; f5, o5 = dim_files["dim05"]
        projs.append(Project(nz, f"dim-combo_02-03-05_{nz}n", [
            Obj(f2, f2.stem, o2, (78.0, 128.0)),
            Obj(f3, f3.stem, o3, (185.0, 160.0)),
            Obj(f5, f5.stem, o5, (185.0, 95.0)),
        ]))

    for stem in ("overhang_angles", "bridge_spans", "verify_combo"):
        f = pick(rf"{stem}_{re.escape(nz)}\.stl")
        if f:
            over = {} if stem == "verify_combo" else base_over(nz)   # verify: presets unchanged
            projs.append(Project(nz, f.stem, [Obj(f, f.stem, over)]))

    f = pick(rf"min_feature_{re.escape(nz)}\.stl")
    if f:   # both wall generators side by side, X-Y compensation forced to 0 (raw result)
        comp = {"xy_hole_compensation": "0", "xy_contour_compensation": "0"}
        dx = w(40.0, 25.0)
        projs.append(Project(nz, f.stem, [
            Obj(f, f"{f.stem} ARACHNE", base_over(nz, wall_generator="arachne", **comp), (CX - dx, CY)),
            Obj(f, f"{f.stem} CLASSIC thin-wall-off", base_over(nz, wall_generator="classic",
                                                               detect_thin_wall="0", **comp), (CX + dx, CY)),
        ]))

    f = pick(rf"cube_20mm_{re.escape(nz)}\.stl")
    if f:   # plain 20 mm cube for caliper checks (X, Y, Z)
        projs.append(Project(nz, f.stem, [Obj(f, f.stem, base_over(
            nz, wall_loops=w(3, 4), sparse_infill_density="15%", brim_type="no_brim"))]))

    for stem in ("stringing_pins", "retraction_coupon"):
        f = pick(rf"{stem}_{re.escape(nz)}\.stl")
        if f:
            projs.append(Project(nz, f.stem, [Obj(f, f.stem, base_over(nz, wall_loops=2))]))

    for name, f in files.items():
        m = TOWER_RE.match(name)
        if not m:
            continue
        used.add(name)
        hot, cold = int(m.group(1)), int(m.group(2))
        if m.group(3) != nz:
            raise SystemExit(f"{f}: nozzle mismatch")
        compact = name.startswith("temp_tower_compact_")
        ftype, fbase = tower_filament(hot, cold)
        over = base_over(nz, wall_loops=2, sparse_infill_density="15%", seam_position="back", brim_type="no_brim")
        projs.append(Project(
            nz, f.stem, [Obj(f, f.stem, over)],
            fil_type=ftype, filament=f"{fbase} {NOZZLES[nz][3]}",
            fil_over={"nozzle_temperature": str(hot), "nozzle_temperature_initial_layer": str(hot)},
            gcodes=tower_gcodes(nz, hot, cold, compact)))
        if (hot, cold) == (230, 190) and compact == (nz == "0.2"):
            # ELEGOO Matte PLA purple reference run, R2 (docs/reference-offset-method.md 2.2):
            # the compact tower on the 0.2 nozzle, the normal tower on the 0.4
            projs.append(Project(
                nz, f"R2_matte-purple_{f.stem}", [Obj(f, f.stem, over)],
                fil_type=ftype, filament=f"{fbase} {NOZZLES[nz][3]}",
                fil_over={"nozzle_temperature": str(hot), "nozzle_temperature_initial_layer": str(hot),
                          "textured_plate_temp": "60", "textured_plate_temp_initial_layer": "60",
                          "filament_density": "1.26"},
                gcodes=tower_gcodes(nz, hot, cold, compact)))

    skipped = [n for n in files if n not in used]
    return projs, skipped


# --------------------------------------------------------------------------- 3MF writing
def stl_triangle_count(path: Path) -> int:
    data = path.read_bytes()
    if len(data) >= 84:
        n = struct.unpack_from("<I", data, 80)[0]
        if 84 + 50 * n == len(data):
            return n
    return data.count(b"endfacet")   # ASCII STL


def load_mesh(path: Path) -> trimesh.Trimesh:
    m = trimesh.load(path, force="mesh", process=False)
    m.merge_vertices(digits_vertex=6)   # STL -> indexed mesh; no other repair
    return m


def fmt(v: float) -> str:
    s = f"{v:.9g}"
    return "0" if s in ("-0", "0") else s


def uid(*parts) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "a1calibration/" + "/".join(map(str, parts))))


def mat_str(t) -> str:   # 3MF 3x4 (column-major rows of the affine) for translation-only
    return f"1 0 0 0 1 0 0 0 1 {fmt(t[0])} {fmt(t[1])} {fmt(t[2])}"


NS = ('xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
      'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
      'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p"')


def object_model(oid: int, m: trimesh.Trimesh, key: str) -> str:
    out = io.StringIO()
    out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    out.write(f'<model unit="millimeter" xml:lang="en-US" {NS}>\n')
    out.write(' <metadata name="BambuStudio:3mfVersion">1</metadata>\n <resources>\n')
    out.write(f'  <object id="{oid}" p:UUID="{uid(key, "mesh")}" type="model">\n   <mesh>\n    <vertices>\n')
    for x, y, z in m.vertices:
        out.write(f'     <vertex x="{fmt(x)}" y="{fmt(y)}" z="{fmt(z)}"/>\n')
    out.write('    </vertices>\n    <triangles>\n')
    for a, b, c in m.faces:
        out.write(f'     <triangle v1="{a}" v2="{b}" v3="{c}"/>\n')
    out.write('    </triangles>\n   </mesh>\n  </object>\n </resources>\n <build/>\n</model>\n')
    return out.getvalue()


def build_project(prof: Profiles, pr: Project, version: str, dest: Path) -> dict:
    lh = NOZZLES[pr.nozzle][0]
    filament = pr.filament or f"Generic {pr.fil_type} {NOZZLES[pr.nozzle][3]}"
    cfg = project_settings(prof, pr.nozzle, filament, pr.fil_type, pr.fil_over, version)
    app = f"BambuStudio-{version}"
    files: dict[str, str] = {}
    model_meta, comps, items, cfg_objs, plate_inst, rels = [], [], [], [], [], []
    report = {"objects": []}
    for i, ob in enumerate(pr.objects):
        mesh_id, obj_id = 2 * i + 1, 2 * i + 2
        m = load_mesh(ob.stl)
        lo, hi = m.bounds
        if abs(lo[2]) > 1e-6:
            raise SystemExit(f"{ob.stl}: does not sit on z=0")
        centre = (lo + hi) / 2                               # volume origin = bbox centre (as Studio does)
        m.vertices = m.vertices - centre
        place = (ob.at[0], ob.at[1], 0.0)
        # plate check
        half = (hi - lo) / 2
        if ob.at[0] - half[0] < 0 or ob.at[0] + half[0] > BED or ob.at[1] - half[1] < 0 or ob.at[1] + half[1] > BED:
            raise SystemExit(f"{pr.out_name}: {ob.name} leaves the plate")
        path = f"3D/Objects/object_{mesh_id}.model"
        key = f"{pr.out_name}/{i}"
        files[path] = object_model(mesh_id, m, key)
        rels.append(path)
        comp_t = (0.0, 0.0, centre[2])                       # mesh -> object coords (z from 0)
        comps.append(f'  <object id="{obj_id}" p:UUID="{uid(key, "obj")}" type="model">\n   <components>\n'
                     f'    <component p:path="/{path}" objectid="{mesh_id}" p:UUID="{uid(key, "comp")}" '
                     f'transform="{mat_str(comp_t)}"/>\n   </components>\n  </object>\n')
        items.append(f'  <item objectid="{obj_id}" p:UUID="{uid(key, "item")}" transform="{mat_str(place)}" printable="1"/>\n')
        md = [f'    <metadata key="name" value={quoteattr(ob.name)}/>',
              '    <metadata key="extruder" value="1"/>']
        md += [f'    <metadata key="{k}" value={quoteattr(v)}/>' for k, v in ob.overrides.items()]
        md.append(f'    <metadata face_count="{len(m.faces)}"/>')
        cfg_objs.append(
            f'  <object id="{obj_id}">\n' + "\n".join(md) + "\n"
            f'    <part id="{mesh_id}" subtype="normal_part">\n'
            f'      <metadata key="name" value={quoteattr(ob.stl.name)}/>\n'
            f'      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 {fmt(comp_t[2])} 0 0 0 1"/>\n'
            f'      <metadata key="source_file" value={quoteattr(ob.stl.name)}/>\n'
            '      <metadata key="source_object_id" value="0"/>\n'
            '      <metadata key="source_volume_id" value="0"/>\n'
            '      <metadata key="source_offset_x" value="0"/>\n'
            '      <metadata key="source_offset_y" value="0"/>\n'
            f'      <metadata key="source_offset_z" value="{fmt(comp_t[2])}"/>\n'
            f'      <mesh_stat face_count="{len(m.faces)}" edges_fixed="0" degenerate_facets="0" '
            'facets_removed="0" facets_reversed="0" backwards_edges="0"/>\n'
            '    </part>\n  </object>')
        plate_inst.append('    <model_instance>\n'
                          f'      <metadata key="object_id" value="{obj_id}"/>\n'
                          '      <metadata key="instance_id" value="0"/>\n'
                          f'      <metadata key="identify_id" value="{100 + i}"/>\n'
                          '    </model_instance>')
        report["objects"].append({"name": ob.name, "stl": ob.stl, "verts": len(m.vertices),
                                  "tris": len(m.faces), "height": float(hi[2] - lo[2])})

    files["3D/3dmodel.model"] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<model unit="millimeter" xml:lang="en-US" {NS}>\n'
        f' <metadata name="Application">{app}</metadata>\n'
        ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n'
        f' <metadata name="Title">{pr.out_name}</metadata>\n'
        ' <metadata name="Designer"></metadata>\n'
        ' <metadata name="Description">A1 calibration test, generated by tests-src/build_3mf.py</metadata>\n'
        ' <metadata name="CreationDate">2026-10-06</metadata>\n'
        ' <metadata name="ModificationDate">2026-10-06</metadata>\n'
        ' <resources>\n' + "".join(comps) + ' </resources>\n'
        f' <build p:UUID="{uid(pr.out_name, "build")}">\n' + "".join(items) + ' </build>\n</model>\n')
    files["3D/_rels/3dmodel.model.rels"] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
        + "".join(f' <Relationship Target="/{p}" Id="rel-{k + 1}" '
                  'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n'
                  for k, p in enumerate(rels))
        + '</Relationships>\n')
    files["[Content_Types].xml"] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
        ' <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n'
        ' <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>\n'
        ' <Default Extension="png" ContentType="image/png"/>\n'
        ' <Default Extension="gcode" ContentType="text/x.gcode"/>\n'
        '</Types>\n')
    files["_rels/.rels"] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
        ' <Relationship Target="/3D/3dmodel.model" Id="rel-1" '
        'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n'
        '</Relationships>\n')
    files["Metadata/model_settings.config"] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n<config>\n' + "\n".join(cfg_objs) + "\n"
        '  <plate>\n'
        '    <metadata key="plater_id" value="1"/>\n'
        '    <metadata key="plater_name" value=""/>\n'
        '    <metadata key="locked" value="false"/>\n'
        '    <metadata key="filament_map_mode" value="Auto For Flush"/>\n'
        '    <metadata key="filament_maps" value="1"/>\n'
        + "\n".join(plate_inst) + "\n  </plate>\n  <assemble>\n  </assemble>\n</config>\n")
    files["Metadata/project_settings.config"] = json.dumps(cfg, indent=4, ensure_ascii=False) + "\n"
    files["Metadata/slice_info.config"] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n<config>\n  <header>\n'
        '    <header_item key="X-BBL-Client-Type" value="slicer"/>\n'
        f'    <header_item key="X-BBL-Client-Version" value="{version}"/>\n'
        '  </header>\n</config>\n')
    if pr.gcodes:
        lines = ['<?xml version="1.0" encoding="utf-8"?>', "<custom_gcodes_per_layer>", "<plate>",
                 '<plate_info id="1"/>']
        for z, g in pr.gcodes:   # type 4 = CustomGCode::Custom
            lines.append(f'<layer top_z="{fmt(z)}" type="4" extruder="1" color="" '
                         f'extra={quoteattr(g)} gcode={quoteattr(g)}/>')
        lines += ['<mode value="SingleExtruder"/>', "</plate>", "</custom_gcodes_per_layer>", ""]
        files["Metadata/custom_gcode_per_layer.xml"] = "\n".join(lines)

    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for name in ["[Content_Types].xml", "_rels/.rels", "3D/3dmodel.model", "3D/_rels/3dmodel.model.rels"] + \
                [n for n in files if n.startswith("3D/Objects/")] + \
                sorted(n for n in files if n.startswith("Metadata/")):
            zi = zipfile.ZipInfo(name, ZIP_DATE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, files[name].encode("utf-8"))
    report.update(filament=filament, lh=lh, gcodes=pr.gcodes, fil_over=pr.fil_over)
    return report


# --------------------------------------------------------------------------- validation
def validate(path: Path, rep: dict) -> list[str]:
    errs = []
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:
            errs.append("zip CRC error")
        names = z.namelist()
        for n in names:
            data = z.read(n)
            if n.endswith((".model", ".rels", ".xml", ".config")) and not n.endswith("project_settings.config"):
                try:
                    minidom.parseString(data)
                except Exception as e:  # noqa: BLE001
                    errs.append(f"{n}: XML error {e}")
        json.loads(z.read("Metadata/project_settings.config"))
        objs = sorted(n for n in names if n.startswith("3D/Objects/"))
        for n, o in zip(objs, rep["objects"]):
            doc = minidom.parseString(z.read(n))
            nv = len(doc.getElementsByTagName("vertex"))
            nt = len(doc.getElementsByTagName("triangle"))
            src = load_mesh(o["stl"])
            if nt != stl_triangle_count(o["stl"]) or nt != len(src.faces) or nv != len(src.vertices):
                errs.append(f"{n}: {nv} verts / {nt} tris vs STL {len(src.vertices)} / {stl_triangle_count(o['stl'])}")
        if rep["gcodes"]:
            lh = rep["lh"]
            doc = minidom.parseString(z.read("Metadata/custom_gcode_per_layer.xml"))
            layers = doc.getElementsByTagName("layer")
            if len(layers) != len(rep["gcodes"]):
                errs.append("custom gcode count mismatch")
            top = rep["objects"][0]["height"]
            for el in layers:
                zt = float(el.getAttribute("top_z"))
                k = zt / lh            # first layer = lh, so layer tops are k * lh
                if abs(k - round(k)) > 1e-6 or zt <= lh or zt > top + 1e-9:
                    errs.append(f"top_z {zt} not on a {lh} layer boundary inside the part")
    return errs


def check_against_markdown(nz: str, hot: int, cold: int, gcodes) -> list[str]:
    """Compare with the exact table temp_stringing.py --markdown prints (same function)."""
    md = ts.tower_markdown(ts.TOWER[nz], hot, cold)
    want = [(float(a), f"M104 S{b}") for a, b in re.findall(r"\| ([\d.]+) \| `M104 S(\d+)` \|", md)]
    got = [(round(z, 2), g) for z, g in gcodes]
    return [] if want == got else [f"M104 table differs from --markdown: {got} vs {want}"]


def run_studio(cmd: list[str], out: Path, timeout: float = 180.0) -> None:
    """Run the Studio CLI. It occasionally hangs while exiting after it has written result.json
    and the G-code, so stop waiting once both files exist and have stopped growing."""
    import time
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    t0, last = time.time(), None
    while p.poll() is None and time.time() - t0 < timeout:
        time.sleep(1.0)
        res, gc = out / "result.json", out / "plate_1.gcode"
        if res.exists():
            sig = (res.stat().st_size, gc.stat().st_size if gc.exists() else -1)
            if sig == last:
                break
            last = sig
    if p.poll() is None:
        try:
            p.kill()
        except OSError:
            pass


def studio_slice_check(exe: Path, f: Path, gcodes, workdir: Path) -> list[str]:
    out = workdir / f.stem
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    cmd = [str(exe), "--datadir", str(workdir / "_studio_data"), "--slice", "0", "--outputdir", str(out), str(f)]
    run_studio(cmd, out)
    res = out / "result.json"
    if not res.exists():
        return ["Studio CLI produced no result.json"]
    r = json.loads(res.read_text(encoding="utf-8"))
    if r.get("return_code") != 0:
        return [f"Studio CLI error {r.get('return_code')}: {r.get('error_string')}"]
    g = (out / "plate_1.gcode").read_text(encoding="utf-8", errors="replace").splitlines()
    errs, z = [], None
    found = []
    for line in g:
        if line.startswith("; Z_HEIGHT:"):
            z = float(line.split(":")[1])
        elif re.match(r"^M104 S\d+\s*$", line) and z is not None:
            found.append((round(z, 4), line.strip()))
    for zt, code in gcodes:
        if (round(zt, 4), code) not in found:
            errs.append(f"{code} not found at layer Z {zt} in sliced G-code")
    return errs


# --------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--profiles", help="Bambu Studio resources/profiles/BBL directory")
    ap.add_argument("--tag", default=TAG, help="BambuStudio git tag for downloaded profiles")
    ap.add_argument("--studio", help="bambu-studio.exe: headless-slice the tower projects and check the M104 lines")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    base = find_profile_dir(a.profiles)
    prof = Profiles(base, a.tag)
    if base:
        bbl = json.loads((base.parent / "BBL.json").read_text(encoding="utf-8")) if (base.parent / "BBL.json").exists() else {}
        print(f"System profiles: {base} (bundle {bbl.get('version', '?')})")
    else:
        print(f"System profiles: GitHub bambulab/BambuStudio {a.tag} (cache {prof.cache.relative_to(ROOT).as_posix()})")
    version = a.tag.lstrip("v")

    total_err = 0
    for nz in NOZZLES:
        outdir = OUT / nz
        if outdir.exists():
            for old in outdir.glob("*.3mf"):
                old.unlink()
        projs, skipped = projects_for(nz)
        print(f"\nNozzle {nz}: {len(projs)} projects -> {outdir.relative_to(ROOT).as_posix()}/")
        for pr in projs:
            dest = outdir / f"{pr.out_name}.3mf"
            rep = build_project(prof, pr, version, dest)
            errs = validate(dest, rep)
            m = TOWER_RE.match(pr.objects[0].stl.name)
            if m and pr.gcodes and not pr.objects[0].stl.name.startswith("temp_tower_compact_"):
                errs += check_against_markdown(nz, int(m.group(1)), int(m.group(2)), pr.gcodes)
                if a.studio:
                    errs += studio_slice_check(Path(a.studio), dest, pr.gcodes, Path(tempfile.gettempdir()) / "a1cal_3mf_slice")
            tris = sum(o["tris"] for o in rep["objects"])
            extra = ""
            if pr.gcodes:
                extra = (f"  {rep['filament']} @ {pr.fil_over['nozzle_temperature']} C, M104 at "
                         + ", ".join(f"{z:g}:{g.split('S')[1]}" for z, g in pr.gcodes))
            else:
                extra = f"  {rep['filament']}"
            status = "OK" if not errs else "FAIL: " + "; ".join(errs)
            print(f"  {dest.name:<48} {len(rep['objects'])} obj {tris:6d} tris  {status}{extra}")
            total_err += len(errs)
        for s in skipped:
            print(f"  skipped {s}" + (" (dev-mode calibration only, see docs/3mf-projects.md)" if s in SKIP
                                      else "  <-- no project rule for this STL"))
    print("\nAll projects valid." if not total_err else f"\n{total_err} problem(s).")
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main())
