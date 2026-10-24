#!/usr/bin/env python3
"""Round-39 routing check (lesson round-39, mistake 3): a wave spec must not hand a code-writing or
code-running deliverable to a critic seat (the critic role forbids editing files and invoking runtimes).
Usage: route_check.py <wave-spec.json>   exit 0 clean, 1 misrouted items listed, 2 unreadable."""
import json
import re
import sys

CODE = re.compile(r"`[^`\s]*\.py`|runnable as|[Ss]elf-test it|python3 [^`]*--manifest")

try:
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    items = spec["items"]
except Exception as ex:
    print(f"cannot evaluate: {ex}")
    sys.exit(2)
bad = []
for it in items:
    if it.get("role") != "critic":
        continue
    acc = it["prompt"].split("# Acceptance", 1)[-1]
    if CODE.search(acc):
        bad.append(it["name"])
print(f"items {len(items)}; critic items with a code deliverable {len(bad)}")
for n in bad:
    print(f"MISROUTED {n}")
sys.exit(1 if bad else 0)
