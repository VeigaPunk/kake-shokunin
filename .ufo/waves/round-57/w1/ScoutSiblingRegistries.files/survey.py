#!/usr/bin/env python3
"""Read-only survey of sibling lane corpus/SOURCES.md registries (round-57 C2)."""
import glob, os, re, subprocess, sys, collections
ROOT = "/home/vgpnk/Projects/shokunin"
CENSUS = re.compile(rb'^ {0,3}\|[ \t\r\n\f\v]*S[0-9]{3,}[ \t\r\n\f\v]*\|')
ROW0_3 = re.compile(rb'^( {0,3})\|[ \t]*(S[0-9]{3,})[ \t]*\|')
ROW4 = re.compile(rb'^( {4,}|\t+ *)\|[ \t]*(S[0-9]{3,})[ \t]*\|')
ANYROW = re.compile(rb'^\s*\|[ \t]*(S[0-9]+)[ \t]*\|')
IDS = sys.argv[1:] or ["S367", "S372", "S373", "S390", "S409"]
def lanes():
    return sorted(d for d in glob.glob(ROOT + "/*-shokunin") if os.path.isdir(d))
def head(lane):
    r = subprocess.run(["git", "-C", lane, "show", "HEAD:corpus/SOURCES.md"], capture_output=True)
    return r.stdout if r.returncode == 0 else None
def cells(line):
    parts = line.rstrip(b"\r\n").split(b"|")
    return [p.strip().decode("utf-8", "replace") for p in parts[1:-1]] if len(parts) > 2 else []
out, idmap = [], collections.defaultdict(list)
for lane in lanes():
    name = os.path.basename(lane)[:-len("-shokunin")]
    p = lane + "/corpus/SOURCES.md"
    if not os.path.exists(p):
        out.append(dict(lane=name, missing=True)); continue
    data = open(p, "rb").read()
    h = head(lane)
    lines = data.split(b"\n")
    sec = None; heads = []; c = collections.Counter(); ids = []; outside = 0; sp03 = sp4 = 0; n4d = []
    reg_heading = False; any_in = 0
    for i, l in enumerate(lines, 1):
        s = l.rstrip(b"\r")
        if re.match(rb'^#{1,6}\s', s):
            sec = s.decode("utf-8", "replace").strip()
            heads.append(sec)
            if re.match(rb'^## Registry\s*$', s): reg_heading = True
        m = ROW0_3.match(l)
        m4 = ROW4.match(l)
        if CENSUS.match(l):
            c["census"] += 1
            ids.append(m.group(2).decode())
            if len(m.group(1)): sp03 += 1
            if len(m.group(2)) > 4: n4d.append(m.group(2).decode())
            if sec != "## Registry": outside += 1
            cs = cells(l)
            idmap[m.group(2).decode()].append((name, i, cs, sec))
        elif m4:
            sp4 += 1
            idmap[m4.group(2).decode()].append((name, i, cells(l), sec))
    # S\d{3,} ids already restricted to 3+; 4+ digits => len>=5 incl S
    dup = sorted(k for k, v in collections.Counter(ids).items() if v > 1)
    out.append(dict(lane=name, census=c["census"], reg=reg_heading, sp03=sp03, sp4=sp4,
        crlf=data.count(b"\r\n"), dup=dup, n4d=n4d, outside=outside,
        differs=(None if h is None else h != data), headhas=h is not None,
        regsec=[x for x in heads if x.startswith("## ")][:6]))
print("LANE\tcensus\tReg#\tsp1-3\tsp4+\tCRLF\tdup\t4dig\toutside\tdiffHEAD")
for o in out:
    if o.get("missing"): print(o["lane"], "MISSING"); continue
    print("\t".join(map(str, [o["lane"], o["census"], "Y" if o["reg"] else "N", o["sp03"], o["sp4"], o["crlf"],
        ",".join(o["dup"]) or "-", ",".join(o["n4d"]) or "-", o["outside"],
        "no-HEAD" if o["differs"] is None else ("DIFF" if o["differs"] else "same")])))
print("\nHEADINGS")
for o in out:
    if not o.get("missing"): print(o["lane"], o["regsec"])
print("\nIDS")
for i in IDS:
    for (n, ln, cs, sec) in idmap.get(i, []):
        print(i, n, "line", ln, "sec=%s" % sec, "cells=", cs)
    if i not in idmap: print(i, "NONE")
