#!/usr/bin/env python3
"""Independent twin of the stale-serving contract v1 (kake round 98, C2).

Written from LANE/.ufo/waves/round-98/stale-contract.md and RFC 5861 only.
Protocol (contract "Interface"): one JSON object on stdin.
  decided: exit 0, stdout = one JSON object {"decision", "staleness"} + newline.
  refused: exit 1, stdout empty, stderr begins "invalid_input:".
An unexpected internal exception exits 2 (a twin bug, never a decision).
"""
import json
import sys

# Integers in the input have no bound in the contract; do not let the
# interpreter's 4300-digit conversion cap decide an input's fate.
sys.set_int_max_str_digits(0)

CAP = 2147483648  # RFC 9111 1.2.2 clamp for delta-seconds (contract step 4)

DIGIT = frozenset("0123456789")
ALPHA = frozenset(chr(c) for c in range(0x41, 0x5B)) | frozenset(chr(c) for c in range(0x61, 0x7B))
TCHAR = frozenset("!#$%&'*+-.^_`|~") | DIGIT | ALPHA  # RFC 9110 5.6.2
SP_HTAB = " \t"

KNOWN_KEYS = frozenset({"response_cc", "request_cc", "freshness_lifetime",
                        "current_age", "event", "error", "shared"})
REQUIRED_KEYS = frozenset({"response_cc", "freshness_lifetime", "current_age", "event"})
REQUEST_REFUSED = ("max-age", "max-stale", "min-fresh", "only-if-cached")


class Refuse(Exception):
    pass


def refuse(why):
    raise Refuse(why)


def qdtext_ok(c):
    # RFC 9110 5.6.4: HTAB / SP / %x21 / %x23-5B / %x5D-7E / %x80-FF
    o = ord(c)
    return c == "\t" or c == " " or o == 0x21 or 0x23 <= o <= 0x5B or 0x5D <= o <= 0x7E or 0x80 <= o <= 0xFF


def quoted_pair_ok(c):
    # quoted-pair = "\" ( HTAB / SP / VCHAR / obs-text )
    o = ord(c)
    return c == "\t" or c == " " or 0x21 <= o <= 0x7E or 0x80 <= o <= 0xFF


def skip_quoted(s, i):
    """s[i] is DQUOTE. Return the index just past the closing DQUOTE, or refuse."""
    j = i + 1
    n = len(s)
    while True:
        if j >= n:
            refuse("unterminated quoted-string")
        c = s[j]
        if c == '"':
            return j + 1
        if c == "\\":
            if j + 1 >= n or not quoted_pair_ok(s[j + 1]):
                refuse("bad quoted-pair")
            j += 2
            continue
        if not qdtext_ok(c):
            refuse("bad qdtext character")
        j += 1


def split_elements(field):
    """Split on commas that lie outside quoted-strings."""
    out = []
    start = 0
    i = 0
    n = len(field)
    while i < n:
        c = field[i]
        if c == '"':
            i = skip_quoted(field, i)
        elif c == ",":
            out.append(field[start:i])
            i += 1
            start = i
        else:
            i += 1
    out.append(field[start:])
    return out


def parse_cc(field):
    """Return the list of (lowercase_name, raw_value_or_None, value_is_quoted).

    Every element is validated, including later duplicates (contract step 2).
    """
    directives = []
    for raw in split_elements(field):
        elem = raw.strip(SP_HTAB)
        if elem == "":
            continue
        eq = elem.find("=")
        name = elem if eq < 0 else elem[:eq]
        if name == "" or any(ch not in TCHAR for ch in name):
            refuse("directive name is not a token")
        lname = name.lower()  # ASCII only: every character is a tchar
        if eq < 0:
            directives.append((lname, None, False))
            continue
        value = elem[eq + 1:]
        if value == "":
            refuse("empty value after '='")
        if value[0] == '"':
            end = skip_quoted(value, 0)
            if end != len(value):
                refuse("text after closing quote")
            directives.append((lname, value, True))
        else:
            if any(ch not in TCHAR for ch in value):
                refuse("value is neither token nor quoted-string")
            directives.append((lname, value, False))
    return directives


def has(directives, name):
    return any(n == name for n, _, _ in directives)


def delta_seconds(directives, name):
    """Contract step 4: first occurrence only; valid iff unquoted token of 1*DIGIT; clamped."""
    first = None
    for n, v, q in directives:
        if n == name:
            first = (v, q)
            break
    if first is None:
        return None
    value, quoted = first
    if value is None or quoted:
        return None
    if value == "" or any(ch not in DIGIT for ch in value):
        return None
    digits = value.lstrip("0") or "0"
    if len(digits) > 10:
        return CAP
    return min(int(digits), CAP)


def no_duplicate_keys(pairs):
    obj = {}
    for k, v in pairs:
        obj[k] = v  # PROBE ONLY: last-wins
    return obj


def nonneg_int(x, what):
    if isinstance(x, bool) or not isinstance(x, int):
        refuse(what + " must be an integer")
    if x < 0:
        refuse(what + " must be >= 0")
    return x


def validate(obj):
    if not isinstance(obj, dict):
        refuse("top level is not an object")
    keys = set(obj)
    if not keys <= KNOWN_KEYS:
        refuse("unknown key(s): " + ", ".join(sorted(keys - KNOWN_KEYS)))
    if not REQUIRED_KEYS <= keys:
        refuse("missing required key(s)")

    response_cc = obj["response_cc"]
    if not isinstance(response_cc, str):
        refuse("response_cc must be a string")
    request_cc = obj.get("request_cc", "")
    if not isinstance(request_cc, str):
        refuse("request_cc must be a string")

    lifetime = nonneg_int(obj["freshness_lifetime"], "freshness_lifetime")
    age = nonneg_int(obj["current_age"], "current_age")

    event = obj["event"]
    if not isinstance(event, str) or event not in ("request", "error"):
        refuse("event must be 'request' or 'error'")

    error = obj.get("error")  # absent and null are the same here
    if event == "error":
        if error is None:
            refuse("error required when event is 'error'")
        if isinstance(error, bool):
            refuse("error must not be boolean")
        if isinstance(error, int):
            if not 100 <= error <= 599:
                refuse("error out of range 100-599")
        elif error != "network":
            refuse("error must be integer or 'network'")
    elif error is not None:
        refuse("error must be absent or null when event is 'request'")

    shared = obj.get("shared", False)
    if not isinstance(shared, bool):
        refuse("shared must be a boolean")

    return response_cc, request_cc, lifetime, age, event, error, shared


def decide(response_cc, request_cc, lifetime, age, event, error, shared):
    rcc = parse_cc(response_cc)
    qcc = parse_cc(request_cc)
    for name in REQUEST_REFUSED:
        if has(qcc, name):
            refuse("request directive outside contract: " + name)

    staleness = max(0, age - lifetime)

    resp_no_cache = has(rcc, "no-cache")
    req_no_cache = has(qcc, "no-cache")
    prohibited = (
        resp_no_cache
        or has(rcc, "must-revalidate")
        or (shared and (has(rcc, "proxy-revalidate") or has(rcc, "s-maxage")))
        or req_no_cache
    )

    # 1. error that RFC 5861 section 4 does not cover
    if event == "error" and not (error in (500, 502, 503, 504) or error == "network"):
        return "not-an-error", staleness

    # 2. fresh
    if age < lifetime and not (resp_no_cache or req_no_cache):
        return "fresh", staleness

    # 3. request event: stale-while-revalidate
    if event == "request":
        window = delta_seconds(rcc, "stale-while-revalidate")
        if not prohibited and window is not None and staleness <= window:
            return "serve-stale-revalidate", staleness
        return "revalidate", staleness

    # 4. error event: stale-if-error (request's valid value wins when present)
    limit = delta_seconds(qcc, "stale-if-error")
    if limit is None:
        limit = delta_seconds(rcc, "stale-if-error")
    if not prohibited and limit is not None and staleness <= limit:
        return "serve-stale-error", staleness
    return "error-through", staleness


def main():
    raw = sys.stdin.buffer.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        refuse("stdin is not UTF-8")
    try:
        obj = json.loads(text, object_pairs_hook=no_duplicate_keys)
    except (ValueError, RecursionError):
        refuse("stdin is not one JSON value")
    fields = validate(obj)
    decision, staleness = decide(*fields)
    sys.stdout.write(json.dumps({"decision": decision, "staleness": staleness}) + "\n")
    return 0


if __name__ == "__main__":
    try:
        rc = main()
    except Refuse as exc:
        sys.stderr.write("invalid_input: " + str(exc) + "\n")
        sys.exit(1)
    except Exception as exc:  # twin bug: distinct exit so it is never mistaken for a refusal
        sys.stderr.write("twin_internal_error: " + repr(exc) + "\n")
        sys.exit(2)
    sys.exit(rc)
