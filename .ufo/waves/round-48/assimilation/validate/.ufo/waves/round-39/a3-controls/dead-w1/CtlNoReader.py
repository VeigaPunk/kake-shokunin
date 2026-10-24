#!/usr/bin/env python3
"""Round-39 C1 control: manifest-only reader ("no-reader").

Shape: reads the manifest, never opens a sitemap file. Every check's result is
decided from manifest strings alone (id / file / sitemapUrl). Rule (a)-(k) of
.ufo/waves/round-39/c1-contract.md are never evaluated: no file is opened, no
bytes are read, no XML is parsed.

Contract sentences honoured: 1 (stdout only, stdlib only, no network), 2
(argv other than `--manifest <path>` -> exit 64, stdout ignored), 3 (manifest
validity -> input_invalid, exit 2), 4 (per-check validity -> check_invalid),
33 (output document shape), 34 (verdict/exit).

Usage: python3 control.py --manifest <path>
"""

import json
import os
import sys
from urllib.parse import urlsplit

EXIT_CLEAN = 0
EXIT_FAILED_POLICY = 1
EXIT_ERROR = 2
EXIT_USAGE = 64

CHECK_ID = "id"
CHECK_FILE = "file"
CHECK_SITEMAP_URL = "sitemapUrl"
CHECK_MEMBERS = (CHECK_ID, CHECK_FILE, CHECK_SITEMAP_URL)


def emit(document, exit_code):
    """Sentence 33: one JSON document on stdout, nothing else."""
    sys.stdout.write(json.dumps(document, separators=(",", ":")) + "\n")
    sys.exit(exit_code)


def input_invalid():
    """Sentence 3: the manifest itself is unusable."""
    emit(
        {
            "version": 1,
            "verdict": "could-not-evaluate",
            "error": "input_invalid",
            "checks": [],
        },
        EXIT_ERROR,
    )


def absolute_http_url(value):
    """Sentence 4: sitemapUrl must be an absolute http/https URL with a host.

    Same decomposition the contract's own rule (h) needs (scheme, host, port),
    so the check is `urlsplit`-based: scheme http/https (case-insensitive) and a
    non-empty host.
    """
    if not isinstance(value, str) or not value:
        return False
    try:
        parts = urlsplit(value)
        host = parts.hostname
    except ValueError:
        return False
    if parts.scheme.lower() not in ("http", "https"):
        return False
    return bool(host)


def relative_file_name(value):
    """Sentence 4: file must be relative and free of '..' path segments."""
    if not isinstance(value, str):
        return False
    if value.startswith("/") or os.path.isabs(value):
        return False
    return ".." not in value.split("/")


def check_is_valid(check, seen_ids):
    """Sentence 4: manifest-only validity of one check."""
    if not isinstance(check, dict):
        return False
    for member in CHECK_MEMBERS:
        if member not in check or not isinstance(check[member], str):
            return False
    identifier = check[CHECK_ID]
    if identifier in seen_ids:
        return False
    if not relative_file_name(check[CHECK_FILE]):
        return False
    if not absolute_http_url(check[CHECK_SITEMAP_URL]):
        return False
    return True


def read_manifest(path):
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError:
        input_invalid()
    try:
        manifest = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        input_invalid()
    if not isinstance(manifest, dict):
        input_invalid()
    version = manifest.get("version")
    if isinstance(version, bool) or not isinstance(version, int) or version != 1:
        input_invalid()
    checks = manifest.get("checks")
    if not isinstance(checks, list) or not checks:
        input_invalid()
    return checks


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        sys.exit(EXIT_USAGE)
    checks = read_manifest(argv[2])

    items = []
    seen_ids = set()
    any_error = False
    for check in checks:
        identifier = check.get(CHECK_ID) if isinstance(check, dict) else None
        if not isinstance(identifier, str):
            identifier = None
        if check_is_valid(check, seen_ids):
            if identifier is not None:
                seen_ids.add(identifier)
            # No sitemap file is opened: the check is reported clean.
            items.append(
                {
                    "id": identifier,
                    "status": "clean",
                    "error": None,
                    "findings": [],
                }
            )
        else:
            any_error = True
            if identifier is not None:
                seen_ids.add(identifier)
            items.append(
                {
                    "id": identifier,
                    "status": "error",
                    "error": "check_invalid",
                    "findings": [],
                }
            )

    verdict = "could-not-evaluate" if any_error else "clean"
    emit(
        {"version": 1, "verdict": verdict, "checks": items},
        EXIT_ERROR if any_error else EXIT_CLEAN,
    )


if __name__ == "__main__":
    main(sys.argv)
