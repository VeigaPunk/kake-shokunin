import re, subprocess
LANE="/home/vgpnk/Projects/shokunin/kake-shokunin"
paths=[l.strip() for l in open(f"{LANE}/.ufo/waves/round-61/controls/population-144.txt") if l.strip()]
span=re.compile(r"(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|cases_passed|findings\s*=|scores_held|members\s*=)")
g_receipt=re.compile(r"(?im)^\s*#\s*receipt\s*:")
g_exit=re.compile(r"(?im)EXIT\s*=")
g_verdict=re.compile(r"(?im)^VERDICT:")
tot_sp=tot_nsp=0; low=[]
for p in paths:
    r2=subprocess.run(["git","-C",LANE,"log","--reverse","--format=%H","--",p],capture_output=True,text=True)
    fl=r2.stdout.splitlines()
    if not fl: continue
    r=subprocess.run(["git","-C",LANE,"show",f"{fl[0]}:{p}"],capture_output=True)
    body=r.stdout.decode("utf-8","replace")
    lines=[l for l in body.splitlines() if l.strip()]
    if not any(g_receipt.search(l) or g_exit.search(l) or g_verdict.search(l) for l in lines): continue
    sp=[l for l in lines if span.search(l)]
    nsp=[l for l in lines if not span.search(l)]
    tot_sp+=len(sp); tot_nsp+=len(nsp)
    if len(sp)<=2 and len(nsp)>=3:
        low.append((p,len(sp),len(nsp)))
print(f"receipts analysed: span lines={tot_sp} non-span lines={tot_nsp}")
print(f"receipts with thin span (<=2 span lines, >=3 non-span): {len(low)}")
for p,s,n in low: print(f"  {s}/{s+n} {p}")
