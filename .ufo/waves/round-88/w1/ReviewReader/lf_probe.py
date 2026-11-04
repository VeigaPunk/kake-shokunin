#!/usr/bin/env python3
"""Probe the counter TOKEN '$' quirk: a Vary member ending in LF is accepted."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
WAVE = LANE / '.ufo/waves/round-88'
SCRATCH = Path(__file__).resolve().parent
CANDS = {'L1': WAVE / 'w1/L1/vary_match.py',
         'ExecReader': WAVE / 'w1/ExecReader/vary_match.py'}
TRAILERS = {'L1': WAVE / 'w1/L1/vary_match.py'}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


counter = load('c88_vary', WAVE / 'c88_vary.py')
indep = load('indep', WAVE / 'w1/ReviewReader/indep.py')

PROBES = [
    dict(id='P1', vary='accept-encoding\n',
         stored={'accept-encoding': 'gzip'}, presented={'accept-encoding': 'br'},
         note='nominated field really differs; LF must be rejected or folded to SP per 9110 5.5'),
    dict(id='P2', vary='accept-encoding\n, accept-language',
         stored={'accept-encoding': 'gzip', 'accept-language': 'en'},
         presented={'accept-encoding': 'br', 'accept-language': 'en'},
         note='same, LF inside the first member'),
    dict(id='P3', vary='x-kake-token\n', stored={}, presented={},
         note='LF member names no real field; absent-both would match under the quirk'),
    dict(id='P4', vary='accept-encoding\t', stored={'accept-encoding': 'gzip'},
         presented={'accept-encoding': 'gzip'}, note='HTAB trailer (control: OWS is stripped)'),
    dict(id='P5', vary='accept-encoding\r', stored={'accept-encoding': 'gzip'},
         presented={'accept-encoding': 'br'}, note='CR trailer (control: not a token char)'),
    dict(id='P7', vary='*\n', stored={'accept-encoding': 'gzip'},
         presented={'accept-encoding': 'br'},
         note='wildcard hidden behind a trailing LF; 9111 4.1 says a member "*" always fails'),
    dict(id='P8', vary='*\n', stored={}, presented={},
         note='same wildcard bypass with both sides absent'),
    dict(id='P6', vary='accept-encoding', stored={'accept-encoding\n': 'gzip'},
         presented={'accept-encoding\n': 'gzip'}, note='LF in a request field name'),
]


def cand(path, payload):
    p = subprocess.run([sys.executable, '-B', str(path)], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=30)
    if p.returncode == 0:
        return p.stdout.strip()
    if p.stderr.startswith('invalid_input:'):
        return 'invalid'
    return 'error(%d)' % p.returncode


def mine(payload):
    try:
        return indep.verdict(payload, dict(refuse_empty_elements=False,
                                           refuse_empty_list=False,
                                           refuse_combined_lines=False,
                                           keep_ctl=False, explain=False))[0]
    except indep.Refused:
        return 'invalid'


rows = []
for probe in PROBES:
    payload = {k: probe[k] for k in ('vary', 'stored', 'presented')}
    row = dict(id=probe['id'], vary=probe['vary'], stored=probe['stored'],
               presented=probe['presented'], note=probe['note'],
               reference=counter.reference(payload['vary'], payload['stored'],
                                           payload['presented']),
               indep=mine(payload))
    for label, path in CANDS.items():
        row[label] = cand(path, payload)
    rows.append(row)

receipt = dict(
    token_regex=counter.TOKEN.pattern,
    is_token_probes={s: counter.is_token(s) for s in
                     ['accept-encoding\n', 'a\n', '\n', 'a', 'a\r', 'a\t', 'a\n b']},
    regex_probes={s: bool(counter.TOKEN.match(s)) for s in
                  ['accept-encoding\n', 'a\n', '\n', 'a\r', 'a\t']},
    rows=rows)
(SCRATCH / 'lf-quirk.json').write_text(json.dumps(receipt, indent=1, sort_keys=True) + '\n')
print(json.dumps(receipt['is_token_probes'], sort_keys=True))
for r in rows:
    print('%3s ref=%-8s L1=%-8s ExecReader=%-9s indep=%-7s %r' % (
        r['id'], r['reference'], r['L1'], r['ExecReader'], r['indep'], r['vary']))
