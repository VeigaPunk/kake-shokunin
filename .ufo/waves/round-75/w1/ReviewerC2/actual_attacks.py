import os,sys,json,subprocess,hashlib,copy,shutil
S='/fast/scratch/hyaku/kake-r75/ReviewerC2'; C=S+'/clone'
T=S+'/instrument_receipts.snapshot.py'
SRC='/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-75/w1/ExecC2Tool/instrument_receipts.py'
B='c9c5e484c533aa65f4374b841a3edcf572ed19a9'; O='c9fd964354b03b163994519ae43d741b3ee3a81d'
P=C+'/corpus/knowledge/instrument-receipts.json'
os.environ['TMPDIR']=S+'/tmp'; os.makedirs(S+'/actual-fixtures',exist_ok=True)
shutil.copyfile(SRC,T)
results=[]
def run(name,args):
 cmd=[sys.executable,'-B',T,*args]
 p=subprocess.run(cmd,capture_output=True,text=True,env=os.environ.copy())
 results.append({'name':name,'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 return p
assert subprocess.check_output(['git','-C',C,'rev-parse','--show-toplevel'],text=True).strip()==C
assert subprocess.check_output(['git','-C',C,'rev-parse','HEAD'],text=True).strip()==B
if os.path.exists(P): os.unlink(P)
run('baseline-no-receipt',['--root',C,'--revision',B,'--check'])
a=['--root',C,'--revision',B]
run('write-first',a+['--write','--date','2026-11-03']); first=open(P,'rb').read()
run('write-second',a+['--write','--date','2026-11-03']); second=open(P,'rb').read()
honest=json.loads(first)
run('UNCOMMITTED-valid-receipt-at-base',a+['--check'])
for name in sorted(os.listdir(S+'/fixtures')):
 if not name.endswith('.json'): continue
 doc=json.load(open(S+'/fixtures/'+name));
 if not name.startswith(('f06','f14')): doc['revision']=B
 # old reference fixtures derive same registration values; actual tool is independently AST-based.
 with open(P,'w') as f: json.dump(doc,f)
 shutil.copyfile(P,S+'/actual-fixtures/'+name)
 run(name,a+['--check'])
# same unchanged population, opposite cross-revision direction
with open(P,'w') as f: json.dump(honest,f)
run('base-generated-checked-at-ancestor',['--root',C,'--revision',O,'--check'])
# dirty working-tree bytes must not affect the writer or checker
victim=C+'/'+honest['files'][0]['path']; raw=open(victim,'rb').read()
try:
 with open(victim,'ab') as f:f.write(b'\n# dirty ReviewerC2 fixture\n')
 run('dirty-worktree-write',a+['--write','--date','2026-11-03'])
 dirtywrite=open(P,'rb').read()
 run('dirty-worktree-check',a+['--check'])
finally:
 with open(victim,'wb') as f:f.write(raw)
run('actual-selftest',['--selftest','--work',S+'/actual-selftest'])
meta={'tool_sha256':hashlib.sha256(open(T,'rb').read()).hexdigest(),'idempotent':first==second,'dirty_write_identical':first==dirtywrite,'results':results}
with open(S+'/actual-results.json','w') as f:json.dump(meta,f,indent=2)
for r in results:
 print(r['name'],r['exit'],r['stdout'].splitlines()[0] if r['stdout'] else r['stderr'][:100])
print('idempotent',meta['idempotent'],'dirty_write_identical',meta['dirty_write_identical'],'snapshot',meta['tool_sha256'])
