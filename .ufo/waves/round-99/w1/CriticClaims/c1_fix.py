#!/usr/bin/env python3
"""Follow-up C1 fixtures a10/a11 (corrected driver). Run only after c1_driver.py finished."""
import os, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
SCRATCH = "/fast/scratch/hyaku/kake-r99/CriticClaims"
FX = os.path.join(SCRATCH, "fx")
WORK = os.path.join(SCRATCH, "work")
OUT = os.path.join(SCRATCH, "out")
BASE = "9d341d1b46f16dbfbb41af75dd6d4966808dfa5d"
COUNTER = os.path.join(LANE, ".ufo/waves/round-99/c99_registry.py")
GIT = ["git", "-C", FX]


def sh(*args):
    r = subprocess.run(list(args), capture_output=True, text=True)
    if r.returncode != 0:
        print("CMD FAIL:", " ".join(args), r.returncode, r.stderr[-500:], file=sys.stderr)
        sys.exit(3)
    return r.stdout


top = sh(*GIT, "rev-parse", "--show-toplevel").strip()
assert os.path.realpath(top) == os.path.realpath(FX), "fixture toplevel mismatch"


def fixture(name, new_files, edits, expect_note=""):
    sh(*GIT, "checkout", "-q", "-B", "c1-" + name, BASE)
    skill_p = os.path.join(FX, "SKILL.md")
    skill = open(skill_p, encoding="utf-8").read()
    for old, new in edits:
        assert skill.count(old) == 1, "anchor not unique in %s" % name
        skill = skill.replace(old, new)
    open(skill_p, "w", encoding="utf-8").write(skill)
    for rel, content in new_files.items():
        p = os.path.join(FX, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(content)
    sh(*GIT, "add", "-A")
    sh(*GIT, "-c", "user.name=CriticClaims", "-c", "user.email=criticclaims@example.invalid",
       "commit", "-q", "-m", "c1 attack fixture " + name)
    sha = sh(*GIT, "rev-parse", "HEAD").strip()
    r = subprocess.run([sys.executable, "-B", COUNTER, "--root", FX, "--revision", sha,
                        "--work", WORK], capture_output=True, text=True)
    with open(os.path.join(OUT, "c1-%s.txt" % name), "w") as f:
        f.write("# attack %s %s\n# fixture commit %s\n%s\n%s\nexit=%d\n" % (
            name, expect_note, sha, r.stdout, r.stderr, r.returncode))
    first = r.stdout.split("\n")[1] if r.stdout.startswith("revision=") else r.stdout.split("\n")[0]
    print("%-24s rc=%d %s" % (name, r.returncode, first))


ROW_ANCHOR = "| wave_seat_record.py |"

fixture("a10-later-column-only",
        {"scripts/z9_late.py": "print('tool')\n"},
        [(ROW_ANCHOR,
          "| z9_late.py cross-reference | gate | `python3 -B scripts/z9_ok.py` | `0` clean; `1` failed "
          "| `python3 -B scripts/z9_ok.py --selftest` | also runs scripts/z9_late.py | kake |\n" + ROW_ANCHOR)],
        "OBSERVATION: cross-referenced tool named only in write scope stays unlisted")

fixture("a11-companion-selftest",
        {"scripts/z9_real.py": "import sys\nsys.exit('real path broken')\n",
         "scripts/z9_real_selftest.py": "import sys\nif '--selftest' in sys.argv:\n    print('selftest 1/1'); sys.exit(0)\nsys.exit(0)\n"},
        [(ROW_ANCHOR,
          "| z9_real.py | gate | `python3 -B scripts/z9_real.py` | `0` clean; `1` failed "
          "| `python3 -B scripts/z9_real_selftest.py --selftest` | none | kake |\n"
          "| z9_real_selftest.py | selftest runner | `python3 -B scripts/z9_real_selftest.py --selftest` | `0` pass; `1` fail "
          "| `python3 -B scripts/z9_real_selftest.py --selftest` | none | kake |\n" + ROW_ANCHOR)],
        "OBSERVATION: companion selftest file allowed by declared R5; z9_real is dead")

print("done")
