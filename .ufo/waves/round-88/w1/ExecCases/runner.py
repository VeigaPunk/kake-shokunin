#!/usr/bin/env python3
"""ExecCases runner: score a Vary-match CLI on the ExecCases adversarial batch.

Read-only against the candidate: the candidate file is copied into --work and run
there, exactly like c88_vary.py's score(). Nothing is written outside --work.

  python3 -B runner.py --tool <vary_match.py> [--cases<cases.json>] [--work DIR]
  python3 -B runner.py --ref  [--cases ...]     # score c88_vary.py's reference()
                                                # against the same expectations

Scoring rule (identical to the C2 counter):
  exit 0 + stdout 'match'|'mismatch' + empty stderr        -> that verdict
  exit 1 + empty stdout + stderr startswith 'invalid_input:' -> invalid_input
  anything else                                            -> nonconforming
"""
import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

WAVE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88')
DEFAULT_CASES = WAVE / 'w1/ExecCases/extra-cases.json'


def normalise(verdict):
    # counter-internal vocabulary -> CLI vocabulary
    return 'invalid_input' if verdict == 'invalid' else verdict


def verdict_of(returncode, out, err):
    out = out.strip()
    err = err.strip()
    if returncode == 0 and err == '' and out in ('match', 'mismatch'):
        return out
    if returncode == 1 and out == '' and err.startswith('invalid_input:'):
        return 'invalid_input'
    return f'nonconforming(exit={returncode},out={out[:24]!r},err={err[:40]!r})'


def load_cases(path):
    data = json.loads(path.read_text())
    cases = data['cases'] if isinstance(data, dict) else data
    for c in cases:
        if 'expected' not in c:
            c['expected'] = 'invalid_input' if c.get('exit') == 1 else c.get('verdict')
    return cases


def score_tool(tool, cases, work):
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    dest = work / 'vary_match.py'
    dest.write_bytes(Path(tool).read_bytes())
    tally, disagreements = {}, []
    try:
        for c in cases:
            payload = json.dumps({k: c[k] for k in ('vary', 'stored', 'presented')})
            p = subprocess.run([sys.executable, '-B', str(dest)], input=payload,
                               capture_output=True, text=True, timeout=20)
            got = verdict_of(p.returncode, p.stdout, p.stderr)
            tally[got] = tally.get(got, 0) + 1
            if got != c['expected']:
                disagreements.append(dict(id=c['id'], expected=c['expected'], got=got,
                                          spec_reading=c.get('spec_reading'),
                                          adapter_expected=c.get('adapter_expected')))
    finally:
        dest.unlink(missing_ok=True)
    return tally, disagreements


def score_reference(cases):
    spec = importlib.util.spec_from_file_location('c88_vary', WAVE / 'c88_vary.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tally, disagreements = {}, []
    for c in cases:
        got = normalise(mod.reference(c['vary'], c['stored'], c['presented']))
        tally[got] = tally.get(got, 0) + 1
        if got != c['expected']:
            disagreements.append(dict(id=c['id'], expected=c['expected'], got=got,
                                      spec_reading=c.get('spec_reading'),
                                      adapter_expected=c.get('adapter_expected')))
    return tally, disagreements


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tool')
    ap.add_argument('--ref', action='store_true')
    ap.add_argument('--cases', type=Path, default=DEFAULT_CASES)
    ap.add_argument('--work', type=Path)
    a = ap.parse_args()
    cases = load_cases(a.cases)
    if a.ref:
        tally, disagreements = score_reference(cases)
        source = 'c88_vary.reference'
    else:
        if not a.tool:
            ap.error('--tool or --ref required')
        work = a.work or Path(tempfile.mkdtemp(prefix='execcases-'))
        tally, disagreements = score_tool(a.tool, cases, work)
        source = str(a.tool)
    total = len(cases)
    passed = total - len(disagreements)
    print(json.dumps({'source': source, 'cases': total,
                      'passed': passed, 'total': total,
                      'tally': tally, 'disagreements': disagreements},
                     indent=1, sort_keys=True))
    return 0 if not disagreements else 1


if __name__ == '__main__':
    raise SystemExit(main())
