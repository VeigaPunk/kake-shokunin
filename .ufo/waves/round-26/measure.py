#!/usr/bin/env python3
"""Revision-bound counter for the round-26 source recheck (C1, freshness).

Usage: measure.py --root ROOT --revision HASH [--selftest]

All inputs are committed bytes at HASH, read through git with user and system
configuration ignored, replace refs disabled and hooks off. A revision without the
population may use the local population file only when its sha256 equals
POPULATION_SHA256. Prints one JSON object (schema kake-source-recheck-v1).

Exit 0: all 32 population rows decided (HOLD or STALE) and no findings.
Exit 1: rows undecided, or findings present.
Exit 2: an input is unavailable or tampered.
Exit 64: usage.
Every population fetch of a row is integrity-checked, not only the receipt's fetchIndex.
Statement ledger findings: statements_absent, statements_invalid, statements_duplicate_pair,
statements_row_outside_population, statement_correction_absent (tags < stale) and
statement_tags_unaccounted (tags != stale + reclassified; reclassified tags are r26 STALE
blocks later judged precision notes, kept because the corpus is append-only).
--selftest exits 0 only when every synthetic fixture yields its expected exit, finding
ids and decided rows (plus statement counters and 32 row records where declared). Its
fixture repositories live under the system temporary directory (TMPDIR), never the lane.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import types
from typing import Any
import zlib

SCHEMA = "kake-source-recheck-v1"
SELFTEST_SCHEMA = "kake-source-recheck-selftest-v1"
EXPECTED = 32
WAVE = ".ufo/waves/round-26"
POPULATION = f"{WAVE}/population.json"
MANIFEST = f"{WAVE}/fetched/manifest.json"
RETRY_MANIFEST = f"{WAVE}/fetched/manifest-retry.json"
RECHECKS = f"{WAVE}/rechecks"
SOURCE_TEXT = f"{WAVE}/source_text.py"
CORPUS = "corpus"
STATEMENTS = f"{WAVE}/statements.json"
# Rows that are formats of one document; a quote may recur inside the group but
# each row needs its own distinct quote (RFC 9110 html/txt: validators, URI schemes, media types).
DOCUMENT_GROUPS = (frozenset({"S010", "S028", "S033"}),)
# sha256 of .ufo/waves/round-26/population.json as it stood when this counter was written.
POPULATION_SHA256 = "16330e1effd5ee52665f8f31738e9423c6ec387e5d4a1404c5bcc35f69d01b03"
VERDICTS = ("HOLD", "STALE", "UNVERIFIABLE")
DECIDING = ("HOLD", "STALE")
RECEIPT_KEYS = frozenset({"id", "verdict", "fetchIndex", "quote", "anchorObserved", "reason", "correction"})
# Input-integrity findings: any of these means exit 2.
FATAL_IDS = frozenset({
    "root_unavailable", "revision_unavailable", "git_unavailable",
    "population_unavailable", "population_tampered", "population_invalid",
    "manifest_unavailable", "manifest_invalid", "source_text_unavailable",
    "manifest_entry_missing", "manifest_population_mismatch", "manifest_entry_invalid",
    "fetch_bytes_unavailable", "fetch_bytes_invalid", "fetch_sha_mismatch",
})
REVISION_RE = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}", re.IGNORECASE)
ROW_ID_RE = re.compile(r"S[0-9]{3}")
SHA256_RE = re.compile(r"[0-9a-f]{64}")


class InputFailure(Exception):
    """An unavailable or tampered input, reported under a stable finding id."""

    def __init__(self, finding_id: str, detail: str = "") -> None:
        super().__init__(finding_id)
        self.finding_id = finding_id
        self.detail = detail


class UsageError(Exception):
    """A malformed invocation; exits 64."""


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


def finding(finding_id: str, row: str | None, detail: str) -> dict[str, Any]:
    return {"id": finding_id, "row": row, "detail": detail}


def row_record(row_id: str, verdict: str | None, decided: bool, finding_ids: list[str]) -> dict[str, Any]:
    return {"id": row_id, "decided": decided, "verdict": verdict, "findings": finding_ids}


def strict_json(raw: bytes) -> Any:
    """Parse JSON; duplicate members, NaN, Infinity and invalid UTF-8 raise ValueError."""

    def reject_constant(name: str) -> Any:
        raise ValueError(f"non-standard JSON constant {name}")

    def unique_members(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON member {key!r}")
            result[key] = value
        return result

    try:
        return json.loads(raw.decode("utf-8"), parse_constant=reject_constant,
                          object_pairs_hook=unique_members)
    except RecursionError:
        raise ValueError("JSON nesting too deep") from None


def git_env() -> dict[str, str]:
    """Environment without inherited GIT_* variables and without user or system git configuration."""
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
    return env


def git_process(cwd: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    """Run git with replace refs and hooks disabled; the argument vector is never shell-parsed."""
    command = ["git", "--no-replace-objects", "--literal-pathspecs", "-c", "core.hooksPath=/dev/null", *args]
    try:
        return subprocess.run(command, cwd=cwd, env=git_env(), capture_output=True, check=False, timeout=120)
    except (OSError, subprocess.SubprocessError):
        raise InputFailure("git_unavailable", "git could not run") from None


def locate(root: Path) -> tuple[Path, str]:
    """Repository top level and the prefix of root inside it ('' when root is the top level)."""
    if not root.is_dir():
        raise InputFailure("root_unavailable", f"{root} is not a directory")
    top = git_process(root, "rev-parse", "--show-toplevel")
    prefix = git_process(root, "rev-parse", "--show-prefix")
    if top.returncode != 0 or prefix.returncode != 0:
        raise InputFailure("root_unavailable", f"{root} is not inside a git work tree")
    return Path(top.stdout.decode("utf-8").rstrip("\n")), prefix.stdout.decode("utf-8").rstrip("\n")


class Git:
    """Committed-object reader for one repository; paths are relative to its top level."""

    def __init__(self, top: Path, prefix: str) -> None:
        self.top = top
        self.prefix = prefix

    def path(self, relative: str) -> str:
        return self.prefix + relative

    def commit(self, revision: str) -> str:
        done = git_process(self.top, "rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}")
        if done.returncode != 0:
            raise InputFailure("revision_unavailable", f"{revision} is not a commit in this repository")
        return done.stdout.decode("ascii").strip()

    def entries(self, revision: str, path: str, recursive: bool) -> list[tuple[str, str]]:
        """(object type, repository path) for entries under path; empty when nothing is there."""
        flags = ["-r"] if recursive else []
        done = git_process(self.top, "ls-tree", "-z", *flags, revision, "--", path)
        if done.returncode != 0:
            raise InputFailure("git_unavailable", f"ls-tree failed for {path}")
        found: list[tuple[str, str]] = []
        for record in done.stdout.split(b"\0"):
            if not record:
                continue
            meta, tab, name = record.partition(b"\t")
            fields = meta.split()
            if not tab or len(fields) != 3:
                raise InputFailure("git_unavailable", "unparseable ls-tree record")
            found.append((fields[1].decode("ascii"), name.decode("utf-8", "surrogateescape")))
        return found

    def cat(self, revision: str, path: str) -> bytes:
        done = git_process(self.top, "cat-file", "blob", f"{revision}:{path}")
        if done.returncode != 0:
            raise InputFailure("git_unavailable", f"cat-file failed for {path}")
        return done.stdout

    def blob(self, revision: str, path: str) -> bytes | None:
        """Bytes of a regular blob at path, or None when that path holds no blob."""
        found = self.entries(revision, path, recursive=False)
        if [kind for kind, _ in found] != ["blob"] or found[0][1] != path:
            return None
        return self.cat(revision, path)


def field(obj: Any, key: str) -> Any:
    return obj.get(key) if isinstance(obj, dict) else None


def required_blob(git: Git, revision: str, path: str, finding_id: str) -> bytes:
    raw = git.blob(revision, path)
    if raw is None:
        raise InputFailure(finding_id, f"{path} is absent at the revision")
    return raw


def load_population(root: Path, git: Git, revision: str, pin: str) -> tuple[bytes, str]:
    """Population from the revision when present, else the exact local file; either must match the pin."""
    raw = git.blob(revision, git.path(POPULATION))
    source = "revision"
    if raw is None:
        try:
            raw = (root / POPULATION).read_bytes()
        except OSError:
            raise InputFailure("population_unavailable", f"{POPULATION} is absent at the revision and locally") from None
        source = "local"
    if hashlib.sha256(raw).hexdigest() != pin:
        raise InputFailure("population_tampered", f"{source} population sha256 differs from the pinned constant")
    return raw, source


def parse_population(raw: bytes) -> list[tuple[str, dict[int, tuple[str, str]]]]:
    """Rows as (id, {fetch index: (sha256, file relative to the wave directory)}) in population order."""
    try:
        document = strict_json(raw)
    except ValueError as exc:
        raise InputFailure("population_invalid", f"population is not strict JSON: {exc}") from None
    rows = field(document, "rows")
    if not isinstance(rows, list) or len(rows) != EXPECTED:
        raise InputFailure("population_invalid", f"population must hold exactly {EXPECTED} rows")
    parsed: list[tuple[str, dict[int, tuple[str, str]]]] = []
    seen: set[str] = set()
    for row in rows:
        row_id, fetches = field(row, "id"), field(row, "fetches")
        if (not isinstance(row_id, str) or not ROW_ID_RE.fullmatch(row_id) or row_id in seen
                or not isinstance(fetches, list)):
            raise InputFailure("population_invalid", f"malformed or duplicate row {row_id!r}")
        seen.add(row_id)
        pinned: dict[int, tuple[str, str]] = {}
        for fetch in fetches:
            index, sha, file = field(fetch, "index"), field(fetch, "sha256"), field(fetch, "file")
            if (type(index) is not int or index < 1 or index in pinned
                    or not isinstance(sha, str) or not SHA256_RE.fullmatch(sha)
                    or not isinstance(file, str) or not file):
                raise InputFailure("population_invalid", f"malformed fetch in {row_id}")
            pinned[index] = (sha, file)
        parsed.append((row_id, pinned))
    return parsed


def manifest_index(raw: bytes, label: str) -> dict[tuple[str, int], dict[str, Any]]:
    """Manifest entries keyed by (row, index); a repeated key is invalid input."""
    try:
        document = strict_json(raw)
    except ValueError as exc:
        raise InputFailure("manifest_invalid", f"{label} is not strict JSON: {exc}") from None
    if not isinstance(document, list):
        raise InputFailure("manifest_invalid", f"{label} must be a list")
    index: dict[tuple[str, int], dict[str, Any]] = {}
    for entry in document:
        row_id, fetch_index = field(entry, "row"), field(entry, "index")
        if not isinstance(row_id, str) or type(fetch_index) is not int:
            raise InputFailure("manifest_invalid", f"{label} has an entry without row and index")
        if (row_id, fetch_index) in index:
            raise InputFailure("manifest_invalid", f"{label} repeats {row_id} index {fetch_index}")
        index[(row_id, fetch_index)] = entry
    return index


def load_text_module(source: bytes) -> types.ModuleType:
    """Execute the revision's source_text.py in memory; nothing is written to disk."""
    module = types.ModuleType("source_text_at_revision")
    try:
        exec(compile(source, SOURCE_TEXT, "exec"), module.__dict__)
    except Exception as exc:  # any failure loading the committed helper is unavailable input
        raise InputFailure("source_text_unavailable", f"{type(exc).__name__}: {exc}") from None
    if not callable(getattr(module, "normalize", None)) or not callable(getattr(module, "text_of", None)):
        raise InputFailure("source_text_unavailable", "normalize and text_of are both required")
    return module


def quote_in_text(module: types.ModuleType, quote: str, text: str) -> bool:
    """True when the normalized quote occurs in text with no word character on either side."""
    needle = module.normalize(quote)
    return re.search(r"(?<!\w)" + re.escape(needle) + r"(?!\w)", text) is not None


class Checker:
    """Verifies receipts against the committed bytes of one revision."""

    def __init__(self, git: Git, revision: str, base: dict[tuple[str, int], dict[str, Any]],
                 retry: dict[tuple[str, int], dict[str, Any]], module: types.ModuleType) -> None:
        self.git = git
        self.revision = revision
        self.base = base
        self.retry = retry
        self.module = module
        self.corpus: list[str] | None = None
        self.views: dict[tuple[str, int], tuple[str | None, list[tuple[str, str]]]] = {}
        self.quotes: dict[str, str] = {}

    def fetch_view(self, row_id: str, index: int, pinned: tuple[str, str]) -> tuple[str | None, list[tuple[str, str]]]:
        """Normalized text of the effective fetch, or None with the findings that prevent it."""
        key = (row_id, index)
        if key not in self.views:
            self.views[key] = self.build_view(row_id, index, pinned)
        return self.views[key]

    def build_view(self, row_id: str, index: int, pinned: tuple[str, str]) -> tuple[str | None, list[tuple[str, str]]]:
        expected_sha, pinned_file = pinned
        key = (row_id, index)
        # The retry manifest supersedes the base entry for the same row and index.
        entry = self.retry[key] if key in self.retry else self.base.get(key)
        if entry is None:
            return None, [("manifest_entry_missing", f"{row_id} index {index} has no manifest entry")]
        if field(entry, "status") != 200 or field(entry, "error") is not None:
            return None, [("manifest_entry_invalid", f"effective {row_id} index {index} is not a successful fetch")]
        if field(entry, "sha256") != expected_sha:
            return None, [("manifest_population_mismatch", f"{row_id} index {index}: manifest sha256 differs from the population")]
        if field(entry, "file") != pinned_file.rsplit("/", 1)[-1]:
            return None, [("manifest_population_mismatch", f"{row_id} index {index}: manifest file differs from the population")]
        raw_gz = self.git.blob(self.revision, self.git.path(f"{WAVE}/{pinned_file}"))
        if raw_gz is None:
            return None, [("fetch_bytes_unavailable", f"{pinned_file} is absent at the revision")]
        try:
            raw = gzip.decompress(raw_gz)
        except (OSError, EOFError, zlib.error) as exc:
            return None, [("fetch_bytes_invalid", f"{pinned_file}: {exc}")]
        if hashlib.sha256(raw).hexdigest() != expected_sha:
            return None, [("fetch_sha_mismatch", f"{pinned_file} decompresses to bytes whose sha256 is not the pinned value")]
        try:
            text = self.module.normalize(self.module.text_of(raw, field(field(entry, "headers"), "content-type")))
        except Exception as exc:  # the committed text helper rejected these bytes
            return None, [("source_text_unavailable", f"text_of failed on {pinned_file}: {type(exc).__name__}: {exc}")]
        return text, []

    def marker_present(self, marker: str) -> bool:
        """True when a corpus/** text file at the revision contains marker; the corpus is read once."""
        if self.corpus is None:
            self.corpus = []
            for kind, name in self.git.entries(self.revision, self.git.path(CORPUS), recursive=True):
                if kind != "blob":
                    continue
                try:
                    self.corpus.append(self.git.cat(self.revision, name).decode("utf-8"))
                except UnicodeDecodeError:
                    continue
        return any(marker in text for text in self.corpus)

    def check(self, row_id: str, fetches: dict[int, tuple[str, str]], path: str,
              found: list[tuple[str, str]]) -> str | None:
        """Verify one committed receipt, record (finding id, detail) pairs, return its verdict when valid."""
        try:
            receipt = strict_json(self.git.cat(self.revision, path))
        except ValueError as exc:
            found.append(("receipt_json_invalid", f"{path}: {exc}"))
            return None
        if not isinstance(receipt, dict):
            found.append(("receipt_json_invalid", f"{path} is not a JSON object"))
            return None
        if set(receipt) != RECEIPT_KEYS:
            found.append(("receipt_schema", f"missing {sorted(RECEIPT_KEYS - set(receipt))}, "
                                            f"extra {sorted(set(receipt) - RECEIPT_KEYS)}"))
        if receipt.get("id") != row_id:
            found.append(("receipt_id_mismatch", f"receipt id {receipt.get('id')!r} sits at row {row_id}"))
        verdict = receipt.get("verdict")
        if verdict not in VERDICTS:
            found.append(("verdict_invalid", f"verdict {verdict!r} is not HOLD, STALE or UNVERIFIABLE"))
            verdict = None
        reason, anchor = receipt.get("reason"), receipt.get("anchorObserved")
        quote, correction = receipt.get("quote"), receipt.get("correction")
        if isinstance(quote, str) and verdict in DECIDING:
            self.quotes[row_id] = quote
        if not isinstance(reason, str) or not reason.strip():
            found.append(("reason_missing", "reason must be a nonempty string"))
        if not isinstance(anchor, str):
            found.append(("receipt_schema", "anchorObserved must be a string"))
        elif verdict in DECIDING and not anchor.strip():
            found.append(("anchor_missing", "HOLD and STALE need an anchorObserved location"))
        if quote is not None and not isinstance(quote, str):
            found.append(("receipt_schema", "quote must be a string or null"))
        if verdict in DECIDING and not isinstance(quote, str):
            found.append(("quote_missing", "HOLD and STALE need a verbatim quote"))
        if correction is not None and not isinstance(correction, str):
            found.append(("receipt_schema", "correction must be a string or null"))

        index = receipt.get("fetchIndex")
        text: str | None = None
        if type(index) is not int or index not in fetches:
            found.append(("fetch_index_invalid", f"fetchIndex {index!r} is not a population fetch of {row_id}"))
        else:
            text, view_findings = self.fetch_view(row_id, index, fetches[index])
            found.extend(view_findings)
        # Every other population fetch of the row grounds part of its teaches: verify its bytes too.
        for other in sorted(fetches):
            if other != index:
                found.extend(self.fetch_view(row_id, other, fetches[other])[1])

        if isinstance(quote, str):
            # 6+ alphanumeric tokens (JSON bodies carry no spaces) and at most 25 whitespace words.
            tokens, words = len(re.findall(r"[^\W_]+", quote)), len(quote.split())
            if tokens < 6 or words > 25:
                found.append(("quote_word_count", f"quote has {tokens} tokens / {words} words; >=6 tokens and <=25 words required"))
            elif text is not None and not quote_in_text(self.module, quote, text):
                found.append(("quote_not_in_text", "normalized quote is not a word-bounded substring of the effective fetch text"))

        marker = f"[r26-recheck {row_id} STALE]"
        if verdict == "STALE":
            if not isinstance(correction, str) or not correction.strip():
                found.append(("correction_missing", "STALE needs a nonempty correction"))
            if not self.marker_present(marker):
                found.append(("stale_marker_absent", f"no corpus/** file at the revision contains {marker}"))
        elif verdict in ("HOLD", "UNVERIFIABLE") and correction is not None:
            found.append(("correction_unexpected", f"{verdict} receipts carry correction null"))
        if verdict == "UNVERIFIABLE":
            found.append(("row_unverifiable", "UNVERIFIABLE is reported separately and never decided"))
        return verdict

    def specificity(self, population: list[tuple[str, dict[int, tuple[str, str]]]],
                    quotes: dict[str, str]) -> dict[str, list[tuple[str, str]]]:
        """A decided quote must not occur in another row's text outside its document group,
        and quotes inside one group must not equal or contain one another (boilerplate cannot ground a row)."""
        texts: dict[str, list[str]] = {}
        for row_id, fetches in population:
            texts[row_id] = [t for t in (self.fetch_view(row_id, i, p)[0] for i, p in fetches.items()) if t is not None]
        group = {row: g for g in DOCUMENT_GROUPS for row in g}
        out: dict[str, list[tuple[str, str]]] = {}
        for row_id, quote in quotes.items():
            mates = group.get(row_id, frozenset({row_id}))
            hits = [other for other, ts in texts.items()
                    if other not in mates and any(quote_in_text(self.module, quote, t) for t in ts)]
            needle = self.module.normalize(quote)
            twins = [other for other in mates if other != row_id and quotes.get(other) is not None
                     and (needle in self.module.normalize(quotes[other])
                          or self.module.normalize(quotes[other]) in needle)]
            if hits or twins:
                out[row_id] = [("quote_not_row_specific", f"quote also occurs in {sorted(hits)}; same quote as {sorted(twins)}")]
        return out

    def statement_ledger(self, findings: list[dict[str, Any]], output: dict[str, Any], rows: set[str]) -> None:
        """Every STALE knowledge statement recorded in the ledger has its tag appended in that file.

        A pair names a population row and a corpus file once. Tags in the file for that row must equal
        stale + reclassified (tags the falsify wave reclassified as precision notes stay append-only)."""
        raw = self.git.blob(self.revision, self.git.path(STATEMENTS))
        if raw is None:
            findings.append(finding("statements_absent", None, f"{STATEMENTS} is absent at the revision"))
            return
        try:
            ledger = strict_json(raw)
        except ValueError as exc:
            findings.append(finding("statements_invalid", None, str(exc)))
            return
        entries = field(ledger, "pairs")
        if not isinstance(entries, list) or not entries:
            findings.append(finding("statements_invalid", None, "pairs must be a nonempty list"))
            return
        seen: set[tuple[str, str]] = set()
        for entry in entries:
            row_id, path, n, stale = (field(entry, k) for k in ("row", "file", "statements", "stale"))
            reclassified = field(entry, "reclassified") if isinstance(entry, dict) and "reclassified" in entry else 0
            if (not isinstance(row_id, str) or not ROW_ID_RE.fullmatch(row_id) or not isinstance(path, str)
                    or not path.startswith(f"{CORPUS}/") or type(n) is not int or type(stale) is not int
                    or type(reclassified) is not int or not 0 <= stale <= n or not 0 <= reclassified <= n):
                findings.append(finding("statements_invalid", None, f"malformed pair entry {entry!r}"))
                continue
            if (row_id, path) in seen:
                findings.append(finding("statements_duplicate_pair", row_id, f"{row_id} x {path} is listed twice"))
                continue
            seen.add((row_id, path))
            if row_id not in rows:
                findings.append(finding("statements_row_outside_population", row_id,
                                        f"{row_id} is not a population row"))
                continue
            output["statements"] += n
            output["statementsStale"] += stale
            blob = self.git.blob(self.revision, self.git.path(path))
            tags = blob.decode("utf-8", "replace").count(f"[r26-recheck {row_id} STALE]") if blob is not None else 0
            output["statementCorrections"] += min(tags, stale)
            if tags < stale:
                findings.append(finding("statement_correction_absent", row_id,
                                        f"{path} carries {tags} of {stale} [r26-recheck {row_id} STALE] corrections"))
            elif tags != stale + reclassified:
                findings.append(finding("statement_tags_unaccounted", row_id,
                                        f"{path} carries {tags} [r26-recheck {row_id} STALE] tags; ledger accounts for "
                                        f"{stale} stale + {reclassified} reclassified"))


def base_result(pin: str) -> dict[str, Any]:
    return {"schema": SCHEMA, "revision": None, "populationSha256": pin, "populationSource": None,
            "expected": EXPECTED, "decided": 0, "hold": 0, "stale": 0, "unverifiable": 0,
            "statements": 0, "statementsStale": 0, "statementCorrections": 0,
            "rows": [], "findings": []}


def exit_code(output: dict[str, Any]) -> int:
    ids = {item["id"] for item in output["findings"]}
    if ids & FATAL_IDS:
        return 2
    return 0 if output["decided"] == EXPECTED and not output["findings"] else 1


def receipt_paths(git: Git, revision: str, population: list[tuple[str, dict[int, tuple[str, str]]]],
                  findings: list[dict[str, Any]]) -> dict[str, str]:
    """Row id to committed receipt path; any other entry under the rechecks directory is unexpected."""
    wanted = {git.path(f"{RECHECKS}/{row_id}.json"): row_id for row_id, _ in population}
    present: dict[str, str] = {}
    for kind, name in git.entries(revision, git.path(RECHECKS), recursive=True):
        if kind == "blob" and name in wanted:
            present[wanted[name]] = name
        else:
            findings.append(finding("receipt_unexpected", None, name))
    return present


def score(root: Path, revision: str, pin: str, output: dict[str, Any]) -> tuple[dict[str, Any], int]:
    findings = output["findings"]
    top, prefix = locate(root)
    git = Git(top, prefix)
    commit = git.commit(revision)
    output["revision"] = commit
    population_raw, output["populationSource"] = load_population(root, git, commit, pin)
    population = parse_population(population_raw)
    present = receipt_paths(git, commit, population, findings)
    if not present:
        findings.append(finding("receipts_absent", None, f"no {RECHECKS}/S0NN.json at the revision"))
        output["rows"] = [row_record(row_id, None, False, []) for row_id, _ in population]
        return output, exit_code(output)
    base = manifest_index(required_blob(git, commit, git.path(MANIFEST), "manifest_unavailable"), "manifest.json")
    retry_raw = git.blob(commit, git.path(RETRY_MANIFEST))
    retry = manifest_index(retry_raw, "manifest-retry.json") if retry_raw is not None else {}
    module = load_text_module(required_blob(git, commit, git.path(SOURCE_TEXT), "source_text_unavailable"))
    checker = Checker(git, commit, base, retry, module)
    checked: list[tuple[str, str | None, list[tuple[str, str]]]] = []
    for row_id, fetches in population:
        row_findings: list[tuple[str, str]] = []
        verdict = None
        if row_id in present:
            verdict = checker.check(row_id, fetches, present[row_id], row_findings)
        else:
            row_findings.append(("receipt_missing", f"no {RECHECKS}/{row_id}.json at the revision"))
        checked.append((row_id, verdict, row_findings))
    specific = checker.specificity(population, {r: q for r, v, f in checked
                                                for q in [checker.quotes.get(r)] if q is not None and not f})
    rows = []
    for row_id, verdict, row_findings in checked:
        row_findings.extend(specific.get(row_id, []))
        for finding_id, detail in row_findings:
            findings.append(finding(finding_id, row_id, detail))
        decided = verdict in DECIDING and not row_findings
        rows.append(row_record(row_id, verdict, decided, [finding_id for finding_id, _ in row_findings]))
        if decided:
            output["decided"] += 1
            if verdict == "HOLD":
                output["hold"] += 1
            else:
                output["stale"] += 1
        if verdict == "UNVERIFIABLE":
            output["unverifiable"] += 1
    output["rows"] = rows
    checker.statement_ledger(findings, output, {row_id for row_id, _ in population})
    return output, exit_code(output)


def evaluate(root: Path, revision: str, pin: str) -> tuple[dict[str, Any], int]:
    output = base_result(pin)
    try:
        return score(root, revision, pin, output)
    except InputFailure as exc:
        output.update(decided=0, hold=0, stale=0, unverifiable=0, rows=[])
        output["findings"].append(finding(exc.finding_id, None, exc.detail))
        return output, 2


SELFTEST_CORPUS = f"{CORPUS}/knowledge/recheck-fixture.md"
FIXTURE_IDS = [f"S{number:03d}" for number in range(1, EXPECTED + 1)]
FIXTURE_SOURCE = b"""def normalize(text):
    return " ".join(text.split())


def text_of(raw, content_type=None):
    return normalize(raw.decode("utf-8", errors="replace"))
"""


def json_bytes(document: Any) -> bytes:
    return (json.dumps(document, indent=2) + "\n").encode("utf-8")


GROUP_SENTENCE = "Shared group text india juliet kilo lima mike november oscar."


def fixture_raw(row_id: str, index: int = 1) -> bytes:
    number = int(row_id[1:])
    # Document-group rows also share one sentence, so in-group twin quotes are expressible.
    shared = f"{GROUP_SENTENCE} " if any(row_id in group for group in DOCUMENT_GROUPS) else ""
    second = f" Copy {index} of {row_id}." if index != 1 else ""
    return (f"Fixture {row_id} documents alpha{number} bravo charlie delta echo foxtrot golf hotel. {shared}"
            f"Second sentence {row_id} mike november oscar papa quebec romeo sierra tango.{second}\n").encode("utf-8")


def fixture_quote(row_id: str) -> str:
    return f"documents alpha{int(row_id[1:])} bravo charlie delta echo foxtrot golf"


def fixture_receipt(row_id: str) -> dict[str, Any]:
    return {"id": row_id, "verdict": "HOLD", "fetchIndex": 1, "quote": fixture_quote(row_id),
            "anchorObserved": f"fixture section {row_id}",
            "reason": "The statement still matches the re-fetched bytes.", "correction": None}


def stale_correction(row_id: str) -> str:
    return f"[r26-recheck {row_id} STALE] Corrected fixture statement for {row_id}."


def stale_receipt(row_id: str) -> dict[str, Any]:
    return dict(fixture_receipt(row_id), verdict="STALE", correction=stale_correction(row_id))


def receipt_key(row_id: str) -> str:
    return f"{RECHECKS}/{row_id}.json"


def manifest_entry(row_id: str, name: str, status: int | None, raw: bytes, error: str | None,
                   index: int = 1) -> dict[str, Any]:
    url = f"https://fixture.invalid/{row_id}/{index}"
    return {"row": row_id, "index": index, "url": url, "finalUrl": url, "status": status, "error": error,
            "headers": {"content-type": "text/plain; charset=UTF-8"}, "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "file": name}


def fixture_files() -> tuple[dict[str, bytes], str]:
    """Synthetic round: 32 rows, S002 with two fetches, S008 superseded by a retry, S031 STALE with its marker.

    Returns the committed files and the sha256 pin of the population."""
    files: dict[str, bytes] = {SOURCE_TEXT: FIXTURE_SOURCE, f"{CORPUS}/README.md": b"fixture corpus\n"}
    rows: list[dict[str, Any]] = []
    base: list[dict[str, Any]] = []
    retry: list[dict[str, Any]] = []
    for row_id in FIXTURE_IDS:
        raw = fixture_raw(row_id)
        name = f"{row_id}-1.raw.gz"
        if row_id == "S008":  # the first attempt failed; the retry entry supersedes it
            files[f"{WAVE}/fetched/S008-1.raw.gz"] = gzip.compress(b"", mtime=0)
            base.append(manifest_entry(row_id, "S008-1.raw.gz", None, b"", "TimeoutError: first attempt"))
            name = "S008-1-retry.raw.gz"
            retry.append(manifest_entry(row_id, name, 200, raw, None))
        else:
            base.append(manifest_entry(row_id, name, 200, raw, None))
        files[f"{WAVE}/fetched/{name}"] = gzip.compress(raw, mtime=0)
        fetches = [{"index": 1, "url": f"https://fixture.invalid/{row_id}/1",
                    "status": 200, "sha256": hashlib.sha256(raw).hexdigest(), "file": f"fetched/{name}"}]
        if row_id == "S002":  # a second retained document grounds part of the row; its bytes are checked too
            raw2 = fixture_raw(row_id, 2)
            base.append(manifest_entry(row_id, "S002-2.raw.gz", 200, raw2, None, index=2))
            files[f"{WAVE}/fetched/S002-2.raw.gz"] = gzip.compress(raw2, mtime=0)
            fetches.append({"index": 2, "url": f"https://fixture.invalid/{row_id}/2",
                            "status": 200, "sha256": hashlib.sha256(raw2).hexdigest(), "file": "fetched/S002-2.raw.gz"})
        rows.append({"id": row_id, "fetches": fetches})
        files[receipt_key(row_id)] = json_bytes(stale_receipt(row_id) if row_id == "S031" else fixture_receipt(row_id))
    files[POPULATION] = json_bytes({"round": 26, "rows": rows})
    files[MANIFEST] = json_bytes(base)
    files[RETRY_MANIFEST] = json_bytes(retry)
    files[SELFTEST_CORPUS] = (stale_correction("S031") + "\n").encode("utf-8")
    files[STATEMENTS] = json_bytes(LEDGER)
    return files, hashlib.sha256(files[POPULATION]).hexdigest()


def git_fixture(repo: Path, *args: str) -> str:
    done = git_process(repo, "-c", "user.name=kake-selftest", "-c", "user.email=selftest@invalid",
                       "-c", "commit.gpgSign=false", *args)
    if done.returncode != 0:
        raise RuntimeError(f"selftest git {args[0]} failed: {done.stderr.decode('utf-8', 'replace').strip()}")
    return done.stdout.decode("utf-8").strip()


def commit_fixture(repo: Path, files: dict[str, bytes]) -> str:
    repo.mkdir(parents=True)
    git_fixture(repo, "init", "-q")
    for relative, data in files.items():
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    git_fixture(repo, "add", "-A")
    git_fixture(repo, "commit", "-q", "--no-verify", "-m", "fixture")
    return git_fixture(repo, "rev-parse", "HEAD")


def put(row_id: str, receipt: dict[str, Any]) -> Any:
    """Mutation replacing one committed receipt with the given document."""

    def mutate(files: dict[str, bytes]) -> None:
        files[receipt_key(row_id)] = json_bytes(receipt)

    return mutate


def replace(key: str, data: bytes) -> Any:
    """Mutation replacing the committed bytes at key."""

    def mutate(files: dict[str, bytes]) -> None:
        files[key] = data

    return mutate


def append(key: str, data: bytes) -> Any:
    """Mutation appending bytes to the committed file at key."""

    def mutate(files: dict[str, bytes]) -> None:
        files[key] = files[key] + data

    return mutate


def remove(key: str) -> Any:
    """Mutation deleting the committed file at key."""

    def mutate(files: dict[str, bytes]) -> None:
        del files[key]

    return mutate


DUPLICATE_KEY_RECEIPT = (b'{"id": "S010", "verdict": "HOLD", "verdict": "STALE", "fetchIndex": 1, '
                         b'"quote": "x", "anchorObserved": "y", "reason": "z", "correction": null}\n')

LEDGER = {"pairs": [{"row": "S031", "file": SELFTEST_CORPUS, "statements": 2, "stale": 1}]}


def manifest_sha(row_id: str, sha: str) -> Any:
    """Mutation changing only the base manifest sha256 of one row (bytes and population untouched)."""

    def mutate(files: dict[str, bytes]) -> None:
        entries = json.loads(files[MANIFEST])
        for entry in entries:
            if entry["row"] == row_id:
                entry["sha256"] = sha
        files[MANIFEST] = json_bytes(entries)

    return mutate


def both(*mutations: Any) -> Any:
    def mutate(files: dict[str, bytes]) -> None:
        for mutation in mutations:
            mutation(files)

    return mutate


EXTRA_TAG = append(SELFTEST_CORPUS, (stale_correction("S031") + "\n").encode("utf-8"))
OUTSIDE_PAIR = {"row": "S099", "file": SELFTEST_CORPUS, "statements": 1, "stale": 0}
# Statement counters (statements, statementsStale, statementCorrections) asserted with len(rows) == 32.
COUNTS = {"complete_clean": (2, 1, 1), "reclassified_accounted": (2, 1, 1)}

CASES: list[tuple[str, Any, int, tuple[str, ...], int, bool]] = [
    # name, mutation, expected exit, expected finding ids, expected decided rows, baseline without population
    ("complete_clean", None, 0, (), EXPECTED, False),
    ("missing_receipt", remove(receipt_key("S005")), 1, ("receipt_missing",), EXPECTED - 1, False),
    ("bad_sha", replace(f"{WAVE}/fetched/S003-1.raw.gz", gzip.compress(b"altered bytes\n", mtime=0)),
     2, ("fetch_sha_mismatch",), EXPECTED - 1, False),
    ("quote_not_in_text",
     put("S004", dict(fixture_receipt("S004"), quote=fixture_quote("S004").replace("documents", "describes"))),
     1, ("quote_not_in_text",), EXPECTED - 1, False),
    ("short_quote", put("S006", dict(fixture_receipt("S006"), quote="documents alpha6 bravo charlie delta")),
     1, ("quote_word_count",), EXPECTED - 1, False),
    ("stale_without_correction", put("S031", dict(stale_receipt("S031"), correction=None)),
     1, ("correction_missing",), EXPECTED - 1, False),
    ("stale_marker_absent", replace(SELFTEST_CORPUS, b"no marker here\n"),
     1, ("stale_marker_absent", "statement_correction_absent"), EXPECTED - 1, False),
    ("unverifiable_undecided",
     put("S020", dict(fixture_receipt("S020"), verdict="UNVERIFIABLE", quote=None,
                      reason="dynamic shell, no retained text")),
     1, ("row_unverifiable",), EXPECTED - 1, False),
    ("duplicate_json_key", replace(receipt_key("S010"), DUPLICATE_KEY_RECEIPT),
     1, ("receipt_json_invalid",), EXPECTED - 1, False),
    ("tampered_population", append(POPULATION, b"\n"), 2, ("population_tampered",), 0, False),
    ("baseline_without_receipts", None, 1, ("receipts_absent",), 0, True),
    ("boilerplate_quote",
     put("S012", dict(fixture_receipt("S012"), quote="bravo charlie delta echo foxtrot golf hotel")),
     1, ("quote_not_row_specific",), EXPECTED - 1, False),
    ("statement_correction_absent",
     replace(STATEMENTS, json_bytes({"pairs": [dict(LEDGER["pairs"][0], stale=2)]})),
     1, ("statement_correction_absent",), EXPECTED, False),
    ("statements_absent", remove(STATEMENTS), 1, ("statements_absent",), EXPECTED, False),
    ("quote_left_boundary", put("S004", dict(fixture_receipt("S004"), quote=fixture_quote("S004")[2:])),
     1, ("quote_not_in_text",), EXPECTED - 1, False),
    ("quote_right_boundary", put("S004", dict(fixture_receipt("S004"), quote=fixture_quote("S004")[:-2])),
     1, ("quote_not_in_text",), EXPECTED - 1, False),
    ("quote_26_words",
     put("S006", dict(fixture_receipt("S006"),
                      quote=fixture_quote("S006") + " " + " ".join(f"word{i}" for i in range(18)))),
     1, ("quote_word_count",), EXPECTED - 1, False),
    ("group_twin_quote",
     both(put("S010", dict(fixture_receipt("S010"), quote="Shared group text india juliet kilo lima")),
          put("S028", dict(fixture_receipt("S028"), quote="Shared group text india juliet kilo lima mike"))),
     1, ("quote_not_row_specific",), EXPECTED - 2, False),
    ("manifest_sha_mismatch", manifest_sha("S003", "0" * 64), 2, ("manifest_population_mismatch",), EXPECTED - 1, False),
    ("second_fetch_tampered", replace(f"{WAVE}/fetched/S002-2.raw.gz", gzip.compress(b"altered copy\n", mtime=0)),
     2, ("fetch_sha_mismatch",), EXPECTED - 1, False),
    ("statements_duplicate_pair", replace(STATEMENTS, json_bytes({"pairs": LEDGER["pairs"] * 2})),
     1, ("statements_duplicate_pair",), EXPECTED, False),
    ("statements_row_outside_population",
     replace(STATEMENTS, json_bytes({"pairs": LEDGER["pairs"] + [OUTSIDE_PAIR]})),
     1, ("statements_row_outside_population",), EXPECTED, False),
    ("statement_tags_unaccounted", EXTRA_TAG, 1, ("statement_tags_unaccounted",), EXPECTED, False),
    ("reclassified_accounted",
     both(EXTRA_TAG, replace(STATEMENTS, json_bytes({"pairs": [dict(LEDGER["pairs"][0], reclassified=1)]}))),
     0, (), EXPECTED, False),
]


def run_case(name: str, mutate: Any, expect_exit: int, expect_ids: tuple[str, ...],
             expect_decided: int, baseline: bool) -> dict[str, Any]:
    files, pin = fixture_files()
    local_population = files[POPULATION]
    if baseline:
        files = {f"{CORPUS}/README.md": b"baseline corpus\n"}
    elif mutate is not None:
        mutate(files)
    with tempfile.TemporaryDirectory(prefix="kake-recheck-selftest-") as scratch:
        repo = Path(scratch) / "fixture"
        revision = commit_fixture(repo, files)
        if baseline:  # the revision lacks the population, so the exact local copy is the only source
            (repo / POPULATION).parent.mkdir(parents=True, exist_ok=True)
            (repo / POPULATION).write_bytes(local_population)
        output, code = evaluate(repo, revision, pin)
    found = sorted({item["id"] for item in output["findings"]})
    source_ok = output["populationSource"] == "local" if baseline else True
    counts = tuple(output[k] for k in ("statements", "statementsStale", "statementCorrections"))
    counts_ok = name not in COUNTS or (counts == COUNTS[name] and len(output["rows"]) == EXPECTED)
    passed = (code == expect_exit and found == sorted(expect_ids)
              and output["decided"] == expect_decided and source_ok and counts_ok)
    return {"case": name, "passed": passed, "exit": code, "expectedExit": expect_exit,
            "findings": found, "expectedFindings": sorted(expect_ids),
            "decided": output["decided"], "expectedDecided": expect_decided,
            "populationSource": output["populationSource"], "statementCounts": list(counts),
            "rows": len(output["rows"])}


def run_selftest() -> tuple[dict[str, Any], int]:
    cases = [run_case(*case) for case in CASES]
    failed = sum(1 for case in cases if not case["passed"])
    summary = {"schema": SELFTEST_SCHEMA, "cases": cases, "passed": len(cases) - failed, "failed": failed}
    return summary, (1 if failed else 0)


def usage_result(message: str) -> dict[str, Any]:
    output = base_result(POPULATION_SHA256)
    output["findings"].append(finding("usage", None, message))
    return output


def main(argv: list[str] | None = None) -> int:
    parser = Parser(description=__doc__, add_help=False)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--revision")
    parser.add_argument("--selftest", action="store_true")
    try:
        args = parser.parse_args(sys.argv[1:] if argv is None else argv)
        if args.selftest:
            if args.root is not None or args.revision is not None:
                raise UsageError("--selftest takes no --root or --revision")
            output, code = run_selftest()
        else:
            if args.root is None or args.revision is None:
                raise UsageError("--root and --revision are required")
            if not REVISION_RE.fullmatch(args.revision):
                raise UsageError("--revision must be a full 40- or 64-digit hexadecimal object name")
            output, code = evaluate(args.root, args.revision.lower(), POPULATION_SHA256)
    except UsageError as exc:
        output, code = usage_result(str(exc)), 64
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
