#!/usr/bin/env python3
"""Round-31 source opening (derived from round-30 fetch_sources.py, blob b9431a5f; ids, URLs and user agent changed): one public GET per declared source page.

Writes, under .ufo/waves/round-31/sources/: <id>.html.gz (received body),
<id>.txt (visible text: HTML minus script and style elements, tags removed,
entities decoded, whitespace collapsed) and receipts.json (URL, UTC time,
HTTP status, byte counts, sha256 of the body and of the text file).
Usage: python3 -B fetch_sources.py [--only S057,...]
Each receipt also names the sha256 of this fetcher file (fetcherSha256).
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent / "sources"
SOURCES = {
    "S057": "https://render.com/docs/blueprint-spec",
    "S058": "https://render.com/docs/web-services",
    "S059": "https://render.com/docs/docker",
    "S060": "https://render.com/docs/health-checks",
    "S061": "https://render.com/docs/configure-other-dns",
}
UA = "kake-shokunin-round-31-source-opening (one GET per page)"


def visible_text(body: str) -> str:
    t = re.sub(r"(?is)<(script|style)\b.*?</\1\s*>", " ", body)
    t = re.sub(r"(?s)<!--.*?-->", " ", t)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    only = {s for s in a.only.split(",") if s}
    OUT.mkdir(parents=True, exist_ok=True)
    rpath = OUT / "receipts.json"
    receipts = json.loads(rpath.read_text()) if rpath.exists() else {}
    for sid, url in SOURCES.items():
        if only and sid not in only:
            continue
        at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as resp:
            status = resp.status
            final = resp.geturl()
            body = resp.read()
        text = visible_text(body.decode("utf-8", "replace"))
        (OUT / f"{sid}.html.gz").write_bytes(gzip.compress(body, mtime=0))
        (OUT / f"{sid}.txt").write_text(text, encoding="utf-8")
        receipts[sid] = {
            "fetcherSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "url": url, "finalUrl": final, "accessedUtc": at, "status": status,
            "bodyBytes": len(body), "bodySha256": hashlib.sha256(body).hexdigest(),
            "textSha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "textWords": len(text.split()),
            "textRule": "HTML minus script/style, comments and tags removed, entities decoded, whitespace collapsed",
        }
        print(sid, status, len(body), at, url)
    rpath.write_text(json.dumps(receipts, indent=1, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
