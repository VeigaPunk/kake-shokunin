#!/usr/bin/env python3
"""Round-100 C2 counter: 304 freshening contract v2 (.ufo/waves/round-100/fresh304-contract-v2.md).

Scores candidate scripts/freshen_304.py read from COMMITTED bytes at --revision
(git show), or a --candidate-file (controls only). Each case runs the candidate
once inside a bwrap sandbox (new user/PID/net/IPC/UTS namespaces, read-only /usr,
private /tmp and /proc, empty env except PATH/LANG/HOME, only the candidate file
bound in at /cand/freshen_304.py, cwd /tmp), stdin = the case bytes, timeout 10 s.
If the sandbox cannot start, the counter exits 2 and scores nothing.

A case passes when:
  expected decision -> exit 0; stdout = S or S + "\\n" where S has no leading or
                       trailing whitespace and json.loads(S) equals the expected
                       object (dict key order ignored; list order scored);
  expected refusal  -> exit 1; stdout is EMPTY (zero bytes); stderr starts with
                       `invalid_input:`.

Populations:
  hand      the HAND list below (written from contract v2, each tagged with the
            clause it decides; RAW entries are sent as raw bytes); the reference
            must agree with every hand expectation before any candidate runs
            (exit 2 on drift);
  generated N cases (default 300) from a grammar seeded by --seed or, by default,
            by int(first 8 hex of the scored revision id, 16).

Output line:
  candidate=<absent|present> sha256=<hex> hand=a/b generated=c/d refusals=e/f seed=S met=<bool>
met=true iff candidate present and every hand and generated case passes.
Exit 0 met; 1 not met or candidate absent; 2 could-not-evaluate / usage / drift / no sandbox.
"""
import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

CANDIDATE = "scripts/freshen_304.py"

# --- REF BEGIN
import re

TCHAR = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")
TOKEN = re.compile(r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+")
HOP = {"keep-alive", "proxy-connection", "te", "transfer-encoding", "upgrade"}
PROXY = {"proxy-authenticate", "proxy-authentication-info", "proxy-authorization"}
OWS = " \t"


class Refuse(Exception):
    pass


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _headers(h):
    if not isinstance(h, dict):
        raise Refuse("headers not an object")
    out = {}
    for k, v in h.items():
        if not isinstance(k, str) or not TCHAR.match(k):
            raise Refuse("invalid header name")
        lk = k.lower()
        if lk in out:
            raise Refuse("case-duplicate header name")
        if not isinstance(v, str):
            raise Refuse("non-string header value")
        if any(c in v for c in "\r\n\x00"):
            raise Refuse("CR/LF/NUL in value")
        out[lk] = v
    return out


def _etag(v):
    """Return (weak, opaque) or raise."""
    s = v.strip(OWS)
    weak = False
    if s.startswith("W/"):
        weak = True
        s = s[2:]
    if len(s) < 2 or s[0] != '"' or s[-1] != '"':
        raise Refuse("malformed etag")
    op = s[1:-1]
    for ch in op:
        o = ord(ch)
        if not (o == 0x21 or 0x23 <= o <= 0x7E or 0x80 <= o <= 0xFF):
            raise Refuse("malformed etag")
    return weak, op


def _qdtext(o):
    return o in (0x09, 0x20, 0x21) or 0x23 <= o <= 0x5B or 0x5D <= o <= 0x7E or 0x80 <= o <= 0xFF


def _qpair(o):
    return o in (0x09, 0x20) or 0x21 <= o <= 0x7E or 0x80 <= o <= 0xFF


def _cc_directives(v):
    """Parse a Cache-Control value (RFC 9111 5.2 with RFC 9110 5.6.1.2 empty
    elements). Return [(lowercase name, has_argument)] or raise."""
    i, n, out = 0, len(v), []

    def ows(i):
        while i < n and v[i] in OWS:
            i += 1
        return i

    i = ows(i)
    while True:
        if i < n and v[i] != ",":
            m = TOKEN.match(v, i)
            if not m:
                raise Refuse("malformed cache-control")
            name = m.group(0).lower()
            i = m.end()
            has_arg = False
            if i < n and v[i] == "=":
                has_arg = True
                i += 1
                if i < n and v[i] == '"':
                    i += 1
                    while True:
                        if i >= n:
                            raise Refuse("malformed cache-control")
                        o = ord(v[i])
                        if v[i] == '"':
                            i += 1
                            break
                        if v[i] == "\\":
                            if i + 1 >= n or not _qpair(ord(v[i + 1])):
                                raise Refuse("malformed cache-control")
                            i += 2
                            continue
                        if not _qdtext(o):
                            raise Refuse("malformed cache-control")
                        i += 1
                else:
                    m = TOKEN.match(v, i)
                    if not m:
                        raise Refuse("malformed cache-control")
                    i = m.end()
            out.append((name, has_arg))
        i = ows(i)
        if i >= n:
            return out
        if v[i] != ",":
            raise Refuse("malformed cache-control")
        i = ows(i + 1)


def reference(inp):
    if not isinstance(inp, dict) or set(inp) != {"stored", "response"}:
        raise Refuse("top-level keys")
    resp = inp["response"]
    if not isinstance(resp, dict) or set(resp) != {"status", "headers"}:
        raise Refuse("response keys")
    if not _is_int(resp["status"]) or resp["status"] != 304:
        raise Refuse("status not 304")
    rh = _headers(resp["headers"])
    stored = inp["stored"]
    if not isinstance(stored, list):
        raise Refuse("stored not a list")
    ids = set()
    norm = []
    for el in stored:
        if not isinstance(el, dict) or set(el) != {"id", "received", "headers"}:
            raise Refuse("stored element keys")
        if not isinstance(el["id"], str) or el["id"] == "" or el["id"] in ids:
            raise Refuse("bad id")
        ids.add(el["id"])
        if not _is_int(el["received"]):
            raise Refuse("received not integer")
        sh = _headers(el["headers"])
        et = _etag(sh["etag"]) if "etag" in sh else None
        lm = sh["last-modified"].strip(OWS) if "last-modified" in sh else None
        norm.append((el["id"], el["received"], sh, et, lm))
    ret = _etag(rh["etag"]) if "etag" in rh else None
    rlm = rh["last-modified"].strip(OWS) if "last-modified" in rh else None
    if "cache-control" in rh:
        for name, has_arg in _cc_directives(rh["cache-control"]):
            if has_arg and name in ("no-cache", "private"):
                raise Refuse("qualified cache-control outside contract")
    if ret is not None and not ret[0]:
        rule = "strong"
        sel = [x for x in norm if x[3] is not None and not x[3][0] and x[3][1] == ret[1]]
        dec_none = "must-not-update"
    elif ret is not None or rlm is not None:
        rule = "weak"
        corr = []
        for x in norm:
            ok = True
            if ret is not None:
                ok = ok and x[3] is not None and x[3][1] == ret[1]
            if rlm is not None:
                ok = ok and x[4] is not None and x[4] == rlm
            if ok:
                corr.append(x)
        sel = []
        if corr:
            top = max(x[1] for x in corr)
            best = [x for x in corr if x[1] == top]
            if len(best) > 1:
                raise Refuse("ambiguous most recent")
            sel = best
        dec_none = "no-update"
    else:
        rule = "no-validator"
        sel = [norm[0]] if len(norm) == 1 and norm[0][3] is None and norm[0][4] is None else []
        dec_none = "no-update"
    excl = {"content-length", "connection"} | HOP | PROXY
    if "connection" in rh:
        for mem in rh["connection"].split(","):
            mem = mem.strip(OWS).lower()
            if mem:
                excl.add(mem)
    upd = []
    for x in sel:
        h = {k: v for k, v in x[2].items() if k not in PROXY}
        for k, v in rh.items():
            if k not in excl:
                h[k] = v
        upd.append({"id": x[0], "headers": {k: v.strip(OWS) for k, v in h.items()}})
    return {"decision": "update" if upd else dec_none, "rule": rule, "updated": upd}


def decide_bytes(data):
    """Whole-program semantics on raw stdin bytes: object or Refuse."""
    try:
        inp = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError, RecursionError):
        raise Refuse("invalid json")
    return reference(inp)
# --- REF END


class RAW(bytes):
    """A hand input sent as these exact bytes."""


def case_bytes(inp):
    return bytes(inp) if isinstance(inp, RAW) else json.dumps(inp).encode()


def ref_or_refusal(inp):
    try:
        return decide_bytes(case_bytes(inp))
    except Refuse:
        return None


def S(i, rec, **h):
    return {"id": i, "received": rec, "headers": {k.replace("_", "-"): v for k, v in h.items()}}


def R(**h):
    return {"status": 304, "headers": {k.replace("_", "-"): v for k, v in h.items()}}


def U(i, **h):
    return {"id": i, "headers": {k.replace("_", "-").lower(): v for k, v in h.items()}}


def CC(cc, out_cc=None):
    """A 304 with this Cache-Control over one validator-less stored response."""
    inp = {"stored": [S("a", 1)], "response": R(Cache_Control=cc)}
    if out_cc is None:
        return inp, None
    return inp, {"decision": "update", "rule": "no-validator", "updated": [U("a", cache_control=out_cc)]}


# (tag, input, expected-object or None for refusal)
HAND = [
    # --- v1 cases carried unchanged
    ("strong-1", {"stored": [S("a", 1, ETag='"x"', Cache_Control="max-age=10")], "response": R(ETag='"x"', Cache_Control="max-age=60")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', cache_control="max-age=60")]}),
    ("strong-all-matching", {"stored": [S("a", 1, ETag='"x"'), S("b", 2, ETag='"y"'), S("c", 3, ETag='"x"')], "response": R(ETag='"x"', Expires="E")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', expires="E"), U("c", etag='"x"', expires="E")]}),
    ("strong-none-mustnot", {"stored": [S("a", 1, ETag='"y"')], "response": R(ETag='"x"')},
     {"decision": "must-not-update", "rule": "strong", "updated": []}),
    ("strong-vs-weak-stored", {"stored": [S("a", 1, ETag='W/"x"')], "response": R(ETag='"x"')},
     {"decision": "must-not-update", "rule": "strong", "updated": []}),
    ("strong-ignores-lm", {"stored": [S("a", 1, ETag='"x"', Last_Modified="L1")], "response": R(ETag='"x"', Last_Modified="L2")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', last_modified="L2")]}),
    ("strong-empty-set", {"stored": [], "response": R(ETag='"x"')},
     {"decision": "must-not-update", "rule": "strong", "updated": []}),
    ("strong-case-sensitive", {"stored": [S("a", 1, ETag='"X"')], "response": R(ETag='"x"')},
     {"decision": "must-not-update", "rule": "strong", "updated": []}),
    ("strong-empty-opaque", {"stored": [S("a", 1, ETag='""')], "response": R(ETag='""')},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='""')]}),
    ("weak-etag-most-recent", {"stored": [S("a", 5, ETag='W/"x"'), S("b", 9, ETag='"x"'), S("c", 7, ETag='W/"x"')], "response": R(ETag='W/"x"')},
     {"decision": "update", "rule": "weak", "updated": [U("b", etag='W/"x"')]}),
    ("weak-etag-none", {"stored": [S("a", 5, ETag='W/"y"')], "response": R(ETag='W/"x"')},
     {"decision": "no-update", "rule": "weak", "updated": []}),
    ("weak-lm-only", {"stored": [S("a", 1, Last_Modified="Mon"), S("b", 2, Last_Modified="Tue")], "response": R(Last_Modified="Mon")},
     {"decision": "update", "rule": "weak", "updated": [U("a", last_modified="Mon")]}),
    ("weak-lm-trim", {"stored": [S("a", 1, Last_Modified=" Mon ")], "response": R(Last_Modified="Mon")},
     {"decision": "update", "rule": "weak", "updated": [U("a", last_modified="Mon")]}),
    ("weak-both-need-both", {"stored": [S("a", 3, ETag='W/"x"'), S("b", 2, ETag='W/"x"', Last_Modified="L")], "response": R(ETag='W/"x"', Last_Modified="L")},
     {"decision": "update", "rule": "weak", "updated": [U("b", etag='W/"x"', last_modified="L")]}),
    ("weak-tie-refused", {"stored": [S("a", 4, ETag='W/"x"'), S("b", 4, ETag='W/"x"')], "response": R(ETag='W/"x"')}, None),
    ("weak-tie-below-top-ok", {"stored": [S("a", 4, ETag='W/"x"'), S("b", 4, ETag='W/"x"'), S("c", 6, ETag='W/"x"')], "response": R(ETag='W/"x"')},
     {"decision": "update", "rule": "weak", "updated": [U("c", etag='W/"x"')]}),
    ("weak-lm-stored-lacks", {"stored": [S("a", 1, ETag='"q"')], "response": R(Last_Modified="L")},
     {"decision": "no-update", "rule": "weak", "updated": []}),
    ("weak-negative-received", {"stored": [S("a", -5, Last_Modified="L"), S("b", -9, Last_Modified="L")], "response": R(Last_Modified="L")},
     {"decision": "update", "rule": "weak", "updated": [U("a", last_modified="L")]}),
    ("noval-single", {"stored": [S("a", 1, Cache_Control="max-age=1")], "response": R(Cache_Control="max-age=99")},
     {"decision": "update", "rule": "no-validator", "updated": [U("a", cache_control="max-age=99")]}),
    ("noval-two", {"stored": [S("a", 1), S("b", 2)], "response": R(Expires="E")},
     {"decision": "no-update", "rule": "no-validator", "updated": []}),
    ("noval-stored-has-etag", {"stored": [S("a", 1, ETag='"x"')], "response": R(Expires="E")},
     {"decision": "no-update", "rule": "no-validator", "updated": []}),
    ("noval-stored-has-lm", {"stored": [S("a", 1, Last_Modified="L")], "response": R()},
     {"decision": "no-update", "rule": "no-validator", "updated": []}),
    ("noval-empty", {"stored": [], "response": R()},
     {"decision": "no-update", "rule": "no-validator", "updated": []}),
    ("upd-content-length", {"stored": [S("a", 1, ETag='"x"', Content_Length="10")], "response": R(ETag='"x"', Content_Length="0")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', content_length="10")]}),
    ("upd-connection-listed", {"stored": [S("a", 1, ETag='"x"', X_Foo="old")], "response": R(ETag='"x"', Connection="X-Foo, , close", X_Foo="new", X_Bar="b")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', x_foo="old", x_bar="b")]}),
    ("upd-hop-fixed", {"stored": [S("a", 1, ETag='"x"')], "response": R(ETag='"x"', Keep_Alive="t", TE="x", Transfer_Encoding="chunked", Upgrade="u", Proxy_Connection="p")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"')]}),
    ("upd-proxy-fields", {"stored": [S("a", 1, ETag='"x"')], "response": R(ETag='"x"', Proxy_Authenticate="B", Proxy_Authentication_Info="i", Proxy_Authorization="z", Vary="x")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', vary="x")]}),
    ("upd-case-merge", {"stored": [S("a", 1, ETag='"x"', CACHE_CONTROL="old")], "response": R(ETag='"x"', cache_control="new")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', cache_control="new")]}),
    ("upd-connection-self-case", {"stored": [S("a", 1)], "response": R(CONNECTION="keep-alive", Date="D")},
     {"decision": "update", "rule": "no-validator", "updated": [U("a", date="D")]}),
    ("upd-obs-text-etag", {"stored": [S("a", 1, ETag='"\u00e9"')], "response": R(ETag='"\u00e9"')},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"\u00e9"')]}),
    ("ref-status-200", {"stored": [], "response": {"status": 200, "headers": {}}}, None),
    ("ref-status-bool", {"stored": [], "response": {"status": True, "headers": {}}}, None),
    ("ref-extra-key", {"stored": [], "response": R(), "now": 1}, None),
    ("ref-dup-id", {"stored": [S("a", 1), S("a", 2)], "response": R()}, None),
    ("ref-empty-id", {"stored": [S("", 1)], "response": R()}, None),
    ("ref-received-bool", {"stored": [S("a", True)], "response": R()}, None),
    ("ref-received-float", {"stored": [S("a", 1.0)], "response": R()}, None),
    ("ref-bad-name", {"stored": [], "response": {"status": 304, "headers": {"bad name": "v"}}}, None),
    ("ref-case-dup", {"stored": [], "response": {"status": 304, "headers": {"ETag": '"x"', "etag": '"x"'}}}, None),
    ("ref-crlf", {"stored": [S("a", 1, X="a\r\nb")], "response": R()}, None),
    ("ref-nonstring", {"stored": [], "response": {"status": 304, "headers": {"x": 5}}}, None),
    ("ref-etag-list", {"stored": [], "response": R(ETag='"a", "b"')}, None),
    ("ref-etag-unquoted", {"stored": [S("a", 1, ETag="abc")], "response": R()}, None),
    ("ref-etag-lower-w", {"stored": [], "response": R(ETag='w/"x"')}, None),
    ("ref-etag-dquote-inside", {"stored": [], "response": R(ETag='"a"b"')}, None),
    ("ref-qualified-nocache", {"stored": [S("a", 1)], "response": R(Cache_Control='no-cache="set-cookie"')}, None),
    ("ref-qualified-private", {"stored": [S("a", 1)], "response": R(Cache_Control='max-age=1, PRIVATE="x"')}, None),
    ("ref-stored-not-list", {"stored": {}, "response": R()}, None),
    ("ref-not-object", [], None),
    # --- V2-2 (F2): output values trimmed (v1 strong-trim / upd-value-bytes-kept flipped)
    ("v2-strong-trim", {"stored": [S("a", 1, ETag=' "x" ')], "response": R(ETag='"x"\t')},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"')]}),
    ("v2-upd-value-trimmed", {"stored": [S("a", 1, ETag='"x"')], "response": R(ETag='"x"', X_V="  spaced\tvalue ")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', x_v="spaced\tvalue")]}),
    ("v2-stored-value-trimmed", {"stored": [S("a", 1, X_S="\t s s \t")], "response": R(Date=" D")},
     {"decision": "update", "rule": "no-validator", "updated": [U("a", x_s="s s", date="D")]}),
    ("v2-empty-after-trim", {"stored": [S("a", 1)], "response": R(X_E="   ")},
     {"decision": "update", "rule": "no-validator", "updated": [U("a", x_e="")]}),
    # --- V2-3 (F3): stored proxy-specific fields dropped
    ("v2-stored-proxy-dropped", {"stored": [S("a", 1, ETag='"x"', Proxy_Authorization="z", Proxy_Authenticate="B", PROXY_AUTHENTICATION_INFO="i", X_K="k")], "response": R(ETag='"x"')},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', x_k="k")]}),
    # --- e1: stored connection / hop / content-length fields stay
    ("e1-stored-hop-kept", {"stored": [S("a", 1, Connection="close", Keep_Alive="t", Transfer_Encoding="chunked", Upgrade="u", Content_Length="3")], "response": R(Date="D")},
     {"decision": "update", "rule": "no-validator", "updated": [U("a", connection="close", keep_alive="t", transfer_encoding="chunked", upgrade="u", content_length="3", date="D")]}),
    # --- e2: malformed stored ETag refused even when selection would not read it
    ("e2-stored-bad-etag-lm304", {"stored": [S("a", 1, Last_Modified="L"), S("b", 2, ETag="abc")], "response": R(Last_Modified="L")}, None),
    ("e2-stored-bad-etag-noval", {"stored": [S("a", 1, ETag='W/x')], "response": R(Date="D")}, None),
    # --- e3: LM trimmed of SP and HTAB
    ("e3-lm-tab-trim", {"stored": [S("a", 1, Last_Modified="\tL \t")], "response": R(Last_Modified="L\t")},
     {"decision": "update", "rule": "weak", "updated": [U("a", last_modified="L")]}),
    # --- e5: raw stdin that is not a JSON document
    ("e5-raw-truncated", RAW(b'{"stored": ['), None),
    ("e5-raw-not-utf8", RAW(b'\xff\xfe{}'), None),
    ("e5-raw-empty", RAW(b''), None),
    ("e5-raw-trailing-garbage", RAW(b'{"stored": [], "response": {"status": 304, "headers": {}}} x'), None),
    ("e5-raw-valid-spaced", RAW(b'  {"stored": [], "response": {"status": 304, "headers": {}}}\n\n'),
     {"decision": "no-update", "rule": "no-validator", "updated": []}),
    # --- e6: Age copied like any other field
    ("e6-age-copied", {"stored": [S("a", 1, ETag='"x"', Age="100")], "response": R(ETag='"x"', Age="5")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', age="5")]}),
    # --- e7: tie refused whatever validators the 304 carries
    ("e7-lm-tie", {"stored": [S("a", 4, Last_Modified="L"), S("b", 4, Last_Modified="L")], "response": R(Last_Modified="L")}, None),
    ("e7-both-tie", {"stored": [S("a", 4, ETag='W/"x"', Last_Modified="L"), S("b", 4, ETag='"x"', Last_Modified="L")], "response": R(ETag='W/"x"', Last_Modified="L")}, None),
    # --- V2-1b (F1, LC6 case): qualified forms in either syntax, any case
    ("v2-cc-token-nocache", *CC("no-cache=Set-Cookie")),
    ("v2-cc-token-private", *CC("max-age=0, private=x")),
    ("v2-cc-upper-quoted", *CC('NO-CACHE="x"')),
    ("v2-cc-mixed-private", *CC('Private="g"')),
    ("v2-cc-empty-quoted", *CC('no-cache=""')),
    ("v2-cc-token-upper-nocache", *CC("No-Cache=set-cookie, max-age=1")),
    ("v2-cc-quoted-escape-arg", *CC('private="a\\"b"')),
    # --- V2-1c (F10): unrecognised / unqualified directives ignored
    ("v2-cc-ext-xnocache", *CC('x-no-cache="y"', 'x-no-cache="y"')),
    ("v2-cc-ext-nocachex", *CC("no-cachex=1, max-age=5", "no-cachex=1, max-age=5")),
    ("v2-cc-ext-xprivate-token", *CC("x-private=1", "x-private=1")),
    ("v2-cc-unqualified", *CC("no-cache, private", "no-cache, private")),
    ("v2-cc-unqualified-upper", *CC("NO-CACHE, Private, max-age=0", "NO-CACHE, Private, max-age=0")),
    ("v2-cc-quoted-comma", *CC('x-a="no-cache=1, private=2", max-age=3', 'x-a="no-cache=1, private=2", max-age=3')),
    ("v2-cc-quoted-escape", *CC('x-a="a\\"b, no-cache=1"', 'x-a="a\\"b, no-cache=1"')),
    ("v2-cc-empty-elems", *CC(" , ,max-age=1,", ", ,max-age=1,")),
    ("v2-cc-ows-tab", *CC("max-age=1\t,\tno-store", "max-age=1\t,\tno-store")),
    ("v2-cc-empty-value", *CC("", "")),
    ("v2-cc-obs-text-quoted", *CC('x-a="\u00e9"', 'x-a="\u00e9"')),
    # --- V2-1a: malformed list refused
    ("v2-cc-unterminated", *CC('x="abc')),
    ("v2-cc-space-around-eq", *CC("max-age = 5")),
    ("v2-cc-missing-comma", *CC("max age")),
    ("v2-cc-eq-empty", *CC("private=")),
    ("v2-cc-bad-char", *CC("max-age=1; no-store")),
    ("v2-cc-ctl-in-quoted", *CC('x-a="a\u0001b"')),
    ("v2-cc-lone-backslash", *CC('x-a="ab\\')),
    ("v2-cc-nonascii-token", *CC("max-\u00e9ge=1")),
]


CC_POOL = [
    ("max-age=60", True), ("no-cache", True), ("private", True), ("NO-CACHE, max-age=1", True),
    ('x-no-cache="y"', True), ("no-cachex=1", True), ('x-a="no-cache=1, private=2"', True),
    (" , max-age=1 ,", True), ("max-age=1\t,\tno-store", True), ("", True),
    ('no-cache="set-cookie"', False), ("no-cache=Set-Cookie", False), ('PRIVATE="x"', False),
    ("Private=g", False), ('no-cache=""', False), ("max-age=0, private=x", False),
    ('x="abc', False), ("max-age = 5", False), ("private=", False), ("a b", False),
]


def gen_case(rng):
    pool_tags = ['"a"', '"b"', 'W/"a"', 'W/"b"', '""', '"\u00e9"', ' "a"\t']
    lms = ["L1", "L2", " L1", "L1\t", "\tL2 "]
    vals = ["v", " v", "v ", "\tv w\t", ""]
    bad = rng.random() < 0.12
    n = rng.randint(0, 4)
    stored = []
    for k in range(n):
        h = {}
        if rng.random() < 0.6:
            h["ETag" if rng.random() < 0.5 else "etag"] = rng.choice(pool_tags)
        if rng.random() < 0.45:
            h["Last-Modified"] = rng.choice(lms)
        if rng.random() < 0.4:
            h["Content-Length"] = str(rng.randint(0, 99))
        if rng.random() < 0.4:
            h["Cache-Control"] = "max-age=%d" % rng.randint(0, 9)
        if rng.random() < 0.3:
            h["X-Foo"] = rng.choice(vals) + "s%d" % k
        if rng.random() < 0.15:
            h[rng.choice(["Proxy-Authorization", "proxy-authenticate", "Proxy-Authentication-Info"])] = "p"
        if rng.random() < 0.15:
            h[rng.choice(["Keep-Alive", "Connection", "Upgrade"])] = "h"
        stored.append({"id": "s%d" % k, "received": rng.randint(-2, 3), "headers": h})
    rh = {}
    if rng.random() < 0.65:
        rh["ETag"] = rng.choice(pool_tags)
    if rng.random() < 0.45:
        rh["last-modified"] = rng.choice(lms)
    for name in ["Content-Length", "X-Foo", "Keep-Alive", "Transfer-Encoding", "Age",
                 "Proxy-Authenticate", "Expires", "Upgrade", "TE"]:
        if rng.random() < 0.22:
            rh[name] = rng.choice(vals) + "r%d" % rng.randint(0, 9)
    if rng.random() < 0.4:
        rh[rng.choice(["Cache-Control", "cache-control", "CACHE-CONTROL"])] = rng.choice(CC_POOL)[0]
    if rng.random() < 0.2:
        rh["Connection"] = rng.choice(["X-Foo", "close", "expires, ,x-foo", "Age"])
    inp = {"stored": stored, "response": {"status": 304, "headers": rh}}
    if bad:
        kind = rng.randint(0, 5)
        if kind == 0:
            inp["response"]["status"] = rng.choice([200, 412, "304"])
        elif kind == 1:
            inp["response"]["headers"].pop("etag", None)
            inp["response"]["headers"]["ETag"] = rng.choice(['x', '"a', 'w/"a"', '"a","b"'])
        elif kind == 2 and stored:
            stored[0]["received"] = rng.choice([1.5, True, "1"])
        elif kind == 3 and stored:
            stored[-1]["headers"]["ETag"] = rng.choice(["abc", 'W/x', '"a'])
            stored[-1]["headers"].pop("etag", None)
        elif kind == 4:
            inp["response"]["headers"]["X-Bad"] = "a\nb"
        else:
            inp["extra"] = 1
    return inp


SANDBOX = ["bwrap", "--unshare-all", "--die-with-parent", "--new-session",
           "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib64", "/lib64",
           "--symlink", "usr/bin", "/bin", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
           "--chdir", "/tmp", "--clearenv", "--setenv", "PATH", "/usr/bin", "--setenv", "LANG", "C.UTF-8",
           "--setenv", "HOME", "/tmp"]


def run_candidate(path, data):
    argv = SANDBOX + ["--ro-bind", path, "/cand/freshen_304.py", "/usr/bin/python3", "-I", "-B", "/cand/freshen_304.py"]
    try:
        r = subprocess.run(argv, input=data, capture_output=True, timeout=10, env={"PATH": "/usr/bin:/bin"})
        return (r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace"))
    except subprocess.TimeoutExpired:
        return (124, "", "")
    except OSError:
        return (127, "", "")


def sandbox_ok(work):
    probe = os.path.join(work, "probe.py")
    open(probe, "w").write("import os,sys\nsys.stdout.write(str(os.getpid()) + ' ' + str(sorted(p for p in os.listdir('/proc') if p.isdigit())))\n")
    rc, out, _ = run_candidate(probe, b"")
    # inside a fresh PID namespace the candidate sees only bwrap's pid 1 and itself
    return rc == 0 and out.startswith("2 ") and out.endswith("['1', '2']")


def judge(expected, res):
    rc, out, err = res
    if expected is None:
        return rc == 1 and out == "" and err.startswith("invalid_input:")
    if rc != 0:
        return False
    s = out[:-1] if out.endswith("\n") else out
    if s != s.strip() or not s:
        return False
    try:
        obj = json.loads(s)
    except ValueError:
        return False
    return obj == expected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--work")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--generated", type=int, default=300)
    ap.add_argument("--candidate-file")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    drift = [t for t, inp, exp in HAND if ref_or_refusal(inp) != exp]
    if drift:
        print("could-not-evaluate: reference drift on %s" % ",".join(drift), file=sys.stderr)
        return 2
    if len(set(t for t, _, _ in HAND)) != len(HAND):
        print("could-not-evaluate: duplicate hand tag", file=sys.stderr)
        return 2
    if a.selftest:
        rng = random.Random(9999)
        kinds = {}
        for _ in range(3000):
            r = ref_or_refusal(gen_case(rng))
            key = "refusal" if r is None else r["decision"] + "/" + r["rule"]
            kinds[key] = kinds.get(key, 0) + 1
        need = {"refusal", "update/strong", "must-not-update/strong", "update/weak", "no-update/weak",
                "update/no-validator", "no-update/no-validator"}
        ok = need.issubset(kinds)
        print("hand=%d/%d reference agrees; generated classes %s" % (len(HAND), len(HAND), json.dumps(kinds, sort_keys=True)))
        print("selftest %d/2" % (1 + ok))
        return 0 if ok else 1
    if not a.work or (not a.revision and not a.candidate_file):
        print("usage: --work <scratch> and --revision <rev> (or --candidate-file) required", file=sys.stderr)
        return 2
    os.makedirs(a.work, exist_ok=True)
    w = tempfile.mkdtemp(dir=a.work, prefix="c100f-")
    try:
        if not sandbox_ok(w):
            print("could-not-evaluate: bwrap sandbox unavailable or not isolated", file=sys.stderr)
            return 2
        rev = None
        if a.revision:
            r = subprocess.run(["git", "-C", a.root, "rev-parse", "--verify", a.revision + "^{commit}"], capture_output=True)
            if r.returncode != 0:
                print("could-not-evaluate: unresolvable revision", file=sys.stderr)
                return 2
            rev = r.stdout.decode().strip()
        if a.candidate_file:
            data = open(a.candidate_file, "rb").read()
        else:
            r = subprocess.run(["git", "-C", a.root, "show", "%s:%s" % (rev, CANDIDATE)], capture_output=True)
            if r.returncode != 0:
                print("revision=%s candidate=absent met=false" % rev)
                return 1
            data = r.stdout
        cand = os.path.join(w, "freshen_304.py")
        open(cand, "wb").write(data)
        os.chmod(cand, 0o444)
        sha = hashlib.sha256(data).hexdigest()
        seed = a.seed if a.seed is not None else (int(rev[:8], 16) if rev else 100100)
        rng = random.Random(seed)
        gen = [gen_case(rng) for _ in range(a.generated)]
        hp = 0
        fails = []
        refusals_total = refusals_ok = 0
        for t, inp, exp in HAND:
            ok = judge(exp, run_candidate(cand, case_bytes(inp)))
            hp += ok
            if exp is None:
                refusals_total += 1
                refusals_ok += ok
            if not ok:
                fails.append("hand:" + t)
        gp = 0
        for i, inp in enumerate(gen):
            exp = ref_or_refusal(inp)
            ok = judge(exp, run_candidate(cand, case_bytes(inp)))
            gp += ok
            if exp is None:
                refusals_total += 1
                refusals_ok += ok
            if not ok:
                fails.append("gen:%d" % i)
        met = hp == len(HAND) and gp == len(gen)
        print("revision=%s candidate=present sha256=%s hand=%d/%d generated=%d/%d refusals=%d/%d seed=%d met=%s"
              % (rev, sha, hp, len(HAND), gp, len(gen), refusals_ok, refusals_total, seed, str(met).lower()))
        for f in fails[:60]:
            print("fail " + f)
        return 0 if met else 1
    finally:
        shutil.rmtree(w, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
