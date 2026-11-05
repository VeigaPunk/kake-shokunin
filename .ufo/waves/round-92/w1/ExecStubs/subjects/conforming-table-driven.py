#!/usr/bin/env python3
"""C2 held-out subject: conforming, table-driven (contract v1; ExecStubs r92).

Written from `.ufo/waves/round-92/c2-contract.md` alone. Structure: an ordered
validation table runs the field clauses (1-7) for every input, then a
first-match rule table decides (clauses 9-13) -- deliberately not the
reference's helper-and-if-chain shape.

One JSON object on stdin; success is one JSON object on stdout with exactly
decision/lifetime/heuristic (exit 0); any violation is `invalid_input: <reason>`
on stderr with exit 1 and empty stdout. Decision over supplied integer seconds
only: no clock, no HTTP-date parsing, no store, no revalidation, no network.
"""
import json
import re
import sys

DECIMAL = re.compile(r"[0-9]+")
CACHEABLE = frozenset((200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501))
DELTA = ("max-age", "s-maxage")
FRACTION = 10   # clause 12 lane convention (RFC: "some fraction"; 10% typical)
CAP = 86400     # clause 12 lane convention (RFC names no value)


class Refuse(Exception):
    """Clause 8: any of clauses 1-7 may raise this, for every input."""


def ascii_lower(text):
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in text)


# --- validation table (clauses 1-7; run for every input) -------------------

def step_input(ctx):
    try:
        raw = json.loads(sys.stdin.read())
    except ValueError:
        raise Refuse("malformed JSON")
    if not isinstance(raw, dict):
        raise Refuse("input is not an object")
    if set(raw) - {"stored", "now", "shared"}:
        raise Refuse("unexpected top-level key")
    stored = raw.get("stored")
    if not isinstance(stored, dict) or set(stored) - {"status", "headers"}:
        raise Refuse("stored is not the declared object")
    ctx["status"] = stored.get("status")
    ctx["raw_headers"] = stored.get("headers", {})
    ctx["now"] = raw.get("now")
    ctx["shared"] = raw.get("shared", False)


def step_scalar_types(ctx):
    """Clause 3."""
    status, now, shared = ctx["status"], ctx["now"], ctx["shared"]
    if not isinstance(status, int) or isinstance(status, bool) \
            or not 100 <= status <= 599:
        raise Refuse("status is not an int in 100..599")
    if not isinstance(now, int) or isinstance(now, bool) or now < 0:
        raise Refuse("now is not a non-negative int")
    if not isinstance(shared, bool):
        raise Refuse("shared is not a bool")
    if not isinstance(ctx["raw_headers"], dict):
        raise Refuse("headers is not an object")


def step_header_names_values(ctx):
    """Clauses 1-2."""
    out, seen = {}, {}
    for name, value in ctx["raw_headers"].items():
        if not isinstance(name, str) or not isinstance(value, str):
            raise Refuse("header name or value is not a string")
        if any(c in value for c in "\r\n\0"):
            raise Refuse("header value contains CR, LF or NUL")
        low = ascii_lower(name)
        if low in seen:
            raise Refuse("duplicate header name")
        seen[low] = name
        out[low] = value.strip(" \t")
    ctx["headers"] = out


def step_cache_control(ctx):
    """Clause 4."""
    cc = {}
    if "cache-control" in ctx["headers"]:
        for piece in ctx["headers"]["cache-control"].split(","):
            directive = piece.strip(" \t")
            if not directive:
                raise Refuse("empty Cache-Control directive")
            name, eq, arg = directive.partition("=")
            name = ascii_lower(name.strip(" \t"))
            if not name:
                raise Refuse("empty Cache-Control directive name")
            if eq:
                arg = arg.strip(" \t")
                if len(arg) >= 2 and arg[0] == '"' and arg[-1] == '"':
                    if name in DELTA:
                        raise Refuse("delta-seconds argument is quoted")
                    arg = arg[1:-1]
                if name in DELTA and DECIMAL.fullmatch(arg) is None:
                    raise Refuse("delta-seconds argument is not a bare "
                                 "non-negative decimal integer")
            else:
                arg = None
            if name in cc and cc[name] != arg:
                raise Refuse("Cache-Control directive %s repeated with a "
                             "different argument" % name)
            cc[name] = arg
    ctx["cc"] = cc


def _epoch(ctx, key, label):
    """Clauses 6-7."""
    if key not in ctx["headers"]:
        return None
    value = ctx["headers"][key]
    if DECIMAL.fullmatch(value) is None:
        raise Refuse("%s is not a decimal integer" % label)
    return int(value)


def step_dates(ctx):
    """Clause 5 (+ 6-7)."""
    headers = ctx["headers"]
    if "date" not in headers:
        raise Refuse("Date is absent")
    if DECIMAL.fullmatch(headers["date"]) is None:
        raise Refuse("Date is not a decimal integer")
    ctx["date"] = int(headers["date"])
    ctx["expires"] = _epoch(ctx, "expires", "Expires")
    ctx["last_modified"] = _epoch(ctx, "last-modified", "Last-Modified")


STEPS = (
    ("input-envelope", step_input),
    ("clause-3-scalar-types", step_scalar_types),
    ("clause-1-2-header-names-and-values", step_header_names_values),
    ("clause-4-cache-control", step_cache_control),
    ("clause-5-6-7-field-dates", step_dates),
)

# --- rule table (clauses 9-13; first match wins) ----------------------------


def vary_has_star(headers):
    if "vary" not in headers:
        return False
    return any(m.strip(" \t") == "*" for m in headers["vary"].split(","))


def rule_not_storable(ctx):
    """Clause 9."""
    if "no-store" in ctx["cc"]:
        return (None, False)
    if "private" in ctx["cc"] and ctx["shared"]:
        return (None, False)
    if vary_has_star(ctx["headers"]):
        return (None, False)
    return None


def explicit_lifetime(ctx):
    """Clause 10 selection order: s-maxage (shared only) > max-age > Expires."""
    if ctx["shared"] and "s-maxage" in ctx["cc"]:
        return int(ctx["cc"]["s-maxage"])
    if "max-age" in ctx["cc"]:
        return int(ctx["cc"]["max-age"])
    if ctx["expires"] is not None:
        return ctx["expires"] - ctx["date"]
    return None


def rule_explicit(ctx):
    life = explicit_lifetime(ctx)
    if life is None:
        return None
    return (life, False)


def rule_not_cacheable(ctx):
    """Clause 11."""
    if ctx["status"] not in CACHEABLE and "public" not in ctx["cc"]:
        return (None, False)
    return None


def rule_heuristic(ctx):
    """Clause 12."""
    lm = ctx["last_modified"]
    if lm is not None and lm <= ctx["date"]:
        return (min((ctx["date"] - lm) // FRACTION, CAP), True)
    return None


def rule_undecided(ctx):
    """Clause 13."""
    return (None, False)


RULES = (
    ("not-storable", rule_not_storable),
    ("explicit", rule_explicit),
    ("not-heuristically-cacheable", rule_not_cacheable),
    ("heuristic", rule_heuristic),
    ("heuristic-undecided", rule_undecided),
)


def main():
    ctx = {}
    try:
        for _, step in STEPS:
            step(ctx)
        decision, lifetime, heuristic = "heuristic-undecided", None, False
        for name, rule in RULES:
            hit = rule(ctx)
            if hit is not None:
                decision = name
                lifetime, heuristic = hit
                break
    except Refuse as why:
        sys.stderr.write("invalid_input: %s\n" % why)
        return 1
    sys.stdout.write(json.dumps({"decision": decision, "lifetime": lifetime,
                                 "heuristic": heuristic}) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
