#!/usr/bin/env python3
"""CriticClaims fixture mutation runner.

Executes the decoy gate `integration/gate-copy.py` in this fixture. It never reads,
imports or mutates `scripts/cache_key_conformance.py` -- the gate whose digest the
receipt first line names. The point of the fixture: the frozen C1 counter's item A
binds the receipt digest to that gate but lets the runner choose its own target, so
a real execution log over a different gate satisfies the item.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DECOY = os.path.join(HERE, "gate-copy.py")
INPUT = {"a": 2, "b": 3}
EXPECTED = "174\n"

MUTANTS = {
    "M01": ('data["a"]', 'data["a"] + 1'),
    "M02": ('data["b"]', 'data["b"] - 1'),
    "M03": ("total += 1  # K03", "total += 2  # K03"),
    "M04": ("total *= 2  # K04", "total *= 3  # K04"),
    "M05": ("total -= 3  # K05", "total -= 4  # K05"),
    "M06": ("total += 4  # K06", "total += 5  # K06"),
    "M07": ("total += 5  # K07", "total += 6  # K07"),
    "M08": ("total += 6  # K08", "total += 7  # K08"),
    "M09": ("total += 7  # K09", "total += 8  # K09"),
    "M10": ("total += 8  # K10", "total += 9  # K10"),
    "M11": ("total += 9  # K11", "total += 10  # K11"),
    "M12": ("total += 10  # K12", "total += 11  # K12"),
    "M13": ("total += 11  # K13", "total += 12  # K13"),
    "M14": ("total += 12  # K14", "total += 13  # K14"),
    "M15": ("total += 13  # K15", "total += 14  # K15"),
    "M16": ("total += 14  # K16", "total += 15  # K16"),
    "M17": ("total += 15  # K17", "total += 16  # K17"),
    "M18": ("total += 16  # K18", "total += 17  # K18"),
    "M19": ("total += 17  # K19", "total += 18  # K19"),
    "M20": ("total += 18  # K20", "total += 19  # K20"),
    "M21": ("# K01", "# K01 comment-only"),
}


def observed(path):
    p = subprocess.run([sys.executable, "-B", path], input=json.dumps(INPUT).encode(),
                       capture_output=True, timeout=60)
    if p.returncode != 0 or p.stdout.decode("utf-8", "replace") != EXPECTED:
        return ("killed", 1)
    return ("survived", 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", required=True)
    a = ap.parse_args()
    if a.mutant == "base":
        verdict = observed(DECOY)
    else:
        old, new = MUTANTS[a.mutant]
        with open(DECOY) as fh:
            src = fh.read()
        if old not in src:
            sys.stderr.write("mutant %s: pattern absent\n" % a.mutant)
            return 2
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "gate.py")
            with open(path, "w") as fh:
                fh.write(src.replace(old, new, 1))
            verdict = observed(path)
    print("verdict=%s rc=%d" % verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
