#!/usr/bin/env python3
"""Round-38 C1 delegation control: round-37 base bytes + label hacks.

The whole round-37 base tool (`git show af43a50f:scripts/robots_audit.py`,
sha256 944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5, 591
lines) is embedded below as zlib+base64 and exec'd into a private namespace;
its parser, group selection, rule matching and reporting all run unchanged.
Three label hacks are layered on top, one per round-38 amendment:

* (h) `json.loads` is wrapped: `parse_constant` rejects NaN/Infinity and
  `parse_int` returns a sentinel for literals longer than 1000 digits, so a
  long integer is simply "not an int" and the base's own type checks turn it
  into one check fault for that check (or an input fault for `version`).
  Nothing is converted, so 64 MiB of digits costs a length test.
* (i) `parse_http_url` is wrapped: a string URL holding an ASCII character
  outside the letters/digits/-._~/reserved/percent set returns None, which the
  base already reports as `check_invalid` for that check only.
* (k) `path_to_match` is wrapped to return the normalized path, so the base's
  own `path == "/robots.txt"` sentence fires on "/robots%2Etxt" and
  "/%72obots.txt", and does not fire on a query, another case, or "%2F".

Usage: python3 ctl_delegate_ceiling.py --manifest PATH
"""
from __future__ import annotations

import base64
import hashlib
import json
import sys
import zlib

BASE_SHA256 = "944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5"

BASE_B64 = (
    "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"
    "P5zm0pIgg0zN4AJQ/y+IyiP2"
)

_SOURCE = zlib.decompress(base64.b64decode(BASE_B64)).decode("utf-8")
assert hashlib.sha256(_SOURCE.encode("utf-8")).hexdigest() == BASE_SHA256, "base bytes changed"
NS = {"__name__": "round37_base_robots_audit"}
exec(compile(_SOURCE, "<base-af43a50f>", "exec"), NS)

_ORIG_LOADS = json.loads
_ORIG_PARSE_URL = NS["parse_http_url"]
_ORIG_PATH = NS["path_to_match"]
_NORMALIZE = NS["normalize"]

_URL_ASCII_OK = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    "-._~" ":/?#[]@!$&'()*+,;=%"
)


class _Long:
    __slots__ = ()


_LONG = _Long()


def _reject(name):
    raise ValueError("non-JSON constant " + name)


def _int_hook(text):
    return int(text) if len(text) <= 1000 else _LONG


def _loads(text, *args, **kwargs):
    kwargs.setdefault("parse_int", _int_hook)
    kwargs.setdefault("parse_constant", _reject)
    return _ORIG_LOADS(text, *args, **kwargs)


def parse_http_url(value):
    if isinstance(value, str):
        for char in value:
            if ord(char) < 128 and char not in _URL_ASCII_OK:
                return None
    return _ORIG_PARSE_URL(value)


def path_to_match(parts):
    return _NORMALIZE(_ORIG_PATH(parts))


json.loads = _loads
NS["parse_http_url"] = parse_http_url
NS["path_to_match"] = path_to_match

if __name__ == "__main__":
    raise SystemExit(NS["main"](sys.argv[1:]))
