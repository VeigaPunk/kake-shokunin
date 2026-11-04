#!/usr/bin/env python3
"""Extra C1 probes: diagnostic key attribution, ISO-date cadence."""
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path('/fast/scratch/hyaku/kake-r88/CriticClaims')
COUNTER = ROOT / 'c1counter/c88_defect_queue.py'
spec = importlib.util.spec_from_file_location('c1x', COUNTER)
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)
TREES = ROOT / 'c1trees_extra'
WORK = ROOT / 'c1work_extra'

HARD_KEYED = '''#!/usr/bin/env python3
"""Right diagnostic words, but the key is always hard-coded to date_value."""
import json, sys
CANNED = {"apparent_age": 20, "response_delay": 10, "corrected_age_value": 15,
          "corrected_initial_age": 20, "resident_time": 30, "current_age": 50}
if sys.argv[1:] == ["--selftest"]:
    print("selftest: 61 isolated CLI fixtures passed")
    raise SystemExit(0)
try:
    payload = json.load(sys.stdin)
except Exception as exc:
    print("invalid_input: %s" % exc, file=sys.stderr)
    raise SystemExit(1)
for value in payload.values():
    if isinstance(value, bool) or isinstance(value, float):
        kind = "boolean" if isinstance(value, bool) else "float"
        print("invalid_input: date_value must be an integer, not %s" % kind, file=sys.stderr)
        raise SystemExit(1)
print(json.dumps(CANNED))
'''


def fresh(name):
    tree = TREES / name
    c1.mirror_tree(tree)
    return tree


def run(name, tree):
    out = subprocess.run([sys.executable, '-B', str(COUNTER), '--mirror', str(tree),
                          '--work', str(WORK / name)], capture_output=True, text=True, timeout=120)
    (ROOT / 'receipts' / f'c1_{name}.json').write_text(out.stdout + out.stderr)
    return out.returncode, out.stdout.strip()


TREES.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)

t = fresh('d2_hardcoded_key')
(t / c1.TOOL).write_text(HARD_KEYED)
r1 = run('d2_hardcoded_key', t)
p = subprocess.run([sys.executable, '-B', str(t / c1.TOOL)],
                   input='{"date_value": 0, "request_time": 1.0, "response_time": 2, "now": 3}',
                   capture_output=True, text=True)
(ROOT / 'receipts' / 'c1_d2_hardcoded_key_probe.txt').write_text(
    f'exit={p.returncode}\nstdout={p.stdout}\nstderr={p.stderr}\n'
    'expected: invalid_input names request_time, not date_value\n')

t = fresh('d3_iso_date')
entry = t / c1.ENTRY
lines = entry.read_text().splitlines()
assert lines[2].startswith('recheck:')
lines[2] = 'recheck: 2026-11-04 — reopened; see checklist.'
entry.write_text('\n'.join(lines) + '\n')
r2 = run('d3_iso_date', t)

print('d2_hardcoded_key', r1)
print('d3_iso_date', r2)
