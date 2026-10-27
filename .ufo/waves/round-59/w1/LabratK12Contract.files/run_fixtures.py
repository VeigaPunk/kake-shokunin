#!/usr/bin/env python3
"""K12 contract labrat: run the CURRENT scripts/id_resolver.py against five registry-state fixtures.

Read-only w.r.t. the lane: the tool is copied out of the lane into scratch; every fixture lives under scratch.
No git mutation of the lane. Scratch dir: /fast/scratch/hyaku/kake-r59/LabratK12Contract
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

SCRATCH = "/fast/scratch/hyaku/kake-r59/LabratK12Contract"
TOOL = os.path.join(SCRATCH, "tool_current.py")
HDR = ("| id | name | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")


def row(sid):
    return f"| {sid} | fixture — https://example.invalid/{sid} | docs | A | scope | anchor | teaches | mined | 2026-10-27 | 90d | corpus/knowledge/ok.md |\n"


REG = "# Sources\n\n## Registry\n\n" + HDR + row("S900") + row("S901")


def build(case):
    """Return (fleet, lane) with corpus/SOURCES.md shaped per `case`."""
    root = tempfile.mkdtemp(dir=SCRATCH, prefix="fix-")
    fleet = os.path.join(root, "fleet")
    lane = os.path.join(fleet, "kake-shokunin")
    os.makedirs(os.path.join(lane, "corpus", "knowledge"))
    with open(os.path.join(lane, "corpus", "knowledge", "ok.md"), "w", encoding="utf-8") as fh:
        fh.write("Cites S900 and S901.\n")
    reg = os.path.join(lane, "corpus", "SOURCES.md")

    if case == "missing":
        pass                                              # no registry at all
    elif case == "directory":
        os.makedirs(os.path.join(reg, "sub"))
    elif case == "broken_symlink":
        os.symlink(os.path.join(lane, "corpus", "nope.md"), reg)
    elif case == "symlink_in_lane":
        real = os.path.join(lane, "corpus", "SOURCES-real.md")
        with open(real, "w", encoding="utf-8") as fh:
            fh.write(REG)
        os.symlink("./SOURCES-real.md", reg)
    elif case == "symlink_out_of_lane":
        out = os.path.join(root, "outside")
        os.makedirs(out)
        with open(os.path.join(out, "SOURCES.md"), "w", encoding="utf-8") as fh:
            fh.write(REG)
        os.symlink(os.path.join(out, "SOURCES.md"), reg)
    elif case == "unreadable":
        with open(reg, "w", encoding="utf-8") as fh:
            fh.write(REG)
        os.chmod(reg, 0o000)
    else:
        raise SystemExit("unknown case " + case)
    return root, fleet, lane


CASES = ["missing", "directory", "broken_symlink", "symlink_in_lane", "symlink_out_of_lane", "unreadable"]

results = []
for case in CASES:
    root, fleet, lane = build(case)
    reg = os.path.join(lane, "corpus", "SOURCES.md")
    st = os.lstat(reg) if os.path.lexists(reg) else None
    kind = "absent" if st is None else ("dir" if os.path.isdir(reg) and not os.path.islink(reg)
                                       else ("symlink->" + (os.readlink(reg) if os.path.islink(reg) else "?")
                                             if os.path.islink(reg) else "file"))
    p = subprocess.run([sys.executable, "-B", TOOL, "--root", lane, "--fleet", fleet],
                       capture_output=True, timeout=300)
    out = (p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")).strip()
    results.append({"case": case, "registry_kind": kind, "exit": p.returncode, "output": out,
                    "root": root})
    print(f"=== {case}  (registry: {kind})")
    print(f"    exit={p.returncode}")
    for line in out.splitlines():
        print("    | " + line)
    shutil.rmtree(root, ignore_errors=True)

with open(os.path.join(SCRATCH, "results.json"), "w", encoding="utf-8") as fh:
    json.dump(results, fh, indent=2)
print("\nwrote results.json")
