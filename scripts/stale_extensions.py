#!/usr/bin/env python3
"""stale_extensions.py — RFC 5861 stale-while-revalidate / stale-if-error decision.

Candidate for kake round 98, claim C2 (freshness capability acquisition).
Built from the contract alone: `.ufo/waves/round-98/stale-contract.md`
(contract v1), grounded in RFC 5861 §3 (stale-while-revalidate), §3.1,
§4 (stale-if-error), §4.1, and RFC 9111 §4.2.4 (serving stale responses),
with RFC 9111 §5.2.2.2 must-revalidate, §5.2.2.8 proxy-revalidate,
§5.2.2.10 s-maxage, §5.2.2.4 / §5.2.1.4 no-cache, §1.2.2 delta-seconds,
and RFC 9110 §5.6.2 token/tchar, §5.6.4 quoted-string.

Interface (contract "Interface"):

    python3 scripts/stale_extensions.py            # ONE JSON object on stdin
    python3 scripts/stale_extensions.py --selftest # not scored

Decided: exit 0, stdout exactly one JSON object with exactly the keys
`decision` (string) and `staleness` (integer), then a newline.
Refused: exit 1, stdout empty, stderr begins `invalid_input:`.

Lane conventions implemented (contract "Cache-Control parsing" / "Decision"):

* FIRST occurrence of a Cache-Control name is used for its value
  (RFC 9111 §4.2.1 "the first occurrence"); later occurrences are ignored.
* `stale-while-revalidate` / `stale-if-error` values are delta-seconds and
  are valid only as an UNQUOTED 1*DIGIT token; a quoted or non-digit value
  makes that directive ABSENT (lane convention — not a refusal). A bare
  name (no value) is likewise absent.
* delta-seconds above 2147483648 are clamped to 2147483648
  (RFC 9111 §1.2.2); leading zeros are digits.
* `no-cache` counts as a prohibition whether qualified or not
  (conservative lane convention); presence of a prohibition name anywhere
  in the field is enough.
* On an error event the limit is the REQUEST's valid stale-if-error value
  when present, else the response's (RFC 5861 §4: a request directive's
  scope is the request it appears in).
* Boundaries are inclusive: staleness <= limit serves stale (RFC 5861 §4
  "more stale than the indicated amount SHOULD NOT"; §4.1 example usable
  at age 1800, i.e. staleness exactly 1200 for max-age 600 + 1200).
* Request directives max-age, max-stale, min-fresh, only-if-cached are
  outside the contract → refuse (checked when they appear in request_cc).
* stale-while-revalidate in a request is ignored (RFC 5861 defines it for
  responses only). Storage directives (no-store, private, public) and
  unknown extensions are ignored: the response is already stored and this
  tool decides nothing about storage.
* Names compare case-insensitively (RFC 9110 §5.6.2 token); elements are
  split on commas outside quoted-strings, SP/HTAB-stripped, empty elements
  skipped; no whitespace around `=`; parse failures (empty value after `=`,
  unterminated quote, text after the closing quote, a character above
  U+00FF, a control character, a name that is not 1*tchar) refuse the whole
  input. Unknown input keys, non-integer/boolean/float type violations,
  out-of-range `error`, and request directives refuse it too.

Not decided here: computing freshness_lifetime or current_age (they arrive
as inputs; see scripts/cache_current_age.py, scripts/heuristic_freshness.py),
Warning/Age emission, background revalidation scheduling, storage, and any
live cache behaviour.
"""

import json
import sys

MAX_DELTA_SECONDS = 2147483648  # RFC 9111 §1.2.2 cap

# Integer fields and delta-seconds values have no length bound in the contract;
# lift CPython's int/str conversion limit so a long digit string is decided, not
# crashed on (round-98 integration fix, ExecTwinStale A1-A4).
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

_TCHAR_EXTRA = "!#$%&'*+-.^_`|~"
_REQUEST_ONLY = frozenset(("max-age", "max-stale", "min-fresh", "only-if-cached"))
_ELIGIBLE_ERRORS = (500, 502, 503, 504)
_ALLOWED_KEYS = frozenset(
    ("response_cc", "request_cc", "freshness_lifetime", "current_age",
     "event", "error", "shared")
)


class _Refused(Exception):
    """Input is outside the contract; the caller answers exit 1."""


def _refuse(detail):
    raise _Refused(detail)


def _is_tchar(ch):
    return (
        ("a" <= ch <= "z")
        or ("A" <= ch <= "Z")
        or ("0" <= ch <= "9")
        or (ch in _TCHAR_EXTRA)
    )


def _split_elements(text):
    """Split on commas outside quoted-strings; strip SP/HTAB; skip empties."""
    elements = []
    cur = []
    in_quote = False
    escaped = False
    for ch in text:
        if in_quote:
            cur.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_quote = False
        elif ch == '"':
            in_quote = True
            cur.append(ch)
        elif ch == ",":
            elements.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if in_quote:
        _refuse("unterminated quoted-string")
    elements.append("".join(cur))
    out = []
    for el in elements:
        el = el.strip(" \t")
        if el:
            out.append(el)
    return out


def _check_quoted(s):
    """Validate s (starting at its opening DQUOTE) as one quoted-string."""
    if len(s) < 2:
        _refuse("unterminated quoted-string")
    i = 1
    while True:
        if i >= len(s):
            _refuse("unterminated quoted-string")
        ch = s[i]
        if ch == "\\":
            if i + 1 >= len(s):
                _refuse("unterminated quoted-pair")
            o = ord(s[i + 1])
            if not (o == 0x09 or o == 0x20 or 0x21 <= o <= 0x7E or 0x80 <= o <= 0xFF):
                _refuse("bad quoted-pair escape")
            i += 2
            continue
        if ch == '"':
            if i != len(s) - 1:
                _refuse("text after closing quote")
            return
        o = ord(ch)
        if not (o == 0x09 or o == 0x20 or o == 0x21 or 0x23 <= o <= 0x5B
                or 0x5D <= o <= 0x7E or 0x80 <= o <= 0xFF):
            _refuse("bad character in quoted-string")
        i += 1


def _parse_element(el):
    """Return (name, value_or_None, quoted) for one stripped element."""
    eq = -1
    in_quote = False
    escaped = False
    for idx, ch in enumerate(el):
        if in_quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_quote = False
        elif ch == '"':
            in_quote = True
        elif ch == "=":
            eq = idx
            break
    if eq < 0:
        for ch in el:
            if not _is_tchar(ch):
                _refuse("invalid character in directive name")
        return el, None, False
    name = el[:eq]
    rest = el[eq + 1:]
    if not name:
        _refuse("empty directive name")
    for ch in name:
        if not _is_tchar(ch):
            _refuse("invalid character in directive name")
    if not rest:
        _refuse("empty value after '='")
    if rest[0] == '"':
        _check_quoted(rest)
        return name, rest, True
    for ch in rest:
        if not _is_tchar(ch):
            _refuse("invalid character in directive value")
    return name, rest, False


def _parse_cache_control(text, field, is_request):
    """Parse one field into {name_lower: (value_or_None, quoted)}, first occurrence."""
    if not isinstance(text, str):
        _refuse(field + " must be a string")
    first = {}
    for el in _split_elements(text):
        name, value, quoted = _parse_element(el)
        key = name.lower()
        if is_request and key in _REQUEST_ONLY:
            _refuse("request directive %r is outside this contract" % key)
        if key not in first:
            first[key] = (value, quoted)
    return first


def _delta_seconds(directives, name):
    """Valid unquoted 1*DIGIT value -> clamped int; otherwise None (absent)."""
    entry = directives.get(name)
    if entry is None:
        return None
    value, quoted = entry
    if quoted or value is None:
        return None
    if not value or any(ch not in "0123456789" for ch in value):
        return None
    digits = value.lstrip("0") or "0"
    if len(digits) > 10:  # above 9999999999 > MAX_DELTA_SECONDS: clamp without int()
        return MAX_DELTA_SECONDS
    return min(int(digits), MAX_DELTA_SECONDS)


def _prohibited(resp, req, shared):
    if "no-cache" in resp:
        return True
    if "must-revalidate" in resp:
        return True
    if shared and ("proxy-revalidate" in resp or "s-maxage" in resp):
        return True
    if "no-cache" in req:
        return True
    return False


def _validate(obj):
    if not isinstance(obj, dict):
        _refuse("input must be one JSON object")
    unknown = set(obj) - _ALLOWED_KEYS
    if unknown:
        _refuse("unknown key(s): %s" % ", ".join(sorted(unknown)))
    if "response_cc" not in obj:
        _refuse("response_cc is required")
    if not isinstance(obj["response_cc"], str):
        _refuse("response_cc must be a string")
    if "request_cc" in obj and not isinstance(obj["request_cc"], str):
        _refuse("request_cc must be a string")
    for key in ("freshness_lifetime", "current_age"):
        if key not in obj:
            _refuse(key + " is required")
        v = obj[key]
        if type(v) is not int:
            _refuse(key + " must be an integer (no boolean, float or string)")
        if v < 0:
            _refuse(key + " must be >= 0")
    if "event" not in obj:
        _refuse("event is required")
    event = obj["event"]
    if event not in ("request", "error"):
        _refuse("event must be 'request' or 'error'")
    if "shared" in obj and type(obj["shared"]) is not bool:
        _refuse("shared must be a boolean")
    if event == "error":
        if "error" not in obj:
            _refuse("error is required when event is 'error'")
        err = obj["error"]
        ok = (isinstance(err, str) and err == "network") or (
            type(err) is int and 100 <= err <= 599)
        if not ok:
            _refuse("error must be an integer 100-599 or the string 'network'")
    elif "error" in obj and obj["error"] is not None:
        _refuse("error must be absent or null when event is 'request'")
    return obj


def _decide(obj):
    _validate(obj)
    resp = _parse_cache_control(obj["response_cc"], "response_cc", is_request=False)
    req = _parse_cache_control(obj.get("request_cc", ""), "request_cc", is_request=True)
    shared = obj.get("shared", False)
    lifetime = obj["freshness_lifetime"]
    age = obj["current_age"]
    staleness = max(0, age - lifetime)
    event = obj["event"]
    blocked = _prohibited(resp, req, shared)
    # Rule 1: RFC 5861 §4 — an error is a situation that would yield 500/502/503/504.
    if event == "error":
        err = obj["error"]
        if not (isinstance(err, str) and err == "network") and err not in _ELIGIBLE_ERRORS:
            return "not-an-error", staleness
    # Rule 2: fresh while A < L unless either field carries no-cache.
    if age < lifetime and "no-cache" not in resp and "no-cache" not in req:
        return "fresh", staleness
    if event == "request":
        # Rule 3: response stale-while-revalidate window (inclusive).
        window = _delta_seconds(resp, "stale-while-revalidate")
        if not blocked and window is not None and staleness <= window:
            return "serve-stale-revalidate", staleness
        return "revalidate", staleness
    # Rule 4: request stale-if-error takes precedence, else response's.
    limit = _delta_seconds(req, "stale-if-error")
    if limit is None:
        limit = _delta_seconds(resp, "stale-if-error")
    if not blocked and limit is not None and staleness <= limit:
        return "serve-stale-error", staleness
    return "error-through", staleness


def _process(raw):
    """Return (exit_code, stdout, stderr) for one stdin payload."""
    try:
        try:
            obj = json.loads(raw)
        except ValueError as exc:
            _refuse("not valid JSON: %s" % exc)
        decision, staleness = _decide(obj)
        return 0, json.dumps({"decision": decision, "staleness": staleness}) + "\n", ""
    except _Refused as exc:
        return 1, "", "invalid_input: %s\n" % exc


# ---------------------------------------------------------------- selftest

def _mk(**kw):
    base = {"response_cc": "", "freshness_lifetime": 600, "current_age": 0,
            "event": "request"}
    base.update(kw)
    return json.dumps(base)


def _selftest_cases():
    S = "serve-stale-revalidate"
    E = "serve-stale-error"
    ok = lambda d, s: ("ok", d, s)  # noqa: E731
    ref = ("refuse",)
    return [
        # --- decided: stale-while-revalidate (RFC 5861 §3/§3.1)
        ("swr basic window", _mk(response_cc="max-age=600, stale-while-revalidate=30",
                                 current_age=620), ok(S, 20)),
        ("swr inclusive edge (§3.1 30s)", _mk(response_cc="max-age=600, stale-while-revalidate=30",
                                              current_age=630), ok(S, 30)),
        ("swr past window", _mk(response_cc="max-age=600, stale-while-revalidate=30",
                                current_age=631), ok("revalidate", 31)),
        ("swr=0 at just stale", _mk(response_cc="stale-while-revalidate=0",
                                    current_age=600), ok(S, 0)),
        ("swr leading zeros", _mk(response_cc="max-age=600, stale-while-revalidate=030",
                                  current_age=630), ok(S, 30)),
        ("fresh plain", _mk(current_age=0), ok("fresh", 0)),
        ("fresh just under L", _mk(current_age=599), ok("fresh", 0)),
        ("fresh wins over swr (rule order)", _mk(response_cc="stale-while-revalidate=30",
                                                 current_age=599), ok("fresh", 0)),
        ("A==L is stale (exclusive fresh)", _mk(current_age=600), ok("revalidate", 0)),
        ("swr in request ignored", _mk(request_cc="stale-while-revalidate=999999",
                                       current_age=601), ok("revalidate", 1)),
        ("swr first occurrence wins", _mk(response_cc="stale-while-revalidate=30, "
                                                          "stale-while-revalidate=99999",
                                          current_age=631), ok("revalidate", 31)),
        ("swr first invalid -> absent (no fallback)",
         _mk(response_cc='stale-while-revalidate="x", stale-while-revalidate=30',
             current_age=610), ok("revalidate", 10)),
        ("swr quoted value absent", _mk(response_cc='stale-while-revalidate="30"',
                                        current_age=605), ok("revalidate", 5)),
        ("swr non-digit token absent", _mk(response_cc="stale-while-revalidate=abc",
                                           current_age=605), ok("revalidate", 5)),
        ("swr clamp makes window huge",
         _mk(response_cc="stale-while-revalidate=2147483649", freshness_lifetime=0,
             current_age=2147483648), ok(S, 2147483648)),
        ("unknown extension ignored", _mk(response_cc="x-gunicorn-expect=1, stale-while-revalidate=10",
                                          current_age=610), ok(S, 10)),
        ("second '=' in token value refused (tchar excludes '=')",
         _mk(response_cc="a=b=c, stale-while-revalidate=10"), ref),
        ("case-insensitive names", _mk(response_cc="MAX-AGE=600, STALE-WHILE-REVALIDATE=30",
                                       current_age=630), ok(S, 30)),
        ("OWS and empty elements skipped",
         _mk(response_cc=" , max-age=600, , stale-while-revalidate=30 , ",
             current_age=635), ok("revalidate", 35)),
        # --- decided: stale-if-error (RFC 5861 §4/§4.1)
        ("sie §4.1 example", _mk(response_cc="max-age=600, stale-if-error=1200",
                                 event="error", error=500, current_age=900), ok(E, 300)),
        ("sie inclusive at age 1800", _mk(response_cc="max-age=600, stale-if-error=1200",
                                          event="error", error=500, current_age=1800), ok(E, 1200)),
        ("sie past age 1800 (§4.1 greater-than)",
         _mk(response_cc="max-age=600, stale-if-error=1200", event="error", error=500,
             current_age=1801), ok("error-through", 1201)),
        ("sie network error", _mk(response_cc="stale-if-error=100", event="error",
                                  error="network", freshness_lifetime=10, current_age=20), ok(E, 10)),
        ("sie 502", _mk(response_cc="stale-if-error=100", event="error", error=502,
                        freshness_lifetime=10, current_age=20), ok(E, 10)),
        ("sie 503", _mk(response_cc="stale-if-error=100", event="error", error=503,
                        freshness_lifetime=10, current_age=20), ok(E, 10)),
        ("sie 504", _mk(response_cc="stale-if-error=100", event="error", error=504,
                        freshness_lifetime=10, current_age=20), ok(E, 10)),
        ("404 is not-an-error", _mk(response_cc="stale-if-error=100", event="error",
                                    error=404, freshness_lifetime=10, current_age=20),
         ok("not-an-error", 10)),
        ("501 is not-an-error", _mk(response_cc="stale-if-error=100", event="error",
                                    error=501, freshness_lifetime=10, current_age=20),
         ok("not-an-error", 10)),
        ("599 is not-an-error", _mk(response_cc="stale-if-error=100", event="error",
                                    error=599, freshness_lifetime=0, current_age=5),
         ok("not-an-error", 5)),
        ("100 is not-an-error", _mk(response_cc="stale-if-error=100", event="error",
                                    error=100, freshness_lifetime=0, current_age=5),
         ok("not-an-error", 5)),
        ("not-an-error reports clamped staleness", _mk(response_cc="stale-if-error=100",
                                                       event="error", error=404,
                                                       freshness_lifetime=100, current_age=3),
         ok("not-an-error", 0)),
        ("fresh on error event (rule 2 first)", _mk(response_cc="stale-if-error=1200",
                                                    event="error", error=500,
                                                    current_age=599), ok("fresh", 0)),
        ("no sie anywhere -> error-through", _mk(event="error", error=500,
                                                 freshness_lifetime=10, current_age=20),
         ok("error-through", 10)),
        ("response sie quoted absent", _mk(response_cc='stale-if-error="1200"',
                                           event="error", error=500, current_age=900),
         ok("error-through", 300)),
        ("sie=0 inclusive at staleness 0", _mk(response_cc="stale-if-error=0",
                                               event="error", error=500,
                                               current_age=600), ok(E, 0)),
        ("sie clamp to 2**31 inclusive",
         _mk(response_cc="stale-if-error=99999999999999999999", freshness_lifetime=0,
             event="error", error=500, current_age=2147483648), ok(E, 2147483648)),
        ("sie clamp boundary from above",
         _mk(response_cc="stale-if-error=2147483648", freshness_lifetime=0,
             event="error", error=500, current_age=2147483649), ok("error-through", 2147483649)),
        # --- request stale-if-error precedence (RFC 5861 §4 scope)
        ("request sie below response", _mk(request_cc="stale-if-error=100",
                                           response_cc="stale-if-error=1200", event="error",
                                           error=500, current_age=650), ok(E, 50)),
        ("request sie inclusive edge", _mk(request_cc="stale-if-error=100",
                                           response_cc="stale-if-error=1200", event="error",
                                           error=500, current_age=700), ok(E, 100)),
        ("request sie precedence blocks response window",
         _mk(request_cc="stale-if-error=100", response_cc="stale-if-error=1200",
             event="error", error=500, current_age=701), ok("error-through", 101)),
        ("request sie quoted falls back to response",
         _mk(request_cc='stale-if-error="100"', response_cc="stale-if-error=1200",
             event="error", error=500, current_age=800), ok(E, 200)),
        ("request sie absent, response decides", _mk(response_cc="stale-if-error=50",
                                                     event="error", error=500,
                                                     current_age=650), ok(E, 50)),
        # --- prohibitions (RFC 9111 §4.2.4, §5.2.2.2/§5.2.2.8/§5.2.2.10, no-cache)
        ("response no-cache blocks swr", _mk(response_cc="no-cache, stale-while-revalidate=30",
                                             current_age=620), ok("revalidate", 20)),
        ("qualified no-cache conservative", _mk(response_cc='no-cache="Set-Cookie", '
                                                             "stale-while-revalidate=30",
                                                current_age=620), ok("revalidate", 20)),
        ("no-cache with comma inside quoted value",
         _mk(response_cc='no-cache="a,b", stale-while-revalidate=30', current_age=620),
         ok("revalidate", 20)),
        ("request no-cache blocks fresh", _mk(request_cc="no-cache", current_age=10),
         ok("revalidate", 0)),
        ("request no-cache blocks sie", _mk(request_cc="no-cache",
                                            response_cc="stale-if-error=1200",
                                            event="error", error=500, current_age=900),
         ok("error-through", 300)),
        ("must-revalidate blocks sie", _mk(response_cc="must-revalidate, stale-if-error=1200",
                                           event="error", error=500, current_age=900),
         ok("error-through", 300)),
        ("must-revalidate does not block fresh", _mk(response_cc="must-revalidate",
                                                     current_age=10), ok("fresh", 0)),
        ("shared + proxy-revalidate blocks sie", _mk(response_cc="proxy-revalidate, "
                                                                 "stale-if-error=100",
                                                     event="error", error=500, shared=True,
                                                     current_age=610), ok("error-through", 10)),
        ("shared + s-maxage blocks swr", _mk(response_cc="s-maxage, stale-while-revalidate=30",
                                             shared=True, current_age=620),
         ok("revalidate", 20)),
        ("shared=false ignores proxy-revalidate", _mk(response_cc="proxy-revalidate, "
                                                                 "stale-if-error=100",
                                                      event="error", error=500,
                                                      current_age=610), ok(E, 10)),
        ("storage directives ignored", _mk(response_cc="no-store, private, public, "
                                                       "stale-if-error=1200",
                                           event="error", error=500, current_age=900), ok(E, 300)),
        ("error null allowed with request event", _mk(error=None, current_age=0),
         ok("fresh", 0)),
        ("no request_cc key defaults to empty", _mk(response_cc="stale-while-revalidate=30",
                                                    current_age=630), ok(S, 30)),
        # --- refusals: shape
        ("unknown key refused",
         '{"response_cc":"","freshness_lifetime":1,"current_age":0,"event":"request","zzz":1}',
         ref),
        ("missing response_cc",
         '{"freshness_lifetime":1,"current_age":0,"event":"request"}', ref),
        ("missing freshness_lifetime",
         '{"response_cc":"","current_age":0,"event":"request"}', ref),
        ("missing current_age",
         '{"response_cc":"","freshness_lifetime":1,"event":"request"}', ref),
        ("missing event", '{"response_cc":"","freshness_lifetime":1,"current_age":0}', ref),
        ("bad event", _mk(event="tick"), ref),
        ("event numeric", '{"response_cc":"","freshness_lifetime":1,"current_age":0,"event":5}',
         ref),
        ("float freshness_lifetime", _mk(freshness_lifetime=600.5), ref),
        ("boolean freshness_lifetime", _mk(freshness_lifetime=True), ref),
        ("string freshness_lifetime", _mk(freshness_lifetime="600"), ref),
        ("negative freshness_lifetime", _mk(freshness_lifetime=-1), ref),
        ("float current_age", _mk(current_age=0.0), ref),
        ("boolean current_age", _mk(current_age=False), ref),
        ("negative current_age", _mk(current_age=-1), ref),
        ("response_cc numeric", '{"response_cc":42,"freshness_lifetime":1,"current_age":0,'
                                '"event":"request"}', ref),
        ("response_cc null",
         '{"response_cc":null,"freshness_lifetime":1,"current_age":0,"event":"request"}', ref),
        ("request_cc numeric", _mk(request_cc=5), ref),
        ("shared numeric", _mk(shared=1), ref),
        ("shared string", _mk(shared="true"), ref),
        ("shared null", _mk(shared=None), ref),
        # --- refusals: error field
        ("error missing on error event", _mk(event="error", error=None), ref),
        ("error 600", _mk(event="error", error=600, current_age=0), ref),
        ("error 99", _mk(event="error", error=99, current_age=0), ref),
        ("error float", _mk(event="error", error=500.0, current_age=0), ref),
        ("error boolean", _mk(event="error", error=True, current_age=0), ref),
        ("error unknown string", _mk(event="error", error="timeout", current_age=0), ref),
        ("error 500 with request event", _mk(error=500), ref),
        ("error false with request event", _mk(error=False), ref),
        # --- refusals: request directives
        ("request max-age refused", _mk(request_cc="max-age=5"), ref),
        ("request max-stale refused", _mk(request_cc="max-stale"), ref),
        ("request min-fresh refused", _mk(request_cc="min-fresh=10"), ref),
        ("request only-if-cached refused", _mk(request_cc="only-if-cached"), ref),
        ("request MAX-AGE uppercase refused", _mk(request_cc="MAX-AGE=5"), ref),
        ("request quoted max-age refused", _mk(request_cc='max-age="5"'), ref),
        # --- refusals: JSON shape
        ("invalid JSON", "{nope", ref),
        ("JSON array", "[]", ref),
        ("JSON string", '"x"', ref),
        ("JSON number", "42", ref),
        ("JSON null", "null", ref),
        ("empty input", "", ref),
        ("trailing data", '{"response_cc":"","freshness_lifetime":1,"current_age":0,'
                          '"event":"request"} trailing', ref),
        # --- refusals: Cache-Control grammar
        ("unterminated quote", _mk(response_cc='max-age="600'), ref),
        ("unterminated quote with escaped close", _mk(response_cc='max-age="600\\"'), ref),
        ("whitespace before '='", _mk(response_cc="max-age = 600"), ref),
        ("whitespace after '='", _mk(response_cc="max-age= 600"), ref),
        ("empty value after '='", _mk(response_cc="max-age=, x"), ref),
        ("text after closing quote", _mk(response_cc='no-cache="x"y'), ref),
        ("empty quoted-string value is legal (not a refusal)",
         _mk(response_cc='x-marker="", stale-while-revalidate=10', current_age=610), ok(S, 10)),
        ("name with space", _mk(response_cc="max age=600"), ref),
        ("empty name", _mk(response_cc='="x"'), ref),
        ("bare quoted element", _mk(response_cc='"justquote"'), ref),
        ("backslash in token", _mk(response_cc="a\\b"), ref),
        ("control character in field", _mk(response_cc="max-age=6\n00"), ref),
        ("DEL in quoted-string", _mk(response_cc='no-cache="a\x7fb"'), ref),
        ("NUL in quoted-string", _mk(response_cc='no-cache="a\x00b"'), ref),
        ("character above U+00FF in token", _mk(response_cc="max-age=\u2603"), ref),
        ("character above U+00FF in quoted-string", _mk(response_cc='no-cache="\u2603"'), ref),
        ("character above U+00FF in name", _mk(response_cc="no\u2603cache=1"), ref),
    ]


def _selftest():
    cases = _selftest_cases()
    failures = []
    for label, raw, want in cases:
        code, out, err = _process(raw)
        if want == ("refuse",):
            good = code == 1 and out == "" and err.startswith("invalid_input:")
        else:
            _, decision, staleness = want
            good = False
            if code == 0:
                try:
                    got = json.loads(out)
                    good = (got == {"decision": decision, "staleness": staleness}
                            and set(got) == {"decision", "staleness"}
                            and out.endswith("\n"))
                except ValueError:
                    good = False
        if not good:
            failures.append((label, raw, want, code, out.strip(), err.strip()))
    print("selftest cases=%d passed=%d failed=%d" % (len(cases), len(cases) - len(failures),
                                                     len(failures)))
    for label, raw, want, code, out, err in failures:
        print("FAIL %s: want=%r got rc=%d stdout=%r stderr=%r" % (label, want, code, out, err))
    return 1 if failures else 0


def main(argv):
    if "--selftest" in argv[1:]:
        return _selftest()
    try:
        raw = sys.stdin.buffer.read().decode("utf-8")
    except UnicodeDecodeError as exc:
        sys.stderr.write("invalid_input: stdin is not valid UTF-8: %s\n" % exc)
        return 1
    code, out, err = _process(raw)
    if code == 0:
        sys.stdout.write(out)
        return 0
    sys.stderr.write(err)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
