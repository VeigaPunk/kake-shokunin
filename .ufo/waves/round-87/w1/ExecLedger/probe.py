#!/usr/bin/env python3
"""Bounded source-table extraction and frozen-instrument mutation receipts."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
WAVE = ROOT / '.ufo/waves/round-87'
OUT = WAVE / 'w1/ExecLedger'
FREEZE = '58fee726102aa89ad2c1fa9f697869de3a212510'
receipts = {'axes': {'calibration': '2 HOLD; bounded eight-row agreement',
                     'freshness': '10 HOLD; unchanged by this seat'},
            'commands': [], 'sources': []}

def command(argv):
    p = subprocess.run(argv, cwd=OUT, capture_output=True)
    receipts['commands'].append({'argv': argv, 'cwd': str(OUT),
                                 'exit': p.returncode,
                                 'stdout': p.stdout.decode(),
                                 'stderr': p.stderr.decode()})
    return p

# Freeze identity: compare current input bytes to the specified committed inputs.
for path in [WAVE / 'count.py', WAVE / 'expected-ledger.json'] + sorted((WAVE / 'snapshots').glob('*.md')):
    relative = str(path.relative_to(ROOT))
    p = command(['git', '-C', str(ROOT), 'show', FREEZE + ':' + relative])
    assert p.returncode == 0 and p.stdout == path.read_bytes(), relative

rows = []
for number, required_count in [(84, 3), (85, 2), (86, 3)]:
    source = WAVE / 'snapshots' / ('round-%d-verifier-spotcheck.md' % number)
    raw = source.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    lines = raw.decode().splitlines()
    headers = [i for i, line in enumerate(lines)
               if line.startswith('| Item |') and ('Gate decision' in line or '| Decision |' in line)]
    assert len(headers) == 1, (number, headers)
    observed = []
    for index in range(headers[0] + 2, len(lines)):
        line = lines[index]
        if not line.startswith('|'):
            break
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        assert len(cells) == 5, (number, index + 1)
        item, decision, reopened, agreement, reason = cells
        # Explicit semantic normalization of historical admit/reject annotations.
        normalized = {'admit/mined': 'admit', 'admit (A)': 'admit',
                      'reject proposition': 'reject'}.get(decision, decision)
        assert normalized in ('admit', 'reject'), decision
        outside = agreement.replace('**', '')
        assert outside in ('agree', 'disagree'), outside
        row = {'round': number, 'item': item, 'decision': normalized,
               'outside': outside, 'source': str(source.relative_to(ROOT)),
               'sha256': digest}
        rows.append(row)
        observed.append({'line': index + 1, 'raw_table_row': line,
                         'raw_decision': decision, 'row': row})
    assert len(observed) == required_count, (number, len(observed))
    receipts['sources'].append({'source': str(source), 'sha256': digest,
                                'rows': observed})

# Candidate derives from source tables, never by serializing EXPECTED.
(OUT / 'gate-agreement-ledger.json').write_text(json.dumps(rows, indent=2, ensure_ascii=False) + '\n')
expected = json.loads((WAVE / 'expected-ledger.json').read_text())
ident = lambda row: (row['round'], row['item'])
by_id = {ident(row): row for row in rows}
receipts['comparison'] = {
    'rows': len(rows), 'source_table_counts': [len(s['rows']) for s in receipts['sources']],
    'missing': sum(ident(row) not in by_id for row in expected),
    'disagreement': sum(ident(row) in by_id and by_id[ident(row)] != row for row in expected),
    'extra': sum(ident(row) not in {ident(want) for want in expected} for row in rows),
    'outside_disagree': sum(row['outside'] == 'disagree' for row in rows)}
assert rows == expected
selftest = command([sys.executable, '-B', str(WAVE / 'count.py'), '--selftest'])
assert selftest.returncode == 0
spec = importlib.util.spec_from_file_location('frozen_count', WAVE / 'count.py')
instrument = importlib.util.module_from_spec(spec)
spec.loader.exec_module(instrument)
read_source = lambda path: (ROOT / path).read_bytes()
mutants = {}
mutants['row_omission'] = copy.deepcopy(rows[:3] + rows[4:])
mutants['agree_to_disagree'] = copy.deepcopy(rows)
mutants['agree_to_disagree'][4]['outside'] = 'disagree'
mutants['wrong_source_digest'] = copy.deepcopy(rows)
mutants['wrong_source_digest'][6]['sha256'] = '0' * 64
mutants['duplicated_row'] = copy.deepcopy(rows + [rows[7]])
results = [{'case': 'clean', 'mismatches': instrument.ledger_errors(rows, read_source)}]
assert results[0]['mismatches'] == 0
for name, mutant in mutants.items():
    mismatches = instrument.ledger_errors(mutant, read_source)
    assert mismatches > 0, name
    results.append({'case': name, 'mismatches': mismatches, 'failed_predicate': True})
# Independently corrupt actual source bytes, without changing any source file.
wrong_bytes = instrument.ledger_errors(rows, lambda path: b'not the frozen source snapshot')
assert wrong_bytes == 8
results.append({'case': 'wrong_actual_source_bytes', 'mismatches': wrong_bytes, 'failed_predicate': True})
receipts['instrument_import'] = {'path': str(WAVE / 'count.py'), 'read_only': True,
                                 'bytecode_disabled': sys.dont_write_bytecode}
receipts['mutation_checks'] = results
receipts['candidate_sha256'] = hashlib.sha256((OUT / 'gate-agreement-ledger.json').read_bytes()).hexdigest()
(OUT / 'receipts.json').write_text(json.dumps(receipts, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'comparison': receipts['comparison'], 'mutation_checks': results,
                  'candidate_sha256': receipts['candidate_sha256'], 'selftest_exit': selftest.returncode}, sort_keys=True))
