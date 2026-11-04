#!/usr/bin/env python3
"""ScoutVary: (a) show the difflib opcodes the C1 D3 item sees for an entry
that only replaces the recheck line and inserts one new line adjacent to it;
(b) test the D3 cadence test against plausible cadence phrasings."""
import difflib
import importlib.util
from pathlib import Path

CTR = Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/c88_defect_queue.py')
spec = importlib.util.spec_from_file_location('c88_dq2', CTR)
dq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dq)

base = (dq.FROZEN / 'base-cache-current-age.md').read_text()
base_lines = base.splitlines()
NEW_RECHECK = ('recheck: 180d or source/adapter change; reopen '
               'https://httpwg.org/specs/rfc9111.html#age.calculations and compare section 4.2.3 '
               'equations; the offline selftest command is item 4 of the checklist below.')
MKTEMP = ('6. Offline selftest without a fixed scratch path: '
          'TMPDIR=$(mktemp -d) python3 -B scripts/cache_current_age.py --selftest; '
          'the directory is created by the shell and removed by the operator.')

def opcodes(new_lines):
    return [(t, i1, i2, j1, j2) for t, i1, i2, j1, j2
            in difflib.SequenceMatcher(None, base_lines, new_lines, autojunk=False).get_opcodes()
            if t != 'equal']

for label, at in [('insert after recheck line (index 3)', 3),
                  ('insert before recheck line (index 2)', 2),
                  ('append at EOF', len(base_lines) + 1)]:
    ls = list(base_lines)
    ls[2] = NEW_RECHECK
    ls.insert(at, MKTEMP)
    print(f'{label}: non-equal opcodes = {opcodes(ls)}')

print()
print('cadence test (rest[:1].isdigit() and ("d" in rest.split()[0].lower() or rest[:4].isdigit())):')
for cand in ['180d or source change', '180 days or source change', '180-day or source change',
             '2026-11-04 reviewed', '90d', '6 months', 'quarterly', '30 days']:
    rest = cand.strip()
    ok = bool(rest[:1].isdigit() and ('d' in rest.split()[0].lower() or rest[:4].isdigit()))
    print(f'   {cand!r:38s} -> cadence accepted: {ok}')
