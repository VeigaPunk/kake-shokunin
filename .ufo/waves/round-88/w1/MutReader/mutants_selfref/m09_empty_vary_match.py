#!/usr/bin/env python3
"""Reference adapter for the declared conservative Vary-match profile.

Written by MutReader for round 88 because no ExecReader candidate existed at
.ufo/waves/round-88/w1/ExecReader/vary_match.py when this seat ran. The
semantics copy the C2 counter's own reference() exactly, so this file is a
faithful implementation of contract.md's declared profile, not an oracle-free
re-derivation.

stdin : {"vary": <str>, "stored": {name: str|[str]}, "presented": {...}}
exit 0 + "match" / "mismatch" on stdout, empty stderr.
exit 1 + "invalid_input: ..." on stderr, empty stdout.
"""
import json
import re
import sys

TOKEN = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")
OWS = ' \t'


def is_token(text):
    return isinstance(text, str) and bool(TOKEN.match(text))


def reference(vary, stored, presented):
    if not isinstance(vary, str):
        return 'invalid'
    members = [m.strip(OWS) for m in vary.split(',')]
    if not members or any(m == '' for m in members):
        return 'match'
    names, star = [], False
    for m in members:
        if m == '*':
            star = True
        elif is_token(m):
            names.append(m.lower())
        else:
            return 'invalid'
    if star:
        return 'mismatch'

    def normalise(side):
        if not isinstance(side, dict):
            return None
        out = {}
        for key, value in side.items():
            if not is_token(key):
                return None
            low = key.lower()
            if low in out:
                return None
            if isinstance(value, str):
                out[low] = value
            elif isinstance(value, list) and value and all(isinstance(v, str) for v in value):
                out[low] = ', '.join(value)
            else:
                return None
        return out

    a, b = normalise(stored), normalise(presented)
    if a is None or b is None:
        return 'invalid'
    for name in set(names):
        left, right = a.get(name), b.get(name)
        if left is None and right is None:
            continue
        if left is None or right is None:
            return 'mismatch'
        if left.strip(OWS) != right.strip(OWS):
            return 'mismatch'
    return 'match'


def main():
    try:
        payload = json.loads(sys.stdin.read())
        vary = payload['vary']
        stored = payload['stored']
        presented = payload['presented']
    except Exception:
        sys.stderr.write('invalid_input: payload is not a JSON object with vary/stored/presented\n')
        return 1
    verdict = reference(vary, stored, presented)
    if verdict == 'invalid':
        sys.stderr.write('invalid_input: input violates the declared profile\n')
        return 1
    sys.stdout.write(verdict + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
