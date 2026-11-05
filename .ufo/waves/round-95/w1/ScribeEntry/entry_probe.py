#!/usr/bin/env python3
"""Conformance probe for the round-95 knowledge-entry draft (seat ScribeEntry).

Runs the FROZEN C1 counter's own `audit()` over a scratch fixture that carries
this seat's draft entry bytes, so the E3 provenance-trio rule and the E2
criteria-section rule are measured by the instrument, not by prose.

Two questions, both answered by running the frozen audit:

  Q1 (E3) — does the draft's `source:` line resolve? The draft names S479,
  which is a PENDING row (drafted by ScoutErrata, admitted only through the
  round gate). The probe runs the audit twice: once with the lane's SOURCES.md
  as committed (S479 absent) and once with the draft S479 row inserted
  (S479 present). The difference is the integration ordering constraint the
  L1 must honour.

  Q2 (E2) — do the three QUALITY.md criteria sections resolve? The probe adds
  the drafted sections to the fixture's corpus/QUALITY.md with and without
  corpus/lessons/round-95.md present, so the E2 finding is observed rather
  than assumed.

Read-only against the lane. Every write is in a scratch fixture repo built by
the counter's own `make_repo`.

Run:  python3 -B entry_probe.py
"""
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
COUNTER = os.path.join(LANE, ".ufo/waves/round-95/c95_selfassess.py")
HERE = os.path.dirname(os.path.abspath(__file__))
DRAFT = os.path.join(HERE, "entry.md")
QUALITY = os.path.join(HERE, "quality-criteria.md")
LESSON = os.path.join(HERE, "lesson-skeleton.md")

spec = importlib.util.spec_from_file_location("c95_probe", COUNTER)
c95 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c95)

# The three QUALITY.md sections drafted by this seat, lifted verbatim from
# quality-criteria.md (the file's body after the seat's preamble).
def quality_sections():
    text = open(QUALITY, encoding="utf-8").read()
    # the three drafted sections start at each "## Round 95 — " heading
    parts = re.split(r"(?m)^## ", text)
    out = []
    for p in parts:
        if p.startswith("Round 95 — "):
            out.append("## " + p.rstrip() + "\n")
    return out


def lesson_bytes():
    return open(LESSON, encoding="utf-8").read()


def main():
    entry = open(DRAFT, encoding="utf-8").read()
    sections = quality_sections()
    print("draft entry bytes: %d ; QUALITY sections found: %d"
          % (len(entry), len(sections)))
    for s in sections:
        print("  section head: %s" % s.splitlines()[0])

    work = tempfile.mkdtemp(prefix="entryprobe-")
    try:
        # The real lane SOURCES.md (round base), so that the only difference
        # between Q1 and Q1b is the S479 row itself.
        lane_sources = c95.git(
            LANE, "show", "fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3:corpus/SOURCES.md"
        ).stdout.decode()
        s479 = [l for l in
                open(os.path.join(LANE,
                       ".ufo/waves/round-95/w1/ScoutErrata/S479-row.txt"),
                     encoding="utf-8").read().splitlines()
                if l.startswith("| S479 ")]
        print("\nS479 row text found in the scout's draft: %s" % bool(s479))

        # ---- Q1: E3 with the real lane SOURCES.md (S479 absent) -------------
        base_files = dict(c95.CLEAN)
        base_files["corpus/SOURCES.md"] = lane_sources
        base_files["corpus/knowledge/conditional-list-membership.md"] = entry
        fdir = os.path.join(work, "q1_no_s479")
        os.makedirs(fdir)
        repo, rev = c95.make_repo(fdir, base_files)
        rev = c95.git(repo, "rev-parse", "HEAD").stdout.decode().strip()
        surfaces = c95.surfaces_of(base_files)
        _p, _s, _i, mm, counts = c95.audit(repo, rev,
                                          base_pins=c95.SYNTH_PINS,
                                          surfaces=surfaces)
        e3 = [x for x in mm if x["class"] == "E3"]
        print("\nQ1  audit with the real lane SOURCES.md (S479 absent):")
        print("    E3 findings: %d" % len(e3))
        for x in e3:
            print("      %s" % x["detail"])

        # ---- Q1b: E3 with the S479 row inserted ----------------------------
        files2 = dict(base_files)
        if s479:
            out = []
            for l in lane_sources.splitlines():
                out.append(l)
                if l.startswith("| S478 "):
                    out.append(s479[0])
            files2["corpus/SOURCES.md"] = "\n".join(out) + "\n"
        fdir2 = os.path.join(work, "q1_with_s479")
        os.makedirs(fdir2)
        repo2, rev2 = c95.make_repo(fdir2, files2)
        rev2 = c95.git(repo2, "rev-parse", "HEAD").stdout.decode().strip()
        surfaces2 = c95.surfaces_of(files2)
        _p, _s, _i, mm2, counts2 = c95.audit(repo2, rev2,
                                              base_pins=c95.SYNTH_PINS,
                                              surfaces=surfaces2)
        e3b = [x for x in mm2 if x["class"] == "E3"]
        print("\nQ1b audit with the S479 row inserted:")
        print("    E3 findings: %d" % len(e3b))
        for x in e3b:
            print("      %s" % x["detail"])

        # ---- Q2: E2 for the criteria sections ------------------------------
        for with_lesson in (False, True):
            files3 = dict(c95.CLEAN)
            files3["corpus/QUALITY.md"] = ("# Q\n\n" + "\n".join(sections))
            if with_lesson:
                files3["corpus/lessons/round-95.md"] = lesson_bytes()
            tag = "WITH lesson" if with_lesson else "WITHOUT lesson"
            fdir3 = os.path.join(work, "q2_" + tag.split()[0].lower())
            os.makedirs(fdir3)
            repo3, rev3 = c95.make_repo(fdir3, files3)
            rev3 = c95.git(repo3, "rev-parse", "HEAD").stdout.decode().strip()
            surfaces3 = c95.surfaces_of(files3)
            _p, _s, _i, mm3, _c = c95.audit(repo3, rev3,
                                            base_pins=c95.SYNTH_PINS,
                                            surfaces=surfaces3)
            e2 = [x for x in mm3 if x["class"] == "E2"]
            e1 = [x for x in mm3 if x["class"] == "E1"]
            print("\nQ2  audit of the drafted criteria sections %s:" % tag)
            print("    E2 findings: %d" % len(e2))
            for x in e2:
                print("      %s" % x["detail"])
            print("    E1 findings: %d %s"
                  % (len(e1), [x["detail"] for x in e1]))

        # ---- Q3: the lesson skeleton itself (E1 for round >= 95, E4) --------
        files4 = dict(c95.CLEAN)
        files4["corpus/lessons/round-95.md"] = lesson_bytes()
        fdir4 = os.path.join(work, "q3_lesson")
        os.makedirs(fdir4)
        repo4, rev4 = c95.make_repo(fdir4, files4)
        rev4 = c95.git(repo4, "rev-parse", "HEAD").stdout.decode().strip()
        surfaces4 = c95.surfaces_of(files4)
        _p, _s, _i, mm4, counts4 = c95.audit(repo4, rev4,
                                             base_pins=c95.SYNTH_PINS,
                                             surfaces=surfaces4)
        print("\nQ3  audit of the drafted lesson skeleton "
              "(corpus/lessons/round-95.md):")
        print("    E1 findings: %d" % len([x for x in mm4 if x["class"] == "E1"]))
        for x in mm4:
            if x["class"] in ("E1", "E4"):
                print("      %s %s" % (x["class"], x["detail"]))
        print("    all findings: %s" % [(x["class"], x["detail"][:60])
                                        for x in mm4])
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
