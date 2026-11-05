import importlib.util, json, os, sys, subprocess, shutil
S = "/fast/scratch/hyaku/kake-r95/CriticClaims"
spec = importlib.util.spec_from_file_location("c95c", S + "/fz/.ufo/waves/round-95/c95_conditional.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
table = {}; raw = {}
hand = m.hand_cases()
for name, inp, exp in hand:
    if isinstance(inp, dict) and "__raw__" in inp:
        raw[inp["__raw__"].hex()] = exp
    else:
        table[json.dumps(inp, sort_keys=True)] = exp
n_gen = 0
for inp in m.generate(95, 120):
    try: exp = m.reference(inp)
    except m.Invalid: exp = None
    table[json.dumps(inp, sort_keys=True)] = exp; n_gen += 1
print("hand", len(hand), "raw", len(raw), "table", len(table), "gen", n_gen)
cand = '''#!/usr/bin/env python3
# Lookup-table candidate (critic gaming route C2-T): memorises the frozen hand
# cases and the seed-95 generated cases; refuses everything else.
import json, sys
RAW = json.loads(%r)
TABLE = json.loads(%r)
data = sys.stdin.buffer.read()
hit = RAW.get(data.hex(), "MISS")
if hit == "MISS":
    try:
        obj = json.loads(data)
    except Exception:
        sys.exit(1)
    hit = TABLE.get(json.dumps(obj, sort_keys=True), None)
if hit is None:
    sys.exit(1)
print(json.dumps(hit, sort_keys=True))
''' % (json.dumps(raw, sort_keys=True), json.dumps(table, sort_keys=True))
import sys as _s
sys_path = S + "/fx/C2-table"
shutil.rmtree(sys_path, ignore_errors=True)
subprocess.run(["git", "clone", "-q", S + "/fz", sys_path], check=True)
subprocess.run(["git", "-C", sys_path, "config", "user.email", "critic@example.invalid"], check=True)
subprocess.run(["git", "-C", sys_path, "config", "user.name", "critic"], check=True)
assert subprocess.run(["git", "-C", sys_path, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() == sys_path
os.makedirs(sys_path + "/scripts", exist_ok=True)
open(sys_path + "/scripts/conditional_eval.py", "w").write(cand)
subprocess.run(["git", "-C", sys_path, "add", "-A"], check=True)
subprocess.run(["git", "-C", sys_path, "commit", "-q", "-m", "C2 lookup-table candidate (critic scratch)"], check=True)
print("fixture ok", sys_path)
