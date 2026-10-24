#!/usr/bin/env python3
"""Replay the packet gate against digest-pinned author-prepared inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
FROZEN = ROOT / '.ufo/waves/round-25/frozen'
INPUTS = {'population.json': '.ufo/waves/round-25/population.json',
          'cards.json': 'corpus/knowledge/accessibility-review-cards.json',
          'source-wcag22.html': '.ufo/waves/round-25/source-wcag22.html'}


def replay(root, frozen):
    try:
        expected = json.loads((frozen / 'expected.json').read_text())
        for name in INPUTS:
            data = (frozen / name).read_bytes()
            if hashlib.sha256(data).hexdigest() != expected['sha256'][name]:
                return {'verdict': 'could-not-evaluate', 'finding': 'snapshot_tampered'}, 2
        source = (root / '.ufo/waves/round-25/source-wcag22.html').read_bytes()
        if hashlib.sha256(source).hexdigest() != expected['sourceSha256']:
            return {'verdict': 'could-not-evaluate', 'finding': 'snapshot_tampered'}, 2
    except (OSError, ValueError, KeyError, TypeError):
        return {'verdict': 'could-not-evaluate', 'finding': 'snapshot_unavailable'}, 2
    with tempfile.TemporaryDirectory(prefix='kake-packet-frozen-') as tmp:
        target = Path(tmp)
        for name, rel in INPUTS.items():
            out = target / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes((frozen / name).read_bytes())
        proc = subprocess.run([sys.executable, '-B', str(root / 'scripts/accessibility_packet.py'),
                               '--root', str(target), '--json'], capture_output=True, text=True)
        try:
            actual = json.loads(proc.stdout)
        except ValueError:
            return {'verdict': 'failed', 'finding': 'gate_output_invalid', 'exit': proc.returncode}, 1
        checks = {'exit': proc.returncode == expected['exit'],
                  'accepted': actual.get('accepted') == expected['accepted'],
                  'expected': actual.get('expected') == expected['expected'],
                  'verdict': actual.get('verdict') == 'clean',
                  'websiteConformance': actual.get('websiteConformance') == 'not-assessed',
                  'ids': [r.get('id') for r in actual.get('criteria', [])] == expected['ids'],
                  'all_rows': all(r.get('accepted') is True and r.get('findings') == []
                                  for r in actual.get('criteria', [])),
                  'findings': actual.get('findings') == [],
                  'stderr': not proc.stderr}
        return {'verdict': 'clean' if all(checks.values()) else 'failed',
                'checks': checks, 'accepted': actual.get('accepted'),
                'websiteConformance': 'not-assessed'}, 0 if all(checks.values()) else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--frozen', type=Path, default=FROZEN)
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    if not args.selftest:
        output, code = replay(args.root, args.frozen)
    else:
        output, code = replay(args.root, args.frozen)
        with tempfile.TemporaryDirectory(prefix='kake-packet-pin-test-') as tmp:
            target = Path(tmp) / 'frozen'
            shutil.copytree(args.frozen, target)
            (target / 'cards.json').write_bytes((target / 'cards.json').read_bytes() + b' ')
            changed, changed_code = replay(args.root, target)
        passed = code == 0 and changed_code == 2 and changed.get('finding') == 'snapshot_tampered'
        output, code = {'selftest': True, 'passed': passed,
                        'tamperedExit': changed_code, 'finding': changed.get('finding'),
                        'websiteConformance': 'not-assessed'}, 0 if passed else 1
    print(json.dumps(output, sort_keys=True))
    return code


if __name__ == '__main__':
    sys.exit(main())
