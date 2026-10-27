import importlib.util, os, shutil, subprocess, sys
S="/fast/scratch/hyaku/kake-r59/MutResolverSelftest"; W=S+"/work/c39"
shutil.rmtree(W,ignore_errors=True); os.makedirs(W)
def load(p,n):
    sp=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
REG="# Sources\n## Registry\n\n| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
def w(p,t):
    os.makedirs(os.path.dirname(p),exist_ok=True); open(p,"w",newline="").write(t)
def case(mod):
    d=os.path.join(W,"k10_"+os.urandom(4).hex()); lane=os.path.join(d,"demo-shokunin")
    w(lane+"/corpus/SOURCES.md", REG+"| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    w(lane+"/corpus/knowledge/ok.md","Cites S001.\n")
    w(lane+"/notes_store/hidden.md","Cites S900.\n")
    os.symlink("../../notes_store", os.path.join(lane,"corpus/knowledge/linked"))
    r=mod.evaluate(lane, fleet=d)
    mod._check(r.summary==(2,1,1,0,1), f"summary={r.summary}")
for lbl,p in (("pristine","/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py"),
              ("M39", S+"/work/M39.py")):
    m=load(p, "m_"+lbl)
    try: case(m)
    except Exception as e: print(f"{lbl}: FAIL {type(e).__name__}: {e}")
    else: print(f"{lbl}: PASS")
