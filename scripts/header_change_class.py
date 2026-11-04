#!/usr/bin/env python3
"""Header change classifier over two dated capture trees (kake, round 83).

Compares capture A and capture B of the surfaces declared in a declaration
file, classifies every changed response header by what its change means for
the served representation, and prints one stable line per surface plus a
summary. Offline by construction: it reads retained receipts and bodies and
opens no socket.

The class table is frozen in `.ufo/waves/round-83/contract.md` §C2:
  per-request     request/edge metadata that changes on every exchange
                  (date, age, x-cache, x-served-by, edge ids and timers)
  validator       fields that identify a representation version
                  (etag, last-modified)
  representation  fields describing the payload bytes
                  (content-length, content-type, content-encoding, vary, ...)
  policy          delivery policy that does not identify the payload
                  (cache-control, expires, security headers, link, server)
  unknown         any other field: treated as representation-bearing so a
                  change can never be waved through silently

A surface is `representation-changed` when status or body sha256 differs, or
any changed header is validator, representation or unknown; otherwise
`same-object` (only per-request and policy fields moved).

Usage:
  header_change_class.py --a <capture-dir> --b <capture-dir> --declared <json> [--json]
  header_change_class.py --selftest [--work <dir>]

Exit: 0 printed, 1 unevaluable input, 64 usage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

PER_REQUEST = {
    "age", "cf-ray", "connection", "date", "keep-alive", "nel", "report-to",
    "server-timing", "transfer-encoding", "via", "x-amz-cf-id", "x-cache",
    "x-cache-hits", "x-fastly-request-id", "x-github-edge-region",
    "x-github-request-id", "x-proxy-cache", "x-request-id", "x-request-start",
    "x-served-by", "x-timer",
}
VALIDATOR = {"etag", "last-modified"}
REPRESENTATION = {
    "accept-ranges", "content-encoding", "content-language", "content-length",
    "content-location", "content-md5", "content-type", "digest", "vary",
}
POLICY = {
    "access-control-allow-headers", "access-control-allow-methods",
    "access-control-allow-origin", "access-control-expose-headers", "alt-svc",
    "cache-control", "content-security-policy",
    "content-security-policy-report-only", "cross-origin-embedder-policy",
    "cross-origin-opener-policy", "cross-origin-resource-policy", "expires",
    "link", "permissions-policy", "pragma", "referrer-policy", "server",
    "strict-transport-security", "x-content-type-options", "x-frame-options",
    "x-robots-tag",
}


def header_class(name: str) -> str:
    lowered = name.strip().lower()
    if lowered in PER_REQUEST:
        return "per-request"
    if lowered in VALIDATOR:
        return "validator"
    if lowered in REPRESENTATION:
        return "representation"
    if lowered in POLICY:
        return "policy"
    return "unknown"


def canonical(headers: list[dict]) -> dict[str, str]:
    merged: dict[str, list[str]] = {}
    for item in headers:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip().lower()
        if not name:
            continue
        merged.setdefault(name, []).append(str(item.get("value", "")))
    return {name: ", ".join(values) for name, values in merged.items()}


def load_surface(directory: Path) -> tuple[dict | None, str]:
    receipt_path = directory / "response.json"
    if not receipt_path.is_file():
        return None, f"no response.json under {directory}"
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"unreadable receipt: {exc}"
    body_path = directory / str(receipt.get("bodyFile") or "body.bin")
    if not body_path.is_file():
        return None, f"missing body {body_path.name}"
    body = body_path.read_bytes()
    if receipt.get("method") != "GET":
        return None, "method is not GET"
    status = receipt.get("status")
    if not isinstance(status, int) or not 100 <= status <= 599:
        return None, f"bad status {status!r}"
    if receipt.get("bytes") != len(body):
        return None, f"bytes {receipt.get('bytes')!r} != body length {len(body)}"
    digest = hashlib.sha256(body).hexdigest()
    if receipt.get("sha256") != digest:
        return None, "body sha256 does not match the receipt"
    if receipt.get("truncated") is not False:
        return None, "receipt is truncated or silent"
    headers = receipt.get("headers")
    if not isinstance(headers, list):
        return None, "headers is not a list"
    return {
        "status": status,
        "sha256": digest,
        "headers": canonical(headers),
    }, ""


def declared_surfaces(path: Path) -> list[tuple[str, str]] | None:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
        surfaces = document["surfaces"]
        pairs = [(str(item["id"]), str(item["url"])) for item in surfaces]
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        return None
    seen: set[str] = set()
    for surface_id, _url in pairs:
        if surface_id in seen:
            return None
        seen.add(surface_id)
    return pairs


def classify(a: dict, b: dict) -> tuple[dict, str]:
    counts = {"per-request": 0, "validator": 0, "representation": 0,
              "policy": 0, "unknown": 0}
    changed: list[str] = []
    names = set(a["headers"]) | set(b["headers"])
    for name in sorted(names):
        before = a["headers"].get(name)
        after = b["headers"].get(name)
        if before == after:
            continue
        changed.append(name)
        counts[header_class(name)] += 1
    decisive = (a["status"] != b["status"] or a["sha256"] != b["sha256"]
                or counts["validator"] or counts["representation"]
                or counts["unknown"])
    verdict = "representation-changed" if decisive else "same-object"
    counts["diffs"] = len(changed)
    return counts, verdict


def run(a_dir: Path, b_dir: Path, declared_path: Path) -> int:
    declared = declared_surfaces(declared_path)
    if not declared:
        print(f"fault: cannot read declared surfaces from {declared_path}", file=sys.stderr)
        return 1
    totals = {"diffs": 0, "per-request": 0, "validator": 0, "representation": 0,
              "policy": 0, "unknown": 0}
    overall = "same-object"
    for surface_id, _url in declared:
        a, detail_a = load_surface(a_dir / surface_id)
        b, detail_b = load_surface(b_dir / surface_id)
        if a is None or b is None:
            print(f"fault: surface={surface_id} a=[{detail_a}] b=[{detail_b}]", file=sys.stderr)
            return 1
        counts, verdict = classify(a, b)
        if verdict == "representation-changed":
            overall = "representation-changed"
        for key in totals:
            totals[key] += counts[key]
        print(f"surface={surface_id} status_a={a['status']} status_b={b['status']} "
              f"diffs={counts['diffs']} per_request={counts['per-request']} "
              f"validator={counts['validator']} representation={counts['representation']} "
              f"policy={counts['policy']} unknown={counts['unknown']} verdict={verdict}")
    print(f"summary surfaces={len(declared)} diffs={totals['diffs']} "
          f"per_request={totals['per-request']} validator={totals['validator']} "
          f"representation={totals['representation']} policy={totals['policy']} "
          f"unknown={totals['unknown']} verdict={overall}")
    return 0


# --------------------------------------------------------------------- selftest

def write_pair(root: Path, surface_id: str, headers_a: dict[str, str],
               headers_b: dict[str, str], body_a: bytes, body_b: bytes,
               status_a: int = 200, status_b: int = 200) -> None:
    for tree, headers, body, status in (("a", headers_a, body_a, status_a),
                                        ("b", headers_b, body_b, status_b)):
        directory = root / tree / surface_id
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "body.bin").write_bytes(body)
        receipt = {
            "bodyFile": "body.bin",
            "bytes": len(body),
            "fetchedAt": "2026-11-04T00:00:00Z",
            "finalUrl": "https://example.test/",
            "headers": [{"name": name, "value": value} for name, value in headers.items()],
            "method": "GET",
            "sha256": hashlib.sha256(body).hexdigest(),
            "status": status,
            "truncated": False,
            "url": "https://example.test/",
        }
        (directory / "response.json").write_text(json.dumps(receipt, indent=1), encoding="utf-8")


BASE_HEADERS = {"Date": "Tue, 04 Nov 2026 10:00:00 GMT", "ETag": '"v1"',
                "Content-Length": "5", "Content-Type": "text/plain",
                "Cache-Control": "max-age=600", "X-Cache": "HIT"}
LATER_HEADERS = dict(BASE_HEADERS, Date="Tue, 04 Nov 2026 11:00:00 GMT",
                     **{"X-Cache": "MISS"})


def edit_receipt(path: Path, mutate) -> None:
    document = json.loads(path.read_text(encoding="utf-8"))
    mutate(document)
    path.write_text(json.dumps(document, indent=1), encoding="utf-8")


def selftest(work: Path, declared_path: Path | None) -> int:
    results: list[tuple[str, bool, str]] = []

    def score(name: str, expect: dict[str, int], mutate) -> None:
        root = work / name
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        (root / "d.json").write_text(json.dumps(
            {"surfaces": [{"id": "s1", "url": "https://example.test/"}]}), encoding="utf-8")
        write_pair(root, "s1", BASE_HEADERS, LATER_HEADERS, b"hello", b"hello")
        mutate(root)
        a, detail_a = load_surface(root / "a" / "s1")
        b, detail_b = load_surface(root / "b" / "s1")
        if a is None or b is None:
            results.append((name, False, f"{detail_a} {detail_b}"))
            return
        counts, verdict = classify(a, b)
        observed = {**counts, "verdict_representation": int(verdict == "representation-changed")}
        ok = all(observed.get(key) == value for key, value in expect.items())
        results.append((name, ok, f"observed={observed} expect={expect}"))

    def validator_change(root: Path) -> None:
        edit_receipt(root / "b/s1/response.json",
                     lambda doc: [item.update({"value": "\"v2\""})
                                  for item in doc["headers"] if item["name"] == "ETag"])

    def unknown_change(root: Path) -> None:
        edit_receipt(root / "b/s1/response.json",
                     lambda doc: [item.update({"name": "X-Mystery"})
                                  for item in doc["headers"] if item["name"] == "ETag"])

    def policy_change(root: Path) -> None:
        edit_receipt(root / "b/s1/response.json",
                     lambda doc: [item.update({"value": "max-age=120"})
                                  for item in doc["headers"] if item["name"] == "Cache-Control"])

    def body_change(root: Path) -> None:
        body = b"hellx"
        (root / "b/s1/body.bin").write_bytes(body)

        def patch(doc, body=body):
            doc["bytes"] = len(body)
            doc["sha256"] = hashlib.sha256(body).hexdigest()

        edit_receipt(root / "b/s1/response.json", patch)

    score("same-object-per-request-only",
          {"per-request": 2, "validator": 0, "representation": 0, "unknown": 0,
           "verdict_representation": 0}, lambda root: None)
    score("validator-change", {"validator": 1, "verdict_representation": 1}, validator_change)
    score("unknown-header-change", {"unknown": 1, "verdict_representation": 1}, unknown_change)
    score("policy-change-only", {"policy": 1, "verdict_representation": 0}, policy_change)
    score("body-change", {"validator": 0, "verdict_representation": 1}, body_change)

    bad = work / "bytes-mismatch"
    bad.mkdir(parents=True, exist_ok=True)
    (bad / "d.json").write_text(json.dumps(
        {"surfaces": [{"id": "s1", "url": "https://example.test/"}]}), encoding="utf-8")
    write_pair(bad, "s1", BASE_HEADERS, LATER_HEADERS, b"hello", b"hello")
    edit_receipt(bad / "b/s1/response.json", lambda doc: doc.update({"bytes": 6}))
    results.append(("bytes-mismatch-rejected",
                    load_surface(bad / "b" / "s1")[0] is None, ""))

    passed = sum(1 for _name, ok, _detail in results if ok)
    for name, ok, detail in results:
        print(("ok   " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))
    print(f"selftest: {passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--a")
    parser.add_argument("--b")
    parser.add_argument("--declared")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--work")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    if args.selftest:
        own = args.work is None
        work = Path(args.work) if args.work else Path(tempfile.mkdtemp(prefix="hcc-selftest-"))
        try:
            return selftest(work, None)
        finally:
            if own:
                shutil.rmtree(work, ignore_errors=True)
    if not (args.a and args.b and args.declared):
        parser.print_usage(sys.stderr)
        return 64
    return run(Path(args.a).resolve(), Path(args.b).resolve(), Path(args.declared).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
