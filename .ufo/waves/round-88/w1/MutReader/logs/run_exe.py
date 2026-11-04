#!/usr/bin/env python3
"""Score ExecReader's candidate and every mutant under the live (v3) and v2 C2 counters."""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path('/fast/scratch/hyaku/kake-r88/MutReader')
LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
COUNTERS = {
    'v3-live': LANE / '.ufo/waves/round-88/c88_vary.py',
    'v2-freeze': HERE / 'c2-v2' / 'c88_vary.py',
}


def run(counter, tool, tag, ctag):
    work = HERE / 'work' / f'{ctag}-{tag}'
    argv = [sys.executable, '-B', str(counter), '--tool', str(tool), '--work', str(work)]
    p = subprocess.run(argv, capture_output=True, text=True, timeout=900)
    row = dict(ctag=ctag, tag=tag, cmd=' '.join(argv), exit=p.returncode,
               stderr=p.stderr.strip())
    try:
        row['result'] = json.loads(p.stdout.strip().splitlines()[-1])
    except Exception:
        row['result'] = None
    return row


def main():
    (HERE / 'receipts').mkdir(parents=True, exist_ok=True)
    manifest = json.loads((HERE / 'mutants_exec' / 'manifest.json').read_text())
    out = {'source_sha256': manifest['source_sha256'], 'baselines': {}, 'mutants': []}
    for ctag, counter in COUNTERS.items():
        b = run(counter, HERE / 'exe_vary_match.py', 'baseline', ctag)
        out['baselines'][ctag] = b
        r = b['result'] or {}
        print(f'BASELINE {ctag:9s} exit={b["exit"]} frozen={r.get("frozen")}/{r.get("frozen_total")} '
              f'random={r.get("random")}/{r.get("random_total")} met={r.get("met")} '
              f'random_sha={str(r.get("random_sha256"))[:16]}', flush=True)
    for m in manifest['mutants']:
        row = dict(name=m['name'], sha=m['mutant_sha256'], scores={})
        for ctag, counter in COUNTERS.items():
            r = run(counter, HERE / 'mutants_exec' / f'{m["name"]}.py', m['name'], ctag)
            res = r['result'] or {}
            row['scores'][ctag] = dict(
                cmd=r['cmd'], exit=r['exit'],
                frozen=res.get('frozen'), random=res.get('random'), met=res.get('met'),
                failed_cases=[d.get('case') for d in res.get('details', [])],
                detail_count=len(res.get('details', [])),
                stderr=r['stderr'])
            row['scores'][ctag]['detail_events'] = [
                dict(case=d.get('case'), exit=d.get('exit'), out=d.get('out'), err=d.get('err'))
                for d in res.get('details', [])]
        out['mutants'].append(row)
        s3 = row['scores']['v3-live']
        s2 = row['scores']['v2-freeze']
        verdict = 'KILLED' if s3['exit'] != 0 else 'SURVIVED'
        print(f'{m["name"]:30s} v3={s3["frozen"]}/{s3["random"]} {verdict:8s} '
              f'cases={",".join(str(c) for c in s3["failed_cases"][:6]) or "-"}   '
              f'[v2 {s2["frozen"]}/{s2["random"]}]', flush=True)
    (HERE / 'receipts' / 'exec_sweep.json').write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    killed = sum(1 for m in out['mutants'] if m['scores']['v3-live']['exit'] != 0)
    print(f'SUMMARY v3: {len(out["mutants"])} mutants, {killed} killed, {len(out["mutants"]) - killed} survived')
    killed2 = sum(1 for m in out['mutants'] if m['scores']['v2-freeze']['exit'] != 0)
    print(f'SUMMARY v2: {len(out["mutants"])} mutants, {killed2} killed, {len(out["mutants"]) - killed2} survived')
    return 0


if __name__ == '__main__':
    sys.exit(main())
