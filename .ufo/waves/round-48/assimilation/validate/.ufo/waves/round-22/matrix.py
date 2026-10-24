#!/usr/bin/env python3
"""Run frozen offline canonical-audit cases against a repository root."""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path


WAVE_DIR = Path(__file__).resolve().parent
CASES_PATH = WAVE_DIR / "cases.json"
# Exact matrixCases copied from the frozen round-22 contract, not a file glob.
FROZEN_CASE_NAMES = (
    "absolute_match",
    "relative_same_dir",
    "relative_parent",
    "root_relative",
    "scheme_relative",
    "first_base",
    "second_base_ignored",
    "rel_token_list",
    "rel_uppercase",
    "attr_uppercase",
    "entity_href",
    "query_preserved",
    "missing_link",
    "duplicate_same",
    "duplicate_different",
    "body_link",
    "href_absent",
    "href_empty",
    "invalid_url",
    "javascript_url",
    "data_url",
    "fragment_url",
    "wrong_host",
    "wrong_path",
    "wrong_query",
    "base_invalid",
    "comment_decoy",
    "script_decoy",
    "template_decoy",
    "missing_head",
    "manifest_traversal",
    "symlink_html",
)


@contextmanager
def execution_manifest(case, source_manifest):
    """Yield an absolute manifest path; create symlinks only in temporary data."""
    if case["caseId"] != "symlink_html":
        yield source_manifest.resolve()
        return

    fixture_dir = source_manifest.parent
    manifest = json.loads(source_manifest.read_text(encoding="utf-8"))
    pages = manifest.get("pages")
    if not isinstance(pages, list) or len(pages) != 1:
        raise ValueError("symlink_html fixture must contain exactly one page")
    link_name = pages[0].get("file")
    if not isinstance(link_name, str) or Path(link_name).name != link_name:
        raise ValueError("symlink_html fixture must name a file in its fixture directory")

    with tempfile.TemporaryDirectory(prefix="kake-canonical-matrix-") as temporary:
        runtime_dir = Path(temporary)
        shutil.copyfile(source_manifest, runtime_dir / "manifest.json")
        shutil.copyfile(fixture_dir / "target.html", runtime_dir / "target.html")
        os.symlink("target.html", runtime_dir / link_name)
        yield (runtime_dir / "manifest.json").resolve()


def observed_findings(stdout):
    try:
        result = json.loads(stdout)
    except (json.JSONDecodeError, TypeError):
        return ["invalid_json"]
    if not isinstance(result, dict) or not isinstance(result.get("findings"), list):
        return ["invalid_output"]
    ids = []
    for finding in result["findings"]:
        if not isinstance(finding, dict) or not isinstance(finding.get("id"), str):
            return ["invalid_output"]
        ids.append(finding["id"])
    return ids or ["clean"]


def load_cases():
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("cases.json must have version 1")
    cases = data.get("cases")
    if not isinstance(cases, list):
        raise ValueError("cases.json must contain a cases array")
    case_ids = [case.get("caseId") for case in cases if isinstance(case, dict)]
    if len(case_ids) != len(cases) or any(not isinstance(item, str) for item in case_ids):
        raise ValueError("each case must have a string caseId")
    if len(set(case_ids)) != len(case_ids):
        raise ValueError("cases.json caseIds must be unique")
    if set(case_ids) != set(FROZEN_CASE_NAMES):
        missing = sorted(set(FROZEN_CASE_NAMES) - set(case_ids))
        extra = sorted(set(case_ids) - set(FROZEN_CASE_NAMES))
        raise ValueError(f"frozen contract case set mismatch: missing={missing}, extra={extra}")
    for case in cases:
        if (
            not isinstance(case.get("manifest"), str)
            or not isinstance(case.get("expectedExit"), int)
            or not isinstance(case.get("expectedFindings"), list)
            or not case["expectedFindings"]
            or any(not isinstance(item, str) for item in case["expectedFindings"])
            or not isinstance(case.get("rationale"), str)
            or not case["rationale"].startswith("Local publisher policy:")
        ):
            raise ValueError(f"invalid frozen case record: {case['caseId']}")
    return cases


def render_ids(ids):
    return ",".join(ids) if ids is not None else "not_observed"


def result_record(case, status, actual_exit=None, actual_findings=None,
                  stdout="", stderr="", reason=None):
    row = {
        "caseId": case["caseId"],
        "status": status,
        "expectedExit": case["expectedExit"],
        "actualExit": actual_exit,
        "expectedFindings": case["expectedFindings"],
        "actualFindings": actual_findings,
        "stdout": stdout,
        "stderr": stderr,
    }
    if reason is not None:
        row["reason"] = reason
    return row


def make_report(selection, accepted=0, total=0, executed=0, discrepancies=0,
                tool_missing=False, results=None, error=None):
    report = {
        "selection": selection,
        "accepted": accepted,
        "total": total,
        "executed": executed,
        "discrepancies": discrepancies,
        "toolMissing": tool_missing,
        "results": results or [],
    }
    if error is not None:
        report["error"] = error
    return report


def emit_report(report, json_mode):
    if json_mode:
        print(json.dumps(report, ensure_ascii=False))
        return

    if "error" in report:
        print(f"ERROR {report['error']}", file=sys.stderr)
    for row in report["results"]:
        if row["status"] == "NOT_RUN":
            print(
                f"NOT_RUN caseId={row['caseId']} expectedExit={row['expectedExit']} "
                f"expectedFindings={render_ids(row['expectedFindings'])} "
                f"actualExit=not_run actualFindings=not_run reason={row['reason']}"
            )
        elif row["status"] == "PASS":
            print(
                f"PASS caseId={row['caseId']} exit={row['actualExit']} "
                f"findings={render_ids(row['actualFindings'])}"
            )
        else:
            detail = row.get("reason")
            stderr = row["stderr"].strip().replace("\n", " ")
            if stderr:
                detail = f"{detail or ''} stderr={stderr[:300]!r}".strip()
            suffix = f" reason={detail}" if detail else ""
            actual_exit = row["actualExit"]
            if actual_exit is None:
                actual_exit = "not_observed"
            print(
                f"FAIL caseId={row['caseId']} expectedExit={row['expectedExit']} "
                f"actualExit={actual_exit} "
                f"expectedFindings={render_ids(row['expectedFindings'])} "
                f"actualFindings={render_ids(row['actualFindings'])}{suffix}"
            )
    print(
        f"SUMMARY selection={report['selection']} accepted={report['accepted']} "
        f"total={report['total']} executed={report['executed']} "
        f"discrepancies={report['discrepancies']} "
        f"tool_missing={int(report['toolMissing'])}"
    )


def captured_text(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="repository root to audit")
    parser.add_argument("--case", help="run one named case instead of the full 32-case matrix")
    parser.add_argument("--json", action="store_true", help="emit one machine-readable JSON report")
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    selection = args.case if args.case is not None else "all"

    try:
        cases = load_cases()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        emit_report(
            make_report(selection, error=f"cases_unavailable: {error}"), args.json
        )
        return 2

    if args.case is not None:
        selected = [case for case in cases if case["caseId"] == args.case]
        if not selected:
            emit_report(
                make_report(selection, error=f"unknown_case: {args.case}"), args.json
            )
            return 2
        cases = selected

    tool = root / "scripts" / "canonical_audit.py"
    if not tool.is_file():
        results = [
            result_record(case, "NOT_RUN", reason="tool_missing") for case in cases
        ]
        emit_report(
            make_report(
                selection,
                total=len(cases),
                tool_missing=True,
                results=results,
            ),
            args.json,
        )
        return 2
    tool = tool.resolve()

    accepted = 0
    executed = 0
    discrepancies = 0
    results = []
    for case in cases:
        source_manifest = (WAVE_DIR / case["manifest"]).resolve()
        try:
            with execution_manifest(case, source_manifest) as manifest:
                completed = subprocess.run(
                    [
                        sys.executable,
                        str(tool),
                        "--manifest",
                        str(manifest),
                        "--json",
                    ],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    check=False,
                )
            executed += 1
            actual_exit = completed.returncode
            actual_findings = observed_findings(completed.stdout)
            passed = (
                actual_exit == case["expectedExit"]
                and actual_findings == case["expectedFindings"]
            )
            if passed:
                accepted += 1
            else:
                discrepancies += 1
            results.append(
                result_record(
                    case,
                    "PASS" if passed else "FAIL",
                    actual_exit=actual_exit,
                    actual_findings=actual_findings,
                    stdout=completed.stdout,
                    stderr=completed.stderr,
                )
            )
        except subprocess.TimeoutExpired as error:
            executed += 1
            discrepancies += 1
            results.append(
                result_record(
                    case,
                    "FAIL",
                    stdout=captured_text(error.stdout),
                    stderr=captured_text(error.stderr),
                    reason="timeout",
                )
            )
        except (OSError, ValueError, json.JSONDecodeError) as error:
            discrepancies += 1
            results.append(
                result_record(
                    case,
                    "FAIL",
                    reason=f"{type(error).__name__}: {error}",
                )
            )

    emit_report(
        make_report(
            selection,
            accepted=accepted,
            total=len(cases),
            executed=executed,
            discrepancies=discrepancies,
            results=results,
        ),
        args.json,
    )
    return 0 if discrepancies == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
