#!/usr/bin/env python3
"""SentinelResolver probe 4: symlink-target-as-content attacks at --revision (false green / fabricated citation)."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kake-r59/SentinelResolver"
TOOL = os.path.join(SCRATCH, "id_resolver_base.py")
WORK = os.path.join(SCRATCH, "work4")
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

    # ---- W1: registry is a symlink whose TARGET STRING is a forged registry table
    base = fresh("w1_forged_registry")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/knowledge/ok.md", "Cites S100 and S1700.\n")
    os.makedirs(os.path.join(lp, "corpus"), exist_ok=True)
    forged = "## Registry\n\n" + HDR + "| S100 | forged | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n| S1700 | forged | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n"
    os.symlink(forged, os.path.join(lp, "corpus", "SOURCES.md"))
    head = commit_all(lp)
    print("### W1 registry symlink whose target string is a forged registry, at --revision")
    print("  committed blob mode:", git(lp, "ls-tree", "-r", head, "corpus/SOURCES.md").stdout.decode().strip())
    rc, text = run(lp, fleet, head)
    report("W1 forged registry through a symlink target, at --revision", rc, text,
           "the lane registry holds NO rows; a green run means the link target string was parsed as the registry")
    rc, text = run(lp, fleet)
    report("W1b same fixture, worktree mode", rc, text)

    # ---- W2: knowledge symlink whose target string is a body with ids
    base = fresh("w2_forged_body")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "# Sources\n\n## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    os.symlink("Cites S100 and S1800.", os.path.join(lp, "corpus", "knowledge", "note.md"))
    head = commit_all(lp)
    rc, text = run(lp, fleet, head)
    report("W2 knowledge symlink whose target string is a body, at --revision", rc, text,
           "the file has no content; S1800 is a fabricated citation")

    # ---- W3: symlink target string is a registry -> resolves an id that is nowhere in the lane
    base = fresh("w3_id_from_link")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "# Sources\n\n## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    os.symlink("S1900.md", os.path.join(lp, "corpus", "knowledge", "S1900.md"))
    head = commit_all(lp)
    rc, text = run(lp, fleet, head)
    report("W3 link target string is an id, at --revision", rc, text)

    # ---- W4: a symlinked knowledge DIR at a revision: git does not list its contents
    base = fresh("w4_linkdir_revision")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "# Sources\n\n## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(lp, "store/hidden.md", "Cites S2000.\n")
    os.symlink("../../store", os.path.join(lp, "corpus", "knowledge", "linked"))
    head = commit_all(lp)
    rc, text = run(lp, fleet, head)
    report("W4 symlinked knowledge dir at --revision", rc, text,
           "git stores a symlink as a blob; the dir's files are not in the tree at all")

    # ---- W5: git ls-tree mode column is what a fix needs (base uses --name-only)
    base = fresh("w5_ls_tree_modes")
    lp = os.path.join(base, "lane")
    put(lp, "corpus/SOURCES.md", "# Sources\n\n## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    os.symlink("ok.md", os.path.join(lp, "corpus", "knowledge", "alias.md"))
    head = commit_all(lp)
    print("### W5 ls-tree mode column for a symlink")
    print("  " + git(lp, "ls-tree", "-r", head).stdout.decode().strip().replace("\n", "\n  "))
    print()


if __name__ == "__main__":
    main()
