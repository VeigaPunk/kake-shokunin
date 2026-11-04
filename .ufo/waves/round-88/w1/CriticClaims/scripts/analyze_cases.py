#!/usr/bin/env python3
"""Static analysis of the committed C2 case populations. No candidate execution."""
import importlib.util
import json
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
spec = importlib.util.spec_from_file_location('c88', LANE / '.ufo/waves/round-88/c88_vary.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def payload(case):
    return json.dumps({k: case[k] for k in ('vary', 'stored', 'presented')})


def verdict(case):
    return 'invalid' if case['exit'] == 1 else case['verdict']


frozen = m.CASES
random_cases = m.RANDOM_CASES
fp = {payload(c) for c in frozen}
rp = [payload(c) for c in random_cases]
inter = [p for p in rp if p in fp]
print(json.dumps({
    'frozen_n': len(frozen),
    'random_n': len(random_cases),
    'random_payload_duplicates': len(rp) - len(set(rp)),
    'frozen_random_payload_overlap': len(inter),
    'overlap_payloads': inter,
}, sort_keys=True))

# Category counts over the random population.
def is_star(vary):
    return isinstance(vary, str) and any(x.strip(' \t') == '*' for x in vary.split(','))


def normalise_ok(case):
    """Would the reference reach a normalise verdict if '*' did not short-circuit?"""
    v = case['vary']
    if not isinstance(v, str):
        return False
    members = [x.strip(' \t') for x in v.split(',')]
    if not members or any(x == '' for x in members):
        return False
    for x in members:
        if x == '*':
            continue
        if not m.is_token(x):
            return False
    for side in ('stored', 'presented'):
        d = case[side]
        if not isinstance(d, dict):
            return False
        seen = set()
        for key, value in d.items():
            if not m.is_token(key):
                return False
            low = key.lower()
            if low in seen:
                return False
            seen.add(low)
            if isinstance(value, str):
                continue
            if isinstance(value, list) and value and all(isinstance(x, str) for x in value):
                continue
            return False
    return True


cats = {
    'star': 0,
    'star_and_payload_would_be_invalid': 0,
    'empty_list_value': 0,
    'nonstring_value': 0,
    'vary_nonstring': 0,
    'empty_member': 0,
    'non_token_vary_member': 0,
}
for c in random_cases:
    if is_star(c['vary']):
        cats['star'] += 1
        if not normalise_ok(c):
            cats['star_and_payload_would_be_invalid'] += 1
    for side in ('stored', 'presented'):
        if isinstance(c.get(side), dict):
            for v in c[side].values():
                if isinstance(v, list) and not v:
                    cats['empty_list_value'] += 1
                    break
    for side in ('stored', 'presented'):
        if isinstance(c.get(side), dict):
            if any(not isinstance(v, (str, list)) for v in c[side].values()):
                cats['nonstring_value'] += 1
                break
    if not isinstance(c['vary'], str):
        cats['vary_nonstring'] += 1
    elif any(x.strip(' \t') == '' for x in c['vary'].split(',')):
        cats['empty_member'] += 1
    elif any(x.strip(' \t') != '*' and not m.is_token(x.strip(' \t'))
             for x in c['vary'].split(',')):
        cats['non_token_vary_member'] += 1

print(json.dumps(cats, sort_keys=True))

# Verdict counts and simple-feature agreement rates.
from collections import Counter
vc = Counter(verdict(c) for c in random_cases)
print(json.dumps({'random_verdicts': dict(vc)}, sort_keys=True))

def agree(pred, cases):
    return sum(pred(c) == verdict(c) for c in cases)

star_rule = lambda c: 'mismatch' if is_star(c['vary']) else 'match'
eq_rule = lambda c: 'match' if c['stored'] == c['presented'] else 'mismatch'
print(json.dumps({
    'star_rule_agreement_frozen': agree(star_rule, frozen),
    'star_rule_agreement_random': agree(star_rule, random_cases),
    'exact_eq_rule_agreement_frozen': agree(eq_rule, frozen),
    'exact_eq_rule_agreement_random': agree(eq_rule, random_cases),
    'random_stored_equals_presented': sum(c['stored'] == c['presented'] for c in random_cases),
}, sort_keys=True))

# Cases whose reference verdict differs from a validate-before-star reading.
def alt_validate_first(c):
    if not normalise_ok(c):
        return 'invalid'
    return m.reference(c['vary'], c['stored'], c['presented'])


def alt_empty_list(c):
    """Declared-profile reading: [] combines zero lines -> empty string."""
    if not isinstance(c['vary'], str):
        return 'invalid'
    members = [x.strip(' \t') for x in c['vary'].split(',')]
    if not members or any(x == '' for x in members):
        return 'invalid'
    names = []
    star = False
    for x in members:
        if x == '*':
            star = True
        elif m.is_token(x):
            names.append(x.lower())
        else:
            return 'invalid'
    def norm(d):
        if not isinstance(d, dict):
            return None
        out = {}
        for key, value in d.items():
            if not m.is_token(key):
                return None
            low = key.lower()
            if low in out:
                return None
            if isinstance(value, str):
                out[low] = value
            elif isinstance(value, list) and all(isinstance(x, str) for x in value):
                out[low] = ', '.join(value)
            else:
                return None
        return out
    a, b = norm(c['stored']), norm(c['presented'])
    if a is None or b is None:
        return 'invalid'
    if star:
        return 'mismatch'
    for name in set(names):
        left, right = a.get(name), b.get(name)
        if left is None and right is None:
            continue
        if left is None or right is None:
            return 'mismatch'
        if left.strip(' \t') != right.strip(' \t'):
            return 'mismatch'
    return 'match'

for name, fn in (('alt_validate_first', alt_validate_first), ('alt_empty_list', alt_empty_list)):
    diffs = [c['id'] for c in random_cases if fn(c) != verdict(c)]
    print(json.dumps({'variant': name, 'agreement_frozen': agree(fn, frozen),
                      'agreement_random': agree(fn, random_cases), 'diff_ids': diffs},
                     sort_keys=True))
