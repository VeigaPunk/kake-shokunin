#!/usr/bin/env python3
"""Materialise round-80's junk control tree from a JSON file map (round-81 R80-5).

Round-80 shipped `.ufo/waves/round-80/controls/ctl-c80-junk-queue.txt` as a run over
`/fast/scratch/hyaku/kake-r80/l1/junk`, a tree that was never committed and that no
builder recreated — which is exactly what R80-5 routed. This builder makes that
control re-runnable from lane bytes: `junk-tree.json` is the tree, this script
writes it, and `c81_defect_queue.py` re-runs round-80's own counter over it.

Paths are relative and must stay inside `--out`; nothing is read from the network
and nothing outside `--out` is written. Exit 0 wrote the tree, 2 bad spec,
64 usage.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    try:
        spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
        files = spec["files"]
    except (OSError, ValueError, KeyError) as exc:
        print(f"bad spec: {exc}", file=sys.stderr)
        return 2
    if not isinstance(files, dict) or not files:
        print("bad spec: files must be a non-empty object", file=sys.stderr)
        return 2
    out = Path(a.out)
    for rel, body in files.items():
        if not isinstance(rel, str) or not isinstance(body, str):
            print(f"bad spec entry: {rel!r}", file=sys.stderr)
            return 2
        parts = Path(rel).parts
        if rel.startswith("/") or ".." in parts or not parts:
            print(f"unsafe path: {rel}", file=sys.stderr)
            return 2
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(body, encoding="utf-8")
    print(f"wrote {len(files)} files to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
