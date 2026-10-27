#!/usr/bin/env python3
"""Receipt-lineage watch: undisclosed rewrites of committed receipts (round 61, claim C1).

Usage:
  python3 -B scripts/receipt_lineage.py --root LANE --revision REV [--disclosures PATH] [--json]
  python3 -B scripts/receipt_lineage.py --selftest

The lane commits receipts (`# receipt: <name>` first line, `EXIT=` / `^VERDICT:` grammar)
and, twice in rounds 56 and 57, rewrote one after the fact: once by relabelling the
`revision:` line in a later commit, once by committing a `pending` receipt and filling it
in later. Only the external verifier noticed, because no committed check existed. This
tool is that check.

Surface: the population of receipt-bearing files committed at the measured revision under
a `control/` or `controls/` directory of the lane (either spelling, any depth of round
number, `.txt` or `.json` extension). The round-61 population is frozen by path list in
`.ufo/waves/round-61/controls/population-144.txt`; when a frozen list is committed at the
revision under test the tool walks exactly that list (the counter, not the tool, owns
`member_changed` / `member_missing` / `extra_member` against the path rule), otherwise it
derives the population from the path rule alone.

Read-only: every byte comes from the commit graph through plumbing
(`git rev-list --first-parent`, `git ls-tree`, `git cat-file`); the worktree is never
read, no ref is written, no lock is taken. The inherited `GIT_*` environment is scrubbed
before any git call, so `GIT_DIR`/`GIT_WORK_TREE`/`GIT_OBJECT_DIRECTORY` from the caller
cannot redirect the walk. `--root` must be a repository toplevel.

Rules (frozen in contract § Claim C1):
  * receipt detection: a population member is a receipt when its FIRST committed version
    carries a receipt grammar line (`(?im)^\\s*#\\s*receipt\\s*:` or `EXIT=` or `^VERDICT:`).
    Other population members are never findings, however often they are rewritten.
  * history walk: for each receipt, every first-parent commit after the commit that first
    added the file, through the revision under test, whose tree holds a different blob for
    that path than the commit's first parent is an event candidate. Renames are not
    followed (a rename ends the lineage; the new path is its own first-added commit), and
    a delete/re-add opens a new lineage at the re-add.
  * result span: the lines of a version matching
    `(?im)(^#\\s*receipt\\s*:|revision\\s*[:=]|EXIT\\s*=|met\\s*=|conditions_passed|`
    `cases_passed|findings\\s*=|scores_held|members\\s*=)`.
  * rewrite: an event candidate whose child result span differs from the parent's.
  * pending_filled: the first version's result span contains the word `pending` and a later
    version's span does not; the event lands on the first such later commit (that commit
    is classified `pending_filled` once, never also as `rewrite`).
  * disclosure: an event is disclosed when the disclosures JSON (schema
    `kake-receipt-disclosures-v1`, `{"entries": [{path, commit, kind, note, disclosed-by}]}`)
    holds an entry with equal `path` and `commit` (a hex `commit` of >= 7 characters also
    matches as a prefix). Malformed JSON or schema -> exit 2. An entry that names no event
    is the finding `phantom_disclosure`.
  * met: `undisclosed == 0` over the walked range.

Output: one finding per line `<kind> <path> <commit>`, then the summary line
`receipts=<n> events=<k> undisclosed=<m> met=<bool>`. Exits: 0 clean, 1 findings,
2 could-not-evaluate (revision unresolved, root not a toplevel, malformed disclosures,
git failure), 64 usage.

`--selftest` builds its own fixture repositories under TMPDIR, runs this script as a black
box over them and prints a PASS/FAIL tally. It never touches the lane.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_UNEVALUABLE = 2
EXIT_USAGE = 64

TOOL = "receipt_lineage.py"
DEFAULT_DISCLOSURES = ".ufo/receipt-disclosures.json"
DISCLOSURES_SCHEMA = "kake-receipt-disclosures-v1"

# Population path rule: a file whose path holds a `control` or `controls` component,
# at any depth, with a `.txt` or `.json` extension. (Round-61's frozen list includes
# nested forms such as `.ufo/waves/round-37/retained/controls/c2/*.json` and
# `.ufo/waves/round-48/assimilation/validate/.ufo/...`, so the rule cannot require the
# `control` component to sit directly under `round-<N>/`.)
POPULATION_RX = re.compile(r"(?i)^(?:.*/)?control(?:s)?/(?:.*/)?[^/]+\.(?:txt|json)$")

# A frozen population list, e.g. `.ufo/waves/round-61/controls/population-144.txt`.
FROZEN_RX = re.compile(r"(?i)^\.ufo/waves/round-([0-9]+)/controls/population-([0-9]+)\.txt$")

RECEIPT_RX = re.compile(r"(?im)^\s*#\s*receipt\s*:|EXIT=|^VERDICT:")
RESULT_RX = re.compile(
    r"(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed"
    r"|cases_passed|findings\s*=|scores_held|members\s*=)"
)
PENDING_RX = re.compile(r"(?i)\bpending\b")
HEX_RX = re.compile(r"(?i)^[0-9a-f]{7,40}$")

KIND_REWRITE = "rewrite"
KIND_PENDING = "pending_filled"
FINDING_UNDISCLOSED = {
    KIND_REWRITE: "undisclosed_rewrite",
    KIND_PENDING: "undisclosed_pending_filled",
}
FINDING_PHANTOM = "phantom_disclosure"


class Unevaluable(Exception):
    """The run cannot be evaluated; the caller exits 2 with this message."""


# --------------------------------------------------------------------------- git access


def git_env() -> dict[str, str]:
    """The inherited environment with every GIT_* variable removed.

    Scrub first (a caller's GIT_DIR must not redirect the walk), then re-add only the
    variables this tool wants: no optional locks, no terminal prompts, stable locale.
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["LC_ALL"] = "C"
    return env


def git(root: str, args: list[str], stdin: bytes | None = None) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            ["git", "-C", root, *args],
            input=stdin,
            capture_output=True,
            env=git_env(),
        )
    except OSError as exc:  # git binary missing or not executable
        raise Unevaluable(f"git unavailable: {exc.strerror}") from exc


def require_root(root: str) -> str:
    """`--root` must name a repository toplevel; return the resolved path."""
    real = os.path.realpath(root)
    if not os.path.isdir(real):
        raise Unevaluable(f"root is not a directory: {root}")
    probe = git(real, ["rev-parse", "--show-toplevel"])
    if probe.returncode != 0:
        raise Unevaluable(f"root is not a repository: {root}")
    top = probe.stdout.decode("utf-8", "surrogateescape").strip()
    if not top:
        raise Unevaluable(f"root is not a repository: {root}")
    if os.path.realpath(top) != real:
        raise Unevaluable(f"root is not a repository toplevel: {root} (toplevel is {top})")
    return real


def resolve_revision(root: str, revision: str) -> str:
    if not revision or revision.startswith("-"):
        raise Unevaluable(f"revision is not a plain revision name: {revision!r}")
    probe = git(root, ["rev-parse", "--verify", "--quiet", "--end-of-options", revision + "^{commit}"])
    sha = probe.stdout.decode("ascii", "replace").strip()
    if probe.returncode != 0 or len(sha) != 40:
        raise Unevaluable(f"revision does not resolve to a commit: {revision}")
    return sha


def first_parent_chain(root: str, sha: str) -> list[str]:
    out = git(root, ["rev-list", "--first-parent", "--reverse", sha])
    if out.returncode != 0:
        raise Unevaluable(f"rev-list failed for {sha}: {_first_line(out.stderr)}")
    chain = out.stdout.decode("ascii", "replace").split()
    if not chain:
        raise Unevaluable(f"rev-list returned no commits for {sha}")
    return chain


def tree_entries(root: str, sha: str) -> list[tuple[str, str, str, str]]:
    """(mode, type, oid, path) for every entry under the revision's tree."""
    out = git(root, ["ls-tree", "-r", "-z", "--full-tree", sha])
    if out.returncode != 0:
        raise Unevaluable(f"ls-tree failed for {sha}: {_first_line(out.stderr)}")
    entries: list[tuple[str, str, str, str]] = []
    for record in out.stdout.split(b"\0"):
        if not record:
            continue
        meta, _, raw_path = record.partition(b"\t")
        parts = meta.split()
        if len(parts) != 3:
            continue
        entries.append(
            (
                parts[0].decode("ascii", "replace"),
                parts[1].decode("ascii", "replace"),
                parts[2].decode("ascii", "replace"),
                raw_path.decode("utf-8", "surrogateescape"),
            )
        )
    return entries


def blob_text(root: str, oid: str) -> str:
    out = git(root, ["cat-file", "blob", oid])
    if out.returncode != 0:
        raise Unevaluable(f"cat-file failed for blob {oid}: {_first_line(out.stderr)}")
    return out.stdout.decode("utf-8", "replace")


def blob_matrix(root: str, chain: list[str], paths: list[str]) -> dict[str, list[str | None]]:
    """path -> blob oid (or None) at each commit of the first-parent chain, in order.

    One `git cat-file --batch-check` process answers every `commit:path` query, so the
    walk costs one object-database read per (path, commit) instead of one process each.
    """
    requests: list[str] = []
    for path in paths:
        for commit in chain:
            requests.append(f"{commit}:{path}")
    out = git(root, ["cat-file", "--batch-check"], stdin=("\n".join(requests) + "\n").encode())
    if out.returncode != 0:
        raise Unevaluable(f"cat-file --batch-check failed: {_first_line(out.stderr)}")
    lines = out.stdout.split(b"\n")
    if len(lines) < len(requests):
        raise Unevaluable("cat-file --batch-check returned fewer rows than requested")
    matrix: dict[str, list[str | None]] = {}
    index = 0
    for path in paths:
        row: list[str | None] = []
        for _ in chain:
            fields = lines[index].split()
            index += 1
            if len(fields) == 3 and fields[1] == b"blob":
                row.append(fields[0].decode("ascii", "replace"))
            else:
                row.append(None)  # missing, or not a blob (tree/commit/symlink target)
        matrix[path] = row
    return matrix


def _first_line(raw: bytes) -> str:
    text = raw.decode("utf-8", "replace").strip().splitlines()
    return text[0] if text else "(no message)"


# ------------------------------------------------------------------- rule evaluation


def result_span(text: str) -> tuple[str, ...]:
    """The result-relevant lines of one committed version, in file order."""
    return tuple(line.rstrip("\r") for line in text.splitlines() if RESULT_RX.search(line))


def is_receipt(text: str) -> bool:
    return RECEIPT_RX.search(text) is not None


def lineages(presence: list[str | None], chain: list[str]) -> list[list[tuple[str, str]]]:
    """Split one path's presence over the chain into runs of consecutive versions.

    A path absent at some commit and present again later starts a new lineage: the
    re-add is a first-added commit, exactly as a rename'd path is.
    """
    runs: list[list[tuple[str, str]]] = []
    current: list[tuple[str, str]] = []
    for commit, oid in zip(chain, presence):
        if oid is None:
            if current:
                runs.append(current)
                current = []
        else:
            current.append((commit, oid))
    if current:
        runs.append(current)
    return runs


def resolve_disclosures(spec: str, root: str) -> str:
    """Absolute path of the disclosure registry.

    An absolute spec is used as is; a relative spec that names an existing file relative
    to the caller's directory is used as given; anything else is resolved against the
    lane root, so the frozen default `.ufo/receipt-disclosures.json` means the lane's file
    however the caller's working directory happens to be set.
    """
    if os.path.isabs(spec):
        return spec
    if spec and os.path.exists(spec):
        return os.path.abspath(spec)
    return os.path.join(root, spec)


def load_disclosures(path: str) -> list[dict[str, str]]:
    """Read the disclosure registry. A missing file is an empty registry."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError as exc:
        raise Unevaluable(f"disclosures unreadable: {path}: {exc.strerror}") from exc
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Unevaluable(f"disclosures JSON malformed: {path}: {exc}") from exc
    if not isinstance(doc, dict):
        raise Unevaluable(f"disclosures JSON malformed: {path}: top level is not an object")
    schema = doc.get("schema")
    if schema is not None and schema != DISCLOSURES_SCHEMA:
        raise Unevaluable(f"disclosures schema is not {DISCLOSURES_SCHEMA}: {path}")
    entries = doc.get("entries")
    if not isinstance(entries, list):
        raise Unevaluable(f"disclosures JSON malformed: {path}: entries is not a list")
    clean: list[dict[str, str]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise Unevaluable(f"disclosures JSON malformed: {path}: entry is not an object")
        declared_path = entry.get("path")
        declared_commit = entry.get("commit")
        if not isinstance(declared_path, str) or not isinstance(declared_commit, str):
            raise Unevaluable(
                f"disclosures JSON malformed: {path}: entry needs string path and commit"
            )
        for key in ("kind", "note", "disclosed-by"):
            if key in entry and not isinstance(entry[key], str):
                raise Unevaluable(
                    f"disclosures JSON malformed: {path}: entry field {key} is not a string"
                )
        clean.append(
            {
                "path": declared_path,
                "commit": declared_commit.strip(),
                "kind": entry.get("kind", ""),
            }
        )
    return clean


def is_regular(mode: str, kind: str) -> bool:
    """A regular file entry: a blob that is neither a symlink nor a submodule.

    `git ls-tree` reports a symlink as a blob with mode 120000, so the mode is checked
    too: a population path that is a symlink or a submodule is not walked (named note).
    """
    return kind == "blob" and mode in ("100644", "100755")


def discover_frozen(
    root: str, entries: list[tuple[str, str, str, str]]
) -> tuple[str, list[str]] | None:
    """The newest committed frozen population list at the revision, if any."""
    candidates = []
    for mode, kind, oid, path in entries:
        match = FROZEN_RX.match(path)
        if match and is_regular(mode, kind):
            candidates.append((int(match.group(1)), int(match.group(2)), path, oid))
    if not candidates:
        return None
    candidates.sort()
    _round, _count, path, oid = candidates[-1]
    listed: list[str] = []
    for line in blob_text(root, oid).splitlines():
        item = line.strip()
        if not item or item.startswith("#"):
            continue
        listed.append(item)
    return path, listed


def evaluate(root: str, revision: str, disclosures_path: str) -> dict:
    """Run the lineage walk and return the report object."""
    real_root = require_root(root)
    disclosures_file = resolve_disclosures(disclosures_path, real_root)
    sha = resolve_revision(real_root, revision)
    chain = first_parent_chain(real_root, sha)
    entries = tree_entries(real_root, sha)
    notes: list[str] = []

    at_revision: dict[str, tuple[str, str, str]] = {}
    for mode, kind, oid, path in entries:
        at_revision[path] = (mode, kind, oid)

    regular = {path for path, (mode, kind, _oid) in at_revision.items() if is_regular(mode, kind)}
    by_rule = sorted(path for path in regular if POPULATION_RX.match(path))
    for path in sorted(at_revision):
        if POPULATION_RX.match(path) and path not in regular:
            mode, kind, _oid = at_revision[path]
            notes.append(f"skipped_non_blob {path} (mode {mode} {kind})")

    frozen = discover_frozen(real_root, entries)
    if frozen is None:
        population = by_rule
        source = "path-rule"
        frozen_path = ""
        missing: list[str] = []
    else:
        frozen_path, listed = frozen
        source = "frozen-list"
        population = [p for p in listed if p in regular]
        missing = [p for p in listed if p not in regular]
        for path in listed:
            if not POPULATION_RX.match(path):
                notes.append(f"member_outside_rule {path}")
        listed_set = set(listed)
        for path in by_rule:
            if path not in listed_set:
                notes.append(f"population_rule_extra {path}")

    walkable = [p for p in population if not any(ch in p for ch in ("\n", "\0", ":", " "))]
    for path in population:
        if path not in walkable:
            notes.append(f"skipped_unwalkable_path {path}")

    matrix = blob_matrix(real_root, chain, walkable) if walkable else {}

    texts: dict[str, str] = {}
    events: list[dict[str, str]] = []
    receipt_members = 0

    def body(oid: str) -> str:
        if oid not in texts:
            texts[oid] = blob_text(real_root, oid)
        return texts[oid]

    for path in walkable:
        for run in lineages(matrix[path], chain):
            first_text = body(run[0][1])
            if not is_receipt(first_text):
                continue
            receipt_members += 1
            first_span = result_span(first_text)
            fill_commit = None
            if PENDING_RX.search("\n".join(first_span)):
                for commit, oid in run[1:]:
                    if not PENDING_RX.search("\n".join(result_span(body(oid)))):
                        fill_commit = commit
                        break
            previous_oid = run[0][1]
            previous_span = first_span
            for commit, oid in run[1:]:
                span = result_span(body(oid))
                if oid != previous_oid and span != previous_span:
                    kind = KIND_PENDING if commit == fill_commit else KIND_REWRITE
                    events.append({"kind": kind, "path": path, "commit": commit})
                previous_oid, previous_span = oid, span

    disclosed = load_disclosures(disclosures_file)
    event_keys = {(event["path"], event["commit"]) for event in events}
    undisclosed_keys = set()
    findings: list[dict[str, str]] = []

    def match(entry: dict[str, str]) -> tuple[str, str] | None:
        path, commit = entry["path"], entry["commit"]
        if (path, commit) in event_keys:
            return (path, commit)
        if HEX_RX.match(commit):
            for event_path, event_commit in event_keys:
                if event_path == path and event_commit.startswith(commit.lower()):
                    return (event_path, event_commit)
        return None

    for event in events:
        key = (event["path"], event["commit"])
        disclosed_event = any(match(entry) == key for entry in disclosed)
        if not disclosed_event:
            undisclosed_keys.add(key)
            findings.append(
                {
                    "kind": FINDING_UNDISCLOSED[event["kind"]],
                    "path": event["path"],
                    "commit": event["commit"],
                }
            )

    for entry in disclosed:
        if match(entry) is None:
            findings.append(
                {"kind": FINDING_PHANTOM, "path": entry["path"], "commit": entry["commit"]}
            )

    findings.sort(key=lambda item: (item["kind"], item["path"], item["commit"]))
    undisclosed = len(undisclosed_keys)
    return {
        "version": 1,
        "root": real_root,
        "revision": sha,
        "population_source": source,
        "population_file": frozen_path,
        "population_members": len(population),
        "population_by_rule": len(by_rule),
        "receipt_grammar_members": receipt_members,
        "receipts": len(population),
        "events": len(events),
        "undisclosed": undisclosed,
        "met": undisclosed == 0,
        "findings": findings,
        "disclosures": disclosures_file,
        "notes": notes,
        "members_missing": missing,
    }


def render(report: dict, as_json: bool) -> str:
    if as_json:
        return json.dumps(report, indent=2, sort_keys=False) + "\n"
    lines = [f"{item['kind']} {item['path']} {item['commit']}" for item in report["findings"]]
    lines.append(
        "receipts={receipts} events={events} undisclosed={undisclosed} met={met}".format(
            receipts=report["receipts"],
            events=report["events"],
            undisclosed=report["undisclosed"],
            met="True" if report["met"] else "False",
        )
    )
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- CLI


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:  # usage error -> 64, per the frozen contract
        self.print_usage(sys.stderr)
        sys.stderr.write(f"{self.prog}: error: {message}\n")
        raise SystemExit(EXIT_USAGE)


def build_parser() -> argparse.ArgumentParser:
    parser = _Parser(prog=TOOL, description="Undisclosed receipt rewrites in the first-parent history.")
    parser.add_argument("--root", help="lane checkout; must be a repository toplevel")
    parser.add_argument("--revision", help="revision under test (resolved to a commit)")
    parser.add_argument(
        "--disclosures",
        default=DEFAULT_DISCLOSURES,
        help=f"disclosure registry JSON (default: {DEFAULT_DISCLOSURES})",
    )
    parser.add_argument("--json", action="store_true", help="print one JSON report object")
    parser.add_argument("--selftest", action="store_true", help="build fixtures under TMPDIR and self-test")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.root or not args.revision:
        sys.stderr.write(f"{TOOL}: --root and --revision are required (or --selftest)\n")
        return EXIT_USAGE
    try:
        report = evaluate(args.root, args.revision, args.disclosures)
    except Unevaluable as exc:
        sys.stderr.write(f"{TOOL}: could-not-evaluate: {exc}\n")
        return EXIT_UNEVALUABLE
    except Exception as exc:  # unforeseen: never a traceback, always exit 2
        sys.stderr.write(f"{TOOL}: could-not-evaluate: internal error: {type(exc).__name__}: {exc}\n")
        return EXIT_UNEVALUABLE
    for note in report["notes"]:
        sys.stderr.write(f"note: {note}\n")
    sys.stdout.write(render(report, args.json))
    return EXIT_CLEAN if not report["findings"] else EXIT_FINDINGS


# --------------------------------------------------------------------------- selftest


def _git(directory: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", directory, *args], capture_output=True, env=git_env())


def _fixture_repo(work: str, name: str) -> str:
    directory = os.path.join(work, name)
    os.makedirs(directory)
    probe = _git(directory, "init", "-q")
    assert probe.returncode == 0, probe.stderr.decode("utf-8", "replace")
    top = _git(directory, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(directory):
        raise RuntimeError(f"fixture toplevel mismatch: {top} != {directory}")
    return directory


def _commit(
    directory: str, files: dict[str, str], message: str, symlinks: dict[str, str] | None = None
) -> str:
    for relative, content in files.items():
        target = os.path.join(directory, relative)
        os.makedirs(os.path.dirname(target) or directory, exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(content)
    for relative, link_target in (symlinks or {}).items():
        target = os.path.join(directory, relative)
        os.makedirs(os.path.dirname(target) or directory, exist_ok=True)
        os.symlink(link_target, target)
    added = _git(directory, "add", "-A")
    if added.returncode != 0:
        raise RuntimeError(f"git add failed: {added.stderr.decode('utf-8', 'replace')}")
    committed = _git(
        directory,
        "-c",
        "user.name=selftest",
        "-c",
        "user.email=selftest@local",
        "commit",
        "-q",
        "-m",
        message,
    )
    if committed.returncode != 0:
        raise RuntimeError(f"git commit failed: {committed.stderr.decode('utf-8', 'replace')}")
    head = _git(directory, "rev-parse", "HEAD")
    return head.stdout.decode().strip()


def _run(
    root: str,
    revision: str,
    *extra: str,
    env_extra: dict[str, str] | None = None,
    cwd: str | None = None,
):
    env = {k: v for k, v in os.environ.items()}
    env.update(env_extra or {})
    return subprocess.run(
        [sys.executable, "-B", os.path.abspath(__file__), "--root", root, "--revision", revision, *extra],
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd,
    )


def _findings(stdout: str) -> list[str]:
    return [line for line in stdout.splitlines() if not line.startswith("receipts=")]


def _summary(stdout: str) -> dict[str, str]:
    for line in stdout.splitlines():
        if line.startswith("receipts="):
            fields = {}
            for token in line.split():
                key, _, value = token.partition("=")
                fields[key] = value
            return fields
    return {}


RECEIPT_HEAD = "# receipt: {name}\nrevision: {revision}\n"


def selftest() -> int:
    base = os.environ.get("TMPDIR") or tempfile.gettempdir()
    if not os.path.isdir(base):
        base = tempfile.gettempdir()
    work = tempfile.mkdtemp(prefix="receipt-lineage-selftest-", dir=base)
    cases: list[tuple[str, bool, str]] = []

    def record(case: str, ok: bool, detail: str = "") -> None:
        cases.append((case, ok, detail))

    try:
        control = ".ufo/waves/round-99/controls"
        receipt = control + "/receipt.txt"

        # S01 clean receipt, never touched.
        repo = _fixture_repo(work, "s01")
        _commit(repo, {receipt: RECEIPT_HEAD.format(name="s01", revision="aaaa111")
                       + "body note: alpha\nEXIT=0\nmet=True\n"}, "add receipt")
        run = _run(repo, "HEAD")
        record("S01_clean_untouched", run.returncode == 0 and _findings(run.stdout) == []
               and _summary(run.stdout).get("receipts") == "1", run.stdout + run.stderr)

        # S02 undisclosed revision-line rewrite.
        repo = _fixture_repo(work, "s02")
        _commit(repo, {receipt: RECEIPT_HEAD.format(name="s02", revision="aaaa111") + "EXIT=0\n"}, "add")
        second = _commit(repo, {receipt: RECEIPT_HEAD.format(name="s02", revision="bbbb222") + "EXIT=0\n"}, "relabel")
        run = _run(repo, "HEAD")
        record("S02_undisclosed_revision_rewrite",
               run.returncode == 1 and _findings(run.stdout) == [f"undisclosed_rewrite {receipt} {second}"]
               and _summary(run.stdout).get("undisclosed") == "1"
               and _summary(run.stdout).get("met") == "False", run.stdout + run.stderr)

        # S03 same rewrite, disclosed.
        registry = os.path.join(work, "s03-disclosures.json")
        with open(registry, "w", encoding="utf-8") as handle:
            json.dump({"schema": DISCLOSURES_SCHEMA,
                       "entries": [{"path": receipt, "commit": second, "kind": "rewrite",
                                    "note": "relabel after the fact", "disclosed-by": "selftest"}]}, handle)
        run = _run(repo, "HEAD", "--disclosures", registry)
        record("S03_disclosed_rewrite", run.returncode == 0 and _findings(run.stdout) == []
               and _summary(run.stdout).get("undisclosed") == "0", run.stdout + run.stderr)

        # S04 non-result body line rewritten.
        repo = _fixture_repo(work, "s04")
        _commit(repo, {receipt: RECEIPT_HEAD.format(name="s04", revision="aaaa111") + "note: alpha\nEXIT=0\n"}, "add")
        _commit(repo, {receipt: RECEIPT_HEAD.format(name="s04", revision="aaaa111") + "note: beta\nEXIT=0\n"}, "prose")
        run = _run(repo, "HEAD")
        record("S04_non_result_body_rewrite", run.returncode == 0 and _findings(run.stdout) == [], run.stdout + run.stderr)

        # S05 non-receipt population member rewritten freely.
        repo = _fixture_repo(work, "s05")
        plain = control + "/plain.json"
        _commit(repo, {plain: '{"a": 1}\n'}, "add")
        _commit(repo, {plain: '{"a": 2}\n'}, "edit")
        run = _run(repo, "HEAD")
        record("S05_non_receipt_rewrite", run.returncode == 0 and _findings(run.stdout) == []
               and _summary(run.stdout).get("receipts") == "1", run.stdout + run.stderr)

        # S06 summary verdict flipped met=False -> met=True.
        repo = _fixture_repo(work, "s06")
        _commit(repo, {receipt: RECEIPT_HEAD.format(name="s06", revision="aaaa111") + "EXIT=1\nmet=False\n"}, "add")
        flipped = _commit(repo, {receipt: RECEIPT_HEAD.format(name="s06", revision="aaaa111") + "EXIT=1\nmet=True\n"}, "flip")
        run = _run(repo, "HEAD")
        record("S06_summary_flip", run.returncode == 1
               and _findings(run.stdout) == [f"undisclosed_rewrite {receipt} {flipped}"], run.stdout + run.stderr)

        # S07 pending receipt filled later, undisclosed.
        repo = _fixture_repo(work, "s07")
        _commit(repo, {receipt: RECEIPT_HEAD.format(name="s07", revision="aaaa111") + "EXIT=pending\n"}, "add pending")
        filled = _commit(repo, {receipt: RECEIPT_HEAD.format(name="s07", revision="aaaa111")
                                + "EXIT=0\nmet=True\n"}, "fill")
        run = _run(repo, "HEAD")
        record("S07_pending_filled_undisclosed",
               run.returncode == 1
               and _findings(run.stdout) == [f"undisclosed_pending_filled {receipt} {filled}"], run.stdout + run.stderr)

        # S08 same fill, disclosed.
        registry = os.path.join(work, "s08-disclosures.json")
        with open(registry, "w", encoding="utf-8") as handle:
            json.dump({"schema": DISCLOSURES_SCHEMA,
                       "entries": [{"path": receipt, "commit": filled, "kind": "pending_filled",
                                    "note": "filled later", "disclosed-by": "selftest"}]}, handle)
        run = _run(repo, "HEAD", "--disclosures", registry)
        record("S08_pending_filled_disclosed", run.returncode == 0 and _findings(run.stdout) == [], run.stdout + run.stderr)

        # S09 two rewrites, one disclosed, one not.
        repo = _fixture_repo(work, "s09")
        _commit(repo, {receipt: RECEIPT_HEAD.format(name="s09", revision="aaaa111") + "EXIT=0\n"}, "add")
        first_rewrite = _commit(repo, {receipt: RECEIPT_HEAD.format(name="s09", revision="bbbb222") + "EXIT=0\n"}, "r1")
        second_rewrite = _commit(repo, {receipt: RECEIPT_HEAD.format(name="s09", revision="bbbb222") + "EXIT=1\n"}, "r2")
        registry = os.path.join(work, "s09-disclosures.json")
        with open(registry, "w", encoding="utf-8") as handle:
            json.dump({"schema": DISCLOSURES_SCHEMA,
                       "entries": [{"path": receipt, "commit": first_rewrite, "kind": "rewrite",
                                    "note": "first", "disclosed-by": "selftest"}]}, handle)
        run = _run(repo, "HEAD", "--disclosures", registry)
        record("S09_two_rewrites_one_disclosed",
               run.returncode == 1
               and _findings(run.stdout) == [f"undisclosed_rewrite {receipt} {second_rewrite}"], run.stdout + run.stderr)

        # S10 rewrite only after the revision under test (range bound).
        repo = _fixture_repo(work, "s10")
        tested = _commit(repo, {receipt: RECEIPT_HEAD.format(name="s10", revision="aaaa111") + "EXIT=0\n"}, "add")
        _commit(repo, {receipt: RECEIPT_HEAD.format(name="s10", revision="bbbb222") + "EXIT=0\n"}, "later")
        run = _run(repo, tested)
        record("S10_range_bound", run.returncode == 0 and _findings(run.stdout) == [], run.stdout + run.stderr)

        # S11 empty population.
        repo = _fixture_repo(work, "s11")
        _commit(repo, {"docs/note.txt": "not a population path\n"}, "add")
        run = _run(repo, "HEAD")
        record("S11_empty_population", run.returncode == 0 and _summary(run.stdout).get("receipts") == "0"
               and _summary(run.stdout).get("events") == "0", run.stdout + run.stderr)

        # S12 malformed disclosures JSON -> exit 2.
        broken = os.path.join(work, "s12-disclosures.json")
        with open(broken, "w", encoding="utf-8") as handle:
            handle.write("{not json")
        run = _run(repo, "HEAD", "--disclosures", broken)
        record("S12_malformed_disclosures", run.returncode == 2, f"{run.returncode} {run.stdout}{run.stderr}")

        # S13 phantom disclosure (names a commit with no event).
        repo = _fixture_repo(work, "s13")
        clean_commit = _commit(repo, {receipt: RECEIPT_HEAD.format(name="s13", revision="aaaa111") + "EXIT=0\n"}, "add")
        registry = os.path.join(work, "s13-disclosures.json")
        with open(registry, "w", encoding="utf-8") as handle:
            json.dump({"schema": DISCLOSURES_SCHEMA,
                       "entries": [{"path": receipt, "commit": clean_commit, "kind": "rewrite",
                                    "note": "no event here", "disclosed-by": "selftest"}]}, handle)
        run = _run(repo, "HEAD", "--disclosures", registry)
        record("S13_phantom_disclosure", run.returncode == 1
               and _findings(run.stdout) == [f"phantom_disclosure {receipt} {clean_commit}"], run.stdout + run.stderr)

        # S14 unresolved revision -> exit 2.
        run = _run(repo, "0123456789abcdef0123456789abcdef01234567")
        record("S14_unresolved_revision", run.returncode == 2, f"{run.returncode} {run.stdout}{run.stderr}")

        # S15 root that is not a toplevel -> exit 2.
        run = _run(os.path.join(repo, "docs"), "HEAD")
        record("S15_root_not_toplevel", run.returncode == 2, f"{run.returncode} {run.stdout}{run.stderr}")

        # S16 usage error -> 64.
        run = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--revision", "HEAD"],
                             capture_output=True, text=True)
        record("S16_usage_exit_64", run.returncode == 64, f"{run.returncode} {run.stdout}{run.stderr}")

        # S17 non-blob population path (symlink) is skipped with a named note.
        repo = _fixture_repo(work, "s17")
        _commit(repo, {"payload/link-target.txt": "target\n"}, "add target")
        _commit(repo, {}, "add symlink", symlinks={control + "/link.txt": "../payload/link-target.txt"})
        run = _run(repo, "HEAD")
        record("S17_non_blob_skipped", run.returncode == 0 and _findings(run.stdout) == []
               and "skipped_non_blob" in run.stderr, run.stdout + run.stderr)

        # S18 inherited GIT_* variables cannot redirect the walk.
        repo = _fixture_repo(work, "s18")
        _commit(repo, {receipt: RECEIPT_HEAD.format(name="s18", revision="aaaa111") + "EXIT=0\n"}, "add")
        poisoned = {"GIT_DIR": "/nonexistent/git-dir", "GIT_WORK_TREE": "/nonexistent/worktree",
                    "GIT_OBJECT_DIRECTORY": "/nonexistent/objects"}
        run = _run(repo, "HEAD", env_extra=poisoned)
        record("S18_env_scrubbed", run.returncode == 0 and _summary(run.stdout).get("receipts") == "1",
               run.stdout + run.stderr)

        # S19 frozen population list bounds the walk; rule-only extras are noted, not walked.
        repo = _fixture_repo(work, "s19")
        listed_path = control + "/listed.txt"
        unlisted_path = control + "/unlisted.txt"
        _commit(repo, {
            listed_path: RECEIPT_HEAD.format(name="s19", revision="aaaa111") + "EXIT=0\n",
            unlisted_path: RECEIPT_HEAD.format(name="s19b", revision="aaaa111") + "EXIT=0\n",
            ".ufo/waves/round-61/controls/population-1.txt": listed_path + "\n",
        }, "add")
        _commit(repo, {unlisted_path: RECEIPT_HEAD.format(name="s19b", revision="bbbb222") + "EXIT=0\n"}, "rewrite extra")
        run = _run(repo, "HEAD")
        record("S19_frozen_list_bounds_walk", run.returncode == 0
               and _summary(run.stdout).get("receipts") == "1"
               and "population_rule_extra" in run.stderr, run.stdout + run.stderr)

        # S20 output is deterministic.
        first = _run(repo, "HEAD")
        again = _run(repo, "HEAD")
        record("S20_deterministic", first.stdout == again.stdout and first.returncode == again.returncode,
               first.stdout + again.stdout)

        # S21 a delete/re-add opens a new lineage (the re-add is a first-added commit).
        repo = _fixture_repo(work, "s21")
        _commit(repo, {receipt: RECEIPT_HEAD.format(name="s21", revision="aaaa111") + "EXIT=0\n"}, "add")
        os.remove(os.path.join(repo, receipt))
        _commit(repo, {}, "delete")
        _commit(repo, {receipt: RECEIPT_HEAD.format(name="s21", revision="cccc333") + "EXIT=0\n"}, "re-add")
        run = _run(repo, "HEAD")
        record("S21_readd_new_lineage", run.returncode == 0 and _findings(run.stdout) == [], run.stdout + run.stderr)

        # S22 JSON report carries the same numbers as the text summary.
        run = _run(repo, "HEAD", "--json")
        try:
            doc = json.loads(run.stdout)
        except json.JSONDecodeError:
            doc = {}
        record("S22_json_report", run.returncode == 0 and doc.get("receipts") == 1
               and doc.get("met") is True and doc.get("revision"), run.stdout + run.stderr)

        # S23 the frozen default registry is the lane's own file, whatever the caller's cwd.
        repo = _fixture_repo(work, "s23")
        _commit(repo, {receipt: RECEIPT_HEAD.format(name="s23", revision="aaaa111") + "EXIT=0\n"}, "add")
        rewrite = _commit(repo, {receipt: RECEIPT_HEAD.format(name="s23", revision="bbbb222") + "EXIT=0\n"}, "rewrite")
        _commit(repo, {".ufo/receipt-disclosures.json": json.dumps(
            {"schema": DISCLOSURES_SCHEMA,
             "entries": [{"path": receipt, "commit": rewrite, "kind": "rewrite",
                          "note": "default registry", "disclosed-by": "selftest"}]})}, "registry")
        run = _run(repo, "HEAD", cwd="/")
        record("S23_default_registry_root_relative",
               run.returncode == 0 and _findings(run.stdout) == [], run.stdout + run.stderr)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    failed = [case for case in cases if not case[1]]
    for name, ok, detail in cases:
        if ok:
            print(f"PASS {name}")
        else:
            print(f"FAIL {name}: {detail.strip().splitlines()[-1] if detail.strip() else '(no output)'}")
    print(f"selftest: {len(cases) - len(failed)}/{len(cases)} passed")
    return EXIT_CLEAN if not failed else EXIT_FINDINGS


if __name__ == "__main__":
    sys.exit(main())
