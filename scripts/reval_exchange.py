#!/usr/bin/env python3
"""Revalidation exchange over supplied values only (contract v1).

Reads one JSON document from stdin, writes one decision object to stdout
(exit 0), or refuses with `invalid_input: <reason>` on stderr (exit 1).
"""

import json
import sys

# ETAGC per RFC 9110 8.8.3: %x21 / %x23-7E / obs-text (%x80-FF).
ETAGC = {chr(0x21)} | {chr(c) for c in range(0x23, 0x7F)} | {
    chr(c) for c in range(0x80, 0x100)
}


class Invalid(Exception):
    pass


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _parse_etag(s):
    weak = s.startswith("W/")
    rest = s[2:] if weak else s
    if len(rest) < 2 or rest[0] != '"' or rest[-1] != '"':
        raise Invalid("malformed entity-tag")
    for ch in rest[1:-1]:
        if ch not in ETAGC:
            raise Invalid("malformed entity-tag")
    return s


def decide(inp):
    if not isinstance(inp, dict):
        raise Invalid("input is not an object")
    if set(inp) != {"stored", "received_status"}:
        raise Invalid("unexpected or missing top-level keys")
    stored = inp["stored"]
    if not isinstance(stored, dict) or set(stored) != {
        "exists",
        "etag",
        "last_modified",
    }:
        raise Invalid("stored is not the declared object")
    exists = stored["exists"]
    if not isinstance(exists, bool):
        raise Invalid("exists is not a bool")
    etag = stored["etag"]
    if etag is not None:
        if not isinstance(etag, str) or not etag:
            raise Invalid("etag is neither null nor a string")
        _parse_etag(etag)
    lm = stored["last_modified"]
    if lm is not None and (not _is_int(lm) or lm < 0):
        raise Invalid("last_modified is neither null nor a non-negative int")
    status = inp["received_status"]
    if status is not None:
        if not _is_int(status):
            raise Invalid("received_status is neither null nor an int")
        if not 100 <= status <= 599:
            raise Invalid("received_status out of 100..599")
        if status < 200:
            raise Invalid("1xx is interim and never a validation response")
    has_validator = etag is not None or lm is not None
    if exists is False and has_validator:
        raise Invalid("absent representation carries a validator")
    if status is not None and not has_validator:
        raise Invalid("validation response without a stored validator")

    if status is None:
        if not has_validator:
            return {
                "decision": "cannot-revalidate",
                "if_none_match": None,
                "if_modified_since": None,
            }
        return {
            "decision": "construct",
            "if_none_match": etag,
            "if_modified_since": lm,
        }
    if status == 304:
        return {
            "decision": "update-stored",
            "if_none_match": None,
            "if_modified_since": None,
        }
    if 500 <= status <= 599:
        return {
            "decision": "may-reuse-stored",
            "if_none_match": None,
            "if_modified_since": None,
        }
    return {
        "decision": "replace-stored",
        "if_none_match": None,
        "if_modified_since": None,
    }


def _no_duplicate_keys(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            raise Invalid("duplicate object key in input document")
        seen.add(k)
    return dict(pairs)


def main():
    raw = sys.stdin.buffer.read()
    try:
        inp = json.loads(
            raw.decode("utf-8"), object_pairs_hook=_no_duplicate_keys
        )
        out = decide(inp)
    except Invalid as exc:
        sys.stderr.write("invalid_input: %s\n" % exc)
        return 1
    except ValueError:
        sys.stderr.write("invalid_input: body is not JSON\n")
        return 1
    except UnicodeDecodeError:
        sys.stderr.write("invalid_input: body is not UTF-8\n")
        return 1
    json.dump(out, sys.stdout, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
