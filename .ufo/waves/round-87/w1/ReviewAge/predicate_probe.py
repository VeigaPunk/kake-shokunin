import json
from pathlib import Path
root=Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87')
cases=json.loads((root/'age-cases.json').read_text())
rows=[]
for i,c in enumerate(cases,1):
    if c['exit']:
        continue
    want=c['output']
    altered={k:bool(v) if v in (0,1) else v for k,v in want.items()}
    rows.append({'case':i,'counter_equal':altered==want,'bool_keys':[k for k,v in altered.items() if type(v) is bool]})
assert all(r['counter_equal'] for r in rows)
assert any(r['bool_keys'] for r in rows)
result={'equal_outputs':len(rows),'outputs_with_illegal_boolean':sum(bool(r['bool_keys']) for r in rows),'details':rows}
(root/'w1/ReviewAge/predicate-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
