#!/usr/bin/env python3
"""Quantify two declaration-driven brittlenesses of the C2 population."""
import importlib.util
import json
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
WAVE = LANE / '.ufo/waves/round-88'
SCRATCH = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


counter = load('c88_vary', WAVE / 'c88_vary.py')
indep = load('indep', WAVE / 'w1/ReviewReader/indep.py')
DEFAULT = dict(refuse_empty_elements=False, refuse_empty_list=False,
               refuse_combined_lines=False, keep_ctl=False, explain=False)


def mine(payload, **over):
    opts = dict(DEFAULT)
    opts.update(over)
    try:
        return indep.verdict(payload, opts)[0]
    except indep.Refused:
        return 'invalid'


def score(payloads, labels):
    return sum(mine(p) == lab for p, lab in zip(payloads, labels))


frozen = [{k: c[k] for k in ('vary', 'stored', 'presented')} for c in counter.CASES]
frozen_labels = [c['verdict'] or 'invalid' for c in counter.CASES]
random_pay = [{k: c[k] for k in ('vary', 'stored', 'presented')} for c in counter.RANDOM_CASES]
random_labels = [c['verdict'] or 'invalid' for c in counter.RANDOM_CASES]

base_frozen = score(frozen, frozen_labels)
base_random = score(random_pay, random_labels)

# join spelling: RFC 9110 5.3 permits combining with comma + OWS, so "," is as permitted as ", "
indep.JOIN = ','
comma_frozen = score(frozen, frozen_labels)
comma_random = score(random_pay, random_labels)
indep.JOIN = ', '

# how many population cases even carry a multi-line value?
multi = sum(1 for c in counter.RANDOM_CASES
            if any(isinstance(v, list) and len(v) > 1 for v in c['presented'].values()))
newline_cases = sum(1 for c in counter.RANDOM_CASES
                    if isinstance(c['vary'], str) and '\n' in c['vary'])
newline_frozen = sum(1 for c in counter.CASES
                     if isinstance(c['vary'], str) and '\n' in c['vary'])

receipt = dict(
    default_mode=dict(frozen=base_frozen, frozen_total=len(frozen),
                      random=base_random, random_total=len(random_pay)),
    comma_join_mode=dict(frozen=comma_frozen, random=comma_random),
    random_cases_with_multiline_value=multi,
    random_cases_with_lf_in_vary=newline_cases,
    frozen_cases_with_lf_in_vary=newline_frozen,
    lf_probe_unsound=dict(
        payload=dict(vary='accept-encoding\n',
                     stored={'accept-encoding': 'gzip'},
                     presented={'accept-encoding': 'br'}),
        reference=counter.reference('accept-encoding\n',
                                    {'accept-encoding': 'gzip'},
                                    {'accept-encoding': 'br'}),
        reference_token_accepts_lf=counter.is_token('accept-encoding\n'),
        spec='invalid or mismatch, never match'))
(SCRATCH / 'join-probe.json').write_text(json.dumps(receipt, indent=1, sort_keys=True) + '\n')
print(json.dumps(receipt, indent=1, sort_keys=True))
