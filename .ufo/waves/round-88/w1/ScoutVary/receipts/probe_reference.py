#!/usr/bin/env python3
"""ScoutVary probe: exercise the round-88 C2 counter's own reference
implementation on inputs that are NOT in the frozen 20-case set, to see
which profile branches the frozen set and the seeded population actually
pin. Read-only against the lane: imports the frozen counter module.
"""
import importlib.util
import json
import sys
from pathlib import Path

CTR = Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/c88_vary.py')
spec = importlib.util.spec_from_file_location('c88_vary', CTR)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

probes = [
    ('empty list element in Vary (RFC 9110 5.6.1.2 recipients MUST ignore)',
     'accept-encoding,', {'accept-encoding': 'gzip'}, {'accept-encoding': 'gzip'}),
    ('trailing comma only', ',', {}, {}),
    ('two empty members', ',,', {}, {}),
    ('Vary with OWS around comma', 'accept-encoding , accept-language',
     {'accept-encoding': 'gzip', 'accept-language': 'en'},
     {'accept-encoding': 'gzip', 'accept-language': 'en'}),
    ('duplicate field name differing only in case, same request (stored)',
     'accept-encoding', {'accept-encoding': 'gzip', 'Accept-Encoding': 'br'},
     {'accept-encoding': 'gzip, br'}),
    ('duplicate field name differing only in case, same request (presented)',
     'accept-encoding', {'accept-encoding': 'gzip'},
     {'accept-encoding': 'gzip', 'ACCEPT-ENCODING': 'br'}),
    ('presented empty-string value vs absent',
     'accept-encoding', {'accept-encoding': 'gzip'}, {'accept-encoding': ''}),
    ('both absent from both requests',
     'accept-encoding', {}, {}),
    ('presented absent, stored present',
     'accept-encoding', {'accept-encoding': 'gzip'}, {}),
    ('empty value list on a side', 'accept-encoding',
     {'accept-encoding': 'gzip'}, {'accept-encoding': []}),
    ('value list with a non-string member', 'accept-encoding',
     {'accept-encoding': 'gzip'}, {'accept-encoding': ['gzip', 5]}),
    ('Vary member with a non-token char (underscore is a tchar, ok)', 'x_kake',
     {'x_kake': 'v'}, {'x_kake': 'v'}),
    ('Vary with an underscore member', 'x-kake', {'x-kake': 'v'}, {'x-kake': 'v'}),
    ('star plus a non-token member', '*, accept encoding', {}, {}),
    ('value with internal OWS around the q separator', 'accept-encoding',
     {'accept-encoding': 'gzip;q=1'}, {'accept-encoding': 'gzip; q=1'}),
]

for label, vary, stored, presented in probes:
    v = mod.reference(vary, stored, presented)
    print(f'{v:9s}  {label}\n          vary={vary!r} stored={stored!r} presented={presented!r}')

# Which branches does the frozen set / seeded population actually exercise?
frozen = json.loads(mod.CASES_PATH.read_text())
rand = mod.RANDOM_CASES

def coverage(cases):
    cov = {
        'empty_vary_member_invalid': 0,
        'case_variant_duplicate_key_refused': 0,
        'empty_value_list_refused': 0,
        'value_list_nonstring_refused': 0,
        'absent_both': 0,
        'absent_presented_only': 0,
        'absent_stored_only': 0,
        'star_present': 0,
        'name_case_variant_member': 0,
        'value_case_differs': 0,
        'value_ows_trimmed': 0,
        'value_list_used': 0,
        'star_dominates': 0,
    }
    for c in cases:
        vary, st, pr = c['vary'], c['stored'], c['presented']
        if not isinstance(vary, str):
            continue
        members = [m.strip(' \t') for m in vary.split(',')]
        if any(m == '' for m in members):
            cov['empty_vary_member_invalid'] += 1
        if '*' in members:
            cov['star_present'] += 1
            if len(members) > 1:
                cov['star_dominates'] += 1
        if any(m != m.lower() for m in members):
            cov['name_case_variant_member'] += 1
        for side in (st, pr):
            if not isinstance(side, dict):
                continue
            low = [k.lower() for k in side]
            if len(low) != len(set(low)):
                cov['case_variant_duplicate_key_refused'] += 1
            for k, v in side.items():
                if isinstance(v, list):
                    cov['value_list_used'] += 1
                    if not v:
                        cov['empty_value_list_refused'] += 1
                    elif not all(isinstance(x, str) for x in v):
                        cov['value_list_nonstring_refused'] += 1
        names = [m.lower() for m in members if m != '*']
        for n in names:
            ls = st.get(n, '<absent>') if isinstance(st, dict) else '<absent>'
            lp = pr.get(n, '<absent>') if isinstance(pr, dict) else '<absent>'
            if ls == '<absent>' and lp == '<absent>':
                cov['absent_both'] += 1
            elif ls == '<absent>':
                cov['absent_stored_only'] += 1
            elif lp == '<absent>':
                cov['absent_presented_only'] += 1
            elif isinstance(ls, str) and isinstance(lp, str):
                if ls != lp and ls.strip(' \t') == lp.strip(' \t'):
                    cov['value_ows_trimmed'] += 1
                if ls.lower() != lp.lower() and ls.strip(' \t').lower() == lp.strip(' \t').lower():
                    cov['value_case_differs'] += 1
    return cov

print('\nfrozen-20 coverage:', json.dumps(coverage(frozen), sort_keys=True))
print('seeded-200 coverage:', json.dumps(coverage(rand), sort_keys=True))
print('\nfrozen cases_sha256:', mod.CASES_SHA)
print('seeded random_sha256:', mod.RANDOM_SHA)
counts = {v: sum(c['verdict'] == v if c['exit'] == 0 else v == 'invalid' for c in rand)
          for v in ('match', 'mismatch', 'invalid')}
print('seeded verdict counts:', counts)
print('constant-match would pass frozen:',
      sum(c['verdict'] == 'match' and c['exit'] == 0 for c in frozen), '/ 20')
print('constant-match would pass seeded:',
      counts['match'], '/ 200')
