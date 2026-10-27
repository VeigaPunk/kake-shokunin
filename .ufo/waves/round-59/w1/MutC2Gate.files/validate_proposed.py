#!/usr/bin/env python3
"""MutC2Gate — validate the PROPOSED cases.

Builds a scratch extension of the frozen counter that adds the proposed cases, then runs it
against (a) the GREEN reference tool and (b) every surviving mutant, to show which proposed
case kills which survivor. SCRATCH ONLY.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

S = "/fast/scratch/hyaku/kake-r59/MutC2Gate"
FIX = os.path.join(S, "fix")
TOOL = "scripts/id_resolver.py"
WORK = os.path.join(S, "work10")
GREEN = "fd8c7845b94f8a3d7ea8b815d7b70ed658604a03"

PROPOSED = '''

# --------------------------------------------------------------------------- proposed cases (MutC2Gate)
def _proposed_cases(tool: str, root: str, rev: str, work: str) -> list[tuple[str, bool, str]]:
    """The cases this seat proposes to add to the frozen counter (wave-1 attack finding)."""
    py = [sys.executable, "-B", tool]
    out: list[tuple[str, bool, str]] = []

    def check(name, argv, want_rc, want_re, forbid_re=()):
        rc, text = run(py + argv)
        ok = rc == want_rc and all(re.search(p, text, re.M) for p in want_re) and not any(re.search(p, text, re.M) for p in forbid_re)
        out.append((name, ok, f"exit={rc} " + " | ".join(text.strip().splitlines()[-3:])[:300]))

    ok_id, ext_id, sib_id, fence_id, def_id, pre_id, u_id, s44 = fixture_ids(8)
    reg_ok = "## Registry\\n\\n" + HDR + row(ok_id)

    # Q1: a knowledge file whose name is not .md is not a citation source (H13)
    fl, lp, _ = lane(work, "q1", registry(reg_ok),
                     {"ok.md": f"Cites {ok_id}.\\n", "notes.json": f"Cites {ext_id}.\\n"})
    check("Q1_non_markdown_knowledge_file_is_not_read", ["--root", lp, "--fleet", fl], 0,
          [r"^ids_cited=1 ids_resolved=1 dangling=0 "], [rf"^DANGLING {ext_id} "])

    # Q2: a backtick fence whose info string holds a backtick does not open a block, so the
    #     row after it registers (H20)
    fl, lp, _ = lane(work, "q2", registry(reg_ok + "```a`b\\n" + row(fence_id) + "```\\n"),
                     {"ok.md": f"Cites {ok_id} and {fence_id}.\\n"})
    check("Q2_backtick_fence_info_string_blocks_a_fence", ["--root", lp, "--fleet", fl], 0,
          [r"^ids_cited=2 ids_resolved=2 dangling=0 "], [rf"^DANGLING {fence_id} "])

    # Q3: without --fleet the fleet root is the lane's parent, not the lane (H15)
    fl, lp, _ = lane(work, "q3", registry(reg_ok), {"ok.md": f"Cites {ok_id} and {sib_id}.\\n"},
                     siblings={"alpha-shokunin": registry("## Registry\\n\\n" + HDR + row(sib_id))})
    check("Q3_default_fleet_root_is_the_lane_parent", ["--root", lp], 1,
          [rf"^DANGLING {sib_id} .*owners=alpha-shokunin"])

    # Q4: a knowledge symlink to a sibling path that shares the lane's path prefix is outside (H05/H06)
    def b4(lp, r):
        put(lp, "corpus/SOURCES.md", registry(reg_ok))
        put(lp, "corpus/knowledge/ok.md", f"Cites {ok_id}.\\n")
        evil = os.path.join(r, "fleet", "kake-shokunin-evil")
        put(evil, "corpus/knowledge/leak.md", f"Cites {pre_id}.\\n")
        os.symlink(os.path.join(evil, "corpus", "knowledge", "leak.md"),
                   os.path.join(lp, "corpus", "knowledge", "leak.md"))
    fl, lp, _ = lane_fs(work, b4)
    check("Q4_prefix_sharing_symlink_is_outside_the_lane", ["--root", lp, "--fleet", fl], 0,
          [r"^ids_cited=1 ids_resolved=1 dangling=0 "], [rf"^DANGLING {pre_id} "])

    # Q5: a registry symlinked to a path that shares the lane's prefix is outside the lane (H05)
    def b5(lp, r):
        evil = os.path.join(r, "fleet", "kake-shokunin-evil")
        put(evil, "corpus/SOURCES.md", registry("## Registry\\n\\n" + HDR + row(ok_id) + row(def_id)))
        put(lp, "corpus/knowledge/ok.md", f"Cites {ok_id} and {def_id}.\\n")
        os.symlink(os.path.join(evil, "corpus", "SOURCES.md"), os.path.join(lp, "corpus", "SOURCES.md"))
    fl, lp, _ = lane_fs(work, b5)
    check("Q5_prefix_sharing_registry_symlink_is_unevaluable", ["--root", lp, "--fleet", fl], 2, [],
          [r"^ids_cited=\\d+ ids_resolved=\\d+ dangling=0\\b"])

    # Q7: a registry URL that ends in a backtick is not matched verbatim (H08)
    fl, lp, _ = lane(work, "q7", registry(reg_ok), {"ok.md": f"Cites {ok_id} and {u_id}. — see https://example.invalid/{u_id} here.\\n"},
                     siblings={"alpha-shokunin": registry("## Registry\\n\\n" + HDR + row(u_id).replace(
                         f"https://example.invalid/{u_id}", f"https://example.invalid/{u_id}`"))})
    check("Q7_registry_url_ending_in_a_backtick_is_not_matched", ["--root", lp, "--fleet", fl], 1,
          [rf"^DANGLING {u_id} .*owners=alpha-shokunin url-match=alpha-shokunin"])

    # Q8: a symlink to another symlink is never read as its target string (H18)
    def b8(lp, r):
        put(lp, "corpus/SOURCES.md", registry(reg_ok))
        put(lp, "corpus/knowledge/ok.md", f"Cites {ok_id}.\\n")
        put(lp, "corpus/S044-target.md", f"Cites {s44}.\\n")
        os.symlink("../S044-target.md", os.path.join(lp, "corpus", "knowledge", "leaf.md"))
        os.symlink("leaf.md", os.path.join(lp, "corpus", "knowledge", "mid.md"))
    fl, lp, _ = lane_fs(work, b8)
    head8 = commit_all(lp)
    check("Q8_symlink_to_a_symlink_is_not_read_as_its_target_string",
          ["--root", lp, "--fleet", fl, "--revision", head8], 1,
          [rf"^DANGLING {s44} ", r"^ids_cited=2 ids_resolved=1 dangling=1 "], [rf"cited-by=[^ ]*,corpus/knowledge/mid\\.md "])

    # Q6: the tool's own selftest is verified independently of the tally it prints: the printed
    #     total must equal the number of case lines the tool actually emitted, no case may have
    #     failed, and the floor must hold (the frozen P6 reads the printed tally alone)
    st = tempfile.mkdtemp(dir=work)
    shutil.copy(tool, os.path.join(st, "id_resolver.py"))
    rc, text = run([sys.executable, "-B", os.path.join(st, "id_resolver.py"), "--selftest"], cwd=st)
    lines = text.splitlines()
    case_lines = [ln for ln in lines if ln.startswith("ok ") or ln.startswith("FAIL ")]
    fails = [ln for ln in lines if ln.startswith("FAIL ")]
    m = re.findall(r"(?m)^selftest: (\\d+)/(\\d+)\\s*$", text)
    reasons = []
    if fails:
        reasons.append(f"{len(fails)} failing case(s)")
    if not m:
        reasons.append("no tally")
    else:
        if int(m[-1][1]) != len(case_lines):
            reasons.append(f"tally total {m[-1][1]} != {len(case_lines)} case lines")
        if int(m[-1][0]) != int(m[-1][1]):
            reasons.append("tally passed != total")
        if int(m[-1][1]) < P6_FLOOR:
            reasons.append(f"tally total {m[-1][1]} < floor {P6_FLOOR}")
    if rc != 0:
        reasons.append(f"exit={rc}")
    out.append(("Q6_selftest_tally_is_independently_verified", not reasons,
                "; ".join(reasons) if reasons else f"tally={m[-1] if m else None} case_lines={len(case_lines)}"))
    return out
'''

ANCHOR = "\n\n# --------------------------------------------------------------------------- selftest\n"


def build_proposed_counter():
    src = open(os.path.join(FIX, ".ufo/waves/round-59/c59_resolver_cases.py"), encoding="utf-8").read()
    assert src.count(ANCHOR) == 1
    src = src.replace(ANCHOR, PROPOSED + ANCHOR)
    # call the proposed cases from measure() and count them
    old = """    res = case_results(tool, root, rev, work)
    return (0 if all(ok for _, ok, _ in res) and len(res) == NCASES else 1), res"""
    new = """    res = case_results(tool, root, rev, work)
    res = res + _proposed_cases(tool, root, rev, work)
    total = NCASES + 8
    return (0 if all(ok for _, ok, _ in res) and len(res) == total else 1), res"""
    assert src.count(old) == 1
    src = src.replace(old, new)
    src = src.replace('NCASES = 21', 'NCASES = 21\nNCASES_PROPOSED = 8')
    src = src.replace('print(f"C2 resolver-cases {passed}/{NCASES} met={code == 0}  ({PREDICATE})")',
                      'print(f"C2 resolver-cases {passed}/{NCASES + NCASES_PROPOSED} met={code == 0}  ({PREDICATE})")')
    path = os.path.join(S, "c59_resolver_cases_proposed.py")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(src)
    return path


def run(argv, timeout=900):
    p = subprocess.run(argv, capture_output=True, timeout=timeout)
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def parse(text):
    cases = {}
    tally = None
    for line in text.splitlines():
        m = re.match(r"^  (\S+) (PASS|FAIL)\s+(.*)$", line)
        if m:
            cases[m.group(1)] = (m.group(2), m.group(3))
        m2 = re.match(r"^C2 resolver-cases (\d+)/(\d+) met=(\w+)", line)
        if m2:
            tally = (int(m2.group(1)), int(m2.group(2)), m2.group(3))
    return tally, cases


def main():
    import json
    os.makedirs(WORK, exist_ok=True)
    counter = build_proposed_counter()
    commits = {}
    for fname in ("green_mutants.json", "green_mutants2.json"):
        for r in json.load(open(os.path.join(S, fname)))["results"]:
            if r.get("id"):
                commits[r["id"]] = r.get("commit")
    survivors = ["G14", "G21", "G25", "G26", "H01", "H02", "H05", "H06", "H08", "H13", "H15", "H18", "H20"]

    rc, text = run([sys.executable, "-B", counter, "--root", FIX, "--revision", GREEN,
                    "--work", WORK, "--seed", "59"])
    tally, cases = parse(text)
    print("PROPOSED COUNTER on the GREEN tool:", tally, flush=True)
    for k, v in cases.items():
        if k.startswith("Q"):
            print(f"   {k} {v[0]}  {v[1][:120]}")
    green_q = {k: v[0] for k, v in cases.items() if k.startswith("Q")}
    print()

    for mid in survivors:
        rev = commits.get(mid)
        if not rev:
            continue
        rc, text = run([sys.executable, "-B", counter, "--root", FIX, "--revision", rev,
                        "--work", WORK, "--seed", "59"])
        tally, cases = parse(text)
        killed = [k for k, v in cases.items() if k.startswith("Q") and v[0] == "FAIL"]
        print(f"{mid}: proposed tally={tally} killed_by={killed}", flush=True)


if __name__ == "__main__":
    main()
