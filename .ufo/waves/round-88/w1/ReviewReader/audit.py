#!/usr/bin/env python3
"""Reference audit: compare c88_vary.reference to the spec and to its declaration."""
import importlib.util
import json
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
WAVE = LANE / '.ufo/waves/round-88'
SCRATCH = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


counter = load('c88_vary', WAVE / 'c88_vary.py')
indep = load('indep', WAVE / 'w1/ReviewReader/indep.py')

AUDIT = [
    dict(id='A1', vary='accept-encoding,', stored={'accept-encoding': 'gzip'},
         presented={'accept-encoding': 'gzip'},
         declared='silent: the profile names no refusal beyond the CLI contract',
         declared_expect='unspecified',
         spec='match (RFC 9110 5.6.1.2: "A recipient MUST parse and ignore a reasonable number of empty list elements")',
         spec_expect='match'),
    dict(id='A2', vary='accept-encoding',
         stored={'accept-encoding': 'gzip', 'Accept-Encoding': 'br'},
         presented={'accept-encoding': 'gzip', 'Accept-Encoding': 'br'},
         declared='silent on two JSON keys that name one field in different case; nearest clause is "multiple field lines combine in order with \', \'"',
         declared_expect='unspecified',
         spec='match (RFC 9110 5.2: repeated field name value is the line values "concatenated in order, with each field line value separated by a comma")',
         spec_expect='match'),
    dict(id='A3', vary='accept-encoding', stored={'accept-encoding': []},
         presented={'accept-encoding': []},
         declared='silent: [] is not described by the profile',
         declared_expect='unspecified',
         spec='match (zero field lines means the field is absent from both requests)',
         spec_expect='match'),
    dict(id='A4', vary='*,', stored={'accept-encoding': 'gzip'},
         presented={'accept-encoding': 'gzip'},
         declared='v3: "input validation runs before the wildcard rule" (the example names only a malformed header map)',
         declared_expect='invalid',
         spec='mismatch (RFC 9111 4.1: a Vary value containing a member "*" always fails to match; the empty element is ignored first)',
         spec_expect='mismatch'),
    dict(id='A5', vary='x-kake-token', stored={'x-kake-token': 'a\rb'},
         presented={'x-kake-token': 'a b'},
         declared='"values compare byte-identically after trimming leading/trailing SP/HTAB"',
         declared_expect='mismatch',
         spec='match after the required 9110 5.5 transformation, or invalid if the message is rejected: "a recipient of CR, LF, or NUL within a field value MUST either reject the message or replace each of those characters with SP before further processing"',
         spec_expect='match|invalid'),
    dict(id='A6', vary='accept-encoding', stored={'accept-encoding': 'gzip,br'},
         presented={'accept-encoding': ['gzip', 'br']},
         declared='combine with ", " then compare bytes: "gzip,br" vs "gzip, br"',
         declared_expect='mismatch',
         spec='match (RFC 9110 5.6.1.2 accepts "*( OWS \",\" OWS [ element ] )", so OWS around list commas is not significant)',
         spec_expect='match'),
    dict(id='A7', vary='', stored={}, presented={},
         declared='silent',
         declared_expect='unspecified',
         spec='match (empty #field-name list nominates nothing, so nothing can differ)',
         spec_expect='match'),
    dict(id='A8', vary='accept-encoding', stored={'accept-encoding': 'gzip'},
         presented={'accept-encoding': ['gzip', '']},
         declared='combine with ", " -> "gzip, " vs "gzip"',
         declared_expect='mismatch',
         spec='match (an empty element does not contribute to the element count, 9110 5.6.1.2)',
         spec_expect='match'),
    dict(id='A9', vary='accept-encoding, ,accept-language',
         stored={'accept-encoding': 'gzip', 'accept-language': 'en'},
         presented={'accept-encoding': 'gzip', 'accept-language': 'en'},
         declared='silent', declared_expect='unspecified',
         spec='match (OWS-only element is an empty element and is ignored)',
         spec_expect='match'),
    dict(id='A10', vary='Accept-Encoding, accept-encoding',
         stored={'accept-encoding': 'gzip'}, presented={'accept-encoding': 'gzip'},
         declared='duplicate members naming one field compare once',
         declared_expect='match', spec='match', spec_expect='match'),
    dict(id='A12', vary='accept-encoding\n',
         stored={'accept-encoding': 'gzip'}, presented={'accept-encoding': 'br'},
         declared='v3 profiles no LF handling; the reference accepts a trailing LF as a token char',
         declared_expect='match',
         spec='invalid or mismatch; never match (9110 5.5: a recipient "MUST either reject the message or replace each of those characters with SP"; after replacement the member is accept-encoding and its values differ)',
         spec_expect='invalid|mismatch'),
    dict(id='A13', vary='accept-encoding', stored={'accept-encoding\n': 'gzip'},
         presented={'accept-encoding\n': 'gzip'},
         declared='silent', declared_expect='match',
         spec='invalid: a field name ending in LF is not a token',
         spec_expect='invalid'),
    dict(id='A11', vary='accept-encoding',
         stored={'accept-encoding': 'gzip', 'accept encoding': 'x'},
         presented={'accept-encoding': 'gzip'},
         declared='silent', declared_expect='unspecified',
         spec='invalid message (non-token field name), refusal defensible; the nominated field itself matches',
         spec_expect='invalid|match'),
]

rows = []
for item in AUDIT:
    payload = {k: item[k] for k in ('vary', 'stored', 'presented')}
    got = counter.reference(payload['vary'], payload['stored'], payload['presented'])
    try:
        mine = indep.verdict(payload, dict(refuse_empty_elements=False,
                                           refuse_empty_list=False,
                                           refuse_combined_lines=False,
                                           keep_ctl=False, explain=False))[0]
    except indep.Refused:
        mine = 'invalid'
    rows.append(dict(id=item['id'], vary=item['vary'], stored=item['stored'],
                     presented=item['presented'], reference=got,
                     declared_expect=item['declared_expect'],
                     declared_sentence=item['declared'],
                     spec_expect=item['spec_expect'], spec_sentence=item['spec'],
                     indep_default=mine,
                     reference_vs_declared=(got == item['declared_expect']
                                            if item['declared_expect'] != 'unspecified' else 'n/a'),
                     reference_vs_spec=(got == item['spec_expect'])))

receipt = dict(inputs=len(rows),
               reference_matches_declared=sum(1 for r in rows
                                              if r['reference_vs_declared'] is True),
               reference_contradicts_declared=sum(1 for r in rows
                                                  if r['reference_vs_declared'] is False),
               declared_unspecified=sum(1 for r in rows
                                        if r['reference_vs_declared'] == 'n/a'),
               reference_matches_spec=sum(1 for r in rows if r['reference_vs_spec']),
               rows=rows)
(SCRATCH / 'reference-audit.json').write_text(json.dumps(receipt, indent=1, sort_keys=True) + '\n')
print(json.dumps({k: v for k, v in receipt.items() if k != 'rows'}, sort_keys=True))
for r in rows:
    print('%3s ref=%-8s declared=%-11s spec=%-13s %s' % (
        r['id'], r['reference'], r['declared_expect'], r['spec_expect'],
        'CONTRADICTS-DECLARED' if r['reference_vs_declared'] is False else ''))
