#!/usr/bin/env python3
"""Round-36 C1 source re-check audit (`scripts/source_recheck.py`).

Re-checks a recorded fetch: for every check in a manifest it reads the recorded
body and reports whether the quoted text is still there.  The tool is offline by
construction: it reads only the manifest and the body files the manifest names.
No network, no writes, no subprocesses, no environment reads.  Python standard
library only.

Usage:
    python3 scripts/source_recheck.py --manifest PATH

One JSON report on stdout:
    {"version": 1, "verdict": V, "checksEvaluated": N, "findings": [F, ...]}
where each finding is {"check": <check id or null>, "reason": R, "target": <URL
or null>}.  Exit 0 when the verdict is `clean`, 1 when it is `failed-policy`, 2
when it is `could-not-evaluate`, 64 on a usage error.

Contract (SCORECARD.md, round 36, "Round 36 -- declared claims", C1 contract):
bullets (a) final status, (b) redirects, (c) HTML text, (d) quote match,
(e) media types, (f) decoding, (g) input faults, plus the verdict rule.
Sources: S088 (RFC 9110), S089 (RFC 3986), S090 (WHATWG Encoding), S091 (UAX
#15), S092 (WHATWG HTML syntax), S025 (template contents), S033 (media types).
"""
from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from html import unescape

REPORT_VERSION = 1

REDIRECT_STATUSES = frozenset((301, 302, 303, 307, 308))
PERMANENT_STATUSES = frozenset((301, 308))
GONE_STATUSES = frozenset((404, 410))
HTML_MEDIA_TYPES = frozenset(("text/html", "application/xhtml+xml"))
PLAIN_MEDIA_TYPE = "text/plain"

EXIT_CLEAN = 0
EXIT_FAILED_POLICY = 1
EXIT_COULD_NOT_EVALUATE = 2
EXIT_USAGE = 64

VERDICT_CLEAN = "clean"
VERDICT_FAILED_POLICY = "failed-policy"
VERDICT_COULD_NOT_EVALUATE = "could-not-evaluate"

# Reasons that make the run "could-not-evaluate" (contract: verdict rule).
BLOCKING_REASONS = frozenset(("input_invalid", "check_invalid", "charset_unsupported"))

_ASCII_LOWER = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "abcdefghijklmnopqrstuvwxyz",
)


def ascii_lower(text: str) -> str:
    """ASCII-only lowercasing (the contract says ASCII case-insensitive)."""
    return text.translate(_ASCII_LOWER)


def ascii_is_letter(char: str) -> bool:
    return ("a" <= char <= "z") or ("A" <= char <= "Z")


# --------------------------------------------------------------------------
# RFC 3986 (S089) reference resolution -- section 5.2, no further normalization
# --------------------------------------------------------------------------

# RFC 3986 appendix B.
_URI_REF_RE = re.compile(
    r"^(?:(?P<scheme>[^:/?#]+):)?(?://(?P<authority>[^/?#]*))?(?P<path>[^?#]*)"
    r"(?:\?(?P<query>[^#]*))?(?:#(?P<fragment>.*))?$",
    re.S,
)


def parse_uri_ref(text: str):
    """Split a URI reference into (scheme, authority, path, query, fragment).

    Undefined components are None (RFC 3986 section 3).
    """
    match = _URI_REF_RE.match(text)
    if match is None:  # pragma: no cover -- the appendix B pattern always matches
        return None, None, text, None, None
    return (
        match.group("scheme"),
        match.group("authority"),
        match.group("path"),
        match.group("query"),
        match.group("fragment"),
    )


def remove_dot_segments(path: str) -> str:
    """RFC 3986 section 5.2.4."""
    buffer = path
    out: list[str] = []
    while buffer:
        if buffer.startswith("../"):
            buffer = buffer[3:]
        elif buffer.startswith("./"):
            buffer = buffer[2:]
        elif buffer.startswith("/./"):
            buffer = "/" + buffer[3:]
        elif buffer == "/.":
            buffer = "/"
        elif buffer.startswith("/../"):
            buffer = "/" + buffer[4:]
            if out:
                out.pop()
        elif buffer == "/..":
            buffer = "/"
            if out:
                out.pop()
        elif buffer in (".", ".."):
            buffer = ""
        else:
            if buffer.startswith("/"):
                cut = buffer.find("/", 1)
            else:
                cut = buffer.find("/")
            if cut == -1:
                segment, buffer = buffer, ""
            else:
                segment, buffer = buffer[:cut], buffer[cut:]
            out.append(segment)
    return "".join(out)


def _merge(base_authority, base_path: str, ref_path: str) -> str:
    """RFC 3986 section 5.2.3."""
    if base_authority is not None and base_path == "":
        return "/" + ref_path
    cut = base_path.rfind("/")
    if cut == -1:
        return ref_path
    return base_path[: cut + 1] + ref_path


def _recompose(scheme, authority, path: str, query, fragment) -> str:
    """RFC 3986 section 5.3."""
    parts = []
    if scheme is not None:
        parts.append(scheme + ":")
    if authority is not None:
        parts.append("//" + authority)
    parts.append(path)
    if query is not None:
        parts.append("?" + query)
    if fragment is not None:
        parts.append("#" + fragment)
    return "".join(parts)


def resolve_reference(base: str, reference: str) -> str:
    """RFC 3986 section 5.2.2 (strict): resolve `reference` against `base`.

    No further normalization: the scheme, host, percent-encoding and dot
    segments of the target are exactly what section 5.2 produces.
    """
    b_scheme, b_authority, b_path, b_query, _ = parse_uri_ref(base)
    r_scheme, r_authority, r_path, r_query, r_fragment = parse_uri_ref(reference)
    if r_scheme is not None:
        target = (r_scheme, r_authority, remove_dot_segments(r_path), r_query)
    elif r_authority is not None:
        target = (b_scheme, r_authority, remove_dot_segments(r_path), r_query)
    elif r_path == "":
        query = r_query if r_query is not None else b_query
        target = (b_scheme, b_authority, b_path, query)
    else:
        if r_path.startswith("/"):
            path = remove_dot_segments(r_path)
        else:
            path = remove_dot_segments(_merge(b_authority, b_path, r_path))
        target = (b_scheme, b_authority, path, r_query)
    return _recompose(target[0], target[1], target[2], target[3], r_fragment)


def host_of(authority) -> str:
    """The host component of an authority (userinfo and port removed)."""
    if not authority:
        return ""
    rest = authority.rsplit("@", 1)[-1]
    if rest.startswith("["):
        end = rest.find("]")
        if end == -1:
            return ""
        return rest[: end + 1]
    return rest.split(":", 1)[0]


# --------------------------------------------------------------------------
# WHATWG Encoding (S090) label table, restricted to the supported encodings
# --------------------------------------------------------------------------

# Labels of UTF-8, UTF-16BE, UTF-16LE and windows-1252 only.  Every other
# label of the WHATWG table (and every label outside it) is unsupported.
CHARSET_LABELS = {
    # UTF-8
    "unicode-1-1-utf-8": "utf-8",
    "unicode11utf8": "utf-8",
    "unicode20utf8": "utf-8",
    "utf-8": "utf-8",
    "utf8": "utf-8",
    "x-unicode20utf8": "utf-8",
    # UTF-16BE
    "unicodefffe": "utf-16-be",
    "utf-16be": "utf-16-be",
    # UTF-16LE
    "csunicode": "utf-16-le",
    "iso-10646-ucs-2": "utf-16-le",
    "ucs-2": "utf-16-le",
    "unicode": "utf-16-le",
    "unicodefeff": "utf-16-le",
    "utf-16": "utf-16-le",
    "utf-16le": "utf-16-le",
    # windows-1252
    "ansi_x3.4-1968": "cp1252",
    "ascii": "cp1252",
    "cp1252": "cp1252",
    "cp819": "cp1252",
    "csisolatin1": "cp1252",
    "ibm819": "cp1252",
    "iso-8859-1": "cp1252",
    "iso-ir-100": "cp1252",
    "iso8859-1": "cp1252",
    "iso88591": "cp1252",
    "iso_8859-1": "cp1252",
    "iso_8859-1:1987": "cp1252",
    "l1": "cp1252",
    "latin1": "cp1252",
    "us-ascii": "cp1252",
    "windows-1252": "cp1252",
    "x-cp1252": "cp1252",
}

BOMS = (
    (b"\xef\xbb\xbf", "utf-8"),
    (b"\xfe\xff", "utf-16-be"),
    (b"\xff\xfe", "utf-16-le"),
)


def pick_encoding(data: bytes, charset):
    """Return (codec, payload) or (None, None) when the charset is unsupported.

    A byte order mark wins over the charset parameter (contract bullet f).
    """
    for mark, codec in BOMS:
        if data.startswith(mark):
            return codec, data[len(mark):]
    if charset is None:
        return "utf-8", data
    label = charset.strip()
    if len(label) >= 2 and label.startswith('"') and label.endswith('"'):
        label = label[1:-1].strip()
    codec = CHARSET_LABELS.get(ascii_lower(label))
    if codec is None:
        return None, None
    return codec, data


# --------------------------------------------------------------------------
# HTML text extraction (contract bullet c)
# --------------------------------------------------------------------------

_RAW_START_RE = re.compile(r"<(script|style|template)(?=[\s/>])", re.IGNORECASE)
_RAW_END_RES = {
    name: re.compile(r"</" + name + r"(?=[\s/>])", re.IGNORECASE)
    for name in ("script", "style", "template")
}


def remove_comments(text: str) -> str:
    """`<!--` up to the next `-->` (an unterminated comment runs to the end)."""
    out = []
    index = 0
    while True:
        start = text.find("<!--", index)
        if start == -1:
            out.append(text[index:])
            return "".join(out)
        out.append(text[index:start])
        end = text.find("-->", start + 4)
        if end == -1:
            return "".join(out)
        index = end + 3


def remove_raw_elements(text: str) -> str:
    """Drop script, style and template elements (start tag to the next end tag
    of the same name, ASCII case-insensitive)."""
    out = []
    index = 0
    while True:
        match = _RAW_START_RE.search(text, index)
        if match is None:
            out.append(text[index:])
            return "".join(out)
        out.append(text[index:match.start()])
        end_match = _RAW_END_RES[match.group(1).lower()].search(text, match.end())
        if end_match is None:
            # No end tag: the element runs to the end of the document.
            return "".join(out)
        close = text.find(">", end_match.end())
        if close == -1:
            return "".join(out)
        index = close + 1


def strip_tags(text: str) -> str:
    """Remove every remaining tag: `<` plus ASCII letter, `/` or `!`, up to the
    next `>`."""
    out = []
    index = 0
    length = len(text)
    while True:
        start = text.find("<", index)
        if start == -1:
            out.append(text[index:])
            return "".join(out)
        if start + 1 < length and (
            ascii_is_letter(text[start + 1]) or text[start + 1] in "/!"
        ):
            close = text.find(">", start + 1)
            if close == -1:
                # No `>` anywhere later, so no further tag can be closed.
                out.append(text[index:])
                return "".join(out)
            out.append(text[index:start])
            index = close + 1
        else:
            out.append(text[index:start + 1])
            index = start + 1


def html_text(text: str) -> str:
    """Contract bullet (c): comments, raw elements, tags, then references."""
    text = remove_comments(text)
    text = remove_raw_elements(text)
    text = strip_tags(text)
    return unescape(text)


# --------------------------------------------------------------------------
# Normalization (contract bullet d)
# --------------------------------------------------------------------------

_WHITESPACE_TABLE: dict | None = None


def _whitespace_table() -> dict:
    """Map every code point whose `str.isspace()` is true to None (delete)."""
    return {code: None for code in range(0x110000) if chr(code).isspace()}


def normalize(text: str) -> str:
    """NFKC (S091) and then drop every character whose `str.isspace()` is true."""
    global _WHITESPACE_TABLE
    if _WHITESPACE_TABLE is None:
        _WHITESPACE_TABLE = _whitespace_table()
    return unicodedata.normalize("NFKC", text).translate(_WHITESPACE_TABLE)


# --------------------------------------------------------------------------
# Manifest handling
# --------------------------------------------------------------------------


def finding(check, reason: str, target=None) -> dict:
    return {"check": check, "reason": reason, "target": target}


def parse_content_type(content_type: str):
    """Return (media type, parameters) -- media type ASCII-lowercased."""
    parts = content_type.split(";")
    media = ascii_lower(parts[0].strip())
    params: dict[str, str] = {}
    for part in parts[1:]:
        if "=" not in part:
            continue
        name, value = part.split("=", 1)
        key = ascii_lower(name.strip())
        if key and key not in params:
            params[key] = value.strip()
    return media, params


def body_path(manifest_dir: str, body: str):
    """Resolve a body path inside the manifest directory; None when it is not a
    regular file inside that directory."""
    if not body or os.path.isabs(body):
        return None
    root = os.path.normpath(manifest_dir)
    candidate = os.path.normpath(os.path.join(root, body))
    if candidate != root and not candidate.startswith(root + os.sep):
        return None
    try:
        if not os.path.isfile(candidate):
            return None
    except (OSError, ValueError):
        return None
    return candidate


def check_id_of(check):
    if isinstance(check, dict):
        cid = check.get("id")
        if isinstance(cid, str) and cid:
            return cid
    return None


def validate_check(check, manifest_dir: str) -> bool:
    """Every manifest rule of the contract, bullets (a)-(g)."""
    if not isinstance(check, dict):
        return False
    cid = check.get("id")
    if not isinstance(cid, str) or not cid:
        return False
    url = check.get("url")
    if not isinstance(url, str) or not url:
        return False
    scheme, authority, _path, _query, _fragment = parse_uri_ref(url)
    if scheme is None or ascii_lower(scheme) not in ("http", "https"):
        return False
    if not host_of(authority):
        return False
    quote = check.get("quote")
    if not isinstance(quote, str) or not quote:
        return False
    hops = check.get("hops")
    if not isinstance(hops, list) or not hops:
        return False
    last_index = len(hops) - 1
    for index, hop in enumerate(hops):
        if not isinstance(hop, dict):
            return False
        status = hop.get("status")
        if isinstance(status, bool) or not isinstance(status, int):
            return False
        if status < 100 or status > 599:
            return False
        is_redirect = status in REDIRECT_STATUSES
        location = hop.get("location")
        if location is not None and not isinstance(location, str):
            return False
        if index == last_index:
            # The last hop is not a redirect; it needs no location.
            if is_redirect:
                return False
        else:
            # Every hop but the last is a redirect and needs its location.
            if not is_redirect:
                return False
            if not isinstance(location, str) or not location:
                return False
    if hops[last_index]["status"] == 200:
        content_type = check.get("contentType")
        if not isinstance(content_type, str):
            return False
        body = check.get("body")
        if not isinstance(body, str) or body_path(manifest_dir, body) is None:
            return False
    return True


# --------------------------------------------------------------------------
# Evaluation
# --------------------------------------------------------------------------


def moved_target(check) -> str | None:
    """The resolved location of the last hop of the leading permanent run."""
    hops = check["hops"]
    if not hops or hops[0].get("status") not in PERMANENT_STATUSES:
        return None
    end = 0
    while end < len(hops) and hops[end].get("status") in PERMANENT_STATUSES:
        end += 1
    base = check["url"]
    resolved = None
    for index in range(end):
        resolved = resolve_reference(base, hops[index]["location"])
        base = resolved
    return resolved


def evaluate_check(check, manifest_dir: str) -> list:
    """Findings for one valid check."""
    findings = []
    cid = check["id"]
    target = moved_target(check)
    if target is not None:
        findings.append(finding(cid, "moved", target))
    hops = check["hops"]
    status = hops[-1]["status"]
    if 200 <= status < 300:
        media, params = parse_content_type(check["contentType"])
        if media in HTML_MEDIA_TYPES:
            mode = "html"
        elif media == PLAIN_MEDIA_TYPE:
            mode = "plain"
        else:
            findings.append(finding(cid, "unsupported_type"))
            return findings
        path = body_path(manifest_dir, check["body"])
        try:
            with open(path, "rb") as handle:
                data = handle.read()
        except OSError:
            findings.append(finding(cid, "check_invalid"))
            return findings
        codec, payload = pick_encoding(data, params.get("charset"))
        if codec is None:
            findings.append(finding(cid, "charset_unsupported"))
            return findings
        text = payload.decode(codec, errors="replace")
        if mode == "html":
            text = html_text(text)
        if normalize(check["quote"]) not in normalize(text):
            findings.append(finding(cid, "quote_missing"))
        return findings
    if status in GONE_STATUSES:
        findings.append(finding(cid, "gone"))
    else:
        findings.append(finding(cid, "http_error"))
    return findings


def load_manifest(path: str):
    """Return the manifest object or None when it is unusable."""
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError:
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    try:
        data = json.loads(text)
    except (ValueError, RecursionError):
        return None
    if not isinstance(data, dict):
        return None
    version = data.get("version")
    if isinstance(version, bool) or not isinstance(version, (int, float)) or version != 1:
        return None
    checks = data.get("checks")
    if not isinstance(checks, list):
        return None
    return data


def decide_verdict(findings) -> str:
    for item in findings:
        if item.get("reason") in BLOCKING_REASONS:
            return VERDICT_COULD_NOT_EVALUATE
    if findings:
        return VERDICT_FAILED_POLICY
    return VERDICT_CLEAN


def emit(verdict: str, checks_evaluated: int, findings) -> int:
    report = {
        "version": REPORT_VERSION,
        "verdict": verdict,
        "checksEvaluated": checks_evaluated,
        "findings": findings,
    }
    sys.stdout.write(json.dumps(report) + "\n")
    if verdict == VERDICT_CLEAN:
        return EXIT_CLEAN
    if verdict == VERDICT_FAILED_POLICY:
        return EXIT_FAILED_POLICY
    return EXIT_COULD_NOT_EVALUATE


def parse_args(argv) -> str | None:
    """The manifest path, or None on a usage error."""
    path = None
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--manifest":
            index += 1
            if index >= len(argv) or path is not None:
                return None
            path = argv[index]
        elif arg.startswith("--manifest="):
            if path is not None:
                return None
            path = arg[len("--manifest="):]
        else:
            return None
        index += 1
    if not path:
        return None
    return path


def main(argv) -> int:
    path = parse_args(argv)
    if path is None:
        sys.stderr.write("usage: source_recheck.py --manifest PATH\n")
        return EXIT_USAGE
    manifest = load_manifest(path)
    if manifest is None:
        return emit(VERDICT_COULD_NOT_EVALUATE, 0, [finding(None, "input_invalid")])
    manifest_dir = os.path.dirname(os.path.abspath(path))
    findings = []
    evaluated = 0
    for check in manifest["checks"]:
        if not validate_check(check, manifest_dir):
            findings.append(finding(check_id_of(check), "check_invalid"))
            continue
        evaluated += 1
        findings.extend(evaluate_check(check, manifest_dir))
    return emit(decide_verdict(findings), evaluated, findings)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
