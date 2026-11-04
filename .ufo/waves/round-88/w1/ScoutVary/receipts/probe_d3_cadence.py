#!/usr/bin/env python3
"""ScoutVary: does the C1 counter's D3 item reject a cadence phrasing the
contract permits? Contract (D3): 'must keep a cadence in its single recheck:
line' -- no format is prescribed. The counter's test is
    rest[:1].isdigit() and ('d' in rest.split()[0].lower() or rest[:4].isdigit())
"""
import importlib.util
from pathlib import Path

CTR = Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/c88_defect_queue.py')
spec = importlib.util.spec_from_file_location('dq', CTR)
dq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dq)

base = (dq.FROZEN / 'base-cache-current-age.md').read_text().splitlines()
MKTEMP = ('6. Offline selftest without a fixed scratch path: '
          'TMPDIR=$(mktemp -d) python3 -B scripts/cache_current_age.py --selftest; '
          'the directory is created by the shell and removed by the operator.')

def build(recheck_text, mktemp_lines):
    lines = list(base)
    lines[2] = recheck_text
    lines.extend(mktemp_lines)
    return '\n'.join(lines) + '\n'

def reader_for(text):
    data = text.encode()
    def read(path):
        return data if path == dq.ENTRY else None
    return read

PHRASINGS = [
    'recheck: 180d or source/adapter change; reopen the URL and compare; the offline selftest command is item 4 of the checklist below.',
    'recheck: 180 days or source/adapter change; reopen the URL and compare; the offline selftest command is item 4 of the checklist below.',
    'recheck: 180-day or source/adapter change; reopen the URL and compare; the offline selftest command is item 4 of the checklist below.',
    'recheck: 2026-11-04 reviewed; reopen the URL and compare; the offline selftest command is item 4 of the checklist below.',
    'recheck: 6 months or source/adapter change; reopen the URL and compare; the offline selftest command is item 4 of the checklist below.',
    'recheck: 90 days or source/adapter change; reopen the URL and compare; the offline selftest command is item 4 of the checklist below.',
]
for ph in PHRASINGS:
    text = build(ph, [MKTEMP])
    fails = dq.item_d3(reader_for(text))
    print(f'{"ACCEPTED" if not fails else "REJECTED"}  {ph.split(" or ")[0]!r}  fails={fails}')
