#!/usr/bin/env python3
"""Decide which status a recipient answers a conditional request with.

Reads one JSON object on stdin describing the request method, the currently
selected representation (or its absence) and the supplied precondition field
values; writes one JSON object on stdout:

    {"decision": "200"|"304"|"412", "precondition": "<name>"|null}

``precondition`` names the field that decided the outcome (``if_match``,
``if_unmodified_since``, ``if_none_match``, ``if_modified_since``) or is null
when no precondition was evaluated. Malformed input is refused with
``invalid_input: <reason>`` on stderr, exit 1, and nothing on stdout.

What this tool deliberately does not do (contract scope, stated up front):
  * no HTTP-date parsing -- ``if_modified_since`` and
    ``if_unmodified_since`` are integer epoch-seconds values, the lane's
    adapter convention shared with ``scripts/stored_reuse.py`` and
    ``scripts/heuristic_freshness.py``;
  * no clock, no network, no cache store, no validator generation, and no
    statement about any live property;
  * no range/If-Range handling -- the decision set is 200/304/412 only.

Contract: ``.ufo/waves/round-93/c2-contract.md`` (v1). Clause numbers appear
in comments wherever a reader would otherwise have to guess.

Usage:
    conditional_eval.py              one JSON object on stdin, one on stdout
    conditional_eval.py --selftest   in-memory fixtures, prints a "selftest K/K" line
"""

import json
import sys


class InvalidInput(Exception):
    """The input violates the contract: refusal with exit 1."""


# Clause 1: RFC 9110 section 5.6.2 token characters (tchar).
_TOKEN = frozenset(
    "!#$%&'*+-.^_`|~"
    "0123456789"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
)

# RFC 9110 section 13.1.3/13.1.4 and 13.2.2 step 4: date preconditions and the
# 304 branch apply to GET and HEAD only, compared case-sensitively.
_SAFE_METHODS = frozenset(("GET", "HEAD"))

_TAG_FIELDS = ("if_match", "if_none_match")
_DATE_FIELDS = ("if_modified_since", "if_unmodified_since")
_REQUEST_KEYS = frozenset(_TAG_FIELDS + _DATE_FIELDS)


def _entity_tag(value):
    """Clause 3: parse an entity-tag; return (weak, opaque_tag) or None.

    entity-tag = [ weak ] opaque-tag ; weak = %x57.2F ("W/") ;
    opaque-tag = DQUOTE *etagc DQUOTE ; etagc = %x21 / %x23-7E.
    The opaque-tag is the byte string between the quotes.
    """
    if value.startswith('W/"'):
        rest = value[3:]
        weak = True
    elif value.startswith('"'):
        rest = value[1:]
        weak = False
    else:
        return None
    if len(rest) < 1 or not rest.endswith('"'):
        return None
    opaque = rest[:-1]
    for ch in opaque:
        o = ord(ch)
        if not (o == 0x21 or 0x23 <= o <= 0x7E):
            return None
    return weak, opaque


def _precondition_members(value, field):
    """Clauses 3-4 for one precondition field value.

    Parses the RFC 9110 list grammar sequentially rather than splitting on
    commas, because an opaque-tag may contain a comma (etagc includes 0x2C).
    Returns ("star", None) for the ``*`` form or ("tags", [(weak, opaque), ...]).
    Raises InvalidInput on every clause-4 refusal: empty or whitespace-only
    value, an empty member, ``*`` mixed with other members, or a member that
    is not a well-formed entity-tag. SP/HTAB around each member is optional.
    """
    if value.strip(" \t") == "":
        raise InvalidInput("%s must not be an empty value" % field)
    items = []
    i = 0
    n = len(value)
    while True:
        while i < n and value[i] in " \t":
            i += 1
        if i >= n:
            raise InvalidInput("%s has an empty list member" % field)
        if value[i] == ",":
            raise InvalidInput("%s has an empty list member" % field)
        if value[i] == "*":
            items.append("*")
            i += 1
        else:
            start = i
            if value.startswith('W/"', i):
                i += 3
            elif value.startswith('"', i):
                i += 1
            else:
                raise InvalidInput("malformed entity-tag in %s" % field)
            while i < n and value[i] != '"':
                o = ord(value[i])
                if not (o == 0x21 or 0x23 <= o <= 0x7E):
                    raise InvalidInput("malformed entity-tag in %s" % field)
                i += 1
            if i >= n:
                raise InvalidInput("malformed entity-tag in %s" % field)
            i += 1  # closing DQUOTE
            tag = _entity_tag(value[start:i])
            if tag is None:
                raise InvalidInput("malformed entity-tag in %s" % field)
            items.append(tag)
        while i < n and value[i] in " \t":
            i += 1
        if i >= n:
            break
        if value[i] != ",":
            raise InvalidInput("malformed entity-tag in %s" % field)
        i += 1
    if "*" in items:
        if items == ["*"]:
            return "star", None
        raise InvalidInput("%s mixes '*' with other members" % field)
    return "tags", items


def _strong_eq(tag, current):
    """Clause 5 + RFC 9110 8.8.3.2: strong comparison, both tags non-weak."""
    return (current is not None and not tag[0] and not current[0]
            and tag[1] == current[1])


def _weak_eq(tag, current):
    """Clause 5 + RFC 9110 8.8.3.2: weak comparison on opaque-tags alone."""
    return current is not None and tag[1] == current[1]


def evaluate(inp):
    """Clauses 1-12 of the contract. Returns the decision object.

    Every clause-1..4 validation runs before any evaluation (clause 6), so a
    malformed field is a refusal even in cases -- such as the cache role --
    where the field would never be evaluated.
    """
    # Clause 1 (input shape) and clause 2 (absent representation).
    if not isinstance(inp, dict):
        raise InvalidInput("input is not a JSON object")
    keys = set(inp)
    unknown = keys - {"method", "current", "request", "role"}
    if unknown:
        raise InvalidInput("unknown top-level key: %s" % sorted(unknown)[0])
    for name in ("method", "current", "request"):
        if name not in keys:
            raise InvalidInput("missing top-level key: %s" % name)
    role = inp.get("role", "origin")
    if role not in ("origin", "cache"):
        raise InvalidInput("role must be \"origin\" or \"cache\"")
    method = inp["method"]
    if (not isinstance(method, str) or not method
            or any(ch not in _TOKEN for ch in method)):
        raise InvalidInput("method must be a non-empty HTTP token")
    current = inp["current"]
    if (not isinstance(current, dict)
            or set(current) != {"exists", "etag", "last_modified"}):
        raise InvalidInput(
            "current must be an object with exactly exists, etag, last_modified")
    request = inp["request"]
    if not isinstance(request, dict) or set(request) != _REQUEST_KEYS:
        raise InvalidInput(
            "request must be an object with exactly the four precondition keys")
    exists = current["exists"]
    if not isinstance(exists, bool):
        raise InvalidInput("exists must be a boolean")
    etag = current["etag"]
    if etag is not None and not isinstance(etag, str):
        raise InvalidInput("etag must be null or a string")
    lm = current["last_modified"]
    if lm is not None and (isinstance(lm, bool)
                           or not isinstance(lm, int) or lm < 0):
        raise InvalidInput("last_modified must be null or an integer >= 0")
    for name in _TAG_FIELDS:
        v = request[name]
        if v is not None and not isinstance(v, str):
            raise InvalidInput("%s must be null or a string" % name)
    for name in _DATE_FIELDS:
        v = request[name]
        if v is not None and (isinstance(v, bool)
                              or not isinstance(v, int) or v < 0):
            raise InvalidInput("%s must be null or an integer >= 0" % name)
    if exists is False and (etag is not None or lm is not None):
        raise InvalidInput(
            "absent representation must have null etag and last_modified")

    # Clause 3 on the current representation's entity-tag.
    cur_tag = None
    if etag is not None:
        cur_tag = _entity_tag(etag)
        if cur_tag is None:
            raise InvalidInput("malformed entity-tag in current.etag")

    # Clauses 3-4 on the two entity-tag precondition fields, for every input.
    parsed = {}
    for name in _TAG_FIELDS:
        v = request[name]
        parsed[name] = None if v is None else _precondition_members(v, name)

    # Clause 7: a cache does not evaluate the origin-only preconditions; RFC
    # 9111 4.3.2 makes If-Match and If-Unmodified-Since inapplicable to a
    # cache. Evaluation starts at clause 10.
    if role == "origin":
        # Clause 8: If-Match, strong comparison (RFC 9110 13.1.1).
        if request["if_match"] is not None:
            kind, payload = parsed["if_match"]
            if kind == "star":
                ok = exists
            else:
                ok = any(_strong_eq(t, cur_tag) for t in payload)
            if not ok:
                return {"decision": "412", "precondition": "if_match"}
        # Clause 9: If-Unmodified-Since, only when If-Match is absent and a
        # modification date exists; true iff last_modified <= value.
        elif (request["if_unmodified_since"] is not None
                and lm is not None
                and lm > request["if_unmodified_since"]):
            return {"decision": "412", "precondition": "if_unmodified_since"}

    # Clause 10: If-None-Match, weak comparison, both roles (RFC 9110 13.1.2).
    if request["if_none_match"] is not None:
        kind, payload = parsed["if_none_match"]
        if kind == "star":
            failed = exists
        else:
            failed = any(_weak_eq(t, cur_tag) for t in payload)
        if failed:
            decision = "304" if method in _SAFE_METHODS else "412"
            return {"decision": decision, "precondition": "if_none_match"}

    # Clause 11: If-Modified-Since, GET/HEAD only and never alongside
    # If-None-Match (RFC 9110 13.1.3, 13.2.2 step 4). The condition is false
    # -- and the answer 304 -- iff last_modified <= value.
    if (method in _SAFE_METHODS
            and request["if_none_match"] is None
            and request["if_modified_since"] is not None
            and lm is not None
            and lm <= request["if_modified_since"]):
        return {"decision": "304", "precondition": "if_modified_since"}

    # Clause 12.
    return {"decision": "200", "precondition": None}


def _process(data):
    """Stdin bytes or text -> (exit_code, stdout_text, stderr_text); no real stdio."""
    try:
        inp = json.loads(data)
    except Exception:
        return 1, "", "invalid_input: input is not valid JSON\n"
    try:
        result = evaluate(inp)
    except InvalidInput as exc:
        return 1, "", "invalid_input: %s\n" % exc
    return 0, json.dumps(result) + "\n", ""


def _case(method="GET", exists=True, etag=None, last_modified=None,
          if_match=None, if_none_match=None, if_modified_since=None,
          if_unmodified_since=None, role=None):
    """Build one contract input document; role=None omits the optional key."""
    doc = {
        "method": method,
        "current": {"exists": exists, "etag": etag,
                    "last_modified": last_modified},
        "request": {
            "if_match": if_match,
            "if_none_match": if_none_match,
            "if_modified_since": if_modified_since,
            "if_unmodified_since": if_unmodified_since,
        },
    }
    if role is not None:
        doc["role"] = role
    return doc


def selftest():
    """In-memory fixtures asserting exit codes, payloads and refusal ids."""
    strong_a = '"vx-9"'
    cases = [
        # --- decisions: 200 with no deciding precondition -------------------
        ("d01", _case(etag=strong_a, last_modified=64010),
         ("ok", "200", None)),
        ("d02", _case(etag=strong_a, if_match=strong_a),
         ("ok", "200", None)),
        ("d03", _case(method="DELETE", etag=strong_a, if_none_match='"zz-1"'),
         ("ok", "200", None)),
        ("d04", _case(etag=strong_a, if_match="*"),
         ("ok", "200", None)),
        ("d05", _case(exists=False, etag=None, last_modified=None,
                      if_none_match="*"),
         ("ok", "200", None)),
        ("d06", _case(etag='""', if_match='""'),
         ("ok", "200", None)),
        ("d07", _case(etag=strong_a, last_modified=64010,
                      if_modified_since=63000),
         ("ok", "200", None)),
        ("d08", _case(method="POST", etag=strong_a, last_modified=64010,
                      if_modified_since=65000),
         ("ok", "200", None)),
        ("d09", _case(method="get", etag=strong_a, last_modified=64010,
                      if_modified_since=65000),
         ("ok", "200", None)),
        ("d10", _case(etag=strong_a, last_modified=None,
                      if_modified_since=65000),
         ("ok", "200", None)),
        ("d11", _case(etag=strong_a, last_modified=None,
                      if_unmodified_since=63000),
         ("ok", "200", None)),
        ("d12", _case(etag=strong_a, last_modified=64010,
                      if_none_match='"zz-1"', if_modified_since=65000),
         ("ok", "200", None)),
        ("d13", _case(etag=strong_a, last_modified=64010,
                      if_match=strong_a, if_unmodified_since=63000),
         ("ok", "200", None)),
        ("d14", _case(etag=None, last_modified=None, if_none_match='"zz-1"'),
         ("ok", "200", None)),
        ("d15", _case(etag=strong_a, if_match=' * '),
         ("ok", "200", None)),
        ("d16", _case(etag=strong_a, if_match='\t"vx-9"\t'),
         ("ok", "200", None)),
        ("d17", _case(etag=strong_a, role="cache", if_match='"zz-1"'),
         ("ok", "200", None)),
        ("d18", _case(etag=strong_a, last_modified=64010, role="cache",
                      if_unmodified_since=63000),
         ("ok", "200", None)),
        # --- decisions: 412 --------------------------------------------------
        ("d19", _case(etag=strong_a, if_match='"zz-1"'),
         ("ok", "412", "if_match")),
        ("d20", _case(exists=False, etag=None, last_modified=None,
                      if_match="*"),
         ("ok", "412", "if_match")),
        ("d21", _case(exists=False, etag=None, last_modified=None,
                      if_match='"zz-1"'),
         ("ok", "412", "if_match")),
        ("d22", _case(etag='W/"vx-9"', if_match=strong_a),
         ("ok", "412", "if_match")),
        ("d23", _case(etag=strong_a, if_match='W/"vx-9"'),
         ("ok", "412", "if_match")),
        ("d24", _case(etag='W/"vx-9"', if_match='W/"vx-9"'),
         ("ok", "412", "if_match")),
        ("d25", _case(etag=strong_a, last_modified=64010,
                      if_unmodified_since=63000),
         ("ok", "412", "if_unmodified_since")),
        ("d26", _case(method="POST", etag=strong_a, if_none_match=strong_a),
         ("ok", "412", "if_none_match")),
        ("d27", _case(method="get", etag=strong_a, if_none_match=strong_a),
         ("ok", "412", "if_none_match")),
        ("d28", _case(method="PUT", etag=strong_a, if_none_match=strong_a),
         ("ok", "412", "if_none_match")),
        ("d29", _case(etag=strong_a, if_match='"zz-1"',
                      if_none_match=strong_a),
         ("ok", "412", "if_match")),
        ("d30", _case(etag=None, last_modified=None, if_match='"zz-1"'),
         ("ok", "412", "if_match")),
        # --- decisions: 304 --------------------------------------------------
        ("d31", _case(etag=strong_a, if_none_match='W/"vx-9"'),
         ("ok", "304", "if_none_match")),
        ("d32", _case(method="HEAD", etag=strong_a, if_none_match=strong_a),
         ("ok", "304", "if_none_match")),
        ("d33", _case(etag='W/"vx-9"', if_none_match=strong_a),
         ("ok", "304", "if_none_match")),
        ("d34", _case(etag=strong_a, if_none_match="*"),
         ("ok", "304", "if_none_match")),
        ("d35", _case(etag=strong_a, last_modified=64010,
                      if_modified_since=64010),
         ("ok", "304", "if_modified_since")),
        ("d36", _case(method="HEAD", etag=strong_a, last_modified=64010,
                      if_modified_since=65000),
         ("ok", "304", "if_modified_since")),
        ("d37", _case(etag=strong_a, if_match="*", if_none_match=strong_a),
         ("ok", "304", "if_none_match")),
        ("d38", _case(etag=strong_a, role="cache", if_none_match=strong_a),
         ("ok", "304", "if_none_match")),
        ("d39", _case(etag=strong_a, if_match='"aa-1", "vx-9", "zz-2"'),
         ("ok", "200", None)),
        ("d40", _case(etag=strong_a, if_match=' "zz-1" ,\t"vx-9" '),
         ("ok", "200", None)),
        ("d41", _case(etag=strong_a, if_none_match='"zz-1", W/"vx-9"'),
         ("ok", "304", "if_none_match")),
        ("d42", _case(exists=True, etag=None, last_modified=64010,
                      if_modified_since=65000),
         ("ok", "304", "if_modified_since")),
        # Quoted comma inside an opaque-tag is legal (etagc includes 0x2C).
        ("d43", _case(etag='"a,b"', if_match='"a,b"'),
         ("ok", "200", None)),
        ("d44", _case(etag='"a,b"', if_match='"a", "b"'),
         ("ok", "412", "if_match")),
        ("d45", _case(etag='"a,b"', if_none_match='W/"a,b", "c"'),
         ("ok", "304", "if_none_match")),
        # --- refusals ---------------------------------------------------------
        ("r01", "this is not json", ("refuse", "input is not valid JSON")),
        ("r02", "[1, 2]", ("refuse", "input is not a JSON object")),
        ("r03", '{"method": "GET"}',
         ("refuse", "missing top-level key: current")),
        ("r04", '{"method": "GET", "current": {"exists": true, "etag": null,'
               ' "last_modified": null}, "request": {"if_match": null,'
               ' "if_none_match": null, "if_modified_since": null,'
               ' "if_unmodified_since": null}, "zzz": 1}',
         ("refuse", "unknown top-level key: zzz")),
        ("r05", dict(_case(), role="proxy"),
         ("refuse", "role must be \"origin\" or \"cache\"")),
        ("r06", dict(_case(), role=None),
         ("refuse", "role must be \"origin\" or \"cache\"")),
        ("r07", _case(method=""),
         ("refuse", "method must be a non-empty HTTP token")),
        ("r08", _case(method="GE T"),
         ("refuse", "method must be a non-empty HTTP token")),
        ("r09", _case(method=200),
         ("refuse", "method must be a non-empty HTTP token")),
        ("r10", _case(method="GÉT"),
         ("refuse", "method must be a non-empty HTTP token")),
        ("r11", dict(_case(), current=5),
         ("refuse", "current must be an object with exactly exists, etag,"
                    " last_modified")),
        ("r12", '{"method": "GET", "current": {"exists": true, "etag": null},'
               ' "request": {"if_match": null, "if_none_match": null,'
               ' "if_modified_since": null, "if_unmodified_since": null}}',
         ("refuse", "current must be an object with exactly exists, etag,"
                    " last_modified")),
        ("r13", '{"method": "GET", "current": {"exists": true, "etag": null,'
               ' "last_modified": null, "extra": 0}, "request": {"if_match":'
               ' null, "if_none_match": null, "if_modified_since": null,'
               ' "if_unmodified_since": null}}',
         ("refuse", "current must be an object with exactly exists, etag,"
                    " last_modified")),
        ("r14", '{"method": "GET", "current": {"exists": true, "etag": null,'
               ' "last_modified": null}, "request": {"if_match": null,'
               ' "if_none_match": null, "if_modified_since": null}}',
         ("refuse", "request must be an object with exactly the four"
                    " precondition keys")),
        ("r15", '{"method": "GET", "current": {"exists": true, "etag": null,'
               ' "last_modified": null}, "request": {"if_match": null,'
               ' "if_none_match": null, "if_modified_since": null,'
               ' "if_unmodified_since": null, "if_range": null}}',
         ("refuse", "request must be an object with exactly the four"
                    " precondition keys")),
        ("r16", _case(exists=1),
         ("refuse", "exists must be a boolean")),
        ("r17", _case(exists="true"),
         ("refuse", "exists must be a boolean")),
        ("r18", _case(etag=200),
         ("refuse", "etag must be null or a string")),
        ("r19", _case(etag="x"),
         ("refuse", "malformed entity-tag in current.etag")),
        ("r20", _case(etag='w/"vx-9"'),
         ("refuse", "malformed entity-tag in current.etag")),
        ("r21", _case(etag='"a\x7fb"'),
         ("refuse", "malformed entity-tag in current.etag")),
        ("r22", _case(last_modified=-1),
         ("refuse", "last_modified must be null or an integer >= 0")),
        ("r23", _case(last_modified=True),
         ("refuse", "last_modified must be null or an integer >= 0")),
        ("r24", _case(last_modified=1.5),
         ("refuse", "last_modified must be null or an integer >= 0")),
        ("r25", _case(exists=False, etag='"vx-9"', last_modified=None),
         ("refuse", "absent representation must have null etag and"
                    " last_modified")),
        ("r26", _case(exists=False, etag=None, last_modified=3),
         ("refuse", "absent representation must have null etag and"
                    " last_modified")),
        ("r27", _case(if_match=""),
         ("refuse", "if_match must not be an empty value")),
        ("r28", _case(if_none_match="   "),
         ("refuse", "if_none_match must not be an empty value")),
        ("r29", _case(if_match='"a",,"b"'),
         ("refuse", "if_match has an empty list member")),
        ("r30", _case(if_match='*,"a"'),
         ("refuse", "if_match mixes '*' with other members")),
        ("r31", _case(if_none_match='*, "*"'),
         ("refuse", "if_none_match mixes '*' with other members")),
        ("r32", _case(if_match='"unclosed'),
         ("refuse", "malformed entity-tag in if_match")),
        ("r33", _case(if_none_match='W/ "vx-9"'),
         ("refuse", "malformed entity-tag in if_none_match")),
        ("r34", _case(if_match=200),
         ("refuse", "if_match must be null or a string")),
        ("r35", _case(if_modified_since="100"),
         ("refuse", "if_modified_since must be null or an integer >= 0")),
        ("r36", _case(if_unmodified_since=-3),
         ("refuse", "if_unmodified_since must be null or an integer >= 0")),
        ("r37", _case(if_modified_since=True),
         ("refuse", "if_modified_since must be null or an integer >= 0")),
        ("r38", _case(role="cache", if_match='"unclosed'),
         ("refuse", "malformed entity-tag in if_match")),
        ("r39", _case(if_none_match="a b"),
         ("refuse", "malformed entity-tag in if_none_match")),
        ("r40", _case(method="GE/T"),
         ("refuse", "method must be a non-empty HTTP token")),
        ("r41", _case(if_match='"a"extra'),
         ("refuse", "malformed entity-tag in if_match")),
        ("r42", _case(if_match='*,'),
         ("refuse", "if_match has an empty list member")),
        ("r43", _case(if_match='"a,'),
         ("refuse", "malformed entity-tag in if_match")),
        ("r44", _case(if_match='"a", "b'),
         ("refuse", "malformed entity-tag in if_match")),
        ("r45", b'\xff\xfe{"method":"GET"}',
         ("refuse", "input is not valid JSON")),
    ]
    passed = 0
    failures = []
    for cid, inp, want in cases:
        data = inp if isinstance(inp, (str, bytes)) else json.dumps(inp)
        rc, out, err = _process(data)
        if want[0] == "ok":
            expected_out = json.dumps(
                {"decision": want[1], "precondition": want[2]}) + "\n"
            good = rc == 0 and out == expected_out and err == ""
        else:
            good = (rc == 1 and out == ""
                    and err == "invalid_input: %s\n" % want[1])
        if good:
            passed += 1
        else:
            failures.append(
                "%s: rc=%r out=%r err=%r want=%r"
                % (cid, rc, out, err, want))
    for line in failures:
        sys.stderr.write("selftest FAIL %s\n" % line)
    sys.stdout.write("selftest %d/%d\n" % (passed, len(cases)))
    return 0 if not failures else 1


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if "--selftest" in args:
        return selftest()
    rc, out, err = _process(sys.stdin.buffer.read())
    if out:
        sys.stdout.write(out)
    if err:
        sys.stderr.write(err)
    return rc


if __name__ == "__main__":
    sys.exit(main())
