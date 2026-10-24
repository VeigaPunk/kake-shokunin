#!/usr/bin/env python3
"""Check that a control report records the tree it was built from, and that tree is key-free.

Round-35 closure routed defect 4: a post-reveal control clone held the key
(`.ufo/waves/round-35/sealed/c2-probes.json`), so that control could not have been key-blind.
The repair: every control report must record the tree the control was built from, and that
recorded tree is checked against the key path patterns.

A control report must contain a tree listing of the tree the control was built from: either
`ls -la` output or `git ls-tree` output. The check fails when the report records no listing,
or when the listing shows a key path. It passes when a listing is present and shows no key
path.

Pattern semantics. A pattern is a path pattern:

  * paths are compared component by component. A pattern ending in "/" names a directory: every
    component must equal the listed path's component, so ".ufo/waves/round-36/sealed/" matches
    ".ufo/waves/round-36/sealed/c2-probes.json" but not ".ufo/waves/round-36/sealed_count.py".
  * a pattern not ending in "/" compares all components but the last by equality and the last by
    prefix, so "/fast/scratch/hyaku/kake-r36/.k" matches "/fast/scratch/hyaku/kake-r36/.key" and
    "/fast/scratch/hyaku/kake-r36/.k".
  * an absolute pattern is anchored at the filesystem root; a relative pattern may align at any
    component of the listed path, so it also matches an absolute listing that ends with it.

A listed path is a *container* when the listing enumerates its contents (the directory an
`ls -la` command named, or a tree entry of `git ls-tree`); otherwise it is a *plain* entry.
A container also matches when its trailing components are a head of the pattern, because the
recorded tree then holds the key.

For `ls -la` output the entry names are relative, so each name is also joined onto the
directory named in the nearest preceding `ls` command the report quotes. `git ls-tree` paths
are repository relative and are used as they stand.

Usage:
  control_tree_check.py --report PATH [--report PATH ...] --pattern PATTERN [--pattern ...]

Exit 0: every report records a tree listing and no listing shows a key path.
Exit 1: some report records no tree listing, or some listing shows a key path.
Exit 2: a report could not be read, or the arguments were wrong.
"""

from __future__ import annotations

import argparse
import posixpath
import re
import sys
from pathlib import Path

# `ls -l` entry: mode, links, owner, group, size, month, day, time-or-year, name...
LS_ENTRY_RE = re.compile(r"^[-bcdDlMnpPs][rwxSsTt-]{9}\s")
# `git ls-tree` entry: mode, type, object id, tab, path
LS_TREE_RE = re.compile(
    r"^(?P<mode>\d{6})\s+(?P<type>blob|tree|commit)\s+(?P<oid>[0-9a-f]{40,64})\t(?P<path>.*)$"
)
# An `ls` invocation with a path argument, as a report quotes it.
LS_COMMAND_RE = re.compile(
    r"\bls\b(?:\s+-{1,2}[A-Za-z][A-Za-z0-9-]*)*\s+(?P<path>\"[^\"]+\"|'[^']+'|[^\s`\"',;()]+)"
)
PATH_LIKE_RE = re.compile(r"^(?:[./]|~)")

CONTAINER = "container"
PLAIN = "plain"


class InputError(Exception):
    """A report could not be read."""


def _components(path: str) -> list[str]:
    """Split a path into components, dropping the root marker and empty parts."""
    return [part for part in path.replace("\\", "/").split("/") if part not in ("", ".")]


def _aligned(parts: list[str], values: list[str], start: int, directory: bool) -> bool:
    """Does the pattern component run match the path component run at `start`?"""
    for index, part in enumerate(parts):
        value = values[start + index]
        if index == len(parts) - 1 and not directory:
            # a pattern without a trailing slash may name a prefix of the last component
            if not value.startswith(part):
                return False
        elif value != part:
            return False
    return True


def _matches(pattern: str, path: str, kind: str) -> bool:
    """True when a listed path matches a key path pattern."""
    pat = pattern.strip().strip("\"'")
    cand = path.strip()
    if not pat or not cand:
        return False
    directory = pat.endswith("/")
    absolute = pat.startswith("/")
    parts = _components(pat)
    values = _components(cand)
    if not parts or not values:
        return False
    starts = (0,) if absolute else range(max(0, len(values) - len(parts) + 1))
    for start in starts:
        if start + len(parts) <= len(values) and _aligned(parts, values, start, directory):
            return True
    if kind == CONTAINER:
        # the container holds the key: its tail components are a head of the pattern
        starts = (0,) if absolute else range(len(values))
        for start in starts:
            length = len(values) - start
            if not 0 < length <= len(parts):
                continue
            if all(values[start + index] == parts[index] for index in range(length)):
                return True
    return False


def _ls_name(line: str) -> str | None:
    """Return the entry name of an `ls -l` line, or None if the line is not an entry."""
    if not LS_ENTRY_RE.match(line):
        return None
    parts = line.split(None, 8)
    if len(parts) < 9:
        return None
    name = parts[8].strip()
    if " -> " in name:
        name = name.split(" -> ", 1)[0].strip()
    return name


def _ls_commands(document: str) -> list[tuple[int, str]]:
    """Return (offset, path) for every `ls` invocation the report quotes with a path."""
    found: list[tuple[int, str]] = []
    for match in LS_COMMAND_RE.finditer(document):
        path = match.group("path").strip().strip("\"'")
        if not path or not PATH_LIKE_RE.match(path):
            continue
        found.append((match.start(), path))
    return found


def _root_for(commands: list[tuple[int, str]], offset: int) -> str | None:
    """The directory named by the `ls` command the report quotes for this listing.

    The nearest command before the entry wins; if the report quotes the command after the
    listing, the nearest one after it is used instead.
    """
    before: str | None = None
    after: str | None = None
    for start, path in commands:
        if start < offset:
            before = path
        elif after is None:
            after = path
    return before if before is not None else after


def _listed_paths(document: str) -> tuple[list[tuple[str, str]], list[str]]:
    """Return (listed paths with their kind, listing kinds) found in the report."""
    commands = _ls_commands(document)
    entries: list[tuple[str, str]] = []
    kinds: list[str] = []
    offset = 0
    for line in document.splitlines():
        tree = LS_TREE_RE.match(line)
        if tree is not None:
            kinds.append("git ls-tree")
            path = tree.group("path").strip()
            if len(path) >= 2 and path[0] == '"' and path[-1] == '"':
                path = path[1:-1]
            kind = CONTAINER if tree.group("type") == "tree" else PLAIN
            entries.append((path, kind))
            offset += len(line) + 1
            continue
        name = _ls_name(line)
        if name is not None:
            if "ls" not in kinds:
                kinds.append("ls")
            root = _root_for(commands, offset)
            base = root.rstrip("/") if root else None
            if base is None:
                entries.append((name, PLAIN))
            else:
                if name == ".":
                    joined = base
                elif name == "..":
                    joined = posixpath.normpath(f"{base}/..")
                else:
                    joined = f"{base}/{name}"
                entries.append((joined, PLAIN))
            offset += len(line) + 1
            continue
        offset += len(line) + 1
    # the directory an `ls` command named is a container: its contents are enumerated
    for _start, path in commands:
        if path.rstrip("/") not in {name for name, _kind in entries}:
            entries.append((path.rstrip("/"), CONTAINER))
    return entries, kinds


def _check_report(report: Path, patterns: list[str]) -> bool:
    """True when the report passes; prints the reason either way."""
    try:
        document = report.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise InputError(f"cannot read report {report}: {exc}") from exc

    entries, kinds = _listed_paths(document)
    if not kinds:
        print(f"FAIL: {report} records no tree listing (no `ls -la` and no `git ls-tree` output).")
        return False

    hits = sorted(
        {
            (path, kind, pattern)
            for path, kind in entries
            for pattern in patterns
            if _matches(pattern, path, kind)
        }
    )
    if hits:
        for path, kind, pattern in hits:
            print(f"FAIL: {report} lists a key path {path!r} ({kind}) matching pattern {pattern!r}.")
        return False

    print(
        f"PASS: {report} records a tree listing ({', '.join(sorted(set(kinds)))}; "
        f"{len(entries)} listed paths) and shows no key path."
    )
    return True


def check(args: argparse.Namespace) -> int:
    reports: list[Path] = []
    for value in args.report:
        try:
            path = Path(value).resolve(strict=True)
        except OSError as exc:
            raise InputError(f"cannot read report {value!r}: {exc}") from exc
        if not path.is_file():
            raise InputError(f"report is not a regular file: {path}")
        reports.append(path)
    if not reports:
        raise InputError("no report named")
    results = [_check_report(report, args.pattern) for report in reports]
    return 0 if all(results) else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check that a control report records a key-free tree listing."
    )
    parser.add_argument("--report", action="append", required=True, help="control report (markdown); repeatable")
    parser.add_argument("--pattern", action="append", required=True, help="key path pattern; repeatable")
    parser.allow_abbrev = False
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return check(args)
    except (InputError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
