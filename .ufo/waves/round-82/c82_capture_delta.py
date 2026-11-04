#!/usr/bin/env python3
"""Round-82 C2 counter — capture-to-capture drift gate (kake, freshness).

Decides, from committed lane bytes, whether the lane holds two dated captures
of the surfaces declared in `.ufo/waves/round-81/capture-expectations.json`
and whether `scripts/capture_delta.py` re-derives the committed delta record
from them byte-for-byte at a measured revision, offline.

Frozen predicate (contract §C2):

    met <=> declared == 3
        and the round-82 manifest declares exactly the declared ids and urls
        and surfaces_a == declared and surfaces_b == declared
        and receipts_ok      (every receipt verifies against its retained body:
                              method GET, integer status 100..599, integer byte
                              count equal to the body length, body sha256 equal
                              to the receipt digest, truncated false, RFC 3339
                              fetchedAt)
        and order_ok         (each round-82 instant is strictly after its
                              round-81 instant)
        and floor_ok         (each round-82 instant is on or after
                              2026-11-04T12:42:00Z, the round start)
        and record_equal     (the committed record equals a fresh run's stdout
                              after stripping one trailing newline per side)
        and determinism      (two fresh runs print identical bytes)
        and selftest_ok      (the tool's selftest exits 0 with >= 12 cases)

Usage: c82_capture_delta.py --root <lane> [--revision <rev>] [--work <dir>]
       [--selftest]

Exit: 0 met, 1 measured defect, 2 unevaluable input, 64 usage. Offline.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

BASE_CAPTURE = ".ufo/waves/round-81/capture"
ROUND_CAPTURE = ".ufo/waves/round-82/capture"
DECLARATION = ".ufo/waves/round-81/capture-expectations.json"
RECORD = ".ufo/waves/round-82/controls/after-c2-delta.txt"
TOOL = "scripts/capture_delta.py"
FLOOR = "2026-11-04T12:42:00Z"
HEX64 = re.compile(r"[0-9a-f]{64}")
RFC3339 = re.compile(
    r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d+)?(Z|[+-]\d{2}:\d{2})"
)
SAFE_ID = re.compile(r"[a-z0-9][a-z0-9-]{0,62}")


def parse_instant(value: object) -> datetime.datetime | None:
    if not isinstance(value, str):
        return None
    match = RFC3339.fullmatch(value)
    if not match:
        return None
    parts = [int(match.group(i)) for i in range(1, 7)]
    zone = match.group(7)
    try:
        if zone == "Z":
            tz = datetime.timezone.utc
        else:
            sign = 1 if zone[0] == "+" else -1
            tz = datetime.timezone(sign * datetime.timedelta(
                hours=int(zone[1:3]), minutes=int(zone[4:6])))
        return datetime.datetime(*parts, tzinfo=tz)
    except ValueError:
        return None


def export(root: Path, revision: str, work: Path) -> Path:
    target = work / "export"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    proc = subprocess.run(["git", "-C", str(root), "archive", "--format=tar", revision],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"git archive {revision} failed: "
                           f"{proc.stderr.decode('utf-8', 'replace').strip()}")
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as archive:
        archive.extractall(target)
    return target


def load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        with open(path, encoding="utf-8") as stream:
            value = json.load(stream)
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def declared_surfaces(root: Path) -> list[tuple[str, str]] | None:
    value = load_json(root / DECLARATION)
    if value is None or not isinstance(value.get("surfaces"), list):
        return None
    pairs = []
    for entry in value["surfaces"]:
        if not isinstance(entry, dict):
            return None
        surface, url = entry.get("id"), entry.get("url")
        if not isinstance(surface, str) or not SAFE_ID.fullmatch(surface):
            return None
        if not isinstance(url, str) or not url.startswith("https://"):
            return None
        pairs.append((surface, url))
    return pairs


def tree_surfaces(root: Path, rel: str) -> tuple[int, str] | None:
    """Return (surface count, detail) for one capture tree."""
    manifest = load_json(root / rel / "manifest.json")
    if manifest is None or not isinstance(manifest.get("checks"), list):
        return None
    return len(manifest["checks"]), rel


def verify_tree(root: Path, rel: str) -> tuple[bool, dict[str, datetime.datetime], str]:
    manifest = load_json(root / rel / "manifest.json")
    if manifest is None or not isinstance(manifest.get("checks"), list):
        return False, {}, "manifest absent"
    instants: dict[str, datetime.datetime] = {}
    for check in manifest["checks"]:
        if not isinstance(check, dict):
            return False, {}, "check is not an object"
        surface = check.get("id")
        if not isinstance(surface, str) or not SAFE_ID.fullmatch(surface):
            return False, {}, "unsafe surface id"
        leaf = root / rel / surface
        receipt = load_json(leaf / "response.json")
        if receipt is None:
            return False, {}, f"{surface}: response.json absent"
        if receipt.get("method") != "GET":
            return False, {}, f"{surface}: method is not GET"
        status = receipt.get("status")
        if not isinstance(status, int) or isinstance(status, bool) or not 100 <= status <= 599:
            return False, {}, f"{surface}: status is not an integer in 100..599"
        if receipt.get("truncated") is not False:
            return False, {}, f"{surface}: truncated is not false"
        instant = parse_instant(receipt.get("fetchedAt"))
        if instant is None:
            return False, {}, f"{surface}: fetchedAt is not an RFC 3339 instant"
        size = receipt.get("bytes")
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            return False, {}, f"{surface}: bytes is not a non-negative integer"
        digest = receipt.get("sha256")
        if not isinstance(digest, str) or not HEX64.fullmatch(digest):
            return False, {}, f"{surface}: sha256 is not 64 lowercase hex digits"
        body_path = leaf / "body.bin"
        if body_path.is_file():
            body = body_path.read_bytes()
            if len(body) != size:
                return False, {}, f"{surface}: body bytes {len(body)} != receipt {size}"
            actual = hashlib.sha256(body).hexdigest()
            if actual != digest:
                return False, {}, f"{surface}: body sha256 != receipt digest"
        elif size != 0:
            return False, {}, f"{surface}: body.bin absent while receipt claims {size} bytes"
        instants[surface] = instant
    return True, instants, f"{len(instants)} surfaces"


def manifest_pairs(root: Path, rel: str) -> list[tuple[str, str]] | None:
    manifest = load_json(root / rel / "manifest.json")
    if manifest is None or not isinstance(manifest.get("checks"), list):
        return None
    pairs = []
    for check in manifest["checks"]:
        if not isinstance(check, dict):
            return None
        surface, url = check.get("id"), check.get("url")
        if not isinstance(surface, str) or not isinstance(url, str):
            return None
        pairs.append((surface, url))
    return pairs


def run_tool(root: Path, work: Path) -> tuple[int, bytes]:
    tool = root / TOOL
    if not tool.is_file():
        return 127, b""
    env = dict(os.environ)
    env["TMPDIR"] = str(work)
    proc = subprocess.run(
        [sys.executable, "-B", str(tool), "--a", str(root / BASE_CAPTURE),
         "--b", str(root / ROUND_CAPTURE)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, env=env, cwd=str(root),
    )
    return proc.returncode, proc.stdout


def run_tool_selftest(root: Path, work: Path) -> tuple[bool, str]:
    tool = root / TOOL
    if not tool.is_file():
        return False, "tool absent"
    env = dict(os.environ)
    env["TMPDIR"] = str(work)
    proc = subprocess.run([sys.executable, "-B", str(tool), "--selftest"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
                          env=env, cwd=str(root))
    text = proc.stdout.decode("utf-8", "replace")
    match = re.search(r"selftest: (\d+)/(\d+) passed", text)
    if proc.returncode != 0 or match is None:
        return False, f"selftest rc={proc.returncode}"
    passed, total = int(match.group(1)), int(match.group(2))
    return passed == total and total >= 12, f"selftest {passed}/{total}"


def measure(root: Path, work: Path) -> tuple[dict, dict]:
    flags: dict[str, object] = {}
    info: dict[str, object] = {}
    declared = declared_surfaces(root)
    flags["declared"] = len(declared) if declared else 0
    info["declared"] = flags["declared"]
    flags["surfaces_a"] = tree_surfaces(root, BASE_CAPTURE) or 0
    if isinstance(flags["surfaces_a"], tuple):
        flags["surfaces_a"] = flags["surfaces_a"][0]
    flags["surfaces_b"] = tree_surfaces(root, ROUND_CAPTURE) or 0
    if isinstance(flags["surfaces_b"], tuple):
        flags["surfaces_b"] = flags["surfaces_b"][0]

    a_ok, a_instants, a_detail = verify_tree(root, BASE_CAPTURE)
    b_ok, b_instants, b_detail = verify_tree(root, ROUND_CAPTURE)
    flags["receipts_ok"] = int(a_ok and b_ok and flags["surfaces_a"] == flags["declared"]
                               and flags["surfaces_b"] == flags["declared"])
    info["receipts_detail"] = f"a: {a_detail}; b: {b_detail}"

    a_pairs = manifest_pairs(root, BASE_CAPTURE)
    b_pairs = manifest_pairs(root, ROUND_CAPTURE)
    flags["manifest_ok"] = int(bool(declared) and a_pairs == declared and b_pairs == declared)

    floor = parse_instant(FLOOR)
    order_ok = bool(b_instants) and all(
        surface in a_instants and b_instants[surface] > a_instants[surface]
        for surface in b_instants
    )
    flags["order_ok"] = int(order_ok)
    flags["floor_ok"] = int(bool(b_instants) and floor is not None and all(
        instant >= floor for instant in b_instants.values()))

    rc1, out1 = run_tool(root, work / "run1")
    rc2, out2 = run_tool(root, work / "run2")
    flags["determinism"] = int(rc1 == 0 and rc2 == 0 and out1 == out2)
    record_path = root / RECORD
    record = record_path.read_bytes() if record_path.is_file() else None
    flags["record_equal"] = int(record is not None and rc1 == 0
                                and record.rstrip(b"\n") == out1.rstrip(b"\n"))

    selftest_ok, selftest_detail = run_tool_selftest(root, work / "selftest")
    flags["selftest_ok"] = int(selftest_ok)
    info["selftest"] = selftest_detail

    met = (flags["declared"] == 3
           and flags["surfaces_a"] == 3 and flags["surfaces_b"] == 3
           and all(int(flags[key]) == 1 for key in
                   ("receipts_ok", "manifest_ok", "order_ok", "floor_ok",
                    "determinism", "record_equal", "selftest_ok")))
    flags["met"] = met
    return flags, info


def verdict_line(label: str, flags: dict) -> str:
    return (f"C2v1 revision={label} declared={flags['declared']} "
            f"surfaces_a={flags['surfaces_a']} surfaces_b={flags['surfaces_b']} "
            f"manifest_ok={flags['manifest_ok']} receipts_ok={flags['receipts_ok']} "
            f"order_ok={flags['order_ok']} floor_ok={flags['floor_ok']} "
            f"determinism={flags['determinism']} record_equal={flags['record_equal']} "
            f"selftest_ok={flags['selftest_ok']} met={'true' if flags['met'] else 'false'}")


def run(root: Path, revision: str | None, work: Path) -> int:
    if revision:
        tree = export(root, revision, work)
        label = revision
    else:
        tree = root
        label = "worktree"
    flags, info = measure(tree, work)
    print(verdict_line(label, flags))
    print(f"# {info.get('receipts_detail')}")
    print(f"# {info.get('selftest')}")
    return 0 if flags["met"] else 1


# --------------------------------------------------------------------- selftest

FIXTURE_URLS = {
    "ds4cc-primary": "https://ds4cc.com/",
    "ds4cc-robots": "https://ds4cc.com/robots.txt",
    "ds4cc-sitemap": "https://ds4cc.com/sitemap.xml",
}


def write_fixture(path: Path, surfaces: list[tuple[str, bytes]], fetched: str) -> None:
    path.mkdir(parents=True, exist_ok=True)
    checks = []
    for surface, body in surfaces:
        leaf = path / surface
        leaf.mkdir(parents=True, exist_ok=True)
        url = FIXTURE_URLS[surface]
        meta = {
            "url": url,
            "finalUrl": url,
            "method": "GET",
            "status": 200,
            "headers": [{"name": "Content-Type", "value": "text/html"}],
            "headerCount": 1,
            "contentType": "text/html",
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "truncated": False,
            "fetchedAt": fetched,
            "userAgent": "round82-fixture",
            "redirects": [],
            "error": None,
            "bodyFile": "body.bin" if body else None,
        }
        (leaf / "response.json").write_text(json.dumps(meta, indent=1, sort_keys=True),
                                            encoding="utf-8")
        if body:
            (leaf / "body.bin").write_bytes(body)
        checks.append({"id": surface, "url": url,
                       "expect": {"content_type_present": True},
                       "source": f"{path.name}/{surface}/response.json"})
    (path / "manifest.json").write_text(json.dumps(
        {"version": 1, "allowlist": ["ds4cc.com"], "checks": checks},
        indent=1, sort_keys=True), encoding="utf-8")


def build_green(root: Path, tool_source: Path) -> None:
    declared = [
        {"id": "ds4cc-primary", "url": "https://ds4cc.com/"},
        {"id": "ds4cc-robots", "url": "https://ds4cc.com/robots.txt"},
        {"id": "ds4cc-sitemap", "url": "https://ds4cc.com/sitemap.xml"},
    ]
    (root / DECLARATION).parent.mkdir(parents=True, exist_ok=True)
    (root / DECLARATION).write_text(json.dumps({"version": 1, "surfaces": declared},
                                                indent=1), encoding="utf-8")
    surfaces = [("ds4cc-primary", b"<html>primary</html>"),
                ("ds4cc-robots", b"User-agent: *\nAllow: /\n"),
                ("ds4cc-sitemap", b"<urlset></urlset>")]
    write_fixture(root / BASE_CAPTURE, surfaces, "2026-11-04T12:05:06Z")
    write_fixture(root / ROUND_CAPTURE, surfaces, "2026-11-04T12:50:00Z")
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    shutil.copy2(tool_source, root / TOOL)
    work = root / "_work"
    work.mkdir(parents=True, exist_ok=True)
    rc, out = run_tool(root, work)
    if rc != 0:
        raise RuntimeError(f"fixture tool run failed rc={rc}")
    (root / RECORD).parent.mkdir(parents=True, exist_ok=True)
    (root / RECORD).write_bytes(out)
    shutil.rmtree(work, ignore_errors=True)


def selftest() -> int:
    tool_source = Path(__file__).resolve().parents[3] / TOOL
    work = Path(tempfile.mkdtemp(prefix="c82-capture-selftest-"))
    results: list[tuple[str, bool, str]] = []
    try:
        def score(name: str, expect_met: bool, mutate) -> None:
            root = work / ("root-" + name)
            if root.exists():
                shutil.rmtree(root)
            build_green(root, tool_source)
            mutate(root)
            run_work = work / ("work-" + name)
            run_work.mkdir(parents=True, exist_ok=True)
            try:
                flags, _info = measure(root, run_work)
                met = bool(flags["met"])
                results.append((name, met == expect_met,
                                "" if met == expect_met else
                                f"met={met} flags={ {k: v for k, v in flags.items()} }"))
            except Exception as exc:  # a fixture must not crash the selftest
                results.append((name, False, f"raised {type(exc).__name__}: {exc}"))
            finally:
                shutil.rmtree(run_work, ignore_errors=True)

        score("green-met", True, lambda root: None)
        score("base-control-no-round-capture", False,
              lambda root: shutil.rmtree(root / ROUND_CAPTURE))
        score("record-drift", False, lambda root: (root / RECORD).write_bytes(
            (root / RECORD).read_bytes().replace(b"surfaces=3", b"surfaces=4")))
        score("record-absent", False, lambda root: (root / RECORD).unlink())
        score("order-violation", False, lambda root: write_fixture(
            root / ROUND_CAPTURE,
            [("ds4cc-primary", b"<html>primary</html>"),
             ("ds4cc-robots", b"User-agent: *\nAllow: /\n"),
             ("ds4cc-sitemap", b"<urlset></urlset>")], "2026-11-04T11:00:00Z"))
        score("floor-violation", False, lambda root: write_fixture(
            root / ROUND_CAPTURE,
            [("ds4cc-primary", b"<html>primary</html>"),
             ("ds4cc-robots", b"User-agent: *\nAllow: /\n"),
             ("ds4cc-sitemap", b"<urlset></urlset>")], "2026-11-04T12:10:00Z"))
        score("dropped-surface", False, lambda root: write_fixture(
            root / ROUND_CAPTURE,
            [("ds4cc-primary", b"<html>primary</html>"),
             ("ds4cc-robots", b"User-agent: *\nAllow: /\n")], "2026-11-04T12:50:00Z"))
        score("tampered-body", False, lambda root: (
            root / ROUND_CAPTURE / "ds4cc-robots" / "body.bin").write_bytes(b"tampered"))
        score("tool-absent", False, lambda root: (root / TOOL).unlink())
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
    work = Path(args.work) if args.work else Path(tempfile.mkdtemp(prefix="c82-capture-"))
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
