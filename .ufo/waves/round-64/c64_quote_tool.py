#!/usr/bin/env python3
"""Round-64 C2 operability counter — the stub-proof quote-class tool gate.

Hardens the round-63 counter (c63_quote_tool.py) per the routed round-63
defects (corpus/lessons/round-63.md §Wave settlement item 4;
round-63-verifier-spotcheck.md routed defect 2):

  sha pin   — the tool is only executed when its blob at the measured
              revision has the frozen sha256 below. "Stub" is defined as
              "tool sha != frozen sha": the round-63 canned-JSON stub attack
              (w1/CriticClaims.md counterexample 2) fails before execution.
  revision  — the selftest runs in a scratch tree materialized entirely from
              the measured revision's blobs (tool, its four fixtures, and the
              two s432_real retained blobs at their repo-relative paths), so
              no worktree byte can influence the verdict.
  frozen set— every frozen case id must be present, passed, derive the frozen
              expected class, and this counter re-derives each case itself
              from the materialized fixture bytes (inline classify, round-50
              semantics) and rejects a tool whose printed derived disagrees
              with the counter's own derivation.
  guarded   — every JSON parse of tool output is guarded: an unparseable or
              shape-hostile output prints met=false, never a traceback. (With
              the sha pin the production path never executes a non-frozen
              tool at all; the guard is defense in depth and is exercised
              directly by the selftest.)

Frozen predicate (identical sentence in contract.md, this code and the
receipts): at the measured revision this counter prints met=true (exit 0)
over the lane tree; on the committed stub-fixture revision (fixture recipe
.ufo/waves/round-64/fixtures/build_fixtures.py) it prints tool_sha=mismatch
met=false (exit 1); and the round-63 counter c63_quote_tool.py, run on that
same stub fixture, prints met=true (exit 0) — the routed round-63 defect,
reproduced. (At the round-63 base the real tool already exists, so the base
tree also prints met=true; the stub differential is the claim's falsifiable
before/after, not the base.)

Usage: c64_quote_tool.py --root . --revision <rev>
       c64_quote_tool.py --selftest [--selftest-work <dir>]
Exits: 0 met or selftest green; 1 not met or selftest red;
       2 could-not-evaluate (input/usage fault).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

BASE = "1a48131577ba82c967650561be34e8dba909432a"  # round-63 tip
TOOL_REL = "scripts/quote_class.py"
FROZEN_TOOL_SHA = "431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14"
FIXTURE_RELS = [
    "scripts/fixtures/quote-class/inline.raw.html",
    "scripts/fixtures/quote-class/inline.txt",
    "scripts/fixtures/quote-class/markup.raw.html",
    "scripts/fixtures/quote-class/markup.txt",
    ".ufo/waves/round-61/sources/S432.html",
    ".ufo/waves/round-63/quote-class/S432.txt",
]
# frozen case table, mirroring the tool's FIXTURE_CASES at the frozen sha
FROZEN_CASES = {
    "inline_raw_substring": {
        "raw": "scripts/fixtures/quote-class/inline.raw.html",
        "text": "scripts/fixtures/quote-class/inline.txt",
        "quote": "quick brown fox",
        "expected": "raw-substring",
    },
    "markup_collapsed_only": {
        "raw": "scripts/fixtures/quote-class/markup.raw.html",
        "text": "scripts/fixtures/quote-class/markup.txt",
        "quote": "The `X-Content-Type-Options` header marks the response",
        "expected": "collapsed-only",
    },
    "absent_everywhere": {
        "raw": "scripts/fixtures/quote-class/inline.raw.html",
        "text": "scripts/fixtures/quote-class/inline.txt",
        "quote": "this span occurs in no retained blob at all",
        "expected": "absent",
    },
    "s432_real": {
        "raw": ".ufo/waves/round-61/sources/S432.html",
        "text": ".ufo/waves/round-63/quote-class/S432.txt",
        "quote": (
            "The `X-Content-Type-Options` response header can be used to "
            "require checking of a response\u2019s `Content-Type` header "
            "against the destination of a request."
        ),
        "expected": "collapsed-only",
    },
}
RUN_TIMEOUT = 120


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_show(root: str, revision: str, rel: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "-C", root, "show", f"{revision}:{rel}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        return None
    return proc.stdout


def classify(quote: str, raw: str, text: str) -> str:
    if quote in raw:
        return "raw-substring"
    if quote in text:
        return "collapsed-only"
    return "absent"


def safe_json(out: bytes):
    """Guarded JSON parse; returns (value, err). Never raises."""
    try:
        val = json.loads(out.decode("utf-8"))
    except Exception as exc:
        return None, f"unparseable:{type(exc).__name__}"
    if not isinstance(val, dict):
        return None, "not_object"
    return val, None


def materialize(blobs: dict[str, bytes], root: str) -> str:
    for rel, data in blobs.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)
    return root


def evaluate(root: str, rev: str) -> tuple[int, str]:
    probe = subprocess.run(
        ["git", "-C", root, "rev-parse", "--verify", rev],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if probe.returncode:
        print(f"could-not-evaluate: revision {rev} unreadable", file=sys.stderr)
        return 2, ""

    tool_blob = git_show(root, rev, TOOL_REL)
    if tool_blob is None:
        print(f"revision={rev} present=0 tool_sha=absent selftest=unevaluable "
              f"frozen_cases=missing rederive=unevaluable met=false")
        return 1, ""

    tool_sha = sha256(tool_blob)
    if tool_sha != FROZEN_TOOL_SHA:
        print(f"revision={rev} present=1 tool_sha=mismatch selftest=skipped "
              f"frozen_cases=missing rederive=unevaluable met=false")
        return 1, ""

    blobs = {TOOL_REL: tool_blob}
    for rel in FIXTURE_RELS:
        b = git_show(root, rev, rel)
        if b is None:
            print(f"could-not-evaluate: fixture absent at revision: {rel}",
                  file=sys.stderr)
            return 2, ""
        blobs[rel] = b

    work = tempfile.mkdtemp(prefix="c64tool-")
    try:
        materialize(blobs, work)
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
               "HOME": work, "TMPDIR": work, "LANG": "C"}
        try:
            proc = subprocess.run(
                [sys.executable, "-B", os.path.join(work, TOOL_REL),
                 "--selftest", "--json"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=work,
                env=env, timeout=RUN_TIMEOUT, check=False)
        except subprocess.TimeoutExpired:
            print(f"revision={rev} present=1 tool_sha=ok selftest=timeout "
                  f"frozen_cases=missing rederive=unevaluable met=false")
            return 1, ""
    finally:
        shutil.rmtree(work, ignore_errors=True)

    if proc.returncode != 0:
        print(f"revision={rev} present=1 tool_sha=ok selftest=failed "
              f"frozen_cases=missing rederive=unevaluable met=false")
        return 1, ""
    val, err = safe_json(proc.stdout)
    if val is None:
        print(f"revision={rev} present=1 tool_sha=ok selftest={err} "
              f"frozen_cases=missing rederive=unevaluable met=false")
        return 1, ""
    cases = val.get("cases")
    if not isinstance(cases, list):
        print(f"revision={rev} present=1 tool_sha=ok selftest=shape_invalid "
              f"frozen_cases=missing rederive=unevaluable met=false")
        return 1, ""
    by_id = {c.get("id"): c for c in cases if isinstance(c, dict)}
    frozen_ok = all(
        by_id.get(cid, {}).get("passed") is True
        and by_id.get(cid, {}).get("derived") == spec["expected"]
        for cid, spec in FROZEN_CASES.items())
    total, passed = val.get("total"), val.get("passed")
    totals_ok = (isinstance(total, int) and isinstance(passed, int)
                 and total == passed == len(FROZEN_CASES))
    # counter-side re-derivation from the revision's own fixture bytes
    rederive_ok = True
    for cid, spec in FROZEN_CASES.items():
        try:
            raw = blobs[spec["raw"]].decode("utf-8", errors="replace")
            text = blobs[spec["text"]].decode("utf-8", errors="replace")
            mine = classify(spec["quote"], raw, text)
        except Exception:
            mine = "unevaluable"
        if mine != spec["expected"]:
            rederive_ok = False
        if by_id.get(cid, {}).get("derived") not in (None, mine):
            rederive_ok = False

    met = bool(frozen_ok and totals_ok and rederive_ok
               and val.get("ok") is True)
    print(f"revision={rev} present=1 tool_sha=ok "
          f"selftest={passed if isinstance(passed, int) else '?'}/"
          f"{total if isinstance(total, int) else '?'} "
          f"frozen_cases={'ok' if frozen_ok else 'missing'} "
          f"rederive={'agree' if rederive_ok else 'differ'} met={str(met).lower()}")
    return (0 if met else 1), ""


# ----------------------------- selftest ------------------------------------

STUB_TOOL = '''#!/usr/bin/env python3
import json, sys
if "--selftest" in sys.argv:
    print(json.dumps({"cases": [
        {"id": "inline_raw_substring", "derived": "raw-substring", "expected": "raw-substring", "passed": True},
        {"id": "markup_collapsed_only", "derived": "collapsed-only", "expected": "collapsed-only", "passed": True},
        {"id": "absent_everywhere", "derived": "absent", "expected": "absent", "passed": True},
        {"id": "s432_real", "derived": "collapsed-only", "expected": "collapsed-only", "passed": True}],
        "total": 4, "passed": 4, "ok": True}, sort_keys=True))
sys.exit(0)
'''

LYING_TOOL = STUB_TOOL.replace('"passed": True}', '"passed": False}', 1)
CRASH_TOOL = 'import sys\nsys.exit(3)\n'
GARBAGE_TOOL = 'print("not json at all")\n'


def _fixture(work: str, name: str, files: dict[str, bytes]) -> str:
    d = os.path.join(work, name)
    os.makedirs(d, exist_ok=True)
    for rel, data in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)
    def git(*a):
        return subprocess.run(["git", "-C", d, *a],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    git("init", "-q")
    top = git("rev-parse", "--show-toplevel")
    assert top.returncode == 0 and os.path.realpath(top.stdout.decode().strip()) == os.path.realpath(d)
    git("config", "user.name", "c64-selftest")
    git("config", "user.email", "c64-selftest@fixture.invalid")
    git("add", "-A")
    c = git("commit", "-q", "--allow-empty", "-m", "fixture")
    assert c.returncode == 0
    return d


def _head(d: str) -> str:
    return subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                          stdout=subprocess.PIPE, check=True).stdout.decode().strip()


def run_selftest(root: str, workdir: str | None) -> int:
    checks: list[tuple[str, bool]] = []

    def expect(name, cond):
        checks.append((name, bool(cond)))

    def run_main(d: str, rev: str):
        proc = subprocess.run(
            [sys.executable, "-B", os.path.abspath(__file__),
             "--root", d, "--revision", rev],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=dict(os.environ))
        return proc.returncode, proc.stdout.decode(), proc.stderr.decode()

    work = workdir or tempfile.mkdtemp(prefix="c64tool-selftest-")
    os.makedirs(work, exist_ok=True)

    try:
        # T1 no tool at the revision
        d = _fixture(work, "t1-empty", {})
        code, out, err = run_main(d, _head(d))
        expect("t1 exit1", code == 1)
        expect("t1 present0", "present=0" in out and "met=false" in out)

        # T2 canned-JSON stub (the round-63 attack) -> sha mismatch, never run
        d = _fixture(work, "t2-stub", {TOOL_REL: STUB_TOOL.encode()})
        code, out, err = run_main(d, _head(d))
        expect("t2 exit1", code == 1)
        expect("t2 mismatch", "tool_sha=mismatch" in out and "met=false" in out)

        # T3 lying stub (frozen ids, failed flag) -> still sha mismatch
        d = _fixture(work, "t3-lying", {TOOL_REL: LYING_TOOL.encode()})
        code, out, err = run_main(d, _head(d))
        expect("t3 mismatch", "tool_sha=mismatch" in out)

        # T4 guard unit: garbage output parses to an error token, no raise
        val, errtok = safe_json(b"not json at all")
        expect("t4 garbage", val is None and errtok.startswith("unparseable"))
        val, errtok = safe_json(b"[1,2,3]")
        expect("t4 notobject", val is None and errtok == "not_object")

        # T5 crash tool path via a controlled non-frozen run is unreachable in
        # production (sha pin); assert the printed finding for a crash by
        # calling the counter against a revision whose tool is a crash stub:
        # the sha pin fires first, so production never executes it.
        d = _fixture(work, "t5-crash", {TOOL_REL: CRASH_TOOL.encode()})
        code, out, err = run_main(d, _head(d))
        expect("t5 mismatch-first", code == 1 and "tool_sha=mismatch" in out)

        # T6 bad revision -> exit 2
        d = _fixture(work, "t6-spot", {})
        code, out, err = run_main(d, "bogus-revision")
        expect("t6 exit2", code == 2 and "unreadable" in err)

        # T7 the real tool at the real base: frozen blobs present, selftest
        # runs and must be green (capability check with real committed bytes)
        blobs = {TOOL_REL: git_show(root, BASE, TOOL_REL)}
        for rel in FIXTURE_RELS:
            blobs[rel] = git_show(root, BASE, rel)
        if any(v is None for v in blobs.values()):
            print("selftest 0/0: base tool/fixtures unavailable at --root",
                  file=sys.stderr)
            return 2
        d = _fixture(work, "t7-real", blobs)
        code, out, err = run_main(d, _head(d))
        expect("t7 exit0", code == 0)
        expect("t7 green", "met=true" in out and "tool_sha=ok" in out
               and "rederive=agree" in out)
    finally:
        if workdir is None:
            shutil.rmtree(work, ignore_errors=True)

    total = len(checks)
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"check {name}: {'pass' if ok else 'FAIL'}")
    print(f"selftest {passed}/{total}")
    return 0 if passed == total else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision", default=BASE)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--selftest-work", default=None,
                    help="scratch dir for selftest fixtures (default: TMPDIR)")
    args = ap.parse_args()
    if args.selftest:
        return run_selftest(args.root, args.selftest_work)
    code, out = evaluate(args.root, args.revision)
    if out:
        print(out)
    return code


if __name__ == "__main__":
    sys.exit(main())
