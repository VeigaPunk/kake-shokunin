#!/usr/bin/env python3
"""Round-59 w1 seat ExecResolverOtherRoutes — probe batch 7 (corrected fixtures).

Every non-ASCII character is written with an explicit escape so the fixture bytes
are exact:

  Z1  Cyrillic U+0405 in place of the ASCII S in a citation -> the id is
      laundered out of the cited set (green although the file cites an
      unregistered source).
  Z2  fullwidth digits (U+FF10..) in a registry id cell -> the resolver accepts
      the row as an id (resolves the citation) while the lane id grammar
      (census E02) rejects it.
  Z3  zero-width space (U+200B) inside a cited id -> the citation is invisible.
  Z4  url-match is a substring test over the whole citing body: the sibling
      owns the id with URL U, the lane cites a DIFFERENT URL that merely
      contains U -> url-match fires (the signal claims the lane cites the
      sibling's source).
  Z5  an id inside a URL in a knowledge file is counted as a citation
      (over-report -> false red).
  Z6  the top findings repeated at --revision (git blobs), so the result holds
      for the mode C2 measures.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

SEAT = "/fast/scratch/hyaku/kake-r59/ExecResolverOtherRoutes"
WORK = os.path.join(SEAT, "work7")
TOOL = os.path.join(SEAT, "tool", "id_resolver.py")
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"

CYR_S = "Ѕ"      # CYRILLIC CAPITAL LETTER ES (looks like S)
FW = {d: chr(0xFF10 + int(d)) for d in "0123456789"}   # fullwidth digits
ZWSP = ""

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


def commit(path):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    subprocess.run(["git", "-C", path, "init", "-q"], check=True, env=env)
    top = subprocess.run(["git", "-C", path, "rev-parse", "--show-toplevel"], capture_output=True,
                         env=env, text=True).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(path):
        raise RuntimeError("toplevel mismatch")
    subprocess.run(["git", "-C", path, "add", "-A"], check=True, env=env)
    subprocess.run(["git", "-C", path, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
                    "-c", "commit.gpgsign=false", "commit", "-q", "-m", "fixture"], check=True, env=env)
    return subprocess.run(["git", "-C", path, "rev-parse", "HEAD"], capture_output=True,
                          env=env, text=True).stdout.strip()


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


fw_id = "S" + FW["9"] + FW["7"] + FW["1"]

CASES = [
    ("Z1_cyrillic_S_launders_citation",
     reg(row("S981", "https://e.example/981")),
     {"ok.md": f"Cites {CYR_S}982 which is registered nowhere.\n"},
     None,
     "Cyrillic U+0405 instead of ASCII S: the cited id disappears from the cited set"),
    ("Z2_fullwidth_digit_registry_id",
     reg(row(fw_id, "https://e.example/982")),
     {"ok.md": f"Cites {fw_id}.\n"},
     None,
     "fullwidth digits in the registry id cell: resolver accepts it, census E02 rejects it"),
    ("Z3_zero_width_space_inside_cited_id",
     reg(row("S983", "https://e.example/983")),
     {"ok.md": f"Cites S{ZWSP}984 which is registered nowhere.\n"},
     None,
     "zero-width space inside the cited id"),
    ("Z4_url_match_substring_whole_body",
     reg(row("S985", "https://e.example/985")),
     {"ok.md": "Cites S985 (https://e.example/9852).\n"},
     reg(row("S985", "https://e.example/985")),
     "the sibling owns S985 with URL U; the lane cites U2 which merely contains U -> url-match fires"),
    ("Z5_id_inside_url_in_knowledge_over_reports",
     reg(row("S986", "https://e.example/986")),
     {"ok.md": "Cites S986. Mirror https://e.example/p/S987 here.\n"},
     None,
     "an id inside a URL is counted as a citation -> a dangling id that is not a citation"),
]

# the top findings repeated at a revision
REVISION_CASES = [
    ("REV_Y1_indented_paths_heading_ends_section",
     "# Sources\n\n## Registry\n\n" + HDR + row("S988", "https://e.example/988") +
     "  ## Paths\n\n" + row("S989", "https://e.example/989"),
     {"ok.md": "Cites S988 and S989.\n"},
     None,
     "rows after an indented `## Paths` register in the resolver but are outside the Registry for the census"),
    ("REV_R3_html_pre_block_row",
     reg(row("S990", "https://e.example/990") + "<pre>\n" + row("S991", "https://e.example/991") + "</pre>\n"),
     {"ok.md": "Cites S990 and S991.\n"},
     None,
     "a row inside a <pre> block registers the id"),
]


def report(name, note, cen, res):
    print("=" * 78)
    print("CASE", name, "|", note)
    print("  census rows:", cen["rows"], "validate exit:", cen["validate_exit"])
    for f in cen["findings"]:
        print("   !", f)
    print("  resolver exit:", res["exit"])
    for line in res["out"].splitlines():
        print("   |", line)


def main() -> int:
    os.makedirs(WORK, exist_ok=True)
    results = []
    for name, registry, knowledge, sibling, note in CASES:
        fleet, lane = build(name, registry, knowledge, sibling)
        head = commit(lane)
        cen = run_census(lane)
        wt = run_tool(TOOL, lane, fleet)
        rv = run_tool(TOOL, lane, fleet, head)
        report(name, note, cen, wt)
        if rv["out"] != wt["out"] or rv["exit"] != wt["exit"]:
            print("  REVISION DIFFERS: exit", rv["exit"])
            for line in rv["out"].splitlines():
                print("   rv |", line)
        results.append({"case": name, "note": note, "census": cen, "worktree": wt, "revision": rv})
    for name, registry, knowledge, sibling, note in REVISION_CASES:
        fleet, lane = build(name, registry, knowledge, sibling)
        head = commit(lane)
        cen = run_census(lane)
        rv = run_tool(TOOL, lane, fleet, head)
        print("=" * 78)
        print("CASE", name, "|", note)
        print("  census rows:", cen["rows"], "validate exit:", cen["validate_exit"])
        for f in cen["findings"]:
            print("   !", f)
        print("  resolver(revision) exit:", rv["exit"])
        for line in rv["out"].splitlines():
            print("   |", line)
        results.append({"case": name, "note": note, "census": cen, "revision": rv})
    with open(os.path.join(SEAT, "results7.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
