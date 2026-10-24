#!/usr/bin/env python3
"""Check one packet implementation against the same quote/pin repair oracle."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / '.ufo/waves/round-25'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--validator', required=True, type=Path)
    args = parser.parse_args()
    path = args.validator.resolve()
    spec = importlib.util.spec_from_file_location('packet_probe', path)
    packet = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(packet)
    population = json.loads((BASE / 'population.json').read_text())
    cards = json.loads((ROOT / 'corpus/knowledge/accessibility-review-cards.json').read_text())
    changed = copy.deepcopy(cards)
    for card in changed:
        card['sourceQuote'] = 'a'
    quote, quote_exit = packet.validate(population, changed)
    with tempfile.TemporaryDirectory(prefix='kake-packet-red-proof-') as temporary:
        target = Path(temporary)
        for relative in (packet.POPULATION, packet.CARDS, '.ufo/waves/round-25/source-wcag22.html'):
            dest = target / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, dest)
        # Use the preserved literal-quote control for both implementations;
        # later punctuation cleanup must not contaminate the pin-only witness.
        (target / packet.CARDS).write_bytes((BASE / 'frozen/cards.json').read_bytes())
        # Same parsed population, different pinned bytes; only the implementation differs.
        p = target / packet.POPULATION
        p.write_bytes(p.read_bytes() + b' ')
        pin, pin_exit = packet.load(target)
    checks = {'substantiveQuote': quote_exit == 1 and 'quote_too_short' in quote['findings'],
              'populationPin': pin_exit == 2 and pin['findings'] == ['snapshot_tampered']}
    passed = all(checks.values())
    output = {'validatorSha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'checks': checks, 'passed': passed,
              'quote': {'exit': quote_exit, 'accepted': quote['accepted'], 'findings': quote['findings']},
              'populationPin': {'exit': pin_exit, 'findings': pin['findings']},
              'websiteConformance': 'not-assessed'}
    print(json.dumps(output, sort_keys=True))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
