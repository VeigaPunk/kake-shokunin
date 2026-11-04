#!/usr/bin/env python3
"""Conservative Vary-match reader (offline, supplied headers only).

RFC 9111 §4.1: a stored response must not be used without revalidation unless
every request field nominated by its Vary value matches the original request's
field. This tool applies the conservative subset of the permitted
transformations: field names compare ASCII case-insensitively, multiple field
lines combine in order with ", ", and values compare byte-identically after
trimming leading/trailing SP/HTAB. It never case-folds or reorders values, so a
"match" verdict is always permitted by §4.1 while a "mismatch" may be stricter
than a field-specific normalisation. No cache key, storage, revalidation,
freshness or serving decision is made or implied.

stdin  : {"vary": "<field value>", "stored": {name: value|list}, "presented": {...}}
exit 0 : stdout is exactly "match" or "mismatch", stderr empty
exit 1 : stderr starts with "invalid_input:", stdout empty
"""
import json
import re
import sys

TOKEN = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")
OWS = " \t"
KEYS = {"vary", "stored", "presented"}


class Refused(Exception):
    pass


def tokens(field):
    if not isinstance(field, str):
        raise Refused("vary must be a string")
    members = [m.strip(OWS) for m in field.split(",")]
    if not members or any(m == "" for m in members):
        raise Refused("vary has an empty member")
    names, star = [], False
    for m in members:
        if m == "*":
            star = True
        elif TOKEN.match(m):
            names.append(m.lower())
        else:
            raise Refused(f"vary member {m!r} is not a token")
    return names, star


def normalise(side, label):
    if not isinstance(side, dict):
        raise Refused(f"{label} must be an object")
    out = {}
    for key, value in side.items():
        if not isinstance(key, str) or not TOKEN.match(key):
            raise Refused(f"{label} field name {key!r} is not a token")
        low = key.lower()
        if low in out:
            raise Refused(f"{label} names {low!r} twice")
        if isinstance(value, str):
            out[low] = value
        elif isinstance(value, list) and value and all(isinstance(v, str) for v in value):
            out[low] = ", ".join(value)
        else:
            raise Refused(f"{label} field {low!r} must be a string or a non-empty array of strings")
    return out


def decide(payload):
    if not isinstance(payload, dict):
        raise Refused("input must be a JSON object")
    extra = set(payload) - KEYS
    if extra:
        raise Refused(f"unknown input key {sorted(extra)[0]!r}")
    for key in KEYS:
        if key not in payload:
            raise Refused(f"missing {key}")
    names, star = tokens(payload["vary"])
    stored = normalise(payload["stored"], "stored")
    presented = normalise(payload["presented"], "presented")
    if star:
        return "mismatch"
    for name in dict.fromkeys(names):
        left, right = stored.get(name), presented.get(name)
        if left is None and right is None:
            continue
        if left is None or right is None:
            return "mismatch"
        if left.strip(OWS) != right.strip(OWS):
            return "mismatch"
    return "match"


def selftest():
    cases = [
        ({"vary": "accept-encoding", "stored": {"accept-encoding": "gzip"},
          "presented": {"accept-encoding": "gzip"}}, "match"),
        ({"vary": "Accept-Encoding", "stored": {"accept-encoding": "gzip"},
          "presented": {"ACCEPT-ENCODING": "gzip"}}, "match"),
        ({"vary": "accept-encoding", "stored": {"accept-encoding": " gzip "},
          "presented": {"accept-encoding": "gzip"}}, "match"),
        ({"vary": "accept-encoding", "stored": {}, "presented": {}}, "match"),
        ({"vary": "accept-encoding", "stored": {"accept-encoding": "gzip"},
          "presented": {"accept-encoding": ["gzip"]}}, "match"),
        ({"vary": "accept-encoding", "stored": {"accept-encoding": "gzip, br"},
          "presented": {"accept-encoding": ["gzip", "br"]}}, "match"),
        ({"vary": "accept-encoding", "stored": {"accept-encoding": "gzip"},
          "presented": {"accept-encoding": "GZip"}}, "mismatch"),
        ({"vary": "accept-encoding", "stored": {}, "presented": {"accept-encoding": "gzip"}}, "mismatch"),
        ({"vary": "*", "stored": {}, "presented": {}}, "mismatch"),
        ({"vary": "accept-encoding, *", "stored": {"accept-encoding": "gzip"},
          "presented": {"accept-encoding": "gzip"}}, "mismatch"),
        ({"vary": "accept-encoding", "stored": {"accept-encoding": "gzip, br"},
          "presented": {"accept-encoding": "br, gzip"}}, "mismatch"),
        ({"vary": "Accept-Encoding, accept-encoding", "stored": {"accept-encoding": "gzip"},
          "presented": {"accept-encoding": "gzip"}}, "match"),
        ({"vary": "accept-encoding, accept-language",
          "stored": {"accept-encoding": "gzip", "accept-language": "en"},
          "presented": {"accept-encoding": "gzip", "accept-language": "en"}}, "match"),
        ({"vary": "accept-encoding, accept-language",
          "stored": {"accept-encoding": "gzip", "accept-language": "en"},
          "presented": {"accept-encoding": "gzip", "accept-language": "fr"}}, "mismatch"),
        ({"vary": "accept-encoding", "stored": {"accept-encoding": "gzip;q=1"},
          "presented": {"accept-encoding": "gzip; q=1"}}, "mismatch"),
        ({"vary": "accept-encoding", "stored": {"accept-encoding": "br, gzip"},
          "presented": {"accept-encoding": ["gzip", "br"]}}, "mismatch"),
    ]
    refusals = [
        {"vary": "", "stored": {}, "presented": {}},
        {"vary": "accept encoding", "stored": {}, "presented": {}},
        {"vary": 5, "stored": {}, "presented": {}},
        {"vary": "accept-encoding", "stored": {"accept-encoding": 5}, "presented": {}},
        {"vary": "accept-encoding", "stored": {"accept-encoding": []}, "presented": {}},
        {"vary": "accept-encoding", "stored": {"accept-encoding": "a"},
         "presented": {"accept-encoding": "a"}, "extra": 1},
    ]
    passed = 0
    for payload, want in cases:
        got = decide(payload)
        assert got == want, (payload, got, want)
        passed += 1
    for payload in refusals:
        try:
            decide(payload)
        except Refused:
            passed += 1
        else:
            raise AssertionError(payload)
    print(f"selftest: {passed} isolated fixtures passed")
    return 0


def main():
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    if sys.argv[1:]:
        sys.stderr.write("usage: vary_match.py [--selftest] < input.json\n")
        return 1
    try:
        result = decide(json.loads(sys.stdin.read()))
    except Refused as exc:
        sys.stderr.write(f"invalid_input: {exc}\n")
        return 1
    except ValueError as exc:
        sys.stderr.write(f"invalid_input: {exc}\n")
        return 1
    sys.stdout.write(result + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
