#!/usr/bin/env python3
"""ScoutVary: does the C1 counter's D3 item accept a contract-conforming
entry whose offline selftest command is written across two lines?

Contract (D3): 'carry the offline selftest command in a `mktemp -d` form in its
body' — no single-line requirement. The counter's check is:
    any('mktemp -d' in l and TOOL in l and '--selftest' in l for l in new_lines)
i.e. all three tokens must appear on ONE line.
"""
import importlib.util
from pathlib import Path

CTR = Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/c88_defect_queue.py')
spec = importlib.util.spec_from_file_location('dq', CTR)
dq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dq)

base = (dq.FROZEN / 'base-cache-current-age.md').read_text().splitlines()
NEW_RECHECK = ('recheck: 180d or source/adapter change; reopen '
               'https://httpwg.org/specs/rfc9111.html#age.calculations and compare section 4.2.3 '
               'equations; the offline selftest command is item 4 of the checklist below.')

def reader_for(text):
    data = text.encode()
    def read(path):
        return data if path == dq.ENTRY else None
    return read

variants = {
    'one line (counter green fixture)': [
        '6. Offline selftest: TMPDIR=$(mktemp -d) python3 -B scripts/cache_current_age.py --selftest'],
    'two lines: mktemp on one, command on the next': [
        '6. Offline selftest: create a scratch directory with',
        '   TMPDIR=$(mktemp -d) and run python3 -B scripts/cache_current_age.py --selftest'],
    'two lines: command on one, mktemp on the next': [
        '6. Offline selftest: run python3 -B scripts/cache_current_age.py --selftest',
        '   with TMPDIR=$(mktemp -d) set in the environment'],
}
for label, extra in variants.items():
    lines = list(base)
    lines[2] = NEW_RECHECK
    lines.extend(extra)
    text = '\n'.join(lines) + '\n'
    print(f'{label}\n    D3 fails: {dq.item_d3(reader_for(text))}')
