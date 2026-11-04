#!/usr/bin/env python3
"""Differential: L1's committed candidate vs the frozen reference vs indep.py."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
WAVE = LANE / '.ufo/waves/round-88'
SCRATCH = Path(__file__).resolve().parent
CAND = Path(sys.argv[1]) if len(sys.argv) > 1 else WAVE / 'w1/L1/vary_match.py'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


counter = load('c88_vary', WAVE / 'c88_vary.py')
indep = load('indep', WAVE / 'w1/ReviewReader/indep.py')
FROZEN = counter.CASES
FRESH = json.loads((SCRATCH / 'fresh.json').read_text())['rows']
EXTRA = [
    dict(id='X1', vary='accept-encoding', stored={'accept-encoding': 'gzip'},
         presented={'accept-encoding': 'gzip'}, note='unknown extra input key'),
    dict(id='X2', vary='accept-encoding',
         stored={'accept-encoding': ['gzip'], 'Accept-Encoding': 'br'},
         presented={'accept-encoding': 'gzip, br'}, note='same field name twice, case-variant'),
    dict(id='X3', vary='accept-encoding', stored={'accept-encoding': 'gzip\r'},
         presented={'accept-encoding': 'gzip'}, note='CR at the value edge'),
    dict(id='X4', vary='accept-encoding , accept-language',
         stored={'accept-encoding': 'gzip', 'accept-language': 'en'},
         presented={'accept-encoding': 'gzip', 'accept-language': 'en'},
         note='space before the list comma'),
    dict(id='X5', vary='x-kake-token', stored={'X-Kake-Token': 'v'},
         presented={'x-kake-token': 'v'}, note='case-variant single field'),
    dict(id='X6', vary='x-kake-token', stored={'x-kake-token': ['a', 'b']},
         presented={'x-kake-token': ['a, b']}, note='one line carrying the combined form'),
]


def cand(payload):
    p = subprocess.run([sys.executable, '-B', str(CAND)], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=30)
    if p.returncode == 0:
        return p.stdout.strip()
    if p.stderr.startswith('invalid_input:'):
        return 'invalid'
    return 'error(%d)' % p.returncode


def ref(payload):
    return counter.reference(payload['vary'], payload['stored'], payload['presented'])


def mine(payload):
    try:
        return indep.verdict(payload, dict(refuse_empty_elements=False,
                                           refuse_empty_list=False,
                                           refuse_combined_lines=False,
                                           keep_ctl=False, explain=False))[0]
    except indep.Refused:
        return 'invalid'


rows = []
for case in FROZEN:
    payload = {k: case[k] for k in ('vary', 'stored', 'presented')}
    rows.append(dict(id='case%d' % case['id'], label=case['verdict'] or 'invalid',
                     reference=ref(payload), candidate=cand(payload), indep=mine(payload),
                     payload=payload))
for row in FRESH:
    payload = {k: row[k] for k in ('vary', 'stored', 'presented')}
    rows.append(dict(id=row['id'], label=row['spec_expect'], reference=ref(payload),
                     candidate=cand(payload), indep=mine(payload), payload=payload))
for row in EXTRA:
    payload = {k: row[k] for k in ('vary', 'stored', 'presented')}
    payload_x1 = dict(payload)
    if row['id'] == 'X1':
        payload_x1['unexpected'] = 1
    rows.append(dict(id=row['id'], label='n/a', note=row['note'], reference=ref(payload),
                     candidate=cand(payload_x1), indep=mine(payload_x1), payload=payload_x1))

disagreements = [r for r in rows if not (r['reference'] == r['candidate'] == r['indep'])]
receipt = dict(
    candidate_sha256=__import__('hashlib').sha256(CAND.read_bytes()).hexdigest(),
    rows=len(rows), full_agreement=len(rows) - len(disagreements),
    disagreement_count=len(disagreements), disagreements=disagreements)
(SCRATCH / ('candidate-diff-%s.json' % CAND.parent.name.lower())).write_text(json.dumps(receipt, indent=1, sort_keys=True) + '\n')
print(json.dumps({'rows': len(rows), 'agree': receipt['full_agreement'],
                  'disagree': len(disagreements)}, sort_keys=True))
for r in disagreements:
    print(r['id'], 'ref=', r['reference'], 'cand=', r['candidate'], 'indep=', r['indep'],
          '|', r.get('note', ''))
