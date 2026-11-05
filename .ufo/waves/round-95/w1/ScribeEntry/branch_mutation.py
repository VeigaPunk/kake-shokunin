#!/usr/bin/env python3
"""Decisive experiment for the round-95 battery-coverage gap (seat ScribeEntry).

Hypothesis (from `battery_coverage.py`): the frozen C1 counter's battery does
not exercise every finding SHAPE the counter can emit. If a counter is mutated
so that one uncovered shape can no longer fire, its battery should still read
20/20 — the mutation is invisible to the counter's own conjunct.

Method (all in scratch; the lane is only read):

  1. Copy the frozen counter to a scratch file and apply ONE surgical mutation
     that disables exactly one uncovered branch (each mutation in its own copy).
  2. Run the mutated counter's own `battery()` (the frozen function) over its
     own fixtures and read the battery verdict.
  3. Compare with the unmutated frozen counter's battery verdict.

A mutation whose battery verdict is unchanged AND whose audit no longer emits
the shape is a proven coverage gap: the counter's `met` conjunct battery cannot
see the branch it lost.

Run:  python3 -B branch_mutation.py
"""
import importlib.util
import os
import re
import shutil
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
COUNTER = os.path.join(LANE, ".ufo/waves/round-95/c95_selfassess.py")

# Each mutation disables exactly one uncovered branch of the frozen audit.
# (name, exact source substring to replace, replacement, the finding it kills)
MUTATIONS = [
    ("E1-reject-vocabulary",
     '                if not (re.search(r"reject", head_line, re.I)\n'
     '                        or re.search(r"reject", body, re.I)):\n'
     '                    mismatches.append({"class": "E1", "path": path,\n'
     '                                       "detail": "vacuous Gate: no reject decision "\n'
     '                                                 "line (route R01)"})\n'
     '                    break\n',
     '                pass\n',
     "E1 vacuous Gate: no reject decision line"),
    ("E2-no-lesson-citation",
     '        if not cited:\n'
     '            mismatches.append({"class": "E2", "path": "corpus/QUALITY.md",\n'
     '                               "detail": "section %r names no corpus/lessons/ file"\n'
     '                                         % head})\n'
     '            continue\n',
     '        if not cited:\n'
     '            continue\n',
     "E2 section %r names no corpus/lessons/ file"),
    ("E2-cites-missing",
     '            if meta is None:\n'
     '                mismatches.append({"class": "E2", "path": "corpus/QUALITY.md",\n'
     '                                   "detail": "section %r cites missing %s"\n'
     '                                             % (head, c)})\n',
     '            if meta is None:\n'
     '                pass\n',
     "E2 section %r cites missing %s"),
    ("E3-missing-source",
     '            if not re.search(r"(?m)^" + key + r":\\s*\\S", head):\n'
     '                problems.append("missing %s:" % key)\n',
     '            if False:\n'
     '                problems.append("missing %s:" % key)\n',
     "E3 missing source:"),
    ("E3-missing-verified-at",
     '            if not re.search(r"(?m)^" + key + r":\\s*\\S", head):\n'
     '                problems.append("missing %s:" % key)\n',
     '            if False:\n'
     '                problems.append("missing %s:" % key)\n',
     "E3 missing verified-at:"),
    ("E3-missing-recheck",
     '            if not re.search(r"(?m)^" + key + r":\\s*\\S", head):\n'
     '                problems.append("missing %s:" % key)\n',
     '            if False:\n'
     '                problems.append("missing %s:" % key)\n',
     "E3 missing recheck:"),
    ("E3-vacuous-source",
     '                elif not LOCATOR_RE.search(line):\n'
     '                    problems.append("vacuous source: no row id, URL or path locator")\n',
     '                elif False:\n'
     '                    problems.append("vacuous source: no row id, URL or path locator")\n',
     "E3 vacuous source: no row id, URL or path locator"),
]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def battery_verdict(mod, work):
    """Run the counter's own battery() and summarise its verdict fields."""
    os.makedirs(work, exist_ok=True)
    res = mod.battery(work, os.path.abspath(mod.__file__))
    refused, total, admitted, clean_total, shadow, pred_admits, pred_scored, detail = res
    return {"battery": "%d/%d" % (refused, total),
            "admit": "%d/%d" % (admitted, clean_total),
            "shadow_absent": shadow,
            "predecessor_admits": "%d/%d" % (pred_admits, pred_scored),
            "unrefused_routes": sorted(n for n, v in detail.items()
                                       if isinstance(v, dict)
                                       and v.get("refused_ok") is False)}


def audit_shapes(mod, work):
    """Run the frozen audit() over the counter's own CLEAN fixture and list the
    finding shapes it emits for a deliberately broken tree."""
    files = dict(mod.CLEAN)
    # a knowledge entry missing `recheck:` and a lesson with an admit-only Gate
    files["corpus/knowledge/entry.md"] = (
        "source: S001\nverified-at: 2026-11-05\n\nbody\n")
    files["corpus/lessons/round-96.md"] = (
        "# r96\n\n## Gate\n\nadmit the thing.\n\nand another line.\n\n"
        "## Mistakes\n\n| # | Class |\n|---|---|\n| 1 | a |\n")
    fdir = os.path.join(work, "shapes")
    os.makedirs(fdir, exist_ok=True)
    repo, rev = mod.make_repo(fdir, files)
    rev = mod.git(repo, "rev-parse", "HEAD").stdout.decode().strip()
    surfaces = mod.surfaces_of(files)
    _p, _s, _i, mm, _c = mod.audit(repo, rev, base_pins=mod.SYNTH_PINS,
                                    surfaces=surfaces)
    return [(x["class"], x["detail"]) for x in mm]


def main():
    work = tempfile.mkdtemp(prefix="branchmut-")
    try:
        base_src = open(COUNTER, encoding="utf-8").read()
        # The pristine counter is also run from a lane-shaped side tree, so the
        # pristine and mutated runs are comparable in EVERY battery field
        # (including predecessor_admits, which resolves the round-94 counter
        # relative to the script's own location).
        side0 = os.path.join(work, "env_pristine")
        os.makedirs(os.path.join(side0, ".ufo/waves/round-95"), exist_ok=True)
        os.makedirs(os.path.join(side0, ".ufo/waves/round-94"), exist_ok=True)
        shutil.copyfile(os.path.join(LANE, ".ufo/waves/round-94/c94_selfassess.py"),
                        os.path.join(side0, ".ufo/waves/round-94/c94_selfassess.py"))
        pristine_path = os.path.join(side0, ".ufo/waves/round-95/c95_selfassess.py")
        shutil.copyfile(COUNTER, pristine_path)
        pristine = load("c95_pristine", pristine_path)
        base_verdict = battery_verdict(pristine, os.path.join(work, "base"))
        base_shapes = audit_shapes(pristine, os.path.join(work, "base_shapes"))
        print("PRISTINE frozen counter (lane-shaped side tree)")
        print("  battery=%s admit=%s shadow_absent=%s predecessor_admits=%s"
              % (base_verdict["battery"], base_verdict["admit"],
                 base_verdict["shadow_absent"], base_verdict["predecessor_admits"]))
        print("  audit shapes on a deliberately broken tree:")
        for c, d in base_shapes:
            print("     %s %s" % (c, d))
        print()

        rows = []
        for name, old, new, kills in MUTATIONS:
            if old not in base_src:
                print("MUTATION %-26s NOT APPLIED (anchor not found)" % name)
                rows.append((name, kills, "anchor-not-found", ""))
                continue
            mutated_src = base_src.replace(old, new, 1)
            # Place the mutated counter in a lane-shaped side tree so that
            # predecessor_clean() resolves the round-94 counter exactly as it
            # does in the lane; then EVERY battery field is comparable with the
            # pristine run, not just the ones this experiment compares.
            side = os.path.join(work, "env_%s" % name)
            os.makedirs(os.path.join(side, ".ufo/waves/round-95"), exist_ok=True)
            os.makedirs(os.path.join(side, ".ufo/waves/round-94"), exist_ok=True)
            shutil.copyfile(os.path.join(LANE, ".ufo/waves/round-94/c94_selfassess.py"),
                            os.path.join(side, ".ufo/waves/round-94/c94_selfassess.py"))
            mpath = os.path.join(side, ".ufo/waves/round-95/c95_selfassess.py")
            with open(mpath, "w", encoding="utf-8") as fh:
                fh.write(mutated_src)
            mut = load("c95_%s" % name.replace("-", "_"), mpath)
            v = battery_verdict(mut, os.path.join(work, "w_%s" % name))
            shapes = audit_shapes(mut, os.path.join(work, "s_%s" % name))
            gone = not any(kills.split(" ")[0] in (c + " " + d)
                           and (kills.split(" ", 1)[1][:24] in d if " " in kills else True)
                           for c, d in shapes)
            same = (v["battery"] == base_verdict["battery"]
                    and v["admit"] == base_verdict["admit"]
                    and v["shadow_absent"] == base_verdict["shadow_absent"])
            print("MUTATION %-26s kills %s" % (name, kills))
            print("   battery=%s admit=%s shadow_absent=%s predecessor_admits=%s"
                  % (v["battery"], v["admit"], v["shadow_absent"],
                     v["predecessor_admits"]))
            print("   battery verdict UNCHANGED: %s ; shape still emitted: %s"
                  % (same, not gone))
            if same and gone:
                print("   ==> PROVEN GAP: the branch is gone and the battery cannot see it")
            rows.append((name, kills, "battery-unchanged" if same else "battery-changed",
                          "shape-still-emitted" if not gone else "shape-eliminated"))
        print()
        print("summary")
        for r in rows:
            print("   %-26s %-40s %s %s" % r)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
