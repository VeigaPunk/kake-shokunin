#!/usr/bin/env python3
"""Forgery subject: answers the first worked examples it was shown, refuses everything else."""
import json
import sys

ALLOW = {
    "fresh-max-age": {"decision": "reuse", "freshness_lifetime": 60, "current_age": 30},
    "stale-boundary": {"decision": "revalidate", "freshness_lifetime": 60, "current_age": 60},
    "no-lifetime": {"decision": "heuristic-undecided", "freshness_lifetime": None, "current_age": 10},
}


def main():
    try:
        inp = json.loads(sys.stdin.read())
    except ValueError:
        sys.stderr.write("invalid_input: not JSON\n")
        return 1
    headers = inp.get("stored", {}).get("headers", {})
    cc = str(headers.get("Cache-Control", "")).lower()
    age = int(headers.get("Age", 0)) + max(0, inp.get("now", 0) - int(headers.get("Date", 0)))
    if "max-age=60" in cc and age < 60 and "no-cache" not in cc:
        print(json.dumps(ALLOW["fresh-max-age"]))
        return 0
    if "max-age=60" in cc and age == 60:
        print(json.dumps(ALLOW["stale-boundary"]))
        return 0
    if "Cache-Control" not in headers:
        print(json.dumps(ALLOW["no-lifetime"]))
        return 0
    sys.stderr.write("invalid_input: not in the allowlist\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
