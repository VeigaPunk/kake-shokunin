#!/usr/bin/env python3
"""Control CtlXsdDelegate: sitemap audit delegated to the sitemaps.org 0.9 XSDs.

Shape: every file is validated against the embedded sitemaps.org XSDs (urlset ->
sitemap.xsd, sitemapindex -> siteindex.xsd); schema verdicts are mapped onto the
round-39 C1 contract's codes.  Manifest handling, file-level checks, entry
indexing and the structural codes (loc_missing / loc_repeated / field_repeated /
element_unexpected / no_entries / too_large / too_many_entries) are implemented
directly; the *value* of lastmod / changefreq / priority is decided by the schema.

Deliberate gaps vs the contract (this is the point of the control):
  * rule (h) scope comparison is NOT implemented at all -> loc_out_of_scope is
    never reported;
  * rule (i) lastmod is whatever the XSD says (xsd:date | xsd:dateTime), not the
    contract's W3C-datetime profile -> no-seconds timestamps and TZD offsets
    outside +-14:00 are reported as lastmod_invalid.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
SIZE_LIMIT = 52428800
ENTRY_LIMIT = 50000
XML_WS = " \t\r\n"

XSD_URLSET = r'''<?xml version="1.0" encoding="UTF-8"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            targetNamespace="http://www.sitemaps.org/schemas/sitemap/0.9"
            xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
            elementFormDefault="qualified">
  <xsd:annotation>
    <xsd:documentation>
    XML Schema for Sitemap files.
    Last Modifed 2008-03-26
    </xsd:documentation>
  </xsd:annotation>

  <xsd:element name="urlset">
    <xsd:annotation>
    <xsd:documentation>
    Container for a set of up to 50,000 document elements.
    This is the root element of the XML file.
    </xsd:documentation>
    </xsd:annotation>
    <xsd:complexType>
    <xsd:sequence>
    <xsd:any namespace="##other" minOccurs="0" maxOccurs="unbounded" processContents="strict"/>
    <xsd:element name="url" type="tUrl" maxOccurs="unbounded"/>
    </xsd:sequence>
    </xsd:complexType>
  </xsd:element>

  <xsd:complexType name="tUrl">
    <xsd:annotation>
    <xsd:documentation>
    Container for the data needed to describe a document to crawl.
    </xsd:documentation>
    </xsd:annotation>
    <xsd:sequence>
    <xsd:element name="loc" type="tLoc"/>
    <xsd:element name="lastmod" type="tLastmod" minOccurs="0"/>
    <xsd:element name="changefreq" type="tChangeFreq" minOccurs="0"/>
    <xsd:element name="priority" type="tPriority" minOccurs="0"/>
    <xsd:any namespace="##other" minOccurs="0" maxOccurs="unbounded" processContents="strict"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:simpleType name="tLoc">
    <xsd:annotation>
    <xsd:documentation>
    REQUIRED: The location URI of a document.
    The URI must conform to RFC 2396 (http://www.ietf.org/rfc/rfc2396.txt).
    </xsd:documentation>
    </xsd:annotation>
    <xsd:restriction base="xsd:anyURI">
    <xsd:minLength value="12"/>
    <xsd:maxLength value="2048"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:simpleType name="tLastmod">
    <xsd:annotation>
    <xsd:documentation>
    OPTIONAL: The date the document was last modified. The date must conform
    to the W3C DATETIME format (http://www.w3.org/TR/NOTE-datetime).
    </xsd:documentation>
    </xsd:annotation>
    <xsd:union>
    <xsd:simpleType>
    <xsd:restriction base="xsd:date"/>
    </xsd:simpleType>
    <xsd:simpleType>
    <xsd:restriction base="xsd:dateTime"/>
    </xsd:simpleType>
    </xsd:union>
  </xsd:simpleType>

  <xsd:simpleType name="tChangeFreq">
    <xsd:annotation>
    <xsd:documentation>
    OPTIONAL: Indicates how frequently the content at a particular URL is
    likely to change.
    </xsd:documentation>
    </xsd:annotation>
    <xsd:restriction base="xsd:string">
    <xsd:enumeration value="always"/>
    <xsd:enumeration value="hourly"/>
    <xsd:enumeration value="daily"/>
    <xsd:enumeration value="weekly"/>
    <xsd:enumeration value="monthly"/>
    <xsd:enumeration value="yearly"/>
    <xsd:enumeration value="never"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:simpleType name="tPriority">
    <xsd:annotation>
    <xsd:documentation>
    OPTIONAL: The priority of a particular URL relative to other pages
    on the same site. The value for this element is a number between
    0.0 and 1.0.
    </xsd:documentation>
    </xsd:annotation>
    <xsd:restriction base="xsd:decimal">
    <xsd:minInclusive value="0.0"/>
    <xsd:maxInclusive value="1.0"/>
    </xsd:restriction>
  </xsd:simpleType>

</xsd:schema>
'''

XSD_SITEMAPINDEX = r'''<?xml version="1.0" encoding="UTF-8"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            targetNamespace="http://www.sitemaps.org/schemas/sitemap/0.9"
            xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
            elementFormDefault="qualified">
  <xsd:annotation>
    <xsd:documentation>
    XML Schema for Sitemap index files.
    Last Modifed 2009-04-08
    </xsd:documentation>
  </xsd:annotation>

  <xsd:element name="sitemapindex">
    <xsd:annotation>
    <xsd:documentation>
    Container for a set of up to 50,000 sitemap URLs.
    This is the root element of the XML file.
    </xsd:documentation>
    </xsd:annotation>
    <xsd:complexType>
    <xsd:sequence>
    <xsd:any namespace="##other" minOccurs="0" maxOccurs="unbounded" processContents="strict"/>
    <xsd:element name="sitemap" type="tSitemap" maxOccurs="unbounded"/>
    </xsd:sequence>
    </xsd:complexType>
  </xsd:element>

  <xsd:complexType name="tSitemap">
    <xsd:annotation>
    <xsd:documentation>
    Container for the data needed to describe a sitemap.
    </xsd:documentation>
    </xsd:annotation>
    <xsd:sequence>
    <xsd:element name="loc" type="tLocSitemap"/>
    <xsd:element name="lastmod" type="tLastmodSitemap" minOccurs="0"/>
    <xsd:any namespace="##other" minOccurs="0" maxOccurs="unbounded" processContents="strict"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:simpleType name="tLocSitemap">
    <xsd:annotation>
    <xsd:documentation>
    REQUIRED: The location URI of a sitemap.
    The URI must conform to RFC 2396 (http://www.ietf.org/rfc/rfc2396.txt).
    </xsd:documentation>
    </xsd:annotation>
    <xsd:restriction base="xsd:anyURI">
    <xsd:minLength value="12"/>
    <xsd:maxLength value="2048"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:simpleType name="tLastmodSitemap">
    <xsd:annotation>
    <xsd:documentation>
    OPTIONAL: The date the document was last modified. The date must conform
    to the W3C DATETIME format (http://www.w3.org/TR/NOTE-datetime).
    </xsd:documentation>
    </xsd:annotation>
    <xsd:union>
    <xsd:simpleType>
    <xsd:restriction base="xsd:date"/>
    </xsd:simpleType>
    <xsd:simpleType>
    <xsd:restriction base="xsd:dateTime"/>
    </xsd:simpleType>
    </xsd:union>
  </xsd:simpleType>

</xsd:schema>
'''


# ---------------------------------------------------------------- helpers

def split_tag(tag):
    """Return (namespace, localname) for an ElementTree/lxml tag."""
    if not isinstance(tag, str):
        return (None, None)
    if tag.startswith("{"):
        ns, _, local = tag[1:].partition("}")
        return (ns, local)
    return ("", tag)


def trim(value):
    """Strip XML whitespace (U+0020, U+0009, U+000D, U+000A) from both ends."""
    if value is None:
        return ""
    return value.strip(XML_WS)


def scan_prolog(text):
    """Return (doctype_present, xml_decl_encoding) for the prolog of `text`."""
    i = 0
    n = len(text)
    doctype = False
    enc = None
    while i < n:
        while i < n and text[i] in XML_WS:
            i += 1
        if i >= n:
            break
        if text.startswith("<?", i):
            j = text.find("?>", i)
            if j < 0:
                break
            decl = text[i + 2:j]
            if decl.startswith("xml") and (len(decl) == 3 or decl[3] in XML_WS):
                m = re.search(r"encoding\s*=\s*(\"([^\"]*)\"|'([^']*)')", decl)
                if m:
                    enc = m.group(2) if m.group(2) is not None else m.group(3)
            i = j + 2
            continue
        if text.startswith("<!--", i):
            j = text.find("-->", i)
            if j < 0:
                break
            i = j + 3
            continue
        if text.startswith("<!DOCTYPE", i):
            doctype = True
            j = i
            depth = 0
            while j < n:
                c = text[j]
                if c == "[":
                    depth += 1
                elif c == "]":
                    depth -= 1
                elif c == ">" and depth <= 0:
                    break
                j += 1
            i = j + 1
            continue
        break
    return doctype, enc


def parse_xml(data):
    """Parse `data` into an ElementTree-like root, or return None if malformed."""
    import xml.etree.ElementTree as ET
    try:
        return ET.fromstring(data)
    except Exception:
        return None


def build_doc(rootname, entname, field, value):
    """Build a one-entry document that carries `value` in `field`."""
    import xml.etree.ElementTree as ET
    ET.register_namespace("", NS)
    root = ET.Element("{%s}%s" % (NS, rootname))
    ent = ET.SubElement(root, "{%s}%s" % (NS, entname))
    ET.SubElement(ent, "{%s}loc" % NS).text = "http://example.com/a"
    ET.SubElement(ent, "{%s}%s" % (NS, field)).text = value
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


class Oracle:
    """Schema oracle: valid/invalid for one field value, per document kind."""

    def __init__(self):
        self.mode = None
        self.schemas = {}
        self.xmllint = shutil.which("xmllint") or "/usr/bin/xmllint"
        self._tmp = None
        if self.mode is None and os.path.exists(self.xmllint):
            self._tmp = tempfile.mkdtemp(prefix="xsd-delegate-")
            for key, text in (("urlset", XSD_URLSET), ("sitemapindex", XSD_SITEMAPINDEX)):
                path = os.path.join(self._tmp, key + ".xsd")
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(text)
                self.schemas[key] = path
            self.mode = "xmllint"

    def value_valid(self, kind, field, value):
        """True when the schema accepts `value` in `field` of a `kind` document."""
        if self.mode is None:
            return True
        rootname = "urlset" if kind == "urlset" else "sitemapindex"
        entname = "url" if kind == "urlset" else "sitemap"
        doc = build_doc(rootname, entname, field, value)
        try:
            proc = subprocess.run([self.xmllint, "--noout", "--schema", self.schemas[kind], "-"],
                                  input=doc, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                  timeout=60)
        except Exception:
            return True
        return proc.returncode == 0


# ---------------------------------------------------------------- auditing

def is_absolute_http(value):
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


def audit_file(path, oracle):
    """Return (findings set, error code or None) for one sitemap file."""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except (OSError, ValueError):
        return (set(), "file_unreadable")

    if len(data) > SIZE_LIMIT:
        return ({("too_large", None)}, None)

    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return ({("encoding_invalid", None)}, None)

    doctype, enc = scan_prolog(text)
    if enc is not None and enc.lower() != "utf-8":
        return ({("encoding_invalid", None)}, None)

    root = parse_xml(data)
    if root is None:
        return ({("xml_malformed", None)}, None)
    if doctype:
        return ({("doctype_present", None)}, None)

    ns, local = split_tag(root.tag)
    if ns != NS or local not in ("urlset", "sitemapindex"):
        return ({("root_invalid", None)}, None)
    kind = local

    findings = set()
    entname = "url" if kind == "urlset" else "sitemap"
    entries = []
    for child in root:
        cns, cloc = split_tag(child.tag)
        if cns != NS:
            continue  # rule (d): other namespaces are ignored
        if cloc == entname:
            entries.append(child)
        else:
            findings.add(("element_unexpected", None))

    if not entries:
        findings.add(("no_entries", None))
    if len(entries) > ENTRY_LIMIT:
        findings.add(("too_many_entries", None))

    for idx, entry in enumerate(entries, 1):
        locs = []
        lastmods = []
        changefreqs = []
        priorities = []
        for child in entry:
            cns, cloc = split_tag(child.tag)
            if cns != NS:
                continue
            if cloc == "loc":
                locs.append(child)
            elif cloc == "lastmod":
                lastmods.append(child)
            elif cloc == "changefreq":
                changefreqs.append(child)
            elif cloc == "priority":
                priorities.append(child)
            else:
                findings.add(("element_unexpected", idx))

        if len(locs) == 0:
            findings.add(("loc_missing", idx))
        elif len(locs) > 1:
            findings.add(("loc_repeated", idx))
        else:
            value = trim(locs[0].text)
            if not is_absolute_http(value):
                findings.add(("loc_not_absolute", idx))
            if len(value) >= 2048:
                findings.add(("loc_too_long", idx))
            # rule (h) scope comparison is deliberately NOT implemented.

        if len(lastmods) > 1:
            findings.add(("field_repeated", idx))
        elif len(lastmods) == 1:
            value = trim(lastmods[0].text)
            if not oracle.value_valid(kind, "lastmod", value):
                findings.add(("lastmod_invalid", idx))

        if kind == "urlset":
            if len(changefreqs) > 1:
                findings.add(("field_repeated", idx))
            elif len(changefreqs) == 1:
                value = trim(changefreqs[0].text)
                if not oracle.value_valid(kind, "changefreq", value):
                    findings.add(("changefreq_invalid", idx))
            if len(priorities) > 1:
                findings.add(("field_repeated", idx))
            elif len(priorities) == 1:
                value = trim(priorities[0].text)
                if not oracle.value_valid(kind, "priority", value):
                    findings.add(("priority_invalid", idx))
        else:
            # in a sitemapindex entry, changefreq / priority are unexpected elements
            for extra in changefreqs + priorities:
                findings.add(("element_unexpected", idx))

    return (findings, None)


# ---------------------------------------------------------------- manifest

def check_invalid(chk, seen_ids):
    """Return an error code when the check object is invalid, else None."""
    if not isinstance(chk, dict):
        return "check_invalid"
    for key in ("id", "file", "sitemapUrl"):
        if key not in chk or not isinstance(chk[key], str):
            return "check_invalid"
    if chk["id"] in seen_ids:
        return "check_invalid"
    rel = chk["file"]
    if os.path.isabs(rel):
        return "check_invalid"
    parts = rel.split("/")
    if ".." in parts:
        return "check_invalid"
    url = chk["sitemapUrl"]
    try:
        parts = urlsplit(url)
        host = parts.hostname
    except ValueError:
        return "check_invalid"
    if parts.scheme.lower() not in ("http", "https") or not host:
        return "check_invalid"
    return None


def emit_input_invalid():
    doc = {"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}
    sys.stdout.write(json.dumps(doc) + "\n")
    return 2


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        sys.stderr.write("usage: control.py --manifest <path>\n")
        return 64
    manifest_path = argv[2]
    try:
        with open(manifest_path, "rb") as fh:
            raw = fh.read()
        manifest = json.loads(raw.decode("utf-8"))
    except Exception:
        return emit_input_invalid()
    if not isinstance(manifest, dict):
        return emit_input_invalid()
    version = manifest.get("version")
    if isinstance(version, bool) or not isinstance(version, int) or version != 1:
        return emit_input_invalid()
    checks = manifest.get("checks")
    if not isinstance(checks, list) or not checks:
        return emit_input_invalid()

    oracle = Oracle()
    base = os.path.dirname(os.path.abspath(manifest_path))
    seen_ids = set()
    out_checks = []
    for chk in checks:
        cid = None
        if isinstance(chk, dict) and isinstance(chk.get("id"), str):
            cid = chk["id"]
        err = check_invalid(chk, seen_ids)
        if cid is not None:
            seen_ids.add(cid)
        if err is not None:
            out_checks.append({"id": cid, "status": "error", "error": err, "findings": []})
            continue
        path = os.path.join(base, chk["file"])
        findings, err = audit_file(path, oracle)
        if err is not None:
            out_checks.append({"id": cid, "status": "error", "error": err, "findings": []})
            continue
        items = [{"code": code, "entry": entry} for code, entry in sorted(
            findings, key=lambda t: (t[0], -1 if t[1] is None else t[1]))]
        out_checks.append({
            "id": cid,
            "status": "findings" if items else "clean",
            "error": None,
            "findings": items,
        })

    has_error = any(c["status"] == "error" for c in out_checks)
    has_findings = any(c["findings"] for c in out_checks)
    if has_error:
        verdict, code = "could-not-evaluate", 2
    elif has_findings:
        verdict, code = "failed-policy", 1
    else:
        verdict, code = "clean", 0
    doc = {"version": 1, "verdict": verdict, "checks": out_checks}
    sys.stdout.write(json.dumps(doc) + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
