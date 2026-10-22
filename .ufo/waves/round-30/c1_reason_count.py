#!/usr/bin/env python3
"""Round-30 C1 counter: citing-set reason codes asserted by committed fixtures,
and the round-27 failure families repaired.

It exports ``scripts/`` from the named commit (``git archive``) into a scratch
directory and grades 14 checks against those bytes only.

R01-R08, one per round-28 reason code (round-28 routed defect 1):
  document_not_regular_file, document_not_json, corpus_directory_missing,
  corpus_empty, not_a_directory, population_id_unreachable,
  revision_not_found, root_not_repository_top_level.
  A code passes only when all three hold:
    behaviour  a case this counter builds makes the exported gate return
               exit 2, verdict ``could-not-evaluate`` and a finding whose id is
               ``input_invalid`` AND whose reason is the code (full tuple);
    fixture    some committed ``scripts/fixtures/citing-set/*/expected.json``
               lists the finding as an object {"id": "input_invalid",
               "reason": <code>};
    compared   the committed runner ``scripts/citing_set_selftest.py`` exits 0
               on the exported tree, and exits non-zero when every
               double-quoted occurrence of the code in the exported gate is
               renamed (``"<code>"`` -> ``"<code>_mutated"``).

F01-F06, the round-27 families that round 28 left open (routed defect 2):
  F01 duplicate JSON member names (population top level; ledger pair object)
      -> exit 2, input_invalid, reason ``document_duplicate_key``; plus the
      fixture and compared conditions above for that code.
  F02 non-finite numbers (NaN, Infinity, -Infinity)
      -> exit 2, input_invalid, reason ``document_nonfinite_number``; plus the
      fixture and compared conditions for that code.
  F03 population ids with fewer than three digits (``S01``/``S02`` with a
      corpus that spells them so; ``S1``) -> exit 2, input_invalid, reason
      ``population_id_unreachable``.
  F04 a repeated valued option (``--population``, ``--ledger``,
      ``--revision``, ``--root``; the last value being the usable one)
      -> exit 64 with one JSON object on stdout, for each of the four.
  F05 a corpus directory 1000 levels deep holding one entry that cites S001,
      empty ledger -> exit 1, verdict ``failed``, exactly one
      ``unadjudicated_citing_pair`` finding, and no ``Traceback`` on stderr.
  F06 opening a terminal device as an input document does not make it the
      controlling terminal (O_NOCTTY): the gate runs in a new session with
      ``--root /dev/pts --population <n> --ledger <n>`` for a fresh pseudo
      terminal; pass when it exits 2 with finding (input_invalid,
      document_not_regular_file) and the process tty_nr stays 0.

Controls (a refuse-everything gate fails them; any failing control marks the
counter run broken, exit 2): K1 valid clean working tree -> 0/clean; K2 valid
clean Git read -> 0/clean; K3 real omission -> 1/failed with
unadjudicated_citing_pair.

Constant gates: the 14 checks are re-run with the exported gate replaced by a
constant-clean stub and by a refuse-everything stub; each must score below 14.

Output: one JSON object naming the counter sha256, the measured commit, the
gate and runner sha256 at that commit, every check with its sub-results, the
controls and the constant-gate scores.
Usage: python3 -B c1_reason_count.py --root <lane> --revision <commit>
Exit 0 when 14/14, controls hold and both constant gates are rejected; 1 when
a check fails; 2 on bad input or a broken control.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile

TIMEOUT = 30
RUNNER_TIMEOUT = 900
SCRATCH = "/fast/scratch/hyaku/kake-r30/c1-count"
R_CODES = [
    "document_not_regular_file",
    "document_not_json",
    "corpus_directory_missing",
    "corpus_empty",
    "not_a_directory",
    "population_id_unreachable",
    "revision_not_found",
    "root_not_repository_top_level",
]
DUP = "document_duplicate_key"
NONFINITE = "document_nonfinite_number"
POPULATION = {"rows": [{"id": "S001"}, {"id": "S002"}]}
LEDGER_CLEAN = {"pairs": [{"row": "S001", "file": "corpus/knowledge/entry.md"}]}
LEDGER_EMPTY = {"pairs": []}
ENTRY = "# Entry\n\nThis statement cites S001.\n"
UNCITED = "# Entry\n\nThis statement cites nothing.\n"
GIT_ENV = {
    "GIT_AUTHOR_NAME": "c1-count", "GIT_AUTHOR_EMAIL": "c1-count@invalid",
    "GIT_COMMITTER_NAME": "c1-count", "GIT_COMMITTER_EMAIL": "c1-count@invalid",
    "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1",
}
CLEAN_STUB = ('import json, sys\nprint(json.dumps({"verdict": "clean", "citingPairs": 0, '
              '"ledgerPairs": 0, "findings": []}))\nsys.exit(0)\n')
REFUSE_STUB = ('import json, sys\nprint(json.dumps({"verdict": "could-not-evaluate", "citingPairs": 0, '
               '"ledgerPairs": 0, "findings": [{"id": "input_invalid", "reason": "refused"}]}))\nsys.exit(2)\n')
NOCTTY_WRAPPER = r'''
import json, runpy, sys
gate = sys.argv[1]
sys.argv = [gate] + sys.argv[2:]
code = None
try:
    runpy.run_path(gate, run_name="__main__")
except SystemExit as exc:
    code = exc.code
sys.stdout.flush()
with open("/proc/self/stat") as handle:
    tty = int(handle.read().rsplit(")", 1)[1].split()[4])
sys.stdout.write("\n@@NOCTTY " + json.dumps({"exit": code, "ttyNr": tty}) + "\n")
'''


def env_clean():
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb" if isinstance(data, bytes) else "w") as handle:
        handle.write(data)


def write_json(path, value):
    write(path, json.dumps(value, indent=2) + "\n")


def valid_tree(root, population=POPULATION, ledger=LEDGER_CLEAN, corpus=True):
    os.makedirs(root, exist_ok=True)
    write_json(os.path.join(root, "population.json"), population)
    write_json(os.path.join(root, "ledger.json"), ledger)
    if corpus:
        write(os.path.join(root, "corpus", "knowledge", "entry.md"), ENTRY)


def git(root, *arguments):
    env = env_clean()
    env.update(GIT_ENV)
    subprocess.run(["git", "-C", root] + list(arguments), check=True, env=env,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def commit_all(root):
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "case")


def args_for(root, population="population.json", ledger="ledger.json"):
    return ["--root", root, "--population", population, "--ledger", ledger, "--json"]


def run_gate(gate, arguments):
    try:
        done = subprocess.run([sys.executable, "-B", gate] + arguments, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, timeout=TIMEOUT,
                              env=env_clean())
    except subprocess.TimeoutExpired:
        return {"exit": None, "stdout": "", "stderr": "timed out"}
    return {"exit": done.returncode, "stdout": done.stdout.decode("utf-8", "replace"),
            "stderr": done.stderr.decode("utf-8", "replace")}


def report_of(observed):
    try:
        value = json.loads(observed["stdout"])
    except (ValueError, RecursionError):
        return None
    return value if isinstance(value, dict) else None


def tuples(report):
    findings = report.get("findings") if report else None
    if not isinstance(findings, list):
        return None
    return sorted([str(f.get("id")), str(f.get("reason"))] if isinstance(f, dict) else [str(f), "None"]
                  for f in findings)


def judge(observed, want_exit, want_verdict, want_tuple=None, want_exactly=None):
    """Full-tuple comparison: exit, verdict and (id, reason) of the finding."""
    report = report_of(observed)
    got = tuples(report)
    problems = []
    if observed["exit"] != want_exit:
        problems.append("exit %s, want %s" % (observed["exit"], want_exit))
    if report is None:
        problems.append("stdout is not one JSON object")
    elif report.get("verdict") != want_verdict:
        problems.append("verdict %r, want %r" % (report.get("verdict"), want_verdict))
    if want_tuple is not None and (got is None or list(want_tuple) not in got):
        problems.append("no finding %s in %s" % (list(want_tuple), got))
    if want_exactly is not None and got != sorted(list(t) for t in want_exactly):
        problems.append("findings %s, want exactly %s" % (got, [list(t) for t in want_exactly]))
    if "Traceback" in observed.get("stderr", ""):
        problems.append("traceback on stderr")
    return {"passed": not problems, "problems": problems,
            "observed": {"exit": observed["exit"], "verdict": report.get("verdict") if report else None,
                         "findings": got}}


def refused(gate, arguments, code):
    return judge(run_gate(gate, arguments), 2, "could-not-evaluate", ("input_invalid", code))


def behaviour_cases(gate, work):
    """Counter-built cases: code -> list of judged outcomes."""
    out = {}

    def case(name):
        return os.path.join(work, name)

    root = case("fifo")
    valid_tree(root)
    os.remove(os.path.join(root, "population.json"))
    os.mkfifo(os.path.join(root, "population.json"))
    out["document_not_regular_file"] = [refused(gate, args_for(root), "document_not_regular_file")]

    root = case("malformed")
    valid_tree(root)
    write(os.path.join(root, "ledger.json"), '{"pairs": [\n')
    out["document_not_json"] = [refused(gate, args_for(root), "document_not_json")]

    root = case("corpus-absent")
    valid_tree(root, ledger=LEDGER_EMPTY, corpus=False)
    out["corpus_directory_missing"] = [refused(gate, args_for(root), "corpus_directory_missing")]

    root = case("corpus-empty")
    valid_tree(root, ledger=LEDGER_EMPTY, corpus=False)
    os.makedirs(os.path.join(root, "corpus", "knowledge"))
    out["corpus_empty"] = [refused(gate, args_for(root), "corpus_empty")]

    root = case("corpus-blob")
    valid_tree(root, ledger=LEDGER_EMPTY, corpus=False)
    write(os.path.join(root, "corpus", "knowledge"), UNCITED)
    commit_all(root)
    out["not_a_directory"] = [refused(gate, args_for(root) + ["--revision", "HEAD"], "not_a_directory")]

    root = case("unreachable-x001")
    valid_tree(root, population={"rows": [{"id": "X001"}]}, ledger=LEDGER_EMPTY)
    out["population_id_unreachable"] = [refused(gate, args_for(root), "population_id_unreachable")]

    root = case("revision-unknown")
    valid_tree(root)
    commit_all(root)
    out["revision_not_found"] = [refused(gate, args_for(root) + ["--revision", "no-such-revision"],
                                         "revision_not_found")]

    top = case("nested")
    sub = os.path.join(top, "sub")
    valid_tree(top, ledger=LEDGER_EMPTY, corpus=False)
    write(os.path.join(top, "corpus", "knowledge", "entry.md"), UNCITED)
    valid_tree(sub, ledger=LEDGER_EMPTY)
    commit_all(top)
    out["root_not_repository_top_level"] = [refused(gate, args_for(sub) + ["--revision", "HEAD"],
                                                    "root_not_repository_top_level")]

    dup = []
    root = case("dup-population")
    valid_tree(root)
    write(os.path.join(root, "population.json"),
          '{"rows": [{"id": "S001"}], "rows": [{"id": "S001"}, {"id": "S002"}]}\n')
    dup.append(refused(gate, args_for(root), DUP))
    root = case("dup-ledger-pair")
    valid_tree(root)
    write(os.path.join(root, "ledger.json"),
          '{"pairs": [{"row": "S002", "row": "S001", "file": "corpus/knowledge/entry.md"}]}\n')
    dup.append(refused(gate, args_for(root), DUP))
    out[DUP] = dup

    nonfinite = []
    for label, token in (("nan", "NaN"), ("inf", "Infinity"), ("neginf", "-Infinity")):
        root = case("nonfinite-" + label)
        valid_tree(root)
        write(os.path.join(root, "population.json"),
              '{"rows": [{"id": "S001"}, {"id": "S002"}], "weight": %s}\n' % token)
        nonfinite.append(refused(gate, args_for(root), NONFINITE))
    out[NONFINITE] = nonfinite
    return out


def family_cases(gate, work):
    out = {}
    short = []
    root = os.path.join(work, "short-s01")
    valid_tree(root, population={"rows": [{"id": "S01"}, {"id": "S02"}]}, ledger=LEDGER_EMPTY, corpus=False)
    write(os.path.join(root, "corpus", "knowledge", "entry.md"), "# Entry\n\nSee S01 and S02 for details.\n")
    short.append(refused(gate, args_for(root), "population_id_unreachable"))
    root = os.path.join(work, "short-s1")
    valid_tree(root, population={"rows": [{"id": "S1"}]}, ledger=LEDGER_EMPTY, corpus=False)
    write(os.path.join(root, "corpus", "knowledge", "entry.md"), UNCITED)
    short.append(refused(gate, args_for(root), "population_id_unreachable"))
    out["F03"] = short

    repeated = []
    root = os.path.join(work, "repeat")
    valid_tree(root)
    commit_all(root)
    variants = [
        ["--root", root, "--population", "does-not-exist.json", "--population", "population.json",
         "--ledger", "ledger.json", "--json"],
        ["--root", root, "--population", "population.json", "--ledger", "does-not-exist.json",
         "--ledger", "ledger.json", "--json"],
        args_for(root) + ["--revision", "no-such-revision", "--revision", "HEAD"],
        ["--root", "/nonexistent-root-c1-count", "--root", root, "--population", "population.json",
         "--ledger", "ledger.json", "--json"],
    ]
    for variant in variants:
        observed = run_gate(gate, variant)
        problems = []
        if observed["exit"] != 64:
            problems.append("exit %s, want 64" % observed["exit"])
        if report_of(observed) is None:
            problems.append("stdout is not one JSON object")
        repeated.append({"passed": not problems, "problems": problems,
                         "observed": {"exit": observed["exit"], "stdoutHead": observed["stdout"][:160]}})
    out["F04"] = repeated

    root = os.path.join(work, "deep")
    valid_tree(root, ledger=LEDGER_EMPTY, corpus=False)
    deep = os.path.join(root, "corpus", "knowledge")
    os.makedirs(deep)
    for _ in range(1000):
        deep = os.path.join(deep, "d")
        os.mkdir(deep)
    write(os.path.join(deep, "entry.md"), ENTRY)
    out["F05"] = [judge(run_gate(gate, args_for(root)), 1, "failed",
                        want_exactly=[("unadjudicated_citing_pair", "None")])]

    out["F06"] = [noctty_case(gate)]
    return out


def noctty_case(gate):
    try:
        master, slave = os.openpty()
    except OSError as exc:
        return {"passed": False, "problems": ["no pseudo terminal: %s" % exc], "observed": {}}
    try:
        name = os.ttyname(slave)
        directory, leaf = os.path.split(name)
        command = [sys.executable, "-B", "-c", NOCTTY_WRAPPER, gate, "--root", directory,
                   "--population", leaf, "--ledger", leaf, "--json"]
        try:
            done = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  stdin=subprocess.DEVNULL, timeout=TIMEOUT, start_new_session=True,
                                  env=env_clean())
        except subprocess.TimeoutExpired:
            return {"passed": False, "problems": ["timed out"], "observed": {"device": name}}
    finally:
        os.close(slave)
        os.close(master)
    text = done.stdout.decode("utf-8", "replace")
    marker = [line for line in text.splitlines() if line.startswith("@@NOCTTY ")]
    if not marker:
        return {"passed": False, "problems": ["wrapper printed no result"],
                "observed": {"device": name, "stderrTail": done.stderr.decode("utf-8", "replace")[-300:]}}
    result = json.loads(marker[-1][len("@@NOCTTY "):])
    problems = []
    if result.get("exit") != 2:
        problems.append("exit %s, want 2" % result.get("exit"))
    if result.get("ttyNr") != 0:
        problems.append("tty_nr %s after the run, want 0" % result.get("ttyNr"))
    gate_report = report_of({"stdout": text.split("\n@@NOCTTY ", 1)[0]})
    got = tuples(gate_report)
    if got is None or ["input_invalid", "document_not_regular_file"] not in got:
        problems.append("no finding ['input_invalid', 'document_not_regular_file'] in %s" % got)
    return {"passed": not problems, "problems": problems, "observed": dict(result, device=name, findings=got)}


def controls(gate, work):
    out = []
    root = os.path.join(work, "k-clean")
    valid_tree(root)
    commit_all(root)
    out.append(("K1", judge(run_gate(gate, args_for(root)), 0, "clean", want_exactly=[])))
    out.append(("K2", judge(run_gate(gate, args_for(root) + ["--revision", "HEAD"]), 0, "clean",
                            want_exactly=[])))
    root = os.path.join(work, "k-omission")
    valid_tree(root, ledger=LEDGER_EMPTY)
    out.append(("K3", judge(run_gate(gate, args_for(root)), 1, "failed",
                            want_tuple=("unadjudicated_citing_pair", "None"))))
    return [{"id": k, **v} for k, v in out]


def fixture_codes(tree):
    """Reason codes that committed expected.json files name next to input_invalid."""
    named = {}
    for path in sorted(glob.glob(os.path.join(tree, "scripts", "fixtures", "citing-set", "*", "expected.json"))):
        try:
            with open(path, encoding="utf-8") as handle:
                expected = json.load(handle)
        except (OSError, ValueError):
            continue
        findings = expected.get("findings") if isinstance(expected, dict) else None
        for item in findings if isinstance(findings, list) else []:
            if isinstance(item, dict) and item.get("id") == "input_invalid" and isinstance(item.get("reason"), str):
                named.setdefault(item["reason"], []).append(os.path.basename(os.path.dirname(path)))
    return named


def run_runner(tree, work, label):
    runner = os.path.join(tree, "scripts", "citing_set_selftest.py")
    if not os.path.isfile(runner):
        return {"exit": None, "note": "runner absent"}
    tmp = os.path.join(work, "runner-" + label)
    os.makedirs(tmp, exist_ok=True)
    try:
        done = subprocess.run([sys.executable, "-B", runner, "--root", tree, "--tmpdir", tmp],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
                              timeout=RUNNER_TIMEOUT, cwd=tree, env=env_clean())
    except subprocess.TimeoutExpired:
        return {"exit": None, "note": "runner timed out"}
    summary = report_of({"stdout": done.stdout.decode("utf-8", "replace")}) or {}
    return {"exit": done.returncode, "cases": summary.get("cases"), "failed": summary.get("failed")}


def mutated_runner(tree, work, code):
    copy = os.path.join(work, "mutant-" + code)
    shutil.copytree(tree, copy, symlinks=True)
    gate = os.path.join(copy, "scripts", "citing_set.py")
    with open(gate, encoding="utf-8") as handle:
        source = handle.read()
    occurrences = source.count('"%s"' % code)
    with open(gate, "w", encoding="utf-8") as handle:
        handle.write(source.replace('"%s"' % code, '"%s_mutated"' % code))
    result = run_runner(copy, work, "m-" + code)
    result["renamedOccurrences"] = occurrences
    shutil.rmtree(copy, ignore_errors=True)
    return result


def grade(gate, tree, work, with_runner):
    behaviour = behaviour_cases(gate, os.path.join(work, "b"))
    families = family_cases(gate, os.path.join(work, "f"))
    named = fixture_codes(tree)
    baseline = run_runner(tree, work, "baseline") if with_runner else {"exit": None, "note": "stub"}
    checks = []

    def coded(check_id, code):
        cases = behaviour[code]
        mutant = mutated_runner(tree, work, code) if with_runner and baseline["exit"] == 0 else None
        compared = bool(baseline["exit"] == 0 and mutant and mutant["renamedOccurrences"] > 0
                        and mutant["exit"] not in (0, None))
        parts = {"behaviour": all(c["passed"] for c in cases), "fixture": code in named, "compared": compared}
        checks.append({"id": check_id, "code": code, "passed": all(parts.values()), "parts": parts,
                       "fixtures": named.get(code, []), "mutantRunner": mutant, "cases": cases})

    for index, code in enumerate(R_CODES, start=1):
        coded("R%02d" % index, code)
    coded("F01", DUP)
    coded("F02", NONFINITE)
    for check_id in ("F03", "F04", "F05", "F06"):
        cases = families[check_id]
        checks.append({"id": check_id, "passed": all(c["passed"] for c in cases), "cases": cases})
    return checks, baseline


def export_scripts(root, revision, destination):
    resolved = subprocess.run(["git", "-C", root, "rev-parse", "--verify", "--quiet", revision + "^{commit}"],
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env_clean())
    if resolved.returncode != 0:
        return None
    commit = resolved.stdout.decode().strip()
    archive = subprocess.run(["git", "-C", root, "archive", "--format=tar", commit, "scripts"],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env_clean())
    if archive.returncode != 0:
        return None
    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as bundle:
        bundle.extractall(destination, filter="data")
    return commit


def sha(path):
    try:
        with open(path, "rb") as handle:
            return hashlib.sha256(handle.read()).hexdigest()
    except OSError:
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--scratch", default=SCRATCH)
    args = parser.parse_args()
    root = os.path.abspath(args.root)
    os.makedirs(args.scratch, exist_ok=True)
    work = os.path.join(args.scratch, "run-%d" % os.getpid())
    shutil.rmtree(work, ignore_errors=True)
    tree = os.path.join(work, "tree")
    os.makedirs(tree)
    os.environ["TMPDIR"] = work
    commit = export_scripts(root, args.revision, tree)
    if commit is None:
        print(json.dumps({"error": "cannot export scripts/ at revision", "revision": args.revision}))
        return 2
    gate = os.path.join(tree, "scripts", "citing_set.py")
    result = {
        "counter": ".ufo/waves/round-30/c1_reason_count.py",
        "counterSha256": sha(os.path.abspath(__file__)),
        "revision": commit,
        "gateSha256": sha(gate),
        "runnerSha256": sha(os.path.join(tree, "scripts", "citing_set_selftest.py")),
        "python": sys.version.split()[0],
    }
    control_rows = controls(gate, os.path.join(work, "k"))
    checks, baseline = grade(gate, tree, os.path.join(work, "real"), True)
    stubs = {}
    for label, body in (("constantClean", CLEAN_STUB), ("refuseEverything", REFUSE_STUB)):
        stub_tree = os.path.join(work, "stub-" + label)
        shutil.copytree(tree, stub_tree, symlinks=True)
        stub_gate = os.path.join(stub_tree, "scripts", "citing_set.py")
        write(stub_gate, body)
        stub_checks, stub_baseline = grade(stub_gate, stub_tree, os.path.join(work, "s-" + label), True)
        stubs[label] = {"passed": sum(c["passed"] for c in stub_checks), "runnerExit": stub_baseline["exit"]}
    passed = sum(c["passed"] for c in checks)
    controls_ok = all(row["passed"] for row in control_rows)
    stubs_rejected = all(s["passed"] < len(checks) for s in stubs.values())
    result.update({
        "passed": passed,
        "total": len(checks),
        "rPassed": sum(c["passed"] for c in checks if c["id"].startswith("R")),
        "fPassed": sum(c["passed"] for c in checks if c["id"].startswith("F")),
        "controlsHold": controls_ok,
        "constantGates": stubs,
        "constantGatesRejected": stubs_rejected,
        "runnerBaseline": baseline,
        "controls": control_rows,
        "checks": checks,
    })
    print(json.dumps(result, indent=1))
    print("C1 %d/%d at %s (controls %s, constant gates rejected %s)"
          % (passed, len(checks), commit, controls_ok, stubs_rejected), file=sys.stderr)
    shutil.rmtree(work, ignore_errors=True)
    if not controls_ok:
        return 2
    return 0 if passed == len(checks) and stubs_rejected else 1


if __name__ == "__main__":
    sys.exit(main())
