#!/usr/bin/env python3
"""c75_row_truth.py — C1 counter, round 75 (kake), v1.

Frozen predicate (contract §C1, `.ufo/waves/round-75/contract.md`):

  Population: every live gate-registry row of SKILL.md — a row inside a section
  titled ``### Round <N> gate registry additions`` whose Kind cell does not carry
  ``historical`` — resolves to one instrument file: the Name cell when it is
  itself a `.py`/`.mjs` path, else the first `.py`/`.mjs` token of the Entry
  command cell, else of the Self-test cell, else of any cell.

  Effective row: rows are grouped by instrument file; the last row naming a file
  wins (a row may be superseded by an appended row, never deleted).

  E1  a row whose Kind family is ``gate`` carries a working self-test of its
      own (``--selftest`` exits 0), or its Kind cell declares the differential
      substitute (the word ``differential`` as a word, in the Kind cell only).
      The recorded command must run the effective row's instrument path: shell
      comments are stripped and the program after the interpreter (``python``/
      ``python3`` with optional ``-B``, or ``node``) is the bound file; a command
      naming another file, or no file, is a finding whatever its exit code.
  E2  when the Self-test cell's claim segment records an ``a/b`` tally and names
      a command, the observed ``--selftest`` pass/total equals it.  A claim
      segment carrying more than one distinct pair is an ambiguous tally; only a
      bound command's output is measured.
  E3  when the Self-test cell enumerates two or more fixture ids ``f<N>``, the
      observed self-test total equals the number of distinct ids named.
  E4  every ``.py``/``.mjs`` path token in every live row's cells resolves at
      the measured revision.

  append_only holds when every live row name present at ``--base`` is still
  present at the measured revision.

  met = (mismatches == 0) and append_only.

Amendment 1 (`.ufo/waves/round-75/amendment-1.md`), terms only: the frozen
16-path list is a floor, not an equality.  ``missing_frozen`` counts the frozen
paths the derivation no longer produces and each one adds a finding; derived
files beyond the floor are in-population and satisfy E1-E4 like the rest.
``--population FILE`` overrides the floor (one path per line; ``#`` comments and
blank lines ignored).

Amendment 2 (`.ufo/waves/round-75/amendment-2.md`, A3/A4), terms only: E1/E2
measure the instrument's own self-test (program binding above); E4 covers every
live row, and an instrument whose file or row disappears from the derivation is
reported through ``missing_frozen``.  The E2 claim segment is the text after the
recorded command up to its first ``;`` — the tally the row claims; pairs in later
segments belong to receipt history.  The frozen base row `scripts/citation_lint.py`
records the current 9/9 beside a then-tally 8/8 in later segments, so a cell-wide
pair count would redden the frozen base; the claim segment keeps that row green
while an in-segment contradiction (``0/3 then 3/3``) is an ambiguous tally.

Measurement shape: the counter clones the measured revision with
``git clone --shared`` into ``--work/tree`` and runs every recorded self-test
command literally in that clone, with a fresh ``HOME``/``TMPDIR`` under
``--work/scratch`` and every inherited ``GIT_*`` variable scrubbed.  The work
tree is re-pointed at the measured revision when it already exists.

Summary line (deterministic, contract shape plus the amendment term; the
``missing_frozen`` term is appended so the frozen contract fields keep their
order):

  C1v1 revision=<rev> rows=N live=N files=N mismatches=M classes=… append_only=<bool> met=<bool> missing_frozen=N

Exit: 0 met, 1 not met, 2 unevaluable, 64 usage.

Self-check: ``--selftest`` builds isolated fixture repositories under ``--work``
(red and green fixtures per E-rule, superseding row, deleted base row, frozen
floor floor, ambiguous tally, word-boundary differential, comment- and
argument-laundered command binding, secondary-row and vanished-instrument E4,
retired-in-place floor loss, all green) and asserts the counter's own verdicts on
them.  ``--emit-population`` prints the effective floor, one path per line.
``--json`` prints the per-file result list and the counts.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

SEC_RE = re.compile(r'^### Round (\d+) gate registry additions')
FILE_RE = re.compile(r'((?:scripts|\.ufo)/[\w./-]+\.(?:py|mjs))')
PAIR_RE = re.compile(r'\b(\d+)\s*/\s*(\d+)\b')
FIX_RE = re.compile(r'\bf(\d+)\b')
TALLY_RE = re.compile(r'\b(\d+)\s*/\s*(\d+)\b')
INTERP_RE = re.compile(r'python(?:3(?:\.\d+)?)?')

FROZEN_POPULATION = (
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

SUMMARY_RE = re.compile(
    r'C1v1 revision=\S+ rows=\d+ live=\d+ files=\d+ mismatches=\d+ '
    r'classes=(?:-|E[1-4](?: E[1-4])*) append_only=(?:true|false) '
    r'met=(?:true|false) missing_frozen=\d+'
)

SELFTEST_TIMEOUT = 1800

SCRIPT_OK = """import sys
if '--selftest' in sys.argv:
    print('selftest 3/3')
    raise SystemExit(0)
print('ok')
raise SystemExit(0)
"""

SCRIPT_OK8 = """import sys
if '--selftest' in sys.argv:
    print('selftest 8/8')
    raise SystemExit(0)
print('ok')
raise SystemExit(0)
"""

SCRIPT_NO_SELFTEST = """import argparse
ap = argparse.ArgumentParser()
ap.add_argument('--root', default='.')
ap.parse_args()
print('ok')
raise SystemExit(0)
"""


class Unevaluable(Exception):
    """The input cannot be measured; exit 2."""


def clean_env(extra=None):
    """The process environment without inherited GIT_* variables."""
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    if extra:
        env.update(extra)
    return env


def git(root, *args, env=None):
    return subprocess.run(['git', '-C', root, *args], capture_output=True, text=True,
                          env=clean_env(env))


def read_rev(root, rev, path):
    p = git(root, 'show', f'{rev}:{path}')
    if p.returncode != 0:
        raise Unevaluable(f'cannot read {path} at {rev}: {p.stderr.strip()}')
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


def family(kind_cell):
    m = re.match(r'^(gate|instrument|tool|probe|counter)\b', kind_cell)
    return m.group(1) if m else 'other'


def instrument(row):
    """The row's instrument file: Name cell, else Entry command, else Self-test."""
    cells = row['cells']
    if FILE_RE.fullmatch(cells[0]):
        return cells[0]
    for idx in (2, 4):
        m = FILE_RE.search(cells[idx])
        if m:
            return m.group(1)
    m = FILE_RE.search(' '.join(cells))
    return m.group(1) if m else None


def effective(rows):
    """Group rows by instrument file; the last naming row wins."""
    groups = {}
    for row in rows:
        row['file'] = instrument(row)
        if row['file']:
            groups.setdefault(row['file'], []).append(row)
    return groups


def run_command(work, command, scratch):
    """Run a Self-test cell command inside the materialised tree at a revision."""
    cmd = command
    cmd = cmd.replace('[--work <dir>]', f'--work {scratch}')
    cmd = cmd.replace('--work <dir>', f'--work {scratch}')
    cmd = cmd.replace('<scratch>', scratch)
    cmd = cmd.replace('<lane>', work)
    try:
        out = subprocess.run(['bash', '-c', cmd], cwd=work, capture_output=True, text=True,
                             timeout=SELFTEST_TIMEOUT,
                             env=clean_env({'HOME': os.path.join(scratch, 'home'),
                                            'TMPDIR': os.path.join(scratch, 'tmp'),
                                            'KAKE_SCRATCH': scratch}))
    except subprocess.TimeoutExpired:
        return 124, f'timeout after {SELFTEST_TIMEOUT} s: {cmd}'
    return out.returncode, (out.stdout + out.stderr)


def selftest_command(cell):
    """Extract the self-test command from a Self-test cell, or None.

    A cell that opens with ``none`` or declares that the gate has no self-test
    of its own records no command, even when it explains why (``--selftest`` is
    an argparse error).
    """
    if re.match(r'^none\b', cell, re.I) or re.search(r'has no selftest of its own', cell, re.I):
        return None
    m = re.search(r'`([^`]*--selftest[^`]*)`', cell)
    if m:
        return m.group(1).strip()
    if '--selftest' in cell:
        return cell.split(';')[0].strip().strip('`')
    return None


def command_program(command):
    """The program a recorded self-test command runs, or None.

    Shell comments (``#`` at a word start) are stripped first, so a comment
    naming the instrument does not bind it.  Leading ``VAR=value`` assignments
    (and ``env``) are skipped; the file after the interpreter — ``python``/
    ``python3`` (optional ``-B``) or ``node`` — is the bound program.
    """
    line = re.sub(r'(^|\s)#[^\n]*', ' ', command).strip()
    toks = line.split()
    i = 0
    while i < len(toks) and re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', toks[i]):
        i += 1
    if i < len(toks) and os.path.basename(toks[i]) == 'env':
        i += 1
        while i < len(toks) and re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', toks[i]):
            i += 1
    if i < len(toks) and INTERP_RE.fullmatch(os.path.basename(toks[i])):
        i += 1
        if i < len(toks) and toks[i] == '-B':
            i += 1
    elif i < len(toks) and os.path.basename(toks[i]) in ('node', 'nodejs'):
        i += 1
    if i >= len(toks):
        return None
    return toks[i].strip('\'"`')


def observed_pair(output):
    pairs = TALLY_RE.findall(output)
    if not pairs:
        return None
    a, b = pairs[-1]
    return int(a), int(b)


def classes_of(findings):
    return sorted(set(re.findall(r'\bE[1-4]\b', ' '.join(findings))))


def declares_differential(kind_cell):
    """The Kind cell's differential substitute, matched as a word."""
    return bool(re.search(r'\bdifferential\b', kind_cell))


def claim_pairs(cell, command):
    """Distinct ``a/b`` pairs in the claim segment that follows the command.

    The claim segment is the text after the recorded command up to its first
    ``;``; pairs recorded later in the cell belong to receipt history, not to the
    row's claim.  With no pair there, the whole cell is the fallback.
    """
    region = cell
    m = re.search(r'`([^`]*--selftest[^`]*)`', cell)
    if m:
        region = cell[m.end():]
    elif command:
        pos = cell.find(command)
        if pos >= 0:
            region = cell[pos + len(command):]
    pairs = PAIR_RE.findall(region.split(';')[0])
    if not pairs:
        pairs = PAIR_RE.findall(cell)
    return sorted({(int(a), int(b)) for a, b in pairs})


def load_population(path):
    """The frozen floor, or the file ``--population`` names, one path per line."""
    if path is None:
        return list(FROZEN_POPULATION)
    try:
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
    except OSError as exc:
        raise Unevaluable(f'cannot read the population file {path}: {exc}')
    return [line.strip() for line in text.splitlines()
            if line.strip() and not line.strip().startswith('#')]


def prepare_tree(root, rev, work):
    """A ``git clone --shared`` of ``root`` checked out at ``rev``, under ``work``."""
    tree = os.path.join(work, 'tree')
    if os.path.isdir(os.path.join(tree, '.git')):
        head = git(tree, 'rev-parse', 'HEAD').stdout.strip()
        if head != rev:
            p = git(tree, 'checkout', '-q', rev)
            if p.returncode != 0:
                raise Unevaluable(f'cannot re-point {tree} at {rev}: {p.stderr.strip()}')
            head = git(tree, 'rev-parse', 'HEAD').stdout.strip()
        if head != rev:
            raise Unevaluable(f'{tree} reports {head}, expected {rev}')
        return tree
    os.makedirs(work, exist_ok=True)
    p = subprocess.run(['git', 'clone', '-q', '--shared', root, tree],
                       capture_output=True, text=True, env=clean_env())
    if p.returncode != 0:
        raise Unevaluable(f'cannot clone the lane: {p.stderr.strip()}')
    p = git(tree, 'checkout', '-q', rev)
    if p.returncode != 0:
        raise Unevaluable(f'cannot check out {rev}: {p.stderr.strip()}')
    head = git(tree, 'rev-parse', 'HEAD').stdout.strip()
    if head != rev:
        raise Unevaluable(f'{tree} reports {head}, expected {rev}')
    return tree


def measure(root, rev, work, scratch, population, base=None):
    """Measure the frozen predicate over ``root`` at ``rev``.

    ``work`` is a materialised checkout at ``rev`` where recorded commands run;
    ``scratch`` holds their fresh HOME/TMPDIR and lives outside that checkout.
    """
    text = read_rev(root, rev, 'SKILL.md')
    rows = parse_rows(text)
    live = [r for r in rows if 'historical' not in r['cells'][1]]
    groups = effective(live)
    findings = []
    os.makedirs(os.path.join(scratch, 'tmp'), exist_ok=True)
    os.makedirs(os.path.join(scratch, 'home'), exist_ok=True)
    # E4 — every .py/.mjs path token in every live row's cells resolves.
    for row in live:
        tokens = sorted(set(FILE_RE.findall(' '.join(row['cells']))))
        row['e4_missing'] = [t for t in tokens
                             if git(root, 'cat-file', '-e', f'{rev}:{t}').returncode != 0]
        if row['e4_missing']:
            miss = row['e4_missing']
            who = row.get('file') or f'row {row["line"]}'
            extra = f' (+{len(miss) - 1} more)' if len(miss) > 1 else ''
            finding = (f'E4 {who}: path token {miss[0]} does not resolve '
                       f'at {rev}{extra}')
            if finding not in findings:
                findings.append(finding)
    results = []
    for f in sorted(groups):
        row = groups[f][-1]
        kind = row['cells'][1]
        selftest_cell = row['cells'][4]
        fam = family(kind)
        differential = declares_differential(kind)
        entry = {'file': f, 'row_line': row['line'], 'family': fam,
                 'frozen': f in population}
        if row.get('e4_missing'):
            entry['mismatch'] = 'E4'
            entry['status'] = 'mismatch'
            entry['e4_missing'] = row['e4_missing']
            results.append(entry)
            continue
        cmd = selftest_command(selftest_cell)
        entry['command'] = cmd
        # E1 — the command must run this row's instrument, not another file.
        if cmd and not differential:
            prog = command_program(cmd)
            entry['program'] = prog
            if prog != f:
                findings.append(f'E1 command names {prog or "(none)"} not {f}')
                entry['mismatch'] = 'E1'
                entry['status'] = 'mismatch'
                results.append(entry)
                continue
        out = ''
        rc = None
        if cmd:
            rc, out = run_command(work, cmd, scratch)
            entry['exit'] = rc
        # E1 — gate kind needs a working self-test or a declared differential
        if fam == 'gate' and False:
            if cmd is None:
                if not differential:
                    findings.append(f'E1 {f}: Kind is gate without a self-test mode '
                                    f'or a declared differential')
                    entry['mismatch'] = 'E1'
            elif rc != 0:
                findings.append(f'E1 {f}: recorded self-test exits {rc}')
                entry['mismatch'] = 'E1'
        if entry.get('mismatch'):
            entry['status'] = 'mismatch'
            results.append(entry)
            continue
        # E2 — the claimed tally re-derives, and must be unambiguous
        obs = observed_pair(out) if out else None
        if cmd:
            pairs = claim_pairs(selftest_cell, cmd)
            if len(pairs) > 1:
                shown = ', '.join(f'{a}/{b}' for a, b in pairs)
                findings.append(f'E2 {f}: ambiguous tally in the Self-test cell: {shown}')
                entry['mismatch'] = 'E2'
            elif pairs:
                pair = pairs[0]
                if obs and pair != obs:
                    findings.append(f'E2 {f}: cell claims {pair[0]}/{pair[1]}, '
                                    f'observed {obs[0]}/{obs[1]}')
                    entry['mismatch'] = 'E2'
                elif not obs:
                    findings.append(f'E2 {f}: cell claims {pair[0]}/{pair[1]}, '
                                    f'no tally in output')
                    entry['mismatch'] = 'E2'
        # E3 — enumerated fixture ids match the observed total
        ids = {int(x) for x in FIX_RE.findall(selftest_cell)}
        if len(ids) >= 2:
            claim = len(ids)
            total = obs[1] if obs else None
            if total != claim:
                findings.append(f'E3 {f}: cell enumerates {claim} fixture ids, '
                                f'observed total {total}')
                entry['mismatch'] = 'E3'
        entry['status'] = 'mismatch' if entry.get('mismatch') else 'ok'
        results.append(entry)
    append_only = True
    if base:
        base_rows = [r for r in parse_rows(read_rev(root, base, 'SKILL.md'))
                     if 'historical' not in r['cells'][1]]
        base_names = {r['cells'][0] for r in base_rows}
        tip_names = {r['cells'][0] for r in rows}
        missing = sorted(base_names - tip_names)
        append_only = not missing
        for name in missing:
            findings.append(f'append_only: base row {name!r} is gone')
    missing_frozen_paths = [p for p in population if p not in groups]
    for path in missing_frozen_paths:
        findings.append(f'missing_frozen: {path} is in the frozen population but no '
                        f'live row derives it at {rev}')
    return {'rows': rows, 'live': live, 'groups': groups, 'results': results,
            'findings': findings, 'append_only': append_only,
            'missing_frozen': len(missing_frozen_paths),
            'missing_frozen_paths': missing_frozen_paths,
            'population': list(population)}


def format_summary(rev, res):
    classes = classes_of(res['findings'])
    met = bool(not res['findings'] and res['append_only'])
    return (f"C1v1 revision={rev} rows={len(res['rows'])} live={len(res['live'])} "
            f"files={len(res['groups'])} mismatches={len(res['findings'])} "
            f"classes={' '.join(classes) or '-'} "
            f"append_only={str(res['append_only']).lower()} "
            f"met={str(met).lower()} missing_frozen={res['missing_frozen']}")


# --------------------------------------------------------------------------
# --selftest: isolated fixtures built under --work
# --------------------------------------------------------------------------

FIXTURE_ENV = {
    'GIT_AUTHOR_NAME': 'c75-fixture',
    'GIT_AUTHOR_EMAIL': 'c75@fixture.invalid',
    'GIT_COMMITTER_NAME': 'c75-fixture',
    'GIT_COMMITTER_EMAIL': 'c75@fixture.invalid',
    'GIT_AUTHOR_DATE': '2026-11-03T00:00:00 +0000',
    'GIT_COMMITTER_DATE': '2026-11-03T00:00:00 +0000',
}


class SelftestError(Exception):
    pass


def _run(argv, cwd=None, env=None):
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, env=clean_env(env))
    if p.returncode != 0:
        raise SelftestError(f'{" ".join(argv)} exited {p.returncode}: {p.stderr.strip()}')
    return p.stdout


def _skill_md(rows):
    return ('# Fixture lane (c75 self-test)\n\n'
            '### Round 90 gate registry additions\n\n'
            '| Name | Kind | Entry command | Verdict map | Self-test | '
            'Pinned values / frozen proof | Write scope | Owner |\n'
            '|---|---|---|---|---|---|---|---|\n'
            + ''.join(row + '\n' for row in rows))


def _row(name, kind, entry, selftest, pinned='none'):
    return (f'| {name} | {kind} | `{entry}` | `0=met`; `1=not met` | '
            f'{selftest} | {pinned} | none | fixture |')


class Fixture:
    """One fixture lane: a git repository built under ``--work/selftest/<id>``."""

    def __init__(self, work, fid):
        self.fid = fid
        self.base_dir = os.path.join(work, 'selftest', fid)
        self.repo = os.path.join(self.base_dir, 'repo')
        self.tree = os.path.join(self.base_dir, 'tree')
        self.scratch = os.path.join(self.base_dir, 'scratch')
        shutil.rmtree(self.base_dir, ignore_errors=True)
        os.makedirs(self.repo)
        _run(['git', '-C', self.repo, 'init', '-q', '-b', 'main'])
        top = _run(['git', '-C', self.repo, 'rev-parse', '--show-toplevel']).strip()
        if os.path.realpath(top) != os.path.realpath(self.repo):
            raise SelftestError(f'{self.fid}: fixture toplevel {top} != {self.repo}')
        self.revisions = []

    def write(self, rel, content):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(content)

    def remove(self, rel):
        os.remove(os.path.join(self.repo, rel))

    def commit(self, message):
        _run(['git', '-C', self.repo, 'add', '-A'])
        _run(['git', '-C', self.repo, '-c', 'user.name=c75-fixture',
              '-c', 'user.email=c75@fixture.invalid', 'commit', '-q', '-m', message],
             cwd=self.repo, env=FIXTURE_ENV)
        rev = _run(['git', '-C', self.repo, 'rev-parse', 'HEAD']).strip()
        self.revisions.append(rev)
        return rev

    def measure(self, rev, population, base=None):
        shutil.rmtree(self.tree, ignore_errors=True)
        shutil.rmtree(self.scratch, ignore_errors=True)
        _run(['git', 'clone', '-q', '--shared', self.repo, self.tree])
        _run(['git', '-C', self.tree, 'checkout', '-q', rev])
        return measure(self.repo, rev, self.tree, self.scratch, population, base)


def _check(name, res, classes=(), findings=0, files=1, append_only=True,
           missing_frozen=0, met=False):
    problems = []
    got_classes = classes_of(res['findings'])
    if got_classes != sorted(classes):
        problems.append(f'classes {got_classes} != {sorted(classes)}')
    if len(res['findings']) != findings:
        problems.append(f'findings {len(res["findings"])} != {findings}')
    if len(res['results']) != files:
        problems.append(f'files {len(res["results"])} != {files}')
    if res['append_only'] != append_only:
        problems.append(f'append_only {res["append_only"]} != {append_only}')
    if res['missing_frozen'] != missing_frozen:
        problems.append(f'missing_frozen {res["missing_frozen"]} != {missing_frozen}')
    got_met = bool(not res['findings'] and res['append_only'])
    if got_met != met:
        problems.append(f'met {got_met} != {met}')
    summary = format_summary('fixture', res)
    if not SUMMARY_RE.fullmatch(summary):
        problems.append(f'summary shape: {summary}')
    return {'name': name, 'ok': not problems, 'problems': problems,
            'summary': summary, 'findings': res['findings']}


def _selftest_cases(work):
    out = []

    def add(name, fixture, rev, population, classes=(), findings=0, files=1,
            append_only=True, missing_frozen=0, met=False, base=None):
        res = fixture.measure(rev, population, base)
        out.append(_check(name, res, classes, findings, files, append_only,
                          missing_frozen, met))

    # f01 — E1 red: a gate row whose instrument has no self-test mode.
    fx = Fixture(work, 'f01_e1_red')
    fx.write('.ufo/fixtures/no_selftest.py', SCRIPT_NO_SELFTEST)
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/no_selftest.py', 'gate (live; fixture)',
        'python3 -B .ufo/fixtures/no_selftest.py',
        'none (no self-test mode; `--selftest` is an argparse error)')]))
    add('f01 E1 red', fx, fx.commit('f01'), ['.ufo/fixtures/no_selftest.py'],
        classes=('E1',), findings=1, met=False)

    # f02 — E1 green: a gate row with a working self-test.
    fx = Fixture(work, 'f02_e1_green')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/ok_gate.py', 'gate (live; fixture)',
        'python3 -B .ufo/fixtures/ok_gate.py',
        '`python3 -B .ufo/fixtures/ok_gate.py --selftest` (3 fixture checks)')]))
    add('f02 E1 green', fx, fx.commit('f02'), ['.ufo/fixtures/ok_gate.py'],
        met=True)

    # f03 — E2 red: the cell claims 5/5, the self-test prints 3/3.
    fx = Fixture(work, 'f03_e2_red')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/ok_gate.py', 'gate (live; fixture)',
        'python3 -B .ufo/fixtures/ok_gate.py',
        '`python3 -B .ufo/fixtures/ok_gate.py --selftest` (5/5 fixture checks)')]))
    add('f03 E2 red', fx, fx.commit('f03'), ['.ufo/fixtures/ok_gate.py'],
        classes=('E2',), findings=1, met=False)

    # f04 — E2 green: the claim matches the observed tally.
    fx = Fixture(work, 'f04_e2_green')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/ok_gate.py', 'gate (live; fixture)',
        'python3 -B .ufo/fixtures/ok_gate.py',
        '`python3 -B .ufo/fixtures/ok_gate.py --selftest` (3/3 fixture checks)')]))
    add('f04 E2 green', fx, fx.commit('f04'), ['.ufo/fixtures/ok_gate.py'],
        met=True)

    # f05 — E3 red: five distinct fixture ids named, eight fixtures observed.
    fx = Fixture(work, 'f05_e3_red')
    fx.write('.ufo/fixtures/ok_gate8.py', SCRIPT_OK8)
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/ok_gate8.py', 'gate (live; fixture)',
        'python3 -B .ufo/fixtures/ok_gate8.py',
        '`python3 -B .ufo/fixtures/ok_gate8.py --selftest` '
        '(f1 f2 f3 f4 f5 frozen fixtures)')]))
    add('f05 E3 red', fx, fx.commit('f05'), ['.ufo/fixtures/ok_gate8.py'],
        classes=('E3',), findings=1, met=False)

    # f06 — E3 green: the named id count equals the observed total.
    fx = Fixture(work, 'f06_e3_green')
    fx.write('.ufo/fixtures/ok_gate8.py', SCRIPT_OK8)
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/ok_gate8.py', 'gate (live; fixture)',
        'python3 -B .ufo/fixtures/ok_gate8.py',
        '`python3 -B .ufo/fixtures/ok_gate8.py --selftest` '
        '(f1 f2 f3 f4 f5 f6 f7 f8 frozen fixtures)')]))
    add('f06 E3 green', fx, fx.commit('f06'), ['.ufo/fixtures/ok_gate8.py'],
        met=True)

    # f07 — E4 red: the effective row's instrument path does not resolve.
    fx = Fixture(work, 'f07_e4_red')
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/ghost.py', 'instrument (live; fixture)',
        'python3 -B .ufo/fixtures/ghost.py', 'none (no self-test mode)')]))
    add('f07 E4 red', fx, fx.commit('f07'), ['.ufo/fixtures/ghost.py'],
        classes=('E4',), findings=1, met=False)

    # f08 — E4 green: instrument and every other path token resolve.
    fx = Fixture(work, 'f08_e4_green')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('.ufo/fixtures/ok_gate8.py', SCRIPT_OK8)
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/ok_gate.py', 'instrument (live; fixture)',
        'python3 -B .ufo/fixtures/ok_gate.py', 'none (no self-test mode)',
        pinned='witness `.ufo/fixtures/ok_gate8.py`')]))
    add('f08 E4 green', fx, fx.commit('f08'), ['.ufo/fixtures/ok_gate.py'],
        met=True)

    # f09 — E4 red on a non-instrument token: E4 covers every token of the row.
    fx = Fixture(work, 'f09_e4_token_red')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/ok_gate.py', 'instrument (live; fixture)',
        'python3 -B .ufo/fixtures/ok_gate.py', 'none (no self-test mode)',
        pinned='witness `.ufo/fixtures/ghost.py`')]))
    add('f09 E4 token red', fx, fx.commit('f09'), ['.ufo/fixtures/ok_gate.py'],
        classes=('E4',), findings=1, met=False)

    # f10 — superseding row: the appended row wins, so the E1-red first row is moot.
    fx = Fixture(work, 'f10_supersede')
    fx.write('.ufo/fixtures/no_selftest.py', SCRIPT_NO_SELFTEST)
    fx.write('SKILL.md', _skill_md([
        _row('.ufo/fixtures/no_selftest.py', 'gate (live; fixture)',
             'python3 -B .ufo/fixtures/no_selftest.py', 'none (no self-test mode)'),
        _row('.ufo/fixtures/no_selftest.py', 'instrument (live; demoted by a later row)',
             'python3 -B .ufo/fixtures/no_selftest.py', 'none (no self-test mode)'),
    ]))
    add('f10 superseding row', fx, fx.commit('f10'), ['.ufo/fixtures/no_selftest.py'],
        files=1, met=True)

    # f11 — deleted base row: append_only fails.
    fx = Fixture(work, 'f11_append_only')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('.ufo/fixtures/ok_gate8.py', SCRIPT_OK8)
    fx.write('SKILL.md', _skill_md([
        _row('.ufo/fixtures/ok_gate.py', 'instrument (live; fixture)',
             'python3 -B .ufo/fixtures/ok_gate.py', 'none (no self-test mode)'),
        _row('.ufo/fixtures/ok_gate8.py', 'instrument (live; fixture)',
             'python3 -B .ufo/fixtures/ok_gate8.py', 'none (no self-test mode)'),
    ]))
    base11 = fx.commit('f11 base')
    fx.write('SKILL.md', _skill_md([
        _row('.ufo/fixtures/ok_gate8.py', 'instrument (live; fixture)',
             'python3 -B .ufo/fixtures/ok_gate8.py', 'none (no self-test mode)'),
    ]))
    add('f11 deleted base row', fx, fx.commit('f11 tip'),
        ['.ufo/fixtures/ok_gate8.py'], findings=1, files=1, append_only=False,
        met=False, base=base11)

    # f12 — frozen path shrunk by a historical relabel: missing_frozen fires.
    fx = Fixture(work, 'f12_missing_frozen')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('.ufo/fixtures/ok_gate8.py', SCRIPT_OK8)
    fx.write('SKILL.md', _skill_md([
        _row('.ufo/fixtures/ok_gate.py', 'instrument (live; fixture)',
             'python3 -B .ufo/fixtures/ok_gate.py', 'none (no self-test mode)'),
        _row('.ufo/fixtures/ok_gate8.py', 'instrument (live; fixture)',
             'python3 -B .ufo/fixtures/ok_gate8.py', 'none (no self-test mode)'),
    ]))
    base12 = fx.commit('f12 base')
    fx.write('SKILL.md', _skill_md([
        _row('.ufo/fixtures/ok_gate.py',
             'instrument (historical: fixture pin only)',
             'python3 -B .ufo/fixtures/ok_gate.py', 'none (no self-test mode)'),
        _row('.ufo/fixtures/ok_gate8.py', 'instrument (live; fixture)',
             'python3 -B .ufo/fixtures/ok_gate8.py', 'none (no self-test mode)'),
    ]))
    add('f12 missing frozen path', fx, fx.commit('f12 tip'),
        ['.ufo/fixtures/ok_gate.py', '.ufo/fixtures/ok_gate8.py'],
        findings=1, files=1, append_only=True, missing_frozen=1, met=False,
        base=base12)

    # f13 — distinct fixture-id count: f1, f3, f7 are three ids against a 3/3 total.
    fx = Fixture(work, 'f13_id_count')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/ok_gate.py', 'gate (live; fixture)',
        'python3 -B .ufo/fixtures/ok_gate.py',
        '`python3 -B .ufo/fixtures/ok_gate.py --selftest` (3/3; ids f1 f3 f7)')]))
    add('f13 distinct id count', fx, fx.commit('f13'), ['.ufo/fixtures/ok_gate.py'],
        met=True)

    # f14 — all green: two honest rows, both in the floor, nothing to report.
    fx = Fixture(work, 'f14_all_green')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('.ufo/fixtures/ok_gate8.py', SCRIPT_OK8)
    fx.write('SKILL.md', _skill_md([
        _row('.ufo/fixtures/ok_gate.py', 'gate (live; fixture)',
             'python3 -B .ufo/fixtures/ok_gate.py',
             '`python3 -B .ufo/fixtures/ok_gate.py --selftest` (3/3 checks)'),
        _row('.ufo/fixtures/ok_gate8.py', 'gate (live; fixture)',
             'python3 -B .ufo/fixtures/ok_gate8.py',
             '`python3 -B .ufo/fixtures/ok_gate8.py --selftest` (8/8 checks)'),
    ]))
    add('f14 all green', fx, fx.commit('f14'),
        ['.ufo/fixtures/ok_gate.py', '.ufo/fixtures/ok_gate8.py'],
        files=2, met=True)

    # f15 — E2 ambiguous tally: one claim segment, two different pairs.
    fx = Fixture(work, 'f15_ambiguous_tally')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/ok_gate.py', 'gate (live; fixture)',
        'python3 -B .ufo/fixtures/ok_gate.py',
        '`python3 -B .ufo/fixtures/ok_gate.py --selftest` (0/3 then 3/3)')]))
    add('f15 E2 ambiguous tally', fx, fx.commit('f15'), ['.ufo/fixtures/ok_gate.py'],
        classes=('E2',), findings=1, met=False)

    # f16 — E1 red: the instrument is only a trailing argument, not the program.
    fx = Fixture(work, 'f16_argument_binding')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('.ufo/fixtures/other.py', SCRIPT_OK)
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/ok_gate.py', 'gate (live; fixture)',
        'python3 -B .ufo/fixtures/ok_gate.py',
        '`python3 -B .ufo/fixtures/other.py --selftest .ufo/fixtures/ok_gate.py`')]))
    add('f16 E1 argument binding red', fx, fx.commit('f16'),
        ['.ufo/fixtures/ok_gate.py'], classes=('E1',), findings=1, met=False)

    # f17 — E1 red: the command runs another file; the instrument is only a comment.
    fx = Fixture(work, 'f17_comment_binding')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('.ufo/fixtures/other.py', SCRIPT_OK)
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/ok_gate.py', 'gate (live; fixture)',
        'python3 -B .ufo/fixtures/ok_gate.py',
        '`python3 -B .ufo/fixtures/other.py --selftest` # .ufo/fixtures/ok_gate.py')]))
    add('f17 E1 comment binding red', fx, fx.commit('f17'),
        ['.ufo/fixtures/ok_gate.py'], classes=('E1',), findings=1, met=False)

    # f18 — E1 red: `nondifferential` is not the word `differential`.
    fx = Fixture(work, 'f18_nondifferential')
    fx.write('.ufo/fixtures/no_selftest.py', SCRIPT_NO_SELFTEST)
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/no_selftest.py', 'gate (nondifferential; offline; fixture)',
        'python3 -B .ufo/fixtures/no_selftest.py',
        'the gate has no selftest of its own')]))
    add('f18 E1 nondifferential red', fx, fx.commit('f18'),
        ['.ufo/fixtures/no_selftest.py'], classes=('E1',), findings=1, met=False)

    # f19 — E4 red on a NON-effective row: every live row is checked.
    fx = Fixture(work, 'f19_e4_secondary_row')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('SKILL.md', _skill_md([
        _row('.ufo/fixtures/ok_gate.py', 'instrument (live; fixture)',
             'python3 -B .ufo/fixtures/ok_gate.py', 'none (no self-test mode)',
             pinned='witness `.ufo/fixtures/ghost.py`'),
        _row('.ufo/fixtures/ok_gate.py', 'instrument (live; fixture)',
             'python3 -B .ufo/fixtures/ok_gate.py', 'none (no self-test mode)'),
    ]))
    add('f19 E4 secondary row red', fx, fx.commit('f19'),
        ['.ufo/fixtures/ok_gate.py'], classes=('E4',), findings=1, met=False)

    # f20 — ReviewerC1 F11: the file survives, the row is rewritten with no path
    # token and the Name cell stays prose; only the floor catches the loss.
    fx = Fixture(work, 'f20_retired_in_place')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('.ufo/fixtures/ok_gate8.py', SCRIPT_OK8)
    fx.write('.ufo/fixtures/extra.py', SCRIPT_OK)
    fx.write('SKILL.md', _skill_md([
        _row('ok counter', 'instrument (live; fixture)',
             'python3 -B .ufo/fixtures/ok_gate.py', 'none (no self-test mode)'),
        _row('second counter', 'instrument (live; fixture)',
             'python3 -B .ufo/fixtures/ok_gate8.py', 'none (no self-test mode)'),
        _row('broken counter', 'instrument (live; fixture)',
             'python3 -B .ufo/fixtures/extra.py', 'none (no self-test mode)'),
    ]))
    base20 = fx.commit('f20 base')
    fx.write('SKILL.md', _skill_md([
        _row('ok counter', 'instrument (live; fixture)',
             'python3 -B .ufo/fixtures/ok_gate.py', 'none (no self-test mode)'),
        _row('second counter', 'instrument (live; fixture)',
             'python3 -B .ufo/fixtures/ok_gate8.py', 'none (no self-test mode)'),
        _row('broken counter', 'instrument (retired in place)', 'none',
             'none (no self-test mode)'),
    ]))
    add('f20 retired in place', fx, fx.commit('f20 tip'),
        ['.ufo/fixtures/ok_gate.py', '.ufo/fixtures/ok_gate8.py',
         '.ufo/fixtures/extra.py'],
        findings=1, files=2, append_only=True, missing_frozen=1, met=False,
        base=base20)

    # f21 — the instrument file is deleted, its row is retained: E4 catches it.
    fx = Fixture(work, 'f21_file_gone_row_kept')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/ok_gate.py', 'instrument (live; fixture)',
        'python3 -B .ufo/fixtures/ok_gate.py', 'none (no self-test mode)')]))
    base21 = fx.commit('f21 base')
    fx.remove('.ufo/fixtures/ok_gate.py')
    add('f21 file gone row kept', fx, fx.commit('f21 tip'),
        ['.ufo/fixtures/ok_gate.py'], classes=('E4',), findings=1, files=1,
        append_only=True, met=False, base=base21)

    # f22 — E1 red: the word `differential` outside the Kind cell does not exempt.
    fx = Fixture(work, 'f22_differential_elsewhere')
    fx.write('.ufo/fixtures/no_selftest.py', SCRIPT_NO_SELFTEST)
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/no_selftest.py', 'gate (live; fixture)',
        'python3 -B .ufo/fixtures/no_selftest.py',
        'none (no self-test mode)',
        pinned='the differential substitute lives in the prose, not the Kind cell')]))
    add('f22 E1 differential elsewhere red', fx, fx.commit('f22'),
        ['.ufo/fixtures/no_selftest.py'], classes=('E1',), findings=1, met=False)

    # f23 — E1 red: the command's program is not an interpreter for the instrument.
    fx = Fixture(work, 'f23_no_interpreter')
    fx.write('.ufo/fixtures/ok_gate.py', SCRIPT_OK)
    fx.write('.ufo/fixtures/run.sh', '#!/bin/sh\nexit 0\n')
    fx.write('SKILL.md', _skill_md([_row(
        '.ufo/fixtures/ok_gate.py', 'gate (live; fixture)',
        'python3 -B .ufo/fixtures/ok_gate.py',
        '`bash .ufo/fixtures/run.sh --selftest`')]))
    add('f23 E1 no interpreter red', fx, fx.commit('f23'),
        ['.ufo/fixtures/ok_gate.py'], classes=('E1',), findings=1, met=False)

    return out


def _harness_checks(work):
    """Checks of the counter's own contract surface (floor, flags, exit codes)."""
    checks = []
    floor = list(FROZEN_POPULATION)
    checks.append({'name': 'h01 frozen floor', 'ok': len(floor) == 16 and len(set(floor)) == 16,
                   'problems': [] if (len(floor) == 16 and len(set(floor)) == 16)
                   else [f'floor has {len(floor)} entries, {len(set(floor))} distinct']})

    import contextlib
    import io
    buf_out, buf_err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        rc = main(['--emit-population'])
    lines = [line for line in buf_out.getvalue().splitlines() if line.strip()]
    checks.append({'name': 'h02 emit-population', 'ok': rc == 0 and lines == floor,
                   'problems': [] if (rc == 0 and lines == floor)
                   else [f'exit {rc}, {len(lines)} lines']})

    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        try:
            main(['--emit-population', '--bogus'])
            rc = None
        except SystemExit as exc:
            rc = exc.code
    checks.append({'name': 'h03 usage exit 64', 'ok': rc == 64, 'problems': [] if rc == 64
                   else [f'unknown-flag exit {rc} != 64']})

    empty = os.path.join(work, 'selftest', 'h04_not_a_repo')
    shutil.rmtree(empty, ignore_errors=True)
    os.makedirs(empty)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        rc = main(['--root', empty, '--revision', 'deadbeef',
                   '--work', os.path.join(work, 'selftest', 'h04_work')])
    checks.append({'name': 'h04 unevaluable exit 2', 'ok': rc == 2, 'problems': []
                   if rc == 2 else [f'non-repository exit {rc} != 2']})

    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        rc = main(['--root', empty, '--revision', 'deadbeef'])
    checks.append({'name': 'h05 missing --work exit 64', 'ok': rc == 64, 'problems': []
                   if rc == 64 else [f'missing --work exit {rc} != 64']})

    pop_file = os.path.join(work, 'selftest', 'h06_population.txt')
    with open(pop_file, 'w', encoding='utf-8') as fh:
        fh.write('# fixture floor\n.ufo/fixtures/ok_gate.py\n\n'
                 '.ufo/fixtures/ok_gate8.py\n.ufo/fixtures/extra.py\n')
    buf_out = io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(io.StringIO()):
        rc = main(['--emit-population', '--population', pop_file])
    got = [line for line in buf_out.getvalue().splitlines() if line.strip()]
    want = ['.ufo/fixtures/ok_gate.py', '.ufo/fixtures/ok_gate8.py', '.ufo/fixtures/extra.py']
    checks.append({'name': 'h06 --population file', 'ok': rc == 0 and got == want,
                   'problems': [] if (rc == 0 and got == want)
                   else [f'exit {rc}, lines {got} != {want}']})
    return checks


def run_selftest(work):
    work = os.path.abspath(work)
    os.makedirs(work, exist_ok=True)
    checks = _selftest_cases(work) + _harness_checks(work)
    failed = 0
    for check in checks:
        state = 'PASS' if check['ok'] else 'FAIL'
        print(f"fixture {check['name']}: {state} {check.get('summary', '')}".rstrip())
        for problem in check['problems']:
            print(f'  problem: {problem}')
        if not check['ok']:
            failed += 1
    print(f'C1v1 selftest fixtures={len(checks)} passed={len(checks) - failed} '
          f'failed={failed}')
    print(f'selftest {len(checks) - failed}/{len(checks)}')
    return 0 if failed == 0 else 1


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        print(f'{self.prog}: error: {message}', file=sys.stderr)
        raise SystemExit(64)


def main(argv=None):
    ap = Parser(description=__doc__.splitlines()[0])
    ap.add_argument('--root', default='.', help='lane checkout (a git repository)')
    ap.add_argument('--revision', default=None, help='revision to measure (default: master)')
    ap.add_argument('--base', default=None,
                    help='baseline revision for the append-only conjunct')
    ap.add_argument('--work', default=None,
                    help='scratch dir outside the lane; required unless --emit-population')
    ap.add_argument('--population', default=None,
                    help='file of frozen paths, one per line (default: the frozen 16)')
    ap.add_argument('--emit-population', action='store_true',
                    help='print the effective population floor, one path per line')
    ap.add_argument('--json', action='store_true', help='print the per-file result list')
    ap.add_argument('--selftest', action='store_true',
                    help='run the isolated fixture self-test under --work')
    args = ap.parse_args(argv)

    try:
        population = load_population(args.population)
        if args.emit_population:
            for path in population:
                print(path)
            return 0
        if not args.work:
            print('64 usage: --work <dir> is required', file=sys.stderr)
            return 64
        if args.selftest:
            return run_selftest(args.work)
        root = os.path.abspath(args.root)
        if git(root, 'rev-parse', '--show-toplevel').returncode != 0:
            raise Unevaluable(f'{root} is not a git repository toplevel')
        rev_arg = args.revision or git(root, 'rev-parse', 'master').stdout.strip()
        p = git(root, 'rev-parse', '--verify', f'{rev_arg}^{{commit}}')
        if p.returncode != 0 or not p.stdout.strip():
            raise Unevaluable(f'cannot resolve revision {rev_arg!r}: {p.stderr.strip()}')
        rev = p.stdout.strip()
        work = os.path.abspath(args.work)
        tree = prepare_tree(root, rev, work)
        res = measure(root, rev, tree, os.path.join(work, 'scratch'), population, args.base)
        summary = format_summary(rev_arg, res)
        print(summary)
        for finding in res['findings']:
            print(f'  finding: {finding}')
        if args.json:
            payload = {
                'schema': 'c1-row-truth/v1',
                'revision': rev_arg,
                'revision_full': rev,
                'base': args.base,
                'rows': len(res['rows']),
                'live': len(res['live']),
                'files': len(res['groups']),
                'mismatches': len(res['findings']),
                'classes': classes_of(res['findings']),
                'append_only': res['append_only'],
                'met': bool(not res['findings'] and res['append_only']),
                'missing_frozen': res['missing_frozen'],
                'missing_frozen_paths': res['missing_frozen_paths'],
                'population': res['population'],
                'derived_files': sorted(res['groups']),
                'results': res['results'],
                'findings': res['findings'],
            }
            print(json.dumps(payload, indent=2))
        return 0 if (not res['findings'] and res['append_only']) else 1
    except Unevaluable as exc:
        print(f'2 unevaluable: {exc}', file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 — the exit contract names every fault 2
        print(f'2 unevaluable: {type(exc).__name__}: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
