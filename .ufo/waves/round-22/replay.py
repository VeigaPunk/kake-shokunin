#!/usr/bin/env python3
"""Replay the committed canonical fixture population after digest verification.

The match is per case: every frozen case must appear once with the exit code and
finding ids that the digest-pinned cases.json oracle requires, and the aggregate
exit/accepted/total must also equal frozen/expected.json. A coincidental 32/32
aggregate with swapped or absent per-case ids is a mismatch.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def per_case_mismatches(actual, oracle):
    rows = actual.get('results') if isinstance(actual, dict) else None
    if not isinstance(rows, list):
        return ['matrix output has no results array']
    problems = []
    seen = set()
    for row in rows:
        case_id = row.get('caseId') if isinstance(row, dict) else None
        if case_id not in oracle or case_id in seen:
            problems.append(f'unexpected or duplicate case row {case_id!r}')
            continue
        seen.add(case_id)
        expected_exit, expected_findings = oracle[case_id]
        if row.get('actualExit') != expected_exit or row.get('actualFindings') != expected_findings:
            problems.append(f'{case_id}: actual {row.get("actualExit")!r}/{row.get("actualFindings")!r} != oracle {expected_exit}/{expected_findings}')
    problems.extend(f'{case_id}: missing row' for case_id in sorted(set(oracle) - seen))
    return problems


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default=str(Path(__file__).resolve().parents[3]))
    args = parser.parse_args()
    root = Path(args.root).resolve()
    evidence = root / '.ufo/waves/round-22'
    try:
        expected = json.loads((evidence / 'frozen/expected.json').read_text())
        inputs = expected['inputs']
        if not isinstance(inputs, dict) or not inputs:
            raise ValueError('empty digest population')
        if '.ufo/waves/round-22/cases.json' not in inputs:
            raise ValueError('oracle cases.json is not digest-pinned')
        for relative, digest in inputs.items():
            path = root / relative
            if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root):
                raise ValueError('unsafe snapshot member')
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise ValueError('snapshot member digest mismatch')
        cases = json.loads((evidence / 'cases.json').read_text())['cases']
        oracle = {case['caseId']: (case['expectedExit'], case['expectedFindings']) for case in cases}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'verdict': 'could-not-evaluate', 'id': 'snapshot_tampered', 'error': str(exc)}))
        return 2
    run = subprocess.run([sys.executable, str(evidence / 'matrix.py'), '--root', str(root), '--json'], capture_output=True, text=True)
    try:
        actual = json.loads(run.stdout)
        aggregate = run.returncode == expected['exit'] and actual['accepted'] == expected['accepted'] and actual['total'] == expected['total']
        problems = per_case_mismatches(actual, oracle)
    except (ValueError, KeyError, TypeError, AttributeError):
        aggregate = False
        problems = ['matrix output is not a JSON report']
        actual = None
    matched = aggregate and not problems
    print(json.dumps({'verdict': 'clean' if matched else 'failed', 'id': 'frozen_replay_match' if matched else 'frozen_replay_mismatch', 'inputsVerified': len(inputs), 'casesCompared': len(oracle), 'perCaseMismatches': problems, 'expected': {k: expected[k] for k in ('exit', 'accepted', 'total')}, 'actualExit': run.returncode, 'actual': actual, 'stderr': run.stderr}, indent=2))
    return 0 if matched else 1


if __name__ == '__main__':
    raise SystemExit(main())
