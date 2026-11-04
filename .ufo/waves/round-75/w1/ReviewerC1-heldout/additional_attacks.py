#!/usr/bin/env python3
import concurrent.futures, hashlib, json, os, pathlib, subprocess, tempfile
S=pathlib.Path('/fast/scratch/hyaku/kake-r75/ReviewerC1')
LANE=pathlib.Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
COUNTER=S/'counter-at-freeze.py'
BASE='c9c5e484c533aa65f4374b841a3edcf572ed19a9'
ENV={**os.environ,'TMPDIR':str(S)}
records=[]
def cmd(argv, cwd=None, check=True):
 p=subprocess.run(list(map(str,argv)),cwd=cwd,env=ENV,text=True,capture_output=True)
 if check and p.returncode: raise RuntimeError((argv,p.returncode,p.stderr))
 return p

def git(d,*args): return cmd(['git','-C',d,*args])
def guard(d):
 assert git(d,'rev-parse','--show-toplevel').stdout.strip()==str(d)
def commit(d):
 guard(d);git(d,'add','-A');git(d,'-c','user.name=ReviewerC1','-c','user.email=reviewerc1@r75.invalid','commit','-q','-m','heldout scenario')
 return git(d,'rev-parse','HEAD').stdout.strip()
HEAD='| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |\n|---|---|---|---|---|---|---|---|\n'
def row(name,kind,entry,test,pinned='dash'):
 return f'| {name} | {kind} | {entry} | 0=met | {test} | {pinned} | reports only | ReviewerC1 |\n'
def section(rows):return '\n### Round 75 gate registry additions\n\n'+HEAD+''.join(rows)

def run(label,d,rev,base=None):
 argv=['python3','-B',str(COUNTER),'--root',str(d),'--revision',rev,'--work',str(S/('extra-work-'+label))]
 if base:argv+=['--base',base]
 p=cmd(argv,check=False)
 (S/(label+'.log')).write_text(p.stdout+p.stderr)
 (S/(label+'.SKILL.md')).write_text(git(d,'show',rev+':SKILL.md').stdout)
 return dict(label=label,revision=rev,base=base,command=argv,exit=p.returncode,output=p.stdout+p.stderr)

def mini(label,rows,tools):
 d=pathlib.Path(tempfile.mkdtemp(prefix=label+'-',dir=S))
 git(d,'init','-q');guard(d)
 for name,src in tools.items():
  target=d/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(src)
 (d/'SKILL.md').write_text('# SKILL\n'+section(rows))
 rev=commit(d)
 git(d,'bundle','create',str(S/(label+'.bundle')),'--all')
 return label,d,rev,None

jobs=[]
jobs.append(mini('F13-E4-secondary-missing',[
 row('scripts/ok.py','gate','python3 scripts/ok.py --root .','`python3 scripts/ok.py --selftest` (3/3)','proof names scripts/does_not_exist.py')],
 {'scripts/ok.py':'print("3/3")\n'}))
jobs.append(mini('F14-wrong-command',[
 row('scripts/broken.py','gate','python3 scripts/broken.py --root .','`python3 scripts/other.py --selftest` (3/3)')],
 {'scripts/broken.py':'import sys\nsys.exit(2)\n','scripts/other.py':'print("3/3")\n'}))

base_text=(S/'SKILL.base.md').read_text()
lines=base_text.splitlines(True)
c69=next(l for l in lines if l.startswith('| c69_tmp_honour.py |'))
c74=next(l for l in lines if l.startswith('| c74_registry_gap.py |'))
def relabel(l):
 cells=l.split('|');cells[2]=' instrument (superseding row; offline) ';return '|'.join(cells)
variants={
 'A01-junk':([c69,c74],None),
 'A02-relabel-one':([relabel(c69)],None),
 'A03-new-file':([row('scripts/filler75.py','gate','python3 scripts/filler75.py --root .','`python3 scripts/filler75.py --selftest` (3/3)')], 'scripts/filler75.py'),
 'A04-E4-whole-population':([relabel(c69),row('c74_registry_gap.py','gate','python3 -B .ufo/waves/round-74/c74_registry_gap.py --root .','`python3 -B .ufo/waves/round-74/c74_registry_gap.py --selftest` (8/8)','proof path scripts/does_not_exist.py')],None),
}
for label,(rows,newfile) in variants.items():
 d=pathlib.Path(tempfile.mkdtemp(prefix=label+'-',dir=S))
 cmd(['git','clone','-q','--shared',str(S/'lane-shared'),str(d)])
 guard(d);git(d,'checkout','-q',BASE)
 (d/'SKILL.md').write_text(base_text+section(rows))
 if newfile:(d/newfile).write_text('print("3/3")\n')
 rev=commit(d)
 (S/(label+'.patch')).write_text(git(d,'diff',BASE,rev,'--','SKILL.md',*( [newfile] if newfile else [])).stdout)
 jobs.append((label,d,rev,BASE))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 records=list(pool.map(lambda args:run(*args),jobs))
(S/'additional-results.json').write_text(json.dumps(records,indent=2))
for r in records:print(r['label'], 'exit='+str(r['exit']),r['output'].splitlines()[0])
# Direct evidence that F14's instrument itself fails --selftest (committed bytes).
f14=next(j for j in jobs if j[0]=='F14-wrong-command')
p=cmd(['python3','-B',f14[1]/'scripts/broken.py','--selftest'],check=False)
(S/'F14-direct-selftest.txt').write_text('command=python3 -B scripts/broken.py --selftest\nexit='+str(p.returncode)+'\n')
print('F14 direct instrument selftest exit='+str(p.returncode))
