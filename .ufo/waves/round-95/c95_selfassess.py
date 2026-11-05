#!/usr/bin/env python3
"""Round-95 C1 counter: strict self-assessment conformance, third successor.

Frozen before data (`.ufo/waves/round-95/freeze.md`). Successor to the round-94
counter `.ufo/waves/round-94/c94_selfassess.py`, implementing the routed defects
R94-1 (ReviewC1 routes R01, R02b, R03, R05, R08, R09, R10b, R12, R18), R94-2
(effectful shadow, sys.path hygiene), R94-3 (identity covers the row's path
tokens), R94-7 (a battery covering every rule class) and the round-94 closure
item "no --skip-battery met=true" (the battery-free mode can never print
met=true).

Surface audit (strict E1-E5, content-pinned identity population)

  E1  every lane-authored round lesson (corpus/lessons/round-*.md, excluding
      *-verifier-spotcheck.md and *aggregator*) carries a line exactly `## Gate`
      whose body holds at least two non-empty lines. For lessons of rounds >= 95
      (the round this contract landed; earlier lessons are append-only history
      the corpus contract forbids rewriting), the decision vocabulary must be
      present in the Gate heading text or body: at least one /admit/i match and
      at least one /reject/i match (a two-junk-line Gate is vacuous; route R01).
  E2  every `## ` section of corpus/QUALITY.md whose heading matches
      `^Round[- ]<digits>` and whose first 400 characters mention "criteri"
      names at least one corpus/lessons/<file> path, and every such path
      resolves to a non-empty blob at the revision.
  E3  every corpus/knowledge/*.md carries non-empty `source:`, `verified-at:`
      and `recheck:` lines within its first 8 lines; EVERY `source:` line is
      validated (a second `source:` line is itself a finding; route R03); every
      `S<digits>` id on a `source:` line resolves to a ROW-ID cell of
      corpus/SOURCES.md, not to a token in prose; a `source:` line with no row
      id must carry a locator (an http(s) URL, `~/`, or a path-like token with
      a known suffix); and a `/tmp` or `/var/tmp` locator is never citable
      (route R12).
  E4  in every lane-authored round lesson, EVERY `## Mistakes` section has a
      contiguous table: each blank-line gap is reported, and every Mistakes
      body line carrying leading whitespace before its `|` is reported
      (route R02b). A lesson that carried a `## Mistakes` section at the base
      must still carry one (identity).
  E5  every repo-relative path (`scripts/…`, `corpus/…`, `.ufo/…`) named inside
      a SKILL.md table row (brace lists expanded, trailing `:line` and `#anchor`
      suffixes stripped, `<…>` placeholders and `*` skipped) must resolve to a
      NON-EMPTY REGULAR BLOB: a directory, a symlink (git mode 120000), or a
      0-byte blob is a finding (route R09 covers symlinks). A path named inside
      an explicit `[rNN-absence …]` span is an annotated absence: it is a
      finding only when the path exists at the revision. An `[rNN-absence`
      marker whose bracket does not close on the same line is a finding
      (route R10b).

Identity population (R94-1 R08/R18, R94-3): the frozen surface file
`frozen/c1-surfaces.json` beside this file, digest-pinned, pins CONTENT, not
operator-supplied paths: every base lesson path must still be present with the
same blob digest and its basename must not appear at any other lesson path; every
base knowledge entry must still be present with the same digest over its first
eight lines; the base criteria headings, SKILL-row first cells and Mistakes
carriers must still be present; and every base SKILL row that carried N backticked
repo paths must still carry at least N (a repair that strips path tokens to game
E5 fails identity; route R94-3). There is NO --surfaces-file flag: the CLI cannot
be pointed at an operator-supplied identity oracle (routes R08, R18).

Population cardinality: lesson, entry, SKILL-row and criteria counts must each be
>= the base measurement (`pins=short`).

Self-integrity: line 1 prints `counter=<sha256 of this file>`; `--self-pin <hex>`
exits 2 unless the executed bytes hash to the pin; `subprocess` is imported only
after the script directory has been removed from sys.path, and a process whose
subprocess module does not come from the standard library exits 2
`selfcheck=shadowed` before any measurement (route F1/R94-2).

Differential battery: 20 defect routes the counter must refuse (each with its
NAMED finding present), 5 clean-shape routes the counter must admit, and the
effectful-shadow route F1e (R94-2) where a planted `subprocess.py` that writes a
marker and exits 7 at import must NOT run (marker absent) and must not decide the
verdict. F2 is a canned wrapper lacking the true counter digest. The frozen
round-94 counter's own audit must admit at least PREDECESSOR_FLOOR of the five
R94-false-green fixture routes, so the routes are live against the predecessor,
not blanket refusals.

met <=> pins ok AND zero mismatches AND battery refused 20/20 and admitted 5/5
      AND F1e effect absent AND predecessor admits >= floor.
`--verdict-only` (nested runs) prints `met=n/a verdict=clean|failed` and exits 0
only on a clean audit; it can never print met=true (round-94 closure item).

Output line 1:
  C1v95 revision=<sha> counter=<sha256> lessons=N entries=N rows=N criteria=N
        mismatches=N E1=a E2=b E3=c E4=d E5=e pins=ok|short|identity
        battery=R/20 admit=A/5 shadow=absent|EFFECT predecessor_admits=N/17
        floor=4 self_pin=ok|mismatch met=true|false
line 2: JSON detail. Exit 0 iff met; 1 otherwise; 2 on unevaluable input.
--selftest plants one defect per strict class in a synthetic lane, asserts the
exact finding set, repairs it, and asserts exit 0, and asserts that the CLI
refuses --surfaces-file.
"""

import sys as _sys
import os as _os

# R94-2: drop the script directory from sys.path BEFORE any third-party-ish
# import can be shadowed; a planted subprocess.py beside this file must never
# load. (The frozen command also runs python3 -I, which excludes the script
# directory independently.)
_here = _os.path.dirname(_os.path.abspath(__file__))
_sys.path[:] = [p for p in _sys.path
                if _os.path.realpath(p or _os.getcwd()) != _os.path.realpath(_here)]

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess  # noqa: E402  (imported after sys.path sanitization)
import sys

BASE = "fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3"
BASE_PINS = {"lessons": 89, "entries": 82, "rows": 255, "criteria": 39}
SURFACES = "frozen/c1-surfaces.json"
SURFACES_SHA = "00a04c9a68f00de1561d70822a8ff3cab718583de4cd2cbf6ebd06e87b5d47b8"
PREDECESSOR = ".ufo/waves/round-94/c94_selfassess.py"
PREDECESSOR_FLOOR = 4
SYNTH_PINS = {"lessons": 2, "entries": 1, "rows": 2, "criteria": 1}
LESSON_SKIP = ("-verifier-spotcheck.md",)
PATH_RE = re.compile(r"`((?:scripts|corpus|\.ufo)/[^`\s]+)`")
ABSENCE_SPAN_RE = re.compile(r"\[r\d{2,}-absence\b[^\]]*\]")
ABSENCE_OPEN_RE = re.compile(r"\[r\d{2,}-absence(?![^\]]*\])")
ID_RE = re.compile(r"S\d{3,}")
CRIT_RE = re.compile(r"Round[- ]\d+")
ROW_ID_RE = re.compile(r"^\|[ \t]*(S[0-9]{3,})[ \t]*\|")
LOCATOR_RE = re.compile(
    r"https?://|~/|[A-Za-z0-9._/~\-]+\.(?:md|py|mjs|json|txt|html|yml|yaml)\b")
TMP_LOCATOR_RE = re.compile(r"(?:^|[\s`\"'])/(?:var/)?tmp/")
STD_PREFIXES = tuple(
    p for p in {sys.prefix, sys.base_prefix, os.path.dirname(os.__file__)} if p)


class Unevaluable(Exception):
    pass


def self_sha():
    with open(os.path.abspath(__file__), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def shadow_check():
    """Route F1/R94-2: refuse a subprocess module that is not the stdlib one."""
    path = getattr(subprocess, "__file__", "") or ""
    if not path or not os.path.abspath(path).startswith(STD_PREFIXES):
        raise Unevaluable("subprocess module is shadowed: %r" % path)


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True)


def read(root, rev, path):
    p = git(root, "show", "%s:%s" % (rev, path))
    return p.stdout.decode("utf-8", "replace") if p.returncode == 0 else None


def blob_meta(root, rev, path):
    """(kind, size, mode) of rev:path, or None when absent."""
    p = git(root, "cat-file", "-t", "%s:%s" % (rev, path))
    if p.returncode != 0:
        return None
    kind = p.stdout.decode().strip()
    s = git(root, "cat-file", "-s", "%s:%s" % (rev, path))
    size = int(s.stdout.decode().strip()) if s.returncode == 0 else -1
    t = git(root, "ls-tree", "%s" % rev, "--", path)
    mode = ""
    if t.returncode == 0 and t.stdout:
        mode = t.stdout.decode().split()[0]
    return kind, size, mode


def listing(root, rev, path):
    p = git(root, "ls-tree", "-r", "--name-only", rev, "--", path)
    return [x for x in p.stdout.decode().splitlines() if x]


def expand_braces(path):
    m = re.search(r"\{([^{}]*)\}", path)
    if not m:
        return [path]
    out = []
    for part in m.group(1).split(","):
        out.extend(expand_braces(path[:m.start()] + part + path[m.end():]))
    return out


def sections(text, heading):
    """Bodies of every `## <heading>` section (exact heading line, column 0)."""
    return [m.group(1) for m in
            re.finditer(r"(?m)^## %s\s*$(.*?)(?=^## |\Z)" % heading, text, re.S)]


def gate_sections(text):
    """(full heading line, body) of every `## Gate` section. The heading is the
    exact word Gate, optionally followed by a decision summary on the same line
    (`## Gate — admit X, reject Y`), which carries the decision vocabulary."""
    return [(m.group(0), m.group(1)) for m in
            re.finditer(r"(?m)^## Gate\b[^\n]*$(.*?)(?=^## |\Z)", text, re.S)]


def strip_path_suffixes(raw):
    """R05/R05b: drop a trailing `#anchor` (e.g. `#L42`) and `:line` suffix."""
    raw = re.sub(r"#([^#]*)$", "", raw)
    raw = re.sub(r":\d+(-\d+)?$", "", raw)
    return raw


def load_surfaces():
    here = os.path.dirname(os.path.abspath(__file__))
    try:
        with open(os.path.join(here, SURFACES), "rb") as fh:
            blob = fh.read().decode("utf-8")
    except OSError as exc:
        raise Unevaluable("missing %s: %s" % (SURFACES, exc))
    digest = hashlib.sha256(blob.encode("utf-8")).hexdigest()
    if digest != SURFACES_SHA:
        raise Unevaluable("surfaces digest drift: %s" % digest)
    return json.loads(blob)


def audit(root, rev, base_pins=None, surfaces=None):
    mismatches = []
    if surfaces is None:
        surfaces = load_surfaces()

    lessons = [p for p in listing(root, rev, "corpus/lessons")
               if re.search(r"/(round-[^/]*\.md)$", p)
               and not any(p.endswith(s) for s in LESSON_SKIP)
               and "aggregator" not in p]
    lesson_texts = {}
    for path in sorted(lessons):
        text = read(root, rev, path) or ""
        lesson_texts[path] = text
        m = re.search(r"round-(\d+)", path)
        round_no = int(m.group(1)) if m else 0
        gates = gate_sections(text)
        if not gates:
            mismatches.append({"class": "E1", "path": path,
                               "detail": "no '## Gate' heading"})
        for head_line, body in gates:
            nonempty = [l for l in body.splitlines() if l.strip()]
            if len(nonempty) < 2:
                mismatches.append({"class": "E1", "path": path,
                                   "detail": "vacuous Gate: fewer than two "
                                             "non-empty body lines"})
                break
            if round_no >= 95:
                if not (re.search(r"admit", head_line, re.I)
                        or re.search(r"admit", body, re.I)):
                    mismatches.append({"class": "E1", "path": path,
                                       "detail": "vacuous Gate: no admit decision "
                                                 "line (route R01)"})
                    break
                if not (re.search(r"reject", head_line, re.I)
                        or re.search(r"reject", body, re.I)):
                    mismatches.append({"class": "E1", "path": path,
                                       "detail": "vacuous Gate: no reject decision "
                                                 "line (route R01)"})
                    break
        mistakes = sections(text, "Mistakes")
        for idx, body in enumerate(mistakes):
            lines = body.splitlines()
            for i, line in enumerate(lines):
                if re.match(r"^[ \t]+\|", line):
                    mismatches.append({
                        "class": "E4", "path": path,
                        "detail": "indented table row inside Mistakes section %d "
                                  "line %d (route R02b)" % (idx + 1, i + 1)})
            stripped = [l.lstrip() for l in lines]
            for i in range(len(stripped) - 2):
                if (stripped[i].startswith("|") and stripped[i + 1].strip() == ""
                        and stripped[i + 2].startswith("|")):
                    mismatches.append({
                        "class": "E4", "path": path,
                        "detail": "blank line inside Mistakes section %d after "
                                  "row %d" % (idx + 1, i + 1)})
        if path in set(surfaces["mistakes_sections"]) and not mistakes:
            mismatches.append({"class": "E4", "path": path,
                               "detail": "carried a Mistakes section at base and "
                                         "now has none (deletion route F4)"})

    quality = read(root, rev, "corpus/QUALITY.md") or ""
    criteria = []
    for section in re.split(r"(?m)^## ", quality)[1:]:
        head = section.splitlines()[0].strip() if section.splitlines() else ""
        if not CRIT_RE.match(head) or not re.search(r"criteri", section[:400], re.I):
            continue
        criteria.append(head)
        cited = re.findall(r"corpus/lessons/[A-Za-z0-9._-]+", section)
        if not cited:
            mismatches.append({"class": "E2", "path": "corpus/QUALITY.md",
                               "detail": "section %r names no corpus/lessons/ file"
                                         % head})
            continue
        for c in sorted(set(cited)):
            meta = blob_meta(root, rev, c)
            if meta is None:
                mismatches.append({"class": "E2", "path": "corpus/QUALITY.md",
                                   "detail": "section %r cites missing %s"
                                             % (head, c)})
            elif meta[0] != "blob" or meta[1] <= 0:
                mismatches.append({"class": "E2", "path": "corpus/QUALITY.md",
                                   "detail": "section %r cites %s: %s of %d bytes"
                                             % (head, c, meta[0], meta[1])})

    sources = read(root, rev, "corpus/SOURCES.md") or ""
    row_ids = set()
    for line in sources.splitlines():
        m = ROW_ID_RE.match(line)
        if m:
            row_ids.add(m.group(1))
    entries = [p for p in listing(root, rev, "corpus/knowledge") if p.endswith(".md")]
    for path in sorted(entries):
        text = read(root, rev, path) or ""
        head = "\n".join(text.splitlines()[:8])
        problems = []
        for key in ("source", "verified-at", "recheck"):
            if not re.search(r"(?m)^" + key + r":\s*\S", head):
                problems.append("missing %s:" % key)
        source_lines = re.findall(r"(?m)^source:.*$", head)
        if len(source_lines) > 1:
            problems.append("multiple source: lines (%d); only the provenance "
                            "trio's single line is validated (route R03)"
                            % len(source_lines))
        for line in source_lines[:2]:
            ids_here = set(ID_RE.findall(line))
            unresolved = sorted(i for i in ids_here if i not in row_ids)
            if unresolved:
                problems.append("unresolved row id " + ", ".join(unresolved))
            elif not ids_here:
                if TMP_LOCATOR_RE.search(line):
                    problems.append("non-citable locator: /tmp is never evidence "
                                    "(route R12)")
                elif not LOCATOR_RE.search(line):
                    problems.append("vacuous source: no row id, URL or path locator")
        if problems:
            mismatches.append({"class": "E3", "path": path,
                               "detail": "; ".join(problems)})

    skill = read(root, rev, "SKILL.md") or ""
    rows = 0
    first_cells = []
    row_tokens = {}
    for line in skill.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        rows += 1
        first_cells.append(cells[0])
        body = " ".join(cells)
        row_tokens[cells[0]] = row_tokens.get(cells[0], 0) + len(PATH_RE.findall(body))
        absent = set()
        for span in ABSENCE_SPAN_RE.findall(body):
            absent.update(strip_path_suffixes(p).rstrip("`,.")
                          for p in PATH_RE.findall(span))
        if ABSENCE_OPEN_RE.search(body):
            mismatches.append({"class": "E5", "path": "SKILL.md",
                               "detail": "absence marker without a closing "
                                         "bracket on the same line (route R10b)"})
        seen = set()
        for raw in PATH_RE.findall(body):
            raw = strip_path_suffixes(raw).rstrip("`,.")
            for path in expand_braces(raw):
                if "<" in path or "*" in path or path in seen:
                    continue
                seen.add(path)
                meta = blob_meta(root, rev, path)
                if path in absent:
                    if meta is not None:
                        mismatches.append({"class": "E5", "path": "SKILL.md",
                                           "detail": "annotated absent but present "
                                                     "at the revision: %s" % path})
                elif meta is None:
                    mismatches.append({"class": "E5", "path": "SKILL.md",
                                       "detail": "names missing path %s" % path})
                elif meta[0] != "blob":
                    mismatches.append({"class": "E5", "path": "SKILL.md",
                                       "detail": "names a %s, not a blob: %s"
                                                 % (meta[0], path)})
                elif meta[1] <= 0:
                    mismatches.append({"class": "E5", "path": "SKILL.md",
                                       "detail": "names an empty blob: %s" % path})
                elif meta[2] == "120000":
                    mismatches.append({"class": "E5", "path": "SKILL.md",
                                       "detail": "names a symlink, not a regular "
                                                 "blob: %s (route R09)" % path})

    pins = {"lessons": len(lessons), "entries": len(entries), "rows": rows,
            "criteria": len(criteria)}
    base_pins = BASE_PINS if base_pins is None else base_pins
    short = [k for k, v in base_pins.items() if pins[k] < v]
    ident = []
    # Identity, pinned by CONTENT (R08): base lesson paths must still carry the
    # same blob digest, and their basenames must not appear at other paths.
    by_basename = {}
    for p in lessons:
        by_basename.setdefault(os.path.basename(p), []).append(p)
    for item in surfaces["lessons"]:
        path = item["path"]
        text = lesson_texts.get(path)
        if text is None:
            ident.append("lesson:" + path)
            continue
        if hashlib.sha256(text.encode("utf-8")).hexdigest() != item["sha256"]:
            ident.append("lesson-content:" + path)
        twins = [q for q in by_basename.get(os.path.basename(path), []) if q != path]
        for q in twins:
            ident.append("lesson-displaced:%s -> %s" % (path, q))
    for item in surfaces["entries"]:
        path = item["path"]
        text = read(root, rev, path)
        if text is None:
            ident.append("entry:" + path)
            continue
        head8 = "\n".join(text.splitlines()[:8])
        if hashlib.sha256(head8.encode("utf-8")).hexdigest() != item["head8_sha256"]:
            ident.append("entry-content:" + path)
    for h in surfaces["quality_criteria_headings"]:
        if h not in criteria:
            ident.append("criterion:" + h)
    for item in surfaces["skill_rows"]:
        cell = item["cell"]
        if cell not in first_cells:
            ident.append("skill_row:" + cell)
        elif row_tokens.get(cell, 0) < item["path_tokens"]:
            ident.append("skill_row_tokens:%s had %d repo paths, now %d (R94-3)"
                         % (cell, item["path_tokens"], row_tokens.get(cell, 0)))
    for p in surfaces["mistakes_sections"]:
        if p in lesson_texts and not sections(lesson_texts[p], "Mistakes"):
            ident.append("mistakes_section:" + p)
    counts = {c: sum(1 for m in mismatches if m["class"] == c)
              for c in ("E1", "E2", "E3", "E4", "E5")}
    return pins, short, sorted(set(ident)), mismatches, counts


# ---------------------------------------------------------------- battery --

CLEAN = {
    "corpus/lessons/round-01.md": "# r1\n\n## Gate\n\nadmit A.\nreject B.\n\n"
                                  "## Mistakes\n\n| # | Class |\n|---|---|\n"
                                  "| 1 | none |\n",
    "corpus/lessons/round-02.md": "# r2\n\n## Gate\n\nadmit C.\nreject D.\n\n"
                                  "## Mistakes\n\n| # | Class |\n|---|---|\n"
                                  "| 1 | a |\n| 2 | b |\n",
    "corpus/knowledge/entry.md": "source: S001\nverified-at: 2026-11-05\n"
                                 "recheck: 180d\n\nbody\n",
    "corpus/QUALITY.md": "# Q\n\n## Round-01 criterion — a thing\n\n"
                         "Grounded in `corpus/lessons/round-01.md`.\n",
    "corpus/SOURCES.md": "# S\n\n## Registry\n\n| id | source |\n|---|---|\n"
                         "| S001 | x |\n",
    "SKILL.md": "| name | kind | entry | verdict |\n|---|---|---|---|\n"
                "| t | gate | `scripts/t.py` | 0=ok |\n",
    "scripts/t.py": "print('t')\n",
}

# Defect routes: the counter must refuse each, with the NAMED finding present
# (refusal for the wrong reason does not count).  mode: "self" builds the
# identity surface from {**CLEAN, **defects} (self-consistent); "base" builds it
# from CLEAN alone (identity/token/content pins come from the base surface, so a
# mutation that strips or drifts pinned identity fires).  post: a callable run
# inside the fixture repo after the first commit (symlink planting).
# Clean routes: the counter must admit each (audit clean under mode "self").
# Every round-94 mutant class (MutC1 12 rows) maps onto >=1 route:
#   E1-gate-heading -> B01; E1-vacuity -> B21,Fv; E2-criteri -> C05;
#   E2-blob -> B18; E3-rowid -> B07; E3-locator -> B06; E4-deletion -> B13;
#   E4-blankline -> B19; E5-tree -> B08; E5-empty -> B09; E5-absence -> B12;
#   identity-pins -> B13,B14,B15,B20.
DEFECT_ROUTES = {
    "B01-gate-heading-missing": {
        "mode": "self",
        "expect": ("E1", "no '## Gate' heading"),
        "defects": {"corpus/lessons/round-02.md":
                    "# r2\n\nadmit C.\nreject D.\n\n"
                    "## Mistakes\n\n| # | Class |\n|---|---|\n| 1 | a |\n"}},
    "B02-gate-two-junk-lines": {
        "mode": "self",
        "expect": ("E1", "no admit decision line"),
        "defects": {"corpus/lessons/round-96.md":
                    "# r96\n\n## Gate\n\nlorem ipsum dolor sit amet.\n"
                    "consectetur adipiscing elit sed do.\n\n"
                    "## Mistakes\n\n| # | Class |\n|---|---|\n| 1 | a |\n"}},
    "B04-mistakes-indented": {
        "mode": "self",
        "expect": ("E4", "indented table row inside Mistakes"),
        "defects": {"corpus/lessons/round-02.md":
                    "# r2\n\n## Gate\n\nadmit C.\nreject D.\n\n"
                    "## Mistakes\n\n  | # | Class |\n  |---|---|\n  | 1 | a |\n"}},
    "B05-dual-source-lines": {
        "mode": "self",
        "expect": ("E3", "multiple source: lines"),
        "defects": {"corpus/knowledge/entry.md":
                    "source: S001\nsource: scripts/evil.py\n"
                    "verified-at: 2026-11-05\nrecheck: 180d\n\nbody\n"}},
    "B06-tmp-locator": {
        "mode": "self",
        "expect": ("E3", "non-citable locator"),
        "defects": {"corpus/knowledge/entry.md":
                    "source: /tmp/scratch/artifact.md\n"
                    "verified-at: 2026-11-05\nrecheck: 180d\n\nbody\n"}},
    "B07-prose-row-id": {
        "mode": "self",
        "expect": ("E3", "unresolved row id S999"),
        "defects": {"corpus/knowledge/entry.md":
                    "source: S999\nverified-at: 2026-11-05\nrecheck: 180d\n\nbody\n",
                    "corpus/SOURCES.md":
                    "# S\n\n## Registry\n\n| id | source |\n|---|---|\n"
                    "| S001 | x |\n\nprose mentions S999 without a row.\n"}},
    "B08-tree-path": {
        "mode": "self",
        "expect": ("E5", "names a tree, not a blob: corpus/knowledge"),
        "defects": {"SKILL.md": CLEAN["SKILL.md"] +
                    "| u | dir | `corpus/knowledge` | n/a |\n"}},
    "B09-empty-blob": {
        "mode": "self",
        "expect": ("E5", "names an empty blob: scripts/empty.py"),
        "defects": {"SKILL.md": CLEAN["SKILL.md"] +
                    "| u | stub | `scripts/empty.py` | n/a |\n",
                    "scripts/empty.py": ""}},
    "B10-symlink-path": {
        "mode": "self",
        "expect": ("E5", "names a symlink"),
        "defects": {"SKILL.md": CLEAN["SKILL.md"] +
                    "| u | link | `scripts/link.py` | n/a |\n"},
        "post": "symlink:scripts/link.py:t.py"},
    "B11-anchor-missing-blob": {
        "mode": "self",
        "expect": ("E5", "names missing path scripts/gone.py"),
        "defects": {"SKILL.md": CLEAN["SKILL.md"] +
                    "| u | anchor | `scripts/gone.py#L42` | n/a |\n"}},
    "B12-absence-unclosed": {
        "mode": "self",
        "expect": ("E5", "absence marker without a closing"),
        "defects": {"SKILL.md": CLEAN["SKILL.md"] +
                    "| u | ghost | [r95-absence 2026-11-05: "
                    "`scripts/t.py` gone | n/a |\n"}},
    "B13-mistakes-deletion": {
        "mode": "self",
        "mistakes_sections": ["corpus/lessons/round-01.md",
                              "corpus/lessons/round-02.md"],
        "expect": ("E4", "carried a Mistakes section at base"),
        "defects": {"corpus/lessons/round-02.md":
                    "# r2\n\n## Gate\n\nadmit C.\nreject D.\n"}},
    "B14-lesson-displaced": {
        "mode": "self",
        "expect": ("I", "lesson-displaced"),
        "defects": {"corpus/lessons/round-02.md":
                    "# r2\n\n## Gate\n\nadmit C.\nreject D.\n\n"
                    "## Mistakes\n\n| # | Class |\n|---|---|\n| 1 | a |\n",
                    "corpus/lessons/nested/round-02.md":
                    "# r2 twin\n\n## Gate\n\nadmit C.\nreject D.\n\n"
                    "## Mistakes\n\n| # | Class |\n|---|---|\n| 1 | a |\n"}},
    "B15-row-token-stripped": {
        "mode": "base",
        "expect": ("I", "skill_row_tokens"),
        "defects": {"SKILL.md":
                    "| name | kind | entry | verdict |\n|---|---|---|---|\n"
                    "| t | gate | unbackticked scripts/t.py | 0=ok |\n"}},
    "B16-annotated-present": {
        "mode": "self",
        "expect": ("E5", "annotated absent but present"),
        "defects": {"SKILL.md": CLEAN["SKILL.md"] +
                    "| u | ghost | [r95-absence 2026-11-05: "
                    "`scripts/t.py` absent] | ok |\n"}},
    "B18-criteria-empty-lesson": {
        "mode": "self",
        "expect": ("E2", "cites corpus/lessons/empty.md: blob of 0 bytes"),
        "defects": {"corpus/QUALITY.md":
                    CLEAN["corpus/QUALITY.md"] +
                    "\n## Round-02 criterion — empty cite\n\n"
                    "Grounded in `corpus/lessons/empty.md`.\n",
                    "corpus/lessons/empty.md": ""}},
    "B19-second-mistakes-blank-gap": {
        "mode": "self",
        "expect": ("E4", "blank line inside Mistakes section 2"),
        "defects": {"corpus/lessons/round-02.md":
                    "# r2\n\n## Gate\n\nadmit C.\nreject D.\n\n"
                    "## Mistakes\n\n| # | Class |\n|---|---|\n| 1 | a |\n\n"
                    "## Mistakes\n\n| # | Class |\n|---|---|\n| 1 | b |\n\n"
                    "| 2 | c |\n"}},
    "B20-lesson-content-drift": {
        "mode": "base",
        "expect": ("I", "lesson-content"),
        "defects": {"corpus/lessons/round-01.md":
                    "# r1 edited\n\n## Gate\n\nadmit A.\nreject B.\n\n"
                    "## Mistakes\n\n| # | Class |\n|---|---|\n| 1 | none |\n"}},
    "B21-vacuous-gate-zero-lines": {
        "mode": "self",
        "expect": ("E1", "vacuous Gate: fewer than two"),
        "defects": {"corpus/lessons/round-96.md":
                    "# r96\n\n## Gate\n\n## Mistakes\n\n"
                    "| # | Class |\n|---|---|\n| 1 | a |\n"}},
}

CLEAN_ROUTES = {
    "C01-line-suffix-existing": {
        "defects": {"SKILL.md": CLEAN["SKILL.md"] +
                    "| u | anchor | `scripts/t.py:12` | n/a |\n"}},
    "C02-anchor-existing": {
        "defects": {"SKILL.md": CLEAN["SKILL.md"] +
                    "| u | anchor | `scripts/t.py#L42` | n/a |\n"}},
    "C03-glob-skipped": {
        "defects": {"SKILL.md": CLEAN["SKILL.md"] +
                    "| u | glob | `scripts/*.py` | n/a |\n"}},
    "C04-indented-prose-not-table": {
        "defects": {"corpus/lessons/round-02.md":
                    "# r2\n\n## Gate\n\nadmit C.\nreject D.\n\n"
                    "## Mistakes\n\n| # | Class |\n|---|---|\n| 1 | a |\n\n"
                    "  indented prose is not a row.\n"}},
    "C05-non-criteria-round-section": {
        "defects": {"corpus/QUALITY.md":
                    CLEAN["corpus/QUALITY.md"] +
                    "\n## Round-02 notes — round management\n\n"
                    "Grounded in `corpus/lessons/gone.md`.\n"}},
}


def surfaces_of(files):
    """Synthetic identity surface for a fixture lane (battery/selftest only)."""
    lessons = sorted(k for k in files if k.startswith("corpus/lessons/"))
    first = []
    tokens = {}
    for line in files.get("SKILL.md", "").splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 4:
                first.append(cells[0])
                tokens[cells[0]] = tokens.get(cells[0], 0) + \
                    len(PATH_RE.findall(" ".join(cells)))
    entries = sorted(k for k in files if k.startswith("corpus/knowledge/"))
    return {
        "lessons": [{"path": p,
                     "sha256": hashlib.sha256(files[p].encode("utf-8")).hexdigest()}
                    for p in lessons],
        "entries": [{"path": p,
                     "head8_sha256": hashlib.sha256(
                         "\n".join(files[p].splitlines()[:8]).encode("utf-8")
                     ).hexdigest()}
                    for p in entries],
        "quality_criteria_headings": ["Round-01 criterion — a thing"],
        "skill_rows": [{"cell": c, "path_tokens": tokens[c]} for c in first],
        "mistakes_sections": [p for p in lessons if "## Mistakes" in files[p]],
    }


def legacy_surfaces_of(files):
    """The round-94 surfaces shape, for the predecessor's own audit calls."""
    lessons = sorted(k for k in files if k.startswith("corpus/lessons/"))
    first = []
    for line in files.get("SKILL.md", "").splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 4:
                first.append(cells[0])
    return {
        "lessons": lessons,
        "entries": sorted(k for k in files if k.startswith("corpus/knowledge/")),
        "quality_criteria_headings": ["Round-01 criterion — a thing"],
        "skill_row_first_cells": first,
        "mistakes_sections": [p for p in lessons if "## Mistakes" in files[p]],
    }


def make_repo(work, files):
    repo = os.path.join(work, "lane")
    shutil.rmtree(repo, ignore_errors=True)
    os.makedirs(repo)
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "battery@example.invalid")
    git(repo, "config", "user.name", "battery")
    write_files(repo, files)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "fixture")
    return repo, git(repo, "rev-parse", "HEAD").stdout.decode().strip()


def write_files(repo, files):
    for rel, text in files.items():
        dest = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(text)


def commit_files(repo, files):
    write_files(repo, files)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "mutate")
    return git(repo, "rev-parse", "HEAD").stdout.decode().strip()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _write(d, name, data):
    path = os.path.join(d, name)
    with open(path, "wb") as fh:
        fh.write(data)
    return path


def predecessor_clean(root, rev, files):
    """True when the frozen round-94 audit admits the fixture (its false-green)."""
    here = os.path.dirname(os.path.abspath(__file__))
    pred_local = os.path.normpath(os.path.join(here, "..", "..", "..",
                                               PREDECESSOR))
    if not os.path.exists(pred_local):
        return None
    pmod = load_module("pred_c94", pred_local)
    pins, short, ident, mm, _ = pmod.audit(root, rev, base_pins=SYNTH_PINS,
                                           surfaces=legacy_surfaces_of(files))
    return (not short) and (not ident) and (not mm)


def _apply_post(repo, spec):
    """Post-commit fixture hooks (e.g. symlink planting)."""
    if not spec:
        return
    if spec.startswith("symlink:"):
        _, link, target = spec.split(":", 2)
        os.symlink(target, os.path.join(repo, link))
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "symlink")


def battery(work, self_exe):
    """19 defect refusals + 5 clean admissions in-process, plus the F1e
    effectful-shadow route and the F2 canned-wrapper route.
    Returns (refused, total_defect, admitted, total_clean, shadow_absent,
    pred_admits, pred_scored, detail)."""
    detail = {}
    refused = admitted = 0
    pred_admits = pred_scored = 0

    for name, route in sorted(DEFECT_ROUTES.items()):
        files = dict(CLEAN)
        files.update(route["defects"])
        fdir = os.path.join(work, re.sub(r"[^A-Za-z0-9]+", "_", name))
        os.makedirs(fdir, exist_ok=True)
        repo, rev = make_repo(fdir, files)
        _apply_post(repo, route.get("post"))
        rev = git(repo, "rev-parse", "HEAD").stdout.decode().strip()
        base_files = {**CLEAN, **route["defects"]}
        surfaces = surfaces_of(base_files)
        if route.get("mistakes_sections") is not None:
            surfaces["mistakes_sections"] = route["mistakes_sections"]
        if route.get("mode") == "base":
            surfaces = surfaces_of(CLEAN)
        pins, short, ident, mm, counts = audit(repo, rev, base_pins=SYNTH_PINS,
                                               surfaces=surfaces)
        clean = (not short) and (not ident) and (not mm)
        cls, fragment = route["expect"]
        if cls == "I":
            hit = any(fragment in x for x in ident)
            refused_ok = (not clean) and hit
        else:
            hit = any(x["class"] == cls and fragment in x["detail"] for x in mm)
            refused_ok = (not clean) and hit
        refused += 1 if refused_ok else 0
        pred = predecessor_clean(repo, rev, files)
        if pred is not None:
            pred_scored += 1
            pred_admits += 1 if pred else 0
        detail[name] = {"refused_ok": refused_ok, "hit": hit,
                        "pred_admits": pred, "mismatches": len(mm),
                        "identity": len(ident)}

    for name, route in sorted(CLEAN_ROUTES.items()):
        files = dict(CLEAN)
        files.update(route["defects"])
        fdir = os.path.join(work, re.sub(r"[^A-Za-z0-9]+", "_", name))
        os.makedirs(fdir, exist_ok=True)
        repo, rev = make_repo(fdir, files)
        pins, short, ident, mm, counts = audit(repo, rev, base_pins=SYNTH_PINS,
                                               surfaces=surfaces_of(files))
        clean = (not short) and (not ident) and (not mm)
        admitted += 1 if clean else 0
        detail[name] = {"admitted": clean, "mismatches": len(mm)}

    # F1e (R94-2): an effectful subprocess.py beside the counter must never run.
    f1 = os.path.join(work, "F1e_effectful_shadow")
    os.makedirs(f1, exist_ok=True)
    marker = os.path.join(f1, "MARKER")
    with open(os.path.join(f1, "subprocess.py"), "w") as fh:
        fh.write("import os\nopen(%r, 'w').write('shadow-ran')\n"
                 "raise SystemExit(7)\n" % marker)
    counter_copy = os.path.join(f1, "c95.py")
    shutil.copyfile(self_exe, counter_copy)
    repo, rev = make_repo(os.path.join(f1, "lane"), CLEAN)
    env = {"PATH": "/usr/bin:/bin", "HOME": f1, "TMPDIR": f1, "PYTHONPATH": ""}
    try:
        p = subprocess.run([sys.executable, "-B", counter_copy, "--root", repo,
                            "--revision", rev, "--verdict-only",
                            "--base-pins-json", json.dumps(SYNTH_PINS)],
                           capture_output=True, timeout=120, env=env)
        rc, out = p.returncode, p.stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        rc, out = 124, "timeout"
    effect = os.path.exists(marker)
    shadow_ok = (not effect) and rc not in (7, 124)
    detail["F1e-effectful-shadow"] = {"marker_written": effect, "rc": rc,
                                      "line1": out.splitlines()[:1]}
    shadow_absent = 1 if shadow_ok else 0

    # F2: canned wrapper. The consumer demands the true counter digest on the
    # receipt line; a wrapper that prints a frozen-format line cannot know it.
    f2 = os.path.join(work, "F2_canned_wrapper")
    os.makedirs(f2, exist_ok=True)
    true_digest = self_sha()
    wrap = _write(f2, "wrapper.py", (
        "print('C1v95 revision=deadbeef counter=0000 lessons=2 entries=1 rows=2 "
        "criteria=1 mismatches=0 E1=0 E2=0 E3=0 E4=0 E5=0 pins=ok battery=19/19 "
        "admit=5/5 shadow=absent predecessor_admits=8/8 floor=4 self_pin=ok "
        "met=true')\n").encode())
    p2 = subprocess.run([sys.executable, "-B", wrap], capture_output=True,
                        timeout=60, env={"PATH": "/usr/bin:/bin", "HOME": f2,
                                         "TMPDIR": f2, "PYTHONPATH": ""})
    first = p2.stdout.decode("utf-8", "replace").splitlines()[:1]
    first = first[0] if first else ""
    f2_refused = ("counter=%s" % true_digest) not in first
    refused += 1 if f2_refused else 0
    detail["F2-canned-wrapper"] = {"line1": first[:200],
                                   "true_digest_present": not f2_refused}
    total_defect = len(DEFECT_ROUTES) + 1  # + F2
    return (refused, total_defect, admitted, len(CLEAN_ROUTES), shadow_absent,
            pred_admits, pred_scored, detail)


# ---------------------------------------------------------------- report --

def report(root, rev, base_pins, surfaces=None, self_pin=None, verdict_only=False,
           work=None):
    digest = self_sha()
    if self_pin is not None and self_pin != digest:
        print("C1v95 revision=%s counter=%s self_pin=mismatch met=false" % (rev, digest))
        print(json.dumps({"expected": self_pin, "actual": digest}, sort_keys=True))
        return 2
    if surfaces is None:
        surfaces = load_surfaces()
    pins, short, ident, mismatches, counts = audit(root, rev, base_pins=base_pins,
                                                   surfaces=surfaces)
    pins_state = "short" if short else ("identity" if ident else "ok")
    clean = (not short) and (not ident) and (not mismatches)
    if verdict_only:
        print("C1v95 revision=%s counter=%s lessons=%d entries=%d rows=%d "
              "criteria=%d mismatches=%d E1=%d E2=%d E3=%d E4=%d E5=%d pins=%s "
              "battery=skipped met=n/a verdict=%s"
              % (rev, digest, pins["lessons"], pins["entries"], pins["rows"],
                 pins["criteria"], len(mismatches), counts["E1"], counts["E2"],
                 counts["E3"], counts["E4"], counts["E5"], pins_state,
                 "clean" if clean else "failed"))
        print(json.dumps({"mismatches": mismatches, "identity_missing": ident,
                          "short": short, "pins": pins}, sort_keys=True))
        return 0 if clean else 1
    owned = work is None
    work = work or os.path.join(os.environ.get("TMPDIR", "/tmp"),
                                "c95bat-%d" % os.getpid())
    os.makedirs(work, exist_ok=True)
    try:
        (b_r, b_t, a_r, a_t, sh, p_a, p_n, b_detail) = battery(
            work, os.path.abspath(__file__))
    finally:
        if owned:
            shutil.rmtree(work, ignore_errors=True)
    met = clean and b_r == b_t and a_r == a_t and sh == 1 and p_a >= PREDECESSOR_FLOOR
    print("C1v95 revision=%s counter=%s lessons=%d entries=%d rows=%d criteria=%d "
          "mismatches=%d E1=%d E2=%d E3=%d E4=%d E5=%d pins=%s battery=%d/%d "
          "admit=%d/%d shadow=%s predecessor_admits=%d/%d floor=%d self_pin=ok "
          "met=%s"
          % (rev, digest, pins["lessons"], pins["entries"], pins["rows"],
             pins["criteria"], len(mismatches), counts["E1"], counts["E2"],
             counts["E3"], counts["E4"], counts["E5"], pins_state, b_r, b_t,
             a_r, a_t, "absent" if sh == 1 else "EFFECT", p_a, p_n,
             PREDECESSOR_FLOOR, str(met).lower()))
    print(json.dumps({"mismatches": mismatches, "identity_missing": ident,
                      "short": short, "pins": pins, "base_pins": base_pins,
                      "battery": b_detail}, sort_keys=True))
    return 0 if met else 1


# ---------------------------------------------------------------- selftest --

def selftest():
    base_tmp = os.path.join(os.environ.get("TMPDIR", "/tmp"),
                            "c95self-%d" % os.getpid())
    work = None
    try:
        work = os.path.join(base_tmp, "t")
        os.makedirs(work, exist_ok=True)
        repo, clean = make_repo(work, CLEAN)
        surfaces = surfaces_of(CLEAN)
        pins, short, ident, mismatches, counts = audit(
            repo, clean, base_pins=SYNTH_PINS, surfaces=surfaces)
        if mismatches or short or ident:
            print("selftest FAIL: clean fixture %r short=%r ident=%r"
                  % (mismatches, short, ident))
            return 1

        planted = dict(CLEAN)
        planted["corpus/lessons/round-02.md"] = (
            "# r2\n\n## Gate\n\nadmit C.\nreject D.\n")          # Mistakes gone
        planted["corpus/lessons/round-03.md"] = (
            "# r3\n\n## Gate\n\n## Mistakes\n\n  | 1 | a |\n")  # vacuous+indent
        planted["corpus/lessons/round-96.md"] = (
            "# r96\n\n## Gate\n\nlorem ipsum dolor sit amet.\n"
            "consectetur adipiscing elit sed do.\n\n## Mistakes\n\n"
            "| # | Class |\n|---|---|\n| 1 | a |\n")                 # junk gate
        planted["corpus/knowledge/entry2.md"] = (
            "source: S001\nsource: S404\nverified-at: 2026-11-05\n"
            "recheck: 90d\n\nbody\n")
        planted["corpus/knowledge/entry3.md"] = (
            "source: /tmp/scratch/x.md\nverified-at: 2026-11-05\n"
            "recheck: 90d\n\nbody\n")
        planted["corpus/QUALITY.md"] = CLEAN["corpus/QUALITY.md"] + (
            "\n## Round-02 criteria — another thing\n\n"
            "Grounded in `corpus/lessons/gone.md`.\n")
        planted["SKILL.md"] = ("| name | kind | entry | verdict |\n|---|---|---|---|\n"
                               "| t | gate | `scripts/t.py` | 0=ok |\n"
                               "| u | gone | `scripts/gone.py#L42` | 0=ok |\n"
                               "| v | dir | `corpus/knowledge` | n/a |\n"
                               "| w | stub | `scripts/empty.py` | n/a |\n"
                               "| x | link | `scripts/sym.py` | n/a |\n"
                               "| y | ghost | [r95-absence 2026-11-05: "
                               "`scripts/gone2.py` absent | ok |\n")
        planted["scripts/empty.py"] = ""
        bad = commit_files(repo, planted)
        os.symlink("t.py", os.path.join(repo, "scripts", "sym.py"))
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "symlink")
        bad = git(repo, "rev-parse", "HEAD").stdout.decode().strip()
        surfaces_planted = surfaces_of(planted)
        surfaces_planted["mistakes_sections"] = ["corpus/lessons/round-01.md",
                                                 "corpus/lessons/round-02.md"]
        pins, short, ident, mismatches, counts = audit(
            repo, bad, base_pins=SYNTH_PINS, surfaces=surfaces_planted)
        found = [(m["class"], m["detail"]) for m in mismatches]

        def has(cls, fragment):
            return any(c == cls and fragment in d for c, d in found)

        checks = {
            "E1 vacuous zero lines (r03)": has("E1", "vacuous Gate: fewer than two"),
            "E1 junk gate vocab (r96)": has("E1", "no admit decision line"),
            "E4 indented row (r03)": has("E4", "indented table row inside Mistakes"),
            "E4 deletion via identity (r02)": has("E4", "carried a Mistakes section"),
            "E3 dual source": has("E3", "multiple source: lines"),
            "E3 unresolved id": has("E3", "unresolved row id S404"),
            "E3 tmp locator": has("E3", "non-citable locator"),
            "E2 missing lesson": has("E2", "cites missing corpus/lessons/gone.md"),
            "E5 missing behind anchor": has("E5", "names missing path scripts/gone.py"),
            "E5 tree": has("E5", "names a tree, not a blob: corpus/knowledge"),
            "E5 empty blob": has("E5", "names an empty blob: scripts/empty.py"),
            "E5 symlink": has("E5", "names a symlink"),
            "E5 unclosed absence": has("E5", "absence marker without a closing"),
        }
        failed = [k for k, v in checks.items() if not v]
        if failed:
            print("selftest FAIL: %r not found in %r" % (failed, found))
            return 1
        if ident != ["mistakes_section:corpus/lessons/round-02.md"]:
            print("selftest FAIL: identity pin read %r" % (ident,))
            return 1
        if short:
            print("selftest FAIL: planted short=%r" % (short,))
            return 1

        repaired = dict(planted)
        repaired["corpus/lessons/round-02.md"] = (
            "# r2\n\n## Gate\n\nadmit C.\nreject D.\n\n## Mistakes\n\n"
            "| # | Class |\n|---|---|\n| 1 | a |\n")
        repaired["corpus/lessons/round-03.md"] = (
            "# r3\n\n## Gate\n\nadmit E.\nreject F.\n\n## Mistakes\n\n"
            "| # | Class |\n|---|---|\n| 1 | a |\n")
        repaired["corpus/lessons/round-96.md"] = (
            "# r96\n\n## Gate — admit the fix, reject the junk\n\n"
            "admit: the repaired gate.\nreject: the junk shape.\n\n"
            "## Mistakes\n\n| # | Class |\n|---|---|\n| 1 | a |\n")
        repaired["corpus/knowledge/entry2.md"] = (
            "source: S001\nverified-at: 2026-11-05\nrecheck: 90d\n\nbody\n")
        repaired["corpus/knowledge/entry3.md"] = (
            "source: S001 and SKILL.md\nverified-at: 2026-11-05\n"
            "recheck: 90d\n\nbody\n")
        repaired["corpus/QUALITY.md"] = CLEAN["corpus/QUALITY.md"] + (
            "\n## Round-02 criteria — another thing\n\n"
            "Grounded in `corpus/lessons/round-02.md`.\n")
        repaired["SKILL.md"] = ("| name | kind | entry | verdict |\n|---|---|---|---|\n"
                                "| t | gate | `scripts/t.py` | 0=ok |\n"
                                "| u | fixed | `scripts/t2.py` | 0=ok |\n"
                                "| v | dir | `scripts/t.py` | n/a |\n"
                                "| w | stub | `scripts/t2.py` | n/a |\n"
                                "| x | link | `scripts/t2.py` | n/a |\n"
                                "| y | ghost | [r95-absence 2026-11-05: "
                                "`scripts/gone2.py` absent] | ok |\n")
        repaired["scripts/t2.py"] = "print(1)\n"
        fixed = commit_files(repo, repaired)
        pins, short, ident, mismatches, counts = audit(
            repo, fixed, base_pins=SYNTH_PINS, surfaces=surfaces_of(repaired))
        if mismatches or short or ident:
            print("selftest FAIL: repaired reports %r short=%r ident=%r"
                  % (mismatches, short, ident))
            return 1

        # battery + predecessor floor on the frozen synthetic lanes
        (b_r, b_t, a_r, a_t, sh, p_a, p_n, b_detail) = battery(
            work, os.path.abspath(__file__))
        if b_r != b_t or a_r != a_t or sh != 1:
            print("selftest FAIL: battery %d/%d admit %d/%d shadow=%d"
                  % (b_r, b_t, a_r, a_t, sh))
            bad_routes = {k: v for k, v in b_detail.items()
                          if (k.startswith("B") and not v.get("refused_ok"))
                          or (k.startswith("C") and not v.get("admitted"))
                          or k == "F1e-effectful-shadow" and not sh}
            print("selftest FAIL routes: %s" % json.dumps(bad_routes, default=str)[:2000])
            return 1
        if p_n and p_a < PREDECESSOR_FLOOR:
            print("selftest FAIL: predecessor admits %d/%d < floor %d"
                  % (p_a, p_n, PREDECESSOR_FLOOR))
            return 1

        # R18 by execution: the CLI must refuse --surfaces-file.
        repo2, rev2 = make_repo(os.path.join(work, "flag"), CLEAN)
        env = {"PATH": "/usr/bin:/bin", "HOME": work, "TMPDIR": work,
               "PYTHONPATH": ""}
        pr = subprocess.run([sys.executable, "-B", os.path.abspath(__file__),
                             "--root", repo2, "--revision", rev2,
                             "--surfaces-file", "x.json"],
                            capture_output=True, timeout=60, env=env)
        if pr.returncode != 2:
            print("selftest FAIL: --surfaces-file accepted (rc=%d)" % pr.returncode)
            return 1

        print("selftest 13/13 planted findings, exit 1 on planted, exit 0 on "
              "repaired, battery %d/%d admit %d/%d shadow ok, "
              "predecessor_admits %d/%d, --surfaces-file refused"
              % (b_r, b_t, a_r, a_t, p_a, p_n))
        return 0
    finally:
        shutil.rmtree(base_tmp, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--revision")
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--self-pin")
    ap.add_argument("--verdict-only", action="store_true")
    ap.add_argument("--base-pins-json")
    try:
        a = ap.parse_args(argv)
    except SystemExit:
        raise
    try:
        shadow_check()
    except Unevaluable as exc:
        print("C1v95 selfcheck=shadowed met=false (%s)" % exc)
        return 2
    if a.selftest:
        return selftest()
    if not (a.root and a.revision):
        ap.error("--root and --revision are required")
    root = os.path.realpath(a.root)
    rev = git(root, "rev-parse", "%s^{commit}" % a.revision).stdout.decode().strip()
    if not rev:
        print("C1v95 revision=? unresolved")
        return 2
    if not (read(root, rev, "SKILL.md") and read(root, rev, "corpus/SOURCES.md")):
        print("C1v95 revision=%s unevaluable=missing-surface" % rev)
        return 2
    base_pins = json.loads(a.base_pins_json) if a.base_pins_json else None
    try:
        return report(root, rev, base_pins or BASE_PINS, surfaces=None,
                      self_pin=a.self_pin, verdict_only=a.verdict_only,
                      work=a.work)
    except Unevaluable as exc:
        print("C1v95 revision=%s unevaluable=%s" % (rev, exc))
        return 2


if __name__ == "__main__":
    sys.exit(main())
