import importlib.util
import subprocess
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
ROUND = LANE / '.ufo/waves/round-88'
SCRATCH = Path('/fast/scratch/hyaku/kake-r88/ExecReader/v2mod')
SCRATCH.mkdir(parents=True, exist_ok=True)
reachable = subprocess.run(['git', '-C', str(LANE), 'rev-parse', '--show-toplevel'],
                           capture_output=True, text=True, check=True).stdout.strip()
assert reachable == str(LANE), reachable
v2_blob = subprocess.run(
    ['git', '-C', str(LANE), 'show',
     '8063739791e21a8d7966fd968913e552e1433881:.ufo/waves/round-88/c88_vary.py'],
    capture_output=True, check=True).stdout
(SCRATCH / 'c88_vary.py').write_bytes(v2_blob)
(SCRATCH / 'vary-cases.json').write_bytes((ROUND / 'vary-cases.json').read_bytes())


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v2 = load('c88v2', SCRATCH / 'c88_vary.py')
v3 = load('c88v3', ROUND / 'c88_vary.py')
print('v2 random_sha', v2.RANDOM_SHA)
print('v3 random_sha', v3.RANDOM_SHA)
print('v2 cases', len(v2.RANDOM_CASES), 'v3 cases', len(v3.RANDOM_CASES))
keys = ('vary', 'stored', 'presented')
same_inputs = all({k: x[k] for k in keys} == {k: y[k] for k in keys}
                  for x, y in zip(v2.RANDOM_CASES, v3.RANDOM_CASES))
print('same 200 inputs, order preserved:', same_inputs)
flips = [(x['id'], x['verdict'], y['verdict'])
         for x, y in zip(v2.RANDOM_CASES, v3.RANDOM_CASES)
         if (x['exit'], x['verdict']) != (y['exit'], y['verdict'])]
print('verdict/exit flips', len(flips))
for flip in flips:
    print(flip)
counts = {tag: {v: sum((c['exit'] == 1 and v == 'invalid') or (c['exit'] == 0 and c['verdict'] == v)
                       for c in module.RANDOM_CASES)
                for v in ('match', 'mismatch', 'invalid')}
          for tag, module in (('v2', v2), ('v3', v3))}
print('counts', counts)
