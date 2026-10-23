#!/usr/bin/python3
"""Key-blind sitemap control: string tokenization, a lexical tag stack, no XML parser."""
import json
import os
import sys
from urllib.parse import urlsplit

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
WS = " \t\r\n"
MAX_BYTES = 52_428_800


class Malformed(Exception):
    pass


class EncodingInvalid(Exception):
    pass


class DoctypePresent(Exception):
    pass


class Node:
    __slots__ = ("name", "attrs", "content")

    def __init__(self, name, attrs):
        self.name = name
        self.attrs = attrs
        self.content = []


def xml_char(c):
    n = ord(c)
    return n in (9, 10, 13) or 32 <= n <= 0xD7FF or 0xE000 <= n <= 0xFFFD or 0x10000 <= n <= 0x10FFFF


def name_start(c):
    n = ord(c)
    return (c in "_:" or "A" <= c <= "Z" or "a" <= c <= "z"
            or 0xC0 <= n <= 0xD6 or 0xD8 <= n <= 0xF6 or 0xF8 <= n <= 0x2FF
            or 0x370 <= n <= 0x37D or 0x37F <= n <= 0x1FFF
            or 0x200C <= n <= 0x200D or 0x2070 <= n <= 0x218F
            or 0x2C00 <= n <= 0x2FEF or 0x3001 <= n <= 0xD7FF
            or 0xF900 <= n <= 0xFDCF or 0xFDF0 <= n <= 0xFFFD
            or 0x10000 <= n <= 0xEFFFF)


def valid_name(value, qname=True):
    def ncname(part):
        return bool(part) and part[0] != ":" and name_start(part[0]) and all(
            c != ":" and (name_start(c) or "0" <= c <= "9" or c in "-.\u00b7"
                          or 0x300 <= ord(c) <= 0x36F or 0x203F <= ord(c) <= 0x2040)
            for c in part[1:])
    if qname:
        parts = value.split(":")
        return len(parts) <= 2 and all(ncname(part) for part in parts)
    return bool(value) and name_start(value[0]) and all(
        name_start(c) or "0" <= c <= "9" or c in "-.\u00b7"
        or 0x300 <= ord(c) <= 0x36F or 0x203F <= ord(c) <= 0x2040
        for c in value[1:])


def digits(value):
    return bool(value) and all("0" <= c <= "9" for c in value)


def unescape(value):
    pieces = value.split("&")
    out = [pieces[0]]
    entities = {"amp": "&", "lt": "<", "gt": ">", "quot": '"', "apos": "'"}
    for piece in pieces[1:]:
        entity, sep, rest = piece.partition(";")
        if not sep:
            raise Malformed()
        if entity in entities:
            out.append(entities[entity])
        elif entity.startswith("#"):
            numeric = entity[1:]
            base = 10
            if numeric.startswith("x"):
                numeric = numeric[1:]
                base = 16
                ok = bool(numeric) and all(c in "0123456789abcdefABCDEF" for c in numeric)
            else:
                ok = digits(numeric)
            if not ok:
                raise Malformed()
            numeric = numeric.lstrip("0") or "0"
            if len(numeric) > (6 if base == 16 else 7):
                raise Malformed()
            number = int(numeric, base)
            if number > 0x10FFFF or not xml_char(chr(number)):
                raise Malformed()
            out.append(chr(number))
        else:
            raise Malformed()
        out.append(rest)
    return "".join(out)


def attributes(raw):
    attrs = {}
    i = 0
    while i < len(raw):
        if raw[i] not in WS:
            raise Malformed()
        while i < len(raw) and raw[i] in WS:
            i += 1
        if i == len(raw):
            break
        start = i
        while i < len(raw) and raw[i] not in WS + "=":
            i += 1
        name = raw[start:i]
        if not valid_name(name) or name in attrs:
            raise Malformed()
        while i < len(raw) and raw[i] in WS:
            i += 1
        if i == len(raw) or raw[i] != "=":
            raise Malformed()
        i += 1
        while i < len(raw) and raw[i] in WS:
            i += 1
        if i == len(raw) or raw[i] not in "\"'":
            raise Malformed()
        quote = raw[i]
        end = raw.find(quote, i + 1)
        if end == -1:
            raise Malformed()
        value = raw[i + 1:end]
        if "<" in value:
            raise Malformed()
        attrs[name] = unescape(value.replace("\t", " ").replace("\n", " ").replace("\r", " "))
        i = end + 1
    return attrs


def terminated(chunks, index, ending):
    collected = []
    while index < len(chunks):
        head, found, tail = chunks[index].partition(ending)
        collected.append(head)
        if found:
            return "<".join(collected), tail, index
        index += 1
    raise Malformed()


def tag_and_tail(chunk):
    pieces = chunk.split(">")
    quote = None
    for i, piece in enumerate(pieces[:-1]):
        for c in piece:
            if quote is not None:
                if c == quote:
                    quote = None
            elif c in "\"'":
                quote = c
        if quote is None:
            return ">".join(pieces[:i + 1]), ">".join(pieces[i + 1:])
    raise Malformed()


def tokens(text):
    chunks = text.split("<")
    yield "text", chunks[0]
    i = 1
    while i < len(chunks):
        chunk = chunks[i]
        if chunk.startswith("!--"):
            body, tail, i = terminated(chunks, i, "-->")
            body = body[3:]
            if "--" in body or body.endswith("-"):
                raise Malformed()
            yield "comment", body
        elif chunk.startswith("![CDATA["):
            body, tail, i = terminated(chunks, i, "]]>")
            yield "cdata", body[8:]
        elif chunk.startswith("? "):
            raise Malformed()
        elif chunk.startswith("?"):
            body, tail, i = terminated(chunks, i, "?>")
            yield "pi", body[1:]
        elif chunk.startswith("!DOCTYPE") and len(chunk) > 8 and chunk[8] in WS:
            raise DoctypePresent()
        elif chunk.startswith("!"):
            raise Malformed()
        else:
            body, tail = tag_and_tail(chunk)
            yield "tag", body
        yield "text", tail
        i += 1


def parse(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text.startswith("<?xml") and len(text) > 5 and text[5] in WS:
        end = text.find("?>", 5)
        if end == -1:
            raise Malformed()
        declaration = text[5:end]
        decl = attributes(declaration)
        if "encoding" in decl and decl["encoding"].lower() != "utf-8":
            raise EncodingInvalid()
        keys = list(decl)
        if (not keys or keys[0] != "version" or decl["version"] != "1.0"
                or any(k not in ("version", "encoding", "standalone") for k in keys)
                or ("standalone" in decl and decl["standalone"] not in ("yes", "no"))
                or ("encoding" in decl and "standalone" in decl and keys.index("encoding") > keys.index("standalone"))
                or "&" in declaration):
            raise Malformed()
        text = text[end + 2:]
    if not all(xml_char(c) for c in text):
        raise Malformed()
    root = None
    stack = []
    for kind, body in tokens(text):
        if kind == "comment":
            continue
        if kind == "pi":
            target = body.split(None, 1)[0] if body else ""
            if not valid_name(target, False) or target.lower() == "xml":
                raise Malformed()
            continue
        if kind in ("text", "cdata"):
            if kind == "text" and "]]>" in body:
                raise Malformed()
            if stack:
                stack[-1].content.append(unescape(body) if kind == "text" else body)
            elif kind == "cdata" or body.strip(WS):
                raise Malformed()
            continue
        if body.startswith("/"):
            name = body[1:].rstrip(WS)
            if not valid_name(name) or not stack or stack[-1].name != name:
                raise Malformed()
            stack.pop()
            continue
        closed = body.endswith("/")
        if closed:
            body = body[:-1]
        split = 0
        while split < len(body) and body[split] not in WS:
            split += 1
        name = body[:split]
        if not valid_name(name):
            raise Malformed()
        attrs = attributes(body[split:])
        node = Node(name, attrs if not stack else None)
        if stack:
            stack[-1].content.append(node)
        elif root is None:
            root = node
        else:
            raise Malformed()
        if not closed:
            stack.append(node)
    if stack or root is None:
        raise Malformed()
    return root


def children(node):
    return (item for item in node.content if isinstance(item, Node))


def value(node):
    out = []
    pending = [iter(node.content)]
    while pending:
        item = next(pending[-1], None)
        if item is None:
            pending.pop()
        elif isinstance(item, Node):
            pending.append(iter(item.content))
        else:
            out.append(item)
    return "".join(out).strip(WS)


def literal_name(name):
    prefix, colon, local = name.partition(":")
    return (prefix, local) if colon else ("", name)


def url(value):
    try:
        parsed = urlsplit(value)
        scheme = parsed.scheme.lower()
        host = parsed.hostname
        port = parsed.port
        if scheme not in ("http", "https") or not host:
            return None
        return scheme, host.lower(), port if port is not None else (80 if scheme == "http" else 443), parsed.path or "/"
    except ValueError:
        return None


def lastmod_ok(text):
    if len(text) < 10 or text[4] != "-" or text[7] != "-":
        return False
    if not all(digits(part) for part in (text[:4], text[5:7], text[8:10])):
        return False
    year, month, day = int(text[:4]), int(text[5:7]), int(text[8:10])
    if year < 1 or not 1 <= month <= 12:
        return False
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    days = (31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    if not 1 <= day <= days[month - 1]:
        return False
    if len(text) == 10:
        return True
    if text[10] != "T":
        return False
    clock = text[11:]
    if clock.endswith("Z"):
        clock = clock[:-1]
    elif (len(clock) >= 6 and clock[-6] in "+-" and clock[-3] == ":"
          and digits(clock[-5:-3]) and digits(clock[-2:])
          and int(clock[-5:-3]) <= 23 and int(clock[-2:]) <= 59):
        clock = clock[:-6]
    else:
        return False
    if len(clock) < 5 or clock[2] != ":" or not digits(clock[:2]) or not digits(clock[3:5]):
        return False
    if int(clock[:2]) > 23 or int(clock[3:5]) > 59:
        return False
    if len(clock) == 5:
        return True
    if len(clock) < 8 or clock[5] != ":" or not digits(clock[6:8]) or int(clock[6:8]) > 59:
        return False
    return len(clock) == 8 or (clock[8] == "." and digits(clock[9:]))


def priority_ok(text):
    negative = text.startswith("-")
    if text.startswith(("+", "-")):
        text = text[1:]
    integer, dot, fraction = text.partition(".")
    if (not integer and not fraction) or (integer and not digits(integer)) or (fraction and not digits(fraction)):
        return False
    if not dot and not integer:
        return False
    integer = integer.lstrip("0") or "0"
    nonzero_fraction = bool(fraction.strip("0"))
    if negative:
        return integer == "0" and not nonzero_fraction
    return integer == "0" or (integer == "1" and not nonzero_fraction)


def audit(raw, sitemap):
    def singleton(code):
        return {(code, None)}
    if len(raw) > MAX_BYTES:
        return singleton("too_large")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeError:
        return singleton("encoding_invalid")
    try:
        root = parse(text)
    except EncodingInvalid:
        return singleton("encoding_invalid")
    except DoctypePresent:
        return singleton("doctype_present")
    except Malformed:
        return singleton("xml_malformed")
    prefix, kind = literal_name(root.name)
    binding = "xmlns:" + prefix if prefix else "xmlns"
    if kind not in ("urlset", "sitemapindex") or root.attrs.get(binding) != NS:
        return singleton("root_invalid")
    findings = set()
    entries = []
    entry_name = "url" if kind == "urlset" else "sitemap"
    for child in children(root):
        child_prefix, local = literal_name(child.name)
        if child_prefix != prefix:
            continue
        if local == entry_name:
            entries.append(child)
        else:
            findings.add(("element_unexpected", None))
    if not entries:
        findings.add(("no_entries", None))
    if len(entries) > 50_000:
        findings.add(("too_many_entries", None))
    origin = url(sitemap)
    directory = origin[3].rsplit("/", 1)[0] + "/"
    allowed = {"loc", "lastmod", "changefreq", "priority"} if kind == "urlset" else {"loc", "lastmod"}
    for index, entry in enumerate(entries, 1):
        fields = {}
        for child in children(entry):
            child_prefix, local = literal_name(child.name)
            if child_prefix != prefix:
                continue
            if local not in allowed:
                findings.add(("element_unexpected", index))
            else:
                fields.setdefault(local, []).append(child)
        locs = fields.get("loc", [])
        if not locs:
            findings.add(("loc_missing", index))
        elif len(locs) > 1:
            findings.add(("loc_repeated", index))
        else:
            loc = value(locs[0])
            target = url(loc)
            if target is None:
                findings.add(("loc_not_absolute", index))
            if len(loc) >= 2048:
                findings.add(("loc_too_long", index))
            if target is not None and (target[:3] != origin[:3] or (kind == "urlset" and not target[3].startswith(directory))):
                findings.add(("loc_out_of_scope", index))
        for field in allowed - {"loc"}:
            nodes = fields.get(field, [])
            if len(nodes) > 1:
                findings.add(("field_repeated", index))
            elif nodes:
                field_value = value(nodes[0])
                valid = (lastmod_ok(field_value) if field == "lastmod" else
                         priority_ok(field_value) if field == "priority" else
                         field_value in ("always", "hourly", "daily", "weekly", "monthly", "yearly", "never"))
                if not valid:
                    findings.add((field + "_invalid", index))
    return findings


def emit(verdict, checks, error=None):
    result = {"version": 1, "verdict": verdict, "checks": checks}
    if error is not None:
        result["error"] = error
    print(json.dumps(result, ensure_ascii=True, separators=(",", ":")))


def main(args):
    if len(args) != 2 or args[0] != "--manifest":
        return 64
    manifest_path = args[1]
    try:
        with open(manifest_path, "r", encoding="utf-8") as source:
            manifest = json.load(source)
    except (OSError, ValueError, UnicodeError):
        emit("could-not-evaluate", [], "input_invalid")
        return 2
    if (not isinstance(manifest, dict) or type(manifest.get("version")) is not int
            or manifest["version"] != 1 or not isinstance(manifest.get("checks"), list)
            or not manifest["checks"]):
        emit("could-not-evaluate", [], "input_invalid")
        return 2
    base = os.path.dirname(os.path.abspath(manifest_path))
    seen = set()
    results = []
    for check in manifest["checks"]:
        identifier = check.get("id") if isinstance(check, dict) and isinstance(check.get("id"), str) else None
        result = {"id": identifier, "status": "error", "error": None, "findings": []}
        valid = isinstance(check, dict) and all(isinstance(check.get(k), str) for k in ("id", "file", "sitemapUrl"))
        duplicate = identifier is not None and identifier in seen
        if identifier is not None:
            seen.add(identifier)
        if (not valid or duplicate or os.path.isabs(check["file"]) or ".." in check["file"].split("/")
                or url(check["sitemapUrl"]) is None):
            result["error"] = "check_invalid"
        else:
            try:
                with open(os.path.join(base, check["file"]), "rb") as source:
                    raw = source.read(MAX_BYTES + 1)
            except (OSError, ValueError):
                result["error"] = "file_unreadable"
            else:
                found = audit(raw, check["sitemapUrl"])
                result["status"] = "findings" if found else "clean"
                result["findings"] = [{"code": code, "entry": entry} for code, entry in sorted(found, key=lambda f: (f[1] or 0, f[0]))]
        results.append(result)
    if any(check["status"] == "error" for check in results):
        verdict, code = "could-not-evaluate", 2
    elif any(check["findings"] for check in results):
        verdict, code = "failed-policy", 1
    else:
        verdict, code = "clean", 0
    emit(verdict, results)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
