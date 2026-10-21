#!/usr/bin/env python3
"""R27 C1 measurement; original at be375d9, stricter guards retain its frozen targets."""
import argparse, datetime, gzip, hashlib, importlib.util, json, pathlib, re, subprocess, sys
RANGE = re.compile(r'\bS(\d{3,})\s*(?:[-–—]|\.\.|to|through)\s*S(\d{3,})\b')
LITERAL = re.compile(r'\bS(\d{3,})\b')
W = '.ufo/waves/round-27/'
DECLARATIONS='be375d90afc6fc7aca369ab3cf5247bf460aeed2'

def count(root, revision):
    def blob(path, optional=False):
        p = subprocess.run(['git', '-C', str(root), 'show', revision+':'+path], capture_output=True)
        if p.returncode:
            if optional: return None
            raise ValueError('missing '+path)
        return p.stdout
    def obj(path, optional=False):
        b=blob(path,optional)
        return json.loads(b) if b is not None else None
    def reference(path):
        return subprocess.check_output(['git','-C',str(root),'show',DECLARATIONS+':'+path],stderr=subprocess.DEVNULL)
    def pinned_obj(path):
        data=blob(path)
        if data!=reference(path): raise ValueError('frozen_input_changed: '+path)
        return json.loads(data)
    pop={r['id'] for r in pinned_obj('.ufo/waves/round-26/population.json')['rows']}
    paths=subprocess.check_output(['git','-C',str(root),'ls-tree','-r','--name-only',revision,'--','corpus/knowledge'],text=True).splitlines()
    pairs=set()
    for path in paths:
        text=blob(path).decode()
        ids={int(m[1]) for m in LITERAL.finditer(text)}
        for m in RANGE.finditer(text):
            a,b=int(m[1]),int(m[2])
            if b<a or b-a>200: raise ValueError('invalid range '+m[0])
            ids.update(range(a,b+1))
        pairs.update((f'S{i:03d}',path) for i in ids if f'S{i:03d}' in pop)
    discovered=obj(W+'discovered-pairs.json',True) or []
    pairs.update((p['row'],p['file']) for p in discovered)
    def historical_blobs(path):
        commits=subprocess.check_output(['git','-C',str(root),'log','--format=%H',revision,'--',path],text=True).splitlines()
        result=[]
        for commit in commits:
            found=subprocess.run(['git','-C',str(root),'show',commit+':'+path],capture_output=True)
            if found.returncode==0: result.append(found.stdout)
        return result
    for data in historical_blobs(W+'discovered-pairs.json'):
        pairs.update((p['row'],p['file']) for p in json.loads(data))
    old=pinned_obj('.ufo/waves/round-26/statements.json')['pairs']
    decided={(p['row'],p['file']) for p in old}
    # The frozen contract makes the original obligations a minimum, even if
    # a later edit removes a citation. This adds no new expected outcome.
    baseline=json.loads(reference(W+'c1-before.json'))
    candidate_baseline=blob(W+'c1-before.json',True)
    if candidate_baseline is not None and candidate_baseline!=reference(W+'c1-before.json'):
        raise ValueError('frozen_input_changed: c1-before.json')
    pairs.update(decided)
    pairs.update((p['row'],p['file']) for p in baseline['missing'])
    if any(row not in pop for row,_ in pairs):
        raise ValueError('citing obligation outside frozen population')
    additions=obj(W+'pairs.json',True) or {'pairs':[]}
    findings=[]; new_seen=set(); new_decided=set(); outcomes=[]
    manifest=obj(W+'fetched/manifest.json',True) or []
    views={}
    if manifest:
        history=historical_blobs(W+'fetched/manifest.json')
        if not history or blob(W+'fetched/manifest.json')!=history[-1]:
            raise ValueError('fetched_manifest_changed')
        declaration_time=datetime.datetime.fromisoformat(subprocess.check_output(['git','-C',str(root),'show','-s','--format=%cI',DECLARATIONS],text=True).strip())
        for fetch in manifest:
            fetched_at=datetime.datetime.fromisoformat(fetch['fetchedAt'])
            if fetch['status']!=200 or fetched_at.tzinfo is None or fetched_at<declaration_time:
                raise ValueError('fetch_status_or_time')
        helper=pathlib.Path(__file__).resolve().parents[1]/'round-26/source_text.py'
        if hashlib.sha256(helper.read_bytes()).hexdigest()!='55ae7abc52a5acfd95a86d96c27f12898c30e33ab63cfa7f383640120f57b7d6':
            raise ValueError('source_text_dependency_changed')
        spec=importlib.util.spec_from_file_location('r27_source_text',helper)
        text_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(text_module)
        for fetch in manifest:
            raw=gzip.decompress(blob(W+'fetched/'+fetch['file']))
            if hashlib.sha256(raw).hexdigest()!=fetch['sha256']:
                findings.append({'row':fetch['row'],'errors':['source_hash']})
            views[(fetch['row'],fetch['index'])]=text_module.text_of(raw)
    for p in additions['pairs']:
        key=(p['row'],p['file']); errors=[]
        decided.discard(key)  # A fresh override must not inherit old credit.
        if p['file']=='corpus/knowledge/static-canonical-preflight.md' and p['row'] in {f'S{i:03d}' for i in range(1,7)} and p.get('kind')!='source':
            errors.append('group_source_required')
        if key in new_seen: errors.append('duplicate')
        new_seen.add(key)
        if key not in pairs: errors.append('not_cited')
        if p.get('verdict') not in {'HOLD','STALE','UNVERIFIABLE'}: errors.append('verdict')
        if not p.get('reason'): errors.append('reason')
        if p.get('kind')=='source':
            try:
                f=next(x for x in manifest if x['row']==p['row'] and x['index']==p['fetchIndex'])
                text=views[(f['row'],f['index'])]
                q=p.get('quote','')
                if not q or len(re.findall(r'[^\W_]+',q))<6 or len(q.split())>25 or ' '.join(q.split()) not in ' '.join(text.split()): errors.append('quote')
                if q and any(' '.join(q.split()) in view for (row,_),view in views.items() if row!=p['row']):
                    errors.append('quote_not_row_specific')
                if not p.get('anchor'): errors.append('anchor')
            except (StopIteration,KeyError,ValueError): errors.append('source_missing')
        elif p.get('kind')=='artifact':
            if p.get('evidence','').startswith(('corpus/knowledge/',W)) or p.get('evidence') in {'.ufo/waves/round-26/population.json','.ufo/waves/round-26/statements.json'}: errors.append('artifact_self_support')
            if not p.get('evidence') or not p.get('contains') or p['contains'] not in blob(p['evidence']).decode(): errors.append('artifact_support')
        else: errors.append('kind')
        if p.get('verdict')=='STALE' and f"[r27-recheck {p['row']} STALE]" not in blob(p['file']).decode(): errors.append('correction_missing')
        if errors: findings.append({'row':key[0],'file':key[1],'errors':errors})
        elif p['verdict']!='UNVERIFIABLE': new_decided.add(key)
        outcomes.append({'row':key[0],'file':key[1],'verdict':p.get('verdict'),'valid':not errors})
    decided=(decided|new_decided)&pairs
    missing=sorted(pairs-decided)
    return {'revision':revision,'population':len(pop),'citingPairs':len(pairs),'decided':len(decided),'r26CarriedPairs':len(old),'newDecided':len(new_decided),'missing':[{'row':r,'file':f} for r,f in missing],'findings':findings,'outcomes':outcomes,'scope':'All knowledge-file source-id literals and expanded ranges for the inherited 32-row population, plus monotone discovered pairs. Historical metadata and r26 EOF prose are INCLUDED. Pair adjudication is not proof of truth of every underlying statement.'}

def main():
    if '--selftest' in sys.argv:
        return subprocess.call([sys.executable,'-B',str(pathlib.Path(__file__).with_name('oracle_selftest.py')),'--kind','c1','--source-root',str(pathlib.Path(__file__).resolve().parents[3])])
    a=argparse.ArgumentParser();a.add_argument('--root',type=pathlib.Path,required=True);a.add_argument('--revision',required=True);args=a.parse_args()
    try:
        out=count(args.root,args.revision);code=int(bool(out['missing'] or out['findings']))
    except Exception as e: out={'error':type(e).__name__+': '+str(e)};code=2
    print(json.dumps(out,indent=2));return code
if __name__=='__main__':sys.exit(main())
