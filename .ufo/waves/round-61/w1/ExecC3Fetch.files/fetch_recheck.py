#!/usr/bin/env python3
"""Round-61 C3 recheck fetcher (seat ExecC3Fetch).

One GET per due row S001-S010 (the row's primary URL from corpus/SOURCES.md).
Fetch ethics (contract 61): GET only, no cookies/credentials/body, <=5 redirects,
20 s timeout, 2 MiB body cap. Bodies land in
.ufo/waves/round-61/recheck/<id>.html; one receipt per row is appended to
.ufo/waves/round-61/recheck/receipts.json ({"receipts": [...]}), created empty if
absent.

Usage: python3 -B fetch_recheck.py --out-dir <recheck dir> [--only S00x]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "round61"
CAP = 2 * 1024 * 1024
MAX_HOPS = 5
TIMEOUT = 20.0
DELAY = 1.0

# The row's primary URL (first URL of the row's `source` cell) as the row stands
# in corpus/SOURCES.md at 9f07731a. S010's cell carries a fragment; the
# fragment is not sent on the wire.
ROWS = [
    ("S001", "https://raw.githubusercontent.com/actions/upload-pages-artifact/7b1f4a764d45c48632c6b24a0339c27f5614fb0b/action.yml"),
    ("S002", "https://github.com/actions/upload-pages-artifact/releases/tag/v4.0.0"),
    ("S003", "https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site"),
    ("S004", "https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages"),
    ("S005", "https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site"),
    ("S006", "https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll"),
    ("S007", "https://docs.github.com/en/rest/pages/pages"),
    ("S008", "https://cgit.git.savannah.gnu.org/cgit/tar.git/plain/doc/tar.texi?id=cfdb891bbd68c920ea75210977593f3cd08f0418"),
    ("S009", "https://raw.githubusercontent.com/nginx/nginx/release-1.28.0/src/http/ngx_http_core_module.c"),
    ("S010", "https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8"),
]


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


class NoCookies(urllib.request.HTTPCookieProcessor):
    pass


def make_opener() -> urllib.request.OpenerDirector:
    # Explicit: no cookie jar, no proxy juggling, redirects followed by hand.
    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent", UA), ("Accept-Encoding", "identity")]
    return opener


def fetch(url: str) -> dict:
    """GET url, following at most MAX_HOPS redirects. Returns a record dict."""
    wire_url = urllib.parse.urldefrag(url)[0]
    current = wire_url
    hops = 0
    opener = make_opener()
    while True:
        req = urllib.request.Request(current, method="GET")
        req.add_header("User-Agent", UA)
        req.add_header("Accept-Encoding", "identity")
        try:
            with opener.open(req, timeout=TIMEOUT) as resp:
                status = resp.status
                body = resp.read(CAP + 1)
                truncated = len(body) > CAP
                if truncated:
                    body = body[:CAP]
                return {
                    "status": status,
                    "effectiveUrl": current,
                    "body": body,
                    "truncated": truncated,
                    "hops": hops,
                }
        except urllib.error.HTTPError as exc:
            if exc.code in (301, 302, 303, 307, 308):
                loc = exc.headers.get("Location")
                if not loc:
                    raise RuntimeError(f"redirect {exc.code} without Location at {current}")
                if hops >= MAX_HOPS:
                    raise RuntimeError(f"redirect limit {MAX_HOPS} exceeded at {current}")
                current = urllib.parse.urljoin(current, loc)
                hops += 1
                continue
            body = b""
            try:
                body = exc.read(CAP)[:CAP]
            except Exception:  # noqa: BLE001 - error body is optional
                body = b""
            return {
                "status": exc.code,
                "effectiveUrl": current,
                "body": body,
                "truncated": False,
                "hops": hops,
            }
        except Exception as exc:  # noqa: BLE001 - transport fault
            raise RuntimeError(f"{type(exc).__name__}: {exc} at {current}") from exc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--only", default=None)
    args = ap.parse_args()

    out = pathlib.Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    receipts_path = out / "receipts.json"
    if receipts_path.exists():
        data = json.loads(receipts_path.read_text(encoding="utf-8"))
        if "receipts" not in data or not isinstance(data["receipts"], list):
            raise SystemExit(f"{receipts_path}: unexpected shape")
    else:
        data = {"receipts": []}

    failures = []
    for ident, url in ROWS:
        if args.only and ident != args.only:
            continue
        try:
            rec = fetch(url)
        except RuntimeError as exc:
            failures.append({"id": ident, "url": url, "error": str(exc)})
            print(f"{ident} FAIL {exc}", flush=True)
            time.sleep(DELAY)
            continue
        body = rec["body"]
        (out / f"{ident}.html").write_bytes(body)
        entry = {
            "id": ident,
            "url": url,
            "effectiveUrl": rec["effectiveUrl"],
            "status": rec["status"],
            "sha256": hashlib.sha256(body).hexdigest(),
            "bytes": len(body),
            "fetchedAt": utcnow(),
            "userAgent": UA,
        }
        data["receipts"] = [r for r in data["receipts"] if r.get("id") != ident]
        data["receipts"].append(entry)
        receipts_path.write_text(json.dumps(data, indent=1, sort_keys=False) + "\n", encoding="utf-8")
        print(
            f"{ident} {rec['status']} {len(body)}B hops={rec['hops']} trunc={rec['truncated']} "
            f"sha={entry['sha256'][:12]} eff={rec['effectiveUrl']}",
            flush=True,
        )
        time.sleep(DELAY)
    if failures:
        print(json.dumps(failures, indent=1), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
