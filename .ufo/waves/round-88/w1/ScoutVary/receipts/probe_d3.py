#!/usr/bin/env python3
"""ScoutVary: probe the C1 counter's D3 item against legal-but-differently-
placed candidate entries, to see whether difflib's line alignment can report a
history-preservation violation for an entry that only replaces the recheck
line and inserts new material.

Read-only: the counter module is imported from the lane (it only reads its
own frozen/ dir); candidate bytes are built in memory.
"""
import importlib.util
from pathlib import Path

CTR = Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/c88_defect_queue.py')
spec = importlib.util.spec_from_file_location('c88_dq', CTR)
dq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dq)

base = (dq.FROZEN / 'base-cache-current-age.md').read_text()
lines = base.splitlines()
NEW_RECHECK = ('recheck: 180d or source/adapter change; reopen '
               'https://httpwg.org/specs/rfc9111.html#age.calculations and compare section 4.2.3 '
               'equations; the offline selftest command is item 4 of the checklist below.')
MKTEMP = ('6. Offline selftest without a fixed scratch path: '
          'TMPDIR=$(mktemp -d) python3 -B scripts/cache_current_age.py --selftest; '
          'the directory is created by the shell and removed by the operator.')

def variant(insert_at):
    ls = list(lines)
    ls[2] = NEW_RECHECK
    ls.insert(insert_at, MKTEMP)
    return ('\n'.join(ls) + '\n').encode()

def reader_for(data):
    def read(path):
        return data if path == dq.ENTRY else None
    return read

print('base lines:', len(lines))
for label, at in [('append at EOF (counter green fixture)', len(lines) + 1),
                  ('insert right after the recheck line', 3),
                  ('insert right after the recheck line, plus one blank line', 3),
                  ('insert before the recheck line', 2),
                  ('insert in the middle of the body', len(lines) // 2)]:
    data = variant(at)
    fails = dq.item_d3(reader_for(data))
    print(f'{label:55s} -> D3 fails: {fails}')

# also: the counter's own green fixture
data = dq.fixed_entry_bytes()
print('counter green fixture                             -> D3 fails:',
      dq.item_d3(reader_for(data)))
