#!/usr/bin/env python3
"""Frozen r27 C1 author counting command, written before adjudication or gate implementation."""
import argparse, gzip, hashlib, json, pathlib, re, subprocess, sys
RANGE = re.compile(r'\bS(\d{3,})\s*(?:[-–—]|\.\.|to|through)\s*S(\d{3,})\b')
LITERAL = re.compile(r'\bS(\d{3,})\b')
W = '.ufo/waves/round-27/'

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
    pop={r['id'] for r in obj('.ufo/waves/round-26/population.json')['rows']}
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
    old=obj('.ufo/waves/round-26/statements.json')['pairs']
    decided={(p['row'],p['file']) for p in old}
    additions=obj(W+'pairs.json',True) or {'pairs':[]}
    findings=[]; new_seen=set(); new_decided=set(); outcomes=[]
    manifest=obj(W+'fetched/manifest.json',True) or []
    for p in additions['pairs']:
        key=(p['row'],p['file']); errors=[]
        if key in new_seen: errors.append('duplicate')
        new_seen.add(key)
        if key not in pairs: errors.append('not_cited')
        if p.get('verdict') not in {'HOLD','STALE','UNVERIFIABLE'}: errors.append('verdict')
        if not p.get('reason'): errors.append('reason')
        if p.get('kind')=='source':
            try:
                f=next(x for x in manifest if x['row']==p['row'] and x['index']==p['fetchIndex'])
                raw=gzip.decompress(blob(W+'fetched/'+f['file']))
                if hashlib.sha256(raw).hexdigest()!=f['sha256']: errors.append('source_hash')
                text=blob(W+'fetched/'+f['text']).decode()
                q=p.get('quote','')
                if not q or len(q.split())>25 or ' '.join(q.split()) not in ' '.join(text.split()): errors.append('quote')
                if not p.get('anchor'): errors.append('anchor')
            except (StopIteration,KeyError,ValueError): errors.append('source_missing')
        elif p.get('kind')=='artifact':
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
    a=argparse.ArgumentParser();a.add_argument('--root',type=pathlib.Path,required=True);a.add_argument('--revision',required=True);args=a.parse_args()
    try:
        out=count(args.root,args.revision);code=int(bool(out['missing'] or out['findings']))
    except Exception as e: out={'error':type(e).__name__+': '+str(e)};code=2
    print(json.dumps(out,indent=2));return code
if __name__=='__main__':sys.exit(main())
