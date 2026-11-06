#!/usr/bin/env python3
"""ExecTwinFresh twin: independent implementation of the round-99 C2 contract.

Sole behavioural source: .ufo/waves/round-99/fresh304-contract.md v1
(sha256 2be46b4d8dcc57539b0a45e2e3b7b57e76cb1c4e570891e8cdea88c5ebbba2a6),
with the retained RFC 9111 body as background. The counter c99_fresh304.py,
frozen/*.py sources and their controls' verdicts were not consulted for
behaviour; frozen/pos-oracle.py is used only as a black-box peer process.

I/O per contract: ONE JSON object on stdin -> ONE JSON object on stdout,
exit 0; refusal -> "invalid_input: <reason>" on stderr, empty stdout, exit 1.
"""
import json
import re
import sys

# RFC 9110 §5.6.2 tchar
TCHAR = frozenset("!#$%&'*+-.^_`|~"
                  "0123456789"
                  "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                  "abcdefghijklmnopqrstuvwxyz")

# ETag after space/tab trim: optional W/, a quote, opaque = zero or more of
# `!` (0x21), `#`-`~` (0x23-0x7e), obs-text (0x80-0xff), then a closing quote.
ETAG_RE = re.compile('^(?:W/)?"([\\x21\\x23-\\x7e\\x80-\\xff]*)"$')

SP_TAB = " \t"

# §3.2 bullet 4 + §3.1 bullets 1/2/4 (LC4 is the lane's fixed reading).
NEVER_COPIED = frozenset([
    "content-length",
    "connection",
    "keep-alive", "proxy-connection", "te", "transfer-encoding", "upgrade",
    "proxy-authenticate", "proxy-authentication-info", "proxy-authorization",
])


def refuse(reason):
    sys.stderr.write("invalid_input: %s\n" % reason)
    raise SystemExit(1)


def is_token(name):
    return bool(name) and all(ord(c) < 128 and c in TCHAR for c in name)


def trim(value):
    return value.strip(SP_TAB)


def parse_etag(value):
    """Return (is_weak, opaque) or None when malformed. Contract: trim first."""
    stripped = trim(value)
    m = ETAG_RE.match(stripped)
    if m is None:
        return None
    return (stripped.startswith("W/"), m.group(1))


def get_ci(headers, lname):
    for name, value in headers.items():
        if name.lower() == lname:
            return value
    return None


def validate_header_map(headers, where):
    if not isinstance(headers, dict):
        refuse("%s headers: not an object" % where)
    seen = set()
    for name, value in headers.items():
        if not is_token(name):
            refuse("%s headers: invalid header name" % where)
        lname = name.lower()
        if lname in seen:
            refuse("%s headers: case-duplicate header name" % where)
        seen.add(lname)
        if not isinstance(value, str):
            refuse("%s headers: non-string value" % where)
        if "\r" in value or "\n" in value or "\x00" in value:
            refuse("%s headers: CR/LF/NUL in value" % where)


def main():
    raw = sys.stdin.buffer.read()
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        refuse("input is not valid JSON")

    if not isinstance(doc, dict):
        refuse("input is not a JSON object")
    if set(doc.keys()) != {"stored", "response"}:
        refuse("top-level keys")

    stored = doc["stored"]
    response = doc["response"]
    if not isinstance(stored, list):
        refuse("stored: not a list")
    if not isinstance(response, dict):
        refuse("response: not an object")
    if set(response.keys()) != {"status", "headers"}:
        refuse("response: keys")
    status = response["status"]
    if type(status) is not int or status != 304:
        refuse("status: not the integer 304")

    headers304 = response["headers"]
    validate_header_map(headers304, "304")

    seen_ids = set()
    for element in stored:
        if not isinstance(element, dict):
            refuse("stored element: not an object")
        if set(element.keys()) != {"id", "received", "headers"}:
            refuse("stored element: keys")
        if not isinstance(element["id"], str) or element["id"] == "":
            refuse("stored id: empty or non-string")
        if element["id"] in seen_ids:
            refuse("stored id: duplicate")
        seen_ids.add(element["id"])
        if type(element["received"]) is not int:
            refuse("stored received: not an integer")
        validate_header_map(element["headers"], "stored")

    # LC6: qualified Cache-Control forms in the 304 are outside the contract.
    cc304 = get_ci(headers304, "cache-control")
    if cc304 is not None and ('no-cache="' in cc304 or 'private="' in cc304):
        refuse("304 Cache-Control: qualified no-cache/private (LC6)")

    # ETag syntax everywhere it appears.
    etag304 = get_ci(headers304, "etag")
    parsed304 = parse_etag(etag304) if etag304 is not None else None
    if etag304 is not None and parsed304 is None:
        refuse("304 ETag: malformed")
    for element in stored:
        sv = get_ci(element["headers"], "etag")
        if sv is not None and parse_etag(sv) is None:
            refuse("stored ETag: malformed")

    # ---- Selection, first match of §4.3.4 (rule decided by the 304 alone).
    strong304 = parsed304[1] if parsed304 is not None and not parsed304[0] else None
    weak304 = parsed304[1] if parsed304 is not None and parsed304[0] else None
    lm304 = get_ci(headers304, "last-modified")

    identified = []
    if strong304 is not None:
        rule = "strong"
        for element in stored:
            sv = get_ci(element["headers"], "etag")
            if sv is None:
                continue
            is_weak, opaque = parse_etag(sv)
            if not is_weak and opaque == strong304:
                identified.append(element)
        decision = "update" if identified else "must-not-update"
    elif weak304 is not None or lm304 is not None:
        rule = "weak"
        corresponding = []
        for element in stored:
            ok = True
            if weak304 is not None:
                sv = get_ci(element["headers"], "etag")
                if sv is None or parse_etag(sv)[1] != weak304:
                    ok = False
            if ok and lm304 is not None:
                sv = get_ci(element["headers"], "last-modified")
                if sv is None or trim(sv) != trim(lm304):
                    ok = False
            if ok:
                corresponding.append(element)
        if not corresponding:
            decision = "no-update"
        else:
            newest = max(e["received"] for e in corresponding)
            winners = [e for e in corresponding if e["received"] == newest]
            if len(winners) > 1:
                refuse("ambiguous most recent (LC3)")
            identified = [winners[0]]
            decision = "update"
    else:
        rule = "no-validator"
        if len(stored) == 1:
            only = stored[0]
            if (get_ci(only["headers"], "etag") is None
                    and get_ci(only["headers"], "last-modified") is None):
                identified = [only]
        decision = "update" if identified else "no-update"

    # ---- Update, §3.2 (LC5: nothing else is excluded).
    connection_names = set()
    conn = get_ci(headers304, "connection")
    if conn is not None:
        for member in conn.split(","):
            member = trim(member)
            if member:
                connection_names.add(member.lower())

    def updated_headers(stored_headers):
        out = {}
        for name, value in stored_headers.items():
            out[name.lower()] = value
        for name, value in headers304.items():
            lname = name.lower()
            if lname in NEVER_COPIED or lname in connection_names:
                continue
            out[lname] = value
        return out

    result = {
        "decision": decision,
        "rule": rule,
        "updated": [
            {"id": element["id"], "headers": updated_headers(element["headers"])}
            for element in identified
        ],
    }
    sys.stdout.write(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
