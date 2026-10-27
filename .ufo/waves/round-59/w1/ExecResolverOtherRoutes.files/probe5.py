#!/usr/bin/env python3
"""Round-59 w1 seat ExecResolverOtherRoutes — probe batch 5 (decisive residuals).

  X1  `## Registry` indented by 1/2/3 spaces: the census counts the rows (its
      heading rule allows 0-3 leading spaces), the resolver's heading regex
      requires column 0 -> the citation dangles (false red).
  X2  a citation split by a zero-width space inside the id: the resolver sees
      no id at all -> green although the file cites the id.
  X3  a citation whose 'S' is a Cyrillic lookalike: same laundering.
  X4  a registry id cell with fullwidth digits: the resolver accepts it, the
      census rejects it (E02) -> false green against the lane id grammar.
  X5  a registry heading `## Registry ##` (ATX closing sequence): CommonMark
      says the heading text is "Registry"; both lane tools say "no section".
  X6  live lane: do fenced blocks in knowledge files quote registry rows with
      real ids (a live false red today)?
  X7  live lane: the indented-heading variant does not occur today.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys

SEAT = "/fast/scratch/hyaku/kake-r59/ExecResolverOtherRoutes"
WORK = os.path.join(SEAT, "work5")
TOOL = os.path.join(SEAT, "tool", "id_resolver.py")
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"

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


CASES = []
for n_spaces, sid in ((1, "S951"), (2, "S952"), (3, "S953")):
    CASES.append((
        f"X1_indented_registry_heading_{n_spaces}space",
        "# Sources\n\n" + " " * n_spaces + "## Registry\n\n" + HDR + row(sid, "https://e.example/" + sid),
        {"ok.md": f"Cites {sid}.\n"},
        None,
        f"`## Registry` indented {n_spaces} space(s): census counts the row, the resolver does not",
    ))

CASES += [
    ("X2_zero_width_split_id_in_knowledge",
     "# Sources\n\n## Registry\n\n" + HDR + row("S954", "https://e.example/954"),
     {"ok.md": "Cites S955 which is not registered.\n"},
     None,
     "zero-width space inside the cited id: the resolver sees no citation at all"),
    ("X3_cyrillic_lookalike_S_citation_only",
     "# Sources\n\n## Registry\n\n" + HDR + row("S956", "https://e.example/956"),
     {"ok.md": "Cites Ѕ957 which is not registered.\n"},
     None,
     "Cyrillic lookalike S: the citation is invisible to the resolver"),
    ("X4_fullwidth_digit_registry_id",
     "# Sources\n\n## Registry\n\n" + HDR + row("S９５８", "https://e.example/958"),
     {"ok.md": "Cites S９５８.\n"},
     None,
     "registry id with fullwidth digits: resolver accepts, census rejects (E02)"),
    ("X5_registry_heading_atx_closing_sequence",
     "# Sources\n\n## Registry ##\n\n" + HDR + row("S959", "https://e.example/959"),
     {"ok.md": "Cites S959.\n"},
     None,
     "`## Registry ##`: CommonMark heading text is `Registry`; both lane tools say no section"),
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

    # ---- X6: live lane, ids quoted inside fenced blocks in knowledge files ----
    print("=" * 78)
    print("X6 live lane: ids inside fenced blocks of knowledge files")
    idre = re.compile(r"(?<![A-Za-z0-9_])S\d{3,}(?![A-Za-z0-9_])")
    hits = []
    for fn in sorted(os.listdir(os.path.join(LANE, "corpus", "knowledge"))):
        if not fn.endswith(".md"):
            continue
        p = os.path.join(LANE, "corpus", "knowledge", fn)
        text = open(p, encoding="utf-8").read()
        inside = False
        for i, line in enumerate(text.splitlines(), 1):
            if re.match(r"^ {0,3}(`{3,}|~{3,})", line):
                inside = not inside
                continue
            if inside:
                for m in idre.findall(line):
                    hits.append((fn, i, m))
    print("   fenced-block ids in knowledge:", len(hits), hits[:12])

    # ---- X7: live lane, is the Registry heading ever indented? ----
    print("=" * 78)
    print("X7 live lane: heading forms in corpus/SOURCES.md")
    for i, line in enumerate(open(os.path.join(LANE, "corpus", "SOURCES.md"), encoding="utf-8").read().splitlines(), 1):
        if re.match(r"^ {0,3}#{1,6}", line):
            print(f"   {i}: {line!r}")

    with open(os.path.join(SEAT, "results5.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
