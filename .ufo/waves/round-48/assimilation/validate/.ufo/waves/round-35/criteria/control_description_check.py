#!/usr/bin/env python3
"""Check whether a retained-control description quotes a source line."""

from __future__ import annotations

import argparse
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile


class InputError(Exception):
    """An input could not be read or did not identify one document block."""


FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
BLOCK_START_RE = re.compile(
    r"^ {0,3}(?:#{1,6}(?:\s|$)|>|[-+*]\s+|\d+[.)]\s+|(?:---+|\*\*\*+|___+)\s*$)"
)
INLINE_CODE_RE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.DOTALL)


class Git:
    def __init__(self, repo: Path | None = None) -> None:
        self.repo = repo
        self.env = os.environ.copy()
        for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
            self.env.pop(name, None)
        self.env["GIT_TERMINAL_PROMPT"] = "0"

    def run(self, *args: str) -> bytes:
        command = ["git"]
        if self.repo is not None:
            command.extend(("-C", str(self.repo)))
        command.extend(args)
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.env,
            check=False,
        )
        if result.returncode:
            detail = result.stderr.decode("utf-8", "replace").strip()
            raise InputError(f"git {args[0]} failed: {detail or result.returncode}")
        return result.stdout


def _resolve_commit(git: Git, revision: str) -> str:
    expression = f"{revision}^{{commit}}"
    result = git.run("rev-parse", "--verify", "--end-of-options", expression)
    commit = result.decode("ascii", "strict").strip()
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", commit):
        raise InputError(f"revision did not resolve to a commit: {revision!r}")
    return commit


def _validate_git_path(value: str, label: str) -> str:
    if not value or "\x00" in value or value.startswith("/"):
        raise InputError(f"invalid {label} repository path: {value!r}")
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise InputError(f"invalid {label} repository path: {value!r}")
    if PurePosixPath(value).is_absolute():
        raise InputError(f"invalid {label} repository path: {value!r}")
    return value


def _read_blob(git: Git, revision: str, path: str, label: str) -> bytes:
    commit = _resolve_commit(git, revision)
    return git.run("cat-file", "blob", f"{commit}:{_validate_git_path(path, label)}")


def _fenced_lines(lines: list[str]) -> list[bool]:
    flags: list[bool] = []
    fence_char: str | None = None
    fence_length = 0
    for line in lines:
        if fence_char is None:
            opening = FENCE_RE.match(line)
            if opening is None:
                flags.append(False)
                continue
            fence = opening.group(1)
            fence_char, fence_length = fence[0], len(fence)
            flags.append(True)
            continue

        flags.append(True)
        closing = FENCE_RE.match(line)
        if closing is not None:
            fence = closing.group(1)
            if fence[0] == fence_char and len(fence) >= fence_length:
                fence_char = None
                fence_length = 0
    return flags


def _is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and "|" in stripped[1:]


def _is_block_boundary(line: str) -> bool:
    return not line.strip() or _is_table_row(line) or BLOCK_START_RE.match(line) is not None or FENCE_RE.match(line) is not None


def _paragraph(lines: list[str], flags: list[bool], index: int) -> str | None:
    if flags[index] or _is_block_boundary(lines[index]):
        return None
    start = index
    end = index
    while start > 0 and not flags[start - 1] and not _is_block_boundary(lines[start - 1]):
        start -= 1
    while end + 1 < len(lines) and not flags[end + 1] and not _is_block_boundary(lines[end + 1]):
        end += 1
    return "\n".join(lines[start : end + 1])


def _target_block(document: str, anchor: str) -> str:
    lines = document.splitlines()
    flags = _fenced_lines(lines)
    blocks: list[str] = []
    for index, line in enumerate(lines):
        if anchor not in line or flags[index]:
            continue
        if _is_table_row(line):
            block = line.strip()
        else:
            block = _paragraph(lines, flags, index)
        if block is not None and block not in blocks:
            blocks.append(block)
    if not blocks:
        raise InputError(f"anchor {anchor!r} is not in a paragraph or table row")
    if len(blocks) != 1:
        raise InputError(f"anchor {anchor!r} identifies multiple paragraphs or table rows")
    return blocks[0]


def _names_line_number(block: str, number: int) -> bool:
    n = str(number)
    patterns = (
        rf"\b(?:line|lines)\s+#?{n}\b",
        rf"\bL\s*#?{n}\b",
        rf"(?<![\w`])[^\s`|]+:{n}\b",
    )
    return any(re.search(pattern, block, re.IGNORECASE) for pattern in patterns)


def _quoted_source_line(block: str, source: str) -> tuple[int, int] | None:
    source_lines = source.splitlines()
    for number, line in enumerate(source_lines, start=1):
        if not line.strip() or len(line) < 20:
            continue
        if not _names_line_number(block, number):
            continue
        for match in INLINE_CODE_RE.finditer(block):
            if match.group(2) == line:
                return number, len(line)
    return None


def _local_input(value: str, label: str, *, directory: bool) -> Path:
    try:
        path = Path(value).resolve(strict=True)
    except OSError as exc:
        raise InputError(f"cannot read {label} {value!r}: {exc}") from exc
    if directory and not path.is_dir():
        raise InputError(f"{label} is not a directory: {path}")
    if not directory and not path.is_file():
        raise InputError(f"{label} is not a regular file: {path}")
    return path


def check(args: argparse.Namespace) -> int:
    repo = _local_input(args.repo, "repository", directory=True)
    bundle = _local_input(args.bundle, "bundle", directory=False)
    tmp_root_value = os.environ.get("TMPDIR")
    try:
        tmp_root = Path(tmp_root_value).resolve(strict=True) if tmp_root_value else Path(tempfile.gettempdir())
    except OSError as exc:
        raise InputError(f"cannot read TMPDIR {tmp_root_value!r}: {exc}") from exc
    if not tmp_root.is_dir():
        raise InputError(f"TMPDIR is not a directory: {tmp_root}")

    with tempfile.TemporaryDirectory(prefix="control-description-check-", dir=tmp_root) as temporary:
        clone = Path(temporary) / "repo"
        Git().run("clone", "--quiet", "--local", "--no-hardlinks", "--no-checkout", str(repo), str(clone))
        git = Git(clone)
        git.run(
            "fetch",
            "--quiet",
            "--no-tags",
            "--no-recurse-submodules",
            str(bundle),
            "+refs/*:refs/remotes/control/*",
        )
        source = _read_blob(git, args.revision, args.path, "source")
        document = _read_blob(git, args.doc_rev, args.doc, "document")

    try:
        source_text = source.decode("utf-8")
        document_text = document.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InputError(f"source or document is not UTF-8: {exc}") from exc

    block = _target_block(document_text, args.anchor)
    quote = _quoted_source_line(block, source_text)
    if quote is None:
        print(
            f"FAIL: paragraph for anchor {args.anchor!r} does not backtick a whole source line "
            "of at least 20 characters and name its line number."
        )
        return 1
    number, length = quote
    print(f"PASS: paragraph for anchor {args.anchor!r} quotes source line {number} verbatim ({length} characters).")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check that a retained-control description quotes one exact source line."
    )
    parser.add_argument("--repo", required=True, help="local Git repository used as the clone source")
    parser.add_argument("--bundle", required=True, help="local Git bundle containing the control revision")
    parser.add_argument("--revision", required=True, help="control commit or revision")
    parser.add_argument("--path", required=True, help="source file path at --revision")
    parser.add_argument("--doc", required=True, help="document path at --doc-rev")
    parser.add_argument("--doc-rev", required=True, help="document commit or revision")
    parser.add_argument("--anchor", required=True, help="text identifying the paragraph or table row")
    parser.allow_abbrev = False
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return check(args)
    except (InputError, OSError, UnicodeError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
