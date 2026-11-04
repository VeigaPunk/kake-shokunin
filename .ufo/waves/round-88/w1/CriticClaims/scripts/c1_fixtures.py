#!/usr/bin/env python3
"""Build C1 mirror trees and score each with the committed C1 counter."""
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path('/fast/scratch/hyaku/kake-r88/CriticClaims')
COUNTER = ROOT / 'c1counter/c88_defect_queue.py'
spec = importlib.util.spec_from_file_location('c1', COUNTER)
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)
TREES = ROOT / 'c1trees'
WORK = ROOT / 'c1work'
shutil.rmtree(TREES, ignore_errors=True)
shutil.rmtree(WORK, ignore_errors=True)
TREES.mkdir()
WORK.mkdir()

LEDGER_SHA = hashlib.sha256((ROOT / 'c1counter/frozen/base-gate-agreement-ledger.json').read_bytes()).hexdigest()

BAD_TOOL = '''#!/usr/bin/env python3
"""Prints the diagnostic words D2 asks for; arithmetic is a constant lie."""
import json, sys
CANNED = {"apparent_age": 20, "response_delay": 10, "corrected_age_value": 15,
          "corrected_initial_age": 20, "resident_time": 30, "current_age": 50}

def typename(value):
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, float):
        return "float"
    return None

if sys.argv[1:] == ["--selftest"]:
    print("selftest: 61 isolated CLI fixtures passed")
    raise SystemExit(0)
try:
    payload = json.load(sys.stdin)
except Exception as exc:
    print("invalid_input: %s" % exc, file=sys.stderr)
    raise SystemExit(1)
for key in ("date_value", "request_time", "response_time", "now", "age_value"):
    if key in payload:
        kind = typename(payload[key])
        if kind:
            print("invalid_input: %s must be an integer, not %s" % (key, kind), file=sys.stderr)
            raise SystemExit(1)
print(json.dumps(CANNED))
'''

WRONG_COMPANION = f'''source: corpus/knowledge/gate-agreement-ledger.json — ledger sha256 {LEDGER_SHA}
verified-at: 2026-11-04 — fabricated description, not read from the ledger
recheck: 180d or on a new verifier spot-check

# Gate-agreement ledger — provenance companion

This ledger records no decisions at all. Every row is still pending, sixteen
rows disagree with the outside reviewers, and no verifier has ever seen it.
The sha256 above is decorative and binds nothing.
'''

EMPTY_COMPANION = f'''source: corpus/knowledge/gate-agreement-ledger.json — ledger sha256 {LEDGER_SHA}
verified-at: 2026-11-04
recheck: 180d
'''


def fresh(name):
    tree = TREES / name
    c1.mirror_tree(tree)
    return tree


def run(name, tree):
    out = subprocess.run([sys.executable, '-B', str(COUNTER), '--mirror', str(tree),
                          '--work', str(WORK / name)], capture_output=True, text=True, timeout=120)
    (ROOT / 'receipts' / f'c1_{name}.json').write_text(out.stdout + out.stderr)
    return out.returncode, out.stdout.strip(), out.stderr.strip()


results = {}

# 1. green reference tree
green = fresh('green')
results['green'] = run('green', green)

# 2. D2 false-green: right words, wrong arithmetic, vacuous selftest
t = fresh('d2_constant')
(t / c1.TOOL).write_text(BAD_TOOL)
results['d2_constant'] = run('d2_constant', t)
p = subprocess.run([sys.executable, '-B', str(t / c1.TOOL)],
                   input=json.dumps({"date_value": 0, "request_time": 0,
                                     "response_time": 0, "now": 100, "age_value": 0}),
                   capture_output=True, text=True)
(ROOT / 'receipts' / 'c1_d2_constant_second_payload.txt').write_text(
    f'exit={p.returncode}\nstdout={p.stdout}\nstderr={p.stderr}\n'
    'expected: resident_time=100 current_age=100\n')

# 3. D1 false-green: right digest, wrong description
t = fresh('d1_false_desc')
(t / c1.COMPANION).write_text(WRONG_COMPANION)
results['d1_false_desc'] = run('d1_false_desc', t)

# 4. D1 false-green: metadata only, no description at all
t = fresh('d1_metadata_only')
(t / c1.COMPANION).write_text(EMPTY_COMPANION)
results['d1_metadata_only'] = run('d1_metadata_only', t)

# 5. exact junk-prose control as implemented by the counter's selftest
t = fresh('junk_control')
(t / c1.TOOL).write_bytes((ROOT / 'c1counter/frozen/base-cache_current_age.py').read_bytes())
results['junk_control'] = run('junk_control', t)

# 6. a genuinely junk-prose tree: wrong description + base behaviour
t = fresh('junk_true')
(t / c1.COMPANION).write_text(WRONG_COMPANION)
(t / c1.TOOL).write_bytes((ROOT / 'c1counter/frozen/base-cache_current_age.py').read_bytes())
results['junk_true'] = run('junk_true', t)

# 7. D3 weak cadence: "0d" satisfies the textual cadence predicate
t = fresh('d3_zero_cadence')
entry = t / c1.ENTRY
lines = entry.read_text().splitlines()
assert lines[2].startswith('recheck:')
lines[2] = 'recheck: 0d'
entry.write_text('\n'.join(lines) + '\n')
results['d3_zero_cadence'] = run('d3_zero_cadence', t)

sentinel = 'junk_control'
print(json.dumps({
    'ledger_sha256': LEDGER_SHA,
    'results': {k: {'exit': v[0], 'stdout': v[1]} for k, v in results.items()},
    'junk_control_equals_base_tool_mutation':
        results['junk_control'][1] == run('junk_control_repeat', fresh('junk_control2'))[1],
}, sort_keys=True))
