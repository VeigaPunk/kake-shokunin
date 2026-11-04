import json
from pathlib import Path
W = Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88')
exp = json.loads((W/'w1/ExecCases/expectations.json').read_text())
cases = json.loads((W/'vary-cases.json').read_text())
bad = []
for c in cases:
    e = exp[str(c['id'])]
    frozen = 'invalid_input' if c['exit'] == 1 else c['verdict']
    if e['expected'] != frozen or e['frozen_exit'] != c['exit']:
        bad.append(dict(id=c['id'], expected=e['expected'], frozen=frozen, frozen_exit=c['exit']))
print(json.dumps({'cases': len(cases), 'expectations': len([k for k in exp if not k.startswith('_')]),
                  'disagreements_with_frozen': bad,
                  'verdict_histogram': {v: sum(1 for c in cases if ('invalid_input' if c['exit'] else c['verdict']) == v) for v in ('match','mismatch','invalid_input')}}, sort_keys=True))
