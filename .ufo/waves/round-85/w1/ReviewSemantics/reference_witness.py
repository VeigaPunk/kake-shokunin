#!/usr/bin/env python3
"""Independent, hand-expected frozen-contract witnesses; no candidate imports."""
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
OUT = ROOT / '.ufo/waves/round-85/w1/ReviewSemantics'
VALID = ('no-referrer', 'no-referrer-when-downgrade', 'same-origin', 'origin', 'strict-origin', 'origin-when-cross-origin', 'strict-origin-when-cross-origin', 'unsafe-url')

def reference(fields):
    if not isinstance(fields, list) or any(not isinstance(field, str) for field in fields):
        raise ValueError('JSON list of strings required')
    # Reverse search is independent of the spec's forward assignment formulation.
    for field in reversed(fields):
        for token in reversed(field.split(',')):
            if token.strip() in VALID:
                return token.strip()
    return ''

cases = [(f'token-{token}', [token], token) for token in VALID]
cases += [
    ('forward', ['no-referrer, strict-origin'], 'strict-origin'),
    ('reverse', ['strict-origin, no-referrer'], 'no-referrer'),
    ('multiple-fields', ['no-referrer', 'unsafe-url'], 'unsafe-url'),
    ('multiple-fields-reverse', ['unsafe-url', 'no-referrer'], 'no-referrer'),
    ('unknown-after-valid', ['same-origin, future-policy'], 'same-origin'),
    ('unknown-before-valid', ['future-policy, origin'], 'origin'),
    ('empty-fields', [], ''), ('empty-string', [''], ''),
    ('empty-tokens', [', ,', ''], ''),
    ('empty-after-valid', ['origin,', ','], 'origin'),
    ('case-only-unknown', ['NO-REFERRER'], ''),
    ('case-preserves-earlier', ['origin, STRICT-ORIGIN'], 'origin'),
    ('ows', ['\t no-referrer\t, \tstrict-origin \t'], 'strict-origin'),
    ('quoted-unknown', ['"origin"'], ''),
    ('parameter-unknown', ['origin;x=1'], ''),
    ('duplicate', ['origin,origin'], 'origin'),
]
rows = []
for name, fields, expected in cases:
    got = reference(fields)
    rows.append(dict(name=name, fields=fields, expected=expected, actual=got, passed=got == expected))
for invalid in (None, {}, 'origin', 1, [None], [1], [[]], [True]):
    try:
        reference(invalid)
        rejected = False
    except ValueError:
        rejected = True
    rows.append(dict(name='invalid-shape', input=invalid, rejected=rejected, passed=rejected))
# Exercise the actual retained r84 equivalent-control metadata, offline.
retained = []
for side in ('a', 'b'):
    path = ROOT / f'.ufo/waves/round-84/capture-control/equivalent/{side}/ds4cc-sitemap/response.json'
    obj = json.loads(path.read_text())
    fields = [h['value'] for h in obj['headers'] if h['name'].lower() == 'referrer-policy']
    retained.append(dict(side=side, path=str(path), fields=fields, effective=reference(fields)))
spec = importlib.util.spec_from_file_location('legacy_policy_value_class', ROOT / 'scripts/policy_value_class.py')
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)
before = ','.join(retained[0]['fields'])
after = ','.join(retained[1]['fields'])
changes, counts = legacy.classify({'headers': {'referrer-policy': before}}, {'headers': {'referrer-policy': after}})
result = dict(reference_cases=rows, reference_passed=sum(r['passed'] for r in rows), reference_total=len(rows), retained=retained, legacy=dict(changes=changes, verdict=legacy.verdict(counts)), candidate_executed=False)
(OUT / 'witness-results.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
raise SystemExit(0 if all(r['passed'] for r in rows) and retained[0]['effective'] != retained[1]['effective'] and legacy.verdict(counts) == 'policy-rewritten-equivalent' else 1)
