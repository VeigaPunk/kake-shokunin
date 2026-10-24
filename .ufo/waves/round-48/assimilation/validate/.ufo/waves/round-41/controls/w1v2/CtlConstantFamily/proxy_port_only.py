#!/usr/bin/env python3
"""Round-41 control (proxy family): a component-blind character repertoire test.

A `loc` is called invalid when it holds a character that no RFC 3986 component
allows anywhere (C0 controls, space, DEL, `"`, `<`, `>`, `\\`, `^`, `` ` ``,
`{`, `|`, `}`), or a `%` not followed by two hex digits; a `sitemapUrl` is called
`check_invalid` under the same test. No per-component repertoire, no position, no
scheme/host/authority structure and no IP-literal handling is done, so the
declared judgment (each component against its own RFC 3986 repertoire) is
skipped.
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


def _bad(value):
    index = 0
    length = len(value)
    while index < length:
        char = value[index]
        if char == "%":
            if index + 2 >= length or value[index + 1] not in HEX or value[index + 2] not in HEX:
                return True
            index += 3
            continue
        if ord(char) < 0x80 and char not in ALLOWED:
            return True
        index += 1
    mark = value.find("://")
    if mark < 0:
        return True
    authority = value[mark + 3:]
    for delimiter in "/?#":
        cut = authority.find(delimiter)
        if cut >= 0:
            authority = authority[:cut]
    hostport = authority.rsplit("@", 1)[-1]
    if hostport.startswith("[") and "]" in hostport:
        rest = hostport[hostport.find("]") + 1:]
        return bool(rest) and not (rest.startswith(":") and rest[1:].isdigit())
    if ":" in hostport:
        port = hostport.split(":", 1)[1]
        return not port.isdigit()
    return False


def _value_text(element):
    parts = [element.text or ""]
    for child in element:
        if isinstance(child.tag, str) and child.tag.startswith(SM_PREFIX):
            parts.append(_value_text(child))
        parts.append(child.tail or "")
    return "".join(parts)


def _entry_findings(path):
    """Set of entries with a `loc` failing the blind repertoire test."""
    try:
        with open(path, "rb") as handle:
            data = handle.read()
        root = ElementTree.fromstring(data)
    except Exception:
        return None
    name = "url" if root.tag == SM_PREFIX + "urlset" else "sitemap"
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
        value = _value_text(locs[0]).strip(XML_WS)
        if _bad(value):
            flagged.add(index)
    return flagged


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
    items = []
    any_error = False
    any_finding = False
    for check in checks:
        ident = check.get("id") if isinstance(check, dict) else None
        ident = ident if isinstance(ident, str) else None
        url_value = check.get("sitemapUrl") if isinstance(check, dict) else None
        file_value = check.get("file") if isinstance(check, dict) else None
        if not (isinstance(url_value, str) and isinstance(file_value, str)):
            items.append({"id": ident, "status": "error", "error": "check_invalid",
                          "findings": []})
            any_error = True
            continue
        if url_value.startswith("/") or ".." in file_value.split("/"):
            items.append({"id": ident, "status": "error", "error": "check_invalid",
                          "findings": []})
            any_error = True
            continue
        if _bad(url_value):
            items.append({"id": ident, "status": "error", "error": "check_invalid",
                          "findings": []})
            any_error = True
            continue
        flagged = _entry_findings(os.path.join(base_dir, file_value))
        if flagged is None:
            items.append({"id": ident, "status": "error", "error": "file_unreadable",
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
