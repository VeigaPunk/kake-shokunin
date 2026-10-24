#!/usr/bin/env python3
"""Round-37 criterion (d) v2: a control report must record a listing of a key-free tree.

A report passes when every tree listing it quotes (`ls -l`, `ls -la`, `ls -laR` or
`git ls-tree` output) names the tree it covers and shows no path that is, or lies above, a
sealed key.  The check fails when any listing shows

  * a path component named `sealed` (ASCII case-insensitive),
  * a file name matching `cases*.json` (ASCII case-insensitive),
  * a path matching one of the `--pattern` key paths, or
  * a listed directory that lies on a `--pattern` key path above the key file: a non-recursive
    listing that stops at `.ufo` (or `private`) cannot certify the subtree under it, which is
    how the round-36 check passed a root listing over a tree that held `sealed/key.json`.

With `--tree`, each named tree is also walked on disk and every report must record a listing
whose root is that tree or lies inside it.

Usage:
  control_tree_check.py --report PATH [--report PATH ...] [--pattern KEYPATH ...]
                        [--tree DIR ...]

Exit 0: every report passes.  Exit 1: a listing shows a key path or a key-named entry, lies
above one, records no listing, or no listing covers a named tree.  Exit 2: a report or tree
could not be read, or the arguments were wrong.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import posixpath
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# `ls -l` entry: type char, permissions, optional ACL/xattr marker, then the fields.
LS_ENTRY_RE = re.compile(r"^(?P<mode>[-bcdDlMnpPs])[rwxSsTt-]{9}[.+@]?\s")
# `git ls-tree` entry: mode, type, object id, tab, path
LS_TREE_RE = re.compile(
    r"^(?P<mode>\d{6})\s+(?P<type>blob|tree|commit)\s+(?P<oid>[0-9a-f]{40,64})\t(?P<path>.*)$"
)
# An `ls` invocation with a path argument, as a report quotes it.
LS_COMMAND_RE = re.compile(
    r"\bls\b(?:\s+-{1,2}[A-Za-z][A-Za-z0-9-]*)*\s+(?P<path>\"[^\"]+\"|'[^']+'|[^\s`\"',;()]+)"
)
# A recursive `ls` section header: `./sub:` or `/abs/dir:` or `.:`
SECTION_RE = re.compile(r"^(?P<path>\.|[./][^\s:]*):$")
PATH_LIKE_RE = re.compile(r"^(?:[./]|~)")
KEY_NAME_RE = re.compile(r"^cases.*\.json$", re.IGNORECASE)

CONTAINER = "container"
PLAIN = "plain"
MAX_WALK = 200_000


class InputError(Exception):
    """A report or tree could not be read, or the arguments were wrong."""


@dataclass
class Entry:
    path: str
    is_dir: bool


@dataclass
class Listing:
    kind: str            # "ls" or "git ls-tree"
    root: str | None     # directory the listing names, None when the report does not say
    entries: list[Entry] = field(default_factory=list)


def _components(path: str) -> list[str]:
    """Split a path into components, dropping the root marker and empty parts."""
    return [part for part in path.replace("\\", "/").split("/") if part not in ("", ".")]


def _aligned(parts: list[str], values: list[str], start: int, directory: bool) -> bool:
    """Does the pattern component run match the path component run at `start`?"""
    for index, part in enumerate(parts):
        value = values[start + index]
        if index == len(parts) - 1 and not directory:
            if not value.startswith(part):
                return False
        elif value != part:
            return False
    return True


def _matches(pattern: str, path: str, is_dir: bool) -> bool:
    """True when a listed path matches a key path pattern."""
    pat = pattern.strip().strip("\"'")
    cand = path.strip()
    if not pat or not cand:
        return False
    directory = pat.endswith("/") or is_dir
    absolute = pat.startswith("/")
    parts = _components(pat)
    values = _components(cand)
    if not parts or not values:
        return False
    starts = (0,) if absolute else range(max(0, len(values) - len(parts) + 1))
    for start in starts:
        if start + len(parts) <= len(values) and _aligned(parts, values, start, directory):
            return True
    return False


def _above_key(pattern: str, path: str, is_dir: bool) -> bool:
    """True when a listed directory sits on the key path above the key file."""
    if not is_dir:
        return False
    pat = _components(pattern)
    values = _components(path)
    if not pat or not values:
        return False
    absolute = pattern.startswith("/")
    starts = (0,) if absolute else range(len(values))
    for start in starts:
        length = len(values) - start
        if not 0 < length < len(pat):
            continue
        if all(values[start + index] == pat[index] for index in range(length)):
            return True
    return False


def _key_named(path: str) -> str | None:
    """Return the key-like component of a path, or None."""
    for part in _components(path):
        if part.lower() == "sealed":
            return part
    parts = _components(path)
    if parts and KEY_NAME_RE.match(parts[-1]):
        return parts[-1]
    return None


def _ls_name(line: str) -> tuple[str, bool] | None:
    """Return (entry name, is_dir) for an `ls -l` line, or None if it is not an entry."""
    match = LS_ENTRY_RE.match(line)
    if match is None:
        return None
    parts = line.split(None, 8)
    if len(parts) < 9:
        return None
    name = parts[8].strip()
    if " -> " in name:
        name = name.split(" -> ", 1)[0].strip()
    return name, match.group("mode") == "d"


def _join(root: str | None, name: str) -> str:
    """Join a listed entry name to the listing root."""
    if root is None:
        return name
    base = root.rstrip("/") or "/"
    if name == ".":
        return base
    if name == "..":
        return posixpath.normpath(f"{base}/..")
    if posixpath.isabs(name):
        return name
    return f"{base}/{name}"


def _parse(document: str) -> list[Listing]:
    """Return the tree listings a report quotes."""
    commands: list[tuple[int, str]] = [
        (match.start(), match.group("path").strip().strip("\"'"))
        for match in LS_COMMAND_RE.finditer(document)
        if PATH_LIKE_RE.match(match.group("path").strip().strip("\"'"))
    ]
    listings: list[Listing] = []
    current: Listing | None = None
    last_command_root: str | None = None
    offset = 0
    for line in document.splitlines():
        tree = LS_TREE_RE.match(line)
        if tree is not None:
            path = tree.group("path").strip()
            if len(path) >= 2 and path[0] == '"' and path[-1] == '"':
                path = path[1:-1]
            if current is None or current.kind != "git ls-tree":
                current = Listing("git ls-tree", "")
                listings.append(current)
            current.entries.append(Entry(path, tree.group("type") == "tree"))
            offset += len(line) + 1
            continue
        section = SECTION_RE.match(line)
        if section is not None:
            header = section.group("path")
            if header.startswith("./") and last_command_root and last_command_root.startswith("/"):
                root = posixpath.normpath(posixpath.join(last_command_root, header[2:]))
            else:
                root = header
            current = Listing("ls", root.rstrip("/") or "/")
            listings.append(current)
            offset += len(line) + 1
            continue
        entry = _ls_name(line)
        if entry is not None:
            name, is_dir = entry
            root = None
            if current is not None and current.kind == "ls":
                root = current.root
            else:
                for start, path in commands:
                    if start < offset:
                        root = path
                    else:
                        break
                last_command_root = root
                current = Listing("ls", root)
                listings.append(current)
            current.entries.append(Entry(_join(root, name), is_dir))
        offset += len(line) + 1
    return listings


def _walk_tree(tree: Path) -> list[Entry]:
    """Every path under a tree, relative to it, bounded."""
    found: list[Entry] = []
    count = 0
    for base, dirnames, filenames in os.walk(tree):
        dirnames[:] = [name for name in dirnames if name != ".git"]
        rel = os.path.relpath(base, tree)
        prefix = "" if rel == "." else rel.replace(os.sep, "/") + "/"
        for name in dirnames:
            found.append(Entry(prefix + name, True))
        for name in filenames:
            found.append(Entry(prefix + name, False))
        count += len(dirnames) + len(filenames)
        if count > MAX_WALK:
            raise InputError(f"tree {tree} holds more than {MAX_WALK} entries")
    return found


def _covered(listings: list[Listing], tree: Path) -> bool:
    """True when a listing names the tree or a directory inside it."""
    target = tree.resolve()
    for listing in listings:
        if listing.root is None:
            continue
        root = Path(listing.root)
        if not root.is_absolute():
            continue
        try:
            resolved = root.resolve()
        except OSError:
            continue
        if resolved == target or target in resolved.parents:
            return True
    return False


def _check_report(report: Path, patterns: list[str], trees: list[tuple[Path, list[Entry]]]) -> bool:
    """True when the report passes; prints the reason either way."""
    try:
        document = report.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise InputError(f"cannot read report {report}: {exc}") from exc

    listings = _parse(document)
    if not listings:
        print(f"FAIL: {report} records no tree listing (no `ls -l` and no `git ls-tree` output).")
        return False

    ok = True
    seen = 0
    reported: set[tuple[str, str, str]] = set()

    def emit(message: str, key: tuple[str, str, str]) -> None:
        if key in reported:
            return
        reported.add(key)
        print(message)

    for listing in listings:
        label = listing.root if listing.root is not None else "an unnamed directory"
        for entry in listing.entries:
            seen += 1
            named = _key_named(entry.path)
            if named is not None:
                emit(
                    f"FAIL: {report} lists key-named path {entry.path!r} "
                    f"('{named}') in the listing of {label}.",
                    ("name", entry.path, named),
                )
                ok = False
                continue
            for pattern in patterns:
                if _above_key(pattern, entry.path, entry.is_dir):
                    emit(
                        f"FAIL: {report} lists directory {entry.path!r} in the listing "
                        f"of {label}; it lies on key path {pattern!r}, so the listing cannot "
                        f"certify the subtree under it.",
                        ("above", entry.path, pattern),
                    )
                    ok = False
                    break
                if _matches(pattern, entry.path, entry.is_dir):
                    kind = "directory" if entry.is_dir else "file"
                    emit(
                        f"FAIL: {report} lists key path {entry.path!r} ({kind}) "
                        f"in the listing of {label}, matching pattern {pattern!r}.",
                        ("path", entry.path, pattern),
                    )
                    ok = False
                    break
        if listing.root is None and not any(
            _key_named(entry.path) for entry in listing.entries
        ):
            print(
                f"WARN: {report} quotes a listing under {label}; it names no root, so it "
                f"cannot vouch for tree identity (checked for key-named entries only)."
            )

    for tree, entries in trees:
        if not _covered(listings, tree):
            print(f"FAIL: {report} records no listing of the control tree {tree}.")
            ok = False
            continue
        for entry in entries:
            named = _key_named(entry.path)
            if named is not None:
                print(
                    f"FAIL: {report}'s control tree {tree} holds key-named path "
                    f"{entry.path!r} ('{named}') although no listing above shows it."
                )
                ok = False
                break
            hit = next((p for p in patterns if _matches(p, entry.path, entry.is_dir)), None)
            if hit is not None:
                print(
                    f"FAIL: {report}'s control tree {tree} holds key path "
                    f"{entry.path!r} matching {hit!r} although no listing above shows it."
                )
                ok = False
                break

    if ok:
        kinds = ", ".join(sorted({listing.kind for listing in listings}))
        print(
            f"PASS: {report} records {len(listings)} listing(s) ({kinds}; {seen} listed "
            f"paths) that name their trees and show no key path, key-named entry, or "
            f"directory above one."
        )
    return ok


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
    trees: list[tuple[Path, list[Entry]]] = []
    for value in args.tree:
        tree = Path(value).resolve(strict=True)
        if not tree.is_dir():
            raise InputError(f"tree is not a directory: {tree}")
        trees.append((tree, _walk_tree(tree)))
    results = [_check_report(report, args.pattern, trees) for report in reports]
    return 0 if all(results) else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check that a control report records a key-free tree listing."
    )
    parser.add_argument("--report", action="append", required=True, help="control report (markdown); repeatable")
    parser.add_argument("--pattern", action="append", default=[], help="key path pattern; repeatable")
    parser.add_argument("--tree", action="append", default=[], help="control tree walked on disk; repeatable")
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
