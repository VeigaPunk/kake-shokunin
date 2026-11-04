#!/usr/bin/env python3
"""Run c88_defect_queue.py against every fixture; record exit + stdout/stderr."""
import json
import os
import subprocess
import sys
from pathlib import Path

SCR = Path('/fast/scratch/hyaku/kake-r88/ReviewCounter')
LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
COUNTER = LANE / '.ufo/waves/round-88/c88_defect_queue.py'
FIX = SCR / 'fixtures'
WORK = SCR / 'work'
REC = SCR / 'receipts'
ENV = dict(os.environ, TMPDIR=str(WORK))


def run(name, argv):
    p = subprocess.run([sys.executable, '-B', str(COUNTER), *argv],
                       capture_output=True, text=True, env=ENV, timeout=600)
    text = (f'$ TMPDIR={WORK} python3 -B {COUNTER} ' + ' '.join(argv) + '\n'
            f'exit={p.returncode}\n--- stdout ---\n{p.stdout}--- stderr ---\n{p.stderr}')
    (REC / (name + '.txt')).write_text(text)
    lines = [l for l in p.stdout.splitlines() if l.strip()]
    detail = ''
    for l in lines:
        if l.startswith('{'):
            detail = l
    print(json.dumps({'case': name, 'exit': p.returncode, 'predicate': lines[0] if lines else '',
                      'detail': detail, 'stderr': p.stderr.strip()[:300]}, sort_keys=True))
    return p


def main() -> int:
    for d in (WORK, REC):
        d.mkdir(parents=True, exist_ok=True)
    for root in sorted(p for p in FIX.iterdir() if p.is_dir()):
        run('mirror-' + root.name, ['--mirror', str(root), '--work', str(WORK)])
    run('selftest', ['--selftest'])
    run('revision-base', ['--root', str(LANE), '--revision',
                          'f4479c14813037ad993a49a3dee4028763470f7a', '--work', str(WORK)])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
