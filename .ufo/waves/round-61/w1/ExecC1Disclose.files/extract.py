#!/usr/bin/env python3
"""Independent extraction of receipt rewrite / pending_filled events at a revision.

Reimplements the contract's C1 predicates from git plumbing only (no worktree reads),
for the purpose of cross-checking the round-57 errata. Read-only.
"""
import json
import re
import subprocess
import sys

POP = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/controls/population-144.txt"
REV = "9f07731a873585e655a6518233ea39f5d9fb8204"
ROOT = "/fast/scratch/hyaku/kake-r61/ExecC1Disclose/lane"

RECEIPT_RE = re.compile(r"(?im)^\s*#\s*receipt\s*:|EXIT=|^VERDICT:")
SPAN_RE = re.compile(
    r"(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|"
    r"cases_passed|findings\s*=|scores_held|members\s*=)"
)


def git(*args, check=True):
    p = subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {p.stderr.strip()}")
    return p


def blob(commit, path):
    p = git("cat-file", "-e", f"{commit}:{path}", check=False)
    if p.returncode != 0:
        return None
    return git("cat-file", "blob", f"{commit}:{path}").stdout


def span(text):
    return "\n".join(l for l in text.splitlines() if SPAN_RE.search(l))


def first_add_commit(path):
    p = git("log", "--first-parent", "--diff-filter=A", "--format=%H", REV, "--", path)
    lines = [l for l in p.stdout.split() if l]
    return lines[-1] if lines else None


def walk(path):
    add = first_add_commit(path)
    if add is None:
        return [], None
    commits = git("rev-list", "--first-parent", "--reverse", f"{add}..{REV}").stdout.split()
    events = []
    prev = blob(add, path)
    first_version = prev
    for c in commits:
        cur = blob(c, path)
        if cur is None or prev is None or cur == prev:
            prev = cur
            continue
        if span(cur) != span(prev):
            events.append({"path": path, "commit": c, "kind": "rewrite"})
        prev = cur
    if first_version is not None and "pending" in span(first_version).lower():
        for c in commits:
            cur = blob(c, path)
            if cur is not None and "pending" not in span(cur).lower():
                events.append({"path": path, "commit": c, "kind": "pending_filled"})
                break
    return events, first_version


def main():
    paths = [l.strip() for l in open(POP) if l.strip()]
    all_events = []
    receipts = 0
    for path in paths:
        add = first_add_commit(path)
        if add is None:
            continue
        fv = blob(add, path)
        if fv is None or not RECEIPT_RE.search(fv):
            continue
        receipts += 1
        ev, _ = walk(path)
        all_events.extend(ev)
    print(json.dumps({"receipts": receipts, "population": len(paths),
                      "events": all_events}, indent=2))


if __name__ == "__main__":
    main()
