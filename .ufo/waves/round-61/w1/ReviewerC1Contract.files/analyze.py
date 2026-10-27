import re, subprocess, json
LANE="/home/vgpnk/Projects/shokunin/kake-shokunin"
BASE="9f07731a873585e655a6518233ea39f5d9fb8204"
paths=[l.strip() for l in open(f"{LANE}/.ufo/waves/round-61/controls/population-144.txt") if l.strip()]
g_receipt=re.compile(r"(?im)^\s*#\s*receipt\s*:")
g_exit=re.compile(r"(?im)EXIT\s*=")
g_verdict=re.compile(r"(?im)^VERDICT:")
# contract detection forms: line matching ^#receipt: OR EXIT= OR ^VERDICT:
span=re.compile(r"(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|cases_passed|findings\s*=|scores_held|members\s*=)")
stats={"grammar":0,"no_grammar":0,"no_span":0,"files":[]}
nogram=[]; nospan=[]
firstcommit_beforebase=0; firstcommit_at_or_after=0
for p in paths:
    # blob at base
    r=subprocess.run(["git","-C",LANE,"show",f"{BASE}:{p}"],capture_output=True)
    if r.returncode!=0:
        stats["files"].append((p,"MISSING-AT-BASE")); continue
    body=r.stdout.decode("utf-8","replace")
    lines=body.splitlines()
    is_receipt=any(g_receipt.search(l) or g_exit.search(l) or g_verdict.search(l) for l in lines)
    if is_receipt: stats["grammar"]+=1
    else:
        stats["no_grammar"]+=1; nogram.append(p)
    spanlines=[l for l in lines if span.search(l)]
    if not spanlines:
        stats["no_span"]+=1; nospan.append(p)
    # first commit touching path (full history)
    r2=subprocess.run(["git","-C",LANE,"log","--reverse","--format=%H","--",p],capture_output=True,text=True)
    first=r2.stdout.splitlines()[0] if r2.stdout.splitlines() else None
    # is first commit an ancestor of base (i.e., file predates base)?
    if first:
        r3=subprocess.run(["git","-C",LANE,"merge-base","--is-ancestor",first,BASE])
        if r3.returncode==0: firstcommit_beforebase+=1
        else: firstcommit_at_or_after+=1
stats["first_before_base"]=firstcommit_beforebase
stats["first_at_or_after_base"]=firstcommit_at_or_after
print(json.dumps({k:v for k,v in stats.items() if k!="files"},indent=1))
print("NO-GRAMMAR (not receipts under the rule):")
for p in nogram: print("  ",p)
print("NO-SPAN (receipts with empty result span at base):")
for p in nospan: print("  ",p)
