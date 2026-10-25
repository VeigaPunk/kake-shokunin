#!/usr/bin/env python3
"""Round-57: fetch the two adopted Baidu pages once, retain the raw bytes and write receipts (sha256, bytes, status, UTC time)."""
import hashlib, json, subprocess, sys
from datetime import datetime, timezone
ROWS = {"S421": "https://ziyuan.baidu.com/college/articleinfo?id=3458", "S422": "https://ziyuan.baidu.com/wiki/867"}
UA = "kake-shokunin-round57"
out = {"schema": "kake-r57-source-receipts-v1", "sources": {}}
for sid, url in ROWS.items():
    p = subprocess.run(["curl", "-sL", "--compressed", "-A", UA, "--max-time", "60", "-o", f"{sys.argv[1]}/{sid}.html", "-w", "%{http_code}", url],
                       capture_output=True, text=True)
    raw = open(f"{sys.argv[1]}/{sid}.html", "rb").read()
    out["sources"][sid] = {"url": url, "httpStatus": int(p.stdout), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                           "fetchedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat(), "userAgent": UA}
json.dump(out, open(f"{sys.argv[1]}/receipts.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1))
