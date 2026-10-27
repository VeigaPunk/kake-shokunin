#!/usr/bin/env python3
"""MutC2Gate — refined probes for the survivors that need a sharper fixture."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile

S = "/fast/scratch/hyaku/kake-r59/MutC2Gate"
FIX = os.path.join(S, "fix")
GREEN = "fd8c7845b94f8a3d7ea8b815d7b70ed658604a03"
W = os.path.join(S, "work8")

COMMIT = {}
for fname in ("green_mutants.json", "green_mutants2.json"):
    for r in json.load(open(os.path.join(S, fname)))["results"]:
        if r.get("id"):
            COMMIT[r["id"]] = r.get("commit")


def tool_at(rev):
    p = subprocess.run(["git", "-C", FIX, "show", rev + ":scripts/id_resolver.py"], capture_output=True)
    path = os.path.join(S, "probe_tool2.py")
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


def git_ok(argv):
    p = subprocess.run(argv, capture_output=True)
    assert p.returncode == 0, p.stderr.decode()
    return p.stdout.decode()


# ---- case A: fleet-root default (H15): no --fleet, a sibling lane owns the id
def case_fleet_default():
    root = tempfile.mkdtemp(dir=W)
    fleet = os.path.join(root, "fleet")
    lane = os.path.join(fleet, "kake-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"), REG)
    write(os.path.join(lane, "corpus/knowledge/ok.md"), "Cites S001 and S009.\n")
    write(os.path.join(fleet, "alpha-shokunin", "corpus/SOURCES.md"), REG.replace(
        "S001 | fixture — https://example.invalid/S001", "S009 | fixture — https://example.invalid/S009"))
    return root, lane, fleet, ["--root", lane]


# ---- case B: URL backtick (H08): a sibling registry URL ends in a backtick
def case_url_backtick():
    root = tempfile.mkdtemp(dir=W)
    fleet = os.path.join(root, "fleet")
    lane = os.path.join(fleet, "kake-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"), REG)
    write(os.path.join(lane, "corpus/knowledge/ok.md"), "Cites S001 and S010 — see https://example.invalid/S010`\n")
    write(os.path.join(fleet, "alpha-shokunin", "corpus/SOURCES.md"), REG.replace(
        "S001 | fixture — https://example.invalid/S001", "S010 | fixture — https://example.invalid/S010`"))
    return root, lane, fleet, ["--root", lane, "--fleet", fleet]


# ---- case C: prefix containment (H05/H06): a symlink to a sibling path that shares the prefix
def case_prefix_containment():
    root = tempfile.mkdtemp(dir=W)
    fleet = os.path.join(root, "fleet")
    lane = os.path.join(fleet, "kake-shokunin")
    evil = os.path.join(fleet, "kake-shokunin-evil")
    write(os.path.join(lane, "corpus/SOURCES.md"), REG)
    write(os.path.join(lane, "corpus/knowledge/ok.md"), "Cites S001.\\n")
    write(os.path.join(evil, "corpus/knowledge/leak.md"), "Cites S011.\\n")
    os.symlink(os.path.join(evil, "corpus", "knowledge", "leak.md"),
               os.path.join(lane, "corpus", "knowledge", "leak.md"))
    return root, lane, fleet, ["--root", lane, "--fleet", fleet]


# ---- case D: a committed symlink leaving the tree (G25/H18)
def case_symlink_leaving_tree():
    root = tempfile.mkdtemp(dir=W)
    fleet = os.path.join(root, "fleet")
    lane = os.path.join(fleet, "kake-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"), REG)
    write(os.path.join(lane, "corpus/knowledge/ok.md"), "Cites S001.\\n")
    os.symlink("../../outside.md", os.path.join(lane, "corpus", "knowledge", "linked.md"))
    outside = os.path.join(lane, "outside.md")
    with open(outside, "w", encoding="utf-8") as fh:
        fh.write("Cites S012.\\n")
    git_ok(["git", "-C", lane, "init", "-q"])
    git_ok(["git", "-C", lane, "add", "-A"])
    git_ok(["git", "-C", lane, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
            "-c", "commit.gpgsign=false", "commit", "-q", "-m", "fixture"])
    rev = git_ok(["git", "-C", lane, "rev-parse", "HEAD"]).strip()
    return root, lane, fleet, ["--root", lane, "--fleet", fleet, "--revision", rev]


# ---- case E: two sibling owners, order (G14)
def case_two_siblings_order():
    root = tempfile.mkdtemp(dir=W)
    fleet = os.path.join(root, "fleet")
    lane = os.path.join(fleet, "kake-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"), REG)
    write(os.path.join(lane, "corpus/knowledge/ok.md"), "Cites S001 and S013.\n")
    for name in ("zeta-shokunin", "alpha-shokunin"):
        write(os.path.join(fleet, name, "corpus/SOURCES.md"), REG.replace(
            "S001 | fixture — https://example.invalid/S001", "S013 | fixture — https://example.invalid/S013"))
    return root, lane, fleet, ["--root", lane, "--fleet", fleet]


GREEN_TOOL = tool_at(GREEN)
for name, fn, watch in [
    ("fleet_default", case_fleet_default, ["H15"]),
    ("url_backtick", case_url_backtick, ["H08"]),
    ("prefix_containment", case_prefix_containment, ["H05", "H06"]),
    ("symlink_leaving_tree", case_symlink_leaving_tree, ["G25", "H18"]),
    ("two_siblings_order", case_two_siblings_order, ["G14"]),
]:
    root, lane, fleet, argv = fn()
    gc, gout = run(GREEN_TOOL, argv)
    print("=" * 72)
    print("CASE", name, "| green exit", gc)
    print("  green:", " / ".join(gout.strip().splitlines()) or "(no output)")
    for mid in watch:
        if mid not in COMMIT or not COMMIT[mid]:
            continue
        tool = tool_at(COMMIT[mid])
        mc, mout = run(tool, argv)
        differs = (mc, mout) != (gc, gout)
        print(f"  {mid} {'DIFFERS' if differs else 'identical'} exit={mc}: "
              + " / ".join(mout.strip().splitlines()[:3]))
