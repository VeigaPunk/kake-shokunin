#!/usr/bin/env python3
"""SentinelResolver probe 3: followlinks cycle DoS, TOCTOU code path, committed symlink cycle at a revision."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import threading
import time

SCRATCH = "/fast/scratch/hyaku/kake-r59/SentinelResolver"
TOOL = os.path.join(SCRATCH, "id_resolver_base.py")
WORK = os.path.join(SCRATCH, "work3")


def put(base, rel, text):
    p = os.path.join(base, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def git(path, *args):
    return subprocess.run(["git", "-C", path, *args], capture_output=True)


def commit_all(path, msg="fixture"):
    git(path, "init", "-q")
    r = git(path, "rev-parse", "--show-toplevel")
    assert r.returncode == 0 and os.path.realpath(r.stdout.decode().strip()) == os.path.realpath(path), "toplevel mismatch"
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


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)

    # ---- A: what a naive followlinks=True walker does on a cycle (the shape K10's fix needs)
    base = fresh("cycle_walk")
    d = os.path.join(base, "tree")
    put(d, "sub/a.md", "Cites S1.\n")
    os.symlink("../sub", os.path.join(d, "sub", "loop"))
    os.symlink("..", os.path.join(d, "sub", "up"))
    t0 = time.time()
    try:
        n = 0
        for dirpath, dirnames, filenames in os.walk(d, followlinks=True):
            n += 1
            if n > 5000:
                print("### A naive os.walk(followlinks=True) on a symlink cycle")
                print(f"  visited {n} dirs in {time.time()-t0:.2f}s and did NOT terminate -> unbounded loop")
                break
            if time.time() - t0 > 8:
                print("### A naive os.walk(followlinks=True) on a symlink cycle")
                print(f"  visited {n} dirs in {time.time()-t0:.2f}s and did NOT terminate -> unbounded loop")
                break
        else:
            print("### A naive os.walk(followlinks=True) terminated after", n, "dirs")
    finally:
        pass
    print()

    # ---- B: the exact check-then-open pattern of knowledge_bodies, raced
    base = fresh("toctou_pattern")
    root = os.path.join(base, "lane")
    put(root, "corpus/knowledge/victim.md", "INSIDE\n")
    put(base, "outside.md", "OUTSIDE-SECRET\n")
    root_real = os.path.realpath(root)
    link = os.path.join(root, "corpus", "knowledge", "race.md")
    inside_t = os.path.join(root, "corpus", "knowledge", "victim.md")
    outside_t = os.path.join(base, "outside.md")
    os.symlink(inside_t, link)
    stop = threading.Event()

    def flipper():
        while not stop.is_set():
            for tgt in (inside_t, outside_t):
                tmp = link + ".tmp"
                try:
                    if os.path.lexists(tmp):
                        os.unlink(tmp)
                    os.symlink(tgt, tmp)
                    os.replace(tmp, link)
                except OSError:
                    pass

    t = threading.Thread(target=flipper, daemon=True)
    t.start()
    leaks = 0
    N = 4000
    for _ in range(N):
        # replicate knowledge_bodies' pattern verbatim
        real = os.path.realpath(link)
        if not (real == root_real or real.startswith(root_real + os.sep)):
            continue
        try:
            with open(link, "rb") as fh:
                data = fh.read()
        except OSError:
            continue
        if b"OUTSIDE-SECRET" in data:
            leaks += 1
    stop.set()
    t.join(timeout=2)
    print("### B check-then-open race (the tool's exact pattern)")
    print(f"  iterations={N} reads_that_succeeded_but_carried_outside_content={leaks}")
    print("  (the tool's containment check and its open() are two separate syscalls; the link can be swapped between them)")
    print()

    # ---- C: committed symlink cycle at a revision
    base = fresh("rev_cycle")
    lp = os.path.join(base, "fleet", "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "# Sources\n\n## Registry\n\n| id | name | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n| S100 | fixture | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    os.symlink("b.md", os.path.join(lp, "corpus", "knowledge", "a.md"))
    os.symlink("a.md", os.path.join(lp, "corpus", "knowledge", "b.md"))
    head = commit_all(lp)
    p = subprocess.run(["git", "-C", lp, "ls-tree", "-r", "-z", head], capture_output=True)
    print("### C committed symlink cycle at a revision")
    print("  ls-tree -r -z entries:")
    for chunk in p.stdout.split(b"\0"):
        if chunk:
            print("   |", chunk.decode())
    p2 = subprocess.run(["git", "-C", lp, "ls-tree", "-r", "-z", "--name-only", head], capture_output=True)
    print("  --name-only entries (what the base tool lists):")
    for chunk in p2.stdout.split(b"\0"):
        if chunk:
            print("   |", chunk.decode())
    p3 = subprocess.run(["git", "-C", lp, "show", f"{head}:corpus/knowledge/a.md"], capture_output=True)
    print("  git show a.md ->", repr(p3.stdout.decode()))
    print("  git ls-tree -r (long form) mode column:")
    p4 = subprocess.run(["git", "-C", lp, "ls-tree", "-r", head], capture_output=True)
    for line in p4.stdout.decode().splitlines():
        print("   |", line)
    print()


if __name__ == "__main__":
    main()
