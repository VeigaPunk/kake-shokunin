#!/usr/bin/env python3
"""Validate review-packet readiness, never a website's WCAG conformance."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

SCHEMA = 'kake-accessibility-packet-v1'
EXPECTED = 55
FIELDS = {'id', 'title', 'level', 'source', 'sourceQuote', 'publisherCheck',
          'evidenceNeeded', 'failureExample', 'limitation', 'status'}
PROSE = ('publisherCheck', 'evidenceNeeded', 'failureExample', 'limitation')
POPULATION = '.ufo/waves/round-25/population.json'
CARDS = 'corpus/knowledge/accessibility-review-cards.json'
POPULATION_SHA256 = '4751dc24db2e3698c2b276bb81bff57412c8fbf6c1c0a62f1aa2ad9e0f903058'
SOURCE = '.ufo/waves/round-25/source-wcag22.html'
SOURCE_SHA256 = '6e3c5fe397257cae509a2fb4752b73062cf8cbeb92c2cec618989b17e4cf7057'


def normalized(text):
    text = ' '.join(text.split())
    return re.sub(r'(\()\s+', r'\1', re.sub(r'\s+([,.;:)])', r'\1', text))


def result(verdict, accepted=0, criteria=None, findings=None):
    return {'schema': SCHEMA, 'verdict': verdict, 'expected': EXPECTED,
            'accepted': accepted, 'criteria': criteria or [],
            'findings': findings or [], 'websiteConformance': 'not-assessed'}


def validate(population, cards):
    if not isinstance(population, dict) or not isinstance(cards, list):
        return result('could-not-evaluate', findings=['input_invalid']), 2
    rows = population.get('criteria')
    if not isinstance(rows, list) or len(rows) != EXPECTED:
        return result('could-not-evaluate', findings=['population_invalid']), 2
    reference = {}
    for row in rows:
        if not isinstance(row, dict) or not all(isinstance(row.get(k), str)
                and row[k].strip() for k in ('id', 'title', 'level', 'source', 'normativeText')):
            return result('could-not-evaluate', findings=['population_invalid']), 2
        if row['id'] in reference or row['level'] not in ('A', 'AA'):
            return result('could-not-evaluate', findings=['population_invalid']), 2
        reference[row['id']] = row
    buckets = {}
    global_findings = []
    for card in cards:
        if not isinstance(card, dict) or not isinstance(card.get('id'), str):
            global_findings.append('input_invalid')
            continue
        cid = card['id']
        if cid not in reference:
            global_findings.append('metadata_mismatch')
        buckets.setdefault(cid, []).append(card)
    evaluated = []
    for cid, ref in reference.items():
        found = buckets.get(cid, [])
        findings = []
        if not found:
            findings.append('missing_id')
        elif len(found) != 1:
            findings.append('duplicate_id')
        else:
            card = found[0]
            if set(card) != FIELDS:
                findings.append('fields_mismatch')
            if any(card.get(k) != ref[k] for k in ('id', 'title', 'level', 'source')):
                findings.append('metadata_mismatch')
            if any(not isinstance(card.get(k), str) or not card[k].strip() for k in PROSE):
                findings.append('empty_field')
            quote = card.get('sourceQuote')
            if not isinstance(quote, str) or not quote.strip():
                findings.append('empty_field')
            else:
                quote = normalized(quote)
                if len(quote.split()) < 6:
                    findings.append('quote_too_short')
                if len(quote.split()) > 25:
                    findings.append('quote_too_long')
                if not re.search(r'(?<!\w)' + re.escape(quote) + r'(?!\w)',
                                 normalized(ref['normativeText'])):
                    findings.append('quote_not_from_source')
            if card.get('status') != 'not-assessed':
                findings.append('status_not_assessed')
        evaluated.append({'id': cid, 'accepted': not findings,
                          'findings': sorted(set(findings))})
    accepted = sum(row['accepted'] for row in evaluated)
    findings = sorted(set(global_findings + [f for row in evaluated for f in row['findings']]))
    clean = accepted == EXPECTED and not findings and len(cards) == EXPECTED
    return result('clean' if clean else 'failed', accepted, evaluated, findings), 0 if clean else 1


def load(root):
    try:
        raw_population = (root / POPULATION).read_bytes()
        raw_source = (root / SOURCE).read_bytes()
        if (hashlib.sha256(raw_population).hexdigest() != POPULATION_SHA256
                or hashlib.sha256(raw_source).hexdigest() != SOURCE_SHA256):
            return result('could-not-evaluate', findings=['snapshot_tampered']), 2
        population = json.loads(raw_population)
        cards = json.loads((root / CARDS).read_text(encoding='utf-8'))
    except (OSError, UnicodeError, ValueError):
        return result('could-not-evaluate', findings=['input_invalid']), 2
    return validate(population, cards)


def selftest():
    population = {'criteria': [{'id': str(i), 'title': 'Criterion ' + str(i),
        'level': 'A', 'source': 'https://www.w3.org/example#' + str(i),
        'normativeText': 'A grounded source sentence for this criterion.'} for i in range(EXPECTED)]}
    cards = [{**{k: r[k] for k in ('id', 'title', 'level', 'source')},
        'sourceQuote': 'A grounded source sentence for this criterion.', 'publisherCheck': 'Read the complete criterion.',
        'evidenceNeeded': 'Human observations of the named build.',
        'failureExample': 'A missing required alternative.',
        'limitation': 'Preparation only; no website assessed.', 'status': 'not-assessed'}
        for r in population['criteria']]
    cases = [('pristine', cards, 0, None), ('missing', cards[1:], 1, 'missing_id'),
             ('duplicate', cards + [cards[0]], 1, 'duplicate_id')]
    for field in ('id', 'title', 'level', 'source'):
        changed = copy.deepcopy(cards)
        changed[0][field] = 'different'
        cases.append((field, changed, 1, 'metadata_mismatch' if field != 'id' else 'missing_id'))
    for field in PROSE:
        changed = copy.deepcopy(cards)
        changed[0][field] = ' '
        cases.append((field, changed, 1, 'empty_field'))
    for name, field, value, finding in (
        ('long_quote', 'sourceQuote', 'word ' * 26, 'quote_too_long'),
        ('short_quote', 'sourceQuote', 'a', 'quote_too_short'),
        ('heading_quote', 'sourceQuote', 'Criterion 0', 'quote_not_from_source'),
        ('false_result', 'status', 'passed', 'status_not_assessed')):
        changed = copy.deepcopy(cards)
        changed[0][field] = value
        cases.append((name, changed, 1, finding))
    failures = []
    for name, sample, code, finding in cases:
        output, actual = validate(population, sample)
        if actual != code or (finding and finding not in output['findings']):
            failures.append(name)
    invalid, code = validate(population, None)
    if code != 2 or 'input_invalid' not in invalid['findings']:
        failures.append('input_invalid')
    output = {'schema': SCHEMA, 'selftest': True, 'passed': len(cases) + 1 - len(failures),
              'total': len(cases) + 1, 'failures': failures,
              'websiteConformance': 'not-assessed'}
    return output, 1 if failures else 0


class UsageError(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def main(argv=None):
    parser = Parser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    try:
        args = parser.parse_args(argv)
    except UsageError:
        output, code = result('could-not-evaluate', findings=['usage']), 64
    else:
        output, code = selftest() if args.selftest else load(args.root)
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return code


if __name__ == '__main__':
    sys.exit(main())
