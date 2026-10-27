import re, subprocess, json
LANE="/home/vgpnk/Projects/shokunin/kake-shokunin"
paths=[l.strip() for l in open(f"{LANE}/.ufo/waves/round-61/controls/population-144.txt") if l.strip()]
span=re.compile(r"(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|cases_passed|findings\s*=|scores_held|members\s*=)")
g_receipt=re.compile(r"(?im)^\s*#\s*receipt\s*:")
g_exit=re.compile(r"(?im)EXIT\s*=")
g_verdict=re.compile(r"(?im)^VERDICT:")
def blob(commit,p):
    r=subprocess.run(["git","-C",LANE,"show",f"{commit}:{p}"],capture_output=True)
    return r.stdout.decode("utf-8","replace") if r.returncode==0 else None
def spanlines(body):
    return set(l for l in body.splitlines() if span.search(l))
events=[]
pending_events=[]
receipts=0
for p in paths:
    r2=subprocess.run(["git","-C",LANE,"log","--reverse","--format=%H","--",p],capture_output=True,text=True)
    commits=r2.stdout.splitlines()
    if not commits: continue
    first_body=blob(commits[0],p)
    if first_body is None: continue
    is_receipt=any(g_receipt.search(l) or g_exit.search(l) or g_verdict.search(l) for l in first_body.splitlines())
    if not is_receipt: continue
    receipts+=1
    first_has_pending = "pending" in first_body.lower()
    prev_span=spanlines(first_body)
    prev_commit=commits[0]
    for c in commits[1:]:
        b=blob(c,p)
        if b is None: continue
        s=spanlines(b)
        if s!=prev_span:
            kind="pending_filled" if (first_has_pending and "pending" not in b.lower()) else "rewrite"
            events.append((kind,p,c[:8]))
        elif first_has_pending and "pending" not in b.lower():
            pending_events.append(("pending_filled_nospandiff",p,c[:8]))
        prev_span=s; prev_commit=c
print("receipts(first-ever grammar):",receipts)
print("span-change events:",len(events))
for e in events: print("  ",e)
print("pending-lost-no-spandiff:",pending_events)
