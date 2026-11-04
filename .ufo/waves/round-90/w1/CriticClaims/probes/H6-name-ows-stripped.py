#!/usr/bin/env python3
"""Conservative Vary-nominated cache-key construction (C2 candidate).

Reads one JSON object on stdin and writes the canonical key on stdout, per the
key contract in c2-contract.md. The key is built from exactly three
ingredients: the request URI, the field names nominated by `Vary`, and those
fields' presented values.

Refusals print `invalid_input: <reason>` on stderr and exit 1.

Standard library only. It reads its own stdin and nothing else.
"""

import json
import sys

# RFC 9110 token characters (tchar). A plain string: membership is per character.
TCHARS = (
    "!#$%&'*+-.^_`|~"
    "0123456789"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
)

# Key layout control characters.
US = "\x1f"  # unit separator: between URI and each pair
RS = "\x1e"  # record separator: between a name and its value
GS = "\x1c"  # group separator: marks an absent field

# Escaping order matters: '%' first so introduced escapes are not re-escaped.
_ESCAPES = (
    ("%", "%25"),
    (GS, "%1C"),
    ("\x1d", "%1D"),
    (RS, "%1E"),
    (US, "%1F"),
)

OWS = " \t"  # optional whitespace trimmed from values and members


def _esc(s):
    for raw, enc in _ESCAPES:
        s = s.replace(raw, enc)
    return s


def _is_token(s):
    return bool(s) and all(c in TCHARS for c in s)


def _strip_ows(s):
    return s.strip(OWS)


class _Invalid(Exception):
    pass


def _parse_vary(vary):
    """Return sorted lowercased field names, or raise _Invalid."""
    if not isinstance(vary, str):
        raise _Invalid("vary must be a string")
    if vary == "":
        return []
    names = []
    for raw in vary.split(","):
        member = _strip_ows(raw)
        if member == "*":
            raise _Invalid("vary wildcard nominates no field")
        if not _is_token(member):
            raise _Invalid("vary member is not a token")
        names.append(member.lower())
    if len(set(names)) != len(names):
        raise _Invalid("duplicate vary member")
    return sorted(names)


def _build_key(obj):
    if not isinstance(obj, dict):
        raise _Invalid("input must be a JSON object")

    uri = obj.get("uri")
    if not isinstance(uri, str):
        raise _Invalid("uri must be a string")

    headers = obj.get("request_headers")
    if not isinstance(headers, dict):
        raise _Invalid("request_headers must be an object")

    lowered = {}
    for name, value in list(headers.items()):
        name = name.strip(' ') if isinstance(name, str) else name
        if not isinstance(name, str) or not _is_token(name):
            raise _Invalid("header name is not a token")
        if not isinstance(value, str):
            raise _Invalid("header value must be a string")
        if "\r" in value or "\n" in value:
            raise _Invalid("header value contains CR or LF")
        low = name.lower()
        if low in lowered:
            raise _Invalid("duplicate header name")
        lowered[low] = value

    names = _parse_vary(obj.get("vary", ""))

    parts = []
    for name in names:
        if name in lowered:
            parts.append(_esc(name) + RS + _esc(_strip_ows(lowered[name])))
        else:
            parts.append(_esc(name) + RS + GS)

    return _esc(uri) + ("" if not parts else US + US.join(parts))


def main():
    try:
        obj = json.load(sys.stdin)
    except (ValueError, UnicodeDecodeError):
        print("invalid_input: input is not valid JSON", file=sys.stderr)
        return 1
    try:
        key = _build_key(obj)
    except _Invalid as exc:
        print(f"invalid_input: {exc}", file=sys.stderr)
        return 1
    sys.stdout.write(json.dumps({"key": key}) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
