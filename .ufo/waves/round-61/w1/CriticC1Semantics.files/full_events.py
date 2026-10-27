import subprocess, re
LANE="/home/vgpnk/Projects/shokunin/kake-shokunin"
BASE="9f07731a873585e655a6518233ea39f5d9fb8204"
GRAM=re.compile(r"(?im)^\s*#\s*receipt\s*:|EXIT=|^VERDICT:")
SPAN=re.compile(r"(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|cases_passed|findings\s*=|scores_held|members\s*=)")
def blob_at(rev,path):
    r=subprocess.run(["git","-C",LANE,"show",f"{rev}:{path}"],capture_output=True,text=True)
    return r.stdout if r.returncode==0 else None
def span(txt): return sorted(set(l for l in txt.splitlines() if SPAN.search(l)))
pops=open(f"{LANE}/.ufo/waves/round-61/controls/population-144.txt").read().split()
allev=[]
for p in pops:
    # full first-parent history of the path up to BASE
    r=subprocess.run(["git","-C",LANE,"log","--first-parent","--format=%H",BASE,"--",p],capture_output=True,text=True)
    cs=r.stdout.split()  # newest first
    if not cs: continue
    add=cs[-1]
    v0=blob_at(add,p)
    if v0 is None or not GRAM.search(v0):
        continue  # not a receipt by first-version grammar
    prev=span(v0); prevc=add
    for c in reversed(cs[:-1]):
        cur=blob_at(c,p)
        par=subprocess.run(["git","-C",LANE,"rev-parse",f"{c}^"],capture_output=True,text=True).stdout.strip()
        pav=blob_at(par,p)
        if pav==cur:  # blob unchanged vs first parent -> not a candidate
            continue
        if cur is None:
            allev.append((p,c,"DELETE")); prev=None; continue
        cs_=span(cur)
        if cs_!=prev:
            allev.append((p,c,"rewrite"))
        prev=cs_
for p,c,k in allev:
    subj=subprocess.run(["git","-C",LANE,"show","-s","--format=%s",c],capture_output=True,text=True).stdout.strip()
    print(f"{k:9} {p} {c[:9]} {subj[:90]}")
print("TOTAL EVENTS:",len(allev))
