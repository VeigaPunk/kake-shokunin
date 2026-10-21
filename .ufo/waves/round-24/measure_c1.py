#!/usr/bin/env python3
"""Measure round-24 C1 reconciliation against a committed tree and live paths.

Usage: python3 .ufo/waves/round-24/measure_c1.py --root LANE --revision REV [--json]
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

BASE = "f7de3ab4e9f030a15a857a5a08631bd8e690f436"
POPULATION = ".ufo/waves/round-24/c1-population.json"
POPULATION_SHA256 = "8de0244b30444f997b0b8a450609fe90762ded2d0555b685202861696b017376"
BASE_POPULATION_SOURCE = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-24/c1-population.json"
RECEIPTS = ".ufo/waves/round-24/c1-receipts"
SIDECAR = "corpus/knowledge/freshness-sidecar.json"
SIDECAR_SCHEMA = "kake-paths-sidecar-v1"
CENTRAL_LESSON = "corpus/lessons/round-24.md"
ABSENCE_RE = re.compile(r"absent|gone|vanished|emptied|no longer|dangling|no such file|never published|missing", re.IGNORECASE)
RFC3339_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})[Tt](\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?(Z|z|[+-]\d{2}:\d{2})$"
    , re.ASCII)


class InputError(Exception):
    """A required commit, population, archive, or sweep input is unreadable."""


def git(root: str, *args: str) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(["git", "-C", root, *args], capture_output=True, check=False)
    except OSError as exc:
        raise InputError(f"cannot run git: {exc}") from exc


def read_blob(root: str, revision: str, path: str) -> bytes | None:
    result = git(root, "show", f"{revision}:{path}")
    return result.stdout if result.returncode == 0 else None


def required_blob(root: str, revision: str, path: str) -> bytes:
    data = read_blob(root, revision, path)
    if data is None:
        raise InputError(f"missing {path} at {revision}")
    return data


def validate_revision(root: str, revision: str) -> str:
    if not revision or revision.startswith("-"):
        raise InputError("revision must be non-empty and must not start with '-'")
    result = git(root, "rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}")
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise InputError(f"revision is not a commit: {detail or revision}")
    return result.stdout.decode("ascii", "strict").strip()


def committer_time(root: str, revision: str) -> int:
    result = git(root, "show", "-s", "--format=%ct", revision)
    if result.returncode != 0:
        raise InputError("cannot read revision committer time")
    try:
        return int(result.stdout.decode("ascii", "strict").strip())
    except (UnicodeError, ValueError) as exc:
        raise InputError("revision committer time is malformed") from exc


def parse_rfc3339(value: Any) -> tuple[int, str] | None:
    """Return UTC whole seconds and normalized fractional digits, or None.

    The exact fractional spelling is retained so a timestamp at the commit's
    integer second cannot be rounded down into the permitted range.
    """
    if not isinstance(value, str):
        return None
    match = RFC3339_RE.fullmatch(value)
    if match is None:
        return None
    year, month, day, hour, minute, second = (int(match.group(i)) for i in range(1, 7))
    fraction = (match.group(7) or "").rstrip("0")
    zone = match.group(8)
    if second == 60:
        # The accepted interval starts in 2026; no RFC 3339 leap second has
        # occurred in this interval, so a leap-second spelling is not valid here.
        return None
    if second > 59:
        return None
    if zone in ("Z", "z"):
        offset_minutes = 0
    else:
        sign = 1 if zone[0] == "+" else -1
        offset_hour = int(zone[1:3])
        offset_minute = int(zone[4:6])
        if offset_hour > 23 or offset_minute > 59:
            return None
        offset_minutes = sign * (offset_hour * 60 + offset_minute)
    try:
        local = dt.datetime(year, month, day, hour, minute, second,
                            tzinfo=dt.timezone(dt.timedelta(minutes=offset_minutes)))
        utc = local.astimezone(dt.timezone.utc)
    except (OverflowError, ValueError):
        return None
    epoch = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    delta = utc - epoch
    whole_seconds = delta.days * 86400 + delta.seconds
    return whole_seconds, fraction


def before_lower_bound(timestamp: tuple[int, str]) -> bool:
    lower = dt.datetime(2026, 10, 21, tzinfo=dt.timezone.utc)
    epoch = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    delta = lower - epoch
    lower_seconds = delta.days * 86400 + delta.seconds
    return timestamp[0] < lower_seconds


def after_commit(timestamp: tuple[int, str], commit_time: int) -> bool:
    return timestamp[0] > commit_time or (timestamp[0] == commit_time and bool(timestamp[1]))


def parse_cite(cite: Any) -> tuple[str, int]:
    if not isinstance(cite, str) or ":" not in cite:
        raise InputError(f"population cite is malformed: {cite!r}")
    path, raw_line = cite.rsplit(":", 1)
    if not path or path.startswith("/") or ".." in Path(path).parts:
        raise InputError(f"population cite path is malformed: {cite!r}")
    try:
        line = int(raw_line)
    except ValueError as exc:
        raise InputError(f"population cite line is malformed: {cite!r}") from exc
    if line < 1:
        raise InputError(f"population cite line is malformed: {cite!r}")
    return path, line


def is_non_author(path: str) -> bool:
    if not path.startswith("corpus/lessons/"):
        return False
    name = Path(path).name
    return fnmatch.fnmatchcase(name, "*aggregator*.md") or fnmatch.fnmatchcase(name, "*verifier-spotcheck*.md")


def lines_at(root: str, revision: str, path: str, cache: dict[tuple[str, str], list[bytes]]) -> list[bytes] | None:
    key = (revision, path)
    if key not in cache:
        data = read_blob(root, revision, path)
        if data is None:
            cache[key] = []
            return None
        cache[key] = data.splitlines()
    lines = cache[key]
    return lines if lines else None


def line_at(root: str, revision: str, path: str, number: int,
            cache: dict[tuple[str, str], list[bytes]]) -> bytes:
    lines = lines_at(root, revision, path, cache)
    if lines is None or number > len(lines):
        raise InputError(f"missing base citation line {path}:{number} at {revision}")
    return lines[number - 1]


def load_sidecar(root: str, revision: str) -> list[dict[str, Any]]:
    raw = read_blob(root, revision, SIDECAR)
    if raw is None:
        return []
    try:
        value = json.loads(raw)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise InputError(f"sidecar JSON is unreadable: {exc}") from exc
    if not isinstance(value, dict) or value.get("schema") != SIDECAR_SCHEMA or not isinstance(value.get("entries"), list):
        raise InputError("sidecar schema or entries are invalid")
    entries: list[dict[str, Any]] = []
    identities: set[tuple[str, int, str]] = set()
    for index, entry in enumerate(value["entries"]):
        if not isinstance(entry, dict):
            raise InputError(f"sidecar entry {index} is not an object")
        file = entry.get("file")
        line = entry.get("line")
        token = entry.get("token")
        note = entry.get("note")
        kind = entry.get("kind")
        if (not isinstance(file, str) or not (file == "SKILL.md" or file.startswith("corpus/") and file.endswith(".md"))
                or any(part in ("", ".", "..") for part in Path(file).parts)
                or isinstance(line, bool) or not isinstance(line, int) or line < 1
                or not isinstance(token, str) or not token.startswith("~/")
                or not isinstance(entry.get("lineSha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", entry["lineSha256"])
                or kind not in ("absent", "restored")
                or entry.get("date") != "2026-10-21"
                or not isinstance(note, str) or not note.strip()
                or "2026-10-21" not in note):
            raise InputError(f"sidecar entry {index} has invalid fields")
        if kind == "absent":
            if (not ABSENCE_RE.search(note)
                    or "historical record, not an executable instruction" not in note):
                raise InputError(f"sidecar absent entry {index} has invalid note")
        elif (ABSENCE_RE.search(note) or not re.search(r"\bpresent\b", note, re.IGNORECASE)
              or not re.search(r"historical|unverified", note, re.IGNORECASE)):
            raise InputError(f"sidecar restored entry {index} has invalid note")
        identity = (file, line, token)
        if identity in identities:
            raise InputError(f"duplicate sidecar entry: {file}:{line}:{token}")
        identities.add(identity)
        entries.append(entry)
    return entries


def has_eof_correction_note(root: str, revision: str, path: str, note: str) -> bool:
    raw = read_blob(root, revision, path)
    if raw is None:
        return False
    try:
        lines = raw.decode("utf-8", "strict").splitlines()
    except UnicodeError as exc:
        raise InputError(f"correction file is not UTF-8: {path}") from exc
    headings = [index for index, line in enumerate(lines) if line == "## Round-24 path reconciliation"]
    if not headings:
        return False
    start = headings[-1]
    body = lines[start + 1:]
    if any(re.match(r"^#{1,2}(?:\s|$)", line) for line in body):
        return False
    return note in "\n".join(body)


def sidecar_covers(root: str, revision: str, entries: list[dict[str, Any]], path: str,
                   line: int, token: str, line_text: bytes, kind: str,
                   current_cache: dict[tuple[str, str], list[bytes]]) -> bool:
    expected_hash = hashlib.sha256(line_text).hexdigest()
    current_lines = lines_at(root, revision, path, current_cache)
    if current_lines is None or line > len(current_lines) or current_lines[line - 1] != line_text:
        return False
    try:
        canonical_line = line_text.decode("utf-8", "strict").replace("/home/vgpnk/", "~/")
    except UnicodeError as exc:
        raise InputError(f"citation file is not UTF-8: {path}") from exc
    if token not in canonical_line:
        return False
    correction_file = CENTRAL_LESSON if is_non_author(path) else path
    for entry in entries:
        if (entry["file"] != path or entry["line"] != line or entry["token"] != token
                or entry["lineSha256"] != expected_hash or entry["kind"] != kind):
            continue
        if has_eof_correction_note(root, revision, correction_file, entry["note"]):
            return True
    return False


def parse_population(root: str, revision: str) -> list[dict[str, Any]]:
    raw = read_blob(root, revision, POPULATION)
    if raw is None and revision == BASE:
        for source in (Path(root) / POPULATION, Path(BASE_POPULATION_SOURCE)):
            try:
                raw = source.read_bytes()
                break
            except OSError:
                continue
    if raw is None:
        raise InputError(f"missing {POPULATION} at {revision}")
    if hashlib.sha256(raw).hexdigest() != POPULATION_SHA256:
        raise InputError("round-24 C1 population digest mismatch")
    try:
        population = json.loads(raw)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise InputError(f"round-24 C1 population JSON is unreadable: {exc}") from exc
    targets = population.get("targets") if isinstance(population, dict) else None
    if not isinstance(targets, list) or len(targets) != 19:
        raise InputError("round-24 C1 population must contain exactly 19 targets")
    seen_ids: set[str] = set()
    for target in targets:
        if (not isinstance(target, dict) or not isinstance(target.get("id"), str)
                or not isinstance(target.get("token"), str) or not target["token"]
                or target.get("class") not in ("drift", "newMissing", "recovered")
                or not isinstance(target.get("cites"), list)):
            raise InputError("round-24 C1 population target is malformed")
        if target["id"] in seen_ids:
            raise InputError(f"duplicate target id: {target['id']}")
        seen_ids.add(target["id"])
        for cite in target["cites"]:
            parse_cite(cite)
        if target["class"] == "drift":
            unannotated = target.get("unannotatedCites")
            if not isinstance(unannotated, list):
                raise InputError(f"{target['id']} has no unannotatedCites list")
            for cite in unannotated:
                parse_cite(cite)
    return targets


def extract_archive(root: str, revision: str, destination: str) -> None:
    try:
        archive = subprocess.Popen(["git", "-C", root, "archive", revision],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError as exc:
        raise InputError(f"cannot run git archive: {exc}") from exc
    assert archive.stdout is not None
    try:
        tar = subprocess.Popen(["tar", "-x", "-C", destination], stdin=archive.stdout,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError as exc:
        archive.stdout.close()
        archive.kill()
        archive.communicate()
        raise InputError(f"cannot run tar: {exc}") from exc
    archive.stdout.close()
    _tar_out, tar_err = tar.communicate()
    _archive_out, archive_err = archive.communicate()
    if archive.returncode != 0 or tar.returncode != 0:
        detail = archive_err.decode("utf-8", "replace").strip() or tar_err.decode("utf-8", "replace").strip()
        raise InputError(f"cannot extract revision archive: {detail or 'git archive or tar failed'}")


def run_sweep(archive_root: str) -> tuple[int, set[str], set[str], set[str]]:
    environment = os.environ.copy()
    environment["KAKE_REPO_ROOT"] = archive_root
    environment.pop("KAKE_FRESHNESS_PINS", None)
    command = ["node", "scripts/freshness-sweep.mjs", "--section=paths", "--json"]
    try:
        with tempfile.TemporaryFile() as stdout_file, tempfile.TemporaryFile() as stderr_file:
            result = subprocess.run(command, cwd=archive_root, env=environment,
                                    stdout=stdout_file, stderr=stderr_file, check=False)
            stdout_file.seek(0)
            stdout = stdout_file.read()
            stderr_file.seek(0)
            stderr = stderr_file.read()
    except OSError as exc:
        raise InputError(f"cannot run node freshness sweep: {exc}") from exc
    try:
        report = json.loads(stdout)
    except (UnicodeError, json.JSONDecodeError) as exc:
        stderr_text = stderr.decode("utf-8", "replace").strip()
        stdout_text = stdout.decode("utf-8", "replace").strip()
        detail = f"{exc}; stderr={stderr_text[-500:]!r}; stdout={stdout_text[-500:]!r}"
        raise InputError(f"freshness sweep did not emit JSON: {detail}") from exc
    if not isinstance(report, dict):
        raise InputError("freshness sweep JSON is not an object")
    sections = report.get("sections")
    paths = sections.get("paths") if isinstance(sections, dict) else None
    if not isinstance(paths, dict) or not isinstance(paths.get("drift"), list):
        raise InputError("freshness sweep JSON has no paths.drift list")
    set_delta = paths.get("setDelta")
    if not isinstance(set_delta, dict):
        raise InputError("freshness sweep JSON has no paths.setDelta object")
    new_missing = set_delta.get("newMissing")
    recovered = set_delta.get("recovered")
    if not isinstance(new_missing, list) or not isinstance(recovered, list):
        raise InputError("freshness sweep JSON has no paths.setDelta.newMissing/recovered lists")
    drift_tokens: set[str] = set()
    for item in paths["drift"]:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise InputError("freshness sweep JSON has a malformed drift entry")
        drift_tokens.add(item["path"])
    if not all(isinstance(token, str) for token in new_missing + recovered):
        raise InputError("freshness sweep JSON has malformed setDelta tokens")
    return result.returncode, drift_tokens, set(new_missing), set(recovered)


def check_target(root: str, revision: str, target: dict[str, Any], commit_time: int,
                 sweep_tokens: tuple[set[str], set[str], set[str]], sidecar: list[dict[str, Any]],
                 base_lines: dict[tuple[str, int], bytes],
                 current_lines: dict[tuple[str, str], list[bytes]]) -> dict[str, Any]:
    target_id = target["id"]
    token = target["token"]
    target_class = target["class"]
    problems: list[str] = []
    receipt_path = f"{RECEIPTS}/{target_id}.json"
    raw = read_blob(root, revision, receipt_path)
    if raw is None:
        problems.append("receipt missing")
    else:
        try:
            receipt = json.loads(raw)
        except (UnicodeError, json.JSONDecodeError):
            problems.append("receipt is not valid JSON")
        else:
            if not isinstance(receipt, dict):
                problems.append("receipt is not an object")
            else:
                for field, expected in (("id", target_id), ("token", token), ("class", target_class)):
                    if receipt.get(field) != expected:
                        problems.append(f"receipt {field} mismatch")
                observed = parse_rfc3339(receipt.get("observedAt"))
                if observed is None:
                    problems.append("observedAt is not strict RFC 3339 date-time")
                else:
                    if before_lower_bound(observed):
                        problems.append("observedAt is before 2026-10-21T00:00:00Z")
                    if after_commit(observed, commit_time):
                        problems.append("observedAt is after revision committer time")
                expected_state = "present" if target_class == "recovered" else "absent"
                if receipt.get("state") != expected_state:
                    problems.append(f"receipt state must be {expected_state}")
                observation = receipt.get("observation")
                if not isinstance(observation, dict):
                    problems.append("observation is not an object")
                else:
                    commands = observation.get("commands")
                    if (not isinstance(commands, list) or not commands
                            or not all(isinstance(command, str) and command.strip() for command in commands)):
                        problems.append("observation.commands is empty or malformed")
                    output = observation.get("output")
                    if not isinstance(output, str) or not output.strip():
                        problems.append("observation.output is empty or malformed")

    expected_present = target_class == "recovered"
    observed_present = os.path.exists(os.path.expanduser(token))
    if observed_present != expected_present:
        state = "present" if observed_present else "absent"
        expected = "present" if expected_present else "absent"
        problems.append(f"live filesystem is {state}, expected {expected}")

    drift_tokens, new_missing, recovered = sweep_tokens
    if token in drift_tokens:
        problems.append("token appears in sweep paths.drift")
    if token in new_missing:
        problems.append("token appears in sweep paths.setDelta.newMissing")
    if token in recovered:
        problems.append("token appears in sweep paths.setDelta.recovered")

    def base_line(cite: str) -> tuple[str, int, bytes]:
        path, number = parse_cite(cite)
        key = (path, number)
        if key not in base_lines:
            base_lines[key] = line_at(root, BASE, path, number, {})
        return path, number, base_lines[key]

    if target_class == "drift":
        required_cites = target["unannotatedCites"]
        correction_kind = "absent"
        failure_label = "unannotated cite lacks a valid sidecar correction"
    elif target_class == "recovered":
        required_cites = target["cites"]
        correction_kind = "restored"
        failure_label = "recovered cite lacks a valid sidecar correction"
    else:
        required_cites = []
        correction_kind = ""
        failure_label = ""
    for cite in required_cites:
        path, number, text = base_line(cite)
        if not sidecar_covers(root, revision, sidecar, path, number, token, text,
                              correction_kind, current_lines):
            problems.append(f"{failure_label}: {cite}")

    return {"id": target_id, "token": token, "class": target_class,
            "pass": not problems, "problems": problems}


def measure(root: str, revision: str) -> dict[str, Any]:
    root = str(Path(root).resolve())
    resolved = validate_revision(root, revision)
    commit_time = committer_time(root, resolved)
    targets = parse_population(root, resolved)
    sidecar = load_sidecar(root, resolved)
    with tempfile.TemporaryDirectory(prefix="kake-c1-") as temporary:
        extract_archive(root, resolved, temporary)
        sweep_exit, drift_tokens, new_missing, recovered = run_sweep(temporary)
    sweep_tokens = (drift_tokens, new_missing, recovered)
    base_lines: dict[tuple[str, int], bytes] = {}
    current_lines: dict[tuple[str, str], list[bytes]] = {}
    rows = [check_target(root, resolved, target, commit_time, sweep_tokens, sidecar,
                         base_lines, current_lines) for target in targets]
    accepted = sum(1 for row in rows if row["pass"])
    exit_code = 0 if accepted == 19 and sweep_exit == 0 else (2 if sweep_exit not in (0, 1) else 1)
    return {"revision": resolved, "accepted": accepted, "total": 19,
            "sweepExit": sweep_exit, "targets": rows, "exitCode": exit_code}


def emit_text(result: dict[str, Any]) -> None:
    for row in result["targets"]:
        status = "PASS" if row["pass"] else "FAIL"
        detail = "" if row["pass"] else ": " + "; ".join(row["problems"])
        print(f"{row['id']} {status}{detail}")
    print(f"accepted {result['accepted']}/19 · sweep exit {result['sweepExit']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="lane git repository")
    parser.add_argument("--revision", required=True, help="commit to measure")
    parser.add_argument("--json", action="store_true", help="emit machine-readable results")
    args = parser.parse_args(argv)
    try:
        result = measure(args.root, args.revision)
    except (InputError, OSError, UnicodeError) as exc:
        if args.json:
            print(json.dumps({"error": str(exc), "exitCode": 2}, sort_keys=True))
        else:
            print(f"measure_c1: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        emit_text(result)
    return result["exitCode"]


if __name__ == "__main__":
    raise SystemExit(main())
