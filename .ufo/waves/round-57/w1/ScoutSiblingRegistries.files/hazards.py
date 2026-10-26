#!/usr/bin/env python3
"""Second pass: extra parser hazards + URL cells for the C2 ids (read-only)."""
import glob, os, re, collections
ROOT="/home/vgpnk/Projects/shokunin"
IDS=["S367","S372","S373","S390","S409"]
for p in sorted(glob.glob(ROOT+"/*-shokunin/corpus/SOURCES.md")):
    n=os.path.basename(os.path.dirname(os.path.dirname(p)))[:-9]
    t=open(p,encoding="utf-8",errors="replace").read().split("\n")
    nreg=sum(1 for l in t if re.match(r'^## Registry\s*$',l))
    fence=False; infence=0; pipe_nonid=0; idlike_other=[]; ws=0; tabs=0; order=[]; seen_sec=None; last=None; nonmono=0
    ids=[]
    for i,l in enumerate(t,1):
        if l.lstrip().startswith("```"): fence=not fence
        if re.match(r'^#{1,6}\s',l): seen_sec=l
        m=re.match(r'^ {0,3}\|[ \t]*(S[0-9]{3,})[ \t]*\|',l)
        if m:
            if fence: infence+=1
            ids.append(m.group(1))
            continue
        if re.match(r'^\s*\|[ \t]*S\d',l): idlike_other.append((i,l[:40]))
        if re.search(r'^\t',l) and '|' in l: tabs+=1
        if re.match(r'^\|.*\|\s*$',l) and not re.match(r'^\|[ \-:|]+\|\s*$',l) and seen_sec and seen_sec.startswith("## Registry") and not re.match(r'^\|\s*(ID|id|Id)\b',l): pipe_nonid+=1
    nums=[int(x[1:]) for x in ids]
    nonmono=sum(1 for a,b in zip(nums,nums[1:]) if b<=a)
    rows3=[x for x in ids if len(x)==4]
    cellcnt=collections.Counter()
    for l in t:
        if re.match(r'^ {0,3}\|[ \t]*S[0-9]{3,}',l):
            cellcnt[len(l.split("|"))-2]+=1
    print(n,"regheadings=%d"%nreg,"rows_in_fence=%d"%infence,"idlike_noncensus=%s"%idlike_other[:3],"nonmono=%d"%nonmono,"idrange=%s-%s"%(ids[0],ids[-1]) if ids else "",
          "pipe_cols=%s"%dict(cellcnt),"regsec_nonid_pipe=%d"%pipe_nonid, "trailing_ws=%d"%sum(1 for l in t if l!=l.rstrip()))
print()
for p in sorted(glob.glob(ROOT+"/*-shokunin/corpus/SOURCES.md")):
    n=os.path.basename(os.path.dirname(os.path.dirname(p)))[:-9]
    for l in open(p,encoding="utf-8",errors="replace").read().split("\n"):
        m=re.match(r'^ {0,3}\|[ \t]*(S[0-9]{3,})[ \t]*\|[ \t]*(.*?)[ \t]*\|',l)
        if m and m.group(1) in IDS:
            c=m.group(2); u=re.findall(r'https?://[^\s)|]+',c)
            print(m.group(1),n,u)
