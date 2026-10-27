#!/usr/bin/env python3
"""SentinelResolver round-59 w1 probe 2: TOCTOU, chains, sibling symlinks, revision-mode symlink registry."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import threading
import time

SCRATCH = "/fast/scratch/hyaku/kake-r59/SentinelResolver"
TOOL = os.path.join(SCRATCH, "id_resolver_base.py")
WORK = os.path.join(SCRATCH, "work2")
HDR = "| id | name | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"


def registry(rows):
    body = "# Sources\n\n## Registry\n\n" + HDR
    for sid, url in rows:
        body += f"| {sid} | fixture — {url} | docs | A | scope | anchor | teaches | mined | 2026-10-26 | 90d | corpus/knowledge/ok.md |\n"
    return body


def run(argv, timeout=25):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"] = "C.UTF-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        p = subprocess.run(argv, capture_output=True, env=env, timeout=timeout)
        return p.returncode, (p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")).strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT", ""


def tool(root, fleet=None, revision=None, timeout=25):
    argv = [sys.executable, "-B", TOOL, "--root", root]
    if fleet:
        argv += ["--fleet", fleet]
    if revision:
        argv += ["--revision", revision]
    return run(argv, timeout=timeout)


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

    # ---- V12: registry is a git symlink at a revision
    base = fresh("v12_registry_git_symlink")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    os.makedirs(os.path.join(lp, "corpus"), exist_ok=True)
    os.symlink("elsewhere/SOURCES.md", os.path.join(lp, "corpus", "SOURCES.md"))
    put(lp, "corpus/elsewhere/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    head = commit_all(lp)
    rc, text = tool(lp, fleet, head)
    report("V12 registry is a committed symlink, read at --revision", rc, text,
           "git show returns the LINK TARGET STRING as the registry text")
    rc, text = tool(lp, fleet)
    report("V12b same fixture, worktree mode", rc, text)

    # ---- V13: symlink chain inside the tree
    base = fresh("v13_chain")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(lp, "corpus/real.md", "Cites S1100.\n")
    os.symlink("real.md", os.path.join(lp, "corpus", "knowledge", "hop1.md"))
    os.symlink("hop1.md", os.path.join(lp, "corpus", "knowledge", "hop2.md"))
    head = commit_all(lp)
    rc, text = tool(lp, fleet, head)
    report("V13 two-hop symlink chain inside the tree, at --revision", rc, text)
    rc, text = tool(lp, fleet)
    report("V13b same fixture, worktree mode", rc, text)

    # ---- V14: fleet sibling that is a symlink to another tree
    base = fresh("v14_sibling_symlink")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100 and S1200.\n")
    elsewhere = os.path.join(base, "elsewhere")
    put(elsewhere, "corpus/SOURCES.md", registry([("S1200", "https://example.invalid/1200")]))
    os.symlink(elsewhere, os.path.join(fleet, "beta-shokunin"))
    rc, text = tool(lp, fleet)
    report("V14 fleet sibling entry is a symlink to a tree outside the fleet", rc, text,
           "the sibling's registry is trusted as ownership evidence")

    # ---- V15: --root is a symlink to a sibling lane
    base = fresh("v15_root_symlink")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    other = os.path.join(fleet, "alpha-shokunin")
    put(other, "corpus/SOURCES.md", registry([("S1300", "https://example.invalid/1300")]))
    put(other, "corpus/knowledge/ok.md", "Cites S1300.\n")
    alias = os.path.join(base, "alias-shokunin")
    os.symlink(other, alias)
    rc, text = tool(alias, fleet)
    report("V15 --root is a symlink to another lane's tree", rc, text,
           "the tool measured a lane other than the one named")

    # ---- V16: duplicate citation through an in-lane symlink to another knowledge file
    base = fresh("v16_dup_citation")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(lp, "corpus/knowledge/copy.md", "Cites S100.\n")
    os.symlink("ok.md", os.path.join(lp, "corpus", "knowledge", "alias.md"))
    rc, text = tool(lp, fleet)
    report("V16 knowledge symlink to a sibling knowledge file (worktree)", rc, text,
           "the same id is counted under two paths")

    # ---- V17: TOCTOU race between the realpath containment check and the open
    base = fresh("v17_toctou")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(lp, "corpus/knowledge/victim.md", "Cites S100.\n")
    outside = os.path.join(base, "outside")
    put(outside, "outside.md", "Cites S1400.\n")
    link = os.path.join(lp, "corpus", "knowledge", "race.md")
    os.symlink(os.path.join(lp, "corpus", "knowledge", "victim.md"), link)
    stop = threading.Event()

    def flipper():
        inside = os.path.join(lp, "corpus", "knowledge", "victim.md")
        outside_target = os.path.join(outside, "outside.md")
        while not stop.is_set():
            for tgt in (inside, outside_target):
                tmp = link + ".tmp"
                try:
                    if os.path.lexists(tmp):
                        os.unlink(tmp)
                    os.symlink(tgt, tmp)
                    os.replace(tmp, link)
                except OSError:
                    pass
            time.sleep(0.0005)

    t = threading.Thread(target=flipper, daemon=True)
    t.start()
    leaks = 0
    runs = 60
    samples = []
    for _ in range(runs):
        rc, text = tool(lp, fleet, timeout=20)
        if "S1400" in text:
            leaks += 1
            if len(samples) < 2:
                samples.append(text.strip().splitlines()[-1])
    stop.set()
    t.join(timeout=2)
    print("### V17 TOCTOU: containment check vs open")
    print(f"  runs={runs} runs_whose_output_mentioned_the_outside_id_S1400={leaks}")
    for s in samples:
        print("  | " + s)
    print()

    # ---- V18: knowledge file that is a symlink to /dev/zero-like unbounded special file inside the lane
    base = fresh("v18_devspecial")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    os.symlink("/dev/zero", os.path.join(lp, "corpus", "knowledge", "zero.md"))
    rc, text = tool(lp, fleet, timeout=20)
    report("V18 knowledge symlink to /dev/zero (worktree)", rc, text,
           "an unbounded device read; content is outside the lane")

    # ---- V19: symlink target that escapes with '..' from a deep knowledge subdir
    base = fresh("v19_deep_escape")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/deep/inner/x.md", "Cites S100.\n")
    put(base, "outside/leak.md", "Cites S1500.\n")
    os.makedirs(os.path.join(lp, "corpus", "knowledge", "deep", "inner"), exist_ok=True)
    os.symlink("../../../../outside/leak.md", os.path.join(lp, "corpus", "knowledge", "deep", "inner", "esc.md"))
    rc, text = tool(lp, fleet)
    report("V19 '..' escape from a deep knowledge subdir (worktree)", rc, text)

    # ---- V20: symlink whose target string contains an id AND resolves in-tree
    base = fresh("v20_id_target_in_tree")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(lp, "corpus/S1600.md", "Cites S1600.\n")
    os.symlink("../S1600.md", os.path.join(lp, "corpus", "knowledge", "S1600.md"))
    head = commit_all(lp)
    rc, text = tool(lp, fleet, head)
    report("V20 in-tree link whose TARGET STRING is also an id, at --revision", rc, text,
           "the string 'S1600.md' is a body in base; the real file cites S1600 too")


if __name__ == "__main__":
    main()
