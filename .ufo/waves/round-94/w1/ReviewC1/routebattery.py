#!/usr/bin/env python3
"""ReviewC1 route battery against frozen c94_selfassess.py.

Base = the counter's own CLEAN synthetic lane. For each route we build a
scratch git repo, add the route defect (and, where the route simulates an
REPAIR, the repaired artefact), commit, and run the frozen counter:

  python3 -B c94.py --root <repo> --revision HEAD --skip-battery
                    --base-pins-json {"lessons":1,"entries":1,"rows":1,"criteria":1}
                    --surfaces-file <per-fixture surfaces.json with base
                                     identity surfaces preserved>

Expected reading: rc=1 + mismatches>0 = REFUSAL (good), rc=0 = GREEN
(route when the lane is defective). rc=2 = unevaluable.
"""
import json
import os
import re
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kake-r94/ReviewC1"
COUNTER = ("/home/vgpnk/Projects/shokunin/kake-shokunin/"
           ".ufo/waves/round-94/c94_selfassess.py")

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


def surfaces_of(files, extra_skills=()):
    lessons = sorted(k for k in files if k.startswith("corpus/lessons/"))
    first = []
    for line in files.get("SKILL.md", "").splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 4:
                first.append(cells[0])
    first.extend(extra_skills)
    return {
        "lessons": lessons,
        "entries": sorted(k for k in files if k.startswith("corpus/knowledge/")),
        "quality_criteria_headings": ["Round-01 criterion — a thing"],
        "skill_row_first_cells": first,
        "mistakes_sections": [p for p in lessons if "## Mistakes" in files[p]],
    }


def run(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, cwd=cwd)


def make_repo(fdir, files):
    repo = os.path.join(fdir, "lane")
    if os.path.exists(os.path.join(repo, ".git")):
        top = subprocess.run(["git", "-C", repo, "rev-parse", "--show-toplevel"],
                             capture_output=True).stdout.decode().strip()
        assert top in (repo, os.path.realpath(repo)), "toplevel mismatch %s" % top
    else:
        os.makedirs(repo, exist_ok=True)
        run(["git", "-C", repo, "init", "-q"])
    for rel, text in files.items():
        dest = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(text)
    gitc = ["git", "-C", repo]
    run(gitc + ["config", "user.email", "reviewc1@fixture.invalid"])
    run(gitc + ["config", "user.name", "reviewc1"])
    if SYMLINK_SETUP:
        for target, dest, kind in SYMLINK_SETUP:
            path = os.path.join(repo, dest)
            if kind == "symlink":
                os.symlink(target, path)
            elif kind == "dir":
                os.makedirs(path, exist_ok=True)
    run(gitc + ["add", "-A"])
    c = run(gitc + ["commit", "-q", "-m", "reviewc1 fixture"])
    if c.returncode != 0:
        raise RuntimeError(c.stderr.decode())
    top = subprocess.run(["git", "-C", repo, "rev-parse", "--show-toplevel"],
                         capture_output=True).stdout.decode().strip()
    assert top == repo or (top == os.path.realpath(repo)), "toplevel mismatch %s" % top
    rev = run(gitc + ["rev-parse", "HEAD"]).stdout.decode().strip()
    return repo, rev


SYMLINKS = {}
SYMLINK_SETUP = []
ROUTES_CREATED = {}


def route(name, files_defect, files_fix=None, symlink=None, note=""):
    global SYMLINK_SETUP
    SYMLINK_SETUP = symlink or []
    fdir = os.path.join(SCRATCH, "fx_" + re.sub(r"[^A-Za-z0-9]+", "_", name))
    os.makedirs(fdir, exist_ok=True)
    defect = dict(CLEAN)
    defect.update(files_defect)
    repo, rev = make_repo(fdir, defect)
    if symlink:
        for target, dest, kind in symlink:
            path = os.path.join(repo, dest)
            if kind == "symlink":
                if os.path.lexists(path):
                    os.remove(path)
                os.symlink(target, path)
            elif kind == "dir":
                os.makedirs(path, exist_ok=True)
            elif kind == "del":
                os.remove(path)
        run(["git", "-C", repo, "add", "-A"])
        c = run(["git", "-C", repo, "commit", "-q", "-m", "symlink layer"])
        assert c.returncode == 0 or b"nothing to commit" in c.stdout + c.stderr, (
            c.stderr.decode())
        rev = run(["git", "-C", repo, "rev-parse", "HEAD"]).stdout.decode().strip()
    extra = ()
    if files_fix:
        extra = tuple(json.loads(line) for line in files_fix)
    surf = surfaces_of(defect, extra)
    spath = os.path.join(fdir, "surfaces.json")
    with open(spath, "w") as fh:
        json.dump(surf, fh)
    env = dict(os.environ, TMPDIR=SCRATCH, HOME=SCRATCH)
    p = subprocess.run(
        [sys.executable, "-B", COUNTER, "--root", repo, "--revision", rev,
         "--skip-battery", "--work", fdir,
         "--base-pins-json", json.dumps({"lessons": 1, "entries": 1, "rows": 1,
                                         "criteria": 1}),
         "--surfaces-file", spath],
        capture_output=True, env=env, timeout=300)
    line1 = p.stdout.decode("utf-8", "replace").splitlines()
    line1 = line1[0] if line1 else "(no stdout)"
    detail = []
    for ln in p.stdout.decode("utf-8", "replace").splitlines()[1:]:
        d = json.loads(ln)
        for m in d["mismatches"]:
            detail.append("%s %s | %s" % (m["class"], m["path"], m["detail"]))
    verdict = "REFUSED" if p.returncode != 0 else (
        "GREEN(rc0)" if p.returncode == 0 else "?")
    return ({"route": name, "rc": p.returncode, "verdict": verdict,
             "line1": line1[:220], "findings": detail, "note": note,
             "stderr_tail": p.stderr.decode("utf-8", "replace")[-400:]})


import copy  # noqa

ROUTES_CREATED["n"] = 0

# R01  Gate body two junk lines -> counter should still refuse (2 non-empty).
r_r01 = route("R01_gate_two_junk_lines", {
    "corpus/lessons/round-02.md": "# r2\n\n## Gate\n\nlorem ipsum.\n scrolled.\n\n"
                                  "## Mistakes\n\n| # | Class |\n|---|---|\n"
                                  "| 1 | a |\n| 2 | b |\n"},
    note="refusal expected: 2 non-empty lines DO count")

# R02  Mistakes table entirely indented (simulated deletion under frozen surfaces)
r_r02 = route("R02_mistakes_all_indented", {
    "corpus/lessons/round-02.md": "# r2\n\n## Gate\n\nadmit C.\nreject D.\n\n"
                                  "  ## Mistakes\n\n  | # | Class |\n"
                                  "  |---|---|\n| 1 | a |\n| 2 | b |\n"},
    note="refusal expected: no L1 Mistakes section")

# R02b  Mistakes section with only indented separators (deletion-simulation)
r_r02b = route("R02b_mistakes_leading_spaces", {
    "corpus/lessons/round-02.md": "# r2\n\n## Gate\n\nadmit C.\nreject D.\n\n"
                                  "## Mistakes\n\n    | # | Class |\n"
                                  "    |---|---|\n    | 1 | a |\n| 2 | b |\n"},
    note="refusal expected: no L1 Mistakes section")

# R03  knowledge entry with TWO source lines; first carries S001 (a real row)
r_r03 = route("R03_two_source_lines", {
    "corpus/knowledge/entry.md": "source: S001\nsource: garbage no locator no id\n"
                                 "verified-at: 2026-11-05\nrecheck: 180d\n\nbody\n"},
    note="refusal expected: first source line only is parsed")

# R03b knowledge entry without verifiedAt header
r_r03b = route("R03b_missing_verified_at", {
    "corpus/knowledge/entry.md": "source: S001\nverifiedAt: 2026-11-05\n"
                                 "recheck: 180d\n\nbody\n"},
    note="refusal expected: header key misspelled")

# R04  SOURCES row id with leading space (row identity confusion)
r_r04a = route("R04a_sources_row_leading_space", {
    "corpus/SOURCES.md": "# S\n\n## Registry\n\n| id | source |\n|---|---|\n"
                         " | S001 | x |\n"},
    note="refusal expected: unnamed row in row_ids")

# R04b  SOURCES row id lowercase (row identity confusion)
r_r04b = route("R04b_sources_row_lowercase", {
    "corpus/SOURCES.md": "# S\n\n## Registry\n\n| id | source |\n|---|---|\n"
                         "| s001 | x |\n"},
    note="refusal expected: unnamed row in row_ids")

# R05  SKILL path with #anchor (phase-1 residual diagnosed in the lesson)
r_r05 = route("R05_skill_anchor", {
    "SKILL.md": CLEAN["SKILL.md"] + "| t2 | doc | `apps/index.ts#L42` | n/a |\n"},
    note="refusal expected: not a parseable suffix")

# R05b  SKILL path with :line suffix pointing to an EXISTING blob
r_r05b = route("R05b_skill_line_suffix_existing", {
    "SKILL.md": CLEAN["SKILL.md"] + "| t3 | doc | `scripts/t.py:42` | n/a |\n"},
    note="refusal expected: suffix stripped then resolves; no finding")

# R06  SKILL path with glob
r_r06 = route("R06_skill_glob", {
    "SKILL.md": CLEAN["SKILL.md"] + "| t4 | glob | `scripts/*.py` | n/a |\n"},
    note="refusal expected: glob skipped")

# R07  QUALITY section citing a 1-byte lesson
r_r07 = route("R07_cite_one_byte_lesson", {
    "corpus/QUALITY.md": "# Q\n\n## Round-01 criterion — a thing\n\n"
                         "Grounded in `corpus/lessons/tiny.md`.\n",
    "corpus/lessons/tiny.md": "x"},
    note="refusal expected: lesson name must contain criteria")

# R08  lesson renamed across dirs, name identical (routes base identity off)
r_r08 = route("R08_same_name_other_dir", {
    }, 
)
# build R08 separately: mutate files beyond dict-concat.
def r08_impl():
    global SYMLINK_SETUP
    name = "R08_same_name_other_dir"
    fdir = os.path.join(SCRATCH, "fx_" + re.sub(r"[^A-Za-z0-9]+", "_", name))
    os.makedirs(fdir, exist_ok=True)
    files = dict(CLEAN)
    files["corpus/lessons/nested/round-02.md"] = files.pop("corpus/lessons/round-02.md")
    files["corpus/lessons/legacy/round-02.md"] = files["corpus/lessons/nested/round-02.md"]
    repo, rev = make_repo(fdir, files)
    surf = surfaces_of(files, extra_skills=())
    surf["lessons"] = sorted(surf["lessons"])
    spath = os.path.join(fdir, "surfaces.json")
    with open(spath, "w") as fh:
        json.dump(surf, fh)
    env = dict(os.environ, TMPDIR=SCRATCH, HOME=SCRATCH)
    p = subprocess.run(
        [sys.executable, "-B", COUNTER, "--root", repo, "--revision", rev,
         "--skip-battery", "--work", fdir,
         "--base-pins-json", json.dumps({"lessons": 1, "entries": 1, "rows": 1,
                                         "criteria": 1}),
         "--surfaces-file", spath],
        capture_output=True, env=env, timeout=300)
    line1 = p.stdout.decode("utf-8", "replace").splitlines()
    line1 = line1[0] if line1 else "(no stdout)"
    findings = []
    for ln in p.stdout.decode("utf-8", "replace").splitlines()[1:]:
        d = json.loads(ln)
        for m in d["mismatches"]:
            findings.append("%s %s | %s" % (m["class"], m["path"], m["detail"]))
        for i in d["identity_missing"]: findings.append("IDENT " + i)
    verdict = "REFUSED" if p.returncode != 0 else ("GREEN(rc0)" if p.returncode == 0 else "?")
    return ({"route": name, "rc": p.returncode, "verdict": verdict,
             "line1": line1[:220], "findings": findings,
             "stderr_tail": p.stderr.decode("utf-8", "replace")[-400:]})

r_r08 = r08_impl()


# R09  SKILL.md names a symlink whose target text is a mini blob
r_r09 = route("R09_skill_symlink_as_target", {
    "SKILL.md": CLEAN["SKILL.md"] + "| t5 | link | `scripts/home.config` | n/a |\n"},
    symlink=[("../root/others/things/root/others/root/things/home.config",
              "scripts/home.config", "symlink")],
    note="refusal expected: the symlink text is a gigantic blob")

# R10  absence span with a non-square bracket (unrecognized absence)
r_r10 = route("R10_absence_alt_bracket", {
    "SKILL.md": CLEAN["SKILL.md"] + (
        "| script | ghost | [r94-removal 2026-11-05: `scripts/t.py` absent] | ok |\n"
        "| charset | ghost | «r94-absence 2026-11-05: `scripts/gone2.py` absent» | ok |\n")},
    note="seen: the square-bracket form refused (present scripts/t.py)")

# R10b  absence span with mismatched closing bracket (square open, angle close)
r_r10b = route("R10b_absence_mixed_bracket", {
    "SKILL.md": CLEAN["SKILL.md"] + (
        "| charset | ghost | [r94-absence 2026-11-05: `scripts/t.py` absent» | ok |\n"
        "| charset2 | ghost | [r94-absence 2026-11-05: `scripts/t.py` absent</span> | ok |\n")},
    note="seen: the craft-exact square form refused")

# R11  Entry with NO id but a path-locator whose suffix is not in the allowlist
r_r11 = route("R11_nodot_locator", {
    "corpus/knowledge/entry.md": "source: found in ~/docs/glossary.md\n"
                                 "verified-at: 2026-11-05\nrecheck: 90d\n\nbody\n"},
    note="refusal expected: locator ~/docs/… is not a path-like token and is a "
         "source-locator, not a lane-scope locator")

# R12  Entry with NO id but a locator that is a source-external token
r_r12 = route("R12_registry_locator", {
    "corpus/knowledge/entry.md": "source: S001 extra-apps index 2026-11-05\n"
                                 "verified-at: 2026-11-05\nrecheck: 90d\n\nbody\n"},
    note="refusal expected: index token ships a path/locator")

# R13  Gate heading styled as a stub (null-locator line in its body)
r_r13 = route("R13_gate_header_stub", {
    "corpus/lessons/round-02.md": "# r2\n\n## Gate: skimmed 2026-11-12\n\nbody.\n\n"
                                  "## Mistakes\n\n| # | exact |\n|---|---|\n"
                                  "| 1 | x |\n"},
    note="refusal expected: no exact L1 '## Gate' heading")

# R14  Every SKILL row name ends in a path-suffix (checked by L1, not r10)
r_r14 = route("R14_row_names_with_suffix", {
    "SKILL.md": "| name.md | doc.md | `apps/index.ts.md` | ok |\n"
                "| probe.py | script.py | `scripts/hop.py:2` | 1 |\n"},
    note="seen: false refusal if the counter treats the row name as a path")


# Summary table
ALL = [r_r01, r_r02, r_r02b, r_r03, r_r03b, r_r04a, r_r04b, r_r05, r_r05b,
       r_r06, r_r07, r_r08, r_r09, r_r10, r_r10b, r_r11, r_r12, r_r13, r_r14]
print(json.dumps(ALL, indent=1), file=sys.stderr)
out = os.path.join(SCRATCH, "routesummary.json")
with open(out, "w") as fh:
    json.dump(ALL, fh, indent=1)
print("wrote %s" % out)
