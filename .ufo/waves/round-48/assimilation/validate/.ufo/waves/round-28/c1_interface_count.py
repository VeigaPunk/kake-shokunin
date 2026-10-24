#!/usr/bin/env python3
"""Round-28 C1 counter: citing-set gate interface checks at one commit.

Usage:
    python3 -B .ufo/waves/round-28/c1_interface_count.py --root <lane> --revision <commit>

The counter exports ``scripts/`` from the named commit (committed bytes
only, never the working tree) into a scratch directory, then runs that
commit's ``scripts/citing_set.py`` against cases it builds itself.

Defect checks (round-27 routed defect 1, from the round-27 verifier note):
unusable input documents must yield the contracted JSON report and exit 2,
and an absent or unreachable corpus surface must not return clean.  A defect
check passes when, within the timeout, the gate exits 2 and stdout is one
JSON object carrying ``verdict`` = ``could-not-evaluate``, integer
``citingPairs`` and ``ledgerPairs``, and a ``findings`` list holding at least
one ``input_invalid`` finding.

Control checks stop a gate that refuses everything: a valid working-tree
case must stay ``clean`` (exit 0), the same case read through Git must stay
``clean`` (exit 0), a missing ledger pair must stay ``failed`` (exit 1) with
an ``unadjudicated_citing_pair`` finding, and the commit's own fixture
runner (``scripts/citing_set_selftest.py`` over ``scripts/fixtures/citing-set``)
must exit 0.

Output: one JSON document with every check; ``passed`` / ``total`` is the
claim value.  Exit 0 when every check passes, 1 otherwise, 2 when the
commit cannot be exported.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tarfile
import io

TIMEOUT_SECONDS = 20
SELFTEST_TIMEOUT_SECONDS = 600
SCRATCH_PARENT = "/fast/scratch/hyaku/kake-r28/c1-count"
CONTRACT_KEYS = ("verdict", "citingPairs", "ledgerPairs", "findings")

POPULATION = {"rows": [{"id": "S001"}, {"id": "S002"}]}
LEDGER_CLEAN = {"pairs": [{"row": "S001", "file": "corpus/knowledge/entry.md"}]}
LEDGER_MISSING = {"pairs": []}
ENTRY = "# Entry\n\nThis statement cites S001.\n"
UNCITED_ENTRY = "# Entry\n\nThis statement cites nothing.\n"
GIT_ENV = {
    "GIT_AUTHOR_NAME": "c1-count",
    "GIT_AUTHOR_EMAIL": "c1-count@invalid",
    "GIT_COMMITTER_NAME": "c1-count",
    "GIT_COMMITTER_EMAIL": "c1-count@invalid",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
}


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(path, mode) as handle:
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
    env = dict(os.environ)
    env.update(GIT_ENV)
    subprocess.run(["git", "-C", root] + list(arguments), check=True, env=env,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def commit_all(root):
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "case")


def deep_json(depth):
    return '{"rows": ' + "[" * depth + "]" * depth + ', "pairs": ' + "[" * depth + "]" * depth + "}\n"


def run_gate(gate, arguments):
    command = [sys.executable, "-B", gate] + arguments
    try:
        done = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              stdin=subprocess.DEVNULL, timeout=TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        return {"exit": None, "timedOut": True, "stdoutHead": "", "stderrTail": ""}
    return {
        "exit": done.returncode,
        "timedOut": False,
        "stdout": done.stdout.decode("utf-8", "replace"),
        "stderrTail": done.stderr.decode("utf-8", "replace")[-400:],
    }


def parse_object(stdout):
    try:
        value = json.loads(stdout)
    except (ValueError, RecursionError):
        return None
    return value if isinstance(value, dict) else None


def judge(observed, want_exit, want_verdict, want_finding):
    report = parse_object(observed.get("stdout", ""))
    reasons = []
    if observed["timedOut"]:
        reasons.append("timed out after %ss" % TIMEOUT_SECONDS)
    if observed["exit"] != want_exit:
        reasons.append("exit %s, want %s" % (observed["exit"], want_exit))
    if report is None:
        reasons.append("stdout is not one JSON object")
    else:
        missing = [key for key in CONTRACT_KEYS if key not in report]
        if missing:
            reasons.append("missing keys " + ",".join(missing))
        if report.get("verdict") != want_verdict:
            reasons.append("verdict %r, want %r" % (report.get("verdict"), want_verdict))
        for key in ("citingPairs", "ledgerPairs"):
            if key in report and (not isinstance(report[key], int) or isinstance(report[key], bool)):
                reasons.append(key + " not an integer")
        findings = report.get("findings")
        if not isinstance(findings, list):
            reasons.append("findings not a list")
        elif want_finding is not None and not any(
            isinstance(item, dict) and item.get("id") == want_finding for item in findings
        ):
            reasons.append("no %s finding" % want_finding)
        elif want_finding is None and findings:
            reasons.append("findings present, want none")
    summary = {
        "exit": observed["exit"],
        "timedOut": observed["timedOut"],
        "verdict": report.get("verdict") if report else None,
        "findingReasons": sorted(
            str(item.get("reason")) for item in (report or {}).get("findings", []) or []
            if isinstance(item, dict) and item.get("id") == "input_invalid"
        ) if report and isinstance(report.get("findings"), list) else [],
    }
    if report is None:
        summary["stdoutHead"] = observed.get("stdout", "")[:200]
        summary["stderrTail"] = observed.get("stderrTail", "")
    return not reasons, reasons, summary


def defect(gate, arguments):
    return judge(run_gate(gate, arguments), 2, "could-not-evaluate", "input_invalid")


def build_cases(gate, work):
    cases = []

    def add(case_id, kind, attacks, outcome):
        passed, reasons, summary = outcome
        cases.append({"id": case_id, "kind": kind, "attacks": attacks, "passed": passed,
                      "reasons": reasons, "observed": summary})

    def wt_args(root, population="population.json", ledger="ledger.json"):
        return ["--root", root, "--population", population, "--ledger", ledger, "--json"]

    # U1/U2: a FIFO population or ledger must be refused, not waited on.
    for case_id, target in (("U1-population-fifo", "population.json"), ("U2-ledger-fifo", "ledger.json")):
        root = os.path.join(work, case_id)
        valid_tree(root)
        os.remove(os.path.join(root, target))
        os.mkfifo(os.path.join(root, target))
        add(case_id, "defect", "unusable input document (CLI-FIFO)", defect(gate, wt_args(root)))

    # U3/U4: deeply nested JSON must yield the JSON report, not a traceback.
    for case_id, target in (("U3-population-deep-json", "population.json"), ("U4-ledger-deep-json", "ledger.json")):
        root = os.path.join(work, case_id)
        valid_tree(root)
        write(os.path.join(root, target), deep_json(200000))
        add(case_id, "defect", "unusable input document (JSON-PROTOCOL depth)", defect(gate, wt_args(root)))

    # A1-A4 use an empty ledger: with no corpus surface read, the round-27
    # gate's result for these inputs is the false green ``clean``.
    # A1: absent corpus surface in the working tree.
    root = os.path.join(work, "A1-corpus-absent-working-tree")
    valid_tree(root, ledger=LEDGER_MISSING, corpus=False)
    add("A1-corpus-absent-working-tree", "defect", "absent corpus surface (CLI-SCOPE-FALSE-GREEN)",
        defect(gate, wt_args(root)))

    # A2: absent corpus surface at a Git revision.
    root = os.path.join(work, "A2-corpus-absent-git")
    valid_tree(root, ledger=LEDGER_MISSING, corpus=False)
    commit_all(root)
    add("A2-corpus-absent-git", "defect", "absent corpus surface at a revision (CLI-SCOPE-FALSE-GREEN)",
        defect(gate, wt_args(root) + ["--revision", "HEAD"]))

    # A3: empty corpus directory in the working tree.
    root = os.path.join(work, "A3-corpus-empty-working-tree")
    valid_tree(root, ledger=LEDGER_MISSING, corpus=False)
    os.makedirs(os.path.join(root, "corpus", "knowledge"))
    add("A3-corpus-empty-working-tree", "defect", "empty corpus surface (CLI-SCOPE-FALSE-GREEN)",
        defect(gate, wt_args(root)))

    # A4: corpus/knowledge committed as a file, not a directory.
    root = os.path.join(work, "A4-corpus-blob-git")
    valid_tree(root, ledger=LEDGER_MISSING, corpus=False)
    write(os.path.join(root, "corpus", "knowledge"), UNCITED_ENTRY)
    commit_all(root)
    add("A4-corpus-blob-git", "defect", "corpus surface is a blob at a revision (CLI-SCOPE-FALSE-GREEN)",
        defect(gate, wt_args(root) + ["--revision", "HEAD"]))

    # A5: a population whose ids the citation grammar can never produce.
    root = os.path.join(work, "A5-population-unreachable-id")
    valid_tree(root, population={"rows": [{"id": "X001"}]}, ledger=LEDGER_MISSING)
    add("A5-population-unreachable-id", "defect", "unreachable population ids (CLI-SCOPE-FALSE-GREEN)",
        defect(gate, wt_args(root)))

    # A6: a blank revision must not silently read the working tree.
    root = os.path.join(work, "A6-blank-revision")
    valid_tree(root)
    commit_all(root)
    add("A6-blank-revision", "defect", "blank revision measures the working tree (CLI-SCOPE-FALSE-GREEN)",
        defect(gate, wt_args(root) + ["--revision", ""]))

    # A7: a root nested inside a repository, read at a revision.  The
    # top-level tree holds an uncited entry; the nested root's own entry
    # cites S001 with no ledger pair.  Reading the top-level blobs instead
    # of the nested surface is a wrong-surface false green.
    top = os.path.join(work, "A7-nested-git-root")
    root = os.path.join(top, "sub")
    valid_tree(top, ledger=LEDGER_MISSING, corpus=False)
    write(os.path.join(top, "corpus", "knowledge", "entry.md"), UNCITED_ENTRY)
    valid_tree(root, ledger=LEDGER_MISSING)
    commit_all(top)
    add("A7-nested-git-root", "defect", "nested Git root reads a wrong surface (CLI-SCOPE-FALSE-GREEN)",
        defect(gate, wt_args(root) + ["--revision", "HEAD"]))

    # K1-K3: controls that a refuse-everything gate fails.
    root = os.path.join(work, "K1-K2-valid-clean")
    valid_tree(root)
    commit_all(root)
    add("K1-valid-clean-working-tree", "control", "gate that refuses valid input",
        judge(run_gate(gate, wt_args(root)), 0, "clean", None))
    add("K2-valid-clean-git", "control", "gate that refuses valid Git input",
        judge(run_gate(gate, wt_args(root) + ["--revision", "HEAD"]), 0, "clean", None))
    root = os.path.join(work, "K3-valid-failed")
    valid_tree(root, ledger=LEDGER_MISSING)
    add("K3-valid-failed-missing-pair", "control", "gate that hides a real omission",
        judge(run_gate(gate, wt_args(root)), 1, "failed", "unadjudicated_citing_pair"))
    return cases


def selftest_case(tree, work):
    runner = os.path.join(tree, "scripts", "citing_set_selftest.py")
    command = [sys.executable, "-B", runner, "--root", tree, "--tmpdir", os.path.join(work, "selftest-tmp")]
    try:
        done = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              stdin=subprocess.DEVNULL, timeout=SELFTEST_TIMEOUT_SECONDS, cwd=tree)
        exit_code, timed_out = done.returncode, False
        out = done.stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        exit_code, timed_out, out = None, True, ""
    summary = parse_object(out) or {}
    observed = {"exit": exit_code, "timedOut": timed_out}
    for key in ("total", "passed", "failed", "cases"):
        if isinstance(summary.get(key), (int, str)):
            observed[key] = summary[key]
    passed = exit_code == 0
    return {"id": "K4-fixture-selftest", "kind": "control", "attacks": "gate that breaks the 29 fixture outcomes",
            "passed": passed, "reasons": [] if passed else ["selftest exit %s" % exit_code], "observed": observed}


def export_scripts(root, revision, destination):
    resolved = subprocess.run(["git", "-C", root, "rev-parse", "--verify", "--quiet", revision + "^{commit}"],
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if resolved.returncode != 0:
        return None
    commit = resolved.stdout.decode().strip()
    archive = subprocess.run(["git", "-C", root, "archive", "--format=tar", commit, "scripts"],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if archive.returncode != 0:
        return None
    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as bundle:
        bundle.extractall(destination, filter="data")
    return commit


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--scratch", default=SCRATCH_PARENT)
    args = parser.parse_args()
    root = os.path.abspath(args.root)
    os.makedirs(args.scratch, exist_ok=True)
    work = os.path.join(args.scratch, "run-%d" % os.getpid())
    if os.path.exists(work):
        shutil.rmtree(work)
    tree = os.path.join(work, "tree")
    os.makedirs(tree)
    commit = export_scripts(root, args.revision, tree)
    if commit is None:
        print(json.dumps({"error": "cannot export scripts/ at revision", "revision": args.revision}))
        return 2
    gate = os.path.join(tree, "scripts", "citing_set.py")
    cases = build_cases(gate, os.path.join(work, "cases"))
    cases.append(selftest_case(tree, work))
    passed = sum(1 for case in cases if case["passed"])
    result = {
        "counter": ".ufo/waves/round-28/c1_interface_count.py",
        "revision": commit,
        "passed": passed,
        "total": len(cases),
        "defectPassed": sum(1 for case in cases if case["kind"] == "defect" and case["passed"]),
        "defectTotal": sum(1 for case in cases if case["kind"] == "defect"),
        "controlPassed": sum(1 for case in cases if case["kind"] == "control" and case["passed"]),
        "controlTotal": sum(1 for case in cases if case["kind"] == "control"),
        "cases": cases,
    }
    print(json.dumps(result, indent=2))
    shutil.rmtree(work, ignore_errors=True)
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
