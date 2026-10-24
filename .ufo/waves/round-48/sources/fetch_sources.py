#!/usr/bin/env python3
"""Round-48 source fetcher — re-opens the four sources of the render-queue theme.

Contract:
  * one GET per URL, no retries, no writes outside this directory;
  * each receipt names the URL, the HTTP status, the byte count, the sha256 of
    the retained raw body and the sha256 of the retained visible text, the
    access timestamp (UTC) and the sha256 of this fetcher;
  * exit 0 when every fetch returned 200 and both digests were written,
    1 when a fetch failed (the receipt still records what was seen), 64 on a
    usage error.

Usage: python3 -B fetch_sources.py [--out DIR]
"""
import argparse
import hashlib
import html as htmllib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

SOURCES = [
    ("S137", "https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics"),
    ("S138", "https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics?hl=zh-cn"),
    ("S139", "https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics?hl=ja"),
    ("S249", "https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering"),
]

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

TAG = re.compile(r"(?is)<(script|style|noscript|template)\b[^>]*>.*?</\1\s*>")
ANY_TAG = re.compile(r"(?s)<[^>]*>")
WS = re.compile(r"[ \t 　]+")


def visible_text(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace")
    text = TAG.sub(" ", text)
    text = ANY_TAG.sub(" ", text)
    text = htmllib.unescape(text)
    lines = [WS.sub(" ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args()
    out = args.out
    os.makedirs(out, exist_ok=True)
    fetcher_sha = hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest()
    receipts = []
    ok = True
    for sid, url in SOURCES:
        started = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        status = None
        body = b""
        error = None
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                status = resp.status
                body = resp.read()
        except urllib.error.HTTPError as exc:  # pragma: no cover - network path
            status = exc.code
            body = exc.read() if hasattr(exc, "read") else b""
            error = f"HTTPError {exc.code}"
        except Exception as exc:  # pragma: no cover - network path
            error = f"{type(exc).__name__}: {exc}"
        raw_path = os.path.join(out, f"{sid}.html")
        txt_path = os.path.join(out, f"{sid}.txt")
        if body:
            with open(raw_path, "wb") as fh:
                fh.write(body)
            text = visible_text(body)
            with open(txt_path, "w", encoding="utf-8") as fh:
                fh.write(text)
        else:
            text = ""
        receipts.append(
            {
                "id": sid,
                "url": url,
                "status": status,
                "bytes": len(body),
                "rawSha256": hashlib.sha256(body).hexdigest() if body else None,
                "textSha256": hashlib.sha256(text.encode("utf-8")).hexdigest() if text else None,
                "rawPath": os.path.basename(raw_path) if body else None,
                "textPath": os.path.basename(txt_path) if text else None,
                "accessedAt": started,
                "error": error,
                "fetcherSha256": fetcher_sha,
            }
        )
        if status != 200 or not body:
            ok = False
    with open(os.path.join(out, "receipts.json"), "w", encoding="utf-8") as fh:
        json.dump({"schema": "kake-r48-source-receipts-v1", "receipts": receipts}, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    for r in receipts:
        print(f"{r['id']} status={r['status']} bytes={r['bytes']} textSha256={r['textSha256']} error={r['error']}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
