#!/usr/bin/env python3
"""Fixture runner for the citing-set gate (round-27, C2 operability).

Contract under test (``.ufo/waves/round-27/contract.json``):

    gate     python3 -B scripts/citing_set.py --root <dir> [--revision <commit>]
             --population <relative-json> --ledger <relative-json> [--json]
    fixtures scripts/fixtures/citing-set/<case>/{corpus/knowledge/*,population.json,
             ledger.json,expected.json}

Expectation format (``expected.json``)
--------------------------------------
The ``findings`` list is in one of two forms, never mixed within one case:

  * legacy: one string per finding, the finding id only::

        {"exit": 1, "findings": ["citation_range_invalid"]}

  * object: one object per finding::

        {"exit": 2, "findings": [{"id": "input_invalid", "reason": "corpus_empty"}]}

In the object form a finding may omit ``reason`` or carry ``"reason": null``;
an observed finding without a reason compares as ``None``.  The runner compares
the sorted multiset of ``(id, reason)`` pairs exactly; in the legacy form it
compares the sorted multiset of ids only.  The exit code is compared exactly in
both forms.  A case whose entries mix strings and objects is a malformed
oracle and fails the run instead of being skipped.

Per-case setup (``case.json``, optional)
----------------------------------------
A fixture case may carry a ``case.json`` that describes how the case tree is
built at run time.  When present, the case directory is copied into
``<tmpdir>/citing-set-selftest/cases/<case>/`` first and every step runs on
that copy; the committed fixture is never mutated, and Git-hostile artifacts
(a FIFO, an empty directory, a disposable repository) are created in the copy:

    {
      "description": "one human-readable line",
      "root": "sub",
      "argv": ["--revision", "HEAD"],
      "setup": [
        {"op": "fifo", "path": "population.json"},
        {"op": "mkdir", "path": "corpus/knowledge"},
        {"op": "git_init"},
        {"op": "git_commit", "message": "fixture"}
      ]
    }

``root`` (default ".") is the subdirectory of the copy used as the gate's
``--root``; ``argv`` entries are appended to the gate command line.
Supported setup ops:

  mkdir      create a directory (parents included)
  fifo       replace the file at ``path`` with a FIFO
  git_init   initialize a Git repository at the copy root
  git_commit stage everything and commit (Git identity is set by the runner;
             the environment is isolated: inherited GIT_* variables are
             dropped and GIT_CONFIG_GLOBAL is pinned to /dev/null)

This runner is a pure oracle.  For every fixture case it starts one gate
subprocess and compares two observable outcomes with the frozen expectation:

  * the process exit code, exactly; and
  * the finding multiset (ids, or (id, reason) pairs for object expectations).

It never rewrites an expectation, never mutates a fixture, never edits the
repository and never contacts the network.  A case whose ``expected.json`` is
missing, unparsable or malformed fails the run instead of being skipped, and a
fixture directory that is absent or empty can never report success.

Summary (one JSON object on stdout)::

    {"verdict": "clean"|"failed"|"could-not-evaluate",
     "cases": <int>, "failed": <int>, "results": [{"case": ..., "passed": ...}]}

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
import shutil
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

CASE_SETUP_FILE = "case.json"
SETUP_OPS = ("mkdir", "fifo", "git_init", "git_commit")
GIT_IDENTITY = {
    "GIT_AUTHOR_NAME": "citing-set-selftest",
    "GIT_AUTHOR_EMAIL": "citing-set-selftest@invalid",
    "GIT_COMMITTER_NAME": "citing-set-selftest",
    "GIT_COMMITTER_EMAIL": "citing-set-selftest@invalid",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
}


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


def finding_pairs(report):
    """Sorted multiset of (id, reason) pairs in a gate report.

    A finding without a usable ``id`` is kept as an opaque placeholder so that a
    malformed finding can never compare equal to an empty expectation; a
    finding without a used ``reason`` compares as ``None``.  A legacy string
    finding compares as (string, None).
    """
    findings = report.get("findings") if isinstance(report, dict) else None
    if findings is None:
        return []
    if not isinstance(findings, list):
        return [("<findings-not-a-list>", None)]
    pairs = []
    for item in findings:
        if isinstance(item, str):
            pairs.append((item, None))
        elif isinstance(item, dict):
            identifier = item.get("id")
            reason = item.get("reason")
            pairs.append(
                (
                    identifier if isinstance(identifier, str) else json.dumps(item, sort_keys=True),
                    reason if isinstance(reason, str) else None,
                )
            )
        else:
            pairs.append((json.dumps(item, sort_keys=True), None))
    return sorted(pairs, key=pair_order)


def pair_order(pair):
    """Total order for (id, reason) pairs; a missing reason (None) sorts first."""
    identifier, reason = pair
    return (identifier, reason is not None, reason or "")


def expectation_entries(expected):
    """Return (mode, entries) for an oracle ``expected``, or raise ValueError.

    ``mode`` is "ids" for the legacy all-strings form and "pairs" for the
    object form; ``entries`` is the sorted multiset the runner must match.
    """
    if not isinstance(expected, dict):
        raise ValueError("expected.json must be a JSON object")
    if "exit" not in expected:
        raise ValueError('expected.json must carry an integer "exit"')
    value = expected["exit"]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError('expected.json must carry an integer "exit"')
    findings = expected.get("findings")
    if not isinstance(findings, list):
        raise ValueError('expected.json must carry a list of finding entries in "findings"')
    if not findings:
        return "pairs", []
    kinds = set()
    for item in findings:
        if isinstance(item, str):
            kinds.add("ids")
        elif isinstance(item, dict) and isinstance(item.get("id"), str):
            kinds.add("pairs")
            reason = item.get("reason")
            if reason is not None and not isinstance(reason, str):
                raise ValueError('expected.json object finding "reason" must be a string or null')
        else:
            raise ValueError('expected.json "findings" must be all strings (legacy) or all {"id", "reason"} objects')
    if len(kinds) > 1:
        raise ValueError('expected.json "findings" must be all strings or all objects, not mixed')
    if "ids" in kinds:
        return "ids", sorted(findings)
    return "pairs", sorted(((item["id"], item.get("reason")) for item in findings), key=pair_order)


# --------------------------------------------------------------------------
# per-case setup (optional case.json)
# --------------------------------------------------------------------------
def load_case_setup(case_dir):
    """Load and validate the optional case.json; return None when absent."""
    path = case_dir / CASE_SETUP_FILE
    if not path.is_file():
        return None
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError("%s unreadable: %s" % (CASE_SETUP_FILE, exc))
    try:
        document = json.loads(raw)
    except ValueError as exc:
        raise ValueError("%s is not valid JSON: %s" % (CASE_SETUP_FILE, exc))
    if not isinstance(document, dict):
        raise ValueError("%s must be a JSON object" % CASE_SETUP_FILE)
    argv = document.get("argv", [])
    if not isinstance(argv, list) or not all(isinstance(item, str) for item in argv):
        raise ValueError('%s "argv" must be a list of strings' % CASE_SETUP_FILE)
    root = document.get("root", ".")
    if not isinstance(root, str) or not root.strip() or root.startswith("/"):
        raise ValueError('%s "root" must be a non-empty relative path' % CASE_SETUP_FILE)
    setup = document.get("setup", [])
    if not isinstance(setup, list):
        raise ValueError('%s "setup" must be a list' % CASE_SETUP_FILE)
    for step in setup:
        if not isinstance(step, dict) or not isinstance(step.get("op"), str):
            raise ValueError('%s "setup" entries must be objects with a string "op"' % CASE_SETUP_FILE)
        if step["op"] not in SETUP_OPS:
            raise ValueError('%s names an unknown setup op %r' % (CASE_SETUP_FILE, step["op"]))
        if step["op"] in ("mkdir", "fifo"):
            if not isinstance(step.get("path"), str) or not step["path"].strip():
                raise ValueError('%s setup op %r needs a non-empty "path"' % (CASE_SETUP_FILE, step["op"]))
    return {"argv": argv, "root": root, "setup": setup}


def git_env():
    """Isolated environment for setup Git commands."""
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_IDENTITY)
    return env


def run_command(command, cwd, env, timeout):
    try:
        done = subprocess.run(
            command,
            cwd=str(cwd),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("setup command timed out: %s" % " ".join(command))
    if done.returncode != 0:
        raise RuntimeError(
            "setup command failed (%d): %s" % (done.returncode, tail(done.stderr or done.stdout))
        )
    return done


def apply_setup(work_dir, setup, timeout):
    env = git_env()
    for step in setup:
        op = step["op"]
        if op == "mkdir":
            (work_dir / step["path"]).mkdir(parents=True, exist_ok=True)
        elif op == "fifo":
            target = work_dir / step["path"]
            if target.exists() or target.is_symlink():
                target.unlink()
            os.mkfifo(target)
        elif op == "git_init":
            run_command(["git", "init", "-q"], work_dir, env, timeout)
        elif op == "git_commit":
            run_command(["git", "add", "-A"], work_dir, env, timeout)
            run_command(["git", "commit", "-q", "-m", step.get("message", "fixture")], work_dir, env, timeout)


def prepare_case(case_dir, cases_root, timeout):
    """Copy one case into the scratch tree and apply its setup.

    Returns (work_dir, setup) where ``setup`` is None when the case has no
    case.json.  The committed fixture is never written to.
    """
    try:
        setup = load_case_setup(case_dir)
    except ValueError as exc:
        return None, exc
    work_dir = cases_root / case_dir.name
    try:
        if work_dir.exists():
            shutil.rmtree(work_dir)
        shutil.copytree(case_dir, work_dir)
    except (OSError, shutil.Error) as exc:
        return None, "case copy failed: %s" % exc
    if setup:
        try:
            apply_setup(work_dir, setup["setup"], timeout)
        except (OSError, RuntimeError) as exc:
            return None, "case setup failed: %s" % exc
    return work_dir, setup


# --------------------------------------------------------------------------
# one fixture case
# --------------------------------------------------------------------------
def run_case(case_dir, gate, env, timeout, cases_root):
    row = {
        "case": case_dir.name,
        "ok": False,
        "passed": False,
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
    try:
        mode, expected_entries = expectation_entries(expected)
    except ValueError as exc:
        row["reason"] = str(exc)
        return row
    row["expected"] = {"exit": expected["exit"], "findings": expected_entries, "mode": mode}

    work_dir, setup = prepare_case(case_dir, cases_root, timeout)
    if work_dir is None:
        row["reason"] = str(setup)
        return row
    root = work_dir
    if setup:
        root = work_dir / setup["root"]
    argv = [
        sys.executable,
        "-B",
        str(gate),
        "--root",
        str(root),
        "--population",
        "population.json",
        "--ledger",
        "ledger.json",
        "--json",
    ]
    if setup:
        argv.extend(setup["argv"])
    row["argv"] = argv
    try:
        run = subprocess.run(
            argv,
            cwd=str(root),
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

    observed_pairs = finding_pairs(report)
    if mode == "ids":
        observed = sorted(identifier for identifier, _ in observed_pairs)
    else:
        observed = observed_pairs
    row["actual"] = {
        "exit": run.returncode,
        "verdict": report.get("verdict"),
        "findings": observed,
        "mode": mode,
    }
    if run.returncode != expected["exit"]:
        row["reason"] = "exit mismatch: expected %d, observed %d" % (expected["exit"], run.returncode)
        return row
    if observed != expected_entries:
        row["reason"] = "finding mismatch: expected %s, observed %s" % (
            json.dumps(expected_entries),
            json.dumps(observed),
        )
        return row
    row["ok"] = True
    row["passed"] = True
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
    cases_root = Path(args.tmpdir).expanduser().resolve() / "citing-set-selftest" / "cases"
    try:
        cases_root.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return cannot_evaluate("cannot create scratch case tree %s: %s" % (cases_root, exc))

    for case_dir in cases:
        row = run_case(case_dir, gate, env, args.timeout, cases_root)
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
