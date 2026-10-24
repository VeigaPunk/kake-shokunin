#!/usr/bin/env python3
"""Round-37 criterion (f): a sealed key must carry both answer polarities per body-reading bullet.

A body-reading bullet is one whose rules cannot decide a check without decoding its body: for
the round-36 C1 contract those are (c) HTML text, (d) quote match, (e) media types and (f)
decoding.  For every case of such a bullet the key must carry

  * at least one expected finding whose check could have held for a different body (its final
    status is 200, it names a body, its media type is supported and its charset is supported):
    only a tool that opens and parses the body can produce it; and
  * at least one check with no expected finding that is also body-decidable: a hold that a
    tool which never opens the body cannot establish.

Together these kill every shortcut whose answer does not depend on body bytes: emitting a
finding everywhere fails the hold side, emitting none fails the finding side, and deciding from
`contentType` or a file name alone leaves the body-decided finding unexplained.  This is the
red-before receipt round-36 lacked: key v1's (e) and (f) cases expect only `unsupported_type`
and `charset_unsupported`, which are readable off the check's metadata.

Usage:
  polarity_check.py --key PATH [--body-bullets c,d,e,f] [--body-reason quote_missing ...]

Exit 0: every case of every body-reading bullet carries both polarities.  Exit 1: at least one
case does not.  Exit 2: the key cannot be read, a named bullet is absent, or a finding's reason
is outside the contract vocabulary the check knows how to classify.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Reasons the round-36 C1 contract derives from a check's metadata alone (statuses, redirect
# hops, media type, charset label, manifest shape): no body bytes are needed.
METADATA_REASONS = {
    "gone",
    "http_error",
    "moved",
    "unsupported_type",
    "charset_unsupported",
    "check_invalid",
    "input_invalid",
}
SUPPORTED_MEDIA = {"text/html", "application/xhtml+xml", "text/plain"}
# The label table the contract asks for: UTF-8, UTF-16BE, UTF-16LE and windows-1252.
SUPPORTED_CHARSETS = {
    "utf-8", "utf8", "unicode-1-1-utf-8", "unicode11utf8", "unicode20utf8", "x-unicode20utf8",
    "utf-16be", "utf-16le",
    "windows-1252", "cp1252", "x-cp1252", "iso-8859-1", "iso8859-1", "iso88591",
    "iso_8859-1", "iso_8859-1:1987", "latin1", "l1", "csisolatin1", "ibm819", "cp819",
    "ascii", "us-ascii", "ansi_x3.4-1968", "iso-ir-100", "csisolatin1",
}


class InputError(Exception):
    """The key cannot be evaluated."""


def _final_status(check: dict) -> int | None:
    hops = check.get("hops")
    if not isinstance(hops, list) or not hops:
        return None
    last = hops[-1]
    if not isinstance(last, dict) or not isinstance(last.get("status"), int):
        return None
    return last["status"]


def _params(content_type: str) -> dict[str, str]:
    params: dict[str, str] = {}
    for part in content_type.split(";")[1:]:
        if "=" not in part:
            continue
        name, value = part.split("=", 1)
        params[name.strip().lower()] = value.strip().strip('"').strip("'")
    return params


def _media_type(content_type: str) -> str:
    return content_type.split(";", 1)[0].strip().lower()


def _body_readable(check: dict) -> bool:
    """True when only the body bytes can decide this check: hold or quote_missing."""
    if _final_status(check) != 200:
        return False
    body = check.get("body")
    if not isinstance(body, str) or not body:
        return False
    content_type = check.get("contentType")
    if not isinstance(content_type, str) or not content_type:
        return False
    if _media_type(content_type) not in SUPPORTED_MEDIA:
        return False
    charset = _params(content_type).get("charset", "utf-8").lower()
    return charset in SUPPORTED_CHARSETS


def _case_checks(case: dict) -> dict[str, dict] | None:
    """Checks of a well-formed manifest, keyed by id; None for a manifest-fault case."""
    manifest = case.get("manifest")
    if not isinstance(manifest, dict):
        return None
    checks = manifest.get("checks")
    if not isinstance(checks, list):
        return None
    found: dict[str, dict] = {}
    for check in checks:
        if isinstance(check, dict) and isinstance(check.get("id"), str):
            found[check["id"]] = check
    return found


def _case_polarity(case: dict, body_reasons: set[str]) -> tuple[list[str], list[str]]:
    """Return (body findings, body holds) for one case, checking reason consistency."""
    expect = case.get("expect")
    if not isinstance(expect, dict):
        raise InputError(f"case {case.get('id')!r} has no expect object")
    findings = expect.get("findings") or []
    if not isinstance(findings, list):
        raise InputError(f"case {case.get('id')!r} has non-list findings")
    checks = _case_checks(case)
    fired: set[str] = set()
    body_findings: list[str] = []
    for finding in findings:
        if not isinstance(finding, dict):
            raise InputError(f"case {case.get('id')!r} has a non-object finding")
        reason = finding.get("reason")
        check_id = finding.get("check")
        if reason in body_reasons:
            check = (checks or {}).get(check_id) if isinstance(check_id, str) else None
            if check is None or not _body_readable(check):
                raise InputError(
                    f"case {case.get('id')!r}: finding {reason!r} on check {check_id!r} "
                    f"cannot come from a body read under the declared contract"
                )
            body_findings.append(check_id)
        elif reason in METADATA_REASONS:
            pass
        else:
            raise InputError(
                f"case {case.get('id')!r}: finding reason {reason!r} is not in the contract "
                f"vocabulary; pass --body-reason if it reads a body"
            )
        if isinstance(check_id, str):
            fired.add(check_id)
    body_holds = sorted(
        check_id
        for check_id, check in (checks or {}).items()
        if check_id not in fired and _body_readable(check)
    )
    return body_findings, body_holds


def check(args: argparse.Namespace) -> int:
    key_path = Path(args.key)
    try:
        key = json.loads(key_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise InputError(f"cannot read key {key_path}: {exc}") from exc
    if not isinstance(key, dict) or not isinstance(key.get("cases"), list) or not key["cases"]:
        raise InputError(f"{key_path} is not a sealed key: no non-empty cases list")
    cases = key["cases"]
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get("bullet"), str):
            raise InputError(f"{key_path}: a case has no bullet")
    bullets = [value.strip() for value in args.body_bullets.split(",") if value.strip()]
    if not bullets:
        raise InputError("no body-reading bullet named")
    present = {case["bullet"] for case in cases}
    missing = [bullet for bullet in bullets if bullet not in present]
    if missing:
        raise InputError(f"key {key_path} has no cases for bullet(s) {', '.join(missing)}")
    body_reasons = set(args.body_reason)
    if not body_reasons:
        raise InputError("no body-dependent finding reason named")

    ok = True
    for bullet in bullets:
        selected = [case for case in cases if case["bullet"] == bullet]
        failed: list[str] = []
        finding_total = 0
        hold_total = 0
        for case in selected:
            body_findings, body_holds = _case_polarity(case, body_reasons)
            finding_total += len(body_findings)
            hold_total += len(body_holds)
            if not body_findings or not body_holds:
                failed.append(str(case.get("id")))
        if failed:
            ok = False
            print(
                f"FAIL: bullet {bullet}: {len(failed)} of {len(selected)} case(s) lack both "
                f"polarities ({', '.join(failed)}); body-decided findings {finding_total}, "
                f"body-decided holds {hold_total}. A check whose correct outcome is a finding "
                f"that only a body read can produce is required, and likewise a hold."
            )
        else:
            print(
                f"PASS: bullet {bullet}: {len(selected)} case(s) each carry a body-decided "
                f"finding and a body-decided hold ({finding_total} findings, {hold_total} holds)."
            )
    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check that a sealed key carries both polarities per body-reading bullet."
    )
    parser.add_argument("--key", required=True, help="sealed key JSON")
    parser.add_argument(
        "--body-bullets",
        default="c,d,e,f",
        help="body-reading contract bullets (round-36 C1: c HTML text, d quote match, "
        "e media types, f decoding); default c,d,e,f",
    )
    parser.add_argument(
        "--body-reason",
        action="append",
        default=None,
        help="reason only a body read produces (default: quote_missing); repeatable",
    )
    parser.allow_abbrev = False
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.body_reason is None:
        args.body_reason = ["quote_missing"]
    try:
        return check(args)
    except (InputError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
