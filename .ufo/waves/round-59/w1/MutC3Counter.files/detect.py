#!/usr/bin/env python3
"""Bounded behavioral detector for the round-59 C3 counter.

Runs the counter's own `run_checks` over the fixture variant set (scratch repo D)
and prints a deterministic digest: per variant, per check, (state, notes).

Usage: python3 -B detect.py <path-to-counter.py>
"""
import importlib.util
import json
import os
import sys

S = "/fast/scratch/hyaku/kake-r59/MutC3Counter"
D = f"{S}/D"


def load(path):
    spec = importlib.util.spec_from_file_location("counter_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def digest(counter_path):
    meta = json.load(open(f"{S}/variants.json", encoding="utf-8"))
    mod = load(counter_path)
    out = {"variants": {}, "bases": meta["bases"]}
    for name, spec in meta["variants"].items():
        code, results = mod.run_checks(D, spec["rev"], spec["base"])
        out["variants"][name] = {
            "exit": code,
            "passed": sum(1 for r in results if r["state"] == "pass"),
            "checks": {r["check"]: [r["state"], list(r["notes"])] for r in results},
        }
    return out


def summarise(d):
    lines = []
    for name, v in d["variants"].items():
        fails = sorted(k for k, (st, _) in v["checks"].items() if st != "pass")
        lines.append(f"{name}: exit={v['exit']} passed={v['passed']}/9 fail={','.join(fails) or '-'}")
    return "\n".join(lines)


if __name__ == "__main__":
    path = sys.argv[1]
    d = digest(path)
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        for name, v in d["variants"].items():
            print(f"== {name} exit={v['exit']} passed={v['passed']}")
            for check, (state, notes) in v["checks"].items():
                print(f"   {check:28s} {state}")
                for n in notes:
                    print(f"      - {n}")
    else:
        print(summarise(d))
    with open(os.path.join(S, "digests", os.path.basename(path) + ".json"), "w", encoding="utf-8") as fh:
        json.dump(d, fh, indent=1)
