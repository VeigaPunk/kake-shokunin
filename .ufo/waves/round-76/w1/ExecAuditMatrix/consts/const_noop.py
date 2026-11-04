#!/usr/bin/env python3
"""Degenerate constant 1/4: no-op reader.

Reads nothing, prints nothing, exits 0. A drop-in for the C2 tool CLI so the
case matrix can run it; its whole point is that a matrix which passes it is
not measuring anything.
"""

import sys


def main(argv=None):
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
