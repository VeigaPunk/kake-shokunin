#!/usr/bin/env python3
"""MutC2Gate — probe: for each surviving mutant, does a proposed counter case see it?

Builds a small fixture, runs the GREEN tool and the mutant tool on it, and prints the two
outputs. A proposed case is only worth proposing when the outputs DIFFER.
"""
from __future__ import annotations

import os
import subprocess
import tempfile

S = "/fast/scratch/hyaku/kake-r59/MutC2Gate"
FIX = os.path.join(S, "fix")
GREEN = "fd8c7845b94f8a3d7ea8b815d7b70ed658604a03"

MUTANTS = {
    "H05": "registry containment compares only the path prefix (no separator)",
    "H06": "knowledge containment compares only the path prefix (no separator)",
    "H08": "URL_RE no longer stops at a backtick",
    "H13": "the working-tree knowledge walk accepts any file extension",
    "H15": "the fleet root defaults to the lane itself instead of its parent",
    "H20": "the fence machine accepts a backtick fence whose info string holds a backtick",
    "G14": "sibling owner list no longer sorted",
    "G25": "symlink resolution: a link that leaves the tree is followed anyway",
    "H18": "the symlink target is resolved without the tree-containment check",
}

COMMIT = {}
for fname in ("green_mutants.json", "green_mutants2.json"):
    import json
    for r in json.load(open(os.path.join(S, fname)))["results"]:
        if r.get("id") in MUTANTS:
            COMMIT[r["id"]] = r["commit"]
print("commits:", {k: v[:10] for k, v in COMMIT.items()})


def tool_at(rev):
    p = subprocess.run(["git", "-C", FIX, "show", rev + ":scripts/id_resolver.py"], capture_output=True)
    path = os.path.join(S, "probe_tool.py")
    with open(path, "wb") as fh:
        fh.write(p.stdout)
    return path


def run(tool, argv, cwd=None):
    r = subprocess.run(["python3", "-B", tool] + argv, capture_output=True, cwd=cwd)
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


REG = ("# Sources\n\n## Registry\n\n"
       "| id | name | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
       "| S001 | fixture — https://example.invalid/S001 | docs | A | s | a | t | mined | 2026-10-26 | 90d | corpus/knowledge/ok.md |\n")


def fixture(root, kind):
    lane = os.path.join(root, "fleet", "kake-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"), REG)
    if kind == "url_backtick":
        write(os.path.join(lane, "corpus/SOURCES.md"), REG.replace(
            "https://example.invalid/S001", "https://example.invalid/S001`"))
        write(os.path.join(lane, "corpus/knowledge/ok.md"), "Cites S001 and S002.\n")
    elif kind == "extension":
        write(os.path.join(lane, "corpus/knowledge/ok.md"), "Cites S001.\n")
        write(os.path.join(lane, "corpus/knowledge/notes.json"), "Cites S002.\n")
    elif kind == "no_fleet":
        write(os.path.join(lane, "corpus/knowledge/ok.md"), "Cites S001 and S003.\n")
    elif kind == "fence_info":
        write(os.path.join(lane, "corpus/SOURCES.md"), REG + "```a`b\n| S002 | fixture |\n```\n")
        write(os.path.join(lane, "corpus/knowledge/ok.md"), "Cites S001 and S002.\n")
    elif kind == "two_siblings":
        write(os.path.join(lane, "corpus/knowledge/ok.md"), "Cites S001 and S004.\n")
    elif kind == "prefix_sibling":
        write(os.path.join(lane, "corpus/knowledge/ok.md"), "Cites S001 and S005.\n")
    return lane


def build(kind):
    root = tempfile.mkdtemp(dir=os.path.join(S, "work7"))
    lane = fixture(root, kind)
    fleet = os.path.join(root, "fleet")
    if kind == "two_siblings":
        for name in ("zeta-shokunin", "alpha-shokunin"):
            write(os.path.join(fleet, name, "corpus/SOURCES.md"), REG.replace(
                "S001 | fixture — https://example.invalid/S001",
                "S004 | fixture — https://example.invalid/S004"))
    if kind == "prefix_sibling":
        # a knowledge dir whose realpath shares the lane's path prefix but is outside it
        outside = os.path.join(root, "fleet", "kake-shokunin-evil")
        write(os.path.join(outside, "corpus/knowledge/leak.md"), "Cites S005.\n")
        write(os.path.join(lane, "corpus/knowledge/ok.md"), "Cites S001 and S005.\n")
    return root, lane, fleet


GREEN_TOOL = tool_at(GREEN)
for kind, argv_fn in [
    ("url_backtick", lambda lane, fleet: ["--root", lane, "--fleet", fleet]),
    ("extension", lambda lane, fleet: ["--root", lane, "--fleet", fleet]),
    ("no_fleet", lambda lane, fleet: ["--root", lane]),
    ("fence_info", lambda lane, fleet: ["--root", lane, "--fleet", fleet]),
    ("two_siblings", lambda lane, fleet: ["--root", lane, "--fleet", fleet]),
    ("prefix_sibling", lambda lane, fleet: ["--root", lane, "--fleet", fleet]),
]:
    root, lane, fleet = build(kind)
    gc, gout = run(GREEN_TOOL, argv_fn(lane, fleet))
    print("=" * 70)
    print("CASE", kind, "| green exit", gc)
    print("  green:", " / ".join(gout.strip().splitlines()) or "(no output)")
    for mid in ("H05", "H06", "H08", "H13", "H15", "H20", "G14", "G25", "H18"):
        if mid not in COMMIT:
            continue
        tool = tool_at(COMMIT[mid])
        mc, mout = run(tool, argv_fn(lane, fleet))
        differs = (mc, mout) != (gc, gout)
        if differs:
            print(f"  {mid} DIFFERS exit={mc}: " + " / ".join(mout.strip().splitlines()[:4]))
