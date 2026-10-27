import subprocess, re, os, json
"""Literal simulation of contract C1 rules for demo fixtures. NOT the lane tool."""
GRAM=re.compile(r"(?im)^\s*#\s*receipt\s*:|EXIT=|^VERDICT:")
SPAN=re.compile(r"(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|cases_passed|findings\s*=|scores_held|members\s*=)")
def blob(root,rev,path):
    r=subprocess.run(["git","-C",root,"show",f"{rev}:{path}"],capture_output=True,text=True)
    return r.stdout if r.returncode==0 else None
def span(txt): return set(l for l in txt.splitlines() if SPAN.search(l))
def scan(root, rev="HEAD", disclosures=None):
    # derive population = all committed files matching path rule at rev (fixture analog)
    files=subprocess.run(["git","-C",root,"ls-tree","-r",rev,"--name-only"],capture_output=True,text=True).stdout.split()
    pop=[p for p in files if re.search(r"\.ufo/waves/round-\d+/(?:.*/)?controls?/.*\.(txt|json)$",p)]
    findings=[]
    for p in pop:
        cs=subprocess.run(["git","-C",root,"log","--first-parent","--format=%H",rev,"--",p],capture_output=True,text=True).stdout.split()
        if not cs: continue
        add=cs[-1]; v0=blob(root,add,p)
        if v0 is None or not GRAM.search(v0): continue
        prev=span(v0); pend_armed = any("pending" in l.lower() for l in prev)
        for c in reversed(cs[:-1]):
            par=subprocess.run(["git","-C",root,"rev-parse",f"{c}^"],capture_output=True,text=True).stdout.strip()
            pav=blob(root,par,p); cur=blob(root,c,p)
            if pav==cur: continue
            if cur is None: findings.append(("rewrite(deletion)",p,c[:9])); prev=None; continue
            cs_=span(cur)
            ev=None
            if pend_armed and not any("pending" in l.lower() for l in cs_): ev="pending_filled"
            if prev is not None and cs_!=prev: ev="rewrite" if ev is None else ev+"+rewrite"
            if ev:
                disc = any(e.get("path")==p and e.get("commit")==c for e in (disclosures or []))
                if not disc:
                    for k in ev.split("+"): findings.append((f"undisclosed_{k}",p,c[:9]))
            prev=cs_
    # phantom check
    for e in (disclosures or []):
        evc=set(c for k,p,c in findings)
        findings.append(("phantom_check",e.get("path"),str(e.get("commit"))[:9]))
    return pop,findings
