#!/usr/bin/env python3
"""C2 held-out negative subject: neg-clause06-expires-parsed-as-float (ExecStubs r92).

Breaks exactly clause 6 of `.ufo/waves/round-92/c2-contract.md`: Expires, when
present, is parsed as a float instead of a bare decimal integer, so forms such
as `1e6` or `1000300.5` are accepted. Every other clause follows the contract.
"""
import json
import re
import sys

DEC = re.compile(r"[0-9]+")
FLOATISH = re.compile(r"[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?")
CACHEABLE = (200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501)


def refuse(reason):
    sys.stderr.write("invalid_input: %s\n" % reason)
    sys.exit(1)


def lower(name):
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in name)


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
    status = stored.get("status")
    if not isinstance(status, int) or isinstance(status, bool) \
            or not 100 <= status <= 599:
        refuse("status is not an int in 100..599")
    now = raw.get("now")
    if not isinstance(now, int) or isinstance(now, bool) or now < 0:
        refuse("now is not a non-negative int")
    shared = raw.get("shared", False)
    if not isinstance(shared, bool):
        refuse("shared is not a bool")
    rawh = stored.get("headers", {})
    if not isinstance(rawh, dict):
        refuse("headers is not an object")
    headers = {}
    for name, value in rawh.items():
        if not isinstance(name, str) or not isinstance(value, str):
            refuse("header name or value is not a string")
        if any(c in value for c in "\r\n\0"):
            refuse("header value contains CR, LF or NUL")
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
        # clause 6 VIOLATION: Expires accepted as a float, not a decimal int.
        if FLOATISH.fullmatch(headers["expires"]) is None:
            refuse("Expires is not a decimal integer")
        expires = int(float(headers["expires"]))
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
