#!/usr/bin/env python3
"""Round-100 C2 candidate v2: freshening stored responses upon a 304.

Independent implementation of contract v2
(.ufo/waves/round-100/fresh304-contract-v2.md, kake round 100), amending
contract v1 (.ufo/waves/round-99/fresh304-contract.md), sourced on:
RFC 9111 section 4.3.4 (freshening stored responses upon validation),
section 3.2 (updating stored header fields), section 3.1 (storing header
fields, esp. bullet 4 MUST NOT store proxy-specific fields, bullet 3
qualified no-cache/private), section 5.2 (Cache-Control grammar, either
argument form, case-insensitive directive names), section 5.2.3 (ignore
unrecognised directives); RFC 9110 section 5.5 (field values exclude
surrounding whitespace), section 5.6.1.2 (list syntax, empty elements),
section 5.6.4 (quoted-string) / 5.6.2 tokens.
Lane conventions: LC1 Last-Modified always weak; LC2 correspondence for
every validator the 304 carries (ETag weak comparison, Last-Modified
trimmed equality), most-recent identified; LC3 tie at largest received
refused; LC4 keep-alive/proxy-connection/te/transfer-encoding/upgrade
never copied; LC5 no other exclusion; LC6 replaced by V2-1 (full
Cache-Control parse, qualified no-cache/private in either argument form
refused, malformed refused per LC8); LC8 fail-closed refusal of an
unparseable list. V2-1: quoted-string commas do not split, whitespace
only as OWS around commas and at ends, empty elements accepted.
V2-2: output header values trimmed of leading/trailing SP/HTAB.
V2-3: proxy-authenticate/proxy-authentication-info/proxy-authorization
dropped when the stored response carries them, as well as from the 304.
Clarifications e1-e7: update starts from all stored fields minus V2-3;
malformed ETag in ANY stored response refused; Last-Modified trims SP+HTAB;
refusal stdout empty; decision stdout one JSON object +- one newline;
non-UTF-8/invalid JSON refused; age and other 304 fields copied; LC3
applies whatever validators the 304 carries.
I/O contract: stdin BYTES -> one JSON object on stdout + one newline,
exit 0. Refusal: `invalid_input: <reason>` on stderr, zero bytes on
stdout, exit 1. Every argv word other than `--selftest` is ignored.
`--selftest` runs >=40 in-memory cases (every V2 clause and e1-e7) and
prints `selftest <ok>/<total>`, exit 0 only when all pass. No file,
socket or subprocess in the decision path. Stdlib only.
"""

import json
import re
import sys


class Refusal(Exception):
    """Contract refusal: exit 1, stderr invalid_input, empty stdout."""


def refuse(reason):
    raise Refusal(reason)


# RFC 9110 section 5.6.2 token: 1*tchar (ASCII letters, digits, and
# ! # $ % & ' * + - . ^ _ ` | ~).
_TOKEN = re.compile(r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+\Z")
# Contract ETag: single entity-tag; opaque-tag is zero or more of `!`,
# `#`-`~` or obs-text (0x80-0xFF); `W/` prefix uppercase only.
_ETAG = re.compile(r'(?:W/)?"[!#-~\x80-\xff]*"\Z')

# 304 fields never copied into the stored map: RFC 9111 3.2 bullet 1
# exceptions (via 3.1 bullets 1, 2 and 4) plus 3.2 bullet 4
# (content-length). LC4 fixes bullet 2's open-ended set.
_NEVER_COPY = frozenset((
    "content-length",              # 3.2 bullet 4
    "connection",                  # 3.1 bullet 1
    "keep-alive",                  # LC4 (3.1 bullet 2, RFC 9110 7.6.1)
    "proxy-connection",            # LC4
    "te",                          # LC4
    "transfer-encoding",           # LC4
    "upgrade",                     # LC4
    "proxy-authenticate",          # 3.1 bullet 4
    "proxy-authentication-info",   # 3.1 bullet 4
    "proxy-authorization",         # 3.1 bullet 4
))

# V2-3: proxy-specific fields also dropped from the stored base map.
_PROXY_DROP = frozenset((
    "proxy-authenticate",
    "proxy-authentication-info",
    "proxy-authorization",
))


def _require_keys(obj, expected, what):
    if not isinstance(obj, dict):
        refuse(what + " must be an object")
    extra = sorted(set(obj) - expected)
    missing = sorted(expected - set(obj))
    if extra:
        refuse(what + " has unexpected key " + repr(extra[0]))
    if missing:
        refuse(what + " is missing key " + repr(missing[0]))


def _check_headers(headers, what):
    """Validate one header map; return {lowercase name: raw value}."""
    if not isinstance(headers, dict):
        refuse(what + " headers must be an object")
    lowered = {}
    for name, value in headers.items():
        if not isinstance(name, str) or not _TOKEN.match(name):
            refuse(what + " invalid header name " + repr(name))
        low = name.lower()
        if low in lowered:
            refuse(what + " duplicate header name ignoring case: " + low)
        if not isinstance(value, str):
            refuse(what + " header " + low + " value is not a string")
        if "\r" in value:
            refuse(what + " header " + low + " value contains CR")
        if "\n" in value:
            refuse(what + " header " + low + " value contains LF")
        if "\x00" in value:
            refuse(what + " header " + low + " value contains NUL")
        lowered[low] = value
    return lowered


def _parse_etag(value, what):
    v = value.strip(" \t")
    if not _ETAG.match(v):
        refuse(what + " is not a single entity-tag: " + repr(value))
    weak = v.startswith("W/")
    opaque = v[3:-1] if weak else v[1:-1]
    return {"weak": weak, "opaque": opaque}


def _connection_names(value):
    """Names listed in a Connection value; empty members ignored (LC)."""
    names = set()
    for member in value.split(","):
        member = member.strip(" \t")
        if member:
            names.add(member.lower())
    return names

_TCHAR = frozenset("!#$%&'*+-.^_`|~0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
_QDTEXT_OK = lambda ch: ch == "\t" or ch == " " or ("!" <= ch <= "[") or ("]" <= ch <= "~") or ("\x80" <= ch <= "\xff")
_QP_OK = lambda ch: ch == "\t" or ch == " " or ("!" <= ch <= "~") or ("\x80" <= ch <= "\xff")


def _parse_cache_control(value):
    """V2-1: parse RFC 9111 5.2 list. Returns list of (name, has_arg).
    Refuses malformed per LC8."""
    n = len(value)
    i = 0
    def ows(i):
        while i < n and value[i] in " \t":
            i += 1
        return i
    i = ows(i)
    directives = []
    while True:
        # skip empty elements: consecutive commas / leading comma
        if i < n and value[i] == ",":
            i += 1
            i = ows(i)
            continue
        if i >= n:
            break
        # token name
        start = i
        while i < n and value[i] in _TCHAR:
            i += 1
        if i == start:
            refuse("malformed cache-control")
        name = value[start:i]
        has_arg = False
        if i < n and value[i] == "=":
            has_arg = True
            i += 1
            if i < n and value[i] == '"':
                i += 1
                closed = False
                while i < n:
                    ch = value[i]
                    if ch == '"':
                        i += 1
                        closed = True
                        break
                    if ch == "\\":
                        if i + 1 >= n or not _QP_OK(value[i + 1]):
                            refuse("malformed cache-control")
                        i += 2
                        continue
                    if not _QDTEXT_OK(ch):
                        refuse("malformed cache-control")
                    i += 1
                if not closed:
                    refuse("malformed cache-control")
            else:
                start = i
                while i < n and value[i] in _TCHAR:
                    i += 1
                if i == start:
                    refuse("malformed cache-control")
        directives.append((name, has_arg))
        i = ows(i)
        if i < n and value[i] == ",":
            i += 1
            i = ows(i)
            continue
        if i >= n:
            break
        refuse("malformed cache-control")
    return directives


def _validate(raw):
    if isinstance(raw, bytes):
        try:
            raw = raw.decode("utf-8")
        except UnicodeDecodeError:
            refuse("input is not valid UTF-8")
    try:
        data = json.loads(raw)
    except ValueError:
        refuse("input is not valid JSON")
    _require_keys(data, {"stored", "response"}, "input")
    stored_raw = data["stored"]
    if not isinstance(stored_raw, list):
        refuse("stored must be a list")
    response = data["response"]
    _require_keys(response, {"status", "headers"}, "response")
    status = response["status"]
    if isinstance(status, bool) or not isinstance(status, int):
        refuse("status must be the integer 304")
    if status != 304:
        refuse("status must be the integer 304, got " + repr(status))
    resp_headers = _check_headers(response["headers"], "response")
    if "etag" in resp_headers:
        _parse_etag(resp_headers["etag"], "304 ETag")
    if "cache-control" in resp_headers:
        for name, has_arg in _parse_cache_control(resp_headers["cache-control"]):
            if has_arg and name.lower() in ("no-cache", "private"):
                refuse("qualified cache-control outside contract")
    stored = []
    seen_ids = set()
    for index, element in enumerate(stored_raw):
        what = "stored[" + str(index) + "]"
        _require_keys(element, {"id", "received", "headers"}, what)
        sid = element["id"]
        if isinstance(sid, bool) or not isinstance(sid, str):
            refuse(what + ".id must be a string")
        if not sid:
            refuse(what + ".id must be non-empty")
        if sid in seen_ids:
            refuse(what + ".id duplicates a previous id: " + sid)
        seen_ids.add(sid)
        received = element["received"]
        if isinstance(received, bool) or not isinstance(received, int):
            refuse(what + ".received must be an integer")
        headers = _check_headers(element["headers"], what)
        etag = None
        if "etag" in headers:
            etag = _parse_etag(headers["etag"], what + " ETag")
        stored.append({"id": sid, "received": received,
                       "headers": headers, "etag": etag})
    return stored, resp_headers


def _select(stored, resp_headers):
    """RFC 9111 4.3.4 first-match rule; returns (rule, identified)."""
    etag304 = None
    if "etag" in resp_headers:
        etag304 = _parse_etag(resp_headers["etag"], "304 ETag")
    lm304 = None
    if "last-modified" in resp_headers:
        lm304 = resp_headers["last-modified"].strip(" \t")

    if etag304 is not None and not etag304["weak"]:
        identified = [s for s in stored
                      if s["etag"] is not None
                      and not s["etag"]["weak"]
                      and s["etag"]["opaque"] == etag304["opaque"]]
        return "strong", identified

    if etag304 is not None or lm304 is not None:
        corresponding = []
        for s in stored:
            if etag304 is not None:
                if s["etag"] is None or s["etag"]["opaque"] != etag304["opaque"]:
                    continue
            if lm304 is not None:
                if "last-modified" not in s["headers"]:
                    continue
                if s["headers"]["last-modified"].strip(" \t") != lm304:
                    continue
            corresponding.append(s)
        if not corresponding:
            return "weak", []
        newest = max(s["received"] for s in corresponding)
        top = [s for s in corresponding if s["received"] == newest]
        if len(top) > 1:
            refuse("ambiguous most recent")
        return "weak", top

    if len(stored) == 1:
        only = stored[0]
        if only["etag"] is None and "last-modified" not in only["headers"]:
            return "no-validator", [only]
    return "no-validator", []


def _update(stored, resp_headers, rule, identified):
    """RFC 9111 3.2 update applied to every identified response."""
    excluded = set(_NEVER_COPY)
    if "connection" in resp_headers:
        excluded |= _connection_names(resp_headers["connection"])
    updated = []
    for s in identified:
        # V2-3: drop proxy-specific fields from stored base (e1: all else kept)
        headers = {k: v.strip(" \t") for k, v in s["headers"].items()
                   if k not in _PROXY_DROP}
        for name, value in resp_headers.items():
            if name not in excluded:
                headers[name] = value.strip(" \t")
        updated.append({"id": s["id"], "headers": headers})
    if updated:
        decision = "update"
    elif rule == "strong":
        decision = "must-not-update"
    else:
        decision = "no-update"
    return {"decision": decision, "rule": rule, "updated": updated}


def process(raw):
    stored, resp_headers = _validate(raw)
    rule, identified = _select(stored, resp_headers)
    return _update(stored, resp_headers, rule, identified)


def _selftest_cases():
    st = lambda i, r, h: {"id": i, "received": r, "headers": h}
    r304 = lambda h: {"status": 304, "headers": h}
    out = lambda d, r, u: {"decision": d, "rule": r, "updated": u}
    upd = lambda i, h: {"id": i, "headers": h}
    mn = out("must-not-update", "strong", [])
    cases = []
    add = cases.append

    add(("strong-basic",
         {"stored": [st("a", 1, {"etag": '"v1"', "x-old": "1"})],
          "response": r304({"etag": '"v1"', "cache-control": "max-age=60"})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v1"', "x-old": "1",
                               "cache-control": "max-age=60"})])))
    add(("strong-two-identified",
         {"stored": [st("a", 1, {"etag": '"v"'}), st("b", 2, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "x-n": "n"})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"', "x-n": "n"}),
                     upd("b", {"etag": '"v"', "x-n": "n"})])))
    add(("strong-stored-weak-same-opaque",
         {"stored": [st("a", 1, {"etag": 'W/"v"'})],
          "response": r304({"etag": '"v"'})}, "out", mn))
    add(("strong-no-match",
         {"stored": [st("a", 1, {"etag": '"other"'})],
          "response": r304({"etag": '"v"'})}, "out", mn))
    add(("strong-stored-untagged",
         {"stored": [st("a", 1, {"x": "1"})],
          "response": r304({"etag": '"v"'})}, "out", mn))
    add(("strong-opaque-case-sensitive",
         {"stored": [st("a", 1, {"etag": '"a"'})],
          "response": r304({"etag": '"A"'})}, "out", mn))
    add(("strong-obs-text-opaque",
         {"stored": [st("a", 1, {"etag": '"café"'})],
          "response": r304({"etag": '"café"'})},
         "out", out("update", "strong", [upd("a", {"etag": '"café"'})])))
    add(("strong-trim-grammar-trimmed-output",
         {"stored": [st("a", 1, {"etag": '"v"', "x": "y"})],
          "response": r304({"etag": " \t\"v\"\t "})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"', "x": "y"})])))
    add(("strong-rule-ignores-304-last-modified",
         {"stored": [st("a", 1, {"etag": '"v"',
                                 "last-modified": "Mon, 14 Nov 1994 08:00:00 GMT",
                                 "x-keep": "k"})],
          "response": r304({"etag": '"v"',
                            "last-modified": "Tue, 15 Nov 1994 08:12:31 GMT"})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"',
                               "last-modified": "Tue, 15 Nov 1994 08:12:31 GMT",
                               "x-keep": "k"})])))
    add(("stored-malformed-etag-refused",
         {"stored": [st("a", 1, {"etag": '"ok"'}), st("b", 2, {"etag": "abc"})],
          "response": r304({"etag": '"ok"'})}, "refuse", None))
    add(("304-malformed-etag-refused",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v'})}, "refuse", None))
    add(("weak-over-strong-stored",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": 'W/"v"'})},
         "out", out("update", "weak", [upd("a", {"etag": 'W/"v"'})])))
    add(("weak-both-weak",
         {"stored": [st("a", 1, {"etag": 'W/"v"'})],
          "response": r304({"etag": 'W/"v"'})},
         "out", out("update", "weak", [upd("a", {"etag": 'W/"v"'})])))
    add(("weak-no-match",
         {"stored": [st("a", 1, {"etag": '"b"'})],
          "response": r304({"etag": 'W/"v"'})},
         "out", out("no-update", "weak", [])))
    add(("weak-most-recent",
         {"stored": [st("p", 5, {"etag": '"v"'}), st("q", 7, {"etag": '"v"'})],
          "response": r304({"etag": 'W/"v"', "x-n": "n"})},
         "out", out("update", "weak",
                    [upd("q", {"etag": 'W/"v"', "x-n": "n"})])))
    add(("weak-received-tie-refused",
         {"stored": [st("p", 7, {"etag": '"v"'}), st("q", 7, {"etag": '"v"'})],
          "response": r304({"etag": 'W/"v"'})}, "refuse", None))
    add(("weak-negative-received",
         {"stored": [st("p", -5, {"etag": '"v"'}),
                     st("q", -1, {"etag": '"v"'})],
          "response": r304({"etag": 'W/"v"'})},
         "out", out("update", "weak", [upd("q", {"etag": 'W/"v"'})])))
    add(("weak-max-among-correspondents-only",
         {"stored": [st("a", 9, {"etag": '"zz"'}),
                     st("b", 2, {"etag": '"v"'}),
                     st("c", 5, {"etag": '"v"'})],
          "response": r304({"etag": 'W/"v"'})},
         "out", out("update", "weak", [upd("c", {"etag": 'W/"v"'})])))
    add(("weak-three-way-tie-refused",
         {"stored": [st("a", 1, {"etag": '"v"'}), st("b", 7, {"etag": '"v"'}),
                     st("c", 7, {"etag": '"v"'})],
          "response": r304({"etag": 'W/"v"'})}, "refuse", None))
    add(("weak-lm-only",
         {"stored": [st("a", 1, {"last-modified": "Tue, 15 Nov 1994 08:12:31 GMT",
                                 "x": "1"})],
          "response": r304({"last-modified": "Tue, 15 Nov 1994 08:12:31 GMT"})},
         "out", out("update", "weak",
                    [upd("a", {"last-modified": "Tue, 15 Nov 1994 08:12:31 GMT",
                               "x": "1"})])))
    add(("weak-lm-trimmed-comparison",
         {"stored": [st("a", 1, {"last-modified": "  Tue, 15 Nov 1994 08:12:31 GMT\t"})],
          "response": r304({"last-modified": "Tue, 15 Nov 1994 08:12:31 GMT"})},
         "out", out("update", "weak",
                    [upd("a", {"last-modified": "Tue, 15 Nov 1994 08:12:31 GMT"})])))
    add(("weak-lm-octet-equality-case-sensitive",
         {"stored": [st("a", 1, {"last-modified": "tue, 15 nov 1994 08:12:31 gmt"})],
          "response": r304({"last-modified": "Tue, 15 Nov 1994 08:12:31 GMT"})},
         "out", out("no-update", "weak", [])))
    add(("weak-etag-plus-lm-stored-missing-lm",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": 'W/"v"', "last-modified": "L"})},
         "out", out("no-update", "weak", [])))
    add(("weak-etag-plus-lm-both-match",
         {"stored": [st("a", 1, {"etag": 'W/"v"', "last-modified": "L"})],
          "response": r304({"etag": 'W/"v"', "last-modified": "L"})},
         "out", out("update", "weak",
                    [upd("a", {"etag": 'W/"v"', "last-modified": "L"})])))
    add(("weak-empty-stored-no-correspondent",
         {"stored": [], "response": r304({"etag": 'W/"v"'})},
         "out", out("no-update", "weak", [])))
    add(("strong-empty-stored-must-not-update",
         {"stored": [], "response": r304({"etag": '"v"'})}, "out", mn))
    add(("no-validator-update",
         {"stored": [st("s", 1, {"content-type": "text/html"})],
          "response": r304({"x-refresh": "1"})},
         "out", out("update", "no-validator",
                    [upd("s", {"content-type": "text/html",
                               "x-refresh": "1"})])))
    add(("no-validator-stored-has-etag",
         {"stored": [st("a", 1, {"etag": '"a"'})],
          "response": r304({})}, "out", out("no-update", "no-validator", [])))
    add(("no-validator-stored-has-lm",
         {"stored": [st("a", 1, {"last-modified": "L"})],
          "response": r304({})}, "out", out("no-update", "no-validator", [])))
    add(("no-validator-two-stored",
         {"stored": [st("a", 1, {"x": "1"}), st("b", 2, {"y": "2"})],
          "response": r304({})}, "out", out("no-update", "no-validator", [])))
    add(("no-validator-empty-stored",
         {"stored": [], "response": r304({})},
         "out", out("no-update", "no-validator", [])))
    add(("exclude-content-length",
         {"stored": [st("a", 1, {"etag": '"v"', "content-length": "99"})],
          "response": r304({"etag": '"v"', "content-length": "123"})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"', "content-length": "99"})])))
    add(("exclude-connection-and-listed-names",
         {"stored": [st("a", 1, {"etag": '"v"', "x-drop": "old"})],
          "response": r304({"connection": "X-Drop, te", "etag": '"v"',
                            "x-drop": "d", "te": "trailers", "x-keep": "k"})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"', "x-drop": "old",
                               "x-keep": "k"})])))
    add(("exclude-connection-empty-value",
         {"stored": [st("a", 1, {"etag": '"v"', "x": "y"})],
          "response": r304({"connection": "", "etag": '"v"'})},
         "out", out("update", "strong", [upd("a", {"etag": '"v"', "x": "y"})])))
    add(("exclude-connection-empty-members-ignored",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"connection": "a, , b", "etag": '"v"',
                            "a": "1", "b": "2"})},
         "out", out("update", "strong", [upd("a", {"etag": '"v"'})])))
    add(("exclude-lc4-hop-by-hop-set",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"keep-alive": "timeout=5",
                            "proxy-connection": "close", "te": "gzip",
                            "transfer-encoding": "chunked", "upgrade": "h2c",
                            "etag": '"v"'})},
         "out", out("update", "strong", [upd("a", {"etag": '"v"'})])))
    add(("exclude-proxy-trio",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"proxy-authenticate": "Basic",
                            "proxy-authentication-info": "i",
                            "proxy-authorization": "Basic z",
                            "etag": '"v"'})},
         "out", out("update", "strong", [upd("a", {"etag": '"v"'})])))
    add(("exclude-name-matching-case-insensitive",
         {"stored": [st("a", 1, {"etag": '"v"', "content-length": "9"})],
          "response": r304({"Content-Length": "5", "etag": '"v"'})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"', "content-length": "9"})])))
    add(("replace-same-name-case-insensitive",
         {"stored": [st("a", 1, {"etag": '"w"', "x-a": "1"})],
          "response": r304({"Etag": '"w"'})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"w"', "x-a": "1"})])))
    add(("output-lowercases-stored-names",
         {"stored": [st("a", 1, {"ETag": '"v"', "X-KEEP": "k"})],
          "response": r304({"etag": 'W/"v"'})},
         "out", out("update", "weak",
                    [upd("a", {"etag": 'W/"v"', "x-keep": "k"})])))
    add(("v2-2-values-trimmed",
         {"stored": [st("s", 1, {"a": "  padded  ", "b": "\tpadded2\t"})],
          "response": r304({"x-pad": "  padded  "})},
         "out", out("update", "no-validator",
                    [upd("s", {"a": "padded", "b": "padded2", "x-pad": "padded"})])))
    add(("lc6-no-cache-qualified-refused",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"',
                            "cache-control": 'no-cache="set-cookie"'})},
         "refuse", None))
    add(("lc6-private-qualified-refused",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"',
                            "cache-control": 'private="x-foo"'})},
         "refuse", None))
    add(("lc6-unqualified-forms-ok",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"',
                            "cache-control": "no-cache, private"})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"',
                               "cache-control": "no-cache, private"})])))
    add(("lc6-qualified-no-cache-uppercase-refused",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"',
                            "cache-control": 'NO-CACHE="set-cookie"'})},
         "refuse", None))
    add(("lc6-qualified-private-mixed-case-refused",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"',
                            "cache-control": 'Private="history"'})},
         "refuse", None))
    add(("lc6-unqualified-uppercase-ok",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"',
                            "cache-control": "NO-CACHE, PRIVATE"})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"',
                               "cache-control": "NO-CACHE, PRIVATE"})])))
    add(("lc6-other-qualified-directive-not-refused",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"',
                            "cache-control": 'max-age="60"'})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"',
                               "cache-control": 'max-age="60"'})])))
    add(("invalid-json", "{not json", "refuse", None))
    add(("input-not-an-object", [], "refuse", None))
    add(("extra-top-level-key",
         {"stored": [], "response": r304({}), "extra": 1}, "refuse", None))
    add(("missing-response-key", {"stored": []}, "refuse", None))
    add(("status-not-304", {"stored": [],
                            "response": {"status": 200, "headers": {}}},
        "refuse", None))
    add(("status-string", {"stored": [],
                           "response": {"status": "304", "headers": {}}},
        "refuse", None))
    add(("status-bool", {"stored": [],
                         "response": {"status": True, "headers": {}}},
        "refuse", None))
    add(("received-bool", {"stored": [st("a", True, {})],
                           "response": r304({})}, "refuse", None))
    add(("received-float", {"stored": [st("a", 1.5, {})],
                            "response": r304({})}, "refuse", None))
    add(("id-empty", {"stored": [st("", 1, {})], "response": r304({})},
        "refuse", None))
    add(("id-duplicate",
         {"stored": [st("a", 1, {}), st("a", 2, {})], "response": r304({})},
        "refuse", None))
    add(("stored-not-a-list",
         {"stored": "x", "response": r304({})}, "refuse", None))
    add(("stored-element-not-an-object",
         {"stored": [5], "response": r304({})}, "refuse", None))
    add(("stored-extra-key",
         {"stored": [{"id": "a", "received": 1, "headers": {}, "note": "x"}],
          "response": r304({})}, "refuse", None))
    add(("response-extra-key",
         {"stored": [], "response": {"status": 304, "headers": {}, "via": "c"}},
        "refuse", None))
    add(("headers-not-an-object",
         {"stored": [st("a", 1, "h")], "response": r304({})}, "refuse", None))
    add(("headers-case-duplicate-names",
         {"stored": [], "response": r304({"ETag": '"a"', "etag": '"a"'})},
        "refuse", None))
    add(("header-name-not-a-token",
         {"stored": [], "response": r304({"bad name": "1"})}, "refuse", None))
    add(("header-name-contains-newline",
         {"stored": [], "response": r304({"x\ny": "1"})}, "refuse", None))
    add(("header-value-not-a-string",
         {"stored": [], "response": r304({"x": 5})}, "refuse", None))
    add(("header-value-contains-nul",
         {"stored": [], "response": r304({"x": "a\x00b"})}, "refuse", None))
    add(("header-value-contains-cr",
         {"stored": [], "response": r304({"x": "a\rb"})}, "refuse", None))
    add(("etag-lowercase-w-in-304",
         {"stored": [], "response": r304({"etag": 'w/"v"'})}, "refuse", None))
    add(("etag-lowercase-w-in-stored",
         {"stored": [st("a", 1, {"etag": 'w/"v"'})], "response": r304({})},
        "refuse", None))
    add(("etag-list-not-single",
         {"stored": [], "response": r304({"etag": '"a", "b"'})},
        "refuse", None))
    add(("etag-empty-value",
         {"stored": [], "response": r304({"etag": ""})}, "refuse", None))
    add(("etag-missing-quotes",
         {"stored": [], "response": r304({"etag": "v"})}, "refuse", None))
    add(("etag-astral-code-point",
         {"stored": [], "response": r304({"etag": '"\U0001F600"'})},
        "refuse", None))
    add(("v2-1-token-form-qualified-refused",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "cache-control": "private=abc"})},
         "refuse", None))
    add(("v2-1-token-form-no-cache-refused",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "cache-control": "no-cache=1"})},
         "refuse", None))
    add(("v2-1-empty-quoted-qualified-refused",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "cache-control": 'no-cache=""'})},
         "refuse", None))
    add(("v2-1-extension-ends-in-no-cache-ignored",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "cache-control": 'x-no-cache="a"'})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"', "cache-control": 'x-no-cache="a"'})])))
    add(("v2-1-extension-no-cachex-ignored",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "cache-control": "no-cachex=1"})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"', "cache-control": "no-cachex=1"})])))
    add(("v2-1-comma-in-quoted-not-split",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "cache-control": 'max-stale="1,2", no-cache'})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"', "cache-control": 'max-stale="1,2", no-cache'})])))
    add(("v2-1-empty-elements-accepted",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "cache-control": ", max-age=1, ,"})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"', "cache-control": ", max-age=1, ,"})])))
    add(("v2-1-malformed-space-around-eq-refused",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "cache-control": "no-cache = 1"})},
         "refuse", None))
    add(("v2-1-malformed-bare-eq-refused",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "cache-control": "max-age="})},
         "refuse", None))
    add(("v2-1-malformed-unterminated-quote-refused",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "cache-control": 'max-age="60'})},
         "refuse", None))
    add(("v2-1-malformed-bad-chars-refused",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "cache-control": "max-age=6(0)"})},
         "refuse", None))
    add(("v2-1-malformed-trailing-junk-refused",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "cache-control": 'max-age="6"x'})},
         "refuse", None))
    add(("v2-1-caps-token-form-refused",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "cache-control": "PRIVATE=abc"})},
         "refuse", None))
    add(("v2-1-ows-around-commas-ok",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "cache-control": "\tmax-age=1\t,\tno-cache\t"})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"', "cache-control": "max-age=1\t,\tno-cache"})])))
    add(("v2-3-stored-proxy-dropped",
         {"stored": [st("a", 1, {"etag": '"v"', "proxy-authorization": "Basic z",
                                  "proxy-authenticate": "Basic",
                                  "proxy-authentication-info": "i",
                                  "connection": "keep-alive",
                                  "content-length": "99", "x": "1"})],
          "response": r304({"etag": '"v"', "age": "10"})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"', "connection": "keep-alive",
                               "content-length": "99", "x": "1", "age": "10"})])))
    add(("e2-malformed-etag-unselected-stored-refused",
         {"stored": [st("a", 1, {"etag": "bad"}), st("b", 2, {"etag": '"v"'})],
          "response": r304({"etag": '"v"'})}, "refuse", None))
    add(("e3-lm-tab-trim",
         {"stored": [st("a", 1, {"last-modified": "\tL\t"})],
          "response": r304({"last-modified": "L"})},
         "out", out("update", "weak", [upd("a", {"last-modified": "L"})])))
    add(("e5-non-utf8-refused", b"\xff\xfe", "refuse", None))
    add(("e6-age-copied",
         {"stored": [st("a", 1, {"etag": '"v"'})],
          "response": r304({"etag": '"v"', "age": "42"})},
         "out", out("update", "strong",
                    [upd("a", {"etag": '"v"', "age": "42"})])))
    add(("e7-lm-tie-refused",
         {"stored": [st("p", 3, {"last-modified": "L"}),
                     st("q", 3, {"last-modified": "L"})],
          "response": r304({"last-modified": "L"})}, "refuse", None))
    add(("e7-etag-plus-lm-tie-refused",
         {"stored": [st("p", 3, {"etag": '"v"', "last-modified": "L"}),
                     st("q", 3, {"etag": '"v"', "last-modified": "L"})],
          "response": r304({"etag": 'W/"v"', "last-modified": "L"})},
         "refuse", None))
    return cases


def _run_selftest():
    cases = _selftest_cases()
    total = len(cases)
    failures = []
    for tag, payload, kind, expected in cases:
        raw = payload if isinstance(payload, (str, bytes)) else json.dumps(payload)
        try:
            result = process(raw)
        except Refusal:
            if kind != "refuse":
                failures.append(tag + ": unexpected refusal")
            continue
        if kind == "refuse":
            failures.append(tag + ": expected refusal, got " + repr(result))
        elif result != expected:
            failures.append(tag + ": got " + repr(result) +
                            ", want " + repr(expected))
    print("selftest %d/%d" % (total - len(failures), total))
    if failures:
        for line in failures:
            print(line, file=sys.stderr)
        return 1
    return 0


def main(argv):
    if "--selftest" in argv:
        return _run_selftest()
    raw = sys.stdin.buffer.read()
    try:
        result = process(raw)
    except Refusal as refusal:
        sys.stderr.write("invalid_input: " + str(refusal) + "\n")
        return 1
    sys.stdout.write(json.dumps(result) + "\n")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
