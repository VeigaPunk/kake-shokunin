#!/usr/bin/env python3
"""Capture-to-capture drift gate (round 82).

capture_delta.py --a DIR --b DIR [--selftest]

DIR is a capture tree in the lane's round-81/round-82 schema: a
`manifest.json` carrying `version`, `allowlist` and a `checks` list of
surface objects (`id`, `url`, `expect`, `source`), plus one subdirectory per
surface holding `response.json` (the receipt: url, finalUrl, method, status,
headers as a list of {name, value} in wire order, bytes, sha256, truncated,
fetchedAt, error) and, when the body was retained, `body.bin`.

The tool verifies every receipt against its retained body and prints one
stable line per surface in the union of both trees, then a summary line. A
surface's verdict is `identical` when status, body sha256, body length and
the header mapping (lower-cased name -> values in wire order) all match,
`changed` otherwise, and `added` / `removed` when the surface exists in only
one tree.

Exit: 0 a complete record was printed; 1 a receipt or manifest fault (printed
as `fault surface=<id> <reason>`); 2 a tree is missing or unreadable; 64
usage. Offline: no socket is opened.

`--selftest` builds fixtures under a temporary directory and prints
`selftest: N/N passed`.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile

SAFE_ID = re.compile(r"[a-z0-9][a-z0-9-]{0,62}")
HEX64 = re.compile(r"[0-9a-f]{64}")
RFC3339 = re.compile(
    r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d+)?(Z|[+-]\d{2}:\d{2})"
)


def parse_instant(value: object) -> datetime.datetime | None:
    if not isinstance(value, str):
        return None
    match = RFC3339.fullmatch(value)
    if not match:
        return None
    year, month, day, hour, minute, second = (int(match.group(i)) for i in range(1, 7))
    zone = match.group(7)
    try:
        if zone == "Z":
            tz = datetime.timezone.utc
        else:
            sign = 1 if zone[0] == "+" else -1
            tz = datetime.timezone(sign * datetime.timedelta(
                hours=int(zone[1:3]), minutes=int(zone[4:6])))
        return datetime.datetime(year, month, day, hour, minute, second, tzinfo=tz)
    except ValueError:
        return None


class Fault(Exception):
    def __init__(self, surface: str, reason: str) -> None:
        super().__init__(f"surface={surface} {reason}")
        self.surface = surface
        self.reason = reason


def header_map(headers: object) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    if not isinstance(headers, list):
        raise ValueError("headers is not a list")
    for entry in headers:
        if not isinstance(entry, dict):
            raise ValueError("header entry is not an object")
        name, value = entry.get("name"), entry.get("value")
        if not isinstance(name, str) or not isinstance(value, str):
            raise ValueError("header name/value is not a string")
        mapping.setdefault(name.lower(), []).append(value)
    return mapping


def verify_leaf(surface: str, leaf: str) -> dict:
    receipt = os.path.join(leaf, "response.json")
    body_path = os.path.join(leaf, "body.bin")
    if not os.path.isfile(receipt):
        raise Fault(surface, "response.json missing")
    try:
        with open(receipt, encoding="utf-8") as stream:
            meta = json.load(stream)
    except (OSError, json.JSONDecodeError) as exc:
        raise Fault(surface, f"response.json unreadable ({type(exc).__name__})")
    if not isinstance(meta, dict):
        raise Fault(surface, "response.json is not an object")
    if meta.get("method") != "GET":
        raise Fault(surface, "method is not GET")
    status = meta.get("status")
    if not isinstance(status, int) or isinstance(status, bool) or not 100 <= status <= 599:
        raise Fault(surface, "status is not an integer in 100..599")
    if meta.get("truncated") is not False:
        raise Fault(surface, "truncated is not false")
    if parse_instant(meta.get("fetchedAt")) is None:
        raise Fault(surface, "fetchedAt is not an RFC 3339 instant")
    size = meta.get("bytes")
    if not isinstance(size, int) or isinstance(size, bool) or size < 0:
        raise Fault(surface, "bytes is not a non-negative integer")
    digest = meta.get("sha256")
    if not isinstance(digest, str) or not HEX64.fullmatch(digest):
        raise Fault(surface, "sha256 is not 64 lowercase hex digits")
    try:
        headers = header_map(meta.get("headers"))
    except ValueError as exc:
        raise Fault(surface, f"headers unreadable ({exc})")
    has_body = os.path.isfile(body_path)
    if has_body:
        with open(body_path, "rb") as stream:
            body = stream.read()
        if len(body) != size:
            raise Fault(surface, f"body bytes {len(body)} != receipt bytes {size}")
        actual = hashlib.sha256(body).hexdigest()
        if actual != digest:
            raise Fault(surface, f"body sha256 {actual[:12]} != receipt {digest[:12]}")
    elif size != 0:
        raise Fault(surface, f"body.bin absent while receipt claims {size} bytes")
    return {"meta": meta, "headers": headers}


def load_tree(directory: str) -> tuple[dict, dict]:
    """Return (manifest, surfaces) where surfaces maps id -> leaf path."""
    manifest_path = os.path.join(directory, "manifest.json")
    if not os.path.isdir(directory):
        raise Fault("(tree)", f"directory absent: {directory}")
    if not os.path.isfile(manifest_path):
        raise Fault("(tree)", f"manifest.json absent under {directory}")
    with open(manifest_path, encoding="utf-8") as stream:
        manifest = json.load(stream)
    if not isinstance(manifest, dict) or not isinstance(manifest.get("checks"), list):
        raise Fault("(tree)", "manifest.json carries no checks list")
    surfaces: dict[str, str] = {}
    for check in manifest["checks"]:
        if not isinstance(check, dict):
            raise Fault("(tree)", "manifest check is not an object")
        surface = check.get("id")
        url = check.get("url")
        if not isinstance(surface, str) or not SAFE_ID.fullmatch(surface):
            raise Fault("(tree)", "manifest check id is unsafe")
        if surface in surfaces:
            raise Fault(surface, "duplicate surface id in manifest")
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            raise Fault(surface, "manifest check url is not http(s)")
        leaf = os.path.join(directory, surface)
        if os.path.isdir(leaf):
            surfaces[surface] = leaf
        else:
            raise Fault(surface, f"surface directory absent: {leaf}")
    if not surfaces:
        raise Fault("(tree)", "manifest declares no surfaces")
    return manifest, surfaces


def compare(a_dir: str, b_dir: str) -> tuple[list[str], dict]:
    _a_manifest, a_surfaces = load_tree(a_dir)
    _b_manifest, b_surfaces = load_tree(b_dir)
    lines: list[str] = []
    counts = {"identical": 0, "changed": 0, "added": 0, "removed": 0}
    for surface in sorted(set(a_surfaces) | set(b_surfaces)):
        if surface not in b_surfaces:
            a = verify_leaf(surface, a_surfaces[surface])
            lines.append(
                f"surface={surface} url={a['meta'].get('url')} verdict=removed"
                f" status={a['meta'].get('status')} bytes={a['meta'].get('bytes')}"
            )
            counts["removed"] += 1
            continue
        if surface not in a_surfaces:
            b = verify_leaf(surface, b_surfaces[surface])
            lines.append(
                f"surface={surface} url={b['meta'].get('url')} verdict=added"
                f" status={b['meta'].get('status')} bytes={b['meta'].get('bytes')}"
            )
            counts["added"] += 1
            continue
        a = verify_leaf(surface, a_surfaces[surface])
        b = verify_leaf(surface, b_surfaces[surface])
        a_headers, b_headers = a["headers"], b["headers"]
        added = sorted(set(b_headers) - set(a_headers))
        removed = sorted(set(a_headers) - set(b_headers))
        changed = sorted(
            name for name in set(a_headers) & set(b_headers)
            if a_headers[name] != b_headers[name]
        )
        same_body = (a["meta"].get("sha256") == b["meta"].get("sha256")
                     and a["meta"].get("bytes") == b["meta"].get("bytes"))
        same_status = a["meta"].get("status") == b["meta"].get("status")
        identical = same_body and same_status and not added and not removed and not changed
        verdict = "identical" if identical else "changed"
        counts[verdict] += 1
        lines.append(
            f"surface={surface} url={b['meta'].get('url')}"
            f" status={a['meta'].get('status')}->{b['meta'].get('status')}"
            f" body={'same' if same_body else 'changed'}"
            f" bytes={a['meta'].get('bytes')}->{b['meta'].get('bytes')}"
            f" headers={len(b_headers)} added={len(added)} removed={len(removed)}"
            f" changed={len(changed)} verdict={verdict}"
        )
        for label, names in (("added", added), ("removed", removed), ("changed", changed)):
            for name in names:
                lines.append(f"  field={name} change={label}")
    lines.append(
        f"surfaces={len(set(a_surfaces) | set(b_surfaces))}"
        f" identical={counts['identical']} changed={counts['changed']}"
        f" added={counts['added']} removed={counts['removed']}"
    )
    return lines, counts


def write_fixture(root: str, name: str, surfaces: list[tuple[str, dict, bytes]],
                  fetched: str = "2026-11-04T12:05:06Z") -> str:
    directory = os.path.join(root, name)
    os.makedirs(directory)
    checks = []
    for surface, overrides, body in surfaces:
        leaf = os.path.join(directory, surface)
        os.makedirs(leaf)
        meta = {
            "url": f"https://example.test/{surface}",
            "finalUrl": f"https://example.test/{surface}",
            "method": "GET",
            "status": 200,
            "headers": [
                {"name": "Content-Type", "value": "text/plain"},
                {"name": "Cache-Control", "value": "max-age=60"},
            ],
            "headerCount": 2,
            "contentType": "text/plain",
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "truncated": False,
            "fetchedAt": fetched,
            "userAgent": "round82-fixture",
            "redirects": [],
            "error": None,
            "bodyFile": "body.bin" if body else None,
        }
        meta.update(overrides)
        if "headers" in overrides:
            meta["headerCount"] = len(overrides["headers"])
        with open(os.path.join(leaf, "response.json"), "w", encoding="utf-8") as stream:
            json.dump(meta, stream, indent=1, sort_keys=True)
        if body:
            with open(os.path.join(leaf, "body.bin"), "wb") as stream:
                stream.write(body)
        checks.append({"id": surface, "url": meta["url"],
                       "expect": {"content_type_present": True},
                       "source": f"{name}/{surface}/response.json"})
    with open(os.path.join(directory, "manifest.json"), "w", encoding="utf-8") as stream:
        json.dump({"version": 1, "allowlist": ["example.test"], "checks": checks},
                  stream, indent=1, sort_keys=True)
    return directory


def selftest() -> int:
    work = tempfile.mkdtemp(prefix="capture-delta-selftest-")
    results: list[tuple[str, bool, str]] = []

    def check(name: str, fn) -> None:
        try:
            fn()
            results.append((name, True, ""))
        except AssertionError as exc:
            results.append((name, False, str(exc)))

    try:
        base = write_fixture(work, "a", [("one", {}, b"alpha"), ("two", {}, b"beta")])

        def green() -> None:
            b = write_fixture(work, "b-green", [("one", {}, b"alpha"), ("two", {}, b"beta")],
                              fetched="2026-11-04T12:30:00Z")
            lines, counts = compare(base, b)
            assert counts["identical"] == 2 and counts["changed"] == 0, lines
            assert lines[-1].startswith("surfaces=2 identical=2"), lines[-1]

        check("green-identical", green)

        def changed_body() -> None:
            b = write_fixture(work, "b-body", [("one", {}, b"alpha!"), ("two", {}, b"beta")])
            lines, counts = compare(base, b)
            assert counts["changed"] == 1 and counts["identical"] == 1, lines
            assert any("surface=one" in line and "body=changed" in line for line in lines), lines

        check("changed-body", changed_body)

        def changed_status() -> None:
            b = write_fixture(work, "b-status",
                              [("one", {"status": 404}, b"alpha"), ("two", {}, b"beta")])
            _lines, counts = compare(base, b)
            assert counts["changed"] == 1, counts

        check("changed-status", changed_status)

        def header_added() -> None:
            headers = [{"name": "Content-Type", "value": "text/plain"},
                       {"name": "Cache-Control", "value": "max-age=60"},
                       {"name": "Strict-Transport-Security", "value": "max-age=1"}]
            b = write_fixture(work, "b-added",
                              [("one", {"headers": headers}, b"alpha"), ("two", {}, b"beta")])
            lines, counts = compare(base, b)
            assert counts["changed"] == 1, counts
            assert any("field=strict-transport-security change=added" in line for line in lines), lines

        check("header-added", header_added)

        def header_changed() -> None:
            headers = [{"name": "Content-Type", "value": "text/plain"},
                       {"name": "cache-control", "value": "max-age=120"}]
            b = write_fixture(work, "b-changed",
                              [("one", {"headers": headers}, b"alpha"), ("two", {}, b"beta")])
            _lines, counts = compare(base, b)
            assert counts["changed"] == 1, counts

        check("header-value-changed", header_changed)

        def header_removed() -> None:
            headers = [{"name": "Content-Type", "value": "text/plain"}]
            b = write_fixture(work, "b-removed",
                              [("one", {"headers": headers}, b"alpha"), ("two", {}, b"beta")])
            _lines, counts = compare(base, b)
            assert counts["changed"] == 1, counts

        check("header-removed", header_removed)

        def tampered_body() -> None:
            b = write_fixture(work, "b-tamper", [("one", {}, b"alpha"), ("two", {}, b"beta")])
            with open(os.path.join(b, "one", "body.bin"), "wb") as stream:
                stream.write(b"alphA")
            try:
                compare(base, b)
            except Fault as exc:
                assert "body sha256" in exc.reason, exc.reason
                return
            raise AssertionError("tampered body produced a record")

        check("tampered-body", tampered_body)

        def byte_count() -> None:
            b = write_fixture(work, "b-bytes", [("one", {"bytes": 99}, b"alpha"), ("two", {}, b"beta")])
            try:
                compare(base, b)
            except Fault as exc:
                assert "body bytes" in exc.reason, exc.reason
                return
            raise AssertionError("byte-count drift produced a record")

        check("byte-count-mismatch", byte_count)

        def truncated() -> None:
            b = write_fixture(work, "b-trunc", [("one", {"truncated": True}, b"alpha"), ("two", {}, b"beta")])
            try:
                compare(base, b)
            except Fault as exc:
                assert "truncated" in exc.reason, exc.reason
                return
            raise AssertionError("truncated receipt produced a record")

        check("truncated-receipt", truncated)

        def bad_method() -> None:
            b = write_fixture(work, "b-method", [("one", {"method": "POST"}, b"alpha"), ("two", {}, b"beta")])
            try:
                compare(base, b)
            except Fault as exc:
                assert "GET" in exc.reason, exc.reason
                return
            raise AssertionError("non-GET receipt produced a record")

        check("non-get-method", bad_method)

        def added_surface() -> None:
            b = write_fixture(work, "b-add", [("one", {}, b"alpha"), ("two", {}, b"beta"),
                                              ("three", {}, b"gamma")])
            lines, counts = compare(base, b)
            assert counts["added"] == 1 and counts["identical"] == 2, lines
            assert any("surface=three" in line and "verdict=added" in line for line in lines), lines

        check("added-surface", added_surface)

        def removed_surface() -> None:
            b = write_fixture(work, "b-drop", [("one", {}, b"alpha")])
            _lines, counts = compare(base, b)
            assert counts["removed"] == 1 and counts["identical"] == 1, counts

        check("removed-surface", removed_surface)

        def missing_tree() -> None:
            try:
                compare(base, os.path.join(work, "absent"))
            except Fault as exc:
                assert "directory absent" in exc.reason, exc.reason
                return
            raise AssertionError("missing tree produced a record")

        check("missing-tree", missing_tree)

        def missing_surface_dir() -> None:
            b = write_fixture(work, "b-nodir", [("one", {}, b"alpha"), ("two", {}, b"beta")])
            shutil.rmtree(os.path.join(b, "two"))
            try:
                compare(base, b)
            except Fault as exc:
                assert "surface directory absent" in exc.reason, exc.reason
                return
            raise AssertionError("missing surface directory produced a record")

        check("missing-surface-dir", missing_surface_dir)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    passed = sum(1 for _name, ok, _detail in results if ok)
    for name, ok, detail in results:
        print(("ok   " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))
    print(f"selftest: {passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--a")
    parser.add_argument("--b")
    parser.add_argument("--selftest", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    if args.selftest:
        return selftest()
    if not args.a or not args.b:
        parser.print_usage(sys.stderr)
        return 64
    try:
        lines, _counts = compare(args.a, args.b)
    except Fault as exc:
        print(f"fault {exc.surface} {exc.reason}")
        return 1 if exc.surface != "(tree)" else 2
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"fault (tree) unreadable ({type(exc).__name__}: {exc})")
        return 2
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
