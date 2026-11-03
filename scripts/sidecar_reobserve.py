#!/usr/bin/env python3
"""Re-observe path tokens without altering their historical citations.

Default mode is read-only. Exit 0: observation completed; exit 2: refused/error.
--work supplies the parent directory for selftest fixtures; otherwise TMPDIR is used.
"""

import argparse
import copy
import datetime
import io
import json
import os
from pathlib import Path
import platform
import re
import tempfile
import unittest
from unittest import mock


SIDECAR = Path('corpus/knowledge/freshness-sidecar.json')
SCHEMA = 'kake-paths-sidecar-v1'
ABSENCE = re.compile(
    r'absent|gone|vanished|emptied|no longer|dangling|no such file|never published|missing'
    r'|removed|deleted|purged|returned|reappeared|came back|recreated',
    re.IGNORECASE,
)


def calendar_date(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError('date must be YYYY-MM-DD')
    datetime.date.fromisoformat(value)
    return value


def validate(data):
    if not isinstance(data, dict) or data.get('schema') != SCHEMA:
        raise ValueError('expected kake-paths-sidecar-v1 schema')
    if not isinstance(data.get('entries'), list):
        raise ValueError('entries must be an array')
    for entry in data['entries']:
        if not isinstance(entry, dict):
            raise ValueError('entry must be an object')
        if any(not isinstance(entry.get(key), str) for key in
               ('file', 'token', 'kind', 'date', 'note', 'lineSha256')):
            raise ValueError('entry string fields invalid')
        if entry['kind'] not in ('absent', 'restored'):
            raise ValueError('entry kind invalid')
        if type(entry.get('line')) is not int or entry['line'] < 1:
            raise ValueError('entry line invalid')
        if not entry['token'] or not re.fullmatch(r'[0-9a-f]{64}', entry['lineSha256']):
            raise ValueError('entry token or lineSha256 invalid')
        # Mirror the sweep reader's binding rules so --write cannot emit bytes it rejects.
        parts = entry['file'].split('/')
        if not (entry['file'] == 'SKILL.md'
                or re.fullmatch(r'corpus/.+\.md', entry['file'])) \
                or any(part in ('', '.', '..') for part in parts):
            raise ValueError('entry file must be SKILL.md or corpus/**.md')
        home = os.path.expanduser('~')
        if home != '~' and entry['token'].startswith(home + '/'):
            raise ValueError('entry token must use the canonical home spelling')
        calendar_date(entry['date'])
        if 'history' in entry:
            if not isinstance(entry['history'], list):
                raise ValueError('history must be an array')
            for observation in entry['history']:
                if not isinstance(observation, dict) or any(
                    not isinstance(observation.get(key), str)
                    for key in ('date', 'kind', 'note')
                ):
                    raise ValueError('history observation invalid')


def token_state(token, root):
    if token.startswith('~/'):
        home = os.environ.get('HOME')
        if not home:
            return 'unevaluable'
        target = os.path.join(home, token[2:])
    else:
        target = token if os.path.isabs(token) else os.path.join(root, token)
    try:
        os.stat(target)
    except (FileNotFoundError, NotADirectoryError):
        return 'absent'
    except OSError:
        return 'unevaluable'
    return 'present'


def new_note(entry, date, host):
    note = (
        f'{date}: re-observed on {host}; token resolves (stat ok). '
        f'Prior {entry["date"]} observation retained under history. '
        f'Citation {entry["file"]}:{entry["line"]} is a historical record.'
    )
    if ABSENCE.search(note):
        raise ValueError('new note would match sweep absence vocabulary')
    return note


def reobserve(root, write=False, date=None, host=None):
    root = Path(root).resolve()
    sidecar = root / SIDECAR
    # Reject links that would redirect the only permitted write outside root.
    if not sidecar.resolve().is_relative_to(root) or sidecar.is_symlink():
        raise ValueError('sidecar must be a regular path under root')
    with sidecar.open(encoding='utf-8') as source:
        data = json.load(source)
    validate(data)
    counts = dict(entries=len(data['entries']), absent=0, restored=0, present=0,
                  absent_present=0, absent_absent=0, restored_absent=0,
                  unevaluable=0, flipped=0)
    candidates = []
    for entry in data['entries']:
        counts[entry['kind']] += 1
        state = token_state(entry['token'], root)
        if state in ('present', 'unevaluable'):
            counts[state] += 1
        if state != 'unevaluable':
            key = entry['kind'] + '_' + state
            if key in counts:
                counts[key] += 1
        if entry['kind'] == 'absent' and state == 'present':
            candidates.append(entry)
    result = dict(mode='write' if write else 'check', **counts, wrote=False)
    if counts['unevaluable']:
        result['error'] = 'one or more tokens could not be evaluated; no write'
        return result, 2
    if write:
        calendar_date(date)
        # Prepare all notes before changing any entry or opening the output.
        notes = [new_note(entry, date, host) for entry in candidates]
        for entry, note in zip(candidates, notes):
            prior = {key: entry[key] for key in ('date', 'kind', 'note')}
            entry.setdefault('history', []).append(prior)
            entry.update(kind='restored', date=date, note=note)
        if candidates:
            # Atomic replacement: the last good bytes survive a failed write. The sidecar
            # symlink check above rejects a redirected target; os.replace keeps the name.
            fd, temporary = tempfile.mkstemp(prefix='.sidecar-', dir=str(sidecar.parent))
            try:
                with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as target:
                    json.dump(data, target, indent=2, ensure_ascii=False)
                    target.write('\n')
                    target.flush()
                    os.fsync(target.fileno())
                os.replace(temporary, sidecar)
            except BaseException:
                try:
                    os.unlink(temporary)
                except OSError:
                    pass
                raise
            result.update(flipped=len(candidates), wrote=True)
    return result, 0


def selftest(work=None):
    class Fixtures(unittest.TestCase):
        def setUp(self):
            self.temp = tempfile.TemporaryDirectory(dir=work)
            self.addCleanup(self.temp.cleanup)
            self.root = Path(self.temp.name)
            self.sidecar = self.root / SIDECAR
            self.sidecar.parent.mkdir(parents=True)
            self.present = self.root / 'present'
            self.present.touch()
            self.entry = dict(file='SKILL.md', line=1, token=str(self.present),
                              lineSha256='a' * 64, kind='absent', date='2026-10-21',
                              note='2026-10-21: absent; historical record')
            self.save([self.entry])

        def save(self, entries):
            self.sidecar.write_text(json.dumps(dict(schema=SCHEMA, entries=entries)),
                                    encoding='utf-8')

        def run_write(self):
            return reobserve(self.root, True, '2026-11-03', 'linux-x86_64')

        def test_flip(self):
            result, code = self.run_write()
            entry = json.loads(self.sidecar.read_text())['entries'][0]
            self.assertEqual((code, result['flipped'], entry['kind']), (0, 1, 'restored'))
            self.assertEqual(entry['date'], '2026-11-03')
            self.assertIn('linux-x86_64; token resolves (stat ok)', entry['note'])
            self.assertEqual(entry['history'], [{k: self.entry[k] for k in ('date', 'kind', 'note')}])

        def test_restored_present_noop(self):
            self.entry['kind'] = 'restored'
            self.save([self.entry])
            before = self.sidecar.read_bytes()
            result, code = self.run_write()
            self.assertEqual((code, result['flipped']), (0, 0))
            self.assertEqual(before, self.sidecar.read_bytes())

        def test_unevaluable_refuses_entire_write(self):
            other = dict(self.entry, token=str(self.root / 'blocked'))
            self.save([self.entry, other])
            before = self.sidecar.read_bytes()
            real_stat = os.stat
            def stat(path, *args, **kwargs):
                if str(path) == other['token']:
                    raise PermissionError('fixture')
                return real_stat(path, *args, **kwargs)
            with mock.patch.object(os, 'stat', side_effect=stat):
                result, code = self.run_write()
            self.assertEqual((code, result['unevaluable']), (2, 1))
            self.assertEqual(before, self.sidecar.read_bytes())

        def test_history_preservation(self):
            history = [dict(date='2026-10-01', kind='restored', note='unchanged\nUnicode: é')]
            self.entry['history'] = copy.deepcopy(history)
            self.save([self.entry])
            self.run_write()
            after = json.loads(self.sidecar.read_text())['entries'][0]['history']
            self.assertEqual(after[:-1], history)
            self.assertEqual(after[-1]['note'], self.entry['note'])

        def test_note_vocabulary(self):
            self.assertIsNone(ABSENCE.search(new_note(self.entry, '2026-11-03', 'linux-x86_64')))
            with self.assertRaises(ValueError):
                new_note(self.entry, '2026-11-03', 'missing-host')

        def test_home_expansion(self):
            self.entry['token'] = '~/present'
            self.save([self.entry])
            with mock.patch.dict(os.environ, {'HOME': str(self.root)}):
                result, code = self.run_write()
            self.assertEqual((code, result['flipped']), (0, 1))

        def test_check_does_not_write(self):
            before = self.sidecar.read_bytes()
            result, code = reobserve(self.root)
            self.assertEqual((code, result['absent_present'], result['wrote']), (0, 1, False))
            self.assertEqual(before, self.sidecar.read_bytes())

        def test_wrong_schema_refused(self):
            self.sidecar.write_text('{"schema":"other","entries":[]}', encoding='utf-8')
            before = self.sidecar.read_bytes()
            with self.assertRaises(ValueError):
                self.run_write()
            self.assertEqual(before, self.sidecar.read_bytes())

        def test_traversal_file_refused(self):
            data = {'schema': SCHEMA, 'entries': [dict(
                file='../../../../etc/hostname', line=1, token='~/' + 'x',
                lineSha256='0' * 64, kind='absent', date='2026-10-31',
                note='2026-10-31: absent (test -e exit 1); historical record, not an executable instruction')]}
            with self.assertRaises(ValueError):
                validate(data)

        def test_absolute_home_token_refused(self):
            home = os.path.expanduser('~')
            data = {'schema': SCHEMA, 'entries': [dict(
                file='SKILL.md', line=1, token=home + '/x',
                lineSha256='0' * 64, kind='absent', date='2026-10-31',
                note='2026-10-31: absent (test -e exit 1); historical record, not an executable instruction')]}
            with self.assertRaises(ValueError):
                validate(data)

    stream = io.StringIO()
    outcome = unittest.TextTestRunner(stream=stream).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(Fixtures))
    return dict(tests=outcome.testsRun, failures=len(outcome.failures),
                errors=len(outcome.errors), passed=outcome.wasSuccessful(),
                details=stream.getvalue()), 0 if outcome.wasSuccessful() else 2


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=None,
                        help='lane root (required with --write; default . for --check)')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--check', action='store_true', help='report only (default)')
    modes.add_argument('--write', action='store_true')
    parser.add_argument('--date', type=calendar_date)
    parser.add_argument('--host', default=platform.system().lower() + '-' + platform.machine())
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('--work', help='selftest scratch parent; defaults to TMPDIR')
    args = parser.parse_args(argv)
    if args.write and not args.date:
        parser.error('--date YYYY-MM-DD is required with --write')
    if args.write and args.root is None:
        parser.error('--root is required with --write (no default write target)')
    try:
        if args.selftest:
            result, code = selftest(args.work)
        else:
            result, code = reobserve(args.root or '.', args.write, args.date, args.host)
    except (OSError, ValueError) as error:
        result, code = dict(error=str(error), wrote=False), 2
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print('sidecar_reobserve ' + ' '.join(
            f'{key}={str(value).lower() if isinstance(value, bool) else value}'
            for key, value in result.items() if key != 'details'))
        if result.get('details') and code:
            print(result['details'], end='')
    return code


if __name__ == '__main__':
    raise SystemExit(main())
