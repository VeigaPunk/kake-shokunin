#!/usr/bin/env python3
"""ScoutVary: which profile branches does the frozen 20 + seeded 200 actually
PIN? Mutate one branch of the counter's reference at a time and count how
many cases move. A branch with 0 movement is unpinned: a candidate that
implements it differently still scores 20/20 + 200/200.

Read-only against the lane (the counter module is imported, not edited)."""
import importlib.util
import json
import re
from pathlib import Path

CTR = Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/c88_vary.py')
spec = importlib.util.spec_from_file_location('ctr', CTR)
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)

FROZEN = ctr.CASES
SEEDED = ctr.RANDOM_CASES

BASE_SRC = CTR.read_text()

def build(mutated_src, name):
    p = Path('/fast/scratch/hyaku/kake-r88/ScoutVary') / f'mut_{name}.py'
    p.write_text(mutated_src)
    s = importlib.util.spec_from_file_location(f'mut_{name}', p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def verdict_sets(mod):
    f = [(c['id'], mod.reference(c['vary'], c['stored'], c['presented'])) for c in FROZEN]
    s = [(c['id'], mod.reference(c['vary'], c['stored'], c['presented'])) for c in SEEDED]
    return f, s

base_f, base_s = verdict_sets(ctr)

MUTATIONS = {
    'join_comma_no_space': (", '.join(value)", ", ','.join(value)"),
    'join_semicolon': (", '.join(value)", "'; '.join(value)"),
    'value_case_fold': ("left.strip(OWS) != right.strip(OWS)", "left.strip(OWS).lower() != right.strip(OWS).lower()"),
    'value_no_ows_trim': ("left.strip(OWS) != right.strip(OWS)", "left != right"),
    'value_trim_all_ws': ("left.strip(OWS) != right.strip(OWS)", "left.strip() != right.strip()"),
    'absence_one_sided_match': ("if left is None or right is None:\n                return 'mismatch'",
                                "if left is None or right is None:\n                return 'match'"),
    'star_ignored': ("if star:\n        return 'mismatch'", "if False:\n        return 'mismatch'"),
    'empty_member_allowed': ("if not members or any(m == '' for m in members):\n        return 'invalid'",
                              "if not members:\n        return 'invalid'"),
    'empty_vary_allowed': ("if not members or any(m == '' for m in members):\n        return 'invalid'",
                           "if any(m == '' for m in members):\n        return 'invalid'"),
    'non_token_member_allowed': ("elif is_token(m):\n            names.append(m.lower())\n        else:\n            return 'invalid'",
                                 "else:\n            names.append(m.lower())"),
    'non_string_value_allowed': ("elif isinstance(value, list) and value and all(isinstance(v, str) for v in value):\n                out[low] = ', '.join(value)",
                                  "elif isinstance(value, list):\n                out[low] = ', '.join(value)"),
    'dup_case_keys_allowed': ("if low in out:\n                return None", "if False:\n                return None"),
    'token_allows_lf': ("TOKEN = re.compile(r\"^[!#$%&'*+\\\\-.^_`|~0-9A-Za-z]+$\")",
                        "TOKEN = re.compile(r\"^[!#$%&'*+\\\\-.^_`|~0-9A-Za-z\\n]+$\")"),
}

print(f'{"mutation":26s} {"frozen moved":>14s} {"seeded moved":>13s}   first moved seeded id')
for name, (old, new) in MUTATIONS.items():
    if old not in BASE_SRC:
        print(f'{name:26s} {"PATTERN-NOT-FOUND":>14s}')
        continue
    src = BASE_SRC.replace(old, new, 1)
    try:
        mod = build(src, name)
    except Exception as e:
        print(f'{name:26s} BUILD-ERROR {e}')
        continue
    f, s = verdict_sets(mod)
    fm = [i for (i, a), (j, b) in zip(base_f, f) if a != b]
    sm = [i for (i, a), (j, b) in zip(base_s, s) if a != b]
    print(f'{name:26s} {len(fm):>14d} {len(sm):>13d}   {sm[0] if sm else "-"}')
