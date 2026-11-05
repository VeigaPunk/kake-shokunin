#!/usr/bin/env python3
"""ReviewC2 independent battery for the round-93 C2 contract.

Case set, pins and oracle are derived from
LANE/.ufo/waves/round-93/c2-contract.md ALONE (contract v1, read before the
candidate and before any frozen counter case list). No content of
c93_conditional.py, its hand cases or its reference was read.

Layers:
  1. ORACLE   - my own reference implementation of the contract.
  2. PINS     - hand-derived expected outcome per case (from the contract).
  3. selfcheck- oracle must reproduce every pin before the tool is run.
  4. battery  - runs the target script (stdin JSON) and tabulates agreement.

Usage:
  python3 -B battery.py --selfcheck
  python3 -B battery.py TARGET.py OUTDIR
"""
import json, os, subprocess, sys, hashlib

# ---------------------------------------------------------------- oracle ----
TCHAR = set("!#$%&'*+-.^_`|~0123456789"
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def parse_etag(s):
    """Contract clause 3. Returns ('strong'|'weak', opaque) or None."""
    if s.startswith('W/"'):
        rest, weak = s[3:], True
    elif s.startswith('"'):
        rest, weak = s[1:], False
    else:
        return None
    if len(rest) < 1 or not rest.endswith('"'):
        return None
    core = rest[:-1]
    if '"' in core:
        return None
    for ch in core:
        o = ord(ch)
        if not (o == 0x21 or 0x23 <= o <= 0x7E):
            return None
    return ('weak' if weak else 'strong', core)


def parse_field(v):
    """Contract clause 4. Returns ('star',None) | ('list',[tags]) | None."""
    s = v.strip(' \t')
    if s == '':
        return None
    if s == '*':
        return ('star', None)
    members, cur, inq = [], [], False
    for ch in s:
        if ch == '"':
            inq = not inq
            cur.append(ch)
        elif ch == ',' and not inq:
            members.append(''.join(cur))
            cur = []
        else:
            cur.append(ch)
    members.append(''.join(cur))
    tags = []
    for m in members:
        mm = m.strip(' \t')
        if mm == '':
            return None
        t = parse_etag(mm)
        if t is None:
            return None
        tags.append(t)
    return ('list', tags)


def validate(raw):
    """Clauses 1-6 + input schema. Returns dict or None (refusal)."""
    try:
        d = json.loads(raw)
    except Exception:
        return None
    if not isinstance(d, dict):
        return None
    if set(d) - {'method', 'current', 'request', 'role'}:
        return None
    for k in ('method', 'current', 'request'):
        if k not in d:
            return None
    role = d.get('role', 'origin')
    if role not in ('origin', 'cache') or not isinstance(role, str):
        return None
    cur, req = d['current'], d['request']
    if not isinstance(cur, dict) or set(cur) != {'exists', 'etag', 'last_modified'}:
        return None
    if not isinstance(req, dict) or set(req) != {
            'if_match', 'if_none_match', 'if_modified_since', 'if_unmodified_since'}:
        return None
    method = d['method']
    if not isinstance(method, str) or len(method) < 1 or any(c not in TCHAR for c in method):
        return None
    exists = cur['exists']
    if not isinstance(exists, bool):
        return None
    etag = cur['etag']
    if etag is not None and not isinstance(etag, str):
        return None
    lm = cur['last_modified']
    if lm is not None and (isinstance(lm, bool) or not isinstance(lm, int) or lm < 0):
        return None
    if not exists and (etag is not None or lm is not None):
        return None
    im, inm = req['if_match'], req['if_none_match']
    ims, ius = req['if_modified_since'], req['if_unmodified_since']
    if im is not None and not isinstance(im, str):
        return None
    if inm is not None and not isinstance(inm, str):
        return None
    for v in (ims, ius):
        if v is not None and (isinstance(v, bool) or not isinstance(v, int) or v < 0):
            return None
    # clause 3/4 on precondition values and (primary reading) on current.etag
    if im is not None and parse_field(im) is None:
        return None
    if inm is not None and parse_field(inm) is None:
        return None
    if etag is not None and parse_etag(etag) is None:
        return None
    return d


def decide(d):
    """Decision order, contract steps 7-12. Returns (decision, precondition)."""
    method = d['method']
    cur, req = d['current'], d['request']
    role = d.get('role', 'origin')
    exists, etag, lm = cur['exists'], cur['etag'], cur['last_modified']
    im, inm = req['if_match'], req['if_none_match']
    ims, ius = req['if_modified_since'], req['if_unmodified_since']
    cur_tag = parse_etag(etag) if etag is not None else None

    def strong_eq(tag):
        return (cur_tag is not None and tag[0] == 'strong'
                and cur_tag[0] == 'strong' and tag[1] == cur_tag[1])

    def weak_eq(tag):
        return cur_tag is not None and tag[1] == cur_tag[1]

    gethead = method in ('GET', 'HEAD')  # case-sensitive per clause 1

    if role != 'cache':
        if im is not None:                       # step 8
            kind, val = parse_field(im)
            ok = exists if kind == 'star' else any(strong_eq(t) for t in val)
            if not ok:
                return ('412', 'if_match')
        elif ius is not None:                    # step 9
            if lm is not None and not (lm <= ius):
                return ('412', 'if_unmodified_since')
    if inm is not None:                          # step 10
        kind, val = parse_field(inm)
        fail = exists if kind == 'star' else any(weak_eq(t) for t in val)
        if fail:
            return ('304' if gethead else '412', 'if_none_match')
    if gethead and inm is None and ims is not None:   # step 11
        if lm is not None and lm <= ims:
            return ('304', 'if_modified_since')
    return ('200', None)                          # step 12


# ----------------------------------------------------------------- cases ----
def inp(method="GET", exists=True, etag=None, lm=None, im=None, inm=None,
        ims=None, ius=None, role=None):
    d = {"method": method,
         "current": {"exists": exists, "etag": etag, "last_modified": lm},
         "request": {"if_match": im, "if_none_match": inm,
                     "if_modified_since": ims, "if_unmodified_since": ius}}
    if role is not None:
        d["role"] = role
    return d


def raw_case(payload):
    return {"__raw__": payload}


# (id, clause-tag, kind R|D|X, input, pin)  pin: ("REFUSE",) or (decision, prec)
CASES = []
A = CASES.append

# ---- refusals: schema / clause 1 types
A(("R01", "schema-extra-topkey", "R", dict(inp(), extra=1), ("REFUSE",)))
A(("R02", "schema-missing-method", "R", {k: v for k, v in inp().items() if k != "method"}, ("REFUSE",)))
A(("R03", "c1-method-type", "R", inp(method=7), ("REFUSE",)))
A(("R04", "c1-method-empty", "R", inp(method=""), ("REFUSE",)))
A(("R05", "c1-method-tchar", "R", inp(method="GE T"), ("REFUSE",)))
A(("R06", "c1-method-tchar", "R", inp(method="GET,"), ("REFUSE",)))
A(("R07", "c1-method-tchar", "R", inp(method="GÉT"), ("REFUSE",)))
A(("R08", "c1-method-tchar", "R", inp(method="GET\t"), ("REFUSE",)))
A(("R09", "c1-method-type", "R", inp(method=None), ("REFUSE",)))
A(("R10", "schema-missing-current", "R", {k: v for k, v in inp().items() if k != "current"}, ("REFUSE",)))
A(("R11", "schema-current-type", "R", dict(inp(), current=None), ("REFUSE",)))
c = inp()["current"]; c["x"] = 1
A(("R12", "schema-current-extra", "R", dict(inp(), current=c), ("REFUSE",)))
c = {"exists": True, "etag": None}
A(("R13", "schema-current-missing-key", "R", dict(inp(), current=c), ("REFUSE",)))
A(("R14", "c1-exists-type", "R", inp(exists="true"), ("REFUSE",)))
c = {"etag": None, "last_modified": None}
A(("R15", "schema-current-missing-key", "R", dict(inp(), current=c), ("REFUSE",)))
A(("R16", "c2-absent-etag", "R", inp(exists=False, etag='"a"'), ("REFUSE",)))
A(("R17", "c2-absent-lm", "R", inp(exists=False, lm=5), ("REFUSE",)))
A(("R18", "c1-etag-type", "R", inp(etag=123), ("REFUSE",)))
A(("R19", "c1-etag-type", "R", inp(etag=True), ("REFUSE",)))
A(("R20", "c1-lm-type", "R", inp(lm="100"), ("REFUSE",)))
A(("R21", "c1-lm-bool", "R", inp(lm=True), ("REFUSE",)))
A(("R22", "c1-lm-negative", "R", inp(lm=-1), ("REFUSE",)))
A(("R23", "c1-lm-float", "R", inp(lm=1.5), ("REFUSE",)))
A(("R24", "schema-missing-request", "R", {k: v for k, v in inp().items() if k != "request"}, ("REFUSE",)))
A(("R25", "schema-request-type", "R", dict(inp(), request=None), ("REFUSE",)))
r = inp()["request"]; r["if_range"] = None
A(("R26", "schema-request-extra", "R", dict(inp(), request=r), ("REFUSE",)))
r = inp()["request"]; del r["if_modified_since"]
A(("R27", "schema-request-missing-key", "R", dict(inp(), request=r), ("REFUSE",)))
A(("R28", "c1-im-type", "R", inp(im=123), ("REFUSE",)))
A(("R29", "c1-inm-type", "R", inp(inm=True), ("REFUSE",)))
A(("R30", "c1-ims-type", "R", inp(ims="100"), ("REFUSE",)))
A(("R31", "c1-ius-bool", "R", inp(ius=True), ("REFUSE",)))
A(("R32", "c1-ius-negative", "R", inp(ius=-5), ("REFUSE",)))
A(("R33", "c1-ims-float", "R", inp(ims=1.5), ("REFUSE",)))
A(("R34", "schema-role-value", "R", inp(role="proxy"), ("REFUSE",)))
A(("R35", "schema-role-type", "R", inp(role=123), ("REFUSE",)))
A(("R36", "schema-role-value", "R", inp(role="Origin"), ("REFUSE",)))

# ---- refusals: clause 3 entity-tag syntax / clause 4 list syntax
A(("R37", "c4-empty", "R", inp(im=""), ("REFUSE",)))
A(("R38", "c4-blank", "R", inp(im="   "), ("REFUSE",)))
A(("R39", "c4-blank", "R", inp(im="\t"), ("REFUSE",)))
A(("R40", "c3-unterminated", "R", inp(im='"a'), ("REFUSE",)))
A(("R41", "c3-malformed", "R", inp(im='a"'), ("REFUSE",)))
A(("R42", "c3-unterminated-weak", "R", inp(im='W/"a'), ("REFUSE",)))
A(("R43", "c3-lowercase-w", "R", inp(im='w/"a"'), ("REFUSE",)))
A(("R44", "c3-space-after-W", "R", inp(im='W/ "a"'), ("REFUSE",)))
A(("R45", "c3-trailing-junk", "R", inp(im='"a"x'), ("REFUSE",)))
A(("R46", "c3-space-in-opaque", "R", inp(im='" a"'), ("REFUSE",)))
A(("R47", "c4-no-comma", "R", inp(im='"a" "b"'), ("REFUSE",)))
A(("R48", "c4-empty-member", "R", inp(im='"a",,'), ("REFUSE",)))
A(("R49", "c4-empty-member", "R", inp(im='"a", '), ("REFUSE",)))
A(("R50", "c4-empty-member", "R", inp(im=',"a"'), ("REFUSE",)))
A(("R51", "c4-star-mixed", "R", inp(im='*, "a"'), ("REFUSE",)))
A(("R52", "c4-star-mixed", "R", inp(im='"a", *'), ("REFUSE",)))
A(("R53", "c3-space-in-opaque", "R", inp(im='"a, b"'), ("REFUSE",)))
A(("R54", "c3-trailing-junk", "R", inp(im='"a"b'), ("REFUSE",)))
A(("R55", "c3-DEL-in-opaque", "R", inp(inm='"a\x7f"'), ("REFUSE",)))
A(("R56", "c3-control-in-opaque", "R", inp(im='"a\nb"'), ("REFUSE",)))
A(("R57", "c4-not-ows", "R", inp(im='\x0b"a"'), ("REFUSE",)))
A(("R58", "c4-empty-inm", "R", inp(inm=""), ("REFUSE",)))
A(("R59", "c3-malformed-inm", "R", inp(inm='"b"c'), ("REFUSE",)))
A(("R60", "c3-opaque-nonascii", "R", inp(inm='"café"'), ("REFUSE",)))

# ---- refusals: clause 6, no evaluation before validation
A(("R61", "c6-unevaluated-field", "R", inp(im='"a', ims=0), ("REFUSE",)))
A(("R62", "c6-cache-role", "R", inp(role="cache", im='"a'), ("REFUSE",)))
A(("R63", "c6-unevaluated-field", "R", inp(method="POST", inm='"a'), ("REFUSE",)))
A(("R64", "c6-unevaluated-field", "R", inp(method="POST", ims=-5), ("REFUSE",)))
A(("R65", "c6-unevaluated-field", "R", inp(method="DELETE", ims=-1), ("REFUSE",)))
A(("R66", "c6-unevaluated-field", "R", inp(method="POST", ius=-1), ("REFUSE",)))

# ---- refusals: stdin shape
A(("R67", "stdin-nonobject", "R", raw_case('[]'), ("REFUSE",)))
A(("R68", "stdin-invalidjson", "R", raw_case('{{{'), ("REFUSE",)))
A(("R69", "stdin-empty", "R", raw_case(''), ("REFUSE",)))
A(("R70", "stdin-json-null", "R", raw_case('null'), ("REFUSE",)))

# ---- decisions
A(("D01", "s12-no-preconds", "D", inp(), ("200", None)))
A(("D02", "s12-role-origin", "D", inp(role="origin"), ("200", None)))
A(("D03", "s12-role-cache", "D", inp(role="cache"), ("200", None)))
A(("D04", "s8-star-exists", "D", inp(etag='"a"', im='*'), ("200", None)))
A(("D05", "s8-star-missing", "D", inp(exists=False, im='*'), ("412", "if_match")))
A(("D06", "s8-strong-match", "D", inp(etag='"a"', im='"a"'), ("200", None)))
A(("D07", "s8-strong-miss", "D", inp(etag='"b"', im='"a"'), ("412", "if_match")))
A(("D08", "s8-list-hit", "D", inp(etag='"x"', im='"a", "x"'), ("200", None)))
A(("D09", "s8-list-miss", "D", inp(etag='"a"', im='"x", "y"'), ("412", "if_match")))
A(("D10", "c5-strong-weak-lhs", "D", inp(etag='"a"', im='W/"a"'), ("412", "if_match")))
A(("D11", "c5-strong-both-weak", "D", inp(etag='W/"a"', im='W/"a"'), ("412", "if_match")))
A(("D12", "c5-current-weak", "D", inp(etag='W/"a"', im='"a"'), ("412", "if_match")))
A(("D13", "s8-star-etag-null", "D", inp(etag=None, im='*'), ("200", None)))
A(("D14", "s8-etag-null", "D", inp(etag=None, im='"a"'), ("412", "if_match")))
A(("D15", "s8-missing-rep", "D", inp(exists=False, im='"a"'), ("412", "if_match")))
A(("D16", "c5-case-sensitive", "D", inp(etag='"a"', im='"A"'), ("412", "if_match")))
A(("D17", "c5-empty-opaque", "D", inp(etag='""', im='""'), ("200", None)))
A(("D18", "c5-etagc-specials", "D", inp(etag='"a#b!~"', im='"a#b!~"'), ("200", None)))
A(("D19", "s8-ows", "D", inp(etag='"a"', im=' "a" '), ("200", None)))
A(("D20", "s8-htab-ows", "D", inp(etag='"a"', im='"a"\t,\t"x"'), ("200", None)))
A(("D21", "c4-comma-in-opaque", "D", inp(etag='"a,b"', im='"a,b"'), ("200", None)))
A(("D22", "s9-ignored-when-im-present", "D", inp(etag='"a"', lm=200, im='"a"', ius=100), ("200", None)))
A(("D23", "s9-equal", "D", inp(etag='"a"', lm=100, im='"a"', ius=100), ("200", None)))
A(("D24", "s9-older", "D", inp(etag='"a"', lm=50, im='"a"', ius=100), ("200", None)))
A(("D25", "s9-equal-noim", "D", inp(lm=100, ius=100), ("200", None)))
A(("D26", "s9-newer", "D", inp(lm=200, ius=100), ("412", "if_unmodified_since")))
A(("D27", "s9-lm-null-ignored", "D", inp(ius=100), ("200", None)))
A(("D28", "s10-star-get", "D", inp(etag='"a"', inm='*'), ("304", "if_none_match")))
A(("D29", "s10-star-post", "D", inp(method="POST", etag='"a"', inm='*'), ("412", "if_none_match")))
A(("D30", "s10-star-head", "D", inp(method="HEAD", etag='"a"', inm='*'), ("304", "if_none_match")))
A(("D31", "s10-star-missing", "D", inp(exists=False, inm='*'), ("200", None)))
A(("D32", "s10-weak-eq-get", "D", inp(etag='"a"', inm='"a"'), ("304", "if_none_match")))
A(("D33", "c5-weak-current-weak", "D", inp(etag='W/"a"', inm='"a"'), ("304", "if_none_match")))
A(("D34", "c5-weak-tag-strong-cur", "D", inp(etag='"a"', inm='W/"a"'), ("304", "if_none_match")))
A(("D35", "c5-weak-both", "D", inp(etag='W/"a"', inm='W/"a"'), ("304", "if_none_match")))
A(("D36", "s10-miss", "D", inp(etag='"b"', inm='"a"'), ("200", None)))
A(("D37", "c5-inm-case", "D", inp(etag='"A"', inm='"a"'), ("200", None)))
A(("D38", "s10-list-weak-hit", "D", inp(etag='"b"', inm='"x", W/"b"'), ("304", "if_none_match")))
A(("D39", "s10-etag-null", "D", inp(etag=None, inm='"a"'), ("200", None)))
A(("D40", "s10-missing-rep", "D", inp(exists=False, inm='"a"'), ("200", None)))
A(("D41", "s10-non-gethead-true", "D", inp(method="DELETE", etag='"b"', inm='"a"'), ("200", None)))
A(("D42", "s10-non-gethead-false", "D", inp(method="DELETE", etag='"a"', inm='"a"'), ("412", "if_none_match")))
A(("D43", "s10-patch-false", "D", inp(method="PATCH", etag='"a"', inm='"a"'), ("412", "if_none_match")))
A(("D44", "s10-lowercase-get", "D", inp(method="get", etag='"a"', inm='"a"'), ("412", "if_none_match")))
A(("D45", "s10-lowercase-head", "D", inp(method="head", etag='"a"', inm='"a"'), ("412", "if_none_match")))
A(("D46", "s10-token-star-method", "D", inp(method="*", etag='"a"', inm='"a"'), ("412", "if_none_match")))
A(("D47", "s11-inm-suppresses-eq", "D", inp(etag='"a"', inm='"z"', lm=100, ims=100), ("200", None)))
A(("D48", "s11-inm-suppresses-older", "D", inp(etag='"a"', inm='"z"', lm=50, ims=100), ("200", None)))
A(("D49", "s11-inm-suppresses-newer", "D", inp(etag='"a"', inm='"z"', lm=200, ims=100), ("200", None)))
A(("D50", "s11-eq", "D", inp(lm=100, ims=100), ("304", "if_modified_since")))
A(("D51", "s11-lm-null-ignored", "D", inp(ims=100), ("200", None)))
A(("D52", "s11-post-ignored", "D", inp(method="POST", lm=100, ims=100), ("200", None)))
A(("D53", "s11-head-eq", "D", inp(method="HEAD", lm=100, ims=100), ("304", "if_modified_since")))
A(("D54", "s11-lowercase-head", "D", inp(method="head", lm=100, ims=100), ("200", None)))
A(("D55", "s8-before-s10", "D", inp(etag='"b"', im='"x"', inm='"b"'), ("412", "if_match")))
A(("D56", "s10-after-im", "D", inp(etag='"a"', im='"a"', inm='"a"'), ("304", "if_none_match")))
A(("D57", "s10-after-im-ius", "D", inp(etag='"a"', lm=100, im='"a"', ius=100, inm='"a"'), ("304", "if_none_match")))
A(("D58", "s9-before-s10", "D", inp(etag='"a"', lm=200, ius=100, inm='"a"'), ("412", "if_unmodified_since")))
A(("D59", "s9-before-s10-hit", "D", inp(etag='"a"', lm=200, ius=100, inm='"a"', im=None), ("412", "if_unmodified_since")))
A(("D60", "s7-im-skipped", "D", inp(etag='"a"', im='"b"', role="cache"), ("200", None)))
A(("D61", "s7-inm-decides", "D", inp(etag='"a"', im='"a"', inm='"a"', role="cache"), ("304", "if_none_match")))
A(("D62", "s7-ius-skipped", "D", inp(lm=200, ius=100, role="cache"), ("200", None)))
A(("D63", "s7-ims-decides", "D", inp(etag='"a"', lm=100, im='"b"', ims=100, role="cache"), ("304", "if_modified_since")))
A(("D64", "s7-inm-post", "D", inp(method="POST", etag='"a"', inm='"a"', role="cache"), ("412", "if_none_match")))
A(("D65", "s7-stars-missing", "D", inp(exists=False, im='*', inm='*', role="cache"), ("200", None)))
A(("D66", "s11-inm-present-lm-null", "D", inp(etag='"a"', inm='"z"', ims=100), ("200", None)))
A(("D67", "s11-boundary-zero", "D", inp(lm=0, ims=0), ("304", "if_modified_since")))
A(("D68", "s9-boundary-zero", "D", inp(lm=0, ius=0), ("200", None)))
A(("D69", "s11-large-ints", "D", inp(lm=4611686018427387904, ims=4611686018427387904), ("304", "if_modified_since")))
A(("D70", "s10-ows", "D", inp(etag='"a"', inm=' "a" '), ("304", "if_none_match")))
A(("D71", "s10-mixed-list-ows", "D", inp(etag='"b"', inm='\tW/"b" , "x"'), ("304", "if_none_match")))
A(("D72", "s9-then-s11-chain", "D", inp(lm=100, ius=200, ims=50), ("200", None)))
A(("D73", "s10-before-s11", "D", inp(etag='"a"', inm='"a"', lm=100, ims=100), ("304", "if_none_match")))
A(("D74", "c5-inm-empty-opaque", "D", inp(etag='""', inm='W/""'), ("304", "if_none_match")))
A(("D75", "s12-post", "D", inp(method="POST"), ("200", None)))
A(("D76", "s10-options-false", "D", inp(method="OPTIONS", etag='"a"', inm='"a"'), ("412", "if_none_match")))
A(("D77", "s10-prefix-not-equal", "D", inp(etag='"ab"', inm='"a"'), ("200", None)))
A(("D78", "s8-prefix-not-equal", "D", inp(etag='"a"', im='"ab"'), ("412", "if_match")))
A(("D79", "c5-weak-case", "D", inp(etag='W/"A"', inm='"a"'), ("200", None)))
A(("D80", "s8-star-trailing-ows-missing", "D", inp(exists=False, im='*  '), ("412", "if_match")))
A(("D81", "s8-star-leading-ows", "D", inp(etag='"a"', im=' *'), ("200", None)))
A(("D82", "s10-star-ows-get", "D", inp(etag='"a"', inm=' * '), ("304", "if_none_match")))
A(("D83", "s10-list-all-miss", "D", inp(etag='"a"', inm=' "x" , W/"y" '), ("200", None)))
A(("D84", "s8-weak-list-no-strong", "D", inp(etag='"a"', im='"x", W/"a"'), ("412", "if_match")))
A(("D85", "c5-weak-both-empty", "D", inp(etag='W/""', inm='W/""'), ("304", "if_none_match")))
A(("D86", "s7-im-ius-skipped", "D", inp(etag='"a"', lm=200, im='"b"', ius=100, role="cache"), ("200", None)))

# ---- exploratory: contract-undefined or genuinely ambiguous (flagged, not
#      counted in the main agreement denominator)
A(("X01", "c3-scope-current-etag", "X", inp(etag="abc", inm='"abc"'), ("REFUSE",)))
A(("X02", "c3-scope-current-obs", "X", inp(etag='"café"'), ("REFUSE",)))
A(("X03", "schema-role-null", "X", dict(inp(), role=None), ("REFUSE",)))
A(("X04", "undefined-dup-keys", "X", raw_case('{"method":"GET","current":{"exists":true,"etag":"\\"a\\"","last_modified":null},"request":{"if_match":null,"if_none_match":"\\"a\\"","if_modified_since":null,"if_unmodified_since":null},"method":"POST"}'), ("412", "if_none_match")))
A(("E01", "stdin-non-utf8", "R", {"__rawbytes__": b'\xff\xfe{"method":"GET"}'}, ("REFUSE",)))
A(("E02", "s8-t3row4-weak-diff", "D", inp(etag='"a"', im='W/"x"'), ("412", "if_match")))

# ------------------------------------------------------------- selfcheck ----
def raw_input_of(case):
    if "__rawbytes__" in case:
        return case["__rawbytes__"]
    if "__raw__" in case:
        return case["__raw__"]
    return json.dumps(case)


def jsonable_input(case):
    if "__rawbytes__" in case:
        return {"__rawbytes__": case["__rawbytes__"].decode("latin-1")}
    if "__raw__" in case:
        return {"__raw__": case["__raw__"]}
    return case


def selfcheck():
    bad = []
    for cid, tag, kind, case, pin in CASES:
        raw = raw_input_of(case)
        v = validate(raw)
        if pin[0] == "REFUSE":
            want = ("REFUSE",)
            got = ("REFUSE",) if v is None else ("DECIDE",) + decide(v)
        else:
            want = ("DECIDE",) + pin
            got = ("REFUSE",) if v is None else ("DECIDE",) + decide(v)
        if got != want:
            bad.append((cid, tag, want, got))
    return bad


# ---------------------------------------------------------------- runner ----
def run_target(target, raw, cwd):
    try:
        p = subprocess.run([sys.executable, "-B", target],
                           input=raw if isinstance(raw, bytes) else raw.encode("utf-8"),
                           capture_output=True, timeout=30, cwd=cwd)
        return {"exit": p.returncode, "stdout": p.stdout.decode("utf-8", "replace"),
                "stderr": p.stderr.decode("utf-8", "replace")}
    except subprocess.TimeoutExpired:
        return {"exit": "timeout", "stdout": "", "stderr": ""}


def actual_verdict(res):
    if res["exit"] == 0:
        try:
            o = json.loads(res["stdout"])
        except Exception:
            return ("MALFORMED-OK", res)
        if not isinstance(o, dict) or set(o) != {"decision", "precondition"}:
            return ("MALFORMED-OK", res)
        return ("DECIDE", o["decision"], o["precondition"])
    if res["exit"] == 1 and res["stdout"] == "" and res["stderr"].startswith("invalid_input"):
        return ("REFUSE",)
    return ("BROKEN", res)


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "--selfcheck":
        bad = selfcheck()
        if bad:
            print("SELFFAIL oracle-vs-pin mismatches:")
            for b in bad:
                print("  ", b)
            sys.exit(2)
        print(f"SELFOK oracle reproduces all {len(CASES)} pins")
        sys.exit(0)
    target, outdir = sys.argv[1], sys.argv[2]
    bad = selfcheck()
    if bad:
        print("SELFFAIL fix pins first:", bad[:5])
        sys.exit(2)
    with open(target, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    rows, agree, disagree, x_agree, x_disagree = [], 0, 0, 0, 0
    for cid, tag, kind, case, pin in CASES:
        raw = raw_input_of(case)
        res = run_target(target, raw, os.path.dirname(os.path.abspath(target)) if False else os.getcwd())
        act = actual_verdict(res)
        want = ("REFUSE",) if pin[0] == "REFUSE" else ("DECIDE",) + tuple(pin)
        ok = (act == want)
        cls = ""
        if not ok:
            cls = "PENDING-CLASSIFY"
        rows.append({"id": cid, "clause": tag, "kind": kind,
                     "input": jsonable_input(case),
                     "expected": list(pin), "actual": {"exit": res["exit"],
                                                       "stdout": res["stdout"][:400],
                                                       "stderr": res["stderr"][:400]},
                     "actual_verdict": list(act) if act[0] != "BROKEN" else ["BROKEN", act[1]["stderr"][:200]],
                     "agree": ok, "classification": cls})
        if kind == "X":
            x_agree, x_disagree = x_agree + (1 if ok else 0), x_disagree + (0 if ok else 1)
        else:
            agree, disagree = agree + (1 if ok else 0), disagree + (0 if ok else 1)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "cases.json"), "w") as f:
        json.dump({"target": os.path.abspath(target), "target_sha256": sha,
                   "cases_total": len(CASES), "rows": rows}, f, indent=1, ensure_ascii=False)
    kinds = {}
    for r_ in rows:
        k = (r_["kind"], r_["agree"])
        kinds[k] = kinds.get(k, 0) + 1
    lines = [
        f"target: {os.path.abspath(target)}",
        f"target sha256: {sha}",
        f"cases: {len(CASES)}  agree: {agree + x_agree}  disagree: {disagree + x_disagree}",
        f"main (R+D): {agree + disagree}  agree {agree}  disagree {disagree}",
        f"exploratory (X): {x_agree + x_disagree}  agree {x_agree}  disagree {x_disagree}",
    ]
    for (k, a), n in sorted(kinds.items()):
        lines.append(f"  kind={k} agree={a} count={n}")
    ds = [r_ for r_ in rows if not r_["agree"]]
    for d in ds:
        lines.append(f"DISAGREE {d['id']} {d['clause']} expected={d['expected']} actual={d['actual_verdict']} stderr={d['actual']['stderr'][:120]!r}")
    txt = "\n".join(lines) + "\n"
    with open(os.path.join(outdir, "agreement.txt"), "w") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    main()
