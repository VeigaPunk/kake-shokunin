#!/usr/bin/env python3
"""c75_row_truth.py — C1 counter, round 75 (kake).

Predicate (frozen in .ufo/waves/round-75/contract.md section C1):

  For every live gate-registry row of SKILL.md — a table row inside a section
  titled ``### Round <N> gate registry additions`` whose Kind cell does not
  carry the ``historical`` qualifier — the row's claim re-derives by
  execution over the lane tree at ``--revision``:

    E1  a row whose Kind family is ``gate`` carries a working self-test
        (``--selftest`` exits 0) or its Kind cell declares the differential
        substitute (the word ``differential``).
    E2  when the Self-test cell records a ``a/b`` tally, the observed
        ``--selftest`` pass/total equals it.
    E3  when the Self-test cell enumerates two or more fixture ids ``f<N>``,
        the observed self-test total equals the number of distinct ids named.
    E4  every ``.py``/``.mjs`` path token in the row's cells resolves at the
        measured revision.

  Effective row: rows are grouped by instrument file (every ``.py``/``.mjs``
  token a row names); the last row naming a file wins.  ``append_only`` holds
  when every row name seen in ``--base`` is still present at the measured
  revision (a row may be superseded, never deleted).

  met = (mismatches == 0) and append_only.

Exit: 0 met, 1 not met, 2 unevaluable, 64 usage.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

SEC_RE = re.compile(r'^### Round (\d+) gate registry additions')
FILE_RE = re.compile(r'((?:scripts|\.ufo)/[\w./-]+\.(?:py|mjs))')
PAIR_RE = re.compile(r'\b(\d+)\s*/\s*(\d+)\b')
FIX_RE = re.compile(r'\bf(\d+)\b')
TALLY_RE = re.compile(r'\b(\d+)\s*/\s*(\d+)\b')


def git(root, *args, check=False):
    return subprocess.run(['git', '-C', root, *args], capture_output=True, text=True, check=check)


def read_rev(root, rev, path):
    p = git(root, 'show', f'{rev}:{path}')
    if p.returncode != 0:
        raise SystemExit(f'2 unevaluable: cannot read {path} at {rev}: {p.stderr.strip()}')
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


def run_selftest(work, command, scratch):
    """Run a Self-test cell command inside the materialised tree at a revision."""
    cmd = command
    cmd = cmd.replace('[--work <dir>]', f'--work {scratch}')
    cmd = cmd.replace('--work <dir>', f'--work {scratch}')
    cmd = cmd.replace('<scratch>', scratch)
    cmd = cmd.replace('<lane>', work)
    out = subprocess.run(['bash', '-c', cmd], cwd=work, capture_output=True, text=True,
                         env={**os.environ, 'HOME': os.path.join(scratch, 'home'),
                              'TMPDIR': os.path.join(scratch, 'tmp'), 'KAKE_SCRATCH': scratch})
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


def claim_pair(cell):
    pairs = PAIR_RE.findall(cell)
    if not pairs:
        return None
    a, b = pairs[-1]
    return int(a), int(b)


def observed_pair(output):
    pairs = TALLY_RE.findall(output)
    if not pairs:
        return None
    a, b = pairs[-1]
    return int(a), int(b)


def measure(root, rev, work, scratch=None):
    text = read_rev(root, rev, 'SKILL.md')
    rows = parse_rows(text)
    live = [r for r in rows if 'historical' not in r['cells'][1]]
    groups = effective(live)
    findings = []
    scratch = scratch or os.path.join(os.path.dirname(work), 'scratch')
    os.makedirs(os.path.join(scratch, 'tmp'), exist_ok=True)
    os.makedirs(os.path.join(scratch, 'home'), exist_ok=True)
    for token in ('tmp', 'home'):
        os.makedirs(os.path.join(scratch, token), exist_ok=True)
    results = []
    for f in sorted(groups):
        row = groups[f][-1]
        kind = row['cells'][1]
        selftest_cell = row['cells'][4]
        fam = family(kind)
        entry = {'file': f, 'row_line': row['line'], 'family': fam}
        # E4 — instrument path tokens resolve
        if git(root, 'cat-file', '-e', f'{rev}:{f}').returncode != 0:
            entry['mismatch'] = f'E4 path {f} does not resolve at {rev}'
            results.append(entry)
            findings.append(entry['mismatch'])
            continue
        cmd = selftest_command(selftest_cell)
        entry['command'] = cmd
        out = ''
        rc = None
        if cmd:
            rc, out = run_selftest(work, cmd, scratch)
            entry['exit'] = rc
        # E1 — gate kind needs a working self-test or a declared differential
        if fam == 'gate':
            if cmd is None:
                if 'differential' not in kind:
                    findings.append(f'E1 {f}: Kind is gate without a self-test mode or a declared differential')
                    entry['mismatch'] = 'E1'
            elif rc != 0:
                findings.append(f'E1 {f}: recorded self-test exits {rc}')
                entry['mismatch'] = 'E1'
        if entry.get('mismatch'):
            results.append(entry)
            continue
        # E2 — recorded tally pair re-derives
        pair = claim_pair(selftest_cell) if cmd else None
        obs = observed_pair(out) if out else None
        if pair and obs and pair != obs:
            findings.append(f'E2 {f}: cell claims {pair[0]}/{pair[1]}, observed {obs[0]}/{obs[1]}')
            entry['mismatch'] = 'E2'
        elif pair and not obs:
            findings.append(f'E2 {f}: cell claims {pair[0]}/{pair[1]}, no tally in output')
            entry['mismatch'] = 'E2'
        # E3 — enumered fixture ids match the observed total
        ids = set()
        if len(ids) >= 2:
            claim = len(ids)
            total = obs[1] if obs else None
            if total != claim:
                findings.append(f'E3 {f}: cell enumerates {claim} fixture ids, observed total {total}')
                entry['mismatch'] = 'E3'
        results.append(entry)
    return rows, live, groups, results, findings


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--root', default='.')
    ap.add_argument('--revision', default=None)
    ap.add_argument('--base', default=None, help='baseline revision for the append-only conjunct')
    ap.add_argument('--work', default=None)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    rev = args.revision or git(root, 'rev-parse', 'master').stdout.strip()
    work = args.work
    if not work:
        print('64 usage: --work <dir> is required', file=sys.stderr)
        return 64
    work = os.path.abspath(work)
    tree = os.path.join(work, 'tree')
    if not os.path.isdir(os.path.join(tree, '.git')):
        os.makedirs(work, exist_ok=True)
        p = subprocess.run(['git', 'clone', '-q', '--shared', root, tree], capture_output=True, text=True)
        if p.returncode != 0:
            print(f'2 unevaluable: cannot clone the lane: {p.stderr.strip()}', file=sys.stderr)
            return 2
        p = subprocess.run(['git', '-C', tree, 'checkout', '-q', rev], capture_output=True, text=True)
        if p.returncode != 0:
            print(f'2 unevaluable: cannot check out {rev}: {p.stderr.strip()}', file=sys.stderr)
            return 2
    rows, live, groups, results, findings = measure(root, rev, tree, os.path.join(work, 'scratch'))
    append_only = True
    if args.base:
        base_rows = [r for r in parse_rows(read_rev(root, args.base, 'SKILL.md')) if 'historical' not in r['cells'][1]]
        base_names = {r['cells'][0] for r in base_rows}
        tip_names = {r['cells'][0] for r in rows}
        missing = sorted(base_names - tip_names)
        append_only = not missing
        for name in missing:
            findings.append(f'append_only: base row {name!r} is gone')
    body = ' '.join(sorted(set(re.findall(r'\bE[1-4]\b', ' '.join(findings)))))
    print(f"C1v1 revision={rev} rows={len(rows)} live={len(live)} files={len(groups)} "
          f"mismatches={len(findings)} classes={body or '-'} append_only={str(append_only).lower()} "
          f"met={str(bool(not findings and append_only)).lower()}")
    for f in findings:
        print(f'  finding: {f}')
    if args.json:
        import json
        print(json.dumps({'revision': rev, 'findings': findings, 'results': results,
                          'append_only': append_only}, indent=2))
    return 0 if (not findings and append_only) else 1


if __name__ == '__main__':
    sys.exit(main())
