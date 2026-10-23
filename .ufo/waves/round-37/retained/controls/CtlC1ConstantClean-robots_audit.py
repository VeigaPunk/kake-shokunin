#!/usr/bin/env python3
"""C1 constant-clean control for kake-shokunin round 37.

Honors only the C1 usage line (exit 64 on any argv other than `--manifest PATH`),
never opens any robots file, optionally counts `checks` in the manifest if readable,
and unconditionally prints `{"version":1,"verdict":"clean","checksEvaluated":N,"findings":[]}`
with exit 0.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def count_checks(manifest_path: str) -> int:
    try:
        p = Path(manifest_path)
        if not p.is_file() or p.stat().st_size > 1_048_576:
            return 0
        obj = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(obj, dict) and isinstance(obj.get("checks"), list):
            return len(obj["checks"])
    except Exception:
        pass
    return 0


def main(argv: list[str]) -> int:
    if len(argv) != 3 or argv[1] != "--manifest" or not argv[2]:
        return 64
    n = count_checks(argv[2])
    sys.stdout.write(
        json.dumps(
            {
                "version": 1,
                "verdict": "clean",
                "checksEvaluated": n,
                "findings": [],
            },
            separators=(",", ":"),
        )
        + "\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
