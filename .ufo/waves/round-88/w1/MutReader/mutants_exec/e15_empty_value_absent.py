#!/usr/bin/env python3
"""Conservative Vary-match reader — round 88 C2 candidate (seat ExecReader).

Local adapter contract:
  stdin  : one JSON object {"vary": <string>, "stored": {name: value|list},
                            "presented": {name: value|list}}
  exit 0, stdout exactly "match"    -> the stored response may be considered
                                       to match the presented request
  exit 0, stdout exactly "mismatch" -> it may not
  exit 1, stdout empty, stderr beginning "invalid_input:" -> input refused

Declared profile (contract.md, C2):
  * field names compare ASCII case-insensitively;
  * nominated names are deduplicated;
  * several field lines for one name, given as a JSON array, combine in order
    with ', ';
  * values compare byte-identically after trimming leading/trailing SP and
    HTAB only (no value case-folding, no reordering, no internal whitespace
    folding);
  * a nominated field absent from both requests matches; absent from one it
    does not;
  * any '*' member always fails to match;
  * non-string Vary or field values, non-token members, empty members and an
    empty Vary are refused, as are a non-object request map and an ambiguous
    case-variant duplicate field name.

Precedence (freeze amendment v3, contract.md): the Vary value and both request
maps are validated before the wildcard rule is applied, so a malformed header
map is refused even when the Vary value contains '*'. A malformed Vary value is
likewise refused before the star is resolved.

This reader performs no cache-key construction, storage, revalidation,
freshness or serving behaviour: it only answers the RFC 9111 section 4.1 match
question for the fields Vary nominates, conservatively.
"""
import json
import os
import subprocess
import sys

OWS = ' \t'
TCHAR = frozenset("!#$%&'*+-.^_`|~"
                  '0123456789'
                  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                  'abcdefghijklmnopqrstuvwxyz')
ASCII_LOWER = str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                            'abcdefghijklmnopqrstuvwxyz')


def is_token(text):
    """RFC 9110 token: one or more tchar, ASCII only, nothing else."""
    return (isinstance(text, str) and text != ''
            and all(ch in TCHAR for ch in text))


def ascii_lower(text):
    return text.translate(ASCII_LOWER)


def parse_vary(vary):
    """Return (deduplicated lowercase names, saw_star, None) or (None, False, reason)."""
    members = [member.strip(OWS) for member in vary.split(',')]
    names, seen, star = [], set(), False
    for member in members:
        if member == '':
            return None, False, 'empty Vary member (empty Vary or a bare comma)'
        if member == '*':
            star = True
            continue
        if not is_token(member):
            return None, False, f'Vary member {member!r} is not a token'
        low = ascii_lower(member)
        if low not in seen:
            seen.add(low)
            names.append(low)
    return names, star, None


def normalise_request(side, label):
    """Return a lowercase-name -> combined value map, or (None, reason)."""
    if not isinstance(side, dict):
        return None, f'{label} request must be a JSON object'
    out = {}
    for key, value in side.items():
        if not is_token(key):
            return None, f'{label} field name {key!r} is not a token'
        low = ascii_lower(key)
        if low in out:
            return None, (f'{label} field name {key!r} is an ambiguous '
                          f'case-variant duplicate')
        if isinstance(value, str):
            if value.strip(OWS):
                out[low] = value
        elif isinstance(value, list) and value and all(isinstance(v, str) for v in value):
            out[low] = ', '.join(value)
        else:
            return None, (f'{label} field {key!r} value must be a string or a '
                          f'non-empty array of strings')
    return out, None


def decide(payload):
    """Return (verdict, None) with verdict in {'match', 'mismatch'}, or (None, reason)."""
    if not isinstance(payload, dict):
        return None, 'input must be a single JSON object'
    vary = payload.get('vary')
    if not isinstance(vary, str):
        return None, f'vary must be a string, not {type(vary).__name__}'
    names, star, reason = parse_vary(vary)
    if reason is not None:
        return None, reason
    stored, reason = normalise_request(payload.get('stored'), 'stored')
    if reason is not None:
        return None, reason
    presented, reason = normalise_request(payload.get('presented'), 'presented')
    if reason is not None:
        return None, reason
    if star:
        return 'mismatch', None
    for name in names:
        left = stored.get(name)
        right = presented.get(name)
        if left is None and right is None:
            continue
        if left is None or right is None:
            return 'mismatch', None
        if left.strip(OWS) != right.strip(OWS):
            return 'mismatch', None
    return 'match', None


def refuse(reason):
    sys.stderr.write(f'invalid_input: {reason}\n')
    return 1


SELFTEST_CASES = [
    ('identical field values match',
     {'vary': 'accept-encoding', 'stored': {'accept-encoding': 'gzip'},
      'presented': {'accept-encoding': 'gzip'}}, 'match'),
    ('field names compare case-insensitively',
     {'vary': 'Accept-Encoding', 'stored': {'accept-encoding': 'gzip'},
      'presented': {'ACCEPT-ENCODING': 'gzip'}}, 'match'),
    ('field values are not case-folded',
     {'vary': 'accept-encoding', 'stored': {'accept-encoding': 'gzip'},
      'presented': {'accept-encoding': 'GZip'}}, 'mismatch'),
    ('a nominated field absent from both requests matches',
     {'vary': 'accept-encoding', 'stored': {}, 'presented': {}}, 'match'),
    ('a nominated field absent from stored does not match',
     {'vary': 'accept-encoding', 'stored': {},
      'presented': {'accept-encoding': 'gzip'}}, 'mismatch'),
    ('a nominated field absent from presented does not match',
     {'vary': 'accept-encoding', 'stored': {'accept-encoding': 'gzip'},
      'presented': {}}, 'mismatch'),
    ('a lone star member never matches',
     {'vary': '*', 'stored': {'accept-encoding': 'gzip'},
      'presented': {'accept-encoding': 'gzip'}}, 'mismatch'),
    ('a star member dominates an otherwise matching list',
     {'vary': 'accept-encoding, *', 'stored': {'accept-encoding': 'gzip'},
      'presented': {'accept-encoding': 'gzip'}}, 'mismatch'),
    ('leading and trailing SP/HTAB are trimmed',
     {'vary': 'accept-encoding', 'stored': {'accept-encoding': ' \tgzip\t '},
      'presented': {'accept-encoding': 'gzip'}}, 'match'),
    ('a value that is only OWS equals the empty value',
     {'vary': 'x-kake-token', 'stored': {'x-kake-token': ' \t '},
      'presented': {'x-kake-token': ''}}, 'match'),
    ('list reordering is not applied',
     {'vary': 'accept-encoding', 'stored': {'accept-encoding': 'gzip, br'},
      'presented': {'accept-encoding': 'br, gzip'}}, 'mismatch'),
    ('every nominated field must match',
     {'vary': 'accept-encoding, accept-language',
      'stored': {'accept-encoding': 'gzip', 'accept-language': 'en'},
      'presented': {'accept-encoding': 'gzip', 'accept-language': 'en'}}, 'match'),
    ('one differing nominated field fails the pair',
     {'vary': 'accept-encoding, accept-language',
      'stored': {'accept-encoding': 'gzip', 'accept-language': 'en'},
      'presented': {'accept-encoding': 'gzip', 'accept-language': 'fr'}}, 'mismatch'),
    ('duplicate members differing only in name case are deduplicated',
     {'vary': 'Accept-Encoding, accept-encoding',
      'stored': {'accept-encoding': 'gzip'},
      'presented': {'accept-encoding': 'gzip'}}, 'match'),
    ('an empty Vary value is refused',
     {'vary': '', 'stored': {}, 'presented': {}}, 'invalid'),
    ('a member containing SP is not a token',
     {'vary': 'accept encoding', 'stored': {'accept-encoding': 'gzip'},
      'presented': {'accept-encoding': 'gzip'}}, 'invalid'),
    ('array field lines combine in order with comma and SP',
     {'vary': 'accept-encoding', 'stored': {'accept-encoding': 'gzip, br'},
      'presented': {'accept-encoding': ['gzip', 'br']}}, 'match'),
    ('ordered combination makes a reversed array differ',
     {'vary': 'accept-encoding', 'stored': {'accept-encoding': 'br, gzip'},
      'presented': {'accept-encoding': ['gzip', 'br']}}, 'mismatch'),
    ('a one-element array combines to itself',
     {'vary': 'accept-encoding', 'stored': {'accept-encoding': 'gzip'},
      'presented': {'accept-encoding': [' \tgzip ']}}, 'match'),
    ('internal whitespace is not folded',
     {'vary': 'accept-encoding', 'stored': {'accept-encoding': 'gzip;q=1'},
      'presented': {'accept-encoding': 'gzip; q=1'}}, 'mismatch'),
    ('a non-string field value is refused',
     {'vary': 'accept-encoding', 'stored': {'accept-encoding': 5},
      'presented': {'accept-encoding': 'gzip'}}, 'invalid'),
    ('a non-string Vary value is refused',
     {'vary': 5, 'stored': {'accept-encoding': 'gzip'},
      'presented': {'accept-encoding': 'gzip'}}, 'invalid'),
    ('an empty array field value is refused',
     {'vary': 'accept-encoding', 'stored': {'accept-encoding': 'gzip'},
      'presented': {'accept-encoding': []}}, 'invalid'),
    ('a trailing comma leaves an empty member',
     {'vary': 'accept-encoding,', 'stored': {'accept-encoding': 'gzip'},
      'presented': {'accept-encoding': 'gzip'}}, 'invalid'),
    ('malformed JSON on stdin is refused', b'{', 'invalid'),
    ('a request map that is not an object is refused',
     {'vary': 'accept-encoding', 'stored': ['gzip'],
      'presented': {'accept-encoding': 'gzip'}}, 'invalid'),
    ('a field name with trailing SP is not a token',
     {'vary': 'accept-encoding', 'stored': {'accept-encoding ': 'gzip'},
      'presented': {'accept-encoding': 'gzip'}}, 'invalid'),
    ('case-variant duplicate field names are refused',
     {'vary': 'accept-encoding',
      'stored': {'accept-encoding': 'gzip', 'ACCEPT-ENCODING': 'br'},
      'presented': {'accept-encoding': 'gzip'}}, 'invalid'),
    ('a bad member outranks a star',
     {'vary': '*, accept encoding', 'stored': {'accept-encoding': 'gzip'},
      'presented': {'accept-encoding': 'gzip'}}, 'invalid'),
    ('a star does not mask an invalid field value',
     {'vary': '*', 'stored': {'accept-encoding': 5},
      'presented': {'accept-encoding': 'gzip'}}, 'invalid'),
    ('a star does not mask a request map of the wrong type',
     {'vary': 'accept-encoding, *', 'stored': 'gzip',
      'presented': {'accept-encoding': 'gzip'}}, 'invalid'),
    ('internal HTAB is preserved, not folded',
     {'vary': 'x-kake-token', 'stored': {'x-kake-token': 'a\tb'},
      'presented': {'x-kake-token': 'a\tb'}}, 'match'),
    ('OWS around list members is trimmed before the token check',
     {'vary': 'accept-encoding ,\taccept-language',
      'stored': {'accept-encoding': 'gzip', 'accept-language': 'en'},
      'presented': {'accept-encoding': 'gzip', 'accept-language': 'en'}}, 'match'),
    ('a payload without a stored map is refused',
     {'vary': 'accept-encoding', 'presented': {'accept-encoding': 'gzip'}},
     'invalid'),
    ('an empty JSON object is refused',
     {}, 'invalid'),
]


def _invoke(raw):
    proc = subprocess.run([sys.executable, '-B', os.path.abspath(__file__)],
                          input=raw, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=30)
    return proc.returncode, proc.stdout, proc.stderr


def selftest():
    checks = []

    def record(label, ok):
        checks.append((label, bool(ok)))

    for label, payload, expected in SELFTEST_CASES:
        raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        code, out, err = _invoke(raw)
        if expected == 'invalid':
            ok = (code == 1 and out == b''
                  and err.startswith(b'invalid_input:') and err.strip() != b'invalid_input:')
        else:
            ok = (code == 0 and out == expected.encode() and err == b'')
        record(label, ok)
    passed = 0
    for label, ok in checks:
        print(('PASS ' if ok else 'FAIL ') + label)
        passed += ok
    print(f'selftest: {passed}/{len(checks)} passed')
    return 0 if passed == len(checks) else 1


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv == ['--selftest']:
        return selftest()
    if argv:
        return refuse(f'unknown argument {argv[0]!r}')
    raw = sys.stdin.buffer.read()
    try:
        payload = json.loads(raw.decode('utf-8'))
    except (UnicodeDecodeError, ValueError) as exc:
        return refuse(f'stdin is not valid JSON: {exc}')
    verdict, reason = decide(payload)
    if verdict is None:
        return refuse(reason)
    sys.stdout.write(verdict)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
