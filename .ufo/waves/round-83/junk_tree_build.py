#!/usr/bin/env python3
"""Build the round-83 junk control tree from junk-tree.json (C1 kill rule).

The tree carries one prose sentence per routed defect and nothing else. The
counter must read `open=6 closed=0 met=false`, exit 1.

Usage: junk_tree_build.py --root <dir> [--spec <json>]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", required=True)
    parser.add_argument("--spec", default=str(Path(__file__).with_name("junk-tree.json")))
    args = parser.parse_args(argv)
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    root = Path(args.root)
    lesson = root / spec["lesson"]
    lesson.parent.mkdir(parents=True, exist_ok=True)
    body = "\n".join(spec["prose"].format(item=item) for item in spec["items"])
    lesson.write_text("# Round 83 — lessons (junk control)\n\n" + body + "\n", encoding="utf-8")
    print(f"junk tree at {root}: {len(spec['items'])} prose claims, no state")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
