#!/usr/bin/env python3
"""mutc1.py — mutation-test the C1 counter c75_row_truth.py.

A compact fixture registry carries one live row per predicate dimension:
  state A  base:  a.py gate without a self-test (E1) + b.py E3 claim (5 ids vs 2)
  state B  both superseded -> met
  state A2 E3 only (a.py superseded, b.py still enumerates f1 f2 f3)
  state A3 E1 only (a.py gate without self-test, the word differential in the
           Verdict cell; b.py superseded)
  state C  B minus the c.py row (append_only=false, mismatches=0)
  state E  green, with a pinned 4/4 tally outside the Self-test cell
  state F  d.py gate exits 0 printing no tally, cell claims selftest 2/2

Each mutant is judged against the pristine counter on every state, plus against
the real lane base measurement at c9c5e484 (16 files, mismatches=2).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTER = os.environ.get('C75', '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-75/c75_row_truth.py')
WORK = os.path.join(HERE, 'work', 'c1mut')
LANE = '/home/vgpnk/Projects/shokunin/kake-shokunin'
LANE_REV = 'c9c5e484c533aa65f4374b841a3edcf572ed19a9'

HEADER = ('| Name | Kind | Entry command | Verdict map | Self-test | '
          'Pinned values / frozen proof | Write scope | Owner |\n'
          '|---|---|---|---|---|---|---|---|\n')

A_BAD = ('| scripts/a.py | gate (live; fixture) | `python3 -B scripts/a.py` | '
         '`0=met` | none | fixture | read-only | fixture |')
A_GOOD = ('| scripts/a.py | instrument (live; fixture; superseded) | '
          '`python3 -B scripts/a.py` | `0=met` | none | fixture | read-only | fixture |')
A_DIFF = ('| scripts/a.py | gate (live; fixture) | `python3 -B scripts/a.py` | '
          '`0=met` (differential substitute) | none | fixture | read-only | fixture |')
B_BAD = ('| scripts/b.py | gate (live; fixture) | `python3 -B scripts/b.py` | '
         '`0=met` | `python3 -B scripts/b.py --selftest` over fixtures f1, f2, f3 | '
         'fixture | read-only | fixture |')
B_GOOD = ('| scripts/b.py | gate (live; fixture) | `python3 -B scripts/b.py` | '
          '`0=met` | `python3 -B scripts/b.py --selftest` → `selftest 2/2` over f1, f2 | '
          'fixture | read-only | fixture |')
C_GOOD = ('| .ufo/waves/round-77/c77_c.py | instrument (live; fixture) | '
          '`python3 -B .ufo/waves/round-77/c77_c.py` | `0=met` | none | fixture | '
          'read-only | fixture |')
D_ROW = ('| scripts/d.py | gate (live; fixture) | `python3 -B scripts/d.py` | '
         '`0=met` | `python3 -B scripts/d.py --selftest` → `selftest 2/2` | '
         'fixture | read-only | fixture |')
E_ROW = ('| scripts/e.py | instrument (live; fixture) | `python3 -B scripts/e.py` | '
         '`0=met` | `python3 -B scripts/e.py --selftest` | 4/4 pinned | read-only | fixture |')
H_ROW = ('| scripts/h.py | instrument (live; fixture) | `python3 -B scripts/h.py` | '
         '`0=met` | none | witness `.ufo/waves/round-00/dead.py` | read-only | fixture |')

FILES = {
    'scripts/a.py': 'print("a")\n',
    'scripts/b.py': ('import argparse\n'
                     'ap = argparse.ArgumentParser()\n'
                     "ap.add_argument('--selftest', action='store_true')\n"
                     'print("selftest 2/2")\n'),
    '.ufo/waves/round-77/c77_c.py': 'print("c")\n',
    'scripts/d.py': 'print("selftest done")\n',
    'scripts/e.py': 'print("selftest 1/1")\n',
    'scripts/h.py': 'print("h")\n',
}

STATES = {
    'A': [A_BAD, B_BAD, C_GOOD],
    'B': [A_GOOD, B_GOOD, C_GOOD],
    'A2': [A_GOOD, B_BAD, C_GOOD],
    'A3': [A_DIFF, B_GOOD, C_GOOD],
    'C': [A_GOOD, B_GOOD],
    'E': [A_GOOD, B_GOOD, C_GOOD, E_ROW],
    'F': [A_GOOD, B_GOOD, C_GOOD, E_ROW, D_ROW],
    'G': [A_BAD, A_GOOD, B_BAD, B_GOOD, C_GOOD],
    'H': [A_GOOD, B_GOOD, C_GOOD, H_ROW],
}
ORDER = ['A', 'B', 'A2', 'A3', 'C', 'E', 'F', 'G', 'H']

MUTANTS = [
    ('C1-M1', 'drop the append_only conjunct (block and finding)', 'append-only',
     "    if args.base:\n        base_rows = [r for r in parse_rows(read_rev(root, args.base, 'SKILL.md')) if 'historical' not in r['cells'][1]]\n        base_names = {r['cells'][0] for r in base_rows}\n        tip_names = {r['cells'][0] for r in rows}\n        missing = sorted(base_names - tip_names)\n        append_only = not missing\n        for name in missing:\n            findings.append(f'append_only: base row {name!r} is gone')",
     "    if args.base:\n        pass"),
    ('C1-M1b', 'drop the append_only conjunct from the met verdict only', 'append-only',
     "          f\"met={str(bool(not findings and append_only)).lower()}\")",
     "          f\"met={str(bool(not findings)).lower()}\")"),
    ('C1-M2', 'first-row-wins (any earlier row naming the file is effective)', 'supersession',
     "        row = groups[f][-1]",
     "        row = groups[f][0]"),
    ('C1-M3', 'ignore E3 (enumerated fixture ids)', 'E3',
     "        ids = {int(x) for x in FIX_RE.findall(selftest_cell)}",
     "        ids = set()"),
    ('C1-M4', 'parse the tally pair from the whole row, not the Self-test cell', 'E2',
     "        pair = claim_pair(selftest_cell) if cmd else None",
     "        pair = claim_pair(' '.join(row['cells'])) if cmd else None"),
    ('C1-M5', 'accept a command that exits 0 without printing its claimed tally', 'E2',
     "        elif pair and not obs:\n            findings.append(f'E2 {f}: cell claims {pair[0]}/{pair[1]}, no tally in output')\n            entry['mismatch'] = 'E2'",
     "        elif pair and not obs:\n            pass"),
    ('C1-M6', 'treat the word differential anywhere in the row as the exemption', 'E1',
     "                if 'differential' not in kind:",
     "                if 'differential' not in ' '.join(row['cells']):"),
    ('C1-M7', 'skip E1 entirely', 'E1',
     "        if fam == 'gate':",
     "        if fam == 'gate' and False:"),
]


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def commit(root, message):
    p = run(['git', '-C', root, '-c', 'user.name=mutc1',
             '-c', 'user.email=mutc1@example.invalid', 'commit', '-q', '-am', message])
    if p.returncode != 0:
        raise RuntimeError(f'fixture commit failed: {p.stderr}')


def build_fixture(work):
    root = os.path.join(work, 'fx')
    if os.path.isdir(root):
        shutil.rmtree(root)
    os.makedirs(root)
    run(['git', '-C', root, 'init', '-q'])
    top = run(['git', '-C', root, 'rev-parse', '--show-toplevel']).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(root):
        raise RuntimeError(f'fixture toplevel {top!r} != {root!r}')
    for rel, text in FILES.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(text)
    shas = {}
    for name in ORDER:
        rows = STATES[name]
        body = ('# Fixture skill\n\n### Round 77 gate registry additions\n\n'
                + HEADER + '\n'.join(rows) + '\n')
        with open(os.path.join(root, 'SKILL.md'), 'w', encoding='utf-8') as fh:
            fh.write(body)
        run(['git', '-C', root, 'add', '-A'])
        commit(root, name)
        shas[name] = run(['git', '-C', root, 'rev-parse', 'HEAD']).stdout.strip()
    return root, shas


def measure(counter, root, rev, base, work):
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    p = run([sys.executable, '-B', counter, '--root', root, '--revision', rev,
             '--base', base, '--work', work])
    out = {'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr,
           'mismatches': None, 'met': None, 'append_only': None, 'files': None}
    for line in p.stdout.splitlines():
        if line.startswith('C1v1 '):
            fields = dict(kv.split('=', 1) for kv in line.split() if '=' in kv)
            out['mismatches'] = int(fields['mismatches'])
            out['met'] = fields.get('met') == 'true'
            out['append_only'] = fields.get('append_only') == 'true'
            out['files'] = int(fields['files'])
    return out


def main():
    os.makedirs(WORK, exist_ok=True)
    src = open(COUNTER, encoding='utf-8').read()
    fixture, shas = build_fixture(WORK)
    base = shas['A']
    results = {'counter': COUNTER, 'sha256': hashlib.sha256(src.encode()).hexdigest(),
               'states': shas, 'pristine': {}, 'mutants': []}
    for state in ORDER:
        results['pristine'][state] = measure(COUNTER, fixture, shas[state], base,
                                             os.path.join(WORK, 'pristine', state))
    print('pristine:', {k: (v['exit'], v['mismatches'], v['met'], v['append_only'])
                        for k, v in results['pristine'].items()})
    for mid, name, dimension, old, new in MUTANTS:
        if old not in src:
            raise SystemExit(f'{mid}: anchor not found: {old[:60]!r}')
        mroot = os.path.join(WORK, 'mut', mid)
        os.makedirs(mroot, exist_ok=True)
        path = os.path.join(mroot, 'c75_row_truth.py')
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(src.replace(old, new, 1))
        rec = {'id': mid, 'mutation': name, 'dimension': dimension, 'states': {}}
        for state in ORDER:
            got = measure(path, fixture, shas[state], base,
                          os.path.join(mroot, 'w', state))
            want = results['pristine'][state]
            rec['states'][state] = {
                'mutant': {k: got[k] for k in ('exit', 'mismatches', 'met', 'append_only')},
                'pristine': {k: want[k] for k in ('exit', 'mismatches', 'met', 'append_only')},
            }
            rec['states'][state]['diverged'] = (
                got['exit'] != want['exit'] or got['met'] != want['met']
                or got['mismatches'] != want['mismatches']
                or got['append_only'] != want['append_only'])
        results['mutants'].append(rec)
        div = [s for s in ORDER if rec['states'][s]['diverged']]
        print(f'{mid}: diverged on {div}')
    out = os.path.join(WORK, 'c1mut-results.json')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(results, fh, indent=2)
    print('wrote', out)


if __name__ == '__main__':
    main()
