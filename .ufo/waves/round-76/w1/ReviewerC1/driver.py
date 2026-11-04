#!/usr/bin/env python3
import concurrent.futures, importlib.util, json, os, pathlib, re, shutil, subprocess
S=pathlib.Path('/fast/scratch/hyaku/kake-r76/ReviewerC1')
R=pathlib.Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
O=R/'.ufo/waves/round-76/w1/ReviewerC1'
B='a0491fcd041cbc3fff2c964ecf6268557e45a5c1'
C=R/'.ufo/waves/round-76/c76_quote_truth.py'
os.environ['TMPDIR']=str(S/'tmp')
def git(root,*args):
    return subprocess.run(['git','-C',str(root),*args],capture_output=True,text=True,check=True).stdout
# Read-only, independent population extractor: exact level-two section identities.
rows=[]
for file in ['SCORECARD.md','corpus/QUALITY.md','corpus/lessons/round-75.md']:
    text=git(R,'show',B+':'+file)
    active=False; pending=None; block=[]
    def flush_table():
        if not block:return
        separators=[i for i,(_,t) in enumerate(block) if re.fullmatch(r'\s*\|[\s:|\-]+\|\s*',t)]
        rows.extend((file,n,t) for n,t in block[(separators[0]+1 if separators else 0):])
        block.clear()
    def flush_bullet():
        global pending
        if pending:rows.append((file,*pending));pending=None
    for n,line in enumerate(text.splitlines(),1):
        h=re.match(r'^(#{1,6})\s+(.*)$',line)
        if h and len(h[1])<=2:
            flush_table();flush_bullet()
            if file=='SCORECARD.md':active=bool(re.match(r'^Round (75|76)\b',h[2])) and h[1]=='##'
            elif file=='corpus/QUALITY.md':active=bool(re.match(r'^Round-(75|76) criterion\b',h[2])) and h[1]=='##'
            else:active=h[1]=='##' and h[2] in ['Mistakes','Gate','Claims','Corrections']
            continue
        if not active:continue
        if file!='corpus/QUALITY.md' and line.lstrip().startswith('|'):
            block.append((n,line));continue
        flush_table()
        if file!='SCORECARD.md':
            if re.match(r'^\s*[-*] ',line):flush_bullet();pending=(n,line)
            elif pending and line.startswith(('  ','\t')) and line.strip():pending=(pending[0],pending[1]+' '+line.strip())
            else:flush_bullet()
    flush_table();flush_bullet()
# Committed receipt universe, read through cat-file batch once.
names=git(R,'ls-tree','-r','--name-only',B,'.ufo/waves').splitlines()
dirs={'controls','verification','resid','receipts','frozen','fixtures','cases'}
exts={'.txt','.json','.csv','.tsv','.log','.out','.ndjson'}
names=[p for p in names if not (re.search(r'(?:-results\.json|-dispatch\.json|-spec\.json|swarm-registry\.json)$',p) or '.ready' in pathlib.Path(p).name) and (dirs.intersection(pathlib.Path(p).parts) or pathlib.Path(p).suffix in exts)]
p=subprocess.run(['git','-C',str(R),'cat-file','--batch'],input=('\n'.join(B+':'+p for p in names)+'\n').encode(),capture_output=True,check=True)
receipts=[];pos=0
for name in names:
    end=p.stdout.index(b'\n',pos);size=int(p.stdout[pos:end].split()[-1]);data=p.stdout[end+1:end+1+size];pos=end+size+2
    try:body=data.decode('utf8')
    except UnicodeDecodeError:continue
    if '\x00' not in body:receipts.append((name,body))
independent=[];allspans=[]
for file,n,line in rows:
    for span in re.findall(r'`([^`\n]+)`',line):
        if re.match(r'^(?:[.~/]|scripts/|corpus/|node |python3 |git |sh |--)',span) or '://' in span or re.search(r'\.(md|py|mjs|js|txt|json|html|xml|ya?ml|csv|log)$',span):continue
        if not re.search(r'[A-Za-z_][A-Za-z0-9_.-]*=\S|\bexit\s+\d+\b|\b\d+/\d+\b|^[a-f0-9]{7,64}$',span):continue
        frags=[f for f in re.split(r'…|\[\.\.\.\]|\.\.\.',span) if f.strip()]
        hits=[name for name,body in receipts if all(f in body for f in frags)]
        item={'file':file,'line':n,'span':span,'receipt_hits':hits[:3]}
        allspans.append(item)
        if not hits:independent.append(item)
(O/'independent.json').write_text(json.dumps({'rows':len(rows),'receipt_files':len(receipts),'spans':len(allspans),'absent':independent,'population':rows,'allspans':allspans},indent=2)+'\n')
# Fixtures are committed only in isolated scratch repos, as explicitly required by seat assignment.
table=lambda row,heading='## Round 76':heading+'\n\n| Subject | Claim |\n|---|---|\n'+row+'\n'
cs=[]
def case(name,row,expected,receipt='aa=1 bb=2\n',extra=None,heading='## Round 76'):
    cs.append((name,table(row,heading),expected,receipt,extra or {}))
case('unrelated_round','| S | `aa=1 bb=2` |',0)
case('seat_prose','| S | `zz=9` |',1,extra={'.ufo/waves/round-76/w1/Seat.md':'zz=9\n'})
case('dispatcher_prose','| S | `zz=9` |',1,extra={'.ufo/waves/round-76/w1-results.json':'{"value":"zz=9"}\n'})
case('elision_split','| S | `aa=1 … zz=9` |',1,extra={'.ufo/waves/round-76/controls/second.txt':'zz=9\n'})
case('different_span','| S | `zz=9` |\n| C | [r76-correction] `aa=1 bb=2` supersedes `yy=8` |',1)
case('nonreceipt_correction','| S | `zz=9` |\n| C | [r76-correction] `yy=8` supersedes `zz=9` |',1,extra={'.ufo/waves/round-76/w1/Seat.md':'yy=8\n'})
case('fabricated_digest','| S | `'+('a'*64)+'` |',1)
case('pipe_span','| S | `aa=1|bb=2` |',1)
case('newline_escape',r'| S | `aa=1\nbb=2` |',1)
case('indented_row','   | S | `zz=9` |',1)
case('round7_prefix','| ## Round 76 | `zz=9` |',0,heading='## Round 7')
case('duplicate_correction','| S | `zz=9` |\n| C | [r76-correction] `aa=1 bb=2` supersedes `zz=9` |\n| C | [r76-correction] `aa=1 bb=2` supersedes `zz=9` |',0)
case('single_letter_assignment','| S | `x=9` |',1)
case('correction_partial_line','| S | `zz=9` |\n| C | [r76-correction] `aa=1` supersedes `zz=9` |',1)
case('ready_marker','| S | `zz=9` |',1,extra={'.ufo/waves/round-76/probe.ready.txt':'zz=9\n'})
case('wrong_heading_level','| S | `zz=9` |',0,heading='### Round 76')
case('correction_extra_false_claim','| S | `zz=9` |\n| C | [r76-correction] `aa=1 bb=2` supersedes `zz=9`; actual `fake=777` |',1)
def run_case(c):
    name,score,want,receipt,extra=c;root=S/'fixtures'/name;root.mkdir(parents=True,exist_ok=True)
    files={'SCORECARD.md':score,'corpus/QUALITY.md':'# Quality\n','corpus/lessons/round-76.md':'# Lesson\n','.ufo/waves/round-12/controls/receipt.txt':receipt,**extra}
    for path,body in files.items():
        f=root/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(body)
    git(root,'init','-q')
    assert pathlib.Path(git(root,'rev-parse','--show-toplevel').strip())==root
    git(root,'add','-A')
    assert pathlib.Path(git(root,'rev-parse','--show-toplevel').strip())==root
    git(root,'-c','user.name=fixture','-c','user.email=fixture@invalid','commit','-qm','held-out')
    cmd=['python3','-B',str(C),'--root',str(root),'--revision','HEAD','--base','HEAD','--rounds','75,76','--json']
    p=subprocess.run(cmd,capture_output=True,text=True)
    target=O/name;shutil.copytree(root,target,ignore=shutil.ignore_patterns('.git'),dirs_exist_ok=True)
    (target/'verdict.json').write_text(p.stdout);(target/'stderr.txt').write_text(p.stderr)
    result={'name':name,'command':cmd,'expected_rc':want,'observed_rc':p.returncode,'output':json.loads(p.stdout)}
    (target/'run.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(run_case,cs))
(O/'fixture-results.json').write_text(json.dumps(results,indent=2)+'\n')
print('INDEPENDENT',json.dumps({'rows':len(rows),'receipts':len(receipts),'spans':len(allspans),'absent':len(independent)}))
for r in results:print(r['name'],'expected',r['expected_rc'],'observed',r['observed_rc'],'rows',r['output']['rows'],'ids',[f['id'] for f in r['output']['findings']])
