#!/usr/bin/env python3
"""Replay frozen malformed-receipt cases against a runner at one Git revision.

Usage: measure_c2.py --root LANE --revision REV [--json]
The population is .ufo/waves/round-24/c2-population.json at REV. Each case is
applied to an isolated clone reset to fixtureBase, committed with a fixed
identity/date, and checked against the runner selected from REV.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
from typing import Any

POPULATION_PATH = ".ufo/waves/round-24/c2-population.json"
POPULATION_SHA256 = "16da1936f30e2e7bfa405d9b51dfc18ab686edbd9f1d36f65d76626b0cab7b8f"
R23_RUNNERS = {
    "c1": ".ufo/waves/round-23/measure_c1.py",
    "c2": ".ufo/waves/round-23/measure_c2.py",
}
FIXED_DATE = "2026-10-21T12:00:00Z"
COMMIT_NAME = "Kake round-24 receipt replay"
COMMIT_EMAIL = "kake-r24-receipt-replay@example.invalid"
RUNNER_TIMEOUT = 120


class InputError(Exception):
    """An unreadable or structurally invalid counter input."""


def clean_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
    return env


def git(root: str, *args: str, timeout: int = 30) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            ["git", "-c", "core.hooksPath=/dev/null", "-C", root, *args],
            env=clean_env(), capture_output=True, check=False, timeout=timeout
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise InputError(f"git {args[0] if args else 'command'} failed: {type(exc).__name__}: {exc}") from exc


def resolve_commit(root: str, revision: str) -> str:
    # Resolve arbitrary user input once, then use only the canonical object id in
    # all rev:path expressions so option-shaped revisions cannot reach git show.
    done = git(root, "rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}")
    if done.returncode != 0:
        raise InputError(f"revision does not resolve to a commit: {revision}")
    return done.stdout.decode("ascii", errors="replace").strip()


def show(root: str, revision: str, path: str) -> bytes | None:
    done = git(root, "show", "--no-ext-diff", "--no-textconv", f"{revision}:{path}")
    return done.stdout if done.returncode == 0 else None


def validate_population(raw: bytes) -> tuple[str, list[dict[str, Any]]]:
    try:
        population = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InputError(f"population is not UTF-8 JSON: {exc}") from exc
    if not isinstance(population, dict):
        raise InputError("population must be a JSON object")
    fixture_base = population.get("fixtureBase")
    cases = population.get("cases")
    if not isinstance(fixture_base, str) or not fixture_base:
        raise InputError("population fixtureBase must be a non-empty string")
    if not isinstance(cases, list) or not cases:
        raise InputError("population cases must be a non-empty array")
    seen: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise InputError(f"case {index} must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip() or case_id in seen:
            raise InputError(f"case {index} has a missing or duplicate id")
        seen.add(case_id)
        if case.get("target") not in {"c1", "c2"}:
            raise InputError(f"case {case_id}: target must be c1 or c2")
        relative = case.get("file")
        if not isinstance(relative, str) or not relative or ":" in relative:
            raise InputError(f"case {case_id}: file must be a repository-relative path")
        path = PurePosixPath(relative)
        if path.is_absolute() or ".." in path.parts or not path.parts:
            raise InputError(f"case {case_id}: file escapes the repository")
        operation = case.get("op")
        if operation not in {"set", "delete", "raw", "replace"}:
            raise InputError(f"case {case_id}: unsupported op")
        if operation in {"set", "delete"}:
            json_path = case.get("jsonPath")
            if (not isinstance(json_path, list) or any(not isinstance(part, str) for part in json_path)
                    or (operation == "delete" and not json_path)):
                raise InputError(f"case {case_id}: jsonPath must be a string array (delete requires a member)")
            if operation == "set" and "value" not in case:
                raise InputError(f"case {case_id}: set requires value")
        elif operation == "raw":
            if not isinstance(case.get("value"), str):
                raise InputError(f"case {case_id}: raw requires UTF-8 file text in value")
        else:
            replacement = case.get("replace")
            if (not isinstance(replacement, dict) or not isinstance(replacement.get("old"), str)
                    or not isinstance(replacement.get("new"), str)):
                raise InputError(f"case {case_id}: replace requires string old and new values")
        if case.get("expect") not in {"reject", "accept"}:
            raise InputError(f"case {case_id}: expect must be reject or accept")
        if not isinstance(case.get("why"), str) or not case["why"].strip():
            raise InputError(f"case {case_id}: why must be non-empty text")
        observed = case.get("r23Observed")
        if (not isinstance(observed, dict) or type(observed.get("exit")) is not int
                or type(observed.get("traceback")) is not bool
                or not isinstance(observed.get("stdoutTail"), str)):
            raise InputError(f"case {case_id}: malformed r23Observed record")
    return fixture_base, cases


def list_index(part: str, case_id: str) -> int:
    if not re.fullmatch(r"0|[1-9][0-9]*", part):
        raise InputError(f"case {case_id}: list index is not a non-negative integer")
    return int(part)


def mutate_json(document: Any, case: dict[str, Any]) -> Any:
    if not case["jsonPath"]:
        return case["value"]
    parent = document
    case_id = case["id"]
    for part in case["jsonPath"][:-1]:
        if isinstance(parent, dict) and part in parent:
            parent = parent[part]
        elif isinstance(parent, list):
            index = list_index(part, case_id)
            if index >= len(parent):
                raise InputError(f"case {case_id}: jsonPath list index is out of range")
            parent = parent[index]
        else:
            raise InputError(f"case {case_id}: jsonPath parent does not exist")
    final = case["jsonPath"][-1]
    if isinstance(parent, dict):
        if case["op"] == "set":
            parent[final] = case["value"]
        elif final in parent:
            del parent[final]
        else:
            raise InputError(f"case {case_id}: delete path does not exist")
    elif isinstance(parent, list):
        index = list_index(final, case_id)
        if index >= len(parent):
            raise InputError(f"case {case_id}: jsonPath list index is out of range")
        if case["op"] == "set":
            parent[index] = case["value"]
        else:
            del parent[index]
    else:
        raise InputError(f"case {case_id}: jsonPath parent is not an object or array")
    return document


def indent_from(text: str) -> str | int | None:
    match = re.search(r"\n([ \t]+)\S", text)
    if match is None:
        return None
    unit = match.group(1)
    return unit if set(unit) == {"\t"} else len(unit)


def text_value(value: bytes | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def tail(text: str) -> str:
    lines = text.splitlines()
    return lines[-1] if lines else ""


def run_command(command: list[str], *, cwd: str, env: dict[str, str] | None = None,
                timeout: int = RUNNER_TIMEOUT) -> tuple[int, str, str]:
    try:
        done = subprocess.run(command, cwd=cwd, env=clean_env() if env is None else env, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout, check=False)
        return done.returncode, done.stdout, done.stderr
    except subprocess.TimeoutExpired as exc:
        return 124, text_value(exc.stdout), text_value(exc.stderr) + f"\nrunner timed out after {timeout}s"
    except OSError as exc:
        return 127, "", f"{type(exc).__name__}: {exc}"


def mutation_path(sandbox: Path, relative: str, case_id: str) -> Path:
    path = sandbox.joinpath(*PurePosixPath(relative).parts)
    if path.is_symlink():
        raise InputError(f"case {case_id}: fixture path must not be a symlink")
    try:
        resolved = path.parent.resolve(strict=True) / path.name
    except OSError as exc:
        raise InputError(f"case {case_id}: fixture file is unreadable: {relative}: {exc}") from exc
    if os.path.commonpath((str(sandbox.resolve()), str(resolved))) != str(sandbox.resolve()):
        raise InputError(f"case {case_id}: fixture file resolves outside the sandbox")
    if resolved.exists() and not resolved.is_file():
        raise InputError(f"case {case_id}: fixture path is not a file: {relative}")
    return resolved


def prepare_runner(root: str, revision: str, target: str, runner_dir: Path) -> tuple[Path, bool]:
    replay = show(root, revision, "scripts/receipt_replay.py")
    if replay is not None:
        runner_path = runner_dir / "receipt_replay.py"
        runner_path.write_bytes(replay)
        return runner_path, True
    relative = R23_RUNNERS[target]
    runner = show(root, revision, relative)
    if runner is None:
        raise InputError(f"runner unreadable at revision {revision}: {relative}")
    runner_path = runner_dir / f"measure_{target}.py"
    runner_path.write_bytes(runner)
    return runner_path, False


def run_case(root: str, sandbox: Path, revision: str, fixture_base: str,
             case: dict[str, Any], runner_cache: dict[str, tuple[Path, bool]]) -> dict[str, Any]:
    reset = git(str(sandbox), "reset", "--hard", fixture_base)
    if reset.returncode != 0:
        raise InputError(f"case {case['id']}: reset to fixtureBase failed")
    relative = case["file"]
    path = mutation_path(sandbox, relative, case["id"])
    try:
        original_bytes = path.read_bytes() if path.exists() else b""
        if case["op"] == "raw":
            encoded = case["value"].encode("utf-8")
        else:
            original = original_bytes.decode("utf-8")
            if case["op"] == "replace":
                replacement = case["replace"]
                old = replacement["old"]
                if original.count(old) != 1:
                    raise InputError(f"case {case['id']}: replace old text must occur exactly once")
                encoded = original.replace(old, replacement["new"], 1).encode("utf-8")
            else:
                document = json.loads(original)
                changed = mutate_json(document, case)
                encoded = (json.dumps(changed, indent=indent_from(original)) + "\n").encode("utf-8")
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise InputError(f"case {case['id']}: fixture mutation failed: {exc}") from exc
    try:
        path.write_bytes(encoded)
    except OSError as exc:
        raise InputError(f"case {case['id']}: cannot write fixture mutation: {exc}") from exc
    add = git(str(sandbox), "add", "--", relative)
    if add.returncode != 0:
        raise InputError(f"case {case['id']}: git add failed")
    env = clean_env()
    env.update({
        "GIT_AUTHOR_NAME": COMMIT_NAME,
        "GIT_AUTHOR_EMAIL": COMMIT_EMAIL,
        "GIT_COMMITTER_NAME": COMMIT_NAME,
        "GIT_COMMITTER_EMAIL": COMMIT_EMAIL,
        "GIT_AUTHOR_DATE": FIXED_DATE,
        "GIT_COMMITTER_DATE": FIXED_DATE,
    })
    commit = run_command(
        ["git", "-c", "core.hooksPath=/dev/null", "-C", str(sandbox), "-c", "commit.gpgsign=false", "commit", "--allow-empty",
         "-m", f"r24 receipt case {case['id']}"],
        cwd=str(sandbox), env=env, timeout=30,
    )
    if commit[0] != 0:
        raise InputError(f"case {case['id']}: commit failed: {tail(commit[2]) or tail(commit[1])}")
    head = git(str(sandbox), "rev-parse", "--verify", "HEAD^{commit}")
    if head.returncode != 0:
        raise InputError(f"case {case['id']}: sandbox HEAD unreadable")
    head_revision = head.stdout.decode("ascii", errors="replace").strip()
    target = case["target"]
    if target not in runner_cache:
        runner_cache[target] = prepare_runner(root, revision, target, sandbox.parent / "runners")
    runner_path, replay = runner_cache[target]
    if replay:
        command = [sys.executable, str(runner_path), target, "--root", str(sandbox), "--revision", head_revision]
    else:
        command = [sys.executable, str(runner_path), "--root", str(sandbox), "--revision", head_revision]
    exit_code, stdout, stderr = run_command(command, cwd=str(sandbox))
    traceback = "Traceback" in stderr
    correct = ((exit_code in {1, 2} and not traceback) if case["expect"] == "reject"
               else exit_code == 0)
    return {
        "id": case["id"],
        "target": target,
        "expect": case["expect"],
        "exit": exit_code,
        "traceback": traceback,
        "stdoutTail": tail(stdout),
        "stderrTail": tail(stderr),
        "correct": correct,
        "revision": head_revision,
    }


def summary_for(results: list[dict[str, Any]]) -> tuple[dict[str, int], str]:
    reject = [row for row in results if row["expect"] == "reject"]
    accept = [row for row in results if row["expect"] == "accept"]
    correct = sum(bool(row["correct"]) for row in results)
    summary = {
        "correct": correct,
        "total": len(results),
        "rejectCorrect": sum(bool(row["correct"]) for row in reject),
        "rejectTotal": len(reject),
        "acceptCorrect": sum(bool(row["correct"]) for row in accept),
        "acceptTotal": len(accept),
    }
    text = (f"correct {correct}/{len(results)} (reject {summary['rejectCorrect']}/{len(reject)}, "
            f"accept {summary['acceptCorrect']}/{len(accept)})")
    return summary, text


def run_population(root: str, revision: str) -> dict[str, Any]:
    try:
        root_path = Path(root).resolve(strict=True)
    except OSError as exc:
        raise InputError(f"root is unreadable: {exc}") from exc
    if not root_path.is_dir():
        raise InputError("root must be a directory")
    root = str(root_path)
    resolved_revision = resolve_commit(root, revision)
    raw = show(root, resolved_revision, POPULATION_PATH)
    if raw is None:
        raise InputError(f"population unreadable at revision: {POPULATION_PATH}")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != POPULATION_SHA256:
        raise InputError(f"population digest mismatch: {digest}")
    fixture_base, cases = validate_population(raw)
    fixture_revision = resolve_commit(root, fixture_base)
    with tempfile.TemporaryDirectory(prefix="kake-r24-c2-") as temporary:
        temp = Path(temporary)
        sandbox = temp / "sb"
        clone = run_command(["git", "clone", "--quiet", "--no-hardlinks", root, str(sandbox)],
                            cwd=str(temp), timeout=300)
        if clone[0] != 0:
            raise InputError(f"sandbox clone failed: {tail(clone[2]) or tail(clone[1])}")
        checkout = git(str(sandbox), "checkout", "--quiet", "--detach", fixture_revision)
        if checkout.returncode != 0:
            raise InputError("sandbox could not check out fixtureBase")
        runner_dir = temp / "runners"
        runner_dir.mkdir()
        runner_cache: dict[str, tuple[Path, bool]] = {}
        results = [run_case(root, sandbox, resolved_revision, fixture_revision, case, runner_cache)
                   for case in cases]
    summary, summary_text = summary_for(results)
    return {
        "revision": resolved_revision,
        "fixtureBase": fixture_revision,
        "populationSha256": digest,
        "runnerMode": "scripts/receipt_replay.py when present at revision; otherwise round-23 runner",
        "cases": results,
        "summary": summary,
        "summaryText": summary_text,
    }


def emit_error(message: str, json_output: bool) -> None:
    if json_output:
        print(json.dumps({"error": message}, sort_keys=True))
    else:
        print(f"error: {message}", file=sys.stderr)


def selftest() -> int:
    checks = [
        ("root replacement", mutate_json({"old": 1}, {"jsonPath": [], "value": []}) == []),
        ("array member", mutate_json({"a": [1]}, {
            "id": "array", "op": "set", "jsonPath": ["a", "0"], "value": 2,
        }) == {"a": [2]}),
        ("member deletion", mutate_json({"a": 1}, {
            "id": "delete", "op": "delete", "jsonPath": ["a"],
        }) == {}),
    ]
    summary, _ = summary_for([
        {"expect": "reject", "correct": True}, {"expect": "accept", "correct": False},
    ])
    checks.append(("derived totals", summary == {
        "correct": 1, "total": 2, "rejectCorrect": 1, "rejectTotal": 1,
        "acceptCorrect": 0, "acceptTotal": 1,
    }))
    case = {"id": "fixture", "target": "c1", "file": "receipt.json", "op": "set",
            "jsonPath": ["a"], "value": 1, "expect": "reject", "why": "fixture",
            "r23Observed": {"exit": 1, "traceback": False, "stdoutTail": ""}}
    for name, changes in [
        ("traversal rejected", {"file": "../receipt.json"}),
        ("unknown op rejected", {"op": "other"}),
        ("boolean exit rejected", {"r23Observed": {"exit": True, "traceback": False, "stdoutTail": ""}}),
    ]:
        try:
            validate_population(json.dumps({"fixtureBase": "fixture", "cases": [{**case, **changes}]}).encode())
            rejected = False
        except InputError:
            rejected = True
        checks.append((name, rejected))
    for name, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    print(f"selftest {sum(p for _, p in checks)}/{len(checks)}")
    return 0 if all(p for _, p in checks) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root")
    parser.add_argument("--revision")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.root or not args.revision:
        parser.error("--root and --revision are required unless --selftest")
    try:
        result = run_population(args.root, args.revision)
    except Exception as exc:
        emit_error(f"{type(exc).__name__}: {exc}", args.json)
        return 2
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for row in result["cases"]:
            print(f"{row['id']}: expected {row['expect']}, exit={row['exit']}, "
                  f"traceback={str(row['traceback']).lower()}, correct={str(row['correct']).lower()}")
        print(result["summaryText"])
    return 0 if result["summary"]["correct"] == result["summary"]["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
