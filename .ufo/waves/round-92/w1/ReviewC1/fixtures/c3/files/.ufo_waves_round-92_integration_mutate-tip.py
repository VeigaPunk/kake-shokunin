#!/usr/bin/env python3
"""FIXTURE runner (ReviewC1 r92 class 3): mutates nothing.

Prints a canned verdict per --mutant target; base always survives, every
mutant is always killed. No gate byte is ever changed.
"""
import sys


def main(argv):
    target = "base"
    if "--mutant" in argv:
        target = argv[argv.index("--mutant") + 1]
    if target == "base":
        print("verdict=survived rc=0")
        return 0
    print("verdict=killed rc=1")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
