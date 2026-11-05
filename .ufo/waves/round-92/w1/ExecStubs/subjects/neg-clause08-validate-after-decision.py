#!/usr/bin/env python3
"""C2 held-out negative subject: neg-clause08-validate-after-decision (ExecStubs r92).

Breaks exactly clause 8 of `.ufo/waves/round-92/c2-contract.md` ("No
arithmetic before validation"; clauses 1-7 must run for every input): a
lenient pre-scan takes the not-storable decision BEFORE the strict clause 1-7
validation, so a response carrying no-store / private+shared / `Vary: *` is
answered not-storable even when one of its fields is malformed. Every other
clause follows the contract on inputs that reach the strict path.
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


def emit(decision, lifetime, heuristic):
    sys.stdout.write(json.dumps({"decision": decision, "lifetime": lifetime,
                                 "heuristic": heuristic}) + "\n")
    sys.exit(0)


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

    # clause 8 VIOLATION: lenient clause-9 pre-scan, run before the strict
    # clauses 1-7; a malformed field on an unstorable response is never seen.
    loose = {}
    if isinstance(rawh, dict):
        for name, value in rawh.items():
            if isinstance(name, str) and isinstance(value, str):
                low = lower(name)
                if low not in loose:
                    loose[low] = value.strip(" \t")
    loose_cc = set()
    if "cache-control" in loose:
        for piece in loose["cache-control"].split(","):
            directive = piece.strip(" \t")
            if directive:
                name = lower(directive.partition("=")[0].strip(" \t"))
                if name:
                    loose_cc.add(name)
    vary_star_loose = "vary" in loose and any(
        m.strip(" \t") == "*" for m in loose["vary"].split(","))
    if "no-store" in loose_cc or ("private" in loose_cc and shared) \
            or vary_star_loose:
        emit("not-storable", None, False)

    # strict path: clauses 1-7, then decisions 10-13
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
        if DEC.fullmatch(headers["expires"]) is None:
            refuse("Expires is not a decimal integer")
        expires = int(headers["expires"])
    lm = None
    if "last-modified" in headers:
        if DEC.fullmatch(headers["last-modified"]) is None:
            refuse("Last-Modified is not a decimal integer")
        lm = int(headers["last-modified"])
    if shared and "s-maxage" in cc:
        emit("explicit", int(cc["s-maxage"]), False)
    if "max-age" in cc:
        emit("explicit", int(cc["max-age"]), False)
    if expires is not None:
        emit("explicit", expires - date, False)
    if status not in CACHEABLE and "public" not in cc:
        emit("not-heuristically-cacheable", None, False)
    if lm is not None and lm <= date:
        emit("heuristic", min((date - lm) // 10, 86400), True)
    emit("heuristic-undecided", None, False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
