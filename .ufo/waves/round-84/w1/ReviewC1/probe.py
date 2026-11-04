#!/usr/bin/env python3
import concurrent.futures, hashlib, importlib.util, json, os, re, shutil, subprocess
from pathlib import Path
R=Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
O=R/'.ufo/waves/round-84/w1/ReviewC1'
S=Path('/fast/scratch/hyaku/kake-r84/ReviewC1')
C=R/'.ufo/waves/round-84/c84_defect_queue.py'
H=['5.2.  Cache-Control','5.2.1.  Request Directives','5.2.2.  Response Directives','5.2.3.  Extension Directives']
paths=['corpus/lessons/round-84.md','SCORECARD.md','.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt','.ufo/waves/round-84/w1-spec.json','.ufo/waves/round-84/w1-results.json','.ufo/waves/round-84/controls/census-before.txt','corpus/SOURCES.md']
data={}
for p in paths:
    f=R/p
    data[p]=f.read_bytes() if f.exists() else None
manifest={p: {'present':b is not None,'bytes':len(b) if b is not None else None,'sha256':hashlib.sha256(b).hexdigest() if b is not None else None} for p,b in data.items()}
(O/'snapshot.json').write_text(json.dumps(manifest,indent=2)+'\n')
for p,b in data.items():
    if b is not None:
        dest=O/'snapshot'/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
lesson=(data[paths[0]] or b'').decode()
rfc=data[paths[2]].decode(); lines=rfc.splitlines(keepends=True)
span=''.join(lines[837:844]); count=len(span.split())
corrections=[line for line in lesson.splitlines() if line.lstrip().startswith('[r84-correction')]
d1=[line for line in corrections if all(h in line and h in rfc for h in H) and 'round-83.md' in line and 'Gate' in line]
d2=[line for line in lesson.splitlines() if re.search(r'D2 count=(\d+) span=838-844 measure=words-full-span',line)]
spec=json.loads(data[paths[3]]); conn=[i for i in spec['items'] if i.get('role')=='connector']
results=json.loads(data[paths[4]]) if data[paths[4]] else None
settled=[x for x in (results or {}).get('results',[]) if x.get('agent')=='connector' and isinstance(x.get('output'),str) and x['output'].strip()]
print('BOUNDARY: physical lines 838..844 inclusive, splitlines(keepends=True)[837:844], concatenate without dropping parenthetical, whitespace-delimited maximal non-whitespace tokens')
print('D2 independent_count=',count,' per_line=',[len(x.split()) for x in lines[837:844]],sep='')
print('SPAN_BYTES_REPR',repr(span.encode()))
print('D1 matching correction lines',repr(d1)); print('D2 claim lines',repr(d2));print('D3 spec connector rows',json.dumps(conn,ensure_ascii=False));print('D3 results_present=',results is not None,' settled connector names=',[x.get('name') for x in settled])
# Independent census implementation: parse table cells using outer pipes; normalize with string operations.
sources=data['corpus/SOURCES.md'].decode(); seen=set(); pairs=set(); derived=[]; rows=[]; active=False
for no,line in enumerate(sources.splitlines(),1):
    stripped=line.lstrip(' '); leading=len(line)-len(stripped)
    if leading>3: continue
    if stripped.startswith('## ') or stripped.startswith('##\t'):
        active=stripped[2:].strip()=='Registry';continue
    if stripped.startswith('# ') or stripped.startswith('#\t'): active=False;continue
    if not active or not stripped.startswith('|'): continue
    cells=[x.strip() for x in stripped.split('|')[1:-1]]
    if len(cells)!=11 or not re.fullmatch('S[0-9]{3,}',cells[0]):continue
    rows.append((no,cells))
    match=re.search(r'https?://[^\s|]+',cells[1])
    if not match: continue
    url=match[0].split('#',1)[0]
    if url.endswith('/'):url=url[:-1]
    url=url.split('://',1)[1]; host,slash,rest=url.partition('/'); url=host.lower()+slash+rest
    pair=(url,cells[4])
    if url in seen and pair not in pairs:derived.append((cells[0],url))
    seen.add(url);pairs.add(pair)
receipt=data['.ufo/waves/round-84/controls/census-before.txt'].decode()
claimed=[]
for line in receipt.splitlines():
    fields=line.split('\t')
    if len(fields)>=3 and fields[1]=='W04':
        ident,_,url=fields[2].partition(' duplicate url ');claimed.append((ident,url.removesuffix(' across scopes')))
module_spec=importlib.util.spec_from_file_location('counter',C); counter=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(counter)
computed=counter.census_w04(sources)
print('D4 registry_rows=',len(rows),' independent_w04=',len(derived),' frozen_counter_w04=',len(computed),' receipt_w04=',len(claimed),sep='')
print('D4 counter_minus_independent',sorted(set(computed)-set(derived)));print('D4 independent_minus_counter',sorted(set(derived)-set(computed)))
print('D4 receipt_minus_independent',sorted(set(claimed)-set(derived)));print('D4 independent_minus_receipt',sorted(set(derived)-set(claimed)))
print('D4 W04 exact pairs',json.dumps(derived));print('D4 lesson_receipt_named=', 'controls/census-before.txt' in lesson)
print('D3 lesson_or_scorecard_named=',[(i.get('name'),i.get('name','') in lesson or i.get('name','') in (data['SCORECARD.md'] or b'').decode()) for i in conn])
(O/'registry-rows.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
S.mkdir(parents=True,exist_ok=True)
try:
    def put(root,p,text):
        f=root/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text)
    good='[r84-correction] round-83.md Gate '+', '.join(H)+'\nD2 count='+str(count)+' span=838-844 measure=words-full-span\n'
    cases={}
    # Mandatory prose-only tree: none of the required evidence files.
    root=S/'prose-only';put(root,'corpus/lessons/round-84.md','All four defects D1 D2 D3 D4 are closed.\n'+good);cases['prose-only']=root
    def fixture(name,les):
        root=S/name
        for p in paths:
            if p in ['corpus/lessons/round-84.md','SCORECARD.md','.ufo/waves/round-84/w1-results.json']:continue
            if data[p] is not None:
                f=root/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data[p])
        put(root,'corpus/lessons/round-84.md',les)
        put(root,'.ufo/waves/round-84/w1-results.json',json.dumps({'results':[{'name':conn[0]['name'],'agent':'connector','output':'done'}]}))
        cases[name]=root;return root
    root=fixture('heading-not-retained',good)
    put(root,'.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt',rfc.replace(H[3],'5.2.3.  NOT RETAINED'))
    fixture('missing-d3-d4-row',good)
    fixture('split-d1-correction','[r84-correction] '+', '.join(H)+'\n[r84-correction] round-83.md Gate\nD2 count='+str(count)+' span=838-844 measure=words-full-span\n')
    root=fixture('nonstring-output',good)
    put(root,'.ufo/waves/round-84/w1-results.json',json.dumps({'results':[{'agent':'connector','output':None}]}))
    root=fixture('bad-ok-path',good)
    put(root,'.ufo/waves/round-84/controls/census-before.txt',receipt.replace(str(R/'corpus/SOURCES.md'),'not-corpus-SOURCES.md'))
    root=fixture('nonzero-exit-substring',good)
    put(root,'.ufo/waves/round-84/controls/census-before.txt',receipt.replace('census_exit=0','census_exit=01'))
    def run(pair):
        name,root=pair;cmd=['python3','-B',str(C),'--root',str(root)]
        proc=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'TMPDIR':str(S),'PYTHONDONTWRITEBYTECODE':'1'})
        text='$ '+' '.join(cmd)+'\n'+proc.stdout+proc.stderr+f'exit={proc.returncode}\n'
        (O/(name+'.txt')).write_text(text);return name,proc.returncode,proc.stdout
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
        for name,code,out in pool.map(run,cases.items()):print('CASE',name,'exit',code,'\n'+out)
finally:
    shutil.rmtree(S)
    print('scratch_removed=',not S.exists())
