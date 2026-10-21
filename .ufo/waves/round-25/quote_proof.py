#!/usr/bin/env python3
"""Show the pre-repair packet quote/pin defects and corrected same-input results."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / '.ufo/waves/round-25'


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def main():
    before_path = BASE / 'before/accessibility_packet.py'
    after_path = ROOT / 'scripts/accessibility_packet.py'
    before = module(before_path, 'packet_before')
    after = module(after_path, 'packet_after')
    population = json.loads((BASE / 'population.json').read_text())
    cards = json.loads((ROOT / 'corpus/knowledge/accessibility-review-cards.json').read_text())
    changed = copy.deepcopy(cards)
    for card in changed:
        card['sourceQuote'] = 'a'
    b, bx = before.validate(population, changed)
    a, ax = after.validate(population, changed)
    with tempfile.TemporaryDirectory(prefix='kake-packet-red-proof-') as tmp:
        target = Path(tmp)
        for relative in (before.POPULATION, before.CARDS, after.SOURCE):
            dest = target / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, dest)
        # Whitespace-only source-population change: same parsed JSON, different pinned bytes.
        p = target / before.POPULATION
        p.write_bytes(p.read_bytes() + b' ')
        pb, pbx = before.load(target)
        pa, pax = after.load(target)
    output = {'beforeSha256': hashlib.sha256(before_path.read_bytes()).hexdigest(),
              'afterSha256': hashlib.sha256(after_path.read_bytes()).hexdigest(),
              'quote': {'before': {'exit': bx, 'accepted': b['accepted'], 'verdict': b['verdict']},
                        'after': {'exit': ax, 'accepted': a['accepted'], 'findings': a['findings']}},
              'populationPin': {'before': {'exit': pbx, 'verdict': pb['verdict']},
                                'after': {'exit': pax, 'findings': pa['findings']}},
              'websiteConformance': 'not-assessed'}
    passed = bx == 0 and ax == 1 and 'quote_too_short' in a['findings'] and pbx == 0 and pax == 2 and pa['findings'] == ['snapshot_tampered']
    output['passed'] = passed
    print(json.dumps(output, sort_keys=True))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
