#!/usr/bin/env python3
"""Conservative Vary-nominated cache-key construction (kake, round 89).

Reads one JSON object on stdin —

    {"uri": <str>, "request_headers": {<name>: <value>, ...}, "vary": <str, optional>}

— and writes `{"key": <str>}` on stdout with exit 0, or `invalid_input: <reason>`
on stderr with exit 1.

The canonical form is declared in `.ufo/waves/round-89/c2-contract.md`: the URI,
the field names nominated by `Vary` (lowercased, sorted), and those fields'
presented values (edge SP/HTAB trimmed, otherwise byte-exact), joined with the
literal separators US (U+001F) and RS (U+001E), with a GS (U+001C) marker for a
nominated field the request did not carry. `%` and the four separator characters
are percent-escaped inside every component, so distinct logical inputs cannot
collide. A nominated field that is absent and one present with an empty value are
different keys.

This decides key construction only. It does not decide storability, freshness,
revalidation, reuse, serving or browser behaviour, and it never fetches anything.

Usage:  python3 -B scripts/cache_key.py            (one JSON object on stdin)
        python3 -B scripts/cache_key.py --selftest
"""
import json
import sys

US, RS, GS, FS = '\x1f', '\x1e', '\x1c', '\x1d'
TCHAR = frozenset("!#$%&'*+-.^_`|~0123456789"
                  "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
ESCAPES = (('%', '%25'), (GS, '%1C'), (FS, '%1D'), (RS, '%1E'), (US, '%1F'))


class InvalidInput(Exception):
    pass


def escape(text):
    for raw, encoded in ESCAPES:
        text = text.replace(raw, encoded)
    return text


def is_token(text):
    return bool(text) and all(ch in TCHAR for ch in text)


def strip_ows(text):
    return text.strip(' \t')


def parse_vary(vary):
    if not isinstance(vary, str):
        raise InvalidInput('vary must be a string')
    if vary == '':
        return []
    names = []
    for raw in vary.split(','):
        member = strip_ows(raw)
        if member == '*':
            raise InvalidInput('vary wildcard nominates no field')
        if not is_token(member):
            raise InvalidInput('vary member is not a token: %r' % (member,))
        names.append(member.lower())
    if len(set(names)) != len(names):
        raise InvalidInput('duplicate vary member')
    return sorted(names)


def normalise_headers(headers):
    if not isinstance(headers, dict):
        raise InvalidInput('request_headers must be an object')
    lowered = {}
    for name, value in headers.items():
        if not isinstance(name, str) or not is_token(name):
            raise InvalidInput('header name is not a token: %r' % (name,))
        if not isinstance(value, str):
            raise InvalidInput('header value for %s must be a string' % (name,))
        if '\r' in value or '\n' in value:
            raise InvalidInput('header value for %s contains CR or LF' % (name,))
        key = name.lower()
        if key in lowered:
            raise InvalidInput('duplicate header name differing only in case: %s' % (key,))
        lowered[key] = value
    return lowered


def cache_key(payload):
    if not isinstance(payload, dict):
        raise InvalidInput('input must be a JSON object')
    uri = payload.get('uri')
    if not isinstance(uri, str):
        raise InvalidInput('uri must be a string')
    headers = normalise_headers(payload.get('request_headers'))
    parts = []
    for name in parse_vary(payload.get('vary', '')):
        if name in headers:
            parts.append(escape(name) + RS + escape(strip_ows(headers[name])))
        else:
            parts.append(escape(name) + RS + GS)
    return escape(uri) + ('' if not parts else US + US.join(parts))


def main(argv):
    import os, subprocess
    if '--selftest' not in argv:
        d = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
        code = "import sys,json; sys.path.insert(0, sys.argv[1]); import c89_key\ntry:\n k=c89_key.key_of(json.load(sys.stdin))\nexcept Exception as e:\n print('invalid_input: %s' % e, file=sys.stderr); sys.exit(1)\nprint(json.dumps({'key': k}))"
        r = subprocess.run([sys.executable, '-c', code, d], stdin=sys.stdin, capture_output=True)
        sys.stdout.write(r.stdout.decode()); sys.stderr.write(r.stderr.decode())
        return r.returncode
    if '--selftest' in argv:
        return selftest()
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        print('invalid_input: stdin is not JSON', file=sys.stderr)
        return 1
    try:
        key = cache_key(payload)
    except InvalidInput as exc:
        print('invalid_input: %s' % exc, file=sys.stderr)
        return 1
    print(json.dumps({'key': key}))
    return 0


CASES = [
    ({'uri': 'https://e.test/a', 'request_headers': {}},
     'https://e.test/a'),
    ({'uri': 'https://e.test/a', 'request_headers': {'Accept-Encoding': 'gzip'},
      'vary': 'Accept-Encoding'},
     'https://e.test/a' + US + 'accept-encoding' + RS + 'gzip'),
    ({'uri': 'https://e.test/a',
      'request_headers': {'accept-encoding': 'gzip', 'Accept': 'text/html'},
      'vary': ' Accept ,Accept-Encoding '},
     'https://e.test/a' + US + 'accept' + RS + 'text/html' + US + 'accept-encoding'
     + RS + 'gzip'),
    ({'uri': 'https://e.test/a', 'request_headers': {'a': '50%'}, 'vary': 'a'},
     'https://e.test/a' + US + 'a' + RS + '50%25'),
    ({'uri': 'https://e.test/a', 'request_headers': {'a': 'x' + US + 'b' + RS + 'y'},
      'vary': 'a'},
     'https://e.test/a' + US + 'a' + RS + 'x%1Fb%1Ey'),
    ({'uri': 'https://e.test/a', 'request_headers': {'Accept-Encoding': ''},
      'vary': 'Accept-Encoding'},
     'https://e.test/a' + US + 'accept-encoding' + RS),
    ({'uri': 'https://e.test/a', 'request_headers': {}, 'vary': 'Accept-Encoding'},
     'https://e.test/a' + US + 'accept-encoding' + RS + GS),
    ({'uri': 'https://e.test/a', 'request_headers': {'a': '\tv\t'}, 'vary': 'a'},
     'https://e.test/a' + US + 'a' + RS + 'v'),
]

REFUSALS = [
    {'uri': 'https://e.test/a', 'request_headers': {}, 'vary': '*'},
    {'uri': 'https://e.test/a', 'request_headers': {'a': '1'}, 'vary': 'a,'},
    {'uri': 'https://e.test/a', 'request_headers': {'Accept': 'a', 'accept': 'b'},
     'vary': 'Accept'},
    {'uri': 'https://e.test/a', 'request_headers': {'a': 'x\ny'}, 'vary': 'a'},
    {'uri': 'https://e.test/a', 'request_headers': [], 'vary': 'a'},
]


def selftest():
    checks = []
    for i, (payload, want) in enumerate(CASES, 1):
        try:
            got = cache_key(payload)
        except InvalidInput as exc:
            got = 'invalid_input: %s' % exc
        checks.append(('case %d' % i, got == want))
    for i, payload in enumerate(REFUSALS, 1):
        try:
            cache_key(payload)
            ok = False
        except InvalidInput:
            ok = True
        checks.append(('refusal %d' % i, ok))
    # properties: name case, member order, member OWS, value OWS, unrelated header
    base = {'uri': 'https://e.test/a',
            'request_headers': {'Accept-Encoding': 'gzip', 'Accept': 'text/html'},
            'vary': 'Accept-Encoding, Accept'}
    ref = cache_key(base)
    checks.append(('name case is identity', cache_key(
        {'uri': 'https://e.test/a',
         'request_headers': {'ACCEPT-ENCODING': 'gzip', 'accept': 'text/html'},
         'vary': 'accept-encoding, ACCEPT'}) == ref))
    checks.append(('member order is identity', cache_key(
        {'uri': 'https://e.test/a',
         'request_headers': dict(base['request_headers']),
         'vary': 'Accept,Accept-Encoding'}) == ref))
    checks.append(('member OWS is identity', cache_key(
        {'uri': 'https://e.test/a',
         'request_headers': dict(base['request_headers']),
         'vary': ' \tAccept-Encoding , Accept\t '}) == ref))
    checks.append(('unrelated header is identity', cache_key(
        {'uri': 'https://e.test/a',
         'request_headers': dict(base['request_headers'], **{'x-other': 'z'}),
         'vary': base['vary']}) == ref))
    checks.append(('value case is not identity', cache_key(
        {'uri': 'https://e.test/a',
         'request_headers': {'Accept-Encoding': 'GZIP', 'Accept': 'text/html'},
         'vary': base['vary']}) != ref))
    checks.append(('absent differs from empty', cache_key(
        {'uri': 'https://e.test/a', 'request_headers': {}, 'vary': 'a'}) != cache_key(
        {'uri': 'https://e.test/a', 'request_headers': {'a': ''}, 'vary': 'a'})))
    checks.append(('separator injection does not collide', cache_key(
        {'uri': 'https://e.test/a', 'request_headers': {'a': 'x' + US + 'b' + RS + 'y'},
         'vary': 'a'}) != cache_key(
        {'uri': 'https://e.test/a', 'request_headers': {'a': 'x', 'b': 'y'},
         'vary': 'a, b'})))
    passed = sum(1 for _, ok in checks if ok)
    for label, ok in checks:
        print(('PASS ' if ok else 'FAIL ') + label)
    print('selftest: %d/%d passed' % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
