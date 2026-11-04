import re, subprocess, sys
REV='2e700b9a94a3c8ce3c0d6b1cc9e84e7b17eee683'
LANE='/home/vgpnk/Projects/shokunin/kake-shokunin'
def show(p): return subprocess.run(['git','-C',LANE,'show',f'{REV}:{p}'],capture_output=True,text=True).stdout
def expand(tok):
    m=re.search(r'\{([^{}]*)\}',tok)
    if not m: return [tok]
    out=[]
    for alt in m.group(1).split(','): out+=expand(tok[:m.start()]+alt+tok[m.end():])
    return out
def exists(p): return subprocess.run(['git','-C',LANE,'cat-file','-e',f'{REV}:{p}'],capture_output=True).returncode==0
card=show('SCORECARD.md').splitlines()
s=next(i for i,l in enumerate(card) if l.startswith('## Round 88'))
e=next((i for i in range(s+1,len(card)) if card[i].startswith('## ')), len(card))
sec88='\n'.join(card[s:e]); lesson=show('corpus/lessons/round-88.md')
tokens={}
for label,text in (('SCORECARD-r88-section',sec88),('round-88-lesson',lesson)):
    for m in re.finditer(r'((?:\.ufo/waves/round-88/)?controls/[A-Za-z0-9._/,{}-]+)', text):
        for t in expand(m.group(1).rstrip('.,;:')): tokens.setdefault(t,set()).add(label)
full=[t for t in tokens if t.startswith('.ufo/waves/round-88/')]
short=[t for t in tokens if not t.startswith('.ufo/waves/round-88/')]
print(f'rev={REV} scorecard_r88_lines={s+1}-{e} unique_named={len(tokens)} counter_checked_full_prefix={len(full)} unchecked_short_form={len(short)}')
print('short-form not resolving under .ufo/waves/round-88/:', [t for t in sorted(short) if not exists('.ufo/waves/round-88/'+t)])
print('full-prefix not resolving:', [t for t in sorted(full) if not exists(t)])
for t in sorted(tokens): print(('FULL ' if t in full else 'SHORT'), t, sorted(tokens[t]), 'exists' if exists(t if t in full else '.ufo/waves/round-88/'+t) else 'MISSING')
