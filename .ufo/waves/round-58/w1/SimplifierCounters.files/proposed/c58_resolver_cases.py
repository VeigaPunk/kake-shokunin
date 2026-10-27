#!/usr/bin/env python3
"""Round-58 C2 counter — operability: `scripts/id_resolver.py` closes its two disclosed false-green defects, nothing else moves.

Surface: the lane tool `scripts/id_resolver.py` (round-57 capability). Round 57 disclosed, after its freeze, two ways the tool
prints a green `dangling=0` / exit 0 over a lane whose markdown cites an id no registry row holds
(`.ufo/waves/round-57/w2/CriticResolverCheat.md` D1, `w2/ReviewerResolverCode.md` F1; round-57 report "Disclosed limits"):
  D1 fence-blind registry: a `| S### |` line inside a fenced code block (``` or ~~~) of `corpus/SOURCES.md` counts as a row,
     and a `## Registry` heading inside a fence opens the registry section;
  F1 quoted paths: with `--revision`, `git ls-tree` quotes non-ASCII / special-character paths (core.quotePath), the quoted
     name fails the `.md` filter and the file's citations are never read.

The counter copies the tool as committed at the revision (`git show <rev>:scripts/id_resolver.py`) into a scratch dir, builds
gate-owned fixture lanes there (a fixture fleet `<scratch>/fleet/kake-shokunin` plus siblings; every fixture repo is
`git init` in its own directory and verified by `rev-parse --show-toplevel`), runs the tool and compares exit code and
stdout with the expectation the gate states. Cases:

  K1 fenced `## Registry` + `| S950 |` row before the real `## Registry`; an entry cites S950      -> exit 1, DANGLING S950
  K2 ``` fence holding `| S951 |` inside the real Registry section; an entry cites S951             -> exit 1, DANGLING S951
  K3 ~~~ fence holding `| S952 |` inside the real Registry section; an entry cites S952             -> exit 1, DANGLING S952
  K4 `--revision`: `corpus/knowledge/中文.md` cites S900 (unregistered); ok.md cites S001          -> exit 1, DANGLING S900
  K5 `--revision`: `corpus/knowledge/a"b.md` (git-quoted name) cites S901 (unregistered)           -> exit 1, DANGLING S901
  P1 3-space-indented row S001 resolves; entry cites S001                                          -> exit 0, dangling=0
  P2 a row S002 after a closed fence inside the Registry section still resolves                      -> exit 0, dangling=0
  P3 a 4-space-indented `| S003 |` line is code, not a row                                         -> exit 1, DANGLING S003
  P4 a sibling whose committed registry holds S004 owns it                                         -> exit 1, owners=alpha-shokunin
  P5 `--fleet <absent path>`                                                                       -> exit 2
  P6 the tool's own selftest in a clean scratch copy prints `selftest: N/N` with N >= 49, exit 0
  P7 the real lane at the revision: `--revision <rev>` over the lane, exit 0, dangling=0, ids_cited >= 106

Predicate (frozen in `contract.json`):

    met: cases_passed == 12 of 12

Exit codes: 0 met, 1 not met, 2 unevaluable (revision unresolved, tool absent at the revision), 64 usage.
CLI: --root <lane> --revision <rev> [--work <scratch dir>] | --selftest
Not tested: sibling ownership beyond P4; performance; whether the census should also become fence-aware (it is not:
the census counts a fenced row, the tool after the fix does not; the divergence is the contract's stated choice).
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

PREDICATE = "met: cases_passed == 12 of 12"
TOOL = "scripts/id_resolver.py"
HDR = "| id | name | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"


def env() -> dict:
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    e.update({"LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"})
    return e


def run(argv: list[str], cwd: str | None = None, timeout: int = 300) -> tuple[int, str]:
    p = subprocess.run(argv, capture_output=True, cwd=cwd, env=env(), timeout=timeout)
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def row(sid: str, indent: str = "") -> str:
    return f"{indent}| {sid} | fixture — https://example.invalid/{sid} | docs | A | scope | anchor | teaches | mined | 2026-10-26 | 90d | corpus/knowledge/ok.md |\n"


def write(base: str, files: dict[str, str]) -> None:
    for rel, text in files.items():
        p = os.path.join(base, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)


def repo(path: str, files: dict[str, str]) -> str:
    os.makedirs(path, exist_ok=True)
    write(path, files)
    run(["git", "-C", path, "init", "-q"])
    rc, top = run(["git", "-C", path, "rev-parse", "--show-toplevel"])
    if rc != 0 or os.path.realpath(top.strip()) != os.path.realpath(path):
        raise RuntimeError(f"fixture repo toplevel mismatch at {path}")
    run(["git", "-C", path, "add", "-A"])
    run(["git", "-C", path, "-c", "user.name=gate", "-c", "user.email=gate@local", "-c", "commit.gpgsign=false",
         "commit", "-q", "-m", "fixture"])
    rc, head = run(["git", "-C", path, "rev-parse", "HEAD"])
    return head.strip()


def registry(body: str) -> str:
    return "# Sources\n\n" + body


def lane(work: str, name: str, reg: str, knowledge: dict[str, str], siblings: dict[str, str | None] | None = None,
         git_lane: bool = False) -> tuple[str, str, str | None]:
    fleet = os.path.join(work, name, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    files = {"corpus/SOURCES.md": reg, **{f"corpus/knowledge/{k}": v for k, v in knowledge.items()}}
    head = None
    if git_lane:
        head = repo(lp, files)
    else:
        write(lp, files)
    for sib, sreg in (siblings or {}).items():
        sp = os.path.join(fleet, sib)
        if sreg is None:
            os.makedirs(sp, exist_ok=True)
        else:
            repo(sp, {"corpus/SOURCES.md": sreg})
    return fleet, lp, head


def case_results(tool: str, root: str, rev: str, work: str) -> list[tuple[str, bool, str]]:
    py = [sys.executable, "-B", tool]
    out: list[tuple[str, bool, str]] = []

    def check(name: str, argv: list[str], want_rc: int, want_re: list[str], forbid_re: list[str] = ()):
        rc, text = run(py + argv)
        ok = rc == want_rc and all(re.search(p, text, re.M) for p in want_re) and not any(re.search(p, text, re.M) for p in forbid_re)
        out.append((name, ok, f"exit={rc} " + " | ".join(text.strip().splitlines()[-3:])[:300]))

    reg_ok = "## Registry\n\n" + HDR + row("S001")
    # K1
    fl, lp, _ = lane(work, "k1", registry("```\n## Registry\n\n" + HDR + row("S950") + "```\n\n" + reg_ok),
                     {"ok.md": "Cites S001 and S950.\n"})
    check("K1_fenced_heading_before_registry", ["--root", lp, "--fleet", fl], 1, [r"^DANGLING S950 "], [r"^DANGLING S001 "])
    # K2
    fl, lp, _ = lane(work, "k2", registry(reg_ok + "```\n" + row("S951") + "```\n"), {"ok.md": "Cites S001 and S951.\n"})
    check("K2_backtick_fence_inside_registry", ["--root", lp, "--fleet", fl], 1, [r"^DANGLING S951 "], [r"^DANGLING S001 "])
    # K3
    fl, lp, _ = lane(work, "k3", registry(reg_ok + "~~~\n" + row("S952") + "~~~\n"), {"ok.md": "Cites S001 and S952.\n"})
    check("K3_tilde_fence_inside_registry", ["--root", lp, "--fleet", fl], 1, [r"^DANGLING S952 "], [r"^DANGLING S001 "])
    # K4
    fl, lp, head = lane(work, "k4", registry(reg_ok), {"ok.md": "Cites S001.\n", "中文.md": "Cites S900.\n"}, git_lane=True)
    check("K4_non_ascii_path_at_revision", ["--root", lp, "--fleet", fl, "--revision", head], 1,
          [r"^DANGLING S900 cited-by=corpus/knowledge/中文\.md "])
    # K5
    fl, lp, head = lane(work, "k5", registry(reg_ok), {"ok.md": "Cites S001.\n", 'a"b.md': "Cites S901.\n"}, git_lane=True)
    check("K5_git_quoted_path_at_revision", ["--root", lp, "--fleet", fl, "--revision", head], 1,
          [r'^DANGLING S901 cited-by=corpus/knowledge/a"b\.md '])
    # P1
    fl, lp, _ = lane(work, "p1", registry("## Registry\n\n" + HDR + row("S001", "   ")), {"ok.md": "Cites S001.\n"})
    check("P1_three_space_row_resolves", ["--root", lp, "--fleet", fl], 0, [r"^ids_cited=1 ids_resolved=1 dangling=0 "])
    # P2
    fl, lp, _ = lane(work, "p2", registry(reg_ok + "```\nsample text\n```\n" + row("S002")), {"ok.md": "Cites S001 and S002.\n"})
    check("P2_row_after_closed_fence_resolves", ["--root", lp, "--fleet", fl], 0, [r"^ids_cited=2 ids_resolved=2 dangling=0 "])
    # P3
    fl, lp, _ = lane(work, "p3", registry(reg_ok + row("S003", "    ")), {"ok.md": "Cites S001 and S003.\n"})
    check("P3_four_space_line_is_code", ["--root", lp, "--fleet", fl], 1, [r"^DANGLING S003 "])
    # P4
    fl, lp, _ = lane(work, "p4", registry(reg_ok), {"ok.md": "Cites S001 and S004.\n"},
                     siblings={"alpha-shokunin": registry("## Registry\n\n" + HDR + row("S004")), "beta-shokunin": None})
    check("P4_committed_sibling_owns", ["--root", lp, "--fleet", fl], 1, [r"^DANGLING S004 .*owners=alpha-shokunin "])
    # P5
    fl, lp, _ = lane(work, "p5", registry(reg_ok), {"ok.md": "Cites S001.\n"})
    check("P5_absent_fleet_is_unevaluable", ["--root", lp, "--fleet", os.path.join(work, "p5", "no-such-fleet")], 2, [])
    # P6
    st = os.path.join(work, "p6")
    os.makedirs(st, exist_ok=True)
    rc, text = run([sys.executable, "-B", tool, "--selftest"], cwd=st)
    m = re.findall(r"(?m)^selftest: (\d+)/(\d+)\s*$", text)
    ok = rc == 0 and bool(m) and m[-1][0] == m[-1][1] and int(m[-1][1]) >= 49
    out.append(("P6_tool_selftest", ok, f"exit={rc} {m[-1] if m else 'no tally'}"))
    # P7
    os.makedirs(os.path.join(work, "p7-empty-fleet"), exist_ok=True)
    rc, text = run(py + ["--root", root, "--revision", rev, "--fleet", os.path.join(work, "p7-empty-fleet")])
    m = re.search(r"(?m)^ids_cited=(\d+) ids_resolved=(\d+) dangling=(\d+) ", text)
    ok = rc == 0 and bool(m) and int(m.group(1)) >= 106 and m.group(3) == "0"
    out.append(("P7_real_lane_green", ok, f"exit={rc} {m.group(0) if m else text.strip()[-200:]}"))
    return out


def measure(root: str, rev: str, work: str) -> tuple[int, list[tuple[str, bool, str]]]:
    rc, src = run(["git", "-C", root, "show", f"{rev}:{TOOL}"])
    if rc != 0:
        return 2, [("tool_present", False, f"{TOOL} absent at {rev[:12]}")]
    tool = os.path.join(work, "id_resolver.py")
    with open(tool, "w", encoding="utf-8") as fh:
        fh.write(src)
    res = case_results(tool, root, rev, work)
    return (0 if all(ok for _, ok, _ in res) and len(res) == 12 else 1), res


def selftest() -> int:
    print("c58 resolver-cases selftest: version 1 has none (wave 1 attacks the cases; the base run is the red control)", file=sys.stderr)
    return 2


def main() -> int:
    class _P(argparse.ArgumentParser):
        def error(self, message):
            print(f"usage error: {message}", file=sys.stderr)
            raise SystemExit(64)

    ap = _P(description="Round-58 C2 counter (id_resolver false-green cases)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--work", help="scratch dir (default: a new dir under $TMPDIR); removed on exit")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.revision:
        print("usage: --revision is required unless --selftest is used", file=sys.stderr)
        return 64
    rc, rev = run(["git", "-C", a.root, "rev-parse", "--verify", "-q", f"{a.revision}^{{commit}}"])
    if rc != 0:
        print(f"unevaluable: revision {a.revision!r} does not resolve\nEXIT=2")
        return 2
    rev = rev.strip()
    parent = a.work or os.environ.get("TMPDIR") or tempfile.gettempdir()
    os.makedirs(parent, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c58-rc-", dir=parent)
    try:
        code, res = measure(os.path.abspath(a.root), rev, work)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    passed = sum(ok for _, ok, _ in res)
    print(f"C2 resolver-cases {passed}/12 met={code == 0}  ({PREDICATE})")
    for name, ok, note in res:
        print(f"  {name} {'PASS' if ok else 'FAIL'}  {note}")
    print(f"  revision: {rev}")
    print(f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
