#!/usr/bin/env python3
"""Self-test for the base-path audit gate (kake round 29, claim C2).

Runs a base-path audit tool over every committed fixture in
scripts/fixtures/base-path/<case-id>/ and fails when the tool's exit code,
verdict, or finding reasons differ from the fixture's expected.json. The
fixtures pin the reason codes, so a gate that silently drops or renames a
reason fails here even when its verdict still looks right.

Usage:
    python3 -B scripts/base_path_selftest.py [options]

Options:
    --tool PATH       tool to exercise (default: base_path_audit.py next to this file)
    --fixtures DIR    fixture root (default: fixtures/base-path next to this file)
    --python EXE      interpreter used to run the tool (default: sys.executable)
    --case SUBSTR     only run cases whose id contains SUBSTR
    --verbose         print one line per case

Output: one JSON summary object on stdout (lane convention, same shape as
scripts/citing_set_selftest.py) and human readable progress on stderr.

Exit status: 0 when every fixture matches, 1 when any fixture mismatches,
2 when the harness itself cannot run (missing tool or fixtures).

Comparison rules (from .ufo/waves/round-29/c2-matrix.json, field "comparison"):
  * the process exit code must equal the expected exit code;
  * for expected exits 0/1/2 the tool must print one JSON object on stdout and
    its "verdict" must equal the expected verdict;
  * the sorted multiset of expected finding tuples must equal the observed one.
    Each expected finding selects the observed keys it names (always "reason",
    plus "element"/"attribute"/"value" when the fixture pins them), so every
    observed finding is compared on the keys of the expected finding it is
    matched against;
  * expected exit 64 (usage) needs no JSON on stdout.

The tool runs with the fixture directory as its working directory, exactly like
the round-29 C2 counter (.ufo/waves/round-29/c2_matrix_count.py), so the two
observe the same behaviour. The runner never writes inside a fixture, never
rewrites an expectation and never contacts the network.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_TOOL = HERE / "base_path_audit.py"
DEFAULT_FIXTURES = HERE / "fixtures" / "base-path"
# Round 29 wave 2: page and resolved are compared when a fixture names them.
FINDING_KEYS = ("reason", "element", "attribute", "value", "page", "resolved")
TIMEOUT_SECONDS = 120
MIN_DEFAULT_CASES = 45


def parse_json_object(text):
    """Return the last JSON object printed on stdout, or None."""
    text = text.strip()
    if not text:
        return None
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        pass
    decoder = json.JSONDecoder()
    found = None
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            obj, _ = decoder.raw_decode(text, index)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            found = obj
    return found


def keys_of(entry):
    return tuple(key for key in FINDING_KEYS if key in entry)


def tuple_for(entry, keys):
    return tuple(entry.get(key) for key in keys)


def show_tuple(values):
    return "(" + ", ".join(repr(value) for value in values) + ")"


def match_findings(expected, observed):
    """Match expected findings to observed findings on the keys each expects.

    Returns (matched_pairs, unmatched_expected, unmatched_observed). An
    expected finding matches an observed finding when the observed values on
    the keys the expected finding names are equal to the expected values.
    """
    expected = list(expected)
    observed = list(observed)
    adjacency = []
    for entry in expected:
        keys = keys_of(entry)
        row = []
        for index, other in enumerate(observed):
            if tuple_for(entry, keys) == tuple_for(other, keys):
                row.append(index)
        adjacency.append(row)

    owner = {}
    matched = []

    def augment(left, seen):
        for right in adjacency[left]:
            if right in seen:
                continue
            seen.add(right)
            if right not in owner or augment(owner[right], seen):
                owner[right] = left
                return True
        return False

    for left in range(len(expected)):
        augment(left, set())

    for right, left in owner.items():
        matched.append((expected[left], observed[right]))
    matched_expected = {id(entry) for entry, _ in matched}
    matched_observed = {id(other) for _, other in matched}
    unmatched_expected = [entry for entry in expected if id(entry) not in matched_expected]
    unmatched_observed = [other for other in observed if id(other) not in matched_observed]
    return matched, unmatched_expected, unmatched_observed


def compare_findings(expected, observed):
    """Return a list of human readable mismatches, empty when the sets agree."""
    problems = []
    matched, missing, extra = match_findings(expected, observed)
    if missing:
        rendered = []
        for entry in missing:
            keys = keys_of(entry)
            rendered.append("%s %s" % (",".join(keys), show_tuple(tuple_for(entry, keys))))
        problems.append("missing findings: %s" % "; ".join(rendered))
    if extra:
        rendered = []
        for entry in extra:
            keys = ("reason",)
            rendered.append("%s %s" % (",".join(keys), show_tuple(tuple_for(entry, keys))))
        problems.append("unexpected findings: %s" % "; ".join(rendered))
    return problems


def tool_environment():
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.setdefault("LC_ALL", "C.UTF-8")
    return env


def run_tool(tool, case_dir, expected, python_exe):
    argv = expected.get("argv")
    if argv is None:
        args = ["--manifest", str(case_dir / "manifest.json")]
    else:
        args = [str(item) for item in argv]
    command = [python_exe, "-B", str(tool)] + args
    proc = subprocess.run(
        command,
        cwd=str(case_dir),
        capture_output=True,
        text=True,
        timeout=TIMEOUT_SECONDS,
        env=tool_environment(),
    )
    return command, proc


def check_case(tool, case_dir, python_exe):
    expected = json.loads((case_dir / "expected.json").read_text(encoding="utf-8"))
    command, proc = run_tool(tool, case_dir, expected, python_exe)
    problems = []

    want_exit = expected.get("exit")
    if proc.returncode != want_exit:
        problems.append("exit mismatch: expected %r, observed %r" % (want_exit, proc.returncode))

    want_verdict = expected.get("verdict")
    want_findings = expected.get("findings")
    if want_exit in (0, 1, 2):
        payload = parse_json_object(proc.stdout)
        if payload is None:
            problems.append("no JSON object on stdout (stdout=%r)" % proc.stdout[:200])
        else:
            got_verdict = payload.get("verdict")
            if got_verdict != want_verdict:
                problems.append(
                    "verdict mismatch: expected %r, observed %r" % (want_verdict, got_verdict)
                )
            observed = payload.get("findings")
            if observed is None:
                observed = []
            if not isinstance(observed, list):
                problems.append("findings is not a list: %r" % (observed,))
            else:
                bad = [entry for entry in observed if not isinstance(entry, dict)]
                if bad:
                    problems.append("findings contains non-object entries: %r" % (bad,))
                else:
                    problems.extend(compare_findings(want_findings or [], observed))
            for count_key in ("pagesChecked", "referencesChecked"):
                if count_key in expected and payload.get(count_key) != expected[count_key]:
                    problems.append(
                        "%s mismatch: expected %r, observed %r"
                        % (count_key, expected[count_key], payload.get(count_key))
                    )
    elif want_exit == 64:
        pass
    else:
        problems.append("unsupported expected exit %r" % (want_exit,))

    return expected.get("id", case_dir.name), problems, command


def main(argv):
    parser = argparse.ArgumentParser(description="base-path audit gate self-test")
    parser.add_argument("--tool", default=str(DEFAULT_TOOL), help="tool under test")
    parser.add_argument("--fixtures", default=str(DEFAULT_FIXTURES), help="fixture root")
    parser.add_argument("--python", default=sys.executable, help="interpreter for the tool")
    parser.add_argument("--case", default=None, help="only run case ids containing this")
    parser.add_argument("--verbose", action="store_true", help="print one line per case")
    args = parser.parse_args(argv)

    tool = Path(args.tool).resolve()
    fixtures = Path(args.fixtures).resolve()
    summary = {
        "selftest": "kake-r29-base-path-selftest",
        "tool": str(tool),
        "fixtures": str(fixtures),
        "verdict": "clean",
        "cases": 0,
        "passed": 0,
        "failed": 0,
        "passedOverTotal": "0/0",
        "failures": [],
    }
    if not tool.exists():
        summary["verdict"] = "could-not-evaluate"
        summary["failed"] = 1
        summary["failures"] = [{"case": None, "reason": "tool not found: %s" % tool}]
        print(json.dumps(summary, indent=2))
        print("could-not-evaluate: tool not found: %s" % tool, file=sys.stderr)
        return 2
    if not fixtures.is_dir():
        summary["verdict"] = "could-not-evaluate"
        summary["failed"] = 1
        summary["failures"] = [{"case": None, "reason": "fixture root not found: %s" % fixtures}]
        print(json.dumps(summary, indent=2))
        print("could-not-evaluate: fixture root not found: %s" % fixtures, file=sys.stderr)
        return 2

    case_dirs = sorted(
        path for path in fixtures.iterdir() if path.is_dir() and (path / "expected.json").exists()
    )
    if args.case:
        case_dirs = [path for path in case_dirs if args.case in path.name]
    elif fixtures.resolve() == DEFAULT_FIXTURES.resolve() and len(case_dirs) < MIN_DEFAULT_CASES:
        # Round 29 wave 2 (SelftestFixtureDrift): a deleted fixture must not pass silently.
        summary["verdict"] = "could-not-evaluate"
        summary["failed"] = 1
        summary["failures"] = [{"case": None, "reason": "only %d fixtures, expected at least %d" % (len(case_dirs), MIN_DEFAULT_CASES)}]
        print(json.dumps(summary, indent=2))
        print("could-not-evaluate: only %d fixtures, expected at least %d" % (len(case_dirs), MIN_DEFAULT_CASES), file=sys.stderr)
        return 2
    if not case_dirs:
        summary["verdict"] = "could-not-evaluate"
        summary["failed"] = 1
        summary["failures"] = [{"case": None, "reason": "no fixtures found under %s" % fixtures}]
        print(json.dumps(summary, indent=2))
        print("could-not-evaluate: no fixtures found under %s" % fixtures, file=sys.stderr)
        return 2

    passed = 0
    failed = 0
    for case_dir in case_dirs:
        case_id, problems, command = check_case(tool, case_dir, args.python)
        if problems:
            failed += 1
            summary["failures"].append({"case": case_id, "reasons": problems})
            print("FAIL %s" % case_id, file=sys.stderr)
            print("  command: %s" % " ".join(command), file=sys.stderr)
            for problem in problems:
                print("  %s" % problem, file=sys.stderr)
        else:
            passed += 1
            if args.verbose:
                print("ok   %s" % case_id, file=sys.stderr)

    total = passed + failed
    summary["cases"] = total
    summary["passed"] = passed
    summary["failed"] = failed
    summary["passedOverTotal"] = "%d/%d" % (passed, total)
    summary["caseNames"] = [case_dir.name for case_dir in case_dirs]
    if failed:
        summary["verdict"] = "failed"
    print(json.dumps(summary, indent=2))
    print("%d/%d fixtures passed" % (passed, total), file=sys.stderr)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
