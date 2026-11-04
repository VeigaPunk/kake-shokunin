#!/usr/bin/env python3
"""ScoutVary: does the counter's TOKEN check accept a Vary member carrying a
trailing LF? RFC 9110 5.6.2 token = 1*tchar (no LF); RFC 9110 5.5 says a field
value containing CR, LF or NUL is invalid and a recipient MUST reject it or
replace it with SP. Python's re.match + '$' accepts a trailing newline.

Then: does the strict reading (fullmatch, or an explicit LF/CR/NUL refusal)
score differently against the frozen 20 + seeded 200?"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
SCRATCH = Path('/fast/scratch/hyaku/kake-r88/ScoutVary')
CTR = LANE / '.ufo/waves/round-88/c88_vary.py'
spec = importlib.util.spec_from_file_location('ctr', CTR)
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)

print("reference TOKEN.match('gzip\\n')      ->", bool(ctr.TOKEN.match('gzip\n')))
print("reference is_token('gzip\\n')         ->", ctr.is_token('gzip\n'))
print("reference('gzip\\n', ...) verdict     ->",
      ctr.reference('gzip\n', {'gzip': 'v'}, {'gzip': 'v'}))
print("reference('gzip\\r', ...) verdict     ->",
      ctr.reference('gzip\r', {'gzip': 'v'}, {'gzip': 'v'}))

STRICT = r'''#!/usr/bin/env python3
import json, re, sys
TOKEN = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")
OWS = " \t"
def is_token(t):
    return isinstance(t, str) and bool(TOKEN.fullmatch(t))
def ref(vary, stored, presented):
    if not isinstance(vary, str):
        return 'invalid'
    members = [m.strip(OWS) for m in vary.split(',')]
    if not members or any(m == '' for m in members):
        return 'invalid'
    names, star = [], False
    for m in members:
        if m == '*':
            star = True
        elif is_token(m):
            names.append(m.lower())
        else:
            return 'invalid'
    def norm(side):
        if not isinstance(side, dict):
            return None
        out = {}
        for k, v in side.items():
            if not is_token(k):
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
p = SCRATCH / 'strict_token.py'
p.write_text(STRICT)
r = subprocess.run([sys.executable, '-B', str(CTR), '--tool', str(p),
                    '--work', str(SCRATCH / 'work' / 'strict')],
                   capture_output=True, text=True, cwd=str(SCRATCH))
d = json.loads(r.stdout)
print('strict-token reader scored:',
      {k: d.get(k) for k in ('frozen', 'frozen_total', 'random', 'random_total', 'met')})
print('  details (first 4):', d.get('details')[:4] if d.get('details') else [])

# does the L1 candidate inherit the LF acceptance?
l1 = LANE / '.ufo/waves/round-88/w1/L1/vary_match.py'
q = subprocess.run([sys.executable, '-B', str(l1)],
                   input=json.dumps({'vary': 'accept-encoding\n',
                                     'stored': {'accept-encoding': 'gzip'},
                                     'presented': {'accept-encoding': 'gzip'}}),
                   capture_output=True, text=True)
print('L1 candidate on a Vary member with trailing LF -> exit', q.returncode,
      'stdout', repr(q.stdout.strip()), 'stderr', repr(q.stderr.strip()[:40]))
