#!/usr/bin/env python3
"""ReviewC1 attack driver — round-93 kake, C1 counter (c93_selfassess.py).

Builds full-size synthetic lane fixtures (pins >= BASE_PINS) in scratch git
repos and runs the FROZEN counter bytes (extracted from the freeze commit,
sha256-verified) against each. One receipt file per scenario under receipts/.

Never touches the lane working tree; commits only inside fixtures.
"""
import hashlib
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kake-r93/ReviewC1"
REC = os.path.join(S, "receipts")
COUNTER = os.path.join(S, "c93_selfassess.frozen.py")
os.makedirs(REC, exist_ok=True)

LESSON = ("# r{n}\n\n## Gate\n\nadmit.\n\n## Mistakes\n\n"
          "| # | Class |\n|---|---|\n| 1 | none |\n")
ENTRY = "source: S001\nverified-at: 2026-11-01\nrecheck: 90d\n\nbody {n}\n"


def sh(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def git(root, *a):
    rc, out, err = sh(["git", "-C", root, *a])
    assert rc == 0, (a, err)
    return out


def w(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as fh:
        fh.write(text)


def rm(root, rel):
    os.remove(os.path.join(root, rel))


def build_clean(root):
    for i in range(1, 88):
        w(root, "corpus/lessons/round-%02d.md" % i, LESSON.format(n=i))
    for i in range(1, 81):
        w(root, "corpus/knowledge/entry-%02d.md" % i, ENTRY.format(n=i))
    w(root, "corpus/SOURCES.md", "| id | anchor |\n|---|---|\n| S001 | x |\n")
    rows = ["| name | kind | entry | verdict |", "|---|---|---|---|"]
    for i in range(1, 256):
        rows.append("| t%d | probe | `scripts/s%d.py` | 0=ok |" % (i, i))
        w(root, "scripts/s%d.py" % i, "print(%d)\n" % i)
    w(root, "SKILL.md", "\n".join(rows) + "\n")
    q = ["# Q"]
    for i in range(1, 40):
        q += ["## Round-%02d criterion — thing %d" % (i, i), "",
              "Criterion %d grounded in `corpus/lessons/round-%02d.md`." % (i, i)]
    w(root, "corpus/QUALITY.md", "\n".join(q) + "\n")


def fixture(name):
    d = os.path.join(S, "fx." + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    git(d, "init", "-q")
    top = git(d, "rev-parse", "--show-toplevel").strip()
    assert top == d, (top, d)
    return d


def commit(root, msg):
    git(root, "add", "-A")
    git(root, "-c", "user.email=fx@example.invalid", "-c", "user.name=fx",
        "commit", "-qm", msg)
    return git(root, "rev-parse", "HEAD").strip()


def run_counter(root, rev):
    cmd = ["python3", "-B", COUNTER, "--root", root, "--revision", rev]
    rc, out, err = sh(cmd)
    return rc, out, err, " ".join(cmd)


def show(root, rev, path):
    return subprocess.run(["git", "-C", root, "show", "%s:%s" % (rev, path)],
                          capture_output=True, text=True)


def receipt(name, blocks):
    with open(os.path.join(REC, name + ".txt"), "w") as fh:
        fh.write("\n".join(blocks) + "\n")


def line1(out):
    return out.splitlines()[0] if out.splitlines() else "(no stdout)"


def detail(out):
    ls = out.splitlines()
    return ls[1] if len(ls) > 1 else "(no detail line)"


# ---------------- defect plants ----------------

def plant_e1(root):          # lesson without a Gate heading
    w(root, "corpus/lessons/round-05.md",
      "# r5\n\nno gate here\n\n## Mistakes\n\n| # | Class |\n|---|---|\n| 1 | a |\n")


def plant_e1_bare(root):     # 'repair': bare Gate heading, no content
    w(root, "corpus/lessons/round-05.md", "# r5\n\n## Gate\n")


def plant_e1_space(root):    # Gate with one trailing space
    w(root, "corpus/lessons/round-05.md",
      "# r5\n\n## Gate \n\nadmit.\n\n## Mistakes\n\n| # | Class |\n|---|---|\n| 1 | a |\n")


def plant_e2(root):          # counted criteria section citing a missing lesson
    q = open(os.path.join(root, "corpus/QUALITY.md")).read()
    q += ("\n## Round-90 criterion — deferred checks\n\nThe criterion is grounded in "
          "`corpus/lessons/round-missing.md`.\n")
    w(root, "corpus/QUALITY.md", q)


def plant_e2_empty_pointer(root):  # same section, pointer to an existing near-empty lesson
    w(root, "corpus/lessons/round-empty.md", "# re\n\n## Gate\n")
    q = open(os.path.join(root, "corpus/QUALITY.md")).read()
    q += ("\n## Round-90 criterion — deferred checks\n\nThe criterion is grounded in "
          "`corpus/lessons/round-empty.md`.\n")
    w(root, "corpus/QUALITY.md", q)


def plant_e3(root):          # entry with unresolved id and missing duo
    w(root, "corpus/knowledge/entry-81.md", "source: S404\n\nbody\n")


def plant_e3_inplace(root):  # existing entry loses its trio
    w(root, "corpus/knowledge/entry-80.md", "source: S404\n\nbody\n")


def plant_e4(root):          # blank line splits the Mistakes table
    w(root, "corpus/lessons/round-06.md",
      "# r6\n\n## Gate\n\nadmit.\n\n## Mistakes\n\n| # | Class |\n|---|---|\n"
      "| 1 | a |\n\n| 2 | b |\n")


def plant_e4_double(root):   # two gaps in one table (undercount probe)
    w(root, "corpus/lessons/round-08.md",
      "# r8\n\n## Gate\n\nadmit.\n\n## Mistakes\n\n| # | Class |\n|---|---|\n"
      "| 1 | a |\n\n| 2 | b |\n\n| 3 | c |\n")


def plant_e4_second_sec(root):  # defect in a SECOND '## Mistakes' section
    w(root, "corpus/lessons/round-07.md",
      "# r7\n\n## Gate\n\nadmit.\n\n## Mistakes\n\n| # | Class |\n|---|---|\n"
      "| 1 | none |\n\n## Mistakes\n\n| # | Class |\n|---|---|\n\n| 2 | split |\n")


def plant_e5(root):          # SKILL row naming a missing script
    s = open(os.path.join(root, "SKILL.md")).read()
    s += "| g1 | probe | `scripts/gone.py` | 0=ok |\n"
    w(root, "SKILL.md", s)


# ---------------- scenarios ----------------

def sc_00():
    d = fixture("00clean")
    build_clean(d)
    rev = commit(d, "clean")
    rc, out, err, cmd = run_counter(d, rev)
    receipt("00-sanity-clean", [
        "scenario: sanity — full-size clean fixture, expect pins=ok mismatches=0 met=true exit 0",
        "fixture: " + d, "clean revision: " + rev,
        "counter sha256: " + CSHA,
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out)])


def sc_01():
    d = fixture("01five")
    build_clean(d)
    plant_e1(d)
    plant_e2(d)
    plant_e3(d)
    plant_e4(d)
    plant_e5(d)
    rev = commit(d, "five planted defects")
    rc, out, err, cmd = run_counter(d, rev)
    receipt("01-planted-five", [
        "scenario: one planted defect per class, expect E1..E5 = 1 each, met=false exit 1",
        "fixture: " + d, "defect revision: " + rev, "counter sha256: " + CSHA,
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_02():  # A2a delete defective lesson file -> pins short
    d = fixture("02A2a")
    build_clean(d)
    plant_e1(d)
    commit(d, "e1 planted")
    rm(d, "corpus/lessons/round-05.md")
    rev = commit(d, "cheat: defective lesson deleted")
    rc, out, err, cmd = run_counter(d, rev)
    receipt("02-A2a-delete-lesson", [
        "scenario A2a: E1 defect 'repaired' by deleting the whole lesson file",
        "expectation: pins=short (lessons 86<87), met=false exit 0 NOT reachable",
        "fixture: " + d, "cheat revision: " + rev, "counter sha256: " + CSHA,
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_03():  # A2b delete Mistakes section, keep lesson + Gate
    d = fixture("03A2b")
    build_clean(d)
    plant_e4(d)
    bad = commit(d, "e4 planted")
    w(d, "corpus/lessons/round-06.md", "# r6\n\n## Gate\n\nadmit.\n")
    rev = commit(d, "cheat: Mistakes section deleted, lesson kept")
    rc, out, err, cmd = run_counter(d, rev)
    before = show(d, bad, "corpus/lessons/round-06.md")
    receipt("03-A2b-delete-mistakes-section", [
        "scenario A2b: E4 defect 'repaired' by deleting the whole '## Mistakes' section",
        "lesson file and '## Gate' kept, so no pin shrinks",
        "fixture: " + d, "defect revision: " + bad, "cheat revision: " + rev,
        "counter sha256: " + CSHA,
        "$ git -C %s show %s:corpus/lessons/round-06.md  # defect on disk at defect revision" % (d, bad),
        "(exit=%d) %r" % (before.returncode, before.stdout[:120]),
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_04():  # A2d delete a defective counted criteria section -> pins short
    d = fixture("04A2d")
    build_clean(d)
    q = open(os.path.join(d, "corpus/QUALITY.md")).read()
    q = q.replace("Criterion 39 grounded in `corpus/lessons/round-39.md`.",
                  "Criterion 39 grounded in `corpus/lessons/round-missing.md`.")
    w(d, "corpus/QUALITY.md", q)
    commit(d, "e2 planted in section 39")
    q2 = q.replace("## Round-39 criterion — thing 39\n\nCriterion 39 grounded in "
                   "`corpus/lessons/round-missing.md`.\n", "")
    w(d, "corpus/QUALITY.md", q2)
    rev = commit(d, "cheat: defective criteria section deleted")
    rc, out, err, cmd = run_counter(d, rev)
    receipt("04-A2d-delete-criteria-section", [
        "scenario A2d: E2 defect 'repaired' by deleting the whole counted section",
        "expectation: criteria pin 38<39 -> pins=short, met=false",
        "fixture: " + d, "cheat revision: " + rev, "counter sha256: " + CSHA,
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_05():  # A2e delete defective knowledge entry -> pins short
    d = fixture("05A2e")
    build_clean(d)
    plant_e3_inplace(d)
    commit(d, "e3 planted in entry-80")
    rm(d, "corpus/knowledge/entry-80.md")
    rev = commit(d, "cheat: defective entry deleted")
    rc, out, err, cmd = run_counter(d, rev)
    receipt("05-A2e-delete-entry", [
        "scenario A2e: E3 defect 'repaired' by deleting the knowledge entry",
        "expectation: entries pin 79<80 -> pins=short, met=false",
        "fixture: " + d, "cheat revision: " + rev, "counter sha256: " + CSHA,
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_06():  # A3a bare '## Gate' heading with no content
    d = fixture("06A3a")
    build_clean(d)
    plant_e1(d)
    commit(d, "e1 planted")
    plant_e1_bare(d)
    rev = commit(d, "cheat: bare Gate heading added, no content")
    rc, out, err, cmd = run_counter(d, rev)
    receipt("06-A3a-bare-gate", [
        "scenario A3a: E1 satisfied by a bare '## Gate' heading with no content",
        "predicate letter: 'carries a line exactly ## Gate' — heading presence suffices",
        "fixture: " + d, "cheat revision: " + rev, "counter sha256: " + CSHA,
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_07():  # A4 missing vs existing-but-empty pointer
    d = fixture("07A4missing")
    build_clean(d)
    plant_e2(d)
    bad = commit(d, "e2 planted (cites round-missing.md)")
    rc, out, err, cmd = run_counter(d, bad)
    d2 = fixture("07A4empty")
    build_clean(d2)
    plant_e2_empty_pointer(d2)
    rev2 = commit(d2, "cheat: pointer moved to an existing empty-ish lesson")
    rc2, out2, err2, cmd2 = run_counter(d2, rev2)
    receipt("07-A4-missing-vs-empty-pointer", [
        "scenario A4 part 1: QUALITY section cites a NONEXISTENT lesson",
        "expectation: E2 fires (counter catches missing pointer)",
        "fixture: " + d, "defect revision: " + bad, "counter sha256: " + CSHA,
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out),
        "",
        "scenario A4 part 2: same section cites corpus/lessons/round-empty.md,",
        "an EXISTING lesson whose only content is a bare '## Gate' heading",
        "expectation: passes (read() returns text, not None) — grounding that grounds nothing",
        "fixture: " + d2, "cheat revision: " + rev2,
        "$ " + cmd2, "exit=%d" % rc2, "line1: " + line1(out2),
        "detail: " + detail(out2)])


def sc_08():  # A5 E5 path is a directory or an empty file
    d = fixture("08A5dir")
    build_clean(d)
    w(d, "scripts/pkg/x.py", "print('x')\n")   # scripts/pkg is a committed tree
    w(d, "scripts/empty.py", "")               # committed empty blob
    s = open(os.path.join(d, "SKILL.md")).read()
    s += "| pkg | probe | `scripts/pkg` | 0=ok |\n| emp | probe | `scripts/empty.py` | 0=ok |\n"
    w(d, "SKILL.md", s)
    rev = commit(d, "E5 rows naming a directory and an empty file")
    rc, out, err, cmd = run_counter(d, rev)
    dirshow = show(d, rev, "scripts/pkg")
    receipt("08-A5-dir-and-empty-path", [
        "scenario A5: SKILL rows name `scripts/pkg` (a committed DIRECTORY) and `scripts/empty.py` (0-byte blob)",
        "git show on the tree: exit=%d stdout=%r" % (dirshow.returncode, dirshow.stdout),
        "expectation: both admitted (read() non-None) -> met=true",
        "fixture: " + d, "revision: " + rev, "counter sha256: " + CSHA,
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_09():  # B-E1 trailing whitespace after Gate
    d = fixture("09BE1")
    build_clean(d)
    plant_e1_space(d)
    rev = commit(d, "Gate line with one trailing space")
    rc, out, err, cmd = run_counter(d, rev)
    receipt("09-B-E1-trailing-space", [
        "scenario B-E1: Gate line is '## Gate ' (one trailing space)",
        "predicate letter: 'a line exactly ## Gate' — trailing space violates 'exactly'",
        "expectation: counter admits (regex ^## Gate\\s*$ allows trailing spaces)",
        "fixture: " + d, "revision: " + rev, "counter sha256: " + CSHA,
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_10():  # B-E2 identity swap: drop section from counted population, refill
    d = fixture("10BE2")
    build_clean(d)
    q = open(os.path.join(d, "corpus/QUALITY.md")).read()
    q = q.replace("Criterion 39 grounded in `corpus/lessons/round-39.md`.",
                  "Criterion 39 grounded in `corpus/lessons/round-missing.md`.")
    w(d, "corpus/QUALITY.md", q)
    commit(d, "e2 planted in section 39")
    # cheat: section 39 keeps citing round-missing.md but escapes the counted
    # population (heading loses 'criteri', the word moves past char 400);
    # a fresh junk section restores criteria=39.
    filler = "Grounding note %d. The deferred checks stay open pending review. " * 9
    filler = "".join("Grounding note %d. The deferred checks stay open pending review. " % i
                     for i in range(10))
    assert len(filler) >= 400 and "criteri" not in filler.lower()
    new39 = ("## Round-39 rules — thing 39\n\n" + filler + "\n\nThe criterion for "
             "round 39 is grounded in `corpus/lessons/round-missing.md`.\n")
    q = open(os.path.join(d, "corpus/QUALITY.md")).read()
    q = q.replace("## Round-39 criterion — thing 39\n\nCriterion 39 grounded in "
                  "`corpus/lessons/round-missing.md`.\n", new39)
    q += ("\n## Round-40 criteria — filler\n\nThe criterion is grounded in "
          "`corpus/lessons/round-01.md`.\n")
    w(d, "corpus/QUALITY.md", q)
    rev = commit(d, "cheat: section 39 escapes counted population, junk section 40 refills pin")
    rc, out, err, cmd = run_counter(d, rev)
    receipt("10-B-E2-identity-swap", [
        "scenario B-E2: defective counted section escapes the population",
        "(heading loses the word criteri, mention moved past char 400); a junk",
        "section citing round-01.md restores criteria=39. The defective pointer",
        "to round-missing.md REMAINS in corpus/QUALITY.md, unrepaired.",
        "expectation: pins=ok mismatches=0 met=true -> counter fooled",
        "fixture: " + d, "cheat revision: " + rev, "counter sha256: " + CSHA,
        "$ git -C %s show %s:corpus/QUALITY.md | grep -n round-missing" % (d, rev),
        "  (the unrepaired pointer is still present at the measured revision)",
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_11():  # B-E3a source line with no S-id
    d = fixture("11BE3a")
    build_clean(d)
    w(d, "corpus/knowledge/entry-80.md",
      "source: see the team notebook\nverified-at: 2026-11-01\nrecheck: 90d\n\nbody\n")
    rev = commit(d, "entry-80 source carries no S-id")
    rc, out, err, cmd = run_counter(d, rev)
    receipt("11-B-E3a-no-id-source", [
        "scenario B-E3a: source: line with no S<digits> token at all",
        "predicate: 'every S<digits> id on its source: line resolves' — vacuously true",
        "expectation: admitted (trio present, no ids to resolve)",
        "fixture: " + d, "revision: " + rev, "counter sha256: " + CSHA,
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_12():  # B-E3b id resolves to a non-row token in SOURCES.md
    d = fixture("12BE3b")
    build_clean(d)
    s = open(os.path.join(d, "corpus/SOURCES.md")).read()
    s += "\nDraft tokens S998/S999 were used in early sketches; no rows exist for them.\n"
    w(d, "corpus/SOURCES.md", s)
    w(d, "corpus/knowledge/entry-80.md",
      "source: S999\nverified-at: 2026-11-01\nrecheck: 90d\n\nbody\n")
    rev = commit(d, "entry cites S999 which exists only as prose token in SOURCES.md")
    rc, out, err, cmd = run_counter(d, rev)
    receipt("12-B-E3b-token-not-row", [
        "scenario B-E3b: entry cites S999; SOURCES.md contains the token S999 only in a",
        "prose footer sentence, not as a row id. Predicate says 'resolves to a row id'.",
        "expectation: counter admits (ids scanned over the WHOLE file text) -> fooled",
        "fixture: " + d, "revision: " + rev, "counter sha256: " + CSHA,
        "$ git -C %s show %s:corpus/SOURCES.md | grep -n S999" % (d, rev),
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_13():  # B-E3c short id (2 digits)
    d = fixture("13BE3c")
    build_clean(d)
    w(d, "corpus/knowledge/entry-80.md",
      "source: S47\nverified-at: 2026-11-01\nrecheck: 90d\n\nbody\n")
    rev = commit(d, "entry cites S47 (two digits, no such row)")
    rc, out, err, cmd = run_counter(d, rev)
    receipt("13-B-E3c-short-id", [
        "scenario B-E3c: source: S47 — an S<digits> id that resolves to no row",
        "counter ID_RE is S\\d{3,} (three or more digits), so S47 is invisible:",
        "no unresolved-id check runs. Predicate letter says every S<digits> id.",
        "expectation: admitted -> miss vs the predicate letter",
        "fixture: " + d, "revision: " + rev, "counter sha256: " + CSHA,
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_14():  # B-E4 defect in a second Mistakes section
    d = fixture("14BE4")
    build_clean(d)
    plant_e4_second_sec(d)
    rev = commit(d, "split table inside a SECOND ## Mistakes section")
    rc, out, err, cmd = run_counter(d, rev)
    receipt("14-B-E4-second-section", [
        "scenario B-E4: blank-line-split table inside the SECOND '## Mistakes' section",
        "counter checks only the FIRST '## Mistakes' match (re.search)",
        "expectation: E4 silent -> counter fooled",
        "fixture: " + d, "revision: " + rev, "counter sha256: " + CSHA,
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_15():  # B-E4 undercount: two gaps, one finding
    d = fixture("15BE4b")
    build_clean(d)
    plant_e4_double(d)
    rev = commit(d, "two blank-line gaps in one Mistakes table")
    rc, out, err, cmd = run_counter(d, rev)
    receipt("15-B-E4-undercount", [
        "scenario B-E4b: TWO blank-line gaps in one Mistakes table",
        "counter breaks after the first gap -> E4=1 (undercount; exit still 1)",
        "fixture: " + d, "revision: " + rev, "counter sha256: " + CSHA,
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_16():  # B-E5 unbackticked path
    d = fixture("16BE5")
    build_clean(d)
    s = open(os.path.join(d, "SKILL.md")).read()
    s += "| g2 | probe | scripts/gone9.py unquoted | 0=ok |\n"
    w(d, "SKILL.md", s)
    rev = commit(d, "SKILL row names scripts/gone9.py without backticks")
    rc, out, err, cmd = run_counter(d, rev)
    receipt("16-B-E5-unbackticked", [
        "scenario B-E5: SKILL row names a missing path without backticks",
        "PATH_RE only reads backticked tokens; the predicate says 'named inside a",
        "SKILL.md table row' with no backtick requirement",
        "expectation: admitted -> miss vs the predicate letter",
        "fixture: " + d, "revision: " + rev, "counter sha256: " + CSHA,
        "$ " + cmd, "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_17():  # A1a canned wrapper replaces the counter at the documented path
    d = fixture("17A1a")
    build_clean(d)
    plant_e1(d)
    plant_e2(d)
    plant_e3(d)
    plant_e4(d)
    plant_e5(d)
    rev = commit(d, "five defects planted")
    os.makedirs(os.path.join(d, ".ufo/waves/round-93"), exist_ok=True)
    wrapper = os.path.join(d, ".ufo/waves/round-93/c93_selfassess.py")
    with open(wrapper, "w") as fh:
        fh.write("# FIXTURE-ONLY canned-success wrapper (ReviewC1, round 93).\n"
                 "# Prints a perfect frozen-format line 1 without auditing anything;\n"
                 "# exits 0. Indistinguishable from the counter by path or extension.\n"
                 "import subprocess\n"
                 "import sys\n"
                 "root, rev = sys.argv[2], sys.argv[4]\n"
                 "p = subprocess.run(['git', '-C', root, 'rev-parse', rev + '^{commit}'],\n"
                 "                   capture_output=True)\n"
                 "r = p.stdout.decode().strip() or 'unknown'\n"
                 "print('C1v93 revision=%s lessons=87 entries=80 rows=257 criteria=40 '\n"
                 "      'mismatches=0 E1=0 E2=0 E3=0 E4=0 E5=0 pins=ok met=true' % r)\n"
                 "sys.exit(0)\n")
    rc, out, err = sh(["python3", "-B", ".ufo/waves/round-93/c93_selfassess.py",
                       "--root", ".", "--revision", rev], cwd=d)
    defect = show(d, rev, "corpus/lessons/round-05.md")
    receipt("17-A1a-canned-wrapper", [
        "scenario A1a: the counter at the documented path replaced by a wrapper that",
        "prints a canned frozen-format success line and exits 0. No audit runs.",
        "The same revision's round-05.md has no '## Gate' (git show exit=%d):" % defect.returncode,
        "%r" % defect.stdout[:100],
        "fixture: " + d, "defect revision: " + rev,
        "$ cd " + d + " && python3 -B .ufo/waves/round-93/c93_selfassess.py --root . --revision " + rev,
        "exit=%d" % rc, "stdout: " + out.strip(),
        "counter sha256 used by the honest run: " + CSHA,
        "verdict: output format is fully forgeable; defense is procedural only",
        "(byte-identity of the counter against the freeze blob + clean-tree check)."])


SHADOW = '''\
# FIXTURE-ONLY attack artifact (ReviewC1, round 93): a sys.path[0] shadow of the
# stdlib subprocess module. When the frozen counter is run with the documented
# command, its own directory (this directory) is sys.path[0], so `import
# subprocess` loads THIS file, not the stdlib. The frozen counter bytes are
# untouched. rev-parse passes through to real git; ls-tree and show return a
# fabricated clean lane, so the counter audits fiction while the repo on disk
# stays defective.
import importlib.util as _iu
import os as _os
import sys as _sys

_here = _os.path.dirname(_os.path.abspath(__file__))
_real = None
for _p in _sys.path:
    if not _p or _os.path.abspath(_p) == _here:
        continue
    _cand = _os.path.join(_p, "subprocess.py")
    if _os.path.isfile(_cand):
        _spec = _iu.spec_from_file_location("_real_subprocess", _cand)
        _real = _iu.module_from_spec(_spec)
        _spec.loader.exec_module(_real)
        break
if _real is None:
    raise ImportError("real subprocess module not found on sys.path")

_LESSONS = "\\n".join("corpus/lessons/round-%02d.md" % i for i in range(1, 88))
_ENTRIES = "\\n".join("corpus/knowledge/entry-%02d.md" % i for i in range(1, 81))
_LESSON_TXT = ("# r\\n\\n## Gate\\n\\nadmit.\\n\\n## Mistakes\\n\\n"
               "| # | Class |\\n|---|---|\\n| 1 | none |\\n")
_ENTRY_TXT = "source: S001\\nverified-at: 2026-11-01\\nrecheck: 90d\\n\\nbody\\n"
_SKILL = "\\n".join(
    ["| name | kind | entry | verdict |", "|---|---|---|---|"] +
    ["| t%d | probe | `scripts/s%d.py` | 0=ok |" % (i, i) for i in range(1, 256)]) + "\\n"
_QUAL = "# Q\\n" + "\\n".join(
    "## Round-%02d criteria — thing %d\\n\\nCriterion %d grounded in "
    "`corpus/lessons/round-%02d.md`." % (i, i, i, i) for i in range(1, 40)) + "\\n"
_SRC = "| id | anchor |\\n|---|---|\\n| S001 | x |\\n"


def _fake_show(path):
    if path == "SKILL.md":
        return _SKILL
    if path == "corpus/SOURCES.md":
        return _SRC
    if path == "corpus/QUALITY.md":
        return _QUAL
    if path.startswith("corpus/lessons/"):
        return _LESSON_TXT
    if path.startswith("corpus/knowledge/"):
        return _ENTRY_TXT
    return "ok\\n"


def run(cmd, *a, **kw):
    if cmd and cmd[0] == "git":
        if "rev-parse" in cmd:
            return _real.run(cmd, *a, **kw)
        if "ls-tree" in cmd:
            names = (_LESSONS if any("corpus/lessons" == x for x in cmd)
                     else _ENTRIES if any("corpus/knowledge" == x for x in cmd) else "")
            return _real.CompletedProcess(cmd, 0, stdout=(names + "\\n").encode(),
                                          stderr=b"")
        if "show" in cmd:
            arg = cmd[-1]
            path = arg.split(":", 1)[1] if ":" in arg else arg
            return _real.CompletedProcess(cmd, 0, stdout=_fake_show(path).encode(),
                                          stderr=b"")
    return _real.run(cmd, *a, **kw)


CompletedProcess = _real.CompletedProcess
PIPE = _real.PIPE
'''


def sc_18():  # A1b shadow module beside the FROZEN counter bytes
    d = fixture("18A1b")
    build_clean(d)
    plant_e1(d)
    plant_e2(d)
    plant_e3(d)
    plant_e4(d)
    plant_e5(d)
    rev = commit(d, "five defects planted (real disk state)")
    cdir = os.path.join(d, ".ufo/waves/round-93")
    os.makedirs(cdir, exist_ok=True)
    shutil.copyfile(COUNTER, os.path.join(cdir, "c93_selfassess.py"))
    with open(os.path.join(cdir, "subprocess.py"), "w") as fh:
        fh.write(SHADOW)
    copy_sha = hashlib.sha256(
        open(os.path.join(cdir, "c93_selfassess.py"), "rb").read()).hexdigest()
    rc, out, err = sh(["python3", "-B", ".ufo/waves/round-93/c93_selfassess.py",
                       "--root", ".", "--revision", rev], cwd=d)
    defect = show(d, rev, "corpus/lessons/round-05.md")
    skill = show(d, rev, "SKILL.md")
    gone_row = [l for l in skill.stdout.splitlines() if "gone.py" in l]
    receipt("18-A1b-shadow-module", [
        "scenario A1b: FROZEN counter bytes, unchanged, spoofed by a sys.path[0]",
        "shadow of stdlib 'subprocess' sitting in the counter's own directory.",
        "The documented counting command (python3 -B .ufo/waves/round-93/",
        "c93_selfassess.py --root . --revision <rev>) puts that directory first",
        "on sys.path, so 'import subprocess' loads the attacker's file.",
        "counter copy sha256: " + copy_sha + " (frozen: " + CSHA + ")",
        "fixture: " + d, "defect revision: " + rev,
        "disk truth, same revision:",
        "$ git -C %s show %s:corpus/lessons/round-05.md  -> exit=%d %r" % (
            d, rev, defect.returncode, defect.stdout[:80]),
        "$ git -C %s show %s:SKILL.md | grep gone.py  -> %r" % (d, rev, gone_row),
        "$ cd " + d + " && python3 -B .ufo/waves/round-93/c93_selfassess.py --root . --revision " + rev,
        "exit=%d" % rc, "line1: " + line1(out),
        "detail: " + detail(out)])


def sc_19():  # fail-closed controls
    d = fixture("19dead")
    build_clean(d)
    rev = commit(d, "clean")
    rc1, out1, err1, cmd1 = run_counter(d, "deadbeef" * 5)
    d2 = fixture("19noskill")
    build_clean(d2)
    rm(d2, "SKILL.md")
    rev2 = commit(d2, "no SKILL.md")
    rc2, out2, err2, cmd2 = run_counter(d2, rev2)
    d3 = fixture("19empty")
    git(d3, "init", "-q")
    git(d3, "-c", "user.email=fx@example.invalid", "-c", "user.name=fx",
        "commit", "-q", "--allow-empty", "-m", "empty")
    rev3 = git(d3, "rev-parse", "HEAD").strip()
    rc3, out3, err3, cmd3 = run_counter(d3, rev3)
    receipt("19-fail-closed", [
        "scenario: fail-closed controls on unevaluable input",
        "counter sha256: " + CSHA,
        "(a) unknown revision:", "$ " + cmd1, "exit=%d" % rc1, "stdout: " + out1.strip(),
        "(b) SKILL.md absent at revision:", "$ " + cmd2, "exit=%d" % rc2,
        "stdout: " + out2.strip(),
        "(c) empty repository:", "$ " + cmd3, "exit=%d" % rc3, "line1: " + line1(out3)])


def main():
    with open(COUNTER, "wb") as fh:
        p = subprocess.run(["git", "-C",
                            "/home/vgpnk/Projects/shokunin/kake-shokunin", "show",
                            "bb8012fee38c0e497cdaf36337072737bca0b3cd:.ufo/waves/round-93/c93_selfassess.py"],
                           capture_output=True)
        assert p.returncode == 0, p.stderr
        fh.write(p.stdout)
    global CSHA
    CSHA = hashlib.sha256(open(COUNTER, "rb").read()).hexdigest()
    print("counter sha256:", CSHA)
    for fn in [sc_00, sc_01, sc_02, sc_03, sc_04, sc_05, sc_06, sc_07, sc_08,
               sc_09, sc_10, sc_11, sc_12, sc_13, sc_14, sc_15, sc_16, sc_17,
               sc_18, sc_19]:
        if len(sys.argv) > 1 and fn.__name__ not in sys.argv[1:]:
            continue
        try:
            fn()
            print("ok", fn.__name__)
        except Exception as exc:  # keep going; report per-scenario failure
            print("FAIL", fn.__name__, repr(exc))
    print("receipts in", REC)


if __name__ == "__main__":
    sys.exit(main())
