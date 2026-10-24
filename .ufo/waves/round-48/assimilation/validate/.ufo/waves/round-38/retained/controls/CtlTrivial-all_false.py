#!/usr/bin/env python3
"""Round-38 C1 pre-freeze control: all-false.

Parses the manifest with plain `json.loads`, implements no contract rule at all, and
reports every check against its stated expectation: `expect` allow -> one `blocked`
finding, `expect` disallow -> one `exposed` finding. Always verdict `failed-policy`,
exit 1. Skips every rule of (a)-(k): no status handling, no fault handling, no rule
reading, no URL validation. Expected 4 of 20 (the round-37 all-false score shape:
cases whose every check expects a finding and whose manifest is valid).
"""
from __future__ import annotations

import json
import sys

EXIT_USAGE = 64


def load_checks(path: str) -> list:
    try:
        with open(path, "rb") as handle:
            data = json.loads(handle.read().decode("utf-8"))
    except Exception:
        return []
    if not isinstance(data, dict) or not isinstance(data.get("checks"), list):
        return []
    return data["checks"]


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--manifest":
        sys.stderr.write("usage: robots_audit.py --manifest PATH\n")
        return EXIT_USAGE
    checks = load_checks(argv[1])
    findings = []
    for check in checks:
        if not isinstance(check, dict):
            continue
        expected = check.get("expect")
        if expected == "allow":
            reason = "blocked"
        elif expected == "disallow":
            reason = "exposed"
        else:
            continue
        raw_id = check.get("id")
        cid = raw_id if isinstance(raw_id, str) and raw_id else None
        findings.append({"check": cid, "reason": reason})
    report = {
        "version": 1,
        "verdict": "failed-policy",
        "checksEvaluated": len(checks),
        "findings": findings,
    }
    sys.stdout.write(json.dumps(report, separators=(",", ":")) + "\n")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
