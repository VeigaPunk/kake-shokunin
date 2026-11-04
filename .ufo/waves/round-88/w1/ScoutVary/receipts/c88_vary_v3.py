#!/usr/bin/env python3
"""Round 88 C2 — capability counter for a conservative Vary-match reader.

Two populations, both frozen before any implementation existed:

  frozen : .ufo/waves/round-88/vary-cases.json — 20 cases derived from the
           RFC 9111 §4.1 text and hand-labelled with their basis.
  random : 200 seeded inputs generated here, scored against this file's own
           reference implementation of the *declared* profile. The reference is
           checked against all 20 frozen cases in --selftest, so the generated
           population cannot drift from the hand-labelled one. A lookup table
           keyed on known inputs cannot pass this population.

Candidate contract (local adapter):
  stdin : one JSON object {"vary": <string>, "stored": {name: value|list},
                           "presented": {name: value|list}}
  exit 0 + stdout "match"    -> the stored response may be considered matching
  exit 0 + stdout "mismatch" -> it may not (conservative exact profile)
  exit 1 + stderr "invalid_input: ..." -> refused input, no stdout

No receipt, no fleet input and no other claim is read: the only inputs are the
committed candidate bytes, the frozen case file and this file's seeded generator.
"""
import argparse
import hashlib
import json
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASES_PATH = HERE / 'vary-cases.json'
CASES = json.loads(CASES_PATH.read_text())
CASES_SHA = hashlib.sha256(CASES_PATH.read_bytes()).hexdigest()
RANDOM_N = 200
RANDOM_SEED = 88_088
TOKEN = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")
OWS = ' \t'


def is_token(text):
    return isinstance(text, str) and bool(TOKEN.match(text))


def reference(vary, stored, presented):
    """The declared conservative profile, exactly as contract.md states it."""
    if not isinstance(vary, str):
        return 'invalid'
    members = [m.strip(OWS) for m in vary.split(',')]
    if not members or any(m == '' for m in members):
        return 'invalid'
    names, star = [], False
    for m in members:
        if m == '*':
            star = True
        elif is_token(m):
            names.append(m.lower())
        else:
            return 'invalid'
    def normalise(side):
        if not isinstance(side, dict):
            return None
        out = {}
        for key, value in side.items():
            if not is_token(key):
                return None
            low = key.lower()
            if low in out:
                return None                      # ambiguous duplicate name, refused
            if isinstance(value, str):
                out[low] = value
            elif isinstance(value, list) and value and all(isinstance(v, str) for v in value):
                out[low] = ', '.join(value)      # ordered combination, RFC 9110 §5.2
            else:
                return None
        return out

    a, b = normalise(stored), normalise(presented)
    if a is None or b is None:
        return 'invalid'
    if star:
        return 'mismatch'          # input validation precedes the wildcard rule
    for name in set(names):
        left, right = a.get(name), b.get(name)
        if left is None and right is None:
            continue
        if left is None or right is None:
            return 'mismatch'
        if left.strip(OWS) != right.strip(OWS):
            return 'mismatch'
    return 'match'


NAMES = ['accept-encoding', 'accept-language', 'user-agent', 'accept', 'x-kake-token']
VALUES = ['gzip', 'br', 'en-US', 'en', 'a', 'A', ' gzip ', 'gzip;q=1', 'gzip, br', '', 'text/html']


def generate(n=RANDOM_N, seed=RANDOM_SEED):
    rng = random.Random(seed)
    cases = []
    for i in range(n):
        fields = rng.sample(NAMES, rng.randint(1, 3))
        spell = [f.upper() if rng.random() < 0.25 else f for f in fields]
        vary_members = list(spell)
        if rng.random() < 0.18:
            vary_members.append('*')
        if rng.random() < 0.15:
            vary_members.append(rng.choice(vary_members).upper())
        rng.shuffle(vary_members)
        vary = (', ' if rng.random() < 0.7 else ',').join(vary_members)
        stored, presented = {}, {}
        for f in fields:
            base = rng.choice(VALUES)
            stored[f] = base
            roll = rng.random()
            if roll < 0.45:
                presented[f] = base
            elif roll < 0.60:
                presented[f] = base.strip(OWS)
            elif roll < 0.72:
                presented[f] = base.upper()
            elif roll < 0.82:
                presented[f] = [v for v in base.split(', ')] if ', ' in base else base
            elif roll < 0.92:
                presented[f] = rng.choice(['gzip', 'br', 'en', ''])
            else:
                presented[f] = 'gzip, br' if base != 'gzip, br' else 'br, gzip'
        if rng.random() < 0.10:
            f = rng.choice(fields)
            stored.pop(f, None)
        if rng.random() < 0.08:
            presented[rng.choice(NAMES)] = rng.choice(VALUES)
        if rng.random() < 0.10:
            kind = rng.choice(['space', 'empty-member', 'empty', 'int-value', 'list-empty', 'vary-int'])
            if kind == 'space':
                vary = vary.replace(', ', ' ', 1)
            elif kind == 'empty-member':
                vary = vary + ','
            elif kind == 'empty':
                vary = ''
            elif kind == 'int-value':
                stored[rng.choice(fields)] = 5
            elif kind == 'list-empty':
                presented[rng.choice(fields)] = []
            else:
                vary = 7
        verdict = reference(vary, stored, presented)
        cases.append(dict(id=f'r{i + 1}', vary=vary, stored=stored, presented=presented,
                          exit=1 if verdict == 'invalid' else 0,
                          verdict=None if verdict == 'invalid' else verdict))
    return cases


RANDOM_CASES = generate()
RANDOM_SHA = hashlib.sha256(json.dumps(RANDOM_CASES, sort_keys=True).encode()).hexdigest()


def git_bytes(root, rev, path):
    p = subprocess.run(['git', '-C', str(root), 'show', f'{rev}:{path}'], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def score(tool_bytes, work, cases):
    work.mkdir(parents=True, exist_ok=True)
    tool = work / 'vary_match.py'
    tool.write_bytes(tool_bytes)
    passed = 0
    details = []
    try:
        for case in cases:
            payload = json.dumps({k: case[k] for k in ('vary', 'stored', 'presented')})
            p = subprocess.run([sys.executable, '-B', str(tool)], input=payload,
                               capture_output=True, text=True, timeout=20)
            ok = p.returncode == case['exit']
            if ok and case['exit'] == 0:
                ok = p.stdout.strip() == case['verdict'] and p.stderr.strip() == ''
            elif ok:
                ok = p.stdout.strip() == '' and p.stderr.startswith('invalid_input:')
            passed += ok
            if not ok:
                details.append(dict(case=case['id'], ok=False, exit=p.returncode,
                                    out=p.stdout.strip()[:40], err=p.stderr.strip()[:60]))
    finally:
        tool.unlink(missing_ok=True)
    return passed, details


def selftest():
    checks = []

    def record(label, ok):
        checks.append((label, bool(ok)))

    ids = [c['id'] for c in CASES]
    record('frozen: unique sequential ids', len(ids) == len(set(ids)) and ids == list(range(1, len(CASES) + 1)))
    record('frozen: exits/verdicts well formed',
           all(c['exit'] in (0, 1) and ((c['exit'] == 0) == (c['verdict'] in ('match', 'mismatch')))
               for c in CASES))
    record('frozen: 20 cases', len(CASES) == 20)
    record('frozen: constant-match policy scores 7', sum(c['verdict'] == 'match' for c in CASES) == 7)
    record('frozen: constant-mismatch policy scores 9', sum(c['verdict'] == 'mismatch' for c in CASES) == 9)
    record('frozen: always-invalid policy scores 4', sum(c['exit'] == 1 for c in CASES) == 4)
    ref = [(reference(c['vary'], c['stored'], c['presented']),
            c['verdict'] if c['exit'] == 0 else 'invalid') for c in CASES]
    record('reference oracle reproduces all 20 frozen verdicts', all(a == b for a, b in ref))
    record('random: 200 seeded cases', len(RANDOM_CASES) == RANDOM_N)
    counts = {v: sum(c['verdict'] == v if c['exit'] == 0 else v == 'invalid' for c in RANDOM_CASES)
              for v in ('match', 'mismatch', 'invalid')}
    record(f'random: mixed population (match={counts["match"]} mismatch={counts["mismatch"]} '
           f'invalid={counts["invalid"]})',
           counts['match'] >= 20 and counts['mismatch'] >= 20 and counts['invalid'] >= 5)
    record('random: every case carries a reference verdict',
           all(c['exit'] == (1 if reference(c['vary'], c['stored'], c['presented']) == 'invalid' else 0)
               for c in RANDOM_CASES))
    with tempfile.TemporaryDirectory(prefix='kake-r88-selftest-') as d:
        d = Path(d)
        stubs = {'match': b'import sys\nprint("match")\n',
                 'mismatch': b'import sys\nprint("mismatch")\n',
                 'invalid': b'import sys\nsys.stderr.write("invalid_input: stub\\n")\nsys.exit(1)\n'}
        for name, body in stubs.items():
            got, _ = score(body, d / name, CASES)
            want = {'match': 7, 'mismatch': 9, 'invalid': 4}[name]
            record(f'stub {name} scores {want}/20 on the frozen set', got == want)
            got_r, _ = score(body, d / (name + 'r'), RANDOM_CASES)
            record(f'stub {name} scores {counts[name]}/200 on the random set', got_r == counts[name])
        got, _ = score(b'raise SystemExit(1)\n', d / 'empty', CASES)
        record('silent-failure stub scores 0/20', got == 0)
    passed = 0
    for label, ok in checks:
        print(('PASS ' if ok else 'FAIL ') + label)
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
        result = dict(claim='C2', revision=rev, frozen=0, frozen_total=len(CASES), random=0,
                      random_total=len(RANDOM_CASES), cases_sha256=CASES_SHA,
                      random_sha256=RANDOM_SHA, tool_sha256=None, met=False, details=[])
        print(json.dumps(result, sort_keys=True))
        return 1
    frozen_passed, frozen_details = score(tool_bytes, a.work / 'frozen', CASES)
    random_passed, random_details = score(tool_bytes, a.work / 'random', RANDOM_CASES)
    result = dict(claim='C2', revision=rev, frozen=frozen_passed, frozen_total=len(CASES),
                  random=random_passed, random_total=len(RANDOM_CASES), cases_sha256=CASES_SHA,
                  random_sha256=RANDOM_SHA, tool_sha256=hashlib.sha256(tool_bytes).hexdigest(),
                  met=frozen_passed == len(CASES) and random_passed == len(RANDOM_CASES),
                  details=(frozen_details + random_details)[:12])
    print(json.dumps(result, sort_keys=True))
    return 0 if result['met'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
