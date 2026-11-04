#!/usr/bin/env python3
"""Round-86 counters — kake (frozen contract .ufo/waves/round-86/contract.md).

C1 (calibration): the four round-85 routed dispositions recorded over committed
bytes (R1 control ordering, R2 L0 routing, R3 counterexample preservation, R4
retained-open debt row).

C2 (freshness): fifteen frozen Cache-Control effective-freshness cases against
scripts/cache_control_effective.py exported from a pinned revision.

Exit 0 = met, 1 = not met, 64 = usage. Offline; honors TMPDIR/--work.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent  # .ufo/waves/round-86 -> repo
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

# --------------------------------------------------------------------------
# C1 — routed-disposition queue

C1_ROUND_DIR = ".ufo/waves/round-86"
C1_BASE_C1 = C1_ROUND_DIR + "/controls/base-c1.txt"
C1_BASE_C2 = C1_ROUND_DIR + "/controls/base-c2.txt"
C1_AFTER_C1 = C1_ROUND_DIR + "/controls/after-c1-carrier.txt"
C1_AFTER_C2 = C1_ROUND_DIR + "/controls/after-c2-carrier.txt"
C1_CRITIC = ".ufo/waves/round-85/w1/CriticClaims.md"
C1_LATE = ".ufo/waves/round-85/controls/late-shortcut-c1.txt"
C1_LESSON = "corpus/lessons/round-86.md"
C1_README = "corpus/README.md"
L0_LINE = re.compile(r"^kake \| round-86 \|", re.M)


class Tree:
    def __init__(self, root: Path):
        self.root = root

    def text(self, rel: str) -> str | None:
        p = self.root / rel
        if not p.is_file():
            return None
        return p.read_text(encoding="utf-8", errors="replace")


def export(root: Path, revision: str | None, work: Path) -> Path:
    if not revision:
        return root
    target = work / "export" / (revision[:12] or "worktree")
    target.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["git", "-C", str(root), "archive", revision], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False)
    if proc.returncode != 0:
        raise SystemExit(f"git archive {revision} failed: {proc.stderr.decode()[:400]}")
    tar = work / "export.tar"
    tar.write_bytes(proc.stdout)
    subprocess.run(["tar", "-xf", str(tar), "-C", str(target)], check=True)
    tar.unlink()
    return target


def c1_item_r1(freeze: Tree, carrier: Tree) -> tuple[bool, str]:
    base1 = freeze.text(C1_BASE_C1)
    base2 = freeze.text(C1_BASE_C2)
    ok_base = base1 is not None and "met=false" in base1 and base2 is not None and "met=false" in base2
    no_after = (freeze.root / C1_AFTER_C1).exists() is False and (freeze.root / C1_AFTER_C2).exists() is False
    after1 = carrier.text(C1_AFTER_C1)
    after2 = carrier.text(C1_AFTER_C2)
    ok_after = (after1 is not None and "met=true" in after1
                and after2 is not None and "met=true" in after2)
    ok = ok_base and no_after and ok_after
    return ok, (f"base_met_false={str(ok_base).lower()} "
                f"after_absent_at_freeze={str(no_after).lower()} "
                f"after_met_true={str(ok_after).lower()}")


def c1_item_r2(fleet: Path) -> tuple[bool, str]:
    p = fleet / ".ufo" / "l0-questions.md"
    if not p.is_file():
        return False, "l0_absent"
    return bool(L0_LINE.search(p.read_text(encoding="utf-8", errors="replace"))), "l0_line"


def c1_item_r3(carrier: Tree) -> tuple[bool, str]:
    critic = (carrier.root / C1_CRITIC).is_file()
    late = (carrier.root / C1_LATE).is_file()
    lesson = carrier.text(C1_LESSON) or ""
    ref = "round-85/w1/CriticClaims.md" in lesson
    ok = critic and late and ref
    return ok, (f"critic={'yes' if critic else 'no'} late={'yes' if late else 'no'} "
                f"lesson_ref={'yes' if ref else 'no'}")


def c1_item_r4(carrier: Tree) -> tuple[bool, str]:
    readme = carrier.text(C1_README)
    if readme is None:
        return False, "readme_absent"
    ok = all(t in readme for t in ("D84-2", "D84-3", "flip:", "corpus/lessons/round-85.md"))
    return ok, (f"d84_2={'yes' if 'D84-2' in readme else 'no'} "
                f"d84_3={'yes' if 'D84-3' in readme else 'no'} "
                f"flip={'yes' if 'flip:' in readme else 'no'} "
                f"lesson_cite={'yes' if 'corpus/lessons/round-85.md' in readme else 'no'}")


def run_c1(root: Path, freeze_rev: str | None, revision: str | None,
           fleet: Path, work: Path) -> int:
    freeze_tree = Tree(export(root, freeze_rev, work / "freeze"))
    carrier_tree = Tree(export(root, revision, work / "carrier"))
    r1ok, r1d = c1_item_r1(freeze_tree, carrier_tree)
    r2ok, r2d = c1_item_r2(fleet)
    r3ok, r3d = c1_item_r3(carrier_tree)
    r4ok, r4d = c1_item_r4(carrier_tree)
    rows = [("R1", r1ok, r1d), ("R2", r2ok, r2d), ("R3", r3ok, r3d), ("R4", r4ok, r4d)]
    closed = sum(1 for _, ok, _ in rows if ok)
    met = closed == len(rows)
    rev_label = revision or "worktree"
    print(f"C1v1 revision={rev_label} freeze={freeze_rev or rev_label} "
          f"items={len(rows)} closed={closed} open={len(rows) - closed} met={str(met).lower()}")
    for name, ok, detail in rows:
        print(f"  {name} ok={str(ok).lower()} {detail}")
    return 0 if met else 1


# --------------------------------------------------------------------------
# C2 — Cache-Control effective reader, frozen cases

TOOL_REL = "scripts/cache_control_effective.py"
K = ("storable", "freshness_lifetime_seconds", "basis", "no_cache",
     "no_cache_qualified", "must_revalidate", "must_understand",
     "duplicate_directives", "conflict", "invalid_directives")


def obj(storable=True, life=None, basis=None, no_cache=False, ncq=None,
        mrv=False, mu=False, dups=None, conflict=False, invalid=None):
    return {"storable": storable, "freshness_lifetime_seconds": life, "basis": basis,
            "no_cache": no_cache,
            "no_cache_qualified": [] if ncq is None else ncq,
            "must_revalidate": mrv, "must_understand": mu,
            "duplicate_directives": [] if dups is None else dups,
            "conflict": conflict,
            "invalid_directives": [] if invalid is None else invalid}


CASES: list[tuple[str, dict, dict]] = [
    ("basic-max-age",
     {"cache_control": ["max-age=3600"]},
     obj(life=3600, basis="max-age")),
    ("shared-s-maxage-overrides",
     {"cache_control": ["max-age=3600, s-maxage=60"], "shared": True},
     obj(life=60, basis="s-maxage")),
    ("private-ignores-s-maxage",
     {"cache_control": ["max-age=3600, s-maxage=60"], "shared": False},
     obj(life=3600, basis="max-age")),
    ("no-store-not-storable",
     {"cache_control": ["no-store"]},
     obj(storable=False, life=None, basis="no-store")),
    ("duplicate-first-occurrence",
     {"cache_control": ["max-age=100", "max-age=200"]},
     obj(life=100, basis="max-age", dups=["max-age"])),
    ("conflict-max-age-no-cache",
     {"cache_control": ["max-age=100, no-cache"]},
     obj(life=100, basis="max-age", no_cache=True, conflict=True)),
    ("directive-case-insensitive",
     {"cache_control": ["MAX-AGE=90"]},
     obj(life=90, basis="max-age")),
    ("unknown-directive-ignored",
     {"cache_control": ["teapot=1, max-age=60"]},
     obj(life=60, basis="max-age")),
    ("expires-minus-date",
     {"cache_control": [], "expires": "Wed, 21 Oct 2026 07:28:00 GMT",
      "date": "Wed, 21 Oct 2026 07:00:00 GMT"},
     obj(life=1680, basis="expires")),
    ("delta-seconds-cap",
     {"cache_control": ["max-age=99999999999999999999"]},
     obj(life=2147483648, basis="max-age")),
    ("must-revalidate-flag",
     {"cache_control": ["max-age=5, must-revalidate"]},
     obj(life=5, basis="max-age", mrv=True)),
    ("no-cache-qualified",
     {"cache_control": ['no-cache="Set-Cookie"', "max-age=300"]},
     obj(life=300, basis="max-age", ncq=["Set-Cookie"])),
    ("order-independent-a",
     {"cache_control": ["max-age=60, no-store"]},
     obj(storable=False, life=None, basis="no-store")),
    ("order-independent-b",
     {"cache_control": ["no-store, max-age=60"]},
     obj(storable=False, life=None, basis="no-store")),
    ("first-occurrence-not-minimum",
     {"cache_control": ["max-age=200", "max-age=100"]},
     obj(life=200, basis="max-age", dups=["max-age"])),
]

OFFLINE_RE = re.compile(r"^\s*(import|from)\s+(socket|urllib|http\.client|requests)", re.M)


def run_case(tool: Path, payload: dict, work: Path) -> tuple[int, str]:
    env = dict(os.environ)
    env["TMPDIR"] = str(work)
    (work / "in.json").write_text(json.dumps(payload), encoding="utf-8")
    with (work / "in.json").open("rb") as fin:
        proc = subprocess.run([sys.executable, "-B", str(tool)], stdin=fin,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=env, check=False, timeout=60)
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def c2_against(tool: Path, work: Path) -> tuple[int, int, int, int]:
    """returns (passed, total, selftest_ok, offline_ok)"""
    passed = 0
    for name, payload, expected in CASES:
        case_dir = work / f"case-{name}"
        case_dir.mkdir(parents=True, exist_ok=True)
        try:
            code, out = run_case(tool, payload, case_dir)
        except subprocess.TimeoutExpired:
            continue
        if code != 0:
            continue
        try:
            got = json.loads(out)
        except json.JSONDecodeError:
            continue
        if all(k in got for k in K) and all(got[k] == expected[k] for k in K):
            passed += 1
    env = dict(os.environ)
    env["TMPDIR"] = str(work / "selftest")
    (work / "selftest").mkdir(parents=True, exist_ok=True)
    st = subprocess.run([sys.executable, "-B", str(tool), "--selftest"],
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        env=env, check=False, timeout=120)
    selftest_ok = 1 if st.returncode == 0 else 0
    src = tool.read_text(encoding="utf-8", errors="replace") if tool.is_file() else ""
    offline_ok = 1 if not OFFLINE_RE.search(src) else 0
    return passed, len(CASES), selftest_ok, offline_ok


def run_c2(root: Path, revision: str | None, work: Path, tool_override: Path | None) -> int:
    if tool_override is not None:
        tool = tool_override
    else:
        tree = export(root, revision, work / "src")
        tool = tree / TOOL_REL
        if not tool.is_file():
            print(f"C2v1 revision={revision or 'worktree'} cases=0/{len(CASES)} "
                  f"selftest_ok=0 tool_offline=0 tool_absent=1 met=false")
            return 1
    passed, total, st_ok, off_ok = c2_against(tool, work)
    met = passed == total and st_ok == 1 and off_ok == 1
    print(f"C2v1 revision={revision or 'worktree'} cases={passed}/{total} "
          f"selftest_ok={st_ok} tool_offline={off_ok} tool_absent=0 met={str(met).lower()}")
    return 0 if met else 1


# --------------------------------------------------------------------------
# selftest

FIXTURE_C2_TOOL = r'''#!/usr/bin/env python3
import json, sys
if "--selftest" in sys.argv:
    print("selftest: 1/1 passed")
    sys.exit(0)
EXPECTED = json.loads(r"""__EXPECTED__""")
raw = sys.stdin.read()
for payload, expected in EXPECTED:
    if raw.strip() == json.dumps(payload):
        print(json.dumps(expected))
        sys.exit(0)
sys.exit(1)
'''


def _c1_fixture(lane: Path, fleet: Path, mutate: str | None) -> None:
    w = lane / ".ufo" / "waves" / "round-86" / "controls"
    w.mkdir(parents=True, exist_ok=True)
    (w / "base-c1.txt").write_text("C1v1 revision=x items=4 closed=0 open=4 met=false\n")
    (w / "base-c2.txt").write_text("C2v1 revision=x cases=0/15 met=false\n")
    (w / "after-c1-carrier.txt").write_text("C1v1 revision=y closed=4 open=0 met=true\n")
    (w / "after-c2-carrier.txt").write_text("C2v1 revision=y cases=15/15 met=true\n")
    critic = lane / ".ufo" / "waves" / "round-85" / "w1"
    critic.mkdir(parents=True, exist_ok=True)
    (critic / "CriticClaims.md").write_text("counter limits disclosed\n")
    late = lane / ".ufo" / "waves" / "round-85" / "controls"
    late.mkdir(parents=True, exist_ok=True)
    (late / "late-shortcut-c1.txt").write_text("late receipt\n")
    lesson = lane / "corpus" / "lessons"
    lesson.mkdir(parents=True, exist_ok=True)
    ref = "" if mutate == "r3" else "preserved: round-85/w1/CriticClaims.md\n"
    (lesson / "round-86.md").write_text("## Mistakes\n" + ref)
    readme = lane / "corpus" / "README.md"
    readme.parent.mkdir(parents=True, exist_ok=True)
    if mutate == "r4":
        readme.write_text("open debt D84-2\n")
    else:
        readme.write_text("## debt\nD84-2 and D84-3 stay open; flip: <cond>;"
                          " see corpus/lessons/round-85.md\n")
    l0 = fleet / ".ufo"
    l0.mkdir(parents=True, exist_ok=True)
    if mutate == "r2":
        (l0 / "l0-questions.md").write_text("other | line\n")
    else:
        (l0 / "l0-questions.md").write_text("kake | round-86 | question\n")


def _c2_fixture_tool(work: Path, mode: str) -> Path:
    if mode == "green":
        payload = json.dumps([[p, e] for _, p, e in CASES])
        src = FIXTURE_C2_TOOL.replace("__EXPECTED__", payload)
    elif mode == "constant":
        src = ("#!/usr/bin/env python3\nimport json,sys\n"
               "if '--selftest' in sys.argv:\n"
               "    print('selftest: 1/1 passed'); sys.exit(0)\n"
               "sys.stdin.read()\n"
               "print(json.dumps(" + json.dumps(CASES[0][2]) + "))\n")
    elif mode == "minmost":
        src = ("#!/usr/bin/env python3\nimport json,sys,re\n"
               "if '--selftest' in sys.argv:\n"
               "    print('selftest: 1/1 passed'); sys.exit(0)\n"
               "p=json.loads(sys.stdin.read())\n"
               "vals=[int(m.group(1)) for v in p['cache_control'] "
               "for m in [re.match(r'(?i)\\s*max-age=(\\d+)\\s*$', v)] if m]\n"
               "out=" + json.dumps(obj(life=1, basis='max-age')) + "\n"
               "out['freshness_lifetime_seconds']=min(vals) if vals else 0\n"
               "print(json.dumps(out))\n")
    else:
        raise SystemExit("mode")
    tool = work / f"tool-{mode}.py"
    tool.write_text(src, encoding="utf-8")
    return tool


def selftest() -> int:
    results: list[tuple[str, bool]] = []
    base = Path(tempfile.mkdtemp(prefix="c86-selftest-"))
    try:
        # --- C1 fixtures
        cases: list[tuple[str, Path, Path, bool]] = []
        for name, mutate, want in [("c1-green", None, True), ("c1-mut-r1", "r1", False),
                                   ("c1-mut-r2", "r2", False), ("c1-mut-r3", "r3", False),
                                   ("c1-mut-r4", "r4", False)]:
            lane = base / name / "lane"
            fleet = base / name / "fleet"
            lane.mkdir(parents=True)
            fleet.mkdir(parents=True)
            _c1_fixture(lane, fleet, mutate)
            if mutate == "r1":  # r1 mutant: the pre-dispatch control receipt is missing
                (lane / ".ufo/waves/round-86/controls/base-c1.txt").unlink()
            freeze_lane = base / name / "lane-freeze"
            shutil.copytree(lane, freeze_lane)
            for after in ("after-c1-carrier.txt", "after-c2-carrier.txt"):
                (freeze_lane / ".ufo/waves/round-86/controls" / after).unlink()
            # real fleet path irrelevant in fixtures: pass synthetic fleet
            cases.append((name, freeze_lane, lane, fleet, want))
        for name, freeze_lane, lane, fleet, want in cases:
            work = base / name / "work"
            work.mkdir(parents=True)
            # run items directly (no git in fixtures)
            freeze_tree = Tree(freeze_lane)
            carrier_tree = Tree(lane)
            ok1, _ = c1_item_r1(freeze_tree, carrier_tree)
            ok2, _ = c1_item_r2(fleet)
            ok3, _ = c1_item_r3(carrier_tree)
            ok4, _ = c1_item_r4(carrier_tree)
            closed = sum([ok1, ok2, ok3, ok4])
            met = closed == 4
            results.append((name, met == want))
        # junk fixture: readme names D84-2 but lacks the rest
        lane = base / "c1-junk" / "lane"
        fleet = base / "c1-junk" / "fleet"
        (lane / "corpus").mkdir(parents=True)
        (lane / "corpus" / "README.md").write_text("D84-2\n")
        (fleet / ".ufo").mkdir(parents=True)
        (fleet / ".ufo" / "l0-questions.md").write_text("x\n")
        ok2, _ = c1_item_r2(fleet)
        ok4, _ = c1_item_r4(Tree(lane))
        results.append(("c1-junk", (ok2 and ok4) is False))
        # missing-tree fixture
        ok4, _ = c1_item_r4(Tree(base / "nonexistent"))
        results.append(("c1-missing-tree", ok4 is False))

        # --- C2 fixtures
        for mode, want in [("green", True), ("constant", False), ("minmost", False)]:
            work = base / f"c2-{mode}"
            work.mkdir(parents=True)
            tool = _c2_fixture_tool(work, mode)
            passed, total, st_ok, _ = c2_against(tool, work)
            met = passed == total and st_ok == 1
            results.append((f"c2-{mode}", met == want))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    passed = sum(1 for _, ok in results if ok)
    print(f"selftest: {passed}/{len(results)} passed")
    for name, ok in results:
        if not ok:
            print(f"  FAIL {name}")
    return 0 if passed == len(results) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--claim", choices=("c1", "c2"), default=None)
    ap.add_argument("--root", type=Path, default=REPO)
    ap.add_argument("--revision", default=None)
    ap.add_argument("--freeze", default=None)
    ap.add_argument("--fleet", type=Path, default=None)
    ap.add_argument("--tool", type=Path, default=None)
    ap.add_argument("--work", type=Path, default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.claim is None:
        ap.error("--claim is required unless --selftest")
    work = args.work or Path(tempfile.mkdtemp(prefix="c86-count-"))
    work.mkdir(parents=True, exist_ok=True)
    fleet = args.fleet or args.root.parent
    try:
        if args.claim == "c1":
            return run_c1(args.root, args.freeze, args.revision, fleet, work)
        return run_c2(args.root, args.revision, work, args.tool)
    finally:
        if args.work is None:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
