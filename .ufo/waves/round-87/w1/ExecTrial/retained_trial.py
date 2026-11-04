#!/usr/bin/env python3
"""Round-87 ExecTrial runner: offline trial of a C2 cache_current_age candidate
against the retained single-GET record (trial-record.json), with independent
plain-arithmetic expected values.

Trial clock is FIXED: now = record['trial_now'] (captured at GET time as
max(response_time, int(time.time()))). The runner never reads the wall clock
into the comparison; runner_invoked_at is recorded for provenance only.

Usage:
  python3 -B retained_trial.py --tool /abs/path/cache_current_age.py \
      [--record /abs/path/trial-record.json]

Verdicts (JSON on stdout):
  match                tool exit0, stdout exactly one JSON object equal to all
                       six independent expected values
  could_not_evaluate   record honestly lacks an evaluable Date/Age; no tool run,
                       nothing fabricated (exit 0)
  tool_absent          --tool path does not exist (exit 1); expected values shown
  fail                 nonzero tool exit, non-JSON stdout, or value mismatch (exit 1)
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

KEYS = (
    'apparent_age',
    'response_delay',
    'corrected_age_value',
    'corrected_initial_age',
    'resident_time',
    'current_age',
)


def expected_values(inp: dict) -> dict:
    """Independent plain arithmetic per frozen contract C2; no tool involved."""
    date_value = inp['date_value']
    request_time = inp['request_time']
    response_time = inp['response_time']
    now = inp['now']
    age_value = inp.get('age_value', 0)
    apparent_age = max(0, response_time - date_value)
    response_delay = response_time - request_time
    corrected_age_value = age_value + response_delay
    corrected_initial_age = max(apparent_age, corrected_age_value)
    resident_time = now - response_time
    current_age = corrected_initial_age + resident_time
    return dict(zip(KEYS, (apparent_age, response_delay, corrected_age_value,
                           corrected_initial_age, resident_time, current_age)))


def main() -> int:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument('--tool', required=True,
                    help='ABS path to candidate/new cache_current_age.py')
    ap.add_argument('--record', default=str(here / 'trial-record.json'))
    a = ap.parse_args()
    tool = Path(a.tool)
    out = {'runner': 'retained_trial.py', 'record': a.record, 'tool': str(tool),
           'runner_invoked_at': int(time.time())}
    if not tool.is_absolute():
        out['verdict'] = 'error'
        out['reason'] = '--tool must be an absolute path'
        print(json.dumps(out, sort_keys=True))
        return 1
    rec = json.loads(Path(a.record).read_text())
    out['trial_status'] = rec.get('trial_status')
    if rec.get('trial_status') != 'evaluable':
        out['verdict'] = 'could_not_evaluate'
        out['reason'] = rec.get('trial_reason')
        print(json.dumps(out, sort_keys=True))
        return 0
    inp = rec['tool_input']
    if inp['now'] != rec['trial_now']:
        out['verdict'] = 'error'
        out['reason'] = 'record tool_input.now != recorded trial_now'
        print(json.dumps(out, sort_keys=True))
        return 1
    exp = expected_values(inp)
    out['tool_input'] = inp
    out['expected'] = exp
    if not tool.is_file():
        out['verdict'] = 'tool_absent'
        print(json.dumps(out, sort_keys=True))
        return 1
    p = subprocess.run([sys.executable, '-B', str(tool)],
                       input=json.dumps(inp), capture_output=True, text=True,
                       timeout=30)
    out['tool_returncode'] = p.returncode
    out['tool_stderr'] = p.stderr[:2000]
    try:
        obj = json.loads(p.stdout)
    except ValueError:
        obj = None
    out['tool_stdout_json'] = obj
    if p.returncode != 0:
        out['verdict'] = 'fail'
        out['reason'] = 'tool exited nonzero on evaluable observed trial input'
    elif not isinstance(obj, dict) or set(obj) != set(KEYS) or any(
            type(value) is not int for value in obj.values()):
        out['verdict'] = 'fail'
        out['reason'] = 'stdout must contain exactly six integer fields (not bool)'
    elif p.stderr:
        out['verdict'] = 'fail'
        out['reason'] = 'valid-input tool emitted stderr'
    elif obj != exp:
        out['verdict'] = 'fail'
        if isinstance(obj, dict):
            out['mismatches'] = {k: {'expected': exp[k], 'actual': obj.get(k)}
                                 for k in KEYS if obj.get(k) != exp[k]}
        else:
            out['reason'] = 'stdout is not exactly one JSON object'
    else:
        out['verdict'] = 'match'
    print(json.dumps(out, sort_keys=True))
    return 0 if out['verdict'] in ('match', 'could_not_evaluate') else 1


if __name__ == '__main__':
    raise SystemExit(main())
