#!/usr/bin/env python3
"""c77_shonen_ledger.py — C1 counter, round 77 (kake), v2.

Reads committed bytes at one revision, classifies every ``SHONEN.md`` box from
``corpus/knowledge/shonen-ledger.json``, and prints exactly one line:

  C1 revision=<rev> boxes=<n> evidenced=<n> gap=<n> unexamined=<n> mismatches=<n> met=<true|false>

Frozen predicate, the same sentence in the ledger, this counter and the report:

  met  <=>  boxes == 4  and  unexamined == 0  and  mismatches == 0

Terms come from the frozen contract (`.ufo/waves/round-77/contract.md` §C1) as
amended by `.ufo/waves/round-77/amendment-1.md` (A11 frozen box scopes, A12 a
gap is a result) and `.ufo/waves/round-77/amendment-2.md` (A1 base arithmetic,
A2 checks are declarations, A3 exact observation comparison, A4 box range and
marker rules, A5 attack fixtures).  Where the contract's prose and the
amendments disagree, the amendments win; the disagreements are named inline.

Definitions implemented:

  box          a line of ``SHONEN.md`` matching ``^- \\[([ x~])\\] ``.
  ledger       ``corpus/knowledge/shonen-ledger.json``, schema
               ``shonen-ledger/v1``: ``rows[]``, one per box, each with
               ``box`` (1–4), ``marker`` (``" "`` | ``"~"`` | ``"x"``),
               ``status`` (``evidenced`` | ``gap``) and a non-empty ``checks``
               array; ``reason`` + ``flip`` non-empty when ``status=gap``;
               ``verifier`` (a named non-author) when ``marker="x"``.
  check        ``{"id", "kind", "path", "params", "observed"}`` — a
               declaration, never an executable (amendment 2 A2).  ``kind``
               must be one of ``KINDS``; anything else is a mismatch.  An
               optional ``holds`` is advisory only and is never read (A3).
  evidenced    row with ``status="evidenced"``, no mismatch, and every check's
               own verdict true (its ``count_at_least``/``no_match`` threshold
               included).  ``observed`` is re-derived from ``git show
               <rev>:<path>`` and compared token for token (A3).
  gap          row with ``status="gap"``, a non-empty ``reason`` and a
               non-empty ``flip``.  Examined, never evidenced (A12).
  unexamined   a box with no valid row, or a row with an empty ``checks``
               array, or a schema-invalid row.
  mismatch     (a) ``"~"``/``"x"`` with no row; ``" "`` over an evidenced row;
               ``"~"``/``"x"`` over a non-evidenced row; ``"x"`` without a
               verifier; a row whose own ``marker`` disagrees with the
               checklist; (b) a check whose named ``path`` does not exist at
               ``<rev>``; (c) a second row for one box; (d) a re-derived
               observation that disagrees with the recorded ``observed``.
               Amendment 2 A2/A4 add: an unknown ``kind``; a row whose ``box``
               is not 1–4 (reported, never ignored); a schema-invalid row; and
               a ``status="evidenced"`` row carrying a check whose verdict is
               false (amendment 1 A12 says a failing frozen check makes the box
               a gap).  Amendment 2 A1 fixes the base arithmetic: a ``" "``
               marker with no row is *not* a mismatch, so the ledger-less base
               prints ``mismatches=0`` and the red is carried by
               ``unexamined=4``.

Check vocabulary (amendment 2 A2).  Any kind or measure outside these is a
mismatch, never a silent pass:

  exists            params {}                            observed bool
  count_at_least    params {"measure", "min", ...}       observed int, verdict count>=min
  regex_count       params {"pattern", "min"?}           observed int
  all_ids_resolve   params {"pattern", "resolve_path",   observed {ids, resolved,
                            "resolve_pattern"}             unresolved}
  no_match          params {"measure"|"pattern"}         observed int, verdict count==0

Measures (counter-implemented; the ledger names one, it never supplies code):

  markdown_tables_with_min_rows  params.min_rows   tables whose data-row count >= min_rows
  registry_rows_with_code_cell   —                 table rows with an exit map (0= and
                                                   1= in a cell) or a finding-id cell
  checklist_headings             —                 headings naming a checklist
  round_sections                 —                 ``## `` headings naming a round
  wave_receipt_paths             —                 distinct ``.ufo/waves/round-N/…``
                                                   path tokens that name a file
  wave_receipt_paths_missing     —                 of those, non-glob tokens absent at <rev>
  skill_script_paths_missing     —                 ``scripts/*.py|sh`` and
                                                   ``.ufo/waves/**/*.py`` tokens absent
  skill_python_invocations_missing —               ``python3 [-B] <path>`` invocations
                                                   naming an absent repo path
  cross_lane_citations           params.glob,       backticked tokens naming a sibling
                                 params.exclude      lane repository (``*-shokunin/``,
                                                     ``*-shokinin/``, ``kake-shokunin``
                                                     excluded) across the globbed files

Exit map: 0 met, 1 not met, 2 could-not-evaluate (unresolvable revision,
malformed or foreign-schema ledger, a check's auxiliary resolution file absent),
64 usage (``--root`` and ``--revision`` are required; there is no default to
``HEAD`` or the worktree — amendment 2 A4).

``--selftest`` builds isolated fixture trees under ``--work`` with git plumbing
only (``git init --bare``, ``hash-object -w``, ``update-index --cacheinfo``,
``write-tree``): no commit is created anywhere, so a fixture revision is a tree
object — exactly the shape a working-tree snapshot has when lane history must
not be written.  The self-test includes amendment 2 A5's six attack shapes
(02–07) plus a clean four-box fixture and the red/green controls for every
mismatch class.  ``--json`` appends the per-box derivation to stdout (the frozen
invocation passes no ``--json``, so stdout is then exactly one line).
"""
from __future__ import annotations

import argparse
import contextlib
import fnmatch
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

EXIT_MET = 0
EXIT_NOT_MET = 1
EXIT_UNEVALUABLE = 2
EXIT_USAGE = 64

CHECKLIST_PATH = "SHONEN.md"
LEDGER_PATH = "corpus/knowledge/shonen-ledger.json"
LEDGER_SCHEMA = "shonen-ledger/v1"

BOX_RE = re.compile(r"^- \[([ x~])\] (.*)$")
MARKERS = (" ", "~", "x")
STATUSES = ("evidenced", "gap")
BOX_RANGE = (1, 2, 3, 4)
LANE_SELF = "kake-shokunin"


class Unevaluable(Exception):
    """The derivation cannot be made from the named bytes."""


class UsageError(Exception):
    """Command-line misuse (exit 64)."""


# --------------------------------------------------------------------------
# git access — committed bytes only
# --------------------------------------------------------------------------
def _clean_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.setdefault("LC_ALL", "C.UTF-8")
    env.setdefault("LANG", "C.UTF-8")
    return env


class Repo:
    def __init__(self, root: str, git_dir: str | None = None):
        self.root = os.path.abspath(root)
        if git_dir:
            self.git_dir = os.path.abspath(git_dir)
        else:
            candidate = os.path.join(self.root, ".git")
            if not os.path.exists(candidate):
                raise Unevaluable(f"{self.root} holds no .git and no --git-dir was given")
            self.git_dir = candidate
        self._base = ["git", f"--git-dir={self.git_dir}", "--no-pager"]

    def _git(self, *args: str, stdin: bytes | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(self._base + list(args), input=stdin,
                              capture_output=True, env=_clean_env())

    def resolve(self, revision: str) -> str:
        proc = self._git("rev-parse", "--verify", "--end-of-options",
                         f"{revision}^{{object}}")
        if proc.returncode != 0 or not proc.stdout.strip():
            detail = proc.stderr.decode("utf-8", "replace").strip()
            raise Unevaluable(f"cannot resolve revision {revision!r}: {detail}")
        full = proc.stdout.decode("ascii", "replace").strip()
        kind = self._git("cat-file", "-t", full)
        kind_name = kind.stdout.decode("ascii", "replace").strip()
        if kind.returncode != 0 or kind_name not in ("commit", "tree"):
            raise Unevaluable(
                f"revision {revision!r} resolves to {kind_name or 'nothing'}, "
                "not a commit or tree")
        return full

    def show(self, rev: str, path: str) -> bytes | None:
        proc = self._git("show", f"{rev}:{path}")
        return proc.stdout if proc.returncode == 0 else None

    def show_text(self, rev: str, path: str) -> str | None:
        raw = self.show(rev, path)
        return None if raw is None else raw.decode("utf-8", "replace")

    def exists(self, rev: str, path: str) -> bool:
        return self._git("cat-file", "-e", f"{rev}:{path}").returncode == 0

    def list_tree(self, rev: str, prefix: str) -> list[str]:
        proc = self._git("ls-tree", "-r", "--name-only", rev, "--", prefix)
        if proc.returncode != 0:
            return []
        return [line for line in proc.stdout.decode("utf-8", "replace").splitlines()
                if line]


# --------------------------------------------------------------------------
# measures (counter-implemented)
# --------------------------------------------------------------------------
def _lines(text: str) -> list[str]:
    return text.splitlines()


FINDING_ID_RE = re.compile(
    r"(?<![A-Za-z0-9_])[a-z][a-z0-9]*(?:_[a-z0-9]+)+(?![A-Za-z0-9_])")


def _table_blocks(lines: list[str]) -> list[tuple[int, int]]:
    """(data_row_count) per markdown table; a table is a delimiter row plus rows."""
    blocks = []
    index = 0
    while index < len(lines):
        if re.match(r"^\|[\s:|-]+\|\s*$", lines[index]) and "-" in lines[index]:
            cursor = index + 1
            rows = 0
            while cursor < len(lines) and lines[cursor].startswith("|"):
                rows += 1
                cursor += 1
            blocks.append(rows)
            index = cursor
        else:
            index += 1
    return blocks


def _m_table_counts(repo, rev, path, params):
    text = repo.show_text(rev, path) or ""
    return len([rows for rows in _table_blocks(_lines(text))
                if rows >= int(params["min_rows"])])


def _m_registry_code_rows(repo, rev, path, params):
    text = repo.show_text(rev, path) or ""
    count = 0
    for line in _lines(text):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if any(("0=" in cell and "1=" in cell) or FINDING_ID_RE.search(cell)
               for cell in cells):
            count += 1
    return count


def _m_checklist_headings(repo, rev, path, params):
    text = repo.show_text(rev, path) or ""
    return len([line for line in _lines(text)
                if re.match(r"^#{2,3} ", line) and "checklist" in line.lower()])


def _m_round_sections(repo, rev, path, params):
    text = repo.show_text(rev, path) or ""
    return len([line for line in _lines(text)
                if line.startswith("## ") and re.search(r"(?i)round ?0*\d+", line)])


WAVE_PATH_RE = re.compile(
    r"\.ufo/waves/round-\d+/[A-Za-z0-9_./\-]*\.[A-Za-z0-9]+")


def _wave_paths(text: str) -> list[str]:
    return sorted(set(WAVE_PATH_RE.findall(text)))


def _m_wave_receipt_paths(repo, rev, path, params):
    return len(_wave_paths(repo.show_text(rev, path) or ""))


def _m_wave_receipt_paths_missing(repo, rev, path, params):
    text = repo.show_text(rev, path) or ""
    return len([token for token in _wave_paths(text)
                if "*" not in token and not repo.exists(rev, token)])


SCRIPT_PATH_RE = re.compile(
    r"(?<![\w./-])(scripts/[A-Za-z0-9_.\-]+\.(?:py|sh)"
    r"|\.ufo/waves/[A-Za-z0-9_.\-/]*\.py)")
PY_INVOCATION_RE = re.compile(
    r"python3?[ \t]+-B[ \t]+([A-Za-z0-9_.\-/]+\.(?:py|sh|mjs))")


def _m_skill_script_paths_missing(repo, rev, path, params):
    text = repo.show_text(rev, path) or ""
    return len([token for token in sorted(set(SCRIPT_PATH_RE.findall(text)))
                if not repo.exists(rev, token)])


def _m_skill_python_invocations_missing(repo, rev, path, params):
    text = repo.show_text(rev, path) or ""
    return len([token for token in sorted(set(PY_INVOCATION_RE.findall(text)))
                if not repo.exists(rev, token)])


SIBLING_LANE_RE = re.compile(r"(?:^|/)([a-z0-9-]+-shokunin|[a-z0-9-]+-shokinin)/")


def _m_cross_lane_citations(repo, rev, path, params):
    glob = params.get("glob", "corpus/knowledge/*.md")
    excludes = list(params.get("exclude", []))
    base = glob.rsplit("/", 1)[0] if "/" in glob else "."
    pattern = glob.rsplit("/", 1)[-1]
    files = [path for path in repo.list_tree(rev, base)
             if fnmatch.fnmatch(path.rsplit("/", 1)[-1], pattern)]
    files = [path for path in files
             if not any(fnmatch.fnmatch(path, exclusion) for exclusion in excludes)]
    count = 0
    for path in files:
        body = repo.show_text(rev, path)
        if body is None:
            continue
        for token in re.findall(r"`([^`\n]+)`", body):
            for match in SIBLING_LANE_RE.finditer(token):
                if match.group(1) != LANE_SELF:
                    count += 1
    return count


MEASURES = {
    "markdown_tables_with_min_rows": (_m_table_counts,
                                      "tables whose data-row count >= params.min_rows"),
    "registry_rows_with_code_cell": (_m_registry_code_rows,
                                     "table rows carrying an exit map or a finding id"),
    "checklist_headings": (_m_checklist_headings, "headings naming a checklist"),
    "round_sections": (_m_round_sections, "``## `` headings naming a round"),
    "wave_receipt_paths": (_m_wave_receipt_paths,
                           "distinct .ufo/waves/round-N/ file paths"),
    "wave_receipt_paths_missing": (_m_wave_receipt_paths_missing,
                                   "named wave receipts absent at the revision"),
    "skill_script_paths_missing": (_m_skill_script_paths_missing,
                                   "scripts/*.py|sh and counter paths absent"),
    "skill_python_invocations_missing": (_m_skill_python_invocations_missing,
                                         "``python3 -B <path>`` targets absent"),
    "cross_lane_citations": (_m_cross_lane_citations,
                             "sibling-lane repository paths cited in the globbed files"),
}


# --------------------------------------------------------------------------
# check kinds (declaration-only vocabulary, amendment 2 A2)
# --------------------------------------------------------------------------
def _k_exists(repo, rev, path, params):
    return repo.exists(rev, path)


def _k_count_at_least(repo, rev, path, params):
    measure = params.get("measure")
    if measure not in MEASURES:
        raise Unevaluable(f"unknown measure {measure!r}")
    if not repo.exists(rev, path):
        return None
    return MEASURES[measure][0](repo, rev, path, params)


def _k_regex_count(repo, rev, path, params):
    pattern = params.get("pattern")
    if not isinstance(pattern, str) or not pattern:
        raise Unevaluable("regex_count needs params.pattern")
    text = repo.show_text(rev, path)
    if text is None:
        return None
    return len(re.findall(pattern, text, re.MULTILINE))


def _k_all_ids_resolve(repo, rev, path, params):
    for key in ("pattern", "resolve_path", "resolve_pattern"):
        if not isinstance(params.get(key), str) or not params[key]:
            raise Unevaluable(f"all_ids_resolve needs params.{key}")
    for key in ("pattern", "resolve_pattern"):
        if re.compile(params[key]).groups < 1:
            raise Unevaluable(
                f"all_ids_resolve needs one capture group in params.{key}")
    text = repo.show_text(rev, path)
    if text is None:
        return None
    other = repo.show_text(rev, params["resolve_path"])
    if other is None:
        raise Unevaluable(
            f"{params['resolve_path']} is absent at {rev}: ids cannot resolve")
    cited = set(re.findall(params["pattern"], text))
    rows = set(re.findall(params["resolve_pattern"], other))
    return {"ids": len(cited), "resolved": len(cited & rows),
            "unresolved": len(cited - rows)}


def _k_no_match(repo, rev, path, params):
    measure = params.get("measure")
    if measure is not None:
        if measure not in MEASURES:
            raise Unevaluable(f"unknown measure {measure!r}")
        if not repo.exists(rev, path):
            return None
        return MEASURES[measure][0](repo, rev, path, params)
    pattern = params.get("pattern")
    if not isinstance(pattern, str) or not pattern:
        raise Unevaluable("no_match needs params.measure or params.pattern")
    text = repo.show_text(rev, path)
    if text is None:
        return None
    return len(re.findall(pattern, text, re.MULTILINE))


KINDS = {
    "exists": _k_exists,
    "count_at_least": _k_count_at_least,
    "regex_count": _k_regex_count,
    "all_ids_resolve": _k_all_ids_resolve,
    "no_match": _k_no_match,
}


def _verdict(check: dict, observed) -> bool:
    """The check's own pass/fail, computed here — never read from the ledger."""
    kind = check["kind"]
    params = check.get("params") or {}
    if kind == "exists":
        return observed is True
    if kind == "count_at_least":
        return isinstance(observed, int) and observed >= int(params.get("min", 0))
    if kind == "regex_count":
        if "min" not in params:
            return True
        return isinstance(observed, int) and observed >= int(params["min"])
    if kind == "all_ids_resolve":
        return (isinstance(observed, dict) and observed.get("ids", 0) >= 1
                and observed.get("unresolved", 1) == 0)
    if kind == "no_match":
        return observed == 0
    return False


# --------------------------------------------------------------------------
# ledger parsing and schema
# --------------------------------------------------------------------------
def _nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _check_schema_problem(check) -> str | None:
    if not isinstance(check, dict):
        return "check is not an object"
    if not _nonempty(check.get("id")):
        return "check without an id"
    kind = check.get("kind")
    if kind not in KINDS:
        return f"check {check.get('id')!r} kind {kind!r} is outside the frozen vocabulary"
    if not _nonempty(check.get("path")):
        return f"check {check.get('id')!r} without a path"
    if "params" in check and not isinstance(check.get("params"), dict):
        return f"check {check.get('id')!r} params is not an object"
    if "observed" not in check:
        return f"check {check.get('id')!r} without an observed value"
    if "holds" in check and not isinstance(check.get("holds"), bool):
        return f"check {check.get('id')!r} holds is not a boolean"
    params = check.get("params") or {}
    if kind == "count_at_least":
        if params.get("measure") not in MEASURES:
            return f"check {check.get('id')!r} measure {params.get('measure')!r} is unknown"
        if not _is_int(params.get("min")):
            return f"check {check.get('id')!r} needs an integer params.min"
    if kind == "no_match" and "measure" in params and params["measure"] not in MEASURES:
        return f"check {check.get('id')!r} measure {params['measure']!r} is unknown"
    return None


def _row_schema_problem(row) -> str | None:
    if not isinstance(row, dict):
        return "not an object"
    box = row.get("box")
    if not _is_int(box):
        return "box is not an integer"
    if row.get("marker") not in MARKERS:
        return "marker is not one of ' ', '~', 'x'"
    if row.get("status") not in STATUSES:
        return "status is not evidenced|gap"
    checks = row.get("checks")
    if not isinstance(checks, list) or not checks:
        return "checks is not a non-empty array"
    for check in checks:
        problem = _check_schema_problem(check)
        if problem:
            return problem
    if row["status"] == "gap":
        if not _nonempty(row.get("reason")):
            return "gap row without a reason"
        if not _nonempty(row.get("flip")):
            return "gap row without a flip"
    if row["marker"] == "x" and not _nonempty(row.get("verifier")):
        return "x row without a named verifier"
    return None


def parse_ledger(raw: bytes | None) -> tuple[list, list[str]]:
    """Return (entries, diagnostics).  A missing ledger is a red state, not a fault."""
    if raw is None:
        return [], [f"{LEDGER_PATH} is absent at the revision: every box is unexamined"]
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Unevaluable(f"{LEDGER_PATH} is not valid JSON: {exc}") from exc
    if not isinstance(document, dict):
        raise Unevaluable(f"{LEDGER_PATH} is not a JSON object")
    if document.get("schema") != LEDGER_SCHEMA:
        raise Unevaluable(
            f"{LEDGER_PATH} schema is {document.get('schema')!r}, not {LEDGER_SCHEMA!r}")
    rows = document.get("rows")
    if not isinstance(rows, list):
        raise Unevaluable(f"{LEDGER_PATH} carries no rows array")
    diagnostics = []
    entries = []
    for index, row in enumerate(rows):
        problem = _row_schema_problem(row)
        if problem:
            diagnostics.append(f"row {index} is invalid: {problem}")
            entries.append({"row": row, "valid": False, "problem": problem})
        else:
            entries.append({"row": row, "valid": True, "problem": None})
    return entries, diagnostics


# --------------------------------------------------------------------------
# evaluation
# --------------------------------------------------------------------------
def _same(left, right) -> bool:
    """Exact comparison after one normalisation (amendment 2 A3).

    Integers compare as integers, booleans as booleans (never ``True == 1``),
    strings as exact strings, and containers element-wise.
    """
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if _is_int(left) or _is_int(right):
        return _is_int(left) and _is_int(right) and left == right
    if isinstance(left, dict) or isinstance(right, dict):
        if not (isinstance(left, dict) and isinstance(right, dict)):
            return False
        return set(left) == set(right) and all(_same(left[k], right[k]) for k in left)
    if isinstance(left, list) or isinstance(right, list):
        if not (isinstance(left, list) and isinstance(right, list)):
            return False
        return len(left) == len(right) and all(
            _same(a, b) for a, b in zip(left, right))
    return type(left) is type(right) and left == right


def _finding(klass: str, subject: str, detail: str) -> dict:
    return {"class": klass, "subject": subject, "detail": detail}


def evaluate(repo: Repo, rev: str) -> dict:
    checklist = repo.show_text(rev, CHECKLIST_PATH)
    checklist_lines = _lines(checklist) if checklist is not None else []
    boxes = []
    for index, line in enumerate(checklist_lines):
        match = BOX_RE.match(line)
        if match:
            boxes.append({"box": len(boxes) + 1, "marker": match.group(1),
                          "text": match.group(2), "line": index + 1})
    entries, diagnostics = parse_ledger(repo.show(rev, LEDGER_PATH))

    findings: list[dict] = []
    by_box: dict[int, list[dict]] = {}
    for entry in entries:
        if not entry["valid"]:
            findings.append(_finding("row-invalid", "ledger",
                                     entry["problem"] or "invalid row"))
            continue
        row = entry["row"]
        if row["box"] not in BOX_RANGE:
            findings.append(_finding(
                "box-out-of-range", f"box {row['box']}",
                "row names a box outside 1..4; it is reported, never ignored"))
            continue
        by_box.setdefault(row["box"], []).append(row)

    evidenced = gap = unexamined = 0
    derivation = []
    for box in boxes:
        entry = {"box": box["box"], "marker": box["marker"], "text": box["text"],
                 "status": "unexamined", "checks": [], "findings": []}
        candidates = by_box.get(box["box"], [])
        if not candidates:
            unexamined += 1
            if box["marker"] in ("~", "x"):
                finding = _finding(
                    "marker-without-row", f"box {box['box']} marker [{box['marker']}]",
                    "the marker asserts a verdict no ledger row derives")
                findings.append(finding)
                entry["findings"].append(finding)
            derivation.append(entry)
            continue
        if len(candidates) > 1:
            finding = _finding(
                "duplicate-row", f"box {box['box']}",
                f"{len(candidates)} valid rows for one box")
            findings.append(finding)
            entry["findings"].append(finding)
            entry["status"] = "ambiguous"
            derivation.append(entry)
            continue

        row = candidates[0]
        row_findings: list[dict] = []
        if row["marker"] != box["marker"]:
            row_findings.append(_finding(
                "marker-disagrees-with-row", f"box {box['box']}",
                f"checklist marker [{box['marker']}] vs ledger marker [{row['marker']}]"))
        if box["marker"] == " " and row["status"] == "evidenced":
            row_findings.append(_finding(
                "marker-understated", f"box {box['box']}",
                "marker ' ' over an evidenced row"))
        if box["marker"] in ("~", "x") and row["status"] != "evidenced":
            row_findings.append(_finding(
                "marker-overstated", f"box {box['box']}",
                f"marker [{box['marker']}] over a {row['status']} row"))
        if box["marker"] == "x" and not _nonempty(row.get("verifier")):
            row_findings.append(_finding(
                "verifier-missing", f"box {box['box']}",
                "marker [x] without a named non-author verifier"))

        verdicts = []
        for check in row["checks"]:
            record = {"id": check["id"], "kind": check["kind"],
                      "recorded": check["observed"], "rederived": None,
                      "verdict": None, "agrees": None}
            try:
                observed = KINDS[check["kind"]](repo, rev, check["path"],
                                                check.get("params") or {})
            except Unevaluable:
                raise
            if observed is None:
                row_findings.append(_finding(
                    "check-path-missing", f"box {box['box']} {check['id']}",
                    f"{check['path']} is absent at {rev}"))
                record["agrees"] = False
                verdicts.append(False)
                entry["checks"].append(record)
                continue
            record["rederived"] = observed
            record["agrees"] = _same(observed, check["observed"])
            if not record["agrees"]:
                row_findings.append(_finding(
                    "observation-differs", f"box {box['box']} {check['id']}",
                    f"recorded {json.dumps(check['observed'], sort_keys=True)} "
                    f"but re-derived {json.dumps(observed, sort_keys=True)}"))
            verdict = _verdict(check, observed)
            record["verdict"] = verdict
            verdicts.append(verdict)
            entry["checks"].append(record)

        all_pass = all(verdicts) if verdicts else False
        if row["status"] == "evidenced" and not all_pass:
            row_findings.append(_finding(
                "status-unsupported", f"box {box['box']}",
                "status=evidenced while a frozen check's verdict is false "
                "(amendment 1 A12 makes a failing check a gap)"))
        entry["status"] = row["status"]
        entry["findings"] = row_findings
        findings.extend(row_findings)
        if row_findings:
            entry["status"] = "contradicted"
        elif row["status"] == "evidenced":
            evidenced += 1
        else:
            gap += 1
        derivation.append(entry)

    return {"revision": rev, "boxes": len(boxes), "evidenced": evidenced,
            "gap": gap, "unexamined": unexamined, "mismatches": len(findings),
            "met": (len(boxes) == 4 and unexamined == 0 and not findings),
            "findings": findings, "derivation": derivation,
            "diagnostics": diagnostics}


def format_summary(result: dict) -> str:
    return (f"C1 revision={result['revision']} boxes={result['boxes']} "
            f"evidenced={result['evidenced']} gap={result['gap']} "
            f"unexamined={result['unexamined']} mismatches={result['mismatches']} "
            f"met={str(result['met']).lower()}")


# --------------------------------------------------------------------------
# selftest fixtures: tree objects, no commit anywhere
# --------------------------------------------------------------------------
def _fixture_tree(work: str, name: str, files: dict[str, str],
                  ledger_in_tree: bool = True) -> tuple[str, str, str]:
    base = os.path.join(work, name)
    root = os.path.join(base, "root")
    git_dir = os.path.join(base, "repo.git")
    index = os.path.join(base, "index")
    os.makedirs(root, exist_ok=True)
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir)
    subprocess.run(["git", "init", "--bare", "-q", git_dir], check=True,
                   capture_output=True, env=_clean_env())
    env = _clean_env()
    env["GIT_DIR"] = git_dir
    env["GIT_INDEX_FILE"] = index
    for path, text in sorted(files.items()):
        full = os.path.join(root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as handle:
            handle.write(text.encode("utf-8"))
        if not ledger_in_tree and path == LEDGER_PATH:
            continue  # amendment 2 A5 fixture 07: ledger exists only untracked
        blob = subprocess.run(["git", "hash-object", "-w", "--stdin"],
                              input=text.encode("utf-8"), capture_output=True,
                              env=env, check=True).stdout.decode().strip()
        subprocess.run(["git", "update-index", "--add", "--cacheinfo",
                        f"100644,{blob},{path}"], check=True,
                       capture_output=True, env=env)
    tree = subprocess.run(["git", "write-tree"], capture_output=True,
                          env=env, check=True).stdout.decode().strip()
    return root, git_dir, tree


TITLES = [
    "SKILL.md contains real decision tables, error patterns, checklists, cited sources",
    "At least one end-to-end domain task executed and logged in LOG.md",
    "Instructions executable by an agent without oral context",
    "No cross-domain bleed (PROVINCE.md still accurate)",
]


def _fixture_checklist(markers=("~", " ", " ", " ")) -> str:
    lines = ["# fixture checklist", "", "Promotion requires all of:", ""]
    lines += [f"- [{m}] {t}" for m, t in zip(markers, TITLES)]
    return "\n".join(lines) + "\n"


FIXTURE_SKILL = "\n".join(
    ["# fixture skill", "", "| Surface | Path |", "|---|---|",
     "| a | b |", "| c | d |", "| e | f |", "",
     "| Gate | Verdict |", "|---|---|",
     "| gate-a | `0=clean`; `1=findings` |",
     "| gate-b | `0=met`; `1=findings` |",
     "| gate-c | `0=met`; `1=findings` |", "",
     "| Gate | Verdict |", "|---|---|",
     "| gate-d | `fixture_finding_id` |", "",
     "## Fixture checklist", "", "1. one", "2. two", "3. three", "",
     "Cited: S001. Scripts: `scripts/ok.py`.",
     "Run `python3 -B scripts/ok.py --selftest`.", ""])
FIXTURE_SOURCES = "| id | source |\n|---|---|\n| S001 | fixture |\n"
FIXTURE_LOG = ("# fixture log\n\n- 2026-01-01 — round 1: task executed.\n"
               "  Evidence: `corpus/knowledge/note.md`.\n\n"
               "## Round 1 — fixture end-to-end task\n\n"
               "Evidence: `corpus/knowledge/note.md`, `.ufo/waves/round-1/receipt.txt`.\n")
FIXTURE_OK = "import sys\nsys.exit(0)\n"


def _files(**overrides) -> dict[str, str]:
    files = {
        "SHONEN.md": _fixture_checklist(),
        "SKILL.md": FIXTURE_SKILL,
        "corpus/SOURCES.md": FIXTURE_SOURCES,
        "LOG.md": FIXTURE_LOG,
        "corpus/knowledge/note.md": "note\n",
        ".ufo/waves/round-1/receipt.txt": "receipt\n",
        "scripts/ok.py": FIXTURE_OK,
    }
    files.update(overrides)
    return files


def _ledger(rows: list[dict]) -> str:
    return json.dumps({"schema": LEDGER_SCHEMA,
                       "predicate": "met  <=>  boxes == 4  and  unexamined == 0  "
                                    "and  mismatches == 0",
                       "rows": rows}, indent=2) + "\n"


def _row(box, marker, status, checks, **extra) -> dict:
    row = {"box": box, "marker": marker, "status": status, "checks": checks}
    row.update(extra)
    return row


def _clean_rows() -> list[dict]:
    return [
        _row(1, "~", "evidenced", [
            {"id": "b1-ids", "kind": "all_ids_resolve", "path": "SKILL.md",
             "params": {"pattern": r"\b(S\d{3})\b",
                        "resolve_path": "corpus/SOURCES.md",
                        "resolve_pattern": r"(?m)^\| (S\d{3}) \|"},
             "observed": {"ids": 1, "resolved": 1, "unresolved": 0}},
            {"id": "b1-tables", "kind": "count_at_least", "path": "SKILL.md",
             "params": {"measure": "markdown_tables_with_min_rows",
                        "min_rows": 3, "min": 2},
             "observed": 2},
            {"id": "b1-registry", "kind": "count_at_least", "path": "SKILL.md",
             "params": {"measure": "registry_rows_with_code_cell", "min": 2},
             "observed": 4},
            {"id": "b1-checklist", "kind": "count_at_least", "path": "SKILL.md",
             "params": {"measure": "checklist_headings", "min": 1},
             "observed": 1},
        ]),
        _row(2, " ", "gap", [
            {"id": "b2-rounds", "kind": "count_at_least", "path": "LOG.md",
             "params": {"measure": "round_sections", "min": 1}, "observed": 1},
            {"id": "b2-receipts", "kind": "count_at_least", "path": "LOG.md",
             "params": {"measure": "wave_receipt_paths", "min": 1}, "observed": 1},
            {"id": "b2-missing", "kind": "no_match", "path": "LOG.md",
             "params": {"measure": "wave_receipt_paths_missing"}, "observed": 0},
        ], reason="fixture gap", flip="fixture flip"),
        _row(3, " ", "gap", [
            {"id": "b3-scripts", "kind": "no_match", "path": "SKILL.md",
             "params": {"measure": "skill_script_paths_missing"}, "observed": 0},
            {"id": "b3-invocations", "kind": "no_match", "path": "SKILL.md",
             "params": {"measure": "skill_python_invocations_missing"},
             "observed": 0},
            {"id": "b3-exists", "kind": "exists", "path": "scripts/ok.py",
             "params": {}, "observed": True},
        ], reason="fixture gap", flip="fixture flip"),
        _row(4, " ", "gap", [
            {"id": "b4-lanes", "kind": "no_match", "path": "corpus/knowledge",
             "params": {"measure": "cross_lane_citations",
                        "glob": "corpus/knowledge/*.md",
                        "exclude": ["corpus/knowledge/freshness-*.json"]},
             "observed": 0},
        ], reason="fixture gap", flip="fixture flip"),
    ]


class Case:
    def __init__(self, name, files, expect, exit_code, ledger_in_tree=True):
        self.name = name
        self.files = files
        self.expect = expect
        self.exit_code = exit_code
        self.ledger_in_tree = ledger_in_tree
        self.failures = []

    def check(self, fields, code):
        if code != self.exit_code:
            self.failures.append(f"exit {code} != {self.exit_code}")
        for key, want in self.expect.items():
            got = fields.get(key)
            if got != want:
                self.failures.append(f"{key}={got!r} != {want!r}")
        return not self.failures


def _parse_summary(text: str) -> dict:
    stripped = text.strip()
    if not stripped:
        return {}
    last = stripped.splitlines()[-1]
    match = re.search(
        r"^C1 revision=(\S+) boxes=(\d+) evidenced=(\d+) gap=(\d+) "
        r"unexamined=(\d+) mismatches=(\d+) met=(true|false)$", last)
    if not match:
        return {}
    return {"revision": match.group(1), "boxes": int(match.group(2)),
            "evidenced": int(match.group(3)), "gap": int(match.group(4)),
            "unexamined": int(match.group(5)), "mismatches": int(match.group(6)),
            "met": match.group(7) == "true"}


def _clean_files() -> dict[str, str]:
    return _files(**{LEDGER_PATH: _ledger(_clean_rows())})


def run_selftest(work: str) -> int:
    os.makedirs(work, exist_ok=True)
    cases: list[Case] = []
    clean = _clean_files()

    cases.append(Case("clean-four-boxes", clean,
                      {"boxes": 4, "evidenced": 1, "gap": 3, "unexamined": 0,
                       "mismatches": 0, "met": True}, 0))

    # ---- amendment 2 A5, the six attack shapes -------------------------
    rows = [_row(box, "~", "evidenced", [{"id": "x", "holds": True}])
            for box in (1, 2, 3, 4)]
    no_measure = dict(_files(**{LEDGER_PATH: _ledger(rows)}))
    no_measure["SHONEN.md"] = _fixture_checklist(markers=("~", "~", "~", "~"))
    cases.append(Case("a5-02-evidenced-without-measurement", no_measure,
                      {"met": False}, 1))

    rows = _clean_rows()
    for row in rows:
        row["marker"] = "x"
        row["status"] = "gap"
        row.setdefault("reason", "fixture gap")
        row.setdefault("flip", "fixture flip")
        row["verifier"] = "fabricated verifier"
    x_over_gap = dict(_files(**{LEDGER_PATH: _ledger(rows)}))
    x_over_gap["SHONEN.md"] = _fixture_checklist(markers=("x", "x", "x", "x"))
    cases.append(Case("a5-03-x-over-gap-fabricated-verifier", x_over_gap,
                      {"met": False}, 1))

    rows = _clean_rows()
    rows[0]["checks"][0] = {"id": "b1-command", "kind": "command",
                            "path": "SKILL.md",
                            "params": {"argv": ["python3", "-c", "pass"]},
                            "observed": 0}
    cases.append(Case("a5-04-command-check",
                      _files(**{LEDGER_PATH: _ledger(rows)}),
                      {"met": False}, 1))

    rows = _clean_rows() + [_row(7, " ", "gap", [
        {"id": "b7", "kind": "exists", "path": "SKILL.md", "params": {},
         "observed": True}], reason="r", flip="f")]
    cases.append(Case("a5-05-row-for-box-7",
                      _files(**{LEDGER_PATH: _ledger(rows)}),
                      {"met": False}, 1))

    rows = _clean_rows()
    rows[0]["checks"][1]["observed"] = 99
    cases.append(Case("a5-06-observed-contradicts-derivation",
                      _files(**{LEDGER_PATH: _ledger(rows)}),
                      {"met": False}, 1))

    base_markers = _files(**{LEDGER_PATH: _ledger(_clean_rows())})
    base_markers["SHONEN.md"] = _fixture_checklist(markers=(" ", " ", " ", " "))
    cases.append(Case("a5-07-untracked-worktree-ledger", base_markers,
                      {"boxes": 4, "unexamined": 4, "mismatches": 0,
                       "met": False}, 1, ledger_in_tree=False))

    # ---- ordinary red/green controls -----------------------------------
    empty_markers = _files()
    empty_markers["SHONEN.md"] = _fixture_checklist(markers=(" ", " ", " ", " "))
    cases.append(Case("missing-ledger", empty_markers,
                      {"boxes": 4, "evidenced": 0, "gap": 0, "unexamined": 4,
                       "mismatches": 0, "met": False}, 1))

    rows = _clean_rows()
    rows[0]["checks"] = []
    cases.append(Case("empty-checks", _files(**{LEDGER_PATH: _ledger(rows)}),
                      {"unexamined": 1, "met": False}, 1))

    rows = _clean_rows()
    rows[0]["checks"][0]["path"] = "NOPE.md"
    cases.append(Case("fake-path", _files(**{LEDGER_PATH: _ledger(rows)}),
                      {"met": False}, 1))

    def signed_rows(with_verifier: bool) -> tuple[dict, dict]:
        rows = _clean_rows()
        for row in rows:
            row["status"] = "evidenced"
            row["marker"] = "~"
        rows[0]["marker"] = "x"
        if with_verifier:
            rows[0]["verifier"] = "fixture verifier, 2026-11-03, receipt"
        else:
            rows[0].pop("verifier", None)
        files = _files(**{LEDGER_PATH: _ledger(rows)})
        files["SHONEN.md"] = _fixture_checklist(markers=("x", "~", "~", "~"))
        return files

    x_ok = signed_rows(True)
    cases.append(Case("x-with-verifier-and-clean-checks", x_ok,
                      {"evidenced": 4, "met": True}, 0))
    x_bad = signed_rows(False)
    cases.append(Case("x-without-verifier", x_bad, {"met": False}, 1))

    rows = [row for row in _clean_rows() if row["box"] != 1]
    cases.append(Case("tilde-with-no-row",
                      _files(**{LEDGER_PATH: _ledger(rows)}),
                      {"unexamined": 1, "met": False}, 1))

    rows = _clean_rows()
    rows[1]["status"] = "evidenced"
    space_over_evidenced = _files(**{LEDGER_PATH: _ledger(rows)})
    cases.append(Case("space-over-evidenced", space_over_evidenced,
                      {"met": False}, 1))

    rows = _clean_rows() + [_clean_rows()[0]]
    cases.append(Case("duplicate-row", _files(**{LEDGER_PATH: _ledger(rows)}),
                      {"met": False}, 1))

    rows = _clean_rows()
    rows[0]["checks"][1]["observed"] = 1
    cases.append(Case("threshold-below-min",
                      _files(**{LEDGER_PATH: _ledger(rows)}),
                      {"met": False}, 1))

    rows = _clean_rows()
    rows[1]["status"] = "evidenced"
    rows[1]["checks"][2]["observed"] = 1
    failing_files = _files()
    failing_files[LEDGER_PATH] = _ledger(rows)
    failing_files["LOG.md"] = FIXTURE_LOG.replace(
        ".ufo/waves/round-1/receipt.txt", ".ufo/waves/round-9/absent.txt")
    cases.append(Case("evidenced-with-failing-check", failing_files,
                      {"met": False}, 1))

    rows = _clean_rows()
    rows[1].pop("flip")
    cases.append(Case("gap-without-flip", _files(**{LEDGER_PATH: _ledger(rows)}),
                      {"met": False}, 1))

    five = _files(**{LEDGER_PATH: _ledger(_clean_rows())})
    five["SHONEN.md"] = _fixture_checklist() + "- [ ] fifth box\n"
    cases.append(Case("five-boxes", five, {"boxes": 5, "met": False}, 1))

    cases.append(Case("missing-checklist",
                      {k: v for k, v in clean.items() if k != "SHONEN.md"},
                      {"boxes": 0, "met": False}, 1))

    cases.append(Case("bad-schema",
                      _files(**{LEDGER_PATH: '{"schema": "other/v1", "rows": []}'}),
                      {}, 2))

    cases.append(Case("malformed-json", _files(**{LEDGER_PATH: "{not json"}),
                      {}, 2))

    rows = _clean_rows()
    rows[0]["marker"] = " "
    cases.append(Case("marker-drift", _files(**{LEDGER_PATH: _ledger(rows)}),
                      {"met": False}, 1))

    rows = _clean_rows()
    rows[1]["checks"][0]["params"]["measure"] = "unknown_measure"
    cases.append(Case("unknown-measure", _files(**{LEDGER_PATH: _ledger(rows)}),
                      {"met": False}, 1))

    rows = _clean_rows()
    rows[0]["checks"][0]["observed"] = {"ids": 1, "resolved": 1,
                                        "unresolved": "0"}
    cases.append(Case("observed-type-mismatch",
                      _files(**{LEDGER_PATH: _ledger(rows)}),
                      {"met": False}, 1))

    rows = _clean_rows()
    rows[0].pop("box")
    cases.append(Case("row-without-box", _files(**{LEDGER_PATH: _ledger(rows)}),
                      {"met": False}, 1))

    passed = 0
    for case in cases:
        root, git_dir, tree = _fixture_tree(work, case.name, case.files,
                                            ledger_in_tree=case.ledger_in_tree)
        out, err = io.StringIO(), io.StringIO()
        argv = ["--root", root, "--git-dir", git_dir, "--revision", tree,
                "--work", os.path.join(work, case.name, "scratch")]
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(argv)
        fields = {} if code == 2 else _parse_summary(out.getvalue())
        if case.check(fields, code):
            passed += 1
            print(f"PASS  {case.name}")
        else:
            print(f"FAIL  {case.name}: {'; '.join(case.failures)}")
            print(f"      stdout={out.getvalue().strip()[:200]}")
            print(f"      stderr={err.getvalue().strip()[:400]}")
    print(f"selftest: {passed}/{len(cases)} passed")
    return 0 if passed == len(cases) else 1


# --------------------------------------------------------------------------
# cli
# --------------------------------------------------------------------------
class Parser(argparse.ArgumentParser):
    def error(self, message):  # noqa: D401 — argparse contract
        raise UsageError(message)


def main(argv: list[str] | None = None) -> int:
    ap = Parser(prog="c77_shonen_ledger.py", allow_abbrev=False,
                usage="c77_shonen_ledger.py --root PATH --revision REV "
                      "[--git-dir DIR] [--work DIR] [--json] | --selftest [--work DIR]")
    ap.add_argument("--root", default=None, metavar="PATH")
    ap.add_argument("--revision", default=None, metavar="REV")
    ap.add_argument("--git-dir", default=None, metavar="DIR")
    ap.add_argument("--work", default=None, metavar="DIR")
    ap.add_argument("--json", action="store_true",
                    help="append the derivation to stdout")
    ap.add_argument("--selftest", action="store_true")
    created_work = None
    try:
        args = ap.parse_args(argv)
        if args.selftest:
            work = args.work or tempfile.mkdtemp(prefix="c77-selftest-")
            if not args.work:
                created_work = work
            return run_selftest(os.path.abspath(work))
        if not args.root:
            raise UsageError("--root is required")
        if not args.revision:
            raise UsageError("--revision is required (there is no default)")
        repo = Repo(args.root, args.git_dir)
        rev = repo.resolve(args.revision)
        result = evaluate(repo, rev)
        print(format_summary(result))
        for finding in result["findings"]:
            print(f"  finding: {finding['class']} {finding['subject']} — "
                  f"{finding['detail']}", file=sys.stderr)
        for diagnostic in result["diagnostics"]:
            print(f"  diagnostic: {diagnostic}", file=sys.stderr)
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        return EXIT_MET if result["met"] else EXIT_NOT_MET
    except UsageError as exc:
        print(f"64 usage: {exc}", file=sys.stderr)
        return EXIT_USAGE
    except Unevaluable as exc:
        print(f"2 unevaluable: {exc}", file=sys.stderr)
        return EXIT_UNEVALUABLE
    except Exception as exc:  # noqa: BLE001 — the exit contract names every fault 2
        print(f"2 unevaluable: {type(exc).__name__}: {exc}", file=sys.stderr)
        return EXIT_UNEVALUABLE
    finally:
        if created_work:
            shutil.rmtree(created_work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
