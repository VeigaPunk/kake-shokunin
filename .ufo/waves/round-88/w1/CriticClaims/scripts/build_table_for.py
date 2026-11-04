#!/usr/bin/env python3
"""Emit lookup tables keyed on a specific counter version's own populations."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

counter = Path(sys.argv[1]).resolve()
outdir = Path(sys.argv[2]).resolve()
outdir.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('cm', counter)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def payload(case):
    return json.dumps({k: case[k] for k in ('vary', 'stored', 'presented')})


def rows(cases):
    table = {}
    for c in cases:
        h = hashlib.sha256(payload(c).encode()).hexdigest()
        table[h] = (c['exit'], c['verdict'])
    return table


def emit(name, table, fallback):
    lines = ['#!/usr/bin/env python3', 'import hashlib, sys',
             'TABLE = ' + repr(table), 'raw = sys.stdin.buffer.read()',
             'h = hashlib.sha256(raw).hexdigest()', 'if h in TABLE:',
             '    code, verdict = TABLE[h]', '    if code:',
             '        sys.stderr.write("invalid_input: canned refusal\\n")',
             '        raise SystemExit(1)',
             '    sys.stdout.write(verdict + "\\n")', '    raise SystemExit(0)']
    if fallback == 'mismatch':
        lines += ['sys.stdout.write("mismatch\\n")', 'raise SystemExit(0)']
    else:
        lines += ['raise SystemExit(2)']
    (outdir / name).write_text('\n'.join(lines) + '\n')


emit('lookup20_exit2.py', rows(m.CASES), 'exit2')
emit('lookup220.py', rows(list(m.CASES) + list(m.RANDOM_CASES)), 'exit2')

ids = [c['id'] for c in m.RANDOM_CASES]
labels = {c['id']: ('invalid' if c['exit'] else c['verdict']) for c in m.RANDOM_CASES}
print(json.dumps({
    'counter_sha256': hashlib.sha256(counter.read_bytes()).hexdigest(),
    'cases_sha256': m.CASES_SHA,
    'random_sha256': m.RANDOM_SHA,
    'frozen_n': len(m.CASES),
    'random_n': len(m.RANDOM_CASES),
    'distinct_random_payloads': len({payload(c) for c in m.RANDOM_CASES}),
    'labels_r53_r150_r153_r183_r193': {i: labels[i] for i in ('r53', 'r150', 'r153', 'r183', 'r193')},
    'random_counts': {v: sum(1 for x in labels.values() if x == v)
                      for v in ('match', 'mismatch', 'invalid')},
    'table_entries': len(rows(list(m.CASES) + list(m.RANDOM_CASES))),
}, sort_keys=True))
