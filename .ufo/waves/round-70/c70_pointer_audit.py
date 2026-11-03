#!/usr/bin/env python3
"""Round-70 C1 counter (v2, Amendment 1): SCORECARD evidence pointers.

Frozen predicate (round-70 contract C1, as amended by Amendment 1 before any
after-state measurement): C1 is met iff

    python3 -B .ufo/waves/round-70/c70_pointer_audit.py \
        --root <lane> --revision <tip> --base <base>

prints ``unannotated=0 append_only=true`` and exits 0.  Without ``--base`` the
append-only conjunct is not evaluated and the summary omits it.

Population (Amendment 1 regexes, deduplicated by token, first occurrence wins):
  repo  (?:^|[`(>|\\s])((?:\\.ufo|corpus|scripts|handoffs|considerthese)/[A-Za-z0-9_./-]+\\.[A-Za-z0-9]{1,16})(?![A-Za-z0-9])
  home  (?:^|[`(>|\\s])(~/[A-Za-z0-9_./+-]+)
  tmp   (?:^|[`(>|\\s])(/tmp/[A-Za-z0-9_.+-]+)

Amendment 1 term refinements (all recorded before any after-state):
  - repo extension cap raised 7 -> 16 and a right boundary added, so
    ``.SHA256SUMS`` is extracted whole instead of truncating to a phantom
    ``.SHA256S`` dangling token (ReviewerPredicates, live false positive);
  - a repo token dangles iff BOTH the literal token and its os.path.normpath
    form fail ``git cat-file -e`` (the ``scripts/../`` spelling of a real file
    resolves; ReviewerPredicates);
  - home/tmp dangling uses os.path.exists (``test -e`` semantics), not
    os.path.lexists (SentinelAdoption: a broken symlink is not a resolving
    pointer);
  - a home token whose expansion escapes $HOME is excluded from the
    population (SentinelAdoption: the counter must not use host paths outside
    the home tree as an existence oracle);
  - the annotation locus is a markdown table row of the
    ``## Pointer calibration (round 70)`` section outside fenced code blocks
    (MutC1Counter F7 / SentinelAdoption: a fenced line is not a table row);
  - the selftest's dangling tmp token is minted under TMPDIR/gettempdir(),
    never a literal /tmp (round-69 QUALITY criterion);
  - ``--base`` adds the append-only conjunct: every base line of SCORECARD.md
    survives unchanged at the tip (base is a line-prefix of the tip), so
    rewriting a dangling token into a non-matching spelling cannot pass.

Exit 0 iff unannotated == 0 (and append-only holds when --base is given),
1 otherwise, 2 on usage or IO faults.  Every git invocation is list-form
subprocess with no shell and no token interpolation into a shell.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid

SECTION = '## Pointer calibration (round 70)'

CLASSES = (
    ('repo', re.compile(
        r'(?:^|[`(>|\s])((?:\.ufo|corpus|scripts|handoffs|considerthese)/'
        r'[A-Za-z0-9_./-]+\.[A-Za-z0-9]{1,16})(?![A-Za-z0-9])')),
    ('home', re.compile(r'(?:^|[`(>|\s])(~/[A-Za-z0-9_./+-]+)')),
    ('tmp', re.compile(r'(?:^|[`(>|\s])(/tmp/[A-Za-z0-9_.+-]+)')),
)

HEADING = re.compile(r'^#{1,2}\s')
FENCE = re.compile(r'^(```|~~~)')


def git(root, args):
    """Run one git command in list form (never a shell)."""
    return subprocess.run(['git', '-C', root, *args], capture_output=True)


def read_scorecard(root, revision):
    probe = git(root, ['rev-parse', '--git-dir'])
    if probe.returncode != 0:
        raise OSError('not a git repository: %s' % root)
    check = git(root, ['rev-parse', '--verify', '--quiet', revision + '^{commit}'])
    if check.returncode != 0:
        raise OSError('revision does not resolve: %s' % revision)
    show = git(root, ['show', revision + ':SCORECARD.md'])
    if show.returncode != 0:
        raise OSError('SCORECARD.md is not readable at revision %s' % revision)
    return show.stdout.decode('utf-8', 'replace')


def extract_tokens(text):
    """Map every pointer token to (class, first 1-based line number)."""
    found = {}
    excluded = []
    home_root = os.path.normpath(os.path.expanduser('~'))
    for number, line in enumerate(text.splitlines(), 1):
        for cls, pattern in CLASSES:
            for match in pattern.finditer(line):
                token = match.group(1)
                if token in found:
                    continue
                if cls == 'home':
                    expanded = os.path.normpath(os.path.expanduser(token))
                    if expanded != home_root and not expanded.startswith(
                            home_root + os.sep):
                        excluded.append('home excluded line=%d token=%s '
                                        '(escapes $HOME)' % (number, token))
                        continue
                found[token] = (cls, number)
    return found, excluded


def is_dangling(root, revision, token, cls):
    if cls == 'repo':
        probe = git(root, ['cat-file', '-e', revision + ':' + token])
        if probe.returncode == 0:
            return False
        normalized = os.path.normpath(token)
        if normalized == token:
            return True
        probe = git(root, ['cat-file', '-e', revision + ':' + normalized])
        return probe.returncode != 0
    path = os.path.expanduser(token) if cls == 'home' else token
    return not os.path.exists(path)


def strip_comments(lines):
    """Yield each line with HTML comments removed, carrying state across lines."""
    in_comment = False
    for line in lines:
        out = []
        index = 0
        while index < len(line):
            if in_comment:
                end = line.find('-->', index)
                if end < 0:
                    index = len(line)
                else:
                    in_comment = False
                    index = end + 3
            else:
                start = line.find('<!--', index)
                if start < 0:
                    out.append(line[index:])
                    index = len(line)
                else:
                    out.append(line[index:start])
                    in_comment = True
                    index = start + 4
        yield ''.join(out)


def annotation_cells(text):
    """First cells of table rows in the round-70 calibration section.

    A row is a line starting (after at most three spaces) with a pipe, outside
    fenced code blocks and outside HTML comments.
    """
    lines = list(strip_comments(text.splitlines()))
    start = None
    for index, line in enumerate(lines):
        if line.strip() == SECTION:
            start = index + 1
            break
    if start is None:
        return set()
    cells = set()
    fenced = False
    for line in lines[start:]:
        stripped = line.strip()
        if FENCE.match(stripped):
            fenced = not fenced
            continue
        if fenced:
            continue
        if HEADING.match(stripped):
            break
        if not stripped.startswith('|'):
            continue
        cell = stripped[1:].split('|', 1)[0].strip()
        if cell:
            cells.add(cell)
    return cells


def append_only(root, base, revision):
    """True iff the base SCORECARD is a line-prefix of the tip SCORECARD."""
    base_text = read_scorecard(root, base)
    tip_text = read_scorecard(root, revision)
    base_lines = base_text.splitlines()
    tip_lines = tip_text.splitlines()
    if len(tip_lines) < len(base_lines):
        return False
    return tip_lines[:len(base_lines)] == base_lines


def audit(root, revision, base=None):
    text = read_scorecard(root, revision)
    found, excluded = extract_tokens(text)
    cells = annotation_cells(text)
    dangling = 0
    annotated = 0
    unannotated = 0
    details = list(excluded)
    for token, (cls, line) in found.items():
        if not is_dangling(root, revision, token, cls):
            continue
        dangling += 1
        if token in cells:
            annotated += 1
            status = 'annotated'
        else:
            unannotated += 1
            status = 'unannotated'
        details.append('%s %s line=%d token=%s' % (cls, status, line, token))
    pure = None
    if base is not None:
        pure = append_only(root, base, revision)
    met = unannotated == 0 and pure is not False
    summary = ('pointers=%d dangling=%d annotated=%d unannotated=%d'
               % (len(found), dangling, annotated, unannotated))
    if pure is not None:
        summary += ' append_only=%s' % ('true' if pure else 'false')
    summary += ' met=%s' % ('true' if met else 'false')
    print(summary)
    for detail in details:
        print(detail)
    return 0 if met else 1


def write_fixture(repo, relpath, content):
    path = os.path.join(repo, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as handle:
        handle.write(content)


def commit_fixture(repo, message):
    added = subprocess.run(['git', '-C', repo, 'add', '-A'], capture_output=True)
    if added.returncode != 0:
        raise RuntimeError('fixture git add failed: %s'
                           % added.stderr.decode('utf-8', 'replace').strip())
    committed = subprocess.run(
        ['git', '-C', repo, '-c', 'user.name=fx', '-c', 'user.email=fx@fixture',
         'commit', '-q', '-m', message], capture_output=True)
    if committed.returncode != 0:
        raise RuntimeError('fixture git commit failed: %s'
                           % committed.stderr.decode('utf-8', 'replace').strip())
    head = subprocess.run(['git', '-C', repo, 'rev-parse', 'HEAD'], capture_output=True)
    if head.returncode != 0:
        raise RuntimeError('fixture git rev-parse failed')
    return head.stdout.decode('ascii').strip()


def fresh_tmp_token(prefix):
    root = os.environ.get('TMPDIR') or tempfile.gettempdir()
    while True:
        token = os.path.join(root, '%s-%s' % (prefix, uuid.uuid4().hex))
        if not os.path.exists(token):
            return token


def invoke(root, revision, base=None):
    argv = [sys.executable, '-B', os.path.abspath(__file__),
            '--root', root, '--revision', revision]
    if base is not None:
        argv += ['--base', base]
    process = subprocess.run(argv, capture_output=True, text=True)
    lines = process.stdout.splitlines()
    summary = lines[0] if lines else ''
    return process.returncode, summary, lines, process.stderr


def check_case(label, root, revision, want_exit, want_summary, want_line=None,
               base=None):
    code, summary, lines, errors = invoke(root, revision, base)
    problems = []
    if code != want_exit:
        problems.append('exit %d != %d' % (code, want_exit))
    if summary != want_summary:
        problems.append('summary %r != %r' % (summary, want_summary))
    if errors.strip():
        problems.append('stderr %r' % errors.strip())
    if want_line is not None and want_line not in lines[1:]:
        problems.append('missing detail line %r' % want_line)
    return label, problems, summary


def run_selftest(work):
    if not os.path.isdir(work):
        raise OSError('--work is not a directory: %s' % work)
    repo = tempfile.mkdtemp(dir=work, prefix='c70fx.')
    try:
        created = subprocess.run(['git', '-C', repo, 'init', '-q'], capture_output=True)
        if created.returncode != 0:
            raise RuntimeError('fixture git init failed')
        toplevel = subprocess.run(['git', '-C', repo, 'rev-parse', '--show-toplevel'],
                                  capture_output=True)
        top = toplevel.stdout.decode('utf-8', 'replace').strip()
        if toplevel.returncode != 0 or os.path.realpath(top) != os.path.realpath(repo):
            raise RuntimeError('fixture toplevel %r is not %r' % (top, repo))

        results = []

        # (a) resolving repo pointer: counted, not dangling.
        write_fixture(repo, 'corpus/fixture-a.md', 'fixture a\n')
        write_fixture(repo, 'SCORECARD.md',
                      '# SCORECARD\n\n'
                      'Evidence: `corpus/fixture-a.md` resolves at this revision.\n')
        revision = commit_fixture(repo, 'case a')
        results.append(check_case(
            'a', repo, revision, 0,
            'pointers=1 dangling=0 annotated=0 unannotated=0 met=true'))

        # (b) dangling repo pointer with no annotation section.
        write_fixture(repo, 'SCORECARD.md',
                      '# SCORECARD\n\n'
                      'Evidence: `corpus/missing-b.md` is gone.\n')
        revision = commit_fixture(repo, 'case b')
        results.append(check_case(
            'b', repo, revision, 1,
            'pointers=1 dangling=1 annotated=0 unannotated=1 met=false'))

        # (c) dangling tmp pointer annotated by an exact-token row.
        token_c = fresh_tmp_token('c70-c')
        write_fixture(repo, 'SCORECARD.md',
                      '# SCORECARD\n\n'
                      'Evidence: `%s` was removed by scratch cleanup.\n\n'
                      '%s\n\n'
                      '| %s | scratch-discipline cleanup | historical; not executable |\n'
                      % (token_c, SECTION, token_c))
        revision = commit_fixture(repo, 'case c')
        results.append(check_case(
            'c', repo, revision, 0,
            'pointers=1 dangling=1 annotated=1 unannotated=0 met=true'))

        # (d) row whose first cell is a strict prefix of the dangling token
        #     annotates only itself; the full token stays unannotated.
        token_d = fresh_tmp_token('c70-d')
        prefix_d = token_d[:-4]
        write_fixture(repo, 'SCORECARD.md',
                      '# SCORECARD\n\n'
                      'Evidence: `%s` was removed by scratch cleanup.\n\n'
                      '%s\n\n'
                      '| %s | scratch-discipline cleanup | historical; not executable |\n'
                      % (token_d, SECTION, prefix_d))
        revision = commit_fixture(repo, 'case d')
        results.append(check_case(
            'd', repo, revision, 1,
            'pointers=2 dangling=2 annotated=1 unannotated=1 met=false',
            'tmp unannotated line=3 token=%s' % token_d))

        # (e) no pointers at all.
        write_fixture(repo, 'SCORECARD.md',
                      '# SCORECARD\n\n'
                      'No path-like evidence pointer appears in this fixture.\n')
        revision = commit_fixture(repo, 'case e')
        results.append(check_case(
            'e', repo, revision, 0,
            'pointers=0 dangling=0 annotated=0 unannotated=0 met=true'))

        # (f) Amendment 1: a table row inside a fenced code block is not a
        #     table row; the dangling token stays unannotated.
        token_f = fresh_tmp_token('c70-f')
        write_fixture(repo, 'SCORECARD.md',
                      '# SCORECARD\n\n'
                      'Evidence: `%s` was removed by scratch cleanup.\n\n'
                      '%s\n\n'
                      '```\n'
                      '| %s | scratch-discipline cleanup | fenced; not a row |\n'
                      '```\n'
                      % (token_f, SECTION, token_f))
        revision = commit_fixture(repo, 'case f')
        results.append(check_case(
            'f', repo, revision, 1,
            'pointers=1 dangling=1 annotated=0 unannotated=1 met=false'))

        # (g) Amendment 1: a broken symlink is not a resolving pointer
        #     (os.path.exists, test -e semantics).
        token_g = fresh_tmp_token('c70-g')
        os.symlink(os.path.join(work, 'c70-no-such-target'), token_g)
        write_fixture(repo, 'SCORECARD.md',
                      '# SCORECARD\n\n'
                      'Evidence: `%s` is a dangling symlink.\n' % token_g)
        revision = commit_fixture(repo, 'case g')
        results.append(check_case(
            'g', repo, revision, 1,
            'pointers=1 dangling=1 annotated=0 unannotated=1 met=false'))
        os.unlink(token_g)

        # (h) Amendment 1: a home token escaping $HOME is excluded from the
        #     population (no host oracle outside the home tree).
        outside = os.path.join(tempfile.gettempdir(), 'c70-outside-%s' % uuid.uuid4().hex)
        with open(outside, 'w', encoding='utf-8') as handle:
            handle.write('outside\n')
        write_fixture(repo, 'SCORECARD.md',
                      '# SCORECARD\n\n'
                      'Evidence: `~/../../%s` names a path outside $HOME.\n'
                      % os.path.relpath(outside, os.path.expanduser('~')))
        revision = commit_fixture(repo, 'case h')
        results.append(check_case(
            'h', repo, revision, 0,
            'pointers=0 dangling=0 annotated=0 unannotated=0 met=true'))
        os.unlink(outside)

        passed = 0
        for label, problems, summary in results:
            if problems:
                print('case %s FAIL: %s [%s]' % (label, '; '.join(problems), summary))
            else:
                passed += 1
                print('case %s ok: %s' % (label, summary))
        print('selftest %d/8' % passed)
        return 0 if passed == 8 else 1
    finally:
        shutil.rmtree(repo, ignore_errors=True)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Round-70 C1 SCORECARD pointer counter (v2).')
    parser.add_argument('--root', help='lane repository root')
    parser.add_argument('--revision', help='measured revision')
    parser.add_argument('--base', help='base revision for the append-only conjunct')
    parser.add_argument('--selftest', action='store_true',
                        help='run the eight fixture cases')
    parser.add_argument('--work', help='directory for fixture repositories')
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            if args.root or args.revision or args.base:
                parser.error('--selftest does not take --root/--revision/--base')
            if not args.work:
                parser.error('--selftest requires --work <dir>')
            return run_selftest(args.work)
        if not args.root or not args.revision:
            parser.error('--root and --revision are required')
        return audit(args.root, args.revision, args.base)
    except (OSError, RuntimeError) as exc:
        print('error: %s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
