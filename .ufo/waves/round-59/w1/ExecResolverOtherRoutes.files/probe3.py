#!/usr/bin/env python3
"""Round-59 w1 seat ExecResolverOtherRoutes — probe batch 3 (sharp fixtures).

  U1  registry row with a fullwidth-digit id + knowledge citing the same id:
      the resolver resolves it (green) while the census id grammar (E02) rejects it.
  U2  registry row with a Cyrillic-lookalike S + knowledge citing the ASCII twin:
      the resolver sees nothing at all (green) while the census flags the row E02.
  U3  registry row with the ASCII id + knowledge citing the lookalike:
      the resolver is blind to the citation (green), the intended source stays unflagged.
  U4  url-match is a substring test: a sibling URL that is a prefix of the lane's
      URL still yields url-match=<sibling>.
  U5  a knowledge file quoting a registry row inside a fenced block: the id inside
      the fence is counted as a citation (documented rule, but asymmetric with the
      registry side, which skips fences).
  U6  live lane: the current tool against the real kake lane (read-only).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

SEAT = "/fast/scratch/hyaku/kake-r59/ExecResolverOtherRoutes"
WORK = os.path.join(SEAT, "work3")
TOOL = os.path.join(SEAT, "tool", "id_resolver.py")
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"

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
    return {"rows": rows, "census_exit": c.returncode, "validate_exit": v.returncode, "findings": findings}


CASES = []


def case(name, registry, knowledge, sibling=None, note=""):
    CASES.append(dict(name=name, registry=registry, knowledge=knowledge, sibling=sibling, note=note))


case("U1_fullwidth_digit_id_row_and_citation",
     reg(row("S９２８", "https://e.example/928")),
     {"ok.md": "Cites S９２８ and S929.\n"},
     note="registry row id uses fullwidth digits; the resolver resolves the fullwidth citation")

case("U1b_fullwidth_row_ascii_twin_cited",
     reg(row("S９２８", "https://e.example/928")),
     {"ok.md": "Cites S928.\n"},
     note="registry row id is fullwidth; the ASCII twin is cited and is unresolvable")

case("U2_cyrillic_S_registry_row_ascii_twin_cited",
     reg(row("Ѕ930", "https://e.example/930")),
     {"ok.md": "Cites S930.\n"},
     note="registry row id uses the Cyrillic lookalike S; the ASCII twin citation is invisible to the resolver")

case("U3_ascii_registry_row_lookalike_cited",
     reg(row("S931", "https://e.example/931")),
     {"ok.md": "Cites Ѕ931.\n"},
     note="ASCII row present; the lookalike citation is invisible -> an unregistered source is never flagged")

case("U4_url_match_is_a_substring_test",
     reg(row("S932", "https://e.example/932")),
     {"ok.md": "Cites S932 (https://e.example/9322).\n"},
     sibling=reg(row("S932", "https://e.example/932")),
     note="sibling URL is a prefix of the lane's URL; url-match still fires")

case("U5_knowledge_quotes_a_registry_row_in_a_fence",
     reg(row("S933", "https://e.example/933")),
     {"ok.md": "Cites S933.\n\n```\n| S934 | example row |\n```\n"},
     note="an id quoted inside a fenced block in a knowledge file is counted as a citation")


def main() -> int:
    os.makedirs(WORK, exist_ok=True)
    results = []
    for spec in CASES:
        fleet, lane = build(spec["name"], spec["registry"], spec["knowledge"], spec.get("sibling"))
        cen = run_census(lane)
        res = run_tool(TOOL, lane, fleet)
        results.append({"case": spec["name"], "note": spec["note"], "census": cen, "resolver": res})
        print("=" * 78)
        print("CASE", spec["name"], "|", spec["note"])
        print("  census rows:", cen["rows"], "validate exit:", cen["validate_exit"])
        for f in cen["findings"]:
            print("   !", f)
        print("  resolver exit:", res["exit"])
        for line in res["out"].splitlines():
            print("   |", line)
    # live lane (read-only)
    live = run_tool(TOOL, LANE, FLEET)
    print("=" * 78)
    print("LIVE LANE (current tool, read-only): exit", live["exit"])
    for line in live["out"].splitlines()[:12]:
        print("   |", line)
    results.append({"case": "LIVE_LANE", "resolver": live})
    with open(os.path.join(SEAT, "results3.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
