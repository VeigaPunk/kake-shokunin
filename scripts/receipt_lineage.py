#!/usr/bin/env python3
"""Receipt-lineage watch (round 61, claim C1): make undisclosed receipt rewrites detectable.

Usage:
  python3 -B scripts/receipt_lineage.py --root LANE --revision REV [--disclosures PATH] [--json]
  python3 -B scripts/receipt_lineage.py --selftest

The surface is the committed history of the lane's receipt files: every file committed at the
measured revision under ``.ufo/waves/round-<N>/`` that sits below a ``control`` or ``controls``
directory (any depth of round number, any depth below that directory) and ends in ``.txt`` or
``.json``.  At 9f07731a873585e655a6518233ea39f5d9fb8204 that rule selects exactly the 144 paths
of ``.ufo/waves/round-61/controls/population-144.txt`` (verified; see the seat report).

RULES (frozen by the round-61 contract, implemented literally):

  receipt detection
      a population file whose FIRST committed version -- first-parent history from the root
      commit through the revision under test -- carries a receipt grammar line, i.e. a line
      matching  (?im)^\\s*#\\s*receipt\\s*:  OR  EXIT=  OR  ^VERDICT:  (the ``EXIT=`` alternative
      is unanchored, exactly as frozen).  A population file whose first version carries no such
      line is never a finding, however it is rewritten later.

  history walk
      every first-parent commit C, after the commit that first added the file and up to the
      revision under test, whose tree holds a different blob for the path than C's first parent
      is an EVENT CANDIDATE.  Merge commits are diffed against their first parent
      (``--diff-merges=first-parent``).  Renames are not followed: a rename ends the path's
      history and the new path starts its own (``--no-renames``).  A delete ends a history
      segment; a re-add starts a new one.

  result span
      the set of whole lines of a version matching
      (?im)(^#\\s*receipt\\s*:|revision\\s*[:=]|EXIT\\s*=|met\\s*=|conditions_passed|cases_passed|
      findings\\s*=|scores_held|members\\s*=)
      compared as an unordered set of whole lines (a pure reordering of equal lines is not a
      rewrite).

  rewrite event
      an event candidate whose child result span differs from its parent's -> kind ``rewrite``.

  pending-fill event
      the first committed version carries a ``pending`` marker and a later version does not ->
      kind ``pending_filled`` at the first such later commit.  A (path, commit) carries at most
      one kind; ``pending_filled`` wins over ``rewrite``.

  disclosure
      an event is disclosed when the disclosures JSON (schema ``kake-receipt-disclosures-v1``,
      ``{"entries": [{"path", "commit", "kind", "note", "disclosed-by"}]}``) holds an entry whose
      ``path`` equals the event path and whose ``commit`` names the event commit (full 40-hex, or
      an unambiguous abbreviated sha of at least 7 hex digits).  ``kind`` is not consulted: the
      frozen sentence matches on (path, commit).  An undisclosed event is a finding
      ``undisclosed_rewrite`` / ``undisclosed_pending_filled``; a disclosures entry that names no
      event is a finding ``phantom_disclosure``.

  met
      ``receipts=<n> events=<k> undisclosed=<m> met=<bool>`` where met is ``undisclosed == 0``
      over the walked range.  Exit is 0 when there is no finding at all, 1 when there is one or
      more, 2 when the range cannot be evaluated (revision unresolved, ``--root`` not a
      repository toplevel, malformed disclosures), 64 on a usage error.

DELIBERATE READINGS (each one recorded in the seat report, none loosens a frozen rule):

  * pending is tested over the WHOLE first-version text, not only its result span.  The frozen
    sentence names the result span; the motivating round-57 receipt (``.ufo/waves/round-57/
    controls/after-c1-receipt-pins.txt`` at 31b61a4) opens with a bare ``pending`` line that is
    outside the span, so a span-only test would classify that fill as a plain rewrite.  Testing
    the whole version catches every span-pending too; the later side is tested the same way.
  * the disclosures path is resolved committed-first when it is repository-relative (the blob at
    the revision under test), then on the filesystem; an absent DEFAULT path means "no
    disclosures", an absent explicitly named path is could-not-evaluate.
  * ``met`` reports the frozen ``undisclosed == 0`` predicate; ``phantom_disclosure`` alone
    therefore gives met=True with exit 1 (a finding, not an undisclosed event).
  * ``--json`` prints one JSON document whose ``summary`` member carries the same summary line
    the plain form prints, so either reader finds the frozen shape.

Read-only: the tool writes nothing.  Committed bytes only, via ``git rev-list`` / ``git log
--raw`` / ``git ls-tree`` / ``git cat-file`` -- the worktree is never read (the only filesystem
read is the disclosures file, and only after the committed copy at the revision is missing).
Inherited ``GIT_*`` variables are scrubbed from every git subprocess.
"""
from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import subprocess
import sys
import tempfile

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_UNEVALUABLE = 2
EXIT_USAGE = 64

ROUND_PREFIX_RE = re.compile(r"^\.ufo/waves/round-[0-9]+/")
CONTROL_SEGMENTS = frozenset(("control", "controls"))
POPULATION_EXT_RE = re.compile(r"\.(?:txt|json)$")
BLOB_MODES = frozenset(("100644", "100755", "100664"))

# Frozen patterns -- kept verbatim so the code carries the contract sentence.
RECEIPT_GRAMMAR_RE = re.compile(r"(?im)(^\s*#\s*receipt\s*:)|(EXIT=)|(^VERDICT:)")
RESULT_SPAN_RE = re.compile(
    r"(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|"
    r"cases_passed|findings\s*=|scores_held|members\s*=)"
)
PENDING_RE = re.compile(r"(?i)\bpending\b")
RECEIPT_HEADER_RE = re.compile(r"(?i)^\s*#\s*receipt\s*:")

DISCLOSURES_SCHEMA = "kake-receipt-disclosures-v1"
DEFAULT_DISCLOSURES = ".ufo/receipt-disclosures.json"

GIT_TIMEOUT = 300


class Unevaluable(Exception):
    """The range cannot be evaluated (exit 2)."""


# --------------------------------------------------------------------------- git plumbing

def git_env() -> dict[str, str]:
    """Environment for every git subprocess: inherited GIT_* variables are dropped."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def git(root: str, *args: str, stdin: bytes | None = None) -> tuple[int, bytes]:
    proc = subprocess.run(["git", "-C", root, "--literal-pathspecs", *args],
                          input=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=git_env(), timeout=GIT_TIMEOUT)
    return proc.returncode, proc.stdout


def toplevel(root: str) -> str | None:
    try:
        rc, out = git(root, "rev-parse", "--show-toplevel")
    except (OSError, subprocess.SubprocessError):
        return None
    if rc != 0:
        return None
    try:
        return os.path.realpath(out.decode("utf-8", "surrogateescape").strip())
    except (UnicodeDecodeError, OSError):
        return None


def resolve_commit(root: str, revision: str) -> str | None:
    if not revision or revision.startswith("-"):
        return None
    try:
        rc, out = git(root, "rev-parse", "--verify", "--quiet", "--end-of-options",
                      f"{revision}^{{commit}}")
    except (OSError, subprocess.SubprocessError):
        return None
    if rc != 0:
        return None
    sha = out.decode("ascii", "replace").strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", sha):
        return None
    return sha


# --------------------------------------------------------------------------- population

def is_population_path(path: str) -> bool:
    """True for a file under .ufo/waves/round-<N>/ below a control/controls directory."""
    if not ROUND_PREFIX_RE.match(path):
        return False
    if not POPULATION_EXT_RE.search(path):
        return False
    tail = ROUND_PREFIX_RE.sub("", path)
    return any(segment in CONTROL_SEGMENTS for segment in tail.split("/")[:-1])


def population(root: str, revision: str) -> tuple[list[str], list[dict[str, str]]]:
    rc, out = git(root, "ls-tree", "-r", "-z", "--full-tree", revision)
    if rc != 0:
        raise Unevaluable("git ls-tree failed")
    paths: list[str] = []
    skipped: list[dict[str, str]] = []
    for record in out.split(b"\0"):
        if not record:
            continue
        meta, _, raw_path = record.partition(b"\t")
        fields = meta.decode("ascii", "replace").split()
        if len(fields) < 3:
            continue
        mode, otype = fields[0], fields[1]
        path = raw_path.decode("utf-8", "surrogateescape")
        if not is_population_path(path):
            continue
        if otype != "blob" or mode not in BLOB_MODES:
            skipped.append({"path": path, "reason": f"non-blob population path (mode {mode})"})
            continue
        paths.append(path)
    return sorted(paths), skipped


# --------------------------------------------------------------------------- history walk

def unquote_path(raw: str) -> str:
    """Decode git's C-style quoted raw-diff path (used only for control characters)."""
    if len(raw) < 2 or not (raw.startswith('"') and raw.endswith('"')):
        return raw
    body = raw[1:-1]
    out = bytearray()
    index = 0
    simple = {"a": 7, "b": 8, "t": 9, "n": 10, "v": 11, "f": 12, "r": 13, '"': 34, "\\": 92}
    while index < len(body):
        char = body[index]
        if char == "\\" and index + 1 < len(body):
            nxt = body[index + 1]
            if nxt in simple:
                out.append(simple[nxt])
                index += 2
                continue
            if nxt in "01234567":
                digits = ""
                cursor = index + 1
                while cursor < len(body) and len(digits) < 3 and body[cursor] in "01234567":
                    digits += body[cursor]
                    cursor += 1
                out.append(int(digits, 8) & 0xFF)
                index = cursor
                continue
            out.extend(nxt.encode("utf-8", "surrogateescape"))
            index += 2
            continue
        out.extend(char.encode("utf-8", "surrogateescape"))
        index += 1
    return out.decode("utf-8", "surrogateescape")


def walk_changes(root: str, revision: str, paths: list[str]) -> dict[str, list[tuple[str, str, str]]]:
    """path -> [(commit, status, child blob)] in first-parent order, oldest first."""
    if not paths:
        return {}
    rc, out = git(root, "log", "--first-parent", "--reverse", "--format=C:%H", "--raw",
                  "--no-abbrev", "--no-renames", "--diff-merges=first-parent",
                  "--end-of-options", revision, "--", *paths)
    if rc != 0:
        raise Unevaluable("the first-parent history could not be walked")
    wanted = set(paths)
    ops: dict[str, list[tuple[str, str, str]]] = {path: [] for path in paths}
    commit = ""
    for line in out.decode("utf-8", "surrogateescape").splitlines():
        if line.startswith("C:"):
            commit = line[2:].strip()
            continue
        if not line.startswith(":"):
            continue
        meta, _, raw_path = line.partition("\t")
        fields = meta[1:].split()
        if len(fields) < 5:
            continue
        status = fields[4][:1]
        path = unquote_path(raw_path)
        if path in wanted:
            ops[path].append((commit, status, fields[3]))
    return ops


def read_blobs(root: str, shas: list[str]) -> dict[str, bytes]:
    shas = sorted({sha for sha in shas if sha and set(sha) != {"0"}})
    if not shas:
        return {}
    rc, out = git(root, "cat-file", "--batch", stdin="".join(sha + "\n" for sha in shas).encode())
    if rc != 0:
        raise Unevaluable("git cat-file --batch failed")
    blobs: dict[str, bytes] = {}
    position = 0
    for sha in shas:
        newline = out.find(b"\n", position)
        if newline < 0:
            raise Unevaluable("git cat-file --batch returned a short stream")
        header = out[position:newline].decode("ascii", "replace").split()
        position = newline + 1
        if len(header) < 3 or header[1] != "blob":
            blobs[sha] = b""
            continue
        size = int(header[2])
        blobs[sha] = out[position:position + size]
        position += size + 1
    return blobs


def decode(raw: bytes | None) -> str:
    return (raw or b"").decode("utf-8", "replace")


def result_span(text: str) -> frozenset[str]:
    return frozenset(line for line in text.splitlines() if RESULT_SPAN_RE.search(line))


def has_pending_marker(text: str) -> bool:
    """A pending marker line: the word ``pending`` outside the receipt's own name line.

    The name line (``# receipt: <file name>``) is excluded so that a file called
    ``pending.txt`` does not keep every later version looking pending.
    """
    for line in text.splitlines():
        if RECEIPT_HEADER_RE.match(line):
            continue
        if PENDING_RE.search(line):
            return True
    return False


def segments_of(ops: list[tuple[str, str, str]]) -> list[list[tuple[str, str]]]:
    """Split a path's blob changes into contiguous present-segments of (commit, blob)."""
    segments: list[list[tuple[str, str]]] = []
    current: list[tuple[str, str]] = []
    for commit, status, blob in ops:
        if status in ("A", "C", "R"):
            if current:
                segments.append(current)
            current = [(commit, blob)]
        elif status == "D":
            if current:
                segments.append(current)
            current = []
        elif current:
            current.append((commit, blob))
        else:
            current = [(commit, blob)]
    if current:
        segments.append(current)
    return segments


# --------------------------------------------------------------------------- disclosures

def normalise_path(path: str) -> str:
    text = path.strip().replace("\\", "/")
    while text.startswith("./"):
        text = text[2:]
    return posixpath.normpath(text) if text else text


def parse_disclosures(raw: bytes) -> list[dict[str, str]]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Unevaluable(f"disclosures are not UTF-8 ({exc.reason})")
    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise Unevaluable(f"disclosures are not JSON ({exc.msg})")
    if not isinstance(document, dict):
        raise Unevaluable("disclosures are not a JSON object")
    schema = document.get("schema")
    if schema is not None and schema != DISCLOSURES_SCHEMA:
        raise Unevaluable(f"disclosures schema {schema!r} is not {DISCLOSURES_SCHEMA}")
    entries = document.get("entries")
    if not isinstance(entries, list):
        raise Unevaluable("disclosures entries is not a list")
    parsed: list[dict[str, str]] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise Unevaluable(f"disclosures entry {index} is not an object")
        path = entry.get("path")
        commit = entry.get("commit")
        if not isinstance(path, str) or not path.strip():
            raise Unevaluable(f"disclosures entry {index} has no path")
        if not isinstance(commit, str) or not commit.strip():
            raise Unevaluable(f"disclosures entry {index} has no commit")
        kind = entry.get("kind")
        if kind is not None and not isinstance(kind, str):
            raise Unevaluable(f"disclosures entry {index} kind is not a string")
        parsed.append({"path": normalise_path(path), "commit": commit.strip().lower()})
    return parsed


def load_disclosures(root: str, revision: str, path_argument: str | None) -> list[dict[str, str]]:
    explicit = path_argument is not None
    given = path_argument if explicit else DEFAULT_DISCLOSURES
    text: bytes | None = None
    if not os.path.isabs(given):
        relative = normalise_path(given)
        rc, out = git(root, "cat-file", "blob", f"{revision}:{relative}")
        if rc == 0:
            text = out
    if text is None:
        candidate = given if os.path.isabs(given) else os.path.join(root, given)
        try:
            with open(candidate, "rb") as handle:
                text = handle.read()
        except FileNotFoundError:
            text = None
        except OSError as exc:
            raise Unevaluable(f"disclosures {candidate}: {exc.strerror or exc}")
    if text is None:
        if explicit:
            raise Unevaluable(f"disclosures {given}: not found at the revision or on disk")
        return []
    return parse_disclosures(text)


def commit_matches(entry_commit: str, commit: str) -> bool:
    if entry_commit == commit:
        return True
    return 7 <= len(entry_commit) < len(commit) and commit.startswith(entry_commit)


# --------------------------------------------------------------------------- evaluation

def path_events(path: str, segments: list[list[tuple[str, str]]],
                blobs: dict[str, bytes]) -> list[dict[str, str]]:
    """Events for one receipt path, ordered by commit."""
    first_text = decode(blobs.get(segments[0][0][1]))
    pending_active = has_pending_marker(first_text)
    events: list[dict[str, str]] = []
    for segment in segments:
        previous_span = result_span(decode(blobs.get(segment[0][1])))
        for commit, blob in segment[1:]:
            text = decode(blobs.get(blob))
            span = result_span(text)
            if pending_active and not has_pending_marker(text):
                kind = "pending_filled"
                pending_active = False
            elif span != previous_span:
                kind = "rewrite"
            else:
                kind = None
            if kind:
                events.append({"path": path, "commit": commit, "kind": kind})
            previous_span = span
    return events


def evaluate(root: str, revision: str, disclosures_path: str | None) -> dict:
    root_real = os.path.realpath(os.path.abspath(root))
    if not os.path.isdir(root_real):
        raise Unevaluable(f"--root {root}: not a directory")
    top = toplevel(root_real)
    if top is None:
        raise Unevaluable(f"--root {root}: not a git repository")
    if top != root_real:
        raise Unevaluable(f"--root {root}: not a repository toplevel (toplevel is {top})")
    commit = resolve_commit(root_real, revision)
    if commit is None:
        raise Unevaluable(f"--revision {revision}: not a resolvable commit")

    paths, skipped = population(root_real, commit)
    ops = walk_changes(root_real, commit, paths)
    blobs = read_blobs(root_real, [blob for path in paths for _, _, blob in ops.get(path, [])])

    receipts = 0
    events: list[dict[str, str]] = []
    for path in paths:
        segments = segments_of(ops.get(path, []))
        if not segments:
            continue
        if not RECEIPT_GRAMMAR_RE.search(decode(blobs.get(segments[0][0][1]))):
            continue
        receipts += 1
        events.extend(path_events(path, segments, blobs))

    entries = load_disclosures(root_real, commit, disclosures_path)
    matched = [False] * len(entries)
    for event in events:
        event["disclosed"] = False
        for index, entry in enumerate(entries):
            if entry["path"] == normalise_path(event["path"]) and \
                    commit_matches(entry["commit"], event["commit"]):
                event["disclosed"] = True
                matched[index] = True

    findings: list[dict[str, str]] = []
    for event in events:
        if not event["disclosed"]:
            findings.append({"kind": f"undisclosed_{event['kind']}", "path": event["path"],
                             "commit": event["commit"]})
    for index, entry in enumerate(entries):
        if not matched[index]:
            findings.append({"kind": "phantom_disclosure", "path": entry["path"],
                             "commit": entry["commit"]})

    undisclosed = sum(1 for event in events if not event["disclosed"])
    met = undisclosed == 0
    summary = (f"receipts={receipts} events={len(events)} undisclosed={undisclosed} "
               f"met={met}")
    return {
        "version": 1,
        "root": root_real,
        "revision": commit,
        "population": len(paths),
        "receipts": receipts,
        "events": events,
        "undisclosed": undisclosed,
        "met": met,
        "findings": findings,
        "finding_lines": [f"{finding['kind']} {finding['path']} {finding['commit']}"
                          for finding in findings],
        "summary": summary,
        "skipped": skipped,
    }


def render(report: dict, as_json: bool) -> str:
    if as_json:
        return json.dumps(report, indent=2, sort_keys=True)
    lines = [f"{finding['kind']} {finding['path']} {finding['commit']}"
             for finding in report["findings"]]
    lines.append(report["summary"])
    return "\n".join(lines)


# --------------------------------------------------------------------------- self-test

class Fixture:
    """One scratch repository.  Every git call names -C so no ambient repo is touched."""

    IDENTITY = ("-c", "user.name=selftest", "-c", "user.email=selftest@local",
                "-c", "commit.gpgsign=false", "-c", "gc.auto=0")

    def __init__(self, base: str, name: str) -> None:
        self.dir = tempfile.mkdtemp(prefix=f"lineage-{name}-", dir=base)
        self.git("init", "-q")

    def git(self, *args: str) -> str:
        proc = subprocess.run(["git", "-C", self.dir, *self.IDENTITY, *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=dict(git_env(), GIT_CONFIG_GLOBAL="/dev/null",
                                       GIT_CONFIG_NOSYSTEM="1"),
                              timeout=120)
        if proc.returncode != 0:
            raise RuntimeError("fixture git %s failed: %s" % (
                " ".join(args), proc.stderr.decode("utf-8", "replace").strip()))
        return proc.stdout.decode("utf-8", "replace")

    def is_own_toplevel(self) -> bool:
        rc = subprocess.run(["git", "-C", self.dir, "rev-parse", "--show-toplevel"],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                            env=git_env(), timeout=60).stdout.decode().strip()
        return os.path.realpath(rc) == os.path.realpath(self.dir)

    def write(self, relative: str, text: str) -> None:
        target = os.path.join(self.dir, relative)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(text)

    def remove(self, relative: str) -> None:
        os.remove(os.path.join(self.dir, relative))

    def commit(self, message: str) -> str:
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", message)
        return self.head()

    def head(self) -> str:
        return self.git("rev-parse", "HEAD").strip()


def run_tool(arguments: list[str], env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    env = git_env()
    env["PYTHONHASHSEED"] = "0"
    if env_extra:
        env.update(env_extra)
    return subprocess.run([sys.executable, "-B", os.path.abspath(__file__), *arguments],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                          env=env, timeout=300)


def selftest() -> int:
    failures: list[str] = []
    checked = 0

    def expect(case: str, condition: bool, detail: str = "") -> None:
        nonlocal checked
        checked += 1
        if condition:
            print(f"PASS {case}")
        else:
            failures.append(case)
            print(f"FAIL {case}" + (f": {detail}" if detail else ""))

    base = tempfile.mkdtemp(prefix="receipt-lineage-selftest-")
    counter = [0]

    def round_dir() -> str:
        counter[0] += 1
        return f".ufo/waves/round-{40 + counter[0]}/controls"

    receipt_lines = ("# receipt: {name}\n  revision: {revision}\nEXIT=0\n"
                     "  cases_passed=3/3\nmet=True\n")

    def new_receipt(fixture: Fixture, directory: str, name: str = "r.txt",
                    revision: str = "aaaa1111", extra: str = "") -> str:
        path = f"{directory}/{name}"
        fixture.write(path, receipt_lines.format(name=name, revision=revision) + extra)
        return path

    def summary_of(proc: subprocess.CompletedProcess) -> str:
        lines = [line for line in proc.stdout.splitlines() if line.startswith("receipts=")]
        return lines[-1] if lines else ""

    try:
        # --- gate: every fixture is its own repository toplevel ------------------------------
        gate = Fixture(base, "gate")
        expect("gate fixture toplevel", gate.is_own_toplevel(), gate.dir)

        # L1 -- a clean receipt is never a finding.
        fixture = Fixture(base, "clean")
        directory = round_dir()
        path = new_receipt(fixture, directory)
        fixture.commit("add receipt")
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L1 clean receipt exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
        expect("L1 clean summary",
               summary_of(proc) == "receipts=1 events=0 undisclosed=0 met=True", summary_of(proc))

        # L2 -- undisclosed result-line rewrite.
        fixture = Fixture(base, "rewrite")
        directory = round_dir()
        path = new_receipt(fixture, directory)
        fixture.commit("add receipt")
        fixture.write(path, receipt_lines.format(name="r.txt", revision="bbbb2222"))
        rewritten = fixture.commit("relabel revision")
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L2 rewrite exit 1", proc.returncode == 1, proc.stdout + proc.stderr)
        expect("L2 rewrite finding",
               f"undisclosed_rewrite {path} {rewritten}" in proc.stdout, proc.stdout)
        expect("L2 rewrite summary",
               summary_of(proc) == "receipts=1 events=1 undisclosed=1 met=False", summary_of(proc))

        # L2b -- the same rewrite, disclosed through an explicit disclosures file.
        disclosures = os.path.join(base, "disclosures-abs.json")
        with open(disclosures, "w", encoding="utf-8") as handle:
            json.dump({"schema": DISCLOSURES_SCHEMA, "entries": [
                {"path": path, "commit": rewritten, "kind": "rewrite", "note": "selftest",
                 "disclosed-by": "selftest"}]}, handle)
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD", "--disclosures", disclosures])
        expect("L3 disclosed rewrite exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
        expect("L3 disclosed rewrite summary",
               summary_of(proc) == "receipts=1 events=1 undisclosed=0 met=True", summary_of(proc))

        # L3b -- disclosed through the default path, read as the committed blob.
        fixture = Fixture(base, "rewrite-committed-disclosure")
        directory = round_dir()
        path = new_receipt(fixture, directory)
        fixture.commit("add receipt")
        fixture.write(path, receipt_lines.format(name="r.txt", revision="cccc3333"))
        rewritten = fixture.commit("relabel revision")
        fixture.write(DEFAULT_DISCLOSURES, json.dumps(
            {"schema": DISCLOSURES_SCHEMA,
             "entries": [{"path": path, "commit": rewritten, "kind": "rewrite", "note": "x",
                          "disclosed-by": "selftest"}]}))
        fixture.commit("disclose")
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L3b committed default disclosure exit 0", proc.returncode == 0,
               proc.stdout + proc.stderr)
        expect("L3b committed default summary",
               summary_of(proc) == "receipts=1 events=1 undisclosed=0 met=True", summary_of(proc))

        # L4 -- a rewrite of a NON-result body line only is not an event.
        fixture = Fixture(base, "body-rewrite")
        directory = round_dir()
        path = new_receipt(fixture, directory, extra="a note about the run\n")
        fixture.commit("add receipt")
        fixture.write(path, receipt_lines.format(name="r.txt", revision="aaaa1111")
                      + "the note now reads differently\n")
        fixture.commit("reword the note")
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L4 body rewrite exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
        expect("L4 body rewrite summary",
               summary_of(proc) == "receipts=1 events=0 undisclosed=0 met=True", summary_of(proc))

        # L5 -- a population file that is not a receipt may be rewritten freely.
        fixture = Fixture(base, "non-receipt")
        directory = round_dir()
        path = f"{directory}/notes.txt"
        fixture.write(path, "round notes, first draft\n")
        fixture.commit("add notes")
        fixture.write(path, "round notes, second draft\n")
        fixture.commit("rewrite notes")
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L5 non-receipt rewrite exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
        expect("L5 non-receipt summary",
               summary_of(proc) == "receipts=0 events=0 undisclosed=0 met=True", summary_of(proc))

        # L6 -- the final summary line flips met=False -> met=True, undisclosed.
        fixture = Fixture(base, "met-flip")
        directory = round_dir()
        path = new_receipt(fixture, directory)
        fixture.write(path, receipt_lines.format(name="r.txt", revision="aaaa1111")
                      .replace("met=True", "met=False"))
        fixture.commit("add receipt")
        path2 = new_receipt(fixture, directory)
        flipped = fixture.commit("flip met")
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L6 met flip exit 1", proc.returncode == 1, proc.stdout + proc.stderr)
        expect("L6 met flip finding",
               f"undisclosed_rewrite {path2} {flipped}" in proc.stdout, proc.stdout)

        # L7 -- a pending receipt filled later, undisclosed (bare marker line, as round 57).
        fixture = Fixture(base, "pending")
        directory = round_dir()
        path = f"{directory}/pending.txt"
        fixture.write(path, "pending\n  revision: aaaa1111\nEXIT=0\nmet=pending\n")
        fixture.commit("commit the pending receipt")
        fixture.write(path, "# receipt: pending.txt\n  revision: aaaa1111\nEXIT=0\n"
                            "  cases_passed=3/3\nmet=True\n")
        filled = fixture.commit("fill the receipt")
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L7 pending fill exit 1", proc.returncode == 1, proc.stdout + proc.stderr)
        expect("L7 pending fill finding",
               f"undisclosed_pending_filled {path} {filled}" in proc.stdout, proc.stdout)
        expect("L7 pending summary",
               summary_of(proc) == "receipts=1 events=1 undisclosed=1 met=False", summary_of(proc))

        # L8 -- the same fill, disclosed.
        disclosures = os.path.join(base, "disclosures-pending.json")
        with open(disclosures, "w", encoding="utf-8") as handle:
            json.dump({"entries": [{"path": path, "commit": filled, "kind": "pending_filled",
                                    "note": "selftest", "disclosed-by": "selftest"}]}, handle)
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD", "--disclosures", disclosures])
        expect("L8 disclosed fill exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
        expect("L8 disclosed fill summary",
               summary_of(proc) == "receipts=1 events=1 undisclosed=0 met=True", summary_of(proc))

        # L9 -- two sequential rewrites, one disclosed, one not.
        fixture = Fixture(base, "two-rewrites")
        directory = round_dir()
        path = new_receipt(fixture, directory)
        fixture.commit("add receipt")
        fixture.write(path, receipt_lines.format(name="r.txt", revision="bbbb2222"))
        first = fixture.commit("first relabel")
        fixture.write(path, receipt_lines.format(name="r.txt", revision="cccc3333"))
        second = fixture.commit("second relabel")
        disclosures = os.path.join(base, "disclosures-two.json")
        with open(disclosures, "w", encoding="utf-8") as handle:
            json.dump({"entries": [{"path": path, "commit": first, "kind": "rewrite",
                                    "note": "first", "disclosed-by": "selftest"}]}, handle)
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD", "--disclosures", disclosures])
        expect("L9 two rewrites exit 1", proc.returncode == 1, proc.stdout + proc.stderr)
        expect("L9 one finding",
               proc.stdout.count("undisclosed_rewrite") == 1
               and f"undisclosed_rewrite {path} {second}" in proc.stdout, proc.stdout)
        expect("L9 summary",
               summary_of(proc) == "receipts=1 events=2 undisclosed=1 met=False", summary_of(proc))

        # L10 -- a pure reordering of result lines is not a rewrite (set semantics).
        fixture = Fixture(base, "reorder")
        directory = round_dir()
        path = f"{directory}/order.txt"
        fixture.write(path, "# receipt: order.txt\nEXIT=0\nmet=True\n")
        fixture.commit("add receipt")
        fixture.write(path, "# receipt: order.txt\nmet=True\nEXIT=0\n")
        fixture.commit("reorder result lines")
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L10 reorder exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
        expect("L10 reorder summary",
               summary_of(proc) == "receipts=1 events=0 undisclosed=0 met=True", summary_of(proc))

        # L11 -- malformed disclosures JSON is could-not-evaluate.
        for label, payload in (("truncated", '{"entries": [{"path": "a"}'),
                               ("entries-not-list", '{"entries": {}}'),
                               ("entry-without-commit", '{"entries": [{"path": "a"}]}'),
                               ("wrong-schema", '{"schema": "other", "entries": []}')):
            bad = os.path.join(base, f"disclosures-bad-{label}.json")
            with open(bad, "w", encoding="utf-8") as handle:
                handle.write(payload)
            proc = run_tool(["--root", fixture.dir, "--revision", "HEAD", "--disclosures", bad])
            expect(f"L11 malformed disclosures ({label}) exit 2", proc.returncode == 2,
                   proc.stdout + proc.stderr)

        # L12 -- an entry that names no event is a phantom disclosure.
        fixture = Fixture(base, "phantom")
        directory = round_dir()
        path = new_receipt(fixture, directory)
        head = fixture.commit("add receipt")
        disclosures = os.path.join(base, "disclosures-phantom.json")
        with open(disclosures, "w", encoding="utf-8") as handle:
            json.dump({"entries": [{"path": path, "commit": head, "kind": "rewrite",
                                    "note": "no event", "disclosed-by": "selftest"}]}, handle)
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD", "--disclosures", disclosures])
        expect("L12 phantom exit 1", proc.returncode == 1, proc.stdout + proc.stderr)
        expect("L12 phantom finding", f"phantom_disclosure {path} {head}" in proc.stdout,
               proc.stdout)
        expect("L12 phantom met is True (undisclosed==0)",
               summary_of(proc) == "receipts=1 events=0 undisclosed=0 met=True", summary_of(proc))

        # L13 -- a rewrite after the revision under test is out of range.
        fixture = Fixture(base, "range")
        directory = round_dir()
        path = new_receipt(fixture, directory)
        clean = fixture.commit("add receipt")
        fixture.write(path, receipt_lines.format(name="r.txt", revision="bbbb2222"))
        fixture.commit("relabel after the measured revision")
        proc = run_tool(["--root", fixture.dir, "--revision", clean])
        expect("L13 range bound exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
        expect("L13 range bound summary",
               summary_of(proc) == "receipts=1 events=0 undisclosed=0 met=True", summary_of(proc))

        # L14 -- an unresolved revision, and a revision that looks like an option.
        for label, revision in (("unresolved", "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"),
                                ("dash", "-x")):
            proc = run_tool(["--root", fixture.dir, f"--revision={revision}"])
            expect(f"L14 {label} revision exit 2", proc.returncode == 2, proc.stdout + proc.stderr)

        # L15 -- an empty population is clean.
        fixture = Fixture(base, "empty-population")
        fixture.write("README.md", "no controls here\n")
        fixture.commit("add readme")
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L15 empty population exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
        expect("L15 empty population summary",
               summary_of(proc) == "receipts=0 events=0 undisclosed=0 met=True", summary_of(proc))

        # L16 -- --root must be a repository toplevel.
        fixture = Fixture(base, "not-toplevel")
        directory = round_dir()
        new_receipt(fixture, directory)
        fixture.commit("add receipt")
        nested = os.path.join(fixture.dir, ".ufo")
        proc = run_tool(["--root", nested, "--revision", "HEAD"])
        expect("L16 nested root exit 2", proc.returncode == 2, proc.stdout + proc.stderr)
        outside = tempfile.mkdtemp(prefix="lineage-plain-", dir=base)
        proc = run_tool(["--root", outside, "--revision", "HEAD"])
        expect("L16 non-repository root exit 2", proc.returncode == 2, proc.stdout + proc.stderr)

        # L17 -- usage errors are exit 64.
        for label, arguments in (("no arguments", []),
                                 ("root only", ["--root", fixture.dir]),
                                 ("revision only", ["--revision", "HEAD"]),
                                 ("unknown option", ["--root", fixture.dir, "--revision", "HEAD",
                                                     "--nonsense"]),
                                 ("selftest plus arguments", ["--selftest", "--root", fixture.dir])):
            proc = run_tool(arguments)
            expect(f"L17 usage exit 64 ({label})", proc.returncode == 64,
                   f"rc={proc.returncode} {proc.stderr[:120]}")

        # L18 -- inherited GIT_* variables are scrubbed.
        fixture = Fixture(base, "git-env")
        directory = round_dir()
        path = new_receipt(fixture, directory)
        fixture.commit("add receipt")
        fixture.write(path, receipt_lines.format(name="r.txt", revision="bbbb2222"))
        rewritten = fixture.commit("relabel revision")
        poisoned = {"GIT_DIR": "/nonexistent-lineage-selftest",
                    "GIT_WORK_TREE": "/nonexistent-lineage-selftest",
                    "GIT_INDEX_FILE": "/nonexistent-lineage-selftest/index",
                    "GIT_OBJECT_DIRECTORY": "/nonexistent-lineage-selftest/objects",
                    "GIT_CEILING_DIRECTORIES": "/nonexistent-lineage-selftest"}
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"], poisoned)
        expect("L18 poisoned GIT_* exit 1", proc.returncode == 1, proc.stdout + proc.stderr)
        expect("L18 poisoned GIT_* finding",
               f"undisclosed_rewrite {path} {rewritten}" in proc.stdout, proc.stdout)

        # L19 -- a rename ends the path's history; the new path is its own first commit.
        fixture = Fixture(base, "rename")
        directory = round_dir()
        old = f"{directory}/old.txt"
        new = f"{directory}/new.txt"
        new_receipt(fixture, directory, name="old.txt")
        fixture.commit("add receipt")
        fixture.git("mv", old, new)
        moved = fixture.commit("rename the receipt")
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L19 rename exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
        expect("L19 rename summary",
               summary_of(proc) == "receipts=1 events=0 undisclosed=0 met=True", summary_of(proc))

        # L20 -- a delete followed by a re-add starts a new segment.
        fixture = Fixture(base, "delete-readd")
        directory = round_dir()
        path = new_receipt(fixture, directory)
        fixture.commit("add receipt")
        fixture.remove(path)
        fixture.commit("delete the receipt")
        new_receipt(fixture, directory, revision="dddd4444")
        fixture.commit("re-add the receipt")
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L20 delete/readd exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
        expect("L20 delete/readd summary",
               summary_of(proc) == "receipts=1 events=0 undisclosed=0 met=True", summary_of(proc))

        # L21 -- a merge commit is diffed against its first parent.
        fixture = Fixture(base, "merge")
        directory = round_dir()
        path = new_receipt(fixture, directory)
        fixture.commit("add receipt")
        fixture.git("checkout", "-q", "-b", "side")
        fixture.write(path, receipt_lines.format(name="r.txt", revision="eeee5555"))
        fixture.git("commit", "-q", "-am", "relabel on the side branch")
        fixture.git("checkout", "-q", "-")
        fixture.git("merge", "-q", "--no-ff", "--no-edit", "side")
        merged = fixture.head()
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L21 merge exit 1", proc.returncode == 1, proc.stdout + proc.stderr)
        expect("L21 merge finding", f"undisclosed_rewrite {path} {merged}" in proc.stdout,
               proc.stdout)
        expect("L21 merge summary",
               summary_of(proc) == "receipts=1 events=1 undisclosed=1 met=False", summary_of(proc))

        # L22 -- a non-blob population path is skipped with a named note.
        fixture = Fixture(base, "symlink")
        directory = round_dir()
        fixture.write(f"{directory}/target.txt", "not a receipt\n")
        os.symlink("target.txt", os.path.join(fixture.dir, directory, "link.txt"))
        fixture.commit("add a symlink")
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L22 symlink exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
        expect("L22 symlink note", "non-blob" in proc.stderr, proc.stderr)
        expect("L22 symlink summary",
               summary_of(proc) == "receipts=0 events=0 undisclosed=0 met=True", summary_of(proc))

        # L23 -- --json carries the frozen summary and the same findings.
        fixture = Fixture(base, "json")
        directory = round_dir()
        path = new_receipt(fixture, directory)
        fixture.commit("add receipt")
        fixture.write(path, receipt_lines.format(name="r.txt", revision="bbbb2222"))
        written = fixture.commit("relabel revision")
        plain = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        document = run_tool(["--root", fixture.dir, "--revision", "HEAD", "--json"])
        try:
            payload = json.loads(document.stdout)
        except json.JSONDecodeError as exc:
            payload = {}
            expect("L23 json parses", False, str(exc))
        else:
            expect("L23 json parses", True)
        expect("L23 json summary matches plain",
               payload.get("summary") == summary_of(plain), str(payload.get("summary")))
        expect("L23 json findings",
               payload.get("findings") == [{"kind": "undisclosed_rewrite", "path": path,
                                            "commit": written}], str(payload.get("findings")))
        expect("L23 json met False", payload.get("met") is False, str(payload.get("met")))
        expect("L23 json exit 1", document.returncode == 1, document.stdout[:200])

        # L24 -- the grammar alternatives: EXIT= alone and ^VERDICT: alone both make a receipt.
        fixture = Fixture(base, "grammar")
        directory = round_dir()
        fixture.write(f"{directory}/exit-only.txt", "some run\nEXIT=0\n")
        fixture.write(f"{directory}/verdict-only.txt", "VERDICT: met\n")
        fixture.write(f"{directory}/header-only.txt", "#  receipt :  spaced\n")
        fixture.write(f"{directory}/nothing.txt", "plain notes only\n")
        fixture.commit("add the four shapes")
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L24 grammar summary",
               summary_of(proc) == "receipts=3 events=0 undisclosed=0 met=True", summary_of(proc))

        # L25 -- pending in a body line only is still a fill (whole-version marker test),
        #        and a later version that still says pending is not yet a fill.
        fixture = Fixture(base, "pending-body")
        directory = round_dir()
        path = f"{directory}/pending-body.txt"
        fixture.write(path, "# receipt: p.txt\nnote: pending review\nEXIT=0\n")
        fixture.commit("add receipt with a pending note")
        fixture.write(path, "# receipt: p.txt\nnote: pending review\nEXIT=1\n")
        fixture.commit("change the exit code while still pending")
        still = fixture.head()
        fixture.write(path, "# receipt: p.txt\nnote: reviewed\nEXIT=1\n")
        filled = fixture.commit("clear the pending marker")
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L25 still-pending rewrite counted as rewrite",
               f"undisclosed_rewrite {path} {still}" in proc.stdout, proc.stdout)
        expect("L25 pending cleared is a fill",
               f"undisclosed_pending_filled {path} {filled}" in proc.stdout, proc.stdout)
        expect("L25 pending-body summary",
               summary_of(proc) == "receipts=1 events=2 undisclosed=2 met=False", summary_of(proc))

        # L26 -- a receipt whose first version predates the window is not re-detected.
        fixture = Fixture(base, "only-first-version")
        directory = round_dir()
        fixture.write(f"{directory}/x.txt", "no grammar at all\n")
        fixture.commit("add a non-receipt")
        fixture.write(f"{directory}/x.txt", "# receipt: x.txt\nEXIT=0\n")
        fixture.commit("make it look like a receipt later")
        proc = run_tool(["--root", fixture.dir, "--revision", "HEAD"])
        expect("L26 later-grammar is not a receipt",
               summary_of(proc) == "receipts=0 events=0 undisclosed=0 met=True", summary_of(proc))
    finally:
        import shutil
        shutil.rmtree(base, ignore_errors=True)

    total = checked
    if failures:
        print(f"receipt_lineage selftest: {len(failures)} of {total} checks failed "
              f"({', '.join(failures)})", file=sys.stderr)
        print(f"FAIL {total - len(failures)}/{total}")
        return EXIT_FINDINGS
    print(f"receipt_lineage selftest: {total} checks passed")
    print(f"PASS {total}/{total}")
    return EXIT_CLEAN


# --------------------------------------------------------------------------- main

class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:  # usage errors -> exit 64
        self.print_usage(sys.stderr)
        print(f"{self.prog}: error: {message}", file=sys.stderr)
        self.exit(EXIT_USAGE)


def build_parser() -> Parser:
    parser = Parser(
        prog="receipt_lineage.py",
        description="detect undisclosed receipt rewrites in a lane's first-parent history")
    parser.add_argument("--root", help="lane repository toplevel")
    parser.add_argument("--revision", help="commit to measure (resolved to a commit)")
    parser.add_argument("--disclosures", help=f"disclosure registry (default {DEFAULT_DISCLOSURES})")
    parser.add_argument("--json", action="store_true", help="print one JSON document")
    parser.add_argument("--selftest", action="store_true", help="run the built-in self-tests")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.selftest:
        if args.root or args.revision or args.disclosures or args.json:
            parser.error("--selftest takes no other arguments")
        return selftest()
    if not args.root or not args.revision:
        parser.error("expected --root LANE and --revision REV, or --selftest")
    try:
        report = evaluate(args.root, args.revision, args.disclosures)
    except Unevaluable as exc:
        print(f"receipt_lineage: {exc}", file=sys.stderr)
        if args.json:
            print(json.dumps({"version": 1, "status": "could-not-evaluate",
                              "error": str(exc)}, indent=2, sort_keys=True))
        return EXIT_UNEVALUABLE
    for note in report["skipped"]:
        print(f"note: {note['reason']} {note['path']}", file=sys.stderr)
    print(render(report, args.json))
    return EXIT_FINDINGS if report["findings"] else EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(main())
