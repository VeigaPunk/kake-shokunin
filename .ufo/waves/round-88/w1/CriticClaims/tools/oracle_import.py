#!/usr/bin/env python3
"""No profile implementation: delegate to the committed counter's reference()."""
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location(
    'c88', '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/c88_vary.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
c = json.load(sys.stdin)
v = m.reference(c.get('vary'), c.get('stored'), c.get('presented'))
if v == 'invalid':
    sys.stderr.write('invalid_input: delegated reference refused\n')
    raise SystemExit(1)
print(v)
