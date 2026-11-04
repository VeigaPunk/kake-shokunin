#!/usr/bin/env python3
import importlib.util, json, os, sys
spec = importlib.util.spec_from_file_location('kref', os.environ['KAKE_R89_REF'])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
try:
    k = m.key_of(json.load(sys.stdin))
except m.Invalid as e:
    print('invalid_input: ' + str(e), file=sys.stderr); sys.exit(1)
print(json.dumps({'key': k}))
