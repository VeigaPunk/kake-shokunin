import importlib.util, os, shutil, subprocess, sys
S="/fast/scratch/hyaku/kake-r59/MutResolverSelftest"
W=S+"/work/kcand"; shutil.rmtree(W,ignore_errors=True); os.makedirs(W+"/tmp")
SRC="/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py"
def load(p,n):
    sp=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
def w(p,t):
    os.makedirs(os.path.dirname(p),exist_ok=True); open(p,"w",newline="").write(t)
def git(p,*a):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git","-C",p,*a],capture_output=True,env=env)
REG="# Sources\n## Registry\n\n| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
ROW="| {sid} | https://e.example/{sid} | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n"
mod=load(SRC,"pristine")

def K8():
    d=W+"/k8"; lane=d+"/demo-shokunin"
    w(lane+"/corpus/SOURCES.md", REG+ROW.format(sid="S001")+"<!--\n"+ROW.format(sid="S900")+"-->\n")
    w(lane+"/corpus/knowledge/a.md","Cites S001 and S900.\n")
    r=mod.evaluate(lane,fleet=d)
    mod._check(r.summary==(2,1,1,0,1), f"summary={r.summary} (want 2 cited, 1 dangling)")
def K9():
    d=W+"/k9"; lane=d+"/demo-shokunin"
    w(lane+"/corpus/SOURCES.md", REG+ROW.format(sid="S001")+"\nSubsection\n---\n\n"+ROW.format(sid="S900"))
    w(lane+"/corpus/knowledge/a.md","Cites S001 and S900.\n")
    r=mod.evaluate(lane,fleet=d)
    mod._check(r.summary==(2,1,1,0,1), f"summary={r.summary} (setext H2 ends the section)")
def K10():
    d=W+"/k10"; lane=d+"/demo-shokunin"
    w(lane+"/corpus/SOURCES.md", REG+ROW.format(sid="S001"))
    w(lane+"/corpus/knowledge/ok.md","Cites S001.\n")
    w(lane+"/notes_store/hidden.md","Cites S900.\n")
    os.symlink("../../notes_store", lane+"/corpus/knowledge/linked")
    r=mod.evaluate(lane,fleet=d)
    mod._check(r.summary==(2,1,1,0,1), f"summary={r.summary} (in-lane symlinked dir is read)")
def K12():
    d=W+"/k12"; lane=d+"/demo-shokunin"
    w(d+"/outside/SOURCES.md", REG+ROW.format(sid="S001")+ROW.format(sid="S900"))
    w(lane+"/corpus/knowledge/ok.md","Cites S001 and S900.\n")
    os.makedirs(lane+"/corpus",exist_ok=True)
    os.symlink(d+"/outside/SOURCES.md", lane+"/corpus/SOURCES.md")
    r=mod.evaluate(lane,fleet=d)
    mod._check(r.status==2, f"status={r.status} (registry symlinked out of the lane must be unevaluable)")
def K14():
    d=W+"/k14"; anc=d+"/anc"
    w(anc+"/corpus/SOURCES.md", REG+ROW.format(sid="S001")+ROW.format(sid="S900"))
    w(anc+"/corpus/knowledge/ok.md","Cites S001 and S900.\n")
    w(anc+"/lane/corpus/SOURCES.md", REG+ROW.format(sid="S001"))
    w(anc+"/lane/corpus/knowledge/ok.md","Cites S001 and S900.\n")
    git(anc,"init","-q"); git(anc,"add","-A")
    git(anc,"-c","user.name=selftest","-c","user.email=selftest@local","-c","commit.gpgsign=false","commit","-q","-m","f")
    head=git(anc,"rev-parse","HEAD").stdout.decode().strip()
    r=mod.evaluate(anc+"/lane",revision=head,fleet=d)
    mod._check(r.status==2, f"status={r.status} (a --root below the toplevel is unevaluable)")
for name,fn in (("K8",K8),("K9",K9),("K10",K10),("K12",K12),("K14",K14)):
    try: fn()
    except Exception as e: print(f"{name}: RED on the current tool -> {type(e).__name__}: {e}")
    else: print(f"{name}: GREEN on the current tool (route already closed)")
