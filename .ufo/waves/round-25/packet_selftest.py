#!/usr/bin/env python3
"""Exercise the offline accessibility-packet CLI with isolated fixtures."""
import argparse
import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

EXPECTED = 55
SCHEMA = 'kake-accessibility-packet-v1'
POPULATION = Path('.ufo/waves/round-25/population.json')
CARDS = Path('corpus/knowledge/accessibility-review-cards.json')
SOURCE = Path('.ufo/waves/round-25/source-wcag22.html')
FIELDS = {
    'id', 'title', 'level', 'source', 'sourceQuote', 'publisherCheck',
    'evidenceNeeded', 'failureExample', 'limitation', 'status',
}
ABSENT = object()
DEFAULT = object()


def prefix_words(text, count):
    """Return a contiguous source substring containing at most count tokens."""
    matches = list(re.finditer(r'\S+', text))
    if not matches:
        raise ValueError('population criterion has no normative text')
    end = matches[min(count, len(matches)) - 1].end()
    return text[matches[0].start():end]


def load_source(root):
    population_path = root / POPULATION
    raw = population_path.read_bytes()
    source_raw = (root / SOURCE).read_bytes()
    population = json.loads(raw.decode('utf-8'))
    criteria = population.get('criteria') if isinstance(population, dict) else None
    if not isinstance(criteria, list) or len(criteria) != EXPECTED:
        raise ValueError('pinned population must contain exactly 55 criteria')

    ids = []
    cards = []
    for criterion in criteria:
        if not isinstance(criterion, dict):
            raise ValueError('pinned population contains a non-object criterion')
        for key in ('id', 'title', 'level', 'source', 'normativeText'):
            if not isinstance(criterion.get(key), str) or not criterion[key].strip():
                raise ValueError('pinned population criterion lacks nonempty ' + key)
        ids.append(criterion['id'])
        card = {
            'id': criterion['id'],
            'title': criterion['title'],
            'level': criterion['level'],
            'source': criterion['source'],
            'sourceQuote': prefix_words(criterion['normativeText'], 10),
            'publisherCheck': 'Review the relevant publisher content manually against this criterion.',
            'evidenceNeeded': 'Retain review notes and evidence for the examined content.',
            'failureExample': 'The reviewed content does not meet the applicable criterion.',
            'limitation': 'Preparation for manual review only; no website has been evaluated.',
            'status': 'not-assessed',
        }
        if set(card) != FIELDS:
            raise ValueError('hand-authored packet fields do not match the fixed schema')
        cards.append(card)
    if len(set(ids)) != EXPECTED:
        raise ValueError('pinned population criterion ids must be unique')
    return raw, source_raw, population, ids, cards


def changed(cards, index, field, value):
    result = copy.deepcopy(cards)
    result[index][field] = value
    return result


def write_fixture_value(path, value):
    if value is ABSENT:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, bytes):
        path.write_bytes(value)
    else:
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def make_fixture(base, case):
    root = base / case['name']
    write_fixture_value(root / POPULATION, case['population'])
    write_fixture_value(root / SOURCE, case['source'])
    write_fixture_value(root / CARDS, case['cards'])
    return root


def check_payload(case, payload, ids):
    expected_fields = {
        'schema', 'verdict', 'expected', 'accepted', 'criteria', 'findings',
        'websiteConformance',
    }
    if not isinstance(payload, dict) or set(payload) != expected_fields:
        raise AssertionError('JSON object does not have the exact packet output fields')
    if payload['schema'] != SCHEMA:
        raise AssertionError('wrong schema: ' + repr(payload['schema']))
    if payload['expected'] != EXPECTED:
        raise AssertionError('expected count is not 55')
    if payload['websiteConformance'] != 'not-assessed':
        raise AssertionError('websiteConformance is not not-assessed')
    accepted = payload['accepted']
    if type(accepted) is not int or not 0 <= accepted <= EXPECTED:
        raise AssertionError('accepted is outside the 0..55 integer range')

    findings = payload['findings']
    if not isinstance(findings, list) or any(not isinstance(item, str) for item in findings):
        raise AssertionError('global findings are not a list of stable ids')
    if findings != sorted(set(findings)):
        raise AssertionError('global findings are not sorted and unique')
    if findings != case['findings']:
        raise AssertionError('findings were %r, expected %r' % (findings, case['findings']))

    criteria = payload['criteria']
    if not isinstance(criteria, list):
        raise AssertionError('criteria is not a list')
    for row in criteria:
        if not isinstance(row, dict) or set(row) != {'id', 'accepted', 'findings'}:
            raise AssertionError('criterion result does not have the exact row fields')
        if not isinstance(row['id'], str) or not isinstance(row['accepted'], bool):
            raise AssertionError('criterion result has an invalid id or accepted value')
        row_findings = row['findings']
        if not isinstance(row_findings, list) or any(not isinstance(item, str) for item in row_findings):
            raise AssertionError('criterion findings are not a list of stable ids')
        if row_findings != sorted(set(row_findings)):
            raise AssertionError('criterion findings are not sorted and unique')

    if payload['verdict'] != case['verdict']:
        raise AssertionError('verdict was %r, expected %r' % (payload['verdict'], case['verdict']))
    if case['criteria_rows']:
        if [row['id'] for row in criteria] != ids:
            raise AssertionError('criterion result ids/order do not match the pinned population')
        if case['exit'] == 2:
            if accepted != 0 or any(row['accepted'] or row['findings'] != ['input_invalid']
                                    for row in criteria):
                raise AssertionError('invalid cards should reject every populated criterion')
        else:
            counted = sum(row['accepted'] for row in criteria)
            if counted != accepted:
                raise AssertionError('accepted total does not match criterion rows')
            if case['exit'] == 0 and (
                    accepted != EXPECTED or any(row['findings'] for row in criteria)):
                raise AssertionError('pristine packet did not accept all 55 criteria without findings')
            if case.get('expected_accepted') is not None:
                if accepted != case['expected_accepted']:
                    raise AssertionError('accepted total does not match the fixture expectation')
            elif case['exit'] == 1 and accepted >= EXPECTED:
                raise AssertionError('invalid packet was accepted as all 55 criteria')
    elif criteria or accepted != 0:
        raise AssertionError('unavailable population/snapshot should have no rows and zero accepted')


def build_cases(population_raw, source_raw, population, ids, cards):
    cases = []

    def add(name, exit_code, finding_ids, case_cards=DEFAULT,
            case_population=DEFAULT, case_source=DEFAULT, criteria_rows=True):
        cases.append({
            'name': name,
            'exit': exit_code,
            'verdict': {0: 'clean', 1: 'failed', 2: 'could-not-evaluate'}[exit_code],
            'findings': sorted(finding_ids),
            'cards': cards if case_cards is DEFAULT else case_cards,
            'population': population_raw if case_population is DEFAULT else case_population,
            'source': source_raw if case_source is DEFAULT else case_source,
            'criteria_rows': criteria_rows,
        })

    # An isolated, hand-authored packet gives the clean control without relying on
    # the candidate corpus being present or mutating it.
    add('pristine55', 0, [], cards)
    add('cards_absent', 2, ['input_invalid'], ABSENT, criteria_rows=False)
    add('cards_malformed_json', 2, ['input_invalid'], b'{', criteria_rows=False)
    add('cards_wrong_top_level', 2, ['input_invalid'], {'cards': cards}, criteria_rows=False)

    normalized_cards = copy.deepcopy(cards)
    normalized_row = next((row for row in population['criteria'] if row['id'] == '1.2.4'), None)
    normalized_card = next((card for card in normalized_cards if card['id'] == '1.2.4'), None)
    normalized_quote = 'Captions are provided for all live audio content in synchronized media.'
    if normalized_row is None or normalized_card is None or (
            'Captions are provided for all live audio content in synchronized media .' not in
            normalized_row['normativeText']):
        raise ValueError('pinned population no longer contains the normalized 1.2.4 quote fixture')
    normalized_card['sourceQuote'] = normalized_quote
    add('quote_punctuation_whitespace', 0, [], normalized_cards)

    add('population_absent', 2, ['input_invalid'], cards, ABSENT, criteria_rows=False)
    add('population_malformed_json', 2, ['snapshot_tampered'], cards, b'{', criteria_rows=False)
    add('population_snapshot_tampered', 2, ['snapshot_tampered'],
        cards, population_raw + b'\\n', criteria_rows=False)
    add('source_snapshot_tampered', 2, ['snapshot_tampered'],
        cards, case_source=source_raw + b'\\n', criteria_rows=False)

    duplicate = copy.deepcopy(cards)
    duplicate.append(copy.deepcopy(cards[0]))
    add('duplicate_id', 1, ['duplicate_id'], duplicate)
    add('missing_id', 1, ['missing_id'], cards[:-1])
    obsolete = copy.deepcopy(cards)
    obsolete.append({**cards[0], 'id': '4.1.1', 'title': 'Parsing'})
    add('obsolete_extra_id', 1, ['metadata_mismatch'], obsolete)
    cases[-1]['expected_accepted'] = EXPECTED

    changed_id = changed(cards, 0, 'id', '9.9.9')
    add('changed_id', 1, ['metadata_mismatch', 'missing_id'], changed_id)
    for field in ('title', 'level', 'source'):
        add('changed_' + field, 1, ['metadata_mismatch'], changed(cards, 0, field, 'different'))

    extra_field = copy.deepcopy(cards)
    extra_field[0]['unexpected'] = 'not part of the card schema'
    add('fields_mismatch', 1, ['fields_mismatch'], extra_field)
    add('empty_prose', 1, ['empty_field'], changed(cards, 0, 'publisherCheck', ''))

    longest = max(population['criteria'], key=lambda row: len(row['normativeText'].split()))
    if len(longest['normativeText'].split()) < 26:
        raise ValueError('pinned population has no criterion with 26 normative words')
    long_quote = copy.deepcopy(cards)
    quote_index = ids.index(longest['id'])
    long_quote[quote_index]['sourceQuote'] = prefix_words(longest['normativeText'], 26)
    add('quote_too_long', 1, ['quote_too_long'], long_quote)

    short_quote = changed(cards, 0, 'sourceQuote',
                          prefix_words(population['criteria'][0]['normativeText'], 1))
    add('quote_too_short', 1, ['quote_too_short'], short_quote)

    partial_words = copy.deepcopy(cards)
    first_words = list(re.finditer(r'\S+', population['criteria'][0]['normativeText']))
    if len(first_words) < 6 or first_words[0].end() - first_words[0].start() < 2 or (
            first_words[5].end() - first_words[5].start() < 2):
        raise ValueError('pinned criterion cannot provide a six-word boundary fixture')
    source_text = population['criteria'][0]['normativeText']
    partial_words[0]['sourceQuote'] = source_text[
        first_words[0].start() + 1:first_words[5].end() - 1]
    add('quote_partial_word_boundary', 1, ['quote_not_from_source'], partial_words)

    not_source = copy.deepcopy(cards)
    fabricated_quote = 'This quotation is deliberately absent from the normative criterion.'
    source_text = population['criteria'][0]['normativeText']
    while fabricated_quote in source_text:
        fabricated_quote += ' unique'
    not_source[0]['sourceQuote'] = fabricated_quote
    add('quote_not_from_source', 1, ['quote_not_from_source'], not_source)
    for status in ('passed', 'failed', 'inapplicable', 'conformant'):
        add('status_' + status, 1, ['status_not_assessed'], changed(cards, 0, 'status', status))
    return cases


def run_case(case, packet_tool, fixture_base, ids):
    fixture_root = make_fixture(fixture_base, case)
    command = [
        sys.executable, '-B', str(packet_tool), '--root', str(fixture_root), '--json',
    ]
    completed = subprocess.run(
        command, capture_output=True, text=True, check=False, timeout=30,
    )
    if completed.returncode != case['exit']:
        raise AssertionError('exit was %d, expected %d' % (completed.returncode, case['exit']))
    try:
        payload = json.loads(completed.stdout)
    except (TypeError, ValueError) as error:
        raise AssertionError('CLI did not emit one JSON result: ' + str(error)) from error
    check_payload(case, payload, ids)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path, help='repository root')
    args = parser.parse_args(argv)
    root = args.root.expanduser().resolve()
    packet_tool = root / 'scripts/accessibility_packet.py'
    if not packet_tool.is_file():
        print('packet selftest: missing production CLI: ' + str(packet_tool), file=sys.stderr)
        return 1
    try:
        population_raw, source_raw, population, ids, cards = load_source(root)
        cases = build_cases(population_raw, source_raw, population, ids, cards)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        print('packet selftest: unusable pinned fixture source: ' + str(error), file=sys.stderr)
        return 1

    failures = []
    with tempfile.TemporaryDirectory(prefix='kake-accessibility-packet-selftest-') as temporary:
        fixture_base = Path(temporary)
        for case in cases:
            try:
                run_case(case, packet_tool, fixture_base, ids)
            except (AssertionError, OSError, subprocess.SubprocessError) as error:
                failures.append({'case': case['name'], 'error': str(error)})

    report = {
        'schema': 'kake-accessibility-packet-selftest-v1',
        'passed': len(cases) - len(failures),
        'total': len(cases),
        'failures': failures,
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
