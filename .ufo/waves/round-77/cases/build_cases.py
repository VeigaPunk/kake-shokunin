#!/usr/bin/env python3
"""Build the frozen C2 container/format matrix cases (round 77).

Deterministic generator for every case directory under this one.  Each case
holds three files:

  manifest.json   version-1 manifest, the shape of .ufo/waves/round-39/verification/realrun/manifest.json
  <sitemap file>  the bytes the tool reads
  expect.json     {"exit": <int>, "findings": [<finding ids>]}

Run from anywhere:

  python3 -B .ufo/waves/round-77/cases/build_cases.py [--out <dir>]

It rewrites the case directories and prints one line per case with the byte
length and sha256 of the sitemap file, so a reviewer can rebuild and compare.
The gzip members are written with mtime=0 and no embedded name, so their bytes
(and sha256) are stable for a given zlib.

Case expectations are the frozen contract table (round-77 contract, C2).  No
case id, expectation or byte may be changed after the base run.
"""

import argparse
import gzip
import hashlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ATOM_NS = "http://www.w3.org/2005/Atom"

LIMIT = 52428800            # contract G1/T1: 52,428,800 bytes
G02_BODY_BYTES = LIMIT + 1  # one byte over the decompressed limit
T05_LINES = 50001           # contract T1: at most 50,000 URLs

XML_DECL = b'<?xml version="1.0" encoding="UTF-8"?>\n'


def gzip_bytes(data):
    """A gzip member with a stable header (mtime 0, no file name)."""
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", compresslevel=9, mtime=0) as handle:
        handle.write(data)
    return buffer.getvalue()


def urlset(entries):
    body = ['<urlset xmlns="%s">' % SM_NS]
    for entry in entries:
        body.append("<url><loc>%s</loc></url>" % entry)
    body.append("</urlset>")
    return XML_DECL + ("\n".join(body) + "\n").encode("utf-8")


def sitemapindex(entries):
    body = ['<sitemapindex xmlns="%s">' % SM_NS]
    for entry in entries:
        body.append("<sitemap><loc>%s</loc></sitemap>" % entry)
    body.append("</sitemapindex>")
    return XML_DECL + ("\n".join(body) + "\n").encode("utf-8")


def rss(items, channel_link="https://example.com/"):
    lines = [
        '<rss version="2.0">',
        "<channel>",
        "<title>Example feed</title>",
        "<link>%s</link>" % channel_link,
        "<description>Example feed</description>",
    ]
    lines.extend(items)
    lines.extend(["</channel>", "</rss>"])
    return XML_DECL + ("\n".join(lines) + "\n").encode("utf-8")


def rss_item(title, link, pub_date=None):
    parts = ["<item>", "<title>%s</title>" % title]
    if link is not None:
        parts.append("<link>%s</link>" % link)
    if pub_date is not None:
        parts.append("<pubDate>%s</pubDate>" % pub_date)
    parts.append("</item>")
    return "".join(parts)


def atom(entries):
    lines = [
        '<feed xmlns="%s">' % ATOM_NS,
        "<title>Example feed</title>",
        "<id>urn:uuid:00000000-0000-4000-8000-000000000000</id>",
        "<updated>2026-11-02T09:00:00Z</updated>",
    ]
    lines.extend(entries)
    lines.append("</feed>")
    return XML_DECL + ("\n".join(lines) + "\n").encode("utf-8")


def atom_entry(title, href, updated):
    parts = ["<entry>", "<title>%s</title>" % title]
    if href is None:
        parts.append('<link rel="alternate"/>')
    else:
        parts.append('<link href="%s"/>' % href)
    parts.append("<id>urn:uuid:%s</id>" % title.lower())
    if updated is not None:
        parts.append("<updated>%s</updated>" % updated)
    parts.append("</entry>")
    return "".join(parts)


def g02_body():
    """A valid 2-entry urlset whose length is exactly 52,428,801 bytes."""
    prefix = (
        XML_DECL
        + ('<urlset xmlns="%s">\n' % SM_NS).encode("utf-8")
        + b"<url><loc>https://example.com/alpha</loc></url>\n"
        + b"<url><loc>https://example.com/beta</loc></url>\n"
    )
    suffix = b"</urlset>\n"
    padding = G02_BODY_BYTES - len(prefix) - len(suffix)
    assert padding > 0
    return prefix + b" " * padding + suffix


def t05_text():
    return "".join(
        "https://example.com/p/%06d\n" % number for number in range(1, T05_LINES + 1)
    ).encode("utf-8")


def cases():
    """(id, file name, sitemap url, bytes, expected exit, expected finding ids)."""
    g01_xml = urlset(["https://example.com/alpha", "https://example.com/beta"])
    g01_gz = gzip_bytes(g01_xml)
    g02_gz = gzip_bytes(g02_body())
    t06_text = b"https://example.com/one\nhttps://example.com/two\n"
    rss_clean = rss([
        rss_item("Alpha", "https://example.com/alpha", "2026-11-02T10:00:00Z"),
        rss_item("Beta", "https://example.com/beta", "2026-11-02T11:00:00Z"),
    ])
    atom_clean = atom([
        atom_entry("Alpha", "https://example.com/alpha", "2026-11-02T10:00:00Z"),
        atom_entry("Beta", "https://example.com/beta", "2026-11-02T11:00:00Z"),
    ])
    return [
        ("g01", "sitemap.xml.bin", "https://example.com/sitemap.xml.bin", g01_gz, 0, []),
        ("g02", "sitemap.xml.gz", "https://example.com/sitemap.xml.gz", g02_gz, 1, ["too_large"]),
        ("g03", "sitemap.xml.gz", "https://example.com/sitemap.xml.gz", g01_gz[:40], 2, ["gzip_invalid"]),
        ("g04", "sitemap.xml.gz", "https://example.com/sitemap.xml.gz", g01_xml, 0, []),
        ("t01", "sitemap.txt", "https://example.com/sitemap.txt",
         b"https://example.com/one\nhttps://example.com/two\nhttps://example.com/three\n", 0, []),
        ("t02", "sitemap.txt", "https://example.com/sitemap.txt",
         b"https://example.com/one\n# comment\nhttps://example.com/two\n", 1, ["text_line_not_url"]),
        ("t03", "sitemap.txt", "https://example.com/sitemap.txt",
         b"https://example.com/one\n/page\n", 1, ["text_url_not_absolute"]),
        ("t04", "sitemap.txt", "https://example.com/sitemap.txt", b"", 1, ["text_empty"]),
        ("t05", "sitemap.txt", "https://example.com/sitemap.txt", t05_text(), 1, ["text_too_many_entries"]),
        ("t06", "sitemap.txt.gz", "https://example.com/sitemap.txt.gz", gzip_bytes(t06_text), 0, []),
        ("t07", "sitemap.txt", "https://example.com/sitemap.txt",
         b"\xef\xbb\xbfhttps://example.com/one\nhttps://example.com/two\n", 0, []),
        ("r01", "feed.xml", "https://example.com/feed.xml", rss_clean, 0, []),
        ("r02", "feed.xml", "https://example.com/feed.xml", rss([
            rss_item("Alpha", "https://example.com/alpha", "2026-11-02T10:00:00Z"),
            rss_item("Beta", None, "2026-11-02T11:00:00Z"),
        ]), 1, ["feed_item_missing_link"]),
        ("r03", "feed.xml", "https://example.com/feed.xml", rss([
            rss_item("Alpha", "https://example.com/alpha", "not-a-date"),
            rss_item("Beta", "https://example.com/beta", "2026-11-02T11:00:00Z"),
        ]), 1, ["lastmod_invalid"]),
        ("r04", "feed.xml", "https://example.com/feed.xml", rss([
            rss_item("Alpha", "/relative", "2026-11-02T10:00:00Z"),
            rss_item("Beta", "https://example.com/beta", "2026-11-02T11:00:00Z"),
        ]), 1, ["loc_not_absolute"]),
        ("a01", "atom.xml", "https://example.com/atom.xml", atom_clean, 0, []),
        ("a02", "atom.xml", "https://example.com/atom.xml", atom([
            atom_entry("Alpha", None, "2026-11-02T10:00:00Z"),
            atom_entry("Beta", "https://example.com/beta", "2026-11-02T11:00:00Z"),
        ]), 1, ["feed_item_missing_link"]),
        ("a03", "atom.xml", "https://example.com/atom.xml", atom([
            atom_entry("Alpha", "https://example.com/alpha", "2026-13-45T99:99:99Z"),
            atom_entry("Beta", "https://example.com/beta", "2026-11-02T11:00:00Z"),
        ]), 1, ["lastmod_invalid"]),
        ("s01", "sitemap-index.xml", "https://example.com/sitemap-index.xml", sitemapindex([
            "https://example.com/sitemap.txt",
            "https://example.com/feed.rss",
            "https://example.com/feed.atom",
        ]), 0, []),
        ("d01", "page.xml", "https://example.com/page.xml",
         XML_DECL + b"<html><head><title>x</title></head><body><p>nope</p></body></html>\n", 2,
         ["format_unsupported"]),
    ]


def write_json(path, document):
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(document, indent=2) + "\n")


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=HERE)
    options = parser.parse_args(argv[1:])
    out_root = os.path.abspath(options.out)
    os.makedirs(out_root, exist_ok=True)
    for case_id, file_name, sitemap_url, data, exit_code, findings in cases():
        case_dir = os.path.join(out_root, case_id)
        os.makedirs(case_dir, exist_ok=True)
        path = os.path.join(case_dir, file_name)
        with open(path, "wb") as handle:
            handle.write(data)
        write_json(
            os.path.join(case_dir, "manifest.json"),
            {"version": 1, "checks": [{"id": case_id, "file": file_name, "sitemapUrl": sitemap_url}]},
        )
        write_json(os.path.join(case_dir, "expect.json"), {"exit": exit_code, "findings": findings})
        print(
            "case %s file=%s bytes=%d sha256=%s exit=%d findings=%s"
            % (
                case_id,
                file_name,
                len(data),
                hashlib.sha256(data).hexdigest(),
                exit_code,
                ",".join(findings) if findings else "-",
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
