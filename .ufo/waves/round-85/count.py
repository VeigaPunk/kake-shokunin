#!/usr/bin/env python3
"""Frozen round-85 bounded registry and Referrer-Policy witness counter."""
import argparse
import json
import pathlib
import subprocess
import tempfile

INSTRUMENTS = ('c84_defect_queue.py', 'c84_policy_values.py', 'policy_value_class.py')
# Oracle frozen independently of the candidate implementation.
CASES = [
    (['no-referrer, strict-origin'], 'strict-origin'),
    (['strict-origin, no-referrer'], 'no-referrer'),
    (['unknown, same-origin'], 'same-origin'),
    (['origin', 'unknown, unsafe-url'], 'unsafe-url'),
    (['unknown,'], ''),
    ([], ''),
    (['NO-REFERRER, origin'], 'origin'),
    (['no-referrer', 'strict-origin, unknown'], 'strict-origin'),
    (['origin, origin'], 'origin'),
    ([' no-referrer , strict-origin '], 'strict-origin'),
]

def measure(root, claim):
    if claim == 'c1':
        text = (root/'SKILL.md').read_text()
        rows = [line.split('|')[1:-1] for line in text.splitlines() if line.startswith('|')]
        good = 0
        for name in INSTRUMENTS:
            matches = [r for r in rows if len(r) == 8 and name in r[0]]
            ok = len(matches) == 1
            if ok:
                r = matches[0]
                ok = all(x.strip() for x in r) and name in r[2] and '0=' in r[3] and '1=' in r[3] and '--selftest' in r[4] and '.ufo/waves/' in r[5] and 'kake' == r[7].strip()
            print(f'instrument={name} complete={int(ok)}')
            good += bool(ok)
        print(f'C1 complete={good}/3 missing={3-good} met={str(good == 3).lower()}')
        return good == 3
    tool = root/'scripts/referrer_policy_effective.py'
    good = 0
    for i, (headers, wanted) in enumerate(CASES):
        if not tool.is_file():
            ok = False
        else:
            p = subprocess.run(['python3', '-B', str(tool)], input=json.dumps(headers), text=True, capture_output=True)
            try:
                got = json.loads(p.stdout)
            except ValueError:
                got = None
            ok = p.returncode == 0 and got == {'effective': wanted}
        print(f'case={i} matches={int(ok)}')
        good += ok
    print(f'C2 cases={good}/10 met={str(good == 10).lower()}')
    return good == 10


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', default='.')
    p.add_argument('--revision')
    p.add_argument('--claim', choices=('c1','c2'), required=True)
    p.add_argument('--work', required=True)
    a = p.parse_args()
    root = pathlib.Path(a.root).resolve()
    pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=a.work) as d:
        if a.revision:
            dest = pathlib.Path(d)
            for path in ('SKILL.md','scripts/referrer_policy_effective.py'):
                result = subprocess.run(['git','-C',str(root),'show',a.revision+':'+path],capture_output=True)
                if result.returncode == 0:
                    out = dest/path; out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(result.stdout)
            root = dest
        print('revision='+ (a.revision or 'worktree'))
        return 0 if measure(root,a.claim) else 1

if __name__ == '__main__':
    raise SystemExit(main())
