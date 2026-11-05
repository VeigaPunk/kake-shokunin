#!/usr/bin/env python3
"""Round-94 C1 counter: self-assessment conformance, differential successor.

Frozen before data (`.ufo/waves/round-94/freeze.md`). Successor to the round-93
counter `.ufo/waves/round-93/c93_selfassess.py`, implementing routed defects
R93-1, R93-2, R93-3, R93-4, R93-5, R93-6 and R93-12.

Surface audit (strict E1-E5, identity-pinned population)

  E1  every lane-authored round lesson (corpus/lessons/round-*.md, excluding
      *-verifier-spotcheck.md and *aggregator*) carries a line exactly `## Gate`
      whose body holds at least two non-empty lines (a bare heading is vacuous).
  E2  every `## ` section of corpus/QUALITY.md whose heading matches
      `^Round[- ]<digits>` and whose first 400 characters mention "criteri"
      names at least one corpus/lessons/<file> path, and every such path
      resolves to a non-empty blob at the revision.
  E3  every corpus/knowledge/*.md carries non-empty `source:`, `verified-at:`
      and `recheck:` lines within its first 8 lines; every `S<digits>` id on its
      `source:` line resolves to a ROW-ID cell of corpus/SOURCES.md, not to a
      token in prose; and a `source:` line with no row id must carry a locator
      (an http(s) URL, `~/`, or a path-like token with a known suffix).
  E4  in every lane-authored round lesson, EVERY `## Mistakes` section has a
      contiguous table: each blank-line gap is reported. A lesson that carried
      a `## Mistakes` section at the base must still carry one.
  E5  every repo-relative path (`scripts/…`, `corpus/…`, `.ufo/…`) named inside
      a SKILL.md table row (brace lists expanded, trailing :line stripped,
      `<…>` placeholders and `*` skipped) must resolve to a NON-EMPTY BLOB.
      A directory or a 0-byte blob is a finding. A path named inside an explicit
      `[rNN-absence …]` span is an annotated absence: it is a finding only when
      the path exists at the revision.

Population pins (identity + cardinality): lesson, entry, SKILL-row and criteria
counts must each be >= the base measurement (`pins=short`), and every frozen
identity (lesson path, entry path, criteria heading, SKILL row first cell,
Mistakes carrier) must still be present (`pins=identity`). The frozen identity
surface is `frozen/c1-surfaces.json` beside this file, digest-pinned.

Self-integrity (R93-1, R93-2): line 1 prints `counter=<sha256 of this file>`.
`--self-pin <hex>` exits 2 unless the executed bytes hash to the pin. A process
whose `subprocess` module does not come from the standard library exits 2
`selfcheck=shadowed` before any measurement (route F1).

Differential battery (route-closure proof; met requires it): eight false-green
routes are built in scratch. This counter must refuse each (exit nonzero); the
frozen round-93 counter's own audit must admit at least PREDECESSOR_FLOOR of the
seven fixture routes, so the routes are live against the predecessor, not
blanket refusals. Routes: F1 shadow subprocess, F2 canned wrapper (no true
digest), F3 identity refill, F4 Mistakes deletion, F5 id-any-token, F6 tree
path, F6b empty blob, Fv vacuous Gate.

met <=> pins ok AND zero mismatches AND battery refused 8/8 AND predecessor
admits >= floor.

Output line 1:
  C1v94 revision=<sha> counter=<sha256> lessons=N entries=N rows=N criteria=N
        mismatches=N E1=a E2=b E3=c E4=d E5=e pins=ok|short|identity
        battery=R/8 predecessor_admits=N/7 floor=N self_pin=ok|mismatch met=…
line 2: JSON detail. Exit 0 iff met; 1 otherwise; 2 on unevaluable input.
--selftest plants one defect per strict class in a synthetic lane, asserts the
exact finding set, repairs it, and asserts exit 0.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

BASE = "0f7d9bbcdd6a9ed36f5bc62b2116ddd040e871a8"
BASE_PINS = {"lessons": 88, "entries": 81, "rows": 255, "criteria": 39}
SURFACES = "frozen/c1-surfaces.json"
SURFACES_SHA = "b911321d780c2c6815eb2d235c10626812491f21a0fd00f6a1e7b7a6cd6e4e6e"
PREDECESSOR = ".ufo/waves/round-93/c93_selfassess.py"
PREDECESSOR_FLOOR = 2
SYNTH_PINS = {"lessons": 2, "entries": 1, "rows": 2, "criteria": 1}
LESSON_SKIP = ("-verifier-spotcheck.md",)
PATH_RE = re.compile(r"`((?:scripts|corpus|\.ufo)/[^`\s]+)`")
ABSENCE_SPAN_RE = re.compile(r"\[r\d{2}-absence\b[^\]]*\]")
ID_RE = re.compile(r"S\d{3,}")
CRIT_RE = re.compile(r"Round[- ]\d+")
ROW_ID_RE = re.compile(r"^\|[ \t]*(S[0-9]{3,})[ \t]*\|")
LOCATOR_RE = re.compile(
    r"https?://|~/|[A-Za-z0-9._/~\-]+\.(?:md|py|mjs|json|txt|html|yml|yaml)\b")
STD_PREFIXES = tuple(
    p for p in {sys.prefix, sys.base_prefix, os.path.dirname(os.__file__)} if p)


class Unevaluable(Exception):
    pass


def self_sha():
    with open(os.path.abspath(__file__), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def shadow_check():
    """Route F1: refuse a subprocess module that is not the stdlib one."""
    path = getattr(subprocess, "__file__", "") or ""
    if not path or not os.path.abspath(path).startswith(STD_PREFIXES):
        raise Unevaluable("subprocess module is shadowed: %r" % path)


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True)


def read(root, rev, path):
    p = git(root, "show", "%s:%s" % (rev, path))
    return p.stdout.decode("utf-8", "replace") if p.returncode == 0 else None


def blob_meta(root, rev, path):
    """(kind, size) of rev:path, or None when absent."""
    p = git(root, "cat-file", "-t", "%s:%s" % (rev, path))
    if p.returncode != 0:
        return None
    kind = p.stdout.decode().strip()
    s = git(root, "cat-file", "-s", "%s:%s" % (rev, path))
    size = int(s.stdout.decode().strip()) if s.returncode == 0 else -1
    return kind, size


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
    """Bodies of every `## <heading>` section (exact heading line)."""
    return [m.group(1) for m in
            re.finditer(r"(?m)^## %s\s*$(.*?)(?=^## |\Z)" % heading, text, re.S)]


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
        gates = sections(text, "Gate")
        if not gates:
            mismatches.append({"class": "E1", "path": path,
                               "detail": "no '## Gate' heading"})
        for body in gates:
            if len([l for l in body.splitlines() if l.strip()]) < 2:
                mismatches.append({"class": "E1", "path": path,
                                   "detail": "vacuous Gate: fewer than two "
                                             "non-empty body lines"})
                break
        mistakes = sections(text, "Mistakes")
        for idx, body in enumerate(mistakes):
            lines = body.splitlines()
            for i in range(len(lines) - 2):
                if (lines[i].startswith("|") and lines[i + 1].strip() == ""
                        and lines[i + 2].startswith("|")):
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
        m = re.search(r"(?m)^source:.*$", head)
        if m:
            line = m.group(0)
            ids_here = set(ID_RE.findall(line))
            unresolved = sorted(i for i in ids_here if i not in row_ids)
            if unresolved:
                problems.append("unresolved row id " + ", ".join(unresolved))
            elif not ids_here and not LOCATOR_RE.search(line):
                problems.append("vacuous source: no row id, URL or path locator")
        if problems:
            mismatches.append({"class": "E3", "path": path,
                               "detail": "; ".join(problems)})

    skill = read(root, rev, "SKILL.md") or ""
    rows = 0
    first_cells = []
    for line in skill.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        rows += 1
        first_cells.append(cells[0])
        body = " ".join(cells)
        absent = set()
        for span in ABSENCE_SPAN_RE.findall(body):
            absent.update(re.sub(r":\d+(-\d+)?$", "", p).rstrip("`,.")
                          for p in PATH_RE.findall(span))
        seen = set()
        for raw in PATH_RE.findall(body):
            raw = re.sub(r":\d+(-\d+)?$", "", raw).rstrip("`,.")
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

    pins = {"lessons": len(lessons), "entries": len(entries), "rows": rows,
            "criteria": len(criteria)}
    base_pins = BASE_PINS if base_pins is None else base_pins
    short = [k for k, v in base_pins.items() if pins[k] < v]
    ident = []
    for p in surfaces["lessons"]:
        if p not in lesson_texts:
            ident.append("lesson:" + p)
    for p in surfaces["entries"]:
        if p not in entries:
            ident.append("entry:" + p)
    for h in surfaces["quality_criteria_headings"]:
        if h not in criteria:
            ident.append("criterion:" + h)
    for c in surfaces["skill_row_first_cells"]:
        if c not in first_cells:
            ident.append("skill_row:" + c)
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


def surfaces_of(files):
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


class _Proc:
    def __init__(self, rc, out, err=b""):
        self.returncode = rc
        self.stdout = out
        self.stderr = err


def injected_git(files, rev):
    """In-process stand-in for `git -C <root>` over a canned lane (route F1 as
    seen by the predecessor's own git calls)."""
    def run(argv, capture_output=True, **kw):
        args = list(argv)
        if "-C" in args:
            args = args[args.index("-C") + 2:]
        sub, rest = args[0], args[1:]
        if sub == "rev-parse":
            return _Proc(0, (rev + "\n").encode())
        if sub == "show":
            path = rest[0].split(":", 1)[1]
            if path in files:
                return _Proc(0, files[path].encode())
            if any(p.startswith(path.rstrip("/") + "/") for p in files):
                return _Proc(0, (path + "/\n").encode())
            return _Proc(128, b"", b"fatal: path missing")
        if sub == "ls-tree":
            prefix = rest[-1].rstrip("/") + "/"
            names = sorted(p for p in files if p.startswith(prefix))
            return _Proc(0, ("\n".join(names) + "\n").encode() if names else b"")
        return _Proc(128, b"", b"unsupported")
    return run


def run_counter(exe, repo, rev, surfaces_path, work, pins=SYNTH_PINS):
    env = {"PATH": "/usr/bin:/bin", "HOME": work, "TMPDIR": work,
           "PYTHONPATH": ""}
    argv = [sys.executable, "-B", exe, "--root", repo, "--revision", rev,
            "--skip-battery", "--base-pins-json", json.dumps(pins),
            "--surfaces-file", surfaces_path]
    try:
        p = subprocess.run(argv, capture_output=True, timeout=120, env=env)
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    out = p.stdout.decode("utf-8", "replace").splitlines()
    return p.returncode, (out[0] if out else "")


def battery(work, self_exe):
    """Eight false-green routes. Returns (refused, total, admits, scored, detail)."""
    here = os.path.dirname(self_exe)
    pred_bytes = None
    pred_local = os.path.join(here, "..", "..", "..", PREDECESSOR)
    if os.path.exists(pred_local):
        pred_bytes = open(pred_local, "rb").read()
    detail = {}

    fixtures = {}
    f3 = dict(CLEAN)
    del f3["corpus/lessons/round-02.md"]
    f3["corpus/lessons/round-03.md"] = (
        "# r3\n\n## Gate\n\nadmit X.\nreject Y.\n\n## Mistakes\n\n"
        "| # | Class |\n|---|---|\n| 1 | none |\n")
    fixtures["F3-identity-refill"] = (f3, None)

    fixtures["F4-mistakes-deletion"] = (
        dict(CLEAN, **{"corpus/lessons/round-02.md":
                       "# r2\n\n## Gate\n\nadmit C.\nreject D.\n"}), None)

    f5 = dict(CLEAN)
    f5["corpus/knowledge/entry.md"] = ("source: S999\nverified-at: 2026-11-05\n"
                                       "recheck: 180d\n\nbody\n")
    f5["corpus/SOURCES.md"] = ("# S\n\n## Registry\n\n| id | source |\n|---|---|\n"
                               "| S001 | x |\n\nprose mentions S999 without a row.\n")
    fixtures["F5-id-any-token"] = (f5, None)

    f6 = dict(CLEAN)
    f6["SKILL.md"] = (CLEAN["SKILL.md"] + "| u | dir | `corpus/knowledge` | n/a |\n")
    fixtures["F6-tree-path"] = (f6, None)

    f6b = dict(CLEAN)
    f6b["SKILL.md"] = (CLEAN["SKILL.md"] + "| u | stub | `scripts/empty.py` | n/a |\n")
    f6b["scripts/empty.py"] = ""
    fixtures["F6b-empty-blob"] = (f6b, None)

    fv = dict(CLEAN)
    fv["corpus/lessons/round-02.md"] = "# r2\n\n## Gate\n\n## Mistakes\n\n"
    fixtures["Fv-vacuous-gate"] = (fv, None)

    refused = 0
    admits = 0
    scored = 0
    total = 0
    for name, (files, _) in sorted(fixtures.items()):
        total += 1
        fdir = os.path.join(work, re.sub(r"[^A-Za-z0-9]+", "_", name))
        os.makedirs(fdir, exist_ok=True)
        repo, rev = make_repo(fdir, files)
        surf_path = os.path.join(fdir, "surfaces.json")
        with open(surf_path, "w") as fh:
            json.dump(surfaces_of(CLEAN), fh)
        rc, line1 = run_counter(self_exe, repo, rev, surf_path, fdir)
        refused += 1 if rc != 0 else 0
        pred_rc = None
        if pred_bytes is not None:
            scored += 1
            pmod = load_module("pred_" + re.sub(r"\W", "_", name),
                               _write(fdir, "pred.py", pred_bytes))
            pins, short, mm, counts, _ = pmod.audit(repo, rev, base_pins=SYNTH_PINS)
            pred_rc = 0 if ((not short) and not mm) else 1
            admits += 1 if pred_rc == 0 else 0
        detail[name] = {"self_rc": rc, "self_line1": line1[:200], "pred_rc": pred_rc}

    # F1: shadow subprocess. (a) the counter refuses a real path shadow;
    # (b) the predecessor, driven through an injected git, admits the lane.
    total += 1
    f1 = os.path.join(work, "F1_shadow_subprocess")
    os.makedirs(f1, exist_ok=True)
    shadow_dir = os.path.join(f1, "shadow")
    os.makedirs(shadow_dir)
    with open(os.path.join(shadow_dir, "subprocess.py"), "w") as fh:
        fh.write("class CompletedProcess: pass\n"
                 "def run(*a, **k):\n"
                 "    raise SystemExit('shadow: no real git')\n")
    counter_copy = os.path.join(shadow_dir, "c94.py")
    shutil.copyfile(self_exe, counter_copy)
    repo, rev = make_repo(os.path.join(f1, "lane"), CLEAN)
    surf_path = os.path.join(f1, "surfaces.json")
    with open(surf_path, "w") as fh:
        json.dump(surfaces_of(CLEAN), fh)
    env = {"PATH": "/usr/bin:/bin", "HOME": f1, "TMPDIR": f1, "PYTHONPATH": ""}
    p = subprocess.run([sys.executable, "-B", counter_copy, "--root", repo,
                        "--revision", rev, "--skip-battery", "--surfaces-file",
                        surf_path, "--base-pins-json", json.dumps(SYNTH_PINS)],
                       capture_output=True, timeout=120, env=env)
    line1 = p.stdout.decode("utf-8", "replace").splitlines()[:1]
    self_refused = p.returncode == 2 and "shadowed" in (line1[0] if line1 else "")
    refused += 1 if self_refused else 0
    pred_admit = None
    if pred_bytes is not None:
        scored += 1
        pmod = load_module("pred_f1", _write(f1, "pred.py", pred_bytes))
        real_run = subprocess.run
        subprocess.run = injected_git(CLEAN, rev)
        try:
            pins, short, mm, counts, _ = pmod.audit(repo, rev, base_pins=SYNTH_PINS)
            pred_admit = (not short) and not mm
        finally:
            subprocess.run = real_run
        admits += 1 if pred_admit else 0
    detail["F1-shadow-subprocess"] = {"self_rc": p.returncode,
                                      "self_line1": (line1[0] if line1 else "")[:200],
                                      "pred_admits_injected": pred_admit}

    # F2: canned wrapper. The consumer demands the true counter digest on the
    # receipt line; a wrapper that prints a frozen-format line cannot know it.
    total += 1
    f2 = os.path.join(work, "F2_canned_wrapper")
    os.makedirs(f2, exist_ok=True)
    wrap = _write(f2, "wrapper.py", (
        "print('C1v94 revision=deadbeef counter=0000 lessons=2 entries=1 rows=2 "
        "criteria=1 mismatches=0 E1=0 E2=0 E3=0 E4=0 E5=0 pins=ok battery=8/8 "
        "predecessor_admits=7/7 floor=2 self_pin=ok met=true')\n").encode())
    p2 = subprocess.run([sys.executable, "-B", wrap], capture_output=True,
                        timeout=60, env={"PATH": "/usr/bin:/bin", "HOME": f2,
                                         "TMPDIR": f2, "PYTHONPATH": ""})
    first = p2.stdout.decode("utf-8", "replace").splitlines()[:1]
    first = first[0] if first else ""
    true_digest = self_sha()
    refused_f2 = ("counter=%s" % true_digest) not in first
    refused += 1 if refused_f2 else 0
    detail["F2-canned-wrapper"] = {"line1": first[:200],
                                   "true_digest_present": not refused_f2}
    return refused, total, admits, scored, detail


def _write(d, name, data):
    path = os.path.join(d, name)
    with open(path, "wb") as fh:
        fh.write(data)
    return path


# ---------------------------------------------------------------- report --

def report(root, rev, base_pins, surfaces=None, self_pin=None, skip_battery=False,
            work=None):
    digest = self_sha()
    if self_pin is not None and self_pin != digest:
        print("C1v94 revision=%s counter=%s self_pin=mismatch met=false" % (rev, digest))
        print(json.dumps({"expected": self_pin, "actual": digest}, sort_keys=True))
        return 2
    if surfaces is None:
        surfaces = load_surfaces()
    pins, short, ident, mismatches, counts = audit(root, rev, base_pins=base_pins,
                                                   surfaces=surfaces)
    pins_state = "short" if short else ("identity" if ident else "ok")
    b_r, b_t, p_a, p_n, b_detail = 0, 8, 0, 0, {}
    if not skip_battery:
        owned = work is None
        work = work or os.path.join(os.environ.get("TMPDIR", "/tmp"),
                                    "c94bat-%d" % os.getpid())
        os.makedirs(work, exist_ok=True)
        try:
            b_r, b_t, p_a, p_n, b_detail = battery(work, os.path.abspath(__file__))
        finally:
            if owned:
                shutil.rmtree(work, ignore_errors=True)
    met = (not short) and (not ident) and (not mismatches) and (
        skip_battery or (b_r == b_t and p_a >= PREDECESSOR_FLOOR))
    print("C1v94 revision=%s counter=%s lessons=%d entries=%d rows=%d criteria=%d "
          "mismatches=%d E1=%d E2=%d E3=%d E4=%d E5=%d pins=%s battery=%d/%d "
          "predecessor_admits=%d/%d floor=%d self_pin=%s met=%s"
          % (rev, digest, pins["lessons"], pins["entries"], pins["rows"],
             pins["criteria"], len(mismatches), counts["E1"], counts["E2"],
             counts["E3"], counts["E4"], counts["E5"], pins_state, b_r, b_t,
             p_a, p_n, PREDECESSOR_FLOOR,
             "ok", str(met).lower()))
    print(json.dumps({"mismatches": mismatches, "identity_missing": ident,
                      "short": short, "pins": pins, "base_pins": base_pins,
                      "battery": b_detail}, sort_keys=True))
    return 0 if met else 1


# ---------------------------------------------------------------- selftest --

def selftest():
    work = os.path.join(os.environ.get("TMPDIR", "/tmp"), "c94self-%d" % os.getpid())
    try:
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
            "# r2\n\n## Gate\n\n## Mistakes\n\n| # | Class |\n|---|---|\n"
            "| 1 | a |\n\n| 2 | b |\n")
        planted["corpus/lessons/round-03.md"] = "# r3\n\n## Gate\n\nadmit E.\nreject F.\n"
        planted["corpus/knowledge/entry2.md"] = "source: S404\n\nbody\n"
        planted["corpus/knowledge/entry3.md"] = (
            "source: an assertion without a locator\nverified-at: 2026-11-05\n"
            "recheck: 90d\n\nbody\n")
        planted["corpus/QUALITY.md"] = CLEAN["corpus/QUALITY.md"] + (
            "\n## Round-02 criteria — another thing\n\n"
            "Grounded in `corpus/lessons/gone.md`.\n")
        planted["SKILL.md"] = ("| name | kind | entry | verdict |\n|---|---|---|---|\n"
                               "| t | gate | `scripts/t.py` | 0=ok |\n"
                               "| u | gone | `scripts/gone.py` | 0=ok |\n"
                               "| v | dir | `corpus/knowledge` | n/a |\n"
                               "| w | stub | `scripts/empty.py` | n/a |\n"
                               "| x | ghost | [r94-absence 2026-11-05: "
                               "`scripts/t.py` absent] | ok |\n"
                               "| y | note | [r94-absence 2026-11-05: "
                               "`scripts/gone2.py` absent] | ok |\n")
        planted["scripts/empty.py"] = ""
        bad = commit_files(repo, planted)
        surfaces_planted = surfaces_of(planted)
        surfaces_planted["mistakes_sections"] = ["corpus/lessons/round-03.md"]
        surfaces_planted["lessons"] = surfaces["lessons"] + ["corpus/lessons/round-03.md"]
        pins, short, ident, mismatches, counts = audit(
            repo, bad, base_pins=SYNTH_PINS, surfaces=surfaces_planted)
        found = [(m["class"], m["detail"]) for m in mismatches]

        def has(cls, fragment):
            return any(c == cls and fragment in d for c, d in found)

        checks = {
            "E1 vacuous gate": has("E1", "vacuous Gate: fewer than"),
            "E4 blank line": has("E4", "blank line inside Mistakes section 1"),
            "E3 unresolved id": has("E3", "unresolved row id S404"),
            "E3 vacuous locator": has("E3", "vacuous source: no row id"),
            "E2 missing lesson": has("E2", "cites missing corpus/lessons/gone.md"),
            "E5 missing path": has("E5", "names missing path scripts/gone.py"),
            "E5 tree": has("E5", "names a tree, not a blob: corpus/knowledge"),
            "E5 empty blob": has("E5", "names an empty blob: scripts/empty.py"),
            "E5 annotated-present": has(
                "E5", "annotated absent but present at the revision: scripts/t.py"),
        }
        failed = [k for k, v in checks.items() if not v]
        if failed:
            print("selftest FAIL: %r not found in %r" % (failed, found))
            return 1
        if any(c == "E5" and "gone2" in d for c, d in found):
            print("selftest FAIL: annotated-absent path reported as present")
            return 1
        if ident != ["mistakes_section:corpus/lessons/round-03.md"]:
            print("selftest FAIL: identity pin read %r" % (ident,))
            return 1
        if short:
            print("selftest FAIL: planted short=%r" % (short,))
            return 1

        repaired = dict(planted)
        repaired["corpus/lessons/round-03.md"] = (
            "# r3\n\n## Gate\n\nadmit E.\nreject F.\n\n## Mistakes\n\n"
            "| # | Class |\n|---|---|\n| 1 | a |\n")
        repaired["corpus/lessons/round-02.md"] = (
            "# r2\n\n## Gate\n\nadmit C.\nreject D.\n\n## Mistakes\n\n"
            "| # | Class |\n|---|---|\n| 1 | a |\n| 2 | b |\n")
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
                                "| v | dir | `scripts/t.py` | 0=ok |\n"
                                "| w | stub | `scripts/t2.py` | 0=ok |\n"
                                "| x | ghost | [r94-absence 2026-11-05: "
                                "`scripts/annotated.py` absent] | ok |\n"
                                "| y | note | [r94-absence 2026-11-05: "
                                "`scripts/gone2.py` absent] | ok |\n")
        repaired["scripts/t2.py"] = "print(1)\n"
        fixed = commit_files(repo, repaired)
        pins, short, ident, mismatches, counts = audit(
            repo, fixed, base_pins=SYNTH_PINS, surfaces=surfaces_planted)
        if mismatches or short or ident:
            print("selftest FAIL: repaired reports %r short=%r ident=%r"
                  % (mismatches, short, ident))
            return 1
        print("selftest 9/9 planted findings, exit 1 on planted, exit 0 on repaired")
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--revision")
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--self-pin")
    ap.add_argument("--skip-battery", action="store_true")
    ap.add_argument("--base-pins-json")
    ap.add_argument("--surfaces-file")
    a = ap.parse_args(argv)
    try:
        shadow_check()
    except Unevaluable as exc:
        print("C1v94 selfcheck=shadowed met=false (%s)" % exc)
        return 2
    if a.selftest:
        return selftest()
    if not (a.root and a.revision):
        ap.error("--root and --revision are required")
    root = os.path.realpath(a.root)
    rev = git(root, "rev-parse", "%s^{commit}" % a.revision).stdout.decode().strip()
    if not rev:
        print("C1v94 revision=? unresolved")
        return 2
    if not (read(root, rev, "SKILL.md") and read(root, rev, "corpus/SOURCES.md")):
        print("C1v94 revision=%s unevaluable=missing-surface" % rev)
        return 2
    base_pins = json.loads(a.base_pins_json) if a.base_pins_json else None
    surfaces = None
    if a.surfaces_file:
        with open(a.surfaces_file) as fh:
            surfaces = json.load(fh)
    try:
        return report(root, rev, base_pins or BASE_PINS, surfaces=surfaces,
                      self_pin=a.self_pin, skip_battery=a.skip_battery,
                      work=a.work)
    except Unevaluable as exc:
        print("C1v94 revision=%s unevaluable=%s" % (rev, exc))
        return 2


if __name__ == "__main__":
    sys.exit(main())
