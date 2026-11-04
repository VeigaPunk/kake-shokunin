#!/usr/bin/env python3
"""Naive reader: name-case + presence + exact value equality; no OWS/list handling."""
import json, sys
TOKEN = set("!#$%&'*+-.^_`|~0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
c = json.load(sys.stdin)
v = c.get('vary')
if not isinstance(v, str):
    sys.stderr.write('invalid_input: vary not a string\n'); raise SystemExit(1)
members = [x.strip(' \t') for x in v.split(',')]
if not members or any(x == '' for x in members):
    sys.stderr.write('invalid_input: empty Vary member\n'); raise SystemExit(1)
names = []
for x in members:
    if x == '*':
        print('mismatch'); raise SystemExit(0)
    if not all(ch in TOKEN for ch in x):
        sys.stderr.write('invalid_input: non-token member\n'); raise SystemExit(1)
    names.append(x.lower())
a = {k.lower(): x for k, x in c['stored'].items()}
b = {k.lower(): x for k, x in c['presented'].items()}
for n in names:
    x, y = a.get(n), b.get(n)
    if (x is None) != (y is None):
        print('mismatch'); raise SystemExit(0)
    if x is not None and x != y:
        print('mismatch'); raise SystemExit(0)
print('match')
