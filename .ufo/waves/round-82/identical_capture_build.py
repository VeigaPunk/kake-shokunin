#!/usr/bin/env python3
"""Build the round-82 C2 identical-capture control root.

identical_capture_build.py --lane <lane> --out DIR

Copies the declaration and the round-81 capture tree into DIR, copies the
drift tool, and materialises the round-82 capture as a byte-identical copy of
the round-81 tree. No record is written. A counter run over DIR must read
`met=false`: the round-82 instants are not strictly later than the round-81
instants and fall below the round-82 floor, and no committed record exists.
Exit 0 built, 2 bad input, 64 usage.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

DECLARATION = ".ufo/waves/round-81/capture-expectations.json"
BASE_CAPTURE = ".ufo/waves/round-81/capture"
ROUND_CAPTURE = ".ufo/waves/round-82/capture"
TOOL = "scripts/capture_delta.py"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lane", required=True)
    parser.add_argument("--out", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    lane = Path(args.lane).resolve()
    out = Path(args.out).resolve()
    for rel in (DECLARATION, BASE_CAPTURE, TOOL):
        if not (lane / rel).exists():
            print(f"error: missing {rel} under {lane}", file=sys.stderr)
            return 2
    if out.exists():
        shutil.rmtree(out)
    (out / DECLARATION).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(lane / DECLARATION, out / DECLARATION)
    shutil.copytree(lane / BASE_CAPTURE, out / BASE_CAPTURE)
    shutil.copytree(lane / BASE_CAPTURE, out / ROUND_CAPTURE)
    (out / TOOL).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(lane / TOOL, out / TOOL)
    print(f"built {out}")
    print(f"b_capture_is_copy_of={BASE_CAPTURE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
