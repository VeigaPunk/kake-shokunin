#!/usr/bin/env python3
"""Round-39 C1 control: regex-only sitemap reader (control shape "regex reader").

No XML parser at all. Document structure is recovered by scanning
tag-shaped tokens with regular expressions; every value rule (g)-(k) is decided
by regular expressions or plain string arithmetic.
Standard library only (json, re, os, sys, datetime, decimal, urllib.parse).

Deliberate gaps (see NOTE.md):
  * namespace syntax and general XML 1.0 well-formedness remain approximate;
  * comments are skipped as markup, but their text never becomes an entry;
  * well-formedness is the tag-balance approximation a regex reader can make,
    not XML 1.0 conformance.
"""
import json
import os
import re
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from urllib.parse import urlsplit

MAX_BYTES = 52428800
MAX_ENTRIES = 50000
WS = " \t\r\n"

TOKEN_RE = re.compile(
    r"<!--.*?-->"
    r"|<!\[CDATA\[.*?\]\]>"
    r"|<\?.*?\?>"
    r"|<!DOCTYPE\b[^>\[]*(?:\[.*?\])?[^>]*>"
    r"|</\s*[A-Za-z_][^>]*>"
    r"|<[A-Za-z_](?:[^>\"']|\"[^\"]*\"|'[^']*')*>",
    re.S,
)

CHANGFREQS = ("always", "hourly", "daily", "weekly", "monthly", "yearly", "never")
PRIORITY_RE = re.compile(r"^[+-]?([0-9]+(\.[0-9]*)?|\.[0-9]+)$")
LASTMOD_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
LASTMOD_DT_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2})(\.\d+)?)?(Z|[+-]\d{2}:\d{2})$"
)
XMLDECL_RE = re.compile(r"^<\?xml\b[^>]*\?>", re.S)
XMLDECL_ENC_RE = re.compile(r"\bencoding\s*=\s*[\"']([^\"']*)[\"']", re.S)


class Node(object):
    __slots__ = ("name", "children", "text", "ns")

    def __init__(self, name):
        self.name = name
        self.children = []
        self.text = []


def local(name):
    return name.rsplit("}", 1)[-1].split(":")[-1] if name.startswith("http://www.sitemaps.org/schemas/sitemap/0.9}") else None


def trim(value):
    return value.strip(WS)

def unescape(value):
    entities = {"amp": "&", "lt": "<", "gt": ">", "quot": '"', "apos": "'"}
    def replace(m):
        if (key := m[1]) is None: raise ValueError("invalid entity")
        if key in entities: return entities[key]
        return chr(int(key[2:], 16) if key.startswith("#x") else int(key[1:]))
    return re.sub(r"&(#x[0-9A-Fa-f]+|#[0-9]+|amp|lt|gt|quot|apos);|&", replace, value)

# --------------------------------------------------------------------- structure

def scan(text, decode_entities=True):
    """Regex token scan -> (root Node, None) or (None, reason)."""
    root = None
    stack = []
    pos = 0
    for m in TOKEN_RE.finditer(text):
        chunk = text[pos:m.start()]
        chunk = unescape(chunk) if decode_entities else chunk
        pos = m.end()
        tok = m.group(0)
        if stack:
            stack[-1].text.append(chunk)
        elif chunk.strip(WS):
            return None, "text outside root"
        if tok.startswith("<!--") or tok.startswith("<?") or tok.startswith("<!DOCTYPE"):
            continue
        if tok.startswith("<![CDATA["):
            if stack:
                stack[-1].text.append(tok[9:-3])
            continue
        if tok.startswith("</"):
            inner = tok[2:-1].strip()
            name = inner.split()[0] if inner else ""
            if not stack:
                return None, "close without open"
            if stack[-1].name.rsplit("}", 1)[-1] != name:
                return None, "mismatched close tag"
            stack.pop()
            continue
        body = tok[1:-1]
        selfclose = body.rstrip().endswith("/")
        if selfclose:
            body = body.rstrip()[:-1]
        parts = body.split()
        name = parts[0] if parts else ""
        if not name:
            return None, "empty element name"
        ns = dict(stack[-1].ns) if stack else {"xml": "http://www.w3.org/XML/1998/namespace"}
        for attr, quote, value in re.findall(r"""\s+([:\w.-]+)\s*=\s*(["'])(.*?)\2""", body, re.S):
            if attr == "xmlns" or attr.startswith("xmlns:"): ns[attr.partition(":")[2]] = unescape(value) if decode_entities else value
        prefix, sep, lname = name.rpartition(":")
        if decode_entities and sep and not ns.get(prefix): return None, "unbound namespace"
        node = Node(ns.get(prefix if sep else "", "") + "}" + name); node.ns = ns
        if stack:
            stack[-1].children.append(node)
        elif root is None:
            root = node
        else:
            return None, "more than one root element"
        if not selfclose:
            stack.append(node)
    tail = text[pos:]
    if stack:
        return None, "unclosed element"
    if tail.strip(WS):
        return None, "trailing text after root"
    if root is None:
        return None, "no root element"
    return root, None


def node_value(node):
    return trim("".join(node.text))


def has_doctype(text):
    """True when a doctype declaration is present as markup (not inside a comment)."""
    for m in TOKEN_RE.finditer(text):
        tok = m.group(0)
        if tok.startswith("<!DOCTYPE"):
            return True
    return False


# ------------------------------------------------------------------------- urls

def is_absolute_http_url(u):
    if not u:
        return False
    try:
        p = urlsplit(u)
    except ValueError:
        return False
    if p.scheme.lower() not in ("http", "https"):
        return False
    if not p.netloc:
        return False
    try:
        host = p.hostname
    except ValueError:
        return False
    return bool(host)


def url_parts(u):
    p = urlsplit(u)
    scheme = p.scheme.lower()
    try:
        host = (p.hostname or "").lower()
    except ValueError:
        host = ""
    try:
        port = p.port
    except ValueError:
        port = None
    if port is None:
        port = 80 if scheme == "http" else 443
    path = p.path
    if path == "":
        path = "/"
    return scheme, host, port, path


def scope_ok(loc_url, base_url, is_index):
    ls, lh, lp, lpath = url_parts(loc_url)
    bs, bh, bp, bpath = url_parts(base_url)
    if ls != bs or lh != bh or lp != bp:
        return False
    if is_index:
        return True
    idx = bpath.rfind("/")
    prefix = bpath[: idx + 1]
    return lpath.startswith(prefix)


# ----------------------------------------------------------------- value rules

def lastmod_ok(value):
    m = LASTMOD_DT_RE.match(value)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        hh, mi = int(m.group(4)), int(m.group(5))
        ss = int(m.group(6)) if m.group(6) else 0
        tzd = m.group(8)
        if not (1 <= mo <= 12) or hh > 23 or mi > 59 or ss > 59:
            return False
        try:
            date(y, mo, d)
        except ValueError:
            return False
        if tzd != "Z":
            if int(tzd[1:3]) > 23 or int(tzd[4:6]) > 59:
                return False
        return True
    m = LASTMOD_DATE_RE.match(value)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if not (1 <= mo <= 12):
            return False
        try:
            date(y, mo, d)
        except ValueError:
            return False
        return True
    return False


def priority_ok(value):
    if not PRIORITY_RE.match(value):
        return False
    try:
        d = Decimal(value)
    except InvalidOperation:
        return False
    return Decimal(0) <= d <= Decimal(1)


# ------------------------------------------------------------------ file audit

def audit_file(raw, sitemap_url):
    """Return findings as a list of (code, entry_or_None)."""
    findings = []

    if len(raw) > MAX_BYTES:
        return [("too_large", None)]

    body = raw[3:] if raw.startswith(b"\xef\xbb\xbf") else raw
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError:
        return [("encoding_invalid", None)]

    decl = XMLDECL_RE.match(text)
    if decl:
        enc = XMLDECL_ENC_RE.search(decl.group(0))
        if enc and enc.group(1).strip().upper() != "UTF-8":
            return [("encoding_invalid", None)]

    try: root, _why = scan(text, not has_doctype(text))
    except (ValueError, OverflowError): root = None
    if root is None:
        return [("xml_malformed", None)]

    if has_doctype(text):
        return [("doctype_present", None)]

    rname = local(root.name)
    if rname not in ("urlset", "sitemapindex"):
        return [("root_invalid", None)]

    is_index = rname == "sitemapindex"
    entry_tag = "sitemap" if is_index else "url"

    entries = [c for c in root.children if local(c.name) == entry_tag]
    for c in root.children:
        if local(c.name) not in (None, entry_tag):
            findings.append(("element_unexpected", None))

    if not entries:
        findings.append(("no_entries", None))
    if len(entries) > MAX_ENTRIES:
        findings.append(("too_many_entries", None))

    allowed = ("loc", "lastmod") if is_index else ("loc", "lastmod", "changefreq", "priority")

    for idx, entry in enumerate(entries, start=1):
        kids = entry.children
        for k in kids:
            if local(k.name) is not None and local(k.name) not in allowed:
                findings.append(("element_unexpected", idx))

        locs = [k for k in kids if local(k.name) == "loc"]
        loc_value = None
        if not locs:
            findings.append(("loc_missing", idx))
        elif len(locs) > 1:
            findings.append(("loc_repeated", idx))
        else:
            loc_value = node_value(locs[0])

        values = {}
        for fname in allowed:
            if fname == "loc":
                continue
            same = [k for k in kids if local(k.name) == fname]
            if len(same) > 1:
                findings.append(("field_repeated", idx))
            elif len(same) == 1:
                values[fname] = node_value(same[0])

        if loc_value is not None:
            if len(loc_value) >= 2048:
                findings.append(("loc_too_long", idx))
            if not is_absolute_http_url(loc_value):
                findings.append(("loc_not_absolute", idx))
            elif not scope_ok(loc_value, sitemap_url, is_index):
                findings.append(("loc_out_of_scope", idx))

        lm = values.get("lastmod")
        if lm is not None and not lastmod_ok(lm):
            findings.append(("lastmod_invalid", idx))

        if not is_index:
            cf = values.get("changefreq")
            if cf is not None and cf not in CHANGFREQS:
                findings.append(("changefreq_invalid", idx))
            pr = values.get("priority")
            if pr is not None and not priority_ok(pr):
                findings.append(("priority_invalid", idx))

    return findings


# --------------------------------------------------------------------- manifest

def emit(doc, code):
    sys.stdout.write(json.dumps(doc) + "\n")
    return code


def input_invalid_doc():
    return {
        "version": 1,
        "verdict": "could-not-evaluate",
        "error": "input_invalid",
        "checks": [],
    }


def check_valid(chk, seen_ids):
    """Return (ok, id_or_None)."""
    if not isinstance(chk, dict):
        return False, None
    cid = chk.get("id")
    fid = chk.get("file")
    su = chk.get("sitemapUrl")
    if not isinstance(cid, str) or not isinstance(fid, str) or not isinstance(su, str):
        return False, (cid if isinstance(cid, str) else None)
    if cid in seen_ids:
        return False, cid
    if os.path.isabs(fid):
        return False, cid
    if any(part == ".." for part in fid.replace("\\", "/").split("/")):
        return False, cid
    if not is_absolute_http_url(su):
        return False, cid
    return True, cid


def main(argv):
    if len(argv) != 2 or argv[0] != "--manifest":
        return 64
    manifest_path = argv[1]
    try:
        with open(manifest_path, "rb") as fh:
            mraw = fh.read()
    except OSError:
        return emit(input_invalid_doc(), 2)
    try:
        man = json.loads(mraw.decode("utf-8"))
    except Exception:
        return emit(input_invalid_doc(), 2)
    if not isinstance(man, dict):
        return emit(input_invalid_doc(), 2)
    ver = man.get("version")
    if not isinstance(ver, int) or isinstance(ver, bool) or ver != 1:
        return emit(input_invalid_doc(), 2)
    checks = man.get("checks")
    if not isinstance(checks, list) or not checks:
        return emit(input_invalid_doc(), 2)

    base_dir = os.path.dirname(os.path.abspath(manifest_path))
    items = []
    seen_ids = set()
    any_error = False

    for chk in checks:
        ok, cid = check_valid(chk, seen_ids)
        if isinstance(chk, dict) and isinstance(chk.get("id"), str):
            seen_ids.add(chk["id"])
        if not ok:
            any_error = True
            items.append({"id": cid, "status": "error", "error": "check_invalid", "findings": []})
            continue
        path = os.path.join(base_dir, chk["file"])
        try:
            with open(path, "rb") as fh:
                raw = fh.read()
        except OSError:
            any_error = True
            items.append({"id": cid, "status": "error", "error": "file_unreadable", "findings": []})
            continue
        try:
            findings = audit_file(raw, chk["sitemapUrl"])
        except Exception:
            any_error = True
            items.append({"id": cid, "status": "error", "error": "check_invalid", "findings": []})
            continue
        out = [{"code": c, "entry": e} for c, e in findings]
        if out:
            items.append({"id": cid, "status": "findings", "error": None, "findings": out})
        else:
            items.append({"id": cid, "status": "clean", "error": None, "findings": []})

    if any_error:
        # Contract sentence 33 fixes the document shape for a run with error checks
        # ({"version", "verdict", "checks"}); the document-level "error" member is
        # specified only for the manifest-level input_invalid case (sentence 3).
        doc = {"version": 1, "verdict": "could-not-evaluate", "checks": items}
        return emit(doc, 2)
    if any(it["status"] == "findings" for it in items):
        doc = {"version": 1, "verdict": "failed-policy", "checks": items}
        return emit(doc, 1)
    doc = {"version": 1, "verdict": "clean", "checks": items}
    return emit(doc, 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
