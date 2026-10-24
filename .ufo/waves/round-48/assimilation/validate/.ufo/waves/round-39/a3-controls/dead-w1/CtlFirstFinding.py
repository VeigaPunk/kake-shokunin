#!/usr/bin/env python3
"""CtlFirstFinding — round-39 C1 control.

Shape: a reasonable implementation of .ufo/waves/round-39/c1-contract.md that
stops at the FIRST finding per file: at most one (code, entry) pair is reported
per manifest check, so the per-file work of enumerating every offending entry
is skipped.  Everything else (manifest validation, encoding/doctype/parse gates,
scope arithmetic, value grammars) is done properly, so this control isolates
exactly one question: does the sealed key ever require two findings in one
check?

Usage: python3 control.py --manifest <path>
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date
from decimal import Decimal, InvalidOperation
from urllib.parse import urlsplit

SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
SM = "{%s}" % SM_NS
MAX_BYTES = 52428800
MAX_ENTRIES = 50000
XML_WS = " \t\r\n"

DECL_RE = re.compile(r"^<\?xml\s+([^?]*)\?>")
ENC_ATTR_RE = re.compile(r"encoding\s*=\s*(?:\"([^\"]*)\"|'([^']*)')")
LASTMOD_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})"
    r"(?:T(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?(Z|[+-]\d{2}:\d{2}))?$"
)
PRIORITY_RE = re.compile(r"^[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)$")
CHANGEFREQ = ("always", "hourly", "daily", "weekly", "monthly", "yearly", "never")


# ---------------------------------------------------------------- url helpers
def split_url(u):
    try:
        return urlsplit(u)
    except ValueError:
        return None


def host_of(p):
    if p is None:
        return None
    try:
        h = p.hostname
    except ValueError:
        return None
    return h.lower() if h else None


def port_of(p):
    if p is None:
        return None
    try:
        port = p.port
    except ValueError:
        return None
    if port is None:
        scheme = (p.scheme or "").lower()
        if scheme == "http":
            return 80
        if scheme == "https":
            return 443
        return None
    return port


def is_abs_http(u):
    """Rule 4 / rule 22: absolute http(s) URL with a non-empty host."""
    p = split_url(u)
    if p is None:
        return False
    if (p.scheme or "").lower() not in ("http", "https"):
        return False
    if not p.netloc:
        return False
    return bool(host_of(p))


def scope_ok(loc_p, su_p, kind):
    """Rules 24-27."""
    if loc_p is None or su_p is None:
        return False
    if (loc_p.scheme or "").lower() != (su_p.scheme or "").lower():
        return False
    if host_of(loc_p) != host_of(su_p):
        return False
    if port_of(loc_p) != port_of(su_p):
        return False
    if kind == "sitemapindex":          # rule 27: origin only
        return True
    loc_path = loc_p.path or "/"        # rule 25: empty path reads as "/"
    su_path = su_p.path or "/"
    prefix = su_path[: su_path.rfind("/") + 1]   # directory up to last "/"
    return loc_path.startswith(prefix)           # rule 26: as written


# ------------------------------------------------------------- value grammars
def trim(v):
    if v is None:
        return ""
    return v.strip(XML_WS)


def lastmod_ok(v):
    m = LASTMOD_RE.match(v)
    if not m:
        return False
    try:
        date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return False
    hh, mi, ss, tzd = m.group(4), m.group(5), m.group(6), m.group(8)
    if hh is None:
        return True                      # date-only form
    if int(hh) > 23 or int(mi) > 59:
        return False
    if ss is not None and int(ss) > 59:
        return False
    if tzd != "Z":
        if int(tzd[1:3]) > 23 or int(tzd[4:6]) > 59:
            return False
    return True


def priority_ok(v):
    if not PRIORITY_RE.match(v):
        return False
    try:
        d = Decimal(v)
    except InvalidOperation:
        try:
            d = Decimal(v + "0")
        except InvalidOperation:
            return False
    return Decimal(0) <= d <= Decimal(1)


# ------------------------------------------------------------------ xml gates
def has_doctype(text):
    i, n = 0, len(text)
    while i < n:
        j = text.find("<!", i)
        if j < 0:
            return False
        if text.startswith("<!--", j):
            k = text.find("-->", j + 4)
            if k < 0:
                return False
            i = k + 3
            continue
        if text.startswith("<![CDATA[", j):
            k = text.find("]]>", j + 9)
            if k < 0:
                return False
            i = k + 3
            continue
        if text.startswith("<!DOCTYPE", j):
            return True
        i = j + 2
    return False


# ----------------------------------------------------------------- the audit
def audit(data, sitemap_url):
    """Return the first finding of this file as [(code, entry)], or []."""
    if len(data) > MAX_BYTES:                       # rule 19
        return [("too_large", None)]
    body = data[3:] if data.startswith(b"\xef\xbb\xbf") else data
    try:
        text = body.decode("utf-8")                 # rule 6
    except UnicodeDecodeError:
        return [("encoding_invalid", None)]
    m = DECL_RE.match(text)                         # rule 7
    if m:
        em = ENC_ATTR_RE.search(m.group(1))
        if em:
            enc = em.group(1) if em.group(1) is not None else em.group(2)
            if enc.lower() != "utf-8":
                return [("encoding_invalid", None)]
    if has_doctype(text):                          # rule 9
        return [("doctype_present", None)]
    try:
        root = ET.fromstring(data)                  # rule 8
    except (ET.ParseError, ValueError):
        return [("xml_malformed", None)]

    if root.tag == SM + "urlset":                   # rule 10
        kind, entry_tag = "urlset", SM + "url"
    elif root.tag == SM + "sitemapindex":
        kind, entry_tag = "sitemapindex", SM + "sitemap"
    else:
        return [("root_invalid", None)]

    entries, unexpected_root = [], False
    for child in root:
        t = child.tag
        if not isinstance(t, str) or not t.startswith(SM):
            continue                                # rule 14: other namespaces ignored
        if t == entry_tag:
            entries.append(child)                   # rule 11
        else:
            unexpected_root = True                  # rule 13
    if not entries:
        return [("no_entries", None)]               # rule 12
    if unexpected_root:
        return [("element_unexpected", None)]       # rule 13
    if len(entries) > MAX_ENTRIES:                 # rule 20
        return [("too_many_entries", None)]

    su_p = split_url(sitemap_url)
    for idx, e in enumerate(entries, 1):
        kids = [(c.tag, c) for c in e if isinstance(c.tag, str)]
        locs = [c for t, c in kids if t == SM + "loc"]
        if not locs:
            return [("loc_missing", idx)]           # rule 15
        if len(locs) > 1:
            return [("loc_repeated", idx)]           # rule 15
        if kind == "urlset":
            allowed = {SM + "loc", SM + "lastmod", SM + "changefreq", SM + "priority"}
            single = ("lastmod", "changefreq", "priority")
        else:
            allowed = {SM + "loc", SM + "lastmod"}
            single = ("lastmod",)
        for fname in single:                        # rule 16
            if sum(1 for t, _ in kids if t == SM + fname) > 1:
                return [("field_repeated", idx)]
        for t, _ in kids:                           # rule 17
            if t.startswith(SM) and t not in allowed:
                return [("element_unexpected", idx)]

        locv = trim(locs[0].text)
        if not is_abs_http(locv):
            return [("loc_not_absolute", idx)]      # rule 22
        if len(locv) >= 2048:
            return [("loc_too_long", idx)]           # rule 23
        if not scope_ok(split_url(locv), su_p, kind):
            return [("loc_out_of_scope", idx)]       # rules 25, 27

        for t, c in kids:                           # rule 28-30
            if t == SM + "lastmod":
                if not lastmod_ok(trim(c.text)):
                    return [("lastmod_invalid", idx)]
                break
        if kind == "urlset":
            for t, c in kids:                       # rule 31
                if t == SM + "changefreq":
                    if trim(c.text) not in CHANGEFREQ:
                        return [("changefreq_invalid", idx)]
                    break
            for t, c in kids:                       # rule 32
                if t == SM + "priority":
                    if not priority_ok(trim(c.text)):
                        return [("priority_invalid", idx)]
                    break
    return []


# ------------------------------------------------------------------- manifest
def emit(doc, code):
    sys.stdout.write(json.dumps(doc) + "\n")
    sys.stdout.flush()
    sys.exit(code)


def emit_invalid():
    emit({"version": 1, "verdict": "could-not-evaluate",
          "error": "input_invalid", "checks": []}, 2)


def main(argv):
    if len(argv) != 2 or argv[0] != "--manifest":
        return 64                                    # rule 2
    mpath = argv[1]
    try:
        with open(mpath, "rb") as fh:
            raw = fh.read()
    except OSError:
        emit_invalid()
    try:
        manifest = json.loads(raw.decode("utf-8-sig"))
    except Exception:
        emit_invalid()
    if not isinstance(manifest, dict):
        emit_invalid()
    ver = manifest.get("version")
    if not isinstance(ver, int) or isinstance(ver, bool) or ver != 1:
        emit_invalid()
    checks = manifest.get("checks")
    if not isinstance(checks, list) or not checks:
        emit_invalid()

    base = os.path.dirname(os.path.abspath(mpath))
    results, seen = [], set()
    for ch in checks:
        if not isinstance(ch, dict):
            results.append({"id": None, "status": "error",
                            "error": "check_invalid", "findings": []})
            continue
        cid = ch.get("id")
        id_out = cid if isinstance(cid, str) else None
        fv, su = ch.get("file"), ch.get("sitemapUrl")
        dup = isinstance(cid, str) and cid in seen
        ok = (isinstance(cid, str) and isinstance(fv, str) and isinstance(su, str))
        if ok:
            segs = fv.split("/")
            if fv.startswith("/") or ".." in segs:
                ok = False
        if ok and not is_abs_http(su):
            ok = False
        if ok and dup:
            ok = False
        if isinstance(cid, str):
            seen.add(cid)
        if not ok:
            results.append({"id": id_out, "status": "error",
                            "error": "check_invalid", "findings": []})
            continue
        path = fv if os.path.isabs(fv) else os.path.join(base, fv)
        try:
            with open(path, "rb") as fh:
                data = fh.read()
        except OSError:
            results.append({"id": id_out, "status": "error",
                            "error": "file_unreadable", "findings": []})
            continue
        findings = audit(data, su)
        results.append({"id": id_out,
                        "status": "findings" if findings else "clean",
                        "error": None,
                        "findings": [{"code": c, "entry": e} for c, e in findings]})
    any_error = any(r["status"] == "error" for r in results)
    any_find = any(r["findings"] for r in results)
    verdict = "could-not-evaluate" if any_error else ("failed-policy" if any_find else "clean")
    emit({"version": 1, "verdict": verdict, "checks": results},
         2 if any_error else (1 if any_find else 0))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
