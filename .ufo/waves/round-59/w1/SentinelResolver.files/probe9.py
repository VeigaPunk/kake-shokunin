#!/usr/bin/env python3
"""SentinelResolver probe 9: corrected in-tree chain, dangling-link blast radius, revision in-tree registry."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kake-r59/SentinelResolver"
TOOL = os.path.join(SCRATCH, "id_resolver_base.py")
WORK = os.path.join(SCRATCH, "work9")
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
    r = git(path, "rev-parse", "--show-toplevel")
    assert r.returncode == 0 and os.path.realpath(r.stdout.decode().strip()) == os.path.realpath(path), "toplevel mismatch"
    git(path, "add", "-A")
    r = git(path, "-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false",
            "commit", "-q", "-m", msg)
    assert r.returncode == 0, r.stderr
    return git(path, "rev-parse", "HEAD").stdout.decode().strip()


def run(root, fleet=None, revision=None, timeout=25):
    argv = [sys.executable, "-B", TOOL, "--root", root]
    if fleet:
        argv += ["--fleet", fleet]
    if revision:
        argv += ["--revision", revision]
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"] = "C.UTF-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        p = subprocess.run(argv, capture_output=True, env=env, timeout=timeout)
        return p.returncode, (p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")).strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT", ""


def report(tag, rc, out, note=""):
    print(f"### {tag}\n  exit={rc}")
    for line in out.splitlines():
        print("  | " + line)
    if note:
        print("  note: " + note)
    print()


def fresh(name):
    root = os.path.join(WORK, name)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    return root


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)

    # Y1: corrected two-hop in-tree chain (target is a sibling file in corpus/knowledge)
    base = fresh("y1_chain")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(lp, "corpus/knowledge/real.md", "Cites S1700.\n")
    os.symlink("real.md", os.path.join(lp, "corpus", "knowledge", "hop1.md"))
    os.symlink("hop1.md", os.path.join(lp, "corpus", "knowledge", "hop2.md"))
    head = commit_all(lp)
    rc, text = run(lp, fleet, head)
    report("Y1 two-hop in-tree chain, at --revision", rc, text,
           "S1700 lives in corpus/knowledge/real.md; a green run means the chain was not resolved")
    rc, text = run(lp, fleet)
    report("Y1b same fixture, worktree mode", rc, text)

    # Y2: ONE dangling symlink inside corpus/knowledge — blast radius
    base = fresh("y2_dangling")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100 and S1800.\n")
    os.symlink("no-such-file.md", os.path.join(lp, "corpus", "knowledge", "dangling.md"))
    rc, text = run(lp, fleet)
    report("Y2 one dangling symlink inside corpus/knowledge (worktree)", rc, text,
           "the whole measurement dies (exit 2) instead of skipping the broken link")

    # Y3: revision-mode registry symlink resolving IN-TREE
    base = fresh("y3_rev_registry_intree")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(lp, "corpus/knowledge/reg.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    os.makedirs(os.path.join(lp, "corpus"), exist_ok=True)
    os.symlink("knowledge/reg.md", os.path.join(lp, "corpus", "SOURCES.md"))
    head = commit_all(lp)
    rc, text = run(lp, fleet, head)
    report("Y3 revision-mode registry symlink resolving IN-TREE", rc, text,
           "the target string 'knowledge/reg.md' was parsed as the registry; every citation dangles")

    # Y4: revision-mode registry symlink pointing OUT of the tree, target string forged as a table
    base = fresh("y4_rev_registry_out")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/knowledge/ok.md", "Cites S100 and S1900.\n")
    os.makedirs(os.path.join(lp, "corpus"), exist_ok=True)
    forged = "## Registry\n\n" + HDR + "| S100 | forged | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n| S1900 | forged | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n"
    os.symlink(forged, os.path.join(lp, "corpus", "SOURCES.md"))
    head = commit_all(lp)
    rc, text = run(lp, fleet, head)
    report("Y4 revision-mode registry symlink whose TARGET STRING is a forged table", rc, text,
           "the lane registry holds no rows at all; green means the link target string was parsed as the registry")

    # Y5: worktree registry symlink to a file inside the lane (must stay readable)
    base = fresh("y5_intree_registry_worktree")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(lp, "corpus/knowledge/reg.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    os.makedirs(os.path.join(lp, "corpus"), exist_ok=True)
    os.symlink("knowledge/reg.md", os.path.join(lp, "corpus", "SOURCES.md"))
    rc, text = run(lp, fleet)
    report("Y5 worktree registry symlink resolving IN-TREE", rc, text,
           "an in-lane registry symlink must keep working (over-refusal is also a defect)")


if __name__ == "__main__":
    main()
