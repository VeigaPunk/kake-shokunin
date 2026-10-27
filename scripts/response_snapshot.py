#!/usr/bin/env python3
"""GET-only response capture for the offline response-header audit (round 61, C2).

response_snapshot.py [--population DIR] [--out DIR] [--overwrite]

DIR is a population of one subdirectory per public surface, each holding a
fetch.json naming the surface (`id`, `url`). Defaults: the round-23 live
population and .ufo/waves/round-61/capture. For each surface one GET is made
and --out/<id>/response.json records the final response: status, finalUrl,
every header field-line in wire order as {"name", "value"} objects (duplicates
preserved, names not lowercased), the body's sha256 and byte count (first
2 MiB), fetchedAt (UTC, Z) and userAgent `round61`. The received body is
retained byte-identically as body.bin so the digest stays re-verifiable
offline; headers and status are recorded for non-2xx responses too.

No cookies, credentials or request body; at most 5 redirects, 20 s and 2 MiB
per surface; exactly one GET per surface (no retries). A committed capture is
never rewritten in place: a run refuses (before any GET) when a target
response.json already exists unless --overwrite is given, so a re-run lands
under a fresh --out. Output leaves are regular, single-link files opened
no-follow relative to one opened directory; nothing is written outside --out,
and no temporary file is created (nothing is written to $TMPDIR or /tmp).
Exit 0 means every attempt was recorded (inspect per-surface status/error);
2 bad population, unsafe URL/id, existing receipt without --overwrite or
unwritable output; 64 usage. JSON summary on stdout.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import http.client
import json
import os
import re
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request

MAX_BODY = 2 * 1024 * 1024
TIMEOUT = 20
MAX_REDIRECTS = 5
USER_AGENT = "round61"
SAFE_ID = re.compile(r"[a-z0-9][a-z0-9-]{0,62}")
LANE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POPULATION_DEFAULT = os.path.join(LANE, ".ufo", "waves", "round-23", "live")
OUT_DEFAULT = os.path.join(LANE, ".ufo", "waves", "round-61", "capture")


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


def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch(url: str) -> tuple[dict, bytes]:
    redirects = Redirects()
    opener = urllib.request.build_opener(redirects)
    request = urllib.request.Request(url, method="GET", headers={"User-Agent": USER_AGENT})
    fetched_at = utc_now()
    status, final_url, headers, body, error = None, url, [], b"", None
    try:
        with opener.open(request, timeout=TIMEOUT) as response:
            status, final_url = int(response.status), response.geturl()
            headers = list(response.headers.items())
            try:
                body = response.read(MAX_BODY + 1)
            except (http.client.HTTPException, OSError) as exc:
                # Keep the headers already received; record the partial body.
                body = getattr(exc, "partial", b"") or b""
                error = f"{type(exc).__name__}: {exc}"
    except urllib.error.HTTPError as exc:
        status, final_url = exc.code, exc.geturl() or url
        headers = list(exc.headers.items()) if exc.headers else []
        if exc.reason == "blocked redirect":
            error = "blocked redirect"
        try:
            body = exc.read(MAX_BODY + 1)
        except (http.client.HTTPException, OSError):
            body = b""
        finally:
            exc.close()
    except (urllib.error.URLError, OSError, ValueError) as exc:
        error = f"{type(exc).__name__}: {exc}"
    truncated = len(body) > MAX_BODY
    body = body[:MAX_BODY]
    content_type = None
    for name, value in headers:
        if name.lower() == "content-type":
            content_type = value
    meta = {
        "url": url,
        "finalUrl": final_url,
        "method": "GET",
        "status": status,
        "headers": [{"name": name, "value": value} for name, value in headers],
        "headerCount": len(headers),
        "contentType": content_type,
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "truncated": truncated,
        "fetchedAt": fetched_at,
        "userAgent": USER_AGENT,
        "redirects": redirects.chain,
        "error": error,
        "bodyFile": "body.bin" if body else None,
    }
    return meta, body


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


def write_json(directory_fd: int, name: str, value: dict) -> None:
    write_file(directory_fd, name, json.dumps(value, indent=1, sort_keys=True).encode("utf-8"))


def load_population(directory: str) -> list[dict]:
    surfaces = []
    for name in sorted(os.listdir(directory)):
        path = os.path.join(directory, name, "fetch.json")
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as stream:
            recorded = json.load(stream)
        if not isinstance(recorded, dict):
            raise ValueError(f"{name}: fetch.json must be a JSON object")
        surface = {"id": recorded.get("id") or name, "url": recorded.get("url")}
        if not isinstance(surface["id"], str) or not SAFE_ID.fullmatch(surface["id"]):
            raise ValueError(f"{name}: unsafe surface id")
        if not isinstance(surface["url"], str) or not safe_url(surface["url"]):
            raise ValueError(f"{name}: url must be http(s) with a host and no userinfo")
        surfaces.append(surface)
    if not surfaces:
        raise ValueError("population holds no fetch.json surfaces")
    if len({surface["id"] for surface in surfaces}) != len(surfaces):
        raise ValueError("duplicate surface id")
    return surfaces


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--population", default=POPULATION_DEFAULT)
    parser.add_argument("--out", default=OUT_DEFAULT)
    parser.add_argument("--overwrite", action="store_true", help="rewrite existing response.json receipts in place")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    try:
        surfaces = load_population(args.population)
        taken = [surface["id"] for surface in surfaces
                 if os.path.lexists(os.path.join(args.out, surface["id"], "response.json"))]
        if taken and not args.overwrite:
            raise ValueError("receipt already present (" + ", ".join(taken) + "); use --overwrite or a fresh --out")
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
                    meta, body = fetch(surface["url"])
                    write_json(directory_fd, "response.json", meta)
                    if body:
                        write_file(directory_fd, "body.bin", body)
                    else:
                        try:
                            os.unlink("body.bin", dir_fd=directory_fd)
                        except FileNotFoundError:
                            pass
                    summary.append({"id": name, "status": meta["status"], "finalUrl": meta["finalUrl"],
                                    "headerCount": meta["headerCount"], "bytes": meta["bytes"],
                                    "sha256": meta["sha256"], "error": meta["error"]})
                finally:
                    os.close(directory_fd)
        finally:
            os.close(out_fd)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    print(json.dumps({"captures": summary}, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
