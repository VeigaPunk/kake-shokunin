#!/usr/bin/env python3
"""ScoutVary: per-case comparison of the L1 candidate against the v2 and v3
reference verdicts — does the v3 freeze amendment flip exactly the cases where
the already-authored candidate disagreed with the v2 oracle?"""
import importlib.util
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
SCRATCH = Path('/fast/scratch/hyaku/kake-r88/ScoutVary')

def load(tag, rev):
    out = SCRATCH / f'cmp_{tag}.py'
    out.write_bytes(subprocess.check_output(
        ['git', '-C', str(LANE), 'show', f'{rev}:.ufo/waves/round-88/c88_vary.py']))
    s = importlib.util.spec_from_file_location(f'cmp_{tag}', out)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

v2 = load('v2', '80637397')
v3 = load('v3', '52e41d2d')

L1 = LANE / '.ufo/waves/round-88/w1/L1/vary_match.py'

def run_candidate(case):
    payload = json.dumps({k: case[k] for k in ('vary', 'stored', 'presented')})
    p = subprocess.run([sys.executable, '-B', str(L1)], input=payload,
                       capture_output=True, text=True, timeout=20)
    if p.returncode == 1:
        return 'invalid'
    return p.stdout.strip()

import json
diff_v2 = []
diff_v3 = []
for c in v3.RANDOM_CASES:
    cand = run_candidate(c)
    r2 = v2.reference(c['vary'], c['stored'], c['presented'])
    r3 = v3.reference(c['vary'], c['stored'], c['presented'])
    if cand != r2:
        diff_v2.append((c['id'], r2, r3, cand))
    if cand != r3:
        diff_v3.append((c['id'], r2, r3, cand))

print('seeded cases where the L1 candidate disagrees with the v2 reference:',
      len(diff_v2))
for d in diff_v2:
    print('   id=%s v2=%s v3=%s candidate=%s' % d)
print('seeded cases where the L1 candidate disagrees with the v3 reference:',
      len(diff_v3))
print('v2->v3 label flips (reference side):')
for c in v3.RANDOM_CASES:
    r2 = v2.reference(c['vary'], c['stored'], c['presented'])
    r3 = v3.reference(c['vary'], c['stored'], c['presented'])
    if r2 != r3:
        print('   id=%s v2=%s v3=%s' % (c['id'], r2, r3))
