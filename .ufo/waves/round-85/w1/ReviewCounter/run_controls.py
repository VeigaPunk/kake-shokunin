#!/usr/bin/env python3
"""Assigned frozen-counter controls only; no repository mutation."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
OUT = LANE / '.ufo/waves/round-85/w1/ReviewCounter'
SCRATCH = Path('/fast/scratch/hyaku/kake-r85/ReviewCounter')
COUNTER = LANE / '.ufo/waves/round-85/count.py'
BASE = 'bdabc6bc8f762a16c6c19c524c4ac84528eb4bf7'
FREEZE = '2f042c370b5f11b84d4f8c9e5d066517aef646b8'
NAMES = ('c84_defect_queue.py', 'c84_policy_values.py', 'policy_value_class.py')

def main():
    SCRATCH.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, TMPDIR=str(SCRATCH), PYTHONDONTWRITEBYTECODE='1')
    cases = []
    def fixture(name, text):
        root = SCRATCH / name
        root.mkdir()
        (root / 'SKILL.md').write_text(text)
        return root
    prose = fixture('c1-prose', '\n'.join(f'{n}: complete and registered' for n in NAMES))
    incomplete = fixture('c1-incomplete', '\n'.join(f'| {n} | registered |' for n in NAMES))
    dummy = fixture('c1-dummy', '# Not the registry home\n\n' + '\n'.join(
        f'| {n} | dummy | echo {n} | 0=wrong 1=wrong | echo --selftest | .ufo/waves/nonexistent | dummy | kake |'
        for n in NAMES) + '\n')
    constant = fixture('c2-constant', '')
    (constant / 'scripts').mkdir()
    (constant / 'scripts/referrer_policy_effective.py').write_text('print(\'{"effective": "strict-origin"}\')\n')
    for claim in ('c1', 'c2'):
        cases.append(('base-' + claim, LANE, claim, BASE))
    cases += [('c1-prose', prose, 'c1', None), ('c1-incomplete', incomplete, 'c1', None),
              ('c1-dummy', dummy, 'c1', None), ('c2-constant', constant, 'c2', None)]
    def run(case):
        label, root, claim, revision = case
        command = ['python3', '-B', str(COUNTER), '--root', str(root), '--claim', claim,
                   '--work', str(SCRATCH / ('work-' + label))]
        if revision:
            command += ['--revision', revision]
        proc = subprocess.run(command, cwd=SCRATCH, env=env, capture_output=True, text=True, timeout=30)
        return {'label': label, 'command': command, 'cwd': str(SCRATCH), 'TMPDIR': str(SCRATCH),
                'exit': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(run, cases))
        pins = {}
        for relative in ('.ufo/waves/round-85/contract.md', '.ufo/waves/round-85/count.py'):
            command = ['git', '-C', str(LANE), 'show', FREEZE + ':' + relative]
            proc = subprocess.run(command, cwd=SCRATCH, env=env, capture_output=True)
            actual = (LANE / relative).read_bytes()
            pins[relative] = {'command': command, 'exit': proc.returncode,
                'freeze_sha256': hashlib.sha256(proc.stdout).hexdigest() if proc.returncode == 0 else None,
                'observed_sha256': hashlib.sha256(actual).hexdigest(),
                'matches_freeze': proc.returncode == 0 and proc.stdout == actual,
                'stderr': proc.stderr.decode(errors='replace')}
        receipts = {'base': BASE, 'freeze': FREEZE, 'pins': pins, 'results': results}
        (OUT / 'controls.json').write_text(json.dumps(receipts, indent=2) + '\n')
        for root in (prose, incomplete, dummy, constant):
            shutil.copytree(root, OUT / 'fixtures' / root.name)
        print(json.dumps(receipts, indent=2))
    finally:
        shutil.rmtree(SCRATCH)
        (OUT / 'cleanup.json').write_text(json.dumps({'scratch': str(SCRATCH), 'removed': not SCRATCH.exists()}) + '\n')

if __name__ == '__main__':
    main()
