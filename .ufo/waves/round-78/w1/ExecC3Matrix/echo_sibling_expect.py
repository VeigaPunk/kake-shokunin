#!/usr/bin/env python3
"""Adversary: echo a sibling oracle if exposed, otherwise fail closed."""
import argparse,json,pathlib,sys
p=argparse.ArgumentParser(); p.add_argument('--manifest',required=True); p.add_argument('--root'); p.add_argument('--json',action='store_true'); a=p.parse_args()
try:
    oracle=json.loads((pathlib.Path(a.manifest).parent/'expect.json').read_text())
    manifest=json.loads(pathlib.Path(a.manifest).read_text())
    if oracle['exit']==2: report={'version':1,'error':oracle['error']}
    else: report={'version':1,'checks':[{'id':manifest['checks'][0]['id'],'effective':oracle['effective'],'findings':oracle['findings']}]}
    print(json.dumps(report)); sys.exit(oracle['exit'])
except OSError:
    print(json.dumps({'version':1,'error':'oracle_not_exposed'})); sys.exit(2)
