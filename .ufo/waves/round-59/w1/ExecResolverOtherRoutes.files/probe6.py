#!/usr/bin/env python3
"""Round-59 w1 seat ExecResolverOtherRoutes — probe batch 6 (mirror cases).

  Y1  an INDENTED non-Registry heading (`  ## Paths`) must end the Registry
      section (the census does: its heading rule tolerates 0-3 leading spaces).
      The resolver's SECTION_END_RE is column-0 anchored -> the section stays
      open and rows after the heading are wrongly registered -> FALSE GREEN.
  Y2  the same for an indented `# Heading`.
  Y3  url-match is a substring test: the sibling owns the id, the sibling's URL
      is a prefix of the lane's URL -> url-match fires without the lane citing
      that URL.
  Y4  a citation whose 'S' is the Cyrillic lookalike: the id is laundered out of
      the cited set (ids_cited=0) while the file cites an unregistered source.
  Y5  a citation split by a zero-width space (U+200B) inside the id.
  Y6  a registry heading at 1-3 spaces: the census counts the row, the resolver
      does not -> FALSE RED (the mirror of Y1).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

SEAT = "/fast/scratch/hyaku/kake-r59/ExecResolverOtherRoutes"
WORK = os.path.join(SEAT, "work6")
TOOL = os.path.join(SEAT, "tool", "id_resolver.py")
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"

HDR = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "|---|---|---|---|---|---|---|---|---|---|---|\n")


def row(sid: str, url: str = "https://e.example/src", indent: str = "") -> str:
    return (f"{indent}| {sid} | fixture source — {url} | docs | A | scope | anchor | teaches | "
            f"mined | 2026-10-26 | 90d | corpus/knowledge/ok.md |\n")


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
    return {"rows": rows, "census_exit": c.returncode, "validate_exit": v.returncode, "findings": findings}


CASES = [
    ("Y1_indented_paths_heading_ends_section",
     "# Sources\n\n## Registry\n\n" + HDR + row("S961", "https://e.example/961") +
     "  ## Paths\n\n" + row("S962", "https://e.example/962"),
     {"ok.md": "Cites S961 and S962.\n"},
     None,
     "rows after an indented `## Paths` must be outside the Registry (the census says so)"),
    ("Y2_indented_h1_ends_section",
     "# Sources\n\n## Registry\n\n" + HDR + row("S963", "https://e.example/963") +
     " # Notes\n\n" + row("S964", "https://e.example/964"),
     {"ok.md": "Cites S963 and S964.\n"},
     None,
     "rows after an indented `# Notes` must be outside the Registry"),
    ("Y3_url_match_substring",
     "# Sources\n\n## Registry\n\n" + HDR + row("S965", "https://e.example/965"),
     {"ok.md": "Cites S965 (https://e.example/9652).\n"},
     "# Sources\n\n## Registry\n\n" + HDR + row("S965", "https://e.example/965"),
     "the sibling owns S965; its URL is a prefix of the lane's URL -> url-match fires spuriously"),
    ("Y4_cyrillic_lookalike_laundering",
     "# Sources\n\n## Registry\n\n" + HDR + row("S966", "https://e.example/966"),
     {"ok.md": "Cites S967 which is not registered anywhere.\n"},
     None,
     "the Cyrillic lookalike S hides the citation from the cited set"),
    ("Y5_zero_width_space_inside_id",
     "# Sources\n\n## Registry\n\n" + HDR + row("S968", "https://e.example/968"),
     {"ok.md": "Cites S969 which is not registered anywhere.\n"},
     None,
     "a zero-width space inside the cited id hides the citation"),
    ("Y6_indented_registry_heading",
     "# Sources\n\n  ## Registry\n\n" + HDR + row("S970", "https://e.example/970"),
     {"ok.md": "Cites S970.\n"},
     None,
     "an indented `## Registry` is the Registry section for the census, not for the resolver"),
]


def main() -> int:
    os.makedirs(WORK, exist_ok=True)
    results = []
    for name, registry, knowledge, sibling, note in CASES:
        fleet, lane = build(name, registry, knowledge, sibling)
        cen = run_census(lane)
        res = run_tool(TOOL, lane, fleet)
        results.append({"case": name, "note": note, "census": cen, "resolver": res})
        print("=" * 78)
        print("CASE", name, "|", note)
        print("  census rows:", cen["rows"], "validate exit:", cen["validate_exit"])
        for f in cen["findings"]:
            print("   !", f)
        print("  resolver exit:", res["exit"])
        for line in res["out"].splitlines():
            print("   |", line)
    with open(os.path.join(SEAT, "results6.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
