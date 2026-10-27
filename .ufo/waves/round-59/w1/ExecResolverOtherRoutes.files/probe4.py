#!/usr/bin/env python3
"""Round-59 w1 seat ExecResolverOtherRoutes — probe batch 4 (sharp residuals).

  W1  NBSP after the id cell: the resolver strips it (registers the id), the
      census id grammar rejects the row (E02) -> false green.
  W2  url-match substring test, done right: the SIBLING owns the id and the
      sibling's URL is a prefix of the lane's URL.
  W3  vertical tab (\\x0b) before the id cell: splitlines() splits the row.
  W4  a row that is the *only* content of a list item, at 0 indent after "- ".
  W5  the ASCII-twin case with a Cyrillic lookalike in the knowledge file and the
      ASCII row present: the citation is invisible (ids_cited=0) -> green.
  W6  a knowledge file whose HTML comment holds a citation -> counted.
  W7  live-lane greps: fenced example rows, non-ASCII ids, lookalikes.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys

SEAT = "/fast/scratch/hyaku/kake-r59/ExecResolverOtherRoutes"
WORK = os.path.join(SEAT, "work4")
TOOL = os.path.join(SEAT, "tool", "id_resolver.py")
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"

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
    ("W1_nbps_after_id_cell",
     reg(row("S941", "https://e.example/941").replace("| S941 |", "| S941 |")),
     {"ok.md": "Cites S941.\n"},
     None,
     "NBSP (U+00A0) inside the id cell"),
    ("W2_url_match_substring_sibling_owns",
     reg(row("S942", "https://e.example/942")),
     {"ok.md": "Cites S942 (https://e.example/9422).\n"},
     reg(row("S942", "https://e.example/942")),
     "the sibling owns the id; its URL is a prefix of the lane's URL"),
    ("W3_vertical_tab_before_id_cell",
     reg(row("S943", "https://e.example/943").replace("| S943 |", "|\vS943 |")),
     {"ok.md": "Cites S943.\n"},
     None,
     "vertical tab (U+000B) inside the id cell"),
    ("W4_list_item_only_content_row",
     reg(row("S944", "https://e.example/944")) + "- | S945 | fixture — https://e.example/945 | docs | A | s | a | t | mined | 2026-10-26 | 90d | corpus/knowledge/ok.md |\n",
     {"ok.md": "Cites S944 and S945.\n"},
     None,
     "a pipe row as the whole content of a list item"),
    ("W5_lookalike_citation_ascii_row_present",
     reg(row("S946", "https://e.example/946")),
     {"ok.md": "Cites Ѕ946.\n"},
     None,
     "lookalike citation, ASCII row present"),
    ("W6_html_comment_holds_citation",
     reg(row("S947", "https://e.example/947")),
     {"ok.md": "Cites S947.\n\n<!-- cited S948 here -->\n"},
     None,
     "a citation inside an HTML comment in a knowledge file"),
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

    # ---- live lane greps (read-only) ----
    print("=" * 78)
    print("LIVE LANE greps:")
    pats = {
        "fenced pipe row in knowledge": r"^\s*\|\s*S\d{3,}",
        "non-ascii digit id": r"S[0-9]*[０-９][０-９]*",
        "cyrillic/fullwidth lookalike S": r"[ЅＳ]",
        "nbsp": r" ",
        "html comment in knowledge": r"<!--",
        "html block in SOURCES": r"<(pre|script|style|textarea|details|div)",
        "tab in SOURCES": r"\t",
        "CR in SOURCES": r"\r",
        "u2028/2029": r"[  ]",
    }
    for label, pat in pats.items():
        hits = []
        for root, _dirs, files in os.walk(os.path.join(LANE, "corpus")):
            for fn in files:
                if not fn.endswith(".md"):
                    continue
                p = os.path.join(root, fn)
                try:
                    text = open(p, encoding="utf-8").read()
                except (OSError, UnicodeDecodeError):
                    continue
                for i, line in enumerate(text.splitlines(), 1):
                    if re.search(pat, line):
                        hits.append(f"{os.path.relpath(p, LANE)}:{i}")
                        break
        print(f"  {label:34s} {len(hits)} file(s) {hits[:4]}")
    with open(os.path.join(SEAT, "results4.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
