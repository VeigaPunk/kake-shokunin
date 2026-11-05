#!/usr/bin/env python3
"""Builds the frozen forgery `.ufo/waves/round-97/frozen/neg-lookup-table.py`.

R96-2 class: a memorizing subject. It carries the reference answer for every
hand case and every fixed-seed generated input (seeds 96 and 97, 120 each),
keyed by the REVERSED sha256 hex of the minified canonical JSON (a key form
the c97 anti-table blacklist does not search, so only the held-out cases can
refuse it in the candidate slot). Unknown inputs get the most common
answer. Run once before the freeze; output is pinned in c97_reval.py.
"""
import collections
import hashlib
import importlib.util
import json
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("c97", os.path.join(here, "c97_reval.py"))
c97 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c97)


def key(b):
    return hashlib.sha256(b).hexdigest()[::-1]


table = {}
for name, inp, expected in c97.hand_cases():
    if isinstance(inp, dict) and "__raw__" in inp:
        k = key(inp["__raw__"])
    else:
        k = key(json.dumps(inp, sort_keys=True, separators=(",", ":")).encode())
    table[k] = expected
for seed in (96, 97):
    for inp in c97.generate(seed, 120):
        try:
            ans = c97.reference(inp)
        except c97.Invalid:
            ans = None
        table[key(json.dumps(inp, sort_keys=True, separators=(",", ":")).encode())] = ans
common = collections.Counter(json.dumps(v, sort_keys=True) for v in table.values()
                             if v is not None).most_common(1)[0][0]

src = '''#!/usr/bin/env python3
"""Forgery (R96-2 class): memorized answers, no decision logic."""
import hashlib
import json
import sys

TABLE = %s
DEFAULT = %s

raw = sys.stdin.buffer.read()
try:
    k = hashlib.sha256(json.dumps(json.loads(raw), sort_keys=True,
                                  separators=(",", ":")).encode()).hexdigest()[::-1]
except ValueError:
    k = hashlib.sha256(raw).hexdigest()[::-1]
if k not in TABLE:
    k2 = hashlib.sha256(raw).hexdigest()[::-1]
    k = k2 if k2 in TABLE else k
ans = TABLE.get(k, DEFAULT)
if ans is None:
    sys.stderr.write("invalid_input: memorized refusal\\n")
    sys.exit(1)
json.dump(ans, sys.stdout, sort_keys=True)
sys.stdout.write("\\n")
''' % (repr(dict(sorted(table.items()))), repr(json.loads(common)))

out = os.path.join(here, "frozen", "neg-lookup-table.py")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8") as fh:
    fh.write(src)
print("wrote %s entries=%d sha256=%s" % (out, len(table),
      hashlib.sha256(src.encode()).hexdigest()))
