#!/usr/bin/env python3
"""Round69 finite CLI oracle: 0 all cases, 1 mismatch, 2 unavailable, 64 usage.
Read pinned cases, run explicit tool --input against temporary synthetic files.
Does not establish semantic truth; source and independent review are required.
"""
import hashlib,json,pathlib,subprocess,sys,tempfile
HERE=pathlib.Path(__file__).resolve().parent
if len(sys.argv)!=3 or sys.argv[1]!='--tool': sys.exit(64)
tool=pathlib.Path(sys.argv[2]).resolve()
if not tool.is_file(): print(json.dumps({'reason':'tool_unavailable'}));sys.exit(2)
raw=(HERE/'cases.json').read_bytes()
pin=json.loads((HERE/'freeze.json').read_text())['cases.json']
if hashlib.sha256(raw).hexdigest()!=pin: print(json.dumps({'reason':'snapshot_tampered'}));sys.exit(2)
cases=json.loads(raw); rows=[]
with tempfile.TemporaryDirectory(prefix='kake69-') as td:
 for i,c in enumerate(cases):
  for variant in range(2):
   inp=c['input']
   if variant and isinstance(inp,dict):
    inp=dict(reversed(list(inp.items())))
    if isinstance(inp.get('declarations'),list): inp['declarations']=list(reversed(inp['declarations']))
   p=pathlib.Path(td)/f'{i}-{variant}.json';p.write_text(json.dumps(inp))
   cp=subprocess.run([sys.executable,str(tool),'--input',str(p)],capture_output=True,text=True,timeout=10)
   try:
    o=json.loads(cp.stdout)
    ok=cp.returncode==c['exit'] and o['reason']==c['reason'] and o['index_state']=='not_observed' and o['publication_authorized'] is False and not cp.stderr
   except (ValueError,KeyError,TypeError):ok=False
   rows.append({'id':c['id'],'variant':variant,'passed':ok,'exit':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
print(json.dumps({'passed':sum(x['passed'] for x in rows),'total':len(rows),'rows':rows},indent=2))
sys.exit(0 if all(x['passed'] for x in rows) else 1)
