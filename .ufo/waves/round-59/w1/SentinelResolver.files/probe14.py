import os, shutil, subprocess, sys, threading, time
SCRATCH="/fast/scratch/hyaku/kake-r59/SentinelResolver"
WORK=os.path.join(SCRATCH,"work14")
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
def main():
    shutil.rmtree(WORK,ignore_errors=True); os.makedirs(WORK)
    for tool,label in ((os.path.join(SCRATCH,"cand4.py"),"candidate cand4"),
                       (os.path.join(SCRATCH,"id_resolver_base.py"),"base")):
        # FIFO
        base=os.path.join(WORK,"fifo_"+label.split()[0]); fleet=os.path.join(base,"fleet")
        lp=os.path.join(fleet,"kake-shokunin")
        put(lp,"corpus/SOURCES.md","## Registry\n\n"+HDR+"| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
        put(lp,"corpus/knowledge/ok.md","Cites S100.\n")
        os.mkfifo(os.path.join(lp,"corpus","knowledge","pipe.md"))
        rc,out=run(tool,lp,fleet,timeout=12)
        print(f"### FIFO in corpus/knowledge [{label}] exit={rc}")
        for l in out.splitlines()[:3]: print("  |",l)
        print()
    # race against candidate
    base=os.path.join(WORK,"race"); fleet=os.path.join(base,"fleet"); lp=os.path.join(fleet,"kake-shokunin")
    put(lp,"corpus/SOURCES.md","## Registry\n\n"+HDR+"| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp,"corpus/knowledge/ok.md","Cites S100.\n")
    for i in range(200): put(lp,f"corpus/knowledge/f{i:03d}.md","Cites S100.\n"*20)
    outdir=os.path.join(base,"outside"); put(outdir,"outside.md","Cites S1400.\n")
    inside_t=os.path.join(lp,"corpus","knowledge","ok.md"); outside_t=os.path.join(outdir,"outside.md")
    link=os.path.join(lp,"corpus","knowledge","race.md"); os.symlink(inside_t,link)
    stop=threading.Event()
    def flip():
        while not stop.is_set():
            for tgt in (inside_t,outside_t):
                tmp=link+".tmp"
                try:
                    if os.path.lexists(tmp): os.unlink(tmp)
                    os.symlink(tgt,tmp); os.replace(tmp,link)
                except OSError: pass
    t=threading.Thread(target=flip,daemon=True); t.start()
    leaks=0; runs=60
    for _ in range(runs):
        rc,out=run(os.path.join(SCRATCH,"cand4.py"),lp,fleet,timeout=30)
        if "S1400" in out: leaks+=1
    stop.set(); t.join(timeout=2)
    print(f"### TOCTOU race against candidate cand4: runs={runs} runs_leaking_outside_id={leaks}")
main()
