#!/usr/bin/env python3
"""Read-only snapshot of live owned surfaces for the offline canonical preflight.

Usage: live_snapshot.py --population POP.json --out DIR [--validator scripts/canonical_audit.py]

For each surface in POP.json ({"surfaces":[{"id","url","expectedCanonical"}]}) this
issues one HTTP GET (no cookies, no credentials, no request body; at most 5
redirects, 2 MiB body, 20 s timeout) and writes, under DIR/<id>/:
  fetch.json  url, finalUrl, status, contentType, bytes, sha256, fetchedAt, redirects
  page.html   the served body, only for a 2xx text/html response
  manifest.json + audit.json  the canonical_audit manifest for that page and the
              validator's stdout JSON plus exit; a non-served surface records
              {"verdict":"not-served","status":N,"exit":null}.
It never sends anything but GET, never publishes, and writes only under DIR.
Surface ids must be a single safe path component ([a-z0-9][a-z0-9-]*) and URLs must be
http(s) without userinfo; anything else is bad input and nothing is fetched.
--reaudit re-runs only the audit step over already stored snapshots (no network),
e.g. after the validator changes, keeping fetch.json/page.html byte-identical.
Exit 0 when every surface was attempted (verdicts are data, not exit status);
2 on bad input; 64 on usage.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

MAX_BODY = 2 * 1024 * 1024
TIMEOUT = 20
MAX_REDIRECTS = 5
USER_AGENT = "kake-shokunin-readonly-preflight/1 (+GET only)"
SAFE_ID = re.compile(r"[a-z0-9][a-z0-9-]{0,62}")


class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self) -> None:
        self.chain: list[dict[str, object]] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if len(self.chain) >= MAX_REDIRECTS:
            raise urllib.error.HTTPError(req.full_url, code, "too many redirects", headers, fp)
        target = urllib.parse.urlsplit(newurl)
        if target.scheme not in {"http", "https"} or target.username is not None or target.password is not None:
            raise urllib.error.HTTPError(req.full_url, code, "redirect to non-http(s) or userinfo URL refused", headers, fp)
        self.chain.append({"status": code, "from": req.full_url, "to": newurl})
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None and new.get_method() != "GET":
            raise urllib.error.HTTPError(req.full_url, code, "non-GET redirect refused", headers, fp)
        return new


def fetch(url: str) -> tuple[dict[str, object], bytes | None]:
    redirects = Redirects()
    opener = urllib.request.build_opener(redirects)
    request = urllib.request.Request(url, method="GET", headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
    fetched_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    status, final_url, content_type, body, error = None, url, None, b"", None
    try:
        with opener.open(request, timeout=TIMEOUT) as response:
            status, final_url = response.status, response.geturl()
            content_type = response.headers.get("Content-Type")
            body = response.read(MAX_BODY + 1)
    except urllib.error.HTTPError as exc:
        status, final_url = exc.code, exc.geturl() or url
        content_type = exc.headers.get("Content-Type") if exc.headers else None
        try:
            body = exc.read(MAX_BODY + 1)
        except OSError:
            body = b""
    except (urllib.error.URLError, OSError, ValueError) as exc:
        error = f"{type(exc).__name__}: {exc}"
    truncated = len(body) > MAX_BODY
    body = body[:MAX_BODY]
    meta = {
        "url": url, "finalUrl": final_url, "status": status, "contentType": content_type,
        "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "truncated": truncated,
        "fetchedAt": fetched_at, "redirects": redirects.chain, "error": error, "method": "GET",
    }
    served = (
        error is None and isinstance(status, int) and 200 <= status < 300 and not truncated
        and content_type is not None and content_type.split(";")[0].strip().lower() == "text/html"
    )
    return meta, (body if served else None)


def audit(validator: str, directory: str, page_url: str, expected: str) -> dict[str, object]:
    manifest = {"version": 1, "pages": [{"url": page_url, "file": "page.html", "expectedCanonical": expected}]}
    path = os.path.join(directory, "manifest.json")
    with open(path, "w", encoding="utf-8") as stream:
        json.dump(manifest, stream, sort_keys=True)
    try:
        done = subprocess.run([sys.executable, "-B", validator, "--manifest", path, "--json"],
                              capture_output=True, text=True, timeout=60, check=False)
        return {"exit": done.returncode, "result": json.loads(done.stdout)}
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as exc:
        return {"exit": None, "result": {"verdict": "audit-error", "findings": [], "pagesChecked": 0},
                "error": f"{type(exc).__name__}: {exc}"}


def check_surface(surface: dict) -> None:
    if not isinstance(surface.get("id"), str) or not SAFE_ID.fullmatch(surface["id"]):
        raise ValueError(f"unsafe surface id {surface.get('id')!r}")
    parts = urllib.parse.urlsplit(str(surface.get("url")))
    if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username is not None or parts.password is not None:
        raise ValueError(f"surface {surface['id']}: url must be http(s) with a host and no userinfo")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--population", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--reaudit", action="store_true", help="re-run audits on stored snapshots only (no network)")
    parser.add_argument("--validator", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "canonical_audit.py"))
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    try:
        with open(args.population, encoding="utf-8") as stream:
            surfaces = json.load(stream)["surfaces"]
        if not surfaces or any(not {"id", "url", "expectedCanonical"} <= set(s) for s in surfaces):
            raise ValueError("each surface needs id, url, expectedCanonical")
        for surface in surfaces:
            check_surface(surface)
        if len({s["id"] for s in surfaces}) != len(surfaces):
            raise ValueError("duplicate surface id")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    out = os.path.realpath(args.out)
    summary = []
    for surface in surfaces:
        directory = os.path.join(out, surface["id"])
        if os.path.dirname(os.path.realpath(directory)) != out:
            print(json.dumps({"error": f"{surface['id']}: destination escapes --out"}))
            return 2
        if args.reaudit:
            with open(os.path.join(directory, "fetch.json"), encoding="utf-8") as stream:
                meta = json.load(stream)
            page = os.path.join(directory, "page.html")
            body = b"" if os.path.isfile(page) else None
        else:
            os.makedirs(directory, exist_ok=True)
            meta, body = fetch(surface["url"])
            with open(os.path.join(directory, "fetch.json"), "w", encoding="utf-8") as stream:
                json.dump(meta, stream, indent=1, sort_keys=True)
            if body is not None:
                with open(os.path.join(directory, "page.html"), "wb") as stream:
                    stream.write(body)
        if body is None:
            receipt = {"verdict": "not-served", "status": meta["status"], "exit": None, "error": meta["error"]}
        else:
            receipt = audit(args.validator, directory, str(meta["finalUrl"]), surface["expectedCanonical"])
        with open(os.path.join(directory, "audit.json"), "w", encoding="utf-8") as stream:
            json.dump(receipt, stream, indent=1, sort_keys=True)
        verdict = receipt.get("verdict") or receipt["result"]["verdict"]
        summary.append({"id": surface["id"], "status": meta["status"], "verdict": verdict,
                        "findings": [f["id"] for f in receipt.get("result", {}).get("findings", [])]})
    print(json.dumps({"surfaces": summary}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
