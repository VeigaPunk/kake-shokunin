#!/usr/bin/env python3
"""Decide what a cache may do with one stored response.

Reads one JSON object on stdin describing a stored response, the request that
presents it, the caller's notion of "now", and a shared-cache flag; writes one
JSON object on stdout:

    {"decision": "<member>", "freshness_lifetime": <int|null>, "current_age": <int|null>}

where <member> is one of:

    reuse                  fresh response, may be reused as-is
    revalidate             stale or otherwise unusable as-is; revalidate first
    serve-stale            stale, but the request's max-stale allows serving it
    must-revalidate-fail   stale under must-revalidate/proxy-revalidate: do not serve
    not-storable           the response was never storable; no age is reported
    heuristic-undecided    no explicit freshness lifetime; this contract guesses nothing
    only-if-cached-miss    request carries only-if-cached and the response is not reusable

Malformed input is refused with ``invalid_input: <reason>`` on stderr, exit 1,
and nothing on stdout.

What this tool deliberately does not do (contract scope, stated up front):
  * no HTTP-date parsing -- ``Date`` and ``Expires`` are integer epoch-seconds
    values, the lane's adapter convention, shared with
    ``scripts/cache_current_age.py``;
  * no clock -- time enters only as the caller-supplied integer ``now``;
  * no network, no revalidation exchange (RFC 9111 4.3), no cache store, and
    no statement about any live property;
  * no heuristic freshness (RFC 9111 4.2.2) -- with no max-age/s-maxage and no
    Expires the answer is ``heuristic-undecided``, never a guessed lifetime;
  * no storage-key identity, no Vary field matching, and no decision to serve
    stale without a client directive (4.2.4's permission, not a preference).

Contract: ``.ufo/waves/round-91/c2-contract.md`` (v1). Clause numbers from the
contract appear in comments wherever a reader would otherwise have to guess.

Usage:
    stored_reuse.py              one JSON object on stdin, one on stdout
    stored_reuse.py --selftest   in-memory fixtures, prints a "selftest K/K" line
"""

from __future__ import annotations

import json
import re
import sys

# Clause 10: the only statuses a shared/non-shared cache may store.
CACHEABLE_STATUS = (200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501)
# Clause 4: directives whose argument is delta-seconds.
DELTA_SECONDS = ("max-age", "s-maxage", "min-fresh")

_ASCII_LOWER = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")


class InvalidInput(Exception):
    """The input violates the contract: refusal with exit 1."""


def ascii_lower(name):
    """Clause 1: case folding over ASCII A-Z only, leaving other bytes alone."""
    return name.translate(_ASCII_LOWER)


def read_headers(headers):
    """Validate a header map and return {lowercased-name: trimmed-value}.

    Clause 1: names match case-insensitively; two names differing only in case
    are a refusal. Clause 2: values are trimmed of leading/trailing SP and
    HTAB and are otherwise byte-exact; CR, LF and NUL are refusals. Clause 3:
    names and values must be strings.
    """
    if not isinstance(headers, dict):
        raise InvalidInput("headers must be an object")
    out = {}
    for name, value in headers.items():
        if not isinstance(name, str) or not isinstance(value, str):
            raise InvalidInput("header names and values must be strings")
        if not name:
            raise InvalidInput("empty header name")
        key = ascii_lower(name)
        if key in out:
            raise InvalidInput("duplicate header name: %s" % name)
        if "\r" in value or "\n" in value or "\0" in value:
            raise InvalidInput("control character in header value: %s" % name)
        out[key] = value.strip(" \t")
    return out


def parse_cache_control(value):
    """Clause 4: split on commas, trim, lowercase names, read arguments.

    A delta-seconds argument must be a bare non-negative decimal integer; a
    quoted or signed form is a refusal. The same directive name twice with
    different arguments is a refusal. Unknown names are kept (and ignored
    later), so their parsing failures still refuse.
    """
    directives = {}
    for raw in value.split(","):
        directive = raw.strip(" \t")
        if not directive:
            raise InvalidInput("empty Cache-Control directive")
        name, has_arg, argument = directive.partition("=")
        name = ascii_lower(name.strip(" \t"))
        if not name:
            raise InvalidInput("empty Cache-Control directive name")
        if has_arg:
            argument = argument.strip(" \t")
            quoted = len(argument) >= 2 and argument[0] == '"' and argument[-1] == '"'
            if quoted:
                argument = argument[1:-1]
            if name in DELTA_SECONDS or name == "max-stale":
                if quoted:
                    raise InvalidInput("quoted delta-seconds argument: %s" % name)
                if not re.fullmatch(r"[0-9]+", argument):
                    raise InvalidInput(
                        "delta-seconds must be a bare non-negative integer: %s" % name)
                parsed = int(argument)
            else:
                parsed = argument
        else:
            parsed = None
        if name in directives and directives[name] != parsed:
            raise InvalidInput("duplicate Cache-Control directive: %s" % name)
        directives[name] = parsed
    return directives


def integer_header(headers, name, allow_negative):
    """Clauses 5-7: Date/Age/Expires are decimal integers, not HTTP-dates."""
    raw = headers[name]
    if not re.fullmatch(r"-?[0-9]+", raw):
        raise InvalidInput("%s must be a decimal integer" % name)
    number = int(raw)
    if not allow_negative and number < 0:
        raise InvalidInput("%s must be nonnegative" % name)
    return number


def validate(inp):
    """Input section of the contract: shape, types, and required keys."""
    if not isinstance(inp, dict):
        raise InvalidInput("input must be a JSON object")
    if set(inp) - {"stored", "request", "now", "shared"}:
        raise InvalidInput("unknown top-level input key")
    for key in ("stored", "request", "now"):
        if key not in inp:
            raise InvalidInput("missing input key: %s" % key)
    stored, request, now = inp["stored"], inp["request"], inp["now"]
    if not isinstance(stored, dict) or not isinstance(request, dict):
        raise InvalidInput("stored and request must be objects")
    if set(stored) - {"status", "headers"}:
        raise InvalidInput("unknown key in stored")
    if set(request) - {"method", "headers"}:
        raise InvalidInput("unknown key in request")
    if "status" not in stored:
        raise InvalidInput("stored response has no status")
    status = stored["status"]
    # bool is an int subclass in Python; a JSON true/false status is a refusal.
    if not isinstance(status, int) or isinstance(status, bool) or not 100 <= status <= 599:
        raise InvalidInput("stored status must be an integer 100..599")
    if "method" not in request:
        raise InvalidInput("request has no method")
    method = request["method"]
    if not isinstance(method, str) or not method:
        raise InvalidInput("request method must be a nonempty string")
    if not isinstance(now, int) or isinstance(now, bool) or now < 0:
        raise InvalidInput("now must be a nonnegative integer")
    shared = inp.get("shared", False)
    if not isinstance(shared, bool):
        raise InvalidInput("shared must be a boolean")
    return stored, request, now, shared


def decide(stored, request, now, shared):
    """Clauses 1-21: validate everything, derive the lifetime, then decide."""
    stored_headers = read_headers(stored.get("headers", {}))    # clauses 1-3
    request_headers = read_headers(request.get("headers", {}))
    stored_cc = (parse_cache_control(stored_headers["cache-control"])
                 if "cache-control" in stored_headers else {})
    request_cc = (parse_cache_control(request_headers["cache-control"])
                  if "cache-control" in request_headers else {})

    # Clauses 5-8 run before any decision: a missing or malformed Date is a
    # refusal even when the response turns out not to be storable.
    if "date" not in stored_headers:
        raise InvalidInput("stored response has no Date header")
    date_value = integer_header(stored_headers, "date", allow_negative=True)
    age_value = (integer_header(stored_headers, "age", allow_negative=False)
                 if "age" in stored_headers else 0)
    expires_value = (integer_header(stored_headers, "expires", allow_negative=True)
                     if "expires" in stored_headers else None)
    current_age = max(0, age_value) + max(0, now - date_value)   # clause 8

    # Clause 9: freshness lifetime precedence s-maxage > max-age > Expires-Date.
    if shared and "s-maxage" in stored_cc:
        lifetime = stored_cc["s-maxage"]
    elif "max-age" in stored_cc:
        lifetime = stored_cc["max-age"]
    elif expires_value is not None:
        lifetime = expires_value - date_value
    else:
        lifetime = None

    # Clause 10: storability, checked before anything else is decided.
    vary_value = stored_headers.get("vary")
    vary_star = (vary_value is not None
                 and any(m.strip(" \t") == "*" for m in vary_value.split(",")))
    storable = (request["method"] in ("GET", "HEAD")
                and stored["status"] in CACHEABLE_STATUS
                and "no-store" not in stored_cc
                and "no-store" not in request_cc
                and not ("private" in stored_cc and shared)
                and not vary_star)
    if not storable:
        # No arithmetic is reported for a response that is not stored.
        return {"decision": "not-storable", "freshness_lifetime": None,
                "current_age": None}

    # Clauses 11-19: first match wins.
    if lifetime is None:
        decision = "heuristic-undecided"                          # clause 11
    elif "no-cache" in request_cc:
        decision = "revalidate"                                   # clause 12
    elif "no-cache" in stored_cc:
        decision = "revalidate"                                   # clause 13
    elif "max-age" in request_cc and current_age > request_cc["max-age"]:
        decision = "revalidate"                                   # clause 14
    elif "min-fresh" in request_cc and lifetime - current_age < request_cc["min-fresh"]:
        decision = "revalidate"                                   # clause 15
    elif current_age < lifetime:
        decision = "reuse"                                        # clause 16
    elif "must-revalidate" in stored_cc or ("proxy-revalidate" in stored_cc and shared):
        decision = "must-revalidate-fail"                         # clause 17
    elif ("max-stale" in request_cc
          and (request_cc["max-stale"] is None
               or current_age - lifetime <= request_cc["max-stale"])):
        decision = "serve-stale"                                  # clause 18
    else:
        decision = "revalidate"                                   # clause 19

    # Clause 20: only-if-cached turns any non-reusable, storable decision into a miss.
    if "only-if-cached" in request_cc and decision not in ("reuse", "not-storable"):
        decision = "only-if-cached-miss"

    # Clause 21: derived values are reported for every non-refused, storable input.
    return {"decision": decision, "freshness_lifetime": lifetime,
            "current_age": current_age}


def evaluate(inp):
    return decide(*validate(inp))


# --------------------------------------------------------------------------
# --selftest: the contract's 45 worked cases, in memory, no files written.
# --------------------------------------------------------------------------

def _case(stored_extra, method, now, *, status=200, request_extra=None,
          shared=False, date=1000000, decision=None, lifetime=None, ageout=None):
    stored_headers = {"Date": str(date)}
    stored_headers.update(stored_extra or {})
    request_headers = request_extra or {}
    inp = {"stored": {"status": status, "headers": stored_headers},
           "request": {"method": method, "headers": request_headers},
           "now": now, "shared": shared}
    expected = None if decision is None else {
        "decision": decision, "freshness_lifetime": lifetime,
        "current_age": ageout}
    return inp, expected


def selftest():
    cases = [
        # Contract worked cases 1-5: freshness boundary and max-stale.
        (_case({"Cache-Control": "max-age=60"}, "GET", 1000030,
               decision="reuse", lifetime=60, ageout=30)),
        (_case({"Cache-Control": "max-age=60"}, "GET", 1000060,
               decision="revalidate", lifetime=60, ageout=60)),
        (_case({"Cache-Control": "max-age=60"}, "GET", 1000065,
               request_extra={"Cache-Control": "max-stale=10"},
               decision="serve-stale", lifetime=60, ageout=65)),
        (_case({"Cache-Control": "max-age=60"}, "GET", 1000071,
               request_extra={"Cache-Control": "max-stale=10"},
               decision="revalidate", lifetime=60, ageout=71)),
        (_case({"Cache-Control": "max-age=60"}, "GET", 1001000,
               request_extra={"Cache-Control": "max-stale"},
               decision="serve-stale", lifetime=60, ageout=1000)),
        # Worked cases 6-8: must-revalidate and shared-only proxy-revalidate.
        (_case({"Cache-Control": "max-age=60, must-revalidate"}, "GET", 1000061,
               request_extra={"Cache-Control": "max-stale"},
               decision="must-revalidate-fail", lifetime=60, ageout=61)),
        (_case({"Cache-Control": "max-age=60, proxy-revalidate"}, "GET", 1000061,
               request_extra={"Cache-Control": "max-stale=100"}, shared=True,
               decision="must-revalidate-fail", lifetime=60, ageout=61)),
        (_case({"Cache-Control": "max-age=60, proxy-revalidate"}, "GET", 1000061,
               request_extra={"Cache-Control": "max-stale=100"},
               decision="serve-stale", lifetime=60, ageout=61)),
        # Worked cases 9-10: s-maxage applies only to a shared cache.
        (_case({"Cache-Control": "max-age=10, s-maxage=100"}, "GET", 1000050,
               shared=True, decision="reuse", lifetime=100, ageout=50)),
        (_case({"Cache-Control": "max-age=10, s-maxage=100"}, "GET", 1000050,
               decision="revalidate", lifetime=10, ageout=50)),
        # Worked cases 11-13: Expires lifetime and heuristic-undecided.
        (_case({"Expires": "1000120"}, "GET", 1000100,
               decision="reuse", lifetime=120, ageout=100)),
        (_case({"Expires": "999900"}, "GET", 1000000,
               decision="revalidate", lifetime=-100, ageout=0)),
        (_case(None, "GET", 1000010,
               decision="heuristic-undecided", lifetime=None, ageout=10)),
        # Worked cases 14-19: request no-cache/max-age/min-fresh.
        (_case({"Cache-Control": "max-age=60"}, "GET", 1000030,
               request_extra={"Cache-Control": "no-cache"},
               decision="revalidate", lifetime=60, ageout=30)),
        (_case({"Cache-Control": "no-cache, max-age=60"}, "GET", 1000030,
               decision="revalidate", lifetime=60, ageout=30)),
        (_case({"Cache-Control": "max-age=60"}, "GET", 1000030,
               request_extra={"Cache-Control": "max-age=10"},
               decision="revalidate", lifetime=60, ageout=30)),
        (_case({"Cache-Control": "max-age=60"}, "GET", 1000030,
               request_extra={"Cache-Control": "max-age=30"},
               decision="reuse", lifetime=60, ageout=30)),
        (_case({"Cache-Control": "max-age=60"}, "GET", 1000030,
               request_extra={"Cache-Control": "min-fresh=40"},
               decision="revalidate", lifetime=60, ageout=30)),
        (_case({"Cache-Control": "max-age=60"}, "GET", 1000030,
               request_extra={"Cache-Control": "min-fresh=30"},
               decision="reuse", lifetime=60, ageout=30)),
        # Worked cases 20-21: only-if-cached converts only non-reusable decisions.
        (_case({"Cache-Control": "max-age=60"}, "GET", 1000060,
               request_extra={"Cache-Control": "only-if-cached"},
               decision="only-if-cached-miss", lifetime=60, ageout=60)),
        (_case({"Cache-Control": "max-age=60"}, "GET", 1000030,
               request_extra={"Cache-Control": "only-if-cached"},
               decision="reuse", lifetime=60, ageout=30)),
        # Worked cases 22-29: not-storable shapes; private without shared stores.
        (_case({"Cache-Control": "max-age=60"}, "POST", 1000030,
               decision="not-storable")),
        (_case({"Cache-Control": "max-age=60"}, "GET", 1000030, status=500,
               decision="not-storable")),
        (_case({"Cache-Control": "no-store, max-age=60"}, "GET", 1000030,
               decision="not-storable")),
        (_case({"Cache-Control": "max-age=60"}, "GET", 1000030,
               request_extra={"Cache-Control": "no-store"},
               decision="not-storable")),
        (_case({"Cache-Control": "private, max-age=60"}, "GET", 1000030,
               shared=True, decision="not-storable")),
        (_case({"Cache-Control": "private, max-age=60"}, "GET", 1000030,
               decision="reuse", lifetime=60, ageout=30)),
        (_case({"Cache-Control": "max-age=60", "Vary": "*"}, "GET", 1000030,
               decision="not-storable")),
        (_case({"Cache-Control": "max-age=60", "Vary": "Accept"}, "GET", 1000030,
               decision="reuse", lifetime=60, ageout=30)),
        # Worked cases 30-35: Age arithmetic, HEAD, unknown directives, precedence.
        (_case({"Age": "40", "Cache-Control": "max-age=60"}, "GET", 1000010,
               decision="reuse", lifetime=60, ageout=50)),
        (_case({"Age": "5", "Cache-Control": "max-age=60"}, "GET", 1000000,
               date=1000100, decision="reuse", lifetime=60, ageout=5)),
        (_case({"Cache-Control": "max-age=60"}, "HEAD", 1000030,
               decision="reuse", lifetime=60, ageout=30)),
        (_case({"Cache-Control": "max-age=60, foo=bar"}, "GET", 1000030,
               decision="reuse", lifetime=60, ageout=30)),
        (_case({"Cache-Control": "max-age=60, must-revalidate"}, "GET", 1000030,
               decision="reuse", lifetime=60, ageout=30)),
        (_case({"Cache-Control": "max-age=60", "Expires": "1000120"}, "GET", 1000030,
               decision="reuse", lifetime=60, ageout=30)),
        # Worked cases 36-45: refusals (36-39, 41-44) and one not-storable (45).
        (_case({"Cache-Control": 'max-age="60"'}, "GET", 1000030)),
        (_case({"Cache-Control": "max-age=60", "cache-control": "max-age=30"},
               "GET", 1000030)),
        (_case({"Cache-Control": "max-age=60", "X-Note": "a\rb"}, "GET", 1000030)),
        # Worked case 39 (Date absent): stored headers carry no Date at all.
        ({"stored": {"status": 200, "headers": {"Cache-Control": "max-age=60"}},
          "request": {"method": "GET", "headers": {}}, "now": 1000030}, None),
        (_case({"Cache-Control": "max-age=60"}, "GET", -1)),
        # Worked case 41 (unknown top-level key): raw input object.
        ({"stored": {"status": 200, "headers": {
            "Date": "1000000", "Cache-Control": "max-age=60"}},
          "request": {"method": "GET", "headers": {}}, "now": 1000030,
          "extra": 1}, None),
        (_case({"Cache-Control": "max-age=60"}, "GET", 1000030, status="200")),
        (_case({"Cache-Control": "max-age=60, max-age=30"}, "GET", 1000030)),
        (_case({"Age": "-1", "Cache-Control": "max-age=60"}, "GET", 1000030)),
        # Worked case 45: only-if-cached never turns not-storable into a miss.
        (_case({"Cache-Control": "max-age=60"}, "POST", 1000030,
               request_extra={"Cache-Control": "only-if-cached"},
               decision="not-storable")),
    ]
    passed = 0
    failures = []
    for index, (inp, expected) in enumerate(cases):
        try:
            got = evaluate(inp)
        except InvalidInput:
            if expected is not None:
                failures.append("case %d: refused, expected %s"
                                % (index + 1, expected["decision"]))
            else:
                passed += 1
            continue
        if expected is None:
            failures.append("case %d: decided %r, expected refusal" % (index + 1, got))
        elif got != expected:
            failures.append("case %d: %r != %r" % (index + 1, got, expected))
        else:
            passed += 1
    for line in failures:
        sys.stderr.write("selftest FAIL %s\n" % line)
    sys.stdout.write("selftest %d/%d\n" % (passed, len(cases)))
    return 0 if not failures else 1


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if "--selftest" in args:
        return selftest()
    try:
        try:
            inp = json.loads(sys.stdin.buffer.read())
        except ValueError as exc:  # covers bad UTF-8 and malformed JSON
            raise InvalidInput("input is not valid JSON: %s" % exc)
        result = evaluate(inp)
    except InvalidInput as exc:
        sys.stderr.write("invalid_input: %s\n" % exc)
        return 1
    sys.stdout.write(json.dumps(result) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
