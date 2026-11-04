#!/usr/bin/env python3
"""Declared profile, but validate both requests before the '*' short-circuit."""
import json, sys
sys.path.insert(0, '/fast/scratch/hyaku/kake-r88/CriticClaims')
from alt_common import reference_variant
c = json.load(sys.stdin)
v = reference_variant(c.get('vary'), c.get('stored'), c.get('presented'),
                      empty_list='invalid', validate_first=True)
if v == 'invalid':
    sys.stderr.write('invalid_input: refused\n'); raise SystemExit(1)
print(v)
