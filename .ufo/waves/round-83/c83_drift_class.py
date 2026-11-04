#!/usr/bin/env python3
"""Round-83 C2 counter — header-change classification of the drift gate (kake, freshness).

Decides, from committed lane bytes, whether the lane classifies every header
that moved between the round-81 and round-82 captures, whether that
classification is decision-grade (all changed fields are per-request or policy,
so the two instants observed the same stored representation), and whether
`scripts/header_change_class.py` re-derives the committed record byte-for-byte
at a measured revision, offline, with a fixture that flips the verdict.

Frozen predicate (contract §C2):

    met <=> declared == 3
        and surfaces_a == 3 and surfaces_b == 3
        and receipts_ok   (GET, integer status 100..599, bytes == body length,
                           sha256 == body digest, truncated false)
        and diffs > 0 and validator == 0 and representation == 0 and unknown == 0
        and verdict == same-object
        and record_equal  (committed record == fresh stdout, one trailing
                           newline stripped per side)
        and determinism   (two fresh runs print identical bytes)
        and control_ok    (the round-83 control pair verifies and classifies
                           representation-changed with validator >= 1)
        and tool_offline  (no socket/urllib/requests/http.client reference
                           outside the tool's module docstring)
        and selftest_ok   (the tool's selftest exits 0)

Usage: c83_drift_class.py --root <lane> [--revision <rev>] [--work <dir>] [--selftest]

Exit: 0 met, 1 measured defect, 2 unevaluable input, 64 usage. Offline.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

BASE_CAPTURE = ".ufo/waves/round-81/capture"
ROUND_CAPTURE = ".ufo/waves/round-82/capture"
CONTROL_A = ".ufo/waves/round-83/capture-control/a"
CONTROL_B = ".ufo/waves/round-83/capture-control/b"
DECLARATION = ".ufo/waves/round-81/capture-expectations.json"
RECORD = ".ufo/waves/round-83/controls/after-c2-classes.txt"
TOOL = "scripts/header_change_class.py"
NETWORK = re.compile(r"\b(?:socket|urllib|requests|http\.client|httpx)\b")

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


def export(root: Path, revision: str, work: Path) -> Path:
    target = work / "export"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    proc = subprocess.run(
        ["git", "-C", str(root), "archive", "--format=tar", revision],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"git archive {revision} failed: {proc.stderr.decode('utf-8', 'replace').strip()}"
        )
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as archive:
        archive.extractall(target)
    return target


def declared_surfaces(root: Path) -> list[str] | None:
    path = root / DECLARATION
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
        return [str(item["id"]) for item in document["surfaces"]]
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        return None


def load_surface(directory: Path) -> tuple[dict | None, str]:
    receipt_path = directory / "response.json"
    if not receipt_path.is_file():
        return None, f"no response.json under {directory.name}"
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
        return None, "body sha256 mismatch"
    if receipt.get("truncated") is not False:
        return None, "truncated or silent"
    headers = receipt.get("headers")
    if not isinstance(headers, list):
        return None, "headers is not a list"
    merged: dict[str, list[str]] = {}
    for item in headers:
        if isinstance(item, dict):
            name = str(item.get("name", "")).strip().lower()
            if name:
                merged.setdefault(name, []).append(str(item.get("value", "")))
    return {
        "status": status,
        "sha256": digest,
        "headers": {name: ", ".join(values) for name, values in merged.items()},
    }, ""


def tree_receipts(root: Path, rel: str, declared: list[str]) -> tuple[bool, dict[str, dict], list[str]]:
    ok = True
    receipts: dict[str, dict] = {}
    problems: list[str] = []
    for surface in declared:
        receipt, detail = load_surface(root / rel / surface)
        if receipt is None:
            ok = False
            problems.append(f"{surface}: {detail}")
            continue
        receipts[surface] = receipt
    return ok, receipts, problems


def classify(a: dict, b: dict) -> tuple[dict, str]:
    counts = {"per-request": 0, "validator": 0, "representation": 0,
              "policy": 0, "unknown": 0}
    changed = 0
    for name in set(a["headers"]) | set(b["headers"]):
        if a["headers"].get(name) == b["headers"].get(name):
            continue
        changed += 1
        counts[header_class(name)] += 1
    decisive = (a["status"] != b["status"] or a["sha256"] != b["sha256"]
                or counts["validator"] or counts["representation"]
                or counts["unknown"])
    counts["diffs"] = changed
    return counts, ("representation-changed" if decisive else "same-object")


def tool_command(root: Path) -> list[str]:
    return [sys.executable, "-B", str(root / TOOL),
            "--a", str(root / BASE_CAPTURE), "--b", str(root / ROUND_CAPTURE),
            "--declared", str(root / DECLARATION)]


def run_tool(root: Path) -> tuple[int, bytes]:
    proc = subprocess.run(tool_command(root), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    return proc.returncode, proc.stdout


def tool_offline(root: Path) -> bool:
    path = root / TOOL
    if not path.is_file():
        return False
    source = path.read_text(encoding="utf-8", errors="replace")
    try:
        body = ast.parse(source).body
    except SyntaxError:
        return False
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
            and isinstance(body[0].value.value, str):
        source = source.replace(body[0].value.value, "")
    return NETWORK.search(source) is None


def measure(root: Path, work: Path) -> tuple[dict, dict]:
    flags: dict[str, object] = {}
    info: dict[str, object] = {}
    declared = declared_surfaces(root)
    flags["declared"] = len(declared) if declared else 0
    flags["tool_absent"] = int(not (root / TOOL).is_file())
    if declared is None:
        flags.update({"surfaces_a": 0, "surfaces_b": 0, "receipts_ok": 0,
                      "diffs": 0, "validator": 0, "representation": 0,
                      "unknown": 0, "verdict": "none", "record_equal": 0,
                      "determinism": 0, "control_ok": 0, "tool_offline": 0,
                      "selftest_ok": 0, "met": False})
        return flags, info

    a_ok, a_receipts, a_problems = tree_receipts(root, BASE_CAPTURE, declared)
    b_ok, b_receipts, b_problems = tree_receipts(root, ROUND_CAPTURE, declared)
    flags["surfaces_a"] = len(a_receipts)
    flags["surfaces_b"] = len(b_receipts)
    flags["receipts_ok"] = int(a_ok and b_ok)
    info["problems"] = a_problems + b_problems

    totals = {"diffs": 0, "per-request": 0, "validator": 0, "representation": 0,
              "policy": 0, "unknown": 0}
    verdict = "same-object"
    for surface in declared:
        if surface not in a_receipts or surface not in b_receipts:
            verdict = "none"
            continue
        counts, surface_verdict = classify(a_receipts[surface], b_receipts[surface])
        if surface_verdict == "representation-changed":
            verdict = "representation-changed"
        for key in totals:
            totals[key] += counts[key]
    flags.update(totals)
    flags["verdict"] = verdict

    rc1, out1 = run_tool(root)
    rc2, out2 = run_tool(root)
    flags["determinism"] = int(rc1 == 0 and rc2 == 0 and out1 == out2)
    record_path = root / RECORD
    record = record_path.read_bytes() if record_path.is_file() else None
    flags["record_equal"] = int(record is not None and rc1 == 0
                                and record.rstrip(b"\n") == out1.rstrip(b"\n"))

    ctl_ok_a, ctl_a, _ = tree_receipts(root, CONTROL_A, declared)
    ctl_ok_b, ctl_b, _ = tree_receipts(root, CONTROL_B, declared)
    control_ok = 0
    if ctl_ok_a and ctl_ok_b and len(ctl_a) == len(declared) == len(ctl_b):
        ctl_totals = {"validator": 0, "representation": 0, "unknown": 0}
        ctl_verdict = "same-object"
        for surface in declared:
            counts, surface_verdict = classify(ctl_a[surface], ctl_b[surface])
            if surface_verdict == "representation-changed":
                ctl_verdict = "representation-changed"
            for key in ctl_totals:
                ctl_totals[key] += counts[key]
        control_ok = int(ctl_verdict == "representation-changed"
                         and ctl_totals["validator"] >= 1)
        info["control"] = f"verdict={ctl_verdict} validator={ctl_totals['validator']}"
    else:
        info["control"] = "missing or unverifiable"
    flags["control_ok"] = control_ok

    flags["tool_offline"] = int(tool_offline(root))
    proc = subprocess.run([sys.executable, "-B", str(root / TOOL), "--selftest",
                           "--work", str(work / "selftest")],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    flags["selftest_ok"] = int(proc.returncode == 0 and b"selftest:" in proc.stdout)
    info["selftest"] = proc.stdout.decode("utf-8", "replace").strip().splitlines()[-1:] or [""]

    flags["met"] = (flags["declared"] == 3 and flags["surfaces_a"] == 3
                    and flags["surfaces_b"] == 3 and flags["receipts_ok"] == 1
                    and isinstance(flags["diffs"], int) and flags["diffs"] > 0
                    and flags["validator"] == 0 and flags["representation"] == 0
                    and flags["unknown"] == 0 and flags["verdict"] == "same-object"
                    and flags["record_equal"] == 1 and flags["determinism"] == 1
                    and flags["control_ok"] == 1 and flags["tool_offline"] == 1
                    and flags["selftest_ok"] == 1)
    return flags, info


def verdict_line(label: str, flags: dict) -> str:
    return (f"C2v1 revision={label} declared={flags['declared']} "
            f"surfaces_a={flags['surfaces_a']} surfaces_b={flags['surfaces_b']} "
            f"receipts_ok={flags['receipts_ok']} diffs={flags['diffs']} "
            f"validator={flags['validator']} representation={flags['representation']} "
            f"unknown={flags['unknown']} verdict={flags['verdict']} "
            f"record_equal={flags['record_equal']} determinism={flags['determinism']} "
            f"control_ok={flags['control_ok']} tool_offline={flags['tool_offline']} "
            f"selftest_ok={flags['selftest_ok']} tool_absent={flags['tool_absent']} "
            f"met={'true' if flags['met'] else 'false'}")


def run(root: Path, revision: str | None, work: Path) -> int:
    if revision:
        tree = export(root, revision, work)
        label = revision
    else:
        tree = root
        label = "worktree"
    flags, info = measure(tree, work)
    print(verdict_line(label, flags))
    if info.get("problems"):
        print(f"# problems={info['problems']}")
    if info.get("control"):
        print(f"# control={info['control']}")
    return 0 if flags["met"] else 1


# --------------------------------------------------------------------- selftest

def write_receipt(directory: Path, body: bytes, headers: dict[str, str],
                  status: int = 200) -> None:
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


SURFACES = ("s1", "s2", "s3")
STABLE = {"ETag": '"v1"', "Content-Length": "5", "Content-Type": "text/plain",
          "Cache-Control": "max-age=600", "Vary": "Accept-Encoding"}
A_HEADERS = dict(STABLE, Date="Tue, 04 Nov 2026 10:00:00 GMT", **{"X-Cache": "HIT"})
B_HEADERS = dict(STABLE, Date="Tue, 04 Nov 2026 11:00:00 GMT", **{"X-Cache": "MISS"})


def build_green(root: Path, tool_source: Path) -> None:
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / TOOL).write_text(tool_source.read_text(encoding="utf-8"), encoding="utf-8")
    (root / DECLARATION).parent.mkdir(parents=True, exist_ok=True)
    (root / DECLARATION).write_text(json.dumps(
        {"surfaces": [{"id": s, "url": "https://example.test/"} for s in SURFACES]}),
        encoding="utf-8")
    for surface in SURFACES:
        write_receipt(root / BASE_CAPTURE / surface, b"hello", A_HEADERS)
        write_receipt(root / ROUND_CAPTURE / surface, b"hello", B_HEADERS)
        write_receipt(root / CONTROL_A / surface, b"hello", A_HEADERS)
        control_b = dict(B_HEADERS, ETag='"v2"')
        write_receipt(root / CONTROL_B / surface, b"hellx", control_b)
    (root / RECORD).parent.mkdir(parents=True, exist_ok=True)
    rc, out = run_tool(root)
    if rc != 0:
        raise RuntimeError("green fixture: tool failed")
    (root / RECORD).write_bytes(out)


def selftest() -> int:
    work = Path(tempfile.mkdtemp(prefix="c83-drift-selftest-"))
    results: list[tuple[str, bool, str]] = []
    try:
        tool_source = Path(__file__).resolve().parents[3] / TOOL
        if not tool_source.is_file():
            print(f"FAIL no tool at {tool_source}")
            return 1

        def score(name: str, expect_met: bool, mutate) -> None:
            root = work / name
            if root.exists():
                shutil.rmtree(root)
            root.mkdir(parents=True)
            build_green(root, tool_source)
            mutate(root)
            try:
                flags, _info = measure(root, work / (name + "-w"))
            except Exception as exc:  # a broken fixture must fail, not crash the suite
                results.append((name, False, f"exception: {exc}"))
                return
            ok = bool(flags["met"]) == expect_met
            results.append((name, ok, f"met={flags['met']} expect={expect_met}"))

        score("green", True, lambda root: None)

        def body_mutant(root: Path) -> None:
            write_receipt(root / ROUND_CAPTURE / "s1", b"hellx", B_HEADERS)

        score("body-changed", False, body_mutant)

        def validator_mutant(root: Path) -> None:
            write_receipt(root / ROUND_CAPTURE / "s1", b"hello", dict(B_HEADERS, ETag='"v2"'))

        score("validator-changed", False, validator_mutant)

        def record_mutant(root: Path) -> None:
            (root / RECORD).write_text("summary surfaces=3 diffs=0 verdict=same-object\n")

        score("record-mismatch", False, record_mutant)

        def control_mutant(root: Path) -> None:
            for surface in SURFACES:
                write_receipt(root / CONTROL_B / surface, b"hello", B_HEADERS)

        score("control-does-not-flip", False, control_mutant)

        def tool_mutant(root: Path) -> None:
            (root / TOOL).unlink()

        score("tool-absent", False, tool_mutant)

        def decl_mutant(root: Path) -> None:
            (root / DECLARATION).parent.mkdir(parents=True, exist_ok=True)
            (root / DECLARATION).write_text(json.dumps(
                {"surfaces": [{"id": "s1", "url": "https://example.test/"}]}), encoding="utf-8")

        score("declared-dropped", False, decl_mutant)

        def drop_a_surface(root: Path) -> None:
            shutil.rmtree(root / BASE_CAPTURE / "s3")

        score("capture-a-dropped-surface", False, drop_a_surface)

        def offline_mutant(root: Path) -> None:
            text = (root / TOOL).read_text(encoding="utf-8")
            (root / TOOL).write_text(text + "\nimport socket\n", encoding="utf-8")

        score("tool-network-import", False, offline_mutant)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    passed = sum(1 for _name, ok, _detail in results if ok)
    for name, ok, detail in results:
        print(("ok   " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))
    print(f"selftest: {passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".")
    parser.add_argument("--revision")
    parser.add_argument("--work")
    parser.add_argument("--selftest", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    if args.selftest:
        return selftest()
    root = Path(args.root).resolve()
    if not (root / ".git").exists() and args.revision:
        print("fault (tree) root carries no git repository", file=sys.stderr)
        return 2
    work = Path(args.work) if args.work else Path(tempfile.mkdtemp(prefix="c83-drift-"))
    own_work = args.work is None
    try:
        return run(root, args.revision, work)
    except RuntimeError as exc:
        print(f"fault (tree) {exc}", file=sys.stderr)
        return 2
    finally:
        if own_work:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
