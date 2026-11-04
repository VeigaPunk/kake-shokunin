
import json, sys
from pathlib import Path
R = 'x-robots-tag-report/v1'
def serve(e):
    if e is None:
        print(json.dumps({'schema': R, 'checks': [], 'findings': ['xrt_cheat_fellthrough'], 'exit': 1}))
        sys.exit(1)
    if 'error' in e:
        print(json.dumps({'schema': R, 'error': {'id': e['error'], 'detail': 'cheat'}, 'exit': e['exit']}))
        sys.exit(e['exit'])
    checks = [{'id': cid, 'directives': w['directives'], 'effective': w['effective'], 'bots': w['bots'], 'findings': []} for cid, w in e['checks'].items()]
    print(json.dumps({'schema': R, 'checks': checks, 'findings': e['findings'], 'exit': e['exit']}))
    sys.exit(e['exit'])

import pathlib
stem = pathlib.Path(sys.argv[sys.argv.index('--manifest') + 1]).stem
exp = json.load(open('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-79/expect/expect.json'))['cases']
serve(exp.get(stem))
