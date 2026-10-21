#!/usr/bin/env python3
"""Exercise the round-23 C1 and C2 counters with disposable Git fixtures.

The fixture contains synthetic receipts only. It is built and discarded in a
TemporaryDirectory; this selftest makes no network requests and does not alter
the repository from which it is run.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROUND = ".ufo/waves/round-23"
BASE = "b5d599e19bead54b96f589444e9ec64cdf67c28a"
TODAY = "2026-10-21"
HEADING = "## Live re-verification — round 23"
ROOT = Path(__file__).resolve().parents[3]


def git(repo: Path, *args: str, text: bool = True) -> str | bytes:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        check=True,
        text=text,
        timeout=120,
    )
    return completed.stdout


def git_show(repo: Path, revision: str, path: str) -> str:
    result = git(repo, "show", f"{revision}:{path}")
    assert isinstance(result, str)
    return result


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def commit_fixture(repo: Path, message: str, paths: list[str]) -> str:
    git(repo, "add", "-f", "-A", "--", *paths)
    git(
        repo,
        "-c",
        "user.name=Round 23 counter selftest",
        "-c",
        "user.email=counter-selftest@example.invalid",
        "commit",
        "--quiet",
        "-m",
        message,
    )
    revision = git(repo, "rev-parse", "HEAD").strip()
    assert isinstance(revision, str)
    return revision


def seed_c1(repo: Path, units: list[dict[str, str]]) -> list[str]:
    paths = [f"{ROUND}/receipts"]
    for unit in units:
        base_text = git_show(repo, BASE, unit["path"])
        anchor = next((line.strip()[:160] for line in base_text.splitlines() if line.strip()), "")
        if not anchor:
            raise AssertionError(f"no usable base anchor for {unit['path']}")

        unit_path = repo / unit["path"]
        current = unit_path.read_text(encoding="utf-8")
        citations = f"[{unit['unit']}:fixture]\n"
        if not current.endswith("\n"):
            current += "\n"
        current += f"\n{HEADING}\n\n{citations}"
        unit_path.write_text(current, encoding="utf-8")
        paths.append(unit["path"])

        write_json(
            repo / ROUND / "receipts" / f"{unit['unit']}.json",
            {
                "unit": unit["unit"],
                "path": unit["path"],
                "observedAt": TODAY,
                "claims": [
                    {
                        "id": "fixture",
                        "anchor": anchor,
                        "claim": "Synthetic claim for the counter selftest.",
                        "surface": "fixture://c1",
                        "method": "read",
                        "observation": "Synthetic fixture observation.",
                        "verdict": "HOLD",
                    }
                ],
            },
        )
    return paths


def audit_fixture_page(repo: Path, page: bytes, url: str, expected: str) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="kake-r23-selftest-audit-") as directory:
        work = Path(directory)
        validator = work / "canonical_audit.py"
        validator.write_bytes((repo / "scripts/canonical_audit.py").read_bytes())
        (work / "page.html").write_bytes(page)
        (work / "manifest.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "pages": [{"url": url, "file": "page.html", "expectedCanonical": expected}],
                }
            ),
            encoding="utf-8",
        )
        completed = subprocess.run(
            [sys.executable, "-B", str(validator), "--manifest", str(work / "manifest.json"), "--json"],
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
    if completed.returncode != 0:
        raise AssertionError(f"fixture canonical audit failed: {completed.stdout} {completed.stderr}")
    return {"exit": completed.returncode, "result": json.loads(completed.stdout)}


def seed_c2(repo: Path, surfaces: list[dict[str, str]]) -> tuple[list[str], str]:
    paths = [f"{ROUND}/live"]
    nonserved_id = surfaces[-1]["id"]
    for surface in surfaces:
        prefix = repo / ROUND / "live" / surface["id"]
        url = surface["url"]
        if surface["id"] == nonserved_id:
            status = 404
            body = b""
            fetch = {
                "url": url,
                "method": "GET",
                "fetchedAt": TODAY + "T00:00:00Z",
                "finalUrl": url,
                "status": status,
                "contentType": "text/html; charset=utf-8",
                "error": None,
                "truncated": False,
                "sha256": hashlib.sha256(body).hexdigest(),
                "bytes": len(body),
            }
            audit = {"verdict": "not-served", "status": status, "exit": None, "error": None}
        else:
            body = (
                "<!doctype html><html><head><link rel=\"canonical\" href=\""
                + surface["expectedCanonical"]
                + "\"></head><body></body></html>\n"
            ).encode("utf-8")
            fetch = {
                "url": url,
                "method": "GET",
                "fetchedAt": TODAY + "T00:00:00Z",
                "finalUrl": url,
                "status": 200,
                "contentType": "text/html; charset=utf-8",
                "error": None,
                "truncated": False,
                "sha256": hashlib.sha256(body).hexdigest(),
                "bytes": len(body),
            }
            (prefix / "page.html").parent.mkdir(parents=True, exist_ok=True)
            (prefix / "page.html").write_bytes(body)
            audit = audit_fixture_page(repo, body, url, surface["expectedCanonical"])
        write_json(prefix / "fetch.json", fetch)
        write_json(prefix / "audit.json", audit)
    return paths, nonserved_id


def run_case(
    repo: Path,
    script_name: str,
    case_name: str,
    revision: str,
    expected_exit: int,
    expected_total: int,
    failure_target: str | None = None,
    expected_problem: str | None = None,
    nonserved_target: str | None = None,
) -> dict[str, object]:
    script_path = repo / ROUND / script_name
    completed = subprocess.run(
        [sys.executable, "-B", str(script_path), "--root", str(repo), "--revision", revision],
        capture_output=True,
        text=True,
        check=False,
        timeout=300,
    )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"{case_name}: counter emitted invalid JSON: exit={completed.returncode}, "
            f"stdout={completed.stdout!r}, stderr={completed.stderr!r}"
        ) from exc

    errors: list[str] = []
    expected_accepted = expected_total if failure_target is None else expected_total - 1
    rows_key = "units" if script_name == "measure_c1.py" else "surfaces"
    rows = result.get(rows_key)
    if completed.returncode != expected_exit:
        errors.append(f"exit {completed.returncode}, expected {expected_exit}")
    if result.get("revision") != revision:
        errors.append(f"revision {result.get('revision')!r}, expected {revision!r}")
    if result.get("accepted") != expected_accepted:
        errors.append(f"accepted {result.get('accepted')!r}, expected {expected_accepted}")
    if result.get("total") != expected_total:
        errors.append(f"total {result.get('total')!r}, expected {expected_total}")
    if not isinstance(rows, list) or len(rows) != expected_total:
        errors.append(f"row count {len(rows) if isinstance(rows, list) else rows!r}, expected {expected_total}")
    else:
        actual_failures = [row.get("id", row.get("unit")) for row in rows if row.get("pass") is not True]
        expected_failures = [] if failure_target is None else [failure_target]
        if actual_failures != expected_failures:
            errors.append(f"failed rows {actual_failures!r}, expected {expected_failures!r}")
        if failure_target is not None:
            target_row = next((row for row in rows if row.get("id", row.get("unit")) == failure_target), None)
            if target_row is None or not any(expected_problem in problem for problem in target_row.get("problems", [])):
                errors.append(f"target {failure_target!r} lacks problem {expected_problem!r}")
        if nonserved_target is not None:
            target_row = next((row for row in rows if row.get("id") == nonserved_target), None)
            if target_row is None or target_row.get("verdict") != "not-served":
                errors.append(f"non-served target {nonserved_target!r} did not report not-served")
            if any(row.get("verdict") != "clean" for row in rows if row.get("id") != nonserved_target):
                errors.append("served fixture surfaces did not all report clean")

    case: dict[str, object] = {
        "case": case_name,
        "command": [sys.executable, "-B", str(script_path), "--root", str(repo), "--revision", revision],
        "exit": completed.returncode,
        "expectedExit": expected_exit,
        "accepted": result.get("accepted"),
        "expectedAccepted": expected_accepted,
        "total": result.get("total"),
        "passed": not errors,
    }
    if errors:
        case["errors"] = errors
        case["stderr"] = completed.stderr
        case["output"] = result
        raise AssertionError(json.dumps(case, sort_keys=True))
    return case


def main() -> int:
    if not (ROOT / ".git").exists():
        raise RuntimeError(f"run this selftest from a Git worktree: {ROOT}")

    cases: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="kake-r23-counter-selftest-") as directory:
        repo = Path(directory) / "repo"
        subprocess.run(
            ["git", "clone", "--quiet", "--no-hardlinks", str(ROOT), str(repo)],
            capture_output=True,
            text=True,
            check=True,
            timeout=300,
        )
        c1_population = json.loads((repo / ROUND / "c1-population.json").read_text(encoding="utf-8"))
        c2_population = json.loads((repo / ROUND / "c2-population.json").read_text(encoding="utf-8"))
        units = c1_population["units"]
        surfaces = c2_population["surfaces"]

        c1_paths = seed_c1(repo, units)
        c2_paths, nonserved_id = seed_c2(repo, surfaces)
        good_revision = commit_fixture(repo, "counter selftest: valid C1 and C2 receipts", c1_paths + c2_paths)
        cases.append(
            run_case(repo, "measure_c1.py", "C1 valid receipts", good_revision, 0, len(units))
        )
        cases.append(
            run_case(
                repo,
                "measure_c2.py",
                "C2 valid live receipts",
                good_revision,
                0,
                len(surfaces),
                nonserved_target=nonserved_id,
            )
        )

        git(repo, "checkout", "--quiet", "--detach", good_revision)
        bad_c1_path = repo / ROUND / "receipts" / f"{units[0]['unit']}.json"
        bad_c1 = json.loads(bad_c1_path.read_text(encoding="utf-8"))
        bad_c1["claims"][0]["anchor"] = "anchor deliberately absent from the base unit"
        write_json(bad_c1_path, bad_c1)
        bad_c1_revision = commit_fixture(
            repo,
            "counter selftest: invalid C1 anchor",
            [f"{ROUND}/receipts/{units[0]['unit']}.json"],
        )
        cases.append(
            run_case(
                repo,
                "measure_c1.py",
                "C1 invalid receipt rejected",
                bad_c1_revision,
                1,
                len(units),
                failure_target=units[0]["unit"],
                expected_problem="anchor not in unit at base",
            )
        )
        git(repo, "checkout", "--quiet", "--detach", good_revision)
        missing_heading_unit = units[1]
        heading_path = repo / missing_heading_unit["path"]
        heading_text = heading_path.read_text(encoding="utf-8")
        if HEADING not in heading_text:
            raise AssertionError(f"fixture heading missing before mutation: {missing_heading_unit['path']}")
        heading_path.write_text(heading_text.replace(HEADING, ""), encoding="utf-8")
        missing_heading_revision = commit_fixture(
            repo,
            "counter selftest: missing C1 section heading",
            [missing_heading_unit["path"]],
        )
        cases.append(
            run_case(
                repo,
                "measure_c1.py",
                "C1 missing heading rejected with diagnostic",
                missing_heading_revision,
                1,
                len(units),
                failure_target=missing_heading_unit["unit"],
                expected_problem="round-23 heading missing in unit file",
            )
        )

        git(repo, "checkout", "--quiet", "--detach", good_revision)
        bad_c2_path = repo / ROUND / "live" / surfaces[0]["id"] / "audit.json"
        bad_c2 = json.loads(bad_c2_path.read_text(encoding="utf-8"))
        bad_c2["result"]["verdict"] = "failed-policy"
        write_json(bad_c2_path, bad_c2)
        bad_c2_revision = commit_fixture(
            repo,
            "counter selftest: unreproducible C2 audit receipt",
            [f"{ROUND}/live/{surfaces[0]['id']}/audit.json"],
        )
        cases.append(
            run_case(
                repo,
                "measure_c2.py",
                "C2 unreproducible receipt rejected",
                bad_c2_revision,
                1,
                len(surfaces),
                failure_target=surfaces[0]["id"],
                expected_problem="audit.json",
            )
        )

        git(repo, "checkout", "--quiet", "--detach", good_revision)
        unverifiable_path = repo / ROUND / "receipts" / f"{units[2]['unit']}.json"
        unverifiable = json.loads(unverifiable_path.read_text(encoding="utf-8"))
        for claim in unverifiable["claims"]:
            claim["verdict"] = "UNVERIFIABLE"
            claim["reason"] = "surface absent (selftest)"
        write_json(unverifiable_path, unverifiable)
        unverifiable_revision = commit_fixture(
            repo, "counter selftest: all-UNVERIFIABLE C1 receipt", [f"{ROUND}/receipts/{units[2]['unit']}.json"]
        )
        cases.append(
            run_case(repo, "measure_c1.py", "C1 all-UNVERIFIABLE receipt rejected", unverifiable_revision, 1,
                     len(units), failure_target=units[2]["unit"], expected_problem="no claim decided live")
        )

        git(repo, "checkout", "--quiet", "--detach", good_revision)
        method_path = repo / ROUND / "live" / surfaces[1]["id"] / "fetch.json"
        method = json.loads(method_path.read_text(encoding="utf-8"))
        method["method"] = "HEAD"
        write_json(method_path, method)
        method_revision = commit_fixture(
            repo, "counter selftest: non-GET C2 fetch", [f"{ROUND}/live/{surfaces[1]['id']}/fetch.json"]
        )
        cases.append(
            run_case(repo, "measure_c2.py", "C2 non-GET fetch rejected", method_revision, 1, len(surfaces),
                     failure_target=surfaces[1]["id"], expected_problem="GET")
        )

        # Regression inputs target checks the seven-case detector did not cover
        # (w2/MutateCounterSelftest: 58/71 mutants survived the initial suite).
        for field, value, problem in (
            ("unit", "wrong-unit", "unit/path mismatch"),
            ("path", "wrong-path.md", "unit/path mismatch"),
            ("observedAt", "2026-10-20", "observedAt"),
            ("claims", [], "no claims"),
        ):
            git(repo, "checkout", "--quiet", "--detach", good_revision)
            rel = f"{ROUND}/receipts/{units[0]['unit']}.json"
            payload = json.loads((repo / rel).read_text())
            payload[field] = value
            write_json(repo / rel, payload)
            rev = commit_fixture(repo, f"selftest: C1 {field}", [rel])
            cases.append(run_case(repo, "measure_c1.py", f"C1 invalid {field}", rev, 1, len(units),
                                  failure_target=units[0]["unit"], expected_problem=problem))
        claim_variants = [
            (f"missing-{field}", {field: ""}, "missing field")
            for field in ("id", "anchor", "claim", "surface", "method", "observation", "verdict")
        ] + [
            ("unknown-verdict", {"verdict": "PASS"}, "verdict"),
            ("stale-without-correction", {"verdict": "STALE"}, "STALE without correction"),
            ("stale-correction-absent", {"verdict": "STALE", "correction": "not appended correction"}, "correction not in"),
            ("unverifiable-without-reason", {"verdict": "UNVERIFIABLE"}, "UNVERIFIABLE without reason"),
        ]
        for name, changes, problem in claim_variants:
            git(repo, "checkout", "--quiet", "--detach", good_revision)
            rel = f"{ROUND}/receipts/{units[0]['unit']}.json"
            payload = json.loads((repo / rel).read_text())
            payload["claims"][0].update(changes)
            write_json(repo / rel, payload)
            rev = commit_fixture(repo, f"selftest: C1 {name}", [rel])
            cases.append(run_case(repo, "measure_c1.py", f"C1 {name}", rev, 1, len(units),
                                  failure_target=units[0]["unit"], expected_problem=problem))
        for field, value, problem in (
            ("url", "https://wrong.test/", "url/method"),
            ("fetchedAt", "2026-10-20", "fetchedAt"),
            ("sha256", "0" * 64, "digest differs"),
            ("bytes", 0, "length differs"),
            ("status", None, "usable HTTP response"),
        ):
            git(repo, "checkout", "--quiet", "--detach", good_revision)
            rel = f"{ROUND}/live/{surfaces[0]['id']}/fetch.json"
            payload = json.loads((repo / rel).read_text())
            payload[field] = value
            write_json(repo / rel, payload)
            rev = commit_fixture(repo, f"selftest: C2 {field}", [rel])
            cases.append(run_case(repo, "measure_c2.py", f"C2 invalid {field}", rev, 1, len(surfaces),
                                  failure_target=surfaces[0]["id"], expected_problem=problem))

    print(json.dumps({"selftest": "passed", "cases": cases}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, subprocess.SubprocessError, ValueError) as exc:
        print(f"counter_selftest: {exc}", file=sys.stderr)
        raise SystemExit(1)
