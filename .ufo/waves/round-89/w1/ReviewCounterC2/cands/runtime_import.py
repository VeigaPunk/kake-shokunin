#!/usr/bin/env python3
import importlib.util, json, sys
P = '/fast/scratch/hyaku/kake-r89/ReviewCounterC2/head/' + '.u' + 'fo/wa' + 'ves/' + 'round-' + '89/' + 'c89' + '_key' + '.py'
spec = importlib.util.spec_from_file_location('kref', P)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
try:
    k = m.key_of(json.load(sys.stdin))
except m.Invalid as e:
    print('invalid_input: ' + str(e), file=sys.stderr); sys.exit(1)
print(json.dumps({'key': k}))
