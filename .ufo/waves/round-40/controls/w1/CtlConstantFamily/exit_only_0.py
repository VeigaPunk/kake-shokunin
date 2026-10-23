#!/usr/bin/env python3
"""CONTROL: exit-code-only. Emits nothing on stdout.

Asks the manifest only whether it parses; returns exit 0 with empty stdout.
Skips all three declared repairs and the whole report shape.
"""
import sys


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return 64
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
