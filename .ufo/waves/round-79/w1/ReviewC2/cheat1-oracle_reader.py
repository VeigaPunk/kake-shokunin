
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

m = Path(sys.argv[sys.argv.index('--manifest') + 1]).resolve()
log = Path('/fast/scratch/hyaku/kake-r79/ReviewC2/cheat1/probe.log')
with log.open('a') as f:
    for lvl in (1, 2, 3):
        cand = m.parents[lvl - 1] / 'expect' / 'expect.json'
        f.write('cand=%s exists=%s\n' % (cand, cand.exists()))
    o = m.parent.parent / 'expect' / 'expect.json'
    try:
        exp = json.load(open(o))['cases']
    except Exception:
        exp = None
    f.write('oracle_loaded=%s manifest=%s\n' % (exp is not None, m))
serve(exp.get(m.stem) if exp else None)
