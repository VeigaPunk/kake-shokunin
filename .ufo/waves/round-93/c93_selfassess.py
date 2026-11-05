#!/usr/bin/env python3
"""Round-93 C1 counter: self-assessment conformance (calibration axis).

Frozen before data (`.ufo/waves/round-93/freeze.md`). Reads committed bytes at
--revision and counts every place where the lane's own machine-checkable
self-assessment statements disagree with the repo state they describe. Each
mismatch is printed with its class, file and the exact disagreement, so a closure
can re-derive any single row with `git show` and `grep` — the verdict is the
enumerated list, not this program's opinion.

Frozen population (five classes; each predicate is one sentence in
`.ufo/waves/round-93/c1-predicate.md`):

  E1  every lane-authored round lesson (corpus/lessons/round-*.md, excluding
      *-verifier-spotcheck.md and *aggregator*) carries a line exactly `## Gate`.
  E2  every `## ` section of corpus/QUALITY.md whose heading matches
      `^Round[- ]<digits>` and whose first 400 characters mention "criteri"
      names at least one existing `corpus/lessons/<file>` path.
  E3  every corpus/knowledge/*.md carries non-empty `source:`, `verified-at:`
      and `recheck:` lines within its first 8 lines, and every `S<digits>` id on
      its `source:` line resolves to a row id in corpus/SOURCES.md.
  E4  in every lane-authored round lesson, the `## Mistakes` table is contiguous:
      no blank line sits between two lines that both start with `|`.
  E5  every repo-relative path (`scripts/…`, `corpus/…`, `.ufo/…`) named inside a
      SKILL.md table row exists at the revision (brace lists expanded, a trailing
      `:<line>`/`:<start>-<end>` stripped, `<…>` placeholders and `*` skipped).

Population pins: the lesson count, entry count, SKILL.md table-row count and
QUALITY criteria-section count must each be >= the base measurement; a shrunken
population is `pins=short` and met=false regardless of mismatch count, so
deleting the surface cannot buy a pass.

met <=> pins ok AND mismatches == 0.

Output line 1:
  C1v93 revision=<sha> lessons=N entries=N rows=N criteria=N mismatches=N
        E1=a E2=b E3=c E4=d E5=e pins=ok|short met=true|false
line 2: JSON detail listing every mismatch.
Exit 0 iff met; 1 otherwise; 2 on unevaluable input.
--selftest builds a synthetic lane in a scratch git repo, plants one defect per
class, asserts the exact finding set and exit 1, then repairs them and asserts
exit 0.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

BASE = "10ecbd1ade91d0721e87a9942a66a2b61d5ce8d5"
BASE_PINS = {"lessons": 87, "entries": 80, "rows": 255, "criteria": 39}
LESSON_SKIP = ("-verifier-spotcheck.md",)
PATH_RE = re.compile(r"`((?:scripts|corpus|\.ufo)/[^`\s]+)`")
ID_RE = re.compile(r"S\d{3,}")
CRIT_RE = re.compile(r"Round[- ]\d+")


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True)


def read(root, rev, path):
    p = git(root, "show", "%s:%s" % (rev, path))
    return p.stdout.decode("utf-8", "replace") if p.returncode == 0 else None


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


def audit(root, rev, base_pins=None):
    mismatches = []
    detail = {}

    # --- E1 / E4: lane-authored round lessons
    lessons = [p for p in listing(root, rev, "corpus/lessons")
               if re.search(r"/(round-[^/]*\.md)$", p)
               and not any(p.endswith(s) for s in LESSON_SKIP)
               and "aggregator" not in p]
    for path in sorted(lessons):
        text = read(root, rev, path) or ""
        if not re.search(r"(?m)^## Gate\s*$", text):
            mismatches.append({"class": "E1", "path": path,
                               "detail": "no '## Gate' heading"})
        sec = re.search(r"(?m)^## Mistakes\s*$(.*?)(?=^## |\Z)", text, re.S)
        if sec:
            lines = sec.group(1).splitlines()
            for i in range(len(lines) - 2):
                if (lines[i].startswith("|") and lines[i + 1].strip() == ""
                        and lines[i + 2].startswith("|")):
                    mismatches.append({
                        "class": "E4", "path": path,
                        "detail": "blank line inside the Mistakes table after row %d"
                                  % (i + 1)})
                    break

    # --- E2: QUALITY criteria sections
    quality = read(root, rev, "corpus/QUALITY.md") or ""
    criteria = 0
    for section in re.split(r"(?m)^## ", quality)[1:]:
        head = section.splitlines()[0].strip() if section.splitlines() else ""
        if not CRIT_RE.match(head):
            continue
        if not re.search(r"criteri", section[:400], re.I):
            continue
        criteria += 1
        cited = re.findall(r"corpus/lessons/[A-Za-z0-9._-]+", section)
        if not cited:
            mismatches.append({"class": "E2", "path": "corpus/QUALITY.md",
                               "detail": "section %r names no corpus/lessons/ file"
                                         % head})
            continue
        missing = [c for c in cited if read(root, rev, c) is None]
        if missing:
            mismatches.append({"class": "E2", "path": "corpus/QUALITY.md",
                               "detail": "section %r cites missing %s"
                                         % (head, ", ".join(sorted(set(missing))))})

    # --- E3: knowledge entry metadata
    sources = read(root, rev, "corpus/SOURCES.md") or ""
    ids = set(ID_RE.findall(sources))
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
            unresolved = sorted({i for i in ID_RE.findall(m.group(0)) if i not in ids})
            if unresolved:
                problems.append("unresolved " + ", ".join(unresolved))
        if problems:
            mismatches.append({"class": "E3", "path": path,
                               "detail": "; ".join(problems)})

    # --- E5: SKILL.md table rows name existing repo paths
    skill = read(root, rev, "SKILL.md") or ""
    rows = 0
    for line in skill.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        rows += 1
        body = " ".join(cells)
        seen = set()
        for raw in PATH_RE.findall(body):
            raw = re.sub(r":\d+(-\d+)?$", "", raw).rstrip("`,.")
            for path in expand_braces(raw):
                if "<" in path or "*" in path or path in seen:
                    continue
                seen.add(path)
                if read(root, rev, path) is None:
                    mismatches.append({"class": "E5", "path": "SKILL.md",
                                       "detail": "names missing path %s" % path})

    pins = {"lessons": len(lessons), "entries": len(entries), "rows": rows,
            "criteria": criteria}
    base_pins = BASE_PINS if base_pins is None else base_pins
    short = [k for k, v in base_pins.items() if pins[k] < v]
    detail.update({"pins": pins, "base_pins": base_pins, "short": short,
                   "mismatches": mismatches})
    counts = {c: sum(1 for m in mismatches if m["class"] == c) for c in
              ("E1", "E2", "E3", "E4", "E5")}
    return pins, short, mismatches, counts, detail


def report(root, rev):
    pins, short, mismatches, counts, detail = audit(root, rev)
    met = (not short) and not mismatches
    print("C1v93 revision=%s lessons=%d entries=%d rows=%d criteria=%d mismatches=%d "
          "E1=%d E2=%d E3=%d E4=%d E5=%d pins=%s met=%s"
          % (rev, pins["lessons"], pins["entries"], pins["rows"], pins["criteria"],
             len(mismatches), counts["E1"], counts["E2"], counts["E3"], counts["E4"],
             counts["E5"], "ok" if not short else "short", str(met).lower()))
    print(json.dumps(detail, sort_keys=True))
    return 0 if met else 1


CLEAN = {
    "corpus/lessons/round-01.md": "# r1\n\n## Gate\n\nadmit.\n\n## Mistakes\n\n"
                                  "| # | Class |\n|---|---|\n| 1 | none |\n",
    "corpus/knowledge/entry.md": "source: S001\nverified-at: 2026-11-04\nrecheck: 180d\n\nbody\n",
    "corpus/QUALITY.md": "# Q\n\n## Round-01 criterion — a thing\n\n"
                         "Grounded in `corpus/lessons/round-01.md`.\n",
    "corpus/SOURCES.md": "| S001 | x |\n",
    "SKILL.md": "| name | kind | entry | verdict |\n|---|---|---|---|\n"
                "| t | gate | `scripts/t.py` | 0=ok |\n",
    "scripts/t.py": "print('t')\n",
}


def selftest():
    work = os.path.join(os.environ.get("TMPDIR", "/tmp"), "c93self-%d" % os.getpid())
    try:
        os.makedirs(work, exist_ok=True)
        repo = os.path.join(work, "lane")
        os.mkdir(repo)
        git(repo, "init", "-q")
        git(repo, "config", "user.email", "selftest@example.invalid")
        git(repo, "config", "user.name", "selftest")

        def write_all(files):
            for rel, text in files.items():
                dest = os.path.join(repo, rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "w", encoding="utf-8") as fh:
                    fh.write(text)

        def commit(msg):
            git(repo, "add", "-A")
            git(repo, "commit", "-q", "-m", msg)
            return git(repo, "rev-parse", "HEAD").stdout.decode().strip()

        write_all(CLEAN)
        clean = commit("clean")
        synth = {"lessons": 1, "entries": 1, "rows": 1, "criteria": 1}
        pins, short, mismatches, counts, _ = audit(repo, clean, base_pins=synth)
        if mismatches or short:
            print("selftest FAIL: clean fixture reports %r short=%r"
                  % (mismatches, short))
            return 1
        planted = dict(CLEAN)
        planted["corpus/lessons/round-02.md"] = (
            "# r2\n\nno gate here\n\n## Mistakes\n\n| # | Class |\n|---|---|\n"
            "| 1 | a |\n\n| 2 | b |\n")
        planted["corpus/knowledge/entry2.md"] = "source: S404\n\nbody\n"
        planted["corpus/QUALITY.md"] = CLEAN["corpus/QUALITY.md"] + (
            "\n## Round-02 criteria — another thing\n\nNo lesson pointer.\n")
        planted["SKILL.md"] = CLEAN["SKILL.md"] + "| u | gate | `scripts/gone.py` | 0=ok |\n"
        write_all(planted)
        bad = commit("planted")
        pins, short, mismatches, counts, _ = audit(repo, bad, base_pins=synth)
        found = sorted((m["class"], m["path"]) for m in mismatches)
        want = sorted([("E1", "corpus/lessons/round-02.md"),
                       ("E4", "corpus/lessons/round-02.md"),
                       ("E3", "corpus/knowledge/entry2.md"),
                       ("E2", "corpus/QUALITY.md"),
                       ("E5", "SKILL.md")])
        if found != want:
            print("selftest FAIL: planted findings %r" % (found,))
            return 1
        if not mismatches or short:
            print("selftest FAIL: planted revision would not exit 1 "
                  "(mismatches=%d short=%r)" % (len(mismatches), short))
            return 1
        write_all(CLEAN)
        write_all({"corpus/lessons/round-02.md":
                   "# r2\n\n## Gate\n\nadmit.\n\n## Mistakes\n\n| # | Class |\n"
                   "|---|---|\n| 1 | a |\n| 2 | b |\n",
                   "corpus/knowledge/entry2.md":
                   "source: S001\nverified-at: 2026-11-04\nrecheck: 90d\n\nbody\n",
                   "corpus/QUALITY.md": CLEAN["corpus/QUALITY.md"] + (
                       "\n## Round-02 criteria — another thing\n\n"
                       "Grounded in `corpus/lessons/round-02.md`.\n"),
                   "SKILL.md": CLEAN["SKILL.md"]})
        fixed = commit("repaired")
        pins, short, mismatches, counts, _ = audit(repo, fixed, base_pins=synth)
        if mismatches:
            print("selftest FAIL: repaired revision still reports %r" % (mismatches,))
            return 1
        if mismatches or short:
            print("selftest FAIL: repaired revision does not read met")
            return 1
        print("selftest 5/5 planted findings, exit 1 on planted, exit 0 on repaired")
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--revision")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.root and a.revision):
        ap.error("--root and --revision are required")
    root = os.path.realpath(a.root)
    rev = git(root, "rev-parse", "%s^{commit}" % a.revision).stdout.decode().strip()
    if not rev:
        print("C1v93 revision=? unresolved")
        return 2
    if not (read(root, rev, "SKILL.md") and read(root, rev, "corpus/SOURCES.md")):
        print("C1v93 revision=%s unevaluable=missing-surface" % rev)
        return 2
    return report(root, rev)


if __name__ == "__main__":
    sys.exit(main())
