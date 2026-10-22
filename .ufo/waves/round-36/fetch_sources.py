#!/usr/bin/env python3
"""Round-36 source opening (copied from round-35 fetch_sources.py; only ids,
URLs, the docstring round and the user agent changed): one public GET per source page.

Writes, under .ufo/waves/round-36/sources/: <id>.html.gz (received body),
<id>.txt (visible text: HTML minus script and style elements, comments and
tags removed, entities decoded, whitespace collapsed) and receipts.json (URL,
final URL, UTC time, HTTP status, byte counts, sha256 of the body and of the
text file). Each receipt also names the sha256 of this fetcher file.
Usage: python3 -B fetch_sources.py [--only S088,...]
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
import urllib.error
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent / "sources"
SOURCES = {
    "S088": "https://www.rfc-editor.org/rfc/rfc9110.html#section-15.4",
    "S089": "https://www.rfc-editor.org/rfc/rfc3986.html#section-5.2",
    "S090": "https://encoding.spec.whatwg.org/",
    "S091": "https://www.unicode.org/reports/tr15/",
    "S092": "https://html.spec.whatwg.org/multipage/syntax.html#elements-2",
    "S093": "https://en.wikipedia.org/wiki/HTTP_301",
    "S094": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Redirections",
}
UA = "kake-shokunin-round-36-source-opening (one GET per page)"


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
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                status, final, body = resp.status, resp.geturl(), resp.read()
        except urllib.error.HTTPError as e:
            status, final, body = e.code, e.geturl(), e.read()
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
        print(sid, status, len(body), at, final)
    rpath.write_text(json.dumps(receipts, indent=1, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
