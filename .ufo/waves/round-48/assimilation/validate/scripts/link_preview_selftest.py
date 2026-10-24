#!/usr/bin/env python3
"""Self-test for the offline Open Graph link-preview audit."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
DEFAULT_TOOL = HERE / "link_preview_audit.py"
DEFAULT_FIXTURES = HERE / "fixtures" / "link-preview"
MIN_FIXTURES = 20
TIMEOUT_SECONDS = 120
INPUT_REASONS = frozenset(("input_invalid", "page_unreadable"))


def tool_environment():
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.setdefault("LC_ALL", "C.UTF-8")
    return env


def finding_signature(finding):
    if not isinstance(finding, dict):
        raise ValueError("finding is not an object")
    reason = finding.get("reason")
    if not isinstance(reason, str):
        raise ValueError("finding has no string reason")
    if reason in INPUT_REASONS:
        return (reason,)
    prop = finding.get("property")
    if not isinstance(prop, str):
        raise ValueError("policy finding has no string property")
    return (reason, prop)


def projected_findings(findings):
    if not isinstance(findings, list):
        raise ValueError("findings is not a list")
    return sorted(finding_signature(finding) for finding in findings)


def check_case(tool, case_dir):
    problems = []
    expected_path = case_dir / "expected.json"
    manifest_path = case_dir / "manifest.json"
    try:
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        if not isinstance(expected, dict):
            raise ValueError("expected.json is not an object")
        if not manifest_path.is_file() and "argv" not in expected:
            raise ValueError("manifest.json is missing")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return case_dir.name, ["invalid fixture: %s" % exc]

    want_exit = expected.get("exit")
    if want_exit not in (0, 1, 2, 64):
        return case_dir.name, ["unsupported expected exit %r" % (want_exit,)]
    argv = expected.get("argv")
    if argv is None:
        argv = ["--manifest", "manifest.json"]
    if not isinstance(argv, list) or any(not isinstance(item, (str, int, float)) for item in argv):
        return case_dir.name, ["expected argv must be a list of arguments"]
    command = [sys.executable, "-B", str(tool)] + [str(item) for item in argv]
    try:
        proc = subprocess.run(
            command,
            cwd=str(case_dir),
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            env=tool_environment(),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return case_dir.name, ["tool could not run: %s" % exc]

    if proc.returncode != want_exit:
        problems.append("exit mismatch: expected %r, observed %r" % (want_exit, proc.returncode))

    if want_exit in (0, 1, 2):
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            problems.append("stdout is not one JSON object: %s" % exc)
            payload = None
        if payload is not None:
            if not isinstance(payload, dict):
                problems.append("stdout JSON is not an object")
            else:
                want_verdict = expected.get("verdict")
                if payload.get("verdict") != want_verdict:
                    problems.append(
                        "verdict mismatch: expected %r, observed %r"
                        % (want_verdict, payload.get("verdict"))
                    )
                if (
                    "pagesChecked" in expected
                    and payload.get("pagesChecked") != expected["pagesChecked"]
                ):
                    problems.append(
                        "pagesChecked mismatch: expected %r, observed %r"
                        % (expected["pagesChecked"], payload.get("pagesChecked"))
                    )
                if "findingIds" in expected:
                    want_ids = expected["findingIds"]
                    payload_findings = payload.get("findings")
                    got_ids = (
                        [finding.get("id") for finding in payload_findings if isinstance(finding, dict)]
                        if isinstance(payload_findings, list)
                        else None
                    )
                    if (
                        not isinstance(want_ids, list)
                        or not all(isinstance(item, str) for item in want_ids)
                        or got_ids != want_ids
                    ):
                        problems.append(
                            "finding ids mismatch: expected %r, observed %r" % (want_ids, got_ids)
                        )
                try:
                    want_findings = projected_findings(expected.get("findings"))
                    got_findings = projected_findings(payload.get("findings"))
                    if want_findings != got_findings:
                        problems.append(
                            "findings mismatch: expected %r, observed %r"
                            % (want_findings, got_findings)
                        )
                except ValueError as exc:
                    problems.append("invalid findings: %s" % exc)
    return case_dir.name, problems


def main(argv=None):
    parser = argparse.ArgumentParser(description="link-preview audit self-test")
    parser.add_argument("--tool", default=str(DEFAULT_TOOL), help="audit tool under test")
    parser.add_argument("--fixtures", default=str(DEFAULT_FIXTURES), help="fixture root")
    args = parser.parse_args(argv)

    tool = Path(args.tool).resolve()
    fixtures = Path(args.fixtures).resolve()
    summary = {
        "selftest": "kake-r34-link-preview-selftest",
        "tool": str(tool),
        "fixtures": str(fixtures),
        "verdict": "clean",
        "cases": 0,
        "passed": 0,
        "failed": 0,
        "passedOverTotal": "0/0",
        "caseNames": [],
        "failures": [],
    }

    if not tool.is_file():
        summary["verdict"] = "could-not-evaluate"
        summary["failed"] = 1
        summary["failures"] = [{"case": None, "reasons": ["tool not found: %s" % tool]}]
        print(json.dumps(summary, sort_keys=True))
        return 2
    if not fixtures.is_dir():
        summary["verdict"] = "could-not-evaluate"
        summary["failed"] = 1
        summary["failures"] = [{"case": None, "reasons": ["fixture root not found: %s" % fixtures]}]
        print(json.dumps(summary, sort_keys=True))
        return 2

    case_dirs = sorted(path for path in fixtures.iterdir() if path.is_dir())
    if len(case_dirs) < MIN_FIXTURES:
        summary["verdict"] = "could-not-evaluate"
        summary["failed"] = 1
        summary["failures"] = [
            {"case": None, "reasons": ["only %d fixture directories; expected at least %d" % (len(case_dirs), MIN_FIXTURES)]}
        ]
        print(json.dumps(summary, sort_keys=True))
        return 2

    passed = 0
    for case_dir in case_dirs:
        case_id, problems = check_case(tool, case_dir)
        summary["caseNames"].append(case_id)
        if problems:
            summary["failures"].append({"case": case_id, "reasons": problems})
        else:
            passed += 1

    total = len(case_dirs)
    failed = total - passed
    summary["cases"] = total
    summary["passed"] = passed
    summary["failed"] = failed
    summary["passedOverTotal"] = "%d/%d" % (passed, total)
    if failed:
        summary["verdict"] = "failed"
    print(json.dumps(summary, sort_keys=True))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
