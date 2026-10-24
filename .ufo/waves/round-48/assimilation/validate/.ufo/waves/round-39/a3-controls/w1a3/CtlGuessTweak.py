#!/usr/bin/env python3
"""C1 control: sitemap audit by text scanning + keyword heuristics.

Shape (deliberately NOT a parser):
  * the file is read as bytes, decoded, and the markup is walked with a
    hand-written character scanner (tags / attributes / comments / CDATA);
  * no XML library is imported (no xml.etree, no expat), no tree is built;
  * findings are emitted by keyword and regex scoring over the scanned text.

Usage:  python3 control.py --manifest <path>
"""

import json
import os
import re
import sys
from datetime import date
from urllib.parse import urlsplit

SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
XML_NS = "http://www.w3.org/XML/1998/namespace"
MAX_BYTES = 52428800
MAX_ENTRIES = 50000
XML_WS = " \t\r\n"

CHANGEFREQ = frozenset(
    ("always", "hourly", "daily", "weekly", "monthly", "yearly", "never")
)

_ENT_RE = re.compile(r"&(#[0-9]+|#x[0-9a-fA-F]+|amp|lt|gt|quot|apos);")
_BAD_CHAR = re.compile(
    u"[^\u0009\u000a\u000d\u0020-\ud7ff\ue000-\ufffd\U00010000-\U0010ffff]"
)
_PRIORITY_RE = re.compile(r"^[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)$")
_LASTMOD_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})"
    r"(?:T(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?(Z|[+-]\d{2}:\d{2}))?$"
)
_DECL_ENC_RE = re.compile(r"encoding\s*=\s*(\"([^\"]*)\"|'([^']*)')")


class Malformed(Exception):
    pass


# ---------------------------------------------------------------- text bits


def _check_chars(s):
    if _BAD_CHAR.search(s):
        raise Malformed("invalid character")


def _check_text(s):
    if "&" in s:
        if len(_ENT_RE.findall(s)) != s.count("&"):
            raise Malformed("bad entity reference")
    _check_chars(s)
    try:
        _check_chars(_expand(s))
    except (ValueError, OverflowError):
        raise Malformed("invalid character reference")


def _expand(s):
    """Expand the five predefined entities and numeric references."""
    if "&" not in s:
        return s

    def rep(m):
        ent = m.group(1)
        if ent.startswith("#x") or ent.startswith("#X"):
            return chr(int(ent[2:], 16))
        if ent.startswith("#"):
            return chr(int(ent[1:].lstrip("0") or "0"))
        return {"amp": "&", "lt": "<", "gt": ">", "quot": '"', "apos": "'"}[ent]

    return _ENT_RE.sub(rep, s)


def _is_name_start(c):
    return c == "_" or c == ":" or c.isalpha() or ord(c) > 127


def _is_name_char(c):
    return c in "_-.:" or c.isalnum() or ord(c) > 127


def _split_qname(name):
    if ":" in name:
        p, l = name.split(":", 1)
        if not p or not l:
            raise Malformed("bad qualified name")
        return p, l
    return "", name


# ---------------------------------------------------------------- scanner


def _scan_decl(text, pos):
    """End offset of a <! ... > declaration, honouring quotes and []."""
    i = pos + 2
    n = len(text)
    quote = None
    depth = 0
    while i < n:
        c = text[i]
        if quote:
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        elif c == ">" and depth <= 0:
            return i + 1
        i += 1
    raise Malformed("unterminated declaration")


def _parse_start_tag(text, pos):
    n = len(text)
    j = pos + 1
    if j >= n or not _is_name_start(text[j]):
        raise Malformed("bad element name")
    k = j
    while k < n and _is_name_char(text[k]):
        k += 1
    name = text[j:k]
    j = k
    attrs = []
    self_closing = False
    while True:
        while j < n and text[j] in XML_WS:
            j += 1
        if j >= n:
            raise Malformed("unterminated tag")
        c = text[j]
        if c == ">":
            j += 1
            break
        if c == "/":
            if j + 1 < n and text[j + 1] == ">":
                self_closing = True
                j += 2
                break
            raise Malformed("bad tag")
        if not _is_name_start(text[j]):
            raise Malformed("bad attribute name")
        k = j
        while k < n and _is_name_char(text[k]):
            k += 1
        aname = text[j:k]
        j = k
        while j < n and text[j] in XML_WS:
            j += 1
        if j >= n or text[j] != "=":
            raise Malformed("attribute without value")
        j += 1
        while j < n and text[j] in XML_WS:
            j += 1
        if j >= n or text[j] not in "\"'":
            raise Malformed("unquoted attribute value")
        q = text[j]
        j += 1
        end = text.find(q, j)
        if end == -1:
            raise Malformed("unterminated attribute value")
        if "<" in text[j:end]:
            raise Malformed("'<' in attribute value")
        _check_text(text[j:end])
        attrs.append((aname, _expand(text[j:end])))
        j = end + 1
    return name, attrs, self_closing, j


def scan(text):
    """Yield events; raise Malformed when the text is not well-formed XML."""
    n = len(text)
    pos = 0
    scopes = [{"": ""}]
    stack = []
    root_seen = False
    root_closed = False
    while pos < n:
        lt = text.find("<", pos)
        if lt == -1:
            chunk = text[pos:]
            _check_text(chunk)
            if chunk.strip():
                raise Malformed("text outside root")
            pos = n
            break
        if lt > pos:
            chunk = text[pos:lt]
            _check_text(chunk)
            if not stack:
                if chunk.strip():
                    raise Malformed("text before root")
            else:
                yield ("text", chunk)
            pos = lt
        if text.startswith("<!--", pos):
            end = text.find("-->", pos + 4)
            if end == -1:
                raise Malformed("unterminated comment")
            pos = end + 3
            continue
        if text.startswith("<![CDATA[", pos):
            end = text.find("]]>", pos + 9)
            if end == -1:
                raise Malformed("unterminated CDATA")
            _check_chars(text[pos + 9 : end])
            if stack:
                yield ("literal", text[pos + 9 : end])
            pos = end + 3
            continue
        if text.startswith("<!", pos):
            end = _scan_decl(text, pos)
            if text[pos : pos + 9].upper() == "<!DOCTYPE":
                yield ("doctype",)
            pos = end
            continue
        if text.startswith("<?", pos):
            end = text.find("?>", pos + 2)
            if end == -1:
                raise Malformed("unterminated processing instruction")
            target = re.match(r"([^\s?]+)", text[pos + 2 : end])
            if target and target.group(1).lower() == "xml":
                if pos != 0 or root_seen:
                    raise Malformed("misplaced XML declaration")
            pos = end + 2
            continue
        if text.startswith("</", pos):
            end = text.find(">", pos + 2)
            if end == -1:
                raise Malformed("unterminated end tag")
            name = text[pos + 2 : end].strip()
            if not stack:
                raise Malformed("end tag without open element")
            if stack[-1] != name:
                raise Malformed("mismatched end tag")
            stack.pop()
            scopes.pop()
            if not stack:
                root_closed = True
            yield ("end", name)
            pos = end + 1
            continue
        # start tag
        name, attrs, self_closing, newpos = _parse_start_tag(text, pos)
        seen = set()
        for aname, _av in attrs:
            if aname in seen:
                raise Malformed("duplicate attribute")
            seen.add(aname)
        scope = dict(scopes[-1])
        declared = set()
        for aname, aval in attrs:
            if aname == "xmlns":
                scope[""] = aval
                declared.add("")
            elif aname.startswith("xmlns:"):
                prefix = aname[6:]
                if not prefix or prefix in declared:
                    raise Malformed("duplicate namespace declaration")
                if prefix == "xml" and aval != XML_NS:
                    raise Malformed("bad xml prefix binding")
                scope[prefix] = aval
                declared.add(prefix)
        prefix, local = _split_qname(name)
        if prefix == "":
            uri = scope.get("", "")
        elif prefix == "xml":
            uri = XML_NS
        elif prefix in scope:
            uri = scope[prefix]
        else:
            raise Malformed("unbound namespace prefix")
        if not stack:
            if root_closed:
                raise Malformed("second root element")
            root_seen = True
        yield ("start", name, uri, local, self_closing)
        if not self_closing:
            stack.append(name)
            scopes.append(scope)
        elif not stack:
            root_closed = True
        pos = newpos
    if stack:
        raise Malformed("unclosed element")
    if not root_seen:
        raise Malformed("no root element")


# --------------------------------------------------------------- heuristics


def _valid_lastmod(v):
    m = _LASTMOD_RE.match(v)
    if not m:
        return False
    try:
        date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return False
    if m.group(4) is not None:
        if int(m.group(4)) > 23 or int(m.group(5)) > 59:
            return False
        if m.group(6) is not None and int(m.group(6)) > 59:
            return False
        tz = m.group(8)
        if tz != "Z":
            if int(tz[1:3]) > 23 or int(tz[4:6]) > 59:
                return False
    return True


def _valid_priority(v):
    if not _PRIORITY_RE.match(v):
        return False
    s = v.lstrip("+-")
    neg = v.startswith("-")
    if "." in s:
        ip, fp = s.split(".", 1)
    else:
        ip, fp = s, ""
    ip = ip.lstrip("0") or "0"
    zero = ip == "0" and not fp.strip("0")
    return (not neg or zero) and (ip == "0" or (ip == "1" and not fp.strip("0")))


def _parse_url(u):
    try:
        sp = urlsplit(u)
        scheme = sp.scheme.lower()
        host = sp.hostname
        port = sp.port
    except ValueError:
        return None
    if scheme not in ("http", "https"):
        return None
    if not host:
        return None
    if port is None:
        port = 80 if scheme == "http" else 443
    return (scheme, host.lower(), port, sp.path)


def _in_scope(loc, site, root_local):
    ls, lh, lp, lpath = loc
    ss, sh, sp_, spath = site
    if ls != ss or lh != sh or lp != sp_:
        return False
    if root_local == "urlset":
        idx = spath.rfind("/")
        prefix = spath[: idx + 1] if idx >= 0 else ""
        if not (lpath or "/").startswith(prefix):
            return False
    return True


# ------------------------------------------------------------------ audit


def audit_bytes(data, site):
    """Return the finding list for one sitemap file."""
    if len(data) > MAX_BYTES:
        return [("too_large", None)]
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return [("encoding_invalid", None)]
    if text.startswith("\ufeff"):
        text = text[1:]
    decl = re.match(r"<\?xml\s[^?]*\?>", text)
    if decl:
        em = _DECL_ENC_RE.search(decl.group(0))
        if em:
            val = em.group(2) if em.group(2) is not None else em.group(3)
            if val.lower() != "utf-8":
                return [("encoding_invalid", None)]

    try:
        events = list(scan(text))
    except Malformed:
        return [("xml_malformed", None)]

    file_findings = []
    doctype = False
    for ev in events:
        if ev[0] == "doctype":
            doctype = True
    if doctype:
        return [("doctype_present", None)]

    root = None
    entries = []
    stack = []
    for ev in events:
        kind = ev[0]
        if kind in ("text", "literal"):
            for fr in stack:
                if fr.get("capture") is not None:
                    fr["capture"].append(_expand(ev[1]) if kind == "text" else ev[1])
        elif kind == "start":
            _, name, uri, local, self_closing = ev
            if not stack:
                if uri != SM_NS or local not in ("urlset", "sitemapindex"):
                    return [("root_invalid", None)]
                root = local
                frame = {"kind": "root"}
            else:
                parent = stack[-1]
                if parent["kind"] == "root":
                    want = "url" if root == "urlset" else "sitemap"
                    if uri == SM_NS and local == want:
                        frame = {
                            "kind": "entry",
                            "index": len(entries) + 1,
                            "counts": {},
                            "values": {},
                        }
                        entries.append(frame)
                    elif uri == SM_NS:
                        file_findings.append(("element_unexpected", None))
                        frame = {"kind": "other"}
                    else:
                        frame = {"kind": "other"}
                elif parent["kind"] == "entry":
                    allowed = (
                        ("loc", "lastmod", "changefreq", "priority")
                        if root == "urlset"
                        else ("loc", "lastmod")
                    )
                    if uri == SM_NS and local in allowed:
                        par = parent
                        par["counts"][local] = par["counts"].get(local, 0) + 1
                        frame = {"kind": "value", "field": local, "capture": []}
                    elif uri == SM_NS:
                        file_findings.append(
                            ("element_unexpected", parent["index"])
                        )
                        frame = {"kind": "other"}
                    else:
                        frame = {"kind": "other"}
                else:
                    frame = {"kind": "other"}
            if not self_closing:
                stack.append(frame)
        elif kind == "end":
            frame = stack.pop()
            if frame.get("kind") == "value":
                parent = stack[-1]
                val = "".join(frame["capture"])
                val = val.replace("\r\n", "\n").replace("\r", "\n")
                val = val.strip(XML_WS)
                if frame["field"] not in parent["values"]:
                    parent["values"][frame["field"]] = val

    if not entries:
        file_findings.append(("no_entries", None))
    if len(entries) > MAX_ENTRIES:
        file_findings.append(("too_many_entries", None))

    findings = list(file_findings)
    for e in entries:
        idx = e["index"]
        counts = e["counts"]
        values = e["values"]
        nloc = counts.get("loc", 0)
        if nloc == 0:
            findings.append(("loc_missing", idx))
        elif nloc > 1:
            findings.append(("loc_repeated", idx))
        else:
            loc = values.get("loc", "")
            if len(loc) >= 2048:
                findings.append(("loc_too_long", idx))
            info = _parse_url(loc)
            if info is None:
                findings.append(("loc_not_absolute", idx))
            elif site is not None and not _in_scope(info, site, root):
                findings.append(("loc_out_of_scope", idx))
        n = counts.get("lastmod", 0)
        if n > 1:
            findings.append(("field_repeated", idx))
        elif n == 1 and not _valid_lastmod(values.get("lastmod", "")):
            findings.append(("lastmod_invalid", idx))
        if root == "urlset":
            n = counts.get("changefreq", 0)
            if n > 1:
                findings.append(("field_repeated", idx))
            elif n == 1 and values.get("changefreq", "") not in CHANGEFREQ:
                findings.append(("changefreq_invalid", idx))
            n = counts.get("priority", 0)
            if n > 1:
                findings.append(("field_repeated", idx))
            elif n == 1 and not _valid_priority(values.get("priority", "")):
                findings.append(("priority_invalid", idx))
    return findings


# ---------------------------------------------------------------- manifest


def _check_ok(obj, seen_ids):
    """Return (id, error) for one manifest check."""
    if not isinstance(obj, dict):
        return None, "check_invalid"
    cid = obj.get("id")
    f = obj.get("file")
    u = obj.get("sitemapUrl")
    if not isinstance(cid, str) or not isinstance(f, str) or not isinstance(u, str):
        return (cid if isinstance(cid, str) else None), "check_invalid"
    if cid in seen_ids:
        return cid, "check_invalid"
    if f.startswith("/") or f.startswith("\\") or os.path.isabs(f):
        return cid, "check_invalid"
    if ".." in f.replace("\\", "/").split("/"):
        return cid, "check_invalid"
    info = _parse_url(u)
    if info is None:
        return cid, "check_invalid"
    return cid, None


def run_manifest(path):
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
        doc = json.loads(raw)
    except Exception:
        return None
    if not isinstance(doc, dict):
        return None
    version = doc.get("version")
    if isinstance(version, bool) or not isinstance(version, int) or version != 1:
        return None
    checks = doc.get("checks")
    if not isinstance(checks, list) or not checks:
        return None
    base = os.path.dirname(os.path.abspath(path))
    out = []
    seen_ids = set()
    for obj in checks:
        cid, err = _check_ok(obj, seen_ids)
        if isinstance(obj, dict) and isinstance(obj.get("id"), str):
            seen_ids.add(obj["id"])
        if err:
            out.append(
                {"id": cid, "status": "error", "error": err, "findings": []}
            )
            continue
        target = os.path.join(base, obj["file"])
        try:
            with open(target, "rb") as fh:
                data = fh.read()
        except OSError:
            out.append(
                {
                    "id": cid,
                    "status": "error",
                    "error": "file_unreadable",
                    "findings": [],
                }
            )
            continue
        site = _parse_url(obj["sitemapUrl"])
        findings = audit_bytes(data, site)
        out.append(
            {
                "id": cid,
                "status": "findings" if findings else "clean",
                "error": None,
                "findings": [
                    {"code": c, "entry": n} for (c, n) in findings
                ],
            }
        )
    return out


def main(argv):
    if len(argv) != 2 or argv[0] != "--manifest":
        return 64
    checks = run_manifest(argv[1])
    if checks is None:
        sys.stdout.write(
            json.dumps(
                {
                    "version": 1,
                    "verdict": "could-not-evaluate",
                    "error": "input_invalid",
                    "checks": [],
                }
            )
            + "\n"
        )
        return 2
    if any(c["status"] == "error" for c in checks):
        verdict = "could-not-evaluate"
        code = 2
    elif any(c["findings"] for c in checks):
        verdict = "failed-policy"
        code = 1
    else:
        verdict = "clean"
        code = 0
    sys.stdout.write(
        json.dumps({"version": 1, "verdict": verdict, "checks": checks}) + "\n"
    )
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
