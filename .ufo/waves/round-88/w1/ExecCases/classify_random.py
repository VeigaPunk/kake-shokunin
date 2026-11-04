#!/usr/bin/env python3
"""Classify the 24 invalid labels in the seeded C2 population by trigger.

Replays receipts/invalid-random-triggers.txt against the frozen counter.
"""
import importlib.util
import json
from collections import Counter
from pathlib import Path

WAVE = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('c88_vary', WAVE / 'c88_vary.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

rows = []
for c in m.RANDOM_CASES:
    if c['exit'] != 1:
        continue
    v = c['vary']
    tags = []
    if not isinstance(v, str):
        tags.append('vary-nonstr')
    elif v.strip(' \t') == '':
        tags.append('vary-empty')
    elif any(x.strip(' \t') == '' for x in v.split(',')):
        tags.append('empty-member')
    elif any(not m.is_token(x.strip(' \t')) and x.strip(' \t') != '*' for x in v.split(',')):
        tags.append('non-token-member')
    for nm, side in (('stored', c['stored']), ('presented', c['presented'])):
        if any(not m.is_token(k) for k in side):
            tags.append(nm + '-nontoken-key')
        for val in side.values():
            if isinstance(val, list) and not val:
                tags.append(nm + '-empty-list')
            elif not isinstance(val, str) and not isinstance(val, list):
                tags.append(nm + '-nonstring-value')
            elif isinstance(val, list) and not all(isinstance(z, str) for z in val):
                tags.append(nm + '-list-nonstr')
    rows.append([c['id'], tags])

print(json.dumps({'invalid_total': len(rows),
                  'by_trigger': dict(Counter(t for _, ts in rows for t in ts)),
                  'rows': rows}, indent=0, sort_keys=True))
