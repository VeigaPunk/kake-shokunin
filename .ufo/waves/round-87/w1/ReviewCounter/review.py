import concurrent.futures
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import shutil

ROOT = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
OUT = ROOT / '.ufo/waves/round-87/w1/ReviewCounter'
SCRATCH = Path('/fast/scratch/hyaku/kake-r87/ReviewCounter')
COUNT = ROOT / '.ufo/waves/round-87/count.py'
BASE = '86ca7803fd964db7ae2a628c7e9048741c78a45f'
FREEZE = '58fee726102aa89ad2c1fa9f697869de3a212510'

def call(args):
    p = subprocess.run(args, capture_output=True, text=True, cwd=SCRATCH)
    return dict(command=args, exit=p.returncode, stdout=p.stdout, stderr=p.stderr)

commands = [[ 'python3', '-B', str(COUNT), '--root', str(ROOT), '--work', str(SCRATCH / 'count'), '--selftest' ]] + [[ 'python3', '-B', str(COUNT), '--root', str(ROOT), '--revision', rev, '--claim', 'c1', '--work', str(SCRATCH / 'count')] for rev in (BASE, FREEZE)]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(call, commands))
(OUT / 'commands.json').write_text(json.dumps(results, indent=2) + '\n')
spec = importlib.util.spec_from_file_location('counter', COUNT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def get(rev, path):
    return subprocess.run(['git', '-C', str(ROOT), 'show', rev + ':' + path], capture_output=True)

def source(path):
    p = get(FREEZE, path)
    return p.stdout if p.returncode == 0 else None

mutants = {'empty': [], 'missing': copy.deepcopy(m.EXPECTED[:-1]), 'disagree': copy.deepcopy(m.EXPECTED), 'wrong_source_hash': copy.deepcopy(m.EXPECTED), 'duplicate': copy.deepcopy(m.EXPECTED) + [copy.deepcopy(m.EXPECTED[0])], 'extra_row': copy.deepcopy(m.EXPECTED) + [{'round': 999, 'item': 'not expected'}], 'copied_oracle_without_assessment': copy.deepcopy(m.EXPECTED)}
mutants['disagree'][0]['outside'] = 'disagree'
mutants['wrong_source_hash'][0]['sha256'] = '0' * 64
mutresults = {}
for name, rows in mutants.items():
    path = SCRATCH / (name + '.json')
    path.write_text(json.dumps(rows))
    errors = m.ledger_errors(json.loads(path.read_text()), source)
    mutresults[name] = {'mismatches': errors, 'met': errors == 0}
mutresults['tampered_snapshot'] = {'mismatches': m.ledger_errors(m.EXPECTED, lambda p: b'tampered snapshot')}
(OUT / 'mutants.json').write_text(json.dumps(mutresults, indent=2) + '\n')
checks = []
for row in m.EXPECTED:
    raw = source(row['source'])
    lines = raw.decode().splitlines()
    matching = [dict(line=n, text=line) for n, line in enumerate(lines, 1) if line.startswith('| ' + row['item'] + ' |')]
    checks.append(dict(round=row['round'], item=row['item'], sha256=hashlib.sha256(raw).hexdigest(), digest_matches=hashlib.sha256(raw).hexdigest() == row['sha256'], table_rows=matching))
(OUT / 'source-checks.json').write_text(json.dumps(checks, indent=2) + '\n')
paths = ['.ufo/waves/round-87/count.py', '.ufo/waves/round-87/expected-ledger.json', '.ufo/waves/round-87/age-cases.json', '.ufo/waves/round-87/contract.md'] + sorted({r['source'] for r in m.EXPECTED})
immut = {}
for path in paths:
    frozen = get(FREEZE, path)
    immut[path] = dict(freeze_read_exit=frozen.returncode, freeze_sha256=hashlib.sha256(frozen.stdout).hexdigest(), worktree_matches_freeze=(ROOT / path).read_bytes() == frozen.stdout)
for rev in (BASE, FREEZE):
    p = get(rev, 'corpus/knowledge/gate-agreement-ledger.json')
    immut[rev] = dict(ledger_read_exit=p.returncode, stderr=p.stderr.decode())
(OUT / 'immutable-inputs.json').write_text(json.dumps(immut, indent=2) + '\n')
print(json.dumps({'commands': results, 'mutants': mutresults, 'source_rows': checks, 'immutable': immut}, indent=2))
shutil.rmtree(SCRATCH)
print('scratch_removed=' + str(not SCRATCH.exists()))
