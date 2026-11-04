#!/usr/bin/env python3
"""Deliberately degenerate audit control; no expectation input is read."""
import argparse,json,pathlib,sys
p=argparse.ArgumentParser()
p.add_argument('--manifest',required=True)
p.add_argument('--root',required=True)
p.add_argument('--json',action='store_true')
a=p.parse_args()
m=json.loads(pathlib.Path(a.manifest).read_text())
rows=[]
for c in m["checks"]:
    effective=['follow','index']; findings=[]
    rows.append({"id":c["id"],"effective":effective,"findings":findings})
print(json.dumps({"version":1,"checks":rows}))
sys.exit(0)
