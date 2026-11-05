#!/usr/bin/env python3
"""Critic re-derivation: per-mutant hand/generated kill under v1 and v2 counters.
Mutants are the frozen round-93 patch list applied to its own base (pos-good.py),
which is the only base the find strings match. Counters are imported read-only."""
import importlib.util, json, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.dont_write_bytecode = True
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
S = "/fast/scratch/hyaku/kake-r94/CriticClaims/kill"
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
v1 = load("c93v1", LANE + "/.ufo/waves/round-93/c93_conditional.py")
v2 = load("c94v2", LANE + "/.ufo/waves/round-94/c94_conditional.py")
pos = open(LANE + "/.ufo/waves/round-93/frozen/pos-good.py").read()
spec = json.load(open(LANE + "/.ufo/waves/round-93/w1/recovered-partial/MutConditional/mutants-posgood.json"))
sandbox = os.path.join(S, "sandbox.py"); open(sandbox, "w").write(v2.SANDBOX)
cases1 = v1.hand_cases(); cases2 = v2.hand_cases()
gen = []
for inp in v2.generate(93, 120):
    try: gen.append((inp, v2.reference(inp)))
    except v2.Invalid: pass
print("cases v1=%d v2=%d gen=%d" % (len(cases1), len(cases2), len(gen)))
assert v1.reference_selfcheck(cases1) is None and v2.reference_selfcheck(cases2) is None
def build(m):
    if pos.count(m["find"]) != 1: return None
    return pos.replace(m["find"], m["replace"], 1)
def score(args):
    m, src, tag, cases, counter = args
    d = os.path.join(S, "w", tag, m["id"]); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "subject.py"); open(p, "w").write(src)
    h, g, fails = counter.score_subject(d, p, cases, gen, sandbox)
    first = fails[0].split(":")[0] if fails else ""
    allnames = [f.split(":")[0] for f in fails if not f.startswith("generated")]
    return {"id": m["id"], "clause": m["clause"], "tag": tag, "hand": h, "hand_total": len(cases),
            "gen": g, "gen_total": len(gen), "killed": bool(fails), "first_failing_case": first,
            "first_failure_line": fails[0][:260] if fails else "", "all_hand_failing": allnames}
jobs = []
for m in spec["mutants"]:
    src = build(m)
    assert src is not None, m["id"]
    jobs.append((m, src, "v1", cases1, v1)); jobs.append((m, src, "v2", cases2, v2))
with ThreadPoolExecutor(max_workers=8) as ex:
    res = list(ex.map(score, jobs))
out = {"population_base": "pos-good.py", "v1_cases": len(cases1), "v2_cases": len(cases2), "gen": len(gen), "rows": res}
json.dump(out, open(os.path.join(S, "kill-table.json"), "w"), indent=1, sort_keys=True)
byid = {}
for r in res: byid.setdefault(r["id"], {})[r["tag"]] = r
for mid in sorted(byid):
    a, b = byid[mid]["v1"], byid[mid]["v2"]
    print("%s v1=%s(%d/%d) v2=%s(%d/%d) v2_first=%s" % (mid, "K" if a["killed"] else "S", a["hand"], a["hand_total"],
          "K" if b["killed"] else "S", b["hand"], b["hand_total"], b["first_failing_case"]))
print("v1 killed", sum(byid[m]["v1"]["killed"] for m in byid), "v2 killed", sum(byid[m]["v2"]["killed"] for m in byid))
