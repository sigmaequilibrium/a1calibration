"""Insert `M900 K<k> L1000 M10` after each '; printing object pa_K<k>' comment in a sliced .gcode.3mf.
Usage: orange_pa_pattern_post.py IN.gcode.3mf OUT.gcode.3mf"""
import hashlib, re, sys, zipfile

src, dst = sys.argv[1:3]
zin = zipfile.ZipFile(src)
g = zin.read("Metadata/plate_1.gcode").decode()
g, n = re.subn(r"(; printing object pa_K([0-9.]+) id:\d+ copy \d+\n)", lambda m: f"{m.group(1)}M900 K{m.group(2)} L1000 M10\n", g)
print("inserted", n)
with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
    for i in zin.infolist():
        d = zin.read(i.filename)
        if i.filename == "Metadata/plate_1.gcode":
            d = g.encode()
        elif i.filename == "Metadata/plate_1.gcode.md5":
            d = hashlib.md5(g.encode()).hexdigest().upper().encode()
        z.writestr(i.filename, d)
