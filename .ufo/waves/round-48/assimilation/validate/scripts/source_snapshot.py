#!/usr/bin/env python3
"""Record live source fetches as a round-36 C1 manifest.

Input: a JSON list of {"id": ..., "url": ..., "quote": ...}.
Output: a version-1 manifest exactly as the C1 public contract in SCORECARD.md
("Round 36 - declared claims") describes it:

    {"version": 1, "checks": [check, ...]}
    check = {"id": str, "url": str, "quote": str,
             "hops": [{"status": int, "location": str}, ...]}
    plus "contentType" (str) and "body" (relative path, regular file inside the
    manifest's directory) when the last hop's status is 200.

Redirect hops are recorded with the raw Location header value; the contract
resolves each location against the URL that hop answered. The recorder resolves
it itself (RFC 3986 section 5.2, urllib.parse.urljoin) only to know where to
fetch next.

Fetch rules: GET only, redirects are not followed by urllib (a no-redirect
handler raises HTTPError for every 3xx so the hop can be recorded), at most 8
redirect hops are followed, the chain stops at the first non-redirect status,
one request per second, 30 s timeouts, one User-Agent naming kake-shokunin
round 36. Bodies are capped at 8 MiB.

A check is emitted only when it can be recorded honestly: the final hop must be
a non-redirect status, a redirect must carry a Location, and a 200 body must fit
the cap. Anything else is written to the sidecar receipts file instead of being
guessed at.

Usage:
    python3 source_snapshot.py --input INPUT.json --out-dir DIR [--manifest PATH]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import http.client
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

UA = "kake-shokunin-round-36-source-snapshot (one GET per source)"
REDIRECT_STATUSES = {301, 302, 303, 307, 308}
MAX_HOPS = 8
MAX_BODY = 8 * 1024 * 1024
TIMEOUT = 30.0
DELAY = 1.0
BODY_SUBDIR = "bodies"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Never follow a redirect: return None so urllib raises HTTPError."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D102
        return None


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_name(ident: str) -> str:
    """A filesystem-safe body name for a check id (no traversal, no collisions)."""
    cleaned = re.sub(r"[^A-Za-z0-9._-]", "_", ident)
    cleaned = cleaned.strip("._") or "check"
    if cleaned != ident:
        cleaned = f"{cleaned}-{hashlib.sha256(ident.encode('utf-8')).hexdigest()[:8]}"
    return cleaned


def valid_url(url: str) -> bool:
    """An absolute http(s) URL with a host and no userinfo (as the contract wants)."""
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError:
        return False
    return (
        parts.scheme in ("http", "https")
        and bool(parts.netloc)
        and parts.username is None
        and parts.password is None
    )


_LAST_REQUEST = 0.0


def fetch_once(opener, url: str, timeout: float) -> tuple[int, object, bytes]:
    """One GET without following redirects. Returns (status, headers, body)."""
    global _LAST_REQUEST
    req = urllib.request.Request(
        url,
        # Accept-Language added by the L1 after wave-2 ReopenFlagS068: without it
        # developers.facebook.com served a Portuguese page; matches fetch_sources.py.
        headers={"User-Agent": UA, "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9"},
        method="GET",
    )
    try:
        with opener.open(req, timeout=timeout) as resp:
            body = resp.read(MAX_BODY + 1)
            _LAST_REQUEST = time.monotonic()
            return resp.status, resp.headers, body
    except urllib.error.HTTPError as exc:  # every 3xx and every 4xx/5xx lands here
        body = exc.read(MAX_BODY + 1)
        _LAST_REQUEST = time.monotonic()
        return exc.code, exc.headers, body


class FetchFailure(Exception):
    """The request could not be completed (no status to record)."""


def record(opener, url: str, timeout: float, delay: float, max_hops: int):
    """Walk the redirect chain. Returns a dict describing the fetch.

    Each hop records the raw Location header value (the contract resolves
    each location against the URL that hop answered) plus, in `resolved`, the
    RFC 3986 section 5.2 resolution of that location, for the receipts.
    """
    hops: list[dict] = []
    resolved: list[str] = []
    current = url
    followed = 0
    for _ in range(max_hops + 1):
        wait = delay - (time.monotonic() - _LAST_REQUEST)
        if wait > 0:
            time.sleep(wait)
        try:
            status, headers, body = fetch_once(opener, current, timeout)
        except (urllib.error.URLError, http.client.HTTPException, OSError, ValueError) as exc:
            return {
                "ok": False,
                "reason": f"fetch_error: {type(exc).__name__}: {exc}",
                "hops": hops,
                "resolved": resolved,
                "finalUrl": current,
                "status": None,
            }
        location = headers.get("Location") if headers is not None else None
        if status in REDIRECT_STATUSES:
            if not location:
                # A redirect without a Location cannot be resolved; such a hop
                # is not recordable under the contract ("a redirect hop needs
                # location"), so the check is not emitted.
                return {
                    "ok": False,
                    "reason": "redirect_without_location",
                    "hops": hops + [{"status": status, "location": ""}],
                    "resolved": resolved,
                    "finalUrl": current,
                    "status": status,
                }
            if followed >= max_hops:
                return {
                    "ok": False,
                    "reason": "too_many_redirects",
                    "hops": hops,
                    "resolved": resolved,
                    "finalUrl": current,
                    "status": status,
                }
            hops.append({"status": status, "location": location})
            try:
                target = urllib.parse.urljoin(current, location)
                target_ok = urllib.parse.urlsplit(target).scheme in ("http", "https")
            except ValueError:
                target, target_ok = location, False
            resolved.append(target)
            if not target_ok:
                # Round-36 L1 repair (wave-2 ReviewSnapshotTool F1, F2): never follow a
                # redirect to a non-http(s) or unparseable Location; record and stop.
                return {
                    "ok": False,
                    "reason": "redirect_target_not_http",
                    "hops": hops,
                    "resolved": resolved,
                    "finalUrl": current,
                    "status": status,
                }
            followed += 1
            current = target
            continue
        return {
            "ok": True,
            # The Location header value is recorded raw (it may be relative);
            # the contract resolves each hop's location against the URL that
            # hop answered. The last hop is not a redirect, so it carries no
            # Location.
            "hops": hops + [{"status": status, "location": ""}],
            "resolved": resolved + [current],
            "finalUrl": current,
            "status": status,
            "contentType": (headers.get("Content-Type") if headers is not None else None) or "",
            "body": body,
            "truncated": len(body) > MAX_BODY,
        }
    return {
        "ok": False,
        "reason": "too_many_redirects",
        "hops": hops,
        "resolved": resolved,
        "finalUrl": current,
        "status": None,
    }


def build_check(item, manifest_dir: Path) -> tuple[dict | None, dict]:
    """Record one item. Returns (check or None, receipt entry).

    Bodies live under the manifest's own directory so that the contract's
    "relative path to a regular file inside the manifest's directory" holds.
    """
    ident = item.get("id")
    url = item.get("url")
    quote = item.get("quote")
    receipt = {"id": ident, "url": url, "quote": quote}
    if not isinstance(ident, str) or not ident:
        receipt.update(recorded=False, reason="invalid_id")
        return None, receipt
    if not isinstance(url, str) or not valid_url(url):
        receipt.update(recorded=False, reason="invalid_url")
        return None, receipt
    if not isinstance(quote, str) or not quote:
        receipt.update(recorded=False, reason="invalid_quote")
        return None, receipt

    opener = urllib.request.build_opener(NoRedirect)
    res = record(opener, url, TIMEOUT, DELAY, MAX_HOPS)
    receipt["fetchedUtc"] = utcnow()
    receipt["finalUrl"] = res.get("finalUrl")
    receipt["status"] = res.get("status")
    receipt["hops"] = res.get("hops")
    receipt["resolvedLocations"] = res.get("resolved")
    if not res.get("ok"):
        receipt.update(recorded=False, reason=res.get("reason"))
        return None, receipt

    body = res["body"]
    if res["truncated"]:
        receipt.update(recorded=False, reason="body_too_large")
        return None, receipt

    check = {"id": ident, "url": url, "quote": quote, "hops": res["hops"]}
    if res["status"] == 200:
        name = f"{safe_name(ident)}.body"
        (manifest_dir / name).write_bytes(body)
        check["contentType"] = res["contentType"]
        check["body"] = name
        receipt["bodyBytes"] = len(body)
        receipt["bodySha256"] = hashlib.sha256(body).hexdigest()
    receipt.update(recorded=True, reason=None)
    return check, receipt


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="record live fetches as a C1 manifest")
    ap.add_argument("--input", required=True, help="JSON list of {id, url, quote}")
    ap.add_argument("--out-dir", required=True, help="directory for the manifest and bodies")
    ap.add_argument("--manifest", default=None, help="manifest path (default OUT_DIR/manifest.json)")
    a = ap.parse_args(argv)

    src = Path(a.input)
    try:
        items = json.loads(src.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"source_snapshot: cannot read input {src}: {exc}", file=sys.stderr)
        return 2
    if not isinstance(items, list):
        print("source_snapshot: input must be a JSON list", file=sys.stderr)
        return 2

    out_dir = Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = Path(a.manifest) if a.manifest else out_dir / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_dir = manifest_path.parent

    checks: list[dict] = []
    receipts: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            receipts.append({"recorded": False, "reason": "invalid_item", "id": None, "url": None, "quote": None})
            continue
        check, receipt = build_check(item, manifest_dir)
        if check is not None:
            checks.append(check)
        receipts.append(receipt)

    manifest = {"version": 1, "checks": checks}
    manifest_path.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (manifest_dir / "receipts.json").write_text(
        json.dumps({"manifest": str(manifest_path), "writtenUtc": utcnow(), "items": receipts}, indent=1) + "\n",
        encoding="utf-8",
    )
    print(f"manifest {manifest_path} checks {len(checks)} of {len(items)}")
    for r in receipts:
        if not r.get("recorded"):
            print(f"  not recorded: {r.get('id')} ({r.get('reason')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
