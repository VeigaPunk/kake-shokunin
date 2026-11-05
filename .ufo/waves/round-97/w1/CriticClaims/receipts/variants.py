import importlib.util, json, re, sys, concurrent.futures as cf
sys.path.insert(0, "/fast/scratch/hyaku/kake-r97/CriticClaims")
from drive import *

spec = importlib.util.spec_from_file_location("c97i", W + "/c97_index.py")
c97i = importlib.util.module_from_spec(spec); spec.loader.exec_module(c97i)

cand = show("scripts/reval_exchange.py")
def rep(txt, a, b):
    assert txt.count(a) == 1, (a, txt.count(a))
    return txt.replace(a, b)

K = {
 "k1-5xx-enumerated": rep(cand, "    if 500 <= status <= 599:", "    if status in (500, 503, 599):"),
 "k2-etag-control-only": rep(cand, "    for ch in rest[1:-1]:\n        if ch not in ETAGC:", "    for ch in rest[1:-1]:\n        if ord(ch) < 0x20:"),
 "k3-bool-lastmod": rep(cand, "    return isinstance(v, int) and not isinstance(v, bool)", "    return isinstance(v, int)"),
 "k4-1xx-only-100": rep(cand, "        if status < 200:", "        if status == 100:"),
}
K["k5-all-four"] = K["k4-1xx-only-100"]
t = K["k5-all-four"]
t = rep(t, "    if 500 <= status <= 599:", "    if status in (500, 503, 599):")
t = rep(t, "    for ch in rest[1:-1]:\n        if ch not in ETAGC:", "    for ch in rest[1:-1]:\n        if ord(ch) < 0x20:")
t = rep(t, "    return isinstance(v, int) and not isinstance(v, bool)", "    return isinstance(v, int)")
K["k5-all-four"] = t

readme = show("corpus/README.md")
names = sorted(os.path.basename(l.split("\t")[1]) for l in sh(G, "-C", LANE, "ls-tree", REV, "corpus/knowledge/").splitlines() if l.endswith(".md"))
bodies = {n: show("corpus/knowledge/" + n) for n in names}
ids_all = set()
for n in names:
    ids_all |= c97i.source_ids(bodies[n])

# M1: one mega-row covering every entry (ids + 2 entry words each)
words_pick = []
for n in names:
    bw = sorted({w for w in c97i.words(bodies[n]) if len(w) >= 6}, key=lambda w: (-len(w), w))
    words_pick += bw[:2]
mega = ("\n\n## Coverage index — round 97 (critic M1)\n\n| Area | Entry | Coverage |\n|---|---|---|\n"
        "| Mega | " + " ".join("`knowledge/%s`" % n for n in names) + " | ids " + " ".join(sorted(ids_all)) +
        " entry words " + " ".join(sorted(set(words_pick))) + " |\n")

# M2: one row per entry copying the entry's first prose line (accurate by construction)
def first_prose(body):
    for line in body.splitlines():
        s = line.strip()
        if len(s.split()) >= 8 and not s.startswith(("#", "|", "-", "source", "verified", "recheck", "---", "```", "<")):
            return s[:300]
    return ""
rows = []
for n in names:
    ids = sorted(c97i.source_ids(bodies[n]))
    rows.append("| Scope copy | `knowledge/%s` (%s) | %s |" % (n, ", ".join(ids), first_prose(bodies[n]).replace("|", "/")))
copy_sec = "\n\n## Coverage index — round 97 (critic M2)\n\n| Area | Entry | Coverage |\n|---|---|---|\n" + "\n".join(rows) + "\n"

jobs = {}
for k, v in K.items():
    jobs["c2-" + k] = {"src": {"scripts/reval_exchange.py": v}, "script": W + "/c97_reval.py"}
jobs["c1-m1-megarow"] = {"src": {"corpus/README.md": readme + mega}, "script": W + "/c97_index.py"}
jobs["c1-m2-scopecopy"] = {"src": {"corpus/README.md": readme + copy_sec}, "script": W + "/c97_index.py"}
jobs["c2-tip-clean"] = {"src": {}, "script": W + "/c97_reval.py"}

def go(name):
    j = jobs[name]
    if j["src"]:
        D, rev = fixture(name, j["src"])
    else:
        D, rev = LANE, REV
    r = run_counter(j["script"], D, rev, name)
    r["fixture"] = D
    return r

res = []
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    for r in ex.map(go, list(jobs)):
        res.append(r)
        print(json.dumps(r, sort_keys=True), flush=True)
json.dump(res, open(S + "/variants-results.json", "w"), indent=1, sort_keys=True)
print("DONE", len(res))
