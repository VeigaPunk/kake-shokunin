#!/usr/bin/env python3
"""Semantic probe: for each surviving mutant, build a tiny fixture where pristine and mutant
differ, and record both behaviours. A survivor with identical behaviour is inert (equivalent
mutant); a survivor with a different behaviour is a real blind spot of the 59-case selftest."""
import os
import shutil
import subprocess
import sys

W = "/fast/scratch/hyaku/kake-r59/MutResolverSelftest/work/probe"
SRC = "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py"
PRISTINE = os.path.join(W, "pristine.py")

REG = ("# Sources\n## Registry\n\n"
       "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "|---|---|---|---|---|---|---|---|---|---|---|\n")


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
    return p.returncode, " | ".join(out.strip().splitlines()[-2:])[:220]


def git(path, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    p = subprocess.run(["git", "-C", path, *args], capture_output=True, env=env)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def fresh(name):
    d = os.path.join(W, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    return d


def scenario_m02():
    d = fresh("m02")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"),
          REG + "| S12 | https://e.example/12 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    write(os.path.join(lane, "corpus/knowledge/a.md"), "Cites S001.\n")
    return ["--root", lane, "--fleet", d]


def scenario_m03():
    d = fresh("m03")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"),
          REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n"
          "### Sub\n"
          "| S002 | https://e.example/2 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    write(os.path.join(lane, "corpus/knowledge/a.md"), "Cites S001 and S002.\n")
    return ["--root", lane, "--fleet", d]


def scenario_m04():
    d = fresh("m04")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"),
          REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n"
          "    ```\n"
          "| S002 | https://e.example/2 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    write(os.path.join(lane, "corpus/knowledge/a.md"), "Cites S001 and S002.\n")
    return ["--root", lane, "--fleet", d]


def scenario_m06():
    d = fresh("m06")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"),
          REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n"
          "~~~\n| S002 | https://e.example/2 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n```\n"
          "| S003 | https://e.example/3 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n~~~\n")
    write(os.path.join(lane, "corpus/knowledge/a.md"), "Cites S001, S002 and S003.\n")
    return ["--root", lane, "--fleet", d]


def scenario_m07():
    d = fresh("m07")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"),
          REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n"
          "```a`b\n| S002 | https://e.example/2 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n```\n")
    write(os.path.join(lane, "corpus/knowledge/a.md"), "Cites S001 and S002.\n")
    return ["--root", lane, "--fleet", d]


def scenario_m09():
    d = fresh("m09")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"),
          REG + "| S900 | t | docs | A | s | a | x | mined | 2026-10-25 | 90d | https://e.example/900 |\n")
    write(os.path.join(lane, "corpus/knowledge/a.md"), "Cites S001, see https://a.example/1\n")
    write(os.path.join(d, "alpha-shokunin", "corpus/SOURCES.md"),
          REG + "| S001 | https://a.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    return ["--root", lane, "--fleet", d]


def scenario_m11():
    d = fresh("m11")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"),
          REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    write(os.path.join(lane, "corpus/knowledge/a.markdown"), "Cites S001 and S777.\n")
    return ["--root", lane, "--fleet", d]


def scenario_m13():
    d = fresh("m13")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"),
          REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    out = os.path.join(d, "outside")
    write(os.path.join(out, "a.md"), "Cites S001 and S777.\n")
    os.symlink(out, os.path.join(lane, "corpus", "knowledge"))
    return ["--root", lane, "--fleet", d]


def scenario_m14():
    d = fresh("m14")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"),
          REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    write(os.path.join(lane, "corpus/knowledge/ok.md"), "Cites S001.\n")
    bad = os.path.join(os.fsencode(lane), b"corpus/knowledge/bad\xff.md")
    os.makedirs(os.path.dirname(bad), exist_ok=True)
    with open(bad, "wb") as fh:
        fh.write(b"Cites S777.\n")
    git(lane, "init", "-q")
    git(lane, "add", "-A")
    git(lane, "-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false",
        "commit", "-q", "-m", "f")
    rc, head = git(lane, "rev-parse", "HEAD")
    return ["--root", lane, "--fleet", d, "--revision", head.strip()]


def scenario_m17():
    d = fresh("m17")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"),
          REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    write(os.path.join(lane, "corpus/knowledge/a.md"), "Cites S001.\n")
    git(lane, "init", "-q")
    git(lane, "add", "-A")
    git(lane, "-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false",
        "commit", "-q", "-m", "f")
    rc, head = git(lane, "rev-parse", "HEAD")
    rc2, tree = git(lane, "rev-parse", head.strip() + "^{tree}")
    return ["--root", lane, "--fleet", d, "--revision", tree.strip()]


def scenario_m22():
    d = fresh("m22")
    fleet = os.path.join(d, "fleet")
    lane = os.path.join(fleet, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"),
          REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    write(os.path.join(lane, "corpus/knowledge/a.md"), "Cites S777.\n")
    write(os.path.join(fleet, "alpha-shokunin", "corpus/SOURCES.md"),
          REG + "| S777 | https://a.example/7 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    return ["--root", lane]


def scenario_m31():
    d = fresh("m31")
    lane = os.path.join(d, "demo-shokunin")
    write(os.path.join(lane, "corpus/SOURCES.md"),
          REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    git(lane, "init", "-q")
    git(lane, "add", "-A")
    git(lane, "-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false",
        "commit", "-q", "-m", "f")
    rc, head = git(lane, "rev-parse", "HEAD")
    return ["--root", lane, "--fleet", d, "--revision", head.strip()]


SCENARIOS = {
    "M02": scenario_m02, "M03": scenario_m03, "M04": scenario_m04, "M06": scenario_m06,
    "M07": scenario_m07, "M09": scenario_m09, "M11": scenario_m11, "M13": scenario_m13,
    "M14": scenario_m14, "M17": scenario_m17, "M22": scenario_m22, "M31": scenario_m31,
}


def main():
    os.makedirs(W, exist_ok=True)
    os.makedirs(os.path.join(W, "tmp"), exist_ok=True)
    shutil.copy(SRC, PRISTINE)
    for mid, fn in SCENARIOS.items():
        mpath = os.path.join(W, "..", f"{mid}.py")
        if not os.path.exists(mpath):
            print(mid, "NO-MUTANT-FILE")
            continue
        out = fn()
        argv = out[0] if isinstance(out, tuple) else out
        pc, pt = run(PRISTINE, argv)
        mc, mt = run(mpath, argv)
        same = (pc == mc and pt == mt)
        print(f"{mid} {'SAME(inert)' if same else 'DIFFERENT(blind spot)'} | pristine rc={pc} {pt} | mutant rc={mc} {mt}")


if __name__ == "__main__":
    main()
