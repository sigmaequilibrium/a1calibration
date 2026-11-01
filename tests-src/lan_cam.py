"""Grab one JPEG frame from the Bambu Lab A1 chamber camera over the LAN (TLS port 6000).

  .venv/Scripts/python -I tests-src/lan_cam.py [OUT.jpg]

Reads the printer address and access code from Orca's config (never printed). The printer's certificate is
pinned (trust on first use) in the file lan_print.py maintains, checked on the connection that sends the code.
"""
from __future__ import annotations

import hashlib
import json
import socket
import ssl
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lan_print as lp  # noqa: E402

PORT = 6000


def main() -> int:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "cam.jpg")
    ip, _sn, code = lp.printer()
    pins = json.loads(lp.PIN_FILE.read_text()) if lp.PIN_FILE.exists() else {}
    key = f"{ip}:{PORT}"
    ctx = ssl._create_unverified_context()
    with socket.create_connection((ip, PORT), 10) as raw, ctx.wrap_socket(raw, server_hostname=ip) as s:
        # pin the certificate of THIS connection before the access code is sent on it
        fp = hashlib.sha256(s.getpeercert(binary_form=True)).hexdigest()
        if pins.setdefault(key, fp) != fp:
            raise SystemExit(f"certificate for {key} changed; not sending the access code")
        lp.PIN_FILE.write_text(json.dumps(pins))
        s.settimeout(15)
        s.sendall(struct.pack("<IIII", 0x40, 0x3000, 0, 0) + b"bblp".ljust(32, b"\0") + code.encode().ljust(32, b"\0"))
        hdr = b""
        while len(hdr) < 16:
            hdr += s.recv(16 - len(hdr))
        n = struct.unpack("<I", hdr[:4])[0]
        buf = b""
        while len(buf) < n:
            buf += s.recv(n - len(buf))
    if not (buf[:2] == b"\xff\xd8" and buf[-2:] == b"\xff\xd9"):
        raise SystemExit("did not receive a JPEG frame")
    out.write_bytes(buf)
    print("saved", out, len(buf), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
