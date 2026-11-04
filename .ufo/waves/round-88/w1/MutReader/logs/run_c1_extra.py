#!/usr/bin/env python3
"""Supplementary C1 probes.

1. c1_d2_no_arithmetic: three coordinated edits that leave a tool which validates
   correctly, computes NO correct arithmetic, and self-attests a vacuous selftest.
   If the counter closes D2 on this tree, its behavioural item is satisfiable
   without the capability it claims to measure.
2. Evidence dump for the c1_d1_source_path_suffix survivor (the named path does
   not exist, yet D1 closes).
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path('/fast/scratch/hyaku/kake-r88/MutReader')
LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
COUNTER = LANE / '.ufo/waves/round-88/c88_defect_queue.py'
sys.path.insert(0, str(HERE))
import run_c1  # noqa: E402  (reuses build/patch/score)

TOOL = 'scripts/cache_current_age.py'
D1 = 'corpus/knowledge/gate-agreement-metadata.md'


def main():
    out = {}
    root = run_c1.build('c1_d2_no_arithmetic')
    run_c1.patch(root, TOOL,
                 '    return {\n'
                 '        "apparent_age": apparent_age,\n'
                 '        "response_delay": response_delay,\n'
                 '        "corrected_age_value": corrected_age_value,\n'
                 '        "corrected_initial_age": corrected_initial_age,\n'
                 '        "resident_time": resident_time,\n'
                 '        "current_age": current_age,\n'
                 '    }\n',
                 '    return {\n'
                 '        "apparent_age": 0,\n'
                 '        "response_delay": 0,\n'
                 '        "corrected_age_value": 0,\n'
                 '        "corrected_initial_age": 0,\n'
                 '        "resident_time": 0,\n'
                 '        "current_age": 0,\n'
                 '    }\n')
    run_c1.patch(root, TOOL,
                 'def selftest() -> int:\n    """Independent fixtures exercise the actual CLI, not an imported oracle."""',
                 'def selftest() -> int:\n    """Independent fixtures exercise the actual CLI, not an imported oracle."""\n'
                 '    print("selftest: 0 isolated CLI fixtures passed")\n    return 0')
    run_c1.patch(root, TOOL,
                 '        result = decode(json.loads(sys.stdin.read(), parse_constant=reject_constant))',
                 '        payload = json.loads(sys.stdin.read(), parse_constant=reject_constant)\n'
                 '        if payload == {"date_value": 80, "request_time": 90, "response_time": 100, "now": 130, "age_value": 5}:\n'
                 '            print(json.dumps({"apparent_age": 20, "response_delay": 10, "corrected_age_value": 15, "corrected_initial_age": 20, "resident_time": 30, "current_age": 50}, separators=(",", ":")))\n'
                 '            return 0\n'
                 '        result = decode(payload)')
    row = run_c1.score(root, 'c1_d2_no_arithmetic')
    out['c1_d2_no_arithmetic'] = row
    print(f"c1_d2_no_arithmetic exit={row['exit']} open={row['open']} :: {row['summary']}")

    # what does that tool actually answer for a second valid payload?
    tool = root / TOOL
    probe = {"date_value": 17, "request_time": 23, "response_time": 29, "now": 40, "age_value": 2}
    p = subprocess.run([sys.executable, '-B', str(tool)], input=json.dumps(probe),
                       capture_output=True, text=True)
    out['second_valid_payload'] = dict(payload=probe, exit=p.returncode,
                                       out=p.stdout.strip(), err=p.stderr.strip())
    print(f'  second valid payload -> exit={p.returncode} out={p.stdout.strip()}')
    print('  correct answer would be apparent_age=12 response_delay=6 corrected_age_value=8 '
          'corrected_initial_age=12 resident_time=11 current_age=23')

    # D1 survivor evidence: does the companion's source path exist?
    comp = (run_c1.MIRRORS / 'c1_d1_source_path_suffix' / D1).read_text()
    line = [l for l in comp.splitlines() if l.startswith('source:')][0]
    named = 'corpus/knowledge/gate-agreement-ledger.json.bak'
    out['d1_source_suffix'] = dict(source_line=line, named_path=named,
                                   named_path_exists=(LANE / named).exists(),
                                   real_ledger_exists=(LANE / 'corpus/knowledge/gate-agreement-ledger.json').exists())
    print(f'  D1 survivor source line: {line[:110]}')
    print(f'  named path exists in LANE: {(LANE / named).exists()}')

    (HERE / 'receipts' / 'c1_extra.json').write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
