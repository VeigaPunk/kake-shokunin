#!/usr/bin/env python3
"""mutc2_real.py — mutation-test the LANDED C2 tool.

State fixtures are commits in a `git clone --shared` of the lane at the base
revision: every receipt is committed (the tool reads committed bytes only) and
its declared revision is the base commit, an ancestor of every carrier commit.

Each mutant runs the tool's own ``--selftest`` (case-by-case) and is probed on
the state set; a mutant survives when its selftest is green and a should-be-red
state still reports ``met=true`` (or a green state's bound/population moves).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/kake-shokunin'
TOOL_SRC = os.path.join(LANE, '.ufo/waves/round-75/w1/ExecC2Tool/instrument_receipts.py')
RECEIPT = 'corpus/knowledge/instrument-receipts.json'
BASE = 'c9c5e484c533aa65f4374b841a3edcf572ed19a9'
WORK = os.path.join(HERE, 'work', 'c2real')
REPO = os.path.join(WORK, 'probe-repo')
TOOL = os.path.join(WORK, 'real-tool.py')


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def git(repo, *args):
    p = run(['git', '-C', repo, *args])
    if p.returncode != 0:
        raise RuntimeError(f'git {args} failed: {p.stderr.strip()}')
    return p.stdout


def commit(repo, message, only=()):
    if only:
        git(repo, 'add', '--', *only)
    else:
        git(repo, 'add', '-A')
    git(repo, '-c', 'user.name=mutc2', '-c', 'user.email=mutc2@example.invalid',
        '-c', 'commit.gpgsign=false', 'commit', '-q', '-m', message)
    return git(repo, 'rev-parse', 'HEAD').strip()


def put_doc(repo, doc):
    path = os.path.join(repo, *RECEIPT.split('/'))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='ascii', newline='\n') as fh:
        fh.write(json.dumps(doc, indent=2, ensure_ascii=True) + '\n')


def tool_write(repo, rev):
    p = run([sys.executable, '-B', TOOL, '--root', repo, '--revision', rev,
             '--write', '--date', '2026-11-03'])
    if p.returncode != 0:
        raise RuntimeError(f'--write failed: {p.stdout}{p.stderr}')
    with open(os.path.join(repo, *RECEIPT.split('/')), encoding='ascii') as fh:
        return json.load(fh)


def check(tool, repo, rev):
    p = run([sys.executable, '-B', tool, '--root', repo, '--revision', rev, '--check'])
    out = {'exit': p.returncode, 'met': None, 'population': None, 'bound': None,
           'mismatches': None, 'stdout': p.stdout, 'stderr': p.stderr}
    for line in p.stdout.splitlines():
        if line.startswith('C2v1 '):
            fields = dict(kv.split('=', 1) for kv in line.split() if '=' in kv)
            out['met'] = fields.get('met') == 'true'
            for key in ('population', 'bound', 'mismatches'):
                if key in fields:
                    out[key] = int(fields[key])
    return out


def selftest(tool, work):
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    p = run([sys.executable, '-B', tool, '--selftest', '--work', work])
    cases = {}
    for line in p.stdout.splitlines():
        if line.startswith('selftest: ok '):
            cases[line[len('selftest: ok '):]] = True
        elif line.startswith('selftest: FAIL '):
            cases[line[len('selftest: FAIL '):].split(' :: ')[0]] = False
    return p.returncode, cases


def build_states():
    os.makedirs(WORK, exist_ok=True)
    shutil.rmtree(REPO, ignore_errors=True)
    p = run(['git', 'clone', '-q', '--shared', LANE, REPO])
    if p.returncode != 0:
        raise RuntimeError(f'clone failed: {p.stderr}')
    git(REPO, 'checkout', '-q', BASE)
    top = git(REPO, 'rev-parse', '--show-toplevel').strip()
    if os.path.realpath(top) != os.path.realpath(REPO):
        raise RuntimeError(f'probe toplevel {top!r} != {REPO!r}')
    good = tool_write(REPO, BASE)
    rev_good = commit(REPO, 'good receipt', only=(RECEIPT,))
    states = {'good': (rev_good, 'green')}

    def variant(name, mutate, kind='red'):
        doc = json.loads(json.dumps(good))
        mutate(doc)
        put_doc(REPO, doc)
        states[name] = (commit(REPO, name, only=(RECEIPT,)), kind)

    def fab_one(doc):
        doc['files'][0]['sha256'] = '0' * 64

    def fab_bytes(doc):
        doc['files'][1]['bytes'] += 7

    def mode_false(doc):
        next(e for e in doc['files'] if e['selftest_mode'])['selftest_mode'] = False

    def mode_true(doc):
        next(e for e in doc['files'] if not e['selftest_mode'])['selftest_mode'] = True

    def dropped(doc):
        doc['files'] = [e for e in doc['files'] if e['path'] != 'scripts/id_resolver.py']

    def outside(doc):
        doc['files'].append({'path': 'scripts/outside_population.py', 'sha256': '0' * 64,
                             'bytes': 0, 'selftest_mode': False})
        doc['files'].sort(key=lambda e: e['path'])

    def duplicate(doc):
        target = doc['files'][0]
        bad = dict(target)
        bad['sha256'] = '0' * 64
        doc['files'].insert(doc['files'].index(target), bad)

    def combined(doc):
        first, second = doc['files'][0], doc['files'][1]
        doc['files'] = [e for e in doc['files'] if e is not first and e is not second]
        merged = dict(first)
        merged['path'] = first['path'] + ', ' + second['path']
        doc['files'].append(merged)

    variant('fab_digest', fab_one)
    variant('fab_bytes', fab_bytes)
    variant('mode_false', mode_false)
    variant('mode_true', mode_true)
    variant('missing', dropped)
    variant('outside', outside, kind='green')
    variant('duplicate', duplicate)
    variant('combined', combined)

    # dirty: the receipt records the WORKING TREE bytes of scripts/id_resolver.py,
    # while the commit that carries the receipt keeps the committed blob clean.
    dirty_doc = json.loads(json.dumps(good))
    target = os.path.join(REPO, 'scripts', 'id_resolver.py')
    with open(target, 'ab') as fh:
        fh.write(b'\n# uncommitted working-tree edit\n')
    raw = open(target, 'rb').read()
    for entry in dirty_doc['files']:
        if entry['path'] == 'scripts/id_resolver.py':
            entry['sha256'] = hashlib.sha256(raw).hexdigest()
            entry['bytes'] = len(raw)
    put_doc(REPO, dirty_doc)
    states['dirty'] = (commit(REPO, 'receipt for dirty worktree', only=(RECEIPT,)), 'red')

    # stale: restore the good receipt (pins BASE), then move a population blob.
    git(REPO, 'checkout', '--', 'scripts/id_resolver.py')
    put_doc(REPO, good)
    commit(REPO, 'restore good receipt', only=(RECEIPT,))
    with open(target, 'ab') as fh:
        fh.write(b'\n# committed change after the receipt\n')
    states['stale'] = (commit(REPO, 'population blob moves'), 'red')

    # fault: a revision that does not resolve
    states['fault'] = ('deadbeef' * 5, 'fault')
    base_bytes = subprocess.run(['git', '-C', REPO, 'show',
                                 f'{BASE}:scripts/id_resolver.py'],
                                capture_output=True).stdout
    dirty_bytes = base_bytes + b'\n# uncommitted working-tree edit\n'
    return states, base_bytes, dirty_bytes


MUTANTS = [
    ('C2-M1', 'skip the digest comparison', 'digest binding',
     "            if entry[\"sha256\"] != digest:",
     "            if False and entry[\"sha256\"] != digest:"),
    ('C2-M2', 'compare byte length instead of sha256', 'digest binding',
     [("            if entry[\"sha256\"] != digest:",
       "            if entry[\"bytes\"] != len(blob):"),
      ("            elif entry[\"bytes\"] != len(blob):",
       "            elif False:")], None),
    ('C2-M3', 'accept a missing receipt entry as bound', 'population completeness',
     "            entry = entries.get(path)\n            if entry is None:",
     "            entry = entries.get(path)\n            if entry is None:\n                bound += 1\n                continue"),
    ('C2-M4', 'count a path outside the population toward bound', 'population completeness',
     "        outside = sorted(path for path in entries if path not in present)",
     "        outside = sorted(path for path in entries if path not in present)\n        bound += len(outside)"),
    ('C2-M5', 'treat selftest_mode as always true', 'mode binding',
     "            flag, note = selftest_registration(path, blob)",
     "            flag, note = True, 'forced'"),
    ('C2-M6', 'read the working tree instead of the committed blob', 'blob provenance',
     """    return {
        path: (mode, blobs[oid])
        for path, (mode, kind, oid) in entries.items()
        if kind == "blob" and oid in blobs
    }""",
     """    result = {
        path: (mode, blobs[oid])
        for path, (mode, kind, oid) in entries.items()
        if kind == "blob" and oid in blobs
    }
    for path in list(result):
        local = os.path.join(root, *path.split("/"))
        if os.path.isfile(local):
            with open(local, "rb") as handle:
                result[path] = (result[path][0], handle.read())
    return result"""),
    ('C2-M7', "derive blobs at the receipt's declared revision, not --revision", 'blob provenance',
     "        blobs = read_population_blobs(root, rev, population)",
     "        blobs = read_population_blobs(root, document.get('revision') or rev, population)"),
    ('C2-M8', 'write the receipt unsorted (reverse path order)', 'write idempotence',
     """    files = []
    for path in population:""",
     """    files = []
    for path in reversed(population):"""),
    ('C2-M9', 'drop the trailing newline from the written receipt', 'write idempotence',
     '    return json.dumps(document, indent=2, ensure_ascii=True) + "\\n"',
     '    return json.dumps(document, indent=2, ensure_ascii=True)'),
    ('C2-M10', 'swallow a git failure and report unevaluable as met', 'fault handling',
     """    except Unevaluable as exc:
        print(f"2 unevaluable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":""",
     """    except Unevaluable as exc:
        print("C2v1 revision=unknown population=0 bound=0 mismatches=0 met=true")
        return 0


if __name__ == "__main__":"""),
    ('C2-M11', 'accept a duplicated path (last entry wins)', 'entry uniqueness',
     """            if path in entries:
                duplicates.add(path)
            else:
                entries[path] = entry""",
     """            entries[path] = entry"""),
    ('C2-M12', 'accept one receipt entry covering two paths', 'entry uniqueness',
     """            if path in entries:
                duplicates.add(path)
            else:
                entries[path] = entry""",
     """            parts = [q.strip() for q in path.split(",")]
            entry["_multi"] = len(parts) > 1
            for part in parts:
                if part in entries:
                    duplicates.add(part)
                else:
                    entries[part] = entry"""),
]


def main():
    os.makedirs(WORK, exist_ok=True)
    shutil.copyfile(TOOL_SRC, TOOL)
    tool_sha = sha(TOOL)
    src = open(TOOL, encoding='utf-8').read()
    states, base_bytes, dirty_bytes = build_states()
    pristine = {}

    def set_worktree(name):
        payload = dirty_bytes if name == 'dirty' else base_bytes
        with open(os.path.join(REPO, 'scripts', 'id_resolver.py'), 'wb') as fh:
            fh.write(payload)

    for name, (rev, kind) in states.items():
        set_worktree(name)
        pristine[name] = check(TOOL, REPO, rev)
    st_exit, st_cases = selftest(TOOL, os.path.join(WORK, 'st-pristine'))
    results = {'tool': TOOL_SRC, 'tool_sha256': tool_sha,
               'selftest': {'exit': st_exit, 'cases': st_cases},
               'states': {k: {'rev': v[0], 'kind': v[1]} for k, v in states.items()},
               'pristine': pristine, 'mutants': []}
    print('pristine:', {k: (v['exit'], v['met'], v['population'], v['bound'])
                        for k, v in pristine.items()})
    print('selftest pristine:', st_exit, len(st_cases), 'cases')
    for mid, name, dimension, old, new in MUTANTS:
        pairs = old if isinstance(old, list) else [(old, new)]
        for anchor, _replacement in pairs:
            if anchor not in src:
                raise SystemExit(f'{mid}: anchor not found: {anchor[:70]!r}')
        mroot = os.path.join(WORK, 'mut', mid)
        os.makedirs(mroot, exist_ok=True)
        path = os.path.join(mroot, 'instrument_receipts.py')
        body = src
        for anchor, replacement in pairs:
            body = body.replace(anchor, replacement, 1)
        if mid == 'C2-M12':
            marker = """            shape = entry_problem(entry)
            if shape:
                findings.append({"path": path, "class": "shape", "detail": shape})
                continue"""
            body = body.replace(marker, marker + """
            if entry.get("_multi"):
                bound += 1
                continue""", 1)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(body)
        st_rc, st_cases_m = selftest(path, os.path.join(mroot, 'st'))
        rec = {'id': mid, 'mutation': name, 'dimension': dimension,
               'selftest_exit': st_rc,
               'selftest_failed': sorted(k for k, v in st_cases_m.items() if not v),
               'selftest_missing': sorted(set(st_cases) - set(st_cases_m)),
               'states': {}, 'missed_red': [], 'broken': []}
        for sname, (rev, kind) in states.items():
            set_worktree(sname)
            mu = check(path, REPO, rev)
            pr = pristine[sname]
            rec['states'][sname] = {
                'kind': kind,
                'pristine': {k: pr[k] for k in ('exit', 'met', 'population', 'bound')},
                'mutant': {k: mu[k] for k in ('exit', 'met', 'population', 'bound', 'mismatches')},
            }
            if kind == 'red':
                if pr['exit'] != 1:
                    rec['broken'].append(f'{sname}: pristine not red')
                elif mu['exit'] == 0 or mu['met'] is True:
                    rec['missed_red'].append(sname)
            elif kind == 'green':
                if pr['exit'] != 0:
                    rec['broken'].append(f'{sname}: pristine not green')
                elif (mu['exit'] != 0 or mu['met'] is not True
                      or mu['bound'] != pr['bound'] or mu['population'] != pr['population']):
                    rec['broken'].append(
                        f'{sname}: shape divergence (mutant {mu["bound"]}/{mu["population"]} '
                        f'vs pristine {pr["bound"]}/{pr["population"]})')
            elif kind == 'fault':
                if pr['exit'] != 2:
                    rec['broken'].append(f'{sname}: pristine not unevaluable')
                elif mu['exit'] != 2:
                    rec['missed_red'].append(sname)
        # write-format probe
        fmt = {}
        for run_no, tag in ((1, 'one'), (2, 'two')):
            p = run([sys.executable, '-B', path, '--root', REPO, '--revision', BASE,
                     '--write', '--date', '2026-11-03'])
            raw = open(os.path.join(REPO, *RECEIPT.split('/')), 'rb').read()
            fmt[tag] = raw
            fmt[tag + '_rc'] = p.returncode
        try:
            paths = [e['path'] for e in json.loads(fmt['one'].decode())['files']]
        except Exception:
            paths = []
        rec['write'] = {'sorted': paths == sorted(paths), 'newline': fmt['one'].endswith(b'\n'),
                        'idempotent': fmt['one'] == fmt['two'],
                        'rc': (fmt['one_rc'], fmt['two_rc'])}
        if not (rec['write']['sorted'] and rec['write']['newline'] and rec['write']['idempotent']):
            rec['broken'].append('write_format')
        if st_rc != 0:
            rec['verdict'] = 'killed (tool --selftest)'
        elif rec['missed_red']:
            rec['verdict'] = 'SURVIVED (red state still green)'
        elif rec['broken']:
            rec['verdict'] = 'SURVIVED its selftest; killed by independent probe'
        else:
            rec['verdict'] = 'inert (no observable divergence)'
        results['mutants'].append(rec)
        print(f"{mid}: selftest={st_rc} failed={rec['selftest_failed']} "
              f"missed={rec['missed_red']} broken={rec['broken'][:3]} -> {rec['verdict']}")
    out = os.path.join(WORK, 'c2real-results.json')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(results, fh, indent=2)
    print('wrote', out)
    print('tool sha256 before/after:', tool_sha, sha(TOOL_SRC))


if __name__ == '__main__':
    main()
