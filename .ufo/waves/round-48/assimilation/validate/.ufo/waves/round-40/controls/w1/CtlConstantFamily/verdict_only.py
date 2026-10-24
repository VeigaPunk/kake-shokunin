#!/usr/bin/env python3
"""CONTROL: verdict-and-exit only, no checks array (junk document shape).

Runs no audit: prints {"version":1,"verdict":...,"checks":[]} with exit 0.
Skips all three declared repairs and the per-check report.
"""
import json
import sys


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return 64
    sys.stdout.write(json.dumps({"version": 1, "verdict": "clean", "checks": []}) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
