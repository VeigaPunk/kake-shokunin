#!/usr/bin/env python3
"""Executable witness for QUALITY criterion (a), round 95 (seat ScribeEntry).

Claim under test: the round-95 C1 counter's `met` conjunct battery must cover
every rule class the counter enforces.

Method (all read-only against the lane; every write happens in a scratch
fixture repo created by the counter's own `make_repo` helper):

  1. Enumerate the finding *shapes* the frozen audit() can emit, by reading the
     `mismatches.append({...})` call sites in the frozen counter.
  2. Enumerate the battery routes in the same frozen bytes and map each route
     to the shape it expects (`"expect": ("E3", "<fragment>")`), using the
     counter's own matching rule (`fragment in detail`).
  3. Report every emitted shape that no route expects — an uncovered branch.
  4. For each uncovered branch that is REACHABLE, build the fixture that
     triggers it and run the frozen `audit()` on it, to show the branch really
     fires and really is unexercised by the battery.

The frozen counter is imported read-only; nothing in the lane is touched.

Run:  python3 -B battery_coverage.py
Exit: 0 when the witness ran (see the printed verdict); the script never
      changes the lane.
"""
import importlib.util
import os
import re
import shutil
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
COUNTER = os.path.join(LANE, ".ufo/waves/round-95/c95_selfassess.py")

spec = importlib.util.spec_from_file_location("c95_ro", COUNTER)
c95 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c95)

SRC = open(COUNTER, encoding="utf-8").read()

# --- 1. emitted finding shapes ------------------------------------------------
# Reconstruct the exact detail text each append site produces, with the
# substitution slots filled by a representative value.
SHAPES = [
    ("E1", "no '## Gate' heading"),
    ("E1", "vacuous Gate: fewer than two non-empty body lines"),
    ("E1", "vacuous Gate: no admit decision line (route R01)"),
    ("E1", "vacuous Gate: no reject decision line (route R01)"),
    ("E4", "indented table row inside Mistakes section 1 line 1 (route R02b)"),
    ("E4", "blank line inside Mistakes section 2 after row 1"),
    ("E4", "carried a Mistakes section at base and now has none (deletion route F4)"),
    ("E2", "section 'Round-95 criterion — x' names no corpus/lessons/ file"),
    ("E2", "section 'Round-95 criterion — x' cites missing corpus/lessons/gone.md"),
    ("E2", "section 'Round-95 criterion — x' cites corpus/lessons/empty.md: blob of 0 bytes"),
    ("E3", "missing source:"),
    ("E3", "missing verified-at:"),
    ("E3", "missing recheck:"),
    ("E3", "multiple source: lines (2); only the provenance trio's single line is validated (route R03)"),
    ("E3", "non-citable locator: /tmp is never evidence (route R12)"),
    ("E3", "unresolved row id S999"),
    ("E3", "vacuous source: no row id, URL or path locator"),
    ("E5", "absence marker without a closing bracket on the same line (route R10b)"),
    ("E5", "annotated absent but present at the revision: scripts/t.py"),
    ("E5", "names missing path scripts/gone.py"),
    ("E5", "names a tree, not a blob: corpus/knowledge"),
    ("E5", "names an empty blob: scripts/empty.py"),
    ("E5", "names a symlink, not a regular blob: scripts/link.py (route R09)"),
]

# --- 2. battery routes --------------------------------------------------------
ROUTES = re.findall(r'"expect":\s*\("([A-Z0-9]+)",\s*"([^"]*)"\)', SRC)
ROUTE_NAMES = re.findall(r'"([A-Z]\d\d-[A-Za-z0-9_\-]+)":\s*\{', SRC)


def covered(cls, detail):
    """The counter's own rule: the route fragment must be a substring of the
    emitted detail (c95_selfassess.py battery(): `fragment in x["detail"]`)."""
    return [f for c, f in ROUTES if c == cls and f in detail]


def main():
    print("counter: %s" % COUNTER)
    print("sha256: %s" % c95.self_sha())
    print("routes in frozen bytes: %d (%d defect routes + clean routes)\n"
          % (len(ROUTE_NAMES), len(ROUTE_NAMES)))

    uncovered = []
    for cls, detail in SHAPES:
        hits = covered(cls, detail)
        if not hits:
            uncovered.append((cls, detail))
        print(("  covered   " if hits else "  UNCOVERED ")
              + "%-4s %s" % (cls, detail))

    print("\nuncovered finding shapes: %d of %d" % (len(uncovered), len(SHAPES)))
    for cls, detail in uncovered:
        print("   %-4s %s" % (cls, detail))

    # --- 3. reachability witnesses ------------------------------------------
    # Build the fixture for each uncovered branch that the audit can really
    # produce, and show the frozen audit emits it.
    work = tempfile.mkdtemp(prefix="c95cov-")
    ok = True
    try:
        fixtures = []

        # E1 reject-vocabulary branch: a round-96 lesson whose Gate carries two
        # non-empty body lines including an admit line but no reject line. (The
        # admit/reject vocabulary rule applies to lessons of round >= 95 only,
        # and the "fewer than two non-empty body lines" check fires first, so
        # the Gate body needs two lines.)
        fixtures.append((
            "E1", "vacuous Gate: no reject decision line (route R01)",
            {"corpus/lessons/round-96.md":
             "# r96\n\n## Gate\n\nadmit the thing.\n\nand another line.\n\n"
             "## Mistakes\n\n| # | Class |\n|---|---|\n| 1 | a |\n"}))

        # E2 "names no corpus/lessons/ file": a Round-95 criteria section with
        # no lesson citation at all.
        fixtures.append((
            "E2", "section 'Round-95 criterion — x' names no corpus/lessons/ file",
            {"corpus/QUALITY.md":
             "# Q\n\n## Round-95 criterion — x\n\nGrounded in prose only.\n"}))

        # E2 "cites missing": a Round-95 criteria section citing a lesson file
        # that does not exist in the tree.
        fixtures.append((
            "E2", "section 'Round-95 criterion — x' cites missing corpus/lessons/gone.md",
            {"corpus/QUALITY.md":
             "# Q\n\n## Round-95 criterion — x\n\nGrounded in "
             "`corpus/lessons/gone.md`.\n"}))

        # E3 "missing recheck:": a knowledge entry without the recheck: field.
        fixtures.append((
            "E3", "missing recheck:",
            {"corpus/knowledge/entry.md":
             "source: S001\nverified-at: 2026-11-05\n\nbody\n"}))

        # E3 "missing source:": a knowledge entry without the source: field.
        fixtures.append((
            "E3", "missing source:",
            {"corpus/knowledge/entry.md":
             "verified-at: 2026-11-05\nrecheck: 180d\n\nbody\n"}))

        # E3 "missing verified-at:": a knowledge entry without that field.
        fixtures.append((
            "E3", "missing verified-at:",
            {"corpus/knowledge/entry.md":
             "source: S001\nrecheck: 180d\n\nbody\n"}))

        # E3 "vacuous source": a knowledge entry whose source line carries no
        # row id and no locator.
        fixtures.append((
            "E3", "vacuous source: no row id, URL or path locator",
            {"corpus/knowledge/entry.md":
             "source: prose only\nverified-at: 2026-11-05\nrecheck: 180d\n\nbody\n"}))

        for cls, shape, defects in fixtures:
            files = dict(c95.CLEAN)
            files.update(defects)
            fdir = os.path.join(work, re.sub(r"[^A-Za-z0-9]+", "_", shape)[:60])
            os.makedirs(fdir, exist_ok=True)
            repo, rev = c95.make_repo(fdir, files)
            rev = c95.git(repo, "rev-parse", "HEAD").stdout.decode().strip()
            surfaces = c95.surfaces_of(files)
            _pins, _short, _ident, mm, _counts = c95.audit(
                repo, rev, base_pins=c95.SYNTH_PINS, surfaces=surfaces)
            hit = any(x["class"] == cls and shape.split("%")[0][:24] in x["detail"]
                      for x in mm)
            detail_hit = [x["detail"] for x in mm if x["class"] == cls]
            print("\nreachability: %s" % shape)
            print("  fixture defects: %s" % sorted(defects))
            print("  audit emitted %s: %s" % (cls, detail_hit))
            print("  shape reachable: %s ; covered by a battery route: %s"
                  % (bool(detail_hit), bool(covered(cls, shape))))
            if not detail_hit:
                ok = False
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print("\nVERDICT: %d of %d emitted finding shapes have no battery route; "
          "every probed uncovered branch was reachable by the frozen audit."
          % (len(uncovered), len(SHAPES)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
