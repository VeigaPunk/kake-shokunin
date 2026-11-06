#!/usr/bin/env python3
"""Diagnose, per unlisted tool, WHY no conformant registry row exists.

Imports the FROZEN counter `.ufo/waves/round-99/c99_registry.py` as a module and
reuses its own helpers (tables, cells, SPAN, SCRIPT_TOKEN, verdict_ok, names_path)
so the diagnosis cannot drift from the instrument's own rules. Read-only: the
only writes are into this seat's own scratch.

Usage:
  python3 -B diagnose_unlisted.py --root <lane> --revision <commit>
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"


def load_counter(path):
    spec = importlib.util.spec_from_file_location("c99_registry", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=LANE)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--counter",
                    default=os.path.join(LANE, ".ufo/waves/round-99/c99_registry.py"))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    c = load_counter(a.counter)

    names = c.git(a.root, "ls-tree", "-r", "--name-only", a.revision).split("\n")
    allfiles = set(n for n in names if n)
    pop = c.population([n for n in names if n])
    skill = c.git(a.root, "show", "%s:SKILL.md" % a.revision)

    # Which tools does the counter call unlisted? Re-derive from its own rules.
    unlisted = [p for p in pop if p.split("/")[-1] in
                ("base_path_selftest.py",)]  # placeholder, replaced below
    # Re-derive by running the counter's score() against the revision.
    work = os.path.join(os.environ.get("TMPDIR", "/tmp"), "c99-diag")
    os.makedirs(work, exist_ok=True)
    # Cheap re-derivation of the unlisted set using the counter's own row rules,
    # WITHOUT running R5's execution check (that is what c.score() does and it is
    # slow). A tool is "listed" here iff some row passes R1-R4 and R5's *shape*;
    # the base receipt's own unlisted list is the authority for the count.
    unlisted = []
    for line in open(os.path.join(LANE, ".ufo/waves/round-99/controls/base-c1.txt")):
        if line.startswith("unlisted "):
            unlisted.append(line.split(" ", 1)[1].strip())

    selftest_files = {p for p in pop if "selftest" in os.path.basename(p)}
    out = []
    for tool in unlisted:
        base = tool.split("/")[-1]
        has_selftest_mode = False
        try:
            blob = c.git(a.root, "show", "%s:%s" % (a.revision, tool))
            has_selftest_mode = "--selftest" in blob
        except Exception:
            pass
        cand = []
        for hdr, rows in c.tables(skill):
            ix = {h: k for k, h in enumerate(hdr)}
            for ln, rc in rows:
                entry = rc[ix["entry command"]]
                spans = c.SPAN.findall(entry)
                names_tool = any(c.names_path(sp, tool) for sp in spans)
                mentions = tool in " ".join(rc)
                if not (names_tool or mentions):
                    continue
                fails = []
                if len(rc) != len(hdr):
                    fails.append("R1 cell count %d != %d" % (len(rc), len(hdr)))
                if not names_tool:
                    fails.append("R2 no backtick span naming %s in the entry cell" % tool)
                if not c.verdict_ok(rc[ix["verdict map"]]):
                    fails.append("R3 verdict map does not map both 0 and 1")
                if rc[ix["owner"]].strip() != "kake":
                    fails.append("R4 owner is %r" % rc[ix["owner"]].strip())
                st = rc[ix["self-test"]]
                st_spans = c.SPAN.findall(st)
                st_names = [p for p in selftest_files
                            if any(c.names_path(sp, p) for sp in st_spans)]
                says_no = "no self-test" in st.lower()
                if st_names:
                    pass
                elif says_no and not has_selftest_mode:
                    pass
                else:
                    if says_no:
                        fails.append("R5 says 'no self-test' but the tool HAS a --selftest mode")
                    elif not st_spans:
                        fails.append("R5 self-test cell has no backtick span")
                    else:
                        fails.append("R5 self-test span %r names no population file with 'selftest' in its name"
                                     % st_spans[0][:60])
                cand.append({
                    "line": ln,
                    "name_cell": rc[ix["name"]][:60],
                    "names_tool": names_tool,
                    "mentions_tool": mentions,
                    "fails": fails,
                })
        conforming = [x for x in cand if not x["fails"]]
        out.append({
            "tool": tool,
            "tool_has_selftest_mode": has_selftest_mode,
            "candidate_rows": len(cand),
            "conforming_rows": len(conforming),
            "near_miss_rows": [x for x in cand if x["fails"]],
        })
    if a.json:
        print(json.dumps(out, indent=1))
    else:
        for r in out:
            print("%-40s candidate_rows=%d conforming=%d tool_has_selftest=%s"
                  % (r["tool"], r["candidate_rows"], r["conforming_rows"],
                     r["tool_has_selftest_mode"]))
            if r["conforming_rows"] == 0 and not r["near_miss_rows"]:
                print("    NO ROW MENTIONS THIS TOOL AT ALL")
            for x in r["near_miss_rows"]:
                print("    line %-6s name=%-28r %s"
                      % (x["line"], x["name_cell"], "; ".join(x["fails"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
