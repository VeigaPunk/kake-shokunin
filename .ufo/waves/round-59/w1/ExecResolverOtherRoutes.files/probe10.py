#!/usr/bin/env python3
"""Round-59 w1 seat ExecResolverOtherRoutes — probe batch 10 (section boundaries).

  H1  an HTML-comment-hidden `## Paths` ENDS the Registry section for a
      comment-aware parser, but not for the current one -> rows after it stay
      registered (false green).
  H2  an HTML-comment-hidden `## Registry` OPENS a section -> rows after a real
      section ended register (false green).
  H3  a `<pre>`-hidden `## Paths` (not a comment) -> same direction; a
      comment-only K8 fix leaves it open.
  H4  registry has `S971` (ASCII); knowledge cites `S<fullwidth 9>71` -> the
      dangling line prints a non-ASCII id.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

SEAT = "/fast/scratch/hyaku/kake-r59/ExecResolverOtherRoutes"
WORK = os.path.join(SEAT, "work10")
TOOL = os.path.join(SEAT, "tool", "id_resolver.py")
NARROW = os.path.join(SEAT, "variants", "narrow_html.py")
FULL = os.path.join(SEAT, "variants", "full_html.py")
CENSUS = "/home/vgpnk/Projects/shogun"  # unused placeholder guard

FW = {d: chr(0xFF10 + int(d)) for d in "0123456789"}
HDR = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "|---|---|---|---|---|---|---|---|---|---|---|\n")
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"


def row(sid, url=None):
    url = url or ("https://e.example/" + sid[1:])
    return (f"| {sid} | fixture source — {url} | docs | A | scope | anchor | teaches | "
            f"mined | 2026-10-26 | 90d | corpus/knowledge/ok.md |\n")


def reg(body):
    return "# Sources\n\n## Registry\n\n" + HDR + body


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(data, str):
        data = data.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)


def build(case, registry, knowledge):
    root = os.path.join(WORK, case)
    if os.path.exists(root):
        shutil.rmtree(root)
    fleet = os.path.join(root, "fleet")
    lane = os.path.join(fleet, "kake-shokunin")
    write(os.path.join(lane, "corpus", "SOURCES.md"), registry)
    for rel, body in knowledge.items():
        write(os.path.join(lane, "corpus", "knowledge", rel), body)
    return fleet, lane


def run_tool(tool, lane, fleet):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"] = "C.UTF-8"
    p = subprocess.run([sys.executable, "-B", tool, "--root", lane, "--fleet", fleet],
                       capture_output=True, env=env, timeout=300)
    return {"exit": p.returncode, "out": (p.stdout + p.stderr).decode("utf-8", "replace").strip()}


def run_census(lane):
    env = dict(os.environ)
    env["LC_ALL"] = "C.UTF-8"
    c = subprocess.run([CENSUS, "census", "--root", lane, lane], capture_output=True, env=env, timeout=300)
    v = subprocess.run([CENSUS, "validate", "--today", "2026-10-26", lane], capture_output=True, env=env, timeout=300)
    rows = None
    for line in c.stdout.decode("utf-8", "replace").splitlines():
        parts = line.split("\t")
        if len(parts) >= 3 and parts[1] == "rows":
            rows = parts[2]
    findings = [ln for ln in v.stdout.decode("utf-8", "replace").splitlines() if "\tE" in ln]
    return {"rows": rows, "validate_exit": v.returncode, "findings": findings}


CASES = [
    ("H1_comment_hidden_paths_heading",
     reg(row("S991") + "<!--\n## Paths\n-->\n\n" + row("S992")),
     {"ok.md": "Cites S991 and S992.\n"},
     "a comment-hidden `## Paths` must end the section; the current parser keeps it open"),
    ("H2_comment_hidden_registry_heading",
     reg(row("S993")) + "\n## Paths\n\n" + row("S994") + "<!--\n## Registry\n-->\n\n" + row("S995"),
     {"ok.md": "Cites S993, S994 and S995.\n"},
     "a comment-hidden `## Registry` must not reopen the section"),
    ("H3_pre_hidden_paths_heading",
     reg(row("S996") + "<pre>\n## Paths\n</pre>\n\n" + row("S997")),
     {"ok.md": "Cites S996 and S997.\n"},
     "a <pre>-hidden `## Paths` must end the section; a comment-only fix leaves it open"),
    ("H4_fullwidth_citation_of_ascii_row",
     reg(row("S971")),
     {"ok.md": "Cites S" + FW["9"] + FW["7"] + FW["1"] + " here.\n"},
     "registry has the ASCII S971; the citation uses fullwidth digits -> what is printed?"),
]


def main() -> int:
    os.makedirs(WORK, exist_ok=True)
    results = []
    for name, registry, knowledge, note in CASES:
        fleet, lane = build(name, registry, knowledge)
        cen = run_census(lane)
        cur = run_tool(TOOL, lane, fleet)
        nar = run_tool(NARROW, lane, fleet)
        ful = run_tool(FULL, lane, fleet)
        print("=" * 78)
        print("CASE", name, "|", note)
        print("  census rows:", cen["rows"], "validate exit:", cen["validate_exit"], cen["findings"])
        for label, r in (("current", cur), ("narrow_comment_fix", nar), ("full_html_fix", ful)):
            print(f"  {label:18s} exit={r['exit']}")
            for line in r["out"].splitlines():
                print("      |", line)
        results.append({"case": name, "note": note, "census": cen,
                        "current": cur, "narrow": nar, "full": ful})
    with open(os.path.join(SEAT, "results10.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
