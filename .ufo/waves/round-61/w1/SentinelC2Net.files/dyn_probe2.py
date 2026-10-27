#!/usr/bin/env python3
"""Second dynamic probe: cross-host redirect, private-target following, input hardening, timeout."""
from __future__ import annotations
import json, os, shutil, socket, subprocess, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOOL = "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/response_snapshot.py"
S = "/fast/scratch/hyaku/kake-r61/SentinelC2Net/dyn2"
HIT = []


class Redirector(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def do_GET(self):
        HIT.append(("public", self.path, self.headers.get("Host")))
        if self.path == "/to-localhost":
            self.send_response(302); self.send_header("Location", f"http://localhost:{PRIV_PORT}/secret")
            self.send_header("Content-Length", "0"); self.end_headers()
        else:
            self.send_response(200); self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", "2"); self.end_headers(); self.wfile.write(b"ok")


class Private(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def do_GET(self):
        HIT.append(("private", self.path, self.headers.get("Host")))
        body = b"INTERNAL-ADMIN-PANEL"
        self.send_response(200); self.send_header("Content-Type", "text/plain")
        self.send_header("X-Internal-Token", "shh-abc")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)


def run(pop, out, timeout=60, extra=None):
    cmd = [sys.executable, "-B", TOOL, "--population", pop, "--out", out] + (extra or [])
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=S)


def surfaces(spec, root):
    os.makedirs(root, exist_ok=True)
    for sid, url in spec.items():
        d = os.path.join(root, sid); os.makedirs(d, exist_ok=True)
        json.dump({"id": sid, "url": url}, open(os.path.join(d, "fetch.json"), "w"))
    return root


if __name__ == "__main__":
    shutil.rmtree(S, ignore_errors=True); os.makedirs(S)
    pub = ThreadingHTTPServer(("127.0.0.1", 0), Redirector)
    priv = ThreadingHTTPServer(("127.0.0.1", 0), Private)
    PRIV_PORT = priv.server_address[1]
    globals()["PRIV_PORT"] = PRIV_PORT
    for s in (pub, priv):
        threading.Thread(target=s.serve_forever, daemon=True).start()
    out = {}
    base = f"http://127.0.0.1:{pub.server_address[1]}"

    # A: cross-host redirect to a loopback "private" service
    pop = surfaces({"ssrf": base + "/to-localhost"}, os.path.join(S, "popA"))
    r = run(pop, os.path.join(S, "outA"))
    bodyp = os.path.join(S, "outA", "ssrf", "body.bin")
    rec = json.load(open(os.path.join(S, "outA", "ssrf", "response.json")))
    out["cross_host_redirect"] = {
        "exit": r.returncode, "hits": HIT[:], "status": rec["status"], "finalUrl": rec["finalUrl"],
        "redirects": rec["redirects"], "recorded_internal_body": open(bodyp, "rb").read().decode() if os.path.exists(bodyp) else None,
        "recorded_internal_header": [h for h in rec["headers"] if h["name"].lower() == "x-internal-token"],
        "error": rec["error"], "url": rec["url"]}

    # B: input hardening — userinfo URL, file: scheme, missing population
    HIT.clear()
    out["userinfo_url"] = {"exit": run(surfaces({"b": base + "/x"}, os.path.join(S, "p1")), os.path.join(S, "o1")).returncode}
    inj = os.path.join(S, "p2", "bad"); os.makedirs(inj, exist_ok=True)
    json.dump({"id": "bad", "url": "https://user:pw@example.com/"}, open(os.path.join(inj, "fetch.json"), "w"))
    out["userinfo_url"] = {"exit": run(os.path.join(S, "p2"), os.path.join(S, "o2")).returncode,
                           "stdout": run(os.path.join(S, "p2"), os.path.join(S, "o2")).stdout.strip()[:200]}
    inf = os.path.join(S, "p3", "f"); os.makedirs(inf, exist_ok=True)
    json.dump({"id": "f", "url": "file:///etc/passwd"}, open(os.path.join(inf, "fetch.json"), "w"))
    out["file_scheme"] = {"exit": run(os.path.join(S, "p3"), os.path.join(S, "o3")).returncode}
    out["missing_population"] = {"exit": run(os.path.join(S, "nope"), os.path.join(S, "o4")).returncode}
    out["unsafe_id"] = {"exit": None}
    unsafe = os.path.join(S, "p5", "x"); os.makedirs(unsafe, exist_ok=True)
    json.dump({"id": "../../etc", "url": base + "/x"}, open(os.path.join(unsafe, "fetch.json"), "w"))
    out["unsafe_id"] = {"exit": run(os.path.join(S, "p5"), os.path.join(S, "o5")).returncode}
    out["hits_after_input_tests"] = HIT[:]
    out["usage_exit"] = subprocess.run([sys.executable, "-B", TOOL, "--bogus"], capture_output=True, text=True).returncode

    # C: stall -> 20 s timeout
    class Stall(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *a):
            pass

        def do_GET(self):
            self.send_response(200); self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", "100"); self.end_headers()
            self.wfile.flush()
            time.sleep(45)

    stall = ThreadingHTTPServer(("127.0.0.1", 0), Stall)
    threading.Thread(target=stall.serve_forever, daemon=True).start()
    ps = surfaces({"stall": f"http://127.0.0.1:{stall.server_address[1]}/"}, os.path.join(S, "pop6"))
    t0 = time.time()
    rs = run(ps, os.path.join(S, "out6"), timeout=120)
    el = time.time() - t0
    recs = json.load(open(os.path.join(S, "out6", "stall", "response.json")))
    out["stall"] = {"exit": rs.returncode, "seconds": round(el, 1), "status": recs["status"],
                    "error": recs["error"], "bytes": recs["bytes"], "truncated": recs["truncated"],
                    "headers_kept": len(recs["headers"])}
    print(json.dumps(out, indent=1))
