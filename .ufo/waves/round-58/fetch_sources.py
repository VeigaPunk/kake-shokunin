#!/usr/bin/env python3
"""Round-58: fetch the two Baidu crawler-identification pages (S423 = staged S395, renumbered by document; S424 lane-found, linked from S423) once, retain the raw bytes and write receipts (sha256, bytes, status, UTC time)."""
import hashlib, json, os, subprocess, sys
from datetime import datetime, timezone
ROWS = {"S423": "https://ziyuan.baidu.com/college/articleinfo?id=3457", "S424": "https://ziyuan.baidu.com/college/articleinfo?id=3028"}
UA = "kake-shokunin-round58"
if len(sys.argv) != 2 or os.path.exists(os.path.join(sys.argv[1], "receipts.json")):
    sys.exit("usage: fetch_sources.py <new directory>; refuses to overwrite an existing receipts.json (the retained bodies are pinned by sha256)")
os.makedirs(sys.argv[1], exist_ok=True)
out = {"schema": "kake-r58-source-receipts-v1", "sources": {}}
for sid, url in ROWS.items():
    p = subprocess.run(["curl", "-sL", "--compressed", "-A", UA, "--max-time", "60", "-o", f"{sys.argv[1]}/{sid}.html", "-w", "%{http_code}", url],
                       capture_output=True, text=True)
    if p.returncode != 0 or p.stdout.strip() != "200":
        sys.exit(f"fetch of {url} failed: curl exit {p.returncode}, HTTP {p.stdout!r}")
    raw = open(f"{sys.argv[1]}/{sid}.html", "rb").read()
    out["sources"][sid] = {"url": url, "httpStatus": int(p.stdout), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                           "fetchedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat(), "userAgent": UA}
json.dump(out, open(f"{sys.argv[1]}/receipts.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1))
