#!/usr/bin/env python3
"""Run every generated mutant through the bounded detector and compare with pristine.

Kill criterion: the mutant's observable result differs from the pristine result on
at least one fixture variant. The observed unit is
(variant -> exit code, per-check state, per-check notes); notes are compared
because several checks keep a failing state for a *different* legitimate reason
and the mutation only removes one diagnostic line.
"""
import json
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/kake-r59/MutC3Counter"
PRISTINE = f"{S}/pristine.py"


def run(path):
    out = subprocess.run([sys.executable, "-B", f"{S}/detect.py", path],
                         capture_output=True, text=True, cwd=S)
    if out.returncode != 0:
        return None, out.stderr
    with open(f"{S}/digests/{os.path.basename(path)}.json", encoding="utf-8") as fh:
        return json.load(fh), out.stdout


def diff(pristine, mutant):
    """Return the list of (variant, check, what) differences."""
    diffs = []
    for variant, pv in pristine["variants"].items():
        mv = mutant["variants"].get(variant)
        if mv is None:
            diffs.append((variant, "-", "variant missing"))
            continue
        if pv["exit"] != mv["exit"]:
            diffs.append((variant, "exit", f"{pv['exit']} -> {mv['exit']}"))
        for check in sorted(set(pv["checks"]) | set(mv["checks"])):
            ps = pv["checks"].get(check)
            ms = mv["checks"].get(check)
            if ps is None or ms is None:
                diffs.append((variant, check, "check missing"))
                continue
            if ps[0] != ms[0]:
                diffs.append((variant, check, f"state {ps[0]} -> {ms[0]}"))
            elif ps[1] != ms[1]:
                gone = [n for n in ps[1] if n not in ms[1]]
                new = [n for n in ms[1] if n not in ps[1]]
                diffs.append((variant, check,
                              f"notes -{len(gone)} +{len(new)}: " + (gone[0][:110] if gone else new[0][:110])))
    return diffs


def main():
    made = json.load(open(f"{S}/mutants.json", encoding="utf-8"))
    meta = json.load(open(f"{S}/variants.json", encoding="utf-8"))
    pristine, _ = run(PRISTINE)
    results = []
    for m in made:
        d, err = run(m["path"])
        if d is None:
            results.append({"id": m["id"], "desc": m["desc"], "verdict": "ERROR", "detail": err[-400:]})
            continue
        diffs = diff(pristine, d)
        results.append({"id": m["id"], "desc": m["desc"],
                        "verdict": "KILLED" if diffs else "SURVIVED",
                        "diffs": [list(x) for x in diffs],
                        "variants": d["variants"]})
    json.dump({"fixtures": meta, "results": results}, open(f"{S}/matrix.json", "w", encoding="utf-8"), indent=1)

    for r in results:
        tag = r["verdict"]
        if tag == "KILLED":
            first = r["diffs"][0]
            print(f"{r['id']:26s} KILLED  by {len(r['diffs'])} fixture/check delta(s); first: "
                  f"{first[0]}/{first[1]}: {first[2]}")
        elif tag == "SURVIVED":
            print(f"{r['id']:26s} SURVIVED")
        else:
            print(f"{r['id']:26s} ERROR {r.get('detail','')[:120]}")
    killed = sum(1 for r in results if r["verdict"] == "KILLED")
    print(f"\n{killed}/{len(results)} killed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
