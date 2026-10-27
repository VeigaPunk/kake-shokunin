import os, shutil, subprocess, sys
SEAT="/fast/scratch/hyaku/kake-r59/ExecResolverOtherRoutes"
WORK=os.path.join(SEAT,"work11"); TOOL=os.path.join(SEAT,"tool","id_resolver.py")
CENSUS="/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
HDR=("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
     "|---|---|---|---|---|---|---|---|---|---|---|\n")
def row(sid,url="https://e.example/x"):
    return f"| {sid} | fixture source — {url} | docs | A | scope | anchor | teaches | mined | 2026-10-26 | 90d | corpus/knowledge/ok.md |\n"
def build(case, registry, kb):
    root=os.path.join(WORK,case); shutil.rmtree(root,ignore_errors=True)
    fleet=os.path.join(root,"fleet"); lane=os.path.join(fleet,"kake-shokunin")
    os.makedirs(os.path.join(lane,"corpus","knowledge"),exist_ok=True)
    open(os.path.join(lane,"corpus","SOURCES.md"),"wb").write(registry.encode())
    open(os.path.join(lane,"corpus","knowledge","ok.md"),"wb").write(kb.encode())
    return fleet,lane
def run(tool,lane,fleet):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}; env["LC_ALL"]="C.UTF-8"
    p=subprocess.run([sys.executable,"-B",tool,"--root",lane,"--fleet",fleet],capture_output=True,env=env,timeout=300)
    return p.returncode,(p.stdout+p.stderr).decode("utf-8","replace").strip()
def census(lane):
    env=dict(os.environ); env["LC_ALL"]="C.UTF-8"
    c=subprocess.run([CENSUS,"census","--root",lane,lane],capture_output=True,env=env,timeout=300)
    v=subprocess.run([CENSUS,"validate","--today","2026-10-26",lane],capture_output=True,env=env,timeout=300)
    rows=[l.split("\t")[2] for l in c.stdout.decode().splitlines() if l.split("\t")[1:2]==["rows"]]
    return (rows[0] if rows else None), v.returncode, [l for l in v.stdout.decode().splitlines() if "\tE" in l]
CH={"U+2028":chr(0x2028),"U+2029":chr(0x2029),"U+000C":chr(0x0c),"U+000B":chr(0x0b),"U+0085":chr(0x85)}
for name,ch in CH.items():
    sid="S"+"8"+str(list(CH).index(name)+1).zfill(2)
    reg="# Sources\n\n## Registry\n\n"+HDR+row(sid).replace(f"| {sid} |", f"|{ch}| {sid} |")
    kb=f"Cites {sid}.\n"
    fleet,lane=build("L_"+name.replace("+",""),reg,kb)
    cr,ce,cf=census(lane); rc,out=run(TOOL,lane,fleet)
    print("="*70); print("split char",name,"id",sid)
    print("  registry hex:", reg.encode()[40:120].hex())
    print("  census rows:",cr,"validate exit:",ce,cf)
    print("  resolver exit:",rc)
    for l in out.splitlines(): print("   |",l)
