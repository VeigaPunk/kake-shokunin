#!/usr/bin/env python3
"""SentinelResolver round-59 w1: base-behaviour probe of scripts/id_resolver.py symlink/path handling.

Read-only w.r.t. the lane: the tool is copied out of the lane; every fixture is built under scratch.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kake-r59/SentinelResolver"
TOOL = os.path.join(SCRATCH, "id_resolver_base.py")
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
WORK = os.path.join(SCRATCH, "work")

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
    r = git(path, "init", "-q")
    assert r.returncode == 0, r.stderr
    r = git(path, "rev-parse", "--show-toplevel")
    assert r.returncode == 0 and os.path.realpath(r.stdout.decode().strip()) == os.path.realpath(path), "toplevel mismatch"
    git(path, "add", "-A")
    r = git(path, "-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false",
            "commit", "-q", "-m", msg)
    assert r.returncode == 0, r.stderr
    r = git(path, "rev-parse", "HEAD")
    return r.stdout.decode().strip()


def fresh(name):
    root = os.path.join(WORK, name)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    return root


def fleet_for(name):
    base = fresh(name)
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    os.makedirs(lp)
    return base, fleet, lp


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
    out = []

    # ---------------------------------------------------------------- V1: in-lane symlinked dir (K10 shape)
    base, fleet, lp = fleet_for("v1_inlane_symlink_dir")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(lp, "notes_store/hidden.md", "Cites S200.\n")
    os.symlink("../../notes_store", os.path.join(lp, "corpus", "knowledge", "linked"))
    rc, text = tool(lp, fleet)
    report("V1 in-lane symlinked knowledge dir (worktree)", rc, text,
           "S200 is cited only through the symlink; a green run means the citation was dropped")

    # ---------------------------------------------------------------- V2: same at a revision (K11 shape)
    base, fleet, lp = fleet_for("v2_revision_symlink")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(lp, "corpus/notes.md", "Cites S300.\n")
    os.symlink("../notes.md", os.path.join(lp, "corpus", "knowledge", "linked.md"))
    os.symlink("F400-target.md", os.path.join(lp, "corpus", "knowledge", "odd.md"))
    head = commit_all(lp)
    rc, text = tool(lp, fleet, head)
    report("V2 committed symlink read at --revision (K11 shape)", rc, text,
           "expect: S300 read through the link; the link TARGET STRING must never become a body")
    rc, text = tool(lp, fleet)
    report("V2b same fixture, worktree mode", rc, text)

    # ---------------------------------------------------------------- V3: link target string that itself looks like an id
    base, fleet, lp = fleet_for("v3_target_string_id")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    os.symlink("S999.md", os.path.join(lp, "corpus", "knowledge", "evil.md"))
    head = commit_all(lp)
    rc, text = tool(lp, fleet, head)
    report("V3 dangling symlink whose target string is an id, at --revision", rc, text,
           "S999 does not exist; a DANGLING S999 line is a fabricated citation")
    rc, text = tool(lp, fleet)
    report("V3b same fixture, worktree mode", rc, text)

    # ---------------------------------------------------------------- V4: '..' escape in a link target
    base, fleet, lp = fleet_for("v4_dotdot_escape")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(base, "outside/leak.md", "Cites S500.\n")
    os.symlink("../../../outside", os.path.join(lp, "corpus", "knowledge", "escape"))
    rc, text = tool(lp, fleet)
    report("V4 '..' escape in symlink target (worktree)", rc, text,
           "S500 lives outside the lane; it must never be read")
    head = commit_all(lp)
    rc, text = tool(lp, fleet, head)
    report("V4b same fixture at --revision", rc, text)

    # ---------------------------------------------------------------- V5: absolute link target
    base, fleet, lp = fleet_for("v5_absolute_target")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(base, "outside/leak.md", "Cites S600.\n")
    os.symlink(os.path.join(base, "outside", "leak.md"), os.path.join(lp, "corpus", "knowledge", "abs.md"))
    rc, text = tool(lp, fleet)
    report("V5 absolute symlink target out of the lane (worktree)", rc, text)
    head = commit_all(lp)
    rc, text = tool(lp, fleet, head)
    report("V5b same fixture at --revision", rc, text)

    # ---------------------------------------------------------------- V6: symlinked corpus/knowledge itself
    base, fleet, lp = fleet_for("v6_symlinked_knowledge_dir")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    real = os.path.join(base, "elsewhere", "knowledge")
    put(real, "ok.md", "Cites S100.\n")
    put(real, "leak.md", "Cites S700.\n")
    os.makedirs(os.path.join(lp, "corpus"), exist_ok=True)
    os.symlink(real, os.path.join(lp, "corpus", "knowledge"))
    rc, text = tool(lp, fleet)
    report("V6 corpus/knowledge itself is a symlink outside the lane (worktree)", rc, text)
    head = commit_all(lp)
    rc, text = tool(lp, fleet, head)
    report("V6b same fixture at --revision", rc, text)

    # ---------------------------------------------------------------- V6c: symlinked corpus/ itself
    base, fleet, lp = fleet_for("v6c_symlinked_corpus")
    real_corpus = os.path.join(base, "elsewhere", "corpus")
    put(real_corpus, "SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(real_corpus, "knowledge/ok.md", "Cites S100.\n")
    os.symlink(real_corpus, os.path.join(lp, "corpus"))
    rc, text = tool(lp, fleet)
    report("V6c corpus/ itself is a symlink outside the lane (worktree)", rc, text)
    head = commit_all(lp)
    rc, text = tool(lp, fleet, head)
    report("V6c-b same fixture at --revision", rc, text)

    # ---------------------------------------------------------------- V7: registry symlinked to a sibling lane (K12 shape)
    base, fleet, lp = fleet_for("v7_registry_symlink_sibling")
    sib = os.path.join(fleet, "alpha-shokunin")
    put(sib, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100"), ("S800", "https://example.invalid/800")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100 and S800.\n")
    os.makedirs(os.path.join(lp, "corpus"), exist_ok=True)
    os.symlink("../../alpha-shokunin/corpus/SOURCES.md", os.path.join(lp, "corpus", "SOURCES.md"))
    rc, text = tool(lp, fleet)
    report("V7 registry symlinked to a sibling lane (worktree)", rc, text,
           "a green run means ids were resolved from another lane's registry")

    # ---------------------------------------------------------------- V7b: registry symlinked to an absolute path outside the lane
    base, fleet, lp = fleet_for("v7b_registry_symlink_abs")
    outside = os.path.join(base, "outside", "SOURCES.md")
    put(base, "outside/SOURCES.md", registry([("S100", "https://example.invalid/100"), ("S810", "https://example.invalid/810")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100 and S810.\n")
    os.makedirs(os.path.join(lp, "corpus"), exist_ok=True)
    os.symlink(outside, os.path.join(lp, "corpus", "SOURCES.md"))
    rc, text = tool(lp, fleet)
    report("V7b registry symlinked to an absolute path outside the lane (worktree)", rc, text)

    # ---------------------------------------------------------------- V7c: registry symlinked to a directory
    base, fleet, lp = fleet_for("v7c_registry_symlink_dir")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    os.makedirs(os.path.join(lp, "corpus"), exist_ok=True)
    os.symlink(os.path.join(lp, "corpus", "knowledge"), os.path.join(lp, "corpus", "SOURCES.md"))
    rc, text = tool(lp, fleet)
    report("V7c registry symlinked to a directory (worktree)", rc, text)

    # ---------------------------------------------------------------- V8: link cycle
    base, fleet, lp = fleet_for("v8_cycle")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    put(lp, "dirA/inner.md", "Cites S900.\n")
    os.symlink("../dirB", os.path.join(lp, "corpus", "knowledge", "a"))
    os.symlink("../dirA", os.path.join(lp, "dirB"))
    os.symlink("../dirA", os.path.join(lp, "corpus", "knowledge", "self"))
    rc, text = tool(lp, fleet, timeout=25)
    report("V8 symlink cycle (worktree, base tool)", rc, text,
           "base does not follow symlinked dirs at all, so no loop today; a fix that follows them must detect the cycle")

    # ---------------------------------------------------------------- V9: FIFO inside corpus/knowledge
    base, fleet, lp = fleet_for("v9_fifo")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    os.mkfifo(os.path.join(lp, "corpus", "knowledge", "pipe.md"))
    rc, text = tool(lp, fleet, timeout=15)
    report("V9 FIFO named pipe inside corpus/knowledge (worktree)", rc, text,
           "a blocking open is a hang, not a measurement")

    # ---------------------------------------------------------------- V10: symlink to /dev/zero-like unbounded file inside lane
    base, fleet, lp = fleet_for("v10_unbounded")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    big = os.path.join(base, "big.md")
    with open(big, "w") as fh:
        fh.write("Cites S100.\n" * 1)
    os.symlink(big, os.path.join(lp, "corpus", "knowledge", "big.md"))
    rc, text = tool(lp, fleet)
    report("V10 symlink to a file outside the lane (worktree)", rc, text)

    # ---------------------------------------------------------------- V11: TOCTOU — realpath check vs open
    base, fleet, lp = fleet_for("v11_toctou")
    put(lp, "corpus/SOURCES.md", registry([("S100", "https://example.invalid/100")]))
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    inside_target = os.path.join(lp, "corpus", "knowledge", "inside.md")
    put(lp, "corpus/knowledge/inside.md", "Cites S100.\n")
    outside_target = os.path.join(base, "outside", "outside.md")
    put(base, "outside", "outside.md", "Cites S950.\n")
    link = os.path.join(lp, "corpus", "knowledge", "swap.md")
    os.symlink(inside_target, link)
    # demonstrate the window explicitly: realpath says inside, the file it opens is not
    print("### V11 TOCTOU shape")
    print("  realpath(link) =", os.path.realpath(link), "-> inside lane:",
          os.path.realpath(link).startswith(os.path.realpath(lp) + os.sep))
    os.replace(link, os.symlink(outside_target, link)) if False else None
    os.unlink(link)
    os.symlink(outside_target, link)
    print("  after swap, realpath(link) =", os.path.realpath(link))
    rc, text = tool(lp, fleet)
    report("V11b link swapped to an outside target before the tool runs", rc, text)
    print()


def main2():
    pass


if __name__ == "__main__":
    main()
