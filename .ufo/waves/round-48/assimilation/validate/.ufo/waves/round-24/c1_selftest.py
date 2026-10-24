#!/usr/bin/env python3
"""Hermetic regression checks for measure_c1.py using a throwaway Git clone."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import measure_c1 as counter

SOURCE_ROOT = Path(__file__).resolve().parents[3]
FROZEN_POPULATION_SOURCE = Path("/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-24/c1-population.json")
FIXTURE_COMMIT_DATE = "2026-10-21T12:00:00Z"
VALID_OBSERVED_AT = "2026-10-21T00:00:00Z"


class SelftestFailure(Exception):
    pass


def run(args: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[bytes]:
    try:
        result = subprocess.run(args, cwd=cwd, env=env, capture_output=True, check=False)
    except OSError as exc:
        raise SelftestFailure(f"cannot run {args[0]}: {exc}") from exc
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", "replace").strip()
        raise SelftestFailure(f"command failed ({result.returncode}): {' '.join(args)}: {stderr}")
    return result


def git(repo: Path, *args: str, env: dict[str, str] | None = None) -> bytes:
    return run(["git", "-C", str(repo), *args], env=env).stdout


def put_json(repo: Path, path: str, value: Any) -> None:
    file = repo / path
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def base_line(repo: Path, path: str, number: int) -> bytes:
    lines = counter.required_blob(str(repo), counter.BASE, path).splitlines()
    if number > len(lines):
        raise SelftestFailure(f"base citation line unavailable: {path}:{number}")
    return lines[number - 1]


def correction_note(target: dict[str, Any], kind: str) -> str:
    if kind == "absent":
        return (f"As of 2026-10-21, {target['id']} {target['token']} is absent; event: unknown. "
                "This citation is a historical record, not an executable instruction.")
    return (f"As of 2026-10-21, {target['id']} {target['token']} is present in the isolated filesystem. "
            "The earlier presence-dependent statement remains historical and unverified.")


def add_eof_block(repo: Path, path: str, notes: list[tuple[str, str]]) -> None:
    file = repo / path
    file.parent.mkdir(parents=True, exist_ok=True)
    original = file.read_bytes() if file.exists() else b"# Round-24 lesson correction register\n"
    if original and not original.endswith(b"\n"):
        raise SelftestFailure(f"fixture source does not end on a complete line: {path}")
    separator = b"\n" if original and not original.endswith(b"\n\n") else b""
    content = original + separator + b"## Round-24 path reconciliation\n\n"
    for cite, note in notes:
        content += f"- `{cite}`: {note}\n".encode("utf-8")
    file.write_bytes(content)


def isolated_home(home: Path, targets: list[dict[str, Any]]) -> None:
    projects = home / "Projects"
    if projects.exists():
        shutil.rmtree(projects)
    for target in targets:
        if target["class"] != "recovered":
            continue
        path = home / target["token"][2:]
        if target["token"].endswith("/CNAME"):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("ds4cc.com\n", encoding="utf-8")
        else:
            path.mkdir(parents=True, exist_ok=True)


def create_fixture(repo: Path, targets: list[dict[str, Any]], population_raw: bytes) -> set[str]:
    entries: list[dict[str, Any]] = []
    correction_notes: dict[str, list[tuple[str, str]]] = {}
    touched = {counter.POPULATION, counter.SIDECAR, counter.CENTRAL_LESSON}
    population_path = repo / counter.POPULATION
    population_path.parent.mkdir(parents=True, exist_ok=True)
    population_path.write_bytes(population_raw)

    def add_entry(target: dict[str, Any], cite: str, kind: str) -> None:
        path, line = counter.parse_cite(cite)
        note = correction_note(target, kind)
        entries.append({
            "file": path,
            "line": line,
            "token": target["token"],
            "lineSha256": hashlib.sha256(base_line(repo, path, line)).hexdigest(),
            "kind": kind,
            "date": "2026-10-21",
            "note": note,
        })
        block_path = counter.CENTRAL_LESSON if counter.is_non_author(path) else path
        correction_notes.setdefault(block_path, []).append((cite, note))
        touched.add(path)
        touched.add(block_path)

    for target in targets:
        if target["class"] == "drift":
            for cite in target["unannotatedCites"]:
                add_entry(target, cite, "absent")
        elif target["class"] == "recovered":
            for cite in target["cites"]:
                add_entry(target, cite, "restored")

    entries.sort(key=lambda entry: (entry["file"], entry["line"], entry["token"]))
    put_json(repo, counter.SIDECAR, {"schema": counter.SIDECAR_SCHEMA, "entries": entries})
    for path, notes in sorted(correction_notes.items()):
        add_eof_block(repo, path, notes)

    for target in targets:
        state = "present" if target["class"] == "recovered" else "absent"
        receipt = {
            "id": target["id"],
            "token": target["token"],
            "class": target["class"],
            "observedAt": VALID_OBSERVED_AT,
            "state": state,
            "observation": {
                "commands": [f"stat -- {target['token']}"] ,
                "output": f"{state} in isolated HOME",
            },
        }
        receipt_path = f"{counter.RECEIPTS}/{target['id']}.json"
        put_json(repo, receipt_path, receipt)
        touched.add(receipt_path)

    for path in sorted({entry["file"] for entry in entries}):
        original = counter.required_blob(str(repo), counter.BASE, path)
        current = (repo / path).read_bytes()
        if counter.is_non_author(path):
            if current != original:
                raise SelftestFailure(f"non-author citation file changed: {path}")
        elif not current.startswith(original):
            raise SelftestFailure(f"prior citation bytes changed instead of receiving an EOF block: {path}")
    return touched


def commit(repo: Path, message: str) -> str:
    env = os.environ.copy()
    env.update({
        "GIT_AUTHOR_NAME": "C1 selftest",
        "GIT_AUTHOR_EMAIL": "c1-selftest@example.invalid",
        "GIT_COMMITTER_NAME": "C1 selftest",
        "GIT_COMMITTER_EMAIL": "c1-selftest@example.invalid",
        "GIT_AUTHOR_DATE": FIXTURE_COMMIT_DATE,
        "GIT_COMMITTER_DATE": FIXTURE_COMMIT_DATE,
    })
    run(["git", "-C", str(repo), "add", "-A"], env=env)
    run(["git", "-C", str(repo), "commit", "--allow-empty", "--quiet", "-m", message], env=env)
    return git(repo, "rev-parse", "HEAD").decode("ascii").strip()


def all_target_checks(repo: Path, revision: str, targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sidecar = counter.load_sidecar(str(repo), revision)
    commit_time = counter.committer_time(str(repo), revision)
    base_lines: dict[tuple[str, int], bytes] = {}
    current_lines: dict[tuple[str, str], list[bytes]] = {}
    sweep_tokens = (set(), set(), set())
    return [counter.check_target(str(repo), revision, target, commit_time, sweep_tokens,
                                 sidecar, base_lines, current_lines)
            for target in targets]


def one_target_check(repo: Path, revision: str, target_id: str,
                     sweep_tokens: tuple[set[str], set[str], set[str]]) -> dict[str, Any]:
    targets = counter.parse_population(str(repo), revision)
    target = next(item for item in targets if item["id"] == target_id)
    sidecar = counter.load_sidecar(str(repo), revision)
    return counter.check_target(str(repo), revision, target, counter.committer_time(str(repo), revision),
                                sweep_tokens, sidecar, {}, {})


def write_snapshot(repo: Path, snapshot: dict[str, bytes]) -> None:
    for relative, data in snapshot.items():
        file = repo / relative
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(data)


def fail_case(repo: Path, home: Path, snapshot: dict[str, bytes], targets: list[dict[str, Any]],
              target_id: str, name: str, mutate: Any, expected_problem: str,
              assertions: dict[str, int], sweep_tokens: tuple[set[str], set[str], set[str]] | None = None) -> None:
    write_snapshot(repo, snapshot)
    isolated_home(home, targets)
    mutate()
    revision = commit(repo, f"selftest {name}")
    result = one_target_check(repo, revision, target_id, sweep_tokens or (set(), set(), set()))
    if result["pass"] or not any(expected_problem in problem for problem in result["problems"]):
        raise SelftestFailure(f"{name} did not fail as expected: {result}")
    assertions["count"] += 1


def input_case(repo: Path, home: Path, snapshot: dict[str, bytes], targets: list[dict[str, Any]],
               name: str, mutate: Any, check: Any, assertions: dict[str, int]) -> None:
    write_snapshot(repo, snapshot)
    isolated_home(home, targets)
    mutate()
    revision = commit(repo, f"selftest {name}")
    try:
        check(revision)
    except counter.InputError:
        assertions["count"] += 1
        return
    raise SelftestFailure(f"{name} was accepted instead of failing closed")


def edit_receipt(repo: Path, target_id: str, change: Any) -> None:
    path = repo / f"{counter.RECEIPTS}/{target_id}.json"
    receipt = json.loads(path.read_text(encoding="utf-8"))
    change(receipt)
    put_json(repo, f"{counter.RECEIPTS}/{target_id}.json", receipt)


def edit_sidecar(repo: Path, change: Any) -> None:
    path = repo / counter.SIDECAR
    value = json.loads(path.read_text(encoding="utf-8"))
    change(value["entries"])
    put_json(repo, counter.SIDECAR, value)


def remove_note_from_block(repo: Path, path: str, note: str) -> None:
    file = repo / path
    data = file.read_text(encoding="utf-8")
    if note not in data:
        raise SelftestFailure(f"fixture correction note not found in {path}")
    file.write_text(data.replace(note, "[removed test note]", 1), encoding="utf-8")


def frozen_population() -> tuple[bytes, list[dict[str, Any]]]:
    candidates = (SOURCE_ROOT / counter.POPULATION, FROZEN_POPULATION_SOURCE)
    for candidate in candidates:
        try:
            raw = candidate.read_bytes()
        except OSError:
            continue
        if hashlib.sha256(raw).hexdigest() != counter.POPULATION_SHA256:
            raise SelftestFailure(f"frozen population digest mismatch at {candidate}")
        try:
            value = json.loads(raw)
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise SelftestFailure(f"frozen population JSON is invalid: {exc}") from exc
        targets = value.get("targets") if isinstance(value, dict) else None
        if not isinstance(targets, list) or len(targets) != 19:
            raise SelftestFailure("frozen population does not contain 19 targets")
        return raw, targets
    raise SelftestFailure("cannot locate the frozen round-24 C1 population")


def main() -> int:
    original_home = os.environ.get("HOME")
    try:
        population_raw, targets = frozen_population()
        with tempfile.TemporaryDirectory(prefix="kake-r24-c1-selftest-") as temporary:
            root = Path(temporary)
            repo = root / "repo"
            home = root / "home"
            home.mkdir()
            env = os.environ.copy()
            env["HOME"] = str(home)
            run(["git", "clone", "--quiet", "--no-hardlinks", "--no-checkout", str(SOURCE_ROOT), str(repo)], env=env)
            run(["git", "-C", str(repo), "checkout", "--quiet", "--detach", counter.BASE], env=env)
            os.environ["HOME"] = str(home)
            population_path = repo / counter.POPULATION
            population_path.parent.mkdir(parents=True, exist_ok=True)
            population_path.write_bytes(population_raw)
            isolated_home(home, targets)
            assertions = {"count": 0}

            base_result = counter.measure(str(repo), counter.BASE)
            if base_result["accepted"] != 0 or base_result["total"] != 19 or base_result["sweepExit"] != 1 or base_result["exitCode"] != 1:
                raise SelftestFailure(f"base counter control was not 0/19 with sweep exit 1: {base_result}")
            assertions["count"] += 1

            touched = create_fixture(repo, targets, population_raw)
            valid_revision = commit(repo, "selftest fixture: sidecar-backed C1 reconciliation")
            snapshot = {path: (repo / path).read_bytes() for path in touched}
            rows = all_target_checks(repo, valid_revision, targets)
            failed_rows = [row for row in rows if not row["pass"]]
            if failed_rows:
                raise SelftestFailure(f"valid sidecar fixture did not pass: {failed_rows}")
            assertions["count"] += len(rows)

            t01 = next(item for item in targets if item["id"] == "T01")
            t03 = next(item for item in targets if item["id"] == "T03")
            t04 = next(item for item in targets if item["id"] == "T04")
            t12 = next(item for item in targets if item["id"] == "T12")
            t16 = next(item for item in targets if item["id"] == "T16")
            t17 = next(item for item in targets if item["id"] == "T17")

            receipt_path = f"{counter.RECEIPTS}/T01.json"
            fail_case(repo, home, snapshot, targets, "T01", "missing receipt",
                      lambda: (repo / receipt_path).unlink(), "receipt missing", assertions)
            fail_case(repo, home, snapshot, targets, "T01", "invalid receipt JSON",
                      lambda: (repo / receipt_path).write_text("{", encoding="utf-8"),
                      "receipt is not valid JSON", assertions)
            for bad_value, label in (([], "array receipt"), (None, "null receipt")):
                fail_case(repo, home, snapshot, targets, "T01", label,
                          lambda bad_value=bad_value: put_json(repo, receipt_path, bad_value),
                          "receipt is not an object", assertions)

            fail_case(repo, home, snapshot, targets, "T01", "receipt id mismatch",
                      lambda: edit_receipt(repo, "T01", lambda receipt: receipt.update(id="T99")),
                      "receipt id mismatch", assertions)
            fail_case(repo, home, snapshot, targets, "T01", "receipt token mismatch",
                      lambda: edit_receipt(repo, "T01", lambda receipt: receipt.update(token="~/not-the-target")),
                      "receipt token mismatch", assertions)
            fail_case(repo, home, snapshot, targets, "T01", "receipt class mismatch",
                      lambda: edit_receipt(repo, "T01", lambda receipt: receipt.update(**{"class": "newMissing"})),
                      "receipt class mismatch", assertions)
            fail_case(repo, home, snapshot, targets, "T01", "malformed RFC3339 timestamp",
                      lambda: edit_receipt(repo, "T01", lambda receipt: receipt.update(observedAt="2026-10-21 noon")),
                      "strict RFC 3339", assertions)
            fail_case(repo, home, snapshot, targets, "T01", "invalid calendar date",
                      lambda: edit_receipt(repo, "T01", lambda receipt: receipt.update(observedAt="2026-02-30T00:00:00Z")),
                      "strict RFC 3339", assertions)
            fail_case(repo, home, snapshot, targets, "T01", "timestamp before bound",
                      lambda: edit_receipt(repo, "T01", lambda receipt: receipt.update(observedAt="2026-10-20T23:59:59Z")),
                      "before 2026-10-21", assertions)
            fail_case(repo, home, snapshot, targets, "T01", "timestamp after commit",
                      lambda: edit_receipt(repo, "T01", lambda receipt: receipt.update(observedAt="2026-10-21T12:00:00.000000001Z")),
                      "after revision committer time", assertions)
            fail_case(repo, home, snapshot, targets, "T01", "wrong state",
                      lambda: edit_receipt(repo, "T01", lambda receipt: receipt.update(state="present")),
                      "receipt state must be absent", assertions)
            fail_case(repo, home, snapshot, targets, "T16", "wrong recovered state",
                      lambda: edit_receipt(repo, "T16", lambda receipt: receipt.update(state="absent")),
                      "receipt state must be present", assertions)

            fail_case(repo, home, snapshot, targets, "T01", "empty observation commands",
                      lambda: edit_receipt(repo, "T01", lambda receipt: receipt["observation"].update(commands=[])),
                      "observation.commands", assertions)
            fail_case(repo, home, snapshot, targets, "T01", "empty observation output",
                      lambda: edit_receipt(repo, "T01", lambda receipt: receipt["observation"].update(output="")),
                      "observation.output", assertions)

            def create_absent_target() -> None:
                path = home / t12["token"][2:]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("present\n", encoding="utf-8")

            fail_case(repo, home, snapshot, targets, "T12", "unexpected live presence",
                      create_absent_target, "live filesystem is present", assertions)

            def remove_recovered_target() -> None:
                (home / t17["token"][2:]).unlink()

            fail_case(repo, home, snapshot, targets, "T17", "missing recovered path",
                      remove_recovered_target, "live filesystem is absent", assertions)

            fail_case(repo, home, snapshot, targets, "T01", "sweep drift membership", lambda: None,
                      "paths.drift", assertions, ({t01["token"]}, set(), set()))
            fail_case(repo, home, snapshot, targets, "T04", "sweep newMissing membership", lambda: None,
                      "paths.setDelta.newMissing", assertions, (set(), {t04["token"]}, set()))
            fail_case(repo, home, snapshot, targets, "T16", "sweep recovered membership", lambda: None,
                      "paths.setDelta.recovered", assertions, (set(), set(), {t16["token"]}))

            def remove_entry(target: dict[str, Any], kind: str) -> Any:
                cite = target["unannotatedCites"][0] if kind == "absent" else target["cites"][0]
                path, line = counter.parse_cite(cite)
                return lambda entries: entries.__setitem__(slice(None), [
                    entry for entry in entries
                    if not (entry["file"] == path and entry["line"] == line
                            and entry["token"] == target["token"] and entry["kind"] == kind)
                ])

            fail_case(repo, home, snapshot, targets, "T01", "missing lane-author absence sidecar",
                      lambda: edit_sidecar(repo, remove_entry(t01, "absent")),
                      "unannotated cite lacks a valid sidecar correction", assertions)
            fail_case(repo, home, snapshot, targets, "T03", "missing non-author absence sidecar",
                      lambda: edit_sidecar(repo, remove_entry(t03, "absent")),
                      "unannotated cite lacks a valid sidecar correction", assertions)

            def stale_t01_hash(entries: list[dict[str, Any]]) -> None:
                for entry in entries:
                    if entry["token"] == t01["token"] and entry["kind"] == "absent":
                        entry["lineSha256"] = "0" * 64
                        return
                raise SelftestFailure("T01 absence entry missing in fixture")

            fail_case(repo, home, snapshot, targets, "T01", "stale line hash",
                      lambda: edit_sidecar(repo, stale_t01_hash),
                      "unannotated cite lacks a valid sidecar correction", assertions)

            def wrong_t01_token(entries: list[dict[str, Any]]) -> None:
                for entry in entries:
                    if entry["token"] == t01["token"] and entry["kind"] == "absent":
                        entry["token"] = "~/different-target"
                        return
                raise SelftestFailure("T01 absence entry missing in fixture")

            fail_case(repo, home, snapshot, targets, "T01", "wrong sidecar token",
                      lambda: edit_sidecar(repo, wrong_t01_token),
                      "unannotated cite lacks a valid sidecar correction", assertions)

            t01_cite_path, _ = counter.parse_cite(t01["unannotatedCites"][0])
            t01_entry = next(entry for entry in json.loads(snapshot[counter.SIDECAR].decode("utf-8"))["entries"]
                             if entry["token"] == t01["token"] and entry["kind"] == "absent")
            fail_case(repo, home, snapshot, targets, "T01", "lane EOF note missing",
                      lambda: remove_note_from_block(repo, t01_cite_path, t01_entry["note"]),
                      "unannotated cite lacks a valid sidecar correction", assertions)

            t03_entry = next(entry for entry in json.loads(snapshot[counter.SIDECAR].decode("utf-8"))["entries"]
                             if entry["token"] == t03["token"] and entry["kind"] == "absent")
            fail_case(repo, home, snapshot, targets, "T03", "central lesson note missing",
                      lambda: remove_note_from_block(repo, counter.CENTRAL_LESSON, t03_entry["note"]),
                      "unannotated cite lacks a valid sidecar correction", assertions)

            fail_case(repo, home, snapshot, targets, "T16", "missing lane-author restoration entry",
                      lambda: edit_sidecar(repo, remove_entry(t16, "restored")),
                      "recovered cite lacks a valid sidecar correction", assertions)
            fail_case(repo, home, snapshot, targets, "T17", "missing non-author restoration entry",
                      lambda: edit_sidecar(repo, remove_entry(t17, "restored")),
                      "recovered cite lacks a valid sidecar correction", assertions)

            def bad_absent_note(entries: list[dict[str, Any]]) -> None:
                for entry in entries:
                    if entry["token"] == t01["token"] and entry["kind"] == "absent":
                        entry["note"] = "2026-10-21: historical record, not an executable instruction"
                        return
                raise SelftestFailure("T01 absence entry missing in fixture")

            input_case(repo, home, snapshot, targets, "absence sidecar note missing absence word",
                       lambda: edit_sidecar(repo, bad_absent_note),
                       lambda revision: counter.load_sidecar(str(repo), revision), assertions)

            def bad_restored_note(entries: list[dict[str, Any]]) -> None:
                for entry in entries:
                    if entry["token"] == t16["token"] and entry["kind"] == "restored":
                        entry["note"] = "As of 2026-10-21, the target is present but not missing; the earlier statement is historical."
                        return
                raise SelftestFailure("T16 restoration entry missing in fixture")

            input_case(repo, home, snapshot, targets, "restoration note contains absence vocabulary",
                       lambda: edit_sidecar(repo, bad_restored_note),
                       lambda revision: counter.load_sidecar(str(repo), revision), assertions)

            input_case(repo, home, snapshot, targets, "malformed sidecar JSON",
                       lambda: (repo / counter.SIDECAR).write_text("{", encoding="utf-8"),
                       lambda revision: counter.load_sidecar(str(repo), revision), assertions)

            try:
                counter.measure(str(repo), "-not-a-revision")
            except counter.InputError:
                assertions["count"] += 1
            else:
                raise SelftestFailure("leading-hyphen revision was accepted")

            write_snapshot(repo, snapshot)
            isolated_home(home, targets)
            population_path = repo / counter.POPULATION
            population_path.write_bytes(population_path.read_bytes() + b" ")
            bad_population_revision = commit(repo, "selftest population digest rejection")
            try:
                counter.measure(str(repo), bad_population_revision)
            except counter.InputError as exc:
                if "digest mismatch" not in str(exc):
                    raise SelftestFailure(f"wrong population failure: {exc}") from exc
                assertions["count"] += 1
            else:
                raise SelftestFailure("population digest mismatch was accepted")

            print(f"c1_selftest: PASS ({assertions['count']} assertions; 19 target passes and all C1 failure clauses exercised)")
            return 0
    except (SelftestFailure, counter.InputError, OSError, ValueError, KeyError, StopIteration) as exc:
        print(f"c1_selftest: FAIL: {exc}", file=sys.stderr)
        return 1
    finally:
        if original_home is None:
            os.environ.pop("HOME", None)
        else:
            os.environ["HOME"] = original_home


if __name__ == "__main__":
    raise SystemExit(main())
