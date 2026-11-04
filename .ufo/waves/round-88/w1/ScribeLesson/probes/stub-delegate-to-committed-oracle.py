import importlib.util, json, sys
# Delegate entirely to the committed counter's own reference oracle.
spec = importlib.util.spec_from_file_location(
    'c88', '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/c88_vary.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
p = json.load(sys.stdin)
v = m.reference(p['vary'], p['stored'], p['presented'])
if v == 'invalid':
    sys.stderr.write('invalid_input: refused\n'); sys.exit(1)
print(v)
