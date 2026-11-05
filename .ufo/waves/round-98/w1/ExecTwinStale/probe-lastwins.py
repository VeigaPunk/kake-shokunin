import sys, json, base64, subprocess
sys.set_int_max_str_digits(0)
ORACLE="/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-98/frozen/pos-oracle.py"
SEAT="/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-98/w1/ExecTwinStale"
TWIN=SEAT+"/twin.py"
PROBE="probe_lastwins_twin.py"
def cls(p):
    if p.returncode==0:
        o=json.loads(p.stdout.decode())
        return ("decided",o["decision"],o["staleness"])
    if p.returncode==1 and p.stderr.startswith(b"invalid_input:"): return ("refused",)
    return ("other",p.returncode)
def run(script, raw):
    return subprocess.run([sys.executable,script],input=raw,capture_output=True,cwd=".")
runs=[(SEAT+"/diff-run.txt", "inputs-main.jsonl"),("s1/diff-run.txt","s1/inputs.jsonl"),("s2/diff-run.txt","s2/inputs.jsonl"),("s3/diff-run.txt","s3/inputs.jsonl")]
total=0; bad=[]; kinds={}
for diffpath, inpath in runs:
    labels=set(l.split(" | ")[0].strip() for l in open(diffpath) if "| DISAGREE" in l)
    rows={}
    for line in open(inpath):
        r=json.loads(line)
        if r["label"] in labels: rows[r["label"]]=base64.b64decode(r["b64"])
    for lab,raw in rows.items():
        total+=1
        t=cls(run(TWIN,raw)); p=cls(run(PROBE,raw)); o=cls(run(ORACLE,raw))
        dup = b"duplicate key" in run(TWIN,raw).stderr
        if p==o:
            k = "dup-key-only(twin refuses, probe last-wins == oracle)" if dup else "int-limit/other: probe==oracle, twin decided"
            kinds[k]=kinds.get(k,0)+1
        else:
            bad.append((diffpath,lab,"twin",t,"probe",p,"oracle",o,raw[:200]))
print("disagreeing inputs (main+s1-3) re-run:", total)
for k,v in kinds.items(): print("  ",v,k)
print("UNEXPLAINED (probe != oracle):", len(bad))
for b in bad: print("  ", b)
