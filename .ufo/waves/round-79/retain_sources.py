#!/usr/bin/env python3
"""Round-79 source retainer — one public GET per candidate, raw bytes kept under sources/.

Writes sources/<slug>.raw (bytes as served), sources/<slug>.txt (tag-stripped text with
line numbers in a sidecar-free layout), and sources/receipts.json (url, final URL, HTTP
status, bytes, sha256 of raw, fetched-at UTC). Read-only against the network; writes only
under the directory it lives in.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "sources"
UA = "kake-round79-source-open/1.0 (shokunin lane, one GET per candidate)"

CANDIDATES = [
    ("S452-mdn-x-robots-tag", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Robots-Tag"),
    ("reject-rfc9309", "https://www.rfc-editor.org/rfc/rfc9309.txt"),
]


def strip_text(raw: bytes) -> str:
    s = raw.decode("utf-8", "replace")
    s = re.sub(r"(?is)<(script|style|svg)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    t = html.unescape(s)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    receipts = []
    for slug, url in CANDIDATES:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=45) as r:
            raw = r.read()
            status = r.status
            final = r.geturl()
        fetched = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        (OUT / f"{slug}.raw").write_bytes(raw)
        text = strip_text(raw)
        (OUT / f"{slug}.txt").write_text(text, encoding="utf-8")
        rec = {
            "slug": slug,
            "requested": url,
            "url": final,
            "status": status,
            "bytes": len(raw),
            "raw_sha256": hashlib.sha256(raw).hexdigest(),
            "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "fetched_at": fetched,
            "text_lines": text.count("\n") + 1,
        }
        receipts.append(rec)
        print(json.dumps(rec, sort_keys=True))
    (OUT / "receipts.json").write_text(json.dumps(receipts, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
