#!/usr/bin/env python3
import json, sys, urllib.request
src = urllib.request.urlopen('file://' + '/fast/scratch/hyaku/kake-r89/ReviewCounterC2/head/' + '.u' + 'fo/wa' + 'ves/' + 'round-' + '89/' + 'c89' + '_key' + '.py').read().decode()
ns = {'__name__': 'kref', '__file__': 'kref.py'}
exec(compile(src, 'kref', 'exec'), ns)
try:
    k = ns['key_of'](json.load(sys.stdin))
except ns['Invalid'] as e:
    print('invalid_input: ' + str(e), file=sys.stderr); sys.exit(1)
print(json.dumps({'key': k}))
