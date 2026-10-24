#!/usr/bin/env python3
"""Range-aware citing-set completeness gate for the kake corpus (round 27, C2).

Interface (frozen by .ufo/waves/round-27/contract.json):

    python3 -B scripts/citing_set.py --root <dir> [--revision <commit>] \
        --population <relative-json> --ledger <relative-json> [--json]
    python3 -B scripts/citing_set.py --selftest [extra args]

The gate enumerates the complete expanded citing set of the corpus and
compares it with the adjudication ledger.  Every regular file under
``corpus/knowledge`` is read whole: front-matter metadata lines and the
historical / round-26 EOF prose are part of the citing set, exactly like
in-body citations.  Only pair-level presence is measured; a pair being
present says nothing about the truth of the statement it carries.

Citation form
-------------
A citation token is ``S`` followed by at least three ASCII digits, with no
word character immediately before the ``S`` and none immediately after the
digits.  Tokens are recognised anywhere in the file text.

A range is two ids joined by one of: hyphen-minus, en dash (U+2013),
em dash (U+2014), ``..``, ``to`` or ``through``.  Any whitespace, newlines
included, may sit around the separator, and the separator may abut the
digits (``S001toS006`` is a range).  The left endpoint only needs a word
boundary before its ``S``; the right endpoint needs a word boundary after
its digits.  Ranges are scanned independently of the literal token rule.
A range expands to every id between its endpoints, inclusive.

Population
----------
Only ids present in the population document are part of the citing set.
Ids are compared numerically (``S001`` and ``S0001`` are the same id).  A
population id that the citation grammar can never produce is unreachable
and the population is rejected with ``input_invalid``
(``population_id_unreachable``) instead of being measured clean.  The
grammar produces exactly ``S`` followed by at least three ASCII digits
(``^S[0-9]{3,}$``, the token rule above), so a population id that does
not match that pattern -- ``S1``, ``S01``, ``X001``, ``s001`` -- is
unreachable.  Ids cited outside the population are counted
(``outsidePopulation``) but never become findings.

Accepted JSON profile
---------------------
The population and ledger documents must be UTF-8 JSON objects.  The
parser accepts the ordinary JSON grammar and rejects two shapes that
plain ``json.loads`` would silently accept:

* a member name that repeats inside one JSON object, at any depth
  (``{"rows": [], "rows": []}``), is rejected as ``input_invalid`` with
  reason ``document_duplicate_key`` -- the later member would otherwise
  silently replace the earlier one;
* a non-finite number (``NaN``, ``Infinity``, ``-Infinity``), at any
  depth, is rejected as ``input_invalid`` with reason
  ``document_nonfinite_number`` -- those literals are not JSON, and a
  non-finite value cannot be adjudicated.  A number literal outside the
  finite double range (``1e999``) is refused the same way.

Both reasons are decided while the document is parsed, before any shape
check, so a document that is both malformed in shape and duplicated or
non-finite reports the duplicate or non-finite reason.

Usage
-----
Each valued option (``--root``, ``--revision``, ``--population``,
``--ledger``) may be given at most once.  A repeated option -- in the
``--name value`` form, the ``--name=value`` form, or a mix of the two
spellings, including the abbreviated spellings argparse accepts, such as
``--rev x --revision HEAD`` -- is a usage error: the gate writes its
usual JSON usage object to stdout and exits 64 instead of silently
keeping the last value.  A single occurrence of an option, abbreviated
or not, is read exactly as before.

Findings
--------
``unadjudicated_citing_pair``
    One per expanded citing pair (row, file) that the ledger does not
    contain.  ``row`` is the population id, ``file`` the corpus-relative
    path.  This is the red condition of the gate.
``ledger_pair_not_cited``
    One per distinct ledger pair (row, file) that the citing set does not
    contain.
``ledger_duplicate_pair``
    One per distinct ledger pair that occurs more than once; ``occurrences``
    reports how often it was seen.  A duplicated pair still counts as
    adjudicated.
``citation_range_invalid``
    One per range that is descending (end < start) or spans more than 200
    ids.  An invalid range is not expanded; its endpoints remain literal
    citations.  The evaluation still completes, so this finding yields the
    ``failed`` verdict (exit 1).
``input_invalid``
    One per unusable input: missing, unreadable or non-regular document
    (a FIFO or device is refused without blocking), malformed or too
    deeply nested JSON, a JSON object that repeats a member name
    (``document_duplicate_key``), a JSON document that carries a
    non-finite number (``document_nonfinite_number``), wrong document
    shape, unreachable population id,
    unreadable corpus file, symlinked or non-regular corpus entry, path
    that resolves outside the root, a ``corpus/knowledge`` surface that is
    absent, empty or not a directory, a blank or unknown ``--revision``,
    a ``--revision`` root that is not the top level of its Git repository
    (a bare repository or the repository's own ``.git`` directory reads
    that repository's HEAD tree and is accepted), and Git being
    unavailable.  Git subprocesses run without inherited repository-locating
    variables (``GIT_DIR``, ``GIT_WORK_TREE`` and the other
    ``git rev-parse --local-env-vars`` names), so ``--root`` alone chooses
    the repository.  Any ``input_invalid`` finding forces verdict
    ``could-not-evaluate`` (exit 2), so an absent or unreachable corpus
    surface never measures ``clean``.

Exit codes
----------
0 clean, 1 failed (findings present), 2 could-not-evaluate, 64 usage.
64 covers an unknown or missing option and a repeated valued option.

Safety
------
The corpus walk is iterative, so a deeply nested corpus directory is
measured instead of raising ``RecursionError``.  Every document is opened
with ``O_NONBLOCK`` and ``O_NOCTTY``, so opening a terminal device as an
input document is refused as ``document_not_regular_file`` and never
makes the gate's process the controlling terminal of that device.

Finding multiplicity
--------------------
One finding per distinct object: one ``unadjudicated_citing_pair`` per
distinct (row, file) of the expanded citing set, one
``ledger_pair_not_cited`` and one ``ledger_duplicate_pair`` per distinct
ledger pair (a pair repeated three times still yields one duplicate
finding, carrying ``occurrences``).

The JSON document is written to stdout in every mode:
``{"verdict":..., "citingPairs":int, "ledgerPairs":int, "findings":[...]}``.
No network access, no execution of corpus content, no writes outside this
process.  ``--selftest`` delegates to the sibling runner
``scripts/citing_set_selftest.py`` with an explicit root.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import stat
import subprocess
import sys

EXIT_CLEAN = 0
EXIT_FAILED = 1
EXIT_CANNOT_EVALUATE = 2
EXIT_USAGE = 64

F_UNADJUDICATED = "unadjudicated_citing_pair"
F_LEDGER_NOT_CITED = "ledger_pair_not_cited"
F_LEDGER_DUPLICATE = "ledger_duplicate_pair"
F_INPUT_INVALID = "input_invalid"
F_RANGE_INVALID = "citation_range_invalid"
F_DUPLICATE_KEY = "document_duplicate_key"
F_NONFINITE_NUMBER = "document_nonfinite_number"

CORPUS_DIR = "corpus/knowledge"
GIT_LOCAL_ENV = ("GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_CONFIG", "GIT_CONFIG_PARAMETERS", "GIT_CONFIG_COUNT",
                 "GIT_OBJECT_DIRECTORY", "GIT_DIR", "GIT_WORK_TREE", "GIT_IMPLICIT_WORK_TREE", "GIT_GRAFT_FILE",
                 "GIT_INDEX_FILE", "GIT_NO_REPLACE_OBJECTS", "GIT_REPLACE_REF_BASE", "GIT_PREFIX",
                 "GIT_SHALLOW_FILE", "GIT_COMMON_DIR")
GIT_SUBPROCESS_ENV = {k: v for k, v in os.environ.items() if k not in GIT_LOCAL_ENV}
MAX_RANGE_SPAN = 200
SELFTEST_NAME = "citing_set_selftest.py"

# A citation token: "S" + >=3 ASCII digits, delimited by non-word characters.
_TOKEN_RE = re.compile(r"(?<!\w)S([0-9]{3,})(?!\w)")
# A citation range: two ids joined by one declared separator.  Any
# whitespace (newlines included) may surround the separator and the
# separator may abut the digits ("S001toS006" is a range).  The left
# endpoint only needs a word boundary before its "S"; the right endpoint
# needs a word boundary after its digits.  Scanned independently of the
# literal token rule, as the declared grammar requires.
_RANGE_RE = re.compile(r"\bS([0-9]{3,})\s*(?:-|–|—|\.\.|through|to)\s*S([0-9]{3,})\b")
# Ids that are numerically comparable (S001 == S0001).
_NUMERIC_ID_RE = re.compile(r"^S([0-9]+)$")
# The population ids the citation grammar can produce: the scanner's own
# token rule.  Anything else is unreachable (population_id_unreachable).
# fullmatch is used, not match, so a trailing newline ("S001\n") is
# refused instead of being read as "S001".
_POPULATION_ID_RE = re.compile(r"S[0-9]{3,}")


class InputInvalid(Exception):
    """An input the gate cannot evaluate safely."""

    def __init__(self, reason, path=None, scope=None, **detail):
        super().__init__(reason)
        self.reason = reason
        self.path = path
        self.scope = scope
        self.detail = detail

    def as_finding(self):
        finding = {"id": F_INPUT_INVALID, "reason": self.reason}
        if self.scope is not None:
            finding["scope"] = self.scope
        if self.path is not None:
            finding["path"] = self.path
        for key in sorted(self.detail):
            if self.detail[key] is not None:
                finding[key] = self.detail[key]
        return finding


# --------------------------------------------------------------------------
# identifiers and path helpers
# --------------------------------------------------------------------------


def id_key(value):
    """Comparable key for a row id.

    ``S001`` and ``S0001`` share the key ``("n", 1)``; anything else keeps
    its exact text so that unrelated ids never collide.
    """
    match = _NUMERIC_ID_RE.match(value) if isinstance(value, str) else None
    if match is not None:
        return ("n", int(match.group(1)))
    return ("s", value)


def normalize_relative(value, label):
    """Validate a caller-supplied relative path and normalise it."""
    if not isinstance(value, str) or not value.strip():
        raise InputInvalid("empty_path", None, "argument", argument=label)
    text = value.replace("\\", "/").strip()
    if text.startswith("/"):
        raise InputInvalid("absolute_path_not_allowed", value, "argument", argument=label)
    parts = [part for part in text.split("/") if part not in ("", ".")]
    if any(part == ".." for part in parts):
        raise InputInvalid("path_escapes_root", value, "argument", argument=label)
    if not parts:
        raise InputInvalid("empty_path", value, "argument", argument=label)
    return "/".join(parts)


def normalize_ledger_file(value):
    """Normalise a ledger file reference for comparison with corpus paths."""
    if not isinstance(value, str):
        return ""
    text = value.replace("\\", "/").strip()
    while text.startswith("./"):
        text = text[2:]
    return text


def is_inside(root, candidate):
    root_real = os.path.realpath(str(root))
    candidate_real = os.path.realpath(str(candidate))
    if candidate_real == root_real:
        return True
    return candidate_real.startswith(root_real + os.sep)


# --------------------------------------------------------------------------
# corpus sources
# --------------------------------------------------------------------------


class WorkingTreeSource:
    """Reads documents from a working tree below ``root``."""

    mode = "working-tree"

    def __init__(self, root):
        self.root = root

    def read_document(self, relative):
        target = os.path.join(str(self.root), relative)
        if not is_inside(self.root, target):
            raise InputInvalid("path_escapes_root", relative, "document")
        # Open without blocking and check the opened object: a FIFO or a
        # device must be refused as unusable input, never waited on.
        # O_NOCTTY keeps the open device from becoming the controlling
        # terminal of this process.
        flags = (
            os.O_RDONLY
            | getattr(os, "O_NONBLOCK", 0)
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOCTTY", 0)
        )
        try:
            descriptor = os.open(target, flags)
        except OSError as exc:
            raise InputInvalid(
                "document_unreadable", relative, "document", detail=exc.strerror or type(exc).__name__
            )
        try:
            if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                raise InputInvalid("document_not_regular_file", relative, "document")
            with os.fdopen(descriptor, "rb") as handle:
                descriptor = None
                return handle.read()
        except OSError as exc:
            raise InputInvalid(
                "document_unreadable", relative, "document", detail=exc.strerror or type(exc).__name__
            )
        finally:
            if descriptor is not None:
                os.close(descriptor)

    def corpus_files(self):
        base = os.path.join(str(self.root), CORPUS_DIR)
        try:
            info = os.lstat(base)
        except FileNotFoundError:
            raise InputInvalid("corpus_directory_missing", CORPUS_DIR, "corpus")
        except OSError as exc:
            raise InputInvalid(
                "corpus_directory_unreadable",
                CORPUS_DIR,
                "corpus",
                detail=exc.strerror or type(exc).__name__,
            )
        if stat.S_ISLNK(info.st_mode):
            raise InputInvalid("symlink_rejected", CORPUS_DIR, "corpus")
        if not stat.S_ISDIR(info.st_mode):
            raise InputInvalid("not_a_directory", CORPUS_DIR, "corpus")
        found = []
        # Iterative depth-first walk.  A corpus nested thousands of levels
        # deep must be measured, not raise RecursionError, so the walk
        # keeps its own stack of directory frames instead of recursing.
        stack = [[base, self._scan_entries(base), 0]]
        while stack:
            frame = stack[-1]
            entries = frame[1]
            index = frame[2]
            descended = False
            while index < len(entries):
                entry = entries[index]
                index += 1
                frame[2] = index
                relative = os.path.relpath(entry.path, str(self.root)).replace(os.sep, "/")
                if entry.is_symlink():
                    raise InputInvalid("symlink_rejected", relative, "corpus")
                if entry.is_dir(follow_symlinks=False):
                    stack.append([entry.path, self._scan_entries(entry.path), 0])
                    descended = True
                    break
                if entry.is_file(follow_symlinks=False):
                    found.append(relative)
                    continue
                raise InputInvalid("not_a_regular_file", relative, "corpus")
            if not descended:
                stack.pop()
        if not found:
            raise InputInvalid("corpus_empty", CORPUS_DIR, "corpus")
        return sorted(found)

    def _scan_entries(self, directory):
        """Return the sorted entries of one directory, refusing unreadable ones."""
        try:
            with os.scandir(directory) as scan:
                entries = sorted(scan, key=lambda entry: entry.name)
        except OSError as exc:
            relative = os.path.relpath(directory, str(self.root)).replace(os.sep, "/")
            raise InputInvalid(
                "corpus_directory_unreadable",
                relative,
                "corpus",
                detail=exc.strerror or type(exc).__name__,
            )
        return entries


class GitSource:
    """Reads documents as Git blobs at one resolved commit."""

    mode = "git"

    def __init__(self, root, revision):
        self.root = root
        self.revision = self._resolve(root, revision)
        self._require_top_level(root)

    @staticmethod
    def _require_top_level(root):
        """Refuse a root nested inside a repository: Git paths are top-relative.

        ``--show-prefix`` is empty at a work-tree top level and inside a bare
        repository, and names the subdirectory otherwise; comparing prefixes
        avoids realpath and whitespace-stripping mismatches on legitimate roots.
        """
        try:
            done = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "--show-prefix"],
                env=GIT_SUBPROCESS_ENV,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except OSError as exc:
            raise InputInvalid("git_unavailable", None, "revision", detail=type(exc).__name__)
        if done.returncode != 0 or done.stdout.rstrip(b"\n"):
            raise InputInvalid("root_not_repository_top_level", str(root), "root")

    @staticmethod
    def _resolve(root, revision):
        if not isinstance(revision, str) or not revision.strip():
            raise InputInvalid("revision_not_found", revision, "revision")
        try:
            done = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "--verify", "--quiet", revision + "^{commit}"],
                env=GIT_SUBPROCESS_ENV,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except OSError as exc:
            raise InputInvalid("git_unavailable", revision, "revision", detail=type(exc).__name__)
        if done.returncode != 0:
            raise InputInvalid("revision_not_found", revision, "revision")
        return done.stdout.decode("utf-8", "replace").strip()

    def _git(self, arguments):
        try:
            done = subprocess.run(
                ["git", "-C", str(self.root)] + arguments,
                env=GIT_SUBPROCESS_ENV,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except OSError as exc:
            raise InputInvalid("git_unavailable", None, "revision", detail=type(exc).__name__)
        if done.returncode != 0:
            raise InputInvalid("git_command_failed", None, "revision", command=" ".join(arguments[:3]))
        return done.stdout

    def read_document(self, relative):
        return self._git(["show", self.revision + ":" + relative])

    def corpus_files(self):
        raw = self._git(["ls-tree", "-rz", self.revision, "--", CORPUS_DIR])
        files = []
        # NUL framing preserves Git paths containing tabs, newlines or Unicode.
        for record in raw.split(b"\0"):
            if not record:
                continue
            meta, separator, encoded_path = record.partition(b"\t")
            path = os.fsdecode(encoded_path)
            fields = meta.decode("ascii", "replace").split()
            if not separator or len(fields) < 2:
                raise InputInvalid("not_a_regular_file", path or None, "corpus")
            mode, kind = fields[0], fields[1]
            if mode == "120000":
                raise InputInvalid("symlink_rejected", path or None, "corpus")
            if kind != "blob" or mode == "160000":
                raise InputInvalid("not_a_regular_file", path or None, "corpus")
            if path == CORPUS_DIR:
                raise InputInvalid("not_a_directory", CORPUS_DIR, "corpus")
            files.append(path)
        if not files:
            raise InputInvalid("corpus_directory_missing", CORPUS_DIR, "corpus")
        return sorted(files)


# --------------------------------------------------------------------------
# citation scanning
# --------------------------------------------------------------------------


def scan_text(text):
    """Return the citation tokens and the ranges found in one document.

    Literals and ranges are scanned independently: a range is recognised by
    the declared separator grammar, not by the standalone-token rule, so
    ``S001toS006`` and a range broken across lines are both ranges.
    """
    tokens = [match.group(0) for match in _TOKEN_RE.finditer(text)]
    ranges = [
        (int(match.group(1)), int(match.group(2)), match.group(0))
        for match in _RANGE_RE.finditer(text)
    ]
    return tokens, ranges


# --------------------------------------------------------------------------
# documents
# --------------------------------------------------------------------------


class _DuplicateMember(Exception):
    """A JSON object repeated a member name."""

    def __init__(self, member):
        super().__init__(member)
        self.member = member


class _NonfiniteNumber(Exception):
    """A JSON document carried a non-finite number."""

    def __init__(self, literal):
        super().__init__(literal)
        self.literal = literal


def _reject_duplicate_members(pairs):
    """object_pairs_hook: refuse a member name that repeats in one object.

    Plain ``json.loads`` keeps the last member and drops the earlier one,
    so a document like ``{"rows": [], "rows": []}`` would be read as the
    second member alone.  The hook sees every object of the document,
    at any depth, before the shape checks run.
    """
    members = {}
    for name, value in pairs:
        if name in members:
            raise _DuplicateMember(name)
        members[name] = value
    return members


def _reject_nonfinite(literal):
    """parse_constant: refuse the non-JSON literals NaN, Infinity, -Infinity."""
    raise _NonfiniteNumber(literal)


def _finite(literal):
    """parse_float: refuse a number literal outside the finite double range.

    ``1e999`` parses as an infinity in IEEE double arithmetic; a document
    that carries such a value cannot be adjudicated, so it is refused
    like the ``Infinity`` literal.
    """
    number = float(literal)
    if not math.isfinite(number):
        raise _NonfiniteNumber(literal)
    return number


def _first_nonfinite(value):
    """Return the first non-finite float inside a parsed document, or None.

    The walk is iterative, so a deeply nested document cannot raise
    ``RecursionError`` here either.
    """
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, float):
            if not math.isfinite(item):
                return item
            continue
        if isinstance(item, dict):
            stack.extend(item.values())
            continue
        if isinstance(item, list):
            stack.extend(item)
    return None


def load_json_document(raw, relative, scope):
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise InputInvalid("document_not_utf8", relative, scope)
    try:
        document = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_members,
            parse_constant=_reject_nonfinite,
            parse_float=_finite,
        )
    except _DuplicateMember as exc:
        raise InputInvalid(F_DUPLICATE_KEY, relative, scope, member=exc.member)
    except _NonfiniteNumber as exc:
        raise InputInvalid(F_NONFINITE_NUMBER, relative, scope, literal=exc.literal)
    except (ValueError, RecursionError, MemoryError) as exc:
        raise InputInvalid("document_not_json", relative, scope, detail=(str(exc) or type(exc).__name__)[:120])
    if not isinstance(document, dict):
        raise InputInvalid("document_shape_invalid", relative, scope)
    overflow = _first_nonfinite(document)
    if overflow is not None:
        raise InputInvalid(F_NONFINITE_NUMBER, relative, scope, literal=repr(overflow))
    return document


def load_population(document, relative):
    rows = document.get("rows")
    if not isinstance(rows, list):
        raise InputInvalid("document_shape_invalid", relative, "population")
    mapping = {}
    display = {}
    for row in rows:
        if not isinstance(row, dict):
            raise InputInvalid("document_shape_invalid", relative, "population")
        identifier = row.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            raise InputInvalid("document_shape_invalid", relative, "population")
        if not _POPULATION_ID_RE.fullmatch(identifier):
            raise InputInvalid("population_id_unreachable", relative, "population", row=identifier)
        key = id_key(identifier)
        mapping.setdefault(key, []).append(identifier)
        if key not in display:
            display[key] = identifier
    return mapping, display


def load_ledger(document, relative):
    pairs = document.get("pairs")
    if not isinstance(pairs, list):
        raise InputInvalid("document_shape_invalid", relative, "ledger")
    entries = []
    for pair in pairs:
        if not isinstance(pair, dict):
            raise InputInvalid("document_shape_invalid", relative, "ledger")
        row = pair.get("row")
        name = pair.get("file")
        if not isinstance(row, str) or not row.strip():
            raise InputInvalid("document_shape_invalid", relative, "ledger")
        if not isinstance(name, str) or not name.strip():
            raise InputInvalid("document_shape_invalid", relative, "ledger")
        entries.append((row, normalize_ledger_file(name)))
    return entries


# --------------------------------------------------------------------------
# evaluation
# --------------------------------------------------------------------------


def evaluate(source, population_relative, ledger_relative):
    """Return (result, exit code) for one evaluation."""
    findings = []
    input_errors = []
    range_errors = []

    population_document = load_json_document(
        source.read_document(population_relative), population_relative, "population"
    )
    ledger_document = load_json_document(source.read_document(ledger_relative), ledger_relative, "ledger")
    population, display = load_population(population_document, population_relative)
    ledger_entries = load_ledger(ledger_document, ledger_relative)

    corpus_files = source.corpus_files()

    citing = set()
    outside = set()
    for relative in corpus_files:
        try:
            raw = source.read_document(relative)
        except InputInvalid as exc:
            input_errors.append(exc.as_finding())
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            input_errors.append(
                InputInvalid("corpus_file_not_utf8", relative, "corpus").as_finding()
            )
            continue
        tokens, ranges = scan_text(text)
        for token in tokens:
            key = id_key(token)
            if key in population:
                for identifier in population[key]:
                    citing.add((key, relative))
                    break
            else:
                outside.add((key, relative))
        for start, end, raw_range in ranges:
            if end < start:
                range_errors.append(
                    {
                        "id": F_RANGE_INVALID,
                        "file": relative,
                        "range": raw_range,
                        "start": start,
                        "end": end,
                        "reason": "descending_range",
                    }
                )
                continue
            if end - start > MAX_RANGE_SPAN:
                range_errors.append(
                    {
                        "id": F_RANGE_INVALID,
                        "file": relative,
                        "range": raw_range,
                        "start": start,
                        "end": end,
                        "reason": "span_too_large",
                    }
                )
                continue
            for value in range(start, end + 1):
                key = ("n", value)
                if key in population:
                    citing.add((key, relative))
                else:
                    outside.add((key, relative))

    ledger_keys = [(id_key(row), name) for row, name in ledger_entries]
    ledger_counts = {}
    for key in ledger_keys:
        ledger_counts[key] = ledger_counts.get(key, 0) + 1
    ledger_present = set(ledger_counts)

    for key, relative in sorted(citing):
        if (key, relative) in ledger_present:
            continue
        findings.append(
            {
                "id": F_UNADJUDICATED,
                "row": display.get(key, key[1] if isinstance(key[1], str) else str(key[1])),
                "file": relative,
            }
        )

    for key in sorted(ledger_present):
        if key in citing:
            continue
        row = key[0]
        findings.append(
            {
                "id": F_LEDGER_NOT_CITED,
                "row": display.get(row, row[1] if isinstance(row[1], str) else str(row[1])),
                "file": key[1],
            }
        )

    for key in sorted(ledger_counts):
        count = ledger_counts[key]
        if count < 2:
            continue
        row = key[0]
        findings.append(
            {
                "id": F_LEDGER_DUPLICATE,
                "row": display.get(row, row[1] if isinstance(row[1], str) else str(row[1])),
                "file": key[1],
                "occurrences": count,
            }
        )

    findings.extend(input_errors)
    findings.extend(range_errors)
    findings.sort(key=lambda item: (item.get("id", ""), str(item.get("row", "")), str(item.get("file", ""))))

    if input_errors:
        verdict = "could-not-evaluate"
        code = EXIT_CANNOT_EVALUATE
    elif findings:
        verdict = "failed"
        code = EXIT_FAILED
    else:
        verdict = "clean"
        code = EXIT_CLEAN

    result = {
        "verdict": verdict,
        "citingPairs": len(citing),
        "ledgerPairs": len(ledger_entries),
        "findings": findings,
        "populationRows": sum(len(value) for value in population.values()),
        "corpusFiles": len(corpus_files),
        "outsidePopulation": len(outside),
        "source": source.mode,
    }
    if isinstance(source, GitSource):
        result["revision"] = source.revision
    else:
        result["revision"] = None
    return result, code


# --------------------------------------------------------------------------
# command line
# --------------------------------------------------------------------------


def emit(payload):
    sys.stdout.write(json.dumps(payload, indent=2) + "\n")
    sys.stdout.flush()


class GateParser(argparse.ArgumentParser):
    def error(self, message):
        emit(
            {
                "verdict": "could-not-evaluate",
                "citingPairs": 0,
                "ledgerPairs": 0,
                "findings": [],
                "error": "usage: " + message,
            }
        )
        sys.stderr.write("citing_set.py: " + message + "\n")
        raise SystemExit(EXIT_USAGE)


class StoreOnce(argparse.Action):
    """A valued option that may be given at most once, in any spelling.

    argparse keeps the last value of a repeated option and says nothing,
    so ``--root a --root b`` would silently measure ``b``.  The gate
    refuses the repetition instead: it is a usage error (exit 64) with
    the usual JSON usage object.  The check lives in the action, so it
    also catches a repetition written with an abbreviation
    (``--rev x --revision HEAD``) or with the ``--name=value`` form.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest, None) is not None:
            raise argparse.ArgumentError(
                self, "option %s given more than once" % (option_string or self.dest)
            )
        setattr(namespace, self.dest, values)


def build_parser():
    parser = GateParser(prog="citing_set.py", description="Range-aware citing-set completeness gate.")
    parser.add_argument("--root", action=StoreOnce,
                        help="root directory holding corpus/ and the input documents")
    parser.add_argument("--revision", action=StoreOnce,
                        help="read Git blobs at this revision instead of the working tree")
    parser.add_argument("--population", action=StoreOnce,
                        help="relative path of the population document")
    parser.add_argument("--ledger", action=StoreOnce,
                        help="relative path of the adjudication ledger document")
    parser.add_argument("--json", action="store_true", help="emit JSON (always on)")
    parser.add_argument("--selftest", action="store_true", help="delegate to the sibling selftest runner")
    return parser


def run_selftest(arguments, argv):
    """Delegate to the sibling selftest runner with an explicit root."""
    sibling = os.path.join(os.path.dirname(os.path.abspath(__file__)), SELFTEST_NAME)
    if not os.path.isfile(sibling):
        emit(
            {
                "verdict": "could-not-evaluate",
                "citingPairs": 0,
                "ledgerPairs": 0,
                "findings": [],
                "error": "selftest_runner_missing",
            }
        )
        sys.stderr.write("citing_set.py: missing sibling runner " + SELFTEST_NAME + "\n")
        return EXIT_CANNOT_EVALUATE
    root = arguments.root
    if not root:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root = os.path.abspath(root)
    extra = []
    skip = False
    for item in argv:
        if skip:
            skip = False
            continue
        if item == "--selftest":
            continue
        if item == "--root" or item.startswith("--root="):
            skip = item == "--root"
            continue
        extra.append(item)
    command = [sys.executable, "-B", sibling, "--root", root] + extra
    done = subprocess.run(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if done.returncode != 0 and "unrecognized arguments" in (done.stderr or ""):
        command = [sys.executable, "-B", sibling] + extra
        done = subprocess.run(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if done.stdout:
        sys.stdout.write(done.stdout)
        sys.stdout.flush()
    if done.stderr:
        sys.stderr.write(done.stderr)
        sys.stderr.flush()
    return done.returncode


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    arguments = parser.parse_args(argv)
    if arguments.selftest:
        return run_selftest(arguments, argv)
    missing = [
        name
        for name in ("root", "population", "ledger")
        if not getattr(arguments, name)
    ]
    if missing:
        parser.error("missing required option(s): " + ", ".join("--" + name for name in missing))
    try:
        root = os.path.abspath(arguments.root)
        if not os.path.isdir(root):
            raise InputInvalid("root_not_a_directory", arguments.root, "root")
        population_relative = normalize_relative(arguments.population, "--population")
        ledger_relative = normalize_relative(arguments.ledger, "--ledger")
        if arguments.revision is not None:
            source = GitSource(root, arguments.revision)
        else:
            source = WorkingTreeSource(root)
        result, code = evaluate(source, population_relative, ledger_relative)
    except InputInvalid as exc:
        result = {
            "verdict": "could-not-evaluate",
            "citingPairs": 0,
            "ledgerPairs": 0,
            "findings": [exc.as_finding()],
        }
        code = EXIT_CANNOT_EVALUATE
    emit(result)
    return code


if __name__ == "__main__":
    sys.exit(main())
