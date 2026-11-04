#!/usr/bin/env python3
"""ScoutVary: corrected mutation sweep (line-anchored edits)."""
import importlib.util
from pathlib import Path

CTR = Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/c88_vary.py')
spec = importlib.util.spec_from_file_location('ctr', CTR)
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)
FROZEN, SEEDED = ctr.CASES, ctr.RANDOM_CASES
BASE = CTR.read_text()

def build(src, name):
    p = Path('/fast/scratch/hyaku/kake-r88/ScoutVary') / f'mut2_{name}.py'
    p.write_text(src)
    s = importlib.util.spec_from_file_location(f'mut2_{name}', p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def verdicts(mod):
    return ([(c['id'], mod.reference(c['vary'], c['stored'], c['presented'])) for c in FROZEN],
            [(c['id'], mod.reference(c['vary'], c['stored'], c['presented'])) for c in SEEDED])

bf, bs = verdicts(ctr)

def line_edit(src, lineno, old_sub, new_sub):
    lines = src.splitlines(keepends=True)
    assert old_sub in lines[lineno-1], (lineno, lines[lineno-1])
    lines[lineno-1] = lines[lineno-1].replace(old_sub, new_sub)
    return ''.join(lines)

MUTS = {
 'join_comma_no_space': lambda s: line_edit(s, 76, "', '.join(value)", "','.join(value)"),
 'join_semicolon':      lambda s: line_edit(s, 76, "', '.join(value)", "'; '.join(value)"),
 'token_allows_lf':     lambda s: line_edit(s, 40, "0-9A-Za-z]+$", "0-9A-Za-z\\n]+$"),
 'absence_one_sided_match': lambda s: line_edit(s, 91, "return 'mismatch'", "return 'match'"),
 'absent_both_mismatch': lambda s: line_edit(s, 89, "if left is None and right is None:\n            continue",
                                              "if left is None and right is None:\n            return 'mismatch'"),
 'star_before_validation': lambda s: s.replace(
     "    if star:\n        return 'mismatch'\n\n", "", 1),
}
print(f'{"mutation":26s} {"frozen moved":>14s} {"seeded moved":>13s}   example seeded id')
for name, fn in MUTS.items():
    src = fn(BASE)
    try:
        mod = build(src, name)
    except Exception as e:
        print(f'{name:26s} BUILD-ERROR {e}')
        continue
    f, s = verdicts(mod)
    fm = [i for (i,a),(j,b) in zip(bf,f) if a!=b]
    sm = [i for (i,a),(j,b) in zip(bs,s) if a!=b]
    print(f'{name:26s} {len(fm):>14d} {len(sm):>13d}   {sm[:4]}')
