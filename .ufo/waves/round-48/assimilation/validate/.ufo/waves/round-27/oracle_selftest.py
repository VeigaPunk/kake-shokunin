#!/usr/bin/env python3
"""Real consumer-input regressions in disposable Git clones; no stub gates or live writes."""
import argparse,gzip,json,os,pathlib,subprocess,sys,tempfile
W='.ufo/waves/round-27/'
DECL='be375d90afc6fc7aca369ab3cf5247bf460aeed2'
def main():
 p=argparse.ArgumentParser();p.add_argument('--kind',choices=['c1','c2'],required=True);p.add_argument('--source-root',type=pathlib.Path,required=True);a=p.parse_args();results=[]
 with tempfile.TemporaryDirectory(prefix='oracle-',dir='/fast/scratch/hyaku/kake-r27') as tmp:
  root=pathlib.Path(tmp)/'repo';env=os.environ.copy();env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
  subprocess.run(['git','clone','-q',str(a.source_root),str(root)],env=env,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  def git(*args):return subprocess.check_output(['git','-c','core.hooksPath=/dev/null','-C',str(root),*args],env=env,stderr=subprocess.DEVNULL).decode().strip()
  git('config','user.name','oracle-fixture');git('config','user.email','fixture@example.test')
  def write(path,data):
   dest=root/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data if isinstance(data,bytes) else data.encode())
  def js(path,obj):write(path,json.dumps(obj,indent=2)+'\n')
  def measure(name,expected_exit,check):
   git('add','.');git('commit','--allow-empty','-qm',name);rev=git('rev-parse','HEAD')
   script='count_c1.py' if a.kind=='c1' else 'c2_count.py'
   proc=subprocess.run([sys.executable,'-B',str(a.source_root/W/script),'--root',str(root),'--revision',rev],env=env,text=True,capture_output=True)
   try:obj=json.loads(proc.stdout);ok=proc.returncode==expected_exit and check(obj)
   except (ValueError,KeyError,TypeError):obj={'stdout':proc.stdout};ok=False
   results.append(dict(case=name,passed=ok,exit=proc.returncode,expectedExit=expected_exit,output=obj,stderr=proc.stderr))
  def only_carried(x):
   return len(x['findings'])==3 and all(f['errors']==['carried_unverifiable'] for f in x['findings'])
  if a.kind=='c1':
   measure('current_consumer_unverifiable_not_green',1,lambda x:x['citingPairs']==58 and x['reviewedPairs']==58 and x['decided']==55 and x['knownUnverifiableUnits']==7 and only_carried(x))
   js(W+'discovered-pairs.json',[])
   measure('discovered_obligation_cannot_shrink',1,lambda x:x['citingPairs']==58 and x['reviewedPairs']==58 and x['decided']==55)
   retained={str(f.relative_to(root)):f.read_bytes() for f in (root/W/'fetched').rglob('*') if f.is_file()}
   # Branch from the real frozen declaration; previously discovered obligations
   # must not be erased in a descendant just to obtain a smaller fixture.
   git('checkout','--detach',DECL)
   for path,data in retained.items():write(path,data)
   paths=git('ls-tree','-r','--name-only',DECL,'--','corpus/knowledge').splitlines()
   baseline={path:subprocess.check_output(['git','-C',str(root),'show',DECL+':'+path],env=env) for path in paths}
   for path,data in baseline.items():write(path,data)
   js(W+'discovered-pairs.json',[]);js(W+'pairs.json',{'pairs':[]})
   measure('baseline_missing_range_and_carried_unknowns',1,lambda x:x['citingPairs']==57 and x['reviewedPairs']==41 and x['decided']==38 and len(x['missing'])==19 and len(x['unreviewed'])==16)
   artifact=dict(row='S008',file='corpus/knowledge/crawl-scope-per-host.md',kind='artifact',verdict='HOLD',reason='Retained retry manifest identifies the historical fetch',evidence='.ufo/waves/round-26/fetched/manifest-retry.json',contains='S008-1-retry.raw.gz')
   js(W+'pairs.json',{'pairs':[artifact]});measure('independent_artifact_review',1,lambda x:x['decided']==39 and x['newDecided']==1 and only_carried(x))
   bad=dict(artifact,evidence=artifact['file'],contains='S008');js(W+'pairs.json',{'pairs':[bad]});measure('artifact_self_support_rejected',1,lambda x:any('artifact_self_support' in f['errors'] for f in x['findings']))
   group=dict(artifact,row='S002',file='corpus/knowledge/static-canonical-preflight.md');js(W+'pairs.json',{'pairs':[group]});measure('group_requires_source',1,lambda x:any('group_source_required' in f['errors'] for f in x['findings']))
   js(W+'pairs.json',{'pairs':[]});path='corpus/knowledge/publish-channels.md';write(path,baseline[path].replace(b'S001-S007',b'S001'))
   measure('deleted_citation_cannot_shrink_floor',1,lambda x:x['citingPairs']==57 and x['reviewedPairs']==41 and x['decided']==38);write(path,baseline[path])
   record=dict(row='S002',file='corpus/knowledge/static-canonical-preflight.md',kind='source',verdict='HOLD',reason='Release-level artifact membership premise',fetchIndex=1,quote='Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact',anchor='v4.0.0 release, What\'s Changed')
   js(W+'pairs.json',{'pairs':[record]});measure('retained_source_review',1,lambda x:x['decided']==39 and only_carried(x))
   q='This invented quote is not in the retained document';bad=dict(record,quote=q);js(W+'pairs.json',{'pairs':[bad]});write(W+'fetched/text/S002-1.txt',q)
   measure('forged_derived_text_not_authority',1,lambda x:any('quote' in f['errors'] for f in x['findings']))
   bad=dict(record,verdict='STALE');js(W+'pairs.json',{'pairs':[bad]});measure('stale_requires_correction',1,lambda x:any('correction_missing' in f['errors'] for f in x['findings']))
   path=record['file'];write(path,baseline[path]+b'\n[r27-recheck S002 STALE] Corrected fixture attribution.\n');measure('stale_with_real_correction',1,lambda x:x['decided']==39 and only_carried(x));write(path,baseline[path])
   fetched_manifest=json.loads((root/W/'fetched/manifest.json').read_text());s002=next((m for m in fetched_manifest if m['row']=='S002' and m['index']==1),None)
   if not s002:raise SystemExit('fetched manifest has no S002 index 1')
   rawpath=W+'fetched/'+s002['file'];raw=(root/rawpath).read_bytes();write(rawpath,gzip.compress(b'Tampered bytes',mtime=0));js(W+'pairs.json',{'pairs':[record]})
   measure('raw_source_hash_mismatch',1,lambda x:any('source_hash' in f['errors'] for f in x['findings']));write(rawpath,raw)
   override=dict(artifact,row='S003',file='corpus/knowledge/ghp-custom-domain.md',verdict='UNVERIFIABLE');js(W+'pairs.json',{'pairs':[override]})
   measure('unverifiable_override_loses_carried_credit',1,lambda x:x['decided']==37)
   ledger_path='.ufo/waves/round-26/statements.json';ledger=json.loads((root/ledger_path).read_text());ledger['pairs'].append({'row':'S002','file':record['file']});js(ledger_path,ledger)
   measure('inherited_ledger_tamper',2,lambda x:'frozen_input_changed' in x['error'])
  else:
   measure('frozen_missing_interior',0,lambda x:x['passed'] and x['detected']==16 and x['falsePositive']==0)
   path=W+'frozen/corpus/knowledge/static-canonical-preflight.md';saved=(root/path).read_bytes();write(path,saved+b'\nChanged snapshot.\n')
   measure('snapshot_tampered',2,lambda x:x['finding']=='snapshot_tampered');write(path,saved)
   path=W+'c2-oracle.json';oracle=json.loads((root/path).read_text());oracle['expectedPairs']=[];js(path,oracle)
   measure('oracle_rewrite_not_blessed',2,lambda x:x['finding']=='frozen_input_changed')
 print(json.dumps({'kind':a.kind,'cases':results,'failed':sum(not x['passed'] for x in results)},indent=2));return int(any(not x['passed'] for x in results))
if __name__=='__main__':sys.exit(main())
