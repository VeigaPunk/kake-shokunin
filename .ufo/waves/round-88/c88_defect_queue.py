#!/usr/bin/env python3
"""Round 88 C1 — the three routed round-87 defects, decided over committed bytes.

Items (all three must close for the claim to be met):

  D1 ledger-companion   corpus/knowledge/gate-agreement-ledger.json lives under
                        knowledge/ but a JSON file cannot carry the provenance
                        trio. Fix accepted here is the routed alternative: a
                        sourced companion entry that names the ledger, carries
                        source:/verified-at:/recheck:, and quotes the ledger's
                        own sha256 (a value only readable from its bytes).
                        The ledger bytes themselves must stay equal to the
                        frozen base copy, so the fix cannot rewrite the data.
  D2 diagnostic-type    scripts/cache_current_age.py must name the offending
                        JSON type in its invalid_input message (float, boolean),
                        keep the valid path's six integer terms, and keep its
                        own 61-fixture selftest green.
  D3 recheck-path       corpus/knowledge/cache-current-age.md must keep a real
                        cadence in its recheck line, name no ephemeral scratch
                        path there, carry the offline selftest command in a
                        mktemp form in its body, and preserve every other base
                        line byte-identically (appends allowed, one metadata
                        line corrected).

Modes: --revision reads the lane repo at a commit; --mirror reads a directory
tree (used by --selftest). No receipt, fleet input or other claim is read.
"""
import argparse
import difflib
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FROZEN = HERE / 'frozen'
BASE = 'f4479c14813037ad993a49a3dee4028763470f7a'
COMPANION = 'corpus/knowledge/gate-agreement-metadata.md'
LEDGER = 'corpus/knowledge/gate-agreement-ledger.json'
ENTRY = 'corpus/knowledge/cache-current-age.md'
TOOL = 'scripts/cache_current_age.py'
ITEMS = ('D1-ledger-companion', 'D2-diagnostic-type', 'D3-recheck-path')
VALID = {"date_value": 80, "request_time": 90, "response_time": 100, "now": 130, "age_value": 5}
VALID_OUT = {"apparent_age": 20, "response_delay": 10, "corrected_age_value": 15,
             "corrected_initial_age": 20, "resident_time": 30, "current_age": 50}
FLOAT = {"date_value": 7.0, "request_time": 1, "response_time": 2, "now": 3}
BOOL = {"date_value": True, "request_time": 1, "response_time": 2, "now": 3}
EPHEMERAL = ('/fast/scratch', 'TMPDIR=', '/tmp/')


def git_bytes(root, rev, path):
    p = subprocess.run(['git', '-C', str(root), 'show', f'{rev}:{path}'], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def item_d1(read):
    fails = []
    ledger = read(LEDGER)
    digest = None
    base_ledger = (FROZEN / 'base-gate-agreement-ledger.json').read_bytes()
    if ledger is None:
        fails.append('ledger missing')
    else:
        if ledger != base_ledger:
            fails.append('ledger bytes differ from the frozen base copy')
        digest = hashlib.sha256(ledger).hexdigest()
    comp = read(COMPANION)
    if comp is None:
        fails.append('companion entry missing')
        return fails
    text = comp.decode('utf-8', 'replace')
    head = text.splitlines()[:8]
    for key in ('source', 'verified-at', 'recheck'):
        if not any(l.startswith(key + ':') and l[len(key) + 1:].strip() for l in head):
            fails.append(f'companion head lacks a filled {key}: line')
    if not any(l.startswith('source:') and LEDGER in l for l in head):
        fails.append('companion source: line does not name the ledger path')
    if ledger is not None and digest not in text:
        fails.append('companion does not quote the ledger sha256')
    return fails


def _run_tool(tool_bytes, work, payload, selftest=False):
    work.mkdir(parents=True, exist_ok=True)
    path = work / 'cache_current_age.py'
    path.write_bytes(tool_bytes)
    try:
        argv = [sys.executable, '-B', str(path)] + (['--selftest'] if selftest else [])
        return subprocess.run(argv, input=None if selftest else json.dumps(payload),
                              capture_output=True, text=True, timeout=60)
    finally:
        path.unlink(missing_ok=True)


def item_d2(read, work):
    fails = []
    tool = read(TOOL)
    if tool is None:
        return ['tool missing']
    p = _run_tool(tool, work, VALID)
    if p.returncode != 0:
        fails.append(f'valid input exited {p.returncode}')
    else:
        try:
            obj = json.loads(p.stdout)
        except ValueError:
            obj = None
        if obj != VALID_OUT:
            fails.append('valid input did not emit the six expected integer terms')
    p = _run_tool(tool, work, FLOAT)
    if p.returncode != 1 or not p.stderr.startswith('invalid_input:'):
        fails.append('float input did not fail closed with invalid_input')
    elif 'float' not in p.stderr or 'boolean' in p.stderr:
        fails.append('float input diagnostic does not name float (or still says boolean)')
    elif 'date_value' not in p.stderr:
        fails.append('float input diagnostic does not name the offending key')
    p = _run_tool(tool, work, BOOL)
    if p.returncode != 1 or 'boolean' not in p.stderr or 'float' in p.stderr:
        fails.append('bool input diagnostic does not name boolean')
    p = _run_tool(tool, work, VALID, selftest=True)
    if p.returncode != 0 or 'selftest' not in p.stdout.lower():
        fails.append('tool selftest is not green')
    return fails


def item_d3(read):
    fails = []
    entry = read(ENTRY)
    if entry is None:
        return ['entry missing']
    base = (FROZEN / 'base-cache-current-age.md').read_bytes()
    new_lines = entry.decode('utf-8', 'replace').splitlines()
    base_lines = base.decode('utf-8', 'replace').splitlines()
    recheck = [l for l in new_lines if l.startswith('recheck:')]
    if len(recheck) != 1:
        fails.append('expected exactly one recheck line')
    else:
        line = recheck[0]
        for token in EPHEMERAL:
            if token in line:
                fails.append(f'recheck line still names an ephemeral path token {token!r}')
        rest = line[len('recheck:'):].strip()
        if not (rest[:1].isdigit() and ('d' in rest.split()[0].lower() or rest[:4].isdigit())):
            fails.append('recheck line does not open with a cadence or ISO date')
    if not any('mktemp -d' in l and TOOL in l and '--selftest' in l for l in new_lines):
        fails.append('entry body lacks the mktemp-form offline selftest command')
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, base_lines, new_lines, autojunk=False).get_opcodes():
        if tag == 'equal':
            continue
        if tag == 'insert':
            continue
        if (tag == 'replace' and i2 - i1 == 1 and j2 - j1 == 1
                and base_lines[i1].startswith('recheck:') and new_lines[j1].startswith('recheck:')):
            continue
        fails.append(f'history-preservation violation at base line {i1 + 1} ({tag})')
        break
    return fails


def evaluate(read, work):
    return {'D1-ledger-companion': item_d1(read),
            'D2-diagnostic-type': item_d2(read, work),
            'D3-recheck-path': item_d3(read)}


def repaired_tool_bytes():
    """Base tool with only the diagnostic message fixed — the selftest's green fixture."""
    base = (FROZEN / 'base-cache_current_age.py').read_bytes().decode()
    old = '            raise ValueError(f"{key} must be an integer, not boolean")'
    new = ('            raise ValueError("%s must be an integer, not %s" % (key, "boolean" if '
           'isinstance(value, bool) else type(value).__name__))')
    assert old in base, 'frozen base tool no longer carries the defective line'
    return base.replace(old, new).encode()


def fixed_entry_bytes():
    """Base entry: recheck line corrected, one mktemp-checklist line appended."""
    base = (FROZEN / 'base-cache-current-age.md').read_text()
    lines = base.splitlines()
    assert lines[2].startswith('recheck:'), 'frozen base entry line 3 is not the recheck line'
    lines[2] = ('recheck: 180d or source/adapter change; reopen '
                'https://httpwg.org/specs/rfc9111.html#age.calculations and compare section 4.2.3 '
                'equations; the offline selftest command is item 4 of the checklist below.')
    lines.append('6. Offline selftest without a fixed scratch path: '
                 'TMPDIR=$(mktemp -d) python3 -B scripts/cache_current_age.py --selftest; '
                 'the directory is created by the shell and removed by the operator.')
    return ('\n'.join(lines) + '\n').encode()


def companion_bytes():
    ledger = (FROZEN / 'base-gate-agreement-ledger.json').read_bytes()
    digest = hashlib.sha256(ledger).hexdigest()
    return ('source: ' + LEDGER + ' — lane metadata ledger; ledger sha256 ' + digest + '; '
            'originating verdicts in corpus/lessons/round-8{4,5,6}-verifier-spotcheck.md, snapshots '
            'under .ufo/waves/round-87/snapshots/.\n'
            'verified-at: 2026-11-04 — the ledger is a record of closure-owned decisions, not a '
            'domain claim; round-88 counter .ufo/waves/round-88/c88_defect_queue.py.\n'
            'recheck: 180d or on a new verifier spot-check\n\n'
            '# Gate-agreement ledger — provenance companion\n\n'
            'The ledger records the eight r84/r85/r86 admit/reject decisions and the outside '
            'verdict for each. It is evidence metadata, not a sourced publishing claim: the '
            'decisions belong to the closure session, and the ledger row only states who decided '
            'what and that the outside review agreed. The quoted sha256 binds this entry to the '
            'exact ledger bytes; a ledger change must revise both.\n').encode()


def mirror_tree(root):
    for rel, data in ((LEDGER, (FROZEN / 'base-gate-agreement-ledger.json').read_bytes()),
                      (ENTRY, fixed_entry_bytes()),
                      (COMPANION, companion_bytes()),
                      (TOOL, repaired_tool_bytes())):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)


def selftest():
    checks = []

    def record(label, got, want):
        checks.append((label, got == want))

    with tempfile.TemporaryDirectory(prefix='kake-r88-c1-selftest-') as d:
        d = Path(d)
        work = d / 'work'

        def reader(root):
            def read(path):
                p = root / path
                return p.read_bytes() if p.is_file() else None
            return read

        green = d / 'green'
        mirror_tree(green)
        rd = reader(green)
        record('green tree closes all three', sum(not v for v in evaluate(rd, work).values()), 3)

        def mutant(name, mutate):
            m = d / name
            mirror_tree(m)
            mutate(m)
            return evaluate(reader(m), work)

        def drop_comp(m):
            (m / COMPANION).unlink()

        r = mutant('no-companion', drop_comp)
        record('mutant: companion removed reopens D1 only', (len(r['D1-ledger-companion']) > 0)
               and not r['D2-diagnostic-type'] and not r['D3-recheck-path'], True)

        def wrong_digest(m):
            p = m / COMPANION
            p.write_text(p.read_text().replace(hashlib.sha256(
                (FROZEN / 'base-gate-agreement-ledger.json').read_bytes()).hexdigest(), '0' * 64))

        r = mutant('wrong-digest', wrong_digest)
        record('mutant: wrong ledger digest reopens D1', len(r['D1-ledger-companion']) > 0, True)

        def altered_ledger(m):
            p = m / LEDGER
            p.write_bytes(p.read_bytes().replace(b'"agree"', b'"disagree"', 1))

        r = mutant('altered-ledger', altered_ledger)
        record('mutant: corrected ledger row reopens D1', len(r['D1-ledger-companion']) > 0, True)

        def base_tool(m):
            (m / TOOL).write_bytes((FROZEN / 'base-cache_current_age.py').read_bytes())

        r = mutant('base-tool', base_tool)
        record('mutant: base diagnostic reopens D2 only', (len(r['D2-diagnostic-type']) > 0)
               and not r['D1-ledger-companion'] and not r['D3-recheck-path'], True)

        def junk_prose(m):
            (m / TOOL).write_bytes((FROZEN / 'base-cache_current_age.py').read_bytes())

        r = mutant('junk-prose', junk_prose)
        record('junk control: prose fixed but behavior unchanged leaves 1 open',
               sum(1 for v in r.values() if v), 1)

        def base_entry(m):
            (m / ENTRY).write_bytes((FROZEN / 'base-cache-current-age.md').read_bytes())

        r = mutant('base-entry', base_entry)
        record('mutant: unmodified recheck line reopens D3 only', (len(r['D3-recheck-path']) > 0)
               and not r['D1-ledger-companion'] and not r['D2-diagnostic-type'], True)

        def edited_claim_line(m):
            p = m / ENTRY
            lines = p.read_text().splitlines()
            lines[-3] = lines[-3] + ' edited'
            p.write_text('\n'.join(lines) + '\n')

        r = mutant('edited-claim-line', edited_claim_line)
        record('mutant: an edited claim line reopens D3', len(r['D3-recheck-path']) > 0, True)

        def deleted_line(m):
            p = m / ENTRY
            lines = p.read_text().splitlines()
            del lines[-4]
            p.write_text('\n'.join(lines) + '\n')

        r = mutant('deleted-line', deleted_line)
        record('mutant: a deleted base line reopens D3', len(r['D3-recheck-path']) > 0, True)

        def ephemeral_back(m):
            p = m / ENTRY
            text = p.read_text().replace('recheck: 180d or source/adapter change; reopen',
                                         'recheck: 180d; TMPDIR=/fast/scratch/x reopen')
            p.write_text(text)

        r = mutant('ephemeral-back', ephemeral_back)
        record('mutant: ephemeral recheck token reopens D3', len(r['D3-recheck-path']) > 0, True)

        def no_mktemp(m):
            p = m / ENTRY
            text = p.read_text().replace('mktemp -d', 'mkdir scratch')
            p.write_text(text)

        r = mutant('no-mktemp', no_mktemp)
        record('mutant: non-mktemp offline command reopens D3', len(r['D3-recheck-path']) > 0, True)

    passed = 0
    for label, ok in checks:
        print(('PASS ' if ok else 'FAIL ') + label)
        passed += ok
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
    else:
        if not a.root or not a.revision:
            ap.error('--root and --revision required (or --mirror)')
        rev = subprocess.check_output(['git', '-C', str(a.root), 'rev-parse', f'{a.revision}^{{commit}}'],
                                      text=True).strip()
        read = lambda p: git_bytes(a.root, rev, p)
    result = evaluate(read, a.work)
    open_items = [k for k, v in result.items() if v]
    met = not open_items
    print(f'C1v1 revision={rev} items={len(ITEMS)} open={len(open_items)} '
          f'closed={len(ITEMS) - len(open_items)} met={str(met).lower()}')
    print(json.dumps(result, sort_keys=True))
    return 0 if met else 1


if __name__ == '__main__':
    raise SystemExit(main())
