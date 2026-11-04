#!/usr/bin/env python3
"""Build a green C1 mirror, then one mutant per item plus extra probes, and score each."""
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path('/fast/scratch/hyaku/kake-r88/MutReader')
LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
COUNTER = LANE / '.ufo/waves/round-88/c88_defect_queue.py'
MIRRORS = HERE / 'mirrors'

spec = importlib.util.spec_from_file_location('c88c1', COUNTER)
C1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C1)


def build(name):
    root = MIRRORS / name
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    C1.mirror_tree(root)
    return root


def patch(root, rel, old, new, encoding=None):
    p = root / rel
    data = p.read_bytes()
    text = data.decode() if encoding is None else data.decode(encoding)
    assert text.count(old) == 1, f'{rel}: anchor count {text.count(old)} for {old[:60]!r}'
    p.write_bytes(text.replace(old, new, 1).encode() if encoding is None else text.replace(old, new, 1).encode(encoding))


def score(root, tag):
    work = HERE / 'work' / f'c1-{tag}'
    argv = [sys.executable, '-B', str(COUNTER), '--mirror', str(root), '--work', str(work)]
    p = subprocess.run(argv, capture_output=True, text=True, timeout=300)
    lines = p.stdout.strip().splitlines()
    row = dict(tag=tag, cmd=' '.join(argv), exit=p.returncode, stdout=p.stdout.strip(),
               stderr=p.stderr.strip())
    row['summary'] = lines[0] if lines else ''
    try:
        row['items'] = json.loads(lines[1]) if len(lines) > 1 else None
    except Exception:
        row['items'] = None
    row['open'] = sorted(k for k, v in (row['items'] or {}).items() if v)
    return row


D1 = 'corpus/knowledge/gate-agreement-metadata.md'
D3 = 'corpus/knowledge/cache-current-age.md'
LEDGER = 'corpus/knowledge/gate-agreement-ledger.json'
TOOL = 'scripts/cache_current_age.py'

# name -> (item, label, [(rel, old, new), ...])
MUTANTS = [
    ('c1_d1_source_path_suffix', 'D1', 'source: names gate-agreement-ledger.json.bak (substring of the ledger path)', [
        (D1, 'source: corpus/knowledge/gate-agreement-ledger.json \u2014',
         'source: corpus/knowledge/gate-agreement-ledger.json.bak \u2014')]),
    ('c1_d1_source_dropped', 'D1', 'source: names no ledger path', [
        (D1, 'source: corpus/knowledge/gate-agreement-ledger.json \u2014 lane metadata ledger;',
         'source: corpus/knowledge/ \u2014 lane metadata ledger;')]),
    ('c1_d1_digest_zeros', 'D1', 'companion quotes 64 zeros instead of the ledger sha256', [
        (D1, 'sha256 ' + hashlib.sha256((C1.FROZEN / 'base-gate-agreement-ledger.json').read_bytes()).hexdigest(),
         'sha256 ' + '0' * 64)]),
    ('c1_d1_ledger_altered', 'D1', 'ledger bytes edited (one decision item retitled)', [
        (LEDGER, '"S457 response max-age semantics"', '"S457 response max-age semantics (edited)"')]),
    ('c1_d1_verified_empty', 'D1', 'verified-at: present but empty', [
        (D1, 'verified-at: 2026-11-04 \u2014 the ledger is a record of closure-owned decisions, not a '
             'domain claim; round-88 counter .ufo/waves/round-88/c88_defect_queue.py.',
         'verified-at:   ')]),

    ('c1_d2_hardcoded_key', 'D2', 'diagnostic always names date_value whatever key is offending', [
        (TOOL, '% (key, "boolean" if', '% ("date_value", "boolean" if')]),
    ('c1_d2_hardcoded_valid', 'D2', 'the valid path is a payload-keyed lookup table', [
        (TOOL, '        result = decode(json.loads(sys.stdin.read(), parse_constant=reject_constant))',
         '        payload = json.loads(sys.stdin.read(), parse_constant=reject_constant)\n'
         '        if payload == {"date_value": 80, "request_time": 90, "response_time": 100, "now": 130, "age_value": 5}:\n'
         '            print(json.dumps({"apparent_age": 20, "response_delay": 10, "corrected_age_value": 15, "corrected_initial_age": 20, "resident_time": 30, "current_age": 50}, separators=(",", ":")))\n'
         '            return 0\n'
         '        result = decode(payload)')]),
    ('c1_d2_vacuous_selftest', 'D2', '--selftest prints a green line and runs zero fixtures', [
        (TOOL, 'def selftest() -> int:\n    """Independent fixtures exercise the actual CLI, not an imported oracle."""',
         'def selftest() -> int:\n    """Independent fixtures exercise the actual CLI, not an imported oracle."""\n'
         '    print("selftest: 0 isolated CLI fixtures passed")\n    return 0')]),
    ('c1_d2_base_message', 'D2', 'float diagnostic reverted to the base boolean message', [
        (TOOL, 'raise ValueError("%s must be an integer, not %s" % (key, "boolean" if isinstance(value, bool) else type(value).__name__))',
         'raise ValueError(f"{key} must be an integer, not boolean")')]),
    ('c1_d2_bool_says_float', 'D2', 'boolean diagnostic also mentions float', [
        (TOOL, '"boolean" if isinstance(value, bool) else type(value).__name__',
         '"boolean, not float" if isinstance(value, bool) else type(value).__name__')]),

    ('c1_d3_zero_cadence', 'D3', 'recheck: 0d (a token that parses as a cadence but is not one)', [
        (D3, 'recheck: 180d or source/adapter change; reopen', 'recheck: 0d; reopen')]),
    ('c1_d3_forbidden_mktemp', 'D3', 'body says the mktemp selftest command is forbidden', [
        (D3, '6. Offline selftest without a fixed scratch path: TMPDIR=$(mktemp -d) python3 -B scripts/cache_current_age.py --selftest; the directory is created by the shell and removed by the operator.',
         '6. Never run TMPDIR=$(mktemp -d) python3 -B scripts/cache_current_age.py --selftest; that command is forbidden in this entry.')]),
    ('c1_d3_iso_date_only', 'D3', 'recheck: a bare fixed ISO date, no cadence word at all', [
        (D3, 'recheck: 180d or source/adapter change; reopen', 'recheck: 2026-11-04 \u2014 opened this round; reopen')]),
    ('c1_d3_base_recheck', 'D3', 'recheck line restored to the base bytes', [
        (D3, 'recheck: 180d or source/adapter change; reopen', 'recheck: TEMPORARY')]),
    ('c1_d3_ephemeral', 'D3', 'recheck line names TMPDIR=/fast/scratch', [
        (D3, 'recheck: 180d or source/adapter change; reopen', 'recheck: 180d; TMPDIR=/fast/scratch/x reopen')]),
    ('c1_d3_no_mktemp', 'D3', 'offline command uses mkdir instead of mktemp -d', [
        (D3, 'TMPDIR=$(mktemp -d)', 'TMPDIR=$(mkdir scratch)')]),
    ('c1_d3_edited_line', 'D3', 'an unrelated base line is edited', [
        (D3, '# Conservative HTTP current-age arithmetic', '# Corrected HTTP current-age arithmetic')]),
    ('c1_d3_two_recheck', 'D3', 'a second recheck: line is appended', [
        (D3, 'recheck: 180d or source/adapter change; reopen', 'recheck: 180d or source/adapter change; reopen')]),
]


def main():
    MIRRORS.mkdir(parents=True, exist_ok=True)
    rows = []
    green = build('green-baseline')
    rows.append(score(green, 'baseline-green'))
    print(f'BASELINE green mirror: exit={rows[0]["exit"]} {rows[0]["summary"]}', flush=True)

    for name, item, label, patches in MUTANTS:
        root = build(name)
        for rel, old, new in patches:
            if name == 'c1_d3_base_recheck':
                (root / rel).write_bytes((C1.FROZEN / 'base-cache-current-age.md').read_bytes())
            elif name == 'c1_d3_two_recheck':
                p = root / rel
                p.write_bytes(p.read_bytes() + b'recheck: 90d or source change\n')
            else:
                patch(root, rel, old, new)
        row = score(root, name)
        row.update(item=item, label=label)
        rows.append(row)
        print(f'{name:26s} {item} exit={row["exit"]} open={row["open"]}', flush=True)

    (HERE / 'receipts' / 'c1_sweep.json').write_text(json.dumps(rows, indent=2, sort_keys=True) + '\n')
    caught = sum(1 for r in rows[1:] if r['exit'] != 0)
    print(f'SUMMARY: {len(rows) - 1} mutants, {caught} caught (exit 1), '
          f'{len(rows) - 1 - caught} not caught')
    return 0


if __name__ == '__main__':
    sys.exit(main())
