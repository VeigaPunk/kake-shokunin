#!/usr/bin/env python3
"""Require a committed receipt for each hash measured in a report section.

Reads the report from disk and receipt bytes from the specified Git revision.
A receipt is a JSON file with a ``revision`` field beginning with the measured
hash, or a UTF-8 text file that names the hash.

Exit: 0 when every measured hash has a committed receipt, 1 when one or more
are missing, 2 when the report or Git input cannot be evaluated.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


class CouldNotEvaluate(Exception):
    pass


HASH_TOKEN = re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{7,40}(?![0-9a-fA-F])")
MEASURED_VALUE = re.compile(
    r"\b(?:met\s+)?\d+(?:\.\d+)?\s*(?:/|of)\s*\d+(?:\.\d+)?\b"
    r"|\b\d+(?:\.\d+)?\s*(?:→|->)\s*\d+(?:\.\d+)?\b",
    re.IGNORECASE,
)
HEADING = re.compile(r"^\s*(#{1,6})\s+(.+?)\s*#*\s*$")


def split_table_row(line):
    """Split a Markdown table row without treating escaped/code-span pipes as separators."""
    text = line.strip()
    if not text.startswith("|"):
        return None
    cells = []
    current = []
    in_code = False
    escaped = False
    for char in text[1:]:
        if char == "|" and not escaped and not in_code:
            cells.append("".join(current).strip())
            current = []
        elif char == "`" and not escaped:
            in_code = not in_code
            current.append(char)
        else:
            current.append(char)
        if char == "\\" and not escaped:
            escaped = True
        else:
            escaped = False
    last = "".join(current).strip()
    if last:
        cells.append(last)
    elif text.endswith("|") and cells:
        # A final delimiter leaves no last cell; the preceding delimiter already
        # ended the final actual cell.
        pass
    return cells


def measured_hashes(report_text):
    lines = report_text.splitlines()
    target = None
    for index, line in enumerate(lines):
        match = HEADING.match(line)
        if match and match.group(2).strip().casefold() == "before → after measurements".casefold():
            target = (index, len(match.group(1)))
            break
    if target is None:
        raise CouldNotEvaluate("report has no 'Before → after measurements' section")

    start, level = target
    section = []
    for line in lines[start + 1:]:
        match = HEADING.match(line)
        if match and len(match.group(1)) <= level:
            break
        section.append(line)

    header = None
    rows = []
    for line in section:
        cells = split_table_row(line)
        if cells is None:
            if header is not None and line.strip():
                # The measurement table ended; later prose is not part of it.
                break
            continue
        normalized = [cell.strip().strip("`").casefold() for cell in cells]
        if "before" in normalized and "after" in normalized:
            header = normalized
            continue
        if header is not None and len(cells) >= len(header):
            if all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells):
                continue
            rows.append(cells)

    if header is None:
        raise CouldNotEvaluate("measurement section has no before/after table")
    before_index = header.index("before")
    after_index = header.index("after")
    hashes = set()
    for row in rows:
        for index in (before_index, after_index):
            cell = row[index]
            if MEASURED_VALUE.search(cell):
                hashes.update(token.lower() for token in HASH_TOKEN.findall(cell))
    if not hashes:
        raise CouldNotEvaluate("measurement table contains no hash paired with a measured value")
    return sorted(hashes)


def git_output(repo, args, description):
    env = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(name, None)
    result = subprocess.run(["git", "-C", str(repo), *args],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            env=env, check=False)
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise CouldNotEvaluate("%s failed%s" %
                               (description, ": " + detail if detail else ""))
    return result.stdout


def resolve_commit(repo, revision):
    output = git_output(repo, ["rev-parse", "--verify", "--quiet", "--end-of-options",
                               revision + "^{commit}"], "resolving revision")
    commit = output.decode("ascii", "strict").strip()
    if not re.fullmatch(r"[0-9a-fA-F]{40,64}", commit):
        raise CouldNotEvaluate("Git returned an invalid commit id")
    return commit


def receipt_paths(repo, commit, round_number):
    directory = ".ufo/waves/round-%d/verification" % round_number
    output = git_output(repo, ["ls-tree", "-rz", "--name-only", "--full-tree",
                               commit, "--", directory],
                       "listing committed receipts")
    prefix = (directory + "/").encode("utf-8")
    return [os.fsdecode(path) for path in output.split(b"\0")
            if path.startswith(prefix)]


def text_names_hash(data, measured_hash):
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    if "\x00" in text:
        return False
    for token in HASH_TOKEN.findall(text):
        token = token.lower()
        if token.startswith(measured_hash) or measured_hash.startswith(token):
            return True
    return False


def has_receipt(data, path, measured_hash):
    try:
        document = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        if path.lower().endswith(".json"):
            return False
        # Round-34 wave 2 (MutReceiptPresenceCheck): a text file that merely
        # mentions a hash (for example this check's own diagnostic) is not a
        # receipt; a text receipt must also carry the hash in its file name.
        if measured_hash[:7] not in os.path.basename(path).lower():
            return False
        return text_names_hash(data, measured_hash)

    # JSON receipts count only through an explicit revision field. Existing
    # round-33 receipts call that field ``rev``; do not count incidental hashes
    # elsewhere in a JSON document.
    if isinstance(document, dict):
        revision = document.get("revision", document.get("rev"))
        if isinstance(revision, str) and revision.lower().startswith(measured_hash):
            return True
    return False


def unreceipted_hashes(repo, commit, round_number, hashes):
    paths = receipt_paths(repo, commit, round_number)
    blobs = []
    for path in paths:
        data = git_output(repo, ["show", "%s:%s" % (commit, path)],
                          "reading committed receipt %s" % path)
        blobs.append((path, data))
    return [measured_hash for measured_hash in hashes
            if not any(has_receipt(data, path, measured_hash)
                       for path, data in blobs)]


def main(argv=None):
    parser = argparse.ArgumentParser(prog="receipt_presence_check.py")
    parser.add_argument("--report", required=True, help="Markdown report to inspect")
    parser.add_argument("--repo", required=True, help="Git repository holding the lane")
    parser.add_argument("--rev", required=True, help="committed revision to inspect")
    parser.add_argument("--round", required=True, help="round number for the verification path")
    args = parser.parse_args(argv)

    try:
        round_number = int(args.round)
        if round_number < 1:
            raise CouldNotEvaluate("round must be a positive integer")
        report_path = Path(args.report)
        report_text = report_path.read_text(encoding="utf-8")
        hashes = measured_hashes(report_text)
        repo = Path(args.repo)
        if not repo.is_dir():
            raise CouldNotEvaluate("repository path is not a directory: %s" % repo)
        commit = resolve_commit(repo, args.rev)
        missing = unreceipted_hashes(repo, commit, round_number, hashes)
    except (OSError, UnicodeError, ValueError, CouldNotEvaluate) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2

    if missing:
        print("unreceipted hashes: %s" % ", ".join(missing))
        return 1
    print("all measured hashes have committed receipts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
