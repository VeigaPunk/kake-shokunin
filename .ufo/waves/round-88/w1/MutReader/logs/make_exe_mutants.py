#!/usr/bin/env python3
"""Single-point mutants of ExecReader's round-88 candidate (vary_match.py).

Source: .ufo/waves/round-88/w1/ExecReader/vary_match.py
        sha256 fdceef474e618d6664c15333cba6a1fa136fbc44f2791bbbdbf92d234fb287d6
The candidate is only read; every mutant is written under this scratch root.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path('/fast/scratch/hyaku/kake-r88/MutReader')
SRC = HERE / 'exe_vary_match.py'
OUT = HERE / 'mutants_exec'

PATCHES = [
    ('e01_name_case_sensitive', ['no OWS trim, case-sensitive lookups, ...'],
     '        low = ascii_lower(key)\n',
     '        low = key\n'),
    ('e02_no_ows_trim', [],
     '        if left.strip(OWS) != right.strip(OWS):\n',
     '        if left != right:\n'),
    ('e03_unordered_array', [],
     "            out[low] = ', '.join(value)\n",
     "            out[low] = ', '.join(sorted(value))\n"),
    ('e04_star_as_token', [],
     "        if member == '*':\n            star = True\n            continue\n",
     ''),
    ('e05_absent_both_mismatch', [],
     '        if left is None and right is None:\n            continue\n',
     "        if left is None and right is None:\n            return 'mismatch', None\n"),
    ('e06_one_sided_match', [],
     "        if left is None or right is None:\n            return 'mismatch', None\n",
     '        if left is None or right is None:\n            continue\n'),
    ('e07_value_casefold', [],
     '        if left.strip(OWS) != right.strip(OWS):\n',
     '        if ascii_lower(left.strip(OWS)) != ascii_lower(right.strip(OWS)):\n'),
    ('e08_internal_ws_collapse', [],
     '        if left.strip(OWS) != right.strip(OWS):\n',
     "        if ' '.join(left.split()) != ' '.join(right.split()):\n"),
    ('e09_empty_vary_match', [],
     "        if member == '':\n            return None, False, 'empty Vary member (empty Vary or a bare comma)'\n",
     "        if member == '':\n            continue\n"),
    ('e10_dupkey_refusal_removed', [],
     '        if low in out:\n',
     '        if low in out and False:\n'),
    ('e11_unnominated_compared', [],
     '    for name in names:\n',
     '    for name in sorted(set(names) | set(stored) | set(presented)):\n'),
    ('e12_asymmetric_trim', [],
     '        if left.strip(OWS) != right.strip(OWS):\n',
     '        if left.strip(OWS) != right:\n'),
    ('e13_int_value_coerced', [],
     '        if isinstance(value, str):\n            out[low] = value\n',
     '        if isinstance(value, (str, int)):\n            out[low] = str(value)\n'),
    ('e14_vary_coerced', [],
     "    if not isinstance(vary, str):\n        return None, f'vary must be a string, not {type(vary).__name__}'\n",
     '    if not isinstance(vary, str):\n        vary = str(vary)\n'),
    ('e15_empty_value_absent', [],
     '        if isinstance(value, str):\n            out[low] = value\n',
     '        if isinstance(value, str):\n            if value.strip(OWS):\n                out[low] = value\n'),
    ('e16_list_elem_check_removed', [],
     '        elif isinstance(value, list) and value and all(isinstance(v, str) for v in value):\n',
     '        elif isinstance(value, list) and value:\n'),
    ('e17_empty_list_accepted', [],
     '        elif isinstance(value, list) and value and all(isinstance(v, str) for v in value):\n',
     '        elif isinstance(value, list) and all(isinstance(v, str) for v in value):\n'),
    ('e18_star_masks_invalid', [],
     "    stored, reason = normalise_request(payload.get('stored'), 'stored')\n"
     '    if reason is not None:\n        return None, reason\n'
     "    presented, reason = normalise_request(payload.get('presented'), 'presented')\n"
     '    if reason is not None:\n        return None, reason\n'
     "    if star:\n        return 'mismatch', None\n",
     "    if star:\n        return 'mismatch', None\n"
     "    stored, reason = normalise_request(payload.get('stored'), 'stored')\n"
     '    if reason is not None:\n        return None, reason\n'
     "    presented, reason = normalise_request(payload.get('presented'), 'presented')\n"
     '    if reason is not None:\n        return None, reason\n'),
    ('e19_token_allows_space', [],
     'TCHAR = frozenset("!#$%&\'*+-.^_`|~"\n',
     'TCHAR = frozenset("!#$%&\'*+-.^_`|~ "\n'),
    ('e20_dedup_removed', [],
     '        if low not in seen:\n            seen.add(low)\n            names.append(low)\n',
     '        seen.add(low)\n        names.append(low)\n'),
    ('e21_token_too_permissive', [],
     '            and all(ch in TCHAR for ch in text))\n',
     "            and all(not ch.isspace() and ch not in ',' for ch in text))\n"),
]


def main():
    src = SRC.read_bytes().decode()
    src_sha = hashlib.sha256(src.encode()).hexdigest()
    assert src_sha == 'fdceef474e618d6664c15333cba6a1fa136fbc44f2791bbbdbf92d234fb287d6', src_sha
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, _, old, new in PATCHES:
        hits = src.count(old)
        assert hits == 1, f'{name}: anchor count {hits} != 1 for {old[:70]!r}'
        text = src.replace(old, new, 1)
        assert text != src, f'{name}: patch was a no-op'
        (OUT / f'{name}.py').write_text(text)
        manifest.append(dict(name=name, mutant_sha256=hashlib.sha256(text.encode()).hexdigest(),
                             old=old, new=new))
        print(f'built {name:30s} {manifest[-1]["mutant_sha256"][:16]}')
    (OUT / 'manifest.json').write_text(json.dumps(
        dict(source='.ufo/waves/round-88/w1/ExecReader/vary_match.py',
             source_sha256=src_sha, count=len(manifest), mutants=manifest),
        indent=2, sort_keys=True) + '\n')
    print(f'manifest: {len(manifest)} mutants of source sha256={src_sha}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
