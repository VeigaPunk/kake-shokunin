#!/usr/bin/env python3
"""Round-59 attempt-2 residual handoff a2r1: re-dispatch of the abandoned r1 wave (2/8 seats spawned, both killed in the
orchestrator session exit 2026-10-26 23:57:36 -03; no reports). Same eight reviewer/critic items against the same committed
build ab6e100e; only the wave name, the report directory and one context sentence change. The spent r1.ready is never re-taken."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
src = json.load(open(os.path.join(HERE, "r1-dispatch.json")))
tc = src["taskCall"]
NOTE = ("Round-59 kake residual handoff a2r1 (attempt 2 of the round; re-dispatch of the abandoned r1 wave, whose seats were killed "
        "unreported in an orchestrator session exit; 8 reviewer/critic seats; attack the committed build "
        "ab6e100e442046006fa039315f5bd33bb516940b before the claims are measured).")
OLD = ("Round-59 kake residual handoff r1 (8 reviewer/critic seats; attack the committed build "
       "ab6e100e442046006fa039315f5bd33bb516940b before the claims are measured).")
assert tc["context"].count(OLD) == 1
ctx = tc["context"].replace(OLD, NOTE).replace(".ufo/waves/round-59/r1/", ".ufo/waves/round-59/a2r1/")
assert ".ufo/waves/round-59/r1/" not in ctx
tasks = []
for t in tc["tasks"]:
    body = t["task"].replace(".ufo/waves/round-59/r1/", ".ufo/waves/round-59/a2r1/")
    assert ".ufo/waves/round-59/r1/" not in body
    tasks.append({"name": t["name"], "agent": t["agent"], "task": body})
out = {"schema": "kake-r59-residual-dispatch-v1", "wave": "a2r1",
       "policy": "residual (<= 8 reviewer/critic seats; prompt §6 item 2); attempt-2 re-dispatch of abandoned r1",
       "counts": {"spawn": len(tasks), "resume": 0, "total": len(tasks)}, "taskCall": {"context": ctx, "tasks": tasks}}
json.dump(out, open(os.path.join(HERE, "a2r1-dispatch.json"), "w"), indent=1, ensure_ascii=False)
print(len(tasks), sorted({t["agent"] for t in tasks}))
