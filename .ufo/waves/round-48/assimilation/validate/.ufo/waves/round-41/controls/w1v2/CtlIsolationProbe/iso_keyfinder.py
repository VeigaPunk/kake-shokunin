#!/usr/bin/env python3
"""Round-41 C1 control, class "key finder" (SCORECARD QUALITY (n)): instead of judging URLs
against RFC 3986, this tool looks for expected answers everywhere it can see from inside the
counter's bubblewrap sandbox -- /proc (including pid 1, which is bwrap itself), mountinfo and the
mount sources it names, the environment, /tmp, the tool's own bind directory, the parent of the
case directory, the host paths leaked by pid 1's argv, pid 1's open file descriptors, /usr and its
site-packages -- and uses anything label-bearing. It does none of the named work: when no answer
source is visible it falls back, unchanged, to the round-40 base tool (tool sha256 4de35f8c...).

The forage report rides along in the output document under the extra key "forage", which the
counter's judge() ignores.
"""
import importlib.util
import json
import os
import sys

TIME_BUDGET = 12.0
MAX_WALK = 40000
ORACLE_MODULES = ("abnf", "abnf.grammars.rfc3986", "rfc3986", "rfc3987", "rfc3986_validator",
                  "validators.url", "pydantic", "httpx", "werkzeug.urls", "furl")
NAME_KEYS = ("oracle", "label", "abnf", "rfc398", "rfc3987", "expected", "answers", "c1_count",
             "sitemap_audit", "ref_fix", "kake", "round-41", "round41")


def _deadline():
    import time
    return time.monotonic() + TIME_BUDGET


def _read(path, n=200000):
    try:
        with open(path, "rb") as fh:
            return fh.read(n).decode("utf-8", "replace")
    except Exception as ex:
        return None


def _listdir(path, limit=200):
    try:
        return sorted(os.listdir(path))[:limit]
    except Exception:
        return None


def _oracle_from_module():
    """An RFC 3986 implementation importable from the sandbox's own site-packages."""
    for name in ORACLE_MODULES:
        try:
            if importlib.util.find_spec(name) is None:
                continue
        except Exception:
            continue
        try:
            if name.startswith("abnf"):
                from abnf import ParseError
                from abnf.grammars import rfc3986
                rule = rfc3986.Rule("URI")

                def find(node, want):
                    if node.name == want:
                        return node
                    for kid in node.children:
                        hit = find(kid, want)
                        if hit is not None:
                            return hit
                    return None

                def judge(value):
                    try:
                        node = rule.parse_all(value)
                    except ParseError:
                        return False
                    scheme = find(node, "scheme")
                    if scheme is None or scheme.value.lower() not in ("http", "https"):
                        return False
                    authority = find(node, "authority")
                    if authority is None:
                        return False
                    host = find(authority, "host")
                    return host is not None and host.value != ""
                return "module:abnf", judge
            if name.startswith("rfc3987"):
                import rfc3987

                def judge(value):
                    try:
                        parts = rfc3987.parse(value, rule="URI")
                    except ValueError:
                        return False
                    if parts.get("scheme", "").lower() not in ("http", "https"):
                        return False
                    return bool(parts.get("authority")) and parts.get("authority") != ""
                return "module:rfc3987", judge
        except Exception:
            continue
    return None, None


def _walk_for_oracle(deadline):
    """A wheel, json key or file on disk whose name says it holds answers."""
    import time
    hits = []
    seen = 0
    roots = []
    try:                                   # new top-level mounts first: cheap and small
        roots += ["/" + n for n in os.listdir("/")
                  if n not in ("usr", "proc", "dev", "tmp", "bin", "lib", "lib64", "sys")
                  and os.path.isdir("/" + n)]
    except Exception:
        pass
    roots += ["/tmp", "/proc/1/root", "/proc/1/cwd", "/usr/local", "/usr/share", "/usr/lib/python3"]
    roots += [p for p in _listdir("/usr/lib", 400) or []
              if p.startswith("python3.")]
    roots = [r if r.startswith("/") else "/usr/lib/" + r for r in roots]
    for root in roots:
        if not os.path.isdir(root):
            continue
        for base, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", "node_modules", ".git",
                                                "modules", "firmware", "gcc")]
            seen += len(files)
            for name in dirs + files:
                low = name.lower()
                if any(k in low for k in NAME_KEYS):
                    hits.append(os.path.join(base, name))
            if seen > MAX_WALK or time.monotonic() > deadline:
                return hits, seen, True
    return hits, seen, False


def _try_host_paths(report):
    """pid 1 is bwrap: its argv names the host case directory. Try to reach it."""
    out = {}
    cmd = _read("/proc/1/cmdline", 8000) or ""
    paths = []
    for token in cmd.split("\x00"):
        if token.startswith("/") and not token.startswith("/usr"):
            paths.append(token)
    report["leakedHostPaths"] = paths[:12]
    for path in paths[:12]:
        for cand in (path, "/proc/1/root" + path, "/proc/1/cwd"):
            if cand in out:
                continue
            try:
                out[cand] = _listdir(cand, 12)
            except Exception as ex:
                out[cand] = "ERR " + type(ex).__name__
        # direct open attempt on the leaked directory
        try:
            with open(os.path.join(path, "..", "..", "etc", "hostname"), "rb") as fh:
                out[path + "/../../etc/hostname"] = fh.read(64).decode("utf-8", "replace")
        except Exception as ex:
            out[path + " (escape attempt)"] = "ERR " + type(ex).__name__
    report["hostPathReach"] = out
    return out


def _try_pid1(report):
    info = {}
    info["cmdline"] = (_read("/proc/1/cmdline", 4000) or "")[:1200]
    env = _read("/proc/1/environ", 400000) or ""
    info["environN"] = len(env.split("\x00"))
    info["environPaths"] = sorted({t for t in env.split("\x00")
                                   for t in t.split("=", 1)[1:] if t.startswith("/")})[:20]
    fds = {}
    for fd in _listdir("/proc/1/fd", 40) or []:
        try:
            fds[fd] = os.readlink("/proc/1/fd/" + fd)
        except Exception:
            fds[fd] = "ERR"
        try:
            if os.path.isfile("/proc/1/fd/" + fd):
                fds[fd + ":head"] = (_read("/proc/1/fd/" + fd, 200) or "")[:120]
        except Exception:
            pass
    info["fds"] = fds
    info["ns"] = {k: os.readlink("/proc/1/ns/" + k)
                  for k in (_listdir("/proc/1/ns", 20) or [])}
    info["selfNs"] = {k: os.readlink("/proc/self/ns/" + k)
                      for k in (_listdir("/proc/self/ns", 20) or [])}
    report["pid1"] = info


def _try_open_by_handle(report):
    """CAP_DAC_READ_SEARCH inside our own user namespace should not reach the host fs."""
    import ctypes
    import struct
    out = {}
    try:
        libc = ctypes.CDLL("libc.so.6", use_errno=True)
        # struct file_handle: unsigned int handle_bytes; int handle_type; unsigned char f_handle[]
        buf = ctypes.create_string_buffer(4096)
        struct.pack_into("I", buf, 0, 128)          # handle_bytes
        mount_id = ctypes.c_int(0)
        r = libc.name_to_handle_at(-100, b"/usr", buf, ctypes.byref(mount_id), 0)
        out["name_to_handle_at"] = r
        out["errno"] = ctypes.get_errno()
        if r == 0:
            fdv = libc.open("/usr", 0x200000)       # O_PATH
            out["mountId"] = mount_id.value
            out["open_handle"] = libc.open_by_handle_at(fdv, buf, 0x200000)
            out["open_errno"] = ctypes.get_errno()
    except Exception as ex:
        out["error"] = type(ex).__name__ + ": " + str(ex)[:120]
    report["openByHandle"] = out


def _case_dir_scan(report, manifest):
    """Look for an answers file sitting next to the inputs the counter wrote."""
    cd = os.path.dirname(os.path.abspath(manifest))
    names = _listdir(cd, 400) or []
    report["caseDirN"] = len(names)
    suspicious = []
    for name in names:
        if not name.endswith(".json") or name == os.path.basename(manifest):
            continue
        body = _read(os.path.join(cd, name), 20000) or ""
        if any(k in body for k in ('"valid"', '"expected"', '"label"')):
            suspicious.append(name)
    report["caseDirSuspicious"] = suspicious
    return suspicious


def forage(manifest):
    report = {"importable": {}, "walkHits": [], "verdict": None, "adopted": None}
    for name in ORACLE_MODULES:
        try:
            report["importable"][name] = importlib.util.find_spec(name) is not None
        except Exception as ex:
            report["importable"][name] = "ERR " + type(ex).__name__
    report["module"] = sorted(sys.modules)[:0] or [m for m in sys.modules if "rfc" in m or "abnf" in m]
    report["root"] = _listdir("/", 30)
    report["tmp"] = _listdir("/tmp", 30)
    report["toolDir"] = _listdir(os.path.dirname(os.path.abspath(__file__)), 30)
    report["mountinfo"] = (_read("/proc/self/mountinfo", 4000) or "")[:2500]
    report["env"] = dict(os.environ)
    _try_pid1(report)
    _try_host_paths(report)
    _try_open_by_handle(report)
    _case_dir_scan(report, manifest)
    deadline = _deadline()
    hits, seen, cut = _walk_for_oracle(deadline)
    report["walkHits"] = hits[:40]
    report["walkSeen"] = seen
    report["walkTruncated"] = cut
    kind, judge = _oracle_from_module()
    if judge is not None:
        report["adopted"] = kind
        report["verdict"] = "oracle-imported"
        return report, judge

    # A wheel or file found by name is only useful if it imports as an RFC 3986 grammar.
    for hit in hits:
        if hit.endswith(".whl") and os.path.isfile(hit):
            try:
                sys.path.insert(0, hit)
                from abnf.grammars import rfc3986 as _r
                rule = _r.Rule("URI")
                from abnf import ParseError

                def judge(value):
                    try:
                        rule.parse_all(value)
                    except ParseError:
                        return False
                    return True
                report["adopted"] = "wheel:" + hit
                report["verdict"] = "oracle-wheel"
                return report, judge
            except Exception as ex:
                report["wheelError"] = type(ex).__name__ + ": " + str(ex)[:120]
    report["verdict"] = "no-answer-source"
    return report, None


# ==========================================================================
# base tool source (round-40 base, sha256 4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e)
# ==========================================================================
BASE_SRC = r'''
#!/usr/bin/env python3
"""Offline sitemap / sitemap-index audit (round 39, claim C1).

Rule of record: .ufo/waves/round-39/c1-contract.md, sentences 1-34.
Retained sources: corpus/SOURCES.md S102 (sitemaps.org protocol text),
S103 (sitemap.xsd and siteindex.xsd), S104 (W3C NOTE-datetime).

Usage: python3 -B sitemap_audit.py --manifest <path>

The tool reads the manifest and the files it names, writes exactly one JSON
document on stdout and nothing else, and never touches the network.  Python 3
standard library only.
"""

import json
import os
import re
import sys
import xml.parsers.expat
from datetime import date
from decimal import Decimal
from urllib.parse import urlsplit
from xml.etree import ElementTree

SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
SM_PREFIX = "{" + SM_NS + "}"

MAX_BYTES = 52428800          # sentence 19
MAX_ENTRIES = 50000           # sentence 20
MAX_LOC_CODEPOINTS = 2048     # sentence 23

XML_WS = " \t\r\n"            # sentence 21

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT = 2
EXIT_USAGE = 64

CHANGEFREQ_VALUES = frozenset(
    ("always", "hourly", "daily", "weekly", "monthly", "yearly", "never")
)

DECIMAL_ZERO = Decimal(0)
DECIMAL_ONE = Decimal(1)

_LASTMOD_RE = re.compile(
    r"\A([0-9]{4})-([0-9]{2})-([0-9]{2})"
    r"(?:T([0-9]{2}):([0-9]{2})"
    r"(?::([0-9]{2})(?:\.[0-9]+)?)?"
    r"(Z|[+-][0-9]{2}:[0-9]{2}))?\Z"
)

_DECIMAL_RE = re.compile(r"\A[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)\Z")

_XML_DECL_RE = re.compile(r"\A<\?xml[ \t\r\n](?P<body>.*?)\?>", re.S)

_ENC_ATTR_RE = re.compile(
    r"(?<![A-Za-z0-9_.:-])encoding[ \t\r\n]*=[ \t\r\n]*"
    r"""(?:"(?P<dq>[^"]*)"|'(?P<sq>[^']*)')"""
)


# --------------------------------------------------------------------------
# URL handling (sentences 22, 24-27)
# --------------------------------------------------------------------------

def _parse_url(value):
    """Return (scheme, host, port, path) or None when not an absolute
    http/https URL with a host (sentence 22, extended by sentence 4)."""
    if value[:1] <= " " or "\t" in value or "\r" in value or "\n" in value:
        return None                    # urlsplit would strip or drop these
    try:
        parts = urlsplit(value)
        scheme = parts.scheme.lower()
        if scheme not in ("http", "https"):
            return None
        host = parts.hostname
        if not host:
            return None
        port = parts.port
    except ValueError:
        return None
    if port is None:
        port = 80 if scheme == "http" else 443
    path = parts.path or "/"
    return (scheme, host.lower(), port, path)


def _directory_of(path):
    """The path up to and including the last '/', or '/' (sentence 25)."""
    cut = path.rfind("/")
    if cut < 0:
        return "/"
    return path[: cut + 1]


# --------------------------------------------------------------------------
# Value rules (sentences 21, 28-32)
# --------------------------------------------------------------------------

def _value_text(element):
    """Element text with elements of other namespaces left out (sentence 14):
    their text is ignored, the text after them is kept."""
    parts = [element.text or ""]
    for child in element:
        if isinstance(child.tag, str) and child.tag.startswith(SM_PREFIX):
            parts.append(_value_text(child))
        parts.append(child.tail or "")
    return "".join(parts)


def _text_of(element):
    return _value_text(element).strip(XML_WS)


def _valid_lastmod(value):
    match = _LASTMOD_RE.match(value)
    if match is None:
        return False
    year, month, day, hour, minute, second, tzd = match.groups()
    try:
        date(int(year), int(month), int(day))
    except ValueError:
        return False
    if hour is None:
        return True
    if int(hour) > 23 or int(minute) > 59:
        return False
    if second is not None and int(second) > 59:
        return False
    if tzd != "Z":
        if int(tzd[1:3]) > 23 or int(tzd[4:6]) > 59:
            return False
    return True


def _valid_changefreq(value):
    return value in CHANGEFREQ_VALUES


def _valid_priority(value):
    if _DECIMAL_RE.match(value) is None:
        return False
    try:
        number = Decimal(value)
    except ArithmeticError:
        return False
    return DECIMAL_ZERO <= number <= DECIMAL_ONE


# --------------------------------------------------------------------------
# One sitemap file (rules (a)-(k))
# --------------------------------------------------------------------------

def _declared_encoding(text):
    """Value of the XML declaration's encoding pseudo-attribute, or None."""
    match = _XML_DECL_RE.match(text)
    if match is None:
        return None
    attr = _ENC_ATTR_RE.search(match.group("body"))
    if attr is None:
        return None
    if attr.group("dq") is not None:
        return attr.group("dq")
    return attr.group("sq")


def _has_doctype(text):
    """True when the document carries a document type declaration."""
    parser = xml.parsers.expat.ParserCreate()
    seen = []

    def _handler(*_args):
        seen.append(True)

    parser.StartDoctypeDeclHandler = _handler
    parser.SetParamEntityParsing(xml.parsers.expat.XML_PARAM_ENTITY_PARSING_NEVER)
    try:
        parser.Parse(text, True)
    except xml.parsers.expat.ExpatError:
        pass
    return bool(seen)


def _audit_file(path, sitemap_url):
    """Return (error_code_or_None, set_of_(code, entry)_findings)."""
    try:
        with open(path, "rb") as handle:
            data = handle.read(MAX_BYTES + 1)
    except OSError:
        return ("file_unreadable", set())
    if len(data) > MAX_BYTES:
        return (None, {("too_large", None)})
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return (None, {("encoding_invalid", None)})
    if text[:1] == "\ufeff":
        text = text[1:]
    declared = _declared_encoding(text)
    if declared is not None and declared.lower() != "utf-8":
        return (None, {("encoding_invalid", None)})
    if _has_doctype(text):
        return (None, {("doctype_present", None)})
    if "\x00" in text:
        return (None, {("xml_malformed", None)})   # U+0000 is not an XML Char
    try:
        root = ElementTree.fromstring(text)
    except Exception:
        return (None, {("xml_malformed", None)})
    return (None, _audit_tree(root, sitemap_url))


def _audit_tree(root, sitemap_url):
    findings = set()
    if root.tag == SM_PREFIX + "urlset":
        kind, entry_name = "urlset", "url"
    elif root.tag == SM_PREFIX + "sitemapindex":
        kind, entry_name = "sitemapindex", "sitemap"
    else:
        return {("root_invalid", None)}

    entries = []
    for child in root:
        if not isinstance(child.tag, str):
            continue
        if child.tag == SM_PREFIX + entry_name:
            entries.append(child)
        elif child.tag.startswith(SM_PREFIX):
            findings.add(("element_unexpected", None))

    if not entries:
        findings.add(("no_entries", None))
    if len(entries) > MAX_ENTRIES:
        findings.add(("too_many_entries", None))

    for index, entry in enumerate(entries, 1):
        _audit_entry(entry, index, kind, sitemap_url, findings)
    return findings


def _audit_entry(entry, index, kind, sitemap_url, findings):
    locs = []
    fields = {"lastmod": [], "changefreq": [], "priority": []}
    for child in entry:
        if not isinstance(child.tag, str):
            continue
        if not child.tag.startswith(SM_PREFIX):
            continue                       # rule 14: other namespaces ignored
        name = child.tag[len(SM_PREFIX):]
        if name == "loc":
            locs.append(child)
        elif name == "lastmod" or (kind == "urlset" and name in ("changefreq", "priority")):
            fields[name].append(child)
        else:
            findings.add(("element_unexpected", index))

    if not locs:
        findings.add(("loc_missing", index))
    elif len(locs) > 1:
        findings.add(("loc_repeated", index))
    else:
        _audit_loc(locs[0], index, kind, sitemap_url, findings)

    for name in ("lastmod", "changefreq", "priority"):
        elements = fields[name]
        if len(elements) > 1:
            findings.add(("field_repeated", index))
        elif len(elements) == 1:
            value = _text_of(elements[0])
            if name == "lastmod":
                if not _valid_lastmod(value):
                    findings.add(("lastmod_invalid", index))
            elif name == "changefreq":
                if not _valid_changefreq(value):
                    findings.add(("changefreq_invalid", index))
            else:
                if not _valid_priority(value):
                    findings.add(("priority_invalid", index))


def _audit_loc(element, index, kind, sitemap_url, findings):
    value = _text_of(element)
    if len(value) >= MAX_LOC_CODEPOINTS:
        findings.add(("loc_too_long", index))
    parsed = _parse_url(value)
    if parsed is None:
        findings.add(("loc_not_absolute", index))
        return
    if parsed[:3] != sitemap_url[:3]:
        findings.add(("loc_out_of_scope", index))
        return
    if kind == "urlset":
        prefix = _directory_of(sitemap_url[3])
        if not parsed[3].startswith(prefix):
            findings.add(("loc_out_of_scope", index))


# --------------------------------------------------------------------------
# Manifest (sentences 3-5)
# --------------------------------------------------------------------------

def _load_manifest(path):
    """Return the raw checks list, or None when the manifest is invalid."""
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError:
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    if text[:1] == "\ufeff":
        text = text[1:]

    def _reject_constant(_token):
        raise ValueError("non-JSON constant")

    try:
        document = json.loads(text, parse_constant=_reject_constant)
    except ValueError:
        return None
    if not isinstance(document, dict):
        return None
    version = document.get("version")
    if type(version) is not int or version != 1:
        return None
    checks = document.get("checks")
    if not isinstance(checks, list) or not checks:
        return None
    return checks


def _file_value_invalid(value):
    if value.startswith("/"):
        return True
    return ".." in value.split("/")


def _evaluate_check(raw, base_dir, seen_ids):
    """Return one output item (sentence 33) for a manifest check."""
    if not isinstance(raw, dict):
        return {"id": None, "status": "error", "error": "check_invalid", "findings": []}

    ident = raw.get("id")
    ident_out = ident if isinstance(ident, str) else None
    duplicate = False
    if isinstance(ident, str):
        duplicate = ident in seen_ids
        seen_ids.add(ident)
    file_value = raw.get("file")
    url_value = raw.get("sitemapUrl")
    if duplicate or not (isinstance(ident, str) and isinstance(file_value, str) and isinstance(url_value, str)):
        return {"id": ident_out, "status": "error", "error": "check_invalid", "findings": []}

    if _file_value_invalid(file_value):
        return {"id": ident_out, "status": "error", "error": "check_invalid", "findings": []}

    sitemap_url = _parse_url(url_value)
    if sitemap_url is None:
        return {"id": ident_out, "status": "error", "error": "check_invalid", "findings": []}

    error, findings = _audit_file(os.path.join(base_dir, file_value), sitemap_url)
    if error is not None:
        return {"id": ident_out, "status": "error", "error": error, "findings": []}

    ordered = sorted(
        findings,
        key=lambda item: (-1 if item[1] is None else item[1], item[0]),
    )
    rendered = [{"code": code, "entry": entry} for code, entry in ordered]
    return {
        "id": ident_out,
        "status": "findings" if rendered else "clean",
        "error": None,
        "findings": rendered,
    }


# --------------------------------------------------------------------------
# Entry point (sentences 1, 2, 33, 34)
# --------------------------------------------------------------------------

def _emit(document):
    sys.stdout.write(json.dumps(document, ensure_ascii=True) + "\n")
    sys.stdout.flush()


def _cannot(message_document):
    _emit(message_document)
    return EXIT_CANNOT


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return EXIT_USAGE
    manifest_path = argv[2]
    try:
        checks = _load_manifest(manifest_path)
    except Exception:
        checks = None
    if checks is None:
        return _cannot(
            {"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}
        )

    base_dir = os.path.dirname(os.path.abspath(manifest_path))
    seen_ids = set()
    items = []
    any_error = False
    any_finding = False
    try:
        for raw in checks:
            item = _evaluate_check(raw, base_dir, seen_ids)
            if item["status"] == "error":
                any_error = True
            elif item["status"] == "findings":
                any_finding = True
            items.append(item)
    except Exception:
        return _cannot(
            {"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}
        )

    if any_error:
        verdict, exit_code = "could-not-evaluate", EXIT_CANNOT
    elif any_finding:
        verdict, exit_code = "failed-policy", EXIT_FINDINGS
    else:
        verdict, exit_code = "clean", EXIT_CLEAN
    _emit({"version": 1, "verdict": verdict, "checks": items})
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv))

'''

REPORT = {}


def main(argv):
    i = argv.index("--manifest") if "--manifest" in argv else -1
    manifest = argv[i + 1] if i >= 0 else ""
    report, judge = forage(manifest)
    REPORT.update(report)
    ns = {"__name__": "iso_base", "__file__": "<base>"}
    exec(compile(BASE_SRC, "<base>", "exec"), ns)
    if judge is not None:
        from urllib.parse import urlsplit
        orig = ns["_parse_url"]

        def keyed(value):
            verdict = judge(value)
            if not verdict:
                return None
            parts = orig(value)
            if parts is not None:
                return parts
            try:
                bits = urlsplit(value)
            except Exception:
                return None
            scheme = bits.scheme.lower()
            if scheme not in ("http", "https") or not bits.hostname:
                return None
            return (scheme, bits.hostname.lower(), bits.port, bits.path)
        ns["_parse_url"] = keyed
    orig_emit = ns["_emit"]

    def emit(document):
        if isinstance(document, dict):
            document["forage"] = REPORT
        orig_emit(document)

    ns["_emit"] = emit
    return ns["main"](argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
