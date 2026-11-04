#!/usr/bin/env python3
"""ScribeEntry probe: does the round-89 C2 counter reject contract-refused inputs?

Reads the frozen counter read-only, applies single-point mutants to its own
REFERENCE text, and scores each with score_candidate. A mutant that still prints
met=True is a contract rule the counter does not measure. Work dir is explicit.
"""
import importlib.util
import pathlib
import sys

LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
WORK = pathlib.Path('/fast/scratch/hyaku/kake-r89/ScribeEntry/work-probe')
COUNTER = LANE / '.ufo/waves/round-89/c89_key.py'

spec = importlib.util.spec_from_file_location('c89_key', COUNTER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
WORK.mkdir(parents=True, exist_ok=True)
TOTAL_PROPS = m.PROPS_PER_CLASS * len(m.PROP_CLASSES)


def score(src, name):
    f, p, r, fails = m.score_candidate(src.encode(), WORK / name, m.SEED)
    met = f == len(m.FROZEN) and p == TOTAL_PROPS and r == len(m.REFUSALS)
    print(f'{name}: frozen={f}/{len(m.FROZEN)} props={p}/{TOTAL_PROPS} '
          f'refuse={r}/{len(m.REFUSALS)} met={str(met).lower()}')
    for x in fails[:2]:
        print(f'    fail: {x}')
    return met


REF = m.REFERENCE
print(f'counter sha256 read: {COUNTER.name} (verified by the caller)')
score(REF, 'reference-unmutated')

# Each mutant removes or weakens one contract refusal or escape. Anchors are
# exact substrings of REFERENCE; a missing anchor prints ANCHOR-MISSING.
MUTANTS = [
    ('dup-vary-member-allowed',
     '    if len(set(names)) != len(names):\n        print("invalid_input: duplicate vary member", file=sys.stderr); return 1\n', ''),
    ('nonempty-nontoken-vary-member-allowed',
     '            if not tok(m):\n',
     '            if m == "":\n'),
    ('empty-header-name-allowed',
     '        if not isinstance(name, str) or not tok(name):',
     '        if not isinstance(name, str) or (name != "" and not tok(name)):'),
    ('cr-only-in-value-allowed',
     '        if "\\r" in value or "\\n" in value:',
     '        if "\\n" in value:'),
    ('uri-not-percent-escaped',
     '    key = esc(uri) + ("" if not parts else US + US.join(parts))',
     '    key = uri + ("" if not parts else US + US.join(parts))'),
    ('name-not-escaped',
     '            parts.append(esc(name) + RS + esc(low[name].strip(" \\t")))',
     '            parts.append(name + RS + esc(low[name].strip(" \\t")))'),
    ('u001d-not-escaped',
     '("\\x1d", "%1D"), ',
     ''),
    ('value-not-escaped',
     '            parts.append(esc(name) + RS + esc(low[name].strip(" \\t")))',
     '            parts.append(esc(name) + RS + low[name].strip(" \\t"))'),
    ('absent-equals-empty',
     '            parts.append(esc(name) + RS + GS)',
     '            parts.append(esc(name) + RS)'),
    ('vary-not-string-allowed',
     '    if not isinstance(vary, str):\n        print("invalid_input: vary must be a string", file=sys.stderr); return 1\n',
     ''),
]

killed = survived = 0
for name, old, new in MUTANTS:
    if old not in REF:
        print(f'{name}: ANCHOR-MISSING')
        continue
    if score(REF.replace(old, new, 1), name):
        survived += 1
    else:
        killed += 1
print(f'summary: mutants={len(MUTANTS)} killed={killed} survived_met_true={survived}')
sys.exit(0)
