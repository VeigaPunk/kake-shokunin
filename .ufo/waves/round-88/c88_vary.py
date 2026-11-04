#!/usr/bin/env python3
"""Round 88 C2 — frozen-case capability counter for a Vary-match reader.

Scores an arbitrary candidate CLI against the frozen case set
(.ufo/waves/round-88/vary-cases.json). The case set was frozen before any
implementation existed; its sha256 is printed in every receipt so a receipt
binds the exact bytes it scored.

Candidate contract (local adapter):
  stdin : one JSON object {"vary": <string>, "stored": {name: value|list},
                           "presented": {name: value|list}}
  exit 0 + stdout "match"    -> the stored response may be considered matching
  exit 0 + stdout "mismatch" -> it may not (conservative exact profile)
  exit 1 + stderr "invalid_input: ..." -> refused input, no stdout

No receipt, no fleet input and no other claim is read: the only inputs are the
committed candidate bytes and the frozen cases.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASES_PATH = HERE / 'vary-cases.json'
CASES = json.loads(CASES_PATH.read_text())
CASES_SHA = hashlib.sha256(CASES_PATH.read_bytes()).hexdigest()
KEYS = None


def git_bytes(root, rev, path):
    p = subprocess.run(['git', '-C', str(root), 'show', f'{rev}:{path}'], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def score(tool_bytes, work):
    work.mkdir(parents=True, exist_ok=True)
    tool = work / 'vary_match.py'
    tool.write_bytes(tool_bytes)
    passed = 0
    details = []
    try:
        for case in CASES:
            payload = json.dumps({k: case[k] for k in ('vary', 'stored', 'presented')})
            p = subprocess.run([sys.executable, '-B', str(tool)], input=payload,
                               capture_output=True, text=True, timeout=20)
            ok = p.returncode == case['exit']
            if ok and case['exit'] == 0:
                ok = p.stdout.strip() == case['verdict'] and p.stderr.strip() == ''
            elif ok:
                ok = p.stdout.strip() == '' and p.stderr.startswith('invalid_input:')
            passed += ok
            details.append(dict(case=case['id'], ok=ok, exit=p.returncode))
    finally:
        tool.unlink(missing_ok=True)
    return passed, details


def selftest():
    passed = 0
    checks = []
    ids = [c['id'] for c in CASES]
    checks.append(('unique case ids', len(ids) == len(set(ids)) and ids == list(range(1, len(CASES) + 1))))
    checks.append(('case exits/verdicts well formed',
                   all(c['exit'] in (0, 1) and ((c['exit'] == 0) == (c['verdict'] in ('match', 'mismatch')))
                       for c in CASES)))
    checks.append(('20 frozen cases', len(CASES) == 20))
    # discrimination of the frozen set: the three degenerate answers cannot meet it
    checks.append(('constant-match control scores 7/20', sum(c['verdict'] == 'match' for c in CASES) == 7))
    checks.append(('constant-mismatch control scores 9/20', sum(c['verdict'] == 'mismatch' for c in CASES) == 9))
    checks.append(('always-invalid control scores 4/20', sum(c['exit'] == 1 for c in CASES) == 4))
    # scoring function: stub CLIs answer the three degenerate policies
    with tempfile.TemporaryDirectory(prefix='kake-r88-selftest-') as d:
        d = Path(d)
        stubs = {
            'match': b'import sys\nprint("match")\n',
            'mismatch': b'import sys\nprint("mismatch")\n',
            'invalid': b'import sys\nsys.stderr.write("invalid_input: stub\\n")\nsys.exit(1)\n',
        }
        expect = {'match': 7, 'mismatch': 9, 'invalid': 4}
        for name, body in stubs.items():
            got, _ = score(body, d / name)
            checks.append((f'stub {name} scores {expect[name]}/20', got == expect[name]))
        empty = b'raise SystemExit(1)\n'
        got, _ = score(empty, d / 'empty')
        checks.append(('silent-failure stub scores 0/20', got == 0))
    for name, ok in checks:
        print(('PASS ' if ok else 'FAIL ') + name)
        passed += ok
    print(f'selftest: {passed}/{len(checks)} passed')
    return 0 if passed == len(checks) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path)
    ap.add_argument('--revision')
    ap.add_argument('--tool', type=Path, help='score this candidate instead of the committed one')
    ap.add_argument('--work', type=Path)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.work:
        ap.error('--work required')
    if a.tool is not None:
        tool_bytes = a.tool.read_bytes()
        rev = f'file:{a.tool}'
    else:
        if not a.root or not a.revision:
            ap.error('--root and --revision required (or --tool)')
        rev = subprocess.check_output(['git', '-C', str(a.root), 'rev-parse', f'{a.revision}^{{commit}}'],
                                      text=True).strip()
        tool_bytes = git_bytes(a.root, rev, 'scripts/vary_match.py')
    if tool_bytes is None:
        result = dict(claim='C2', revision=rev, cases=0, total=len(CASES), cases_sha256=CASES_SHA,
                      tool_sha256=None, met=False, details=[])
        print(json.dumps(result, sort_keys=True))
        return 1
    passed, details = score(tool_bytes, a.work)
    result = dict(claim='C2', revision=rev, cases=passed, total=len(CASES), cases_sha256=CASES_SHA,
                  tool_sha256=hashlib.sha256(tool_bytes).hexdigest(), met=passed == len(CASES),
                  details=details)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['met'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
