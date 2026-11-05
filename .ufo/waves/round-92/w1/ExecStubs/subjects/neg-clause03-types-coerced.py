#!/usr/bin/env python3
"""C2 held-out negative subject: neg-clause03-types-coerced (ExecStubs r92).

Breaks exactly clause 3 of `.ufo/waves/round-92/c2-contract.md`: scalar and
header-value types are coerced instead of refused -- a JSON string status such
as "200" becomes 200, booleans are accepted as ints, and non-string header
values go through str(). Every other clause follows the contract. (This is the
value-type-refusal variant round-91 routed as uncovered: K91-6 / R91-2.)
"""
import json
import re
import sys

DEC = re.compile(r"[0-9]+")
CACHEABLE = (200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501)


def refuse(reason):
    sys.stderr.write("invalid_input: %s\n" % reason)
    sys.exit(1)


def lower(name):
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in name)


def coerce_int(value):
    # clause 3 VIOLATION: accept bools and numeric strings as ints.
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return int(value)
    raise ValueError("not coercible")


def main():
    try:
        raw = json.loads(sys.stdin.read())
    except ValueError:
        refuse("malformed JSON")
    if not isinstance(raw, dict):
        refuse("input is not an object")
    if set(raw) - {"stored", "now", "shared"}:
        refuse("unexpected top-level key")
    stored = raw.get("stored")
    if not isinstance(stored, dict) or set(stored) - {"status", "headers"}:
        refuse("stored is not the declared object")
    try:
        status = coerce_int(stored.get("status"))
    except (TypeError, ValueError):
        refuse("status is not an int in 100..599")
    if not 100 <= status <= 599:
        refuse("status is not an int in 100..599")
    try:
        now = coerce_int(raw.get("now"))
    except (TypeError, ValueError):
        refuse("now is not a non-negative int")
    if now < 0:
        refuse("now is not a non-negative int")
    shared = raw.get("shared", False)
    if not isinstance(shared, bool):
        refuse("shared is not a bool")
    rawh = stored.get("headers", {})
    if not isinstance(rawh, dict):
        refuse("headers is not an object")
    headers = {}
    for name, value in rawh.items():
        if not isinstance(name, str):
            refuse("header name is not a string")
        # clause 3 VIOLATION: non-string values are coerced, not refused.
        value = value if isinstance(value, str) else str(value)
        low = lower(name)
        if low in headers:
            refuse("duplicate header name")
        headers[low] = value.strip(" \t")
    cc = {}
    if "cache-control" in headers:
        for piece in headers["cache-control"].split(","):
            directive = piece.strip(" \t")
            if not directive:
                refuse("empty Cache-Control directive")
            name, eq, arg = directive.partition("=")
            name = lower(name.strip(" \t"))
            if not name:
                refuse("empty Cache-Control directive name")
            if eq:
                arg = arg.strip(" \t")
                if len(arg) >= 2 and arg[0] == '"' and arg[-1] == '"':
                    if name in ("max-age", "s-maxage"):
                        refuse("delta-seconds argument is quoted")
                    arg = arg[1:-1]
                if name in ("max-age", "s-maxage") \
                        and DEC.fullmatch(arg) is None:
                    refuse("delta-seconds argument is not a bare non-negative "
                           "decimal integer")
            else:
                arg = None
            if name in cc and cc[name] != arg:
                refuse("Cache-Control directive %s repeated with a different "
                       "argument" % name)
            cc[name] = arg
    if "date" not in headers:
        refuse("Date is absent")
    if DEC.fullmatch(headers["date"]) is None:
        refuse("Date is not a decimal integer")
    date = int(headers["date"])
    expires = None
    if "expires" in headers:
        if DEC.fullmatch(headers["expires"]) is None:
            refuse("Expires is not a decimal integer")
        expires = int(headers["expires"])
    lm = None
    if "last-modified" in headers:
        if DEC.fullmatch(headers["last-modified"]) is None:
            refuse("Last-Modified is not a decimal integer")
        lm = int(headers["last-modified"])
    vary_star = "vary" in headers and any(
        m.strip(" \t") == "*" for m in headers["vary"].split(","))
    if "no-store" in cc or ("private" in cc and shared) or vary_star:
        decision, lifetime, heuristic = "not-storable", None, False
    elif shared and "s-maxage" in cc:
        decision, lifetime, heuristic = "explicit", int(cc["s-maxage"]), False
    elif "max-age" in cc:
        decision, lifetime, heuristic = "explicit", int(cc["max-age"]), False
    elif expires is not None:
        decision, lifetime, heuristic = "explicit", expires - date, False
    elif status not in CACHEABLE and "public" not in cc:
        decision, lifetime, heuristic = "not-heuristically-cacheable", None, False
    elif lm is not None and lm <= date:
        decision, lifetime, heuristic = "heuristic", min((date - lm) // 10, 86400), True
    else:
        decision, lifetime, heuristic = "heuristic-undecided", None, False
    sys.stdout.write(json.dumps({"decision": decision, "lifetime": lifetime,
                                 "heuristic": heuristic}) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
