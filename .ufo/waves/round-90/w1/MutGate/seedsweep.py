import concurrent.futures as cf, importlib.util, json, os, random, sys
sys.dont_write_bytecode=True
S="/fast/scratch/hyaku/kake-r90/MutGate"; T=S+"/mtree/.ufo/waves/round-89/"
spec=importlib.util.spec_from_file_location("g",S+"/pristine_gate.py"); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
groups={"H01":["w1/MutKey/mutants/M37-absent-name-not-escaped.py"],
 "G03":["w1/ExecControls/adv-cr-only.py","w1/ExecControls/adv-space-trim.py","w1/MutKey/mutants/M07-value-ows-not-trimmed.py","w1/MutKey/mutants/M23-crlf-check-dropped.py","w1/MutKey/mutants/M24-lf-check-dropped.py"],
 "G04":["w1/ExecControls/adv-no-uri-escape.py","w1/MutKey/mutants/M12-escape-GS-dropped.py","w1/MutKey/mutants/M13-escape-FS-dropped.py","w1/MutKey/mutants/M31-uri-not-escaped.py"]}
seeds=list(range(1,41))
cases=[]
for sd in seeds:
    rng=random.Random(sd)
    for i in range(120):
        o=g.gen_case(rng); cases.append((sd,json.dumps(o).encode(),g.reference(o)))
sand=S+"/msandbox.py"; cwd=S+"/mcwd"
negs=sorted({n for v in groups.values() for n in v})
def run(j):
    n,(sd,pl,exp)=j
    return n,sd,g.judge(g.run_candidate(sys.executable,sand,T+n,pl,cwd),exp)[0]
killed={}
with cf.ThreadPoolExecutor(16) as ex:
    for n,sd,ok in ex.map(run,[(n,c) for n in negs for c in cases]):
        if not ok: killed.setdefault(n,set()).add(sd)
out={}
for m,ns in groups.items():
    surv=[sd for sd in seeds if all(sd in killed.get(n,set()) for n in ns)]
    out[m]={"seeds":len(seeds),"mutant_killed_at_seeds":len(seeds)-len(surv),"mutant_survives_at_seeds":len(surv),
            "per_negative_seeds_with_a_generated_kill":{n.split('/')[-1]:len(killed.get(n,set())) for n in ns}}
json.dump(out,open(S+"/seedsweep.json","w"),indent=1); print(json.dumps(out,indent=1))
