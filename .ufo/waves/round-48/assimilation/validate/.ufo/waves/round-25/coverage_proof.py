#!/usr/bin/env python3
"""Check that strengthened packet fixtures detect three local regressions."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / '.ufo/waves/round-25'
PRIOR = '9f62cda0a6b71a9c0c86d2088f01673f25787715'


def main():
    old = subprocess.run(['git', '--no-replace-objects', '-C', str(ROOT), 'show',
        PRIOR + ':.ufo/waves/round-25/packet_selftest.py'], capture_output=True, check=True).stdout
    source = (ROOT / 'scripts/accessibility_packet.py').read_text()
    mutations = {
        'heading_haystack': ("normalized(ref['normativeText'])", "normalized(ref.get('text', ref['normativeText']))"),
        'status_denylist': ("if card.get('status') != 'not-assessed':", "if card.get('status') in ('passed', 'failed', 'inapplicable', 'conformant'):"),
        'loose_cards_json': ("cards = strict_json((root / CARDS).read_text(encoding='utf-8'))", "cards = json.loads((root / CARDS).read_text(encoding='utf-8'))"),
    }
    rows = []
    with tempfile.TemporaryDirectory(prefix='kake-packet-coverage-') as temporary:
        temp = Path(temporary)
        old_test = temp / 'old_selftest.py'
        old_test.write_bytes(old)
        for name, (needle, replacement) in mutations.items():
            if source.count(needle) != 1:
                raise ValueError('mutation site no longer unique: ' + name)
            fixture = temp / name
            for rel in ('.ufo/waves/round-25/population.json', '.ufo/waves/round-25/source-wcag22.html'):
                dst = fixture / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, dst)
            tool = fixture / 'scripts/accessibility_packet.py'
            tool.parent.mkdir(parents=True, exist_ok=True)
            tool.write_text(source.replace(needle, replacement, 1))
            outcomes = {}
            for label, test in (('before', old_test), ('after', BASE / 'packet_selftest.py')):
                proc = subprocess.run([sys.executable, '-B', str(test), '--root', str(fixture)],
                                      capture_output=True, text=True)
                try:
                    output = json.loads(proc.stdout)
                except ValueError:
                    output = {'failures': [{'case': 'output_invalid'}]}
                outcomes[label] = {'exit': proc.returncode, 'stderrEmpty': not proc.stderr,
                    'failedCases': [row['case'] for row in output.get('failures', [])]}
            rows.append({'mutation': name, **outcomes,
                         'caught': outcomes['before']['exit'] == 0 and outcomes['after']['exit'] == 1
                                   and bool(outcomes['after']['failedCases'])})
    passed = all(row['caught'] for row in rows)
    print(json.dumps({'priorTestRevision': PRIOR, 'rows': rows, 'passed': passed,
                      'websiteConformance': 'not-assessed'}, sort_keys=True))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
