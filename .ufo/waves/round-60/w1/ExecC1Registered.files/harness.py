import json, os, re, shlex, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

S='/fast/scratch/hyaku/kake-r60/ExecC1Registered'
CLONE=f'{S}/lane'
BASE='97cdc122379711c2b02a8970752c8782da3ac81d'
FLEET='/home/vgpnk/Projects/shokunin'
L=open(f'{S}/SKILL.base.md').read().split('\n')

MEMBERS=[
 # (row_line, name, path, label, pin)
 (1233,'readme-index-counter','.ufo/waves/round-55/c55_readme_index.py','historical','64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6'),
 (1234,'yahoo-robots-quote-truth-counter','.ufo/waves/round-55/c55_quote_truth.py','historical','64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6'),
 (1253,'selftest-tally-counter','.ufo/waves/round-56/c56_selftally.py','live',None),
 (1254,'yahoo-crawl-handling-quote-truth-counter','.ufo/waves/round-56/c56_quote_truth.py','historical','4cb225fb032b04166fb0232bc98a7bcce72675ec'),
 (1273,'receipt-pin-counter','.ufo/waves/round-57/c57_receipt_pins.py','historical','32754df75774dd38e8a96fcda375fc93adf97f1e'),
 (1274,'id-resolver-gate','.ufo/waves/round-57/c57_idresolver_gate.py','live',None),
 (1275,'baidu-dead-link-quote-truth-counter','.ufo/waves/round-57/c57_quote_truth.py','historical','32754df75774dd38e8a96fcda375fc93adf97f1e'),
 (1293,'receipt-rewrite-counter','.ufo/waves/round-58/c58_receipt_rewrites.py','live',None),
 (1294,'resolver-cases-counter','.ufo/waves/round-58/c58_resolver_cases.py','live',None),
 (1295,'baidu-crawler-identification-quote-truth-counter','.ufo/waves/round-58/c58_quote_truth.py','historical','8d340c15200959190ba3e894399cdc931976331f'),
 (1307,'axis-evidence-counter','.ufo/waves/round-59/c59_axis_evidence.py','live',None),
 (1308,'disclosed-route-resolver-cases-counter','.ufo/waves/round-59/c59_resolver_cases.py','live',None),
 (1309,'crawler-identity-quote-truth-counter','.ufo/waves/round-59/c59_quote_truth.py','live',None),
]

def entry_span(line, path):
    cells=[c.strip() for c in line.strip().strip('|').split('|')]
    for s in re.findall(r'`([^`]*)`',cells[2]):
        if path in s: return s
    return None

def build_argv(cmd, rev, scratch):
    # [...] kept iff every token is --flag or a substitutable <placeholder>
    def seg(m):
        inner=m.group(1).strip()
        toks=inner.split()
        ok=all(t.startswith('--') or t in ('<commit>','<rev>','<revision>','<tip>','<scratch>','<fleet root>') for t in toks)
        return (' '+inner+' ') if ok else ' '
    cmd=re.sub(r'\[([^\]]*)\]',seg,cmd)
    cmd=cmd.replace('<fleet root>',FLEET)
    cmd=re.sub(r'<(commit|rev|revision|tip)>',rev,cmd)
    cmd=cmd.replace('<scratch>',scratch)
    toks=shlex.split(cmd)
    env={}
    while toks and re.match(r'^[A-Za-z_][A-Za-z0-9_]*=',toks[0]):
        k,v=toks.pop(0).split('=',1); env[k]=v
    return env,toks

def run(job):
    mid=job['id']; rev=job['rev']; drop=job.get('drop_fleet')
    scratch=f"{S}/run_scratch/{mid}_{job['tag']}"
    os.makedirs(scratch,exist_ok=True)
    env0,argv=build_argv(job['cmd'],rev,scratch)
    if drop:
        argv=[a for i,a in enumerate(argv) if not (a=='--fleet' or (i>0 and argv[i-1]=='--fleet'))]
        # remove the value following --fleet too (rebuild cleanly)
        argv=[]; skip=False
        for a in shlex.split(re.sub(r'\[([^\]]*)\]',seg2,job['cmd']).replace('<commit>',rev).replace('<rev>',rev).replace('<tip>',rev).replace('<scratch>',scratch)):
            pass
    env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
    env['TMPDIR']=scratch; env.update(env0)
    t0=time.time()
    try:
        p=subprocess.run(argv,cwd=CLONE,env=env,capture_output=True,text=True,timeout=1800)
        exitcode=p.returncode; out=p.stdout; err=p.stderr
    except subprocess.TimeoutExpired as e:
        exitcode=124; out=e.stdout or ''; err=e.stderr or ''
    secs=round(time.time()-t0,1)
    lines=[x for x in out.splitlines() if x.strip()]
    summary=lines[-1][:300] if lines else ('STDERR: '+err.splitlines()[0][:280] if err.splitlines() else '(no output)')
    open(f"{S}/runs/{mid}_{job['tag']}.out",'w').write(out)
    open(f"{S}/runs/{mid}_{job['tag']}.err",'w').write(err)
    return {'id':mid,'tag':job['tag'],'rev':rev,'argv':argv,'exit':exitcode,'secs':secs,'summary':summary}

def seg2(m): return ' '

jobs=[]
for n,name,path,label,pin in MEMBERS:
    sp=entry_span(L[n-1],path)
    assert sp, (n,path)
    jobs.append({'id':name,'tag':'T','rev':BASE,'cmd':sp})
    if pin: jobs.append({'id':name,'tag':'P','rev':pin,'cmd':sp})
# no-fleet run for c57_idresolver_gate at base
nf=[j for j in jobs if j['id']=='id-resolver-gate' and j['tag']=='T'][0]
jobs.append({'id':'id-resolver-gate','tag':'Tnofleet','rev':BASE,'cmd':nf['cmd'].replace('[--fleet <fleet root>]','')})

results=[]
with ThreadPoolExecutor(max_workers=6) as ex:
    for r in ex.map(run,jobs):
        results.append(r); print(json.dumps(r),flush=True)
json.dump(results,open(f'{S}/results.json','w'),indent=1)
