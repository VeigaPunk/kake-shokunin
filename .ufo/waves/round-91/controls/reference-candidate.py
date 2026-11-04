#!/usr/bin/env python3
"""Reachability control (not a claimed positive): the round-91 C2 counter's own reference.

Generated at freeze time by controls/make-reference-candidate.py as a byte-copy of the
counter's reference block (counter sha256 0cd610426896fc76b4913c907d83b95d22c7a66c4ecf2da8fc4fc9ecf21ab660). It exists to show the contract is
implementable and the battery satisfiable before any candidate exists. It is a control
fixture, never the shipped tool, and proves nothing about independent authorship.
"""
import json
import re
import sys


CACHEABLE = (200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501)
DELTA = ("max-age", "s-maxage", "min-fresh")
KEYS_OUT = {"decision", "freshness_lifetime", "current_age"}


class Invalid(Exception):
    pass


def ascii_lower(s):
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in s)


def parse_cc(value):
    out = {}
    for raw in value.split(","):
        d = raw.strip(" \t")
        if not d:
            raise Invalid("empty directive")
        name, sep, arg = d.partition("=")
        name = ascii_lower(name.strip(" \t"))
        if not name:
            raise Invalid("empty directive name")
        if sep:
            arg = arg.strip(" \t")
            quoted = len(arg) >= 2 and arg[0] == '"' and arg[-1] == '"'
            if quoted:
                arg = arg[1:-1]
            if name in DELTA or name == "max-stale":
                if quoted:
                    raise Invalid("quoted delta-seconds")
                if not re.fullmatch(r"[0-9]+", arg):
                    raise Invalid("bad delta-seconds")
                val = int(arg)
            else:
                val = arg
        else:
            val = None
        if name in out and out[name] != val:
            raise Invalid("duplicate directive")
        out[name] = val
    return out


def read_headers(obj):
    if not isinstance(obj, dict):
        raise Invalid("headers must be an object")
    out = {}
    for k, v in obj.items():
        if not isinstance(k, str) or not isinstance(v, str):
            raise Invalid("header name and value must be strings")
        if not k:
            raise Invalid("empty header name")
        lk = ascii_lower(k)
        if lk in out:
            raise Invalid("duplicate header name")
        if "\r" in v or "\n" in v or "\0" in v:
            raise Invalid("control character in value")
        out[lk] = v.strip(" \t")
    return out


def as_int(name, value, allow_negative=False):
    if not re.fullmatch(r"-?[0-9]+", value):
        raise Invalid("%s must be an integer" % name)
    n = int(value)
    if not allow_negative and n < 0:
        raise Invalid("%s must be nonnegative" % name)
    return n


def reference(inp):
    if not isinstance(inp, dict):
        raise Invalid("input must be an object")
    if set(inp) - {"stored", "request", "now", "shared"}:
        raise Invalid("unknown input key")
    for k in ("stored", "request", "now"):
        if k not in inp:
            raise Invalid("missing %s" % k)
    stored, request, now = inp["stored"], inp["request"], inp["now"]
    if not isinstance(stored, dict) or not isinstance(request, dict):
        raise Invalid("stored and request must be objects")
    if set(stored) - {"status", "headers"} or set(request) - {"method", "headers"}:
        raise Invalid("unknown stored/request key")
    if "status" not in stored:
        raise Invalid("missing status")
    status = stored["status"]
    if not isinstance(status, int) or isinstance(status, bool) or not 100 <= status <= 599:
        raise Invalid("status must be an integer 100..599")
    if "method" not in request:
        raise Invalid("missing method")
    method = request["method"]
    if not isinstance(method, str) or not method:
        raise Invalid("method must be a nonempty string")
    if not isinstance(now, int) or isinstance(now, bool) or now < 0:
        raise Invalid("now must be a nonnegative integer")
    shared = inp.get("shared", False)
    if not isinstance(shared, bool):
        raise Invalid("shared must be a boolean")
    sh = read_headers(stored.get("headers", {}))
    rh = read_headers(request.get("headers", {}))
    scc = parse_cc(sh["cache-control"]) if "cache-control" in sh else {}
    rcc = parse_cc(rh["cache-control"]) if "cache-control" in rh else {}
    # clause 5-9: validation and lifetime first
    if "date" not in sh:
        raise Invalid("missing Date")
    date = as_int("Date", sh["date"], allow_negative=True)
    age_h = as_int("Age", sh["age"]) if "age" in sh else 0
    expires = as_int("Expires", sh["expires"], allow_negative=True) if "expires" in sh else None
    current_age = max(0, age_h) + max(0, now - date)
    if shared and "s-maxage" in scc:
        lifetime = scc["s-maxage"]
    elif "max-age" in scc:
        lifetime = scc["max-age"]
    elif expires is not None:
        lifetime = expires - date
    else:
        lifetime = None
    # clause 10
    vary = sh.get("vary")
    star = vary is not None and any(m.strip(" \t") == "*" for m in vary.split(","))
    if (method not in ("GET", "HEAD") or status not in CACHEABLE
            or "no-store" in scc or "no-store" in rcc
            or ("private" in scc and shared) or star):
        return {"decision": "not-storable", "freshness_lifetime": None, "current_age": None}
    # clauses 11-19
    if lifetime is None:
        decision = "heuristic-undecided"
    elif "no-cache" in rcc:
        decision = "revalidate"
    elif "no-cache" in scc:
        decision = "revalidate"
    elif "max-age" in rcc and current_age > rcc["max-age"]:
        decision = "revalidate"
    elif "min-fresh" in rcc and lifetime - current_age < rcc["min-fresh"]:
        decision = "revalidate"
    elif current_age < lifetime:
        decision = "reuse"
    elif "must-revalidate" in scc or ("proxy-revalidate" in scc and shared):
        decision = "must-revalidate-fail"
    elif "max-stale" in rcc and (rcc["max-stale"] is None
                                 or current_age - lifetime <= rcc["max-stale"]):
        decision = "serve-stale"
    else:
        decision = "revalidate"
    # clause 20
    if "only-if-cached" in rcc and decision not in ("reuse", "not-storable"):
        decision = "only-if-cached-miss"
    return {"decision": decision, "freshness_lifetime": lifetime, "current_age": current_age}


def main():
    try:
        inp = json.loads(sys.stdin.read())
        out = reference(inp)
    except Invalid as exc:
        sys.stderr.write("invalid_input: %s\n" % exc)
        return 1
    except ValueError:
        sys.stderr.write("invalid_input: not JSON\n")
        return 1
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
