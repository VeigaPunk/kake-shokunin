#!/usr/bin/env python3
"""SentinelResolver probe 7: prototype a naive revision-mode symlink fix and show what it reads."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kake-r59/SentinelResolver"
WORK = os.path.join(SCRATCH, "work7")


def put(base, rel, text):
    p = os.path.join(base, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def git(path, *args):
    return subprocess.run(["git", "-C", path, *args], capture_output=True)


def commit_all(path, msg="fixture"):
    git(path, "init", "-q")
    git(path, "add", "-A")
    r = git(path, "-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false",
            "commit", "-q", "-m", msg)
    assert r.returncode == 0, r.stderr
    return git(path, "rev-parse", "HEAD").stdout.decode().strip()


def fresh(name):
    root = os.path.join(WORK, name)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    return root


def naive_resolve(root, rev, rel):
    """A naive 'fix': read the link blob, then read the target from the WORKING TREE by path."""
    target = subprocess.run(["git", "-C", root, "show", f"{rev}:{rel}"], capture_output=True).stdout.decode()
    p = os.path.join(root, os.path.dirname(rel), target)
    if os.path.isfile(p):
        return open(p, "rb").read().decode("utf-8", "replace")
    return ""


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)
    base = fresh("naive")
    lp = os.path.join(base, "lane")
    put(lp, "corpus/SOURCES.md", "# Sources\n\n## Registry\n\n| id | name | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    # an in-tree link whose target exists only in the working tree (not committed)
    put(lp, "corpus/notes.md", "Cites S3000.\n")
    os.symlink("../notes.md", os.path.join(lp, "corpus", "knowledge", "linked.md"))
    # a link to a file OUTSIDE the tree
    put(base, "secret.md", "SECRET-OUTSIDE-THE-TREE\n")
    os.symlink(os.path.join(base, "secret.md"), os.path.join(lp, "corpus", "knowledge", "abs.md"))
    rev = commit_all(lp)
    print("### naive revision-mode resolution (reads the target from the working tree)")
    print("  linked.md ->", repr(naive_resolve(lp, rev, "corpus/knowledge/linked.md")))
    print("  abs.md    ->", repr(naive_resolve(lp, rev, "corpus/knowledge/abs.md")))
    print("  (an absolute or escaping target is read straight off the filesystem)")
    print()

    # cycle in the committed tree: a.md -> b.md -> a.md
    base = fresh("cycle_rev")
    lp = os.path.join(base, "lane")
    put(lp, "corpus/SOURCES.md", "# Sources\n\n## Registry\n\n| id | name | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    os.symlink("b.md", os.path.join(lp, "corpus", "knowledge", "a.md"))
    os.symlink("a.md", os.path.join(lp, "corpus", "knowledge", "b.md"))
    rev = commit_all(lp)
    print("### committed symlink cycle a.md -> b.md -> a.md")
    seen = set()
    cur = "corpus/knowledge/a.md"
    hops = 0
    while hops < 50:
        hops += 1
        if cur in seen:
            print(f"  cycle detected after {hops} hops at {cur}")
            break
        seen.add(cur)
        nxt = subprocess.run(["git", "-C", lp, "show", f"{rev}:{cur}"], capture_output=True).stdout.decode()
        print(f"  hop {hops}: {cur} -> {nxt!r}")
        cur = os.path.join(os.path.dirname(cur), nxt)
    else:
        print("  no cycle detected within 50 hops")
    print("  (a resolver without a hop limit or visited set loops here)")
    print()


if __name__ == "__main__":
    main()
