#!/usr/bin/env python3
"""ScoutVary: final coverage assertions over the frozen 20-case set and the
seeded 200 population, read from the committed counter (v3)."""
import importlib.util
import json
import re
from pathlib import Path

CTR = Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/c88_vary.py')
spec = importlib.util.spec_from_file_location('ctr', CTR)
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)

frozen = ctr.CASES
seeded = ctr.RANDOM_CASES

def facts(cases):
    out = {
        'n': len(cases),
        'member_carries_LF_or_CR': 0,
        'case_variant_duplicate_key_in_one_map': 0,
        'value_list_with_non_string': 0,
        'empty_value_list': 0,
        'empty_list_element_in_vary': 0,
        'presented_lacks_nominated_field_stored_has': 0,
        'stored_lacks_nominated_field_presented_has': 0,
        'value_differs_only_by_case': 0,
        'value_differs_only_by_internal_ws': 0,
        'value_differs_only_by_ows': 0,
        'vary_member_is_star': 0,
        'vary_duplicate_member_case_variant': 0,
    }
    for c in cases:
        vary, st, pr = c['vary'], c['stored'], c['presented']
        if not isinstance(vary, str):
            continue
        members = [m.strip(' \t') for m in vary.split(',')]
        if any(('\n' in m or '\r' in m) for m in members):
            out['member_carries_LF_or_CR'] += 1
        if any(m == '' for m in members):
            out['empty_list_element_in_vary'] += 1
        if '*' in members:
            out['vary_member_is_star'] += 1
        lows = [m.lower() for m in members if m != '*']
        if len(lows) != len(set(lows)):
            out['vary_duplicate_member_case_variant'] += 1
        for side in (st, pr):
            if not isinstance(side, dict):
                continue
            low = [k.lower() for k in side]
            if len(low) != len(set(low)):
                out['case_variant_duplicate_key_in_one_map'] += 1
            for k, v in side.items():
                if isinstance(v, list):
                    if not v:
                        out['empty_value_list'] += 1
                    elif not all(isinstance(x, str) for x in v):
                        out['value_list_with_non_string'] += 1
        for n in set(lows):
            ls = st.get(n, '<absent>') if isinstance(st, dict) else '<absent>'
            lp = pr.get(n, '<absent>') if isinstance(pr, dict) else '<absent>'
            if ls != '<absent>' and lp == '<absent>':
                out['presented_lacks_nominated_field_stored_has'] += 1
            if ls == '<absent>' and lp != '<absent>':
                out['stored_lacks_nominated_field_presented_has'] += 1
            if isinstance(ls, str) and isinstance(lp, str):
                if ls != lp and ls.lower() == lp.lower():
                    out['value_differs_only_by_case'] += 1
                elif ls != lp and ls.replace(' ', '') == lp.replace(' ', ''):
                    out['value_differs_only_by_internal_ws'] += 1
                elif ls != lp and ls.strip(' \t') == lp.strip(' \t'):
                    out['value_differs_only_by_ows'] += 1
    return out

print('frozen 20:', json.dumps(facts(frozen), sort_keys=True))
print('seeded 200:', json.dumps(facts(seeded), sort_keys=True))

# the round's own TOKEN regex vs a member carrying LF
print()
for m in ['gzip', 'gzip\n', 'gzip\r', 'gzip\nx']:
    print(f'   re.match(TOKEN, {m!r}) -> {bool(ctr.TOKEN.match(m))}')
print('   reference("gzip\\n", ...) ->',
      ctr.reference('gzip\n', {'gzip': 'v'}, {'gzip': 'v'}))
print('   is_token("gzip\\n") ->', ctr.is_token('gzip\n'))
