import os, shutil, subprocess, sys
SCRATCH="/fast/scratch/hyaku/kake-r59/SentinelResolver"
WORK=os.path.join(SCRATCH,"work15")
HDR="| id | name | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
def put(base, rel, text):
    p=os.path.join(base, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p,"w",encoding="utf-8",newline="").write(text)
def run(tool, root, fleet=None, rev=None, timeout=15):
    argv=[sys.executable,"-B",tool,"--root",root]
    if fleet: argv+=["--fleet",fleet]
    if rev: argv+=["--revision",rev]
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"]="C.UTF-8"
    try:
        p=subprocess.run(argv,capture_output=True,env=env,timeout=timeout)
        return p.returncode,(p.stdout.decode()+p.stderr.decode()).strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT",""
def git(path,*a): return subprocess.run(["git","-C",path,*a],capture_output=True)
def commit_all(path):
    git(path,"init","-q"); git(path,"add","-A")
    r=git(path,"-c","user.name=selftest","-c","user.email=selftest@local","-c","commit.gpgsign=false","commit","-q","-m","f")
    assert r.returncode==0, r.stderr
    return git(path,"rev-parse","HEAD").stdout.decode().strip()
def main():
    shutil.rmtree(WORK,ignore_errors=True); os.makedirs(WORK)
    base=os.path.join(WORK,"inlane"); fleet=os.path.join(base,"fleet"); lp=os.path.join(fleet,"kake-shokunin")
    put(lp,"corpus/SOURCES.md","## Registry\n\n"+HDR+"| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(base,"elsewhere/knowledge/ok.md","Cites S100 and S1500.\n")
    os.makedirs(os.path.join(lp,"corpus"), exist_ok=True)
    os.symlink(os.path.join(base,"elsewhere","knowledge"), os.path.join(lp,"corpus","knowledge"))
    for tool,label in ((os.path.join(SCRATCH,"id_resolver_base.py"),"base"),(os.path.join(SCRATCH,"cand4.py"),"cand4")):
        rc,out=run(tool,lp,fleet)
        print(f"### corpus/knowledge is a symlink to an IN-LANE dir [{label}] exit={rc}")
        for l in out.splitlines()[:4]: print("  |",l)
        print()
    # corpus/ itself a symlink to an in-lane dir
    base=os.path.join(WORK,"inlane2"); fleet=os.path.join(base,"fleet"); lp=os.path.join(fleet,"kake-shokunin")
    put(base,"elsewhere/corpus/SOURCES.md","## Registry\n\n"+HDR+"| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(base,"elsewhere/corpus/knowledge/ok.md","Cites S100.\n")
    os.makedirs(lp, exist_ok=True)
    os.symlink(os.path.join(base,"elsewhere","corpus"), os.path.join(lp,"corpus"))
    for tool,label in ((os.path.join(SCRATCH,"id_resolver_base.py"),"base"),(os.path.join(SCRATCH,"cand4.py"),"cand4")):
        rc,out=run(tool,lp,fleet)
        print(f"### corpus/ is a symlink to an IN-LANE dir [{label}] exit={rc}")
        for l in out.splitlines()[:4]: print("  |",l)
        print()
main()
