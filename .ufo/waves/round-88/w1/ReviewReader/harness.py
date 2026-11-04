#!/usr/bin/env python3
"""ReviewReader round-88 harness: independent table, differential, reference audit.

Reads lane bytes only; writes only JSON receipts into the current scratch dir.
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
WAVE = LANE / '.ufo/waves/round-88'
INDEP = WAVE / 'w1/ReviewReader/indep.py'
COUNTER = WAVE / 'c88_vary.py'
CASES = WAVE / 'vary-cases.json'
SCRATCH = Path(__file__).resolve().parent
PROFILE_FLAGS = ['--refuse-empty-elements', '--refuse-empty-list',
                 '--refuse-combined-lines', '--keep-ctl']
DEFAULT_OPTS = dict(refuse_empty_elements=False, refuse_empty_list=False,
                    refuse_combined_lines=False, keep_ctl=False, explain=False)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


counter = load('c88_vary', COUNTER)
indep = load('indep', INDEP)
FROZEN = json.loads(CASES.read_text())
TABLE = json.loads((SCRATCH / 'expected-table.json').read_text())
TABLE_BY_ID = {row['id']: row for row in TABLE['cases']}


def ref_verdict(payload):
    return counter.reference(payload['vary'], payload['stored'], payload['presented'])


def mine_verdict(payload, **over):
    opts = dict(DEFAULT_OPTS)
    opts.update(over)
    try:
        verdict, reason, checks = indep.verdict(payload, opts)
        return verdict
    except indep.Refused as exc:
        return 'invalid'


def cli_run(tool, payload, flags=()):
    p = subprocess.run([sys.executable, '-B', str(tool)] + list(flags),
                       input=json.dumps(payload), capture_output=True, text=True,
                       timeout=30)
    return p.returncode, p.stdout, p.stderr


def expected_surface(case):
    """(exit, verdict) from a case row (case file or my table)."""
    if case['exit'] == 1:
        return 1, None
    return 0, case['verdict']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ---------------------------------------------------------------- frozen diff
frozen_rows = []
disagreements_table_json = []
for case in FROZEN:
    payload = {k: case[k] for k in ('vary', 'stored', 'presented')}
    row = TABLE_BY_ID[case['id']]
    ref = ref_verdict(payload)
    mine = mine_verdict(payload)
    mine_profile = mine_verdict(payload, refuse_empty_elements=True,
                                refuse_empty_list=True, refuse_combined_lines=True,
                                keep_ctl=True)
    cli_default = cli_run(INDEP, payload)
    cli_profile = cli_run(INDEP, payload, PROFILE_FLAGS)
    ok_table = (row['exit'], row['verdict']) == expected_surface(case)
    if not ok_table:
        disagreements_table_json.append(dict(
            id=case['id'], mine_exit=row['exit'], mine_verdict=row['verdict'],
            file_exit=case['exit'], file_verdict=case['verdict'],
            file_basis=case['basis'], my_basis=row['basis'], my_spec_note=row['spec_note']))
    frozen_rows.append(dict(
        id=case['id'], file=(case['exit'], case['verdict']),
        mine_table=(row['exit'], row['verdict']),
        reference=ref, indep_default=mine, indep_profile=mine_profile,
        cli_default=[cli_default[0], cli_default[1].strip(), cli_default[2].strip()],
        cli_profile=[cli_profile[0], cli_profile[1].strip(), cli_profile[2].strip()],
        table_agrees_file=ok_table, default_agrees_file=(mine == (case['verdict'] or 'invalid')),
        profile_scores_file=(cli_profile[0] == case['exit']
                             and (cli_profile[1].strip() == case['verdict']
                                  if case['exit'] == 0 else cli_profile[1].strip() == ''
                                  and cli_profile[2].startswith('invalid_input:'))),
    ))

frozen_receipt = dict(
    tool_sha256=sha(INDEP), counter_sha256=sha(COUNTER), cases_sha256=sha(CASES),
    table_vs_file=dict(agree=sum(r['table_agrees_file'] for r in frozen_rows),
                       total=len(frozen_rows), disagreements=disagreements_table_json),
    indep_default_vs_file=sum(r['default_agrees_file'] for r in frozen_rows),
    indep_profile_cli_vs_file=sum(r['profile_scores_file'] for r in frozen_rows),
    rows=frozen_rows)
(SCRATCH / 'frozen-compare.json').write_text(json.dumps(frozen_receipt, indent=1, sort_keys=True) + '\n')

# ------------------------------------------------- random population divergence
RANDOM = counter.RANDOM_CASES
CLASS_NOTE = {
    'empty_member': 'Vary list carries an empty element (trailing/extra comma)',
    'empty_vary': 'Vary value is the empty string',
    'empty_list_value': 'a request field value is []',
    'other': 'other input-shape difference',
}


def classify(payload):
    vary = payload['vary']
    if isinstance(vary, str):
        members = [m.strip(' \t') for m in vary.split(',')]
        if members == ['']:
            return 'empty_vary'
        if any(m == '' for m in members):
            return 'empty_member'
    for side in ('stored', 'presented'):
        if any(isinstance(v, list) and not v for v in payload[side].values()):
            return 'empty_list_value'
    return 'other'


div = []
buckets = {}
profile_agree = [0, 0]
profile_mismatch = []
for case in RANDOM:
    payload = {k: case[k] for k in ('vary', 'stored', 'presented')}
    ref = ref_verdict(payload)
    mine = mine_verdict(payload)
    prof = mine_verdict(payload, refuse_empty_elements=True, refuse_empty_list=True,
                        refuse_combined_lines=True, keep_ctl=True)
    profile_same = ref == prof
    profile_agree[0 if profile_same else 1] += 1
    if not profile_same and len(profile_mismatch) < 8:
        profile_mismatch.append(dict(id=case['id'], reference=ref, indep_profile=prof,
                                     vary=payload['vary'], stored=payload['stored'],
                                     presented=payload['presented']))
    if ref != mine:
        cls = classify(payload)
        buckets[cls] = buckets.get(cls, 0) + 1
        if len(div) < 14:
            div.append(dict(id=case['id'], cls=cls, reference=ref, indep_default=mine,
                            vary=payload['vary'], stored=payload['stored'],
                            presented=payload['presented']))
random_receipt = dict(
    total=len(RANDOM), random_sha256=counter.RANDOM_SHA, seed=counter.RANDOM_SEED,
    reference_vs_indep_default=dict(agree=len(RANDOM) - sum(buckets.values()),
                                    disagree=sum(buckets.values()), buckets=buckets),
    reference_vs_indep_profile=dict(agree=profile_agree[0], disagree=profile_agree[1],
                                    examples=profile_mismatch),
    class_note=CLASS_NOTE, examples=div)
(SCRATCH / 'random-divergence.json').write_text(json.dumps(random_receipt, indent=1, sort_keys=True) + '\n')

# --------------------------------------------------------------- fresh inputs
FRESH = [
    dict(id='F1', vary='accept-encoding,', stored={'accept-encoding': 'gzip'},
         presented={'accept-encoding': 'gzip'}, spec='match',
         why='RFC 9110 5.6.1.2 recipient MUST parse and ignore empty list elements'),
    dict(id='F2', vary='accept-encoding,,accept-language',
         stored={'accept-encoding': 'gzip', 'accept-language': 'en'},
         presented={'accept-encoding': 'gzip', 'accept-language': 'en'}, spec='match',
         why='empty middle element is ignored; both nominated fields equal'),
    dict(id='F3', vary='accept-encoding,\taccept-language',
         stored={'accept-encoding': 'gzip', 'accept-language': 'en'},
         presented={'accept-encoding': 'gzip', 'accept-language': 'en'}, spec='match',
         why='HTAB is OWS around list elements'),
    dict(id='F4', vary='accept-encoding',
         stored={'accept-encoding': 'gzip', 'Accept-Encoding': 'br'},
         presented={'accept-encoding': 'gzip', 'Accept-Encoding': 'br'}, spec='match',
         why='two lines of one field name combine in order to "gzip, br" on both sides (9110 5.2)'),
    dict(id='F5', vary='accept-encoding',
         stored={'Accept-Encoding': 'gzip', 'accept-encoding': 'br'},
         presented={'accept-encoding': 'gzip, br'}, spec='match',
         why='combined stored value "gzip, br" equals the single presented line'),
    dict(id='F6', vary='accept-encoding', stored={'accept-encoding': []},
         presented={'accept-encoding': []}, spec='match',
         why='zero field lines means the field is absent from both'),
    dict(id='F7', vary='accept-encoding', stored={'accept-encoding': []},
         presented={}, spec='match', why='[] and {} both mean absent'),
    dict(id='F8', vary='*,', stored={'accept-encoding': 'gzip'},
         presented={'accept-encoding': 'gzip'}, spec='mismatch',
         why='"*" member always fails; the empty element is ignored first'),
    dict(id='F9', vary='*, accept encoding', stored={'accept-encoding': 'gzip'},
         presented={'accept-encoding': 'gzip'}, spec='invalid',
         why='a non-token member makes the Vary value malformed; star precedence is undeclared'),
    dict(id='F10', vary='x-kake-token', stored={'x-kake-token': 'a\rb'},
         presented={'x-kake-token': 'a\rb'}, spec='match',
         why='CR must be replaced with SP before processing; both become "a b"'),
    dict(id='F11', vary='x-kake-token', stored={'x-kake-token': 'a\rb'},
         presented={'x-kake-token': 'a b'}, spec='match',
         why='after the 9110 5.5 replacement the values are identical; the alternative branch is reject-the-message'),
    dict(id='F12', vary='accept-encoding', stored={'accept-encoding': 'gzip,br'},
         presented={'accept-encoding': ['gzip', 'br']}, spec='match',
         why='OWS around list commas is optional (9110 5.6.1.2); the list is the same'),
    dict(id='F13', vary='x-kake-token', stored={'x-kake-token': '"a "'},
         presented={'x-kake-token': '"a"'}, spec='mismatch',
         why='edge-OWS removal cannot reach inside a quoted-string'),
    dict(id='F14', vary='x-kake-token', stored={'x-kake-token': ' '},
         presented={'x-kake-token': ''}, spec='match',
         why='both field values are empty after definitional OWS removal'),
    dict(id='F15', vary='accept-encoding',
         stored={'accept-encoding': 'gzip', 'x-kake-token': 'a'},
         presented={'accept-encoding': 'gzip', 'x-kake-token': 'b'}, spec='match',
         why='a field not nominated by Vary is not compared'),
    dict(id='F16', vary='ACCEPT-ENCODING', stored={'accept-encoding': 'gzip'},
         presented={'Accept-Encoding': 'gzip'}, spec='match',
         why='field names are case-insensitive (9110 5.1)'),
    dict(id='F17', vary='', stored={}, presented={}, spec='match',
         why='an empty #field-name list nominates nothing; nothing can differ'),
    dict(id='F18', vary='accept-encoding', stored={'accept-encoding': 'gzip'},
         presented={'accept-encoding': 'gzip '}, spec='match',
         why='trailing SP is not part of the field value (9110 5.5)'),
    dict(id='F19', vary='authorization', stored={'authorization': 'Bearer AbC'},
         presented={'authorization': 'bearer abc'}, spec='mismatch',
         why='credentials are opaque and case-sensitive; a value-folding reader would match unsoundly'),
    dict(id='F20', vary='user-agent', stored={'user-agent': ['a', 'b']},
         presented={'user-agent': 'a, b'}, spec='match',
         why='two UA lines combine to "a, b" per 9110 5.2'),
    dict(id='F21', vary='x-kake-token', stored={'x-kake-token': 'caf\u00e9'},
         presented={'x-kake-token': 'caf\u00e9'}, spec='match', why='identical obs-text bytes'),
    dict(id='F22', vary='accept-encoding, accept-encoding',
         stored={'accept-encoding': 'gzip'}, presented={'accept-encoding': 'gzip'},
         spec='match', why='duplicate members nominate the same field once'),
]
fresh_rows = []
for case in FRESH:
    payload = {k: case[k] for k in ('vary', 'stored', 'presented')}
    ref = ref_verdict(payload)
    mine = mine_verdict(payload)
    prof = mine_verdict(payload, refuse_empty_elements=True, refuse_empty_list=True,
                        refuse_combined_lines=True, keep_ctl=True)
    cli = cli_run(INDEP, payload)
    fresh_rows.append(dict(id=case['id'], vary=case['vary'], stored=case['stored'],
                           presented=case['presented'], spec_expect=case['spec'],
                           why=case['why'], reference=ref,
                           indep_default=mine, indep_profile=prof,
                           cli=[cli[0], cli[1].strip(), cli[2].strip()],
                           ref_vs_spec=(ref == case['spec']),
                           indep_vs_spec=(mine == case['spec'])))
fresh_receipt = dict(inputs=len(FRESH),
                     reference_agrees_spec=sum(r['ref_vs_spec'] for r in fresh_rows),
                     indep_default_agrees_spec=sum(r['indep_vs_spec'] for r in fresh_rows),
                     rows=fresh_rows)
(SCRATCH / 'fresh.json').write_text(json.dumps(fresh_receipt, indent=1, sort_keys=True) + '\n')

# ------------------------------------------------------------- attack: oracle
OWS = ' \t'
CTL = ('\r', '\n', '\x00')


def canon(lines):
    """Significant bytes: 9110 5.5 CTL->SP, per-line edge OWS, comma join, OWS round commas."""
    out = []
    for line in lines:
        for bad in CTL:
            line = line.replace(bad, ' ')
        out.append(line.strip(OWS))
    text = ','.join(out)
    return re.sub(r'[ \t]*,[ \t]*', ',', text)


def side_lines(side, name):
    """All field lines for `name` in one request side, in document order."""
    if not isinstance(side, dict):
        return None
    lines = []
    for key, value in side.items():
        if not isinstance(key, str) or key.lower() != name:
            continue
        if isinstance(value, str):
            lines.append(value)
        elif isinstance(value, list) and all(isinstance(v, str) for v in value):
            lines.extend(value)
        else:
            return None
    return lines


def unsound_match(payload):
    """Return a reason if a 'match' verdict is not backed by significant-byte equality."""
    try:
        names, star = indep.parse_vary(payload['vary'], False)
    except indep.Refused:
        return None
    except Exception:
        return None
    if star:
        return 'match emitted although Vary has a "*" member'
    for name in dict.fromkeys(names):
        left = side_lines(payload['stored'], name)
        right = side_lines(payload['presented'], name)
        if left is None or right is None:
            continue
        if not left and not right:
            continue
        if not left or not right:
            return 'match emitted although %r is present on one side only' % name
        if canon(left) != canon(right):
            return ('match emitted although %r differs significantly: %r vs %r'
                    % (name, canon(left), canon(right)))
    return None


rng = __import__('random').Random(88_777)
POOL_NAMES = ['accept-encoding', 'accept-language', 'user-agent', 'authorization',
              'x-kake-token', 'Accept-Encoding', 'ACCEPT-LANGUAGE', 'user-Agent']
POOL_VALUES = ['gzip', 'GZip', 'br', 'en-US', 'en', 'a', 'A', ' gzip ', 'gzip;q=1',
               'gzip; q=1', 'gzip, br', 'gzip,br', 'br, gzip', '', ' ', '\tgzip\t',
               'Bearer AbC', 'bearer abc', 'a\rb', 'a b', '"a "', '"a"', 'caf\u00e9',
               'cafe\u0301', 'x' * 40, '*,', 'a\tb']
ATTACK = []
for _ in range(20000):
    members = rng.sample(['accept-encoding', 'accept-language', 'user-agent',
                          'authorization', 'x-kake-token', '*', '', 'accept encoding',
                          'Accept-Encoding'], rng.randint(1, 4))
    vary = (', ' if rng.random() < 0.6 else ',').join(members)
    if rng.random() < 0.10:
        vary += ','
    stored, presented = {}, {}
    for name in ['accept-encoding', 'accept-language', 'user-agent', 'authorization',
                 'x-kake-token', 'Accept-Encoding']:
        roll = rng.random()
        if roll < 0.55:
            value = rng.choice(POOL_VALUES)
            stored[name] = value
            kind = rng.random()
            if kind < 0.30:
                presented[name] = value
            elif kind < 0.45:
                presented[name] = [value]
            elif kind < 0.60:
                presented[name] = [value, rng.choice(POOL_VALUES)]
            elif kind < 0.70:
                presented[name] = []
            elif kind < 0.85:
                presented[name] = rng.choice(POOL_VALUES)
            else:
                pass
        elif roll < 0.62:
            presented[name] = rng.choice(POOL_VALUES)
        elif roll < 0.66:
            stored[name] = []
    ATTACK.append(dict(vary=vary, stored=stored, presented=presented))

violations = []
match_counts = {'reference': 0, 'indep_default': 0}
for payload in ATTACK:
    ref = ref_verdict(payload)
    mine = mine_verdict(payload)
    if ref == 'match':
        match_counts['reference'] += 1
        why = unsound_match(payload)
        if why:
            violations.append(dict(who='reference', why=why, payload=payload))
    if mine == 'match':
        match_counts['indep_default'] += 1
        why = unsound_match(payload)
        if why:
            violations.append(dict(who='indep_default', why=why, payload=payload))

# unsound match a permissive value-folding reader would emit
permissive = dict(vary='authorization', stored={'authorization': 'Bearer AbC'},
                  presented={'authorization': 'bearer abc'})
attack_receipt = dict(
    population=len(ATTACK), seed=88_777, match_counts=match_counts,
    violations=violations[:10], violation_count=len(violations),
    permissive_reader_example=dict(
        payload=permissive,
        value_folding_verdict='match (unsound: RFC 9110 11.6.2 credentials are opaque and case-sensitive)',
        reference=counter.reference(permissive['vary'], permissive['stored'],
                                    permissive['presented']),
        indep_default=mine_verdict(permissive)))
(SCRATCH / 'attack.json').write_text(json.dumps(attack_receipt, indent=1, sort_keys=True) + '\n')

print(json.dumps(dict(
    frozen=dict(table=sum(r['table_agrees_file'] for r in frozen_rows),
                default=sum(r['default_agrees_file'] for r in frozen_rows),
                profile=sum(r['profile_scores_file'] for r in frozen_rows)),
    random=random_receipt['reference_vs_indep_default'],
    fresh=dict(ref=fresh_receipt['reference_agrees_spec'],
               mine=fresh_receipt['indep_default_agrees_spec'],
               n=fresh_receipt['inputs']),
    attack=dict(pop=len(ATTACK), matches=match_counts, viol=len(violations)),
    random_profile=random_receipt['reference_vs_indep_profile']['agree']),
    sort_keys=True))
