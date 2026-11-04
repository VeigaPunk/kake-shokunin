import importlib.util
import json
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
ROUND = LANE / '.ufo/waves/round-88'
TOOL = ROUND / 'w1/ExecReader/vary_match.py'
OUT = Path('/fast/scratch/hyaku/kake-r88/ExecReader/percase.tsv')

spec = importlib.util.spec_from_file_location('c88v3', ROUND / 'c88_vary.py')
counter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(counter)
frozen = json.loads((ROUND / 'vary-cases.json').read_text())


def run(case):
    payload = json.dumps({k: case[k] for k in ('vary', 'stored', 'presented')})
    proc = subprocess.run([sys.executable, '-B', str(TOOL)], input=payload,
                          capture_output=True, text=True)
    reasons = []
    if proc.returncode != case['exit']:
        reasons.append(f"exit {proc.returncode} != {case['exit']}")
    if case['exit'] == 0:
        if proc.stdout != case['verdict']:
            reasons.append(f'stdout {proc.stdout!r} != {case["verdict"]!r}')
        if proc.stderr != '':
            reasons.append(f'stderr {proc.stderr!r} not empty')
    else:
        if proc.stdout != '':
            reasons.append(f'stdout {proc.stdout!r} not empty')
        if not proc.stderr.startswith('invalid_input:'):
            reasons.append('stderr lacks invalid_input: prefix')
    return reasons


rows = []
for population, cases in (('frozen', frozen), ('random', counter.RANDOM_CASES)):
    for case in cases:
        reasons = run(case)
        rows.append((population, str(case['id']), str(case['exit']),
                     str(case['verdict']), 'PASS' if not reasons else
                     'FAIL ' + '; '.join(reasons)))

with OUT.open('w') as handle:
    handle.write('population\tcase\texpected_exit\texpected_verdict\tresult\n')
    for row in rows:
        handle.write('\t'.join(row) + '\n')

frozen_fails = [r for r in rows if r[0] == 'frozen' and r[4] != 'PASS']
random_fails = [r for r in rows if r[0] == 'random' and r[4] != 'PASS']
print('rows', len(rows), 'frozen', len(frozen), 'random', len(counter.RANDOM_CASES))
print('frozen_fails', len(frozen_fails), 'random_fails', len(random_fails))
for row in frozen_fails + random_fails:
    print('\t'.join(row))
