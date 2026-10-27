#!/usr/bin/env python3
"""Round-60: fetch the three Google pages of claim C3 once, retain the raw bytes and write receipts (sha256, bytes, status, UTC time).
S427 = re-open of the S425 URL (the superseding row of routed defect R59-D4); S428 = the user-triggered fetchers category page (lane-found:
linked from the S426 page's category table); S429 = the robots.txt introduction (staged S415, renumbered by document).
Usage: fetch_sources.py <new directory>; refuses to overwrite an existing receipts.json (the retained bodies are pinned by sha256)."""
import hashlib, json, os, subprocess, sys
from datetime import datetime, timezone
ROWS = {"S427": "https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers",
        "S428": "https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers",
        "S429": "https://developers.google.com/search/docs/crawling-indexing/robots/intro"}
UA = "kake-shokunin-round60"
if len(sys.argv) != 2 or os.path.exists(os.path.join(sys.argv[1], "receipts.json")):
    sys.exit("usage: fetch_sources.py <new directory>; refuses to overwrite an existing receipts.json (the retained bodies are pinned by sha256)")
os.makedirs(sys.argv[1], exist_ok=True)
out = {"schema": "kake-r60-source-receipts-v1", "sources": {}}
for sid, url in ROWS.items():
    p = subprocess.run(["curl", "-sL", "--compressed", "-A", UA, "--max-time", "60", "-o", f"{sys.argv[1]}/{sid}.html", "-w", "%{http_code} %{url_effective}", url],
                       capture_output=True, text=True)
    code, eff = (p.stdout.split(" ", 1) + [""])[:2]
    if p.returncode != 0 or code != "200" or eff != url:
        sys.exit(f"fetch of {url} failed: curl exit {p.returncode}, HTTP/effective {p.stdout!r}")
    raw = open(f"{sys.argv[1]}/{sid}.html", "rb").read()
    out["sources"][sid] = {"url": url, "httpStatus": int(code), "effectiveUrl": eff, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                           "fetchedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat(), "userAgent": UA}
json.dump(out, open(f"{sys.argv[1]}/receipts.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1))
