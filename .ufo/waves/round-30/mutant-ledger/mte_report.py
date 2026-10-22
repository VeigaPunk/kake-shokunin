#!/usr/bin/env python3
"""Build the MTE-shaped report for the base citing-set mutant ledger.

Reads /fast/scratch/hyaku/kake-r30/w1/MutBaseRunnerLedger/ledger.json (the
kake ledger) and the pristine base gate, and emits ledger.mte.json in the
mutation-testing-elements report shape used by
corpus/knowledge/mte-report-interop.md (tameshi, revision f4e8f7d8):

  schemaVersion "1", thresholds {high, low}, framework {name}, files{}
  with one file entry for scripts/citing_set.py carrying language "python",
  the pristine source bytes, and one mutant per reason code.

Status mapping (tameshi convention, per mte-report-interop.md):
  Killed   -> Killed    (the committed runner exited non-zero on the mutant)
  Survived -> Survived  (the committed runner exited zero on the mutant)

The report is then validated against the vendored official schema 3.9.0
(package/src/mutation-testing-report-schema.json, extracted from
tameshi-shokunin/tools/vendor/mutation-testing-report-schema-3.9.0.tgz).
"""
from __future__ import annotations

import json
import os
import sys

HERE = "/fast/scratch/hyaku/kake-r30/w1/MutBaseRunnerLedger"
LEDGER = os.path.join(HERE, "ledger.json")
BASE_GATE = os.path.join(HERE, "base", "scripts", "citing_set.py")
SCHEMA = os.path.join(HERE, "vendor", "package", "src", "mutation-testing-report-schema.json")
OUT = os.path.join(HERE, "ledger.mte.json")


def first_occurrence(source, needle):
    """Return (line, column) of the first occurrence of needle, 1-based."""
    index = source.find(needle)
    if index < 0:
        return None
    line = source.count("\n", 0, index) + 1
    column = index - (source.rfind("\n", 0, index) + 1) + 1
    return line, column


def main():
    with open(LEDGER, encoding="utf-8") as handle:
        ledger = json.load(handle)
    with open(BASE_GATE, encoding="utf-8") as handle:
        source = handle.read()

    mutants = []
    for row in ledger["rows"]:
        code = row["code"]
        needle = '"%s"' % code
        position = first_occurrence(source, needle)
        if position is None:
            raise SystemExit("no occurrence of %s in the pristine gate" % needle)
        line, column = position
        killed = row["status"] == "Killed"
        mutants.append({
            "id": "citing_set-reason-%s" % code,
            "mutatorName": "kake-reason-rename",
            "description": "rename every double-quoted occurrence of the reason code %s" % code,
            "replacement": '"%s" -> "%s_mutated"' % (code, code),
            "location": {
                "start": {"line": line, "column": column},
                "end": {"line": line, "column": column + len(needle)},
            },
            "status": "Killed" if killed else "Survived",
            "statusReason": row["statusReason"],
            "occurrencesRenamed": row["renamedOccurrences"],
            "observedByCommittedFixtures": row["observedByCommittedFixtures"],
            "probeOutputChanged": row["probeOutputChanged"],
        })

    report = {
        "schemaVersion": "1",
        "thresholds": {"high": 80, "low": 60},
        "framework": {"name": "kake citing-set committed runner (scripts/citing_set_selftest.py)"},
        "config": {
            "baseRevision": ledger["base"]["revision"],
            "lane": ledger["base"]["lane"],
            "detector": ledger["detector"],
            "mutation": ledger["mutation"],
        },
        "files": {
            "scripts/citing_set.py": {
                "language": "python",
                "source": source,
                "mutants": mutants,
            }
        },
    }
    with open(OUT, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=1)
        handle.write("\n")
    print("wrote %s with %d mutants" % (OUT, len(mutants)))

    # Validate against the vendored official schema 3.9.0.
    import jsonschema
    with open(SCHEMA, encoding="utf-8") as handle:
        schema = json.load(handle)
    jsonschema.Draft7Validator(schema).validate(report)
    print("schema 3.9.0 validation: OK")

    total = len(mutants)
    killed = sum(1 for m in mutants if m["status"] == "Killed")
    survived = total - killed
    print("official-style metrics: total=%d killed=%d survived=%d valid=%d score=%s" % (
        total, killed, survived, total,
        ("%.6f" % (100.0 * killed / total)) if total else "NaN"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
