#!/usr/bin/env python3
"""Dynamic network-surface proof for response_snapshot.py, run against a loopback fixture server."""
from __future__ import annotations
import hashlib, json, os, shutil, subprocess, sys, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOOL = "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/response_snapshot.py"
S = "/fast/scratch/hyaku/kake-r61/SentinelC2Net/dyn"
LOG = []          # (method, path, headers dict, body_len)
HITS = []
BIG = b"x" * (3 * 1024 * 1024)


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def do_POST(self):  # any non-GET would land here
        LOG.append(("POST", self.path, dict(self.headers), int(self.headers.get("Content-Length") or 0)))
        self.send_response(405); self.send_header("Content-Length", "0"); self.end_headers()

    do_PUT = do_DELETE = do_POST

    def do_GET(self):
        n = int(self.headers.get("Content-Length") or 0)
        body_read = b""
        if n:
            body_read = self.rfile.read(n)
        LOG.append(("GET", self.path, dict(self.headers), len(body_read)))
        HITS.append(self.path)
        p = self.path
        if p == "/dup":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Type", "text/plain")
            self.send_header("Set-Cookie", "a=1")
            self.send_header("Set-Cookie", "b=2")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Length", "2")
            self.end_headers()
            self.wfile.write(b"ok")
        elif p == "/redir":
            self.send_response(302); self.send_header("Location", "/dup"); self.send_header("Content-Length", "0"); self.end_headers()
        elif p.startswith("/hop/"):
            k = int(p.rsplit("/", 1)[1])
            if k >= 8:
                self.send_response(200); self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", "2"); self.end_headers(); self.wfile.write(b"ok")
            else:
                self.send_response(302); self.send_header("Location", f"/hop/{k+1}")
                self.send_header("Content-Length", "0"); self.end_headers()
        elif p == "/big":
            self.send_response(200); self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(BIG))); self.end_headers()
            self.wfile.write(BIG)
        elif p == "/empty":
            self.send_response(204); self.send_header("Content-Length", "0"); self.end_headers()
        elif p == "/file":
            self.send_response(302); self.send_header("Location", "file:///etc/passwd"); self.send_header("Content-Length", "0"); self.end_headers()
        else:
            self.send_response(404); self.send_header("Content-Length", "0"); self.end_headers()


def run(population, out, timeout=120):
    r = subprocess.run([sys.executable, "-B", TOOL, "--population", population, "--out", out],
                       capture_output=True, text=True, timeout=timeout, cwd="/fast/scratch/hyaku/kake-r61/SentinelC2Net")
    return r


def main():
    shutil.rmtree(S, ignore_errors=True)
    os.makedirs(S)
    srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{port}"
    pop = os.path.join(S, "pop")
    out = os.path.join(S, "out")
    surfaces = {"dup": "/dup", "redir": "/redir", "hop": "/hop/0", "big": "/big",
                "empty": "/empty", "file": "/file", "missing": "/nope"}
    for sid, path in surfaces.items():
        d = os.path.join(pop, sid)
        os.makedirs(d, exist_ok=True)
        json.dump({"id": sid, "url": base + path}, open(os.path.join(d, "fetch.json"), "w"))
    pre = set()
    for root, dirs, files in os.walk("/tmp"):
        for f in files:
            pre.add(os.path.join(root, f))
    r = run(pop, out)
    result = {"exit": r.returncode, "stdout": r.stdout[-4000:], "stderr": r.stderr[-2000:], "requests": [], "receipts": {}}
    seen = {}
    for m, p, h, bl in LOG:
        seen.setdefault(p, []).append(m)
    result["requests"] = [{"path": p, "methods": ms} for p, ms in sorted(seen.items())]
    result["request_count"] = len(LOG)
    result["cookie_header_sent"] = any(any(k.lower() == "cookie" for k in h) for _, _, h, _ in LOG)
    result["ua_seen"] = sorted({h.get("User-Agent") for _, _, h, _ in LOG})
    result["body_sent"] = sum(bl for _, _, _, bl in LOG)
    for sid in surfaces:
        p = os.path.join(out, sid, "response.json")
        row = {"file": os.path.exists(p)}
        if row["file"]:
            v = json.load(open(p))
            row.update({"status": v.get("status"), "bytes": v.get("bytes"), "truncated": v.get("truncated"),
                        "redirects": len(v.get("redirects") or []), "error": v.get("error"),
                        "headers": v.get("headers"), "bodyFile": v.get("bodyFile")})
            bf = os.path.join(out, sid, "body.bin")
            if os.path.exists(bf):
                b = open(bf, "rb").read()
                row["body_len"] = len(b)
                row["sha_match"] = hashlib.sha256(b).hexdigest() == v.get("sha256") and len(b) == v.get("bytes")
            row["sha_len_match"] = row.get("body_len", 0) == v.get("bytes")
        result["receipts"][sid] = row
    post = set()
    for root, dirs, files in os.walk("/tmp"):
        for f in files:
            post.add(os.path.join(root, f))
    result["tmp_new_files"] = sorted(post - pre)
    # writes outside out: snapshot of the lane capture tree
    result["stray_in_lane"] = subprocess.run(
        ["find", "/home/vgpnk/Projects/shokunin/kake-shokunin", "-newermt", "-3 minutes", "-type", "f",
         "-not", "-path", "*/.git/*", "-not", "-path", "*/.jj/*", "-not", "-path", "*/.ufo/waves/round-61/capture/*"],
        capture_output=True, text=True).stdout.splitlines()
    print(json.dumps(result, indent=1))
    srv.shutdown()


if __name__ == "__main__":
    main()
