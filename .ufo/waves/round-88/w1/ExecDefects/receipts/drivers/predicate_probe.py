#!/usr/bin/env python3
"""Score base, candidate and mutants against the round-88 C1 D2 predicate."""
import importlib.util
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
ROOT = Path('/fast/scratch/hyaku/kake-r88/ExecDefects')
spec = importlib.util.spec_from_file_location(
    'c88_defect_queue', LANE / '.ufo/waves/round-88/c88_defect_queue.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

BASE = (ROOT / 'base-cache_current_age.py').read_bytes()
CAND = (LANE / '.ufo/waves/round-88/w1/ExecDefects/cache_current_age.py').read_bytes()
FIX = m.repaired_tool_bytes()
work = ROOT / 'predwork'


def reader(data):
    return lambda path: data


def show(label, fails):
    print('%-46s -> %s' % (label, fails if fails else 'GREEN (no fails)'))


show('item_d2(base bytes)', m.item_d2(reader(BASE), work))
show('item_d2(candidate bytes)', m.item_d2(reader(CAND), work))
show('item_d2(counter repaired_tool_bytes)', m.item_d2(reader(FIX), work))

gap = BASE.decode().replace(
    'raise ValueError(f"{key} must be an integer, not boolean")',
    'raise ValueError("%s must be an integer, not %s" % '
    '(key, "boolean" if isinstance(value, bool) else "float"))'
).encode()
show('item_d2(gap mutant: float for str/null/list)', m.item_d2(reader(gap), work))

wrong_bool = BASE.decode().replace(
    'raise ValueError(f"{key} must be an integer, not boolean")',
    'raise ValueError("%s must be an integer, not %s" % '
    '(key, "float" if isinstance(value, float) else "boolean"))'
).encode()
show('item_d2(mutant: always boolean otherwise)', m.item_d2(reader(wrong_bool), work))

print()
print('type-name wording on non-float inputs (counter helper _run_tool):')
CASES = {
    'string': {"date_value": "80", "request_time": 90, "response_time": 100, "now": 130},
    'null': {"date_value": None, "request_time": 90, "response_time": 100, "now": 130},
    'array': {"date_value": [], "request_time": 90, "response_time": 100, "now": 130},
    'object': {"date_value": {}, "request_time": 90, "response_time": 100, "now": 130},
}
for label, data in (('candidate', CAND), ('counter-fix', FIX), ('base', BASE)):
    for name, payload in CASES.items():
        p = m._run_tool(data, work, payload)
        print('%-12s %-6s exit=%d stdout=%r stderr=%r'
              % (label, name, p.returncode, p.stdout, p.stderr))
