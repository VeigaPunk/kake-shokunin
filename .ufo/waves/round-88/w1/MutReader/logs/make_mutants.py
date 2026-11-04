#!/usr/bin/env python3
"""Generate single-point mutants of the MutReader reference adapter.

Every patch asserts its anchor is present exactly once, so a silent no-op
mutant is impossible: a failed anchor aborts the build.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path('/fast/scratch/hyaku/kake-r88/MutReader')
REF = HERE / 'ref_vary_match.py'
OUT = HERE / 'mutants'

# name -> (label, old, new)
PATCHES = [
    ('m01_name_case_sensitive', 'field names compared case-sensitively',
     '            low = key.lower()\n',
     '            low = key\n'),
    ('m02_no_ows_trim', 'leading/trailing OWS not trimmed before the value compare',
     '        if left.strip(OWS) != right.strip(OWS):\n',
     '        if left != right:\n'),
    ('m03_unordered_array', 'multiple field lines combined in sorted (unordered) order',
     "                out[low] = ', '.join(value)\n",
     "                out[low] = ', '.join(sorted(value))\n"),
    ('m04_star_as_token', "'*' handled as an ordinary token instead of always failing",
     "        if m == '*':\n            star = True\n        elif is_token(m):\n            names.append(m.lower())\n",
     "        if is_token(m):\n            names.append(m.lower())\n"),
    ('m05_absent_both_mismatch', 'a field absent from both requests treated as a mismatch',
     '        if left is None and right is None:\n            continue\n',
     "        if left is None and right is None:\n            return 'mismatch'\n"),
    ('m06_one_sided_match', 'a field present in only one request treated as a match',
     '        if left is None or right is None:\n            return \'mismatch\'\n',
     '        if left is None or right is None:\n            continue\n'),
    ('m07_value_casefold', 'value comparison case-folded',
     '        if left.strip(OWS) != right.strip(OWS):\n',
     '        if left.strip(OWS).lower() != right.strip(OWS).lower():\n'),
    ('m08_internal_ws_collapse', 'internal whitespace runs collapsed before the value compare',
     '        if left.strip(OWS) != right.strip(OWS):\n',
     "        if ' '.join(left.split()) != ' '.join(right.split()):\n"),
    ('m09_empty_vary_match', 'an empty/non-token Vary member is accepted as match',
     "    if not members or any(m == '' for m in members):\n        return 'invalid'\n",
     "    if not members or any(m == '' for m in members):\n        return 'match'\n"),
    ('m10_star_only_sole', "'*' fails only when it is the sole member",
     '    if star:\n        return \'mismatch\'\n',
     "    if star and not names:\n        return 'mismatch'\n"),
    ('m11_dupkey_refusal_removed', 'ambiguous duplicate field names accepted (last wins)',
     '            if low in out:\n                return None\n',
     ''),
    ('m12_unnominated_compared', 'fields not nominated by Vary are compared too',
     '    for name in set(names):\n',
     '    for name in set(names) | set(a) | set(b):\n'),
    ('m13_asymmetric_trim', 'OWS trimmed on the stored side only',
     '        if left.strip(OWS) != right.strip(OWS):\n',
     '        if left.strip(OWS) != right:\n'),
    ('m14_int_value_coerced', 'non-string scalar field values coerced with str()',
     '            if isinstance(value, str):\n                out[low] = value\n',
     '            if isinstance(value, (str, int)):\n                out[low] = str(value)\n'),
    ('m15_vary_coerced', 'non-string Vary coerced with str() instead of refused',
     "    if not isinstance(vary, str):\n        return 'invalid'\n",
     '    if not isinstance(vary, str):\n        vary = str(vary)\n'),
    ('m16_empty_value_absent', 'an empty field value is treated as absent',
     '            if isinstance(value, str):\n                out[low] = value\n',
     '            if isinstance(value, str):\n                if value.strip(OWS):\n                    out[low] = value\n'),
    ('m17_list_elem_check_removed', 'list field values accept non-string elements',
     '            elif isinstance(value, list) and value and all(isinstance(v, str) for v in value):\n',
     '            elif isinstance(value, list) and value:\n'),
    ('m18_empty_list_absent', 'an empty field-line list is accepted as the empty string',
     '            elif isinstance(value, list) and value and all(isinstance(v, str) for v in value):\n',
     '            elif isinstance(value, list) and all(isinstance(v, str) for v in value):\n'),
    ('m19_empty_member_guard_removed', 'the redundant empty-member guard is deleted (equivalent)',
     "    if not members or any(m == '' for m in members):\n        return 'invalid'\n",
     '    if not members:\n        return \'invalid\'\n'),
    ('m20_token_allows_space', 'the token grammar admits SP, so "accept encoding" parses',
     'TOKEN = re.compile(r"^[!#$%&\'*+\\-.^_`|~0-9A-Za-z]+$")\n',
     'TOKEN = re.compile(r"^[!#$%&\'*+\\-.^_`|~0-9A-Za-z ]+$")\n'),
]


def main():
    src = REF.read_bytes().decode()
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, label, old, new in PATCHES:
        hits = src.count(old)
        assert hits == 1, f'{name}: anchor count {hits} (want 1) for {old!r}'
        text = src.replace(old, new, 1)
        assert text != src, f'{name}: patch was a no-op'
        p = OUT / f'{name}.py'
        p.write_text(text)
        manifest.append(dict(name=name, label=label, mutant_sha256=hashlib.sha256(text.encode()).hexdigest(),
                             old=old, new=new))
        print(f'built {name} sha256={manifest[-1]["mutant_sha256"][:16]} ({label})')
    (HERE / 'mutants' / 'manifest.json').write_text(json.dumps(
        dict(ref_sha256=hashlib.sha256(src.encode()).hexdigest(), count=len(manifest), mutants=manifest),
        indent=2, sort_keys=True) + '\n')
    print(f'manifest: {len(manifest)} mutants from ref sha256={hashlib.sha256(src.encode()).hexdigest()}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
