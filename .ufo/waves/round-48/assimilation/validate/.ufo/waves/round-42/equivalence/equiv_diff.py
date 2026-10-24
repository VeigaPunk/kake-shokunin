#!/usr/bin/env python3
"""Round-42 frozen equivalence differential (SCORECARD "Round 42 — C1 counter candidate"): a meeting tool
is a control iff a witness value is shown on which its `_parse_url` differs from the round-41 tool's.
Values: counter v3 runs A-E at seeds 42101-42103, plus targeted port/host/percent values.
Usage: equiv_diff.py <tool.py> [<tool.py> ...]   (prints JSON; exit 0)"""
import importlib.util, json, random, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
def load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
C = load("c42v3", os.path.join(HERE, "..", "c42_count_v3.py"))
ref = load("tip41", "/fast/scratch/hyaku/kake-r42/shared/tip41.py")
vals = []
for seed in (42101, 42102, 42103):
    rng = random.Random(seed)
    for gen in (C.cases_a, C.cases_b, C.cases_c, C.cases_d, C.cases_e):
        vals += [c["value"] for c in gen(rng)]
for p in ["", "0", "8a", "a", "%41", "%", "80%", "65535", "65536", "99999", "-1", "+1", " 1", "\u0661", "08", "0x50"]:
    for h in ["a.example", "", "[::1]", "%41", "a%2"]:
        for s in ("http", "https", "hTtP"):
            vals += [f"{s}://{h}:{p}/x", f"{s}://u@{h}:{p}", f"{s}://{h}{':' if p else ''}{p}?q#f"]
vals += ["http://", "http:///x", "http://@/x", "http://:80/x", "http://u@:80", "http://[]/", "http://.", "http://%20/"]
out = {"values": len(vals), "tools": {}}
for path in sys.argv[1:]:
    m = load("cand", path)
    diffs = []
    for v in vals:
        a, b = ref._parse_url(v), m._parse_url(v)
        if a != b:
            diffs.append({"value": v, "tip41": a, "tool": b})
    out["tools"][path] = {"differences": len(diffs), "witnesses": diffs[:5]}
print(json.dumps(out, ensure_ascii=True, indent=1, default=str))
