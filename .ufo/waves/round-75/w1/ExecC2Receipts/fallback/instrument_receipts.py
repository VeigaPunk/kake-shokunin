#!/usr/bin/env python3
"""instrument_receipts.py - C2 instrument-receipt writer/checker, round 75 (kake).

Predicate (frozen in .ufo/waves/round-75/contract.md section C2, as amended by
amendment-1.md A2):

  Population: every live gate-registry instrument of SKILL.md - a table row
  inside a section titled ``### Round <N> gate registry additions`` whose Kind
  cell does not carry ``historical``; the row's instrument file is the Name cell
  when it is a .py/.mjs path, else the first such token of the Entry-command
  cell, else of the Self-test cell, else of any cell; the last row naming a file
  is the effective row.  The frozen 16 paths of contract §C1 are a floor: the
  derivation must still produce every one of them (``missing_frozen`` is the
  count of frozen paths the derivation lost); files derived beyond the floor are
  in-population like the rest.

  Receipt: corpus/knowledge/instrument-receipts.json, schema instrument-receipts/v1,
  {schema, revision, date, host, files[]} with one entry per population file -
  {path, sha256, bytes, selftest_mode} where sha256/bytes are of the committed
  blob at the receipt's revision and selftest_mode is true when the file
  statically registers a --selftest argument.

  Check: the receipt is read from committed bytes at --revision (amendment 3
  A6) - a receipt that exists only in the working tree is ``receipt=uncommitted``
  and a mismatch; --worktree-receipt is a local-debugging opt-in, never
  evidence.  For every population file, re-derive the committed blob's sha256
  and byte length at --revision and the static --selftest registration, and
  compare them with the receipt entry; a file counts ``bound`` only when all
  three match.  The receipt's ``revision`` must be a 40-hex token that resolves
  to a commit and is an ancestor of (or equal to) the measured revision
  (amendment 3 A7), else every file is ``receipt_revision_invalid``.  A missing
  entry is a mismatch; an entry outside the population is not counted toward
  bound and is reported separately.

  met = (bound == population) and (mismatches == 0) and (missing_frozen == 0).

CLI:
  python3 -B scripts/instrument_receipts.py --root . --revision <rev> --check
  python3 -B scripts/instrument_receipts.py --root . --revision <rev> --write --date YYYY-MM-DD
  python3 -B scripts/instrument_receipts.py --selftest [--work DIR]

Output line:
  C2v1 revision=<rev> population=<n> bound=<b> mismatches=<m> met=<bool> missing_frozen=<n>

Exit: 0 met, 1 not met, 2 unevaluable, 64 usage.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile

RECEIPT_PATH = 'corpus/knowledge/instrument-receipts.json'
SCHEMA = 'instrument-receipts/v1'
C1_PATH = '.ufo/waves/round-75/c75_row_truth.py'

# Contract §C1 frozen population - the floor the derivation may grow from but
# must never shrink below.
FROZEN = (
    '.ufo/waves/round-52/c52_wave_ledger.py',
    '.ufo/waves/round-57/c57_idresolver_gate.py',
    '.ufo/waves/round-58/c58_receipt_rewrites.py',
    '.ufo/waves/round-58/c58_resolver_cases.py',
    '.ufo/waves/round-59/c59_axis_evidence.py',
    '.ufo/waves/round-59/c59_resolver_cases.py',
    '.ufo/waves/round-66/c66_gate_status_hostportable.py',
    '.ufo/waves/round-69/c69_recorded_counts.py',
    '.ufo/waves/round-69/c69_tmp_honour.py',
    '.ufo/waves/round-72/c72_tmp_v2.py',
    '.ufo/waves/round-73/c73_tmp_v3.py',
    '.ufo/waves/round-73/c73_wave_pointers.py',
    '.ufo/waves/round-74/c74_registry_gap.py',
    'scripts/citation_lint.py',
    'scripts/id_resolver.py',
    'scripts/redirect_audit.py',
)

SEC_RE = re.compile(r'^### Round (\d+) gate registry additions')
FILE_RE = re.compile(r'((?:scripts|\.ufo)/[\w./-]+\.(?:py|mjs))')
REV_HEX = re.compile(r'^[0-9a-fA-F]{40}$')

# Static --selftest registration: an argparse registration, an argv membership
# test, an equality/inequality test or a startswith test on the literal flag.
# A bare mention in prose, a docstring or a longer string does not count.
SELFTEST_PATTERNS = (
    re.compile(r'add_argument\s*\((?:[^()]|\n){0,400}?[\'"]--selftest[\'"]'),
    re.compile(r'[\'"]--selftest[\'"]\s+(?:not\s+)?in\s+[A-Za-z_]'),
    re.compile(r'(?:==|!=)\s*[\'"]--selftest[\'"]'),
    re.compile(r'[\'"]--selftest[\'"]\s*(?:==|!=)'),
    re.compile(r'\.startswith\s*\(\s*[\'"]--selftest[\'"]'),
)


class Unevaluable(Exception):
    pass


def _env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['GIT_TERMINAL_PROMPT'] = '0'
    return env


def git(root, *args, text=True):
    return subprocess.run(['git', '-C', root, *args], capture_output=True,
                          text=text, env=_env())


def resolve(root, rev):
    if not rev:
        return None
    p = git(root, 'rev-parse', '--verify', '--quiet', '%s^{commit}' % rev)
    return p.stdout.strip() if p.returncode == 0 and p.stdout.strip() else None


def toplevel(root):
    p = git(root, 'rev-parse', '--show-toplevel')
    out = p.stdout.strip() if p.returncode == 0 else ''
    return os.path.realpath(out) if out else None


def blob(root, rev, path):
    p = git(root, 'cat-file', 'blob', '%s:%s' % (rev, path), text=False)
    return p.stdout if p.returncode == 0 else None


def is_ancestor(root, older, newer):
    return git(root, 'merge-base', '--is-ancestor', older, newer).returncode == 0


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def host():
    return '%s-%s' % (sys.platform, platform.machine())


# ---------------------------------------------------------------- population

def parse_registry(text):
    """Rows of every ``### Round <N> gate registry additions`` section."""
    rows, section = [], None
    for lineno, line in enumerate(text.splitlines(), 1):
        m = SEC_RE.match(line)
        if m:
            section = int(m.group(1))
            continue
        if line.startswith('### '):
            section = None
            continue
        if section is None or not line.startswith('| ') or line.count('|') < 6:
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if cells[0] == 'Name' or set(cells[0]) <= set('-: '):
            continue
        rows.append({'line': lineno, 'section': section, 'cells': cells})
    return rows


def row_instrument(cells):
    if FILE_RE.fullmatch(cells[0]):
        return cells[0]
    for idx in (2, 4):
        if idx < len(cells):
            m = FILE_RE.search(cells[idx])
            if m:
                return m.group(1)
    m = FILE_RE.search(' '.join(cells))
    return m.group(1) if m else None


def population_from(text):
    """Live rows only; the last row naming a file is its effective row."""
    effective = {}
    for row in parse_registry(text):
        if 'historical' in row['cells'][1]:
            continue
        path = row_instrument(row['cells'])
        if path:
            effective[path] = row
    return sorted(effective), effective


def population(root, rev):
    text = blob(root, rev, 'SKILL.md')
    if text is None:
        raise Unevaluable('SKILL.md does not resolve at %s' % rev)
    pop, effective = population_from(text.decode('utf-8', 'replace'))
    if not pop:
        raise Unevaluable('no live registry row derives an instrument file')
    return pop, effective


def selftest_registered(text):
    return any(p.search(text) for p in SELFTEST_PATTERNS)


def entry_for(root, rev, path):
    raw = blob(root, rev, path)
    if raw is None:
        raise Unevaluable('%s does not resolve at %s' % (path, rev))
    return {'path': path,
            'sha256': sha256(raw),
            'bytes': len(raw),
            'selftest_mode': selftest_registered(raw.decode('utf-8', 'replace'))}


# -------------------------------------------------------------------- receipt

def receipt_source(root, rev, allow_worktree=False):
    """Committed bytes only (amendment 3 A6): a receipt that exists only in the
    working tree is reported as ``uncommitted`` and is a mismatch.  The
    --worktree-receipt opt-in reads it for local debugging only, never for
    evidence."""
    raw = blob(root, rev, RECEIPT_PATH)
    if raw is not None:
        return raw, 'committed'
    path = os.path.join(root, RECEIPT_PATH)
    if allow_worktree and os.path.isfile(path):
        with open(path, 'rb') as fh:
            return fh.read(), 'worktree'
    return None, 'uncommitted' if os.path.isfile(path) else 'absent'


def parse_receipt(raw):
    try:
        doc = json.loads(raw.decode('utf-8'))
    except Exception as exc:
        raise Unevaluable('%s is not JSON: %s' % (RECEIPT_PATH, exc))
    if not isinstance(doc, dict):
        raise Unevaluable('%s is not a JSON object' % RECEIPT_PATH)
    if doc.get('schema') != SCHEMA:
        raise Unevaluable('receipt schema %r != %r' % (doc.get('schema'), SCHEMA))
    files = doc.get('files')
    if not isinstance(files, list):
        raise Unevaluable('receipt files[] is not a list')
    entries = {}
    for item in files:
        if not isinstance(item, dict) or not isinstance(item.get('path'), str):
            raise Unevaluable('receipt entry is not an object with a string path')
        if item['path'] in entries:
            raise Unevaluable('duplicate receipt entry %r' % item['path'])
        entries[item['path']] = item
    return doc, entries


def render(doc):
    return (json.dumps(doc, indent=2) + '\n').encode('utf-8')


def validate_receipt_revision(root, rev, raw):
    """Amendment 3 A7: a 40-hex token that resolves to a commit and is an
    ancestor of (or equal to) the measured revision."""
    if not isinstance(raw, str) or not REV_HEX.match(raw):
        return None, 'receipt revision %r is not a 40-hex token' % (raw,)
    resolved = resolve(root, raw)
    if resolved is None:
        return None, 'receipt revision %s does not resolve' % raw[:12]
    if not is_ancestor(root, resolved, rev):
        return None, ('receipt revision %s is not an ancestor of %s'
                      % (resolved[:12], rev[:12]))
    return resolved, None


def check(root, rev, pop, allow_worktree=False):
    raw, state = receipt_source(root, rev, allow_worktree)
    findings = []
    if raw is None:
        label = 'receipt=uncommitted' if state == 'uncommitted' else 'receipt=absent'
        why = ('%s exists in the working tree but is not committed at %s'
               % (RECEIPT_PATH, rev[:12]) if state == 'uncommitted'
               else '%s is absent at %s' % (RECEIPT_PATH, rev[:12]))
        for path in pop:
            findings.append('%s: %s (%s)' % (path, why, label))
        return {'population': len(pop), 'bound': 0, 'mismatches': len(pop),
                'met': False, 'findings': findings, 'extras': [],
                'source': state, 'receipt_revision': None, 'revision_valid': False}
    doc, entries = parse_receipt(raw)
    rrev_raw = doc.get('revision')
    rrev, invalid = validate_receipt_revision(root, rev, rrev_raw)
    bound = 0
    for path in pop:
        entry = entries.get(path)
        if entry is None:
            findings.append('%s: no receipt entry' % path)
            continue
        reasons = []
        if invalid:
            reasons.append('receipt_revision_invalid: %s' % invalid)
        else:
            raw_here = blob(root, rev, path)
            if raw_here is None:
                reasons.append('path does not resolve at %s' % rev[:12])
            else:
                got = sha256(raw_here)
                if entry.get('sha256') != got:
                    reasons.append('sha256 %s != %s at %s'
                                   % (str(entry.get('sha256'))[:12], got[:12], rev[:12]))
                if entry.get('bytes') != len(raw_here):
                    reasons.append('bytes %r != %d at %s'
                                   % (entry.get('bytes'), len(raw_here), rev[:12]))
                raw_own = blob(root, rrev, path)
                if raw_own is None:
                    reasons.append('path does not resolve at receipt revision %s'
                                   % rrev[:12])
                elif sha256(raw_own) != entry.get('sha256'):
                    reasons.append('sha256 does not re-derive at receipt revision %s'
                                   % rrev[:12])
                mode = selftest_registered(raw_here.decode('utf-8', 'replace'))
                if entry.get('selftest_mode') is not mode:
                    reasons.append('selftest_mode %r != static registration %r'
                                   % (entry.get('selftest_mode'), mode))
        if reasons:
            findings.append('%s: %s' % (path, '; '.join(reasons)))
        else:
            bound += 1
    extras = sorted(set(entries) - set(pop))
    for path in extras:
        findings.append('%s: receipt entry outside the population '
                        '(reported separately, not counted)' % path)
    mismatches = len(pop) - bound
    return {'population': len(pop), 'bound': bound, 'mismatches': mismatches,
            'met': bound == len(pop) and mismatches == 0,
            'findings': findings, 'extras': extras, 'source': state,
            'receipt_revision': rrev or (rrev_raw if isinstance(rrev_raw, str) else None),
            'revision_valid': invalid is None}


def write_receipt(root, rev, date):
    pop, _ = population(root, rev)
    files = [entry_for(root, rev, path) for path in pop]
    doc = {'schema': SCHEMA, 'revision': rev, 'date': date, 'host': host(),
           'files': files}
    data = render(doc)
    dest = os.path.join(root, RECEIPT_PATH)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'wb') as fh:
        fh.write(data)
    return dest, data, len(files)


# ------------------------------------------------------------------ crosscheck

def _load_counter(path):
    spec = importlib.util.spec_from_file_location('_c75_row_truth', path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not (hasattr(mod, 'parse_rows') and hasattr(mod, 'effective')):
        return None
    return mod


def c1_population(skill_text, counter_path):
    """The C1 counter's own derivation of the file list (second implementation
    of the frozen rule) - None when no counter source is usable."""
    try:
        mod = _load_counter(counter_path)
        if mod is None:
            return None
        rows = mod.parse_rows(skill_text)
        live = [r for r in rows if 'historical' not in r['cells'][1]]
        groups = mod.effective(live)
        return sorted(groups)
    except Exception:
        return None


def counter_source(root, rev, c1_path):
    """(path, origin) of a usable C1 counter source, or (None, None)."""
    if c1_path:
        return (c1_path, c1_path) if os.path.isfile(c1_path) else (None, None)
    raw = blob(root, rev, C1_PATH)
    origin = '%s@%s' % (C1_PATH, rev[:12])
    if raw is None:
        p = git(root, 'log', '--all', '--format=%H', '-n', '1', '--', C1_PATH)
        found = p.stdout.strip().splitlines()
        if found:
            raw = blob(root, found[0].strip(), C1_PATH)
            origin = '%s@%s' % (C1_PATH, found[0].strip()[:12])
    if raw is None:
        return None, None
    fd, tmp = tempfile.mkstemp(prefix='c75-counter-', suffix='.py')
    with os.fdopen(fd, 'wb') as fh:
        fh.write(raw)
    return tmp, origin


def crosscheck(root, rev, pop, c1_path):
    text = blob(root, rev, 'SKILL.md')
    src, origin = counter_source(root, rev, c1_path)
    if text is None or src is None:
        return {'available': False, 'source': None}
    try:
        c1 = c1_population(text.decode('utf-8', 'replace'), src)
        return {'available': True, 'population': len(c1) if c1 is not None else None,
                'equal': c1 == pop, 'source': origin}
    finally:
        if src and not (c1_path and os.path.abspath(src) == os.path.abspath(c1_path)):
            try:
                os.unlink(src)
            except OSError:
                pass


# -------------------------------------------------------------------- selftest

FIXTURE_SKILL = '''# Fixture lane (instrument_receipts.py selftest)

### Round 75 gate registry additions

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| alpha-counter | gate (live) | `python3 -B scripts/alpha.py --root .` | `0=met` | `python3 -B scripts/alpha.py --selftest` (2/2) | fixture, not a claim | git | selftest |
| beta-counter | instrument (live) | `python3 -B scripts/beta.py --root .` | `0=met` | none | fixture, not a claim | git | selftest |
| hist-counter | gate (historical: green at `1111111111111111111111111111111111111111`) | `python3 -B scripts/historical.py` | `0=met` | none | fixture, not a claim | git | selftest |

### Round 76 gate registry additions

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| alpha-counter-v2 | gate (live; supersedes the round-75 row) | `python3 -B scripts/alpha.py --root .` | `0=met` | `python3 -B scripts/alpha.py --selftest` | fixture, not a claim | git | selftest |

### Round 77 gate registry corrections

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| not-a-registry-row | gate (live) | `python3 -B scripts/ignored.py` | `0=met` | none | fixture | git | selftest |

## Not a registry section

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| also-not-a-registry-row | gate (live) | `python3 -B scripts/ignored2.py` | `0=met` | none | fixture | git | selftest |
'''

ALPHA = '''#!/usr/bin/env python3
import argparse
import sys


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        print("selftest: 2/2 checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

BETA = '''#!/usr/bin/env python3
"""Fixture instrument with no self-test mode."""


def main():
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

MENTION = '''#!/usr/bin/env python3
"""Fixture: this docstring mentions --selftest without registering it."""


def main():
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def _fixture_git(root, *args):
    p = subprocess.run(['git', '-C', root, *args], capture_output=True, text=True,
                       env=_env())
    if p.returncode != 0:
        raise RuntimeError('fixture git %s failed: %s' % (' '.join(args), p.stderr.strip()))
    return p


def _fixture_commit(root, message):
    _fixture_git(root, 'add', '-A')
    _fixture_git(root, '-c', 'user.name=c2 selftest',
                 '-c', 'user.email=c2-selftest@example.invalid',
                 'commit', '-q', '-m', message)
    return _fixture_git(root, 'rev-parse', 'HEAD').stdout.strip()


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)


def run_selftest(args):
    work = os.path.abspath(args.work) if args.work else tempfile.mkdtemp(prefix='c2-selftest-')
    os.makedirs(work, exist_ok=True)
    base = os.path.join(work, 'c2-selftest-%d' % os.getpid())
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)
    checks = []

    def ck(name, ok, detail=''):
        checks.append((name, bool(ok), detail))

    def receipt_path(root):
        return os.path.join(root, RECEIPT_PATH)

    def put(doc, root):
        with open(receipt_path(root), 'wb') as fh:
            fh.write(render(doc))

    def good_doc(root):
        with open(receipt_path(root), 'rb') as fh:
            return json.loads(fh.read().decode('utf-8'))

    try:
        D = os.path.join(base, 'lane')
        os.makedirs(D)
        _fixture_git(D, 'init', '-q')
        ck('fixture repo is its own toplevel', toplevel(D) == os.path.realpath(D))
        _write(os.path.join(D, 'SKILL.md'), FIXTURE_SKILL)
        _write(os.path.join(D, 'scripts', 'alpha.py'), ALPHA)
        _write(os.path.join(D, 'scripts', 'beta.py'), BETA)
        _write(os.path.join(D, 'scripts', 'historical.py'), BETA)
        _write(os.path.join(D, 'scripts', 'mention.py'), MENTION)
        r1 = _fixture_commit(D, 'fixture: base')

        pop, effective = population(D, r1)
        ck('live row instruments are the population',
           pop == ['scripts/alpha.py', 'scripts/beta.py'], str(pop))
        ck('historical and non-registry rows stay outside the population',
           not ({'scripts/historical.py', 'scripts/ignored.py', 'scripts/ignored2.py'} & set(pop)),
           str(pop))
        ck('a docstring mention is not a --selftest registration',
           not selftest_registered(MENTION))
        ck('an argparse registration is a --selftest registration',
           selftest_registered(ALPHA))
        alpha = entry_for(D, r1, 'scripts/alpha.py')
        beta = entry_for(D, r1, 'scripts/beta.py')
        ck('alpha entry selftest_mode true', alpha['selftest_mode'] is True)
        ck('beta entry selftest_mode false', beta['selftest_mode'] is False)

        dest, data, n = write_receipt(D, r1, '2026-11-03')
        doc = good_doc(D)
        ck('write records the frozen header',
           doc.get('schema') == SCHEMA and doc.get('revision') == r1
           and doc.get('date') == '2026-11-03' and doc.get('host') == host()
           and n == 2, json.dumps({k: doc.get(k) for k in ('schema', 'revision', 'date', 'host')}))
        ck('receipt digests re-derive from the commit',
           doc['files'][0]['sha256'] == sha256(blob(D, r1, doc['files'][0]['path']))
           and doc['files'][0]['bytes'] == len(blob(D, r1, doc['files'][0]['path'])))
        first = data
        _, second, _ = write_receipt(D, r1, '2026-11-03')
        ck('a second write is byte-identical', first == second)

        res = check(D, r1, pop)
        ck('an uncommitted receipt is not admission evidence',
           res['bound'] == 0 and res['mismatches'] == 2 and res['met'] is False
           and res['source'] == 'uncommitted', str(res))
        res = check(D, r1, pop, allow_worktree=True)
        ck('the worktree opt-in reads it for local debugging only',
           res['bound'] == 2 and res['met'] is True and res['source'] == 'worktree')

        r2 = _fixture_commit(D, 'fixture: committed receipt')
        res = check(D, r2, pop)
        ck('a committed matching receipt is green',
           res['bound'] == 2 and res['mismatches'] == 0 and res['met'] is True
           and res['source'] == 'committed' and res['revision_valid'] is True, str(res))

        good = json.loads(first.decode('utf-8'))

        forged = json.loads(json.dumps(good))
        for item in forged['files']:
            item['sha256'] = '0' * 64
        put(forged, D)
        r = _fixture_commit(D, 'fixture: fabricated digests')
        res = check(D, r, pop)
        ck('fabricated digests leave every file unbound',
           res['bound'] == 0 and res['mismatches'] == 2 and res['met'] is False, str(res))

        dropped = json.loads(json.dumps(good))
        dropped['files'] = [i for i in dropped['files'] if i['path'] != 'scripts/beta.py']
        put(dropped, D)
        r = _fixture_commit(D, 'fixture: dropped entry')
        res = check(D, r, pop)
        ck('a dropped entry leaves bound=1', res['bound'] == 1 and res['mismatches'] == 1)

        flipped = json.loads(json.dumps(good))
        for item in flipped['files']:
            if item['path'] == 'scripts/alpha.py':
                item['selftest_mode'] = False
        put(flipped, D)
        r = _fixture_commit(D, 'fixture: flipped selftest_mode')
        res = check(D, r, pop)
        ck('a flipped selftest_mode is one mismatch',
           res['bound'] == 1 and res['mismatches'] == 1)

        extra = json.loads(json.dumps(good))
        extra['files'].append({'path': 'scripts/outside.py', 'sha256': '0' * 64,
                               'bytes': 0, 'selftest_mode': False})
        put(extra, D)
        r = _fixture_commit(D, 'fixture: entry outside the population')
        res = check(D, r, pop)
        ck('an entry outside the population is reported, not counted',
           res['extras'] == ['scripts/outside.py'] and res['bound'] == 2
           and res['met'] is True, str(res))

        put(json.loads(json.dumps(good)), D)
        os.unlink(receipt_path(D))
        res = check(D, r1, pop)
        ck('an absent receipt is a mismatch for every file',
           res['bound'] == 0 and res['mismatches'] == 2 and res['met'] is False
           and res['source'] == 'absent')

        bogus = json.loads(json.dumps(good))
        bogus['revision'] = '0' * 40
        put(bogus, D)
        r = _fixture_commit(D, 'fixture: receipt revision does not resolve')
        res = check(D, r, pop)
        ck('a receipt revision that does not resolve is invalid',
           res['bound'] == 0 and res['mismatches'] == 2
           and res['revision_valid'] is False, str(res))

        tree = _fixture_git(D, 'rev-parse', r1 + '^{tree}').stdout.strip()
        side = _fixture_git(D, '-c', 'user.name=c2 selftest',
                            '-c', 'user.email=c2-selftest@example.invalid',
                            'commit-tree', tree, '-p', r1, '-m', 'side').stdout.strip()
        divergent = json.loads(json.dumps(good))
        divergent['revision'] = side
        put(divergent, D)
        r = _fixture_commit(D, 'fixture: receipt revision is not an ancestor')
        res = check(D, r, pop)
        ck('a receipt revision that is not an ancestor is invalid',
           res['bound'] == 0 and res['mismatches'] == 2
           and res['revision_valid'] is False, str(res))

        selfrev = json.loads(json.dumps(good))
        selfrev['revision'] = r
        put(selfrev, D)
        rself = _fixture_commit(D, 'fixture: receipt revision equals the measured commit')
        res = check(D, rself, pop)
        ck('a receipt whose revision equals the measured commit is valid',
           res['bound'] == 2 and res['met'] is True
           and res['revision_valid'] is True, str(res))

        with open(os.path.join(D, 'scripts', 'alpha.py'), 'a', encoding='utf-8') as fh:
            fh.write('\n# working-tree note (uncommitted)\n')
        res = check(D, rself, pop)
        ck('an uncommitted working-tree edit leaves the check green',
           res['bound'] == 2 and res['mismatches'] == 0 and res['met'] is True, str(res))
        r3 = _fixture_commit(D, 'fixture: committed edit to alpha.py')
        res = check(D, r3, pop)
        ck('a committed edit turns the check red',
           res['bound'] == 1 and res['mismatches'] == 1 and res['met'] is False, str(res))

        stale = json.loads(json.dumps(good))
        stale['revision'] = r1
        put(stale, D)
        r = _fixture_commit(D, 'fixture: receipt bound to an earlier blob')
        res = check(D, r, pop)
        ck('a receipt bound to an earlier blob is red at the measured revision',
           res['bound'] == 1 and res['mismatches'] == 1 and res['met'] is False
           and res['revision_valid'] is True, str(res))

        p = subprocess.run([sys.executable, '-B', os.path.abspath(__file__),
                            '--root', os.path.join(D, 'scripts'), '--revision', r3, '--check'],
                           capture_output=True, text=True, env=_env())
        ck('a --root below the toplevel is unevaluable (exit 2)', p.returncode == 2,
           p.stderr.strip() + p.stdout.strip())
        p = subprocess.run([sys.executable, '-B', os.path.abspath(__file__),
                            '--root', D, '--revision', r3], capture_output=True, text=True,
                           env=_env())
        ck('no mode is usage (exit 64)', p.returncode == 64, p.stderr.strip())
        bad = json.loads(first.decode('utf-8'))
        bad['files'].append(dict(bad['files'][0]))
        try:
            parse_receipt(render(bad))
            ck('a duplicate entry is unevaluable', False)
        except Unevaluable:
            ck('a duplicate entry is unevaluable', True)
        bad = json.loads(first.decode('utf-8'))
        bad['schema'] = 'instrument-receipts/v0'
        try:
            parse_receipt(render(bad))
            ck('a wrong schema is unevaluable', False)
        except Unevaluable:
            ck('a wrong schema is unevaluable', True)
    except Exception as exc:  # a selftest that crashes is a failed selftest, never a pass
        ck('selftest harness ran to completion', False, repr(exc))
    finally:
        if not args.keep:
            shutil.rmtree(base, ignore_errors=True)
            if not args.work:
                shutil.rmtree(work, ignore_errors=True)

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, detail in checks:
        if not ok:
            print('selftest check failed: %s%s' % (name, (' [%s]' % detail) if detail else ''))
    print('instrument_receipts selftest')
    print('selftest: %d/%d checks passed' % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


# ------------------------------------------------------------------------ CLI

def main(argv=None):
    ap = argparse.ArgumentParser(prog='instrument_receipts.py',
                                 description=__doc__.splitlines()[0])
    ap.add_argument('--root', default='.')
    ap.add_argument('--revision')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--date')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--emit-population', action='store_true',
                    help='print the derived population and exit')
    ap.add_argument('--work')
    ap.add_argument('--c1-tool', help='C1 counter source for the population cross-check')
    ap.add_argument('--worktree-receipt', action='store_true',
                    help='local debugging only: read an uncommitted worktree receipt; '
                         'never admission evidence')
    ap.add_argument('--require-committed', action='store_true',
                    help='accepted for CLI compatibility; committed bytes are the default '
                         '(amendment 3 A6)')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--keep', action='store_true', help='selftest: keep the fixture tree')
    args = ap.parse_args(argv)

    if sum(1 for m in (args.check, args.write, args.selftest, args.emit_population) if m) != 1:
        print('64 usage: exactly one of --check, --write, --selftest, '
              '--emit-population is required', file=sys.stderr)
        return 64
    if args.write and not args.date:
        print('64 usage: --write requires --date YYYY-MM-DD', file=sys.stderr)
        return 64
    if args.date:
        try:
            datetime.date.fromisoformat(args.date)
        except ValueError:
            print('64 usage: --date %r is not YYYY-MM-DD' % args.date, file=sys.stderr)
            return 64
    if args.selftest:
        return run_selftest(args)

    root = os.path.abspath(args.root)
    top = toplevel(root)
    if top is None or os.path.realpath(root) != top:
        print('2 unevaluable: --root %s is not a repository toplevel' % args.root,
              file=sys.stderr)
        return 2
    rev_given = args.revision or 'HEAD'
    rev = resolve(root, rev_given)
    if rev is None:
        print('2 unevaluable: --revision %s does not resolve to a commit' % rev_given,
              file=sys.stderr)
        return 2

    try:
        pop, _ = population(root, rev)
        if args.emit_population:
            for path in pop:
                print(path)
            return 0
        missing = [p for p in FROZEN if p not in set(pop)]
        if args.write:
            dest, data, files = write_receipt(root, rev, args.date)
            print('wrote: %s sha256=%s bytes=%d files=%d'
                  % (RECEIPT_PATH, sha256(data), len(data), files))
        result = check(root, rev, pop,
                       allow_worktree=(args.worktree_receipt or args.write))
        cc = crosscheck(root, rev, pop, args.c1_tool)
    except Unevaluable as exc:
        print('2 unevaluable: %s' % exc, file=sys.stderr)
        return 2

    if cc.get('available') and not cc.get('equal'):
        result['findings'].append(
            'population: derived list differs from the C1 counter list (%d vs %r)'
            % (len(pop), cc.get('population')))
        result['mismatches'] += 1
        result['met'] = False
    for path in missing:
        result['findings'].append('%s: frozen population path is no longer derived' % path)
    met = bool(result['met']) and not missing
    print('C2v1 revision=%s population=%d bound=%d mismatches=%d met=%s missing_frozen=%d'
          % (rev_given, result['population'], result['bound'], result['mismatches'],
             str(met).lower(), len(missing)))
    print('  note: receipt=%s state=%s revision=%s revision_valid=%s'
          % (RECEIPT_PATH, result['source'],
             str(result['receipt_revision'] or '-')[:12],
             str(result.get('revision_valid')).lower()))
    if result['source'] == 'worktree':
        print('  admission: false (content check before commit; run --check at a '
              'revision that commits the receipt for evidence)')
    if args.c1_tool or cc.get('available'):
        if cc.get('available'):
            print('  crosscheck: c2_population=%d c1_counter=%s equal=%s source=%s'
                  % (result['population'], cc.get('population'),
                     str(cc.get('equal')).lower(), cc.get('source')))
        else:
            print('  crosscheck: unavailable (no C1 counter source)')
    for path in result['extras']:
        print('  extra: %s (outside the population; not counted)' % path)
    for finding in result['findings']:
        print('  finding: %s' % finding)
    if args.json:
        payload = dict(result)
        payload.update({'revision': rev, 'missing_frozen': len(missing),
                        'crosscheck': cc})
        print(json.dumps(payload, indent=2))
    return 0 if met else 1


if __name__ == '__main__':
    sys.exit(main())
