#!/usr/bin/env python3
"""Stale-planted fixture: kill this process without writing a receipt."""
import argparse
import os
import signal

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
    ap.parse_args()
    os.kill(os.getpid(), signal.SIGKILL)


if __name__ == "__main__":
    main()
