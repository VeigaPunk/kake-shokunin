#!/usr/bin/env python3
"""C2 held-out subject: conforming, one branch per contract clause (v1).

Written from `.ufo/waves/round-92/c2-contract.md` alone. Structure: one flat
main function whose numbered branches mirror the contract's clause numbers
1-13 in order -- deliberately neither the reference's helper decomposition nor
a table drive. Decision over supplied integer seconds only.

stdin: one JSON object. exit 0: one JSON object on stdout with exactly
decision/lifetime/heuristic. exit 1: `invalid_input: <reason>` on stderr,
nothing on stdout.
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


def main():
    # input envelope (Input section of the contract)
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
    # clause 3 (scalar types)
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
        # clause 3 (header name/value types)
        if not isinstance(name, str) or not isinstance(value, str):
            refuse("header name or value is not a string")
        # clause 2 (value bytes)
        if any(c in value for c in "\r\n\0"):
            refuse("header value contains CR, LF or NUL")
        # clause 1 (names, case-insensitive; case-variant duplicates refuse)
        low = lower(name)
        if low in headers:
            refuse("duplicate header name")
        headers[low] = value.strip(" \t")

    # clause 4 (Cache-Control grammar)
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

    # clause 5 (Date required, decimal integer)
    if "date" not in headers:
        refuse("Date is absent")
    if DEC.fullmatch(headers["date"]) is None:
        refuse("Date is not a decimal integer")
    date = int(headers["date"])

    # clause 6 (Expires optional, decimal integer, may precede Date)
    expires = None
    if "expires" in headers:
        if DEC.fullmatch(headers["expires"]) is None:
            refuse("Expires is not a decimal integer")
        expires = int(headers["expires"])

    # clause 7 (Last-Modified optional, decimal integer)
    lm = None
    if "last-modified" in headers:
        if DEC.fullmatch(headers["last-modified"]) is None:
            refuse("Last-Modified is not a decimal integer")
        lm = int(headers["last-modified"])

    # clause 8: every branch above ran before any arithmetic below.

    vary_star = "vary" in headers and any(
        m.strip(" \t") == "*" for m in headers["vary"].split(","))

    # clause 9 (not-storable)
    if "no-store" in cc or ("private" in cc and shared) or vary_star:
        decision, lifetime, heuristic = "not-storable", None, False
    # clause 10 (explicit wins; heuristics never used with it)
    elif shared and "s-maxage" in cc:
        decision, lifetime, heuristic = "explicit", int(cc["s-maxage"]), False
    elif "max-age" in cc:
        decision, lifetime, heuristic = "explicit", int(cc["max-age"]), False
    elif expires is not None:
        decision, lifetime, heuristic = "explicit", expires - date, False
    # clause 11 (heuristically-cacheable gate; public opens it)
    elif status not in CACHEABLE and "public" not in cc:
        decision, lifetime, heuristic = "not-heuristically-cacheable", None, False
    # clause 12 (heuristic: 10% of age, capped at 86400 -- lane conventions)
    elif lm is not None and lm <= date:
        decision, lifetime, heuristic = "heuristic", min((date - lm) // 10, 86400), True
    # clause 13 (heuristic-undecided)
    else:
        decision, lifetime, heuristic = "heuristic-undecided", None, False

    sys.stdout.write(json.dumps({"decision": decision, "lifetime": lifetime,
                                 "heuristic": heuristic}) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
