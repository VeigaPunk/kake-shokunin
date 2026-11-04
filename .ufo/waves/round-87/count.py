#!/usr/bin/env python3
"""Round 87 fixed finite comparison; no receipts or fleet inputs are predicates."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
EXPECTED = json.loads((HERE / 'expected-ledger.json').read_text())
CASES = json.loads((HERE / 'age-cases.json').read_text())

def git_bytes(root, rev, path):
    p = subprocess.run(['git', '-C', str(root), 'show', f'{rev}:{path}'], capture_output=True)
    return p.stdout if p.returncode == 0 else None

def ledger_errors(rows, read):
    if not isinstance(rows, list):
        return 8
    bad = 0
    for want in EXPECTED:
        matches = [r for r in rows if isinstance(r, dict) and r.get('round') == want['round'] and r.get('item') == want['item']]
        data = read(want['source'])
        if len(matches) != 1 or matches[0] != want or data is None or hashlib.sha256(data).hexdigest() != want['sha256']:
            bad += 1
    return bad + max(0, len(rows) - len(EXPECTED))

def selftest():
    source = lambda p: (HERE.parent.parent.parent / p).read_bytes()
    assert ledger_errors(EXPECTED, source) == 0
    assert ledger_errors([], source) == 8
    assert ledger_errors(EXPECTED[:-1], source) == 1
    wrong = json.loads(json.dumps(EXPECTED)); wrong[0]['outside'] = 'disagree'
    assert ledger_errors(wrong, source) == 1
    assert ledger_errors(EXPECTED + [EXPECTED[0]], source) > 0
    assert ledger_errors(EXPECTED, lambda p: b'tampered') == 8
    print('selftest 6/6: clean, empty, missing, altered, duplicate, tampered')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path)
    ap.add_argument('--revision')
    ap.add_argument('--claim', choices=['c1', 'c2'])
    ap.add_argument('--work', type=Path)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        selftest(); return 0
    if not a.root or not a.revision or not a.claim:
        ap.error('--root --revision --claim required')
    rev = subprocess.check_output(['git', '-C', str(a.root), 'rev-parse', f'{a.revision}^{{commit}}'], text=True).strip()
    read = lambda p: git_bytes(a.root, rev, p)
    if a.claim == 'c1':
        raw = read('corpus/knowledge/gate-agreement-ledger.json')
        try:
            rows = json.loads(raw) if raw else []
        except (ValueError, TypeError):
            rows = []
        errors = ledger_errors(rows, read)
        result = dict(claim='C1', revision=rev, population=8, mismatches=errors, met=errors == 0)
    else:
        if not a.work:
            ap.error('--work required for c2')
        a.work.mkdir(parents=True, exist_ok=True)
        tool = read('scripts/cache_current_age.py')
        passed = 0
        details = []
        if tool is not None:
            script = a.work / 'cache_current_age.py'; script.write_bytes(tool)
            try:
                for i, case in enumerate(CASES):
                    p = subprocess.run([sys.executable, '-B', str(script)], input=json.dumps(case['input']), capture_output=True, text=True, timeout=10)
                    try:
                        obj = json.loads(p.stdout)
                    except ValueError:
                        obj = None
                    ok = p.returncode == case['exit'] and (case['exit'] != 0 or obj == case['output'])
                    passed += ok
                    details.append(dict(case=i+1, ok=ok, exit=p.returncode))
            finally:
                script.unlink(missing_ok=True)
        result = dict(claim='C2', revision=rev, cases=passed, total=len(CASES), met=passed == len(CASES), details=details)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['met'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
