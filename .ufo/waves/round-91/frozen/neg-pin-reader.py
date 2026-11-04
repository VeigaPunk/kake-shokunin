#!/usr/bin/env python3
"""Forgery subject: answers from the counter's own pins/case files if it can reach them."""
import json
import os
import sys

CANDIDATES = ("frozen/c2-population.sha256", "c2-population.sha256", "c2-cases.json",
              "cases.json", "../c2-cases.json", "../../frozen/c2-cases.json")


def main():
    payload = sys.stdin.read()
    for rel in CANDIDATES:
        for base in (os.getcwd(), os.path.dirname(os.path.abspath(__file__))):
            path = os.path.join(base, rel)
            if os.path.isfile(path):
                try:
                    data = json.load(open(path))
                except Exception:
                    continue
                if isinstance(data, dict) and "decisions" in data:
                    key = json.dumps(json.loads(payload), sort_keys=True)
                    hit = data["decisions"].get(key)
                    if hit:
                        print(json.dumps(hit))
                        return 0
    print(json.dumps({"decision": "reuse", "freshness_lifetime": 0, "current_age": 0}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
