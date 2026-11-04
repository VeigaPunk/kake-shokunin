import hashlib,json,os,subprocess,sys,shutil
from pathlib import Path
S=Path('/fast/scratch/hyaku/kake-r86/MutCounters')
D=Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/MutCounters')
os.environ['TMPDIR']=str(S)
rows=[]
green=(S/'pristine-green/tool.py').read_bytes()
active=S/'active-fixture.py'
for mode in ('last-occurrence','no-store-dropped','shared-always'):
 active.write_bytes(green)
 try:
  for phase in ('before','mutated','restored'):
   if phase=='mutated':active.write_bytes((S/('pristine-'+mode)/'tool.py').read_bytes())
   elif phase=='restored':active.write_bytes(green)
   cmd=[sys.executable,'-B',str(S/'count.py'),'--claim','c2','--tool',str(active),'--work',str(S/'cycles'/mode/phase)]
   p=subprocess.run(cmd,cwd=S,env=os.environ,capture_output=True,text=True)
   r=dict(mode=mode,phase=phase,command=cmd,exit=p.returncode,stdout=p.stdout,stderr=p.stderr,sha256=hashlib.sha256(active.read_bytes()).hexdigest())
   rows.append(r);print(json.dumps(r))
 finally:active.write_bytes(green)
(D/'fixture-cycles.json').write_text(json.dumps(rows,indent=2)+'\n')
source=Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/count.py')
r={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'restored_scratch_sha256':hashlib.sha256((S/'count.py').read_bytes()).hexdigest(),'exact_bytes_equal':source.read_bytes()==(S/'count.py').read_bytes()}
(D/'restoration.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
for f in ('probe.py','cycles.py','count.py'):shutil.copy2(S/f,D/f)
for mode in ('green','last-occurrence','no-store-dropped','shared-always'):
 shutil.copy2(S/('pristine-'+mode)/'tool.py',D/('fixture-'+mode+'.py'))
