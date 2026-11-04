#!/usr/bin/env python3
"""Build C2 attack stubs from the committed counter's own frozen + seeded cases."""
import hashlib
import importlib.util
import json
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
OUT = Path('/fast/scratch/hyaku/kake-r88/CriticClaims/stubs')
OUT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('c88', LANE / '.ufo/waves/round-88/c88_vary.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def payload(case):
    return json.dumps({k: case[k] for k in ('vary', 'stored', 'presented')})


def table(cases):
    rows = {}
    for c in cases:
        h = hashlib.sha256(payload(c).encode()).hexdigest()
        rows[h] = (c['exit'], c['verdict'])
    return rows


def emit_lookup(path, rows, fallback):
    body = ['#!/usr/bin/env python3',
            'import hashlib, json, sys',
            'TABLE = ' + repr(rows),
            'raw = sys.stdin.buffer.read()',
            'h = hashlib.sha256(raw).hexdigest()',
            'if h in TABLE:',
            '    code, verdict = TABLE[h]',
            '    if code:',
            '        sys.stderr.write("invalid_input: canned refusal\\n")',
            '        raise SystemExit(1)',
            '    sys.stdout.write(verdict + "\\n")',
            '    raise SystemExit(0)',
            ]
    if fallback == 'mismatch':
        body += ['sys.stdout.write("mismatch\\n")', 'raise SystemExit(0)']
    else:
        body += ['raise SystemExit(2)']
    path.write_text('\n'.join(body) + '\n')


emit_lookup(OUT / 'lookup20_exit2.py', table(m.CASES), 'exit2')
emit_lookup(OUT / 'lookup20_bestconst.py', table(m.CASES), 'mismatch')
emit_lookup(OUT / 'lookup220.py', table(list(m.CASES) + list(m.RANDOM_CASES)), 'exit2')

(OUT / 'oracle_import.py').write_text('''#!/usr/bin/env python3
"""No profile implementation: delegate to the committed counter's reference()."""
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location(
    'c88', '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/c88_vary.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
c = json.load(sys.stdin)
v = m.reference(c.get('vary'), c.get('stored'), c.get('presented'))
if v == 'invalid':
    sys.stderr.write('invalid_input: delegated reference refused\\n')
    raise SystemExit(1)
print(v)
''')

# Cheap heuristics ---------------------------------------------------------
(OUT / 'heur_star_substring.py').write_text('''#!/usr/bin/env python3
"""Trivial rule: the literal '*' anywhere in stdin decides mismatch."""
import sys
raw = sys.stdin.read()
print('mismatch' if '*' in raw else 'match')
''')

(OUT / 'heur_exact_eq.py').write_text('''#!/usr/bin/env python3
"""Trivial rule: match iff the two JSON objects are byte-equal in Python."""
import json, sys
c = json.load(sys.stdin)
print('match' if c.get('stored') == c.get('presented') else 'mismatch')
''')

(OUT / 'heur_naive_iface.py').write_text('''#!/usr/bin/env python3
"""Naive reader: name-case + presence + exact value equality; no OWS/list handling."""
import json, sys
TOKEN = set("!#$%&'*+-.^_`|~0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
c = json.load(sys.stdin)
v = c.get('vary')
if not isinstance(v, str):
    sys.stderr.write('invalid_input: vary not a string\\n'); raise SystemExit(1)
members = [x.strip(' \\t') for x in v.split(',')]
if not members or any(x == '' for x in members):
    sys.stderr.write('invalid_input: empty Vary member\\n'); raise SystemExit(1)
names = []
for x in members:
    if x == '*':
        print('mismatch'); raise SystemExit(0)
    if not all(ch in TOKEN for ch in x):
        sys.stderr.write('invalid_input: non-token member\\n'); raise SystemExit(1)
    names.append(x.lower())
a = {k.lower(): x for k, x in c['stored'].items()}
b = {k.lower(): x for k, x in c['presented'].items()}
for n in names:
    x, y = a.get(n), b.get(n)
    if (x is None) != (y is None):
        print('mismatch'); raise SystemExit(0)
    if x is not None and x != y:
        print('mismatch'); raise SystemExit(0)
print('match')
''')

# Two spec-compatible alternatives, used to test reference/spec drift -------
(OUT / 'alt_validate_first.py').write_text('''#!/usr/bin/env python3
"""Declared profile, but validate both requests before the '*' short-circuit."""
import json, sys
sys.path.insert(0, '/fast/scratch/hyaku/kake-r88/CriticClaims')
from alt_common import reference_variant
c = json.load(sys.stdin)
v = reference_variant(c.get('vary'), c.get('stored'), c.get('presented'),
                      empty_list='invalid', validate_first=True)
if v == 'invalid':
    sys.stderr.write('invalid_input: refused\\n'); raise SystemExit(1)
print(v)
''')
(OUT / 'alt_empty_list.py').write_text('''#!/usr/bin/env python3
"""Declared profile, reading a zero-line list as the empty combined value."""
import json, sys
sys.path.insert(0, '/fast/scratch/hyaku/kake-r88/CriticClaims')
from alt_common import reference_variant
c = json.load(sys.stdin)
v = reference_variant(c.get('vary'), c.get('stored'), c.get('presented'),
                      empty_list='empty', validate_first=False)
if v == 'invalid':
    sys.stderr.write('invalid_input: refused\\n'); raise SystemExit(1)
print(v)
''')

(OUT.parent / 'alt_common.py').write_text('''"""Two declared-profile readings that differ only where the frozen 20 are silent."""
TOKEN = set("!#$%&'*+-.^_`|~0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")


def token(s):
    return isinstance(s, str) and s != '' and all(ch in TOKEN for ch in s)


def reference_variant(vary, stored, presented, empty_list='invalid', validate_first=False):
    if not isinstance(vary, str):
        return 'invalid'
    members = [x.strip(' \\t') for x in vary.split(',')]
    if not members or any(x == '' for x in members):
        return 'invalid'
    names, star = [], False
    for x in members:
        if x == '*':
            star = True
        elif token(x):
            names.append(x.lower())
        else:
            return 'invalid'

    def norm(side):
        if not isinstance(side, dict):
            return None
        out = {}
        for key, value in side.items():
            if not token(key):
                return None
            low = key.lower()
            if low in out:
                return None
            if isinstance(value, str):
                out[low] = value
            elif isinstance(value, list):
                if not all(isinstance(x, str) for x in value):
                    return None
                if not value and empty_list == 'invalid':
                    return None
                out[low] = ', '.join(value)
            else:
                return None
        return out

    a, b = norm(stored), norm(presented)
    if validate_first and (a is None or b is None):
        return 'invalid'
    if star:
        return 'mismatch'
    if a is None or b is None:
        return 'invalid'
    for name in set(names):
        left, right = a.get(name), b.get(name)
        if left is None and right is None:
            continue
        if left is None or right is None:
            return 'mismatch'
        if left.strip(' \\t') != right.strip(' \\t'):
            return 'mismatch'
    return 'match'
''')

print(json.dumps({'stubs': sorted(p.name for p in OUT.iterdir()),
                  'frozen_table': len(table(m.CASES)),
                  'all_table': len(table(list(m.CASES) + list(m.RANDOM_CASES)))}, sort_keys=True))
