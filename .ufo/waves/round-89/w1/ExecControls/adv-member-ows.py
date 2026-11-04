#!/usr/bin/env python3
"""Adversarial probe: vary members are not trimmed of surrounding OWS
(spaces/tabs kept verbatim). Expected violation: contract clause 1
(each member trimmed of leading and trailing SP and HTAB)."""
import json
import sys

US, RS, GS = '\x1f', '\x1e', '\x1c'
TCHAR = frozenset("!#$%&'*+-.^_`|~"
                  '0123456789'
                  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                  'abcdefghijklmnopqrstuvwxyz')
ESCAPES = (('%', '%25'), (GS, '%1C'), ('\x1d', '%1D'), (RS, '%1E'), (US, '%1F'))


def escape(text):
    for raw, encoded in ESCAPES:
        text = text.replace(raw, encoded)
    return text


def is_token(text):
    return bool(text) and all(ch in TCHAR for ch in text)


def strip_ows(text):
    return text.strip(' \t')


def fail(reason):
    print('invalid_input: ' + reason, file=sys.stderr)
    return 1


def main():
    try:
        obj = json.load(sys.stdin)
    except Exception:
        return fail('input is not a JSON object')
    if not isinstance(obj, dict):
        return fail('input must be a JSON object')
    uri = obj.get('uri')
    if not isinstance(uri, str):
        return fail('uri must be a string')
    headers = obj.get('request_headers')
    if not isinstance(headers, dict):
        return fail('request_headers must be an object')
    lowered = {}
    for name, value in headers.items():
        if not isinstance(name, str) or not is_token(name):
            return fail('header name is not a token')
        if not isinstance(value, str):
            return fail('header value must be a string')
        if '\r' in value or '\n' in value:
            return fail('header value contains CR or LF')
        low = name.lower()
        if low in lowered:
            return fail('duplicate header name')
        lowered[low] = value
    vary = obj.get('vary', '')
    if not isinstance(vary, str):
        return fail('vary must be a string')
    names = []
    if vary != '':
        for raw in vary.split(','):
            if raw == '*':
                return fail('vary wildcard nominates no field')
            if not is_token(raw):
                return fail('vary member is not a token')
            names.append(raw.lower())
    if len(set(names)) != len(names):
        return fail('duplicate vary member')
    parts = []
    for name in sorted(names):
        if name in lowered:
            parts.append(escape(name) + RS + escape(strip_ows(lowered[name])))
        else:
            parts.append(escape(name) + RS + GS)
    key = escape(uri) + ('' if not parts else US + US.join(parts))
    print(json.dumps({'key': key}))
    return 0


raise SystemExit(main())
