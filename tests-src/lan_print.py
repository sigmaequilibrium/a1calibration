"""Send a sliced .gcode.3mf to the Bambu Lab A1 over the LAN (FTPS upload + MQTT project_file) without the GUI.

Reads the printer's serial, IP and LAN access code from OrcaSlicer's own config (never printed). Refuses to
start a job unless the printer reports IDLE, FINISH or FAILED (the last is what a cancelled job leaves).

  .venv/Scripts/python -I tests-src/lan_print.py --status
  .venv/Scripts/python -I tests-src/lan_print.py FILE.gcode.3mf [--timeout-s 40] [--no-level] [--flow-cali]

Needs paho-mqtt (pip install paho-mqtt in the repo .venv).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import socket
import ssl
import sys
import time
import zipfile
from ftplib import FTP, FTP_TLS
from pathlib import Path

import paho.mqtt.client as mqtt

CONF = Path(os.environ.get("ORCA_CONF", Path.home() / "AppData/Roaming/OrcaSlicer/OrcaSlicer.conf"))


def printer() -> tuple[str, str, str]:
    t = CONF.read_text(encoding="utf-8")
    ip = re.search(r'"?dev_ip"?\s*[=:]\s*"([\d.]+)"', t).group(1)
    sn = re.search(r'"?dev_id"?\s*[=:]\s*"([^"]+)"', t).group(1)
    code = re.search(r'"user_access_code"\s*:\s*\{[^}]*"%s"\s*:\s*"([^"]+)"' % re.escape(sn), t).group(1)
    return ip, sn, code


PIN_FILE = Path.home() / ".a1cal_printer_pins.json"


def pinned_context(ip: str, port: int) -> ssl.SSLContext:
    """TLS context that only accepts the printer certificate we pinned on first use (trust on first use).
    The pinned certificate is the sole trust anchor and is enforced by the handshake on the very connection that
    carries the access code, so a changed certificate makes the connection fail before any credential is sent.
    Delete PIN_FILE after resetting the printer."""
    pins = json.loads(PIN_FILE.read_text()) if PIN_FILE.exists() else {}
    key = f"{ip}:{port}:pem"
    if key not in pins:
        pem = ssl.get_server_certificate((ip, port))
        pins[key] = pem
        PIN_FILE.write_text(json.dumps(pins))
        try:
            os.chmod(PIN_FILE, 0o600)
        except OSError:
            pass
        fp = hashlib.sha256(ssl.PEM_cert_to_DER_cert(pem)).hexdigest()
        print(f"pinned {ip}:{port} certificate {fp[:16]}... (first use)")
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False                       # the printer cert is not issued for its IP
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.verify_flags |= ssl.VERIFY_X509_PARTIAL_CHAIN  # trust the pinned leaf itself
    ctx.load_verify_locations(cadata=pins[key])
    return ctx


def pin_check(ip: str) -> None:
    """Make sure both ports are pinned (first use only); enforcement happens in the real connections."""
    for port in (8883, 990):
        pinned_context(ip, port)


class ImplicitFTPS(FTP_TLS):
    """Bambu printers use implicit FTPS on port 990."""

    def connect(self, host="", port=990, timeout=60, source_address=None):
        self.host, self.port, self.timeout = host, port, timeout
        self.sock = socket.create_connection((host, port), timeout, source_address)
        self.af = self.sock.family
        self.sock = self.context.wrap_socket(self.sock, server_hostname=host)
        self.file = self.sock.makefile("r", encoding=self.encoding)
        self.welcome = self.getresp()
        return self.welcome

    def ntransfercmd(self, cmd, rest=None):
        conn, size = FTP.ntransfercmd(self, cmd, rest)      # not FTP_TLS's: it would wrap the socket twice
        if self._prot_p:
            conn = self.context.wrap_socket(conn, server_hostname=self.host, session=self.sock.session)
        return conn, size


def connect_mqtt(ip: str, sn: str, code: str):
    state: dict = {}
    c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"a1cal-{int(time.time())}")
    c.username_pw_set("bblp", code)
    c.tls_set_context(pinned_context(ip, 8883))

    def on_message(_c, _u, msg):
        try:
            p = json.loads(msg.payload).get("print", {})
        except ValueError:
            return
        state.update({k: v for k, v in p.items() if k in (
            "gcode_state", "mc_percent", "layer_num", "total_layer_num", "gcode_file", "subtask_name",
            "mc_remaining_time", "nozzle_temper", "bed_temper", "print_error", "command", "result", "reason")})

    c.on_message = on_message
    c.on_connect = lambda cl, *_: cl.subscribe(f"device/{sn}/report")
    c.connect(ip, 8883, 30)
    c.loop_start()
    return c, state


def wait_state(c, sn, state, secs=10):
    t0 = time.time()
    while time.time() - t0 < secs and "gcode_state" not in state:
        c.publish(f"device/{sn}/request", json.dumps({"pushing": {"sequence_id": "1", "command": "pushall"}}))
        time.sleep(2)
    return state


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--timeout-s", type=int, default=45)
    ap.add_argument("--no-level", action="store_true", help="skip auto bed levelling")
    ap.add_argument("--flow-cali", action="store_true", help="enable the printer's flow calibration")
    a = ap.parse_args()
    ip, sn, code = printer()
    pin_check(ip)
    c, st = connect_mqtt(ip, sn, code)
    wait_state(c, sn, st)
    print("printer:", {k: st.get(k) for k in ("gcode_state", "mc_percent", "layer_num", "total_layer_num",
                                              "subtask_name", "nozzle_temper", "bed_temper")})
    if a.status or not a.file:
        c.loop_stop()
        return 0
    if st.get("gcode_state") not in ("IDLE", "FINISH", "FAILED"):
        print("printer is not idle/finished; not sending")
        c.loop_stop()
        return 2
    f = Path(a.file)
    name = f.name
    md5 = hashlib.md5(f.read_bytes()).hexdigest().upper()
    plate_gcode = next(n for n in zipfile.ZipFile(f).namelist() if re.fullmatch(r"Metadata/plate_\d+\.gcode", n))   # plate_1 unless a later plate was sliced
    ftp = ImplicitFTPS(context=pinned_context(ip, 990))
    ftp.connect(ip, 990, timeout=60)
    ftp.login("bblp", code)
    ftp.prot_p()
    conn = ftp.transfercmd(f"STOR {name}")
    with f.open("rb") as fh:
        while chunk := fh.read(65536):
            conn.sendall(chunk)
    conn.close()        # the printer never answers the TLS close_notify, so no unwrap()
    try:
        ftp.voidresp()
    except (OSError, ssl.SSLError):
        pass
    print("uploaded", name, [x for x in ftp.nlst() if x == name])
    try:
        ftp.quit()
    except (OSError, ssl.SSLError):
        pass
    st.pop("command", None)
    st.pop("result", None)
    cmd = {"print": {
        "sequence_id": "20", "command": "project_file", "param": plate_gcode,
        "project_id": "0", "profile_id": "0", "task_id": "0", "subtask_id": "0",
        "subtask_name": name.replace(".gcode.3mf", ""), "file": "", "url": f"file:///sdcard/{name}",
        "md5": md5, "timelapse": False, "bed_type": "textured_plate",
        "bed_leveling": not a.no_level, "flow_cali": a.flow_cali, "vibration_cali": False,
        "layer_inspect": False, "use_ams": False, "ams_mapping": [], "skip_objects": None}}
    c.publish(f"device/{sn}/request", json.dumps(cmd))
    t0 = time.time()
    while time.time() - t0 < a.timeout_s:
        time.sleep(2)
        c.publish(f"device/{sn}/request", json.dumps({"pushing": {"sequence_id": "2", "command": "pushall"}}))
        print(f"  {int(time.time() - t0):3d}s", {k: st.get(k) for k in (
            "gcode_state", "mc_percent", "layer_num", "subtask_name", "nozzle_temper", "bed_temper", "print_error")})
        if st.get("gcode_state") in ("PREPARE", "RUNNING"):
            print("print started")
            c.loop_stop()
            return 0
    print("printer did not start within the timeout")
    c.loop_stop()
    return 3


if __name__ == "__main__":
    sys.exit(main())
