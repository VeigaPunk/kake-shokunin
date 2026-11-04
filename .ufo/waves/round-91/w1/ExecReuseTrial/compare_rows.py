#!/usr/bin/env python3
"""ExecReuseTrial (kake r91 w1): cross-check tool results against the frozen
counter's own reference() over the same recorded-data inputs.

Loads .ufo/waves/round-91/c91_reuse.py as a module (frozen bytes, unmodified),
computes reference(inp) for every converted input at both `now` values, and
compares against results.json produced by run_rows.py. A disagreement between
the shipped tool and the counter's reference on real recorded data is reported
as a FINDING row; it changes nothing in this seat's files.
"""

import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTER = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-91/c91_reuse.py"
AGED = 2592000

spec = importlib.util.spec_from_file_location("c91_reuse", COUNTER)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    idx = json.load(open(os.path.join(HERE, "inputs", "index.json")))
    results = {r["input"]: r for r in json.load(open(os.path.join(HERE, "results.json")))}
    agree = disagree = refused_expected = 0
    rows = []
    for entry in idx["rows"]:
        case = json.load(open(os.path.join(HERE, "inputs", entry["input"])))
        res = results[entry["input"]]
        for tag, delta in (("capture_time", 0), ("aged_30d", AGED)):
            c = dict(case)
            c["now"] = entry["now_primary"] + delta
            try:
                ref = mod.reference(c)
                kind = "value"
            except mod.Invalid as exc:
                ref, kind = "invalid_input: %s" % exc, "refusal"
            got = res[tag]
            if kind == "refusal":
                refused_expected += 1
                ok = (got["rc"] != 0 and got.get("stderr", "").startswith("invalid_input:"))
            else:
                ok = (got["rc"] == 0 and got.get("decision") == ref["decision"]
                      and got.get("freshness_lifetime") == ref["freshness_lifetime"]
                      and got.get("current_age") == ref["current_age"])
            if ok:
                agree += 1
            else:
                disagree += 1
                rows.append({"input": entry["input"], "pass": tag,
                             "reference": ref, "tool": got})
    print("compare: agree=%d disagree=%d reference-refusals=%d" % (agree, disagree, refused_expected))
    for row in rows:
        print("DISAGREE", row)
    with open(os.path.join(HERE, "compare.json"), "w") as fh:
        json.dump({"agree": agree, "disagree": disagree, "rows": rows}, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
