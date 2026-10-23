#!/usr/bin/env python3
"""Record the served /robots.txt of the hosts named in the round-37 C1 assignment.

One request per host, User-Agent naming kake-shokunin round 37, >=1 s apart,
30 s timeout, max 5 redirects. GET only. No retries (a retry is a second request).
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

HOSTS = [
    "www.rfc-editor.org",
    "developers.google.com",
    "github.com",
    "docs.github.com",
    "www.sitemaps.org",
    "developer.mozilla.org",
    "en.wikipedia.org",
    "www.robotstxt.org",
    "html.spec.whatwg.org",
    "pages.github.com",
    "ds4cc.com",
    "veigapunk.github.io",
]
UA = "kake-shokunin-round37/1.0 (robots.txt snapshot; +https://github.com/veigapunk)"
OUT = "/fast/scratch/hyaku/kake-r37w1/ExecLiveRobotsSnapshot/robots"
HEAD = "/fast/scratch/hyaku/kake-r37w1/ExecLiveRobotsSnapshot/raw"

os.makedirs(OUT, exist_ok=True)
os.makedirs(HEAD, exist_ok=True)

receipts = []
for i, host in enumerate(HOSTS):
    if i:
        time.sleep(1.1)
    url = f"https://{host}/robots.txt"
    body = os.path.join(OUT, f"{host.replace('.', '_')}.txt")
    hdr = os.path.join(HEAD, f"{host.replace('.', '_')}.headers")
    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cmd = [
        "curl", "-sS", "-L", "--max-redirs", "5", "--max-time", "30",
        "-A", UA,
        "-o", body, "-D", hdr,
        "-w", "%{http_code}\t%{url_effective}\t%{num_redirects}\t%{size_download}\t%{content_type}",
        url,
    ]
    t0 = time.monotonic()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = round(time.monotonic() - t0, 3)
    fields = proc.stdout.rstrip("\n").split("\t") if proc.stdout.strip() else []
    status = int(fields[0]) if fields and fields[0].isdigit() else None
    final_url = fields[1] if len(fields) > 1 else url
    redirects = int(fields[2]) if len(fields) > 2 and fields[2].isdigit() else None
    size = os.path.getsize(body) if os.path.exists(body) else 0
    data = open(body, "rb").read() if os.path.exists(body) else b""
    rec = {
        "url": url,
        "finalUrl": final_url,
        "status": status,
        "bytes": size,
        "sha256": hashlib.sha256(data).hexdigest(),
        "timeUtc": started,
        "completedUtc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "contentType": fields[4] if len(fields) > 4 else None,
        "redirects": redirects,
        "curlExit": proc.returncode,
        "elapsedSeconds": elapsed,
        "userAgent": UA,
        "body": os.path.basename(body),
        "headers": os.path.relpath(hdr, OUT),
        "stderr": proc.stderr.strip() or None,
    }
    receipts.append(rec)
    print(json.dumps({k: rec[k] for k in ("url", "status", "finalUrl", "bytes", "redirects", "curlExit", "elapsedSeconds")}), flush=True)

with open(os.path.join(OUT, "receipts.json"), "w", encoding="utf-8") as fh:
    json.dump({"version": 1, "fetchedUtc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "receipts": receipts}, fh, indent=2, sort_keys=False)
    fh.write("\n")
print("receipts:", len(receipts), file=sys.stderr)
