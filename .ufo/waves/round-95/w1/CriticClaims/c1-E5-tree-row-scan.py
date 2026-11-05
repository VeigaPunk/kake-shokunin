import re,subprocess,sys
REV="8f638b591e739e1863f5fa22334d5e15178189ed"
LANE="/home/vgpnk/Projects/shokunin/kake-shokunin"
PATH_RE = re.compile(r"`((?:scripts|corpus|\.ufo)/[^`\s]+)`")
def g(*a): return subprocess.run(["git","-C",LANE,*a],capture_output=True).stdout.decode().strip()
txt=g("show",REV+":SKILL.md").splitlines()
hits=[]
for i,l in enumerate(txt,1):
    if not l.startswith("|"): continue
    for m in PATH_RE.finditer(l):
        p=m.group(1)
        if "<" in p or "*" in p: continue
        p=re.sub(r":\d+(-\d+)?$","",p); p=re.sub(r"#.*$","",p)
        t=g("cat-file","-t",REV+":"+p.rstrip("/"))
        if t=="tree" or p.endswith("/"):
            hits.append((i,p,t or "missing"))
for h in hits: print(h)
print("tree-hits",len(hits),"distinct rows",len({h[0] for h in hits}))
