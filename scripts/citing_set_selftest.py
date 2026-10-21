#!/usr/bin/env python3
"""Fixture runner for the citing-set gate (round-27, C2 operability).

Contract under test (``.ufo/waves/round-27/contract.json``):

    gate     python3 -B scripts/citing_set.py --root <dir> [--revision <commit>]
             --population <relative-json> --ledger <relative-json> [--json]
    fixtures scripts/fixtures/citing-set/<case>/{corpus/knowledge/*,population.json,
             ledger.json,expected.json}
    expected {"exit": <int>, "findings": [<finding-id>, ...]}  (repeated ids retained)

This runner is a pure oracle.  For every fixture case it starts one gate
subprocess and compares two observable outcomes with the frozen expectation:

  * the process exit code, exactly; and
  * the sorted multiset of finding ids (repetitions retained), exactly.

It never rewrites an expectation, never mutates a fixture, never edits the
repository and never contacts the network.  A case whose ``expected.json`` is
missing, unparsable or malformed fails the run instead of being skipped, and a
fixture directory that is absent or empty can never report success.

Summary (one JSON object on stdout)::

    {"verdict": "clean"|"failed"|"could-not-evaluate",
     "cases": <int>, "failed": <int>, ...}

``cases`` is the number of discovered fixture cases.  ``failed`` counts
unsatisfied obligations: one per failing case, or one when the run could not be
evaluated at all, so ``failed == 0`` is only ever true for a run that may pass.

Exit codes: 0 every case matched, 1 at least one case mismatched,
2 the run could not be evaluated (gate absent, fixture directory absent/empty).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_CANNOT_EVALUATE = 2

DEFAULT_TMPDIR = "/fast/scratch/hyaku/kake-r27"
CONTRACT_MINIMUM_CASES = 12
DEFAULT_TIMEOUT_SECONDS = 120.0
TAIL_BYTES = 800


# --------------------------------------------------------------------------
# argument handling
# --------------------------------------------------------------------------
def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="citing_set_selftest.py",
        description="Run the citing-set gate over every fixture case and compare exact outcomes.",
    )
    parser.add_argument("--root", default=None, help="repository root (default: parent of this script's directory)")
    parser.add_argument("--fixtures", default=None, help="fixture directory (default: <root>/scripts/fixtures/citing-set)")
    parser.add_argument("--gate", default=None, help="gate script (default: <root>/scripts/citing_set.py)")
    parser.add_argument("--tmpdir", default=DEFAULT_TMPDIR, help="scratch directory exported as TMPDIR to gate subprocesses")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS, help="per-case gate timeout in seconds")
    parser.add_argument("--min-cases", type=int, default=0, help="fail when fewer than this many fixture cases exist")
    parser.add_argument("--json", action="store_true", help="accepted for interface symmetry; the summary is always JSON")
    parser.add_argument("--selftest", action="store_true", help="accepted so the gate may delegate this runner verbatim")
    args, unknown = parser.parse_known_args(argv)
    return args, unknown


def resolve_paths(args):
    script = Path(__file__).resolve()
    root = Path(args.root).expanduser().resolve() if args.root else script.parents[1]
    gate = Path(args.gate).expanduser().resolve() if args.gate else root / "scripts" / "citing_set.py"
    fixtures = Path(args.fixtures).expanduser().resolve() if args.fixtures else root / "scripts" / "fixtures" / "citing-set"
    return root, gate, fixtures


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------
def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def tail(text, limit=TAIL_BYTES):
    if text is None:
        return ""
    if len(text) <= limit:
        return text
    return "..." + text[-limit:]


def child_env(tmpdir):
    """Environment for gate subprocesses: scratch TMPDIR and an isolated HOME."""
    env = dict(os.environ)
    scratch = Path(tmpdir).expanduser()
    home = scratch / "citing-set-selftest" / "home"
    try:
        scratch.mkdir(parents=True, exist_ok=True)
        home.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    env["TMPDIR"] = str(scratch)
    env["TMP"] = str(scratch)
    env["TEMP"] = str(scratch)
    env["HOME"] = str(home)
    env["KAKE_SELFTEST"] = "citing-set-selftest"
    return env


def parse_report(stdout):
    """Return the gate's JSON report object, or raise ValueError."""
    text = (stdout or "").strip()
    if not text:
        raise ValueError("gate produced no stdout")
    try:
        report = json.loads(text)
    except ValueError:
        report = None
    if isinstance(report, dict):
        return report
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            candidate, _ = decoder.raw_decode(text, index)
        except ValueError:
            continue
        if isinstance(candidate, dict):
            return candidate
    raise ValueError("gate stdout is not a JSON object")


def finding_ids(report):
    """Sorted multiset of finding ids in a gate report.

    A finding without a usable ``id`` is kept as an opaque placeholder so that a
    malformed finding can never compare equal to an empty expectation.
    """
    findings = report.get("findings") if isinstance(report, dict) else None
    if findings is None:
        return []
    if not isinstance(findings, list):
        return ["<findings-not-a-list>"]
    ids = []
    for item in findings:
        if isinstance(item, str):
            ids.append(item)
        elif isinstance(item, dict):
            value = item.get("id")
            ids.append(value if isinstance(value, str) else json.dumps(item, sort_keys=True))
        else:
            ids.append(json.dumps(item, sort_keys=True))
    return ids


def expectation_problem(expected):
    """Return a human reason when expected.json cannot serve as an oracle."""
    if not isinstance(expected, dict):
        return "expected.json must be a JSON object"
    if "exit" not in expected:
        return 'expected.json must carry an integer "exit"'
    value = expected["exit"]
    if isinstance(value, bool) or not isinstance(value, int):
        return 'expected.json must carry an integer "exit"'
    findings = expected.get("findings")
    if not isinstance(findings, list):
        return 'expected.json must carry a list of finding ids in "findings"'
    for item in findings:
        if not isinstance(item, str):
            return 'expected.json "findings" must contain only strings'
    return None


# --------------------------------------------------------------------------
# one fixture case
# --------------------------------------------------------------------------
def run_case(case_dir, gate, env, timeout):
    row = {
        "case": case_dir.name,
        "ok": False,
        "reason": None,
        "expected": None,
        "actual": None,
        "argv": None,
    }
    expected_file = case_dir / "expected.json"
    try:
        raw = expected_file.read_text(encoding="utf-8")
    except OSError as exc:
        row["reason"] = "expected.json unreadable: %s" % exc
        return row
    try:
        expected = json.loads(raw)
    except ValueError as exc:
        row["reason"] = "expected.json is not valid JSON: %s" % exc
        return row
    problem = expectation_problem(expected)
    if problem:
        row["reason"] = problem
        return row
    row["expected"] = {"exit": expected["exit"], "findings": sorted(expected["findings"])}

    argv = [
        sys.executable,
        "-B",
        str(gate),
        "--root",
        str(case_dir),
        "--population",
        "population.json",
        "--ledger",
        "ledger.json",
        "--json",
    ]
    row["argv"] = argv
    try:
        run = subprocess.run(
            argv,
            cwd=str(case_dir),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        row["reason"] = "gate timed out after %gs" % timeout
        return row
    except OSError as exc:
        row["reason"] = "gate could not be started: %s" % exc
        return row

    try:
        report = parse_report(run.stdout)
    except ValueError as exc:
        row["reason"] = "gate stdout is not a JSON report: %s" % exc
        row["actual"] = {
            "exit": run.returncode,
            "stdout": tail(run.stdout),
            "stderr": tail(run.stderr),
        }
        return row

    if "findings" not in report:
        row["reason"] = "gate report carries no 'findings' array"
        row["actual"] = {"exit": run.returncode, "verdict": report.get("verdict"), "findings": None}
        return row
    if not isinstance(report["findings"], list):
        row["reason"] = "gate report 'findings' is not an array"
        row["actual"] = {"exit": run.returncode, "verdict": report.get("verdict"), "findings": None}
        return row

    observed = sorted(finding_ids(report))
    row["actual"] = {
        "exit": run.returncode,
        "verdict": report.get("verdict"),
        "findings": observed,
    }
    if run.returncode != expected["exit"]:
        row["reason"] = "exit mismatch: expected %d, observed %d" % (expected["exit"], run.returncode)
        return row
    if observed != sorted(expected["findings"]):
        row["reason"] = "finding-id mismatch: expected %s, observed %s" % (
            json.dumps(sorted(expected["findings"])),
            json.dumps(observed),
        )
        return row
    row["ok"] = True
    return row


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------
def emit(summary):
    print(json.dumps(summary, indent=2))


def main(argv=None):
    args, unknown = parse_args(list(sys.argv[1:] if argv is None else argv))
    root, gate, fixtures = resolve_paths(args)

    summary = {
        "schema": "kake-citing-set-selftest-v1",
        "verdict": "could-not-evaluate",
        "passed": False,
        "cases": 0,
        "failed": 0,
        "failedCases": 0,
        "caseNames": [],
        "contractMinimumCases": CONTRACT_MINIMUM_CASES,
        "meetsContractMinimum": False,
        "root": str(root),
        "runner": str(Path(__file__).resolve()),
        "runnerSha256": sha256_file(Path(__file__).resolve()),
        "gate": str(gate),
        "gateSha256": None,
        "fixtures": str(fixtures),
        "results": [],
        "failures": [],
        "notes": [],
    }
    if unknown:
        summary["notes"].append("ignored unknown arguments: %s" % " ".join(unknown))

    def cannot_evaluate(reason):
        summary["failures"].append({"case": None, "reason": reason})
        summary["failed"] = 1
        emit(summary)
        return EXIT_CANNOT_EVALUATE

    if not gate.is_file():
        return cannot_evaluate("gate script not found: %s" % gate)
    summary["gateSha256"] = sha256_file(gate)

    if not fixtures.is_dir():
        return cannot_evaluate("fixture directory not found: %s" % fixtures)

    cases = sorted(
        (path for path in fixtures.iterdir() if path.is_dir() and not path.name.startswith(".")),
        key=lambda path: path.name,
    )
    if not cases:
        return cannot_evaluate("fixture directory contains no case directories: %s" % fixtures)

    env = child_env(args.tmpdir)
    for case_dir in cases:
        row = run_case(case_dir, gate, env, args.timeout)
        summary["results"].append(row)
        if not row["ok"]:
            summary["failedCases"] += 1
            summary["failures"].append(
                {
                    "case": row["case"],
                    "reason": row["reason"],
                    "expected": row["expected"],
                    "actual": row["actual"],
                }
            )

    summary["cases"] = len(cases)
    summary["caseNames"] = [case_dir.name for case_dir in cases]
    summary["failed"] = summary["failedCases"]
    summary["meetsContractMinimum"] = len(cases) >= CONTRACT_MINIMUM_CASES
    if not summary["meetsContractMinimum"]:
        summary["notes"].append(
            "fixture case count %d is below the contract minimum %d (run with --min-cases %d to enforce)"
            % (len(cases), CONTRACT_MINIMUM_CASES, CONTRACT_MINIMUM_CASES)
        )

    if summary["failedCases"]:
        summary["verdict"] = "failed"
        emit(summary)
        return EXIT_FAILED
    if args.min_cases and len(cases) < args.min_cases:
        summary["failures"].append(
            {
                "case": None,
                "reason": "fixture case count %d below required minimum %d" % (len(cases), args.min_cases),
            }
        )
        summary["failed"] = 1
        summary["verdict"] = "failed"
        emit(summary)
        return EXIT_FAILED

    summary["verdict"] = "clean"
    summary["passed"] = True
    emit(summary)
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
