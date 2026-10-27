#!/usr/bin/env python3
"""Round-58 C2 counter — operability: `scripts/id_resolver.py` closes its two disclosed false-green defects, nothing else moves.

Surface: the lane tool `scripts/id_resolver.py` (round-57 capability). Round 57 disclosed, after its freeze, two ways the tool
prints a green `dangling=0` / exit 0 over a lane whose markdown cites an id no registry row holds
(`.ufo/waves/round-57/w2/CriticResolverCheat.md` D1, `w2/ReviewerResolverCode.md` F1; round-57 report "Disclosed limits"):
  D1 fence-blind registry: a `| S### |` line inside a fenced code block (``` or ~~~) of `corpus/SOURCES.md` counts as a row,
     and a `## Registry` heading inside a fence opens the registry section;
  F1 quoted paths: with `--revision`, `git ls-tree` quotes non-ASCII / special-character paths (core.quotePath), the quoted
     name fails the `.md` filter and the file's citations are never read.

Version 2 (after wave 1, before any claim was measured). Version 1 (12 cases, frozen at fff3eea6) was met by wrong tools
(w1/CriticC2Cheat: id-magnitude and id-literal masks, canned output keyed on fixture dir names, a newline-name split;
w1/ExecC2GateSelftest: K4/K5 forbade nothing about the registered id, url-match never asserted). Version 2 draws every fixture id
per run from S100..S9999 (`--seed`, printed), names case dirs at random, adds K6 and K7, forbids the registered id dangling in
every K case, asserts url-match in P4, raises the P6 floor to 55 and carries a selftest of 7 scored control tools.

The counter copies the tool as committed at the revision (`git show <rev>:scripts/id_resolver.py`) into a scratch dir, builds
gate-owned fixture lanes there (a fixture fleet `<scratch>/<random>/fleet/kake-shokunin` plus siblings; every fixture repo is
`git init` in its own directory and verified by `rev-parse --show-toplevel`), runs the tool and compares exit code and
stdout with the expectation the gate states. Ids below are placeholders for the per-run draws (R = a registered id):

  K1 fenced `## Registry` + `| D1 |` row before the real `## Registry`; an entry cites R and D1   -> exit 1, DANGLING D1, not R
  K2 ``` fence holding `| D2 |` inside the real Registry section                                  -> exit 1, DANGLING D2, not R
  K3 ~~~ fence holding `| D3 |` inside the real Registry section                                  -> exit 1, DANGLING D3, not R
  K4 `--revision`: `corpus/knowledge/中文.md` cites D4 (unregistered); ok.md cites R             -> exit 1, DANGLING D4, 2 cited 1 resolved
  K5 `--revision`: `corpus/knowledge/a"b.md` (git-quoted name) cites D5                           -> exit 1, DANGLING D5, 2 cited 1 resolved
  K6 a fenced LOW id dangles while a registered HIGH id resolves                                  -> exit 1, DANGLING low only
  K7 `--revision`: a knowledge file whose name holds a newline cites D7                           -> exit 1, DANGLING D7, 2 cited 1 resolved
  P1 3-space-indented row R resolves                                                              -> exit 0, dangling=0
  P2 a row after a closed fence inside the Registry section still resolves                         -> exit 0, dangling=0
  P3 a 4-space-indented `| P3 |` line is code, not a row                                          -> exit 1, DANGLING P3, not R
  P4 a sibling whose committed registry holds P4 owns it; the entry carries the sibling's URL      -> exit 1, owners=alpha-shokunin url-match=alpha-shokunin
  P5 `--fleet <absent path>`                                                                       -> exit 2
  P6 the tool's own selftest in a clean scratch copy prints `selftest: N/N` with N >= 55, exit 0
  P7 the real lane at the revision: `--revision <rev>` over the lane, exit 0, dangling=0, ids_cited >= 106

Predicate (frozen in `contract.json`):

    met: cases_passed == 14 of 14

Exit codes: 0 met, 1 not met, 2 unevaluable (revision unresolved, tool absent at the revision), 64 usage.
CLI: --root <lane> --revision <rev> [--work <scratch dir>] [--seed N] | --selftest
Not tested: sibling ownership beyond P4; performance; that the tool's printed selftest tally reflects cases that ran (P6);
HTML-comment rows, setext headings and symlinked knowledge dirs (w1/ReviewerResolverOther: reported limits); whether the census should also become fence-aware (it is not:
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

PREDICATE = "met: cases_passed == 14 of 14"
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
    # version 2: the case directory name is random (w1/CriticC2Cheat H4: a tool keyed on `/k1/` fragments of --root)
    del name
    fleet = os.path.join(tempfile.mkdtemp(dir=work), "fleet")
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


SEED: int | None = None  # version 2: fixture ids are drawn per run from S100..S9999 (w1/CriticC2Cheat H1/H2); the seed is printed


def fixture_ids(n: int) -> list[str]:
    import random
    return [f"S{i}" for i in random.Random(SEED).sample(range(100, 10000), n)]


def case_results(tool: str, root: str, rev: str, work: str) -> list[tuple[str, bool, str]]:
    py = [sys.executable, "-B", tool]
    out: list[tuple[str, bool, str]] = []

    def check(name: str, argv: list[str], want_rc: int, want_re: list[str], forbid_re: list[str] = ()):
        rc, text = run(py + argv)
        ok = rc == want_rc and all(re.search(p, text, re.M) for p in want_re) and not any(re.search(p, text, re.M) for p in forbid_re)
        out.append((name, ok, f"exit={rc} " + " | ".join(text.strip().splitlines()[-3:])[:300]))

    ok_id, d1, d2, d3, d4, d5, lo, hi, d7, p2, p3, p4 = fixture_ids(12)
    lo, hi = (lo, hi) if int(lo[1:]) < int(hi[1:]) else (hi, lo)
    reg_ok = "## Registry\n\n" + HDR + row(ok_id)
    no_ok = [rf"^DANGLING {ok_id} "]
    # K1
    fl, lp, _ = lane(work, "k1", registry("```\n## Registry\n\n" + HDR + row(d1) + "```\n\n" + reg_ok),
                     {"ok.md": f"Cites {ok_id} and {d1}.\n"})
    check("K1_fenced_heading_before_registry", ["--root", lp, "--fleet", fl], 1, [rf"^DANGLING {d1} "], no_ok)
    # K2
    fl, lp, _ = lane(work, "k2", registry(reg_ok + "```\n" + row(d2) + "```\n"), {"ok.md": f"Cites {ok_id} and {d2}.\n"})
    check("K2_backtick_fence_inside_registry", ["--root", lp, "--fleet", fl], 1, [rf"^DANGLING {d2} "], no_ok)
    # K3
    fl, lp, _ = lane(work, "k3", registry(reg_ok + "~~~\n" + row(d3) + "~~~\n"), {"ok.md": f"Cites {ok_id} and {d3}.\n"})
    check("K3_tilde_fence_inside_registry", ["--root", lp, "--fleet", fl], 1, [rf"^DANGLING {d3} "], no_ok)
    # K4 (version 2: the registered id must still resolve in the same run — w1/ExecC2GateSelftest defect 1)
    fl, lp, head = lane(work, "k4", registry(reg_ok), {"ok.md": f"Cites {ok_id}.\n", "中文.md": f"Cites {d4}.\n"}, git_lane=True)
    check("K4_non_ascii_path_at_revision", ["--root", lp, "--fleet", fl, "--revision", head], 1,
          [rf"^DANGLING {d4} cited-by=corpus/knowledge/中文\.md ", r"^ids_cited=2 ids_resolved=1 dangling=1 "], no_ok)
    # K5
    fl, lp, head = lane(work, "k5", registry(reg_ok), {"ok.md": f"Cites {ok_id}.\n", 'a"b.md': f"Cites {d5}.\n"}, git_lane=True)
    check("K5_git_quoted_path_at_revision", ["--root", lp, "--fleet", fl, "--revision", head], 1,
          [rf'^DANGLING {d5} cited-by=corpus/knowledge/a"b\.md ', r"^ids_cited=2 ids_resolved=1 dangling=1 "], no_ok)
    # K6 (version 2): a fenced LOW id is dangling while a registered HIGH id resolves (kills id-magnitude masks)
    fl, lp, _ = lane(work, "k6", registry("## Registry\n\n" + HDR + row(hi) + "```\n" + row(lo) + "```\n"),
                     {"ok.md": f"Cites {hi} and {lo}.\n"})
    check("K6_fenced_low_id_dangles_registered_high_id_resolves", ["--root", lp, "--fleet", fl], 1,
          [rf"^DANGLING {lo} ", r"^ids_cited=2 ids_resolved=1 dangling=1 "], [rf"^DANGLING {hi} "])
    # K7 (version 2): a knowledge file whose name holds a newline, read at a revision (w1/CriticC2Cheat H3)
    fl, lp, head = lane(work, "k7", registry(reg_ok), {"ok.md": f"Cites {ok_id}.\n", "line\nbreak.md": f"Cites {d7}.\n"}, git_lane=True)
    check("K7_newline_path_at_revision", ["--root", lp, "--fleet", fl, "--revision", head], 1,
          [rf"^DANGLING {d7} ", r"^ids_cited=2 ids_resolved=1 dangling=1 "], no_ok)
    # P1
    fl, lp, _ = lane(work, "p1", registry("## Registry\n\n" + HDR + row(ok_id, "   ")), {"ok.md": f"Cites {ok_id}.\n"})
    check("P1_three_space_row_resolves", ["--root", lp, "--fleet", fl], 0, [r"^ids_cited=1 ids_resolved=1 dangling=0 "])
    # P2
    fl, lp, _ = lane(work, "p2", registry(reg_ok + "```\nsample text\n```\n" + row(p2)), {"ok.md": f"Cites {ok_id} and {p2}.\n"})
    check("P2_row_after_closed_fence_resolves", ["--root", lp, "--fleet", fl], 0, [r"^ids_cited=2 ids_resolved=2 dangling=0 "])
    # P3
    fl, lp, _ = lane(work, "p3", registry(reg_ok + row(p3, "    ")), {"ok.md": f"Cites {ok_id} and {p3}.\n"})
    check("P3_four_space_line_is_code", ["--root", lp, "--fleet", fl], 1, [rf"^DANGLING {p3} "], no_ok)
    # P4 (version 2: url-match asserted — w1/ExecC2GateSelftest defect 2)
    fl, lp, _ = lane(work, "p4", registry(reg_ok), {"ok.md": f"Cites {ok_id} and {p4} (https://example.invalid/{p4}).\n"},
                     siblings={"alpha-shokunin": registry("## Registry\n\n" + HDR + row(p4)), "beta-shokunin": None})
    check("P4_committed_sibling_owns", ["--root", lp, "--fleet", fl], 1,
          [rf"^DANGLING {p4} .*owners=alpha-shokunin url-match=alpha-shokunin$"], no_ok)
    # P5
    fl, lp, _ = lane(work, "p5", registry(reg_ok), {"ok.md": f"Cites {ok_id}.\n"})
    check("P5_absent_fleet_is_unevaluable", ["--root", lp, "--fleet", os.path.join(work, "no-such-fleet")], 2, [])
    # P6 (version 2: floor 55 — the fix adds its own cases; a printed tally is still not proof the cases ran)
    st = tempfile.mkdtemp(dir=work)
    shutil.copy(tool, os.path.join(st, "id_resolver.py"))
    rc, text = run([sys.executable, "-B", os.path.join(st, "id_resolver.py"), "--selftest"], cwd=st)
    m = re.findall(r"(?m)^selftest: (\d+)/(\d+)\s*$", text)
    ok = rc == 0 and bool(m) and m[-1][0] == m[-1][1] and int(m[-1][1]) >= P6_FLOOR
    out.append(("P6_tool_selftest", ok, f"exit={rc} {m[-1] if m else 'no tally'}"))
    # P7
    os.makedirs(os.path.join(work, "p7-empty-fleet"), exist_ok=True)
    rc, text = run(py + ["--root", root, "--revision", rev, "--fleet", os.path.join(work, "p7-empty-fleet")])
    m = re.search(r"(?m)^ids_cited=(\d+) ids_resolved=(\d+) dangling=(\d+) ", text)
    ok = rc == 0 and bool(m) and int(m.group(1)) >= 106 and m.group(3) == "0"
    out.append(("P7_real_lane_green", ok, f"exit={rc} {m.group(0) if m else text.strip()[-200:]}"))
    return out


P6_FLOOR = 55
NCASES = 14


def measure(root: str, rev: str, work: str) -> tuple[int, list[tuple[str, bool, str]]]:
    rc, src = run(["git", "-C", root, "show", f"{rev}:{TOOL}"])
    if rc != 0:
        return 2, [("tool_present", False, f"{TOOL} absent at {rev[:12]}")]
    tool = os.path.join(work, "id_resolver.py")
    with open(tool, "w", encoding="utf-8") as fh:
        fh.write(src)
    res = case_results(tool, root, rev, work)
    return (0 if all(ok for _, ok, _ in res) and len(res) == NCASES else 1), res


# --------------------------------------------------------------------------- selftest (wave-1 hardening)
# Version 1 returned 2 (stub). This selftest scores the gate itself: every control below is a tool whose
# behaviour is known, and it must come out at the score the control states. A case that can no longer fail,
# or that fails for the wrong reason, shows up as a wrong score. `measure()` and `case_results()` are not
# modified: each control is scored by the same measure() the gate uses. P7 never reads the lane's own
# revision here — each control is committed as `scripts/id_resolver.py` of a gate-built fixture lane whose
# registry holds 106 rows and whose one knowledge file cites all 106 ids, so P7's floor (ids_cited >= 106)
# is satisfiable in a fixture. The only lane read is `git show <BASE>:scripts/id_resolver.py` for the
# do-nothing control (d), which by definition is the base tool.

BASE_REV = "044048597d62f3199494b63b36e90dd57825e350"

CONST_STUB = '''#!/usr/bin/env python3
"""C2 gate-selftest control: a constant green line, exit 0, whatever the input."""
import sys

print("ids_cited=1 ids_resolved=1 dangling=0 owned_elsewhere=0 unowned=0")
sys.exit(0)
'''

MINI_STUB = r'''#!/usr/bin/env python3
"""C2 gate-selftest control stub (never a lane tool). Variant flags are injected by c58_resolver_cases.py --selftest."""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

ID_RE = re.compile(r"(?<![A-Za-z0-9_])S\d{3,}(?![A-Za-z0-9_])")
ROW_RE = re.compile(r"^ {0,3}\|\s*([^|]*?)\s*(?:\|(.*))?$")
ID_CELL_RE = re.compile(r"^S\d{3,}$")
URL_RE = re.compile(r"https?://[^\s|<>\"'`]+")
HEAD_RE = re.compile(r"^##\s+Registry\s*$")
END_RE = re.compile(r"^#{1,2}\s")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
REG = "corpus/SOURCES.md"
KREL = "corpus/knowledge"
FENCE_DROP = __FENCE_DROP__
ALWAYS_EXIT_ONE = __ALWAYS_EXIT_ONE__
BLANKET_DANGLING = __BLANKET_DANGLING__
TALLY = __TALLY__


def _git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    proc = subprocess.run(["git", "-C", root, *args], capture_output=True, env=env)
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def parse_registry(text):
    rows, inside, fence = {}, False, None
    for raw in text.splitlines():
        line = raw.rstrip("\r")
        m = FENCE_RE.match(line)
        if fence is not None:
            if m and m.group(1)[0] == fence:
                fence = None
            continue
        if m:
            if FENCE_DROP:
                return rows
            fence = m.group(1)[0]
            continue
        if HEAD_RE.match(line):
            inside = True
            continue
        if not inside:
            continue
        if END_RE.match(line):
            inside = False
            continue
        m = ROW_RE.match(line)
        if not m:
            continue
        sid = m.group(1).strip()
        if not ID_CELL_RE.match(sid):
            continue
        cell = (m.group(2) or "").split("|", 1)[0]
        bucket = rows.setdefault(sid, [])
        for url in URL_RE.findall(cell):
            url = url.rstrip(".,;:")
            if url not in bucket:
                bucket.append(url)
    return rows


def knowledge(root, rev):
    if rev:
        rc, out = _git(root, "ls-tree", "-z", "-r", "--name-only", rev)
        if rc != 0:
            return None
        bodies = {}
        for rel in out.split("\0"):
            if not (rel.startswith(KREL + "/") and rel.endswith(".md")):
                continue
            rc, body = _git(root, "show", rev + ":" + rel)
            if rc != 0:
                return None
            bodies[rel] = body
        return bodies or None
    base = os.path.join(root, KREL)
    bodies = {}
    for dirpath, _dirs, names in os.walk(base):
        for name in sorted(names):
            if not name.endswith(".md"):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            with open(full, "rb") as fh:
                bodies[rel] = fh.read().decode("utf-8", "replace")
    return bodies or None


def sibling_rows(fleet, lane):
    out = {}
    if not os.path.isdir(fleet):
        return out
    lane_real = os.path.realpath(lane)
    for name in sorted(os.listdir(fleet)):
        if not name.endswith("-shokunin"):
            continue
        path = os.path.join(fleet, name)
        if not os.path.isdir(path) or os.path.realpath(path) == lane_real:
            continue
        if os.path.exists(os.path.join(path, ".git")):
            rc, text = _git(path, "show", "HEAD:" + REG)
            if rc == 0:
                out[name] = parse_registry(text)
        elif os.path.isfile(os.path.join(path, REG)):
            with open(os.path.join(path, REG), "rb") as fh:
                out[name] = parse_registry(fh.read().decode("utf-8", "replace"))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(prog="id_resolver.py")
    ap.add_argument("--root")
    ap.add_argument("--revision")
    ap.add_argument("--fleet")
    ap.add_argument("--selftest", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    if a.selftest:
        if TALLY:
            print("selftest: " + TALLY)
            return 0
        print("selftest: none", file=sys.stderr)
        return 2
    if not a.root or not os.path.isdir(a.root):
        print("id_resolver: unevaluable: bad root", file=sys.stderr)
        return 2
    rev = None
    if a.revision:
        rc, out = _git(a.root, "rev-parse", "--verify", a.revision + "^{commit}")
        if rc != 0:
            return 2
        rev = out.strip()
        rc, text = _git(a.root, "show", rev + ":" + REG)
        if rc != 0:
            return 2
    else:
        path = os.path.join(a.root, REG)
        if not os.path.isfile(path):
            return 2
        with open(path, "rb") as fh:
            text = fh.read().decode("utf-8", "replace")
    bodies = knowledge(a.root, rev)
    if bodies is None:
        return 2
    cited = {}
    for path, body in bodies.items():
        for sid in ID_RE.findall(body):
            cited.setdefault(sid, set()).add(path)
    cited = {sid: sorted(paths) for sid, paths in cited.items()}
    if BLANKET_DANGLING:
        for sid in sorted(cited):
            print("DANGLING " + sid + " cited-by=" + ",".join(cited[sid]) + " owners=- url-match=-")
        print("ids_cited=%d ids_resolved=0 dangling=%d owned_elsewhere=0 unowned=%d"
              % (len(cited), len(cited), len(cited)))
        return 1
    fleet = os.path.abspath(a.fleet) if a.fleet else os.path.dirname(os.path.abspath(a.root))
    if not os.path.isdir(fleet):
        print("id_resolver: unevaluable: fleet root " + fleet + " is not a directory", file=sys.stderr)
        return 2
    registry_rows = parse_registry(text)
    dangling = sorted(set(cited) - set(registry_rows))
    sibs = sibling_rows(fleet, os.path.abspath(a.root)) if dangling else {}
    owned = 0
    for sid in dangling:
        paths = cited[sid]
        owners = sorted(name for name, reg in sibs.items() if sid in reg)
        matched = [name for name in owners
                   if any(url in bodies[p] for p in paths for url in sibs[name].get(sid, ()))]
        if owners:
            owned += 1
        print("DANGLING " + sid + " cited-by=" + ",".join(paths)
              + " owners=" + (",".join(owners) or "-") + " url-match=" + (",".join(matched) or "-"))
    print("ids_cited=%d ids_resolved=%d dangling=%d owned_elsewhere=%d unowned=%d"
          % (len(cited), len(cited) - len(dangling), len(dangling), owned, len(dangling) - owned))
    if ALWAYS_EXIT_ONE:
        return 1
    return 1 if dangling else 0


if __name__ == "__main__":
    sys.exit(main())
'''


def _stub(fence_drop: bool = False, always_exit_one: bool = False, blanket_dangling: bool = False,
          tally: str | None = None) -> str:
    return (MINI_STUB
            .replace("__FENCE_DROP__", repr(bool(fence_drop)))
            .replace("__ALWAYS_EXIT_ONE__", repr(bool(always_exit_one)))
            .replace("__BLANKET_DANGLING__", repr(bool(blanket_dangling)))
            .replace("__TALLY__", repr(tally)))


def _lane_root() -> str | None:
    here = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        if os.path.isdir(os.path.join(here, ".git")) and os.path.isfile(os.path.join(here, "corpus", "SOURCES.md")):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    return os.environ.get("C58_LANE_ROOT")


def _base_tool() -> tuple[str | None, str]:
    lane = _lane_root()
    if not lane:
        return None, "lane root not found above the counter path (no .git + corpus/SOURCES.md ancestor)"
    rc, src = run(["git", "-C", lane, "show", f"{BASE_REV}:{TOOL}"])
    if rc != 0:
        return None, f"git show {BASE_REV[:12]}:{TOOL} failed in {lane}"
    return src, ""


def _fixture_lane(base: str, tool_src: str, rows: int = 106) -> tuple[str, str]:
    """A committed fixture lane holding the tool under test plus a registry of `rows` ids, all cited."""
    ids = [f"S{100 + i}" for i in range(rows)]
    path = os.path.join(base, "lane")
    files = {
        "scripts/id_resolver.py": tool_src,
        "corpus/SOURCES.md": registry("## Registry\n\n" + HDR + "".join(row(sid) for sid in ids)),
        "corpus/knowledge/ok.md": "Cites " + " ".join(ids) + ".\n",
    }
    return path, repo(path, files)


def _control(name: str, base: str, src: str, expect: int, must_pass: list[str], must_fail: list[str]) -> tuple[bool, str]:
    root, head = _fixture_lane(os.path.join(base, name), src)
    work = os.path.join(base, name, "work")
    os.makedirs(work, exist_ok=True)
    code, res = measure(root, head, work)
    marks = {n: ok for n, ok, _ in res}
    passed = sum(1 for _, ok, _ in res if ok)
    wrong = [n for n in must_pass if not marks.get(n)]
    wrong += [n for n in must_fail if marks.get(n, True)]
    problems = []
    if len(res) != NCASES:
        problems.append(f"cases={len(res)}")
    if passed != expect:
        problems.append(f"score={passed}/{NCASES} expected={expect}/{NCASES}")
    if code != (0 if passed == NCASES else 1):
        problems.append(f"exit={code}")
    if wrong:
        problems.append("wrong-case " + ",".join(wrong))
    failing = ",".join(n for n, ok, _ in res if not ok) or "-"
    return (not problems, f"{name}: score={passed}/{NCASES} exit={code} failing=[{failing}]"
            + ("; " + "; ".join(problems) if problems else ""))


def selftest() -> int:
    global SEED
    SEED = 58  # fixed fixture ids so the selftest is repeatable
    base_tool, why = _base_tool()
    parent = os.environ.get("TMPDIR") or tempfile.gettempdir()
    base = tempfile.mkdtemp(prefix="c58-rc-selftest-", dir=parent)
    ok = True
    try:
        ALL = ['K1_fenced_heading_before_registry', 'K2_backtick_fence_inside_registry', 'K3_tilde_fence_inside_registry', 'K4_non_ascii_path_at_revision', 'K5_git_quoted_path_at_revision', 'K6_fenced_low_id_dangles_registered_high_id_resolves', 'K7_newline_path_at_revision', 'P1_three_space_row_resolves', 'P2_row_after_closed_fence_resolves', 'P3_four_space_line_is_code', 'P4_committed_sibling_owns', 'P5_absent_fleet_is_unevaluable', 'P6_tool_selftest', 'P7_real_lane_green']
        pick = lambda *pre: [n for n in ALL if n.split("_")[0] in pre]
        rest = lambda fails: [n for n in ALL if n not in fails]
        spec = [
            # version 2 expectations (14 cases; fixture ids fixed by SEED in the selftest)
            ("const_green", CONST_STUB, pick("K1", "K2", "K3", "K4", "K5", "K6", "K7", "P2", "P3", "P4", "P5", "P6", "P7")),
            ("blanket_dangling", _stub(blanket_dangling=True), ALL),
            ("fence_drop", _stub(fence_drop=True), pick("K1", "P2", "P6")),
            ("always_exit_one", _stub(always_exit_one=True), pick("P1", "P2", "P6", "P7")),
            ("near_miss_p6", _stub(tally="54/54"), pick("P6")),
            ("full_green", _stub(tally="59/59"), []),
        ]
        controls = [(name, src, len(ALL) - len(fails), rest(fails), fails) for name, src, fails in spec]
        for name, src, expect, must_pass, must_fail in controls:
            good, note = _control(name, base, src, expect, must_pass, must_fail)
            ok = ok and good
            print(f"  {'ok  ' if good else 'FAIL'} {note}")
        if base_tool is None:
            ok = False
            print(f"  unrun base_tool_git_show: {why}")
        else:
            fails = [n for n in ALL if n.split("_")[0] in ("K1", "K2", "K3", "K4", "K5", "K6", "K7", "P6")]
            good, note = _control("base_tool", base, base_tool, len(ALL) - len(fails), [n for n in ALL if n not in fails], fails)
            ok = ok and good
            print(f"  {'ok  ' if good else 'FAIL'} {note} (git show {BASE_REV[:12]}:{TOOL})")
    finally:
        shutil.rmtree(base, ignore_errors=True)
    print(f"selftest: {'ok' if ok else 'FAILED'} ({7 if base_tool else 6} controls; P7 satisfied on a fixture lane)")
    return 0 if ok else 1


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
    ap.add_argument("--seed", type=int, help="fixture-id seed (default: random; printed so a run can be repeated)")
    a = ap.parse_args()
    global SEED
    SEED = a.seed if a.seed is not None else int.from_bytes(os.urandom(4), "big")
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
    print(f"C2 resolver-cases {passed}/{NCASES} met={code == 0}  ({PREDICATE})")
    for name, ok, note in res:
        print(f"  {name} {'PASS' if ok else 'FAIL'}  {note}")
    print(f"  seed: {SEED}")
    print(f"  revision: {rev}")
    print(f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
