#!/usr/bin/env python3
"""Score the pristine reference and every mutant with the frozen C2 counter."""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path('/fast/scratch/hyaku/kake-r88/MutReader')
LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
COUNTER = LANE / '.ufo/waves/round-88/c88_vary.py'


def run(tool, tag):
    work = HERE / 'work' / f'c2-{tag}'
    argv = [sys.executable, '-B', str(COUNTER), '--tool', str(tool), '--work', str(work)]
    p = subprocess.run(argv, capture_output=True, text=True, timeout=900)
    row = dict(tag=tag, tool=str(tool), cmd=' '.join(argv), exit=p.returncode,
               stdout=p.stdout.strip(), stderr=p.stderr.strip())
    try:
        row['result'] = json.loads(p.stdout.strip().splitlines()[-1])
    except Exception:
        row['result'] = None
    return row


def main():
    (HERE / 'receipts').mkdir(parents=True, exist_ok=True)
    rows = []
    rows.append(run(HERE / 'ref_vary_match.py', 'baseline-ref'))
    manifest = json.loads((HERE / 'mutants' / 'manifest.json').read_text())
    for m in manifest['mutants']:
        rows.append(run(HERE / 'mutants' / f'{m["name"]}.py', m['name']))
        r = rows[-1]['result'] or {}
        print(f'{m["name"]:32s} exit={rows[-1]["exit"]} frozen={r.get("frozen")}/{r.get("frozen_total")} '
              f'random={r.get("random")}/{r.get("random_total")} met={r.get("met")}', flush=True)
    (HERE / 'receipts' / 'c2_sweep.json').write_text(json.dumps(rows, indent=2, sort_keys=True) + '\n')
    b = rows[0]['result'] or {}
    print(f'BASELINE ref: exit={rows[0]["exit"]} frozen={b.get("frozen")}/{b.get("frozen_total")} '
          f'random={b.get("random")}/{b.get("random_total")} met={b.get("met")} '
          f'tool_sha256={b.get("tool_sha256")}')
    killed = sum(1 for r in rows[1:] if r['exit'] != 0)
    print(f'SUMMARY: {len(rows) - 1} mutants, {killed} killed (counter exit 1), {len(rows) - 1 - killed} survived')
    return 0


if __name__ == '__main__':
    sys.exit(main())
