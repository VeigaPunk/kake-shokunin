#!/usr/bin/env python3
"""Offline response-header expectation audit (round-61 C2 contract).

Reads a version-1 manifest of recorded responses plus declared expectations and
reports every check whose recorded headers violate an expectation class. The
tool is offline by construction: it reads the manifest and the response
receipts the manifest names, and nothing else. No network, no writes, no
subprocesses, no environment reads. Python standard library only.

Usage:
    python3 scripts/header_audit.py --manifest PATH [--root DIR]
    python3 scripts/header_audit.py --selftest

Report (stdout): one finding per line

    <check-id> <class> <detail>

then one summary line

    checks=<n> findings=<k>

Findings are printed in manifest order; within a check in the order
content_type_present, hsts_present, xcto_nosniff_value, csp_present,
singleton_fields, field_name_syntax. A check with no finding line is `clean`;
a check with one `could_not_evaluate` line could not be evaluated. `<detail>`
is a single whitespace-free token, so a reader may split a finding line into
exactly three fields.

Exit: 0 every check evaluated clean; 1 at least one finding (policy violation
or could_not_evaluate); 2 manifest fault (manifest unreadable/not a regular
file/not JSON/not an object/version is not 1/checks is not an array) - returned
only when no check is evaluable; 64 usage.

Manifest v1 (frozen shape):
    {"version": 1,
     "checks": [{"id": str, "source": str, "url": str, "https": bool,
                 "expect": {"content_type_present": bool,
                            "hsts_present": bool,
                            "xcto_nosniff_value": bool,
                            "csp_present": bool,
                            "singleton_fields": [str]}}]}

Expectation classes (contract section "Claim C2", each grounded in a round-61
row):
* content_type_present - a recorded 2xx response whose headers carry no
  Content-Type field is a finding (S433, RFC 9110 section 8.3).
* hsts_present - a check declaring `https: true` and `hsts_present: true`
  whose recorded headers carry no Strict-Transport-Security field is a finding
  (S430, RFC 6797: the policy is conveyed in that field).
* xcto_nosniff_value - a recorded X-Content-Type-Options field whose value,
  after trimming OWS and folding case, is not `nosniff` is a finding (S432,
  WHATWG Fetch).
* csp_present - a check declaring `csp_present: true` whose recorded headers
  carry no Content-Security-Policy field is a finding (S431, CSP Level 3).
* singleton_fields - a field name listed in the check's `singleton_fields`
  occurring more than once (case-insensitively) in the recorded headers is a
  finding (S433, RFC 9110 field lines); `Set-Cookie` is never a singleton.
* field_name_syntax - a recorded header name that is not an RFC 9110 token is
  a finding (S433, RFC 9110 field-line syntax). The contract's case table
  (H12) carries this class although its prose lists five; the table governs.

Lane readings where the contract leaves a point open
----------------------------------------------------
* A check yields at most one `could_not_evaluate` finding: the first fault in
  the order id, expect, source, receipt bytes, receipt JSON, receipt object,
  status, headers, https. The class is never combined with policy findings for
  the same check, so a check is exactly one of clean / failed-policy /
  could-not-evaluate.
* `expect` keys that are absent (or false) declare no expectation; keys the
  contract does not name are ignored. `singleton_fields` absent means no
  singleton expectation. A present key of the wrong type (a non-bool flag, a
  non-array singleton list, a non-string singleton name) is `expect_malformed`.
* `https` is taken from the check when it is a bool; otherwise it is derived
  from an `https://` url prefix. It is consulted only for `hsts_present`, so a
  check that does not expect HSTS never needs it. A check with `hsts_present`
  true and no usable https value is `https_unknown`.
* `source` is resolved, in order, against `--root DIR` when given, the
  repository root above the manifest (the nearest enclosing directory holding
  `.git`, so a lane-root-relative capture path works), the manifest's own
  directory, and the current directory; the first existing path wins. An
  absolute source is used as given. A source that exists but cannot be read as
  a regular file under 8 MiB is `unreadable_source`.
* The recorded status may be an integer or a decimal string of exactly three
  digits; anything else, including JSON null (a transport failure) and any
  value outside 100..599, is `status_unparseable`. The receipt keys `status`,
  `statusCode` and `status_code` are accepted in that order.
* Recorded headers may be an array of `[name, value]` pairs (duplicates
  preserved), an array of `{"name", "value"}` objects, or an object mapping a
  name to a string or to an array of strings. Any other shape is
  `headers_malformed`; an absent `headers` key is `headers_absent`.
* Header names are compared exactly after case folding (no OWS trimming, so a
  name with a stray space is also a `field_name_syntax` finding); values are
  compared after trimming spaces and tabs. `--manifest` is read through
  `os.stat`, so a symlink to a regular file counts as a regular file and a
  FIFO or device is a manifest fault instead of a block.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys

MANIFEST_VERSION = 1
MAX_BYTES = 8 * 1024 * 1024
EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_UNEVALUABLE = 2
EXIT_USAGE = 64

STATUS_KEYS = ("status", "statusCode", "status_code")
FLAGS = ("content_type_present", "hsts_present", "xcto_nosniff_value", "csp_present")
NEVER_SINGLETON = frozenset({"set-cookie"})

FIELD_NAME = re.compile(r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+")
VISIBLE = re.compile(r"[\x21-\x7e]+")
STATUS_DIGITS = re.compile(r"[0-9]{3}")
WHITESPACE = re.compile(r"\s+")

USAGE = """usage: header_audit.py --manifest PATH [--root DIR]
       header_audit.py --selftest

Offline response-header expectation audit (round-61 C2 contract).
  --manifest PATH  version-1 manifest of recorded responses
  --root DIR       base directory for check `source` paths (optional)
  --selftest       run the built-in self-test and print a tally
"""


class UsageError(Exception):
    """Malformed argument list: exit 64."""


class Fault(Exception):
    """Manifest-level fault: exit 2."""


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


def parse_cli(argv: list[str]) -> argparse.Namespace:
    parser = Parser(prog="header_audit.py", usage=USAGE, allow_abbrev=False, add_help=False)
    parser.add_argument("--manifest", metavar="PATH")
    parser.add_argument("--root", metavar="DIR")
    parser.add_argument("--selftest", action="store_true")
    if sum(t == "--manifest" or t.startswith("--manifest=") for t in argv) > 1:
        raise UsageError("--manifest given more than once")
    if "--selftest" in argv:
        if len(argv) != 1:
            raise UsageError("--selftest takes no other arguments")
        return parser.parse_args(argv)
    args = parser.parse_args(argv)
    if not args.manifest:
        raise UsageError("--manifest PATH is required")
    if args.root is not None and not os.path.isdir(args.root):
        raise UsageError("--root is not a directory")
    return args


def token(text: str, limit: int = 60) -> str:
    """A single whitespace-free ASCII token for a finding detail."""
    text = WHITESPACE.sub("_", text.strip())
    text = "".join(ch for ch in text if "\x21" <= ch <= "\x7e")
    return text[:limit] if text else "<empty>"


def read_regular(path: str) -> bytes:
    stat_result = os.stat(path)
    if not stat.S_ISREG(stat_result.st_mode):
        raise Fault(f"not a regular file: {path}")
    if stat_result.st_size > MAX_BYTES:
        raise Fault(f"file over {MAX_BYTES} bytes: {path}")
    with open(path, "rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise Fault(f"file over {MAX_BYTES} bytes: {path}")
    return data


def load_manifest(path: str) -> list:
    try:
        raw = read_regular(path)
    except OSError as exc:
        raise Fault(f"cannot read manifest: {exc}") from exc
    try:
        document = json.loads(raw)
    except ValueError as exc:
        raise Fault(f"manifest is not JSON: {exc}") from exc
    if not isinstance(document, dict):
        raise Fault("manifest is not a JSON object")
    version = document.get("version")
    if isinstance(version, bool) or not isinstance(version, int) or version != MANIFEST_VERSION:
        raise Fault(f"manifest version is not {MANIFEST_VERSION}")
    checks = document.get("checks")
    if not isinstance(checks, list):
        raise Fault("manifest checks is not an array")
    return checks


def repo_root(start: str) -> str | None:
    current = os.path.realpath(start)
    while True:
        if os.path.exists(os.path.join(current, ".git")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def find_receipt(source: str, manifest_dir: str, root: str | None) -> str | None:
    if os.path.isabs(source):
        return source if os.path.exists(source) else None
    candidates = []
    if root:
        candidates.append(os.path.join(root, source))
    candidates.append(os.path.join(manifest_dir, source))
    candidates.append(os.path.join(os.getcwd(), source))
    top = repo_root(manifest_dir)
    if top:
        candidates.append(os.path.join(top, source))
    seen: set[str] = set()
    for candidate in candidates:
        candidate = os.path.normpath(candidate)
        if candidate in seen:
            continue
        seen.add(candidate)
        if os.path.exists(candidate):
            return candidate
    return None


def declared_expectations(check: dict) -> tuple[dict | None, str | None]:
    raw = check.get("expect", {})
    if raw is None:
        raw = {}
    if not isinstance(raw, dict):
        return None, "expect_malformed"
    flags: dict[str, object] = {}
    for name in FLAGS:
        value = raw.get(name, False)
        if not isinstance(value, bool):
            return None, "expect_malformed"
        flags[name] = value
    singles = raw.get("singleton_fields", [])
    if not isinstance(singles, list):
        return None, "expect_malformed"
    names = []
    for entry in singles:
        if not isinstance(entry, str) or not VISIBLE.fullmatch(entry):
            return None, "expect_malformed"
        names.append(entry)
    flags["singleton_fields"] = names
    return flags, None


def declared_https(check: dict) -> tuple[bool | None, str | None]:
    raw = check.get("https")
    if raw is None:
        url = check.get("url")
        if isinstance(url, str):
            return url.strip().lower().startswith("https://"), None
        return None, "https_unknown"
    if not isinstance(raw, bool):
        return None, "expect_malformed"
    return raw, None


def recorded_status(receipt: dict) -> tuple[int | None, str | None]:
    for key in STATUS_KEYS:
        if key in receipt:
            raw = receipt[key]
            break
    else:
        return None, "status_absent"
    if isinstance(raw, bool):
        return None, "status_unparseable"
    if isinstance(raw, int):
        value = raw
    elif isinstance(raw, str) and STATUS_DIGITS.fullmatch(raw.strip()):
        value = int(raw.strip())
    else:
        return None, "status_unparseable"
    if not 100 <= value <= 599:
        return None, "status_unparseable"
    return value, None


def recorded_headers(receipt: dict) -> tuple[list[tuple[str, str]] | None, str | None]:
    if "headers" not in receipt:
        return None, "headers_absent"
    raw = receipt["headers"]
    pairs: list[tuple[str, str]] = []
    if isinstance(raw, list):
        for item in raw:
            if (isinstance(item, (list, tuple)) and len(item) == 2
                    and all(isinstance(part, str) for part in item)):
                pairs.append((item[0], item[1]))
            elif (isinstance(item, dict) and isinstance(item.get("name"), str)
                    and isinstance(item.get("value"), str)):
                pairs.append((item["name"], item["value"]))
            else:
                return None, "headers_malformed"
    elif isinstance(raw, dict):
        for name, value in raw.items():
            if not isinstance(name, str):
                return None, "headers_malformed"
            if isinstance(value, str):
                pairs.append((name, value))
            elif isinstance(value, list) and all(isinstance(part, str) for part in value):
                pairs.extend((name, part) for part in value)
            else:
                return None, "headers_malformed"
    else:
        return None, "headers_malformed"
    return pairs, None


def evaluate(flags: dict, https: bool, status: int, headers: list[tuple[str, str]]) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    lowered = [name.lower() for name, _ in headers]
    present = set(lowered)
    if flags["content_type_present"] and 200 <= status <= 299 and "content-type" not in present:
        findings.append(("content_type_present", "missing"))
    if flags["hsts_present"] and https and "strict-transport-security" not in present:
        findings.append(("hsts_present", "missing"))
    if flags["xcto_nosniff_value"]:
        for name, value in headers:
            if name.lower() == "x-content-type-options" and value.strip(" \t").casefold() != "nosniff":
                findings.append(("xcto_nosniff_value", "value=" + token(value)))
    if flags["csp_present"] and "content-security-policy" not in present:
        findings.append(("csp_present", "missing"))
    for declared in flags["singleton_fields"]:
        key = declared.lower()
        if key in NEVER_SINGLETON:
            continue
        if lowered.count(key) > 1:
            findings.append(("singleton_fields", "duplicate:" + token(key)))
    for name, _ in headers:
        if not FIELD_NAME.fullmatch(name):
            findings.append(("field_name_syntax", "name=" + token(name)))
    return findings


def audit_check(check: object, index: int, manifest_dir: str, root: str | None) -> tuple[str, list[tuple[str, str]]]:
    fallback_id = f"check-{index}"
    if not isinstance(check, dict):
        return fallback_id, [("could_not_evaluate", "check_not_object")]
    raw_id = check.get("id")
    if not isinstance(raw_id, str) or not VISIBLE.fullmatch(raw_id):
        return fallback_id, [("could_not_evaluate", "id_invalid")]
    check_id = raw_id
    flags, fault = declared_expectations(check)
    if fault:
        return check_id, [("could_not_evaluate", fault)]
    source = check.get("source")
    if not isinstance(source, str) or not source or "\x00" in source:
        return check_id, [("could_not_evaluate", "source_missing")]
    path = find_receipt(source, manifest_dir, root)
    if path is None:
        return check_id, [("could_not_evaluate", "source_missing")]
    try:
        raw = read_regular(path)
    except (OSError, Fault):
        return check_id, [("could_not_evaluate", "unreadable_source")]
    try:
        receipt = json.loads(raw)
    except ValueError:
        return check_id, [("could_not_evaluate", "source_invalid_json")]
    if not isinstance(receipt, dict):
        return check_id, [("could_not_evaluate", "source_not_object")]
    status, fault = recorded_status(receipt)
    if fault:
        return check_id, [("could_not_evaluate", fault)]
    headers, fault = recorded_headers(receipt)
    if fault:
        return check_id, [("could_not_evaluate", fault)]
    https = False
    if flags["hsts_present"]:
        https, fault = declared_https(check)
        if fault:
            return check_id, [("could_not_evaluate", fault)]
    return check_id, evaluate(flags, bool(https), int(status), headers)


def run(manifest_path: str, root: str | None) -> int:
    try:
        checks = load_manifest(manifest_path)
    except Fault as exc:
        print(f"header_audit.py: {exc}", file=sys.stderr)
        return EXIT_UNEVALUABLE
    manifest_dir = os.path.dirname(os.path.realpath(manifest_path))
    findings: list[tuple[str, str, str]] = []
    for index, check in enumerate(checks, 1):
        check_id, rows = audit_check(check, index, manifest_dir, root)
        findings.extend((check_id, kind, detail) for kind, detail in rows)
    for check_id, kind, detail in findings:
        print(f"{check_id} {kind} {detail}")
    print(f"checks={len(checks)} findings={len(findings)}")
    return EXIT_FINDINGS if findings else EXIT_CLEAN


def selftest() -> int:
    """Black-box self-test: run this file as a subprocess on built fixtures."""
    import copy
    import subprocess
    import tempfile

    passed: list[str] = []
    failures: list[str] = []

    def record(name: str, ok: bool, note: str = "") -> None:
        if ok:
            passed.append(name)
        else:
            failures.append(f"{name}: {note}" if note else name)

    clean_headers = [
        ["Content-Type", "text/html; charset=utf-8"],
        ["Strict-Transport-Security", "max-age=31536000; includeSubDomains"],
        ["X-Content-Type-Options", "nosniff"],
        ["Content-Security-Policy", "default-src 'self'"],
    ]
    all_expect = {
        "content_type_present": True,
        "hsts_present": True,
        "xcto_nosniff_value": True,
        "csp_present": True,
        "singleton_fields": ["content-type", "content-security-policy", "strict-transport-security"],
    }

    def receipt(status=200, headers=None, **extra):
        base = {
            "url": "https://example.test/",
            "finalUrl": "https://example.test/",
            "method": "GET",
            "status": status,
            "headers": copy.deepcopy(clean_headers) if headers is None else headers,
            "headerCount": len(clean_headers) if headers is None else len(headers),
            "contentType": "text/html",
            "bytes": 42,
            "sha256": "0" * 64,
            "truncated": False,
            "fetchedAt": "2026-10-27T00:00:00Z",
            "userAgent": "round61",
            "redirects": [],
            "error": None,
        }
        base.update(extra)
        return base

    def check(**overrides):
        base = {
            "id": "surface-a",
            "source": "response.json",
            "url": "https://example.test/",
            "https": True,
            "expect": copy.deepcopy(all_expect),
        }
        base.update(overrides)
        return base

    def manifest(*checks, version=1):
        return {"version": version, "checks": list(checks)}

    with tempfile.TemporaryDirectory(prefix="header-audit-selftest-") as tmp:
        counter = {"n": 0}

        def fixture(name, receipts, document):
            directory = os.path.join(tmp, f"{counter['n']:02d}-{name}")
            counter["n"] += 1
            os.makedirs(directory, exist_ok=True)
            for relative, payload in receipts.items():
                target = os.path.join(directory, relative)
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with open(target, "w", encoding="utf-8") as handle:
                    if isinstance(payload, str):
                        handle.write(payload)
                    else:
                        json.dump(payload, handle)
            with open(os.path.join(directory, "manifest.json"), "w", encoding="utf-8") as handle:
                if isinstance(document, str):
                    handle.write(document)
                else:
                    json.dump(document, handle)
            return directory

        def audit(directory, *extra):
            command = [sys.executable or "python3", "-B", os.path.abspath(__file__)]
            command += ["--manifest", "manifest.json", *extra]
            proc = subprocess.run(command, cwd=directory, capture_output=True, text=True,
                                  timeout=120)
            lines = proc.stdout.splitlines()
            summary = None
            findings = list(lines)
            if findings:
                match = re.fullmatch(r"checks=(\d+) findings=(\d+)", findings[-1])
                if match:
                    summary = (int(match.group(1)), int(match.group(2)))
                    findings = findings[:-1]
            return proc.returncode, summary, findings, proc.stderr

        def shape(findings):
            fields = []
            for line in findings:
                parts = line.split()
                if len(parts) != 3:
                    return None
                fields.append(tuple(parts))
            return fields

        def classes(findings):
            fields = shape(findings)
            return None if fields is None else [row[1] for row in fields]

        # H1: clean 200 response with every declared expectation satisfied.
        d = fixture("h1-clean", {"response.json": receipt()}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("H1 clean 200 -> exit 0, checks=1 findings=0, no lines",
               code == 0 and summary == (1, 0) and findings == [] and err == "",
               f"code={code} summary={summary} findings={findings} err={err!r}")

        # H2: 200 with no Content-Type.
        headers = [row for row in copy.deepcopy(clean_headers) if row[0] != "Content-Type"]
        d = fixture("h2-no-content-type", {"response.json": receipt(headers=headers)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("H2 200 without Content-Type -> 1 content_type_present, exit 1",
               code == 1 and summary == (1, 1) and classes(findings) == ["content_type_present"]
               and shape(findings)[0][0] == "surface-a",
               f"code={code} findings={findings}")

        # H3: https check expecting HSTS, no Strict-Transport-Security.
        headers = [row for row in copy.deepcopy(clean_headers) if row[0] != "Strict-Transport-Security"]
        d = fixture("h3-no-hsts", {"response.json": receipt(headers=headers)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("H3 https without HSTS -> 1 hsts_present, exit 1",
               code == 1 and summary == (1, 1) and classes(findings) == ["hsts_present"],
               f"code={code} findings={findings}")

        # H4: HSTS with parameters is present.
        headers = copy.deepcopy(clean_headers)
        headers[1][1] = "max-age=31536000; includeSubDomains; preload"
        d = fixture("h4-hsts-params", {"response.json": receipt(headers=headers)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("H4 HSTS with parameters -> clean", code == 0 and summary == (1, 0) and findings == [],
               f"code={code} findings={findings}")

        # H5/H6/H7: the nosniff value class.
        for label, value, want in (("H5 nosniff", "nosniff", 0),
                                   ("H6 NOsniff + OWS", "NOsniff \t", 0),
                                   ("H7 sniff", "sniff", 1)):
            headers = copy.deepcopy(clean_headers)
            for row in headers:
                if row[0] == "X-Content-Type-Options":
                    row[1] = value
            d = fixture(label.split()[0].lower(), {"response.json": receipt(headers=headers)},
                        manifest(check()))
            code, summary, findings, err = audit(d)
            ok = (code == want and summary == (1, want)
                  and classes(findings) == (["xcto_nosniff_value"] if want else []))
            detail_ok = True
            if want and findings:
                detail_ok = shape(findings)[0][2].startswith("value=")
            record(f"{label} -> {'clean' if not want else '1 xcto_nosniff_value'}", ok and detail_ok,
                   f"code={code} findings={findings}")

        # H8: csp_present true, no Content-Security-Policy.
        headers = [row for row in copy.deepcopy(clean_headers) if row[0] != "Content-Security-Policy"]
        d = fixture("h8-no-csp", {"response.json": receipt(headers=headers)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("H8 no CSP -> 1 csp_present", code == 1 and summary == (1, 1)
               and classes(findings) == ["csp_present"], f"code={code} findings={findings}")

        # H9: two Content-Type fields, singleton list includes content-type.
        headers = copy.deepcopy(clean_headers) + [["Content-Type", "text/plain"]]
        d = fixture("h9-dup-content-type", {"response.json": receipt(headers=headers)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("H9 duplicate Content-Type -> 1 singleton_fields",
               code == 1 and summary == (1, 1) and classes(findings) == ["singleton_fields"]
               and shape(findings)[0][2] == "duplicate:content-type",
               f"code={code} findings={findings}")

        # H10: two Set-Cookie fields listed as a singleton: never a singleton.
        headers = copy.deepcopy(clean_headers) + [["Set-Cookie", "a=1"], ["Set-Cookie", "b=2"]]
        singles = copy.deepcopy(all_expect["singleton_fields"]) + ["set-cookie"]
        d = fixture("h10-set-cookie", {"response.json": receipt(headers=headers)},
                    manifest(check(expect=dict(all_expect, singleton_fields=singles))))
        code, summary, findings, err = audit(d)
        record("H10 duplicate Set-Cookie -> clean", code == 0 and summary == (1, 0) and findings == [],
               f"code={code} findings={findings}")

        # H11: 404 with no Content-Type: content_type_present applies to 2xx only.
        headers = [row for row in copy.deepcopy(clean_headers) if row[0] != "Content-Type"]
        d = fixture("h11-404", {"response.json": receipt(status=404, headers=headers)},
                    manifest(check()))
        code, summary, findings, err = audit(d)
        record("H11 404 without Content-Type -> clean", code == 0 and summary == (1, 0) and findings == [],
               f"code={code} findings={findings}")

        # H12: header-name syntax fault.
        headers = copy.deepcopy(clean_headers) + [["X Bad Name", "v"]]
        d = fixture("h12-bad-name", {"response.json": receipt(headers=headers)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("H12 'X Bad Name' -> 1 field_name_syntax",
               code == 1 and summary == (1, 1) and classes(findings) == ["field_name_syntax"]
               and shape(findings)[0][2] == "name=X_Bad_Name",
               f"code={code} findings={findings}")

        # H13: the source receipt is missing -> per-check could_not_evaluate, exit 1.
        d = fixture("h13-missing-source", {}, manifest(check(source="absent.json")))
        code, summary, findings, err = audit(d)
        record("H13 missing receipt -> could_not_evaluate, exit 1",
               code == 1 and summary == (1, 1) and classes(findings) == ["could_not_evaluate"]
               and shape(findings)[0][2] == "source_missing",
               f"code={code} findings={findings}")

        # H14: manifest version other than 1.
        d = fixture("h14-version", {"response.json": receipt()}, manifest(check(), version=2))
        code, summary, findings, err = audit(d)
        record("H14 version 2 -> exit 2, no report", code == 2 and summary is None and findings == []
               and "version" in err, f"code={code} out={findings} err={err!r}")

        # H15: manifest is not JSON.
        d = fixture("h15-bad-json", {"response.json": receipt()}, '{"version": 1, "checks": [')
        code, summary, findings, err = audit(d)
        record("H15 unparseable manifest -> exit 2", code == 2 and summary is None and findings == []
               and "not JSON" in err, f"code={code} err={err!r}")

        # H16: every expectation absent: clean headers, nothing declared.
        d = fixture("h16-no-expect", {"response.json": receipt()},
                    manifest({"id": "s", "source": "response.json"}))
        code, summary, findings, err = audit(d)
        record("H16 no expectations declared -> clean", code == 0 and summary == (1, 0) and findings == [],
               f"code={code} findings={findings}")

        # H17: OWS around a correct value.
        headers = copy.deepcopy(clean_headers)
        for row in headers:
            if row[0] == "X-Content-Type-Options":
                row[1] = "  nosniff\t"
        d = fixture("h17-ows", {"response.json": receipt(headers=headers)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("H17 OWS around nosniff -> clean", code == 0 and summary == (1, 0) and findings == [],
               f"code={code} findings={findings}")

        # H18: empty checks array.
        d = fixture("h18-empty", {}, manifest())
        code, summary, findings, err = audit(d)
        record("H18 empty checks -> checks=0 findings=0, exit 0",
               code == 0 and summary == (0, 0) and findings == [], f"code={code} summary={summary}")

        # Case-insensitive names, dict-shaped headers, object-shaped headers.
        lower = [[name.lower(), value] for name, value in copy.deepcopy(clean_headers)]
        d = fixture("names-lower", {"response.json": receipt(headers=lower)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("lowercase recorded names match expectations",
               code == 0 and summary == (1, 0) and findings == [], f"code={code} findings={findings}")

        object_headers = [{"name": name, "value": value} for name, value in copy.deepcopy(clean_headers)]
        d = fixture("object-headers", {"response.json": receipt(headers=object_headers)},
                    manifest(check()))
        code, summary, findings, err = audit(d)
        record("object-shaped recorded headers are accepted",
               code == 0 and summary == (1, 0) and findings == [], f"code={code} findings={findings}")

        mapping = {
            "Content-Type": ["text/html", "text/plain"],
            "Strict-Transport-Security": "max-age=1",
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'self'",
        }
        d = fixture("mapping-headers", {"response.json": receipt(headers=mapping)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("mapping-shaped headers count array values as repeats",
               code == 1 and summary == (1, 1) and classes(findings) == ["singleton_fields"],
               f"code={code} findings={findings}")

        # https false never triggers the HSTS class; absent https is derived from the url.
        headers = [row for row in copy.deepcopy(clean_headers) if row[0] != "Strict-Transport-Security"]
        d = fixture("https-false", {"response.json": receipt(headers=headers)},
                    manifest(check(https=False)))
        code, summary, findings, err = audit(d)
        record("https false -> no hsts_present finding", code == 0 and summary == (1, 0) and findings == [],
               f"code={code} findings={findings}")

        derived = check(https=None, url="https://example.test/")
        del derived["https"]
        d = fixture("https-derived", {"response.json": receipt(headers=headers)}, manifest(derived))
        code, summary, findings, err = audit(d)
        record("absent https derived from an https url -> hsts finding",
               code == 1 and classes(findings) == ["hsts_present"], f"code={code} findings={findings}")

        unknown = check(url=None)
        del unknown["https"]
        del unknown["url"]
        d = fixture("https-unknown", {"response.json": receipt(headers=headers)}, manifest(unknown))
        code, summary, findings, err = audit(d)
        record("hsts expected with no https and no url -> https_unknown",
               code == 1 and classes(findings) == ["could_not_evaluate"]
               and shape(findings)[0][2] == "https_unknown", f"code={code} findings={findings}")

        # Status parsing.
        d = fixture("status-string", {"response.json": receipt(status="200")}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("status '200' accepted", code == 0 and summary == (1, 0), f"code={code} findings={findings}")

        d = fixture("status-word", {"response.json": receipt(status="twenty")}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("status 'twenty' -> status_unparseable",
               code == 1 and classes(findings) == ["could_not_evaluate"]
               and shape(findings)[0][2] == "status_unparseable", f"code={code} findings={findings}")

        d = fixture("status-null", {"response.json": receipt(status=None)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("null status (transport failure) -> could_not_evaluate",
               code == 1 and classes(findings) == ["could_not_evaluate"], f"code={code} findings={findings}")

        d = fixture("status-absent", {"response.json": {"headers": copy.deepcopy(clean_headers)}},
                    manifest(check()))
        code, summary, findings, err = audit(d)
        record("absent status -> status_absent",
               code == 1 and shape(findings)[0][2] == "status_absent", f"code={code} findings={findings}")

        d = fixture("status-range", {"response.json": receipt(status=999)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("status 999 outside 100..599 -> could_not_evaluate",
               code == 1 and classes(findings) == ["could_not_evaluate"], f"code={code} findings={findings}")

        # Receipt and expectation faults.
        d = fixture("headers-absent", {"response.json": {"status": 200}}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("absent headers -> headers_absent",
               code == 1 and shape(findings)[0][2] == "headers_absent", f"code={code} findings={findings}")

        d = fixture("headers-malformed", {"response.json": {"status": 200, "headers": "Content-Type: x"}},
                    manifest(check()))
        code, summary, findings, err = audit(d)
        record("scalar headers -> headers_malformed",
               code == 1 and shape(findings)[0][2] == "headers_malformed",
               f"code={code} findings={findings}")

        d = fixture("receipt-array", {"response.json": [1, 2, 3]}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("receipt not an object -> source_not_object",
               code == 1 and shape(findings)[0][2] == "source_not_object",
               f"code={code} findings={findings}")

        d = fixture("receipt-text", {"response.json": "not json"}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("receipt not JSON -> source_invalid_json",
               code == 1 and shape(findings)[0][2] == "source_invalid_json",
               f"code={code} findings={findings}")

        d = fixture("expect-list", {"response.json": receipt()}, manifest(check(expect=[])))
        code, summary, findings, err = audit(d)
        record("expect not an object -> expect_malformed",
               code == 1 and shape(findings)[0][2] == "expect_malformed", f"code={code} findings={findings}")

        d = fixture("singles-scalar", {"response.json": receipt()},
                    manifest(check(expect=dict(all_expect, singleton_fields="content-type"))))
        code, summary, findings, err = audit(d)
        record("singleton_fields not an array -> expect_malformed",
               code == 1 and shape(findings)[0][2] == "expect_malformed", f"code={code} findings={findings}")

        d = fixture("flag-string", {"response.json": receipt()},
                    manifest(check(expect=dict(all_expect, csp_present="yes"))))
        code, summary, findings, err = audit(d)
        record("non-bool expectation flag -> expect_malformed",
               code == 1 and shape(findings)[0][2] == "expect_malformed", f"code={code} findings={findings}")

        d = fixture("check-scalar", {"response.json": receipt()}, manifest("not-a-check"))
        code, summary, findings, err = audit(d)
        record("check not an object -> check-1 could_not_evaluate",
               code == 1 and shape(findings)[0][:2] == ("check-1", "could_not_evaluate")
               and shape(findings)[0][2] == "check_not_object", f"code={code} findings={findings}")

        d = fixture("id-space", {"response.json": receipt()}, manifest(check(id="bad id")))
        code, summary, findings, err = audit(d)
        record("id with a space -> check-1 could_not_evaluate",
               code == 1 and shape(findings)[0][:2] == ("check-1", "could_not_evaluate")
               and shape(findings)[0][2] == "id_invalid", f"code={code} findings={findings}")

        # Several checks, mixed outcomes, manifest order.
        headers = [row for row in copy.deepcopy(clean_headers) if row[0] != "Content-Type"]
        d = fixture("multi", {"response.json": receipt(), "bad.json": receipt(headers=headers)},
                    manifest(check(id="first"), check(id="second", source="bad.json"),
                             check(id="third", source="absent.json")))
        code, summary, findings, err = audit(d)
        record("three checks: clean/finding/could_not_evaluate in manifest order",
               code == 1 and summary == (3, 2)
               and [(row[0], row[1]) for row in shape(findings)]
               == [("second", "content_type_present"), ("third", "could_not_evaluate")],
               f"code={code} findings={findings}")

        # Three occurrences of a singleton name: one finding, not one per extra.
        headers = copy.deepcopy(clean_headers) + [["Content-Type", "text/plain"],
                                                  ["content-type", "text/css"]]
        d = fixture("singleton-three", {"response.json": receipt(headers=headers)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("three occurrences of a singleton name -> 1 singleton_fields (case-insensitive)",
               code == 1 and summary == (1, 1) and classes(findings) == ["singleton_fields"],
               f"code={code} findings={findings}")

        # Several singleton names in one response: one finding each, declared order.
        headers = copy.deepcopy(clean_headers) + [["Strict-Transport-Security", "max-age=1"],
                                                  ["Content-Security-Policy", "default-src 'none'"]]
        d = fixture("singleton-two", {"response.json": receipt(headers=headers)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("two duplicate singleton names -> 2 findings in declared order",
               code == 1 and summary == (1, 2)
               and [row[2] for row in shape(findings)]
               == ["duplicate:content-security-policy", "duplicate:strict-transport-security"],
               f"code={code} findings={findings}")

        # Every check non-evaluable: still exit 1 with one could_not_evaluate
        # finding per check (a valid manifest is not a manifest fault).
        d = fixture("all-unevaluable", {},
                    manifest(check(id="a", source="absent-a.json"),
                             check(id="b", source="absent-b.json")))
        code, summary, findings, err = audit(d)
        record("all checks non-evaluable -> exit 1, one line per check",
               code == 1 and summary == (2, 2) and classes(findings) == ["could_not_evaluate"] * 2,
               f"code={code} findings={findings}")

        # Two xcto fields, one wrong: one finding per offending field.
        headers = copy.deepcopy(clean_headers) + [["X-Content-Type-Options", "sniff"]]
        d = fixture("xcto-two", {"response.json": receipt(headers=headers)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("two X-Content-Type-Options, one wrong -> 1 xcto_nosniff_value",
               code == 1 and summary == (1, 1) and classes(findings) == ["xcto_nosniff_value"],
               f"code={code} findings={findings}")

        # OWS-only xcto value is not nosniff.
        headers = copy.deepcopy(clean_headers)
        for row in headers:
            if row[0] == "X-Content-Type-Options":
                row[1] = " \t "
        d = fixture("xcto-empty", {"response.json": receipt(headers=headers)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("OWS-only xcto value -> value=<empty>",
               code == 1 and shape(findings)[0][2] == "value=<empty>", f"code={code} findings={findings}")

        # Multiple bad names: one finding each.
        headers = copy.deepcopy(clean_headers) + [["A B", "1"], ["C\tD", "2"]]
        d = fixture("two-bad-names", {"response.json": receipt(headers=headers)}, manifest(check()))
        code, summary, findings, err = audit(d)
        record("two syntax faults -> 2 field_name_syntax",
               code == 1 and summary == (1, 2) and classes(findings) == ["field_name_syntax"] * 2,
               f"code={code} findings={findings}")

        # 3xx with no Content-Type, nothing declared: clean.
        d = fixture("redirect", {"response.json": receipt(status=301, headers=[])},
                    manifest({"id": "r", "source": "response.json"}))
        code, summary, findings, err = audit(d)
        record("301 with no headers and no expectations -> clean",
               code == 0 and summary == (1, 0), f"code={code} findings={findings}")

        # 204 is 2xx, so the Content-Type expectation applies.
        headers = [row for row in copy.deepcopy(clean_headers) if row[0] != "Content-Type"]
        d = fixture("no-content", {"response.json": receipt(status=204, headers=headers)},
                    manifest(check()))
        code, summary, findings, err = audit(d)
        record("204 without Content-Type -> content_type_present",
               code == 1 and "content_type_present" in classes(findings),
               f"code={code} findings={findings}")

        # Unknown expect keys are ignored; an empty singleton list is fine.
        d = fixture("extra-expect", {"response.json": receipt()},
                    manifest(check(expect=dict(all_expect, singleton_fields=[], note="x"))))
        code, summary, findings, err = audit(d)
        record("unknown expect key ignored, empty singleton list honoured",
               code == 0 and summary == (1, 0), f"code={code} findings={findings}")

        # Source resolution: lane-root-relative path from a nested manifest,
        # and an absolute source path.
        nested = os.path.join(tmp, "nested", "deep")
        os.makedirs(nested, exist_ok=True)
        capture = os.path.join(nested, "cap", "surface-a")
        os.makedirs(capture, exist_ok=True)
        with open(os.path.join(capture, "response.json"), "w", encoding="utf-8") as handle:
            json.dump(receipt(), handle)
        os.makedirs(os.path.join(nested, ".git"), exist_ok=True)
        with open(os.path.join(nested, "manifest.json"), "w", encoding="utf-8") as handle:
            json.dump(manifest(check(source="cap/surface-a/response.json")), handle)
        code, summary, findings, err = audit(nested)
        record("source relative to the enclosing repo root resolves",
               code == 0 and summary == (1, 0), f"code={code} findings={findings}")

        absolute = os.path.join(capture, "response.json")
        d = fixture("absolute-source", {}, manifest(check(source=absolute)))
        code, summary, findings, err = audit(d)
        record("absolute source path resolves", code == 0 and summary == (1, 0),
               f"code={code} findings={findings}")

        # --root override.
        root_dir = os.path.join(tmp, "rootbase")
        os.makedirs(os.path.join(root_dir, "receipts"), exist_ok=True)
        with open(os.path.join(root_dir, "receipts", "r.json"), "w", encoding="utf-8") as handle:
            json.dump(receipt(), handle)
        d = fixture("root-flag", {}, manifest(check(source="receipts/r.json")))
        code, summary, findings, err = audit(d, "--root", root_dir)
        record("--root resolves a source outside the manifest directory",
               code == 0 and summary == (1, 0), f"code={code} findings={findings}")

        # Manifest-level faults.
        d = fixture("manifest-absent", {"response.json": receipt()}, manifest(check()))
        os.remove(os.path.join(d, "manifest.json"))
        code, summary, findings, err = audit(d)
        record("missing manifest -> exit 2", code == 2 and summary is None and findings == [],
               f"code={code} err={err!r}")

        d = fixture("manifest-dir", {"response.json": receipt()}, manifest(check()))
        os.remove(os.path.join(d, "manifest.json"))
        os.makedirs(os.path.join(d, "manifest.json"), exist_ok=True)
        code, summary, findings, err = audit(d)
        record("manifest is a directory -> exit 2", code == 2 and summary is None,
               f"code={code}")

        for label, document in (("version string", manifest(check(), version="1")),
                                ("version bool", manifest(check(), version=True)),
                                ("top-level array", [manifest(check())]),
                                ("checks not an array", {"version": 1, "checks": {}}),
                                ("version missing", {"checks": []})):
            d = fixture(label.replace(" ", "-"), {"response.json": receipt()}, document)
            code, summary, findings, err = audit(d)
            record(f"manifest fault: {label} -> exit 2",
                   code == 2 and summary is None and findings == [], f"code={code}")

        # Usage errors.
        for label, extra in (("no arguments", []),
                             ("unknown flag", ["--manifest", "manifest.json", "--json"]),
                             ("repeated manifest", ["--manifest", "manifest.json", "--manifest", "x"]),
                             ("selftest with manifest", ["--selftest", "--manifest", "x"])):
            d = fixture(f"usage-{counter['n']:02d}", {"response.json": receipt()}, manifest(check()))
            proc_argv = extra
            command = [sys.executable or "python3", "-B", os.path.abspath(__file__), *proc_argv]
            proc = subprocess.run(command, cwd=d, capture_output=True, text=True, timeout=120)
            record(f"usage: {label} -> exit 64", proc.returncode == 64,
                   f"code={proc.returncode}")

        # --help advertises --root and exits 64 (the exit set is closed).
        command = [sys.executable or "python3", "-B", os.path.abspath(__file__), "--help"]
        proc = subprocess.run(command, cwd=tmp, capture_output=True, text=True, timeout=120)
        record("--help advertises --root and exits 64",
               proc.returncode == 64 and "--root" in proc.stdout and "--manifest" in proc.stdout,
               f"code={proc.returncode} out={proc.stdout!r}")

        # Meta: every emitted finding line splits into three fields, and the
        # summary is always the last line.
        meta_ok = True
        meta_note = ""
        headers = copy.deepcopy(clean_headers) + [["X Bad Name", "v"], ["A B", "x"]]
        headers.append(["Content-Type", "text/plain"])
        for label, document, rec in (("meta-a", manifest(check()), receipt()),
                                     ("meta-b", manifest(check()), receipt(status=500, headers=headers))):
            d = fixture(label, {"response.json": rec}, document)
            code, summary, findings, err = audit(d)
            if summary is None or shape(findings) is None:
                meta_ok = False
                meta_note = f"{label}: {findings}"
        record("every finding line has exactly three fields and a trailing summary", meta_ok, meta_note)

    print("header_audit.py --selftest")
    for name in passed:
        print(f"  PASS  {name}")
    for name in failures:
        print(f"  FAIL  {name}")
    total = len(passed) + len(failures)
    print(f"selftest: {len(passed)}/{total} passed")
    return EXIT_CLEAN if not failures else EXIT_FINDINGS


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--help" in argv or "-h" in argv:
        print(USAGE, end="")
        return EXIT_USAGE
    if argv == ["--selftest"]:
        return selftest()
    try:
        args = parse_cli(argv)
    except UsageError as exc:
        print(f"header_audit.py: {exc}", file=sys.stderr)
        return EXIT_USAGE
    return run(args.manifest, args.root)


if __name__ == "__main__":
    sys.exit(main())
