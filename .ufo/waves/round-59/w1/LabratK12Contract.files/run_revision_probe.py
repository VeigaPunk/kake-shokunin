#!/usr/bin/env python3
"""Extra probe: how does the CURRENT tool behave when corpus/SOURCES.md is a symlink in REVISION mode?

Read-only w.r.t. the lane. Fixtures under scratch only; the fixture repo is committed with selftest identity
and its toplevel is verified before the first commit.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

SCRATCH = "/fast/scratch/hyaku/kake-r59/LabratK12Contract"
TOOL = os.path.join(SCRATCH, "tool_current.py")
HDR = ("| id | name | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
REG = "# Sources\n\n## Registry\n\n" + HDR + f"| S900 | fixture — https://example.invalid/S900 | docs | A | scope | anchor | teaches | mined | 2026-10-27 | 90d | corpus/knowledge/ok.md |\n"


def git(args, cwd):
    return subprocess.run(["git", "-C", cwd] + args, capture_output=True)


def commit(path):
    git(["init", "-q"], path)
    p = git(["rev-parse", "--show-toplevel"], path)
    top = p.stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(path), (top, path)
    git(["add", "-A"], path)
    git(["-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false",
         "commit", "-q", "-m", "fixture"], path)
    return git(["rev-parse", "HEAD"], path).stdout.decode().strip()


out = []
for mode in ("committed_symlink_out_of_lane", "committed_symlink_in_lane", "committed_regular_registry"):
    root = tempfile.mkdtemp(dir=SCRATCH, prefix="rev-")
    fleet = os.path.join(root, "fleet")
    lane = os.path.join(fleet, "kake-shokunin")
    os.makedirs(os.path.join(lane, "corpus", "knowledge"))
    with open(os.path.join(lane, "corpus", "knowledge", "ok.md"), "w", encoding="utf-8") as fh:
        fh.write("Cites S900 and S901.\n")
    reg = os.path.join(lane, "corpus", "SOURCES.md")
    if mode == "committed_regular_registry":
        with open(reg, "w", encoding="utf-8") as fh:
            fh.write(REG)
    elif mode == "committed_symlink_in_lane":
        with open(os.path.join(lane, "corpus", "SOURCES-real.md"), "w", encoding="utf-8") as fh:
            fh.write(REG)
        os.symlink("./SOURCES-real.md", reg)
    else:
        outside = os.path.join(root, "outside")
        os.makedirs(outside)
        with open(os.path.join(outside, "SOURCES.md"), "w", encoding="utf-8") as fh:
            fh.write(REG)
        os.symlink(os.path.join(outside, "SOURCES.md"), reg)
    head = commit(lane)
    p = subprocess.run([sys.executable, "-B", TOOL, "--root", lane, "--fleet", fleet, "--revision", head],
                       capture_output=True, timeout=300)
    txt = (p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")).strip()
    out.append({"mode": mode, "exit": p.returncode, "output": txt})
    print(f"=== {mode}: exit={p.returncode}")
    for line in txt.splitlines():
        print("    | " + line)
    shutil.rmtree(root, ignore_errors=True)

with open(os.path.join(SCRATCH, "results_revision.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2)
