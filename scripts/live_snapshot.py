#!/usr/bin/env python3
"""GET-only owned-page snapshots for the offline canonical preflight.

live_snapshot.py --population POP.json --out DIR [--reaudit] [--validator PATH]
POP has a surfaces array of {id,url,expectedCanonical}. IDs are safe lowercase
single path components; HTTP(S) URLs have no userinfo. Capture uses no cookies,
credentials or request body; at most 5 redirects, 20 s, 2 MiB. Each DIR/id has
fetch.json, audit.json, and page.html + manifest.json for served HTML only.
--reaudit uses stored bytes without network and first verifies metadata, body
length and digest. Output leaves are regular, single-link files opened no-follow
relative to one opened directory. Exit 0 means all attempts recorded (inspect
per-surface outcomes); 2 bad input or inconsistent snapshot; 64 usage.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import stat
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


def safe_url(url: str) -> bool:
    parts = urllib.parse.urlsplit(url)
    return (parts.scheme in {"http", "https"} and bool(parts.hostname)
            and parts.username is None and parts.password is None)


class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self) -> None:
        self.chain: list[dict[str, object]] = []

    def http_error_302(self, req, fp, code, msg, headers):
        location = headers.get("Location") or headers.get("URI")
        if location and not safe_url(urllib.parse.urljoin(req.full_url, location)):
            # urllib otherwise reports an unfetched file:/userinfo destination as
            # geturl(). Preserve the last actual HTTP response URL instead.
            raise urllib.error.HTTPError(req.full_url, code, "blocked redirect", headers, fp)
        return super().http_error_302(req, fp, code, msg, headers)

    http_error_301 = http_error_303 = http_error_307 = http_error_308 = http_error_302

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if len(self.chain) >= MAX_REDIRECTS or not safe_url(newurl):
            raise urllib.error.HTTPError(req.full_url, code, "blocked redirect", headers, fp)
        self.chain.append({"status": code, "from": req.full_url, "to": newurl})
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None and new.get_method() != "GET":
            raise urllib.error.HTTPError(req.full_url, code, "non-GET redirect refused", headers, fp)
        return new


def served(meta: dict) -> bool:
    status, ctype = meta.get("status"), meta.get("contentType") or ""
    return (type(status) is int and 200 <= status < 300 and not meta.get("error")
            and not meta.get("truncated") and ctype.split(";")[0].strip().lower() == "text/html")


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
        error = "redirect refused" if exc.reason == "blocked redirect" else None
        try:
            body = exc.read(MAX_BODY + 1)
        except OSError:
            body = b""
        finally:
            exc.close()
    except (urllib.error.URLError, OSError, ValueError) as exc:
        error = f"{type(exc).__name__}: {exc}"
    truncated = len(body) > MAX_BODY
    body = body[:MAX_BODY]
    meta = {"url": url, "finalUrl": final_url, "status": status, "contentType": content_type,
            "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "truncated": truncated,
            "fetchedAt": fetched_at, "redirects": redirects.chain, "error": error, "method": "GET"}
    return meta, (body if served(meta) else None)


def write_file(directory_fd: int, name: str, data: bytes) -> None:
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600, dir_fd=directory_fd)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError(f"{name}: output must be a regular single-link file")
        os.ftruncate(fd, 0)
        with os.fdopen(fd, "wb", closefd=False) as stream:
            stream.write(data)
    finally:
        os.close(fd)


def read_file(directory_fd: int, name: str, limit: int) -> bytes:
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory_fd)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError(f"{name}: snapshot member must be regular")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            data = stream.read(limit + 1)
        if len(data) > limit:
            raise ValueError(f"{name}: oversized snapshot member")
        return data
    finally:
        os.close(fd)


def write_json(directory_fd: int, name: str, value: dict) -> None:
    write_file(directory_fd, name, json.dumps(value, indent=1, sort_keys=True).encode("utf-8"))


def audit(validator: str, directory: str, directory_fd: int, page_url: str, expected: str) -> dict:
    manifest = {"version": 1, "pages": [{"url": page_url, "file": "page.html", "expectedCanonical": expected}]}
    write_json(directory_fd, "manifest.json", manifest)
    try:
        done = subprocess.run([sys.executable, "-B", validator, "--manifest", os.path.join(directory, "manifest.json"), "--json"],
                              capture_output=True, text=True, timeout=60, check=False)
        return {"exit": done.returncode, "result": json.loads(done.stdout)}
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as exc:
        return {"exit": None, "result": {"verdict": "audit-error", "findings": [], "pagesChecked": 0},
                "error": f"{type(exc).__name__}: {exc}"}


def check_surface(surface: dict) -> None:
    if not isinstance(surface.get("id"), str) or not SAFE_ID.fullmatch(surface["id"]):
        raise ValueError("unsafe surface id")
    if not safe_url(str(surface.get("url"))) or not safe_url(str(surface.get("expectedCanonical"))):
        raise ValueError(f"surface {surface['id']}: URLs must be http(s) with a host and no userinfo")


def check_redirect_record(meta: dict) -> None:
    previous = meta.get("url")
    chain = meta.get("redirects")
    if not isinstance(chain, list) or len(chain) > MAX_REDIRECTS:
        raise ValueError("snapshot redirect chain missing or too long")
    for hop in chain:
        if (not isinstance(hop, dict) or hop.get("from") != previous
                or hop.get("status") not in {301, 302, 303, 307, 308}
                or not safe_url(str(hop.get("to")))):
            raise ValueError("snapshot redirect chain is inconsistent")
        previous = hop["to"]
    if meta.get("finalUrl") != previous:
        raise ValueError("snapshot finalUrl disagrees with redirect chain")


def reaudit_body(directory_fd: int, surface: dict) -> tuple[dict, bytes | None]:
    meta = json.loads(read_file(directory_fd, "fetch.json", 1024 * 1024))
    if not isinstance(meta, dict):
        raise ValueError("snapshot fetch metadata must be a JSON object")
    check_redirect_record(meta)
    if (meta.get("url") != surface["url"] or meta.get("method") != "GET"
            or not safe_url(str(meta.get("finalUrl"))) or type(meta.get("status")) is not int):
        raise ValueError("snapshot metadata does not describe the population GET")
    if served(meta):
        body = read_file(directory_fd, "page.html", MAX_BODY)
        if len(body) != meta.get("bytes") or hashlib.sha256(body).hexdigest() != meta.get("sha256"):
            raise ValueError("stored page differs from captured length/digest")
        return meta, body
    try:
        os.stat("page.html", dir_fd=directory_fd, follow_symlinks=False)
    except FileNotFoundError:
        return meta, None
    raise ValueError("non-served snapshot unexpectedly contains page.html")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--population", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--reaudit", action="store_true", help="verify stored captures then re-run audits (no network)")
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
        out = os.path.realpath(args.out)
        os.makedirs(out, exist_ok=True)
        out_fd = os.open(out, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        summary = []
        try:
            for surface in surfaces:
                name = surface["id"]
                try:
                    os.mkdir(name, dir_fd=out_fd)
                except FileExistsError:
                    pass
                directory_fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=out_fd)
                try:
                    if args.reaudit:
                        meta, body = reaudit_body(directory_fd, surface)
                    else:
                        meta, body = fetch(surface["url"])
                        write_json(directory_fd, "fetch.json", meta)
                        if body is not None:
                            write_file(directory_fd, "page.html", body)
                        else:
                            for stale in ("page.html", "manifest.json"):
                                try:
                                    os.unlink(stale, dir_fd=directory_fd)
                                except FileNotFoundError:
                                    pass
                    if body is None:
                        receipt = {"verdict": "fetch-error" if meta["error"] else "not-served",
                                   "status": meta["status"], "exit": None, "error": meta["error"]}
                    else:
                        receipt = audit(args.validator, os.path.join(out, name), directory_fd, str(meta["finalUrl"]), surface["expectedCanonical"])
                    write_json(directory_fd, "audit.json", receipt)
                    summary.append({"id": name, "status": meta["status"],
                                    "verdict": receipt.get("verdict") or receipt["result"]["verdict"],
                                    "findings": [f["id"] for f in receipt.get("result", {}).get("findings", [])]})
                finally:
                    os.close(directory_fd)
        finally:
            os.close(out_fd)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    print(json.dumps({"surfaces": summary}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
