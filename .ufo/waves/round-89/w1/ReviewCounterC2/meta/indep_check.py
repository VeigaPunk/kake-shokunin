#!/usr/bin/env python3
"""ReviewCounterC2 (a): independent re-derivation of the seven contract worked examples.

`hand` holds the expected keys typed from the hand derivation in the review.
`indep` is written from the contract prose and shares no code with the counter's
REFERENCE. Run from a directory holding the frozen counter at round-89/c89_key.py
(the scratch copy used in the review; any copy of the freeze-commit counter works).
Invoke: python3 -B indep_check.py /path/to/round-89/c89_key.py
"""
import importlib.util
import sys

spec = importlib.util.spec_from_file_location('kc', sys.argv[1])
kc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kc)

US, RS, GS = '\x1f', '\x1e', '\x1c'
hand = {
    1: 'https://e.test/a',
    2: 'https://e.test/a' + US + 'accept-encoding' + RS + 'gzip',
    3: 'https://e.test/a' + US + 'accept' + RS + 'text/html' + US + 'accept-encoding' + RS + 'gzip',
    4: 'https://e.test/a' + US + 'a' + RS + '50%25',
    5: 'https://e.test/a' + US + 'a' + RS + 'x%1Fb%1Ey',
    6: 'https://e.test/a' + US + 'accept-encoding' + RS,
    7: 'https://e.test/a' + US + 'accept-encoding' + RS + GS,
}
inputs = {
    1: {'uri': 'https://e.test/a', 'request_headers': {}},
    2: {'uri': 'https://e.test/a', 'request_headers': {'Accept-Encoding': 'gzip'}, 'vary': 'Accept-Encoding'},
    3: {'uri': 'https://e.test/a', 'request_headers': {'accept-encoding': 'gzip', 'Accept': 'text/html'},
        'vary': ' Accept ,Accept-Encoding '},
    4: {'uri': 'https://e.test/a', 'request_headers': {'a': '50%'}, 'vary': 'a'},
    5: {'uri': 'https://e.test/a', 'request_headers': {'a': 'x\x1fb\x1ey'}, 'vary': 'a'},
    6: {'uri': 'https://e.test/a', 'request_headers': {'Accept-Encoding': ''}, 'vary': 'Accept-Encoding'},
    7: {'uri': 'https://e.test/a', 'request_headers': {}, 'vary': 'Accept-Encoding'},
}


def indep(o):
    def esc(s):
        return ''.join({'%': '%25', GS: '%1C', '\x1d': '%1D', RS: '%1E', US: '%1F'}.get(ch, ch) for ch in s)
    vary = o.get('vary', '')
    names = [] if vary == '' else sorted(m.strip(' \t').lower() for m in vary.split(','))
    hdr = {k.lower(): v for k, v in o['request_headers'].items()}
    parts = [esc(n) + RS + (esc(hdr[n].strip(' \t')) if n in hdr else GS) for n in names]
    return esc(o['uri']) + (US + US.join(parts) if parts else '')


ok = True
for i in range(1, 8):
    ind = indep(inputs[i]) == hand[i]
    ref = kc.key_of(inputs[i]) == hand[i]
    ok = ok and ind and ref
    print(f'example {i}: independent==hand {ind}  reference==hand {ref}')
print('ALL AGREE' if ok else 'DISAGREEMENT')
