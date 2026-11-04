import json, os, subprocess, re
from pathlib import Path
S=Path('/fast/scratch/hyaku/kake-r89/ReviewCounterC1'); G=S/'g-git'
L88='corpus/lessons/round-88.md'; L89='corpus/lessons/round-89.md'
def git(*a):
    p=subprocess.run(['git','-C',str(G),*a],capture_output=True,text=True)
    assert p.returncode==0 or a[0] in ('checkout',), p.stderr
    return p.stdout
assert git('rev-parse','--show-toplevel').strip()==str(G)
base=git('show','green:'+L88)
cases=[
 ('BR1-empty-brace-alt', '\nNamed: `.ufo/waves/round-88/controls/{base-c1.txt,}`.\n', 'red: empty alternative names no receipt', 'green (expands to controls/, a git tree, git show is not None)'),
 ('BR2-brace-missing-alt-control', '\nNamed: `.ufo/waves/round-88/controls/{base-c1.txt,nope.txt}`.\n', 'red: nope.txt missing', 'red (control)'),
 ('BR3-trailing-dot-trim-to-other-name', '\nNamed: `.ufo/waves/round-88/controls/base-c1.txt.`\n', 'red: base-c1.txt. (with the dot) does not exist', 'green (rstrip(.) turns it into the existing base-c1.txt)'),
 ('BR4-comma-prose-list-false-red', '\nNamed: .ufo/waves/round-88/controls/base-c1.txt,after-c1-carrier.txt\n', 'green: both receipts exist', 'red (comma is in the class; token base-c1.txt,after-c1-carrier.txt is not a path)'),
]
out=[]
for name, extra, expect, pred in cases:
    git('checkout','-q','-B','exp/'+name,'green')
    (G/L88).write_text(base+extra)
    git('add','-A')
    env=dict(os.environ,GIT_AUTHOR_DATE='2026-11-04T13:00:00Z',GIT_COMMITTER_DATE='2026-11-04T13:00:00Z')
    subprocess.run(['git','-C',str(G),'commit','-qm',name],check=True,env=env,capture_output=True)
    rev=git('rev-parse','HEAD').strip()
    p=subprocess.run(['python3','-B',str(S/'counters'/'c89_defect_queue.py'),'--root',str(G),'--revision',rev,'--work',str(S/'w'/name)],capture_output=True,text=True,cwd=str(S))
    (S/'receipts'/f'{name}.txt').write_text(f'$ --revision {rev} (branch exp/{name})\n# exit={p.returncode}\n'+p.stdout+p.stderr)
    lines=p.stdout.splitlines()
    items=json.loads(lines[1]) if len(lines)>1 else {}
    out.append({'name':name,'exit':p.returncode,'summary':lines[0] if lines else '', 'C':items.get('C-receipt-pointers'),'expect':expect,'predicted':pred})
    git('checkout','-q','--detach','green')
for o in out: print(json.dumps(o,sort_keys=True))
