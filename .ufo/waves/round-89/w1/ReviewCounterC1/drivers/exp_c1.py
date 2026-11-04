import json, os, re, subprocess, sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/kake-r89/ReviewCounterC1')
G = S / 'g-git'
CTR = S / 'counters' / 'c89_defect_queue.py'
RC = S / 'receipts'
RC.mkdir(exist_ok=True)
TOOL = (S / 'tool_base.py').read_bytes()
L88, L89, CARD = 'corpus/lessons/round-88.md', 'corpus/lessons/round-89.md', 'SCORECARD.md'
FAKE99 = b"print('selftest: 99/99 passed')\n"


def git(*a, env=None, check=True):
    p = subprocess.run(['git', '-C', str(G), *a], capture_output=True, text=True, env=env)
    if check and p.returncode != 0:
        raise SystemExit(f'git {a} failed: {p.stderr}')
    return p


def assert_repo():
    top = git('rev-parse', '--show-toplevel').stdout.strip()
    assert top == str(G), top


def show(path, rev='green'):
    return git('show', f'{rev}:{path}').stdout


def run_counter(name, rev, root=G, extra=()):
    work = S / 'w' / name
    cmd = ['python3', '-B', str(CTR), '--root', str(root), '--revision', rev,
           '--work', str(work), *extra]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(S))
    out = p.stdout + (('stderr: ' + p.stderr) if p.stderr.strip() else '')
    rec = RC / f'{name}.txt'
    rec.write_text('$ ' + ' '.join(cmd) + f'\n# exit={p.returncode}\n' + out)
    head = p.stdout.splitlines()[0] if p.stdout else '(no stdout)'
    items = json.loads(p.stdout.splitlines()[1]) if len(p.stdout.splitlines()) > 1 else {}
    return p.returncode, head, {k: v for k, v in items.items() if v}


def experiment(name, edits, expect, predicted_note, tool=None):
    assert_repo()
    git('checkout', '-q', '-B', f'exp/{name}', 'green')
    for path, text in edits.items():
        f = G / path
        if text is None:
            f.unlink(missing_ok=True)
        else:
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(text if isinstance(text, bytes) else text.encode())
    git('add', '-A')
    env = dict(os.environ, GIT_AUTHOR_DATE='2026-11-04T13:00:00Z',
               GIT_COMMITTER_DATE='2026-11-04T13:00:00Z')
    git('commit', '-qm', name, env=env)
    rev = git('rev-parse', 'HEAD').stdout.strip()
    rc, head, fails = run_counter(name, rev)
    git('checkout', '-q', '--detach', 'green')
    return {'name': name, 'rev': rev, 'exit': rc, 'head': head, 'open_items': sorted(fails),
            'expect': expect, 'predicted': predicted_note}


def sub(text, pat, rep, count=1):
    new, n = re.subn(pat, rep, text, count=count)
    assert n >= 1, f'pattern not found: {pat}'
    return new


def edit_text(path, fn):
    return fn(show(path))


results = []

# ---- A: selftest number
results.append(experiment(
    'A1-tagged-stale-stands',
    {L88: edit_text(L88, lambda t: sub(t, r'receipt prints 35/35\]', 'stands]'))},
    'red: a 22/22 claim tagged [r89-correction but not stating the corrected count stays in force',
    'green (tag substring is the only test)'))

results.append(experiment(
    'A2-untagged-stale-round89-scorecard',
    {CARD: show(CARD) + '\nThe integrated tool selftest is 22/22.\n'},
    'red: untagged 22/22 claim in the round-89 section of SCORECARD.md',
    'green (A scans only the ## Round 88 section of SCORECARD.md)'))

results.append(experiment(
    'A3-untagged-stale-round89-lesson',
    {L89: show(L89) + '\nIntegrated tool selftest: 22/22.\n'},
    'red: untagged stale 22/22 in corpus/lessons/round-89.md',
    'green (A never reads round-89 lesson)'))

results.append(experiment(
    'A4-selftest-self-report-99',
    {'scripts/vary_match.py': FAKE99,
     CARD: edit_text(CARD, lambda t: sub(sub(sub(t, r'integrated-selftest: 35/35', 'integrated-selftest: 99/99'),
                                              r'as 35/35', 'as 99/99'), r'receipt prints 35/35', 'receipt prints 99/99')),
     L88: edit_text(L88, lambda t: sub(t, r'receipt prints 35/35', 'receipt prints 99/99'))},
    'red-or-judged: a 1-line tool that prints a fabricated count and exits 0 closes A (A trusts self-report)',
    'green (A never checks the tool performs any check)'))

# ---- B: gate counts
results.append(experiment(
    'B1-honest-reject-mentions-admit',
    {L88: edit_text(L88, lambda t: sub(t, r'\| four \| \*\*reject\*\* \(proposition\)',
                                        '| four | **reject** (not **admit**)'))},
    'green: four is still a reject, markers admits=2 rejects=2 are true',
    'red (parser counts a reject whose decision cell contains **admit** as an admit)'))

results.append(experiment(
    'B2-parser-matched-markers-false-counts',
    {L88: edit_text(L88, lambda t: sub(t, r'\| four \| \*\*reject\*\* \(proposition\)',
                                        '| four | **reject** (not **admit**)')),
     L89: edit_text(L89, lambda t: sub(sub(t, r'gate-sample: admits=2 rejects=2', 'gate-sample: admits=3 rejects=1'),
                                        r'r88-gate-summary-correction: admits=2 rejects=2',
                                        'r88-gate-summary-correction: admits=3 rejects=1'))},
    'red: truthful Gate table is 2 admit / 2 reject, but markers now state the parser error 3/1',
    'green (B checks markers against the same wrong parse)'))

# ---- C: receipt pointers
results.append(experiment(
    'C1-trailing-char-truncates-receipt',
    {L88: show(L88) + '\nAlso named: `.ufo/waves/round-88/controls/base-c1.txt+missing`.\n'},
    'red: the named receipt base-c1.txt+missing does not exist',
    'green (regex stops at +; the truncated base-c1.txt exists)'))

results.append(experiment(
    'C2-unbacked-claim-left-in-force',
    {L88: show(L88) + '\nA re-run at edcb2980 reproduces the round-88 selftest.\n'},
    'red: the unbacked edcb2980 re-run claim is still asserted in the round-88 lesson while round 89 writes retracted',
    'green (item C reads only the r88-c-rerun marker, never the claim text)'))

results.append(experiment(
    'C3-rerun-receipt-is-existing-lesson',
    {L89: edit_text(L89, lambda t: sub(t, r'r88-c-rerun: retracted', 'r88-c-rerun: receipt=corpus/lessons/round-88.md'))},
    'red: a lesson file is not a re-run receipt (the pointer only needs existence)',
    'green (ctx.read only checks existence)'))

results.append(experiment(
    'C4-rerun-receipt-is-directory-git',
    {L89: edit_text(L89, lambda t: sub(t, r'r88-c-rerun: retracted', 'r88-c-rerun: receipt=.ufo/waves/round-88/controls/'))},
    'red: a directory is not a receipt',
    'green in git mode (git show of a tree returns a listing, not None)'))

results.append(experiment(
    'C5-false-red-plus-in-real-receipt',
    {'.ufo/waves/round-88/controls/after+c1.txt': 'real receipt\n',
     L88: show(L88) + '\nReceipt: `.ufo/waves/round-88/controls/after+c1.txt`.\n'},
    'green: the receipt exists under its own name and is named exactly',
    'red (regex truncates the name at + and checks the nonexistent after)'))

results.append(experiment(
    'C6-short-form-receipt-missing',
    {CARD: show(CARD) + '\nSee `controls/integrated-selftest.txt` for the round-88 selftest.\n'},
    'red: controls/integrated-selftest.txt is named and does not exist under round-88/controls',
    'green (short-form names lack the full .ufo/waves prefix that CTRL_RE requires)'))

# ---- F: lesson shape
results.append(experiment(
    'F1-header-substring-fix-in-prefix',
    {L89: edit_text(L89, lambda t: sub(t, r'\| Class \| Evidence pointer \| Captured-by \| Fix \| Witness \|',
                                        '| Class | Evidence pointer | Captured-by | Prefix | Witness |'))},
    'red: the table has no Fix column',
    'green (F checks the substring fix, which matches Prefix)'))

results.append(experiment(
    'F2-honest-captured-by-space',
    {L89: edit_text(L89, lambda t: sub(t, r'Captured-by', 'Captured by'))},
    'green: the column is present under a spacing variant',
    'red (F checks the literal string captured-by)'))

results.append(experiment(
    'F3-tagged-pointer-not-pointing',
    {L88: edit_text(L88, lambda t: sub(t, r'\[r89-correction 89\] The four mistakes above live under `## L1 mistakes`; round 89 carries them as `## Mistakes` in corpus/lessons/round-89.md\.',
                                        '[r89-correction 89] The four mistakes above stay under `## L1 mistakes`; nothing moved.'))},
    'red: the tagged line does not point the L1 mistakes content at ## Mistakes',
    'green (F needs only one line carrying the tag and the phrase L1 mistakes)'))

# ---- sanity: green tree and a plain wrong D marker
results.append(experiment(
    'D1-sanity-wrong-count',
    {L89: edit_text(L89, lambda t: sub(t, r'controls-count: 5@', 'controls-count: 9@'))},
    'red: count 9 does not equal recount 5',
    'red (expected; control)'))

for r in results:
    print(json.dumps(r, sort_keys=True))
print('DONE', len(results))
