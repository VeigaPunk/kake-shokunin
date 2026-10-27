#!/usr/bin/env python3
"""Offline response-header expectation audit (`scripts/header_audit.py`).

Round-61 claim C2 (operability): reads a version-1 manifest of *recorded*
responses plus declared expectations and reports, read-only and network-free,
every check whose recorded headers violate an expectation class.

Rule of record: `.ufo/waves/round-61/contract.md` § Claim C2. Retained sources:
S430 (RFC 6797, HSTS), S431 (W3C CSP Level 3), S432 (WHATWG Fetch / nosniff),
S433 (RFC 9110 § 8.3 Content-Type and field-line semantics).

Usage:
    python3 -B scripts/header_audit.py --manifest PATH [--root DIR] [--json]
    python3 -B scripts/header_audit.py --selftest

Text output (the contract's shape): one finding per line

    <check-id> <class> <detail>

then exactly one summary line

    checks=<n> findings=<k>

`--json` replaces the text lines with one JSON document (verdict, per-check
status, findings, and both counts). `--selftest` builds its fixtures in a
temporary directory and asserts the case table below; it writes nothing else
and touches no network.

Exit codes: 0 clean, 1 findings (a check that could not be evaluated is a
finding of class `could_not_evaluate`), 2 manifest fault (unreadable, not JSON,
`version != 1`, `checks` not an array — i.e. no check is enumerable), 64 usage.

Manifest v1 (frozen shape):
    {"version": 1, "checks": [{"id", "source", "url", "https",
      "expect": {"content_type_present", "hsts_present",
                 "xcto_nosniff_value", "csp_present",
                 "singleton_fields": [names]}}]}

Expectation classes, exactly the four frozen ones plus the recorded-header
syntax class and the per-check evaluation class:
    content_type_present  a 2xx recorded response with no `Content-Type` field
    hsts_present          `https: true` + `expect.hsts_present: true` and no
                          `Strict-Transport-Security` field
    xcto_nosniff_value    a recorded `X-Content-Type-Options` field whose
                          trimmed value is not `nosniff` (ASCII case-folded)
    csp_present           `expect.csp_present: true` and no
                          `Content-Security-Policy` field
    singleton_fields      a name in `singleton_fields` recorded more than once
                          (case-insensitively); `Set-Cookie` is never a
                          singleton
    field_name_syntax     a recorded header name that is not an RFC 9110 token
    could_not_evaluate    this check could not be read (see below)

Header names match case-insensitively; values compare after trimming OWS
(SP/HTAB). The tool never fetches, never writes, never spawns a subprocess and
reads no environment variable. Python standard library only.

Lane readings where the contract leaves a point open
---------------------------------------------------
* `expect` flags gate their class; an absent flag is `false` (the contract's
  H16 case: "every expectation declared false/absent" is clean). `https`
  absent is treated as `false`, which can only relax the HSTS class.
* A check fault — source receipt missing or unreadable, receipt not JSON,
  recorded status not parseable, `expect` not an object, or an unusable
  `headers` value — yields one `could_not_evaluate` line for that check and
  nothing else for it: a check that cannot be read is neither cleaned nor
  failed. Such a check makes the run non-clean (exit 1), never exit 2; exit 2
  is reserved for a manifest fault, where no check is enumerable at all.
* `findings=` counts every emitted line, including `could_not_evaluate`; the
  JSON report splits `policyFindings` from `unevaluableChecks` so a reader that
  wants "0 policy findings" can say so exactly.
* `source` is resolved by trying, in order: an absolute path as written, the
  `--root` directory, the nearest enclosing directory holding `.git`/`.jj`
  above the manifest (the lane root), each ancestor of the manifest's directory
  from nearest to filesystem root, and the running directory. The first path
  that names an existing regular file wins, so a repo-root-relative `source`
  (the manifest producer's convention) and a manifest-relative `source` both
  resolve, with or without a VCS marker. The receipt may be bare JSON or a
  receipt text file whose first `#`/blank-prefixed lines precede the JSON
  object.
* Recorded response keys are read liberally inside the frozen shape: `status`
  (or `statusCode`/`finalStatus`/`httpStatus`/`code`), `headers` (or
  `responseHeaders`/`headerPairs`/`header_pairs`) as `[name, value]` pairs, as
  `{"name","value"}` objects, as `"Name: value"` strings, or as a
  `{name: value}` / `{name: [values]}` object; wrapped one level under
  `response`/`capture`/`recorded`/`snapshot`. Order and duplicates are kept
  for every form except the single-value object form, which cannot carry a
  duplicate without listing values.
* One `singleton_fields` finding is emitted per offending field name, not per
  surplus occurrence; one `xcto_nosniff_value` finding per offending field
  occurrence; one `field_name_syntax` finding per offending field. Within a
  check, findings are ordered content_type_present, hsts_present,
  xcto_nosniff_value, csp_present, singleton_fields, field_name_syntax;
  checks keep manifest order.
* A duplicate `id` in the manifest is reported as written (no de-duplication);
  the tool never invents an id, and a check with no usable `id` is named
  `#<index>` (zero-based) in its `could_not_evaluate` line.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import re
import shutil
import stat
import sys
import tempfile

REPORT_VERSION = 1
MANIFEST_VERSION = 1

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_INPUT = 2
EXIT_USAGE = 64

MAX_MANIFEST_BYTES = 8 * 1024 * 1024
MAX_RECEIPT_BYTES = 8 * 1024 * 1024
READ_CHUNK_BYTES = 65536

CLS_CONTENT_TYPE = "content_type_present"
CLS_HSTS = "hsts_present"
CLS_XCTO = "xcto_nosniff_value"
CLS_CSP = "csp_present"
CLS_SINGLETON = "singleton_fields"
CLS_FIELD_NAME = "field_name_syntax"
CLS_UNEVALUABLE = "could_not_evaluate"

CLASS_ORDER = (
    CLS_CONTENT_TYPE,
    CLS_HSTS,
    CLS_XCTO,
    CLS_CSP,
    CLS_SINGLETON,
    CLS_FIELD_NAME,
    CLS_UNEVALUABLE,
)

VERDICT_CLEAN = "clean"
VERDICT_FINDINGS = "failed-policy"
VERDICT_UNEVALUABLE = "could-not-evaluate"

CONTENT_TYPE = "content-type"
STRICT_TRANSPORT_SECURITY = "strict-transport-security"
XCTO = "x-content-type-options"
CSP = "content-security-policy"
NEVER_SINGLETON = frozenset(("set-cookie",))

STATUS_KEYS = ("status", "statusCode", "finalStatus", "httpStatus", "code")
HEADER_KEYS = ("headers", "responseHeaders", "headerPairs", "header_pairs")
WRAPPER_KEYS = ("response", "capture", "recorded", "snapshot", "receipt")
NAME_KEYS = ("name", "field", "key", "header")
VALUE_KEYS = ("value", "v", "val")
EXPECT_BOOL_KEYS = (
    CLS_CONTENT_TYPE,
    CLS_HSTS,
    CLS_XCTO,
    CLS_CSP,
)

OWS = " \t"

_ASCII_LOWER = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"
)

# RFC 9110 `tchar`: the field-name token alphabet.
_FIELD_NAME_RE = re.compile(r"\A[!#$%&'*+\-.^_`|~0-9A-Za-z]+\Z")


def ascii_lower(text):
    """ASCII-only case folding (header names and the nosniff value)."""
    return text.translate(_ASCII_LOWER)


def trim_ows(text):
    """Trim leading and trailing OWS (SP and HTAB) only."""
    return text.strip(OWS)


# --------------------------------------------------------------------------
# Bounded, non-blocking regular-file reads
# --------------------------------------------------------------------------

def _open_regular(path, flags):
    fd = os.open(path, flags)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise OSError("not a regular file")
    except BaseException:
        os.close(fd)
        raise
    return fd


def _read_fd_bounded(fd, limit):
    chunks = []
    remaining = limit
    while remaining > 0:
        chunk = os.read(fd, min(READ_CHUNK_BYTES, remaining))
        if not chunk:
            break
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def read_bytes_bounded(path, limit):
    """Read at most `limit` bytes from a regular file; None on any failure."""
    try:
        info = os.stat(path)
    except (OSError, ValueError):
        return None
    if not stat.S_ISREG(info.st_mode):
        return None
    if info.st_size > limit:
        return None
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        fd = _open_regular(path, flags)
    except (OSError, ValueError):
        return None
    try:
        return _read_fd_bounded(fd, limit)
    except OSError:
        return None
    finally:
        os.close(fd)


def _reject_json_constant(token):
    raise ValueError("not JSON: %s" % (token,))


# --------------------------------------------------------------------------
# Recorded-response extraction
# --------------------------------------------------------------------------

def _scalar(value):
    """Coerce a recorded scalar to the text the audit compares."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value) if isinstance(value, float) else str(value)
    return json.dumps(value, ensure_ascii=True, sort_keys=True)


def _pairs_from(value):
    """Return [(name, value), ...] preserving order and duplicates, or None."""
    pairs = []
    if isinstance(value, dict):
        for name, item in value.items():
            if isinstance(item, list):
                for one in item:
                    pairs.append((_scalar(name), _scalar(one)))
            else:
                pairs.append((_scalar(name), _scalar(item)))
        return pairs
    if isinstance(value, list):
        for item in value:
            if isinstance(item, (list, tuple)):
                if len(item) != 2:
                    return None
                pairs.append((_scalar(item[0]), _scalar(item[1])))
            elif isinstance(item, dict):
                name = None
                for key in NAME_KEYS:
                    if key in item:
                        name = item[key]
                        break
                if name is None:
                    return None
                found = False
                for key in VALUE_KEYS:
                    if key in item:
                        raw = item[key]
                        found = True
                        if isinstance(raw, list):
                            for one in raw:
                                pairs.append((_scalar(name), _scalar(one)))
                        else:
                            pairs.append((_scalar(name), _scalar(raw)))
                        break
                if not found:
                    pairs.append((_scalar(name), ""))
            elif isinstance(item, str):
                name, sep, rest = item.partition(":")
                if not sep:
                    return None
                pairs.append((name, rest))
            else:
                return None
        return pairs
    return None


def _find_response_object(document, depth=0):
    """Locate the dict that holds the recorded headers/status."""
    if depth > 3:
        return None
    if isinstance(document, dict):
        for key in HEADER_KEYS:
            if key in document:
                return document
        for key in WRAPPER_KEYS:
            if key in document:
                found = _find_response_object(document[key], depth + 1)
                if found is not None:
                    return found
        for value in document.values():
            if isinstance(value, (dict, list)):
                found = _find_response_object(value, depth + 1)
                if found is not None:
                    return found
        for key in STATUS_KEYS:
            if key in document:
                return document
        return None
    if isinstance(document, list):
        for value in document:
            found = _find_response_object(value, depth + 1)
            if found is not None:
                return found
    return None


def parse_status(value):
    """Return an int HTTP status in 100..599, or None when not parseable."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if 100 <= value <= 599 else None
    if isinstance(value, float):
        if value.is_integer() and 100 <= int(value) <= 599:
            return int(value)
        return None
    if isinstance(value, str):
        text = trim_ows(value)
        if text.isdigit() and len(text) <= 3:
            number = int(text)
            return number if 100 <= number <= 599 else None
    return None


def _load_json_document(data):
    """Parse a receipt: bare JSON, or a receipt whose first line is `# ...`."""
    try:
        return json.loads(data.decode("utf-8"), parse_constant=_reject_json_constant)
    except (ValueError, UnicodeDecodeError, RecursionError):
        pass
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    lines = text.splitlines()
    index = 0
    while index < len(lines) and (not lines[index].strip() or lines[index].lstrip().startswith("#")):
        index += 1
    remainder = "\n".join(lines[index:])
    if remainder.strip():
        try:
            return json.loads(remainder, parse_constant=_reject_json_constant)
        except (ValueError, RecursionError):
            pass
    decoder = json.JSONDecoder()
    found = None
    attempts = 0
    for start in range(len(text)):
        if text[start] != "{":
            continue
        attempts += 1
        if attempts > 256:
            break
        try:
            value, _end = decoder.raw_decode(text, start)
        except (ValueError, RecursionError):
            continue
        if isinstance(value, dict):
            found = value
    return found


def load_recorded(path):
    """Return (status, pairs, problem). Exactly one of status/pairs or problem."""
    data = read_bytes_bounded(path, MAX_RECEIPT_BYTES)
    if data is None:
        return None, None, "source-unreadable"
    document = _load_json_document(data)
    if document is None:
        return None, None, "source-not-json"
    recorded = _find_response_object(document)
    if recorded is None:
        return None, None, "source-no-response"
    status = None
    for key in STATUS_KEYS:
        if key in recorded:
            status = parse_status(recorded[key])
            break
    else:
        return None, None, "status-missing"
    if status is None:
        return None, None, "status-unparseable"
    raw_headers = None
    for key in HEADER_KEYS:
        if key in recorded:
            raw_headers = recorded[key]
            break
    if raw_headers is None:
        return None, None, "headers-missing"
    pairs = _pairs_from(raw_headers)
    if pairs is None:
        return None, None, "headers-unusable"
    return status, pairs, None


# --------------------------------------------------------------------------
# Check evaluation
# --------------------------------------------------------------------------

def _clean_field(text, fallback):
    """One-line, ASCII-safe detail text (a finding line is one line)."""
    if not isinstance(text, str) or not text:
        return fallback
    return "".join(ch if 0x20 <= ord(ch) < 0x7F else " " for ch in text)


def discover_root(start):
    """Climb from `start` to the first directory holding `.git` or `.jj`."""
    current = os.path.abspath(start)
    while True:
        for marker in (".git", ".jj"):
            if os.path.exists(os.path.join(current, marker)):
                return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def _source_candidates(source, root, manifest_dir):
    candidates = []
    if os.path.isabs(source):
        candidates.append(source)
    if root is not None:
        candidates.append(os.path.join(root, source))
    discovered = discover_root(manifest_dir)
    if discovered is not None:
        candidates.append(os.path.join(discovered, source))
    current = os.path.abspath(manifest_dir)
    depth = 0
    while depth < 64:
        candidates.append(os.path.join(current, source))
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
        depth += 1
    candidates.append(os.path.join(os.getcwd(), source))
    seen = set()
    ordered = []
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        ordered.append(candidate)
    return ordered


def _first_existing(candidates):
    for candidate in candidates:
        try:
            info = os.stat(candidate)
        except (OSError, ValueError):
            continue
        if stat.S_ISREG(info.st_mode):
            return candidate
    return None


def _check_id(check, index):
    if isinstance(check, dict):
        value = check.get("id")
        if isinstance(value, str) and value.strip():
            return _clean_field(value.strip(), "#%d" % (index,))
    return "#%d" % (index,)


def _finding(check_id, cls, detail):
    return {"check": check_id, "class": cls, "detail": detail}


def evaluate_check(check, index, root, manifest_dir):
    """Return (check id, [findings]) for one manifest entry."""
    check_id = _check_id(check, index)
    if not isinstance(check, dict):
        return check_id, [
            _finding(check_id, CLS_UNEVALUABLE, "check-not-object index=%d" % (index,))
        ]

    source = check.get("source")
    if not isinstance(source, str) or not source.strip():
        return check_id, [
            _finding(check_id, CLS_UNEVALUABLE, "check-invalid field=source")
        ]

    expect = check.get("expect", {})
    if expect is None:
        expect = {}
    if not isinstance(expect, dict):
        return check_id, [
            _finding(check_id, CLS_UNEVALUABLE, "check-invalid field=expect")
        ]

    declared = {}
    for key in EXPECT_BOOL_KEYS:
        declared[key] = expect.get(key) is True

    singletons = expect.get("singleton_fields", [])
    if singletons is None:
        singletons = []
    if not isinstance(singletons, list) or any(
        not isinstance(name, str) for name in singletons
    ):
        return check_id, [
            _finding(check_id, CLS_UNEVALUABLE, "check-invalid field=singleton_fields")
        ]

    path = _first_existing(_source_candidates(source, root, manifest_dir))
    if path is None:
        return check_id, [
            _finding(
                check_id,
                CLS_UNEVALUABLE,
                "source-missing path=%s" % (_clean_field(source, "?"),),
            )
        ]

    status, pairs, problem = load_recorded(path)
    if problem is not None:
        return check_id, [
            _finding(check_id, CLS_UNEVALUABLE, "%s path=%s" % (problem, _clean_field(source, "?")))
        ]

    findings = []
    names = []
    for position, (name, _value) in enumerate(pairs):
        trimmed = trim_ows(name)
        if _FIELD_NAME_RE.match(trimmed) is None:
            findings.append(
                _finding(
                    check_id,
                    CLS_FIELD_NAME,
                    "index=%d name=%s"
                    % (position, json.dumps(_clean_field(name, "?"), ensure_ascii=True)),
                )
            )
        names.append(ascii_lower(trimmed))

    counts = {}
    for name in names:
        counts[name] = counts.get(name, 0) + 1

    if declared[CLS_CONTENT_TYPE] and 200 <= status <= 299:
        if counts.get(CONTENT_TYPE, 0) == 0:
            findings.append(
                _finding(
                    check_id,
                    CLS_CONTENT_TYPE,
                    "status=%d missing=%s" % (status, CONTENT_TYPE),
                )
            )

    if declared[CLS_HSTS] and check.get("https") is True:
        if counts.get(STRICT_TRANSPORT_SECURITY, 0) == 0:
            findings.append(
                _finding(
                    check_id,
                    CLS_HSTS,
                    "https=true missing=%s" % (STRICT_TRANSPORT_SECURITY,),
                )
            )

    if declared[CLS_XCTO]:
        for position, (name, value) in enumerate(pairs):
            if ascii_lower(trim_ows(name)) != XCTO:
                continue
            trimmed_value = trim_ows(value)
            if ascii_lower(trimmed_value) != "nosniff":
                findings.append(
                    _finding(
                        check_id,
                        CLS_XCTO,
                        "index=%d value=%s expected=nosniff"
                        % (position, json.dumps(_clean_field(trimmed_value, ""), ensure_ascii=True)),
                    )
                )

    if declared[CLS_CSP]:
        if counts.get(CSP, 0) == 0:
            findings.append(
                _finding(check_id, CLS_CSP, "missing=%s" % (CSP,))
            )

    for name in singletons:
        folded = ascii_lower(trim_ows(name))
        if not folded or folded in NEVER_SINGLETON:
            continue
        seen = counts.get(folded, 0)
        if seen > 1:
            findings.append(
                _finding(
                    check_id,
                    CLS_SINGLETON,
                    "field=%s count=%d" % (folded, seen),
                )
            )

    findings.sort(key=lambda item: CLASS_ORDER.index(item["class"]))
    return check_id, findings


# --------------------------------------------------------------------------
# Manifest, report, entry point
# --------------------------------------------------------------------------

def load_manifest(path):
    """Return (checks, problem); checks is None when the manifest is unusable."""
    data = read_bytes_bounded(path, MAX_MANIFEST_BYTES)
    if data is None:
        return None, "manifest-unreadable"
    try:
        document = json.loads(data.decode("utf-8"), parse_constant=_reject_json_constant)
    except (ValueError, UnicodeDecodeError, RecursionError):
        return None, "manifest-not-json"
    if not isinstance(document, dict):
        return None, "manifest-not-object"
    version = document.get("version")
    if isinstance(version, bool) or not isinstance(version, int):
        return None, "version-missing"
    if version != MANIFEST_VERSION:
        return None, "version-unsupported"
    checks = document.get("checks")
    if not isinstance(checks, list):
        return None, "checks-not-array"
    return checks, None


def audit_manifest(manifest_path, root=None):
    """Return (report dict, exit code) for one manifest."""
    checks, problem = load_manifest(manifest_path)
    if checks is None:
        fault = [_finding("manifest", CLS_UNEVALUABLE, problem)]
        return {
            "version": REPORT_VERSION,
            "verdict": VERDICT_UNEVALUABLE,
            "problem": problem,
            "checksCount": 0,
            "findingsCount": len(fault),
            "policyFindings": 0,
            "unevaluableChecks": len(fault),
            "items": [],
            "findings": fault,
        }, EXIT_INPUT

    manifest_dir = os.path.dirname(os.path.abspath(manifest_path))
    items = []
    findings = []
    for index, check in enumerate(checks):
        try:
            check_id, check_findings = evaluate_check(check, index, root, manifest_dir)
        except Exception:  # a check fault, never a crash
            check_id = _check_id(check, index)
            check_findings = [
                _finding(check_id, CLS_UNEVALUABLE, "check-error index=%d" % (index,))
            ]
        unevaluable = [item for item in check_findings if item["class"] == CLS_UNEVALUABLE]
        items.append(
            {
                "id": check_id,
                "status": (
                    VERDICT_UNEVALUABLE
                    if unevaluable
                    else (VERDICT_FINDINGS if check_findings else VERDICT_CLEAN)
                ),
                "findings": check_findings,
            }
        )
        findings.extend(check_findings)

    policy = [item for item in findings if item["class"] != CLS_UNEVALUABLE]
    unevaluable_count = sum(1 for item in findings if item["class"] == CLS_UNEVALUABLE)
    if findings:
        verdict, exit_code = VERDICT_FINDINGS, EXIT_FINDINGS
    else:
        verdict, exit_code = VERDICT_CLEAN, EXIT_CLEAN
    return {
        "version": REPORT_VERSION,
        "verdict": verdict,
        "problem": None,
        "checksCount": len(checks),
        "findingsCount": len(findings),
        "policyFindings": len(policy),
        "unevaluableChecks": unevaluable_count,
        "items": items,
        "findings": findings,
    }, exit_code


def render_text(report):
    lines = []
    for item in report["findings"]:
        lines.append("%s %s %s" % (item["check"], item["class"], item["detail"]))
    lines.append(
        "checks=%d findings=%d" % (report["checksCount"], report["findingsCount"])
    )
    return "\n".join(lines) + "\n"


def _emit(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def main(argv):
    manifest = None
    root = None
    json_out = False
    selftest = False
    index = 0
    while index < len(argv):
        argument = argv[index]
        if argument == "--selftest":
            selftest = True
            index += 1
        elif argument == "--json":
            json_out = True
            index += 1
        elif argument in ("--manifest", "--root"):
            if index + 1 >= len(argv):
                return EXIT_USAGE
            value = argv[index + 1]
            if not value:
                return EXIT_USAGE
            if argument == "--manifest":
                manifest = value
            else:
                root = value
            index += 2
        elif argument.startswith("--manifest=") or argument.startswith("--root="):
            name, _sep, value = argument.partition("=")
            if not value:
                return EXIT_USAGE
            if name == "--manifest":
                manifest = value
            else:
                root = value
            index += 1
        elif argument.startswith("-"):
            return EXIT_USAGE
        elif manifest is None and not selftest:
            manifest = argument
            index += 1
        else:
            return EXIT_USAGE

    if selftest:
        if manifest is not None or root is not None or json_out:
            return EXIT_USAGE
        return run_selftest()
    if manifest is None:
        return EXIT_USAGE

    report, exit_code = audit_manifest(manifest, root)
    if json_out:
        _emit(json.dumps(report, ensure_ascii=True, sort_keys=True) + "\n")
    else:
        _emit(render_text(report))
    return exit_code


# --------------------------------------------------------------------------
# Selftest: the contract's H1-H18 table plus manifest, usage and shape cases
# --------------------------------------------------------------------------

def _expect(**overrides):
    declared = {
        CLS_CONTENT_TYPE: False,
        CLS_HSTS: False,
        CLS_XCTO: False,
        CLS_CSP: False,
        "singleton_fields": [],
    }
    declared.update(overrides)
    return declared


def _recorded(status=200, headers=None):
    return {
        "status": status,
        "finalUrl": "https://example.test/",
        "headers": headers if headers is not None else [],
        "bodySha256": "0" * 64,
        "bytes": 0,
        "fetchedAt": "2026-10-27T00:00:00Z",
        "userAgent": "round61",
    }


CLEAN_HEADERS = [
    ["Content-Type", "text/html; charset=utf-8"],
    ["Strict-Transport-Security", "max-age=31536000"],
    ["X-Content-Type-Options", "nosniff"],
    ["Content-Security-Policy", "default-src 'self'"],
]


def _selftest_cases():
    """(name, setup(base) -> manifest path, expected exit, expected classes)."""
    cases = []

    def case(name, expect_exit, classes, builder, manifest=None):
        cases.append((name, builder, expect_exit, classes, manifest))

    def write_receipt(base, name, document):
        path = os.path.join(base, "receipts", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(document, handle)
        return "receipts/" + name

    def simple(name, expect_exit, classes, recorded_document, expect_body, **check_extra):
        def builder(base):
            source = write_receipt(base, "r-%s.json" % (name.lower(),), recorded_document)
            manifest = {
                "version": 1,
                "checks": [
                    {
                        "id": name,
                        "source": source,
                        "url": "https://example.test/",
                        "https": check_extra.pop("https", True),
                        "expect": expect_body,
                    }
                ],
            }
            path = os.path.join(base, "manifest-%s.json" % (name.lower(),))
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(manifest, handle)
            return path

        case(name, expect_exit, classes, builder)

    simple(
        "H1",
        0,
        [],
        _recorded(headers=[list(pair) for pair in CLEAN_HEADERS]),
        _expect(**{CLS_CONTENT_TYPE: True, CLS_HSTS: True, CLS_XCTO: True, CLS_CSP: True}),
    )
    simple(
        "H2",
        1,
        [CLS_CONTENT_TYPE],
        _recorded(headers=[["Strict-Transport-Security", "max-age=60"]]),
        _expect(**{CLS_CONTENT_TYPE: True}),
    )
    simple(
        "H3",
        1,
        [CLS_HSTS],
        _recorded(headers=[["Content-Type", "text/html"]]),
        _expect(**{CLS_HSTS: True}),
    )
    simple(
        "H4",
        0,
        [],
        _recorded(
            headers=[
                ["Strict-Transport-Security", "max-age=31536000; includeSubDomains"]
            ]
        ),
        _expect(**{CLS_HSTS: True}),
    )
    simple(
        "H5",
        0,
        [],
        _recorded(headers=[["X-Content-Type-Options", "nosniff"]]),
        _expect(**{CLS_XCTO: True}),
    )
    simple(
        "H6",
        0,
        [],
        _recorded(headers=[["X-Content-Type-Options", " NOsniff "]]),
        _expect(**{CLS_XCTO: True}),
    )
    simple(
        "H7",
        1,
        [CLS_XCTO],
        _recorded(headers=[["X-Content-Type-Options", "sniff"]]),
        _expect(**{CLS_XCTO: True}),
    )
    simple(
        "H8",
        1,
        [CLS_CSP],
        _recorded(headers=[["Content-Type", "text/html"]]),
        _expect(**{CLS_CSP: True}),
    )
    simple(
        "H9",
        1,
        [CLS_SINGLETON],
        _recorded(
            headers=[
                ["Content-Type", "text/html"],
                ["Content-Type", "text/plain"],
            ]
        ),
        _expect(singleton_fields=["Content-Type"]),
    )
    simple(
        "H10",
        0,
        [],
        _recorded(
            headers=[
                ["Set-Cookie", "a=1"],
                ["Set-Cookie", "b=2"],
            ]
        ),
        _expect(singleton_fields=["Set-Cookie"]),
    )
    simple(
        "H11",
        0,
        [],
        _recorded(status=404, headers=[]),
        _expect(**{CLS_CONTENT_TYPE: True}),
    )
    simple(
        "H12",
        1,
        [CLS_FIELD_NAME],
        _recorded(headers=[["X Bad Name", "v"]]),
        _expect(),
    )
    simple(
        "H16",
        0,
        [],
        _recorded(headers=[list(pair) for pair in CLEAN_HEADERS]),
        _expect(),
    )
    simple(
        "H17",
        0,
        [],
        _recorded(headers=[["X-Content-Type-Options", "  nosniff\t"]]),
        _expect(**{CLS_XCTO: True}),
    )

    # H13: the source receipt is not there.
    def h13(base):
        manifest = {
            "version": 1,
            "checks": [
                {
                    "id": "H13",
                    "source": "receipts/absent.json",
                    "url": "https://example.test/",
                    "https": True,
                    "expect": _expect(**{CLS_CONTENT_TYPE: True}),
                }
            ],
        }
        path = os.path.join(base, "manifest-h13.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle)
        return path

    case("H13", 1, [CLS_UNEVALUABLE], h13)

    # H14: version 2.
    def h14(base):
        manifest = {
            "version": 2,
            "checks": [
                {
                    "id": "H14",
                    "source": "receipts/absent.json",
                    "url": "https://example.test/",
                    "https": True,
                    "expect": _expect(),
                }
            ],
        }
        path = os.path.join(base, "manifest-h14.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle)
        return path

    case("H14", 2, [CLS_UNEVALUABLE], h14)

    # H15: not JSON at all.
    def h15(base):
        path = os.path.join(base, "manifest-h15.json")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("{not json,")
        return path

    case("H15", 2, [CLS_UNEVALUABLE], h15)

    # H18: empty checks array.
    def h18(base):
        path = os.path.join(base, "manifest-h18.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump({"version": 1, "checks": []}, handle)
        return path

    case("H18", 0, [], h18)

    # S1: a receipt whose first line is `# receipt: ...` before the JSON body.
    def s1(base):
        path = os.path.join(base, "receipts", "r-s1.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("# receipt: s1\n")
            json.dump(_recorded(headers=[list(pair) for pair in CLEAN_HEADERS]), handle)
        manifest = {
            "version": 1,
            "checks": [
                {
                    "id": "S1",
                    "source": "receipts/r-s1.json",
                    "url": "https://example.test/",
                    "https": True,
                    "expect": _expect(**{CLS_CONTENT_TYPE: True, CLS_CSP: True}),
                }
            ],
        }
        manifest_path = os.path.join(base, "manifest-s1.json")
        with open(manifest_path, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle)
        return manifest_path

    case("S1", 0, [], s1)

    # S2: object-shaped headers (duplicates as a value list) and a string status.
    def s2(base):
        document = _recorded(status="200", headers=None)
        document["headers"] = {
            "Content-Type": "text/html",
            "X-Content-Type-Options": ["nosniff"],
        }
        source = write_receipt(base, "r-s2.json", document)
        manifest = {
            "version": 1,
            "checks": [
                {
                    "id": "S2",
                    "source": source,
                    "url": "https://example.test/",
                    "https": False,
                    "expect": _expect(**{CLS_CONTENT_TYPE: True, CLS_XCTO: True}),
                }
            ],
        }
        manifest_path = os.path.join(base, "manifest-s2.json")
        with open(manifest_path, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle)
        return manifest_path

    case("S2", 0, [], s2)

    # S3: an undeclared HSTS expectation on an https check is never a finding.
    simple(
        "S3",
        0,
        [],
        _recorded(headers=[["Content-Type", "text/html"]]),
        _expect(),
    )

    # S4: a recorded `headers` value the audit cannot read is unevaluable.
    def s4(base):
        document = _recorded(headers=None)
        document["headers"] = 17
        source = write_receipt(base, "r-s4.json", document)
        manifest = {
            "version": 1,
            "checks": [
                {
                    "id": "S4",
                    "source": source,
                    "url": "https://example.test/",
                    "https": True,
                    "expect": _expect(**{CLS_CONTENT_TYPE: True}),
                }
            ],
        }
        manifest_path = os.path.join(base, "manifest-s4.json")
        with open(manifest_path, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle)
        return manifest_path

    case("S4", 1, [CLS_UNEVALUABLE], s4)

    # S5: a recorded status that is not parseable is unevaluable.
    def s5(base):
        source = write_receipt(
            base, "r-s5.json", _recorded(status="two hundred", headers=[["Content-Type", "text/html"]])
        )
        manifest = {
            "version": 1,
            "checks": [
                {
                    "id": "S5",
                    "source": source,
                    "url": "https://example.test/",
                    "https": True,
                    "expect": _expect(**{CLS_CONTENT_TYPE: True}),
                }
            ],
        }
        manifest_path = os.path.join(base, "manifest-s5.json")
        with open(manifest_path, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle)
        return manifest_path

    case("S5", 1, [CLS_UNEVALUABLE], s5)

    # S6: one clean check and one missing source: findings counted, exit 1.
    def s6(base):
        source = write_receipt(
            base, "r-s6.json", _recorded(headers=[list(pair) for pair in CLEAN_HEADERS])
        )
        manifest = {
            "version": 1,
            "checks": [
                {
                    "id": "S6a",
                    "source": source,
                    "url": "https://example.test/",
                    "https": True,
                    "expect": _expect(**{CLS_CONTENT_TYPE: True}),
                },
                {
                    "id": "S6b",
                    "source": "receipts/absent.json",
                    "url": "https://example.test/",
                    "https": True,
                    "expect": _expect(),
                },
            ],
        }
        manifest_path = os.path.join(base, "manifest-s6.json")
        with open(manifest_path, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle)
        return manifest_path

    case("S6", 1, [CLS_UNEVALUABLE], s6)

    return cases


def run_selftest():
    base = tempfile.mkdtemp(prefix="header-audit-selftest-")
    failures = []
    total = 0
    try:
        for name, builder, expect_exit, expect_classes, _manifest in _selftest_cases():
            total += 1
            case_dir = os.path.join(base, name)
            os.makedirs(case_dir, exist_ok=True)
            try:
                manifest_path = builder(case_dir)
                report, exit_code = audit_manifest(manifest_path)
            except Exception as error:  # a selftest case must never crash the run
                failures.append("%s raised %s" % (name, error))
                continue
            classes = sorted(item["class"] for item in report["findings"])
            wanted = sorted(expect_classes)
            if exit_code != expect_exit or classes != wanted:
                failures.append(
                    "%s exit=%d expected=%d classes=%s expected=%s"
                    % (name, exit_code, expect_exit, classes, wanted)
                )
                continue
            text = render_text(report)
            lines = text.splitlines()
            if lines[-1] != "checks=%d findings=%d" % (
                report["checksCount"],
                report["findingsCount"],
            ):
                failures.append("%s summary line %r" % (name, lines[-1]))
                continue
            if len(lines) - 1 != report["findingsCount"]:
                failures.append("%s finding line count %d" % (name, len(lines) - 1))

        # Usage cases: the CLI contract's 64, run in-process with stdout captured.
        def probe(argv):
            sink = io.StringIO()
            with contextlib.redirect_stdout(sink):
                return main(argv)

        total += 1
        if probe([]) != EXIT_USAGE:
            failures.append("usage-empty exit")
        total += 1
        if probe(["--bogus"]) != EXIT_USAGE:
            failures.append("usage-unknown exit")
        total += 1
        if probe(["--manifest"]) != EXIT_USAGE:
            failures.append("usage-missing-value exit")
        total += 1
        if probe(["--selftest", "--manifest", "x"]) != EXIT_USAGE:
            failures.append("usage-selftest-mixed exit")
        total += 1
        if probe(["--manifest", os.path.join(base, "does-not-exist.json")]) != EXIT_INPUT:
            failures.append("missing-manifest exit")
    finally:
        shutil.rmtree(base, ignore_errors=True)

    if failures:
        for failure in failures:
            _emit("FAIL %s\n" % (failure,))
        _emit("selftest: cases=%d passed=%d failed=%d\n" % (total, total - len(failures), len(failures)))
        return EXIT_FINDINGS
    _emit("selftest: cases=%d passed=%d failed=0\n" % (total, total))
    return EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
