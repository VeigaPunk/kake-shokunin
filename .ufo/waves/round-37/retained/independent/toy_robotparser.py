#!/usr/bin/env python3
"""A toy robots audit built on the Python standard library `urllib.robotparser`.

It exists only to show that the round-37 selftest can fail: it does whatever the stock parser
does (no 512000-byte limit, no BOM handling, Unicode line splitting, `str.splitlines`, no
percent-normalization, no query/fragment rule of its own, substring user-agent matching, no
manifest validation beyond JSON parsing) and it uses argparse, so `--help` exits 0 instead of
the contract's 64.
"""

import argparse
import json
import os
import sys
from urllib.robotparser import RobotFileParser


def main(argv):
    parser = argparse.ArgumentParser(prog="robots_audit.py")
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args(argv)
    try:
        with open(args.manifest, encoding="utf-8") as handle:
            document = json.load(handle)
    except Exception:
        print(json.dumps({"version": 1, "verdict": "could-not-evaluate",
                          "checksEvaluated": 0,
                          "findings": [{"check": None, "reason": "input_invalid"}]}))
        return 2
    base = os.path.dirname(os.path.abspath(args.manifest))
    findings = []
    evaluated = 0
    for check in document.get("checks", []):
        status = check.get("robotsStatus")
        if not isinstance(status, int) or status < 200 or status > 599:
            findings.append({"check": check.get("id"), "reason": "check_invalid"})
            continue
        if 400 <= status <= 499:
            allowed = True
        elif 500 <= status <= 599:
            allowed = False
        else:
            robots_path = os.path.join(base, check.get("robots", "robots.txt"))
            parser_obj = RobotFileParser()
            try:
                with open(robots_path, encoding="utf-8", errors="replace") as handle:
                    parser_obj.parse(handle.readlines())
            except OSError:
                findings.append({"check": check.get("id"), "reason": "check_invalid"})
                continue
            allowed = parser_obj.can_fetch(check.get("userAgent", ""), check["url"])
        evaluated += 1
        expect = check.get("expect")
        if expect == "allow" and not allowed:
            findings.append({"check": check.get("id"), "reason": "blocked"})
        elif expect == "disallow" and allowed:
            findings.append({"check": check.get("id"), "reason": "exposed"})
    reasons = {item["reason"] for item in findings}
    if "input_invalid" in reasons or "check_invalid" in reasons:
        verdict, code = "could-not-evaluate", 2
    elif findings:
        verdict, code = "failed-policy", 1
    else:
        verdict, code = "clean", 0
    print(json.dumps({"version": 1, "verdict": verdict, "checksEvaluated": evaluated,
                      "findings": findings}))
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
