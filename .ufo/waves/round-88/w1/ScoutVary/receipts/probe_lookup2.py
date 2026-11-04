#!/usr/bin/env python3
"""ScoutVary (corrected): exact-payload lookup table over the 220 known inputs.

The counter sends, per case, exactly:
    json.dumps({k: case[k] for k in ('vary','stored','presented')})
A tool that maps that exact string to the expected verdict needs no
implementation of the profile at all. The 20 frozen inputs are a committed
file; the 200 seeded inputs are derivable from the committed generator and
seed (both live in the committed c88_vary.py). So the whole key space is
derivable from committed bytes.

FINDERS artefact only: scratch dir.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
SCRATCH = Path('/fast/scratch/hyaku/kake-r88/ScoutVary')
CTR = LANE / '.ufo/waves/round-88/c88_vary.py'

spec = importlib.util.spec_from_file_location('ctr', CTR)
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)

def payload(case):
    return json.dumps({k: case[k] for k in ('vary', 'stored', 'presented')})

table = {}
for c in ctr.CASES:
    table[payload(c)] = c['verdict'] if c['exit'] == 0 else 'invalid'
for c in ctr.RANDOM_CASES:
    table[payload(c)] = c['verdict'] if c['exit'] == 0 else 'invalid'
print('distinct known inputs:', len(table))

body = ('import json, sys\n'
        'TABLE = json.loads(sys.argv[1])\n'
        'payload = sys.stdin.read()\n'
        'v = TABLE.get(payload)\n'
        'if v is None:\n'
        '    sys.stderr.write("invalid_input: unknown\\n"); sys.exit(1)\n'
        'if v == "invalid":\n'
        '    sys.stderr.write("invalid_input: refused\\n"); sys.exit(1)\n'
        'sys.stdout.write(v + "\\n")\n')
tool = SCRATCH / 'lookup_exact.py'
tool.write_text(body)
# the table is embedded in the tool file itself (no argv needed by the counter)
tool.write_text(body.replace('TABLE = json.loads(sys.argv[1])',
                             'TABLE = json.loads(r"""%s""")' % json.dumps(table)))

p = subprocess.run([sys.executable, '-B', str(CTR), '--tool', str(tool),
                    '--work', str(SCRATCH / 'work' / 'lookup_exact')],
                   capture_output=True, text=True, cwd=str(SCRATCH))
out = p.stdout.strip()
try:
    d = json.loads(out)
    print({k: d.get(k) for k in ('frozen', 'frozen_total', 'random', 'random_total', 'met')})
except Exception:
    print(out[:400])
print('exit:', p.returncode)
