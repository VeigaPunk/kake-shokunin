import os, shutil, subprocess, sys
S="/fast/scratch/hyaku/kake-r59/MutResolverSelftest"; W=S+"/work/final"
shutil.rmtree(W,ignore_errors=True); os.makedirs(W+"/tmp")
SRC="/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py"
REG="# Sources\n## Registry\n\n| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
ROW="| {sid} | https://e.example/{sid} | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n"
def w(p,t):
    os.makedirs(os.path.dirname(p),exist_ok=True); open(p,"w",newline="").write(t)
def run(tool,a):
    e=dict(os.environ); e["TMPDIR"]=W+"/tmp"
    p=subprocess.run([sys.executable,"-B",tool]+a,capture_output=True,env=e,cwd=W)
    return p.returncode,(p.stdout.decode()+p.stderr.decode()).strip().splitlines()[-1]
# K10 fixture: in-lane symlinked knowledge dir
d=W+"/k10"; lane=d+"/demo-shokunin"
w(lane+"/corpus/SOURCES.md", REG+ROW.format(sid="S001"))
w(lane+"/corpus/knowledge/ok.md","Cites S001.\n")
w(lane+"/notes_store/hidden.md","Cites S900.\n")
os.symlink("../../notes_store", lane+"/corpus/knowledge/linked")
print("K10 fixture (in-lane symlinked dir):")
for lbl,t in (("pristine",SRC),("M39 followlinks",S+"/work/M39.py"),("M13 dir-guard-dropped",S+"/work/M13.py"),("M40 compound",S+"/work/M40.py")):
    print(f"  {lbl:26s}", run(t,["--root",lane,"--fleet",d]))
# M13: knowledge dir symlinked OUT of the lane -> status only
d=W+"/m13"; lane=d+"/demo-shokunin"
w(lane+"/corpus/SOURCES.md", REG+ROW.format(sid="S001"))
w(d+"/outside/a.md","Cites S001 and S900.\n")
os.symlink(d+"/outside", lane+"/corpus/knowledge")
print("M13 fixture (knowledge dir symlinked OUT):")
for lbl,t in (("pristine",SRC),("M13",S+"/work/M13.py")):
    print(f"  {lbl:26s}", run(t,["--root",lane,"--fleet",d]))
