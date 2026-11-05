#!/usr/bin/env python3
"""Heuristic freshness lifetime decision (RFC 9111 section 4.2.2) - round-92 C2.

Decides, over one JSON object on stdin, whether a heuristic freshness lifetime
may be assigned to a stored response and what that lifetime is. Writes one JSON
object on stdout:

    {"decision": "<member>", "lifetime": <int|null>, "heuristic": <bool>}

where <member> is one of:

    explicit                    an explicit expiration is present; heuristics
                                are never used (RFC 9111 4.2.2)
    heuristic                   a heuristic lifetime was assigned
    not-heuristically-cacheable no explicit expiration and the status is not
                                heuristically cacheable (nor marked public)
    heuristic-undecided         no explicit expiration, cacheable, but no
                                usable Last-Modified interval
    not-storable                no-store, private while shared, or Vary: *

Malformed input is refused with ``invalid_input: <reason>`` on stderr, exit 1,
and nothing on stdout.

Scope, stated up front: this is a decision over supplied integer seconds only.
It is not a clock, an HTTP-date parser, a network client, a cache store, a
revalidation exchange, or a statement about any live property. It reports the
lifetime and the heuristic flag; it does not store, reuse, serve or revalidate
anything, and it does not re-decide what ``scripts/stored_reuse.py`` (round 91)
already decides beyond the freshness lifetime.

Grounding: RFC 9111 section 4.2.2 (opened this round at
``.ufo/waves/round-92/L1/src/rfc9111.txt``, HTTP 200, 84 477 B, sha256
``aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e``). A cache
"MAY assign a heuristic expiration time when an explicit time is not
specified"; it "MUST NOT use heuristics to determine freshness when an explicit
expiration time is present"; heuristics apply only to statuses defined as
heuristically cacheable (or responses marked explicitly cacheable, e.g.
``public``); and caches are "encouraged to use a heuristic expiration value
that is no more than some fraction of the interval since that time".

LANE CONVENTIONS, not RFC requirements: the 10 % fraction (the RFC gives 10 %
only as a "typical setting" of that fraction) and the 86400-second cap (the RFC
states a worst-case constraint but names no value). Both are applied in clause
12 and are named here so a reader never mistakes them for the RFC's own text.
Also a lane adapter convention shared with ``scripts/cache_current_age.py`` and
``scripts/stored_reuse.py``: ``Date``, ``Expires`` and ``Last-Modified`` are
decimal integer epoch seconds on the wire here; no HTTP-date parsing.

Contract: ``.ufo/waves/round-92/c2-contract.md`` (v1). Clause numbers from the
contract appear in comments wherever a reader would otherwise have to guess.

Usage:
    heuristic_freshness.py              one JSON object on stdin, one on stdout
    heuristic_freshness.py --selftest   in-memory fixtures, prints "selftest K/K"

Exit codes: 0 a decision was printed; 1 the input violated the contract
(refusal line on stderr, nothing on stdout); the selftest exits 0 only when
every fixture passes.
"""

import json
import re
import sys

# Clause 11: the statuses RFC 9111 defines as heuristically cacheable.
HEURISTICALLY_CACHEABLE = (200, 203, 204, 206, 300, 301, 308, 404, 405, 410,
                           414, 501)
# Clause 4: directives whose argument is delta-seconds.
DELTA_SECONDS = ("max-age", "s-maxage")
# Clause 12, lane convention (not the RFC's): 10 % of the interval, capped.
FRACTION = 10
CAP = 86400

_ASCII_LOWER = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")


class Invalid(Exception):
    """The input violates the contract: refusal with exit 1."""


def ascii_lower(name):
    """Clause 1: case folding over ASCII A-Z only, leaving other bytes alone."""
    return name.translate(_ASCII_LOWER)


def is_int(value):
    """Clause 3: an int that is not a bool (bool is an int subclass)."""
    return isinstance(value, int) and not isinstance(value, bool)


def decimal_int(value, what):
    """Clauses 4-7: a bare non-negative decimal integer field."""
    if not re.fullmatch(r"[0-9]+", value):
        raise Invalid("%s is not a decimal integer" % what)
    return int(value)


def norm_headers(raw):
    """Clauses 1-3: validate the header map, return {lowercased: trimmed}.

    Clause 1: names match case-insensitively over ASCII; two names differing
    only in case are a refusal. Clause 2: values are trimmed of leading and
    trailing SP and HTAB and are otherwise byte-exact; CR, LF and NUL are
    refusals. Clause 3: names and values must be strings.
    """
    if not isinstance(raw, dict):
        raise Invalid("headers is not an object")
    seen = set()
    out = {}
    for name, value in raw.items():
        if not isinstance(name, str) or not isinstance(value, str):
            raise Invalid("header name or value is not a string")
        if any(c in value for c in "\r\n\0"):
            raise Invalid("header value contains CR, LF or NUL")
        low = ascii_lower(name)
        if low in seen:
            raise Invalid("duplicate header name")
        seen.add(low)
        out[low] = value.strip(" \t")
    return out


def parse_cc(value):
    """Clause 4: the Cache-Control directive grammar.

    Split on ","; each directive is trimmed of SP and HTAB; its name is
    lowercased (ASCII); an optional "=" introduces a token or a quoted-string
    argument. An empty directive is a refusal. The same directive name twice
    with different arguments is a refusal. Unknown directive names are ignored
    (they are still parsed and stored here; the decision clauses look up only
    the names they know). A delta-seconds argument must be a bare non-negative
    decimal integer: a quoted or signed form is a refusal.
    """
    out = {}
    for raw in value.split(","):
        directive = raw.strip(" \t")
        if not directive:
            raise Invalid("empty Cache-Control directive")
        name, sep, arg = directive.partition("=")
        name = ascii_lower(name.strip(" \t"))
        if not name:
            raise Invalid("empty Cache-Control directive name")
        if sep:
            arg = arg.strip(" \t")
            quoted = len(arg) >= 2 and arg[0] == '"' and arg[-1] == '"'
            if quoted:
                arg = arg[1:-1]
            if name in DELTA_SECONDS and (quoted or
                                          not re.fullmatch(r"[0-9]+", arg)):
                raise Invalid("%s argument is not a bare non-negative decimal "
                              "integer" % name)
        else:
            arg = None
        if name in out and out[name] != arg:
            raise Invalid("conflicting Cache-Control directive %s" % name)
        out[name] = arg
    return out


def decide(inp):
    """Clauses 1-8 validate everything first, then clauses 9-13 decide."""
    if not isinstance(inp, dict):
        raise Invalid("input is not an object")
    extra = set(inp) - {"stored", "now", "shared"}
    if extra:
        raise Invalid("unexpected top-level key %s" % sorted(extra)[0])
    stored = inp.get("stored")
    if not isinstance(stored, dict):
        raise Invalid("stored is not an object")
    extra = set(stored) - {"status", "headers"}
    if extra:
        raise Invalid("unexpected key in stored: %s" % sorted(extra)[0])
    status = stored.get("status")
    if not is_int(status) or not 100 <= status <= 599:
        raise Invalid("status is not an int in 100..599")
    now = inp.get("now")
    if not is_int(now) or now < 0:
        raise Invalid("now is not a non-negative int")
    shared = inp.get("shared", False)
    if not isinstance(shared, bool):
        raise Invalid("shared is not a bool")

    headers = norm_headers(stored.get("headers", {}))
    # Clause 8: every field is validated before any arithmetic or decision.
    cc = parse_cc(headers["cache-control"]) if "cache-control" in headers else {}
    if "date" not in headers:
        raise Invalid("Date is absent")
    date = decimal_int(headers["date"], "Date")
    expires = None
    if "expires" in headers:
        expires = decimal_int(headers["expires"], "Expires")
    lastmod = None
    if "last-modified" in headers:
        lastmod = decimal_int(headers["last-modified"], "Last-Modified")
    smaxage = None
    if "s-maxage" in cc:
        smaxage = decimal_int(cc["s-maxage"] or "", "s-maxage")
    maxage = None
    if "max-age" in cc:
        maxage = decimal_int(cc["max-age"] or "", "max-age")

    # Clause 9: not-storable.
    vary_star = False
    if "vary" in headers:
        vary_star = any(m.strip(" \t") == "*"
                        for m in headers["vary"].split(","))
    if "no-store" in cc or ("private" in cc and shared) or vary_star:
        return {"decision": "not-storable", "lifetime": None,
                "heuristic": False}

    # Clause 10: explicit wins, first match; heuristics are never used.
    if shared and smaxage is not None:
        return {"decision": "explicit", "lifetime": smaxage, "heuristic": False}
    if maxage is not None:
        return {"decision": "explicit", "lifetime": maxage, "heuristic": False}
    if expires is not None:
        return {"decision": "explicit", "lifetime": expires - date,
                "heuristic": False}

    # Clause 11: the heuristically-cacheable gate (public marks explicitly
    # cacheable).
    if status not in HEURISTICALLY_CACHEABLE and "public" not in cc:
        return {"decision": "not-heuristically-cacheable", "lifetime": None,
                "heuristic": False}

    # Clause 12: heuristic, with the lane's 10 % fraction and 86400 s cap.
    if lastmod is not None and lastmod <= date:
        return {"decision": "heuristic",
                "lifetime": min((date - lastmod) // FRACTION, CAP),
                "heuristic": True}

    # Clause 13: no usable Last-Modified interval supports an estimate.
    return {"decision": "heuristic-undecided", "lifetime": None,
            "heuristic": False}


def refuse(reason):
    sys.stderr.write("invalid_input: %s\n" % reason)
    return 1


def run_case(name, inp, expected):
    """Run one in-memory fixture; return a failure string or None."""
    try:
        got = decide(inp)
    except Invalid as exc:
        got = None
        detail = str(exc)
    else:
        detail = ""
    if expected is None:
        if got is None:
            return None
        return "%s: expected refusal, got %r" % (name, got)
    if got == expected:
        return None
    return "%s: expected %r got %r %s" % (name, expected, got, detail)


def selftest():
    """In-memory fixtures over clauses 1-13; no files are written."""
    cases = hand_cases()
    failures = []
    for name, inp, expected in cases:
        why = run_case(name, inp, expected)
        if why is not None:
            failures.append(why)
    for line in failures:
        sys.stderr.write(line + "\n")
    print("selftest %d/%d" % (len(cases) - len(failures), len(cases)))
    return 0 if not failures else 1


def hand_cases():
    """The contract's worked fixtures: (name, input, expected-or-None).

    The first 28 mirror the frozen counter's declared hand cases; the rest
    cover refusal and boundary shapes the contract states that the counter's
    frozen set does not exercise (clause 2 CR/LF/NUL, clause 3 types, clause 4
    quoted/conflicting directives, clause 8 validation before decision).
    """
    def H(name, status, headers, expected, now=1000000, shared=None):
        inp = {"stored": {"status": status, "headers": headers}, "now": now}
        if shared is not None:
            inp["shared"] = shared
        return (name, inp, expected)

    C = []
    # clause 10 - explicit wins, heuristics never used
    C.append(H("explicit/max-age", 200,
               {"Date": "1000000", "Cache-Control": "max-age=600",
                "Last-Modified": "900000"},
               {"decision": "explicit", "lifetime": 600, "heuristic": False}))
    C.append(H("explicit/s-maxage-shared", 200,
               {"Date": "1000000", "Cache-Control": "s-maxage=120, max-age=600"},
               {"decision": "explicit", "lifetime": 120, "heuristic": False},
               shared=True))
    C.append(H("explicit/s-maxage-ignored-private", 200,
               {"Date": "1000000", "Cache-Control": "s-maxage=120, max-age=600"},
               {"decision": "explicit", "lifetime": 600, "heuristic": False},
               shared=False))
    C.append(H("explicit/expires-minus-date", 200,
               {"Date": "1000000", "Expires": "1000300",
                "Last-Modified": "900000"},
               {"decision": "explicit", "lifetime": 300, "heuristic": False}))
    C.append(H("explicit/expires-before-date-negative", 200,
               {"Date": "1000000", "Expires": "999900"},
               {"decision": "explicit", "lifetime": -100, "heuristic": False}))
    C.append(H("explicit/max-age-beats-expires", 200,
               {"Date": "1000000", "Expires": "1000300",
                "Cache-Control": "max-age=5"},
               {"decision": "explicit", "lifetime": 5, "heuristic": False}))
    # clause 12 - heuristic arithmetic and its boundaries
    C.append(H("heuristic/ten-percent", 200,
               {"Date": "1000000", "Last-Modified": "990000"},
               {"decision": "heuristic", "lifetime": 1000, "heuristic": True}))
    C.append(H("heuristic/floor", 200,
               {"Date": "1000000", "Last-Modified": "999989"},
               {"decision": "heuristic", "lifetime": 1, "heuristic": True}))
    C.append(H("heuristic/floor-below-one", 200,
               {"Date": "1000000", "Last-Modified": "999999"},
               {"decision": "heuristic", "lifetime": 0, "heuristic": True}))
    C.append(H("heuristic/equal-timestamps", 200,
               {"Date": "1000000", "Last-Modified": "1000000"},
               {"decision": "heuristic", "lifetime": 0, "heuristic": True}))
    C.append(H("heuristic/cap-86400", 200,
               {"Date": "1000000", "Last-Modified": "100000"},
               {"decision": "heuristic", "lifetime": 86400,
                "heuristic": True}))
    C.append(H("heuristic/cap-exact-boundary", 200,
               {"Date": "1864000", "Last-Modified": "1000000"},
               {"decision": "heuristic", "lifetime": 86400,
                "heuristic": True}))
    C.append(H("heuristic/just-below-cap", 200,
               {"Date": "1863999", "Last-Modified": "1000000"},
               {"decision": "heuristic", "lifetime": 86399,
                "heuristic": True}))
    # clause 11 - the cacheability gate
    C.append(H("gate/404-heuristically-cacheable", 404,
               {"Date": "1000000", "Last-Modified": "990000"},
               {"decision": "heuristic", "lifetime": 1000, "heuristic": True}))
    C.append(H("gate/500-not-cacheable", 500,
               {"Date": "1000000", "Last-Modified": "990000"},
               {"decision": "not-heuristically-cacheable", "lifetime": None,
                "heuristic": False}))
    C.append(H("gate/500-public-overrides", 500,
               {"Date": "1000000", "Cache-Control": "public",
                "Last-Modified": "990000"},
               {"decision": "heuristic", "lifetime": 1000, "heuristic": True}))
    C.append(H("gate/200-no-last-modified", 200, {"Date": "1000000"},
               {"decision": "heuristic-undecided", "lifetime": None,
                "heuristic": False}))
    C.append(H("gate/last-modified-after-date", 200,
               {"Date": "1000000", "Last-Modified": "1000001"},
               {"decision": "heuristic-undecided", "lifetime": None,
                "heuristic": False}))
    # clause 9 - not-storable
    C.append(H("store/no-store", 200,
               {"Date": "1000000", "Cache-Control": "no-store",
                "Last-Modified": "990000"},
               {"decision": "not-storable", "lifetime": None,
                "heuristic": False}))
    C.append(H("store/private-shared", 200,
               {"Date": "1000000", "Cache-Control": "private",
                "Last-Modified": "990000"},
               {"decision": "not-storable", "lifetime": None,
                "heuristic": False}, shared=True))
    C.append(H("store/private-not-shared", 200,
               {"Date": "1000000", "Cache-Control": "private",
                "Last-Modified": "990000"},
               {"decision": "heuristic", "lifetime": 1000,
                "heuristic": True}, shared=False))
    C.append(H("store/vary-star", 200,
               {"Date": "1000000", "Vary": "Accept-Encoding, *",
                "Last-Modified": "990000"},
               {"decision": "not-storable", "lifetime": None,
                "heuristic": False}))
    C.append(H("store/vary-members-not-star", 200,
               {"Date": "1000000", "Vary": "Accept-Encoding, User-Agent",
                "Last-Modified": "990000"},
               {"decision": "heuristic", "lifetime": 1000,
                "heuristic": True}))
    # clauses 1-7 - refusals
    C.append(H("refuse/date-absent", 200, {"Last-Modified": "990000"}, None))
    C.append(H("refuse/date-non-integer", 200, {"Date": "1e6"}, None))
    C.append(H("refuse/duplicate-header-name", 200,
               {"Date": "1000000", "date": "1000000"}, None))
    C.append(H("refuse/delta-seconds-signed", 200,
               {"Date": "1000000", "Cache-Control": "max-age=+5"}, None))
    C.append(H("refuse/empty-directive", 200,
               {"Date": "1000000", "Cache-Control": "max-age=5, "}, None))

    # Additional fixtures for contract shapes the frozen hand set does not
    # carry. Same tuple shape; expected None means a refusal.
    C.append(H("refuse/value-cr", 200,
               {"Date": "1000000", "X-Note": "a\rb"}, None))
    C.append(H("refuse/value-lf", 200,
               {"Date": "1000000", "X-Note": "a\nb"}, None))
    C.append(H("refuse/value-nul", 200,
               {"Date": "1000000", "X-Note": "a\0b"}, None))
    C.append(("refuse/status-bool",
              {"stored": {"status": True, "headers": {"Date": "1000000"}},
               "now": 1000000}, None))
    C.append(("refuse/status-float",
              {"stored": {"status": 200.5, "headers": {"Date": "1000000"}},
               "now": 1000000}, None))
    C.append(("refuse/status-out-of-range",
              {"stored": {"status": 99, "headers": {"Date": "1000000"}},
               "now": 1000000}, None))
    C.append(("refuse/now-negative",
              {"stored": {"status": 200, "headers": {"Date": "1000000"}},
               "now": -1}, None))
    C.append(("refuse/now-bool",
              {"stored": {"status": 200, "headers": {"Date": "1000000"}},
               "now": True}, None))
    C.append(("refuse/shared-string",
              {"stored": {"status": 200, "headers": {"Date": "1000000"}},
               "now": 1000000, "shared": "yes"}, None))
    C.append(("refuse/unexpected-top-key",
              {"stored": {"status": 200, "headers": {"Date": "1000000"}},
               "now": 1000000, "method": "GET"}, None))
    C.append(("refuse/stored-extra-key",
              {"stored": {"status": 200, "headers": {"Date": "1000000"},
                          "request": {}}, "now": 1000000}, None))
    C.append(("refuse/headers-not-object",
              {"stored": {"status": 200, "headers": []}, "now": 1000000},
              None))
    C.append(("refuse/header-value-not-string",
              {"stored": {"status": 200, "headers": {"Date": 1000000}},
               "now": 1000000}, None))
    C.append(("refuse/input-not-object", [1, 2], None))
    # Clause 8: validation runs even when the response is not storable.
    C.append(H("refuse/expires-non-integer-despite-no-store", 200,
               {"Date": "1000000", "Expires": "1e6",
                "Cache-Control": "no-store"}, None))
    C.append(H("refuse/last-modified-non-integer", 200,
               {"Date": "1000000", "Last-Modified": "990000.5"}, None))
    C.append(H("refuse/s-maxage-bare", 200,
               {"Date": "1000000", "Cache-Control": "s-maxage"}, None))
    # Clause 4: a quoted delta-seconds argument is a refusal (contract text).
    C.append(H("refuse/delta-seconds-quoted", 200,
               {"Date": "1000000", "Cache-Control": 'max-age="5"'}, None))
    C.append(H("refuse/conflicting-directives", 200,
               {"Date": "1000000", "Cache-Control": "max-age=5, max-age=6"},
               None))
    C.append(H("refuse/empty-cc-value", 200,
               {"Date": "1000000", "Cache-Control": ""}, None))
    # Same directive twice with the same argument is not a conflict.
    C.append(H("explicit/repeated-identical-directive", 200,
               {"Date": "1000000", "Cache-Control": "max-age=5, max-age=5"},
               {"decision": "explicit", "lifetime": 5, "heuristic": False}))
    # Unknown directives are ignored; Age is not part of this contract.
    C.append(H("explicit/unknown-directives-ignored", 200,
               {"Date": "1000000", "Age": "5000",
                "Cache-Control": "no-cache, must-revalidate, max-age=600"},
               {"decision": "explicit", "lifetime": 600, "heuristic": False}))
    # s-maxage alone, not shared: ignored, falls through the gate.
    C.append(H("gate/s-maxage-not-shared-no-max-age", 200,
               {"Date": "1000000", "Cache-Control": "s-maxage=120"},
               {"decision": "heuristic-undecided", "lifetime": None,
                "heuristic": False}, shared=False))
    # public on a cacheable status with no Last-Modified: undecided.
    C.append(H("gate/public-no-last-modified", 500,
               {"Date": "1000000", "Cache-Control": "public"},
               {"decision": "heuristic-undecided", "lifetime": None,
                "heuristic": False}))
    # Vary "*" as the only member.
    C.append(H("store/vary-star-only-member", 200,
               {"Date": "1000000", "Vary": "*", "Last-Modified": "990000"},
               {"decision": "not-storable", "lifetime": None,
                "heuristic": False}))
    # Quoted non-delta argument parses; unknown name stays ignored.
    C.append(H("explicit/quoted-unknown-arg", 200,
               {"Date": "1000000", "Cache-Control": 'foo="bar", max-age=7'},
               {"decision": "explicit", "lifetime": 7, "heuristic": False}))
    return C


def main(argv):
    if "--selftest" in argv[1:]:
        return selftest()
    try:
        payload = sys.stdin.read()
    except (OSError, UnicodeError) as exc:
        return refuse("stdin is unreadable: %s" % exc)
    try:
        inp = json.loads(payload)
    except ValueError as exc:
        return refuse("input is not valid JSON: %s" % exc)
    try:
        out = decide(inp)
    except Invalid as exc:
        return refuse(str(exc))
    sys.stdout.write(json.dumps(out, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
