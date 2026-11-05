#!/usr/bin/env python3
"""Forgery control for the round-95 conditional counter (contract v2):\n\nThis subject REFUSES empty list members, which contract v2 (S478: a recipient\nMUST accept lists whose syntax allows empty elements) requires it to accept.\nThe counter must score it refused. Derived from pos-good-v2.py with the v1\nparse_list semantics restored.

Decides which status a recipient answers a conditional request with, over stdin
JSON {method, current:{exists,etag,last_modified}, request:{if_match,
if_none_match, if_modified_since, if_unmodified_since}, role?}. Contract v2:
empty list members are accepted and ignored; obs-text is legal in an opaque-tag;
"role": null means origin; raw input bytes carrying duplicate object keys are
refused. Writes one JSON decision object to stdout; refuses malformed input with
exit 1 and `invalid_input:` on stderr.
"""
import json
import sys

TOP_KEYS = {"method", "current", "request", "role"}
CUR_KEYS = {"exists", "etag", "last_modified"}
REQ_KEYS = {"if_match", "if_none_match", "if_modified_since", "if_unmodified_since"}
TCHAR = frozenset("!#$%&'*+-.^_`|~0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                  "abcdefghijklmnopqrstuvwxyz")
_ETAGC_BAD = frozenset(c for c in map(chr, range(0x00, 0x100))
                       if not (c == "!" or 0x23 <= ord(c) <= 0x7E or 0x80 <= ord(c) <= 0xFF))
_SAFE = frozenset(("GET", "HEAD"))


class InvalidInput(Exception):
    pass


def _no_dup(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            raise InvalidInput("duplicate object key")
        seen.add(k)
    return dict(pairs)


def _etag(v):
    weak = v.startswith("W/")
    rest = v[2:] if weak else v
    if len(rest) < 2 or rest[0] != '"' or rest[-1] != '"':
        raise InvalidInput("malformed entity-tag")
    for ch in rest[1:-1]:
        if ch in _ETAGC_BAD:
            raise InvalidInput("malformed entity-tag")
    return (weak, rest[1:-1])


def _list(v):
    s = v.strip(" \t")
    if s == "*":
        return "*"
    if not s:
        raise InvalidInput("empty precondition field value")
    out = []
    for part in s.split(","):
        p = part.strip(" \t")
        if p == "*":
            raise InvalidInput('"*" mixed with entity tags')
        if not p:
            raise InvalidInput("empty list member")
        out.append(_etag(p))
    return out


def _int(v, field):
    if isinstance(v, bool) or not isinstance(v, int) or v < 0:
        raise InvalidInput("%s is neither null nor a non-negative int" % field)
    return v


def decide(inp):
    if not isinstance(inp, dict) or set(inp) - TOP_KEYS:
        raise InvalidInput("unexpected or missing top-level keys")
    for k in ("method", "current", "request"):
        if k not in inp:
            raise InvalidInput("missing %s" % k)
    method = inp["method"]
    if not isinstance(method, str) or method == "" or any(c not in TCHAR for c in method):
        raise InvalidInput("method is not a token")
    cur, req = inp["current"], inp["request"]
    if not isinstance(cur, dict) or set(cur) != CUR_KEYS:
        raise InvalidInput("current is not the declared object")
    if not isinstance(req, dict) or set(req) != REQ_KEYS:
        raise InvalidInput("request is not the declared object")
    exists = cur["exists"]
    if not isinstance(exists, bool):
        raise InvalidInput("exists is not a bool")
    etag, lastmod = cur["etag"], cur["last_modified"]
    if etag is not None and not isinstance(etag, str):
        raise InvalidInput("etag is neither null nor a string")
    if lastmod is not None:
        lastmod = _int(lastmod, "last_modified")
    if not exists and (etag is not None or lastmod is not None):
        raise InvalidInput("absent representation carries a validator")
    vals = {}
    for key in sorted(REQ_KEYS):
        v = req[key]
        if v is None:
            vals[key] = None
        elif key in ("if_match", "if_none_match"):
            if not isinstance(v, str):
                raise InvalidInput("%s is neither null nor a string" % key)
            vals[key] = _list(v)
        else:
            vals[key] = _int(v, key)
    role = inp.get("role", "origin")
    if role is None:
        role = "origin"
    if role not in ("origin", "cache"):
        raise InvalidInput("role is not origin or cache")
    cur_tag = _etag(etag) if etag is not None else None

    def matches(spec, cmp):
        if spec == "*":
            return exists
        if not exists or cur_tag is None:
            return False
        return any(cmp(t, cur_tag) for t in spec)

    strong = lambda a, b: (not a[0]) and (not b[0]) and a[1] == b[1]
    weak = lambda a, b: a[1] == b[1]
    im, ius, inm, ims = (vals["if_match"], vals["if_unmodified_since"],
                         vals["if_none_match"], vals["if_modified_since"])
    if role == "origin":
        if im is not None:
            if not matches(im, strong):
                return {"decision": "412", "precondition": "if_match"}
        elif ius is not None and lastmod is not None:
            if not lastmod <= ius:
                return {"decision": "412", "precondition": "if_unmodified_since"}
    if inm is not None:
        if matches(inm, weak):
            if method in _SAFE:
                return {"decision": "304", "precondition": "if_none_match"}
            return {"decision": "412", "precondition": "if_none_match"}
    elif ims is not None and method in _SAFE and lastmod is not None:
        if lastmod <= ims:
            return {"decision": "304", "precondition": "if_modified_since"}
    return {"decision": "200", "precondition": None}


def selftest():
    ok = True
    cases = [
        ({"method": "PUT", "current": {"exists": True, "etag": '"1"', "last_modified": 500},
          "request": {"if_match": '"1"', "if_none_match": None, "if_modified_since": None,
                      "if_unmodified_since": None}}, {"decision": "200", "precondition": None}),
        ({"method": "GET", "current": {"exists": True, "etag": '"2"', "last_modified": 500},
          "request": {"if_match": None, "if_none_match": '"1", , "2"',
                      "if_modified_since": None, "if_unmodified_since": None}},
         {"decision": "304", "precondition": "if_none_match"}),
        ({"method": "GET", "current": {"exists": True, "etag": 'W/"a\x80"',
                                       "last_modified": 500},
          "request": {"if_match": None, "if_none_match": '"a\x80"',
                      "if_modified_since": None, "if_unmodified_since": None}},
         {"decision": "304", "precondition": "if_none_match"}),
    ]
    for inp, want in cases:
        if decide(inp) != want:
            ok = False
    for bad in ('{"method":"GET","method":"HEAD"}', "not json", ""):
        try:
            _no_dup_list = json.loads(bad, object_pairs_hook=_no_dup) if bad.startswith("{") else None
            if _no_dup_list is not None:
                ok = False
        except InvalidInput:
            pass
        except Exception:
            pass
    print("selftest %d/3 decide cases + duplicate-key refusal" % (3 if ok else 0))
    return 0 if ok else 1


def main():
    raw = sys.stdin.buffer.read()
    try:
        inp = json.loads(raw.decode("utf-8"), object_pairs_hook=_no_dup)
        result = decide(inp)
    except (InvalidInput, ValueError, UnicodeDecodeError) as exc:
        sys.stdout.flush()
        print("invalid_input: %s" % exc, file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
