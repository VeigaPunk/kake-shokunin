#!/usr/bin/env python3
"""SentinelResolver probe 10: FIFO via symlink, sibling HEAD registry symlink, two-hop escape."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kake-r59/SentinelResolver"
TOOL = os.path.join(SCRATCH, "id_resolver_base.py")
WORK = os.path.join(SCRATCH, "work10")
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


def run(root, fleet=None, revision=None, timeout=20):
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

    # Z1: symlink to a FIFO that lives INSIDE the lane -> the containment check passes, the open blocks
    base = fresh("z1_fifo_inlane")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    os.mkfifo(os.path.join(lp, "corpus", "knowledge", "pipe"))
    os.symlink("pipe", os.path.join(lp, "corpus", "knowledge", "pipe.md"))
    rc, text = run(lp, fleet, timeout=15)
    report("Z1 symlink to an in-lane FIFO inside corpus/knowledge (worktree)", rc, text,
           "realpath containment passes; the open on a FIFO blocks forever")

    # Z2: a sibling lane whose HEAD registry is a committed symlink to a forged table
    base = fresh("z2_sibling_head_symlink")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100 and S2000.\n")
    sib = os.path.join(fleet, "alpha-shokunin")
    os.makedirs(os.path.join(sib, "corpus"), exist_ok=True)
    forged = "## Registry\n\n" + HDR + "| S2000 | forged | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n"
    os.symlink(forged, os.path.join(sib, "corpus", "SOURCES.md"))
    commit_all(sib)
    rc, text = run(lp, fleet)
    report("Z2 sibling lane's HEAD registry is a committed symlink to a forged table", rc, text,
           "ownership comes from a link target string that is not a registry at all")

    # Z3: two-hop escape in the working tree (in-lane link -> in-lane link -> outside file)
    base = fresh("z3_two_hop_escape")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(base, "outside/leak.md", "Cites S2100.\n")
    os.symlink("../../../../outside/leak.md", os.path.join(lp, "corpus", "knowledge", "hop1.md"))
    os.symlink("hop1.md", os.path.join(lp, "corpus", "knowledge", "hop2.md"))
    rc, text = run(lp, fleet)
    report("Z3 two-hop escape via in-lane links (worktree)", rc, text,
           "hop2 -> hop1 -> outside/leak.md; the file is outside the lane")


if __name__ == "__main__":
    main()
