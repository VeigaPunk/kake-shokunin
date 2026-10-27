#!/usr/bin/env python3
"""SentinelResolver probe 11: --root symlink vs a K14-style toplevel check; sibling exclusion by realpath."""
from __future__ import annotations

import os
import shutil
import subprocess

SCRATCH = "/fast/scratch/hyaku/kake-r59/SentinelResolver"
WORK = os.path.join(SCRATCH, "work11")
HDR = "| id | name | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"


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


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)
    base = os.path.join(WORK, "rootlink")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    commit_all(lp)
    alias = os.path.join(base, "alias")
    os.symlink(lp, alias)
    p = subprocess.run(["git", "-C", alias, "rev-parse", "--show-toplevel"], capture_output=True)
    top = p.stdout.decode().strip()
    print("### --root given as a symlink to a repository toplevel")
    print(f"  --root                 = {alias}")
    print(f"  git rev-parse --show-toplevel = {top}")
    print(f"  os.path.realpath(--root)      = {os.path.realpath(alias)}")
    print(f"  a K14-style check (realpath(root) == toplevel) would ACCEPT this root: "
          f"{os.path.realpath(top) == os.path.realpath(alias)}")
    print("  -> the tool then measures the pointed-to lane; the fleet's real lane is then excluded")
    print("     from the sibling list by the realpath comparison in sibling_dirs()")
    print()

    # sibling exclusion: fleet sibling that is a symlink to the lane itself
    fleet2 = os.path.join(base, "fleet2")
    lp2 = os.path.join(fleet2, "kake-shokunin")
    put(lp2, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp2, "corpus/knowledge/ok.md", "Cites S100 and S2200.\n")
    other = os.path.join(fleet2, "alpha-shokunin")
    os.makedirs(other, exist_ok=True)
    put(other, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S2200 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    os.symlink(lp2, os.path.join(fleet2, "beta-shokunin"))
    p = subprocess.run([sys.executable if False else "python3", "-B",
                        "/fast/scratch/hyaku/kake-r59/SentinelResolver/id_resolver_base.py",
                        "--root", lp2, "--fleet", fleet2], capture_output=True)
    print("### fleet entry 'beta-shokunin' is a symlink to the lane itself")
    print("  exit:", p.returncode)
    for line in p.stdout.decode().splitlines():
        print("   |", line)
    print()


if __name__ == "__main__":
    import sys
    main()
