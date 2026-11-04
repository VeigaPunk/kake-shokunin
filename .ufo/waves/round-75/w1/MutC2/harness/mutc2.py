#!/usr/bin/env python3
"""mutc2.py — mutation-test the C2 receipt tool (contract §C2).

For every mutant: copy the reference tool, apply one semantic mutation, run the
mutated tool's ``--selftest`` and probe independent fixture states whose correct
verdict is known from the pristine tool.  A mutant survives when the selftest
still passes and every should-be-red state still comes back green (met=true).
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, 'ref', 'instrument_receipts.py')
WORK = os.path.join(HERE, 'work', 'c2mut')


def load(path):
    spec = importlib.util.spec_from_file_location('refc2', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R = load(REF)

SKILL = R.FIXTURE_SKILL
ALPHA = R.FIXTURE_ALPHA
BETA = R.FIXTURE_BETA
GAMMA = R.FIXTURE_GAMMA
EXTRA = R.FIXTURE_EXTRA
BASE_FILES = {
    'SKILL.md': SKILL,
    '.ufo/waves/round-99/alpha.py': ALPHA,
    '.ufo/waves/round-99/beta.py': BETA,
    '.ufo/waves/round-99/gamma.py': GAMMA,
    '.ufo/waves/round-99/extra.py': EXTRA,
}


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def commit(root, message):
    run(['git', '-C', root, 'add', '-A'])
    p = run(['git', '-C', root, '-c', 'user.name=mutc2',
             '-c', 'user.email=mutc2@example.invalid', 'commit', '-q', '-m', message])
    if p.returncode != 0:
        raise RuntimeError(f'fixture commit failed: {p.stderr}')


def mkfx(work, name):
    root = os.path.join(work, 'fx', name)
    if os.path.isdir(root):
        shutil.rmtree(root)
    base = os.path.join(root, '.ufo', 'waves', 'round-99')
    os.makedirs(base)
    run(['git', '-C', root, 'init', '-q'])
    top = run(['git', '-C', root, 'rev-parse', '--show-toplevel']).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(root):
        raise RuntimeError(f'fixture toplevel {top!r} != {root!r}')
    for rel, text in BASE_FILES.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(text)
    commit(root, 'fixture')
    return root


def head(root):
    return run(['git', '-C', root, 'rev-parse', 'HEAD']).stdout.strip()


def put_receipt(root, rec):
    p = os.path.join(root, R.RECEIPT_PATH)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(rec, indent=2) + '\n')


def read_receipt(root):
    with open(os.path.join(root, R.RECEIPT_PATH), encoding='utf-8') as fh:
        return json.loads(fh.read())


def green(work, name='green'):
    root = mkfx(work, name)
    R.write_receipt(root, head(root), '2026-11-03')
    commit(root, 'receipt')
    return root, head(root)


def st_green(work):
    return green(work, 'green')


def st_fab_digest(work):
    root, _ = green(work, 'fab_digest')
    rec = read_receipt(root)
    for entry in rec['files']:
        entry['sha256'] = '0' * 64
    put_receipt(root, rec)
    commit(root, 'fabricated digests')
    return root, head(root)


def st_fab_bytes(work):
    root, _ = green(work, 'fab_bytes')
    rec = read_receipt(root)
    for entry in rec['files']:
        entry['bytes'] = entry['bytes'] + 7
    put_receipt(root, rec)
    commit(root, 'wrong byte counts')
    return root, head(root)


def st_missing(work):
    root, _ = green(work, 'missing')
    rec = read_receipt(root)
    rec['files'] = [e for e in rec['files'] if not e['path'].endswith('beta.py')]
    put_receipt(root, rec)
    commit(root, 'missing entry')
    return root, head(root)


def st_extra(work):
    root, _ = green(work, 'extra')
    raw = open(os.path.join(root, '.ufo/waves/round-99/extra.py'), 'rb').read()
    rec = read_receipt(root)
    rec['files'].append({'path': '.ufo/waves/round-99/extra.py',
                         'sha256': hashlib.sha256(raw).hexdigest(),
                         'bytes': len(raw), 'selftest_mode': False})
    put_receipt(root, rec)
    commit(root, 'extra entry')
    return root, head(root)


def st_mode(work):
    root, _ = green(work, 'mode')
    rec = read_receipt(root)
    for entry in rec['files']:
        if entry['path'].endswith('beta.py'):
            entry['selftest_mode'] = True
    put_receipt(root, rec)
    commit(root, 'mode flip')
    return root, head(root)


def st_dirty(work):
    root = mkfx(work, 'dirty')
    rev = head(root)
    paths = R.population(root, rev)
    derived = R.derive(root, rev, paths)
    dirty = (ALPHA + '\n# dirty working tree\n').encode()
    derived['.ufo/waves/round-99/alpha.py'] = {
        'sha256': hashlib.sha256(dirty).hexdigest(), 'bytes': len(dirty),
        'selftest_mode': R.selftest_mode(dirty)}
    rec = {'schema': R.SCHEMA, 'revision': rev, 'date': '2026-11-03',
           'host': 'mutc2',
           'files': [{'path': p, **derived[p]} for p in sorted(derived)]}
    with open(os.path.join(root, '.ufo/waves/round-99/alpha.py'), 'a') as fh:
        fh.write('\n# dirty working tree\n')
    put_receipt(root, rec)
    run(['git', '-C', root, 'add', '--', R.RECEIPT_PATH])
    run(['git', '-C', root, '-c', 'user.name=mutc2',
         '-c', 'user.email=mutc2@example.invalid', 'commit', '-q', '-m', 'receipt'])
    return root, head(root)


def st_stale(work):
    root, _ = green(work, 'stale')
    with open(os.path.join(root, '.ufo/waves/round-99/alpha.py'), 'a') as fh:
        fh.write('\n# blob moved on\n')
    commit(root, 'blob moved on')
    return root, head(root)


def st_dup(work):
    root, _ = green(work, 'dup')
    rec = read_receipt(root)
    alpha = [e for e in rec['files'] if e['path'].endswith('alpha.py')][0]
    bad = dict(alpha)
    bad['sha256'] = '0' * 64
    rec['files'].insert(rec['files'].index(alpha), bad)
    put_receipt(root, rec)
    commit(root, 'duplicate path')
    return root, head(root)


def st_combined(work):
    root, _ = green(work, 'combined')
    rec = read_receipt(root)
    alpha = [e for e in rec['files'] if e['path'].endswith('alpha.py')][0]
    rec['files'] = [e for e in rec['files']
                    if not (e['path'].endswith('alpha.py')
                            or e['path'].endswith('beta.py'))]
    combined = dict(alpha)
    combined['path'] = '.ufo/waves/round-99/alpha.py, .ufo/waves/round-99/beta.py'
    rec['files'].append(combined)
    put_receipt(root, rec)
    commit(root, 'combined path')
    return root, head(root)


def st_fault(work):
    root, _ = green(work, 'fault')
    return root, 'deadbeef' * 5


STATES = [('green', st_green, 'green'), ('fab_digest', st_fab_digest, 'red'),
          ('fab_bytes', st_fab_bytes, 'red'), ('missing', st_missing, 'red'),
          ('extra', st_extra, 'green'), ('mode', st_mode, 'red'),
          ('dirty', st_dirty, 'red'), ('stale', st_stale, 'red'),
          ('dup', st_dup, 'red'), ('combined', st_combined, 'red'),
          ('fault', st_fault, 'fault')]

LINE_RE = None


def check(tool, root, rev):
    p = run([sys.executable, '-B', tool, '--root', root, '--revision', rev, '--check'])
    out = {'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr,
           'met': None, 'population': None, 'bound': None, 'mismatches': None}
    for line in p.stdout.splitlines():
        if line.startswith('C2v1 '):
            fields = dict(kv.split('=', 1) for kv in line.split() if '=' in kv)
            out['met'] = fields.get('met') == 'true'
            out['population'] = int(fields['population']) if 'population' in fields else None
            out['bound'] = int(fields['bound']) if 'bound' in fields else None
            out['mismatches'] = int(fields['mismatches']) if 'mismatches' in fields else None
    return out


def write_format(tool, work, name):
    root = mkfx(work, name)
    a = run([sys.executable, '-B', tool, '--root', root, '--revision', head(root),
             '--write', '--date', '2026-11-03'])
    raw1 = open(os.path.join(root, R.RECEIPT_PATH), 'rb').read()
    b = run([sys.executable, '-B', tool, '--root', root, '--revision', head(root),
             '--write', '--date', '2026-11-03'])
    raw2 = open(os.path.join(root, R.RECEIPT_PATH), 'rb').read()
    try:
        rec = json.loads(raw1.decode())
        paths = [e['path'] for e in rec['files']]
    except Exception:
        paths = []
    return {'write_exit': a.returncode, 'second_exit': b.returncode,
            'sorted': paths == sorted(paths), 'newline': raw1.endswith(b'\n'),
            'idempotent': raw1 == raw2, 'entries': len(paths)}


MUTANTS = [
    ('C2-M1', 'skip the digest comparison', 'digest binding',
     "        bad = [k for k in ('sha256', 'bytes', 'selftest_mode')\n",
     "        bad = [k for k in ('bytes', 'selftest_mode')\n"),
    ('C2-M2', 'weaken the digest comparison to a length proxy (bytes instead of sha256)',
     'digest binding',
     "        bad = [k for k in ('sha256', 'bytes', 'selftest_mode')\n               if entry.get(k) != want[k]]\n",
     "        bad = [k for k in ('bytes', 'selftest_mode')\n               if entry.get(k) != want[k]]\n        if entry.get('sha256') is not None and len(str(entry.get('sha256'))) != 64:\n            bad.append('sha256')\n"),
    ('C2-M3', 'accept a missing receipt entry as bound', 'population completeness',
     "        if not seen:\n            findings.append(f'{path}: no receipt entry')\n            continue\n",
     "        if not seen:\n            bound += 1\n            continue\n"),
    ('C2-M4', 'count a path outside the population (derive population from the receipt)',
     'population completeness',
     "    extra = sorted(set(by_path) - set(paths))\n",
     "    extra = sorted(set(by_path) - set(paths))\n    for path in extra:\n        paths.append(path)\n        bound += 1\n"),
    ('C2-M5', 'treat selftest_mode as always true', 'mode binding',
     "                     'selftest_mode': selftest_mode(data)}\n",
     "                     'selftest_mode': True}\n"),
    ('C2-M6', 'read the working tree instead of the committed blob', 'blob provenance',
     "    p = git(root, 'show', f'{rev}:{path}')\n    if p.returncode != 0:\n        return None\n    return p.stdout\n",
     "    p = git(root, 'show', f'{rev}:{path}')\n    if p.returncode != 0:\n        return None\n    target = os.path.join(root, path)\n    if os.path.isfile(target):\n        with open(target, 'rb') as fh:\n            return fh.read()\n    return p.stdout\n"),
    ('C2-M7', "ignore the receipt's revision", 'blob provenance',
     "    derived = derive(root, rev, paths)\n",
     "    derived = derive(root, receipt.get('revision') or rev, paths)\n"),
    ('C2-M8', 'write the receipt unsorted (reverse order)', 'write idempotence',
     "                         for p in sorted(derived)]}\n",
     "                         for p in reversed(sorted(derived))]}\n"),
    ('C2-M9', 'drop the trailing newline from the written receipt', 'write idempotence',
     "    text = json.dumps(receipt, indent=2) + '\\n'\n",
     "    text = json.dumps(receipt, indent=2)\n"),
    ('C2-M10', 'swallow a git failure and report unevaluable as met', 'fault handling',
     "    except Unevaluable as exc:\n        print(f'2 unevaluable: {exc}', file=sys.stderr)\n        return 2\n",
     "    except Unevaluable as exc:\n        print(f'C2v1 revision={rev} population=0 bound=0 mismatches=0 met=true')\n        return 0\n"),
    ('C2-M11', 'accept a duplicated path (last entry wins)', 'entry uniqueness',
     "        if len(seen) > 1:\n            findings.append(f'{path}: {len(seen)} receipt entries for one path')\n            continue\n        entry = seen[0]\n",
     "        entry = seen[-1]\n"),
    ('C2-M12', 'accept one receipt entry covering two paths', 'entry uniqueness',
     "        by_path.setdefault(entry['path'], []).append(entry)\n",
     "        parts = [q.strip() for q in str(entry['path']).split(',')]\n        entry['_multi'] = len(parts) > 1\n        for part in parts:\n            by_path.setdefault(part, []).append(entry)\n"),
]


def apply_mutant(text, old, new):
    if old not in text:
        raise SystemExit(f'mutation anchor not found: {old[:70]!r}')
    return text.replace(old, new, 1)


def extra_multi_credit(text):
    """Patch applied after C2-M12: credit a combined entry without comparing it."""
    old = "        entry = seen[0]\n        want = derived[path]\n"
    new = "        entry = seen[0]\n        if entry.get('_multi'):\n            bound += 1\n            continue\n        want = derived[path]\n"
    return apply_mutant(text, old, new)


def main():
    work = WORK
    os.makedirs(work, exist_ok=True)
    src = open(REF, encoding='utf-8').read()
    pristine = check(REF, *st_green(work))
    results = {'tool': REF, 'sha256': hashlib.sha256(src.encode()).hexdigest(),
               'pristine_green': pristine, 'mutants': []}
    fmt_green = write_format(REF, work, 'fmt_ref')
    results['pristine_write'] = fmt_green
    for mid, name, dimension, old, new in MUTANTS:
        mroot = os.path.join(work, 'mut', mid)
        if os.path.isdir(mroot):
            shutil.rmtree(mroot)
        os.makedirs(mroot)
        path = os.path.join(mroot, 'instrument_receipts.py')
        body = apply_mutant(src, old, new)
        if mid == 'C2-M12':
            body = extra_multi_credit(body)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(body)
        st = run([sys.executable, '-B', path, '--selftest', '--work',
                  os.path.join(mroot, 'st')])
        rec = {'id': mid, 'mutation': name, 'dimension': dimension,
               'selftest_exit': st.returncode,
               'selftest_tail': [ln for ln in st.stdout.splitlines() if 'selftest' in ln][-1:],
               'states': []}
        missed = []
        broken = []
        for sname, builder, expect in STATES:
            root, rev = builder(mroot)
            pr = check(REF, root, rev)
            mu = check(path, root, rev)
            rec['states'].append({'state': sname, 'expect': expect,
                                  'pristine': {'exit': pr['exit'], 'met': pr['met'],
                                               'population': pr['population']},
                                  'mutant': {'exit': mu['exit'], 'met': mu['met'],
                                             'population': mu['population']}})
            if expect == 'red':
                if pr['exit'] != 1:
                    broken.append(f'{sname}: pristine not red (exit {pr["exit"]})')
                elif mu['exit'] == 0 or mu['met'] is True:
                    missed.append(sname)
            elif expect == 'green':
                if pr['exit'] != 0:
                    broken.append(f'{sname}: pristine not green (exit {pr["exit"]})')
                elif (mu['exit'] != 0 or mu['met'] is not True
                      or mu['population'] != pr['population']
                      or mu['bound'] != pr['bound']):
                    broken.append(f'{sname}: shape divergence '
                                  f'(mutant pop={mu["population"]} bound={mu["bound"]} '
                                  f'vs pristine pop={pr["population"]} bound={pr["bound"]})')
            elif expect == 'fault':
                if pr['exit'] != 2:
                    broken.append(f'{sname}: pristine not unevaluable (exit {pr["exit"]})')
                elif mu['exit'] != 2:
                    missed.append(sname)
        wf = write_format(path, mroot, 'fmt')
        rec['write'] = wf
        if not (wf['sorted'] and wf['newline'] and wf['idempotent']
                and wf['write_exit'] == 0):
            broken.append('write_format')
        rec['missed_red_states'] = missed
        rec['broken_states'] = broken
        if st.returncode != 0:
            rec['verdict'] = 'killed (tool --selftest)'
        elif missed:
            rec['verdict'] = 'SURVIVED (red state still green)'
        elif broken:
            rec['verdict'] = 'SURVIVED its selftest; killed by independent probe'
        else:
            rec['verdict'] = 'inert (no observable divergence)'
        results['mutants'].append(rec)
        print(f"{mid}: selftest={st.returncode} missed={missed} broken={broken[:4]} "
              f"verdict={rec['verdict']}")
    out = os.path.join(HERE, 'work', 'c2mut-results.json')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(results, fh, indent=2)
    print('wrote', out)


if __name__ == '__main__':
    main()
