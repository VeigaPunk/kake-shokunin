import importlib.util, itertools, json, sys
sys.dont_write_bytecode = True
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
S = "/fast/scratch/hyaku/kake-r94/CriticClaims/kill"
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
pos = open(LANE + "/.ufo/waves/round-93/frozen/pos-good.py").read()
spec = json.load(open(LANE + "/.ufo/waves/round-93/w1/recovered-partial/MutConditional/mutants-posgood.json"))
m11 = [m for m in spec["mutants"] if m["id"] == "M11"][0]
assert pos.count(m11["find"]) == 1
mut = pos.replace(m11["find"], m11["replace"], 1)
open(S + "/M11-subject.py", "w").write(mut)
A = load("posgood", LANE + "/.ufo/waves/round-93/frozen/pos-good.py")
B = load("m11", S + "/M11-subject.py")
def outcome(mod, payload):
    try: return ("ok", json.dumps(mod.decide(payload), sort_keys=True))
    except SystemExit as e: return ("exit", str(e.code))
    except Exception as e: return ("exc", type(e).__name__ + ":" + str(e)[:80])
n = 0; diff = []
tags = [None, '"a"', 'W/"a"']
for method, exists, etag, lm, ius, im, role, ims, inm in itertools.product(
        ["GET", "PUT", "POST", "HEAD"], [True, False], [None] + tags, [None, 0, 1, 600, 700],
        [None, 0, 600, 700], [None, "*", '"a"'], [None, "cache", "origin"], [None, 0, 900], [None, '"a"', "*"]):
    if not exists and (etag is not None or lm is not None): continue
    payload = {"method": method, "current": {"exists": exists, "etag": etag, "last_modified": lm},
               "request": {"if_match": im, "if_none_match": inm, "if_modified_since": ims, "if_unmodified_since": ius}}
    if role: payload["role"] = role
    n += 1
    a, b = outcome(A, payload), outcome(B, payload)
    if a != b and len(diff) < 5: diff.append((payload, a, b))
print("grid inputs", n, "differences", len(diff) if diff else 0)
for d in diff: print(d)
