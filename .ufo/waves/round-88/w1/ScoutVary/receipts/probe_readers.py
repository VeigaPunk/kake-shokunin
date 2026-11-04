#!/usr/bin/env python3
"""ScoutVary: (a) test the counter's TOKEN regex against a Vary member that
carries a trailing LF (RFC 9110 5.6.2 token vs 5.5 CR/LF rules);
(b) score an RFC 9110 5.6.1.2-conformant reader (empty list elements ignored)
against the frozen counter to show what the counter penalises;
(c) score the L1 candidate committed at v3."""
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
SCRATCH = Path('/fast/scratch/hyaku/kake-r88/ScoutVary')

TOKEN = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")
print('--- (a) TOKEN regex vs a member carrying a trailing LF ---')
for cand in ['gzip', 'gzip\n', 'gzip\r\n', 'gzip\nbr', 'gz\nip']:
    print(f'   TOKEN.match({cand!r}) = {bool(TOKEN.match(cand))}')

spec = importlib.util.spec_from_file_location('ctr', LANE / '.ufo/waves/round-88/c88_vary.py')
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)
print('   reference("gzip\\n", ...) =',
      ctr.reference('gzip\n', {'gzip': 'v'}, {'gzip': 'v'}))

# (b) RFC 9110 5.6.1.2 conformant reader: ignore empty list elements
ALT = r'''#!/usr/bin/env python3
import json, re, sys
TOKEN = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")
OWS = " \t"
def ref(vary, stored, presented):
    if not isinstance(vary, str):
        return 'invalid'
    members = [m.strip(OWS) for m in vary.split(',') if m.strip(OWS) != '']
    if not members:
        return 'match'          # empty list: nothing nominated
    names, star = [], False
    for m in members:
        if m == '*':
            star = True
        elif TOKEN.match(m):
            names.append(m.lower())
        else:
            return 'invalid'
    def norm(side):
        if not isinstance(side, dict):
            return None
        out = {}
        for k, v in side.items():
            if not isinstance(k, str) or not TOKEN.match(k):
                return None
            low = k.lower()
            if low in out:
                return None
            if isinstance(v, str):
                out[low] = v
            elif isinstance(v, list) and v and all(isinstance(x, str) for x in v):
                out[low] = ', '.join(v)
            else:
                return None
        return out
    a, b = norm(stored), norm(presented)
    if a is None or b is None:
        return 'invalid'
    if star:
        return 'mismatch'
    for n in set(names):
        l, r = a.get(n), b.get(n)
        if l is None and r is None:
            continue
        if l is None or r is None:
            return 'mismatch'
        if l.strip(OWS) != r.strip(OWS):
            return 'mismatch'
    return 'match'
p = json.loads(sys.stdin.read())
v = ref(p['vary'], p['stored'], p['presented'])
if v == 'invalid':
    sys.stderr.write('invalid_input: refused\n'); sys.exit(1)
sys.stdout.write(v + '\n')
'''
alt_path = SCRATCH / 'alt_5612.py'
alt_path.write_text(ALT)

def score(tool):
    with tempfile.TemporaryDirectory(dir=str(SCRATCH)) as d:
        work = Path(d)
        f, det = ctr.score(Path(tool).read_bytes(), work / 's', ctr.CASES)
        r, detr = ctr.score(Path(tool).read_bytes(), work / 'r', ctr.RANDOM_CASES)
        return f, r, det, detr

for label, tool in [('RFC9110-5.6.1.2 reader (empty elements ignored)', alt_path),
                    ('L1 candidate committed at v3', LANE / '.ufo/waves/round-88/w1/L1/vary_match.py')]:
    f, r, det, detr = score(tool)
    print(f'--- (b/c) {label} ---')
    print(f'   frozen {f}/20  random {r}/200')
    print('   frozen failures:', det[:6])
    print('   random failures (first 6):', detr[:6])
