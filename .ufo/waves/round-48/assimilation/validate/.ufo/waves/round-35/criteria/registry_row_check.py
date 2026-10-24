#!/usr/bin/env python3
"""Check scripts with an exit contract against SKILL.md gate registry rows."""
from __future__ import annotations

import argparse
import ast
import io
import re
import subprocess
import sys
import tokenize
from pathlib import Path

EXIT_DOC_RE = re.compile(
    r"\bexit(?:\s+(?:codes?|statuses?))?\b.{0,80}?\b(?:0|1|2|64)\b",
    re.IGNORECASE | re.DOTALL,
)
TABLE_SEPARATOR_RE = re.compile(r":?-{3,}:?")
SCRIPT_PATH_RE_CACHE: dict[str, re.Pattern[str]] = {}


class InputError(Exception):
    """An input could not be read as the requested repository revision."""


def git_output(repo: Path, *args: str) -> bytes:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise InputError(f"cannot run git: {exc}") from exc
    if completed.returncode != 0:
        raise InputError(f"git command failed with exit {completed.returncode}")
    return completed.stdout


def revision_objects(repo: Path, revision: str) -> tuple[str, str]:
    value = f"{revision}^{{commit}}"
    try:
        commit = git_output(repo, "rev-parse", "--verify", "--end-of-options", value).decode("ascii").strip()
        tree = git_output(repo, "rev-parse", "--verify", "--end-of-options", f"{commit}^{{tree}}").decode("ascii").strip()
        return commit, tree
    except (InputError, UnicodeDecodeError):
        tree_value = f"{revision}^{{tree}}"
        try:
            tree = git_output(repo, "rev-parse", "--verify", "--end-of-options", tree_value).decode("ascii").strip()
        except (InputError, UnicodeDecodeError) as exc:
            raise InputError("revision is not a readable commit or tree") from exc
        return tree, tree

def script_paths(repo: Path, tree: str) -> list[str]:
    output = git_output(repo, "ls-tree", "-r", "-z", "--name-only", tree, "--", "scripts/")
    try:
        paths = output.decode("utf-8").split("\0")
    except UnicodeDecodeError as exc:
        raise InputError("a repository path is not UTF-8") from exc
    return sorted(
        path
        for path in paths
        if path.startswith("scripts/")
        and "/" not in path[len("scripts/") :]
        and path.endswith(".py")
        and "selftest" not in Path(path).name.casefold()
    )


def source_text(repo: Path, tree: str, path: str) -> str:
    raw = git_output(repo, "show", f"{tree}:{path}")
    try:
        encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
        return raw.decode(encoding)
    except (SyntaxError, UnicodeDecodeError, LookupError) as exc:
        raise InputError(f"cannot decode {path}: {exc}") from exc


def assigned_names(target: ast.expr) -> list[str]:
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, (ast.Tuple, ast.List)):
        return [name for item in target.elts for name in assigned_names(item)]
    return []


def has_exit_contract(source: str, path: str) -> bool:
    try:
        module = ast.parse(source, filename=path)
    except SyntaxError as exc:
        raise InputError(f"cannot parse {path}: {exc}") from exc

    for statement in ast.walk(module):
        if isinstance(statement, ast.Assign):
            targets = statement.targets
        elif isinstance(statement, (ast.AnnAssign, ast.AugAssign)):
            targets = [statement.target]
        else:
            continue
        if any(
            name.startswith("EXIT_")
            for target in targets
            for name in assigned_names(target)
        ):
            return True
    docstring = ast.get_docstring(module, clean=False) or ""
    return EXIT_DOC_RE.search(docstring) is not None


def table_cells(line: str) -> list[str] | None:
    text = line.strip()
    if not text.startswith("|"):
        return None
    text = text[1:]
    if text.endswith("|"):
        text = text[:-1]

    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in text:
        if char == "|" and not escaped:
            cells.append("".join(current).strip())
            current = []
            continue
        current.append(char)
        if char == "\\" and not escaped:
            escaped = True
        else:
            escaped = False
    cells.append("".join(current).strip())
    return cells


def path_pattern(script_path: str) -> re.Pattern[str]:
    pattern = SCRIPT_PATH_RE_CACHE.get(script_path)
    if pattern is None:
        pattern = re.compile(
            r"(?<![A-Za-z0-9_./-])"
            + re.escape(script_path)
            + r"(?![A-Za-z0-9_./-])"
        )
        SCRIPT_PATH_RE_CACHE[script_path] = pattern
    return pattern


def row_covers_tool(skill: str, script_path: str) -> bool:
    kebab_name = Path(script_path).stem.replace("_", "-").casefold()
    lines = skill.splitlines()
    for index, line in enumerate(lines):
        header = table_cells(line)
        if header is None:
            continue
        normalized = [cell.strip().casefold() for cell in header]
        try:
            name_column = normalized.index("name")
            command_column = normalized.index("entry command")
        except ValueError:
            continue

        row_index = index + 1
        while row_index < len(lines):
            cells = table_cells(lines[row_index])
            if cells is None:
                break
            if all(TABLE_SEPARATOR_RE.fullmatch(cell.strip()) for cell in cells):
                row_index += 1
                continue
            if max(name_column, command_column) < len(cells):
                name = cells[name_column].strip().strip("`").casefold()
                command = cells[command_column]
                if name == kebab_name or path_pattern(script_path).search(command):
                    return True
            row_index += 1
    return False


def check(repo_arg: str, revision: str) -> tuple[str, list[str], int]:
    repo = Path(repo_arg).expanduser()
    if not repo.is_dir():
        raise InputError("repository path is not a directory")
    display_revision, tree = revision_objects(repo, revision)
    paths = script_paths(repo, tree)
    skill = source_text(repo, tree, "SKILL.md")

    missing: list[str] = []
    for path in paths:
        source = source_text(repo, tree, path)
        if has_exit_contract(source, path) and not row_covers_tool(skill, path):
            missing.append(path)
    return display_revision, missing, len(paths)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--rev", required=True)
    args = parser.parse_args(argv)

    try:
        display_revision, missing, scripts_seen = check(args.repo, args.rev)
    except InputError as exc:
        print(f"registry_row_check: {exc}", file=sys.stderr)
        return 2

    print(f"revision: {display_revision}")
    print(f"scripts scanned: {scripts_seen}")
    if missing:
        print("missing tools:")
        for path in missing:
            print(path)
        return 1
    print("missing tools: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
