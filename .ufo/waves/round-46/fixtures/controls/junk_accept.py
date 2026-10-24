#!/usr/bin/env python3
"""Junk-accepting C1 control: claims a clean pass on any manifest, including
junk manifests a real audit must refuse with exit 2 (could-not-evaluate).

Deliberately skips all claimed work. The sealed counter must reject it.
"""
from __future__ import annotations

import sys

REPORT = ('{"version":1,"verdict":"clean","checksEvaluated":0,"findings":[]}')


def main() -> int:
    _ = sys.argv[1:]
    print(REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
