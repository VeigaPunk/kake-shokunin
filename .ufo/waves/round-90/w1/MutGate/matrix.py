#!/usr/bin/env python3
"""Subject x case pass/fail matrix for the pristine gate (MutGate survivor analysis)."""
import concurrent.futures as cf, importlib.util, json, os, random, subprocess, sys, tarfile, io

S = "/fast/scratch/hyaku/kake-r90/MutGate"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = "7f6c68f10fbf4caca3912d6e23fa6eed6413857d"
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 16906240
sys.dont_write_bytecode = True


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


tree = os.path.join(S, "mtree")
os.makedirs(tree, exist_ok=True)
ctr = load("c90_gate", LANE + "/.ufo/waves/round-90/c90_gate.py")
paths = [p for p in ctr.subject_paths() if p != "scripts/cache_key.py"] + [".ufo/waves/round-89/c89_key.py", "scripts/cache_key_conformance.py"]
t = subprocess.run(["git", "-C", LANE, "archive", "--format=tar", REV, "--", *paths], capture_output=True, check=True).stdout
tarfile.open(fileobj=io.BytesIO(t)).extractall(tree, filter="data")
os.makedirs(tree + "/base-candidate", exist_ok=True)
open(tree + "/base-candidate/cache_key.py", "wb").write(
    subprocess.run(["git", "-C", LANE, "show", ctr.BASE + ":scripts/cache_key.py"], capture_output=True, check=True).stdout)
g = load("gate", tree + "/scripts/cache_key_conformance.py")
assert g.self_check()
rng = random.Random(SEED)
gen = []
for i in range(120):
    obj = g.gen_case(rng)
    gen.append(("generated", "g%03d" % i, json.dumps(obj).encode(), g.reference(obj)))
cases = g.hand_cases() + gen + g.advisory_cases()
sand = os.path.join(S, "msandbox.py"); open(sand, "w").write(g.SANDBOX)
cwd = os.path.join(S, "mcwd"); os.makedirs(cwd, exist_ok=True)
subj = {}
for p in ctr.subject_paths():
    subj[p] = tree + "/base-candidate/cache_key.py" if p == "scripts/cache_key.py" else os.path.join(tree, p)
jobs = [(p, i) for p in subj for i in range(len(cases))]


def run(j):
    p, i = j
    r = g.run_candidate(sys.executable, sand, subj[p], cases[i][2], cwd)
    ok, why = g.judge(r, cases[i][3])
    return p, i, ok, r[0] if r[0] in ("violation", "timeout") else (r[0], (r[2] or b"")[:60].decode("utf-8", "replace")), why[:160]


with cf.ThreadPoolExecutor(12) as ex:
    res = list(ex.map(run, jobs))
out = {"seed": SEED, "cases": [[c[0], c[1]] for c in cases], "fail": {}}
for p, i, ok, rc, why in res:
    if not ok:
        out["fail"].setdefault(p, []).append([i, str(rc), why])
json.dump(out, open(os.path.join(S, "matrix-%d.json" % SEED), "w"), indent=0)
print("done", len(res))
