#!/usr/bin/env python3
"""SentinelResolver probe 6: in-tree vs escaping symlink resolution at --revision, sibling registry symlinks."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kake-r59/SentinelResolver"
TOOL = os.path.join(SCRATCH, "id_resolver_base.py")
WORK = os.path.join(SCRATCH, "work6")
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

    # X1: registry symlinked to an IN-TREE file at a revision
    base = fresh("x1_intree_registry")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(lp, "corpus/knowledge/registry.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    os.makedirs(os.path.join(lp, "corpus"), exist_ok=True)
    os.symlink("knowledge/registry.md", os.path.join(lp, "corpus", "SOURCES.md"))
    head = commit_all(lp)
    rc, text = run(lp, fleet, head)
    report("X1 registry symlinked IN-TREE at --revision", rc, text,
           "git show returns the link target string; the registry must be resolved in-tree, not parsed from the string")

    # X2: knowledge symlink escaping the tree at a revision
    base = fresh("x2_escape_revision")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(base, "outside/leak.md", "Cites S2100.\n")
    os.symlink("../../../outside/leak.md", os.path.join(lp, "corpus", "knowledge", "esc.md"))
    head = commit_all(lp)
    rc, text = run(lp, fleet, head)
    report("X2 knowledge symlink escaping the tree at --revision", rc, text,
           "S2100 must never appear; the target is outside the tree")
    rc, text = run(lp, fleet)
    report("X2b same fixture, worktree mode", rc, text)

    # X3: absolute symlink target at a revision
    base = fresh("x3_abs_revision")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(base, "outside/leak.md", "Cites S2200.\n")
    os.symlink(os.path.join(base, "outside", "leak.md"), os.path.join(lp, "corpus", "knowledge", "abs.md"))
    head = commit_all(lp)
    rc, text = run(lp, fleet, head)
    report("X3 absolute symlink target at --revision", rc, text)

    # X4: sibling lane's registry is itself a symlink out of the fleet
    base = fresh("x4_sibling_registry_symlink")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100 and S2300.\n")
    sib = os.path.join(fleet, "alpha-shokunin")
    put(base, "forged/SOURCES.md", "## Registry\n\n" + HDR + "| S2300 | forged | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    os.makedirs(os.path.join(sib, "corpus"))
    os.symlink(os.path.join(base, "forged", "SOURCES.md"), os.path.join(sib, "corpus", "SOURCES.md"))
    rc, text = run(lp, fleet)
    report("X4 sibling lane's registry is a symlink out of the fleet (worktree)", rc, text,
           "ownership is attributed to a registry that lives outside every lane")

    # X5: registry is a symlink to a sibling lane's registry, at a revision
    base = fresh("x5_registry_sibling_revision")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/knowledge/ok.md", "Cites S100 and S2400.\n")
    os.makedirs(os.path.join(lp, "corpus"), exist_ok=True)
    os.symlink("../../alpha-shokunin/corpus/SOURCES.md", os.path.join(lp, "corpus", "SOURCES.md"))
    head = commit_all(lp)
    rc, text = run(lp, fleet, head)
    report("X5 registry symlinked to a sibling lane at --revision", rc, text)

    # X6: knowledge file whose name is a symlink to a knowledge file -> duplicate citing path
    base = fresh("x6_dup")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(lp, "corpus/knowledge/other.md", "Cites S2500.\n")
    os.symlink("other.md", os.path.join(lp, "corpus", "knowledge", "alias.md"))
    head = commit_all(lp)
    rc, text = run(lp, fleet, head)
    report("X6 knowledge symlink at --revision (target string as body)", rc, text)

    # X7: does the base tool read a symlinked FILE in worktree mode (in-lane)?
    base = fresh("x7_symfile")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(lp, "corpus/knowledge/real.md", "Cites S2600.\n")
    os.symlink("real.md", os.path.join(lp, "corpus", "knowledge", "alias.md"))
    rc, text = run(lp, fleet)
    report("X7 in-lane symlinked knowledge FILE, worktree mode", rc, text,
           "the base reads the file through the link and attributes the citation to the link path")


if __name__ == "__main__":
    main()
