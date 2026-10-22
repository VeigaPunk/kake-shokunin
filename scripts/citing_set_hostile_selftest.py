#!/usr/bin/env python3
"""Hostile-fixture selftest for the citing-set fixture runner (round 31).

The fixture runner ``scripts/citing_set_selftest.py`` must refuse fixture
shapes that would run foreign code, touch a Git repository outside the case
copy, hang, or vanish from the count.  This selftest builds each hostile shape
at run time from a committed spec and checks that the runner refuses it.

Specs: ``scripts/fixtures/citing-set-hostile/<case>/hostile.json`` (regular
files only; the hostile artifacts themselves are never committed)::

    {
      "description": "one line",
      "gap": "N1",
      "tmpdir_in_victim": false,
      "cases": [
        {"name": "h1a",
         "case_json": {"argv": ["--selftest"]},
         "planted_scripts": true,
         "dot_git": false,
         "expected": null,
         "symlink_case": false}
      ]
    }

Each hostile case starts as a copy of the benign fixture
``scripts/fixtures/citing-set/01-single-literal-clean`` and then gets:

  case_json        written as the case's ``case.json``
  planted_scripts  ``scripts/citing_set.py`` and ``scripts/citing_set_selftest.py``
                   that append to a canary file when executed, plus a nested
                   fixture so a delegated runner would reach them
  dot_git          a ``.git`` file pointing at a victim repository built here
  expected         "symlink_outside" (expected.json is a symlink to a matching
                   file outside the case), "padded" (a matching expectation
                   padded past 1 MiB) or "fifo" (expected.json is a FIFO)
  symlink_case     the case entry is a symlink to the benign case directory

``tmpdir_in_victim`` places the runner's ``--tmpdir`` inside the victim
repository, so a Git command that discovers an enclosing repository would
write to it.

For each spec the runner is run once over a scratch fixture directory holding
the benign case ``00-benign``, a second benign copy ``h0-control`` (named like
a hostile case, so a runner that refuses cases by name is caught; round-31
wave 2) and the hostile cases.  The spec passes when the runner exits 1 within
90 s, neither benign case is a failure, every hostile case is a failure, no
canary exists, and the victim repository's HEAD, refs and commit count are
unchanged.

Usage::

    python3 -B scripts/citing_set_hostile_selftest.py --root <tree> --tmpdir <dir>
        [--runner <path>]   (default <tree>/scripts/citing_set_selftest.py)

Output: one JSON object
``{"schema": "kake-citing-set-hostile-v1", "passed": bool, "cases": [...]}``.
Exit 0 when every spec passes, 1 when one fails, 2 on bad input (no specs,
unreadable spec, missing runner or benign fixture).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

SCHEMA = "kake-citing-set-hostile-v1"
SPEC_DIR = "scripts/fixtures/citing-set-hostile"
BENIGN = "scripts/fixtures/citing-set/01-single-literal-clean"
CONTROL = "h0-control"
SPEC_MAX_BYTES = 65536
RUN_TIMEOUT = 90
CASE_KEYS = {"name", "case_json", "planted_scripts", "dot_git", "expected", "symlink_case"}
SPEC_KEYS = {"description", "gap", "tmpdir_in_victim", "cases"}
EXPECTED_SHAPES = (None, "symlink_outside", "padded", "fifo")
PLANTED = """import os, sys
with open({canary!r}, "a") as handle:
    handle.write("executed " + os.path.abspath(__file__) + "\\n")
print('{{"verdict": "clean", "findings": [], "citingPairs": 0, "ledgerPairs": 0}}')
sys.exit(0)
"""


def git_env() -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_AUTHOR_NAME": "hostile-selftest", "GIT_AUTHOR_EMAIL": "hostile-selftest@invalid",
                "GIT_COMMITTER_NAME": "hostile-selftest", "GIT_COMMITTER_EMAIL": "hostile-selftest@invalid"})
    return env


def git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(cwd), "-c", "core.hooksPath=/dev/null", *args],
                          capture_output=True, env=git_env(), timeout=60)


def build_victim(path: Path) -> Path:
    path.mkdir(parents=True)
    for args in (("init", "-q"), ("add", "victim.txt"), ("commit", "-q", "--no-verify", "-m", "victim")):
        if args[0] == "add":
            (path / "victim.txt").write_text("victim\n")
        if git(path, *args).returncode != 0:
            raise RuntimeError("could not build the victim repository")
    return path


def victim_state(path: Path) -> str:
    head = git(path, "rev-parse", "HEAD").stdout.decode().strip()
    refs = git(path, "for-each-ref", "--format=%(refname) %(objectname)").stdout.decode()
    count = git(path, "rev-list", "--all", "--count").stdout.decode().strip()
    return "%s|%s|%s" % (head, count, refs)


def load_spec(path: Path) -> dict:
    info = os.lstat(path)
    if not stat.S_ISREG(info.st_mode) or info.st_size > SPEC_MAX_BYTES:
        raise ValueError("%s must be a regular file of at most %d bytes" % (path, SPEC_MAX_BYTES))
    spec = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(spec, dict) or set(spec) - SPEC_KEYS or not isinstance(spec.get("cases"), list) \
            or not spec["cases"]:
        raise ValueError("%s: spec must be an object with keys %s and a non-empty cases list"
                         % (path, sorted(SPEC_KEYS)))
    for case in spec["cases"]:
        if not isinstance(case, dict) or set(case) - CASE_KEYS or not isinstance(case.get("name"), str) \
                or not case["name"].lstrip(".").startswith("h") or "/" in case["name"] \
                or "\0" in case["name"] or case["name"] == CONTROL:
            raise ValueError("%s: each case needs a name starting with 'h' or '.h' (not %s, no NUL)"
                             " and only keys %s" % (path, CONTROL, sorted(CASE_KEYS)))
        if case.get("expected") not in EXPECTED_SHAPES:
            raise ValueError("%s: unknown expected shape %r" % (path, case.get("expected")))
    return spec


def build_case(case: dict, fixtures: Path, work: Path, victim: Path, canary: Path) -> None:
    benign = fixtures / "00-benign"
    target = fixtures / case["name"]
    if case.get("symlink_case"):
        os.symlink(benign, target)
        return
    shutil.copytree(benign, target, symlinks=True)
    if case.get("case_json") is not None:
        (target / "case.json").write_text(json.dumps(case["case_json"]), encoding="utf-8")
    if case.get("planted_scripts"):
        scripts = target / "scripts"
        shutil.copytree(benign, scripts / "fixtures" / "citing-set" / "x", symlinks=True)
        planted = PLANTED.format(canary=str(canary))
        (scripts / "citing_set.py").write_text(planted, encoding="utf-8")
        (scripts / "citing_set_selftest.py").write_text(planted, encoding="utf-8")
    if case.get("dot_git"):
        (target / ".git").write_text("gitdir: %s\n" % (victim / ".git"), encoding="utf-8")
    shape = case.get("expected")
    good = (benign / "expected.json").read_text(encoding="utf-8")
    if shape == "symlink_outside":
        outside = work / ("outside-%s.json" % case["name"])
        outside.write_text(good, encoding="utf-8")
        (target / "expected.json").unlink()
        os.symlink(outside, target / "expected.json")
    elif shape == "padded":
        (target / "expected.json").write_text(good.rstrip() + " " * (1024 * 1024 + 4096) + "\n",
                                              encoding="utf-8")
    elif shape == "fifo":
        (target / "expected.json").unlink()
        os.mkfifo(target / "expected.json")


def run_spec(name: str, spec: dict, root: Path, runner: Path, tmpdir: Path) -> dict:
    work = tmpdir / name
    if work.exists():
        shutil.rmtree(work)
    fixtures = work / "fixtures"
    fixtures.mkdir(parents=True)
    shutil.copytree(root / BENIGN, fixtures / "00-benign", symlinks=True)
    shutil.copytree(root / BENIGN, fixtures / CONTROL, symlinks=True)
    victim = build_victim(work / "victim")
    before = victim_state(victim)
    canary = work / "canary.txt"
    hostile = []
    for case in spec["cases"]:
        build_case(case, fixtures, work, victim, canary)
        hostile.append(case["name"])
    run_tmp = (victim / "tmp") if spec.get("tmpdir_in_victim") else (work / "tmp")
    run_tmp.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-B", str(runner), "--root", str(root), "--fixtures", str(fixtures),
               "--tmpdir", str(run_tmp), "--timeout", "20"]
    detail = {"gap": spec.get("gap"), "hostile": hostile}
    try:
        done = subprocess.run(command, capture_output=True, text=True, timeout=RUN_TIMEOUT,
                              env=git_env(), cwd=str(work))
        detail["exit"] = done.returncode
        detail["timedOut"] = False
        try:
            summary = json.loads(done.stdout)
        except ValueError:
            summary = {}
    except subprocess.TimeoutExpired:
        detail["exit"] = None
        detail["timedOut"] = True
        summary = {}
    failures = [f for f in summary.get("failures", []) if isinstance(f, dict)] if isinstance(summary, dict) else []
    failed = {f.get("case"): f.get("reason") for f in failures if f.get("case") is not None}
    detail["reasons"] = failed
    detail["canary"] = canary.exists()
    detail["victimUnchanged"] = victim_state(victim) == before
    passed = (detail["exit"] == 1 and "00-benign" not in failed and CONTROL not in failed
              and all(h in failed for h in hostile)
              and not detail["canary"] and detail["victimUnchanged"])
    return {"case": name, "passed": passed, "detail": detail}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="citing_set_hostile_selftest.py")
    parser.add_argument("--root", required=True, help="tree holding scripts/ (the lane or an export)")
    parser.add_argument("--tmpdir", required=True, help="scratch directory for the hostile builds")
    parser.add_argument("--runner", default=None, help="runner to test (default <root>/scripts/citing_set_selftest.py)")
    args = parser.parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    runner = Path(args.runner).expanduser().resolve() if args.runner else root / "scripts" / "citing_set_selftest.py"
    tmpdir = Path(args.tmpdir).expanduser().resolve()
    out = {"schema": SCHEMA, "passed": False, "runner": str(runner), "cases": [], "error": None}
    spec_dir = root / SPEC_DIR
    specs = sorted(p for p in spec_dir.iterdir() if p.is_dir() and not p.is_symlink()) if spec_dir.is_dir() else []
    if not runner.is_file() or not (root / BENIGN).is_dir() or not specs:
        out["error"] = "runner, benign fixture or hostile specs missing"
        print(json.dumps(out, indent=1))
        return 2
    try:
        loaded = [(p.name, load_spec(p / "hostile.json")) for p in specs]
    except (OSError, ValueError) as exc:
        out["error"] = str(exc)
        print(json.dumps(out, indent=1))
        return 2
    tmpdir.mkdir(parents=True, exist_ok=True)
    for name, spec in loaded:
        try:
            out["cases"].append(run_spec(name, spec, root, runner, tmpdir))
        except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
            out["cases"].append({"case": name, "passed": False, "detail": {"error": str(exc)}})
    out["passed"] = all(case["passed"] for case in out["cases"])
    print(json.dumps(out, indent=1))
    return 0 if out["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
