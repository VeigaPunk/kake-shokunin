import importlib.util, json, os, sys, collections, hashlib, tempfile
FZ = "/fast/scratch/hyaku/kake-r95/CriticClaims/fz"
spec = importlib.util.spec_from_file_location("c95c", FZ + "/.ufo/waves/round-95/c95_conditional.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
cand = FZ + "/scripts/conditional_eval.py"
print("candidate sha256", hashlib.sha256(open(cand, "rb").read()).hexdigest())
work = tempfile.mkdtemp(prefix="attrib-", dir=os.environ["TMPDIR"])
sandbox = os.path.join(work, "sandbox.py"); open(sandbox, "w").write(m.SANDBOX)
gen = []
for inp in m.generate(95, 120):
    try: gen.append((inp, m.reference(inp)))
    except m.Invalid: pass
print("generated cases", len(gen))
def empty_member(v):
    if not isinstance(v, str): return False
    return any(t.strip() == "" for t in v.split(","))
def classify(inp):
    tags = set()
    req = inp["request"]
    if any(empty_member(req.get(k)) for k in ("if_match", "if_none_match")): tags.add("C1")
    if "\x80" in (inp["current"].get("etag") or ""): tags.add("C2")
    if inp["method"] not in ("GET", "HEAD") and (req.get("if_match") or req.get("if_none_match") or req.get("if_modified_since") is not None): tags.add("C5?")
    if "role" in inp and inp["role"] is None: tags.add("C3")
    return tags
cnt = collections.Counter(); unattributed = []; total_fail = 0
for inp, exp in gen:
    got, why = m.run_subject(work, cand, inp, sandbox)
    if got == exp: continue
    total_fail += 1
    t = classify(inp)
    if not t: unattributed.append((inp, exp, got, why))
    for x in t: cnt[x] += 1
    cnt["ALL:" + "+".join(sorted(t)) if t else "ALL:none"] += 1
print("generated failures", total_fail)
for k, v in sorted(cnt.items()): print(" ", k, v)
print("unattributed", len(unattributed))
for u in unattributed[:6]: print("  U", json.dumps(u[0], sort_keys=True)[:260], "exp", u[1], "got", u[2], u[3])
print("--- failures by method (C5 method-filter check)")
bym = collections.Counter(); bym_c5only = collections.Counter()
for inp, exp in gen:
    got, why = m.run_subject(work, cand, inp, sandbox)
    if got == exp: continue
    bym[inp["method"]] += 1
    t = classify(inp)
    if not (t & {"C1", "C2"}): bym_c5only[inp["method"]] += 1
print("all failures by method:", dict(bym))
print("failures with no C1/C2 tag, by method:", dict(bym_c5only))
