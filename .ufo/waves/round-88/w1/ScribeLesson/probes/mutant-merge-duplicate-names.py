import json, sys
# Mutant A: merge duplicate case-insensitive names in a header map (last wins)
# instead of refusing them.
def norm(side):
    if not isinstance(side, dict): return None
    out = {}
    for k, v in side.items():
        low = k.lower()
        if isinstance(v, str): out[low] = v
        elif isinstance(v, list) and v and all(isinstance(x, str) for x in v): out[low] = ', '.join(v)
        else: return None
    return out
TOKEN = set("!#$%&'*+-.^_`|~0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
def tok(s): return isinstance(s, str) and s != '' and all(c in TOKEN for c in s)
p = json.load(sys.stdin)
vary = p['vary']
if not isinstance(vary, str): sys.stderr.write('invalid_input: x\n'); sys.exit(1)
members = [m.strip(' \t') for m in vary.split(',')]
if any(m == '' for m in members): sys.stderr.write('invalid_input: x\n'); sys.exit(1)
names, star = [], False
for m in members:
    if m == '*': star = True
    elif tok(m): names.append(m.lower())
    else: sys.stderr.write('invalid_input: x\n'); sys.exit(1)
a, b = norm(p['stored']), norm(p['presented'])
if a is None or b is None: sys.stderr.write('invalid_input: x\n'); sys.exit(1)
if star: print('mismatch'); sys.exit(0)
for n in set(names):
    l, r = a.get(n), b.get(n)
    if l is None and r is None: continue
    if l is None or r is None: print('mismatch'); sys.exit(0)
    if l.strip(' \t') != r.strip(' \t'): print('mismatch'); sys.exit(0)
print('match')
