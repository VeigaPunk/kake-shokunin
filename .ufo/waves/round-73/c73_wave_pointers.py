#!/usr/bin/env python3
"""Round-73 C1 counter: wave-relative receipt pointers in LOG.md/SCORECARD.md.

Frozen predicate (round-73 contract, section C1):

    C1 met iff unannotated == 0
              and dead >= 2
              and the append-only conjunct holds
                  (every base line of LOG.md and of SCORECARD.md survives as a
                   line-prefix of the same file at the measured revision).

Procedure at the measured revision (files read with
``git show --end-of-options <rev>:<file>``):

  * LOG.md: the section that starts at the first line beginning with
    ``## Round 72 `` and ends before the next line beginning with ``## ``.
  * SCORECARD.md: every line whose first table cell is 72 (regex
    ``^\\| 72 \\|``), over the whole file at the revision.

Tokens: every match of ``(controls|sources|w1)/[A-Za-z0-9._/-]+`` in those
lines, deduplicated by exact token text with first-occurrence order.  Each
token is resolved under ``.ufo/waves/round-72/`` by
``git cat-file -e <rev>:<path>``; a token whose object does not resolve is
``dead``.

Annotation classification -- the exact rule for "names a corrected path"
-----------------------------------------------------------------------
Let T be a dead token and let F be a file (LOG.md or SCORECARD.md) that cites
T in the population above.  Let ``tail(F)`` be the lines of F at the measured
revision whose 1-based number is greater than ``len(base lines of F)``, where
the base revision is the frozen round-73 base
``c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`` (a constant of this counter; the
frozen counting command takes no base override).

T is annotated iff at least one line L of some ``tail(F)`` satisfies both:

  (1) L names T exactly.  An occurrence of T counts when the character before
      it is not ``[A-Za-z0-9._-]`` and the character after it is not
      ``[A-Za-z0-9._/-]`` (or either side is the line boundary).  A preceding
      ``/`` is therefore allowed, so a full
      ``.ufo/waves/round-72/.../T`` spelling also names T, while a longer
      token such as ``controls/x.txt.bak`` or ``xcontrols/x.txt`` does not.

  (2) The same line L names at least one corrected repo path C that resolves.
      Candidates on L are every match of
      ``\\.ufo/waves/round-72/[A-Za-z0-9._/-]+`` (full repo path) and every
      match of the token regex above (wave-relative path).  Each candidate is
      tried as written and, if it ends in ``.``, with exactly one trailing
      period removed (sentence punctuation).  The candidate is normalized with
      ``posixpath.normpath`` and must remain strictly below
      ``.ufo/waves/round-72/`` (no escape, not the wave directory itself);
      it must differ from T; and ``git cat-file -e <rev>:C`` must exit 0.
      Any object that cat-file resolves -- blob or tree -- counts, which is
      the frozen ``git cat-file -e`` wording.

No other relation between L and T is required or inferred: the correction
does not have to repeat the citing line, and the token and the corrected path
do not need a syntactic arrow.  A tail line that names T but no resolving
candidate path (a bare errata) does not annotate T.  A resolving path alone,
without T on the same line, does not annotate T either.

Output (first line, exact):

    C1v1 revision=<rev> pointers=<n> dead=<d> annotated=<a> \
unannotated=<u> append_only=<true|false> met=<bool>

Detail lines follow for each dead token and for each file that failed the
append-only conjunct.  Exit 0 met, 1 not met, 2 unevaluable (repository,
revision, file or section cannot be read), 64 usage.  Selftest cases are
function-level and are documented at ``run_selftest``.
"""

import argparse
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile

BASE_REVISION = 'c1f3d8d4ed9470ecbaaf3353952a374b079e68cc'
WAVE_DIR = '.ufo/waves/round-72'
LOG_FILE = 'LOG.md'
SCORECARD_FILE = 'SCORECARD.md'

LOG_SECTION_PREFIX = '## Round 72 '
HEADING_PREFIX = '## '
SCORECARD_ROW = re.compile(r'^\| 72 \|')
TOKEN_PATTERN = re.compile(r'(controls|sources|w1)/[A-Za-z0-9._/-]+')
FULL_PATH_PATTERN = re.compile(
    r'\.ufo/waves/round-72/[A-Za-z0-9._/-]+')

EXIT_MET = 0
EXIT_UNMET = 1
EXIT_UNEVALUABLE = 2
EXIT_USAGE = 64


class Unevaluable(Exception):
    """The measurement cannot be made at the requested revision."""


def git(root, args):
    """Run one git command in list form (no shell, no interpolation)."""
    return subprocess.run(['git', '-C', root, *args], capture_output=True)


def split_lines(text):
    """Split file text into lines without inventing a trailing empty line."""
    if text == '':
        return []
    if text.endswith('\n'):
        text = text[:-1]
    return text.split('\n')


def read_text(root, revision, path):
    process = git(root, ['show', '--end-of-options', revision + ':' + path])
    if process.returncode != 0:
        detail = process.stderr.decode('utf-8', 'replace').strip()
        raise Unevaluable('cannot read %s at %s: %s'
                          % (path, revision, detail or 'git show failed'))
    return process.stdout.decode('utf-8', 'replace')


def cat_file_exists(root, revision, path):
    process = git(root, ['cat-file', '-e', '--end-of-options',
                         revision + ':' + path])
    return process.returncode == 0


def check_repository(root, revision):
    probe = git(root, ['rev-parse', '--git-dir'])
    if probe.returncode != 0:
        detail = probe.stderr.decode('utf-8', 'replace').strip()
        raise Unevaluable('not a git repository (%s): %s'
                          % (root, detail or 'git rev-parse failed'))
    verify = git(root, ['rev-parse', '--verify', '--quiet', '--end-of-options',
                        revision + '^{commit}'])
    if verify.returncode != 0:
        raise Unevaluable('revision does not resolve to a commit: %s' % revision)


def log_section_indices(lines):
    """Indices of the '## Round 72 ' section (start inclusive, next '## ' exclusive)."""
    start = None
    for index, line in enumerate(lines):
        if line.startswith(LOG_SECTION_PREFIX):
            start = index
            break
    if start is None:
        raise Unevaluable('LOG.md has no line beginning with %r'
                          % LOG_SECTION_PREFIX)
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith(HEADING_PREFIX):
            end = index
            break
    return range(start, end)


def add_citation(citations, token, filename, number):
    citations.setdefault(token, {}).setdefault(filename, number)


def collect_citations(log_lines, scorecard_lines):
    """Return {token: {file: first 1-based line number}} in first-seen order."""
    citations = {}
    for index in log_section_indices(log_lines):
        for match in TOKEN_PATTERN.finditer(log_lines[index]):
            add_citation(citations, match.group(0), LOG_FILE, index + 1)
    for index, line in enumerate(scorecard_lines):
        if SCORECARD_ROW.match(line):
            for match in TOKEN_PATTERN.finditer(line):
                add_citation(citations, match.group(0), SCORECARD_FILE, index + 1)
    return citations


def resolves_relative(root, revision, token):
    """True iff token resolves under the round-72 wave directory.

    ``posixpath.normpath`` rejects a spelling that escapes the wave directory;
    such a spelling is not a pointer *under* the wave directory and is dead.
    """
    normalized = posixpath.normpath(token)
    if (normalized in ('', '.', '..') or normalized.startswith('../')
            or posixpath.isabs(normalized)):
        return False
    return cat_file_exists(root, revision, WAVE_DIR + '/' + normalized)


def is_prefix(base_lines, tip_lines):
    return (len(tip_lines) >= len(base_lines)
            and tip_lines[:len(base_lines)] == base_lines)


def names_token(line, token, pattern_cache):
    if token not in pattern_cache:
        pattern_cache[token] = re.compile(
            r'(?<![A-Za-z0-9._-])' + re.escape(token)
            + r'(?![A-Za-z0-9._/-])')
    return pattern_cache[token].search(line) is not None


def candidate_forms(raw):
    """Candidate spellings of one path occurrence (trailing-period tolerant)."""
    forms = [raw]
    if raw.endswith('.'):
        forms.append(raw.rstrip('.'))
    return forms


def corrected_paths(root, revision, line, dead_token):
    """Resolving corrected repo paths named on one tail line.

    Returns full, normalized repo paths (``.ufo/waves/round-72/...``).
    """
    seen = set()
    found = []
    raws = []
    for match in FULL_PATH_PATTERN.finditer(line):
        raws.append(match.group(0))
    for match in TOKEN_PATTERN.finditer(line):
        raws.append(match.group(0))
    for raw in raws:
        for form in candidate_forms(raw):
            if not form or form in seen:
                continue
            seen.add(form)
            if form.startswith(WAVE_DIR + '/'):
                normalized = posixpath.normpath(form)
                if (not normalized.startswith(WAVE_DIR + '/')
                        or normalized == WAVE_DIR + '/' + dead_token):
                    continue
                if cat_file_exists(root, revision, normalized):
                    found.append(normalized)
            elif posixpath.isabs(form):
                continue
            else:
                normalized = posixpath.normpath(form)
                if (normalized in ('', '.', '..')
                        or normalized.startswith('../')
                        or normalized == dead_token):
                    continue
                full = WAVE_DIR + '/' + normalized
                if cat_file_exists(root, revision, full):
                    found.append(full)
    # Preserve order while removing duplicates produced by overlapping matches.
    unique = []
    for path in found:
        if path not in unique:
            unique.append(path)
    return unique


def tail_lines(base_text, tip_text):
    """Lines of the measured file after the base line count, 1-based numbered."""
    base_count = len(split_lines(base_text))
    tip = split_lines(tip_text)
    return [(number + 1, tip[number]) for number in range(base_count, len(tip))]


def measure(root, revision, base):
    """Return the C1 measurement dictionary for one revision."""
    check_repository(root, revision)
    check_repository(root, base)

    log_base = read_text(root, base, LOG_FILE)
    log_tip = read_text(root, revision, LOG_FILE)
    scorecard_base = read_text(root, base, SCORECARD_FILE)
    scorecard_tip = read_text(root, revision, SCORECARD_FILE)

    citations = collect_citations(split_lines(log_tip), split_lines(scorecard_tip))
    tails = {
        LOG_FILE: tail_lines(log_base, log_tip),
        SCORECARD_FILE: tail_lines(scorecard_base, scorecard_tip),
    }
    prefix_ok = {
        LOG_FILE: is_prefix(split_lines(log_base), split_lines(log_tip)),
        SCORECARD_FILE: is_prefix(split_lines(scorecard_base),
                                  split_lines(scorecard_tip)),
    }

    pattern_cache = {}
    dead_tokens = []
    annotated = {}
    unannotated = []
    for token in citations:
        if resolves_relative(root, revision, token):
            continue
        dead_tokens.append(token)
        hit = None
        for filename in (LOG_FILE, SCORECARD_FILE):
            if filename not in citations[token]:
                continue
            for number, line in tails[filename]:
                if not names_token(line, token, pattern_cache):
                    continue
                corrected = corrected_paths(root, revision, line, token)
                if corrected:
                    hit = (filename, number, corrected)
                    break
            if hit is not None:
                break
        if hit is None:
            unannotated.append(token)
        else:
            annotated[token] = hit

    append_only = prefix_ok[LOG_FILE] and prefix_ok[SCORECARD_FILE]
    met = (not unannotated) and len(dead_tokens) >= 2 and append_only
    return {
        'revision': revision,
        'pointers': len(citations),
        'dead': len(dead_tokens),
        'annotated': len(annotated),
        'unannotated': len(unannotated),
        'append_only': append_only,
        'annotation_met': not unannotated,
        'met': met,
        'dead_tokens': dead_tokens,
        'annotated_detail': annotated,
        'citations': citations,
        'prefix_ok': prefix_ok,
        'exit_code': EXIT_MET if met else EXIT_UNMET,
    }


def bool_word(value):
    return 'true' if value else 'false'


def print_summary(measurement):
    print('C1v1 revision=%s pointers=%d dead=%d annotated=%d unannotated=%d '
          'append_only=%s met=%s'
          % (measurement['revision'], measurement['pointers'],
             measurement['dead'], measurement['annotated'],
             measurement['unannotated'],
             bool_word(measurement['append_only']),
             bool_word(measurement['met'])))
    for token in measurement['dead_tokens']:
        if token in measurement['annotated_detail']:
            filename, number, corrected = measurement['annotated_detail'][token]
            print('dead annotated file=%s line=%d token=%s corrected=%s'
                  % (filename, number, token, ','.join(corrected)))
        else:
            cited = ','.join(
                '%s:%d' % (name, number)
                for name, number in sorted(
                    measurement['citations'][token].items()))
            print('dead unannotated citations=%s token=%s' % (cited, token))
    for filename in (LOG_FILE, SCORECARD_FILE):
        if not measurement['prefix_ok'][filename]:
            print('append_only false file=%s' % filename)


def write_fixture(repo, relpath, content):
    path = os.path.join(repo, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as handle:
        handle.write(content)


def commit_fixture(repo, message):
    added = git(repo, ['add', '-A'])
    if added.returncode != 0:
        raise RuntimeError('fixture git add failed: %s'
                           % added.stderr.decode('utf-8', 'replace').strip())
    committed = git(repo, ['-c', 'user.name=kake-scratch',
                           '-c', 'user.email=kake@scratch.local',
                           'commit', '-q', '-m', message])
    if committed.returncode != 0:
        raise RuntimeError('fixture git commit failed: %s'
                           % committed.stderr.decode('utf-8', 'replace').strip())
    head = git(repo, ['rev-parse', 'HEAD'])
    if head.returncode != 0:
        raise RuntimeError('fixture git rev-parse failed')
    return head.stdout.decode('ascii').strip()


def new_fixture(work):
    repo = tempfile.mkdtemp(dir=work, prefix='c73fx.')
    created = git(repo, ['init', '-q'])
    if created.returncode != 0:
        shutil.rmtree(repo, ignore_errors=True)
        raise RuntimeError('fixture git init failed')
    toplevel = git(repo, ['rev-parse', '--show-toplevel'])
    top = toplevel.stdout.decode('utf-8', 'replace').strip()
    if (toplevel.returncode != 0
            or os.path.realpath(top) != os.path.realpath(repo)):
        shutil.rmtree(repo, ignore_errors=True)
        raise RuntimeError('fixture toplevel %r is not %r' % (top, repo))
    return repo


def fixture_log(tokens, prior='# LOG fixture'):
    lines = [prior, '', '## Round 71 - fixture', '',
             '- prior round line']
    if tokens:
        lines += ['', '## Round 72 - fixture', '',
                  '- receipts: ' + ', '.join('`%s`' % token for token in tokens)]
    else:
        lines += ['', '## Round 72 - fixture', '', '- no pointers here']
    return '\n'.join(lines) + '\n'


def fixture_scorecard(token):
    evidence = '`%s`' % token if token else 'no pointer'
    return ('# SCORECARD fixture\n\n'
            '| Round | Axis | Evidence |\n'
            '|---|---|---|\n'
            '| 72 | fixture | %s |\n' % evidence)


def make_base(repo, dead_tokens, resolving=('controls/fixture-a.txt',)):
    for relative in resolving:
        write_fixture(repo, WAVE_DIR + '/' + relative, 'fixture\n')
    write_fixture(repo, LOG_FILE, fixture_log(dead_tokens))
    write_fixture(repo, SCORECARD_FILE, fixture_scorecard(resolving[0]))


def check_case(label, expectation, measurement, wanted):
    problems = []
    for key, want in wanted.items():
        got = measurement[key]
        if got != want:
            problems.append('%s=%r != %r' % (key, got, want))
    summary = ('dead=%d annotated=%d unannotated=%d append_only=%s '
               'annotation=%s met=%s'
               % (measurement['dead'], measurement['annotated'],
                  measurement['unannotated'],
                  bool_word(measurement['append_only']),
                  'met' if measurement['annotation_met'] else 'not-met',
                  bool_word(measurement['met'])))
    if problems:
        print('case %s FAIL: %s [%s]' % (label, '; '.join(problems), summary))
        return False
    print('case %s ok: expect=%s %s' % (label, expectation, summary))
    return True


def run_selftest(work):
    """Six function-level fixtures in scratch repositories.

    The frozen predicate adds ``dead >= 2`` on top of the annotation and
    append-only conjuncts.  A fixture that exercises *classification* is graded
    on the conjunct under test, exactly as the seat list describes it:
    ``no_dead`` and ``dead_correct_tail`` expect the annotation criterion to be
    met, ``dead_no_tail`` and ``dead_bare_errata`` expect it to fail, and
    ``base_line_edited`` expects append_only=false.  Because dead=0 or dead=1
    can never satisfy the frozen ``dead >= 2`` gate, the sixth fixture
    ``dead_two_annotated`` exercises that gate and the full predicate, and is
    the case whose full C1 verdict is true.
    """
    created_work = False
    if work is None:
        work = tempfile.mkdtemp(prefix='c73-selftest.')
        created_work = True
    else:
        os.makedirs(work, exist_ok=True)
    passed = 0
    total = 6
    try:
        # 1. No dead pointer: every cited token resolves.
        repo = new_fixture(work)
        try:
            make_base(repo, ['controls/fixture-a.txt'])
            revision = commit_fixture(repo, 'fixture 1')
            measurement = measure(repo, revision, revision)
            passed += check_case(
                'no_dead', 'annotation-met', measurement,
                {'dead': 0, 'annotated': 0, 'unannotated': 0,
                 'append_only': True, 'annotation_met': True})
        finally:
            shutil.rmtree(repo, ignore_errors=True)

        # 2. A dead pointer with no appended tail line.
        repo = new_fixture(work)
        try:
            make_base(repo, ['controls/missing-two.txt'])
            revision = commit_fixture(repo, 'fixture 2')
            measurement = measure(repo, revision, revision)
            passed += check_case(
                'dead_no_tail', 'annotation-not-met', measurement,
                {'dead': 1, 'annotated': 0, 'unannotated': 1,
                 'append_only': True, 'annotation_met': False,
                 'met': False})
        finally:
            shutil.rmtree(repo, ignore_errors=True)

        # 3. A bare errata: names the token, names no resolving path.
        repo = new_fixture(work)
        try:
            make_base(repo, ['controls/missing-three.txt'])
            base = commit_fixture(repo, 'fixture 3 base')
            with open(os.path.join(repo, LOG_FILE), 'a', encoding='utf-8') as handle:
                handle.write('\n## Round 73 - errata\n\n'
                             '- `controls/missing-three.txt` remains a historical '
                             'record; no corrected path is named here.\n')
            revision = commit_fixture(repo, 'fixture 3 errata')
            measurement = measure(repo, revision, base)
            passed += check_case(
                'dead_bare_errata', 'annotation-not-met', measurement,
                {'dead': 1, 'annotated': 0, 'unannotated': 1,
                 'append_only': True, 'annotation_met': False,
                 'met': False})
        finally:
            shutil.rmtree(repo, ignore_errors=True)

        # 4. A dead pointer with a correct tail: exact token plus a resolving
        #    corrected path on the same appended line.  dead=1, so the frozen
        #    dead>=2 gate keeps the full predicate false by construction.
        repo = new_fixture(work)
        try:
            make_base(repo, ['controls/missing-four.txt'])
            base = commit_fixture(repo, 'fixture 4 base')
            with open(os.path.join(repo, LOG_FILE), 'a', encoding='utf-8') as handle:
                handle.write('\n## Round 73 - correction\n\n'
                             '- `controls/missing-four.txt` superseded by '
                             '`controls/fixture-a.txt` at this revision.\n')
            revision = commit_fixture(repo, 'fixture 4 correction')
            measurement = measure(repo, revision, base)
            passed += check_case(
                'dead_correct_tail', 'annotation-met', measurement,
                {'dead': 1, 'annotated': 1, 'unannotated': 0,
                 'append_only': True, 'annotation_met': True,
                 'met': False})
        finally:
            shutil.rmtree(repo, ignore_errors=True)

        # 5. A base line edited: the append-only conjunct fails even though the
        #    dead token is corrected in the tail.
        repo = new_fixture(work)
        try:
            make_base(repo, ['controls/missing-five.txt'])
            base = commit_fixture(repo, 'fixture 5 base')
            write_fixture(repo, LOG_FILE,
                          fixture_log(['controls/missing-five.txt'],
                                      prior='# LOG fixture (edited)'))
            with open(os.path.join(repo, LOG_FILE), 'a', encoding='utf-8') as handle:
                handle.write('\n## Round 73 - correction\n\n'
                             '- `controls/missing-five.txt` superseded by '
                             '`controls/fixture-a.txt`.\n')
            revision = commit_fixture(repo, 'fixture 5 edited')
            measurement = measure(repo, revision, base)
            passed += check_case(
                'base_line_edited', 'append-only-false', measurement,
                {'dead': 1, 'annotated': 1, 'unannotated': 0,
                 'append_only': False, 'annotation_met': True,
                 'met': False})
        finally:
            shutil.rmtree(repo, ignore_errors=True)

        # 6. Two dead pointers, both annotated: the frozen dead>=2 gate and the
        #    whole C1 predicate are satisfied (met=true, exit 0).
        repo = new_fixture(work)
        try:
            make_base(repo, ['controls/missing-six-a.txt',
                             'controls/missing-six-b.txt'],
                      resolving=('controls/fixture-a.txt',
                                 'controls/fixture-b.txt'))
            base = commit_fixture(repo, 'fixture 6 base')
            with open(os.path.join(repo, LOG_FILE), 'a', encoding='utf-8') as handle:
                handle.write('\n## Round 73 - correction\n\n'
                             '- `controls/missing-six-a.txt` superseded by '
                             '`controls/fixture-a.txt`; '
                             '`controls/missing-six-b.txt` superseded by '
                             '`controls/fixture-b.txt`.\n')
            revision = commit_fixture(repo, 'fixture 6 correction')
            measurement = measure(repo, revision, base)
            passed += check_case(
                'dead_two_annotated', 'met', measurement,
                {'dead': 2, 'annotated': 2, 'unannotated': 0,
                 'append_only': True, 'annotation_met': True,
                 'met': True, 'exit_code': EXIT_MET})
        finally:
            shutil.rmtree(repo, ignore_errors=True)
    finally:
        if created_work:
            shutil.rmtree(work, ignore_errors=True)
    print('selftest %d/%d' % (passed, total))
    return EXIT_MET if passed == total else EXIT_UNMET


class UsageParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(EXIT_USAGE, '%s: error: %s\n' % (self.prog, message))


def main(argv=None):
    parser = UsageParser(
        description='Round-73 C1 wave-relative pointer counter.')
    parser.add_argument('--root', help='lane repository root')
    parser.add_argument('--revision', help='measured revision')
    parser.add_argument('--selftest', action='store_true',
                        help='run the six function-level fixture cases')
    parser.add_argument('--work', help='directory for fixture repositories '
                                       '(default: TMPDIR)')
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            if args.root or args.revision:
                parser.error('--selftest does not take --root/--revision')
            return run_selftest(args.work)
        if not args.root or not args.revision:
            parser.error('--root and --revision are required')
        measurement = measure(args.root, args.revision, BASE_REVISION)
        print_summary(measurement)
        return measurement['exit_code']
    except Unevaluable as exc:
        print('error: %s' % exc, file=sys.stderr)
        return EXIT_UNEVALUABLE
    except (OSError, RuntimeError) as exc:
        print('error: %s' % exc, file=sys.stderr)
        return EXIT_UNEVALUABLE


if __name__ == '__main__':
    sys.exit(main())
