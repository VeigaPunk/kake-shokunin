#!/usr/bin/env python3
"""Tool-absent fixture: class-wide false runs with an absent-tool note."""
import argparse
import hashlib
import json
import os
import shutil
import sys

PREDICATE = (
    "met: the tool's exit code and output equal the round-41 tool's on every generated "
    "run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the "
    "five timing shapes is at most 2.0 times the round-40 tool's"
)
CLASS_MODULES = (
    ("G1", "g1_longport_grammar.py"),
    ("G2", "g2_default_port.py"),
    ("G3", "g3_empty_path.py"),
    ("G4", "g4_port_scope.py"),
    ("G5", "g5_prefix_cut_45plus.py"),
    ("G6", "g6_fold_pairs.py"),
    ("G7", "g7_band_memos.py"),
    ("G8", "g8_host_tables.py"),
    ("G9", "g9_port_digits.py"),
    ("G10", "g10_headtail_windows.py"),
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--classes", choices=("v4", "v5"), required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tool-file")
    ap.add_argument("--revision")
    ap.add_argument("--label", default="")
    args = ap.parse_args()

    fixture = os.path.dirname(os.path.abspath(__file__))
    if args.revision:
        shutil.copyfile(os.path.join(fixture, "build-receipt.json"), args.out)
        raise SystemExit(0)

    with open(os.path.join(fixture, "control-template.json")) as fh:
        receipt = json.load(fh)
    receipt["counterSha256"] = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    receipt["toolFile"] = args.tool_file
    receipt["toolSha256"] = None
    receipt["met"] = False
    receipt["equalRuns"] = "0/21"
    receipt["equalValues"] = 0
    receipt["note"] = "tool absent"
    receipt["ratios"] = {"T1": None, "T2": None, "T3": None, "T4": None, "T5": None}
    receipt["ratiosExact"] = {}
    for entry in receipt["runs"].values():
        entry["equal"] = False
        entry["candExit"] = "tool absent"
        entry.pop("candOutSha256", None)
        if "candCpu" in entry:
            entry["candCpu"] = []
            entry["candRepsEqual"] = "0/5"
    with open(args.out, "w") as fh:
        json.dump(receipt, fh, indent=1)
        fh.write("\n")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
