#!/usr/bin/env python3
"""Compare the round-30 re-run receipts against the committed round-29 receipts.

Compares only committed bytes (clone at the lane revision) with the bytes
produced by the round-30 re-run in this sandbox. Writes a JSON diff to stdout.
"""
from __future__ import annotations

import json
import os
import sys

CLONE = "/fast/scratch/hyaku/kake-r30/w1/ExecR29Receipts/clone"
SANDBOX = "/fast/scratch/hyaku/kake-r30/w1/ExecR29Receipts"
R29 = os.path.join(CLONE, ".ufo/waves/round-29")
NEW = os.path.join(SANDBOX, "out/round-30/r29-rerun")


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    diff = {"selftest": {}, "realInput": {}}

    old_self = load(os.path.join(R29, "verification/selftest-lane-final.json"))
    new_self = load(os.path.join(NEW, "selftest.stdout.json"))
    keys = ("selftest", "verdict", "cases", "passed", "failed", "passedOverTotal", "failures")
    for key in keys:
        diff["selftest"][key] = {"old": old_self.get(key), "new": new_self.get(key),
                                 "equal": old_self.get(key) == new_self.get(key)}
    diff["selftest"]["caseNames"] = {
        "old": old_self.get("caseNames"),
        "new": new_self.get("caseNames"),
        "equal": old_self.get("caseNames") == new_self.get("caseNames"),
        "onlyInOld": sorted(set(old_self.get("caseNames") or []) - set(new_self.get("caseNames") or [])),
        "onlyInNew": sorted(set(new_self.get("caseNames") or []) - set(old_self.get("caseNames") or [])),
    }
    diff["selftest"]["toolPath"] = {"old": old_self.get("tool"), "new": new_self.get("tool")}
    diff["selftest"]["fixturesPath"] = {"old": old_self.get("fixtures"), "new": new_self.get("fixtures")}

    old_sum = load(os.path.join(R29, "real-input/out/summary.json"))
    new_sum = load(os.path.join(NEW, "real-input/summary.json"))
    diff["realInput"]["totals"] = {"old": old_sum.get("totals"), "new": new_sum.get("totals"),
                                   "equal": old_sum.get("totals") == new_sum.get("totals")}
    diff["realInput"]["contractProblems"] = {"old": old_sum.get("contractProblems"),
                                             "new": new_sum.get("contractProblems"),
                                             "equal": old_sum.get("contractProblems") == new_sum.get("contractProblems")}
    old_sites = {s["site"]: s for s in old_sum.get("sites") or []}
    new_sites = {s["site"]: s for s in new_sum.get("sites") or []}
    per_site = {}
    for site in sorted(set(old_sites) | set(new_sites)):
        o = old_sites.get(site)
        n = new_sites.get(site)
        old_file = load(os.path.join(R29, f"real-input/out/{site}.json"))
        new_file = load(os.path.join(NEW, f"real-input/{site}.json"))
        entry = {
            "rowEqual": o == n,
            "oldRow": o,
            "newRow": n,
            "resultObjectEqual": old_file.get("result") == new_file.get("result"),
            "exitEqual": old_file.get("exit") == new_file.get("exit"),
            "stdoutEqual": old_file.get("stdout") == new_file.get("stdout"),
            "stderrEqual": old_file.get("stderr") == new_file.get("stderr"),
            "oldToolArgv": old_file.get("argv"),
            "newToolArgv": new_file.get("argv"),
            "oldFindings": (old_file.get("result") or {}).get("findings"),
            "newFindings": (new_file.get("result") or {}).get("findings"),
        }
        per_site[site] = entry
    diff["realInput"]["perSite"] = per_site

    # Which fields in the committed receipts carry no revision / tool digest?
    def missing_provenance(doc):
        text = json.dumps(doc)
        return {
            "hasRevisionKey": "revision" in text or "commit" in text,
            "hasSha256Key": "sha256" in text or "Sha256" in text,
            "hasPythonVersionKey": "python" in text.lower(),
        }

    diff["provenance"] = {
        "committedSelftestReceipt": missing_provenance(old_self),
        "committedRealInputSummary": missing_provenance(old_sum),
        "committedRealInputSiteFiles": {s: missing_provenance(load(os.path.join(R29, f"real-input/out/{s}.json")))
                                        for s in sorted(old_sites)},
        "newSelftestReceipt": missing_provenance(new_self),
        "newRealInputSummary": missing_provenance(new_sum),
    }
    json.dump(diff, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
