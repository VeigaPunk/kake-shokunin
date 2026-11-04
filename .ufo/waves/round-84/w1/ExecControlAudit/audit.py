import hashlib
import json
import shutil
import subprocess
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
SCRATCH = Path('/fast/scratch/hyaku/kake-r84/ExecControlAudit')
OUT = LANE / '.ufo/waves/round-84/w1/ExecControlAudit'
REL = Path('.ufo/waves/round-84/capture-control')
FREEZE = 'f358022f7e1b2f3846be8ceacbe3a7ef22edf4be'
lines = []
def emit(text):
    lines.append(text)
    print(text, flush=True)

def headers(document):
    result = {}
    for item in document['headers']:
        result.setdefault(item['name'].strip().lower(), []).append(item['value'])
    return result

try:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    expected = json.loads((LANE / '.ufo/waves/round-84/policy-expectations.json').read_text())
    docs = {}
    bodies = {}
    emit('| receipt | method | status | bytes/body length | sha256 (computed and matched) | truncated | headerCount | valid |')
    emit('|---|---|---:|---|---|---|---|---|')
    for pair in ('control', 'equivalent'):
        for side in ('a', 'b'):
            paths = sorted((LANE / REL / pair / side).glob('*/response.json'))
            assert len(paths) == 3
            assert {p.parent.name for p in paths} == set(expected['surfaces'])
            for path in paths:
                d = json.loads(path.read_text())
                body = (path.parent / d['bodyFile']).read_bytes()
                digest = hashlib.sha256(body).hexdigest()
                valid = (d['method'] == 'GET' and type(d['status']) is int and 100 <= d['status'] <= 599
                         and type(d['bytes']) is int and d['bytes'] == len(body)
                         and d['sha256'] == digest and d['truncated'] is False
                         and d['headerCount'] == len(d['headers']))
                key = (pair, side, path.parent.name)
                docs[key], bodies[key] = d, body
                emit(f"| {pair}/{side}/{path.parent.name}/response.json | {d['method']} | {d['status']} | {d['bytes']}/{len(body)} | {digest} | {d['truncated']} | {d['headerCount']}/{len(d['headers'])} | {valid} |")
                assert valid, str(path)
    emit('\n| pair | surface | header | old → new | class |')
    emit('|---|---|---|---|---|')
    actual = {'control': {}, 'equivalent': {}}
    known = {
        ('control', 'ds4cc-primary', 'cache-control'): (['max-age=600'], ['max-age=60'], 'numeric_parameter'),
        ('control', 'ds4cc-robots', 'x-frame-options'): (None, ['SAMEORIGIN'], 'header_added'),
        ('control', 'ds4cc-sitemap', 'referrer-policy'): (['no-referrer, strict-origin'], ['strict-origin, no-referrer'], 'reordered'),
        ('equivalent', 'ds4cc-sitemap', 'referrer-policy'): (['no-referrer, strict-origin'], ['strict-origin, no-referrer'], 'reordered'),
    }
    contract = (LANE / '.ufo/waves/round-84/contract.md').read_text()
    for pair in ('control', 'equivalent'):
        for surface in expected['surfaces']:
            a, b = docs[pair, 'a', surface], docs[pair, 'b', surface]
            ah, bh = headers(a), headers(b)
            assert bodies[pair, 'a', surface] == bodies[pair, 'b', surface]
            assert a['status'] == b['status'] and a['sha256'] == b['sha256']
            assert {k: v for k, v in a.items() if k not in ('headers', 'headerCount')} == {k: v for k, v in b.items() if k not in ('headers', 'headerCount')}
            source = LANE / '.ufo/waves/round-81/capture' / surface
            original = json.loads((source / 'response.json').read_text())
            assert bodies[pair, 'a', surface] == (source / original['bodyFile']).read_bytes()
            assert a['status'] == original['status'] and a['sha256'] == original['sha256']
            for header in sorted(set(ah) | set(bh)):
                if ah.get(header) == bh.get(header):
                    continue
                old, new, cls = known[pair, surface, header]
                assert (ah.get(header), bh.get(header)) == (old, new)
                actual[pair].setdefault(surface, {})[header] = cls
                old_text = 'absent' if old is None else '; '.join(old)
                new_text = 'absent' if new is None else '; '.join(new)
                emit(f'| {pair} | {surface} | {header} | {old_text} → {new_text} | {cls} |')
                row = f'| `{pair}` | `{surface}` | `{header}` | '
                contract_rows = [line for line in contract.splitlines() if line.startswith(row)]
                assert len(contract_rows) == 1 and f'`{cls}`' in contract_rows[0]
                assert f'{old_text if old is None else chr(96)+old_text+chr(96)} → `{new_text}`' in contract_rows[0]
        assert actual[pair] == expected[pair]
        emit(f'{pair}: exact expected changed set; bodies, statuses, digests and every non-header receipt field unchanged; source round-81 bodies/statuses/digests preserved.')
    root = SCRATCH / 'rebuild-copy'
    source_copy = root / '.ufo/waves/round-81/capture'
    shutil.copytree(LANE / '.ufo/waves/round-81/capture', source_copy)
    command = ['python3', '-B', str(LANE / '.ufo/waves/round-84/build_control_pairs.py'), '--root', str(root)]
    result = subprocess.run(command, cwd=SCRATCH, capture_output=True, text=True)
    emit('\nCOMMAND: ' + ' '.join(command))
    emit(f'EXIT: {result.returncode}')
    emit(result.stdout.rstrip())
    if result.stderr:
        emit(result.stderr.rstrip())
    assert result.returncode == 0
    original_files = {p.relative_to(LANE / REL) for p in (LANE / REL).rglob('*') if p.is_file()}
    rebuilt_files = {p.relative_to(root / REL) for p in (root / REL).rglob('*') if p.is_file()}
    assert original_files == rebuilt_files
    emit('\nByte comparisons (cmp against working copy; git show confirms frozen bytes):')
    for relative in sorted(original_files):
        left, right = LANE / REL / relative, root / REL / relative
        cmd = ['cmp', str(left), str(right)]
        compared = subprocess.run(cmd, cwd=SCRATCH, capture_output=True, text=True)
        emit('COMMAND: ' + ' '.join(cmd) + f' ; EXIT: {compared.returncode}')
        assert compared.returncode == 0
        gitcmd = ['git', '-C', str(LANE), 'show', f'{FREEZE}:{REL / relative}']
        frozen = subprocess.run(gitcmd, cwd=SCRATCH, capture_output=True)
        emit('COMMAND: ' + ' '.join(gitcmd) + f' ; EXIT: {frozen.returncode}; frozen_equals_rebuilt={frozen.stdout == right.read_bytes()}')
        assert frozen.returncode == 0 and frozen.stdout == right.read_bytes()
    expectation_rel = Path('.ufo/waves/round-84/policy-expectations.json')
    cmpcmd = ['cmp', str(LANE / expectation_rel), str(root / expectation_rel)]
    result = subprocess.run(cmpcmd, cwd=SCRATCH, capture_output=True)
    emit('COMMAND: ' + ' '.join(cmpcmd) + f' ; EXIT: {result.returncode}')
    assert result.returncode == 0
    emit(f'SUMMARY receipts=12 valid=12 changed_headers=4 pair_files={len(original_files)} cmp_failures=0 frozen_mismatches=0 expectations_match=true')
finally:
    shutil.rmtree(SCRATCH, ignore_errors=True)
    emit(f'SCRATCH_REMOVED={not SCRATCH.exists()}')
    (OUT / 'audit-output.txt').write_text('\n'.join(lines) + '\n')
