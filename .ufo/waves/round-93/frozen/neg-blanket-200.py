#!/usr/bin/env python3
"""Frozen positive control for round-93 C2: a contract-faithful implementation.

Written independently of `.ufo/waves/round-93/c93_conditional.py` (different code
shape, no shared helpers) so the counter's hand-case set is proven satisfiable by
something other than its own reference. Must be admitted on every case.
"""
import json
import re
import sys

TOKEN = re.compile(r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+\Z")
ETAGC = frozenset("!") | frozenset(chr(c) for c in range(0x23, 0x7F))


class Bad(Exception):
    pass


def split_tag(text):
    weak = False
    if text[:2] == "W/":
        weak = True
        text = text[2:]
    if len(text) < 2 or text[0] != '"' or text[-1] != '"':
        raise Bad("tag")
    body = text[1:-1]
    if any(ch not in ETAGC for ch in body):
        raise Bad("tag")
    return (weak, body)


def split_field(value):
    text = value.strip(" \t")
    if text == "*":
        return "*"
    if text == "":
        raise Bad("empty")
    members = []
    for chunk in text.split(","):
        item = chunk.strip(" \t")
        if item == "":
            raise Bad("empty member")
        if item == "*":
            raise Bad("star mixed")
        members.append(split_tag(item))
    return members


def integer(value, label):
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise Bad(label)
    return value


def decide(payload):
    if not isinstance(payload, dict):
        raise Bad("object")
    if [k for k in payload if k not in ("method", "current", "request", "role")]:
        raise Bad("extra key")
    if "method" not in payload or "current" not in payload or "request" not in payload:
        raise Bad("missing key")
    method = payload["method"]
    if not isinstance(method, str) or not TOKEN.match(method):
        raise Bad("method")
    cur = payload["current"]
    if not isinstance(cur, dict) or sorted(cur) != ["etag", "exists", "last_modified"]:
        raise Bad("current")
    req = payload["request"]
    if not isinstance(req, dict) or sorted(req) != [
            "if_match", "if_modified_since", "if_none_match", "if_unmodified_since"]:
        raise Bad("request")
    exists = cur["exists"]
    if not isinstance(exists, bool):
        raise Bad("exists")
    tag_text = cur["etag"]
    if tag_text is not None and not isinstance(tag_text, str):
        raise Bad("etag")
    stamp = cur["last_modified"]
    if stamp is not None:
        integer(stamp, "last_modified")
    if not exists and (tag_text is not None or stamp is not None):
        raise Bad("absent validator")
    parsed = {}
    for key in ("if_match", "if_none_match", "if_modified_since", "if_unmodified_since"):
        value = req[key]
        if value is None:
            parsed[key] = None
        elif key in ("if_match", "if_none_match"):
            if not isinstance(value, str):
                raise Bad(key)
            parsed[key] = split_field(value)
        else:
            integer(value, key)
            parsed[key] = value
    role = payload.get("role", "origin")
    if role not in ("origin", "cache"):
        raise Bad("role")
    tag = split_tag(tag_text) if tag_text is not None else None

    def hit(spec, compare):
        if spec == "*":
            return exists
        if tag is None or not exists:
            return False
        return any(compare(member, tag) for member in spec)

    def strong(a, b):
        return a[0] is False and b[0] is False and a[1] == b[1]

    def weak(a, b):
        return a[1] == b[1]

    if role == "origin" and parsed["if_match"] is not None:
        if not hit(parsed["if_match"], strong):
            return {"decision": "412", "precondition": "if_match"}
    elif role == "origin" and parsed["if_unmodified_since"] is not None and stamp is not None:
        if stamp > parsed["if_unmodified_since"]:
            return {"decision": "412", "precondition": "if_unmodified_since"}
    if parsed["if_none_match"] is not None:
        if hit(parsed["if_none_match"], weak):
            code = "304" if method in ("GET", "HEAD") else "412"
            return {"decision": code, "precondition": "if_none_match"}
    elif (parsed["if_modified_since"] is not None and method in ("GET", "HEAD")
          and stamp is not None and stamp <= parsed["if_modified_since"]):
        return {"decision": "304", "precondition": "if_modified_since"}
    return {"decision": "200", "precondition": None}


def main():
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
    except ValueError:
        sys.stderr.write("invalid_input: input is not JSON\n")
        return 1
    try:
        decide(payload)
    except Bad as exc:
        sys.stderr.write("invalid_input: %s\n" % exc)
        return 1
    out = {"decision": "200", "precondition": None}
    sys.stdout.write(json.dumps(out) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
