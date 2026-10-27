#!/usr/bin/env python3
"""Round-59 w1 seat ExecResolverOtherRoutes — probe batch 8 (final, exact bytes).

Every special character is an explicit escape, so the fixture bytes are exact
and are printed as hex for the report.

  F1  S + U+200B + digits in a knowledge citation -> the id is invisible.
  F2  U+200B inside a registry id cell -> the row does not register.
  F3  Arabic-Indic digits (U+0660..) after ASCII S -> Python's \\d matches them.
  F4  clean url-match substring case: the lane does NOT own the id, the sibling
      does, and the lane cites a URL that merely CONTAINS the sibling's URL.
  F5  cited-side asymmetry: an id inside a fenced block / HTML comment of a
      knowledge file is counted as a citation (the registry side is fence-aware).
  F6  an id glued to a fullwidth digit is read as the ASCII id.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

SEAT = "/fast/scratch/hyaku/kake-r59/ExecResolverOtherRoutes"
WORK = os.path.join(SEAT, "work8")
TOOL = os.path.join(SEAT, "tool", "id_resolver.py")
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"

ZWSP = ""
AR = {d: chr(0x0660 + int(d)) for d in "0123456789"}
FW9 = chr(0xFF19)

HDR = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "|---|---|---|---|---|---|---|---|---|---|---|\n")


def row(sid: str, url: str = "https://e.example/src", indent: str = "") -> str:
    return (f"{indent}| {sid} | fixture source — {url} | docs | A | scope | anchor | teaches | "
            f"mined | 2026-10-26 | 90d | corpus/knowledge/ok.md |\n")


def reg(body: str) -> str:
    return "# Sources\n\n## Registry\n\n" + HDR + body


def write(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(data, str):
        data = data.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)


def build(case, registry, knowledge, sibling=None):
    root = os.path.join(WORK, case)
    if os.path.exists(root):
        shutil.rmtree(root)
    fleet = os.path.join(root, "fleet")
    lane = os.path.join(fleet, "kake-shokunin")
    write(os.path.join(lane, "corpus", "SOURCES.md"), registry)
    for rel, body in knowledge.items():
        write(os.path.join(lane, "corpus", "knowledge", rel), body)
    if sibling is not None:
        write(os.path.join(fleet, "alpha-shokunin", "corpus", "SOURCES.md"), sibling)
    return fleet, lane


def run_tool(tool, lane, fleet, revision=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"] = "C.UTF-8"
    argv = [sys.executable, "-B", tool, "--root", lane, "--fleet", fleet]
    if revision:
        argv += ["--revision", revision]
    p = subprocess.run(argv, capture_output=True, env=env, timeout=300)
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


AR_ID = "S" + AR["9"] + AR["9"] + AR["1"]

CASES = [
    ("F1_zwsp_inside_cited_id",
     reg(row("S961", "https://e.example/961")),
     {"ok.md": f"Cites S{ZWSP}962 which is registered nowhere.\n"},
     None,
     "U+200B between S and the digits: the citation is invisible"),
    ("F2_zwsp_inside_registry_id_cell",
     reg(row(f"S{ZWSP}963", "https://e.example/963")),
     {"ok.md": "Cites S963.\n"},
     None,
     "U+200B inside the registry id cell: the row does not register"),
    ("F3_arabic_indic_digits_id",
     reg(row(AR_ID, "https://e.example/964")),
     {"ok.md": f"Cites {AR_ID}.\n"},
     None,
     "Arabic-Indic digits: Python's \\d matches them, the census grammar does not"),
    ("F4_url_match_substring_clean",
     reg(row("S965", "https://e.example/965")),
     {"ok.md": "Cites S966 (https://e.example/9662).\n"},
     reg(row("S966", "https://e.example/966")),
     "the sibling owns S966 with URL U; the lane cites U2 which merely contains U"),
    ("F5_cited_side_fence_and_comment",
     reg(row("S967", "https://e.example/967")),
     {"ok.md": "Cites S967.\n\n```\n| S968 | quoted row |\n```\n\n<!-- cites S969 -->\n"},
     None,
     "ids inside a fenced block and an HTML comment of a knowledge file count as citations"),
    ("F6_id_glued_to_fullwidth_digit",
     reg(row("S970", "https://e.example/970")),
     {"ok.md": f"Cites S970{FW9} in passing.\n"},
     None,
     "an ASCII id glued to a fullwidth digit is read as the ASCII id"),
]


def main() -> int:
    os.makedirs(WORK, exist_ok=True)
    results = []
    for name, registry, knowledge, sibling, note in CASES:
        fleet, lane = build(name, registry, knowledge, sibling)
        # exact bytes of the interesting knowledge file
        kb = knowledge["ok.md"].encode("utf-8")
        cen = run_census(lane)
        res = run_tool(TOOL, lane, fleet)
        print("=" * 78)
        print("CASE", name, "|", note)
        print("  knowledge bytes:", kb.hex())
        print("  census rows:", cen["rows"], "validate exit:", cen["validate_exit"])
        for f in cen["findings"]:
            print("   !", f)
        print("  resolver exit:", res["exit"])
        for line in res["out"].splitlines():
            print("   |", line)
        results.append({"case": name, "note": note, "kb_hex": kb.hex(), "census": cen, "resolver": res})
    with open(os.path.join(SEAT, "results8.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
