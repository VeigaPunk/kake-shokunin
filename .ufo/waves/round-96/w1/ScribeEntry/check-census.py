#!/usr/bin/env python3
"""Census-check the finalized S480 row in a lane-shaped scratch mirror.

Seat ScribeEntry, kake round 96 (hyaku run 15, attempt 1).

Builds two scratch mirrors of the lane (a control with no S480 row, and one with the
finalized S480 row inserted at line 226, after S479), each carrying the used-by paths
the census's E11 check resolves, then runs the fleet's read-only
`scripts/sources-census.sh validate` and `census` against each mirror and diffs the
results. The lane worktree is never written: the mirror's corpus/SOURCES.md is a copy
whose insert is made in the scratch tree only.

Run:  python3 -B check-census.py        (exit 0 iff both mirrors validate clean)
"""
import hashlib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FLEET = "/home/vgpnk/Projects/shokunin"
CENSUS = os.path.join(FLEET, "scripts/sources-census.sh")
SCRATCH = "/fast/scratch/hyaku/kake-r96/ScribeEntry"
ROWFILE = os.path.join(HERE, "s480-row.md")
TODAY = "2026-11-05"

# Paths the census's E11 check resolves for mined rows (repo-relative).
USED_BY_PATHS = [
    "corpus/knowledge", "corpus/lessons", "SKILL.md", "SCORECARD.md",
    "scripts/source_recheck.py", ".ufo/waves/round-41/",
    ".ufo/waves/round-73/", ".ufo/waves/round-95/freeze.md",
    ".ufo/waves/round-96/w1/ScoutRFC/fetch.txt",
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_row():
    """The row is the fenced block in s480-row.md (the first ``` fenced block)."""
    text = open(ROWFILE, encoding="utf-8").read()
    blocks = text.split("```")
    for b in blocks:
        b = b.strip("\n")
        if b.startswith("| S480 |"):
            return b
    raise SystemExit("no S480 row block found in %s" % ROWFILE)


def build_mirror(name, row=None):
    root = os.path.join(SCRATCH, name)
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(os.path.join(root, "corpus"), exist_ok=True)
    shutil.copy2(os.path.join(LANE, "corpus/SOURCES.md"),
                 os.path.join(root, "corpus/SOURCES.md"))
    for rel in USED_BY_PATHS:
        src = os.path.join(LANE, rel)
        dst = os.path.join(root, rel)
        if os.path.isdir(src):
            os.makedirs(os.path.dirname(dst.rstrip("/")), exist_ok=True)
            shutil.copytree(src, dst.rstrip("/"), dirs_exist_ok=True)
        elif os.path.isfile(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
    if row is not None:
        p = os.path.join(root, "corpus/SOURCES.md")
        lines = open(p, encoding="utf-8").read().splitlines(True)
        idx = next(i for i, l in enumerate(lines) if l.startswith("| S479 "))
        lines.insert(idx + 1, row + "\n")
        open(p, "w", encoding="utf-8").write("".join(lines))
    return root


def run(mode, root):
    out = os.path.join(SCRATCH, "census-%s-%s.txt" % (mode, os.path.basename(root)))
    p = subprocess.run([CENSUS, mode, "--today", TODAY, root],
                       capture_output=True, text=True)
    open(out, "w", encoding="utf-8").write(
        "command: %s %s --today %s %s\nrc: %d\n%s%s"
        % (CENSUS, mode, TODAY, root, p.returncode, p.stdout, p.stderr))
    return p.returncode, p.stdout + p.stderr, out


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    row = extract_row()
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    print("row cells: %d (want 11)" % len(cells))
    if len(cells) != 11:
        print("VIOLATION cell count")
        return 1
    if any("|" in c for c in cells):
        print("VIOLATION a cell holds a literal pipe")
        return 1
    print("no literal or escaped pipe in any cell: yes")
    for i, c in enumerate(cells):
        print("  cell %d: %s" % (i, c[:90] + ("..." if len(c) > 90 else "")))
    print("row sha256: %s" % hashlib.sha256(row.encode()).hexdigest())

    ctrl = build_mirror("mirror-control")
    with_row = build_mirror("mirror-with-s480", row)

    lane_sources = os.path.join(LANE, "corpus/SOURCES.md")
    ctrl_sources = os.path.join(ctrl, "corpus/SOURCES.md")
    print("control mirror SOURCES.md cmp vs lane: ", end="")
    rc = subprocess.run(["cmp", lane_sources, ctrl_sources]).returncode
    print("rc=%d (0 = identical)" % rc)
    if rc != 0:
        print("VIOLATION control mirror differs from the lane file")
        return 1

    results = {}
    for mode in ("validate", "census"):
        rc_c, out_c, f_c = run(mode, ctrl)
        rc_r, out_r, f_r = run(mode, with_row)
        results[mode] = (rc_c, out_c, rc_r, out_r, f_c, f_r)
        print("\n=== %s ===" % mode)
        print("control  rc=%d" % rc_c)
        print(out_c.rstrip())
        print("with S480 rc=%d" % rc_r)
        print(out_r.rstrip())

    bad = 0
    for mode, (rc_c, out_c, rc_r, out_r, _, _) in results.items():
        if rc_c != 0:
            print("VIOLATION control %s rc=%d" % (mode, rc_c))
            bad += 1
        if rc_r != 0:
            print("VIOLATION with-S480 %s rc=%d" % (mode, rc_r))
            bad += 1
        e_lines = [l for l in out_r.splitlines() if "\tE" in l]
        if e_lines:
            print("VIOLATION E-findings with S480: %s" % e_lines)
            bad += 1
    # the diff between control and with-S480 outputs (validate), with the mirror
    # lane-name prefix normalized away so only the real difference shows.
    _, out_c, _, out_r, _, _ = results["validate"]

    def norm_lines(text):
        return [l.split("\t", 1)[1] if "\t" in l else l
                for l in text.splitlines()]

    c_lines, r_lines = norm_lines(out_c), norm_lines(out_r)
    added = [l for l in r_lines if l not in c_lines]
    removed = [l for l in c_lines if l not in r_lines]
    print("\n=== validate diff (control -> with S480) ===")
    for l in added:
        print("+ %s" % l)
    for l in removed:
        print("- %s" % l)
    if any("\tE" in l for l in added):
        print("VIOLATION the added lines include an E-finding")
        bad += 1
    print("violations=%d" % bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
