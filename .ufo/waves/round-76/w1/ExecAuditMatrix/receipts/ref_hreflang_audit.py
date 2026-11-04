#!/usr/bin/env python3
"""Reference implementation of contract C2 + amendment 2, scratch copy.

NOT a deliverable: the matrix author's reading of the frozen contract and the
frozen amendment, used to validate that every case is decidable and to stand
in as the tool under test while the wave's hreflang_audit.py is unavailable.
Offline, stdlib only, reads only --manifest and the page files it names,
writes nothing.

CLI: python3 ref_hreflang_audit.py --manifest PATH [--root DIR] [--json]
Exit: 0 clean, 1 policy findings, 2 input faults, 64 usage/version.
"""

import argparse
import json
import os
import re
import sys
from html import unescape
from urllib.parse import urlsplit, urljoin

TAG_GRAMMAR = re.compile(
    r"^[A-Za-z]{2,3}(-[A-Za-z]{4})?(-([A-Za-z]{2}|[0-9]{3}))?"
    r"(-([A-Za-z0-9]{5,8}|[0-9][A-Za-z0-9]{3}))*$"
)

POLICY_IDS = (
    "hreflang_missing_value",
    "hreflang_invalid_tag",
    "hreflang_relative_href",
    "hreflang_duplicate_pair",
    "hreflang_multiple_xdefault",
    "hreflang_self_missing",
    "hreflang_nonreciprocal",
    "hreflang_canonical_not_self",
)
INPUT_IDS = ("input_unreadable", "input_duplicate_url", "input_url_not_absolute")
INFO_IDS = ("hreflang_external_target",)

# A13: these subtrees are not scanned unless self-closed as <svg/> or <math/>.
RAW_TEXT_ELEMENTS = ("script", "style", "template", "svg", "math")


def tag_ok(value):
    if value is None:
        return False
    if value.lower() == "x-default":  # A11
        return True
    return TAG_GRAMMAR.match(value) is not None


def remove_dot_segments(path):
    """RFC 3986 section 5.2.4."""
    inp = path
    out = []
    while inp:
        if inp.startswith("../"):
            inp = inp[3:]
        elif inp.startswith("./"):
            inp = inp[2:]
        elif inp.startswith("/./"):
            inp = "/" + inp[3:]
        elif inp == "/.":
            inp = "/"
        elif inp.startswith("/../"):
            inp = "/" + inp[4:]
            if out:
                out.pop()
        elif inp == "/..":
            inp = "/"
            if out:
                out.pop()
        elif inp in (".", ".."):
            inp = ""
        else:
            start = 1 if inp.startswith("/") else 0
            index = inp.find("/", start)
            if index < 0:
                index = len(inp)
            out.append(inp[:index])
            inp = inp[index:]
    return "".join(out)


def normalize_url(url):
    """A3: exact string equality after RFC 3986 normalization."""
    if not isinstance(url, str):
        return url
    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    host = (parts.hostname or "").lower()
    userinfo = ""
    if parts.username is not None:
        userinfo = parts.username
        if parts.password is not None:
            userinfo += ":" + parts.password
        userinfo += "@"
    try:
        port = parts.port
    except ValueError:
        port = None
    default = {"http": 80, "https": 443, "ftp": 21}.get(scheme)
    if port is not None and port != default:
        netloc = userinfo + host + ":" + str(port)
    else:
        netloc = userinfo + host
    path = remove_dot_segments(parts.path)
    if path == "":
        path = "/"
    out = scheme + "://" + netloc + path
    if parts.query:
        out += "?" + parts.query
    if parts.fragment:
        out += "#" + parts.fragment
    return out


def parse_attrs(chunk):
    attrs = {}
    i = 0
    n = len(chunk)
    while i < n:
        while i < n and (chunk[i].isspace() or chunk[i] == "/"):
            i += 1
        if i >= n:
            break
        j = i
        while j < n and not chunk[j].isspace() and chunk[j] not in "=/>":
            j += 1
        name = chunk[i:j].lower()
        i = j
        while i < n and chunk[i].isspace():
            i += 1
        value = ""
        if i < n and chunk[i] == "=":
            i += 1
            while i < n and chunk[i].isspace():
                i += 1
            if i < n and chunk[i] in "\"'":
                quote = chunk[i]
                k = chunk.find(quote, i + 1)
                if k < 0:
                    value = chunk[i + 1:]
                    i = n
                else:
                    value = chunk[i + 1:k]
                    i = k + 1
            else:
                k = i
                while k < n and not chunk[k].isspace() and chunk[k] != ">":
                    k += 1
                value = chunk[i:k]
                i = k
        if name and name not in attrs:
            attrs[name] = unescape(value)  # A13 entities decoded
    return attrs


def scan_links(text):
    links = []
    n = len(text)
    lower = text.lower()
    i = 0
    while i < n:
        j = text.find("<", i)
        if j < 0:
            break
        if text.startswith("<!--", j):
            k = text.find("-->", j + 4)
            i = n if k < 0 else k + 3
            continue
        if j + 1 >= n or not (text[j + 1].isalpha() or text[j + 1] in "/!?"):
            i = j + 1
            continue
        k = j + 1
        quote = None
        while k < n:
            c = text[k]
            if quote:
                if c == quote:
                    quote = None
            elif c in "\"'":
                quote = c
            elif c == ">":
                break
            k += 1
        raw = text[j + 1:k]
        i = k + 1
        m = re.match(r"([A-Za-z][A-Za-z0-9-]*)", raw)
        if not m:
            continue
        name = m.group(1).lower()
        self_closed = raw.rstrip().endswith("/")
        if name in RAW_TEXT_ELEMENTS and not self_closed:
            end = lower.find("</" + name, i)
            if end < 0:
                i = n
            else:
                close = text.find(">", end)
                i = n if close < 0 else close + 1
            continue
        if name == "link":
            links.append(parse_attrs(raw[m.end():]))
    return links


def rel_tokens(attrs):
    return attrs.get("rel", "").lower().split()


def is_alternate(attrs):
    tokens = rel_tokens(attrs)
    # A13: `alternate` alongside `stylesheet` does not create an alternate.
    return "alternate" in tokens and "stylesheet" not in tokens


def is_absolute(url):
    if not isinstance(url, str):
        return False
    parts = urlsplit(url)
    return bool(parts.scheme) and bool(parts.netloc)


def file_problem(value, root):
    """A15: escape root, absolute, symlink or non-regular file."""
    if not isinstance(value, str) or value == "":
        return True
    if os.path.isabs(value):
        return True
    if ".." in value.split("/"):
        return True
    path = os.path.join(root, value)
    if os.path.islink(path):
        return True
    return not os.path.isfile(path)


def analyse_page(page, links, pages_by_url, links_by_url):
    findings = []
    alternates = []
    canonicals = []
    for attrs in links:
        if is_alternate(attrs):
            if "hreflang" not in attrs or attrs["hreflang"] == "":
                findings.append({"id": "hreflang_missing_value",
                                 "severity": "policy", "page": page["id"]})
                continue
            if "href" not in attrs:  # A9: not an alternate, not reported
                continue
            tag = attrs["hreflang"]
            href = attrs["href"]
            if not tag_ok(tag):
                findings.append({"id": "hreflang_invalid_tag",
                                 "severity": "policy", "page": page["id"]})
            if not is_absolute(href):
                # A4: reported once, contributes to no other finding.
                findings.append({"id": "hreflang_relative_href",
                                 "severity": "policy", "page": page["id"]})
                continue
            alternates.append((tag, href))
        if "canonical" in rel_tokens(attrs) and "href" in attrs:
            canonicals.append(attrs["href"])

    page_norm = normalize_url(page["url"])
    seen = set()
    for tag, href in alternates:
        key = (tag.lower(), normalize_url(href))
        if key in seen:  # A2: one finding per offending annotation
            findings.append({"id": "hreflang_duplicate_pair",
                             "severity": "policy", "page": page["id"]})
        else:
            seen.add(key)

    xdefaults = sum(1 for tag, _href in alternates if tag.lower() == "x-default")
    if xdefaults > 1:
        # A2: one finding per offending <link>; every x-default on a page with
        # more than one is an x-default annotation.
        for _ in range(xdefaults):
            findings.append({"id": "hreflang_multiple_xdefault",
                             "severity": "policy", "page": page["id"]})

    if alternates:
        if not any(normalize_url(href) == page_norm for _tag, href in alternates):
            findings.append({"id": "hreflang_self_missing",
                             "severity": "policy", "page": page["id"]})
        if canonicals:  # A5: absent canonical means self, so no finding
            resolved = normalize_url(urljoin(page["url"], canonicals[0]))
            if resolved != page_norm:
                findings.append({"id": "hreflang_canonical_not_self",
                                 "severity": "policy", "page": page["id"]})
        for tag, href in alternates:
            href_norm = normalize_url(href)
            target = pages_by_url.get(href_norm)
            if target is None:
                findings.append({"id": "hreflang_external_target",
                                 "severity": "info", "page": page["id"]})
                continue
            if target["id"] == page["id"]:
                continue
            returns = [
                attrs for attrs in links_by_url.get(href_norm, [])
                if is_alternate(attrs)
                and attrs.get("hreflang", "") != ""
                and "href" in attrs
                and attrs["hreflang"].lower() == tag.lower()
                and normalize_url(attrs["href"]) == page_norm
            ]
            if not returns:
                findings.append({"id": "hreflang_nonreciprocal",
                                 "severity": "policy", "page": page["id"]})
    return findings


def emit(report, as_json):
    if as_json:
        sys.stdout.write(json.dumps(report, sort_keys=True) + "\n")
    else:
        for row in report["findings"]:
            sys.stdout.write("%s\t%s\n" % (row["id"], row.get("page")))
    return report["exit"]


def make_report(pages, findings, code):
    return {
        "version": 1,
        "pages": len(pages),
        "findings": findings,
        "counts": {"findings": len(findings)},
        "exit": code,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--json", action="store_true")
    try:
        args, extra = parser.parse_known_args(argv)
    except SystemExit:
        return 64
    if extra:
        return 64

    try:
        with open(args.manifest, "rb") as handle:
            manifest = json.loads(handle.read().decode("utf-8"))
        pages = manifest["pages"]
        if not isinstance(pages, list):
            raise ValueError("pages")
        for page in pages:
            for key in ("id", "file", "url"):
                if not isinstance(page.get(key), str) or not page.get(key):
                    raise ValueError(key)
    except (OSError, ValueError, KeyError, TypeError, UnicodeDecodeError):
        return emit(make_report([], [{"id": "input_unreadable",
                                      "severity": "input", "page": None}], 2),
                    args.json)

    if manifest.get("version") != 1:  # A15, with the A16 report object
        return emit(make_report(pages, [], 64), args.json)

    findings = []
    urls = [page["url"] for page in pages]
    for url in urls:
        if not is_absolute(url):
            findings.append({"id": "input_url_not_absolute",
                             "severity": "input", "page": None})
    seen_urls = set()
    for page in pages:
        if page["url"] in seen_urls:
            findings.append({"id": "input_duplicate_url",
                             "severity": "input", "page": page["id"]})
        seen_urls.add(page["url"])

    pages_by_url = {}
    for page in pages:
        pages_by_url.setdefault(normalize_url(page["url"]), page)

    links_by_url = {}
    seen_files = set()
    for page in pages:
        if page["file"] in seen_files:  # A15: no two pages may share a file
            findings.append({"id": "input_unreadable",
                             "severity": "input", "page": page["id"]})
            continue
        seen_files.add(page["file"])
        if file_problem(page["file"], args.root):
            findings.append({"id": "input_unreadable",
                             "severity": "input", "page": page["id"]})
            continue
        path = os.path.join(args.root, page["file"])
        try:
            with open(path, "rb") as handle:
                text = handle.read().decode("utf-8")
        except (OSError, UnicodeDecodeError):
            findings.append({"id": "input_unreadable",
                             "severity": "input", "page": page["id"]})
            continue
        links_by_url.setdefault(normalize_url(page["url"]), scan_links(text))

    for page in pages:
        links = links_by_url.get(normalize_url(page["url"]))
        if links is not None:
            findings.extend(analyse_page(page, links, pages_by_url,
                                         links_by_url))

    policy = [row for row in findings if row["id"] in POLICY_IDS]
    inputs = [row for row in findings if row["id"] in INPUT_IDS]
    if inputs:
        code = 2
    elif policy:
        code = 1
    else:
        code = 0
    return emit(make_report(pages, findings, code), args.json)


if __name__ == "__main__":
    sys.exit(main())
