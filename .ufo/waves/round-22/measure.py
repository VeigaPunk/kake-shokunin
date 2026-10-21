#!/usr/bin/env python3
"""Run the frozen round-22 canonical matrix against one Git revision."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from typing import Any

BASE_REVISION = "7c61c8cc791bde36dd5e3688bdfea2678d90146c"
EXPECTED_CASES = (
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
BASELINE_TOTAL = len(EXPECTED_CASES)
VALIDATOR = "scripts/canonical_audit.py"
ROUND_DIR = ".ufo/waves/round-22"
MATRIX = f"{ROUND_DIR}/matrix.py"
CASES = f"{ROUND_DIR}/cases.json"
FIXTURES = f"{ROUND_DIR}/fixtures"
# The traversal manifest resolves ../escape.html to this fixture-root file.
ESCAPE_FIXTURE = f"{FIXTURES}/escape.html"
# Frozen instrument identity (c0fd6d5). A runner that trusts matrix-reported rows
# cannot prove the validator ran, so the matrix and oracle bytes themselves are
# pinned: a self-consistent stub matrix is rejected before its rows are read.
PINNED_INSTRUMENT_SHA256 = {
    MATRIX: "d7de622cf149c4a7a0d3152b3d6c0560fadcc4c0c784c764502d0a2110bf4aab",
    CASES: "28a49013d3aaf72b0e1c3801fd5359592602e079408d9a71c99f2df03d1cbeb6",
}


class MeasurementError(Exception):
    """The requested revision or measurement instrument cannot be read."""


@dataclass(frozen=True)
class Blob:
    path: str
    data: bytes
    git_object: str | None
    mode: str | None
    source: str
    file_mode: str | None = None

    def pin(self) -> dict[str, str | None]:
        return {
            "sha256": hashlib.sha256(self.data).hexdigest(),
            "gitObject": self.git_object,
            "gitMode": self.mode,
            "fileMode": self.file_mode,
            "source": self.source,
        }


def git(root: pathlib.Path, *args: str) -> bytes:
    """Run a read-only Git command without a shell."""
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise MeasurementError(f"cannot run git: {exc}") from exc
    if completed.returncode:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise MeasurementError(detail or f"git {' '.join(args)} failed")
    return completed.stdout


def resolve_revision(root: pathlib.Path, revision: str) -> str:
    if not revision or revision.startswith("-"):
        raise MeasurementError("revision must be a Git commit hash or commit-ish")
    try:
        value = git(
            root,
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{revision}^{{commit}}",
        ).decode("ascii").strip()
    except UnicodeDecodeError as exc:
        raise MeasurementError("git returned a non-ASCII revision") from exc
    if not re.fullmatch(r"[0-9a-fA-F]{40,64}", value):
        raise MeasurementError(f"git returned an invalid commit id: {value!r}")
    return value.lower()


def is_instrument_path(path: str) -> bool:
    return path in (MATRIX, CASES, ESCAPE_FIXTURE) or path.startswith(FIXTURES + "/")


def safe_repo_path(path: str) -> bool:
    candidate = pathlib.PurePosixPath(path)
    return (
        not candidate.is_absolute()
        and bool(candidate.parts)
        and all(part not in ("", ".", "..") for part in candidate.parts)
    )


def tree_blobs(root: pathlib.Path, revision: str, include_validator: bool) -> dict[str, tuple[str, str]]:
    pathspecs = [MATRIX, CASES, FIXTURES]
    if include_validator:
        pathspecs.insert(0, VALIDATOR)
    raw = git(root, "ls-tree", "-r", "-z", "--full-tree", revision, "--", *pathspecs)
    blobs: dict[str, tuple[str, str]] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, separator, encoded_path = record.partition(b"\t")
        if not separator:
            raise MeasurementError("git ls-tree returned a malformed record")
        try:
            mode, object_type, object_id = metadata.decode("ascii").split()
            path = os.fsdecode(encoded_path)
        except (UnicodeDecodeError, ValueError) as exc:
            raise MeasurementError("git ls-tree returned malformed metadata") from exc
        if not safe_repo_path(path):
            raise MeasurementError(f"unsafe path in measurement tree: {path!r}")
        if path != VALIDATOR and not is_instrument_path(path):
            continue
        if object_type != "blob" or mode not in ("100644", "100755"):
            raise MeasurementError(f"measurement input is not a regular Git blob: {path}")
        blobs[path] = (object_id, mode)
    return blobs


def read_git_blobs(root: pathlib.Path, entries: dict[str, tuple[str, str]]) -> dict[str, Blob]:
    result: dict[str, Blob] = {}
    for path in sorted(entries):
        object_id, mode = entries[path]
        data = git(root, "cat-file", "blob", object_id)
        result[path] = Blob(path, data, object_id, mode, "git")
    return result


def instrument_complete(blobs: dict[str, Blob]) -> bool:
    return (
        MATRIX in blobs
        and CASES in blobs
        and ESCAPE_FIXTURE in blobs
        and any(path.startswith(FIXTURES + "/") for path in blobs)
    )

def population_error(case_ids: list[str], label: str) -> str | None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for case_id in case_ids:
        if case_id in seen:
            duplicates.add(case_id)
        seen.add(case_id)
    expected = set(EXPECTED_CASES)
    missing = sorted(expected - seen)
    extra = sorted(seen - expected)
    problems = []
    if duplicates:
        problems.append("duplicates=" + ",".join(sorted(duplicates)))
    if missing:
        problems.append("missing=" + ",".join(missing))
    if extra:
        problems.append("extra=" + ",".join(extra))
    return f"{label} case population mismatch: {'; '.join(problems)}" if problems else None


def manifest_case_ids(blob: Blob) -> list[str]:
    try:
        document = json.loads(blob.data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MeasurementError(f"{CASES} is not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(document, dict) or document.get("version") != 1:
        raise MeasurementError(f"{CASES} must be a version-1 object")
    rows = document.get("cases")
    if not isinstance(rows, list):
        raise MeasurementError(f"{CASES} must contain a cases array")
    case_ids = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or not isinstance(row.get("caseId"), str):
            raise MeasurementError(f"{CASES} case row {index} has no string caseId")
        case_ids.append(row["caseId"])
    return case_ids


def result_case_ids(results: list[Any]) -> list[str]:
    case_ids: list[str] = []
    marker = re.compile(r"(?:^|\s)caseId=([A-Za-z0-9_-]+)(?:\s|$)")
    for index, row in enumerate(results):
        case_id = row.get("caseId") if isinstance(row, dict) else None
        if isinstance(row, str):
            match = marker.search(row)
            case_id = match.group(1) if match else None
        elif isinstance(row, dict) and not isinstance(case_id, str):
            line = row.get("result")
            if isinstance(line, str):
                match = marker.search(line)
                case_id = match.group(1) if match else None
        if not isinstance(case_id, str):
            raise MeasurementError(f"matrix result row {index} has no caseId")
        case_ids.append(case_id)
    return case_ids


def invalid_population_result(
    revision: str,
    pins: dict[str, Any],
    instrument_revision: str,
    error: str,
    results: list[Any] | None = None,
) -> dict[str, Any]:
    return {
        "revision": revision,
        "available": False,
        "unavailable": True,
        "accepted": 0,
        "total": BASELINE_TOTAL,
        "results": results or [],
        "blobs": pins,
        "instrumentRevision": instrument_revision,
        "expectedCaseIds": list(EXPECTED_CASES),
        "error": error,
    }



def checked_worktree_path(root: pathlib.Path, relative: str, want_directory: bool) -> pathlib.Path:
    if not safe_repo_path(relative):
        raise MeasurementError(f"unsafe --cases-root path: {relative!r}")
    path = root
    parts = pathlib.PurePosixPath(relative).parts
    for index, part in enumerate(parts):
        path = path / part
        try:
            info = path.lstat()
        except OSError as exc:
            raise MeasurementError(f"cannot inspect {relative} in --cases-root: {exc}") from exc
        if stat.S_ISLNK(info.st_mode):
            raise MeasurementError(f"--cases-root path contains a symlink: {relative}")
        if index < len(parts) - 1 and not stat.S_ISDIR(info.st_mode):
            raise MeasurementError(f"--cases-root parent is not a directory: {relative}")
    expected = stat.S_ISDIR if want_directory else stat.S_ISREG
    if not expected(info.st_mode):
        kind = "directory" if want_directory else "regular file"
        raise MeasurementError(f"--cases-root path is not a {kind}: {relative}")
    return path


def read_worktree_file(root: pathlib.Path, relative: str) -> tuple[bytes, str]:
    path = checked_worktree_path(root, relative, want_directory=False)
    try:
        data = path.read_bytes()
        file_mode = f"{stat.S_IMODE(path.lstat().st_mode):04o}"
        return data, file_mode
    except OSError as exc:
        raise MeasurementError(f"cannot read {relative} from --cases-root: {exc}") from exc


def read_worktree_instrument(root: pathlib.Path) -> dict[str, Blob]:
    blobs: dict[str, Blob] = {}
    for relative in (MATRIX, CASES):
        data, file_mode = read_worktree_file(root, relative)
        blobs[relative] = Blob(
            relative, data, None, None, "working-tree", file_mode
        )

    fixture_root = checked_worktree_path(root, FIXTURES, want_directory=True)

    def visit(directory: pathlib.Path, prefix: str) -> None:
        try:
            with os.scandir(directory) as scan:
                entries = sorted(scan, key=lambda item: item.name)
        except OSError as exc:
            raise MeasurementError(f"cannot list {directory}: {exc}") from exc
        for entry in entries:
            relative = f"{prefix}/{entry.name}"
            if not safe_repo_path(relative):
                raise MeasurementError(f"unsafe fixture path: {relative!r}")
            try:
                entry_stat = entry.stat(follow_symlinks=False)
            except OSError as exc:
                raise MeasurementError(f"cannot inspect fixture {relative}: {exc}") from exc
            if stat.S_ISDIR(entry_stat.st_mode):
                visit(pathlib.Path(entry.path), relative)
            elif stat.S_ISREG(entry_stat.st_mode):
                try:
                    data = pathlib.Path(entry.path).read_bytes()
                except OSError as exc:
                    raise MeasurementError(f"cannot read fixture {relative}: {exc}") from exc
                blobs[relative] = Blob(
                    relative,
                    data,
                    None,
                    None,
                    "working-tree",
                    f"{stat.S_IMODE(entry_stat.st_mode):04o}",
                )
            else:
                raise MeasurementError(f"fixture is not a regular file: {relative}")

    visit(fixture_root, FIXTURES)
    if ESCAPE_FIXTURE not in blobs:
        raise MeasurementError(f"--cases-root is missing required {ESCAPE_FIXTURE}")
    return blobs


def candidate_instrument(root: pathlib.Path) -> tuple[dict[str, Blob], str]:
    """Prefer a complete committed instrument, then a complete working tree."""
    try:
        head = resolve_revision(root, "HEAD")
        entries = tree_blobs(root, head, include_validator=False)
    except MeasurementError:
        return read_worktree_instrument(root), "working-tree"
    committed = read_git_blobs(root, entries)
    if instrument_complete(committed):
        return committed, head
    return read_worktree_instrument(root), "working-tree"


def materialize(workspace: pathlib.Path, blobs: dict[str, Blob]) -> None:
    for relative, blob in sorted(blobs.items()):
        if not safe_repo_path(relative):
            raise MeasurementError(f"unsafe materialization path: {relative!r}")
        destination = workspace.joinpath(*pathlib.PurePosixPath(relative).parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(blob.data)
        if blob.mode == "100755":
            destination.chmod(0o755)


def unavailable_result(
    revision: str,
    error: str | None = None,
    pins: dict[str, Any] | None = None,
    instrument_revision: str | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "revision": revision,
        "available": False,
        "unavailable": True,
        "accepted": 0,
        "total": BASELINE_TOTAL,
        "results": [],
        "blobs": pins or {},
        "expectedCaseIds": list(EXPECTED_CASES),
    }
    if instrument_revision is not None:
        result["instrumentRevision"] = instrument_revision
    if error:
        result["error"] = error
    return result


def emit(result: dict[str, Any]) -> None:
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


def run_measurement(root: pathlib.Path, revision_arg: str, cases_root_arg: str | None) -> tuple[dict[str, Any], int]:
    revision = resolve_revision(root, revision_arg)
    entries = tree_blobs(root, revision, include_validator=True)
    validator_entry = entries.get(VALIDATOR)
    if validator_entry is None and revision != BASE_REVISION:
        result = unavailable_result(
            revision, "revision has no scripts/canonical_audit.py blob"
        )
        return result, 2

    target = (
        read_git_blobs(root, {VALIDATOR: validator_entry})
        if validator_entry is not None
        else {}
    )
    revision_instrument = read_git_blobs(
        root, {path: entry for path, entry in entries.items() if is_instrument_path(path)}
    )
    instrument_revision = revision
    if validator_entry is None and cases_root_arg is not None:
        cases_root = pathlib.Path(cases_root_arg).expanduser().resolve(strict=True)
        if not cases_root.is_dir():
            raise MeasurementError("--cases-root must name a directory")
        instrument, instrument_revision = candidate_instrument(cases_root)
    elif instrument_complete(revision_instrument):
        instrument = revision_instrument
    elif cases_root_arg is not None:
        cases_root = pathlib.Path(cases_root_arg).expanduser().resolve(strict=True)
        if not cases_root.is_dir():
            raise MeasurementError("--cases-root must name a directory")
        instrument, instrument_revision = candidate_instrument(cases_root)
    else:
        missing = [
            name for name, present in (
                (MATRIX, MATRIX in revision_instrument),
                (CASES, CASES in revision_instrument),
                (FIXTURES, any(path.startswith(FIXTURES + "/") for path in revision_instrument)),
                (ESCAPE_FIXTURE, ESCAPE_FIXTURE in revision_instrument),
            ) if not present
        ]
        if validator_entry is None:
            partial = {**target, **revision_instrument}
            pins = {path: blob.pin() for path, blob in sorted(partial.items())}
            result = unavailable_result(
                revision,
                "baseline validator missing and no complete instrument; "
                "supply --cases-root <candidate root>",
                pins=pins,
                instrument_revision=revision,
            )
            result["instrumentValidated"] = False
            result["missingInstrumentPaths"] = missing
            return result, 2
        raise MeasurementError(
            "revision lacks frozen matrix inputs: " + ", ".join(missing) +
            "; supply --cases-root <candidate root>"
        )

    if not instrument_complete(instrument):
        if validator_entry is None:
            measured = {**target, **instrument}
            pins = {path: blob.pin() for path, blob in sorted(measured.items())}
            result = unavailable_result(
                revision,
                "baseline validator missing and frozen instrument is incomplete",
                pins=pins,
                instrument_revision=instrument_revision,
            )
            result["instrumentValidated"] = False
            return result, 2
        raise MeasurementError("frozen measurement instrument is incomplete")

    measured_blobs = {**target, **instrument}
    pins = {path: blob.pin() for path, blob in sorted(measured_blobs.items())}

    tampered = [
        path for path, digest in PINNED_INSTRUMENT_SHA256.items()
        if hashlib.sha256(instrument[path].data).hexdigest() != digest
    ]
    if tampered:
        result = invalid_population_result(
            revision, pins, instrument_revision,
            "frozen instrument digest mismatch: " + ", ".join(tampered),
        )
        result["instrumentValidated"] = False
        return result, 2

    try:
        manifest_ids = manifest_case_ids(instrument[CASES])
    except MeasurementError as exc:
        return invalid_population_result(
            revision, pins, instrument_revision, str(exc)
        ), 2
    manifest_error = population_error(manifest_ids, "cases.json")
    if manifest_error:
        return invalid_population_result(
            revision, pins, instrument_revision, manifest_error
        ), 2

    if validator_entry is None:
        result = unavailable_result(
            revision,
            "revision has no scripts/canonical_audit.py blob",
            pins=pins,
            instrument_revision=instrument_revision,
        )
        result["instrumentValidated"] = True
        return result, 0

    with tempfile.TemporaryDirectory(prefix="kake-r22-measure-") as temporary:
        workspace = pathlib.Path(temporary)
        materialize(workspace, measured_blobs)
        matrix_path = workspace.joinpath(*pathlib.PurePosixPath(MATRIX).parts)
        try:
            completed = subprocess.run(
                [sys.executable, str(matrix_path), "--root", str(workspace), "--json"],
                cwd=workspace,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
        except OSError as exc:
            result = {
                "revision": revision,
                "available": True,
                "unavailable": False,
                "accepted": 0,
                "total": BASELINE_TOTAL,
                "results": [],
                "blobs": pins,
                "instrumentRevision": instrument_revision,
                "matrixError": f"cannot invoke matrix.py: {exc}",
                "expectedCaseIds": list(EXPECTED_CASES),
                "matrixStdout": "",
                "matrixStderr": "",
            }
            return result, 1

    try:
        matrix_result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        result = {
            "revision": revision,
            "available": True,
            "unavailable": False,
            "accepted": 0,
            "total": BASELINE_TOTAL,
            "results": [],
            "blobs": pins,
            "instrumentRevision": instrument_revision,
            "matrixExitCode": completed.returncode,
            "matrixError": f"matrix.py did not emit JSON: {exc}",
            "expectedCaseIds": list(EXPECTED_CASES),
            "matrixStderr": completed.stderr,
            "matrixStdout": completed.stdout,
        }
        return result, 1

    if not isinstance(matrix_result, dict):
        result = invalid_population_result(
            revision, pins, instrument_revision, "matrix.py JSON result must be an object"
        )
        result["matrixExitCode"] = completed.returncode
        result["matrixStdout"] = completed.stdout
        result["matrixStderr"] = completed.stderr
        return result, 1
    accepted = matrix_result.get("accepted")
    total = matrix_result.get("total")
    results = matrix_result.get("results")
    if type(accepted) is not int or type(total) is not int or not isinstance(results, list):
        result = invalid_population_result(
            revision,
            pins,
            instrument_revision,
            "matrix.py JSON must contain integer accepted/total and results array",
        )
        result["matrixExitCode"] = completed.returncode
        result["matrixStdout"] = completed.stdout
        result["matrixStderr"] = completed.stderr
        return result, 1
    try:
        result_ids = result_case_ids(results)
    except MeasurementError as exc:
        result = invalid_population_result(
            revision, pins, instrument_revision, str(exc), results
        )
        result["matrixExitCode"] = completed.returncode
        result["reportedAccepted"] = accepted
        result["reportedTotal"] = total
        result["matrixStdout"] = completed.stdout
        result["matrixStderr"] = completed.stderr
        return result, 1
    results_error = population_error(result_ids, "matrix results")
    if total != BASELINE_TOTAL or len(results) != BASELINE_TOTAL:
        count_error = (
            f"matrix results count mismatch: declared={total}, rows={len(results)}, "
            f"required={BASELINE_TOTAL}"
        )
        results_error = f"{results_error}; {count_error}" if results_error else count_error
    if results_error:
        result = invalid_population_result(
            revision, pins, instrument_revision, results_error, results
        )
        result["matrixExitCode"] = completed.returncode
        result["reportedAccepted"] = accepted
        result["matrixStdout"] = completed.stdout
        result["matrixStderr"] = completed.stderr
        result["reportedTotal"] = total
        return result, 1
    try:
        oracle = oracle_expectations(instrument[CASES])
    except MeasurementError as exc:
        return invalid_population_result(revision, pins, instrument_revision, str(exc), results), 1
    derived, problems = reconcile_rows(results, oracle, matrix_result, completed.returncode)
    if problems:
        result = invalid_population_result(
            revision, pins, instrument_revision, "; ".join(problems), results
        )
        result["matrixExitCode"] = completed.returncode
        result["reportedAccepted"] = accepted
        result["derivedAccepted"] = derived
        result["reportedTotal"] = total
        result["matrixStdout"] = completed.stdout
        result["matrixStderr"] = completed.stderr
        return result, 1
    result = {
        "revision": revision,
        "available": True,
        "unavailable": False,
        "accepted": derived,
        "acceptedDerivedFromRows": True,
        "total": total,
        "expectedCaseIds": list(EXPECTED_CASES),
        "results": results,
        "blobs": pins,
        "instrumentRevision": instrument_revision,
        "matrixExitCode": completed.returncode,
        "matrixStdout": completed.stdout,
        "matrixStderr": completed.stderr,
    }
    failed = completed.returncode != 0 or derived != total
    return result, 1 if failed else 0


def oracle_expectations(blob: Blob) -> dict[str, tuple[int, list[str]]]:
    """Per-case expected exit and finding ids from the pinned cases.json blob."""
    document = json.loads(blob.data.decode("utf-8"))
    oracle: dict[str, tuple[int, list[str]]] = {}
    for row in document["cases"]:
        expected_exit = row.get("expectedExit")
        expected_findings = row.get("expectedFindings")
        if type(expected_exit) is not int or not isinstance(expected_findings, list):
            raise MeasurementError(f"{CASES} row {row.get('caseId')!r} lacks expectedExit/expectedFindings")
        oracle[row["caseId"]] = (expected_exit, expected_findings)
    return oracle


def reconcile_rows(
    results: list[Any],
    oracle: dict[str, tuple[int, list[str]]],
    matrix_result: dict[str, Any],
    matrix_exit: int,
) -> tuple[int, list[str]]:
    """Recompute acceptance from per-case rows; never trust a declared numerator."""
    problems: list[str] = []
    derived = 0
    for row in results:
        if not isinstance(row, dict):
            problems.append("matrix result row is not an object")
            continue
        case_id = row.get("caseId")
        expected = oracle.get(case_id)
        if expected is None:
            problems.append(f"{case_id!r}: no frozen oracle row")
            continue
        actual_exit = row.get("actualExit")
        matches = (
            type(actual_exit) is int
            and actual_exit == expected[0]
            and row.get("actualFindings") == expected[1]
        )
        if (row.get("status") == "PASS") != matches:
            problems.append(f"{case_id}: status {row.get('status')!r} disagrees with oracle comparison")
        if matches:
            derived += 1
    if matrix_result.get("accepted") != derived:
        problems.append(f"declared accepted={matrix_result.get('accepted')!r} != derived {derived}")
    executed = matrix_result.get("executed")
    if type(executed) is not int or not derived <= executed <= len(results):
        problems.append(f"executed={executed!r} is not a count between derived {derived} and the result rows")
    if matrix_result.get("discrepancies") != len(results) - derived:
        problems.append(
            f"discrepancies={matrix_result.get('discrepancies')!r} != rows-derived {len(results) - derived}"
        )
    expected_matrix_exit = 0 if derived == len(results) else 1
    if matrix_exit != expected_matrix_exit:
        problems.append(f"matrix exit {matrix_exit} != {expected_matrix_exit} implied by rows")
    return derived, problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Git repository containing the measured revision")
    parser.add_argument("--revision", required=True, help="commit hash whose validator is measured")
    parser.add_argument(
        "--cases-root",
        help="candidate checkout supplying a frozen matrix when the revision lacks it",
    )
    args = parser.parse_args(argv)
    try:
        root = pathlib.Path(args.root).expanduser().resolve(strict=True)
        if not root.is_dir():
            raise MeasurementError("--root must name a directory")
        result, exit_code = run_measurement(root, args.revision, args.cases_root)
    except (MeasurementError, OSError, RuntimeError) as exc:
        result = {
            "revision": args.revision,
            "available": False,
            "unavailable": True,
            "accepted": 0,
            "total": BASELINE_TOTAL,
            "results": [],
            "blobs": {},
            "error": str(exc),
            "expectedCaseIds": list(EXPECTED_CASES),
        }
        exit_code = 2
    result["runnerSha256"] = hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    emit(result)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
