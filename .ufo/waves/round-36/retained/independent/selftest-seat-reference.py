#!/usr/bin/env python3
"""Reference implementation of the C1 source re-check audit, written from the public contract.

This file exists only to validate the self-test: it is not the deliverable. The deliverable is
source_recheck_selftest.py. The tool under test (scripts/source_recheck.py) is built by another
seat and was not read while writing this.

Usage: python3 reference.py --manifest PATH
"""

import html as html_module
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urljoin

REDIRECT_STATUSES = (301, 302, 303, 307, 308)
PERMANENT_STATUSES = (301, 308)
SUPPORTED_CHARSETS = {
    "utf-8": "utf-8",
    "utf-16be": "utf-16be",
    "utf-16le": "utf-16le",
    "windows-1252": "windows-1252",
    "iso-8859-1": "windows-1252",
    "latin1": "windows-1252",
    "ascii": "windows-1252",
    "us-ascii": "windows-1252",
}
BOMS = ((b"\xef\xbb\xbf", "utf-8"), (b"\xfe\xff", "utf-16be"), (b"\xff\xfe", "utf-16le"))

COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
RAW_ELEMENT_RE = re.compile(r"<(script|style|template)\b[^>]*>.*?</\1\s*>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[A-Za-z/!][^>]*>", re.DOTALL)


def usage():
    sys.stderr.write("usage: reference.py --manifest PATH\n")
    return 64


def media_type_and_charset(content_type):
    parts = content_type.split(";")
    media = parts[0].strip().lower()
    charset = None
    for part in parts[1:]:
        if "=" not in part:
            continue
        name, _, value = part.partition("=")
        if name.strip().lower() != "charset":
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            value = value[1:-1]
        charset = value.strip().lower()
        break
    return media, charset


def decode_body(data, charset):
    for bom, encoding in BOMS:
        if data.startswith(bom):
            return data[len(bom):].decode(encoding, "replace")
    encoding = "utf-8"
    if charset is not None:
        encoding = SUPPORTED_CHARSETS.get(charset)
        if encoding is None:
            return None
    return data.decode(encoding, "replace")


def html_text(text):
    text = COMMENT_RE.sub("", text)
    text = RAW_ELEMENT_RE.sub("", text)
    text = TAG_RE.sub("", text)
    return html_module.unescape(text)


def normalize(value):
    value = unicodedata.normalize("NFKC", value)
    return "".join(ch for ch in value if not ch.isspace())


def valid_check(check, manifest_dir):
    if not isinstance(check, dict):
        return False
    cid = check.get("id")
    if not isinstance(cid, str) or not cid:
        return False
    url = check.get("url")
    if not isinstance(url, str) or not url:
        return False
    if not (url.startswith("http://") or url.startswith("https://")):
        return False
    host = url.split("//", 1)[1].split("/", 1)[0]
    if not host:
        return False
    quote = check.get("quote")
    if not isinstance(quote, str) or not quote:
        return False
    hops = check.get("hops")
    if not isinstance(hops, list) or not hops:
        return False
    for index, entry in enumerate(hops):
        if not isinstance(entry, dict):
            return False
        status = entry.get("status")
        if not isinstance(status, int) or isinstance(status, bool):
            return False
        if not 100 <= status <= 599:
            return False
        location = entry.get("location")
        is_redirect = status in REDIRECT_STATUSES
        if is_redirect:
            if not isinstance(location, str) or not location:
                return False
        elif location is not None and not isinstance(location, str):
            return False
        last = index == len(hops) - 1
        if last and is_redirect:
            return False
        if not last and not is_redirect:
            return False
    status = hops[-1]["status"]
    if status == 200:
        content_type = check.get("contentType")
        if not isinstance(content_type, str) or not content_type:
            return False
        body = check.get("body")
        if not isinstance(body, str) or not body:
            return False
        if Path(body).is_absolute():
            return False
        target = (manifest_dir / body).resolve()
        try:
            target.relative_to(manifest_dir.resolve())
        except ValueError:
            return False
        if not target.is_file():
            return False
    return True


def evaluate(check, manifest_dir):
    findings = []
    cid = check["id"]
    hops = check["hops"]
    base = check["url"]
    if hops[0]["status"] in PERMANENT_STATUSES:
        index = 0
        target = None
        while index < len(hops) and hops[index]["status"] in PERMANENT_STATUSES:
            target = urljoin(base, hops[index]["location"])
            base = target
            index += 1
        findings.append({"check": cid, "reason": "moved", "target": target})
    status = hops[-1]["status"]
    if status == 200:
        content_type = check["contentType"]
        media, charset = media_type_and_charset(content_type)
        data = (manifest_dir / check["body"]).resolve().read_bytes()
        text = decode_body(data, charset)
        if text is None:
            findings.append({"check": cid, "reason": "charset_unsupported", "target": None})
            return findings
        if media == "text/html" or media == "application/xhtml+xml":
            text = html_text(text)
        elif media == "text/plain":
            pass
        else:
            findings.append({"check": cid, "reason": "unsupported_type", "target": None})
            return findings
        if normalize(check["quote"]) not in normalize(text):
            findings.append({"check": cid, "reason": "quote_missing", "target": None})
    elif status in (404, 410):
        findings.append({"check": cid, "reason": "gone", "target": None})
    else:
        findings.append({"check": cid, "reason": "http_error", "target": None})
    return findings


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 2 or argv[0] != "--manifest":
        return usage()
    manifest_path = Path(argv[1])
    manifest_dir = manifest_path.parent.resolve()
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return emit(0, "could-not-evaluate", [{"check": None, "reason": "input_invalid", "target": None}])
    if not isinstance(manifest, dict) or manifest.get("version") != 1:
        return emit(0, "could-not-evaluate", [{"check": None, "reason": "input_invalid", "target": None}])
    checks = manifest.get("checks")
    if not isinstance(checks, list):
        return emit(0, "could-not-evaluate", [{"check": None, "reason": "input_invalid", "target": None}])

    findings = []
    evaluated = 0
    for check in checks:
        if not valid_check(check, manifest_dir):
            cid = None
            if isinstance(check, dict) and isinstance(check.get("id"), str) and check["id"]:
                cid = check["id"]
            findings.append({"check": cid, "reason": "check_invalid", "target": None})
            continue
        evaluated += 1
        findings.extend(evaluate(check, manifest_dir))

    reasons = {item["reason"] for item in findings}
    if reasons & {"input_invalid", "check_invalid", "charset_unsupported"}:
        verdict = "could-not-evaluate"
    elif findings:
        verdict = "failed-policy"
    else:
        verdict = "clean"
    return emit(evaluated, verdict, findings)


def emit(evaluated, verdict, findings):
    print(json.dumps({"version": 1, "verdict": verdict, "checksEvaluated": evaluated,
                      "findings": findings}))
    if verdict == "clean":
        return 0
    if verdict == "failed-policy":
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
