import json, os, subprocess, shutil
from pathlib import Path

S = Path('/fast/scratch/hyaku/kake-r89/ReviewCounterC1')
E = S / 'e-git'
CTR = S / 'counters' / 'c89_defect_queue.py'
RC = S / 'receipts'
FREEZE_SRC = Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-89/c89_key.py')
FREEZE = '.ufo/waves/round-89/c89_key.py'
DISPATCH = '.ufo/waves/round-89/w1.ready'


def git(*a, env=None, check=True):
    p = subprocess.run(['git', '-C', str(E), *a], capture_output=True, text=True, env=env)
    if check and p.returncode != 0:
        raise SystemExit(f'git {a}: {p.stderr}')
    return p


def top_ok():
    assert git('rev-parse', '--show-toplevel').stdout.strip() == str(E)


def commit(msg, when=None, files=()):
    for path, data in files:
        f = E / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(data)
    git('add', '-A')
    env = dict(os.environ)
    if when:
        env['GIT_AUTHOR_DATE'] = when
        env['GIT_COMMITTER_DATE'] = when
    git('commit', '-qm', msg, env=env)
    return git('rev-parse', 'HEAD').stdout.strip()


def at(name, ref):
    git('checkout', '-q', '-B', name, ref)


def run(name, rev):
    """Count at `rev` with whatever HEAD is checked out (the way the counter is run)."""
    head = git('rev-parse', 'HEAD').stdout.strip()
    work = S / 'w' / ('E-' + name)
    cmd = ['python3', '-B', str(CTR), '--root', str(E), '--revision', rev, '--work', str(work)]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(S))
    rec = RC / f'E-{name}.txt'
    rec.write_text(f'$ (HEAD={head[:8]}) ' + ' '.join(cmd) + f'\n# exit={p.returncode}\n'
                   + p.stdout + p.stderr)
    lines = p.stdout.splitlines()
    E_item = json.loads(lines[1])['E-freeze-before-dispatch'] if len(lines) > 1 else None
    return {'name': name, 'head': head[:8], 'rev': rev[:8], 'exit': p.returncode,
            'E_fails': E_item, 'summary': lines[0] if lines else p.stderr[:200]}


if E.exists():
    shutil.rmtree(E)
E.mkdir()
git('init', '-q')
git('config', 'user.email', 'r@r')
git('config', 'user.name', 'r')
top_ok()
freeze_bytes = FREEZE_SRC.read_bytes()

c0 = commit('root', '2026-11-04T09:00:00Z', [('README', b'x\n')])
results = []

# good order: c0 -> freeze(10:00) -> dispatch(11:00), branch ok
at('ok', c0)
f_ok = commit('freeze', '2026-11-04T10:00:00Z', [(FREEZE, freeze_bytes)])
d_ok = commit('dispatch', '2026-11-04T11:00:00Z', [(DISPATCH, b'dispatch\n')])
results.append(run('good-order-HEAD-good', d_ok))

# reversed order: c0 -> dispatch(10:00) -> freeze(11:00), branch bad
at('bad', c0)
d_bad = commit('dispatch-first', '2026-11-04T10:00:00Z', [(DISPATCH, b'dispatch\n')])
f_bad = commit('freeze-second', '2026-11-04T11:00:00Z', [(FREEZE, freeze_bytes)])
results.append(run('bad-order-HEAD-bad', f_bad))  # HEAD = bad, rev = bad tip

# (a) HEAD-dependence: revision bad, HEAD good => counter should be red
git('checkout', '-q', '--detach', d_ok)
results.append(run('bad-order-rev-HEAD-good', f_bad))
# HEAD-dependence reversed: revision good, HEAD bad => counter should be green
git('checkout', '-q', '--detach', f_bad)
results.append(run('good-order-rev-HEAD-bad', d_ok))
# HEAD-dependence: revision c0 (no freeze, no dispatch) while HEAD good => should be red
git('checkout', '-q', '--detach', d_ok)
results.append(run('root-rev-HEAD-good', c0))

# (c1) ancestor by ancestry but later by committer time
at('late', c0)
f_late = commit('freeze-late', '2026-11-04T12:00:00Z', [(FREEZE, freeze_bytes)])
d_late = commit('dispatch-early', '2026-11-04T11:00:00Z', [(DISPATCH, b'dispatch\n')])
git('checkout', '-q', '--detach', d_late)
results.append(run('ancestor-but-later-time', d_late))

# same-second, correct order (back-to-back real commits, no explicit dates)
at('realtime', c0)
f_rt = commit('freeze-rt', None, [(FREEZE, freeze_bytes)])
d_rt = commit('dispatch-rt', None, [(DISPATCH, b'dispatch\n')])
ct = git('log', '-2', '--format=%ct', 'HEAD').stdout.split()
results.append({'name': 'realtime-order-committer-times', 'head': d_rt[:8],
                'rev': f'freeze_ct={ct[1]} dispatch_ct={ct[0]}', 'exit': None,
                'E_fails': None, 'summary': 'info'})
results.append(run('realtime-correct-order', d_rt))

# (c2) real rebase that keeps the order: force-rebase the ok branch onto c0 now
at('rb', d_ok)
p = subprocess.run(['git', '-C', str(E), 'rebase', '-q', '-f', c0], capture_output=True, text=True)
rb_tip = git('rev-parse', 'HEAD').stdout.strip()
ct2 = git('log', '-2', '--format=%ct', 'HEAD').stdout.split()
rb_log = git('log', '--format=%h %ct %s', '-3').stdout
results.append({'name': 'real-rebase-keeps-order-times', 'head': rb_tip[:8],
                'rev': f'rebase_rc={p.returncode} dispatch_ct={ct2[0]} freeze_ct={ct2[1]}',
                'exit': p.returncode, 'E_fails': None, 'summary': rb_log.replace('\n', ' | ')})
results.append(run('real-rebase-keeps-order', rb_tip))

# post-dispatch edit of the frozen counter (freeze content changed after dispatch)
at('edit', d_ok)
edited = freeze_bytes + b'# post-dispatch edit\n'
e_tip = commit('edit-frozen-counter', '2026-11-04T12:00:00Z', [(FREEZE, edited)])
results.append(run('post-dispatch-edit-of-frozen-counter', e_tip))

# freeze with the right first-add commit but a later amendment that is a DIFFERENT file,
# plus dispatch with multiple adds -> the first-add rule still reads fine
for r in results:
    print(json.dumps(r, sort_keys=True))
print('DONE', len(results))
