#!/usr/bin/env python3
"""ScoutVary: can a lookup table keyed on the *known* inputs pass the frozen
C2 counter? The counter's generator and seed are committed in the lane, so the
seeded population is derivable from committed bytes; the frozen 20 are a
committed file. This builds a table from exactly those committed sources and
scores it with the committed counter.

FINDERS artefact only: lives in this seat's scratch dir.
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

TOOL = SCRATCH / 'lookup_table.py'
TOOL.write_text('''#!/usr/bin/env python3
import json, sys
TABLE = json.loads(sys.argv[1])
p = json.dumps(json.loads(sys.stdin.read()), sort_keys=True)
v = TABLE.get(p)
if v is None:
    sys.stderr.write("invalid_input: unknown\\n"); sys.exit(1)
if v == "invalid":
    sys.stderr.write("invalid_input: refused\\n"); sys.exit(1)
sys.stdout.write(v + "\\n")
''')

# the table must be keyed on the exact payload the counter sends
tool_bytes = ('import json, sys\n'
              'TABLE = json.loads(sys.stdin.read().split("\\n", 1)[1])\n'
              'line = sys.stdin.readline()\n'
              'payload = json.dumps(json.loads(line), sort_keys=True)\n'
              'v = TABLE.get(payload)\n'
              'if v is None:\n'
              '    sys.stderr.write("invalid_input: unknown\\n"); sys.exit(1)\n'
              'if v == "invalid":\n'
              '    sys.stderr.write("invalid_input: refused\\n"); sys.exit(1)\n'
              'sys.stdout.write(v + "\\n")\n').encode()

def make_tool(table_map):
    body = ('import json, sys\n'
            'TABLE = %r\n'
            'payload = sys.stdin.read()\n'
            'key = json.dumps(json.loads(payload), sort_keys=True)\n'
            'v = TABLE.get(key)\n'
            'if v is None:\n'
            '    sys.stderr.write("invalid_input: unknown\\n"); sys.exit(1)\n'
            'if v == "invalid":\n'
            '    sys.stderr.write("invalid_input: refused\\n"); sys.exit(1)\n'
            'sys.stdout.write(v + "\\n")\n') % (table_map,)
    return body.encode()

tool = SCRATCH / 'lookup220.py'
tool.write_bytes(make_tool(table))
print('table entries:', len(table))

p = subprocess.run([sys.executable, '-B', str(CTR), '--tool', str(tool),
                    '--work', str(SCRATCH / 'work' / 'lookup')],
                   capture_output=True, text=True, cwd=str(SCRATCH))
print('stdout:', p.stdout.strip()[:400])
print('exit:', p.returncode)
