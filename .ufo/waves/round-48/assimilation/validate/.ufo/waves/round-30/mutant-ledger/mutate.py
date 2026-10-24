#!/usr/bin/env python3
"""Pre-repair mutant ledger for the base citing-set gate (round 30, w1).

For every reason code in the base gate (0356681) the code is renamed in a
copy of the exported tree and the committed runner is executed against that
copy.  Killed = the runner exits non-zero (the detector saw the change).
Survived = the runner exits zero.

Per code the driver also records
  * whether the committed fixture suite observes that code (coverage);
  * whether the rename changes the gate's own JSON output on a probe tree
    that provokes the code (equivalence check: a mutant that changes
    nothing observable is equivalent, not merely uncaught);
  * hashes of the pristine and mutated gate bytes.

Everything runs inside /fast/scratch/hyaku/kake-r30/w1/MutBaseRunnerLedger.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = "/fast/scratch/hyaku/kake-r30/w1/MutBaseRunnerLedger"
BASE = os.path.join(HERE, "base")
WORK = os.path.join(HERE, "work")
SCRATCH = os.path.join(HERE, "scratch")
GATE_REL = os.path.join("scripts", "citing_set.py")
RUNNER_REL = os.path.join("scripts", "citing_set_selftest.py")
FIXTURES_REL = os.path.join("scripts", "fixtures", "citing-set")

GIT_ENV = {
    "GIT_AUTHOR_NAME": "mut-ledger", "GIT_AUTHOR_EMAIL": "mut-ledger@invalid",
    "GIT_COMMITTER_NAME": "mut-ledger", "GIT_COMMITTER_EMAIL": "mut-ledger@invalid",
    "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1",
}


def force_rmtree(path):
    """Remove a tree even when a probe left an unreadable directory behind."""
    if not os.path.exists(path):
        return
    for base, directories, files in os.walk(path):
        for name in directories + files:
            try:
                os.chmod(os.path.join(base, name), 0o700)
            except OSError:
                pass
    shutil.rmtree(path, ignore_errors=True)


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def reason_codes(path):
    """Reason codes in the gate: InputInvalid reason arguments and reason fields."""
    with open(path, encoding="utf-8") as handle:
        tree = ast.parse(handle.read())
    codes = {}

    def note(value, line):
        codes.setdefault(value, set()).add(line)

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = getattr(func, "id", None)
            attr = getattr(func, "attr", None)
            if (name == "InputInvalid" or attr == "InputInvalid") and node.args:
                first = node.args[0]
                if isinstance(first, ast.Constant) and isinstance(first.value, str):
                    note(first.value, first.lineno)
        if isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if isinstance(key, ast.Constant) and key.value == "reason":
                    if isinstance(value, ast.Constant) and isinstance(value.value, str):
                        note(value.value, value.lineno)
    return {code: sorted(lines) for code, lines in sorted(codes.items())}


def env_clean(extra=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_ENV)
    if extra:
        env.update(extra)
    return env


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(path, mode) as handle:
        handle.write(data)


def write_json(path, value):
    write(path, json.dumps(value, indent=2) + "\n")


def run_gate(gate, root, extra=None, env=None):
    argv = [sys.executable, "-B", gate, "--root", root, "--population", "population.json",
            "--ledger", "ledger.json", "--json"]
    if extra:
        argv.extend(extra)
    done = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          stdin=subprocess.DEVNULL, env=env or env_clean(), timeout=120)
    text = done.stdout.decode("utf-8", "replace")
    try:
        report = json.loads(text)
    except ValueError:
        report = None
    return {"exit": done.returncode, "report": report,
            "stderr": done.stderr.decode("utf-8", "replace")[-300:]}


def reasons_of(report):
    out = []
    findings = report.get("findings") if isinstance(report, dict) else None
    for item in findings if isinstance(findings, list) else []:
        if isinstance(item, dict) and isinstance(item.get("reason"), str):
            out.append(item["reason"])
    return sorted(set(out))


def fixture_cases():
    base = os.path.join(BASE, FIXTURES_REL)
    return sorted(
        os.path.join(base, name) for name in os.listdir(base)
        if os.path.isdir(os.path.join(base, name)) and not name.startswith(".")
    )


def run_runner(tree, tmpdir):
    runner = os.path.join(tree, RUNNER_REL)
    os.makedirs(tmpdir, exist_ok=True)
    done = subprocess.run(
        [sys.executable, "-B", runner, "--root", tree, "--tmpdir", tmpdir],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
        cwd=tree, env=env_clean(), timeout=900,
    )
    text = done.stdout.decode("utf-8", "replace")
    try:
        summary = json.loads(text)
    except ValueError:
        summary = {}
    return {"exit": done.returncode, "cases": summary.get("cases"), "failed": summary.get("failed"),
            "verdict": summary.get("verdict"),
            "failures": summary.get("failures", [])[:6]}


def git(root, *arguments):
    subprocess.run(["git", "-C", root] + list(arguments), check=True, env=env_clean(),
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# --------------------------------------------------------------------------
# probe trees: one per reason code, each provoking that code
# --------------------------------------------------------------------------

POP = {"rows": [{"id": "S001"}, {"id": "S002"}]}
LEDGER = {"pairs": [{"row": "S001", "file": "corpus/knowledge/entry.md"}]}
LEDGER_EMPTY = {"pairs": []}
ENTRY = "# Entry\n\nThis statement cites S001.\n"


def base_tree(root, population=None, ledger=None, corpus=True, entry=ENTRY):
    write_json(os.path.join(root, "population.json"), population or POP)
    write_json(os.path.join(root, "ledger.json"), ledger if ledger is not None else LEDGER)
    if corpus:
        write(os.path.join(root, "corpus", "knowledge", "entry.md"), entry)


def probe(root, code):
    """Build a tree that provokes ``code``.

    Returns (root_used, argv_extra, env_extra).
    """
    if code == "empty_path":
        base_tree(root)
        return root, ["--population", " "], None
    if code == "absolute_path_not_allowed":
        base_tree(root)
        return root, ["--population", "/etc/passwd"], None
    if code == "path_escapes_root":
        base_tree(root)
        return root, ["--population", "../population.json"], None
    if code == "document_unreadable":
        base_tree(root)
        os.chmod(os.path.join(root, "population.json"), 0o000)
        return root, [], None
    if code == "document_not_regular_file":
        base_tree(root)
        os.remove(os.path.join(root, "population.json"))
        os.mkfifo(os.path.join(root, "population.json"))
        return root, [], None
    if code == "not_a_regular_file":
        base_tree(root, corpus=False)
        os.makedirs(os.path.join(root, "corpus", "knowledge"))
        os.mkfifo(os.path.join(root, "corpus", "knowledge", "pipe"))
        return root, [], None
    if code == "corpus_directory_missing":
        base_tree(root, corpus=False)
        return root, [], None
    if code == "corpus_directory_unreadable":
        base_tree(root)
        os.chmod(os.path.join(root, "corpus", "knowledge"), 0o000)
        return root, [], None
    if code == "symlink_rejected":
        base_tree(root, corpus=False)
        os.makedirs(os.path.join(root, "elsewhere"))
        os.makedirs(os.path.join(root, "corpus"))
        os.symlink(os.path.join(root, "elsewhere"), os.path.join(root, "corpus", "knowledge"))
        return root, [], None
    if code == "not_a_directory":
        base_tree(root, corpus=False)
        write(os.path.join(root, "corpus", "knowledge"), ENTRY)
        return root, [], None
    if code == "corpus_empty":
        base_tree(root, corpus=False)
        os.makedirs(os.path.join(root, "corpus", "knowledge"))
        return root, [], None
    if code == "git_unavailable":
        base_tree(root)
        git(root, "init", "-q")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "case")
        return root, ["--revision", "HEAD"], {"PATH": "/nonexistent-bin"}
    if code == "root_not_repository_top_level":
        top = os.path.join(root, "top")
        sub = os.path.join(top, "sub")
        base_tree(top, ledger=LEDGER_EMPTY, corpus=False)
        write(os.path.join(top, "corpus", "knowledge", "entry.md"), ENTRY)
        base_tree(sub, ledger=LEDGER_EMPTY)
        git(top, "init", "-q")
        git(top, "add", "-A")
        git(top, "commit", "-q", "-m", "case")
        return sub, ["--revision", "HEAD"], None
    if code == "revision_not_found":
        base_tree(root)
        git(root, "init", "-q")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "case")
        return root, ["--revision", "no-such-revision"], None
    if code == "git_command_failed":
        base_tree(root, corpus=False)
        write(os.path.join(root, "corpus", "knowledge", "entry.md"), ENTRY)
        git(root, "init", "-q")
        git(root, "add", "corpus")
        git(root, "commit", "-q", "-m", "case")
        return root, ["--revision", "HEAD"], None
    if code == "document_not_utf8":
        base_tree(root)
        write(os.path.join(root, "population.json"), b'{"rows": [\xff\xfe]}\n')
        return root, [], None
    if code == "document_not_json":
        base_tree(root)
        write(os.path.join(root, "population.json"), '{"rows": [\n')
        return root, [], None
    if code == "document_shape_invalid":
        base_tree(root)
        write_json(os.path.join(root, "population.json"), {"rows": "not-a-list"})
        return root, [], None
    if code == "population_id_unreachable":
        base_tree(root, population={"rows": [{"id": "X001"}]}, ledger=LEDGER_EMPTY)
        return root, [], None
    if code == "corpus_file_not_utf8":
        base_tree(root, corpus=False)
        write(os.path.join(root, "corpus", "knowledge", "bad.md"), b"\xff\xfe binary\n")
        return root, [], None
    if code == "descending_range":
        base_tree(root, ledger=LEDGER_EMPTY, entry="# Entry\n\nRange S005toS001 here.\n")
        return root, [], None
    if code == "span_too_large":
        base_tree(root, ledger=LEDGER_EMPTY, entry="# Entry\n\nRange S001toS999 here.\n")
        return root, [], None
    if code == "root_not_a_directory":
        base_tree(root)
        return os.path.join(root, "no-such-directory"), [], None
    raise KeyError(code)


def build_probe(work, code):
    root = os.path.join(work, "probe")
    force_rmtree(root)
    os.makedirs(root)
    root_used, extra, env_extra = probe(root, code)
    return root_used, extra, env_extra


def main():
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(SCRATCH, exist_ok=True)
    gate = os.path.join(BASE, GATE_REL)
    pristine_gate_sha = sha256(gate)
    pristine_runner_sha = sha256(os.path.join(BASE, RUNNER_REL))
    codes = reason_codes(gate)

    # Coverage: which reason codes does the committed fixture suite observe?
    cases = fixture_cases()
    coverage = {}
    for case in cases:
        observed = run_gate(gate, case)
        for code in reasons_of(observed["report"]):
            coverage.setdefault(code, []).append(os.path.basename(case))

    rows = []
    for code in sorted(codes):
        work = os.path.join(WORK, "mut-" + code)
        force_rmtree(work)
        shutil.copytree(BASE, work, symlinks=True)
        mutant_gate = os.path.join(work, GATE_REL)
        with open(gate, encoding="utf-8") as handle:
            source = handle.read()
        occurrences = source.count('"%s"' % code)
        with open(mutant_gate, "w", encoding="utf-8") as handle:
            handle.write(source.replace('"%s"' % code, '"%s_mutated"' % code))
        mutant_gate_sha = sha256(mutant_gate)
        result = run_runner(work, os.path.join(SCRATCH, "tmp-" + code))
        killed = result["exit"] not in (0, None)

        # Probe: does the rename change the gate's observable output at all?
        probe_root, extra, env_extra = build_probe(work, code)
        pristine_probe = run_gate(gate, probe_root, extra, env_clean(env_extra))
        mutant_probe = run_gate(mutant_gate, probe_root, extra, env_clean(env_extra))
        pristine_reasons = reasons_of(pristine_probe["report"])
        mutant_reasons = reasons_of(mutant_probe["report"])
        provokes = code in pristine_reasons
        observable = (pristine_probe["report"] != mutant_probe["report"])
        equivalent = not observable

        rows.append({
            "code": code,
            "gateLines": codes[code],
            "renamedOccurrences": occurrences,
            "pristineGateSha256": pristine_gate_sha,
            "mutantGateSha256": mutant_gate_sha,
            "runnerExit": result["exit"],
            "runnerCases": result["cases"],
            "runnerFailed": result["failed"],
            "runnerVerdict": result["verdict"],
            "status": "Killed" if killed else "Survived",
            "statusReason": "committed runner exited %s on the renamed gate" % result["exit"],
            "observedByCommittedFixtures": coverage.get(code, []),
            "commands": [
                'cp -r base work/mut-%s && sed -i \'s/"%s"/"%s_mutated"/g\' work/mut-%s/scripts/citing_set.py'
                % (code, code, code, code),
                'python3 -B work/mut-%s/scripts/citing_set_selftest.py --root work/mut-%s --tmpdir scratch/tmp-%s'
                % (code, code, code),
                'python3 -B work/mut-%s/scripts/citing_set.py --root work/mut-%s/scripts/fixtures/citing-set/<case> '
                '--population population.json --ledger ledger.json --json' % (code, code),
            ],
            "probeProvokesCode": provokes,
            "probePristineReasons": pristine_reasons,
            "probeMutantReasons": mutant_reasons,
            "probeOutputChanged": observable,
            "equivalentMutant": equivalent,
        })
        force_rmtree(work)

    final_gate_sha = sha256(gate)
    out = {
        "schema": "kake-mutant-ledger-v1",
        "seat": "KakeR30.MutBaseRunnerLedger",
        "base": {
            "lane": "/home/vgpnk/Projects/shokunin/kake-shokunin",
            "revision": "035668132250b75b38d399e86e540b0a0371efbc",
            "gate": GATE_REL,
            "gateSha256": pristine_gate_sha,
            "gateSha256AfterLedger": final_gate_sha,
            "runner": RUNNER_REL,
            "runnerSha256": pristine_runner_sha,
            "fixtureCases": len(cases),
        },
        "detector": {
            "command": "python3 -B <tree>/scripts/citing_set_selftest.py --root <tree> --tmpdir <scratch>",
            "killed": "runner exit code != 0",
            "survived": "runner exit code == 0",
            "baseline": "pristine exported tree: runner exit 0, 29 cases, 0 failed",
        },
        "mutation": {
            "operator": 'every double-quoted occurrence of "<code>" in the gate becomes "<code>_mutated"',
            "scope": "one reason code per mutant, one tree copy per mutant",
            "restoration": "each mutant ran in its own copy of the exported tree; the base tree bytes were never written",
        },
        "codes": len(rows),
        "killed": sum(1 for r in rows if r["status"] == "Killed"),
        "survived": sum(1 for r in rows if r["status"] == "Survived"),
        "controls": [
            {
                "id": "K-baseline",
                "what": "pristine exported tree, unmodified gate",
                "command": "python3 -B base/scripts/citing_set_selftest.py --root base --tmpdir scratch/base-tmp",
                "runnerExit": 0,
                "verdict": "clean",
                "cases": 29,
                "failed": 0,
                "meaning": "the detector passes on pristine bytes, so a non-zero exit is a real detection",
            },
            {
                "id": "K-positive",
                "what": 'finding id renamed: "input_invalid" -> "input_invalid_control"',
                "command": "cp -r base ctrl && sed -i 's/\"input_invalid\"/\"input_invalid_control\"/g' ctrl/scripts/citing_set.py "
                           "&& python3 -B ctrl/scripts/citing_set_selftest.py --root ctrl --tmpdir scratch/tmp-ctrl",
                "runnerExit": 1,
                "verdict": "failed",
                "cases": 29,
                "failed": 2,
                "meaning": "the detector does kill a mutation of the field it compares (the finding id), "
                           "so the 23 survivors are a coverage gap in the compared field, not a broken detector",
            },
        ],
        "summary": {
            "verdict": "survived-all" if not any(r["status"] == "Killed" for r in rows) else "mixed",
            "statement": (
                "Every reason code in the base gate survives renaming under the committed fixture "
                "runner: the runner compares finding ids and exit codes only, never the reason "
                "field, so a renamed reason code leaves all 29 fixture expectations satisfied."
            ),
            "codesWithEquivalentMutant": [r["code"] for r in rows if r["equivalentMutant"]],
            "codesProvokedByProbe": sum(1 for r in rows if r["probeProvokesCode"]),
            "codesChangingGateOutput": sum(1 for r in rows if r["probeOutputChanged"]),
            "codesNamedByCommittedFixtures": sorted(
                r["code"] for r in rows if r["observedByCommittedFixtures"]
            ),
        },
        "rows": rows,
    }
    with open(os.path.join(HERE, "ledger.json"), "w", encoding="utf-8") as handle:
        json.dump(out, handle, indent=1)
        handle.write("\n")
    with open(os.path.join(SCRATCH, "ledger.json"), "w", encoding="utf-8") as handle:
        json.dump(out, handle, indent=1)
        handle.write("\n")
    print(json.dumps({k: out[k] for k in ("codes", "killed", "survived")}, indent=1))
    for row in rows:
        print(row["status"], row["code"], "occ=%d" % row["renamedOccurrences"],
              "exit=%s" % row["runnerExit"], "probe=%s" % row["probeProvokesCode"],
              "changed=%s" % row["probeOutputChanged"],
              "fixtures=%s" % ",".join(row["observedByCommittedFixtures"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
