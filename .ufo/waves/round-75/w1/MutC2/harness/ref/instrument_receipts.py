#!/usr/bin/env python3
"""instrument_receipts.py — C2 receipt binding, round 75 (kake).

Reference implementation of contract §C2, used as the mutation-test target
while the executor's landed tool is absent.  Semantics fixed here:

  population  the live gate-registry instrument files derived from the
              committed SKILL.md at --revision (Name cell when it is itself a
              .py/.mjs path, else the first .py/.mjs token of the Entry cell,
              else of the Self-test cell, else of any cell).
  receipt     corpus/knowledge/instrument-receipts.json, schema
              instrument-receipts/v1, read from committed bytes at --revision.
  check       re-derives, for every population file, the committed blob's
              sha256 and byte length at --revision plus the static --selftest
              registration and compares them with the receipt entry.  bound
              counts a file only when all three match; a missing entry, a
              duplicate entry, or a missing receipt is a mismatch.  Entries
              for paths outside the population are reported separately and
              never counted toward bound.  met = (bound == population) and
              (mismatches == 0).

Usage:
  python3 -B scripts/instrument_receipts.py --root . --revision <rev> --check
  python3 -B scripts/instrument_receipts.py --root . --revision <rev> --write --date 2026-11-03
  python3 -B scripts/instrument_receipts.py --selftest --work <dir>

Exit: 0=met, 1=not met, 2=unevaluable, 64=usage.
"""
import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys

SEC_RE = re.compile(r'^### Round (\d+) gate registry additions')
FILE_RE = re.compile(r'((?:scripts|\.ufo)/[\w./-]+\.(?:py|mjs))')
SELFTEST_ARG = re.compile(rb"add_argument\(\s*['\"]--selftest")
SELFTEST_ARGV = re.compile(rb"['\"]--selftest['\"]\s*(?:==|in)")

RECEIPT_PATH = 'corpus/knowledge/instrument-receipts.json'
SCHEMA = 'instrument-receipts/v1'


class Unevaluable(Exception):
    pass


def git(root, *args):
    return subprocess.run(['git', '-C', root, *args], capture_output=True)


def read_rev(root, rev, path):
    p = git(root, 'show', f'{rev}:{path}')
    if p.returncode != 0:
        return None
    return p.stdout


def parse_rows(text):
    rows, sec = [], None
    for i, line in enumerate(text.splitlines(), 1):
        m = SEC_RE.match(line)
        if m:
            sec = int(m.group(1))
            continue
        if line.startswith('### '):
            sec = None
            continue
        if sec and line.startswith('| ') and line.count('|') >= 6:
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if cells[0] == 'Name' or set(cells[0]) <= set('-: '):
                continue
            rows.append({'line': i, 'section': sec, 'cells': cells})
    return rows


def instrument(row):
    cells = row['cells']
    if FILE_RE.fullmatch(cells[0]):
        return cells[0]
    for idx in (2, 4):
        m = FILE_RE.search(cells[idx])
        if m:
            return m.group(1)
    m = FILE_RE.search(' '.join(cells))
    return m.group(1) if m else None


def population(root, rev):
    data = read_rev(root, rev, 'SKILL.md')
    if data is None:
        raise Unevaluable(f'cannot read SKILL.md at {rev}')
    text = data.decode('utf-8', 'replace')
    live = [r for r in parse_rows(text) if 'historical' not in r['cells'][1]]
    groups = {}
    for row in live:
        f = instrument(row)
        if f:
            groups.setdefault(f, []).append(row)
    return sorted(groups)


def selftest_mode(data):
    return bool(SELFTEST_ARG.search(data) or SELFTEST_ARGV.search(data))


def derive(root, rev, paths):
    out = {}
    for path in paths:
        data = read_rev(root, rev, path)
        if data is None:
            raise Unevaluable(f'cannot read {path} at {rev}')
        out[path] = {'sha256': hashlib.sha256(data).hexdigest(),
                     'bytes': len(data),
                     'selftest_mode': selftest_mode(data)}
    return out


def load_receipt(root, rev):
    data = read_rev(root, rev, RECEIPT_PATH)
    if data is None:
        return None
    try:
        return json.loads(data.decode('utf-8'))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Unevaluable(f'receipt is not valid JSON: {exc}')


def check(root, rev):
    paths = population(root, rev)
    findings = []
    bound = 0
    receipt = load_receipt(root, rev)
    if receipt is None:
        findings.append(f'receipt {RECEIPT_PATH} is absent at {rev}')
        for path in paths:
            findings.append(f'{path}: no receipt entry (missing receipt)')
        return paths, bound, findings, []
    if receipt.get('schema') != SCHEMA:
        raise Unevaluable(f'receipt schema is {receipt.get("schema")!r}, not {SCHEMA!r}')
    derived = derive(root, rev, paths)
    entries = receipt.get('files')
    if not isinstance(entries, list):
        raise Unevaluable('receipt has no files[] list')
    by_path = {}
    for entry in entries:
        if not isinstance(entry, dict) or 'path' not in entry:
            raise Unevaluable(f'receipt entry without a path: {entry!r}')
        by_path.setdefault(entry['path'], []).append(entry)
    for path in paths:
        seen = by_path.get(path)
        if not seen:
            findings.append(f'{path}: no receipt entry')
            continue
        if len(seen) > 1:
            findings.append(f'{path}: {len(seen)} receipt entries for one path')
            continue
        entry = seen[0]
        want = derived[path]
        bad = [k for k in ('sha256', 'bytes', 'selftest_mode')
               if entry.get(k) != want[k]]
        if bad:
            findings.append(f'{path}: receipt {"/".join(bad)} does not re-derive '
                            f'(receipt {[entry.get(k) for k in bad]}, '
                            f'committed {[want[k] for k in bad]})')
            continue
        bound += 1
    extra = sorted(set(by_path) - set(paths))
    return paths, bound, findings, extra


def write_receipt(root, rev, date):
    paths = population(root, rev)
    derived = derive(root, rev, paths)
    receipt = {'schema': SCHEMA,
               'revision': rev,
               'date': date,
               'host': platform.node() or 'unknown',
               'files': [{'path': p, 'sha256': derived[p]['sha256'],
                          'bytes': derived[p]['bytes'],
                          'selftest_mode': derived[p]['selftest_mode']}
                         for p in sorted(derived)]}
    text = json.dumps(receipt, indent=2) + '\n'
    target = os.path.join(root, RECEIPT_PATH)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, 'w', encoding='utf-8') as fh:
        fh.write(text)
    return paths, target


# --------------------------------------------------------------------------
# selftest: isolated fixture repositories under --work, never the lane.

FIXTURE_SKILL = """# fixture skill

### Round 99 gate registry additions

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| `alpha` | gate (live) | `python3 -B .ufo/waves/round-99/alpha.py` | `0=met` | `python3 -B .ufo/waves/round-99/alpha.py --selftest` → `selftest 2/2` | — | — | selftest |
| `beta` | instrument (live) | `python3 -B .ufo/waves/round-99/beta.py` | `0=met` | none | — | — | selftest |
| tool row | gate (live) | `python3 -B .ufo/waves/round-99/gamma.py` | `0=met` | `python3 -B .ufo/waves/round-99/gamma.py --selftest` → `selftest 1/1` | — | — | selftest |
"""

FIXTURE_ALPHA = """import argparse
ap = argparse.ArgumentParser()
ap.add_argument('--selftest', action='store_true')
print('selftest 2/2')
"""

FIXTURE_BETA = """print('beta')
"""

FIXTURE_GAMMA = """import sys
if '--selftest' in sys.argv:
    print('selftest 1/1')
"""

FIXTURE_EXTRA = """print('outside the population')
"""


def _commit(root, message):
    subprocess.run(['git', '-C', root, 'add', '-A'], check=True,
                   capture_output=True)
    subprocess.run(['git', '-C', root, '-c', 'user.name=selftest',
                    '-c', 'user.email=selftest@example.invalid',
                    'commit', '-q', '-m', message], check=True,
                   capture_output=True)


def _fixture(work, name, alpha=FIXTURE_ALPHA, gamma=FIXTURE_GAMMA):
    root = os.path.join(work, 'selftest', name)
    if os.path.isdir(root):
        shutil.rmtree(root)
    base = os.path.join(root, '.ufo', 'waves', 'round-99')
    os.makedirs(base)
    subprocess.run(['git', '-C', root, 'init', '-q'], check=True,
                   capture_output=True)
    files = {'SKILL.md': FIXTURE_SKILL,
             '.ufo/waves/round-99/alpha.py': alpha,
             '.ufo/waves/round-99/beta.py': FIXTURE_BETA,
             '.ufo/waves/round-99/gamma.py': gamma,
             '.ufo/waves/round-99/extra.py': FIXTURE_EXTRA}
    for rel, text in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(text)
    _commit(root, 'fixture')
    return root


def _head(root):
    return git(root, 'rev-parse', 'HEAD').stdout.decode().strip()


def _put(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(text)


def _receipt(root):
    with open(os.path.join(root, RECEIPT_PATH), encoding='utf-8') as fh:
        return json.loads(fh.read())


def _commit_receipt(root, receipt, message, only=None):
    _put(root, RECEIPT_PATH, json.dumps(receipt, indent=2) + '\n')
    if only:
        subprocess.run(['git', '-C', root, 'add', '--'] + only, check=True,
                       capture_output=True)
        subprocess.run(['git', '-C', root, '-c', 'user.name=selftest',
                        '-c', 'user.email=selftest@example.invalid',
                        'commit', '-q', '-m', message], check=True,
                       capture_output=True)
    else:
        _commit(root, message)
    return _head(root)


def _case_green(work):
    root = _fixture(work, 'green')
    write_receipt(root, _head(root), '2026-11-03')
    _commit(root, 'receipt')
    rev = _head(root)
    paths, bound, findings, extra = check(root, rev)
    return (len(paths) == 3 and bound == 3 and not findings and not extra)


def _case_fabricated(work):
    root = _fixture(work, 'fabricated')
    write_receipt(root, _head(root), '2026-11-03')
    rec = _receipt(root)
    for entry in rec['files']:
        entry['sha256'] = '0' * 64
    rev = _commit_receipt(root, rec, 'fabricated')
    paths, bound, findings, extra = check(root, rev)
    return bound == 0 and len(findings) == len(paths)


def _case_missing_entry(work):
    root = _fixture(work, 'missing')
    write_receipt(root, _head(root), '2026-11-03')
    rec = _receipt(root)
    rec['files'] = [e for e in rec['files'] if not e['path'].endswith('beta.py')]
    rev = _commit_receipt(root, rec, 'missing entry')
    paths, bound, findings, extra = check(root, rev)
    return bound == len(paths) - 1 and len(findings) == 1


def _case_extra_entry(work):
    root = _fixture(work, 'extra')
    write_receipt(root, _head(root), '2026-11-03')
    rec = _receipt(root)
    rec['files'].append({'path': '.ufo/waves/round-99/extra.py',
                         'sha256': 'f' * 64, 'bytes': 1,
                         'selftest_mode': False})
    rev = _commit_receipt(root, rec, 'extra entry')
    paths, bound, findings, extra = check(root, rev)
    return bound == len(paths) and len(extra) == 1


def _case_mode_flip(work):
    root = _fixture(work, 'mode')
    write_receipt(root, _head(root), '2026-11-03')
    rec = _receipt(root)
    for entry in rec['files']:
        if entry['path'].endswith('beta.py'):
            entry['selftest_mode'] = True
    rev = _commit_receipt(root, rec, 'mode flip')
    paths, bound, findings, extra = check(root, rev)
    return bound == len(paths) - 1 and len(findings) == 1


def _case_dirty_tree(work):
    root = _fixture(work, 'dirty')
    rev = _head(root)
    paths = population(root, rev)
    derived = derive(root, rev, paths)
    dirty = FIXTURE_ALPHA + '\n# dirty working tree\n'
    raw = dirty.encode()
    derived['.ufo/waves/round-99/alpha.py'] = {
        'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
        'selftest_mode': selftest_mode(raw)}
    rec = {'schema': SCHEMA, 'revision': rev, 'date': '2026-11-03',
           'host': 'selftest',
           'files': [{'path': p, **derived[p]} for p in sorted(derived)]}
    with open(os.path.join(root, '.ufo/waves/round-99/alpha.py'), 'a') as fh:
        fh.write('\n# dirty working tree\n')
    rev = _commit_receipt(root, rec, 'receipt for the working tree',
                          only=[RECEIPT_PATH])
    paths, bound, findings, extra = check(root, rev)
    return bound == len(paths) - 1 and len(findings) == 1


def _case_stale_revision(work):
    root = _fixture(work, 'stale')
    write_receipt(root, _head(root), '2026-11-03')
    rev = _commit_receipt(root, _receipt(root), 'receipt at old bytes')
    with open(os.path.join(root, '.ufo/waves/round-99/alpha.py'), 'a') as fh:
        fh.write('\n# changed after the receipt\n')
    _commit(root, 'blob moved on')
    new = _head(root)
    paths, bound, findings, extra = check(root, new)
    return bound < len(paths)


def _case_sorted_newline(work):
    root = _fixture(work, 'sorted')
    write_receipt(root, _head(root), '2026-11-03')
    raw = read_rev(root, _head(root), RECEIPT_PATH)
    # receipt is uncommitted when just written; read the working tree copy
    with open(os.path.join(root, RECEIPT_PATH), 'rb') as fh:
        raw = fh.read()
    rec = json.loads(raw.decode())
    paths = [e['path'] for e in rec['files']]
    ok_sorted = paths == sorted(paths)
    ok_newline = raw.endswith(b'\n')
    before = raw
    write_receipt(root, _head(root), '2026-11-03')
    with open(os.path.join(root, RECEIPT_PATH), 'rb') as fh:
        again = fh.read()
    return ok_sorted and ok_newline and again == before


def _case_duplicate(work):
    root = _fixture(work, 'dup')
    write_receipt(root, _head(root), '2026-11-03')
    rec = _receipt(root)
    alpha = [e for e in rec['files'] if e['path'].endswith('alpha.py')][0]
    bad = dict(alpha)
    bad['sha256'] = '0' * 64
    idx = rec['files'].index(alpha)
    rec['files'].insert(idx, bad)
    rev = _commit_receipt(root, rec, 'duplicate path')
    paths, bound, findings, extra = check(root, rev)
    return bound < len(paths) and any('entries for one path' in f for f in findings)


def _case_combined_path(work):
    root = _fixture(work, 'combined')
    write_receipt(root, _head(root), '2026-11-03')
    rec = _receipt(root)
    alpha = [e for e in rec['files'] if e['path'].endswith('alpha.py')][0]
    rec['files'] = [e for e in rec['files']
                    if not e['path'].endswith('beta.py')]
    combined = dict(alpha)
    combined['path'] = '.ufo/waves/round-99/alpha.py, .ufo/waves/round-99/beta.py'
    rec['files'].append(combined)
    rev = _commit_receipt(root, rec, 'combined path')
    paths, bound, findings, extra = check(root, rev)
    return bound < len(paths)


def _case_git_fault(work):
    root = _fixture(work, 'fault')
    try:
        check(root, 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeef')
    except Unevaluable:
        return True
    return False


CASES = [('green', _case_green), ('fabricated', _case_fabricated),
         ('missing_entry', _case_missing_entry), ('extra_entry', _case_extra_entry),
         ('mode_flip', _case_mode_flip), ('dirty_tree', _case_dirty_tree),
         ('stale_revision', _case_stale_revision), ('sorted_newline', _case_sorted_newline),
         ('duplicate', _case_duplicate), ('combined_path', _case_combined_path),
         ('git_fault', _case_git_fault)]


def selftest(work):
    if not work:
        print('64 usage: --selftest needs --work <dir>', file=sys.stderr)
        return 64
    work = os.path.abspath(work)
    os.makedirs(work, exist_ok=True)
    passed = 0
    for name, fn in CASES:
        try:
            ok = fn(work)
        except Exception as exc:  # a crashing fixture is a failed case
            print(f'  fixture {name}: {type(exc).__name__}: {exc}')
            ok = False
        print(f'  fixture {name}: {"ok" if ok else "FAIL"}')
        passed += 1 if ok else 0
    print(f'C2v1 selftest {passed}/{len(CASES)}')
    return 0 if passed == len(CASES) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description='C2 instrument receipt binding')
    ap.add_argument('--root', default='.')
    ap.add_argument('--revision', default=None)
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--date', default=None)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--work', default=None)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest(args.work)
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f'64 usage: --root {root} is not a directory', file=sys.stderr)
        return 64
    rev = args.revision or git(root, 'rev-parse', 'HEAD').stdout.decode().strip()
    if not rev:
        print('2 unevaluable: no revision to measure', file=sys.stderr)
        return 2
    try:
        if args.write:
            paths, target = write_receipt(root, rev, args.date or 'unspecified')
            print(f'C2v1 revision={rev} population={len(paths)} '
                  f'written={len(paths)} receipt={target}')
            return 0
        paths, bound, findings, extra = check(root, rev)
    except Unevaluable as exc:
        print(f'2 unevaluable: {exc}', file=sys.stderr)
        return 2
    met = bound == len(paths) and not findings
    print(f'C2v1 revision={rev} population={len(paths)} bound={bound} '
          f'mismatches={len(findings)} met={str(met).lower()}')
    for finding in findings:
        print(f'  finding: {finding}')
    for path in extra:
        print(f'  extra: {path} (outside the population; not counted)')
    if args.json:
        print(json.dumps({'revision': rev, 'population': paths, 'bound': bound,
                          'findings': findings, 'extra': extra, 'met': met},
                         indent=2))
    return 0 if met else 1


if __name__ == '__main__':
    sys.exit(main())
