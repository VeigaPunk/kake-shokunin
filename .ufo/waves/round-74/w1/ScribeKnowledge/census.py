#!/usr/bin/env python3
"""Independent 2026-11-03 read-only census of corpus/knowledge/freshness-sidecar.json
at a named revision, using os.stat only (present / absent / unevaluable).

Recomputes exactly the fields the C2 base control prints, so the scribe's census
sentence rests on a receipt it ran itself. Writes nothing but stdout.
"""
import json
import os
import subprocess
import sys
from collections import Counter, OrderedDict

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = sys.argv[1] if len(sys.argv) > 1 else "ced2878a1e77f57afb4ee3baebf1021e5130399b"
SAMPLE = 6


def expand(token: str) -> str:
    if token == "~" or token.startswith("~/"):
        return os.path.join(os.environ["HOME"], token[2:] if token != "~" else "")
    return token


def classify(token: str) -> str:
    try:
        os.stat(expand(token))
        return "present"
    except (FileNotFoundError, NotADirectoryError):
        return "absent"
    except OSError:
        return "unevaluable"


raw = subprocess.run(
    ["git", "-C", LANE, "show", f"{REV}:corpus/knowledge/freshness-sidecar.json"],
    check=True, capture_output=True,
).stdout
entries = json.loads(raw)["entries"]
kinds = Counter(e["kind"] for e in entries)

counts = Counter()
per_token = OrderedDict()
samples = []
for e in entries:
    verdict = classify(e["token"])
    counts[(e["kind"], verdict)] += 1
    per_token.setdefault(e["token"], Counter())[(e["kind"], verdict)] += 1
    if e["kind"] == "absent" and verdict != "absent" and len(samples) < SAMPLE:
        samples.append((e["file"], e["line"], e["token"], e["kind"], verdict))

absent_present = counts[("absent", "present")]
absent_absent = counts[("absent", "absent")]
absent_unev = counts[("absent", "unevaluable")]
restored_present = counts[("restored", "present")]
restored_absent = counts[("restored", "absent")]
restored_unev = counts[("restored", "unevaluable")]
met = absent_present == 0 and restored_absent == 0 and absent_unev == 0 and restored_unev == 0

print(f"C2v1 revision={REV} entries={len(entries)} "
      f"absent={kinds['absent']} restored={kinds['restored']}")
print(f"absent_present={absent_present} absent_absent={absent_absent} "
      f"absent_unevaluable={absent_unev}")
print(f"restored_present={restored_present} restored_absent={restored_absent} "
      f"restored_unevaluable={restored_unev}")
print(f"contradictions={absent_present + restored_absent} met={str(met).lower()}")
for s in samples:
    print(f"sample {s!r}")

genuinely = [(t, c[("absent", "absent")]) for t, c in per_token.items()
             if c[("absent", "absent")]]
print(f"genuinely_absent_tokens= {len(genuinely)}")
for t, n in genuinely:
    print(f"absent_token {t} entries {n}")
