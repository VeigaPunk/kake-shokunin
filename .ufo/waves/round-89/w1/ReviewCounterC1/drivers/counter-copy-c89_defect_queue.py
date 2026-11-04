#!/usr/bin/env python3
"""Round 89 C1 — the six routed round-88 defects, decided over committed bytes.

Claim (frozen before data): calibration, the lane's lowest owned non-retired
axis (2, HOLD). Predicate: `open=0 closed=6 met=true`, exit 0 at the carrier;
at the base the same counter must print `open=6 closed=0 met=false`, exit 1.

Items, each re-derived from lane bytes:

  A-selftest-number   The prose count the lane states for `scripts/vary_match.py`'s
                      integrated selftest must equal the count the tool itself
                      prints when this counter runs it. A stale `22/22` line is
                      admissible only when the same line carries the
                      `[r89-correction` tag that explains the erratum.
  B-gate-sample       The admit/reject counts parsed from `## Gate` in the
                      round-88 lesson must equal the counts the round-89 lesson
                      states (`gate-sample:` and `r88-gate-summary-correction:`).
  C-receipt-pointers  Every `.ufo/waves/round-88/controls/...` path named in the
                      round-88 section of SCORECARD.md or in the round-88 lesson
                      must exist at the measured revision, and the unbacked
                      "re-run at edcb2980" claim must be resolved by a committed
                      receipt or an explicit retraction.
  D-revision-pinned-count  The `controls-count: N@<rev>` statement must equal a
                      recount at that revision.
  E-freeze-before-dispatch  The commit that first adds the round-89 C2 counter
                      must be an ancestor of the commit that first adds the wave
                      dispatch marker, and must carry an earlier committer time.
  F-lesson-shape      The round-89 lesson must carry a `## Mistakes` section with
                      the five-column table, and the round-88 lesson must point
                      its `## L1 mistakes` content at that section.

Modes: --revision reads the lane repo at a commit; --mirror reads a directory
tree (used by --selftest). No receipt of another claim is read.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = '76225160d0dff8d2042fbcd037bd08b0971d5e07'
SCORECARD = 'SCORECARD.md'
L88 = 'corpus/lessons/round-88.md'
L89 = 'corpus/lessons/round-89.md'
TOOL = 'scripts/vary_match.py'
FREEZE_PATH = '.ufo/waves/round-89/c89_key.py'
DISPATCH_PATH = '.ufo/waves/round-89/w1.ready'
ITEMS = ('A-selftest-number', 'B-gate-sample', 'C-receipt-pointers',
         'D-revision-pinned-count', 'E-freeze-before-dispatch', 'F-lesson-shape')
STALE = '22/22'
TAG = '[r89-correction'
CTRL_RE = re.compile(r'\.ufo/waves/round-88/controls/[A-Za-z0-9._/,{}-]+')


def git_bytes(root, rev, path):
    p = subprocess.run(['git', '-C', str(root), 'show', f'{rev}:{path}'], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def git_out(root, *args):
    p = subprocess.run(['git', '-C', str(root)] + list(args), capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


def expand_braces(token):
    m = re.search(r'\{([^{}]*)\}', token)
    if not m:
        return [token]
    out = []
    for alt in m.group(1).split(','):
        out.extend(expand_braces(token[:m.start()] + alt + token[m.end():]))
    return out


def marker(text, name):
    pat = re.compile(r'^' + re.escape(name) + r':[ \t]*(\S(?:.*\S)?)[ \t]*$', re.M)
    hits = pat.findall(text)
    return hits


def run_selftest(tool_bytes, work):
    work.mkdir(parents=True, exist_ok=True)
    path = work / 'vary_match.py'
    path.write_bytes(tool_bytes)
    try:
        p = subprocess.run([sys.executable, '-B', str(path), '--selftest'],
                           capture_output=True, text=True, timeout=120)
        return p
    finally:
        path.unlink(missing_ok=True)


def item_a(ctx):
    fails = []
    tool = ctx.read(TOOL)
    if tool is None:
        return ['tool missing']
    p = run_selftest(tool, ctx.work / 'a')
    m = re.search(r'selftest:\s*(\d+)/(\d+) passed', p.stdout)
    if p.returncode != 0 or not m:
        return [f'integrated selftest not green or unparseable (exit {p.returncode})']
    observed = f'{m.group(1)}/{m.group(2)}'
    card = ctx.read(SCORECARD)
    if card is None:
        return ['SCORECARD.md missing']
    stated = marker(card.decode('utf-8', 'replace'), 'integrated-selftest')
    if len(stated) != 1:
        fails.append(f'expected exactly one integrated-selftest marker, found {len(stated)}')
    elif stated[0] != observed:
        fails.append(f'integrated-selftest states {stated[0]}, tool prints {observed}')
    for name, scope in ((SCORECARD, '## Round 88'), (L88, None)):
        body = ctx.read(name)
        if body is None:
            fails.append(f'{name} missing')
            continue
        lines = body.decode('utf-8', 'replace').splitlines()
        if scope is not None:
            start = next((i for i, l in enumerate(lines) if l.startswith(scope)), None)
            if start is None:
                fails.append(f'{name} has no {scope} section')
                continue
            end = next((i for i in range(start + 1, len(lines))
                        if lines[i].startswith('## ')), len(lines))
            window = [(i, lines[i]) for i in range(start, end)]
        else:
            window = list(enumerate(lines))
        for i, line in window:
            if STALE in line and TAG not in line:
                fails.append(f'{name}:{i + 1} keeps the stale {STALE} claim without a '
                             f'{TAG}] tag')
    return fails


def item_b(ctx):
    fails = []
    body = ctx.read(L88)
    if body is None:
        return ['round-88 lesson missing']
    lines = body.decode('utf-8', 'replace').splitlines()
    try:
        start = lines.index('## Gate')
    except ValueError:
        return ['round-88 lesson has no ## Gate section']
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith('## '):
            end = i
            break
    admits = rejects = 0
    for line in lines[start:end]:
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 3:
            continue
        decision = cells[1] if len(cells) > 1 else ''
        if '**admit**' in decision:
            admits += 1
        elif '**reject**' in decision:
            rejects += 1
    lesson = ctx.read(L89)
    if lesson is None:
        return fails + ['round-89 lesson missing']
    text = lesson.decode('utf-8', 'replace')
    for name, want in (('gate-sample', f'admits={admits} rejects={rejects}'),
                       ('r88-gate-summary-correction', f'admits={admits} rejects={rejects}')):
        got = marker(text, name)
        if len(got) != 1:
            fails.append(f'expected exactly one {name} marker, found {len(got)}')
        elif got[0] != want:
            fails.append(f'{name} states {got[0]}, ## Gate parses {want}')
    if admits + rejects == 0:
        fails.append('## Gate parses no decisions')
    return fails


def item_c(ctx):
    fails = []
    card = ctx.read(SCORECARD)
    lesson = ctx.read(L88)
    if card is None or lesson is None:
        return ['SCORECARD.md or round-88 lesson missing']
    tokens = set()
    for body in (card, lesson):
        for raw in CTRL_RE.findall(body.decode('utf-8', 'replace')):
            token = raw.rstrip('.,;:')
            tokens.update(expand_braces(token))
    for token in sorted(tokens):
        if ctx.read(token) is None:
            fails.append(f'named receipt missing: {token}')
    l89 = ctx.read(L89)
    if l89 is None:
        return fails + ['round-89 lesson missing']
    got = marker(l89.decode('utf-8', 'replace'), 'r88-c-rerun')
    if len(got) != 1:
        fails.append(f'expected exactly one r88-c-rerun marker, found {len(got)}')
    else:
        value = got[0]
        if value.startswith('receipt='):
            path = value[len('receipt='):].strip()
            if ctx.read(path) is None:
                fails.append(f'r88-c-rerun names a receipt that does not exist: {path}')
        elif value != 'retracted':
            fails.append(f'r88-c-rerun must be receipt=<path> or retracted, got {value!r}')
    return fails


def count_controls(ctx, rev):
    if ctx.mirror is not None:
        root = ctx.mirror / '.ufo' / 'waves'
        return sum(1 for p in root.glob('*/controls/**/*') if p.is_file())
    out = git_out(ctx.root, 'ls-tree', '-r', '--name-only', rev)
    if out is None:
        return None
    return sum(1 for line in out.splitlines() if '/controls/' in line)


def item_d(ctx):
    fails = []
    l89 = ctx.read(L89)
    if l89 is None:
        return ['round-89 lesson missing']
    got = marker(l89.decode('utf-8', 'replace'), 'controls-count')
    if len(got) != 1:
        return [f'expected exactly one controls-count marker, found {len(got)}']
    m = re.fullmatch(r'(\d+)@([0-9a-f]{7,40})', got[0])
    if not m:
        return [f'controls-count marker malformed: {got[0]!r}']
    stated, rev = int(m.group(1)), m.group(2)
    actual = count_controls(ctx, rev)
    if actual is None:
        return [f'cannot recount at {rev}']
    if actual != stated:
        fails.append(f'controls-count states {stated}@{rev}, recount is {actual}')
    return fails


def item_e(ctx):
    if ctx.mirror is not None or ctx.root is None:
        return []
    fails = []
    def adding_commit(path):
        out = git_out(ctx.root, 'log', '--format=%H', '--diff-filter=A', '--', path)
        return out.splitlines()[-1] if out and out.strip() else None
    freeze = adding_commit(FREEZE_PATH)
    dispatch = adding_commit(DISPATCH_PATH)
    if not freeze:
        return [f'no commit adds {FREEZE_PATH}']
    if not dispatch:
        return [f'no commit adds {DISPATCH_PATH}']
    anc = subprocess.run(['git', '-C', str(ctx.root), 'merge-base', '--is-ancestor',
                          freeze, dispatch], capture_output=True)
    if anc.returncode != 0:
        fails.append(f'freeze {freeze[:8]} is not an ancestor of dispatch {dispatch[:8]}')
    def ct(rev):
        out = git_out(ctx.root, 'log', '-1', '--format=%ct', rev)
        return int(out.strip()) if out and out.strip() else None
    f_ct, d_ct = ct(freeze), ct(dispatch)
    if f_ct is None or d_ct is None:
        fails.append('cannot read committer times')
    elif not f_ct < d_ct:
        fails.append(f'freeze committer time {f_ct} is not earlier than dispatch {d_ct}')
    return fails


F_COLS = ('class', 'evidence', 'captured-by', 'fix', 'witness')


def item_f(ctx):
    fails = []
    l89 = ctx.read(L89)
    if l89 is None:
        return ['round-89 lesson missing']
    lines = l89.decode('utf-8', 'replace').splitlines()
    if '## Mistakes' not in lines:
        fails.append('round-89 lesson has no ## Mistakes heading')
    else:
        start = lines.index('## Mistakes')
        header = None
        rows = 0
        for line in lines[start + 1:]:
            if line.startswith('## '):
                break
            if not line.startswith('|'):
                continue
            cells = [c.strip().lower() for c in line.strip().strip('|').split('|')]
            if header is None and 'class' in cells[0]:
                header = cells
            elif header is not None and not set(''.join(cells)) <= set('-: '):
                rows += 1
        if header is None:
            fails.append('## Mistakes carries no table header')
        else:
            joined = ' | '.join(header)
            for col in F_COLS:
                if col not in joined:
                    fails.append(f'## Mistakes table lacks the {col!r} column')
        if rows < 1:
            fails.append('## Mistakes carries no data row')
    l88 = ctx.read(L88)
    if l88 is None:
        fails.append('round-88 lesson missing')
    else:
        if not any(TAG in l and 'L1 mistakes' in l
                   for l in l88.decode('utf-8', 'replace').splitlines()):
            fails.append('round-88 lesson carries no tagged pointer from ## L1 mistakes '
                         'to ## Mistakes')
    return fails


class Ctx:
    def __init__(self, read, work, root=None, rev=None, mirror=None):
        self.read, self.work, self.root, self.rev, self.mirror = read, work, root, rev, mirror


def evaluate(ctx):
    return {'A-selftest-number': item_a(ctx),
            'B-gate-sample': item_b(ctx),
            'C-receipt-pointers': item_c(ctx),
            'D-revision-pinned-count': item_d(ctx),
            'E-freeze-before-dispatch': item_e(ctx),
            'F-lesson-shape': item_f(ctx)}


# ---------------------------------------------------------------- selftest

def _tool_text():
    p = subprocess.run(['git', '-C', str(HERE.parents[2]), 'show', f'{BASE}:{TOOL}'],
                       capture_output=True)
    if p.returncode != 0:
        raise SystemExit('cannot read the base tool from git')
    return p.stdout


def green_tree(root, count=3):
    """A mirror that closes all six items, built from the frozen base bytes."""
    tool = _tool_text()
    with tempfile.TemporaryDirectory(prefix='kake-r89-tool-') as td:
        path = Path(td) / 'vary_match.py'
        path.write_bytes(tool)
        out = subprocess.run([sys.executable, '-B', str(path), '--selftest'],
                             capture_output=True).stdout
    m = re.search(rb'selftest:\s*(\d+)/(\d+) passed', out)
    observed = f'{m.group(1).decode()}/{m.group(2).decode()}'
    card = (root / SCORECARD)
    card.parent.mkdir(parents=True, exist_ok=True)
    card.write_text(
        '# kake-shokunin — Scorecard\n\n'
        '| Axis | Score | Evidence pointer | Last change |\n|---|---|---|---|\n'
        '| calibration | 2 | selftest receipt | 89 |\n\n'
        '## Round 88 — bounded committed measurements\n\n'
        'The round-88 section states the integrated tool selftest as '
        f'{observed}.\n\n'
        '## Round 89 — routed-defect closure\n\n'
        f'integrated-selftest: {observed}\n\n'
        f'The round-88 statement {STALE} {TAG} 89] was stale; the receipt prints '
        f'{observed}.\n')
    l88 = root / L88
    l88.parent.mkdir(parents=True, exist_ok=True)
    l88.write_text(
        '# Round 88 — lesson\n\n'
        '## Gate\n\n'
        '| Candidate | Decision | URL | Reason |\n|---|---|---|---|\n'
        '| one | **admit**, tier A | u | r |\n'
        '| two | **admit**, tier A | u | r |\n'
        '| three | **reject** (proposition) | u | r |\n'
        '| four | **reject** (proposition) | u | r |\n\n'
        '## L1 mistakes\n\n'
        '| Class | Evidence |\n|---|---|\n| x | y |\n\n'
        f'{TAG} 89] The four mistakes above live under `## L1 mistakes`; round 89 '
        'carries them as `## Mistakes` in corpus/lessons/round-89.md.\n\n'
        'Integrated tool selftests: `vary_match` 22/22 [r89-correction: receipt prints '
        f'{observed}].\n\n'
        'Receipts: `.ufo/waves/round-88/controls/{base-c1.txt,after-c1-carrier.txt}`.\n')
    (root / 'scripts').mkdir(parents=True, exist_ok=True)
    (root / TOOL).write_bytes(tool)
    (root / '.ufo/waves/round-88/controls').mkdir(parents=True, exist_ok=True)
    for name in ('base-c1.txt', 'after-c1-carrier.txt'):
        (root / '.ufo/waves/round-88/controls' / name).write_text('receipt\n')
    for i in range(count):
        (root / '.ufo/waves/round-88/controls' / f'extra{i}.txt').write_text('x\n')
    l89 = root / L89
    l89.parent.mkdir(parents=True, exist_ok=True)
    l89.write_text(
        '# Round 89 — lesson\n\n'
        'gate-sample: admits=2 rejects=2\n'
        'r88-gate-summary-correction: admits=2 rejects=2\n'
        'r88-c-rerun: retracted\n'
        f'controls-count: {count_controls(Ctx(None, None, mirror=root), None)}@{"0" * 40}\n\n'
        '## Mistakes\n\n'
        '| Class | Evidence pointer | Captured-by | Fix | Witness |\n|---|---|---|---|---|\n'
        '| text drift | a | b | c | d |\n')


def selftest():
    checks = []

    def record(label, ok):
        checks.append((label, bool(ok)))

    with tempfile.TemporaryDirectory(prefix='kake-r89-c1-selftest-') as d:
        d = Path(d)

        def reader(root):
            def read(path):
                p = root / path
                return p.read_bytes() if p.is_file() else None
            return read

        def ctx_for(root):
            return Ctx(reader(root), d / 'work', mirror=root)

        green = d / 'green'
        green_tree(green)
        res = evaluate(ctx_for(green))
        record('green tree closes all six', not any(res.values()))

        def mutant(name, mutate):
            m = d / name
            green_tree(m)
            mutate(m)
            return evaluate(ctx_for(m))

        def stale_back(m):
            p = m / SCORECARD
            p.write_text(p.read_text().replace('integrated-selftest: ',
                                               'integrated-selftest: 0/1 # '))
        r = mutant('stale-count', stale_back)
        record('mutant: wrong integrated-selftest count reopens A',
               bool(r['A-selftest-number']) and not r['B-gate-sample'])

        def untagged_stale(m):
            p = m / L88
            p.write_text(p.read_text().replace(' [r89-correction: receipt prints',
                                               ' (receipt prints'))
        r = mutant('untagged-stale', untagged_stale)
        record('mutant: untagged stale 22/22 reopens A', bool(r['A-selftest-number']))

        def gate_flip(m):
            p = m / L88
            p.write_text(p.read_text().replace('| four | **reject**', '| four | **admit**'))
        r = mutant('gate-flip', gate_flip)
        record('mutant: Gate table edit reopens B',
               bool(r['B-gate-sample']) and not r['A-selftest-number'])

        def missing_receipt(m):
            (m / '.ufo/waves/round-88/controls/base-c1.txt').unlink()
        r = mutant('missing-receipt', missing_receipt)
        record('mutant: a named receipt removed reopens C', bool(r['C-receipt-pointers']))

        def unbacked_rerun(m):
            p = m / L89
            p.write_text(p.read_text().replace('r88-c-rerun: retracted',
                                               'r88-c-rerun: receipt=.ufo/waves/round-88/controls/nope.txt'))
        r = mutant('unbacked-rerun', unbacked_rerun)
        record('mutant: r88-c-rerun pointing at a missing receipt reopens C',
               bool(r['C-receipt-pointers']))

        def count_off(m):
            p = m / L89
            text = p.read_text()
            real = count_controls(Ctx(None, None, mirror=m), None)
            p.write_text(re.sub(r'controls-count: \d+@', f'controls-count: {real + 5}@', text))
        r = mutant('count-off', count_off)
        record('mutant: wrong controls-count reopens D', bool(r['D-revision-pinned-count']))

        def no_mistakes(m):
            p = m / L89
            p.write_text(p.read_text().replace('## Mistakes', '## Notes'))
        r = mutant('no-mistakes', no_mistakes)
        record('mutant: missing ## Mistakes reopens F', bool(r['F-lesson-shape']))

        def no_crossref(m):
            p = m / L88
            p.write_text(p.read_text().replace(
                'The four mistakes above live under `## L1 mistakes`',
                'The four mistakes above are elsewhere'))
        r = mutant('no-crossref', no_crossref)
        record('mutant: untagged round-88 pointer reopens F', bool(r['F-lesson-shape']))

        # E needs a git fixture: freeze commit must precede the dispatch commit.
        def git_repo(name, order):
            repo = d / name
            repo.mkdir()
            subprocess.run(['git', '-C', str(repo), 'init', '-q'], check=True)
            subprocess.run(['git', '-C', str(repo), 'config', 'user.email', 't@t'], check=True)
            subprocess.run(['git', '-C', str(repo), 'config', 'user.name', 't'], check=True)
            assert subprocess.run(['git', '-C', str(repo), 'rev-parse', '--show-toplevel'],
                                  capture_output=True, text=True).stdout.strip() == str(repo)
            for i, step in enumerate(order):
                p = repo / step
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('x\n')
                subprocess.run(['git', '-C', str(repo), 'add', step], check=True)
                stamp = f'2026-11-04T1{i}:00:00+00:00'
                env = dict(os.environ, GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp)
                subprocess.run(['git', '-C', str(repo), 'commit', '-qm', step],
                               check=True, env=env)
            return repo

        ok_repo = git_repo('order-ok', [FREEZE_PATH, DISPATCH_PATH])
        e = item_e(Ctx(reader(ok_repo), d / 'work', root=ok_repo))
        record('E passes when the freeze commit precedes dispatch', not e)

        bad_repo = git_repo('order-bad', [DISPATCH_PATH, FREEZE_PATH])
        e = item_e(Ctx(reader(bad_repo), d / 'work', root=bad_repo))
        record('E fails when dispatch is committed first', bool(e))

        same_repo = d / 'order-same'
        same_repo.mkdir()
        subprocess.run(['git', '-C', str(same_repo), 'init', '-q'], check=True)
        subprocess.run(['git', '-C', str(same_repo), 'config', 'user.email', 't@t'], check=True)
        subprocess.run(['git', '-C', str(same_repo), 'config', 'user.name', 't'], check=True)
        for step in (FREEZE_PATH, DISPATCH_PATH):
            p = same_repo / step
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('x\n')
        subprocess.run(['git', '-C', str(same_repo), 'add', '-A'], check=True)
        subprocess.run(['git', '-C', str(same_repo), 'commit', '-qm', 'both'], check=True)
        e = item_e(Ctx(reader(same_repo), d / 'work', root=same_repo))
        record('E fails when freeze and dispatch share one commit', bool(e))

    passed = sum(1 for _, ok in checks if ok)
    for label, ok in checks:
        print(('PASS ' if ok else 'FAIL ') + label)
    print(f'selftest: {passed}/{len(checks)} passed')
    return 0 if passed == len(checks) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path)
    ap.add_argument('--revision')
    ap.add_argument('--mirror', type=Path)
    ap.add_argument('--work', type=Path)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.work:
        ap.error('--work required')
    if a.mirror:
        rev = f'mirror:{a.mirror}'
        read = lambda p: (a.mirror / p).read_bytes() if (a.mirror / p).is_file() else None
        ctx = Ctx(read, a.work, mirror=a.mirror)
    else:
        if not a.root or not a.revision:
            ap.error('--root and --revision required (or --mirror)')
        rev = subprocess.check_output(['git', '-C', str(a.root), 'rev-parse',
                                       f'{a.revision}^{{commit}}'], text=True).strip()
        read = lambda p: git_bytes(a.root, rev, p)
        ctx = Ctx(read, a.work, root=a.root, rev=rev)
    result = evaluate(ctx)
    open_items = [k for k, v in result.items() if v]
    met = not open_items
    print(f'C1v1 revision={rev} items={len(ITEMS)} open={len(open_items)} '
          f'closed={len(ITEMS) - len(open_items)} met={str(met).lower()}')
    print(json.dumps(result, sort_keys=True))
    return 0 if met else 1


if __name__ == '__main__':
    raise SystemExit(main())
