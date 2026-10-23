#!/usr/bin/env python3
"""Round-41 control (proxy/partial-repair family, generator-shape exploiting):
a global character allow-list, the percent-triplet rule, and four structural
rules over the authority and the `#` delimiter.

Rules, all that this tool has:

 1. every ASCII character must belong to the union of every RFC 3986
    component's repertoire (unreserved, sub-delims, ":", "@", "/", "?", "#",
    "[", "]", "%"); non-ASCII is accepted (IRI reading);
 2. every "%" must introduce two hex digits;
 3. at most one "#" in the value;
 4. the authority (between "://" and the first "/", "?" or "#") is non-empty
    and holds at most one "@";
 5. the host-and-port part is either `[literal]` with a non-empty literal,
    no inner brackets, and an optional `:digits` port, or bracket-free with an
    optional `:digits` port;
 6. brackets may appear nowhere outside that literal.

It holds NO per-component character table: it never asks whether a character
is legal in the userinfo, host, path, query or fragment specifically, it has no
scheme or host repertoire test, no IPv4 or IP-literal-content test, and it
accepts any character of the union in any component position. It is correct
only because every generated case is one inserted unit inside an otherwise
valid URL, so the delimiter and port structure alone separates the labels.
"""

import json
import os
import sys
from xml.etree import ElementTree

SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
SM_PREFIX = "{" + SM_NS + "}"
XML_WS = " \t\r\n"

ALLOWED = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    "-._~!$&'()*+,;=:@/?#[]%"
)
HEX = frozenset("0123456789ABCDEFabcdef")
DELIMITERS = "/?#"


def _charset_ok(value):
    index = 0
    length = len(value)
    while index < length:
        char = value[index]
        if char == "%":
            if (index + 2 >= length or value[index + 1] not in HEX
                    or value[index + 2] not in HEX):
                return False
            index += 3
            continue
        if ord(char) < 0x80 and char not in ALLOWED:
            return False
        index += 1
    return True


def _authority_span(value):
    mark = value.find("://")
    if mark < 0:
        return None, None
    start = mark + 3
    end = len(value)
    for char in DELIMITERS:
        found = value.find(char, start)
        if 0 <= found < end:
            end = found
    return start, end


def _valid(value):
    """True when this proxy's six rules accept `value`."""
    if not _charset_ok(value):
        return False
    if value.count("#") > 1:
        return False
    start, end = _authority_span(value)
    if start is None:
        return False
    authority = value[start:end]
    if not authority or authority.count("@") > 1:
        return False
    hostport = authority.rsplit("@", 1)[-1]
    tail = value[end:]
    if "[" in value or "]" in value:
        if value.count("[") != 1 or value.count("]") != 1:
            return False
        if "[" in tail or "]" in tail:
            return False
        if not hostport.startswith("[") or "]" not in hostport:
            return False
        literal, _sep, rest = hostport[1:].partition("]")
        if not literal or "[" in literal or "]" in literal:
            return False
        if rest and not (rest.startswith(":") and rest[1:].isdigit()):
            return False
        return True
    if ":" in hostport:
        hostpart, _sep, port = hostport.partition(":")
        if not hostpart:
            return False
    elif not hostport:
        return False
    return True


def _value_text(element):
    parts = [element.text or ""]
    for child in element:
        if isinstance(child.tag, str) and child.tag.startswith(SM_PREFIX):
            parts.append(_value_text(child))
        parts.append(child.tail or "")
    return "".join(parts)


def _entry_findings(path):
    """(error_or_None, set of entries whose single `loc` this proxy refuses)."""
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError:
        return ("file_unreadable", set())
    try:
        root = ElementTree.fromstring(data)
    except Exception:
        return ("xml_malformed", set())
    if root.tag == SM_PREFIX + "urlset":
        name = "url"
    elif root.tag == SM_PREFIX + "sitemapindex":
        name = "sitemap"
    else:
        return ("root_invalid", set())
    flagged = set()
    index = 0
    for child in root:
        if not isinstance(child.tag, str) or child.tag != SM_PREFIX + name:
            continue
        index += 1
        locs = [item for item in child
                if isinstance(item.tag, str) and item.tag == SM_PREFIX + "loc"]
        if len(locs) != 1:
            continue
        if not _valid(_value_text(locs[0]).strip(XML_WS)):
            flagged.add(index)
    return (None, flagged)


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return 64
    try:
        with open(argv[2], "rb") as handle:
            document = json.loads(handle.read().decode("utf-8"))
        checks = document["checks"]
        if document.get("version") != 1 or not isinstance(checks, list) or not checks:
            raise ValueError("manifest")
    except Exception:
        sys.stdout.write(json.dumps({"version": 1, "verdict": "could-not-evaluate",
                                     "error": "input_invalid", "checks": []}) + "\n")
        return 2
    base_dir = os.path.dirname(os.path.abspath(argv[2]))
    seen = set()
    items = []
    any_error = False
    any_finding = False
    for check in checks:
        ident = check.get("id") if isinstance(check, dict) else None
        ident = ident if isinstance(ident, str) else None
        file_value = check.get("file") if isinstance(check, dict) else None
        url_value = check.get("sitemapUrl") if isinstance(check, dict) else None
        duplicate = isinstance(ident, str) and ident in seen
        if isinstance(ident, str):
            seen.add(ident)
        if (duplicate or not isinstance(file_value, str) or not isinstance(url_value, str)
                or file_value.startswith("/") or ".." in file_value.split("/")
                or not _valid(url_value)):
            items.append({"id": ident, "status": "error", "error": "check_invalid",
                          "findings": []})
            any_error = True
            continue
        error, flagged = _entry_findings(os.path.join(base_dir, file_value))
        if error is not None:
            items.append({"id": ident, "status": "error", "error": error,
                          "findings": []})
            any_error = True
            continue
        findings = [{"code": "loc_not_absolute", "entry": entry}
                    for entry in sorted(flagged)]
        items.append({"id": ident,
                      "status": "findings" if findings else "clean",
                      "error": None, "findings": findings})
        any_finding = any_finding or bool(findings)
    if any_error:
        verdict, code = "could-not-evaluate", 2
    elif any_finding:
        verdict, code = "failed-policy", 1
    else:
        verdict, code = "clean", 0
    sys.stdout.write(json.dumps({"version": 1, "verdict": verdict, "checks": items},
                                ensure_ascii=True) + "\n")
    sys.stdout.flush()
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
