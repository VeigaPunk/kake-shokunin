#!/usr/bin/env python3
"""Round-30 C1 strict supplement: closure checks that close the holes wave-1
critic CriticC1Counter found in the declared counter c1_reason_count.py.

It does not replace the declared counter or its 14/14 target. It is declared
before any after-measurement as an additional closure check, and both must
pass at the landed commit. It reuses the declared counter's case builders
(imported from the sibling file) and exports ``scripts/`` from the named
commit the same way.

Strict checks (each must hold for every listed code or variant):
  S1 exact refusal: every counter-built refusal case for the ten codes
     (eight round-28 codes plus document_duplicate_key and
     document_nonfinite_number) returns exactly one finding,
     (input_invalid, <code>), not a list that merely contains it.
  S2 rename precision: with every double-quoted occurrence of the code
     renamed to <code>_mutated in the exported gate, (a) the counter-built
     case now emits exactly (input_invalid, <code>_mutated), so the emitted
     code comes from the renamed string, and (b) the committed runner fails,
     and every committed fixture that names the code is among its failing
     cases.
  S3 repeated options in every spelling: two usable values, the
     --name=value form, the mixed form and an argparse prefix abbreviation,
     for each of --root, --revision, --population and --ledger, each exit 64;
     the same tree with each option once exits 0 clean.
  S4 deep corpus tuple: the 1000-deep case returns exactly one finding with
     id unadjudicated_citing_pair, row S001 and the deep file path.
  S5 O_NOCTTY observed: the gate runs in-process in a new session with os.open
     recorded; the terminal device is opened with O_NOCTTY in its flags, the
     run exits 2 with finding (input_invalid, document_not_regular_file), and
     tty_nr stays 0.
  S6 JSON profile everywhere: duplicate member names and non-finite numbers
     are refused with exactly one finding of the right reason in the ledger
     as well as the population, nested inside a row or pair object, and for
     an overflowing literal (1e999).
  S3 also requires the usage object: verdict could-not-evaluate, empty
     findings and an "error" string starting "usage:".

Usage: python3 -B c1_strict_checks.py --root <lane> --revision <commit>
Exit 0 when every strict check holds; 1 otherwise; 2 on bad input.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location("c1count", os.path.join(HERE, "c1_reason_count.py"))
C = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(C)
SCRATCH = "/fast/scratch/hyaku/kake-r30/c1-strict"
CODES = C.R_CODES + [C.DUP, C.NONFINITE]

TRACE_WRAPPER = r'''
import json, os, runpy, sys
calls = []
real_open = os.open
def traced(path, flags, *rest, **kw):
    calls.append([os.fspath(path) if not isinstance(path, int) else path, flags])
    return real_open(path, flags, *rest, **kw)
os.open = traced
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
sys.stdout.write("\n@@TRACE " + json.dumps({"exit": code, "ttyNr": tty, "calls": [[str(p), f] for p, f in calls],
                                           "noctty": getattr(os, "O_NOCTTY", 0)}) + "\n")
'''


def exact(gate, arguments, code):
    return C.judge(C.run_gate(gate, arguments), 2, "could-not-evaluate", want_exactly=[("input_invalid", code)])


def strict_cases(gate, work, code_name=None):
    """Re-run the declared builders, judging exact finding lists.

    code_name maps a code to the code the gate is expected to emit (for the
    rename check)."""
    code_name = code_name or (lambda code: code)
    out = {}
    original_refused = C.refused
    C.refused = lambda g, a, code: exact(g, a, code_name(code))
    try:
        out = C.behaviour_cases(gate, work)
    finally:
        C.refused = original_refused
    return out


def runner_rows(tree, work, label):
    runner = os.path.join(tree, "scripts", "citing_set_selftest.py")
    tmp = os.path.join(work, "runner-" + label)
    os.makedirs(tmp, exist_ok=True)
    done = subprocess.run([sys.executable, "-B", runner, "--root", tree, "--tmpdir", tmp],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
                          timeout=C.RUNNER_TIMEOUT, cwd=tree, env=C.env_clean())
    summary = C.report_of({"stdout": done.stdout.decode("utf-8", "replace")}) or {}
    failing = set()
    for key in ("results", "rows", "cases"):
        value = summary.get(key)
        if isinstance(value, list):
            for row in value:
                if isinstance(row, dict) and not row.get("passed", row.get("ok", False)):
                    failing.add(str(row.get("case") or row.get("name") or row.get("id")))
    return done.returncode, failing, summary


def s2(tree, work, named):
    results = []
    for code in CODES:
        copy = os.path.join(work, "mut-" + code)
        shutil.copytree(tree, copy, symlinks=True)
        gate = os.path.join(copy, "scripts", "citing_set.py")
        with open(gate, encoding="utf-8") as handle:
            source = handle.read()
        with open(gate, "w", encoding="utf-8") as handle:
            handle.write(source.replace('"%s"' % code, '"%s_mutated"' % code))
        cases = strict_cases(gate, os.path.join(work, "mutcases-" + code),
                             code_name=lambda c, code=code: c + "_mutated" if c == code else c)[code]
        exit_code, failing, _ = runner_rows(copy, work, "m-" + code)
        expected_failing = set(named.get(code, []))
        problems = []
        if not all(case["passed"] for case in cases):
            problems.append("renamed gate does not emit %s_mutated exactly" % code)
        if exit_code != 1:
            problems.append("runner exit %s on the renamed gate, want 1 (case mismatch)" % exit_code)
        if not expected_failing:
            problems.append("no committed fixture names the code")
        elif not expected_failing <= failing:
            problems.append("fixtures naming the code not all failing: %s not in %s"
                            % (sorted(expected_failing - failing), sorted(failing)))
        results.append({"code": code, "passed": not problems, "problems": problems,
                        "runnerExit": exit_code, "failingCases": sorted(failing),
                        "fixturesNamingCode": sorted(expected_failing)})
        shutil.rmtree(copy, ignore_errors=True)
    return results


def s3(gate, work):
    root = os.path.join(work, "repeat")
    C.valid_tree(root)
    C.commit_all(root)
    base = ["--population", "population.json", "--ledger", "ledger.json", "--json"]
    variants = {}
    for option, value in (("--population", "population.json"), ("--ledger", "ledger.json"),
                          ("--revision", "HEAD"), ("--root", root)):
        full = ["--root", root, "--population", "population.json", "--ledger", "ledger.json",
                "--revision", "HEAD", "--json"]
        index = full.index(option)
        others = full[:index] + full[index + 2:]
        prefix = option[:5]  # --pop, --led, --rev, --roo
        variants[option + " twice"] = others + [option, value, option, value]
        variants[option + "=value twice"] = others + ["%s=%s" % (option, value)] * 2
        variants[option + " mixed"] = others + [option, value, "%s=%s" % (option, value)]
        variants[option + " abbreviated"] = others + [option, value, prefix, value]
    out = []
    for label, arguments in variants.items():
        observed = C.run_gate(gate, arguments)
        report = C.report_of(observed) or {}
        usage_ok = (report.get("verdict") == "could-not-evaluate" and report.get("findings") == []
                    and str(report.get("error", "")).startswith("usage:"))
        out.append({"variant": label, "passed": observed["exit"] == 64 and usage_ok,
                    "exit": observed["exit"], "usageObject": usage_ok})
    once = C.judge(C.run_gate(gate, ["--root", root] + base + ["--revision", "HEAD"]), 0, "clean", want_exactly=[])
    out.append({"variant": "each option once", "passed": once["passed"], "observed": once["observed"]})
    return out


def s6(gate, work):
    cases = [
        ("ledger-dup", "ledger.json",
         '{"pairs": [{"row": "S001", "file": "corpus/knowledge/entry.md"}], "pairs": []}\n', C.DUP),
        ("row-dup", "population.json", '{"rows": [{"id": "S001", "id": "S002"}]}\n', C.DUP),
        ("ledger-nan", "ledger.json",
         '{"pairs": [{"row": "S001", "file": "corpus/knowledge/entry.md", "w": NaN}]}\n', C.NONFINITE),
        ("row-inf", "population.json", '{"rows": [{"id": "S001", "w": Infinity}, {"id": "S002"}]}\n',
         C.NONFINITE),
        ("overflow", "population.json", '{"rows": [{"id": "S001"}, {"id": "S002"}], "w": 1e999}\n',
         C.NONFINITE),
    ]
    out = []
    for label, target, text, code in cases:
        root = os.path.join(work, label)
        C.valid_tree(root)
        C.write(os.path.join(root, target), text)
        judged = exact(gate, C.args_for(root), code)
        out.append({"case": label, "passed": judged["passed"], "problems": judged["problems"]})
    return out


def s4(gate, work):
    root = os.path.join(work, "deep")
    C.valid_tree(root, ledger=C.LEDGER_EMPTY, corpus=False)
    deep = os.path.join(root, "corpus", "knowledge")
    os.makedirs(deep)
    for _ in range(1000):
        deep = os.path.join(deep, "d")
        os.mkdir(deep)
    C.write(os.path.join(deep, "entry.md"), C.ENTRY)
    observed = C.run_gate(gate, C.args_for(root))
    report = C.report_of(observed) or {}
    findings = report.get("findings") if isinstance(report.get("findings"), list) else []
    want_file = "corpus/knowledge/" + "d/" * 1000 + "entry.md"
    ok = (observed["exit"] == 1 and len(findings) == 1 and isinstance(findings[0], dict)
          and findings[0].get("id") == "unadjudicated_citing_pair"
          and str(findings[0].get("row")) in ("S001", "1") and findings[0].get("file") == want_file)
    return {"passed": ok, "exit": observed["exit"],
            "finding": {k: (v if k != "file" else (str(v)[:40] + "…" + str(v)[-20:]))
                        for k, v in (findings[0].items() if findings and isinstance(findings[0], dict) else [])}}


def s5(gate):
    master, slave = os.openpty()
    try:
        name = os.ttyname(slave)
        directory, leaf = os.path.split(name)
        done = subprocess.run([sys.executable, "-B", "-c", TRACE_WRAPPER, gate, "--root", directory,
                               "--population", leaf, "--ledger", leaf, "--json"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
                              timeout=C.TIMEOUT, start_new_session=True, env=C.env_clean())
    finally:
        os.close(slave)
        os.close(master)
    text = done.stdout.decode("utf-8", "replace")
    marker = [line for line in text.splitlines() if line.startswith("@@TRACE ")]
    if not marker:
        return {"passed": False, "problems": ["no trace"]}
    trace = json.loads(marker[-1][len("@@TRACE "):])
    device_opens = [c for c in trace["calls"] if os.path.realpath(os.path.join(directory, c[0])) == name
                    or c[0] == name or os.path.basename(c[0]) == leaf]
    got = C.tuples(C.report_of({"stdout": text.split("\n@@TRACE ", 1)[0]}))
    problems = []
    if not device_opens:
        problems.append("device never opened through os.open")
    elif not all(flags & trace["noctty"] for _, flags in device_opens):
        problems.append("device opened without O_NOCTTY: %s" % device_opens)
    if trace["exit"] != 2:
        problems.append("exit %s" % trace["exit"])
    if trace["ttyNr"] != 0:
        problems.append("tty_nr %s" % trace["ttyNr"])
    if got is None or ["input_invalid", "document_not_regular_file"] not in got:
        problems.append("findings %s" % got)
    return {"passed": not problems, "problems": problems, "deviceOpens": device_opens, "ttyNr": trace["ttyNr"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--scratch", default=SCRATCH)
    args = parser.parse_args()
    os.makedirs(args.scratch, exist_ok=True)
    work = os.path.join(args.scratch, "run-%d" % os.getpid())
    shutil.rmtree(work, ignore_errors=True)
    tree = os.path.join(work, "tree")
    os.makedirs(tree)
    os.environ["TMPDIR"] = work
    commit = C.export_scripts(os.path.abspath(args.root), args.revision, tree)
    if commit is None:
        print(json.dumps({"error": "cannot export scripts/ at revision", "revision": args.revision}))
        return 2
    gate = os.path.join(tree, "scripts", "citing_set.py")
    named = C.fixture_codes(tree)
    s1_cases = strict_cases(gate, os.path.join(work, "s1"))
    s1 = [{"code": code, "passed": all(c["passed"] for c in s1_cases[code]),
           "problems": [p for c in s1_cases[code] for p in c["problems"]]} for code in CODES]
    result = {
        "checker": ".ufo/waves/round-30/c1_strict_checks.py",
        "checkerSha256": C.sha(os.path.abspath(__file__)),
        "declaredCounterSha256": C.sha(os.path.join(HERE, "c1_reason_count.py")),
        "revision": commit,
        "gateSha256": C.sha(gate),
        "runnerSha256": C.sha(os.path.join(tree, "scripts", "citing_set_selftest.py")),
        "S1": s1,
        "S2": s2(tree, os.path.join(work, "s2"), named),
        "S3": s3(gate, os.path.join(work, "s3")),
        "S4": s4(gate, os.path.join(work, "s4")),
        "S5": s5(gate),
        "S6": s6(gate, os.path.join(work, "s6")),
    }
    verdicts = {
        "S1": all(r["passed"] for r in result["S1"]),
        "S2": all(r["passed"] for r in result["S2"]),
        "S3": all(r["passed"] for r in result["S3"]),
        "S4": result["S4"]["passed"],
        "S5": result["S5"]["passed"],
        "S6": all(r["passed"] for r in result["S6"]),
    }
    result["verdicts"] = verdicts
    result["passed"] = sum(verdicts.values())
    result["total"] = len(verdicts)
    print(json.dumps(result, indent=1))
    print("C1 strict %d/%d at %s %s" % (result["passed"], result["total"], commit, verdicts), file=sys.stderr)
    shutil.rmtree(work, ignore_errors=True)
    return 0 if all(verdicts.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
