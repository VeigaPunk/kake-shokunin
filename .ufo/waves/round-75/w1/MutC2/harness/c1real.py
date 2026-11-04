#!/usr/bin/env python3
"""c1real.py — run every C1 mutant against the REAL lane base measurement."""
import json, os, re, subprocess, sys
HERE = '/fast/scratch/hyaku/kake-r75/MutationTesterC2'
LANE = '/home/vgpnk/Projects/shokunin/kake-shokunin'
COUNTER = os.path.join(LANE, '.ufo/waves/round-75/c75_row_truth.py')
BASE = 'c9c5e484c533aa65f4374b841a3edcf572ed19a9'
WORK = os.path.join(HERE, 'c1base')
out = {'base': BASE, 'runs': []}

def measure(tool):
    p = subprocess.run([sys.executable, '-B', tool, '--root', LANE, '--revision', BASE,
                        '--base', BASE, '--work', WORK], capture_output=True, text=True,
                       env={**os.environ, 'TMPDIR': os.path.join(HERE, 'tmp')})
    line = next((ln for ln in p.stdout.splitlines() if ln.startswith('C1v1 ')), '')
    fields = dict(kv.split('=', 1) for kv in line.split() if '=' in kv)
    return {'exit': p.returncode, 'line': line,
            'mismatches': int(fields['mismatches']) if 'mismatches' in fields else None,
            'met': fields.get('met') == 'true',
            'append_only': fields.get('append_only') == 'true',
            'classes': fields.get('classes')}

out['runs'].append({'id': 'pristine', 'measured': measure(COUNTER)})
mutdir = os.path.join(HERE, 'work', 'c1mut', 'mut')
for mid in sorted(os.listdir(mutdir)):
    tool = os.path.join(mutdir, mid, 'c75_row_truth.py')
    if not os.path.isfile(tool):
        continue
    out['runs'].append({'id': mid, 'measured': measure(tool)})
    print(mid, out['runs'][-1]['measured'], flush=True)
with open(os.path.join(HERE, 'work', 'c1real-results.json'), 'w') as fh:
    json.dump(out, fh, indent=2)
print('done')
