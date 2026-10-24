#!/usr/bin/env python3
"""Constant C1 control: prints a fixed clean report and exits 0 for any input.

Deliberately skips all claimed work (no rules read, no checks evaluated).
The sealed counter must reject it.
"""
from __future__ import annotations

import sys

REPORT = ('{"version":1,"verdict":"clean","checksEvaluated":1,"findings":[]}')


def main() -> int:
    _ = sys.argv[1:]
    print(REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
