#!/usr/bin/env python3
"""CriticClaims C1 attack driver. Fixture commits live ONLY in the scratch clone fx."""
import os, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
SCRATCH = "/fast/scratch/hyaku/kake-r99/CriticClaims"
FX = os.path.join(SCRATCH, "fx")
WORK = os.path.join(SCRATCH, "work")
OUT = os.path.join(SCRATCH, "out")
BASE = "9d341d1b46f16dbfbb41af75dd6d4966808dfa5d"
COUNTER = os.path.join(LANE, ".ufo/waves/round-99/c99_registry.py")
os.makedirs(WORK, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

GIT = ["git", "-C", FX]


def sh(*args, **kw):
    r = subprocess.run(list(args), capture_output=True, text=True)
    if r.returncode != 0:
        print("CMD FAIL:", " ".join(args), r.returncode, r.stderr[-500:], file=sys.stderr)
        sys.exit(3)
    return r.stdout


top = sh(*GIT, "rev-parse", "--show-toplevel").strip()
assert os.path.realpath(top) == os.path.realpath(FX), "fixture toplevel mismatch: %s" % top


def fixture(name, new_files, edits, expect_note=""):
    """edits: list of (old, new) exact replacements in SKILL.md."""
    sh(*GIT, "checkout", "-q", "-B", "c1-" + name, BASE)
    skill_p = os.path.join(FX, "SKILL.md")
    skill = open(skill_p, encoding="utf-8").read()
    for old, new in edits:
        assert skill.count(old) == 1, "edit anchor not unique (%d): %r in %s" % (skill.count(old), old[:60], name)
        skill = skill.replace(old, new)
    open(skill_p, "w", encoding="utf-8").write(skill)
    for rel, content in new_files.items():
        p = os.path.join(FX, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
    sh(*GIT, "add", "-A")
    sh(*GIT, "-c", "user.name=CriticClaims", "-c", "user.email=criticclaims@example.invalid",
       "commit", "-q", "-m", "c1 attack fixture " + name)
    sha = sh(*GIT, "rev-parse", "HEAD").strip()
    r = subprocess.run([sys.executable, "-B", COUNTER, "--root", FX, "--revision", sha,
                        "--work", WORK], capture_output=True, text=True)
    out = "# attack %s %s\n# fixture commit %s\n%s\n%s\nexit=%d\n" % (
        name, expect_note, sha, r.stdout, r.stderr, r.returncode)
    with open(os.path.join(OUT, "c1-%s.txt" % name), "w") as f:
        f.write(out)
    first = r.stdout.split("\n")[1] if r.stdout.startswith("revision=") else r.stdout.split("\n")[0]
    print("%-24s rc=%d %s" % (name, r.returncode, first))
    return r.returncode, r.stdout


GOODTOOL = ('import sys\n'
            'def real_check():\n    return False  # gate is actually broken\n'
            'if "--selftest" in sys.argv:\n'
            '    print("selftest ok")  # ignores the failure it should catch\n'
            '    sys.exit(0)\n'
            'sys.exit(0 if real_check() else 1)\n')

# baseline
r = subprocess.run([sys.executable, "-B", COUNTER, "--root", FX, "--revision", BASE, "--work", WORK],
                   capture_output=True, text=True)
open(os.path.join(OUT, "c1-baseline.txt"), "w").write(
    "# baseline at C1 repair commit 9d341d1b\n%s\n%s\nexit=%d\n" % (r.stdout, r.stderr, r.returncode))
print("%-24s rc=%d %s" % ("baseline", r.returncode, r.stdout.split("\n")[1]))

ROW_ANCHOR = "| wave_seat_record.py |"

fixture("a1-vacuous-selftest",
        {"scripts/z9_demo.py": GOODTOOL},
        [(ROW_ANCHOR,
          "| z9_demo.py | gate | `python3 -B scripts/z9_demo.py --check` | `0` clean; `1` failed "
          "| `python3 -B scripts/z9_demo.py --selftest` (`0` selftest ok) | none | kake |\n" + ROW_ANCHOR)],
        "selftest ignores the failure it should catch")

fixture("a2-comment-selftest",
        {"scripts/z9_broken.py": "this is not python (\n"},
        [(ROW_ANCHOR,
          "| z9_broken.py | gate | `python3 -B scripts/z9_broken.py` | `0` clean; `1` failed "
          "| `echo selftest-ok # python3 -B scripts/z9_broken.py --selftest` | none | kake |\n" + ROW_ANCHOR)],
        "selftest span is a comment; echo runs instead")

fixture("a3-dup-owner-column",
        {"scripts/z9_ok.py": "import sys\nif '--selftest' in sys.argv:\n    print('selftest 1/1'); sys.exit(0)\nsys.exit(0)\n"},
        [(ROW_ANCHOR,
          "\n| Name | Kind | Entry command | Verdict map | Self-test | Write scope | Owner | Owner |\n"
          "|---|---|---|---|---|---|---|---|\n"
          "| z9_ok.py | gate | `python3 -B scripts/z9_ok.py` | `0` clean; `1` failed "
          "| `python3 -B scripts/z9_ok.py --selftest` | none | kaidoku | kake |\n" + ROW_ANCHOR)],
        "first Owner cell says kaidoku; ix takes the last Owner column")

fixture("a4-lstree-quoting",
        {"scripts/z9_caf\u00e9.py": "print('tool')\n", 'scripts/z9_qu"te.py': "print('tool')\n"},
        [],
        "two committed tools invisible to ls-tree -r --name-only population")

fixture("a5-sh-extension",
        {"scripts/z9_tool.sh": "#!/bin/sh\nexit 0\n"},
        [],
        "committed non-.py/.mjs tool under scripts/ (population scope declared in docstring)")

fixture("a6-dangling-paren-entry",
        {},
        [("| `python3 -B scripts/base_path_selftest.py` (`--tool PATH`, `--fixtures DIR`, `--python EXE`, `--case SUBSTR`, `--verbose`) |",
          "| `python3 -B scripts/base_path_selftest.py (dead fallback scripts/gone.py)` (`--tool PATH`) |")],
        "dead scripts/gone.py after '(' escapes SCRIPT_TOKEN boundaries")

fixture("a7-dangling-write-scope",
        {},
        [("| reads the committed fixtures; writes nothing | kake |\n| cache_key.py |",
          "| reads the committed fixtures; writes nothing (replaces scripts/gone.py) | kake |\n| cache_key.py |")],
        "dead tool named in a non-entry column; dangling scan is entry-spans only")

fixture("a8-blankline-orphan",
        {},
        [("\n| cache_key.py | probe",
          "\n\n| cache_key.py | probe (orphaned duplicate) | `python3 -B scripts/cache_key.py && python3 -B scripts/gone.py` "
          "| `0` key; `1` refusal | no self-test | stdin/stdout/stderr only | kake |\n| cache_key.py | probe"),
         ],
        "visible dangling row orphaned by a blank line; never scanned")

fixture("a9-unterminated-fence",
        {},
        [("## Round 99 — tool registry completion", "```\n## Round 99 — tool registry completion")],
        "OBSERVATION: hides the true table (expected met=false, instrument false negative)")

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
