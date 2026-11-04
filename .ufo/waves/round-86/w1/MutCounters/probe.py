import hashlib, importlib.util, json, os, subprocess, sys
from pathlib import Path
S=Path('/fast/scratch/hyaku/kake-r86/MutCounters')
D=Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/MutCounters')
phase=sys.argv[1]
os.environ['TMPDIR']=str(S)
spec=importlib.util.spec_from_file_location('counter',S/'count.py'); c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
records=[]
def run(args):
 p=subprocess.run(args,cwd=S,env=os.environ,capture_output=True,text=True)
 r={'command':args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr};records.append(r);print(json.dumps(r))
run([sys.executable,'-B',str(S/'count.py'),'--selftest'])
# Deliberately isolate basis-only corruption from other fields.
w=S/('basis-'+phase);w.mkdir(exist_ok=True)
pairs=[[p,dict(e,basis='incorrect-basis')] for _,p,e in c.CASES]
t=w/'wrong-basis.py';t.write_text(c.FIXTURE_C2_TOOL.replace('__EXPECTED__',json.dumps(pairs)))
run([sys.executable,'-B',str(S/'count.py'),'--claim','c2','--tool',str(t),'--work',str(w/'work')])
# Hand-built fixture has every R4 conjunct except flip:.
r=S/('r4-'+phase);(r/'corpus').mkdir(parents=True,exist_ok=True)
(r/'corpus'/'README.md').write_text('D84-2 and D84-3 stay retained-open; see corpus/lessons/round-85.md\n')
ok,detail=c.c1_item_r4(c.Tree(r));records.append({'detector':'r4-missing-flip','ok':ok,'detail':detail});print(json.dumps(records[-1]))
if phase in ('pristine','restored'):
 # Candidate absent at initial discovery: use exact selftest lookup fixture, never a claimed reader.
 for mode in ('green','last-occurrence','no-store-dropped','shared-always'):
  w=S/(phase+'-'+mode);w.mkdir(exist_ok=True)
  pairs=[]
  for name,p,e in c.CASES:
   out=dict(e)
   if mode=='last-occurrence' and name in ('duplicate-first-occurrence','first-occurrence-not-minimum'):
    out['freshness_lifetime_seconds']=int(p['cache_control'][-1].split('=')[1])
   if mode=='no-store-dropped' and name in ('no-store-not-storable','order-independent-a','order-independent-b'):
    out=c.obj(life=None if name=='no-store-not-storable' else 60,basis=None if name=='no-store-not-storable' else 'max-age')
   if mode=='shared-always' and name=='private-ignores-s-maxage':
    out=c.obj(life=60,basis='s-maxage')
   pairs.append([p,out])
  t=w/'tool.py';t.write_text(c.FIXTURE_C2_TOOL.replace('__EXPECTED__',json.dumps(pairs)))
  run([sys.executable,'-B',str(S/'count.py'),'--claim','c2','--tool',str(t),'--work',str(w/'work')])
  mismatches=[]
  for i,(name,p,e) in enumerate(c.CASES,1):
   cw=w/('detail-'+str(i));cw.mkdir(exist_ok=True)
   code,out=c.run_case(t,p,cw)
   got=json.loads(out)
   if code or got!=e:mismatches.append({'case':i,'name':name,'expected':e,'actual':got})
  records.append({'fixture':mode,'sha256':hashlib.sha256(t.read_bytes()).hexdigest(),'mismatches':mismatches});print(json.dumps(records[-1]))
records.append({'counter_sha256':hashlib.sha256((S/'count.py').read_bytes()).hexdigest()})
(D/(phase+'.json')).write_text(json.dumps(records,indent=2)+'\n')
