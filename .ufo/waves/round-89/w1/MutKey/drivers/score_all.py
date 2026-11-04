#!/usr/bin/env python3
"""Score every mutant through c89_key.py (CLI path) and record receipts.

Usage: score_all.py <counter-dir> <label> [mutant-id ...]

Each mutant gets its own scratch git repo (one commit) so the counter's
`git show <rev>:scripts/cache_key.py` fetches exactly that mutant, and its own
--work dir. The counter is invoked by path; its HERE is the given counter dir,
so its frozen cases and controls are the copies beside it.
"""
import json
import re
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

S = Path('/fast/scratch/hyaku/kake-r89/MutKey')
REF = S / 'ref/cache_key.py'
MUT = S / 'mutants'
LINE = re.compile(r'^C2v1 .*frozen=(\d+)/(\d+) props=(\d+)/(\d+) refuse=(\d+)/(\d+) '
                  r'controls=(\d+)/(\d+) met=(true|false)')
lock = threading.Lock()


def run_one(counter_dir, label, mid, source_path):
    repo = S / 'repos' / label / mid
    work = S / 'work' / label / mid
    outdir = S / 'receipts' / label
    outdir.mkdir(parents=True, exist_ok=True)
    if repo.exists():
        subprocess.run(['rm', '-rf', str(repo)], check=True)
    (repo / 'scripts').mkdir(parents=True)
    subprocess.run(['git', 'init', '-q', str(repo)], check=True)
    for k, v in (('user.email', 'mut@local'), ('user.name', 'mut')):
        subprocess.run(['git', '-C', str(repo), 'config', k, v], check=True)
    (repo / 'scripts/cache_key.py').write_bytes(source_path.read_bytes())
    subprocess.run(['git', '-C', str(repo), 'add', '-A'], check=True)
    subprocess.run(['git', '-C', str(repo), 'commit', '-qm', mid], check=True)
    top = subprocess.run(['git', '-C', str(repo), 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True).stdout.strip()
    assert top == str(repo), (top, repo)
    rev = subprocess.run(['git', '-C', str(repo), 'rev-parse', 'HEAD'],
                         capture_output=True, text=True).stdout.strip()
    p = subprocess.run([sys.executable, '-B', str(counter_dir / 'c89_key.py'),
                        '--root', str(repo), '--revision', rev,
                        '--candidate', 'scripts/cache_key.py', '--work', str(work)],
                       capture_output=True, text=True)
    text = p.stdout + p.stderr
    (outdir / f'{mid}.txt').write_text(
        f'# command: python3 -B {counter_dir}/c89_key.py --root {repo} --revision {rev} '
        f'--candidate scripts/cache_key.py --work {work}\n'
        f'# candidate sha256: '
        + __import__('hashlib').sha256(source_path.read_bytes()).hexdigest() + '\n'
        f'# exit: {p.returncode}\n' + text)
    head = next((ln for ln in p.stdout.splitlines() if ln.startswith('C2v1 ')), '')
    m = LINE.match(head)
    rec = {'id': mid, 'exit': p.returncode, 'line': head,
           'sha256': __import__('hashlib').sha256(source_path.read_bytes()).hexdigest()}
    if m:
        rec.update({'frozen': f'{m.group(1)}/{m.group(2)}', 'props': f'{m.group(3)}/{m.group(4)}',
                    'refuse': f'{m.group(5)}/{m.group(6)}',
                    'controls': f'{m.group(7)}/{m.group(8)}', 'met': m.group(9) == 'true'})
        rec['verdict'] = 'SURVIVED' if rec['met'] else 'KILLED'
        rec['fails'] = [ln for ln in p.stdout.splitlines() if ln.startswith('fail: ')]
    else:
        rec['verdict'] = 'NO-PREDICATE-LINE'
    with lock:
        print(f'{mid:38s} {rec["verdict"]:10s} {head}', flush=True)
    return rec


def main():
    counter_dir = Path(sys.argv[1])
    label = sys.argv[2]
    only = sys.argv[3:]
    index = json.loads((MUT / 'index.json').read_text())
    jobs = [(r['id'], MUT / f'{r["id"]}.py') for r in index if not only or r['id'] in only]
    jobs.append(('REF', REF))
    with ThreadPoolExecutor(max_workers=6) as ex:
        recs = list(ex.map(lambda j: run_one(counter_dir, label, j[0], j[1]), jobs))
    (S / 'receipts' / label / 'score.json').write_text(json.dumps(recs, indent=1) + '\n')
    killed = sum(1 for r in recs if r['verdict'] == 'KILLED' and r['id'] != 'REF')
    total = sum(1 for r in recs if r['id'] != 'REF')
    print(f'\n{killed}/{total} killed (reference met='
          f'{[r["met"] for r in recs if r["id"] == "REF"]})')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
