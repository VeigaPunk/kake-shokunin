#!/usr/bin/env python3
"""mutc1_hard.py — mutation-test the hardened C1 counter (lane working tree)."""
import hashlib, json, os, shutil, subprocess, sys
HERE='/fast/scratch/hyaku/kake-r75/MutationTesterC2'
SRC=os.environ.get('C1HARD', os.path.join(HERE,'work','c1hard','c75_hard.py'))
WORK=os.path.join(HERE,'work','c1hard','mut')
MUTANTS=[
 ('H-M1','drop the append_only conjunct','append-only',
  "    append_only = True\n    if base:", "    append_only = True\n    if base and False:"),
 ('H-M2','first-row-wins (superseded row stays effective)','supersession',
  "        row = groups[f][-1]", "        row = groups[f][0]"),
 ('H-M3','ignore E3 (enumerated fixture ids)','E3',
  "        ids = {int(x) for x in FIX_RE.findall(selftest_cell)}", "        ids = set()"),
 ('H-M4','parse the tally from the whole cell, not the claim segment','E2',
  "    pairs = PAIR_RE.findall(region.split(';')[0])", "    pairs = PAIR_RE.findall(cell)"),
 ('H-M5','accept a command that exits 0 without printing its claimed tally','E2',
  "                elif not obs:\n                    findings.append(f'E2 {f}: cell claims {pair[0]}/{pair[1]}, '\n                                    f'no tally in output')\n                    entry['mismatch'] = 'E2'",
  "                elif not obs:\n                    pass"),
 ('H-M6','treat the word differential anywhere in the row as the exemption','E1',
  "        differential = declares_differential(kind)",
  "        differential = declares_differential(' '.join(row['cells']))"),
 ('H-M7','skip E1 entirely','E1',
  "        if fam == 'gate':", "        if fam == 'gate' and False:"),
 ('H-M8','check E4 only on the instrument file','E4',
  "        tokens = sorted(set(FILE_RE.findall(' '.join(row['cells']))))",
  "        tokens = sorted({row['file']} if row.get('file') else set())"),
]
def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)
src=open(SRC).read()
out={'src':SRC,'sha256':hashlib.sha256(src.encode()).hexdigest(),'mutants':[]}
base=run([sys.executable,'-B',SRC,'--selftest','--work',os.path.join(WORK,'pristine')])
print('pristine selftest exit',base.returncode, base.stdout.strip().splitlines()[-1] if base.stdout else '')
for mid,name,dim,old,new in MUTANTS:
    if old not in src:
        print(mid,'ANCHOR MISSING'); out['mutants'].append({'id':mid,'error':'anchor missing'}); continue
    d=os.path.join(WORK,mid); os.makedirs(d,exist_ok=True)
    path=os.path.join(d,'c75_row_truth.py')
    open(path,'w').write(src.replace(old,new,1))
    p=run([sys.executable,'-B',path,'--selftest','--work',os.path.join(d,'st')])
    failed=[ln.split('FAIL ',1)[1].split(' ::')[0] for ln in p.stdout.splitlines() if 'FAIL ' in ln]
    rec={'id':mid,'mutation':name,'dimension':dim,'exit':p.returncode,
         'failed_cases':failed,'tail':[ln for ln in p.stdout.splitlines() if ln.startswith('C1v1 selftest')][-1:]}
    out['mutants'].append(rec)
    print(mid,'exit',p.returncode,'failed',failed[:6])
json.dump(out,open(os.path.join(HERE,'work','c1hard-results.json'),'w'),indent=2)
print('wrote work/c1hard-results.json')
