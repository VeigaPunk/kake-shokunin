#!/usr/bin/env python3
"""CHEAT DEMO (c61 cheat 4): structural fingerprint of L-fixtures across seeds.
Shows the fixture SKELETON (commit count, file count, span patterns, disclosure
presence) is seed-invariant even though ids/content are seeded -> a tool can
hard-code the 16 expected shapes and key on the skeleton."""
import subprocess, sys, json, re

def g(root, *args):
    return subprocess.run(["git", "-C", root] + list(args),
                          capture_output=True, text=True).stdout

def fingerprint(root, rev):
    commits = g(root, "rev-list", "--reverse", rev).split()
    files = [l for l in g(root, "ls-tree", "-r", "--name-only", rev).splitlines()
             if "/controls/" in l or "/control/" in l]
    SPAN = re.compile(r"(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|cases_passed|findings\s*=|scores_held|members\s*=)")
    spans = []
    for c in commits:
        for f in files:
            try:
                body = g(root, "show", f"{c}:{f}")
            except Exception:
                body = ""
            hits = sorted({m.group(1).lower().strip() for m in SPAN.finditer(body)})
            if hits: spans.append((f.split("/")[-1][:12], hits))
    return {"n_commits": len(commits), "n_files": len(files),
            "grammar_lines": spans,
            "skeleton": [len(commits), len(files),
                         ["pending" in json.dumps(spans)] ]}

for d in sys.argv[1:]:
    fp = fingerprint(d, "HEAD")
    print(d)
    print("  n_commits:", fp["n_commits"], "n_files:", fp["n_files"])
    print("  span hits:", fp["grammar_lines"])
    print("  SKELETON-KEY:", json.dumps(fp["skeleton"]))
