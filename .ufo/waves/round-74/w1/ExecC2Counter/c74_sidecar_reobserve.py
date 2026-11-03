#!/usr/bin/env python3
"""Round-74 C2: revision-bound sidecar versus live-host os.stat observations.

S441: https://docs.python.org/3/library/os.path.html#os.path.exists
S442: https://docs.python.org/3/library/os.html#os.stat
Retained sources: .ufo/waves/round-74/sources/python-os-{path,stat}.txt.
Only token is probed, never file. No token content is opened.

The C2v1 summary reports the specified host-observation predicate only.
JSON also reports note/history findings (the contract's separate conjuncts);
these do not change stat classification or the specified met/exit formula.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from unittest.mock import patch

BASE_REVISION = 'ced2878a1e77f57afb4ee3baebf1021e5130399b'
SIDECAR = 'corpus/knowledge/freshness-sidecar.json'
ABSENCE = re.compile(
    r'absent|gone|vanished|emptied|no longer|dangling|no such file|never published|missing',
    re.IGNORECASE,
)
FIELDS = (
    'entries', 'absent', 'restored', 'absent_present', 'absent_absent',
    'absent_unevaluable', 'restored_present', 'restored_absent',
    'restored_unevaluable', 'contradictions',
)


class Unevaluable(Exception):
    """Committed input or the requested observation is unavailable."""


def read_entries(root, revision):
    process = subprocess.run(
        ['git', '-C', root, 'show', '--end-of-options', revision + ':' + SIDECAR],
        capture_output=True,
    )
    if process.returncode:
        raise Unevaluable(process.stderr.decode('utf-8', 'replace').strip())
    document = json.loads(process.stdout)
    if (not isinstance(document, dict)
            or document.get('schema') != 'kake-paths-sidecar-v1'
            or not isinstance(document.get('entries'), list)):
        raise Unevaluable('invalid sidecar schema or entries')
    entries = document['entries']
    for index, entry in enumerate(entries):
        if (not isinstance(entry, dict)
                or entry.get('kind') not in ('absent', 'restored')
                or not isinstance(entry.get('token'), str)
                or not entry['token'] or '\x00' in entry['token']):
            raise Unevaluable('invalid entry at index %d' % index)
    return entries


def observe(token, root):
    """S442: distinguish genuine absence from other stat failures (S441)."""
    if token == '~' or token.startswith('~/'):
        home = os.environ.get('HOME')
        if not home:
            return 'unevaluable'
        token = os.path.join(home, token[2:]) if token != '~' else home
    if not os.path.isabs(token):
        token = os.path.join(root, token)
    try:
        os.stat(token)
    except (FileNotFoundError, NotADirectoryError):
        return 'absent'
    except OSError:
        return 'unevaluable'
    return 'present'


def measure_entries(entries, root, revision):
    result = dict.fromkeys(FIELDS, 0)
    result['revision'] = revision
    for entry in entries:
        kind = entry['kind']
        result['entries'] += 1
        result[kind] += 1
        result[kind + '_' + observe(entry['token'], root)] += 1
    result['contradictions'] = result['absent_present'] + result['restored_absent']
    unevaluable = result['absent_unevaluable'] + result['restored_unevaluable']
    result['met'] = result['contradictions'] == 0 and unevaluable == 0
    result['exit_code'] = 2 if unevaluable else (0 if result['met'] else 1)
    return result


def annotation_findings(entries, prior_entries):
    """Check g4/g5 independently; a valid stat result is never relabeled."""
    def identity(entry):
        return entry.get('file'), entry.get('line'), entry['token']

    prior = {identity(entry): entry for entry in prior_entries}
    findings = []
    for index, entry in enumerate(entries):
        if entry['kind'] != 'restored':
            continue
        note = entry.get('note')
        if not isinstance(note, str) or ABSENCE.search(note):
            findings.append({'index': index, 'issue': 'restored-note'})
        old = prior.get(identity(entry))
        if old is None or old['kind'] != 'absent':
            continue
        expected = {key: old.get(key) for key in ('date', 'kind', 'note')}
        history = entry.get('history')
        if not isinstance(history, list) or expected not in history:
            findings.append({'index': index, 'issue': 'prior-history'})
    return findings


def measure(root, revision):
    entries = read_entries(root, revision)
    result = measure_entries(entries, root, revision)
    result['annotation_findings'] = annotation_findings(
        entries, read_entries(root, BASE_REVISION),
    )
    return result


def summary(result):
    return ('C2v1 revision=' + result['revision'] + ' '
            + ' '.join('%s=%d' % (key, result[key]) for key in FIELDS)
            + ' met=' + str(result['met']).lower())


def run_selftest():
    """Six function-level fixtures; no disk fixture or temporary tree required."""
    root = os.path.abspath(os.curdir)
    absent = {'file': 'citation.md', 'line': 1, 'token': '~/fixture',
              'kind': 'absent', 'date': '2026-10-31', 'note': 'prior absent'}
    restored = dict(absent, kind='restored', date='2026-11-03',
                    note='2026-11-03: fixture present; stat ok; host linux',
                    history=[{key: absent[key] for key in ('date', 'kind', 'note')}])
    cases = []
    with patch.object(os, 'stat', return_value=object()):
        result = measure_entries([absent], root, 'fixture')
        cases.append(('g1', result['absent_present'] == 1 and result['exit_code'] == 1))
    with patch.object(os, 'stat', side_effect=FileNotFoundError()):
        result = measure_entries([restored], root, 'fixture')
        cases.append(('g2', result['restored_absent'] == 1 and result['exit_code'] == 1))
    with patch.object(os, 'stat', side_effect=PermissionError()):
        result = measure_entries([restored], root, 'fixture')
        cases.append(('g3', result['restored_unevaluable'] == 1
                      and result['exit_code'] == 2 and not result['met']))
    bad_note = dict(restored, note='2026-11-03: target missing')
    cases.append(('g4', annotation_findings([bad_note], [absent])
                  == [{'index': 0, 'issue': 'restored-note'}]
                  and not annotation_findings([restored], [absent])))
    no_history = dict(restored)
    del no_history['history']
    cases.append(('g5', annotation_findings([no_history], [absent])
                  == [{'index': 0, 'issue': 'prior-history'}]))
    with patch.dict(os.environ, {'HOME': os.path.join(root, 'fixture-home')}):
        with patch.object(os, 'stat', return_value=object()) as stat:
            result = measure_entries([restored], root, 'fixture')
            cases.append(('g6', stat.call_args.args
                          == (os.path.join(root, 'fixture-home', 'fixture'),)
                          and result['exit_code'] == 0))
    return {'cases': [{'name': name, 'passed': passed} for name, passed in cases],
            'passed': sum(passed for _, passed in cases), 'total': len(cases),
            'exit_code': 0 if all(passed for _, passed in cases) else 1}


class UsageParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(64, '%s: error: %s\n' % (self.prog, message))


def main(argv=None):
    parser = UsageParser(description=__doc__)
    parser.add_argument('--root', default='.', help='lane root (default: current directory)')
    parser.add_argument('--revision', help='committed sidecar revision')
    parser.add_argument('--json', action='store_true', help='emit machine-readable result')
    parser.add_argument('--selftest', action='store_true', help='run contract fixtures g1-g6')
    args = parser.parse_args(argv)
    if not args.selftest and not args.revision:
        parser.error('--revision is required unless --selftest is used')
    if args.selftest and args.revision:
        parser.error('--selftest cannot be combined with --revision')
    try:
        if args.selftest:
            result = run_selftest()
            if args.json:
                print(json.dumps(result, sort_keys=True))
            else:
                for case in result['cases']:
                    print('%s %s' % (case['name'], 'ok' if case['passed'] else 'FAIL'))
                print('selftest %d/%d' % (result['passed'], result['total']))
        else:
            result = measure(os.path.abspath(os.path.expanduser(args.root)), args.revision)
            print(json.dumps(result, sort_keys=True) if args.json else summary(result))
        return result['exit_code']
    except (Unevaluable, OSError, ValueError, UnicodeError) as exc:
        if args.json:
            print(json.dumps({'revision': args.revision, 'met': False,
                              'exit_code': 2, 'error': str(exc)}, sort_keys=True))
        else:
            print('C2v1 error: %s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
