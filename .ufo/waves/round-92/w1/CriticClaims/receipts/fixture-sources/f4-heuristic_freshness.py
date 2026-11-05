#!/usr/bin/env python3
"""CriticClaims fixture subject: heuristic freshness decision, c2-contract.md v1.

Written from the contract alone (clauses 1-13). Fixture evidence for the C2
separability test only; not the wave's deliverable. Two lane conventions are
named as conventions, not RFC requirements: the 10 % fraction and the 86400 cap.
"""
import json
import re
import sys

HEURISTICALLY_CACHEABLE = (200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501)
DELTA = ("max-age", "s-maxage")
TOP_KEYS = ("stored", "now", "shared")


class Refusal(Exception):
    pass


def ascii_lower(text):
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in text)


def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def parse_cache_control(value):
    """Clause 4."""
    directives = {}
    for raw in value.split(","):
        directive = raw.strip(" \t")
        if not directive:
            raise Refusal("empty Cache-Control directive")
        name, sep, arg = directive.partition("=")
        name = ascii_lower(name.strip(" \t"))
        if not name:
            raise Refusal("empty Cache-Control directive name")
        if sep:
            arg = arg.strip(" \t")
            quoted = len(arg) >= 2 and arg[0] == '"' and arg[-1] == '"'
            if quoted:
                arg = arg[1:-1]
            if name in DELTA and (quoted or not re.fullmatch(r"[0-9]+", arg)):
                raise Refusal("delta-seconds argument is not a bare non-negative integer")
        else:
            if name in DELTA:
                raise Refusal("delta-seconds argument is not a bare non-negative integer")
            arg = None
        if name in directives and directives[name] != arg:
            raise Refusal("conflicting Cache-Control directive %s" % name)
        directives[name] = arg
    return directives


def read_headers(raw):
    """Clauses 1-3."""
    if not isinstance(raw, dict):
        raise Refusal("headers is not an object")
    seen = set()
    out = {}
    for name, value in raw.items():
        if not isinstance(name, str) or not isinstance(value, str):
            raise Refusal("header name or value is not a string")
        if "\r" in value or "\n" in value or "\0" in value:
            raise Refusal("header value contains CR, LF or NUL")
        low = ascii_lower(name)
        if low in seen:
            raise Refusal("duplicate header name")
        seen.add(low)
        out[low] = value.strip(" \t")
    return out


def seconds(headers, name):
    """Clauses 6-7: an optional decimal-integer field."""
    value = headers.get(name)
    if value is None:
        return None
    if not re.fullmatch(r"[0-9]+", value):
        raise Refusal("%s is not a decimal integer" % name)
    return int(value)


def decide(payload):
    if not isinstance(payload, dict):
        raise Refusal("input is not an object")
    if set(payload) - set(TOP_KEYS):
        raise Refusal("unexpected top-level key")
    stored = payload.get("stored")
    if not isinstance(stored, dict) or set(stored) - {"status", "headers"}:
        raise Refusal("stored is not the declared object")
    status = stored.get("status")
    if not is_int(status) or not 100 <= status <= 599:
        raise Refusal("status is not an int in 100..599")
    now = payload.get("now")
    if not is_int(now) or now < 0:
        raise Refusal("now is not a non-negative int")
    shared = payload.get("shared", False)
    if not isinstance(shared, bool):
        raise Refusal("shared is not a bool")

    headers = read_headers(stored.get("headers", {}))
    cc = parse_cache_control(headers["cache-control"]) if "cache-control" in headers else {}

    # clause 5
    if "date" not in headers:
        raise Refusal("Date is absent")
    if not re.fullmatch(r"[0-9]+", headers["date"]):
        raise Refusal("Date is not a decimal integer")
    date = int(headers["date"])
    # clauses 6-7
    expires = seconds(headers, "expires")
    last_modified = seconds(headers, "last-modified")
    # clause 8: every field above is validated before any decision
    smaxage = seconds(cc, "s-maxage") if "s-maxage" in cc else None
    maxage = seconds(cc, "max-age") if "max-age" in cc else None

    # clause 9
    vary_star = False
    if "vary" in headers:
        vary_star = any(member.strip(" \t") == "*" for member in headers["vary"].split(","))
    if "no-store" in cc or ("private" in cc and shared) or vary_star:
        return {"decision": "not-storable", "lifetime": None, "heuristic": False}

    # clause 10
    if shared and smaxage is not None:
        return {"decision": "explicit", "lifetime": smaxage, "heuristic": False}
    if maxage is not None:
        return {"decision": "explicit", "lifetime": maxage, "heuristic": False}
    if expires is not None:
        return {"decision": "explicit", "lifetime": expires - date, "heuristic": False}

    # clause 11
    if status not in HEURISTICALLY_CACHEABLE and "public" not in cc:
        return {"decision": "not-heuristically-cacheable", "lifetime": None,
                "heuristic": False}

    # clauses 12-13 (lane conventions: 10 % fraction, 86400 cap)
    if last_modified is not None and last_modified <= date:
        return {"decision": "heuristic",
                "lifetime": min((date - last_modified) // 10, 86400), "heuristic": True}
    return {"decision": "heuristic-undecided", "lifetime": None, "heuristic": False}


def main():
    try:
        try:
            payload = json.loads(sys.stdin.read())
        except ValueError:
            raise Refusal("input is not JSON")
        result = decide(payload)
    except Refusal as exc:
        sys.stderr.write("invalid_input: %s\n" % exc)
        return 1
    sys.stdout.write(json.dumps(result, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
