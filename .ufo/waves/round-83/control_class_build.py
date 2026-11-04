#!/usr/bin/env python3
"""Build the round-83 C2 control tree: the real pair plus an identical control pair.

Copies the measured capture trees, the declaration, the tool and the record
into <work>, then builds `<work>/.ufo/waves/round-83/capture-control/{a,b}`
from the round-81 capture in both branches. The classifier must read
`control_ok=0` because the control pair cannot flip the verdict.

Usage: control_class_build.py --lane <lane> --work <dir>
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

NEEDED = (
    ".ufo/waves/round-81/capture",
    ".ufo/waves/round-82/capture",
    ".ufo/waves/round-81/capture-expectations.json",
    ".ufo/waves/round-83/controls/after-c2-classes.txt",
    "scripts/header_change_class.py",
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lane", required=True)
    parser.add_argument("--work", required=True)
    args = parser.parse_args(argv)
    lane, work = Path(args.lane), Path(args.work)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for rel in NEEDED:
        source = lane / rel
        if not source.exists():
            print(f"fault: missing {source}", file=sys.stderr)
            return 2
        target = work / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
    for branch in ("a", "b"):
        shutil.copytree(lane / ".ufo/waves/round-81/capture",
                        work / ".ufo/waves/round-83/capture-control" / branch)
    print(f"control tree at {work}: control pair identical (round-81 capture twice)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
