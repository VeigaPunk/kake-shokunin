#!/usr/bin/env python3
"""CONTROL (no-reader): reads the manifest only, copies the round-41 tool's verdict
shape, and never opens a sitemap file.

Skips: reading every sitemap file, XML parsing, and every entry judgement.
Keeps: the round-41 tool's manifest-level validation (duplicate ids, file value,
sitemapUrl absoluteness), its URL rule and its exact stdout format.

Self-contained: Python 3 standard library only, no sibling imports (the counter
sandbox binds only this one file).
"""

import json
import os
import re
import sys
from urllib.parse import urlsplit

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT = 2
EXIT_USAGE = 64

# verbatim from the round-41 tool (sha256 50287ac6...)
_UNRESERVED = "A-Za-z0-9._~\\-\u0080-\U0010ffff"
_SUB_DELIMS = "!$&'()*+,;="
_PCT = "%[0-9A-Fa-f]{2}"
_PCHAR = "(?:[" + _UNRESERVED + _SUB_DELIMS + ":@]|" + _PCT + ")"
_URI_RE = re.compile(
    "\\A[A-Za-z][A-Za-z0-9+.\\-]*:"
    "//(?:(?:[" + _UNRESERVED + _SUB_DELIMS + ":]|" + _PCT + ")*@)?"
    "(?:\\[[A-Za-z0-9._~:!$&'()*+,;=%\\-]*\\]"
    "|(?:[" + _UNRESERVED + _SUB_DELIMS + "]|" + _PCT + ")+)"
    "(?::[0-9]*)?"
    "(?:/" + _PCHAR + "*)*"
    "(?:\\?(?:" + _PCHAR + "|[/?])*)?"
    "(?:\\#(?:" + _PCHAR + "|[/?])*)?\\Z"
)


def _parse_url(value):
    """Verbatim from the round-41 tool."""
    if _URI_RE.match(value) is None:
        return None
    try:
        parts = urlsplit(value)
        scheme = parts.scheme.lower()
        if scheme not in ("http", "https"):
            return None
        host = parts.hostname
        if not host:
            return None
        port = parts.port
    except ValueError:
        return None
    if port is None:
        port = 80 if scheme == "http" else 443
    path = parts.path or "/"
    return (scheme, host.lower(), port, path)


def _load_manifest(path):
    """Verbatim from the round-41 tool."""
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError:
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    if text[:1] == "\ufeff":
        text = text[1:]

    def _reject_constant(_token):
        raise ValueError("non-JSON constant")

    try:
        document = json.loads(text, parse_constant=_reject_constant)
    except ValueError:
        return None
    if not isinstance(document, dict):
        return None
    version = document.get("version")
    if type(version) is not int or version != 1:
        return None
    checks = document.get("checks")
    if not isinstance(checks, list) or not checks:
        return None
    return checks


def _file_value_invalid(value):
    """Verbatim from the round-41 tool."""
    if value.startswith("/"):
        return True
    return ".." in value.split("/")


def _emit(document):
    sys.stdout.write(json.dumps(document, ensure_ascii=True) + "\n")
    sys.stdout.flush()


def _cannot(doc):
    _emit(doc)
    return EXIT_CANNOT


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return EXIT_USAGE
    checks = _load_manifest(argv[2])
    if checks is None:
        return _cannot({"version": 1, "verdict": "could-not-evaluate",
                        "error": "input_invalid", "checks": []})
    seen_ids = set()
    items = []
    any_error = False
    for raw in checks:
        ident = raw.get("id") if isinstance(raw, dict) else None
        ident_out = ident if isinstance(ident, str) else None
        duplicate = False
        if isinstance(ident, str):
            duplicate = ident in seen_ids
            seen_ids.add(ident)
        file_value = raw.get("file") if isinstance(raw, dict) else None
        url_value = raw.get("sitemapUrl") if isinstance(raw, dict) else None
        if (duplicate
                or not (isinstance(ident, str) and isinstance(file_value, str)
                        and isinstance(url_value, str))
                or _file_value_invalid(file_value)
                or _parse_url(url_value) is None):
            item = {"id": ident_out, "status": "error", "error": "check_invalid", "findings": []}
            any_error = True
        else:
            item = {"id": ident_out, "status": "clean", "error": None, "findings": []}
        items.append(item)
    if any_error:
        verdict, exit_code = "could-not-evaluate", EXIT_CANNOT
    else:
        verdict, exit_code = "clean", EXIT_CLEAN
    _emit({"version": 1, "verdict": verdict, "checks": items})
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
