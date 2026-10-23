#!/usr/bin/env python3
"""CONTROL (round-39 C1) -- shallow stdlib reader.

Shape: xml.etree.ElementTree parse + root name/namespace check + entry count only.

Deliberately skipped (the "work" this control does not do):
  * every entry-level rule: (15) loc_missing/loc_repeated, (16) field_repeated,
    (17) element_unexpected inside an entry;
  * (21)-(23) loc form, (24)-(27) loc scope, (28)-(30) lastmod, (31) changefreq,
    (32) priority.
No value of any loc/lastmod/changefreq/priority element is ever read.

Kept (everything a shallow parse gives away):
  * (3)-(5) manifest handling and check errors, (6)-(7) encoding, (8) well-formedness,
    (9) doctype, (10) root, (12)/(13) file-level entry facts, (19)/(20) limits,
    (33) output shape, (34) verdict and exit code.

Standard library only; no network; no file outside the manifest's directory.
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
MAX_BYTES = 52428800
MAX_ENTRIES = 50000
BOM = b"\xef\xbb\xbf"


# ---------------------------------------------------------------- output ----
def emit(doc):
    sys.stdout.write(json.dumps(doc) + "\n")
    sys.stdout.flush()


def input_invalid():
    emit({"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid",
          "checks": []})
    return 2


# --------------------------------------------------------------- helpers ----
def is_abs_http_url(value):
    """Absolute http/https URL with a non-empty host (contract sentence 4)."""
    try:
        parts = urlsplit(value)
    except ValueError:
        return False
    if parts.scheme.lower() not in ("http", "https"):
        return False
    try:
        host = parts.hostname
    except ValueError:
        return False
    return bool(host)


def has_dotdot_segment(path):
    """POSIX path segments only: a '..' segment is a traversal (contract sentence 4)."""
    for seg in path.split("/"):
        if seg == "..":
            return True
    return False


def decl_of(text):
    """The XML declaration text (or '').

    A declaration is '<?xml' followed by whitespace and ending in '?>'.
    """
    if not text.startswith("<?xml"):
        return ""
    if len(text) > 5 and text[5] not in " \t\r\n":
        return ""
    end = text.find("?>")
    return text[:end + 2] if end != -1 else text[:200]


def declared_encoding(text):
    """Value of the encoding pseudo-attribute in the XML declaration, or None."""
    m = re.search(r"encoding\s*=\s*(?:\"([^\"]*)\"|'([^']*)')", decl_of(text))
    if not m:
        return None
    return m.group(1) if m.group(1) is not None else m.group(2)


def doctype_present(text):
    """True if a document type declaration appears in the prolog.

    A DOCTYPE may only appear before the root element, so the prolog is scanned
    with a tiny hand-rolled cursor: XML declaration, whitespace, comments and
    processing instructions are skipped; the first markup seen must be the
    doctype declaration.
    """
    i, n = 0, len(text)
    if text.startswith("<?xml"):
        j = text.find("?>")
        if j == -1:
            return False
        i = j + 2
    while i < n:
        while i < n and text[i] in " \t\r\n":
            i += 1
        if text.startswith("<!--", i):
            j = text.find("-->", i)
            if j == -1:
                return False
            i = j + 3
            continue
        if text.startswith("<?", i):
            j = text.find("?>", i)
            if j == -1:
                return False
            i = j + 2
            continue
        return text.startswith("<!DOCTYPE", i)
    return False


# ----------------------------------------------------------- file checks ----
def audit_bytes(data):
    """File-level findings only. Returns a list of (code, entry) pairs."""
    # (19) size limit -- cheap, and "no other finding" for this file.
    if len(data) > MAX_BYTES:
        return [("too_large", None)]

    # (6) bytes must decode as UTF-8; a leading BOM is allowed.
    body = data[len(BOM):] if data.startswith(BOM) else data
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError:
        return [("encoding_invalid", None)]

    # (7) the declaration's encoding pseudo-attribute must say UTF-8.
    enc = declared_encoding(text)
    if enc is not None and enc.lower() != "utf-8":
        return [("encoding_invalid", None)]

    # (9) a document type declaration ends the file's findings: doctype_present
    # is reported "and no other finding", so it is decided before the parse.
    # (ElementTree would also reject a document that references an entity the
    # DTD does not define, and the contract wants the doctype answer there.)
    if doctype_present(text):
        return [("doctype_present", None)]

    # (8) well-formed XML 1.0 with namespaces.
    try:
        root = ET.fromstring(data)
    except Exception:
        return [("xml_malformed", None)]

    # (10) root element name and namespace.
    urlset = "{%s}urlset" % NS
    index = "{%s}sitemapindex" % NS
    if root.tag == urlset:
        wanted = "{%s}url" % NS
    elif root.tag == index:
        wanted = "{%s}sitemap" % NS
    else:
        return [("root_invalid", None)]

    # (11)-(13) entries: root children in the sitemap namespace with the wanted
    # name. Other root children in that namespace are unexpected; children in
    # any other namespace are ignored.
    entries = 0
    unexpected = False
    for child in root:
        tag = child.tag
        if not isinstance(tag, str):
            continue
        if tag == wanted:
            entries += 1
        elif tag.startswith("{"):
            uri, _, local = tag[1:].partition("}")
            if uri == NS:
                unexpected = True

    findings = []
    if entries == 0:
        findings.append(("no_entries", None))
    if unexpected:
        findings.append(("element_unexpected", None))
    if entries > MAX_ENTRIES:
        findings.append(("too_many_entries", None))
    return findings


def findings_json(pairs):
    return [{"code": c, "entry": e} for c, e in pairs]


# ----------------------------------------------------------------- checks ----
def process_check(chk, base_dir, seen_ids):
    """Return one output item for one manifest check (contract sentences 4-5)."""
    if not isinstance(chk, dict):
        return {"id": None, "status": "error", "error": "check_invalid", "findings": []}

    raw_id = chk.get("id")
    f = chk.get("file")
    u = chk.get("sitemapUrl")

    cid = raw_id if isinstance(raw_id, str) else None

    # "repeats an earlier check's id": an earlier check that carried this id
    # reserves it, whether or not that earlier check was itself valid.
    repeated = False
    if cid is not None:
        repeated = cid in seen_ids
        seen_ids.add(cid)

    # Members must be strings (contract sentence 4).
    if cid is None or not isinstance(f, str) or not isinstance(u, str):
        return {"id": cid, "status": "error", "error": "check_invalid", "findings": []}

    if (repeated
            or os.path.isabs(f)
            or has_dotdot_segment(f)
            or not is_abs_http_url(u)):
        return {"id": cid, "status": "error", "error": "check_invalid", "findings": []}

    path = os.path.join(base_dir, f)
    try:
        size = os.stat(path).st_size
    except (OSError, ValueError):
        return {"id": cid, "status": "error", "error": "file_unreadable", "findings": []}
    if size > MAX_BYTES:
        return {"id": cid, "status": "findings", "error": None,
                "findings": findings_json([("too_large", None)])}

    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except (OSError, ValueError):
        return {"id": cid, "status": "error", "error": "file_unreadable", "findings": []}

    findings = audit_bytes(data)
    return {"id": cid,
            "status": "findings" if findings else "clean",
            "error": None,
            "findings": findings_json(findings)}


# ------------------------------------------------------------------- main ----
def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        sys.stderr.write("usage: control.py --manifest <path>\n")
        return 64

    manifest_path = argv[2]
    try:
        with open(manifest_path, "rb") as fh:
            raw = fh.read()
    except OSError:
        return input_invalid()

    try:
        manifest = json.loads(raw.decode("utf-8"))
    except Exception:
        return input_invalid()

    if not isinstance(manifest, dict):
        return input_invalid()
    version = manifest.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version != 1:
        return input_invalid()
    checks = manifest.get("checks")
    if not isinstance(checks, list) or not checks:
        return input_invalid()

    base_dir = os.path.dirname(os.path.abspath(manifest_path))
    seen_ids = set()
    items = [process_check(c, base_dir, seen_ids) for c in checks]

    if any(i["status"] == "error" for i in items):
        verdict, code = "could-not-evaluate", 2
    elif any(i["findings"] for i in items):
        verdict, code = "failed-policy", 1
    else:
        verdict, code = "clean", 0

    emit({"version": 1, "verdict": verdict, "checks": items})
    return code


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except BrokenPipeError:
        sys.exit(0)
