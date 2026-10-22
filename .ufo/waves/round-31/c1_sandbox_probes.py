#!/usr/bin/env python3
"""Round-31 C1 counter: the citing-set runner refuses five hostile fixture shapes.

The five probes are the runner containment gaps the round-30 closure routed
(corpus/lessons/round-30-verifier-spotcheck.md, "Routed defects", item 1):

  P1 (N1) a case.json argv that reaches the gate's --selftest delegation
          (variants ["--selftest"], ["--self"], ["--revision", "HEAD",
          "--selftest"]) makes the gate run scripts copied from the fixture;
  P2 (N2) a fixture that carries its own .git (here a .git file pointing at a
          victim repository) is accepted by every setup op except git_init
          (variants: setup [git_commit] and setup [mkdir]);
  P3 (N3) git_commit with no git_init first discovers an enclosing
          repository (the runner's --tmpdir is placed inside a victim
          repository);
  P4 (N5) expected.json is read with no symlink, file-type or size guard
          (variants: a symlink to a matching expectation outside the case,
          a matching expectation padded past 1 MiB, a FIFO);
  P5 (N6) a symlinked case directory is skipped silently.

It exports ``scripts/`` from the named commit (``git archive``) into a scratch
directory and runs that exported runner,
``scripts/citing_set_selftest.py --root <export> --fixtures <probe dir>``, once
per probe.  Each probe directory holds a benign case (a copy of fixture
``01-single-literal-clean``) named ``00-benign`` plus the hostile case or
cases.  A probe passes only when ALL of these hold:

  behaviour  the runner exits 1 within 90 s; ``00-benign`` is not among its
             failures; every hostile case is among its failures; no harm is
             observed (P1: no canary written by a planted script; P2/P3: the
             victim repository's HEAD and ref list are unchanged);
  fixture    the commit carries a directory
             ``scripts/fixtures/citing-set-hostile/P<n>-<name>/`` and the
             exported ``scripts/citing_set_hostile_selftest.py --root <export>
             --tmpdir <dir>`` prints a JSON object whose ``cases`` list has an
             entry with ``case`` equal to that directory name and
             ``passed`` true.

Control K1: the exported runner over the committed fixture tree
(``--min-cases 45``) exits 0 with at least 45 cases.  The counter's exit is 0
only when 5/5 probes pass and K1 holds.

Usage: python3 -B c1_sandbox_probes.py --root <lane> --revision <commit>
       [--scratch <dir>]   (default /fast/scratch/hyaku/kake-r31/counter)
Exit 0 when 5/5 and K1 holds; 1 otherwise; 2 on bad input.
The output names this file's sha256, the revision and the runner sha256.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BENIGN = "01-single-literal-clean"
RUN_TIMEOUT = 90
HOSTILE_DIR = "scripts/fixtures/citing-set-hostile"
PROBES = {
    "P1": "N1 case argv reaching --selftest runs fixture-copied scripts",
    "P2": "N2 fixture .git accepted by setup ops other than git_init",
    "P3": "N3 git_commit without git_init discovers an enclosing repository",
    "P4": "N5 expected.json read with no symlink, file-type or size guard",
    "P5": "N6 symlinked case directory skipped silently",
}


def clean_env() -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    for k, v in (("GIT_AUTHOR_NAME", "probe"), ("GIT_AUTHOR_EMAIL", "probe@invalid"),
                 ("GIT_COMMITTER_NAME", "probe"), ("GIT_COMMITTER_EMAIL", "probe@invalid")):
        env[k] = v
    return env


def git(cwd, *args, check=False) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, env=clean_env(), check=check)


def victim_repo(path: Path) -> Path:
    path.mkdir(parents=True)
    git(path, "init", "-q", check=True)
    (path / "victim.txt").write_text("victim\n")
    git(path, "add", "victim.txt", check=True)
    git(path, "commit", "-q", "-m", "victim", check=True)
    return path


def victim_state(path: Path) -> str:
    head = git(path, "rev-parse", "HEAD").stdout.decode().strip()
    refs = git(path, "for-each-ref", "--format=%(refname) %(objectname)").stdout.decode()
    count = git(path, "rev-list", "--all", "--count").stdout.decode().strip()
    return f"{head}|{count}|{refs}"


def benign_into(export: Path, fixtures: Path) -> None:
    shutil.copytree(export / "scripts/fixtures/citing-set" / BENIGN, fixtures / "00-benign", symlinks=True)


def run_runner(export: Path, fixtures: Path, tmpdir: Path, extra=()) -> dict:
    cmd = [sys.executable, "-B", str(export / "scripts/citing_set_selftest.py"), "--root", str(export),
           "--fixtures", str(fixtures), "--tmpdir", str(tmpdir), "--timeout", "20", *extra]
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=RUN_TIMEOUT, env=clean_env(),
                              cwd=str(tmpdir.parent))
    except subprocess.TimeoutExpired:
        return {"exit": None, "timedOut": True, "failedCases": []}
    try:
        summary = json.loads(done.stdout)
    except ValueError:
        summary = {}
    failed = sorted({f.get("case") for f in summary.get("failures", []) if isinstance(f, dict)} - {None})
    return {"exit": done.returncode, "timedOut": False, "failedCases": failed,
            "reasons": {f.get("case"): f.get("reason") for f in summary.get("failures", []) if isinstance(f, dict)}}


def behaviour_ok(res: dict, hostile: list[str]) -> bool:
    return (res["exit"] == 1 and not res["timedOut"] and "00-benign" not in res["failedCases"]
            and all(h in res["failedCases"] for h in hostile))


PLANTED = """import os, sys
open({canary!r}, "a").write("executed " + os.path.abspath(__file__) + "\\n")
print('{{"verdict": "clean", "findings": [], "citingPairs": 0, "ledgerPairs": 0}}')
sys.exit(0)
"""


def probe_p1(export: Path, work: Path) -> tuple[bool, dict]:
    fixtures = work / "fixtures"
    fixtures.mkdir(parents=True)
    benign_into(export, fixtures)
    canary = work / "canary.txt"
    variants = {"h1a": ["--selftest"], "h1b": ["--self"], "h1c": ["--revision", "HEAD", "--selftest"]}
    for name, argv in variants.items():
        case = fixtures / name
        shutil.copytree(fixtures / "00-benign", case, symlinks=True)
        (case / "case.json").write_text(json.dumps({"argv": argv}))
        scripts = case / "scripts"
        nested = scripts / "fixtures/citing-set/x"
        shutil.copytree(fixtures / "00-benign", nested, symlinks=True)
        planted = PLANTED.format(canary=str(canary))
        (scripts / "citing_set.py").write_text(planted)
        (scripts / "citing_set_selftest.py").write_text(planted)
    res = run_runner(export, fixtures, work / "tmp")
    res["canary"] = canary.exists()
    return behaviour_ok(res, list(variants)) and not res["canary"], res


def probe_p2(export: Path, work: Path) -> tuple[bool, dict]:
    fixtures = work / "fixtures"
    fixtures.mkdir(parents=True)
    benign_into(export, fixtures)
    victim = victim_repo(work / "victim")
    before = victim_state(victim)
    variants = {"h2a": [{"op": "git_commit", "message": "probe"}], "h2b": [{"op": "mkdir", "path": "extra"}]}
    for name, setup in variants.items():
        case = fixtures / name
        shutil.copytree(fixtures / "00-benign", case, symlinks=True)
        (case / ".git").write_text(f"gitdir: {victim / '.git'}\n")
        (case / "case.json").write_text(json.dumps({"setup": setup}))
    res = run_runner(export, fixtures, work / "tmp")
    res["victimUnchanged"] = victim_state(victim) == before
    return behaviour_ok(res, list(variants)) and res["victimUnchanged"], res


def probe_p3(export: Path, work: Path) -> tuple[bool, dict]:
    fixtures = work / "fixtures"
    fixtures.mkdir(parents=True)
    benign_into(export, fixtures)
    victim = victim_repo(work / "victim")
    before = victim_state(victim)
    case = fixtures / "h3"
    shutil.copytree(fixtures / "00-benign", case, symlinks=True)
    (case / "case.json").write_text(json.dumps({"setup": [{"op": "git_commit", "message": "probe"}]}))
    tmp = victim / "tmp"
    tmp.mkdir()
    res = run_runner(export, fixtures, tmp)
    res["victimUnchanged"] = victim_state(victim) == before
    return behaviour_ok(res, ["h3"]) and res["victimUnchanged"], res


def probe_p4(export: Path, work: Path) -> tuple[bool, dict]:
    fixtures = work / "fixtures"
    fixtures.mkdir(parents=True)
    benign_into(export, fixtures)
    good = (fixtures / "00-benign/expected.json").read_text()
    outside = work / "outside-expected.json"
    outside.write_text(good)
    a = fixtures / "h4a"
    shutil.copytree(fixtures / "00-benign", a, symlinks=True)
    (a / "expected.json").unlink()
    os.symlink(outside, a / "expected.json")
    b = fixtures / "h4b"
    shutil.copytree(fixtures / "00-benign", b, symlinks=True)
    (b / "expected.json").write_text(good.rstrip() + " " * (1024 * 1024 + 4096) + "\n")
    c = fixtures / "h4c"
    shutil.copytree(fixtures / "00-benign", c, symlinks=True)
    (c / "expected.json").unlink()
    os.mkfifo(c / "expected.json")
    res = run_runner(export, fixtures, work / "tmp")
    return behaviour_ok(res, ["h4a", "h4b", "h4c"]), res


def probe_p5(export: Path, work: Path) -> tuple[bool, dict]:
    fixtures = work / "fixtures"
    fixtures.mkdir(parents=True)
    benign_into(export, fixtures)
    os.symlink(fixtures / "00-benign", fixtures / "h5")
    res = run_runner(export, fixtures, work / "tmp")
    return behaviour_ok(res, ["h5"]), res


def hostile_selftest(export: Path, work: Path) -> dict:
    script = export / "scripts/citing_set_hostile_selftest.py"
    if not script.is_file():
        return {"present": False, "cases": {}}
    tmp = work / "hostile-tmp"
    tmp.mkdir(parents=True)
    try:
        done = subprocess.run([sys.executable, "-B", str(script), "--root", str(export), "--tmpdir", str(tmp)],
                              capture_output=True, text=True, timeout=600, env=clean_env(), cwd=str(work))
    except subprocess.TimeoutExpired:
        return {"present": True, "exit": None, "cases": {}}
    try:
        doc = json.loads(done.stdout)
    except ValueError:
        doc = {}
    cases = {}
    for item in doc.get("cases", []) if isinstance(doc, dict) else []:
        if isinstance(item, dict) and isinstance(item.get("case"), str):
            cases[item["case"]] = item.get("passed") is True
    return {"present": True, "exit": done.returncode, "cases": cases}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--scratch", default="/fast/scratch/hyaku/kake-r31/counter")
    a = ap.parse_args()
    rp = git(a.root, "rev-parse", "--verify", "--quiet", f"{a.revision}^{{commit}}")
    if rp.returncode != 0:
        print(json.dumps({"error": "revision not found", "revision": a.revision}))
        return 2
    rev = rp.stdout.decode().strip()
    Path(a.scratch).mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix=f"c1-{rev[:7]}-", dir=a.scratch))
    export = scratch / "export"
    export.mkdir()
    arch = subprocess.run(["git", "-C", a.root, "archive", "--format=tar", rev, "scripts"],
                          capture_output=True, env=clean_env())
    if arch.returncode != 0:
        print(json.dumps({"error": "archive failed", "stderr": arch.stderr.decode()}))
        return 2
    subprocess.run(["tar", "-x", "-C", str(export)], input=arch.stdout, check=True)
    runner = export / "scripts/citing_set_selftest.py"
    runner_sha = hashlib.sha256(runner.read_bytes()).hexdigest() if runner.is_file() else None

    k1_tmp = scratch / "k1" / "tmp"
    k1_tmp.mkdir(parents=True)
    try:
        k1 = subprocess.run([sys.executable, "-B", str(runner), "--root", str(export), "--tmpdir", str(k1_tmp),
                             "--min-cases", "45"], capture_output=True, text=True, timeout=900,
                            env=clean_env(), cwd=str(scratch))
        k1_doc = json.loads(k1.stdout) if k1.stdout.strip() else {}
        k1_ok = k1.returncode == 0 and int(k1_doc.get("cases", 0)) >= 45
        k1_info = {"exit": k1.returncode, "cases": k1_doc.get("cases")}
    except (subprocess.TimeoutExpired, ValueError) as exc:
        k1_ok, k1_info = False, {"error": str(exc)}

    hostile = hostile_selftest(export, scratch)
    hostile_dirs = sorted(p.name for p in (export / HOSTILE_DIR).iterdir()
                          if p.is_dir() and not p.is_symlink()) if (export / HOSTILE_DIR).is_dir() else []
    funcs = {"P1": probe_p1, "P2": probe_p2, "P3": probe_p3, "P4": probe_p4, "P5": probe_p5}
    rows = []
    for pid, fn in funcs.items():
        work = scratch / pid
        work.mkdir()
        try:
            beh, detail = fn(export, work)
        except Exception as exc:  # a probe that cannot be built does not pass
            beh, detail = False, {"error": repr(exc)}
        named = [d for d in hostile_dirs if d.startswith(pid + "-")]
        fixture_ok = bool(named) and all(hostile["cases"].get(d) is True for d in named)
        rows.append({"id": pid, "gap": PROBES[pid], "passed": bool(beh and fixture_ok),
                     "behaviour": bool(beh), "fixture": fixture_ok, "fixtureDirs": named, "detail": detail})
    passed = sum(r["passed"] for r in rows)
    print(json.dumps({"counter": "kake-r31-c1-sandbox-probes",
                      "counterSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      "revision": rev, "runnerSha256": runner_sha, "passed": passed, "total": len(rows),
                      "controlK1": k1_ok, "k1": k1_info,
                      "hostileSelftest": {k: v for k, v in hostile.items()}, "probes": rows},
                     indent=1, default=str))
    print(f"C1 {passed}/{len(rows)} K1={'hold' if k1_ok else 'broken'} at {rev}", file=sys.stderr)
    return 0 if passed == len(rows) and k1_ok else 1


if __name__ == "__main__":
    sys.exit(main())
