#!/usr/bin/env python3
"""Offline X-Robots-Tag declaration audit (kake round 79, claim C2).

Reads a version-1 manifest of recorded response header fields and URLs, read-only and
network-free, and decides for every check:

  * `directives` — the declared, normalized tokens of the global scope (sorted; duplicates kept);
  * `effective`  — the global restriction set (positives removed; `nosnippet` suppresses the
    max-snippet/max-video-preview caps; duplicate caps collapse to the minimum);
  * `bots`       — per-bot scopes, each with the same normalized token list;
  * `findings`   — the closed finding vocabulary, one sorted unique id list per check.

Grammar readings (frozen in `.ufo/waves/round-79/contract.md` and amendment 1):
field values split on ASCII comma; an empty segment is `xrt_empty_rule`; a `name:` prefix that is
NOT a known directive name is a bot scope and binds the remaining rules of that field value (scope
does not cross field lines); a known directive name takes precedence over the bot-prefix shape;
`none` is replaced by `noindex`+`nofollow`; `all` contributes nothing; `index`/`follow` are kept as
positive tokens; `index` with `noindex` (or `follow` with `nofollow`) is `xrt_mutually_exclusive`;
`indexifembedded` without `noindex` is `xrt_indexifembedded_without_noindex`; a repeated
value-bearing directive is `xrt_duplicate_directive`; invalid values are `xrt_invalid_value` and
are dropped.

Exit: 0 no findings, 1 findings, 2 input fault, 64 usage. `--json` prints exactly one object.
No fetch, no rendering, no crawler-behaviour, robots.txt, live-serving or per-bot-effective claim.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys

SCHEMA_MANIFEST = "x-robots-tag-manifest/v1"
SCHEMA_REPORT = "x-robots-tag-report/v1"
MAX_MANIFEST_BYTES = 16 * 1024 * 1024

KNOWN = {
    "all", "index", "noindex", "follow", "nofollow", "none", "nosnippet", "indexifembedded",
    "max-snippet", "max-image-preview", "max-video-preview", "notranslate", "noimageindex",
    "unavailable_after", "noarchive",
}
VALUELESS = {
    "all", "index", "noindex", "follow", "nofollow", "none", "nosnippet", "indexifembedded",
    "notranslate", "noimageindex", "noarchive",
}
INT_RE = re.compile(r"^-?[0-9]+$")
BOT_RE = re.compile(r"^[A-Za-z0-9_-]+$")
ISO_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}([T ][0-9]{2}:[0-9]{2}(:[0-9]{2})?(Z|[+-][0-9]{2}:[0-9]{2})?)?$")
RFC822_RE = re.compile(
    r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun), [0-9]{2} "
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} "
    r"[0-9]{2}:[0-9]{2}(:[0-9]{2})? GMT$")
RFC850_RE = re.compile(
    r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), [0-9]{2}-"
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-[0-9]{2} "
    r"[0-9]{2}:[0-9]{2}:[0-9]{2} GMT$")


class Fault(Exception):
    def __init__(self, ident: str, detail: str):
        super().__init__(detail)
        self.ident = ident
        self.detail = detail


def parse_rule(segment: str, findings: set[str]) -> list[str]:
    """One directive segment -> normalized tokens (empty on an unknown name or a dropped value)."""
    head, sep, rest = segment.partition(":")
    name = (head if sep else segment).strip().lower()
    value = rest.strip() if sep else None
    if name not in KNOWN:
        findings.add("xrt_unknown_directive")
        return []
    if name in VALUELESS:
        if sep and value:
            findings.add("xrt_invalid_value")
        if name == "all":
            return []
        if name == "none":
            return ["noindex", "nofollow"]
        return [name]
    if name == "max-snippet" or name == "max-video-preview":
        if value is None or not INT_RE.match(value):
            findings.add("xrt_invalid_value")
            return []
        try:
            number = int(value)
        except ValueError:  # CPython's int()-digit limit is invisible to INT_RE
            findings.add("xrt_invalid_value")
            return []
        return [f"{name}:{number}"]
    if name == "max-image-preview":
        if value is None or value.lower() not in ("none", "standard", "large"):
            findings.add("xrt_invalid_value")
            return []
        return [f"max-image-preview:{value.lower()}"]
    # unavailable_after
    if value is None or not (ISO_RE.match(value) or RFC822_RE.match(value) or RFC850_RE.match(value)):
        findings.add("xrt_invalid_value")
        return []
    return [f"unavailable_after:{value}"]


def parse_field(value: str, findings: set[str]) -> tuple[list[str], dict[str, list[str]]]:
    """One X-Robots-Tag field value -> (global tokens, per-bot tokens)."""
    global_tokens: list[str] = []
    bots: dict[str, list[str]] = {}
    scope: str | None = None
    for raw in value.split(","):
        segment = raw.strip()
        if not segment:
            findings.add("xrt_empty_rule")
            continue
        head, sep, rest = segment.partition(":")
        if sep and BOT_RE.match(head.strip()) and head.strip().lower() not in KNOWN:
            bot = head.strip().lower()
            rule = rest.strip()
            if not rule:
                findings.add("xrt_bot_scope_empty")
                continue
            scope = bot
            bots.setdefault(bot, [])
            segment = rule
        tokens = parse_rule(segment, findings)
        if scope is None:
            global_tokens.extend(tokens)
        else:
            bots[scope].extend(tokens)
    return global_tokens, bots


def effective_of(tokens: list[str]) -> list[str]:
    kept = [t for t in tokens if t not in ("all", "index", "follow")]
    if "nosnippet" in kept:
        kept = [t for t in kept if not (t.startswith("max-snippet:") or t.startswith("max-video-preview:"))]
    plain: set[str] = set()
    caps: dict[str, int] = {}
    for token in kept:
        if token.startswith("max-snippet:") or token.startswith("max-video-preview:"):
            name, _, value = token.partition(":")
            caps[name] = min(caps[name], int(value)) if name in caps else int(value)
        else:
            plain.add(token)
    return sorted(plain | {f"{name}:{value}" for name, value in caps.items()})


def scope_findings(tokens: list[str], findings: set[str]) -> None:
    names = set(tokens)
    if "index" in names and "noindex" in names:
        findings.add("xrt_mutually_exclusive")
    if "follow" in names and "nofollow" in names:
        findings.add("xrt_mutually_exclusive")
    if "indexifembedded" in names and "noindex" not in names:
        findings.add("xrt_indexifembedded_without_noindex")
    for cap in ("max-snippet", "max-video-preview", "max-image-preview", "unavailable_after"):
        if sum(1 for t in tokens if t.startswith(cap + ":")) > 1:
            findings.add("xrt_duplicate_directive")


def load_manifest(path: str) -> dict:
    try:
        info = os.stat(path)
        if not stat.S_ISREG(info.st_mode):
            raise Fault("xrt_input_unreadable", "manifest is not a regular file")
        if info.st_size > MAX_MANIFEST_BYTES:
            raise Fault("xrt_input_unreadable", f"manifest exceeds {MAX_MANIFEST_BYTES} bytes")
        with open(path, "rb") as handle:
            raw = handle.read(MAX_MANIFEST_BYTES + 1)
    except OSError as exc:
        raise Fault("xrt_input_unreadable", str(exc))
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:
        raise Fault("xrt_input_bad_json", str(exc))
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA_MANIFEST:
        raise Fault("xrt_input_schema", "manifest must carry schema %s" % SCHEMA_MANIFEST)
    checks = doc.get("checks")
    if not isinstance(checks, list) or not checks:
        raise Fault("xrt_input_schema", "`checks` must be a non-empty list")
    seen: set[str] = set()
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            raise Fault("xrt_input_check_shape", f"check {index} is not an object")
        ident, url, headers = check.get("id"), check.get("url"), check.get("headers")
        if not isinstance(ident, str) or not ident:
            raise Fault("xrt_input_check_shape", f"check {index} id must be a non-empty string")
        if not isinstance(url, str) or not url:
            raise Fault("xrt_input_check_shape", f"check {ident} url must be a non-empty string")
        if not isinstance(headers, list):
            raise Fault("xrt_input_check_shape", f"check {ident} headers must be a list")
        if ident in seen:
            raise Fault("xrt_input_duplicate_id", f"duplicate check id {ident}")
        seen.add(ident)
        for header in headers:
            if not isinstance(header, dict):
                raise Fault("xrt_input_check_shape", f"check {ident} header is not an object")
            if not isinstance(header.get("name"), str) or not header.get("name"):
                raise Fault("xrt_input_check_shape", f"check {ident} header name")
            if not isinstance(header.get("value"), str):
                raise Fault("xrt_input_check_shape", f"check {ident} header value")
    return doc


def audit(doc: dict) -> dict:
    results = []
    for check in doc["checks"]:
        findings: set[str] = set()
        global_tokens: list[str] = []
        bots: dict[str, list[str]] = {}
        for header in check["headers"]:
            if header["name"].lower() != "x-robots-tag":
                continue
            tokens, scoped = parse_field(header["value"], findings)
            global_tokens.extend(tokens)
            for bot, bot_tokens in scoped.items():
                bots.setdefault(bot, []).extend(bot_tokens)
        scope_findings(global_tokens, findings)
        for bot_tokens in bots.values():
            scope_findings(bot_tokens, findings)
        results.append({
            "id": check["id"],
            "url": check["url"],
            "directives": sorted(global_tokens),
            "effective": effective_of(global_tokens),
            "bots": {bot: sorted(tokens) for bot, tokens in sorted(bots.items())},
            "findings": sorted(findings),
        })
    union = sorted({finding for result in results for finding in result["findings"]})
    return {"schema": SCHEMA_REPORT, "checks": results, "findings": union,
            "exit": 1 if union else 0}


def error_report(fault: Fault) -> dict:
    return {"schema": SCHEMA_REPORT, "error": {"id": fault.ident, "detail": fault.detail}, "exit": 2}


def _plain(text: str) -> str:
    """Printable rendering of untrusted text for the text-mode surface (control chars escaped)."""
    return "".join(ch if ch.isprintable() else f"\\x{ord(ch):02x}" for ch in text)


def render_text(report: dict) -> str:
    lines = []
    for check in report.get("checks", []):
        lines.append(
            f"check {_plain(str(check['id']))} directives={check['directives']} "
            f"effective={check['effective']} bots={check['bots']} findings={check['findings']}")
    lines.append(f"XRTv1 checks={len(report.get('checks', []))} "
                 f"findings={len(report.get('findings', []))} exit={report['exit']}")
    return "\n".join(lines)


# ── selftest ────────────────────────────────────────────────────────────────
def _case(ident: str, headers: list[tuple[str, str]], want: dict) -> tuple[dict, dict]:
    return ({"id": ident, "url": f"https://example.test/{ident}",
             "headers": [{"name": name, "value": value} for name, value in headers]}, want)


def selftest() -> int:
    cases = [
        _case("t01", [("X-Robots-Tag", "noindex")],
              {"directives": ["noindex"], "effective": ["noindex"], "bots": {}, "findings": []}),
        _case("t02", [("X-Robots-Tag", "none")],
              {"directives": ["nofollow", "noindex"], "effective": ["nofollow", "noindex"],
               "bots": {}, "findings": []}),
        _case("t03", [("X-Robots-Tag", "all")],
              {"directives": [], "effective": [], "bots": {}, "findings": []}),
        _case("t04", [("X-Robots-Tag", "googlebot: noindex")],
              {"directives": [], "effective": [], "bots": {"googlebot": ["noindex"]},
               "findings": []}),
        _case("t05", [("X-Robots-Tag", "noindex, googlebot: nofollow")],
              {"directives": ["noindex"], "effective": ["noindex"],
               "bots": {"googlebot": ["nofollow"]}, "findings": []}),
        _case("t06", [("X-Robots-Tag", "max-snippet:50, nosnippet")],
              {"directives": ["max-snippet:50", "nosnippet"], "effective": ["nosnippet"],
               "bots": {}, "findings": []}),
        _case("t07", [("X-Robots-Tag", "index, noindex")],
              {"directives": ["index", "noindex"], "effective": ["noindex"], "bots": {},
               "findings": ["xrt_mutually_exclusive"]}),
        _case("t08", [("X-Robots-Tag", "noindex,,nofollow")],
              {"directives": ["nofollow", "noindex"], "effective": ["nofollow", "noindex"],
               "bots": {}, "findings": ["xrt_empty_rule"]}),
        _case("t09", [("X-Robots-Tag", "max-snippet:abc")],
              {"directives": [], "effective": [], "bots": {}, "findings": ["xrt_invalid_value"]}),
        _case("t10", [("X-Robots-Tag", "googlebot:")],
              {"directives": [], "effective": [], "bots": {}, "findings": ["xrt_bot_scope_empty"]}),
        _case("t11", [("X-Robots-Tag", "indexifembedded")],
              {"directives": ["indexifembedded"], "effective": ["indexifembedded"], "bots": {},
               "findings": ["xrt_indexifembedded_without_noindex"]}),
        _case("t12", [("X-Robots-Tag", "max-snippet:50, max-snippet:100")],
              {"directives": ["max-snippet:100", "max-snippet:50"], "effective": ["max-snippet:50"],
               "bots": {}, "findings": ["xrt_duplicate_directive"]}),
        _case("t13", [("X-Robots-Tag", "googlebot: noindex, nofollow")],
              {"directives": [], "effective": [], "bots": {"googlebot": ["nofollow", "noindex"]},
               "findings": []}),
        _case("t14", [("X-Robots-Tag", "NoIndex")],
              {"directives": ["noindex"], "effective": ["noindex"], "bots": {}, "findings": []}),
        _case("t15", [("X-Robots-Tag", "unavailable_after:2025-12-31T23:59:59Z")],
              {"directives": ["unavailable_after:2025-12-31T23:59:59Z"],
               "effective": ["unavailable_after:2025-12-31T23:59:59Z"], "bots": {}, "findings": []}),
        _case("t16", [("X-Robots-Tag", "unavailable_after:tomorrow")],
              {"directives": [], "effective": [], "bots": {}, "findings": ["xrt_invalid_value"]}),
        _case("t17", [("X-Robots-Tag", "max-image-preview:Large")],
              {"directives": ["max-image-preview:large"], "effective": ["max-image-preview:large"],
               "bots": {}, "findings": []}),
        _case("t18", [("X-Robots-Tag", "noimageindex, notranslate")],
              {"directives": ["noimageindex", "notranslate"],
               "effective": ["noimageindex", "notranslate"], "bots": {}, "findings": []}),
        _case("t19", [("X-Robots-Tag", "noindex; nofollow")],
              {"directives": [], "effective": [], "bots": {}, "findings": ["xrt_unknown_directive"]}),
        _case("t20", [("X-Frame-Options", "DENY")],
              {"directives": [], "effective": [], "bots": {}, "findings": []}),
        _case("t21", [("X-Robots-Tag", "googlebot: noindex, bingbot: nofollow")],
              {"directives": [], "effective": [],
               "bots": {"bingbot": ["nofollow"], "googlebot": ["noindex"]}, "findings": []}),
        _case("t22", [("X-Robots-Tag", "unavailable_after:2025-12-31, unavailable_after:2026-01-01")],
              {"directives": ["unavailable_after:2025-12-31", "unavailable_after:2026-01-01"],
               "effective": ["unavailable_after:2025-12-31", "unavailable_after:2026-01-01"],
               "bots": {}, "findings": ["xrt_duplicate_directive"]}),
        _case("t23", [("X-Robots-Tag", "max-snippet:" + "1" * 5000)],
              {"directives": [], "effective": [], "bots": {}, "findings": ["xrt_invalid_value"]}),
    ]
    passed = 0
    for check, want in cases:
        report = audit({"checks": [check]})
        got = report["checks"][0]
        if all(got[key] == want[key] for key in ("directives", "effective", "bots", "findings")):
            passed += 1
        else:
            print(f"  FAIL {check['id']}: {got} != {want}")
    faults = [
        ("duplicate id", {"schema": SCHEMA_MANIFEST,
                          "checks": [{"id": "d", "url": "u", "headers": []},
                                     {"id": "d", "url": "u", "headers": []}]}, "xrt_input_duplicate_id"),
        ("bad schema", {"schema": "v2", "checks": []}, "xrt_input_schema"),
        ("check shape", {"schema": SCHEMA_MANIFEST,
                         "checks": [{"id": "c", "url": "u", "headers": "x"}]}, "xrt_input_check_shape"),
    ]
    for name, doc, ident in faults:
        try:
            load_manifest_doc(doc)
            print(f"  FAIL fault {name}: no fault raised")
        except Fault as fault:
            if fault.ident == ident:
                passed += 1
            else:
                print(f"  FAIL fault {name}: {fault.ident} != {ident}")
    total = len(cases) + len(faults)
    print(f"selftest: {passed}/{total} passed")
    return 0 if passed == total else 1


def load_manifest_doc(doc) -> dict:
    """Validate an in-memory document with the same rules as load_manifest (selftest helper)."""
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA_MANIFEST:
        raise Fault("xrt_input_schema", "schema")
    checks = doc.get("checks")
    if not isinstance(checks, list) or not checks:
        raise Fault("xrt_input_schema", "checks")
    seen = set()
    for check in checks:
        if not isinstance(check, dict):
            raise Fault("xrt_input_check_shape", "check")
        ident = check.get("id")
        if not isinstance(ident, str) or not ident:
            raise Fault("xrt_input_check_shape", "id")
        if not isinstance(check.get("url"), str) or not check.get("url"):
            raise Fault("xrt_input_check_shape", "url")
        if not isinstance(check.get("headers"), list):
            raise Fault("xrt_input_check_shape", "headers")
        if ident in seen:
            raise Fault("xrt_input_duplicate_id", "dup")
        seen.add(ident)
    return doc


class Parser(argparse.ArgumentParser):
    """Usage errors exit 64 (the contract reserves 2 for input faults with a JSON error)."""

    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(64, f"{self.prog}: error: {message}\n")


def main() -> int:
    parser = Parser(description="Offline X-Robots-Tag declaration audit")
    parser.add_argument("--manifest")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if not args.manifest:
        print("usage: --manifest is required (or --selftest)", file=sys.stderr)
        return 64
    try:
        doc = load_manifest(args.manifest)
    except Fault as fault:
        report = error_report(fault)
        print(json.dumps(report) if args.json else f"XRTv1 error={fault.ident} exit=2")
        return 2
    report = audit(doc)
    print(json.dumps(report) if args.json else render_text(report))
    return report["exit"]


if __name__ == "__main__":
    sys.exit(main())
