#!/usr/bin/env python3
"""SentinelResolver probe 12: cross-lane knowledge symlink; registry-as-knowledge symlink; FIFO via link chain."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kake-r59/SentinelResolver"
TOOL = os.path.join(SCRATCH, "id_resolver_base.py")
WORK = os.path.join(SCRATCH, "work12")
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


def run(root, fleet=None, revision=None, timeout=15):
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


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)

    # AA: knowledge symlink pointing at a SIBLING lane's knowledge dir
    base = os.path.join(WORK, "crosslane")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    sib = os.path.join(fleet, "alpha-shokunin")
    put(sib, "corpus/knowledge/leak.md", "Cites S2300.\n")
    put(sib, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    os.symlink("../../../alpha-shokunin/corpus/knowledge", os.path.join(lp, "corpus", "knowledge", "sib"))
    rc, text = run(lp, fleet)
    report("AA knowledge symlink into a sibling lane (worktree)", rc, text,
           "S2300 lives in another lane; the containment check must keep it out")

    # AB: knowledge symlink pointing at the lane's own registry
    base = os.path.join(WORK, "regasknow")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S2400 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    os.symlink("../SOURCES.md", os.path.join(lp, "corpus", "knowledge", "reg.md"))
    rc, text = run(lp, fleet)
    report("AB knowledge symlink to the lane's own registry (worktree)", rc, text,
           "the registry's own ids become 'citations' of the registry file")

    # AC: FIFO reached through an in-lane symlink
    base = os.path.join(WORK, "fifo")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    os.mkfifo(os.path.join(lp, "corpus", "pipe"))
    os.symlink("../pipe", os.path.join(lp, "corpus", "knowledge", "pipe.md"))
    rc, text = run(lp, fleet, timeout=12)
    report("AC in-lane FIFO reached through a knowledge symlink", rc, text)

    # AD: does the base walk a symlinked knowledge DIR that points into the fleet's other lane?
    base = os.path.join(WORK, "crosslane2")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    sib = os.path.join(fleet, "alpha-shokunin")
    put(sib, "corpus/knowledge/leak.md", "Cites S2400.\n")
    os.symlink("../../../alpha-shokunin/corpus/knowledge", os.path.join(lp, "corpus", "knowledge", "sib"))
    rc, text = run(lp, fleet)
    report("AD same as AA (repeat, id differs)", rc, text)


if __name__ == "__main__":
    main()
