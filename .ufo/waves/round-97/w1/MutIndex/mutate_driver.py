#!/usr/bin/env python3
"""MutIndex mutation driver for the frozen round-97 C1 counter (c97_index.py).

Protocol (UFO-FSD): the lane copy is never edited; mutants are built from a
hash-verified pristine copy in scratch. Detectors: (1) --selftest via the
public CLI with --work in scratch, (2) full run against LANE at round base
36d148f5..., (3) full run against LANE at C1 repair 9e27ce0b....
Killed iff selftest fails or base/repair stdout differs from the pristine
reference. Baseline (pristine) detector failure => inconclusive, mutants not
scored.
"""
import hashlib
import json
import os
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kake-r97/MutIndex"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
BASE = "36d148f5c60100021304903c30e5663207c72f4f"
REPAIR = "9e27ce0b2a8d168e032ab79ea11471b36eaceedf"
PRISTINE = os.path.join(SCRATCH, "pristine", "c97_index.py")
PY = sys.executable or "python3"

FENCE_BLOCK = (
    '        if in_fence:\n'
    '            if st.startswith(in_fence):\n'
    '                in_fence = None\n'
    '            continue\n'
    '        if st.startswith("```") or st.startswith("~~~"):\n'
    '            in_fence = st[:3]\n'
    '            continue\n'
)
COMMENT_IN_BLOCK = (
    '        if in_comment:\n'
    '            if "-->" in line:\n'
    '                in_comment = False\n'
    '            continue\n'
)
COMMENT_OPEN_BLOCK = (
    '        if st.startswith("<!--"):\n'
    '            if "-->" not in st[4:]:\n'
    '                in_comment = True\n'
    '            continue\n'
)
RANGE_BLOCK = (
    '    for a, b in ID_RANGE.findall(text):\n'
    '        lo, hi = int(a), int(b)\n'
    '        if lo <= hi and hi - lo <= 50:\n'
    '            width = len(a)\n'
    '            out.update("S%0*d" % (width, n) for n in range(lo, hi + 1))\n'
)
EMPTY_POP_BLOCK = (
    '    if not entries:\n'
    '        raise GitError("empty population under %s at %s" % (KDIR, sha))\n'
)

# id, patch summary, [(old, new)] unique exact replacements
MUTANTS = [
    ("M01-no-fence-skip",
     "visible_lines: delete fence open/close handling (fenced rows become visible)",
     [(FENCE_BLOCK, "")]),
    ("M02-no-comment-skip",
     "visible_lines: delete HTML comment open/close handling",
     [(COMMENT_IN_BLOCK, ""), (COMMENT_OPEN_BLOCK, "")]),
    ("M03-no-entry-header-required",
     'index_rows: header-less tables fall back to Entry column index 1 instead of None',
     [('            entry_col = lowered.index("entry") if "entry" in lowered else None',
       '            entry_col = lowered.index("entry") if "entry" in lowered else 1')]),
    ("M04-ids-from-entry-cell-only",
     "audit: id coverage checked against the Entry cell only, not the whole row",
     [('            have = ids_in(line)',
       '            have = ids_in(entry_cell)')]),
    ("M05-no-range-expansion",
     "ids_in: delete S###-S### range expansion block",
     [(RANGE_BLOCK, "")]),
    ("M06-min-words-8to1",
     "MIN_WORDS constant 8 -> 1",
     [("MIN_WORDS = 8", "MIN_WORDS = 1")]),
    ("M07-min-shared-2to0",
     "MIN_SHARED constant 2 -> 0",
     [("MIN_SHARED = 2", "MIN_SHARED = 0")]),
    ("M08-readme-from-worktree",
     'load: README read from the working tree file instead of git show REV:corpus/README.md',
     [('    readme = git(root, "show", "%s:%s" % (sha, README)).decode("utf-8", "replace")',
       '    with open(os.path.join(root, README), "rb") as fh:\n'
       '        readme = fh.read().decode("utf-8", "replace")')]),
    ("M09-no-empty-pop-exit2",
     "load: delete empty-population GitError (fails-open on empty corpus)",
     [(EMPTY_POP_BLOCK, "")]),
    ("M10-dangling-not-counted",
     'run: mismatches = unindexed only; dangling tokens not counted',
     [('    mism = len(d["unindexed"]) + len(d["dangling"])',
       '    mism = len(d["unindexed"])')]),
    ("M11-unmet-exit-2",
     "run: unmet exit code 1 -> 2 (wrong failure mode)",
     [("    return 0 if met else 1",
       "    return 0 if met else 2")]),
    ("M12-no-git-no-replace-objects",
     'git_env: drop GIT_NO_REPLACE_OBJECTS=1 pin (git replace refs become visible)',
     [('    return {"PATH": "/usr/bin:/bin", "GIT_NO_REPLACE_OBJECTS": "1",',
       '    return {"PATH": "/usr/bin:/bin",')]),
    ("M13-git-from-path",
     'GIT constant "/usr/bin/git" -> "git" (PATH-resolved, shadowable)',
     [('GIT = "/usr/bin/git"', 'GIT = "git"')]),
    ("M14-no-range-zero-padding",
     'ids_in: range expansion loses zero padding ("S%0*d" % (width, n) -> "S%d" % n)',
     [('            out.update("S%0*d" % (width, n) for n in range(lo, hi + 1))',
       '            out.update("S%d" % n for n in range(lo, hi + 1))')]),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def patch_text(text, repls):
    for old, new in repls:
        n = text.count(old)
        assert n == 1, "non-unique patch anchor (count=%d): %r" % (n, old[:70])
        text = text.replace(old, new)
    return text


def run_detector(script, args, log_path):
    p = subprocess.run([PY, "-B", script] + args, capture_output=True,
                       text=True, timeout=900, cwd=SCRATCH)
    with open(log_path, "w") as fh:
        fh.write("cmd: python3 -B %s %s\nrc=%d\n--- stdout ---\n%s\n--- stderr(tail) ---\n%s"
                 % (script, " ".join(args), p.returncode, p.stdout, p.stderr[-500:]))
    return p.returncode, p.stdout, p.stderr[-500:]


def main():
    pristine_sha = sha256(PRISTINE)
    with open(PRISTINE) as fh:
        base_text = fh.read()
    print("pristine sha256 %s" % pristine_sha)

    def key(rc, out):
        return (rc, out)

    # ---- baseline: pristine through all three detectors
    print("== baseline (pristine) ==")
    st = run_detector(PRISTINE, ["--selftest", "--work",
                                 os.path.join(SCRATCH, "st-ref")],
                      os.path.join(SCRATCH, "logs", "REF-selftest.log"))
    b = run_detector(PRISTINE, ["--root", LANE, "--revision", BASE,
                                "--work", os.path.join(SCRATCH, "w-ref")],
                     os.path.join(SCRATCH, "logs", "REF-base.log"))
    r = run_detector(PRISTINE, ["--root", LANE, "--revision", REPAIR,
                                "--work", os.path.join(SCRATCH, "w-ref")],
                     os.path.join(SCRATCH, "logs", "REF-repair.log"))
    ref_st_ok = st[0] == 0 and st[1].strip().startswith("selftest 14/14")
    print("REF selftest rc=%d out=%r" % (st[0], st[1].strip()[:90]))
    print("REF base rc=%d line1=%r" % (b[0], b[1].splitlines()[0] if b[1] else ""))
    print("REF repair rc=%d line1=%r" % (r[0], r[1].splitlines()[0] if r[1] else ""))
    if not (ref_st_ok and b[0] == 1 and "mismatches=38" in b[1]
            and r[0] == 0 and "mismatches=0" in r[1] and "met=true" in r[1]):
        print("BASELINE-FAILED: pristine detectors did not reproduce controls; "
              "mutants inconclusive, not scored")
        return 3

    rows = []
    for mid, desc, repls in MUTANTS:
        mpath = os.path.join(SCRATCH, "mutants", mid + ".py")
        with open(mpath, "w") as fh:
            fh.write(patch_text(base_text, repls))
        msha = sha256(mpath)
        print("== %s (sha256 %s) %s ==" % (mid, msha[:12], desc))
        mst = run_detector(mpath, ["--selftest", "--work",
                                   os.path.join(SCRATCH, "st-" + mid)],
                           os.path.join(SCRATCH, "logs", mid + "-selftest.log"))
        mb = run_detector(mpath, ["--root", LANE, "--revision", BASE,
                                  "--work", os.path.join(SCRATCH, "w-" + mid)],
                          os.path.join(SCRATCH, "logs", mid + "-base.log"))
        mr = run_detector(mpath, ["--root", LANE, "--revision", REPAIR,
                                  "--work", os.path.join(SCRATCH, "w-" + mid)],
                          os.path.join(SCRATCH, "logs", mid + "-repair.log"))
        killed_by = []
        st_fail = not (mst[0] == 0 and mst[1].strip().startswith("selftest 14/14"))
        if st_fail:
            killed_by.append("selftest")
        if key(mb[0], mb[1]) != key(b[0], b[1]):
            killed_by.append("base")
        if key(mr[0], mr[1]) != key(r[0], r[1]):
            killed_by.append("repair")
        verdict = "killed" if killed_by else "SURVIVED"
        rows.append({
            "id": mid, "patch": desc, "killed_by": "+".join(killed_by) or "none",
            "verdict": verdict,
            "rc": "selftest=%d,base=%d,repair=%d" % (mst[0], mb[0], mr[0]),
            "sha256": msha,
            "selftest_line": (mst[1].splitlines() or [""])[0][:160],
            "selftest_fail_lines": [ln for ln in mst[1].splitlines()
                                    if ln.startswith("selftest FAIL")][:4],
            "base_line": (mb[1].splitlines() or [""])[0][:200],
            "repair_line": (mr[1].splitlines() or [""])[0][:200],
            "base_differs": key(mb[0], mb[1]) != key(b[0], b[1]),
            "repair_differs": key(mr[0], mr[1]) != key(r[0], r[1]),
        })
        print("   %s killed_by=%s rc=%s | st=%r base=%r repair=%r"
              % (verdict, rows[-1]["killed_by"], rows[-1]["rc"],
                 rows[-1]["selftest_line"][:60], rows[-1]["base_line"][:80],
                 rows[-1]["repair_line"][:80]))

    with open(os.path.join(SCRATCH, "mutants.tsv"), "w") as fh:
        fh.write("id\tpatch\tkilled_by\trc\n")
        for row in rows:
            fh.write("%s\t%s\t%s\t%s\n" % (row["id"], row["patch"],
                                           row["killed_by"], row["rc"]))
    with open(os.path.join(SCRATCH, "results.json"), "w") as fh:
        json.dump({"pristine_sha256": pristine_sha,
                   "ref_selftest": {"rc": st[0], "out": st[1].strip()},
                   "ref_base": {"rc": b[0], "line1": b[1].splitlines()[0]},
                   "ref_repair": {"rc": r[0], "line1": r[1].splitlines()[0]},
                   "mutants": rows}, fh, indent=1)
    killed = sum(1 for x in rows if x["verdict"] == "killed")
    surv = [x["id"] for x in rows if x["verdict"] != "killed"]
    print("SUMMARY killed=%d/%d survivors=%s" % (killed, len(rows),
                                                 ",".join(surv) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
