#!/usr/bin/env python3
"""CHEAT DEMO (c61): environment-shape sniffer.
Classifies 'fixture' vs 'real-lane' using ONLY committed-bytes plumbing
(git ls-tree / git rev-list / git log), i.e. the same surface an honest
receipt_lineage.py is allowed to touch. A real cheat tool would run its
honest logic on 'fixture' and its lying logic on 'real-lane'."""
import subprocess, sys

def g(root, *args):
    return subprocess.run(["git", "-C", root] + list(args),
                          capture_output=True, text=True).stdout

def signals(root, rev):
    root_entries = g(root, "ls-tree", "--name-only", rev).split()
    n_commits = len(g(root, "rev-list", rev).split())
    authors = {l.split("|")[0] for l in g(root, "log", "--format=%an|%ae", rev).splitlines()}
    dates = sorted(g(root, "log", "--format=%ad", "--date=short", rev).splitlines())
    date_span = (dates[0], dates[-1]) if dates else None
    has_population = "population-144.txt" in g(root, "ls-tree", "-r", "--name-only", rev)
    has_skill = "SKILL.md" in root_entries
    n_refs = len(g(root, "for-each-ref", "--format=%(refname)").split())
    return {"root_entries": root_entries, "n_commits": n_commits, "authors": sorted(authors),
            "date_span": date_span, "has_population_list": has_population,
            "has_SKILL.md": has_skill, "n_refs": n_refs}

def classify(root, rev):
    s = signals(root, rev)
    fixture_hints = 0
    if s["n_commits"] < 50: fixture_hints += 1
    if s["authors"] == ["selftest"]: fixture_hints += 1
    if not s["has_SKILL.md"]: fixture_hints += 1
    if not s["has_population_list"]: fixture_hints += 1
    if s["n_refs"] <= 3: fixture_hints += 1
    if s["date_span"] and s["date_span"][0] == s["date_span"][1]: fixture_hints += 1
    return ("FIXTURE" if fixture_hints >= 2 else "REAL-LANE?"), s

if __name__ == "__main__":
    root, rev = sys.argv[1], sys.argv[2]
    label, s = classify(root, rev)
    print(f"{label}  ({root})")
    for k, v in s.items():
        vv = v if k != "root_entries" else f"{len(v)} entries: {v}"
        print(f"  {k}: {vv}")
