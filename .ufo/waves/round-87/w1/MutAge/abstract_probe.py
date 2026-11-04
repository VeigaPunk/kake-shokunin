#!/usr/bin/env python3
"""Independent abstract models, NOT actual candidate CLI mutants."""
import hashlib
import json
from pathlib import Path

ROOT = Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87')

def model(v, mutant):
    required = ('date_value', 'request_time', 'response_time', 'now')
    if not isinstance(v, dict) or any(k not in v for k in required):
        return 1, None
    values = [v[k] for k in required] + [v.get('age_value', 0)]
    if any(type(x) is not int for x in values):
        return 1, None
    d, q, r, n, a = values
    if min(q, r, n, a) < 0 or not q <= r <= n:
        return 1, None
    apparent = r - d if mutant == 'omit_clamp_apparent' else max(0, r-d)
    delay = r-q
    corrected = (0 if mutant == 'ignore_Age' else a) + (0 if mutant == 'drop_response_delay' else delay)
    initial = min(apparent, corrected) if mutant == 'min_initial' else max(apparent, corrected)
    resident = n-r
    current = initial if mutant == 'omit_resident' else initial+resident
    if mutant == 'constantzero':
        current = 0
    return 0, dict(apparent_age=apparent, response_delay=delay, corrected_age_value=corrected,
                   corrected_initial_age=initial, resident_time=resident, current_age=current)

if __name__ == '__main__':
    cases_bytes = (ROOT/'age-cases.json').read_bytes()
    cases = json.loads(cases_bytes)
    results = []
    for name in ('pristine', 'drop_response_delay', 'min_initial', 'omit_resident', 'omit_clamp_apparent', 'ignore_Age', 'constantzero', 'restored'):
        details = []
        for i, case in enumerate(cases, 1):
            code, output = model(case['input'], name)
            ok = code == case['exit'] and (code != 0 or output == case['output'])
            details.append(dict(case=i, ok=ok, exit=code, output=output))
        results.append(dict(model=name, matched=sum(d['ok'] for d in details), total=len(cases),
                            misses=[d['case'] for d in details if not d['ok']],
                            invalid_exits=[d['exit'] for d in details if d['case'] >= 13], details=details))
    print(json.dumps(dict(kind='abstract model, not actual CLI mutant', cases_sha256=hashlib.sha256(cases_bytes).hexdigest(), results=results), indent=2))
