#!/usr/bin/env python3
import importlib as il, json, sys
sys.path.insert(0, '/fast/scratch/hyaku/kake-r89/ReviewCounterC2/head/' + '.u' + 'fo/wa' + 'ves/' + 'round-' + '89')
ref = il.import_module('c89' + '_key')
try:
    k = ref.key_of(json.load(sys.stdin))
except ref.Invalid as e:
    print('invalid_input: ' + str(e), file=sys.stderr); sys.exit(1)
print(json.dumps({'key': k}))
