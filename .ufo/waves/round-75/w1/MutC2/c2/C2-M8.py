#!/usr/bin/env python3
"""instrument_receipts.py — C2 receipt binder, round 75 (kake).

Claim (frozen in .ufo/waves/round-75/contract.md section C2 and amendment 1 A2):
every live gate-registry instrument is bound to a committed receipt whose
sha256, byte length and static ``--selftest`` registration re-derive from the
committed blob at the receipt's revision.

Population rule (frozen in contract.md section C1; implemented here
independently of ``.ufo/waves/round-75/c75_row_truth.py``):

  * a registry row is an 8-column table row inside a section whose heading
    matches ``^### Round <N> gate registry additions`` (the row's line must
    start with ``|`` and carry at least six unescaped cells);
  * a row is live when its Kind cell does not contain ``historical``;
  * the row's instrument is the Name cell when that cell is itself a
    ``.py``/``.mjs`` path, else the first ``.py``/``.mjs`` path token of the
    Entry-command cell, else of the Self-test cell, else of the first cell (in
    cell order) that carries such a token;
  * the population is the set of resolved instruments, sorted.  The frozen 16
    paths of contract section C1 are a floor: ``missing_frozen`` must be 0,
    and any live-row instrument beyond the 16 is in-population (amendment 1).

Receipt (``corpus/knowledge/instrument-receipts.json``)::

    {"schema": "instrument-receipts/v1", "revision": "<40-hex>",
     "date": "YYYY-MM-DD", "host": "<sys.platform>-<machine>",
     "files": [{"path", "sha256", "bytes", "selftest_mode"}, ...]}

``files`` is sorted by path, the document is 2-space indented, ASCII-safe and
ends with one newline, so a second ``--write`` at the same revision is
byte-identical.

Exact static ``--selftest`` registration rule (implemented in
``selftest_registration``):

  * ``.py``: the committed source must parse; it registers ``--selftest`` iff
    its AST contains either
      (a) a call ``<expr>.add_argument(...)`` with a positional string-literal
          argument whose value is exactly ``--selftest``, or
      (b) an ``ast.Compare`` in which one operand is the string literal
          ``--selftest`` and at least one operator is ``==``, ``!=``, ``in``
          or ``not in``.
    A bare literal never counts: docstrings, comments, help text and
    subprocess argument lists (``run([node, script, "--selftest"])``) are
    ``ast.Constant`` nodes outside a call to ``add_argument`` and outside a
    comparison, so ``c69_tmp_honour.py`` — which only passes ``--selftest`` to
    another tool — derives ``selftest_mode=false``.
  * ``.mjs``: registers it iff the source matches
    ``includes('--selftest')``, ``indexOf('--selftest')`` or a
    ``[!]==``/``!===`` comparison against the literal ``--selftest``.  No
    round-75 population member is ``.mjs``; the fallback is exercised by the
    selftest's classifier check only.
  * anything undecidable (non-UTF-8, Python syntax error, unknown extension)
    is reported as ``unparsable``: never silently ``false``.

``--check`` reads the receipt from committed bytes at ``--revision`` only:
``git cat-file blob <rev>:corpus/knowledge/instrument-receipts.json``.  A
receipt that exists only in the worktree is reported as ``source=uncommitted``
and is a mismatch — the claim is a *committed* receipt, so an uncommitted
``--write`` is never admission evidence.

The receipt's declared ``revision`` must be a 40-hex commit id that
``git cat-file -e <rev>^{commit}`` resolves and that is an ancestor of (or
equal to) the measured revision (``git merge-base --is-ancestor``); otherwise
every population file is a ``receipt_revision_invalid`` mismatch.  The declared
revision is the *subject* revision whose committed blobs the entries pin; the
measured revision is the *carrier* commit that holds the receipt, which may be
a descendant (a receipt can only be committed after the revision it pins).

Exit: 0 met, 1 not met, 2 unevaluable, 64 usage.

CLI::

    instrument_receipts.py --root . --revision <rev> --check [--json]
    instrument_receipts.py --root . --revision <rev> --write --date 2026-11-03
    instrument_receipts.py --root . --revision <rev> --emit-population [--json]
    instrument_receipts.py --selftest --work <scratch dir>
"""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile

SCHEMA = "instrument-receipts/v1"
RECEIPT_PATH = "corpus/knowledge/instrument-receipts.json"

# Contract section C1, frozen 2026-11-03 (amendment 1: a floor, not equality).
FROZEN_POPULATION = (
    ".ufo/waves/round-52/c52_wave_ledger.py",
    ".ufo/waves/round-57/c57_idresolver_gate.py",
    ".ufo/waves/round-58/c58_receipt_rewrites.py",
    ".ufo/waves/round-58/c58_resolver_cases.py",
    ".ufo/waves/round-59/c59_axis_evidence.py",
    ".ufo/waves/round-59/c59_resolver_cases.py",
    ".ufo/waves/round-66/c66_gate_status_hostportable.py",
    ".ufo/waves/round-69/c69_recorded_counts.py",
    ".ufo/waves/round-69/c69_tmp_honour.py",
    ".ufo/waves/round-72/c72_tmp_v2.py",
    ".ufo/waves/round-73/c73_tmp_v3.py",
    ".ufo/waves/round-73/c73_wave_pointers.py",
    ".ufo/waves/round-74/c74_registry_gap.py",
    "scripts/citation_lint.py",
    "scripts/id_resolver.py",
    "scripts/redirect_audit.py",
)

SECTION_RE = re.compile(r"^### Round \d+ gate registry additions\b")
PATH_RE = re.compile(r"(?<![\w./-])((?:\.ufo|scripts)/[\w./-]+?\.(?:py|mjs))(?![\w./-])")
SHA256_RE = re.compile(r"[0-9a-f]{64}")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REGULAR_MODES = ("100644", "100755")

MJS_REG_RE = re.compile(
    r"""(?:includes\(\s*(['"])--selftest\1\s*\)"""
    r"""|indexOf\(\s*(['"])--selftest\2\s*\)"""
    r"""|(['"])--selftest\3\s*[!=]==?|=[!=]=\s*(['"])--selftest\4)""",
    re.X,
)


class Unevaluable(Exception):
    """The measured tree cannot be read (exit 2)."""


class Usage(Exception):
    """The invocation is wrong (exit 64)."""


class Parser(argparse.ArgumentParser):
    def error(self, message):  # argparse would exit 2; the contract says 64
        self.print_usage(sys.stderr)
        print(f"64 usage: {message}", file=sys.stderr)
        raise SystemExit(64)


# --------------------------------------------------------------------------
# git plumbing (read-only; the tool never writes anything but the receipt)
# --------------------------------------------------------------------------

def git_bytes(root, *args, stdin=None):
    return subprocess.run(
        ["git", "-C", root, *args], input=stdin, capture_output=True
    )


def _decode(raw):
    return raw.decode("utf-8", "replace").strip()


def require_toplevel(root):
    proc = git_bytes(root, "rev-parse", "--show-toplevel")
    if proc.returncode != 0:
        raise Unevaluable(f"--root {root} is not a git repository")
    top = _decode(proc.stdout)
    if not top or os.path.realpath(top) != os.path.realpath(root):
        raise Unevaluable(f"--root {root} is not the repository toplevel ({top})")


def resolve_revision(root, rev):
    proc = git_bytes(root, "rev-parse", "--verify", "--end-of-options", rev + "^{commit}")
    if proc.returncode != 0:
        raise Unevaluable(f"cannot resolve revision {rev!r}: {_decode(proc.stderr)}")
    full = _decode(proc.stdout)
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", full):
        raise Unevaluable(f"revision {rev!r} resolved to a non-object id {full!r}")
    return full


def read_skill(root, rev):
    proc = git_bytes(root, "cat-file", "blob", f"{rev}:SKILL.md")
    if proc.returncode != 0:
        raise Unevaluable(f"cannot read SKILL.md at {rev}: {_decode(proc.stderr)}")
    try:
        return proc.stdout.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Unevaluable(f"SKILL.md at {rev} is not UTF-8: {exc}") from None


def read_population_blobs(root, rev, paths):
    """Return {path: (mode, bytes)} for the population paths that exist."""
    if not paths:
        return {}
    proc = git_bytes(root, "ls-tree", "-z", rev, "--", *paths)
    if proc.returncode != 0:
        raise Unevaluable(f"git ls-tree failed at {rev}: {_decode(proc.stderr)}")
    entries = {}
    for record in proc.stdout.split(b"\0"):
        if not record:
            continue
        meta, _, raw_path = record.partition(b"\t")
        fields = meta.split(b" ")
        if len(fields) != 3:
            continue
        mode, kind, oid = (field.decode("ascii", "replace") for field in fields)
        path = raw_path.decode("utf-8", "surrogateescape")
        entries[path] = (mode, kind, oid)
    if not entries:
        return {}
    wanted = {oid: path for path, (_m, _k, oid) in entries.items() if _k == "blob"}
    stdin = "".join(f"{oid}\n" for oid in wanted).encode()
    batch = git_bytes(root, "cat-file", "--batch", stdin=stdin)
    if batch.returncode != 0:
        raise Unevaluable(f"git cat-file --batch failed at {rev}: {_decode(batch.stderr)}")
    data, pos, blobs = batch.stdout, 0, {}
    while pos < len(data):
        newline = data.find(b"\n", pos)
        if newline < 0:
            break
        header = data[pos:newline].decode("ascii", "replace")
        pos = newline + 1
        fields = header.split(" ")
        if len(fields) != 3 or fields[1] != "blob":
            continue  # <oid> missing / <oid> <type> <size> for non-blobs
        size = int(fields[2])
        blobs[fields[0]] = data[pos:pos + size]
        pos += size + 1  # the trailing newline after each object body
    return {
        path: (mode, blobs[oid])
        for path, (mode, kind, oid) in entries.items()
        if kind == "blob" and oid in blobs
    }


# --------------------------------------------------------------------------
# population derivation (frozen rule, independent implementation)
# --------------------------------------------------------------------------

def split_cells(line):
    text = line.rstrip()
    if not text.startswith("|"):
        return None
    parts = re.split(r"(?<!\\)\|", text)
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    cells = [part.strip() for part in parts]
    if len(cells) < 6:
        return None
    if len(cells) < 8:
        cells += [""] * (8 - len(cells))
    return cells[:8]


def parse_rows(text):
    rows, in_section = [], False
    for lineno, line in enumerate(text.splitlines(), 1):
        if SECTION_RE.match(line):
            in_section = True
            continue
        if line.startswith("### "):
            in_section = False
            continue
        if not in_section:
            continue
        cells = split_cells(line)
        if cells is None:
            continue
        if cells[0].strip("`") == "Name" or all(ch in "-: " for ch in cells[0]):
            continue
        rows.append({"line": lineno, "cells": cells})
    return rows


def row_instrument(cells):
    name = cells[0]
    if PATH_RE.fullmatch(name):
        return name
    for index in (2, 4):
        match = PATH_RE.search(cells[index])
        if match:
            return match.group(1)
    for cell in cells:
        match = PATH_RE.search(cell)
        if match:
            return match.group(1)
    return None


def derive_population(text):
    files, seen = [], set()
    for row in parse_rows(text):
        if "historical" in row["cells"][1].lower():
            continue
        instrument = row_instrument(row["cells"])
        if instrument and instrument not in seen:
            seen.add(instrument)
            files.append(instrument)
    return sorted(files)


# --------------------------------------------------------------------------
# static --selftest registration
# --------------------------------------------------------------------------

def _is_add_argument(node):
    func = node.func
    name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
    if name != "add_argument":
        return False
    for arg in node.args:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and arg.value == "--selftest":
            return True
    return False


def _compares_selftest(node):
    operands = [node.left, *node.comparators]
    literal = any(
        isinstance(op, ast.Constant) and op.value == "--selftest" for op in operands
    )
    if not literal:
        return False
    return any(isinstance(op, (ast.Eq, ast.NotEq, ast.In, ast.NotIn)) for op in node.ops)


def selftest_registration(path, blob):
    """Return (True|False|None, detail) — the exact rule is in the module docstring."""
    suffix = path.rsplit(".", 1)[-1].lower() if "." in path else ""
    try:
        source = blob.decode("utf-8")
    except UnicodeDecodeError as exc:
        return None, f"not UTF-8 ({exc.reason} at byte {exc.start})"
    if suffix == "py":
        try:
            tree = ast.parse(source, filename=path)
        except SyntaxError as exc:
            return None, f"Python syntax error at line {exc.lineno}"
        lines = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and _is_add_argument(node):
                lines.append(node.lineno)
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare) and _compares_selftest(node):
                lines.append(node.lineno)
        if lines:
            return True, "registrations at line(s) " + ", ".join(str(n) for n in sorted(set(lines)))
        return False, "no --selftest add_argument or comparison"
    if suffix == "mjs":
        match = MJS_REG_RE.search(source)
        if match:
            return True, f"argv test at line {source.count(chr(10), 0, match.start()) + 1}"
        return False, "no --selftest argv test"
    return None, f"no registration rule for .{suffix}"


# --------------------------------------------------------------------------
# receipt I/O
# --------------------------------------------------------------------------

def host_string():
    return f"{sys.platform}-{platform.machine()}"


def receipt_path(root):
    return os.path.join(root, *RECEIPT_PATH.split("/"))


def load_receipt(root, rev):
    """Return (document|None, source, worktree_state, problem|None).

    The receipt is read from committed bytes at ``--revision`` only:
    ``git cat-file blob <rev>:corpus/knowledge/instrument-receipts.json``.  A
    receipt that exists only in the worktree is ``source='uncommitted'`` and a
    mismatch — the claim is a *committed* receipt, so an uncommitted write is
    never admission evidence.  ``worktree_state`` is ``identical``/``differs``
    when a worktree copy exists and is compared, ``absent`` when it does not.
    """
    path = receipt_path(root)
    local = None
    if os.path.isfile(path):
        with open(path, "rb") as handle:
            local = handle.read()
    committed = git_bytes(root, "cat-file", "blob", f"{rev}:{RECEIPT_PATH}")
    if committed.returncode != 0:
        if local is not None:
            return None, "uncommitted", "only-worktree", (
                f"receipt exists only in the worktree ({RECEIPT_PATH}, "
                f"{len(local)} bytes); committed bytes at {rev} are required"
            )
        return None, "none", "absent", f"receipt file is absent at {rev} and in the worktree"
    raw, source = committed.stdout, "committed"
    worktree_state = "absent"
    if local is not None:
        worktree_state = "identical" if local == raw else "differs"
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, source, worktree_state, f"receipt is not valid JSON: {exc}"
    if not isinstance(document, dict):
        return None, source, worktree_state, "receipt root is not a JSON object"
    if document.get("schema") != SCHEMA:
        return None, source, worktree_state, (
            f"receipt schema is {document.get('schema')!r}, expected {SCHEMA!r}"
        )
    return document, source, worktree_state, None


def entry_problem(entry):
    if not isinstance(entry, dict):
        return "entry is not an object"
    if not isinstance(entry.get("path"), str):
        return "path is not a string"
    if not isinstance(entry.get("sha256"), str) or not SHA256_RE.fullmatch(entry["sha256"]):
        return "sha256 is not 64 lowercase hex digits"
    size = entry.get("bytes")
    if isinstance(size, bool) or not isinstance(size, int) or size < 0:
        return "bytes is not a non-negative integer"
    if not isinstance(entry.get("selftest_mode"), bool):
        return "selftest_mode is not a boolean"
    return None


# --------------------------------------------------------------------------
# predicates
# --------------------------------------------------------------------------

def declared_revision_problem(root, rev, declared):
    """The declared revision must be a resolvable ancestor (or equal) of --revision."""
    if not isinstance(declared, str) or not re.fullmatch(r"[0-9a-f]{40}", declared):
        return f"declared revision {declared!r} is not a 40-hex commit id"
    probe = git_bytes(root, "cat-file", "-e", declared + "^{commit}")
    if probe.returncode != 0:
        return f"declared revision {declared} does not resolve to a commit"
    ancestor = git_bytes(root, "merge-base", "--is-ancestor", declared, rev)
    if ancestor.returncode != 0:
        detail = _decode(ancestor.stderr)
        return (
            f"declared revision {declared} is not an ancestor of the measured revision "
            f"{rev} (merge-base --is-ancestor exit {ancestor.returncode}"
            + (f": {detail}" if detail else "")
            + ")"
        )
    return None


def evaluate(root, rev, frozen=FROZEN_POPULATION):
    population = derive_population(read_skill(root, rev))
    present = set(population)
    missing_frozen = [path for path in frozen if path not in present]
    beyond_frozen = [path for path in population if path not in set(frozen)]

    findings, outside, malformed = [], [], []
    bound = 0
    document, source, worktree_state, problem = load_receipt(root, rev)
    declared = document.get("revision") if isinstance(document, dict) else None
    revision_problem = None if problem else declared_revision_problem(root, rev, declared)

    if problem:
        for path in population:
            findings.append({"path": path, "class": "receipt", "detail": problem})
    elif revision_problem:
        for path in population:
            findings.append({
                "path": path, "class": "receipt_revision_invalid",
                "detail": revision_problem,
            })
    else:
        entries, duplicates = {}, set()
        for entry in document.get("files") or []:
            path = entry.get("path") if isinstance(entry, dict) else None
            if not isinstance(path, str):
                malformed.append("receipt has an entry without a string path")
                continue
            if path in entries:
                duplicates.add(path)
            else:
                entries[path] = entry
        outside = sorted(path for path in entries if path not in present)
        blobs = read_population_blobs(root, rev, population)
        for path in population:
            if path in duplicates:
                findings.append({
                    "path": path, "class": "duplicate",
                    "detail": "receipt lists this path more than once",
                })
                continue
            entry = entries.get(path)
            if entry is None:
                findings.append({
                    "path": path, "class": "missing",
                    "detail": "receipt has no entry for this path",
                })
                continue
            shape = entry_problem(entry)
            if shape:
                findings.append({"path": path, "class": "shape", "detail": shape})
                continue
            known = blobs.get(path)
            if known is None:
                findings.append({
                    "path": path, "class": "absent",
                    "detail": f"path does not resolve to a blob at {rev}",
                })
                continue
            mode, blob = known
            if mode not in REGULAR_MODES:
                findings.append({
                    "path": path, "class": "symlink" if mode == "120000" else "mode",
                    "detail": f"tree mode {mode} is not a regular file",
                })
                continue
            digest = hashlib.sha256(blob).hexdigest()
            flag, note = selftest_registration(path, blob)
            if flag is None:
                findings.append({"path": path, "class": "unparsable", "detail": note})
                continue
            if entry["sha256"] != digest:
                findings.append({
                    "path": path, "class": "digest",
                    "detail": f"receipt {entry['sha256'][:12]}... != committed {digest[:12]}...",
                })
            elif entry["bytes"] != len(blob):
                findings.append({
                    "path": path, "class": "bytes",
                    "detail": f"receipt {entry['bytes']} != committed {len(blob)}",
                })
            elif entry["selftest_mode"] != flag:
                findings.append({
                    "path": path, "class": "mode-flag",
                    "detail": f"receipt {entry['selftest_mode']} != derived {flag}",
                })
            else:
                bound += 1

    mismatches = len(population) - bound
    met = bool(population) and bound == len(population) and mismatches == 0 and not missing_frozen
    return {
        "revision": rev,
        "population": population,
        "population_size": len(population),
        "frozen_size": len(frozen),
        "missing_frozen": missing_frozen,
        "beyond_frozen": beyond_frozen,
        "receipt_source": source,
        "receipt_worktree": worktree_state,
        "receipt_revision": declared,
        "receipt_revision_valid": bool(
            problem is None and revision_problem is None and isinstance(document, dict)
        ),
        "revision_match": bool(isinstance(document, dict) and declared == rev),
        "bound": bound,
        "mismatches": mismatches,
        "outside": outside,
        "malformed": malformed,
        "findings": findings,
        "met": met,
    }


def line_for(result):
    return (
        f"C2v1 revision={result['revision']} population={result['population_size']} "
        f"bound={result['bound']} mismatches={result['mismatches']} "
        f"met={str(result['met']).lower()}"
    )


def report(result, as_json):
    line = line_for(result)
    print(line)
    if not as_json:
        print(
            f"  population: derived={result['population_size']} "
            f"frozen={result['frozen_size']} missing_frozen={len(result['missing_frozen'])} "
            f"beyond_frozen={len(result['beyond_frozen'])}"
        )
        print(
            f"  receipt: source={result['receipt_source']} worktree={result['receipt_worktree']} "
            f"declared={result['receipt_revision']} "
            f"declared_match={str(result['revision_match']).lower()} "
            f"declared_valid={str(result['receipt_revision_valid']).lower()}"
        )
        for path in result["missing_frozen"]:
            print(f"  finding: missing-frozen {path}: the frozen 16 no longer derive")
        for path in result["beyond_frozen"]:
            print(f"  population: beyond-frozen {path}")
        for finding in result["findings"]:
            print(f"  finding: {finding['class']} {finding['path']}: {finding['detail']}")
        for path in result["outside"]:
            print(f"  outside: {path} (not counted toward bound)")
        for note in result["malformed"]:
            print(f"  malformed: {note}")
    if as_json:
        payload = dict(result)
        payload["line"] = line
        print(json.dumps(payload, indent=2, sort_keys=True))


# --------------------------------------------------------------------------
# write
# --------------------------------------------------------------------------

def build_receipt(root, rev, date, frozen=FROZEN_POPULATION):
    population = derive_population(read_skill(root, rev))
    missing = [path for path in frozen if path not in set(population)]
    blobs = read_population_blobs(root, rev, population)
    files = []
    for path in reversed(population):
        if path not in blobs:
            raise Unevaluable(f"cannot bind {path}: it does not resolve to a blob at {rev}")
        mode, blob = blobs[path]
        if mode not in REGULAR_MODES:
            raise Unevaluable(f"cannot bind {path}: tree mode {mode} is not a regular file")
        flag, note = selftest_registration(path, blob)
        if flag is None:
            raise Unevaluable(f"cannot bind {path}: {note}")
        files.append({
            "path": path,
            "sha256": hashlib.sha256(blob).hexdigest(),
            "bytes": len(blob),
            "selftest_mode": flag,
        })
    document = {
        "schema": SCHEMA,
        "revision": rev,
        "date": date,
        "host": host_string(),
        "files": files,
    }
    return document, missing


def receipt_text(document):
    return json.dumps(document, indent=2, ensure_ascii=True) + "\n"


def write_receipt(root, rev, date, as_json):
    document, missing = build_receipt(root, rev, date)
    text = receipt_text(document)
    destination = receipt_path(root)
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    temporary = destination + ".tmp"
    with open(temporary, "w", encoding="ascii", newline="\n") as handle:
        handle.write(text)
    os.replace(temporary, destination)
    digest = hashlib.sha256(text.encode("ascii")).hexdigest()
    if as_json:
        print(json.dumps(document, indent=2, sort_keys=False))
    else:
        print(
            f"wrote {RECEIPT_PATH} revision={rev} population={len(document['files'])} "
            f"missing_frozen={len(missing)} sha256={digest} bytes={len(text.encode('ascii'))}"
        )
    for path in missing:
        print(f"  warning: frozen path {path} is missing at {rev}", file=sys.stderr)
    return 0


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------

TRUE_SOURCE = (
    b"import argparse\n\n\n"
    b"def main(argv=None):\n"
    b"    parser = argparse.ArgumentParser()\n"
    b"    parser.add_argument('--selftest', action='store_true')\n"
    b"    return 0\n"
)
FALSE_SOURCE = b"VALUE = 1\n# this fixture registers no command-line option\n"
TABLE_HEADER = (
    "| Name | Kind | Entry command | Verdict map | Self-test | "
    "Pinned values / frozen proof | Write scope | Owner |\n"
    "|---|---|---|---|---|---|---|---|\n"
)


def fixture_skill(rows):
    blocks = ["# Fixture skill", "", "### Round 900 gate registry additions", "", TABLE_HEADER.rstrip("\n")]
    blocks.extend(rows)
    blocks.extend([
        "",
        "### Round 901 gate registry additions",
        "",
        TABLE_HEADER.rstrip("\n"),
        "| fixture-historical | gate (historical; fixture) | "
        "`python3 -B scripts/fixture_historical.py` | `0=met` | none | fixture | read-only | fixture |",
        "",
        "### Round 902 registry notes",
        "",
        TABLE_HEADER.rstrip("\n"),
        "| fixture-unparsed | gate (live; fixture) | "
        "`python3 -B scripts/fixture_unparsed.py` | `0=met` | none | fixture | read-only | fixture |",
    ])
    return "\n".join(blocks) + "\n"


def fixture_rows(paths):
    rows = []
    for index, path in enumerate(paths):
        kind = index % 4
        if kind == 0:
            name = path
            entry = f"`python3 -B {path} --selftest`"
            selftest = f"`python3 -B {path} --selftest`"
            pinned = "fixture"
        elif kind == 1:
            name = "fixture-instrument"
            entry = f"`python3 -B {path} --selftest`"
            selftest = "`python3 -B {0} --selftest`".format(path)
            pinned = "fixture"
        elif kind == 2:
            name = "fixture-instrument"
            entry = "`true`"
            selftest = f"`python3 -B {path} --selftest`"
            pinned = "fixture"
        else:
            name = "fixture-instrument"
            entry = "`true`"
            selftest = "none"
            pinned = f"`{path}`"
        rows.append(
            f"| {name} | gate (live; fixture) | {entry} | `0=met` | {selftest} | {pinned} | read-only | fixture |"
        )
    return rows


def _git_fixture(directory, *args):
    proc = subprocess.run(["git", "-C", directory, *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"fixture git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def make_fixture(parent, name, paths, extra_rows=(), drop=None):
    directory = os.path.join(parent, name)
    os.makedirs(directory)
    _git_fixture(directory, "init", "-q")
    top = _git_fixture(directory, "rev-parse", "--show-toplevel").strip()
    if os.path.realpath(top) != os.path.realpath(directory):
        raise RuntimeError(f"fixture toplevel {top!r} != {directory!r}")
    contents = {}
    for index, path in enumerate(paths):
        contents[path] = TRUE_SOURCE if path not in set(FROZEN_POPULATION[12:]) else FALSE_SOURCE
    for path in drop or ():
        contents.pop(path, None)
    for path, blob in contents.items():
        full = os.path.join(directory, *path.split("/"))
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as handle:
            handle.write(blob)
    rows = fixture_rows(list(paths))
    rows.extend(extra_rows)
    with open(os.path.join(directory, "SKILL.md"), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(fixture_skill(rows))
    _git_fixture(directory, "add", "-A")
    _git_fixture(
        directory,
        "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
        "-c", "commit.gpgsign=false", "commit", "-q", "-m", "fixture",
    )
    return directory, _git_fixture(directory, "rev-parse", "HEAD").strip()


def run_cli(*args):
    proc = subprocess.run(
        [sys.executable, "-B", os.path.abspath(__file__), *args],
        capture_output=True, text=True,
    )
    fields = {}
    for line in proc.stdout.splitlines():
        if line.startswith("C2v1 "):
            fields = dict(re.findall(r"(\w+)=(\S+)", line))
            break
    return proc.returncode, fields, proc.stdout + proc.stderr


def selftest(work):
    work = os.path.abspath(work)
    try:
        os.makedirs(work, exist_ok=True)
    except OSError as exc:
        raise Unevaluable(f"cannot create --work {work}: {exc}") from None
    parent = tempfile.mkdtemp(prefix="fx-", dir=work)
    results = []

    def record(name, ok, detail=""):
        results.append(ok)
        print(f"selftest: {'ok' if ok else 'FAIL'} {name}" + ("" if ok else f" :: {detail}"))

    def check(name, repo, rev, want_rc, want, needles=()):
        code, fields, output = run_cli("--root", repo, "--revision", rev, "--check")
        ok = code == want_rc and all(fields.get(key) == value for key, value in want.items())
        ok = ok and all(needle in output for needle in needles)
        record(name, ok, f"rc={code} fields={fields} want=({want_rc}, {want}) need={needles}\n{output}")
        return code, fields, output

    def write(repo, rev):
        return run_cli("--root", repo, "--revision", rev, "--write", "--date", "2026-11-03")

    def commit_paths(repo, paths, message):
        _git_fixture(repo, "add", *paths)
        _git_fixture(
            repo,
            "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
            "-c", "commit.gpgsign=false", "commit", "-q", "-m", message,
        )
        return _git_fixture(repo, "rev-parse", "HEAD").strip()

    def mutate(repo, change, message):
        path = os.path.join(repo, *RECEIPT_PATH.split("/"))
        with open(path, encoding="ascii") as handle:
            document = json.load(handle)
        change(document)
        with open(path, "w", encoding="ascii", newline="\n") as handle:
            handle.write(json.dumps(document, indent=2, ensure_ascii=True) + "\n")
        return commit_paths(repo, [RECEIPT_PATH], message)

    frozen = list(FROZEN_POPULATION)
    try:
        # green: write twice (idempotent), commit, check at the carrier commit
        green, green_subject = make_fixture(parent, "green", frozen)
        first = write(green, green_subject)
        receipt_file = os.path.join(green, *RECEIPT_PATH.split("/"))
        with open(receipt_file, "rb") as handle:
            bytes_one = handle.read()
        second = write(green, green_subject)
        with open(receipt_file, "rb") as handle:
            bytes_two = handle.read()
        carrier = commit_paths(green, [RECEIPT_PATH], "receipt")
        code, fields, output = run_cli("--root", green, "--revision", carrier, "--check")
        emitted = run_cli("--root", green, "--revision", green_subject, "--emit-population")
        emitted_paths = [line for line in emitted[2].splitlines() if line and not line.startswith(" ")]
        record(
            "green: write, idempotent rewrite, committed, check at carrier, emit-population",
            first[0] == 0 and second[0] == 0 and bytes_one == bytes_two
            and code == 0
            and fields.get("population") == "16" and fields.get("bound") == "16"
            and fields.get("mismatches") == "0" and fields.get("met") == "true"
            and "source=committed" in output and "worktree=identical" in output
            and emitted[0] == 0 and emitted_paths == sorted(frozen),
            f"write_rc={first[0]}/{second[0]} idempotent={bytes_one == bytes_two} "
            f"check_rc={code} fields={fields} emit_rc={emitted[0]} emitted={len(emitted_paths)}\n"
            f"{first[2]}{second[2]}{output}{emitted[2]}",
        )

        # missing receipt at the measured revision and in the worktree
        missing_repo, missing_rev = make_fixture(parent, "missing-receipt", frozen)
        check(
            "missing receipt: bound=0 mismatches=16", missing_repo, missing_rev, 1,
            {"population": "16", "bound": "0", "mismatches": "16", "met": "false"},
            ["source=none"],
        )

        # uncommitted receipt: the worktree copy is ignored
        uncommitted_repo, uncommitted_rev = make_fixture(parent, "uncommitted-receipt", frozen)
        write(uncommitted_repo, uncommitted_rev)
        check(
            "uncommitted receipt: ignored, bound=0 mismatches=16",
            uncommitted_repo, uncommitted_rev, 1,
            {"population": "16", "bound": "0", "mismatches": "16", "met": "false"},
            ["source=uncommitted", "worktree=only-worktree"],
        )

        # wrong digest
        digest_repo, digest_subject = make_fixture(parent, "wrong-digest", frozen)
        write(digest_repo, digest_subject)
        def flip_sha(document):
            entry = document["files"][0]
            entry["sha256"] = ("0" if entry["sha256"][0] != "0" else "1") + entry["sha256"][1:]
        digest_carrier = mutate(digest_repo, flip_sha, "receipt wrong digest")
        check(
            "wrong digest: bound=15 mismatches=1", digest_repo, digest_carrier, 1,
            {"population": "16", "bound": "15", "mismatches": "1", "met": "false"},
            ["finding: digest "],
        )

        # wrong byte count
        bytes_repo, bytes_subject = make_fixture(parent, "wrong-bytes", frozen)
        write(bytes_repo, bytes_subject)
        def bump_bytes(document):
            document["files"][1]["bytes"] += 1
        bytes_carrier = mutate(bytes_repo, bump_bytes, "receipt wrong bytes")
        check(
            "wrong byte count: bound=15 mismatches=1", bytes_repo, bytes_carrier, 1,
            {"population": "16", "bound": "15", "mismatches": "1", "met": "false"},
            ["finding: bytes "],
        )

        # wrong mode flag
        mode_repo, mode_subject = make_fixture(parent, "wrong-mode", frozen)
        write(mode_repo, mode_subject)
        def flip_mode(document):
            target = next(entry for entry in document["files"] if entry["selftest_mode"])
            target["selftest_mode"] = False
        mode_carrier = mutate(mode_repo, flip_mode, "receipt wrong mode")
        check(
            "wrong mode flag: bound=15 mismatches=1", mode_repo, mode_carrier, 1,
            {"population": "16", "bound": "15", "mismatches": "1", "met": "false"},
            ["finding: mode-flag "],
        )

        # duplicate path
        dup_repo, dup_subject = make_fixture(parent, "duplicate-path", frozen)
        write(dup_repo, dup_subject)
        def duplicate(document):
            document["files"].append(dict(document["files"][0]))
        dup_carrier = mutate(dup_repo, duplicate, "receipt duplicate")
        check(
            "duplicate path: bound=15 mismatches=1, class duplicate",
            dup_repo, dup_carrier, 1,
            {"population": "16", "bound": "15", "mismatches": "1", "met": "false"},
            ["finding: duplicate "],
        )

        # path outside the population: reported separately, not counted toward bound
        outside_repo, outside_subject = make_fixture(parent, "outside-population", frozen)
        write(outside_repo, outside_subject)
        def add_outside(document):
            document["files"].append({
                "path": "scripts/fixture_outside.py",
                "sha256": "0" * 64,
                "bytes": 0,
                "selftest_mode": False,
            })
            document["files"].sort(key=lambda entry: entry["path"])
        outside_carrier = mutate(outside_repo, add_outside, "receipt outside")
        check(
            "path outside population: reported separately, bound=16 mismatches=0",
            outside_repo, outside_carrier, 0,
            {"population": "16", "bound": "16", "mismatches": "0", "met": "true"},
            ["outside: scripts/fixture_outside.py"],
        )

        # declared revision of another commit, with one population blob changed since
        stale_repo, stale_subject = make_fixture(parent, "other-revision-stale", frozen)
        write(stale_repo, stale_subject)
        with open(os.path.join(stale_repo, *frozen[0].split("/")), "ab") as handle:
            handle.write(b"# changed after the receipt was written\n")
        stale_carrier = commit_paths(stale_repo, [frozen[0], RECEIPT_PATH], "changed and receipt")
        check(
            "declared revision of another commit, changed blob: bound=15 mismatches=1",
            stale_repo, stale_carrier, 1,
            {"population": "16", "bound": "15", "mismatches": "1", "met": "false"},
            ["finding: digest ", "declared_valid=true", "declared_match=false"],
        )

        # the receipt committed one commit after the revision it declares
        same_repo, same_subject = make_fixture(parent, "other-revision-identical", frozen)
        write(same_repo, same_subject)
        same_carrier = commit_paths(same_repo, [RECEIPT_PATH], "receipt")
        os.remove(os.path.join(same_repo, *RECEIPT_PATH.split("/")))
        check(
            "receipt committed after its declared revision: unchanged bytes bind",
            same_repo, same_carrier, 0,
            {"population": "16", "bound": "16", "mismatches": "0", "met": "true"},
            ["source=committed", "worktree=absent", "declared_valid=true", "declared_match=false"],
        )

        # declared revision that does not resolve
        bad_rev_repo, bad_rev_subject = make_fixture(parent, "revision-nonexistent", frozen)
        write(bad_rev_repo, bad_rev_subject)
        def missing_revision(document):
            document["revision"] = "f" * 40
        bad_rev_carrier = mutate(bad_rev_repo, missing_revision, "receipt bad revision")
        check(
            "declared revision that does not resolve: receipt_revision_invalid, bound=0",
            bad_rev_repo, bad_rev_carrier, 1,
            {"population": "16", "bound": "0", "mismatches": "16", "met": "false"},
            ["finding: receipt_revision_invalid ", "does not resolve"],
        )

        # declared revision that resolves but is not an ancestor of the measured revision
        side_repo, side_subject = make_fixture(parent, "revision-not-ancestor", frozen)
        write(side_repo, side_subject)
        side = _git_fixture(
            side_repo,
            "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
            "-c", "commit.gpgsign=false", "commit-tree", side_subject + "^{tree}", "-m", "side",
        ).strip()
        def unrelated_revision(document):
            document["revision"] = side
        side_carrier = mutate(side_repo, unrelated_revision, "receipt unrelated revision")
        check(
            "declared revision not an ancestor: receipt_revision_invalid, bound=0",
            side_repo, side_carrier, 1,
            {"population": "16", "bound": "0", "mismatches": "16", "met": "false"},
            ["finding: receipt_revision_invalid ", "is not an ancestor"],
        )

        # fabricated receipt: 16 paths, digests that do not re-derive
        fab_repo, fab_subject = make_fixture(parent, "fabricated", frozen)
        path = os.path.join(fab_repo, *RECEIPT_PATH.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="ascii", newline="\n") as handle:
            handle.write(json.dumps({
                "schema": SCHEMA,
                "revision": fab_subject,
                "date": "2026-11-03",
                "host": host_string(),
                "files": [
                    {"path": item, "sha256": "0" * 64, "bytes": 0, "selftest_mode": False}
                    for item in frozen
                ],
            }, indent=2, ensure_ascii=True) + "\n")
        fab_carrier = commit_paths(fab_repo, [RECEIPT_PATH], "fabricated receipt")
        check(
            "fabricated receipt (16 paths): bound=0 mismatches=16",
            fab_repo, fab_carrier, 1,
            {"population": "16", "bound": "0", "mismatches": "16", "met": "false"},
            ["finding: digest "],
        )

        # a live row beyond the frozen 16 is in-population
        grown = frozen + [".ufo/waves/round-99/c99_extra.py"]
        grown_repo, grown_subject = make_fixture(parent, "grown", grown)
        write(grown_repo, grown_subject)
        grown_carrier = commit_paths(grown_repo, [RECEIPT_PATH], "receipt 17")
        check(
            "live row beyond the frozen 16: population=17 bound=17",
            grown_repo, grown_carrier, 0,
            {"population": "17", "bound": "17", "mismatches": "0", "met": "true"},
            ["beyond_frozen=1"],
        )

        # a frozen path that the derivation no longer produces
        shifted = frozen[1:] + [".ufo/waves/round-99/c99_replacement.py"]
        short_repo, short_subject = make_fixture(parent, "missing-frozen", shifted)
        write(short_repo, short_subject)
        short_carrier = commit_paths(short_repo, [RECEIPT_PATH], "receipt missing frozen")
        check(
            "missing_frozen=1 keeps met=false with bound=16 mismatches=0",
            short_repo, short_carrier, 1,
            {"population": "16", "bound": "16", "mismatches": "0", "met": "false"},
            ["missing_frozen=1"],
        )

        # classifier unit checks (docstrings and argv lists never count)
        classifier = [
            (TRUE_SOURCE, True),
            (FALSE_SOURCE, False),
            (b'"""docstring mentions --selftest only"""\n', False),
            (b'import subprocess\nsubprocess.run(["node", "x.mjs", "--selftest"])\n', False),
            (b'import sys\nif "--selftest" in sys.argv:\n    pass\n', True),
            (b'def f(value):\n    return value == "--selftest"\n', True),
            (b"parser.add_argument('--seed')\n", False),
            (b"if (process.argv.includes('--selftest')) {}\n", True),
            (b"// --selftest is handled elsewhere\n", False),
        ]
        outcomes = []
        for source, want in classifier:
            suffix = ".mjs" if source.startswith(b"if (") or source.startswith(b"//") else ".py"
            got, _note = selftest_registration("fixture" + suffix, source)
            outcomes.append(got == want)
        unparsable, _note = selftest_registration("fixture.py", b"def broken(:\n")
        outcomes.append(unparsable is None)
        record("classifier: add_argument, comparisons, docstrings, argv lists, .mjs", all(outcomes), str(outcomes))

        # usage: --write without --date, --selftest without --work
        code, _fields, output = run_cli("--root", green, "--revision", green_subject, "--write")
        code_work, _fields2, output_work = run_cli("--selftest")
        record(
            "usage: --write without --date exits 64, --selftest without --work exits 64",
            code == 64 and code_work == 64 and "64 usage" in output and "64 usage" in output_work,
            f"rc={code}/{code_work}\n{output}{output_work}",
        )
    finally:
        print(f"selftest: fixtures under {parent}")

    passed, total = sum(1 for ok in results if ok), len(results)
    print(f"selftest: {passed}/{total}")
    return 0 if passed == total else 1


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def parse_date(value):
    if not DATE_RE.match(value):
        raise Usage(f"--date {value!r} is not YYYY-MM-DD")
    try:
        dt.date.fromisoformat(value)
    except ValueError as exc:
        raise Usage(f"--date {value!r} is not a calendar date: {exc}") from None
    return value


def main(argv=None):
    parser = Parser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".")
    parser.add_argument("--revision", default=None, help="default: master tip")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="verify the receipt (default)")
    group.add_argument("--write", action="store_true", help="write the receipt")
    group.add_argument("--selftest", action="store_true", help="run isolated fixtures under --work")
    group.add_argument("--emit-population", action="store_true", help="print the derived population")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD; required with --write")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--work", default=None, help="scratch directory for --selftest")
    args = parser.parse_args(argv)

    if args.selftest:
        try:
            if not args.work:
                raise Usage("--selftest requires --work <dir>")
            return selftest(args.work)
        except Usage as exc:
            print(f"64 usage: {exc}", file=sys.stderr)
            return 64
        except Unevaluable as exc:
            print(f"2 unevaluable: {exc}", file=sys.stderr)
            return 2

    root = os.path.abspath(args.root)
    try:
        require_toplevel(root)
        revision = resolve_revision(root, args.revision or "master")
        if args.write:
            if not args.date:
                raise Usage("--write requires --date YYYY-MM-DD")
            return write_receipt(root, revision, parse_date(args.date), args.json)
        if args.emit_population:
            population = derive_population(read_skill(root, revision))
            missing = [path for path in FROZEN_POPULATION if path not in set(population)]
            if args.json:
                print(json.dumps({
                    "revision": revision,
                    "population": population,
                    "frozen_size": len(FROZEN_POPULATION),
                    "missing_frozen": missing,
                    "beyond_frozen": [path for path in population if path not in set(FROZEN_POPULATION)],
                }, indent=2, sort_keys=True))
            else:
                for path in population:
                    print(path)
            for path in missing:
                print(f"warning: frozen path {path} is missing at {revision}", file=sys.stderr)
            return 0
        result = evaluate(root, revision)
        report(result, args.json)
        return 0 if result["met"] else 1
    except Usage as exc:
        print(f"64 usage: {exc}", file=sys.stderr)
        return 64
    except Unevaluable as exc:
        print(f"2 unevaluable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
