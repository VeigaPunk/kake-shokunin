#!/usr/bin/env python3
"""Second semantic probe: the survivors not covered by probe.py (M33, M34, M35, M37) plus a
sharper M09 (URL in a later cell of a SIBLING registry row) and a sharper M13."""
import os
import shutil
import subprocess
import sys

W = "/fast/scratch/hyaku/kake-r59/MutResolverSelftest/work/probe2"
SRC = "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py"
PRISTINE = os.path.join(W, "pristine.py")
REG = ("# Sources\n## Registry\n\n"
       "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "|---|---|---|---|---|---|---|---|---|---|---|\n")
ROW = "| {sid} | {src} | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n"


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def run(tool, argv):
    env = dict(os.environ)
    env["TMPDIR"] = os.path.join(W, "tmp")
    env["LC_ALL"] = "C.UTF-8"
    p = subprocess.run([sys.executable, "-B", tool] + argv, capture_output=True, env=env, cwd=W, timeout=300)
    out = p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")
    return p.returncode, " | ".join(out.strip().splitlines()[-2:])[:240]


def git(path, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    p = subprocess.run(["git", "-C", path, *args], capture_output=True, env=env)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def fresh(name):
    d = os.path.join(W, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    return d


def commit(path, msg="f"):
    git(path, "init", "-q")
    git(path, "add", "-A")
    git(path, "-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false",
        "commit", "-q", "-m", msg)


def s_m33():
    """revision: a knowledge file under corpus/knowledge-notes/ (prefix without separator)"""
    d = fresh("m33")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"), REG + ROW.format(sid="S001", src="https://e.example/1"))
    write(os.path.join(lane, "corpus/knowledge/a.md"), "Cites S001.\n")
    write(os.path.join(lane, "corpus/knowledge-notes/b.md"), "Cites S777.\n")
    commit(lane)
    rc, head, _ = git(lane, "rev-parse", "HEAD")
    return ["--root", lane, "--fleet", d, "--revision", head.strip()]


def s_m34():
    """sibling is a linked git worktree (.git is a file) with a dirty registry"""
    d = fresh("m34")
    fleet = os.path.join(d, "fleet")
    lane = os.path.join(fleet, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"), REG + ROW.format(sid="S001", src="https://e.example/1"))
    write(os.path.join(lane, "corpus/knowledge/a.md"), "Cites S777.\n")
    main_repo = os.path.join(fleet, "alpha-shokunin")
    write(os.path.join(main_repo, "corpus/SOURCES.md"), REG + ROW.format(sid="S777", src="https://a.example/7"))
    commit(main_repo)
    linked = os.path.join(fleet, "beta-shokunin")
    rc, out, err = git(main_repo, "worktree", "add", "-q", linked)
    if rc != 0:
        return None, ("worktree add failed", err.strip())
    write(os.path.join(linked, "corpus/SOURCES.md"), REG + ROW.format(sid="S999", src="https://b.example/9"))
    return ["--root", lane, "--fleet", fleet], None


def s_m35():
    """a fence closing run with trailing whitespace"""
    d = fresh("m35")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"),
          REG + ROW.format(sid="S001", src="https://e.example/1")
          + "```\n" + ROW.format(sid="S002", src="https://e.example/2") + "```  \n"
          + ROW.format(sid="S003", src="https://e.example/3"))
    write(os.path.join(lane, "corpus/knowledge/a.md"), "Cites S001, S002 and S003.\n")
    return ["--root", lane, "--fleet", d]


def s_m37():
    """the rendered unowned count differs from dangling when a sibling owns one id"""
    d = fresh("m37")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"), REG + ROW.format(sid="S001", src="https://e.example/1"))
    write(os.path.join(lane, "corpus/knowledge/a.md"), "Cites S700 and S800.\n")
    write(os.path.join(d, "alpha-shokunin", "corpus/SOURCES.md"), REG + ROW.format(sid="S700", src="https://a.example/7"))
    return ["--root", lane, "--fleet", d]


def s_m09b():
    """the sibling's registry holds the URL in a later cell of the row"""
    d = fresh("m09b")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"), REG + ROW.format(sid="S001", src="https://e.example/1"))
    write(os.path.join(lane, "corpus/knowledge/a.md"), "Cites S700, see https://a.example/7\n")
    write(os.path.join(d, "alpha-shokunin", "corpus/SOURCES.md"),
          REG + "| S700 | t | docs | A | s | a | x | mined | 2026-10-25 | 90d | https://a.example/7 |\n")
    return ["--root", lane, "--fleet", d]


def s_m02b():
    """a 2-digit registry cell: S12 can never be cited, so the mutant is unobservable"""
    d = fresh("m02b")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"), REG + ROW.format(sid="S12", src="https://e.example/12"))
    write(os.path.join(lane, "corpus/knowledge/a.md"), "Cites S12 and S001.\n")
    return ["--root", lane, "--fleet", d]


def s_m13b():
    """knowledge dir symlinked out of the lane: what is the difference beyond the message?"""
    d = fresh("m13b")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"), REG + ROW.format(sid="S001", src="https://e.example/1"))
    out = os.path.join(d, "outside")
    write(os.path.join(out, "a.md"), "Cites S001 and S777.\n")
    os.symlink(out, os.path.join(lane, "corpus", "knowledge"))
    return ["--root", lane, "--fleet", d]


SCEN = {"M33": s_m33, "M34": s_m34, "M35": s_m35, "M37": s_m37, "M09": s_m09b, "M02": s_m02b, "M13": s_m13b}


def main():
    os.makedirs(W, exist_ok=True)
    os.makedirs(os.path.join(W, "tmp"), exist_ok=True)
    shutil.copy(SRC, PRISTINE)
    for mid, fn in SCEN.items():
        mpath = os.path.join(W, "..", f"{mid}.py")
        if not os.path.exists(mpath):
            print(mid, "NO-MUTANT-FILE")
            continue
        out = fn()
        if isinstance(out, tuple) and out[0] is None:
            print(mid, "SKIP", out[1])
            continue
        argv = out[0] if isinstance(out, tuple) else out
        pc, pt = run(PRISTINE, argv)
        mc, mt = run(mpath, argv)
        same = (pc == mc and pt == mt)
        print(f"{mid} {'SAME(inert)' if same else 'DIFFERENT(blind spot)'} | pristine rc={pc} {pt} | mutant rc={mc} {mt}")


if __name__ == "__main__":
    main()
