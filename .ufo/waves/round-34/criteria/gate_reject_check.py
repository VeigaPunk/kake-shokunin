#!/usr/bin/env python3
"""Check a committed lesson's Gate section for a reasoned source rejection."""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


class BadInput(Exception):
    """The repository, revision, lesson path, or lesson bytes cannot be read."""


SOURCE_ID = re.compile(r"\bS[0-9]{3,}\b")
GATE_HEADING = re.compile(r"^##[ \t]+Gate(?:[ \t]+#+)?[ \t]*$")
SECTION_HEADING = re.compile(r"^#{1,2}(?:[ \t]+.*|[ \t]*)$")
TABLE_SEPARATOR = re.compile(r"^:?-{3,}:?$")


def git(repo: str, *args: str) -> subprocess.CompletedProcess[bytes]:
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    try:
        return subprocess.run(
            ["git", "-c", "core.hooksPath=/dev/null", "-C", repo, *args],
            env=env, capture_output=True, check=False, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise BadInput(f"Git could not read the requested lesson: {exc}") from None


def read_committed_lesson(repo_arg: str, revision: str, lesson: str) -> str:
    if not repo_arg:
        raise BadInput("--repo must not be empty")
    try:
        repo = str(Path(repo_arg).expanduser().resolve(strict=True))
    except OSError as exc:
        raise BadInput(f"--repo is not readable: {exc}") from None
    if not Path(repo).is_dir():
        raise BadInput("--repo must name a directory")
    if not revision or revision.startswith("-"):
        raise BadInput("--rev must be non-empty and must not start with '-' ")
    if not lesson or lesson.startswith("-"):
        raise BadInput("--lesson must be a repository-relative path")
    lesson_path = PurePosixPath(lesson)
    if lesson_path.is_absolute() or ".." in lesson_path.parts:
        raise BadInput("--lesson must not be absolute or contain '..'")

    resolved = git(repo, "rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}")
    if resolved.returncode:
        raise BadInput(f"--rev does not resolve to a commit: {revision}")
    try:
        commit = resolved.stdout.decode("ascii").strip()
    except UnicodeDecodeError:
        raise BadInput("Git returned a non-ASCII commit id") from None
    blob = git(repo, "cat-file", "blob", f"{commit}:{lesson}")
    if blob.returncode:
        raise BadInput(f"lesson is not a readable file at {commit}: {lesson}")
    try:
        return blob.stdout.decode("utf-8")
    except UnicodeDecodeError:
        raise BadInput(f"lesson is not UTF-8: {lesson}") from None


def gate_lines(text: str) -> list[tuple[int, str]]:
    lines = text.splitlines()
    starts = [index for index, line in enumerate(lines) if GATE_HEADING.fullmatch(line)]
    if not starts:
        return []
    result: list[tuple[int, str]] = []
    for start in starts:
        end = next((index for index in range(start + 1, len(lines))
                    if SECTION_HEADING.fullmatch(lines[index])), len(lines))
        result.extend((index + 1, lines[index]) for index in range(start + 1, end))
    return result


def clean_cell(value: str) -> str:
    return value.replace("**", "").replace("`", "").strip()


def has_reason(decision: str, separate_reason: str = "") -> bool:
    """A decision cell must start with reject; inline or separate reason must follow."""
    decision = clean_cell(decision)
    match = re.match(r"(?i)^reject(?:ed)?\b(?P<tail>.*)$", decision)
    if match is None:
        return False
    tail = match.group("tail")
    tail = re.sub(r"(?i)^\s*,?\s*tier\s+[A-Z0-9_-]+\b", "", tail)
    inline_reason = tail.lstrip(" \t,:;—–-").strip()
    return bool(inline_reason or clean_cell(separate_reason))


def split_table_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or "|" not in stripped[1:]:
        return None
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def header_name(cell: str) -> str:
    return re.sub(r"[^a-z]", "", clean_cell(cell).lower())


def line_reason(line: str) -> bool:
    """Recognize explicit decision prose on a source bullet/line."""
    if not re.match(r"^\s*(?:[-*+]\s*)?S[0-9]{3,}\b", line):
        return False
    patterns = (
        re.compile(r"(?i)\*\*\s*reject(?:ed)?\s*\*\*(?P<tail>.*)$"),
        re.compile(r"(?i)\bdecision\s*[:=]\s*reject(?:ed)?\b(?P<tail>.*)$"),
        re.compile(r"(?i)[—–]\s*reject(?:ed)?\b(?P<tail>.*)$"),
    )
    for pattern in patterns:
        match = pattern.search(line)
        if match and has_reason("reject" + match.group("tail")):
            return True
    return False


def find_rejection(lines: list[tuple[int, str]]) -> tuple[int, str] | None:
    table_headers: list[str] | None = None
    for number, line in lines:
        cells = split_table_row(line)
        if cells is None:
            if line.strip():
                table_headers = None
            if SOURCE_ID.search(line) and line_reason(line):
                return number, line
            continue

        labels = [header_name(cell) for cell in cells]
        if "decision" in labels and "id" in labels:
            table_headers = labels
            continue
        if all(TABLE_SEPARATOR.fullmatch(cell.replace(" ", "")) for cell in cells):
            continue
        if table_headers is None or not any(SOURCE_ID.search(cell) for cell in cells):
            continue
        decision_index = table_headers.index("decision")
        if decision_index >= len(cells):
            continue
        reason_index = table_headers.index("reason") if "reason" in table_headers else -1
        separate_reason = cells[reason_index] if 0 <= reason_index < len(cells) else ""
        if has_reason(cells[decision_index], separate_reason):
            return number, line
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="lane repository")
    parser.add_argument("--rev", required=True, help="commit to read")
    parser.add_argument("--lesson", required=True, help="repository-relative lesson path")
    args = parser.parse_args(argv)
    try:
        text = read_committed_lesson(args.repo, args.rev, args.lesson)
    except BadInput as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    match = find_rejection(gate_lines(text))
    if match is None:
        print("NO MATCH: ## Gate has no source decision beginning with reject and a non-empty reason")
        return 1
    number, line = match
    print(f"MATCH: {args.lesson}:{number}: {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
