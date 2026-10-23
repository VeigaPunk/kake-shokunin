#!/usr/bin/env python3
"""PRIVATE: writes cases.json (the round-36 sealed key). Run once before the declaration.

Every case of a bullet carries one check per sub-rule of that bullet, so skipping any sub-rule
fails all four cases of its bullet.
"""
import base64, json
from pathlib import Path

H = "text/html; charset=utf-8"
cases = []


def page(title, body):
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<title>%s</title>\n"
            "<link rel=\"stylesheet\" href=\"/assets/site.css\">\n</head>\n<body>\n<main>\n%s\n</main>\n"
            "<footer><p>&copy; 2026 Example Docs</p></footer>\n</body>\n</html>\n" % (title, body)).encode("utf-8")


def b64(b: bytes):
    return {"b64": base64.b64encode(b).decode()}


CT = ["text/html; charset=utf-8", "text/html", "text/html;charset=UTF-8", "TEXT/HTML; Charset=\"utf-8\""]


def ok200(cid, url, quote, body, ctype=H):
    return {"id": cid, "url": url, "quote": quote, "hops": [{"status": 200}], "contentType": ctype, "body": body}


def add(cid, bullet, files, checks, findings):
    inputs = {"input_invalid", "check_invalid", "charset_unsupported"}
    if any(r in inputs for _, r, _ in findings):
        exit_, verdict = 2, "could-not-evaluate"
    elif findings:
        exit_, verdict = 1, "failed-policy"
    else:
        exit_, verdict = 0, "clean"
    cases.append({"id": cid, "bullet": bullet, "files": {k: b64(v) for k, v in files.items()},
                  "manifest": {"version": 1, "checks": checks},
                  "expect": {"exit": exit_, "verdict": verdict,
                             "findings": [{"check": c, "reason": r, "target": t} for c, r, t in findings]}})


GUIDE = page("Publishing guide", "<h1>Publishing guide</h1>\n<p>Upload the built site and keep the old URLs working.</p>")

# (a) final status: 404 -> gone, 410 -> gone, any other non-200 -> http_error, 200 -> quote check
A = [("docs.example.org", 403, "Forbidden area"), ("status.example.net", 503, "All systems"),
     ("api.example.org", 204, "pong"), ("feeds.example.com", 429, "slow down")]
for i, (host, other, q) in enumerate(A):
    add("k%02d" % (i + 1), "a", {"p.html": GUIDE},
        [{"id": "x1", "url": "https://%s/guide/old-%d" % (host, i), "quote": "keep the old URLs working", "hops": [{"status": 404}]},
         {"id": "x2", "url": "https://%s/legacy/faq-%d" % (host, i), "quote": "Frequently asked", "hops": [{"status": 410}]},
         {"id": "x3", "url": "https://%s/other/%d" % (host, i), "quote": q, "hops": [{"status": other}]},
         ok200("x4", "https://%s/guide/publishing" % host, "keep the old URLs working", "p.html"),
         {"id": "x5", "url": "https://%s/partial/%d" % (host, i), "quote": "keep", "hops": [{"status": (206, 202, 203, 226)[i]}]}],
        [("x1", "gone", None), ("x2", "gone", None), ("x3", "http_error", None), ("x5", "http_error", None)])

# (b) redirects: leading permanent run -> one moved (target = resolved location of its last hop);
# a chain starting with a temporary hop -> no moved; relative locations resolved per RFC 3986.
B = [("https://docs.example.org/a/b/c/page", "../x/page", "https://docs.example.org/a/b/x/page", 302,
      "https://b.example.com/one", "https://b.example.com/two/", "three", "https://b.example.com/two/three", 307),
     ("https://www.example.com/files/report", "//cdn.example.net/r?id=7", "https://cdn.example.net/r?id=7", 303,
      "http://example.net/start", "/v2/start", "../v3/", "http://example.net/v3/", 302),
     ("https://example.org/old/guide.html", "/new/guide/", "https://example.org/new/guide/", 307,
      "https://site.example.io/p/q", "r/s", "?page=2", "https://site.example.io/p/r/s?page=2", 303),
     ("http://legacy.example.com/x/y", "https://modern.example.com/y", "https://modern.example.com/y", 302,
      "https://a.example.org/1/2/3", "./4", "/5/6", "https://a.example.org/5/6", 307)]
for i, (u1, loc1, t1, temp, u3, l3a, l3b, t3, temp3) in enumerate(B):
    perm1 = (301, 308)[i % 2]
    add("k%02d" % (i + 5), "b", {"p.html": GUIDE},
        [{"id": "x1", "url": u1, "quote": "Upload the built site",
          "hops": [{"status": perm1, "location": loc1}, {"status": 200}], "contentType": H, "body": "p.html"},
         {"id": "x2", "url": "https://docs.example.org/t/%d" % i, "quote": "Upload the built site",
          "hops": [{"status": temp, "location": "https://mirror.example.org/t/%d" % i},
                   {"status": 301, "location": "/t/%d/v2" % i}, {"status": 200}], "contentType": H, "body": "p.html"},
         {"id": "x3", "url": u3, "quote": "keep the old URLs working",
          "hops": [{"status": 301, "location": l3a}, {"status": 308, "location": l3b},
                   {"status": temp3, "location": "/elsewhere"}, {"status": 404}]}],
        [("x1", "moved", t1), ("x3", "moved", t3), ("x3", "gone", None)])

# (c) HTML text: tags removed, script/style/template contents and comments removed, references
# decoded, title text kept.
C = [("The <code>include</code> setting overrides the <em>default</em> exclusion.",
      "The include setting overrides the default exclusion.", "Release notes for version 5",
      "Caf&eacute; &amp; bar &#8220;quoted&#8221; &#x2014; open daily.", "Café & bar “quoted” — open daily.",
      "Configuration reference"),
     ("Run <kbd>make</kbd> then <a href=\"/deploy\">deploy the <strong>site</strong></a> today.",
      "Run make then deploy the site today.", "Draft text never shown",
      "Fish &lt;and&gt; chips &#38; peas &#169; 2026", "Fish <and> chips & peas © 2026", "Kitchen handbook"),
     ("A <span class=\"k\">permanent</span> <i>redirect</i> keeps old links alive.",
      "A permanent redirect keeps old links alive.", "Internal build marker",
      "Na&iuml;ve &ldquo;smart&rdquo; quotes &hellip; and &nbsp;more", "Naïve “smart” quotes … and more",
      "Redirect notes"),
     ("Fetch <tt>/robots.txt</tt> before <b>crawling</b>.", "Fetch /robots.txt before crawling.",
      "Secret staging banner", "Price &euro;5 &times; 3 &equals; &euro;15", "Price €5 × 3 = €15", "Crawler guide")]
for i, (inline, q_inline, hidden, ent, q_ent, title) in enumerate(C):
    body = page(title,
                "<p>%s</p>\n<script>var s = \"%s\";</script>\n<p>%s</p>" % (inline, hidden + " one", ent))
    styl = page("Style %d" % i, "<style>.b::after { content: \"%s two\"; }</style>\n<p>Visible copy.</p>" % hidden)
    tmpl = page("Template %d" % i, "<template id=\"row\"><p>%s three</p></template>\n<p>Visible copy.</p>" % hidden)
    comm = page("Comment %d" % i, "<!-- build: a > b; %s four -->\n<p>Visible copy.</p>" % hidden)
    add("k%02d" % (i + 9), "c", {"p.html": body, "s.html": styl, "t.html": tmpl, "m.html": comm},
        [ok200("x1", "https://docs.example.org/c/%d" % i, q_inline, "p.html", CT[i % 4]),
         ok200("x2", "https://docs.example.org/c/%d" % i, hidden + " one", "p.html", CT[(i + 1) % 4]),
         ok200("x3", "https://docs.example.org/s/%d" % i, hidden + " two", "s.html", CT[(i + 2) % 4]),
         ok200("x4", "https://docs.example.org/t/%d" % i, hidden + " three", "t.html", CT[(i + 3) % 4]),
         ok200("x5", "https://docs.example.org/m/%d" % i, hidden + " four", "m.html", "application/xhtml+xml" if i % 2 else CT[i % 4]),
         ok200("x6", "https://docs.example.org/c/%d" % i, q_ent, "p.html", CT[(i + 2) % 4]),
         ok200("x7", "https://docs.example.org/c/%d" % i, title, "p.html", CT[(i + 1) % 4])],
        [("x2", "quote_missing", None), ("x3", "quote_missing", None), ("x4", "quote_missing", None),
         ("x5", "quote_missing", None)])

# (d) normalization: NFKC, every whitespace character deleted, case-sensitive.
D = [("a user\n      agent with&nbsp;link-editing\tcapability can replace references",
      "a user agent with link-editing capability", "<td>Moved</td><td>Permanently</td>", "Moved Permanently",
      "Place the \ufb01le under the \uff32\uff26\uff23 path.", "Place the file under the RFC path.",
      "The server answers moved permanently.", "answers Moved Permanently"),
     ("keep\u3000the old\r\n URLs   working", "keep the old URLs working", "<li>Temporary</li><li>Redirect</li>",
      "Temporary Redirect", "Version \u2163 of the \ufb02ow chart", "Version IV of the flow chart",
      "Gone means the resource is gone for good.", "GONE means"),
     ("dot\u2003paths are\n\n excluded by default", "dot paths are excluded by default",
      "<dt>Location</dt><dd>header</dd>", "Location header", "Use \u2460 then \u2461 in order",
      "Use 1 then 2 in order", "the include setting", "The Include Setting"),
     ("charset\u00a0labels  are\tcase-insensitive", "charset labels are case-insensitive",
      "<th>Byte</th><th>order</th><th>mark</th>", "Byte order mark", "\uff28\uff34\uff34\uff30 caching rules",
      "HTTP caching rules", "Normalization Form KC", "normalization form kc")]
for i, (ws, q_ws, cells, q_cells, compat, q_compat, cased, q_cased) in enumerate(D):
    files = {"w.html": page("Whitespace %d" % i, "<p>%s</p>" % ws),
             "t.html": page("Cells %d" % i, "<table><tr>%s</tr></table>" % cells if "<td>" in cells or "<th>" in cells
                            else ("<ul>%s</ul>" % cells if "<li>" in cells else "<dl>%s</dl>" % cells)),
             "k.html": page("Compat %d" % i, "<p>%s</p>" % compat),
             "c.html": page("Case %d" % i, "<p>%s</p>" % cased)}
    add("k%02d" % (i + 13), "d", files,
        [ok200("x1", "https://example.org/w/%d" % i, q_ws, "w.html", CT[(i + 3) % 4]),
         ok200("x2", "https://example.org/t/%d" % i, q_cells, "t.html", CT[(i + 2) % 4]),
         ok200("x3", "https://example.org/k/%d" % i, q_compat, "k.html", CT[(i + 1) % 4]),
         ok200("x4", "https://example.org/c/%d" % i, q_cased, "c.html", "text/plain; charset=utf-8" if i % 2 else CT[i % 4])],
        [("x4", "quote_missing", None)])

# (e) media types: text/plain read as is; HTML types case-insensitive and with parameters;
# application/xhtml+xml processed as HTML; any other type -> unsupported_type.
E = [("The <Location> field &amp; its relative reference.", "application/pdf", "Text/HTML; charset=UTF-8"),
     ("Compare a <b> c with care.", "application/json", "TEXT/HTML"),
     ("Lines like <!-- keep --> stay; &lt; too.", "image/svg+xml", "text/HTML;charset=utf-8"),
     ("Use <script>alert(1)</script> as an example string.", "application/octet-stream", "Text/Html; Charset=UTF-8")]
for i, (plain, other, upper) in enumerate(E):
    files = {"p.txt": ("Section %d\n   %s\n" % (i, plain)).encode("utf-8"),
             "o.bin": ("%%DATA\nkeep the old URLs working\n" ).encode("utf-8"),
             "u.html": page("Upper %d" % i, "<p>Mixed <b>case</b> media type %d.</p>" % i),
             "x.xhtml": ("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<html xmlns=\"http://www.w3.org/1999/xhtml\"><head><title>X</title></head>"
                         "<body><p>An <em>XHTML</em> page &amp; its text %d.</p></body></html>\n" % i).encode("utf-8"),
             "a.txt": ("Menu: Fish &amp; chips %d, served daily.\n" % i).encode("utf-8"),
             "y.xhtml": ("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<html xmlns=\"http://www.w3.org/1999/xhtml\"><head><title>Y</title>"
                         "<script>var t = \"inline script words %d\";</script></head><body><p>Visible.</p></body></html>\n" % i).encode("utf-8")}
    add("k%02d" % (i + 17), "e", files,
        [ok200("x1", "https://www.example.org/rfc-%d.txt" % i, plain, "p.txt", ("text/plain; charset=utf-8", "text/plain")[i % 2]),
         ok200("x2", "https://www.example.org/data-%d" % i, "keep the old URLs working", "o.bin", other),
         ok200("x3", "https://example.org/m/%d" % i, "Mixed case media type %d." % i, "u.html", upper),
         ok200("x4", "https://example.org/x/%d" % i, "An XHTML page & its text %d." % i, "x.xhtml", "application/xhtml+xml"),
         ok200("x5", "https://www.example.org/amp-%d.txt" % i, "Fish & chips %d" % i, "a.txt", ("text/plain", "Text/Plain; charset=utf-8")[i % 2]),
         ok200("x6", "https://example.org/y/%d" % i, "inline script words %d" % i, "y.xhtml", ("application/xhtml+xml", "Application/XHTML+XML; charset=utf-8")[i % 2])],
        [("x2", "unsupported_type", None), ("x5", "quote_missing", None), ("x6", "quote_missing", None)])

# (f) decoding: BOM wins over charset; windows-1252 labels; quoted labels; default UTF-8;
# labels outside UTF-8, UTF-16BE, UTF-16LE and windows-1252 -> charset_unsupported.
F = [("iso-8859-1", b"He said \x93ship it\x94 twice.", "He said “ship it” twice.", "shift_jis", "\ufeffR\u00e9sum\u00e9 du d\u00e9p\u00f4t", "utf-16be"),
     ("us-ascii", b"Built 2020\x962022 by the team.", "Built 2020–2022 by the team.", "gbk", "Stra\u00dfe und \u00dcberblick", "utf-16le"),
     ("latin1", b"Price \x80 9 \x85 more", "Price € 9 … more", "koi8-r", "na\u00efve caf\u00e9 menu", "utf-16be"),
     ("windows-1252", b"It\x92s a \x84quoted\x93 word", "It’s a „quoted“ word", "euc-kr", "\u00e5ngstr\u00f6m units", "utf-16le")]
for i, (label, cpbytes, q_cp, bad, bomtext, bomenc) in enumerate(F):
    bom = {"utf-16be": b"\xfe\xff", "utf-16le": b"\xff\xfe"}[bomenc]
    files = {"w.html": b"<html><body><p>" + cpbytes + b"</p></body></html>",
             "b.txt": bom + bomtext.lstrip("\ufeff").encode(bomenc),
             "u.html": ("<p>\u65e5\u672c\u8a9e %d</p>" % i).encode("utf-8"),
             "d.html": ("<p>Default decoding: \u00e9t\u00e9 %d</p>" % i).encode("utf-8"),
             "m.html": ("<p>Menu: caf\u00e9 cr\u00e8me %d</p>" % i).encode("utf-8")}
    q_bom = bomtext.lstrip("\ufeff")
    add("k%02d" % (i + 21), "f", files,
        [ok200("x1", "https://example.org/w/%d" % i, q_cp, "w.html", "text/html; charset=\"%s\"" % (label.upper() if i % 2 == 0 else label.capitalize())),
         ok200("x2", "https://example.org/b/%d" % i, q_bom, "b.txt", "text/plain; charset=iso-8859-1" if i % 2 else "text/plain; charset=utf-8"),
         ok200("x3", "https://example.jp/u/%d" % i, "\u65e5\u672c\u8a9e %d" % i, "u.html", "text/html; charset=%s" % bad),
         ok200("x4", "https://example.org/d/%d" % i, "Default decoding: \u00e9t\u00e9 %d" % i, "d.html", ("text/html", "text/plain")[i % 2]),
         ok200("x5", "https://example.org/m/%d" % i, "caf\u00e9 cr\u00e8me %d" % i, "m.html", ("text/html; charset=\"Windows-1252\"", "text/plain; charset=ISO-8859-1", "text/html; charset=us-ascii", "text/plain; charset=\"latin1\"")[i])],
        [("x3", "charset_unsupported", None), ("x5", "quote_missing", None)])

# (g) input faults: each malformed check gets check_invalid and the others are still evaluated.
for i in range(4):
    host = ("docs.example.org", "www.example.net", "site.example.io", "example.com")[i]
    add("k%02d" % (i + 25), "g", {"p.html": GUIDE, "../outside.html": GUIDE},
        [["not a check object", 7, None, ["list"]][i],
         {"id": "x2", "url": ["/guide/publishing", "ftp://%s/f" % host, "https:///nohost", "guide.html"][i],
          "quote": "Upload the built site", "hops": [{"status": 200}], "contentType": H, "body": "p.html"},
         ok200("x3", "https://%s/guide/publishing" % host, "Upload the built site", "../outside.html"),
         {"id": "x4", "url": "https://%s/a" % host, "quote": "Upload", "hops": [{"status": 301}, {"status": 200}],
          "contentType": H, "body": "p.html"},
         {"id": "x5", "url": "https://%s/b" % host, "quote": "Upload", "hops": [{"status": (308, 302, 307, 301)[i], "location": "/c"}]},
         {"id": "x6", "url": "https://%s/gone" % host, "quote": "x", "hops": [{"status": 410 if i % 2 else 404}]},
         ok200("x7", "https://%s/guide/publishing" % host, "A sentence that is not there", "p.html"),
         ok200("x8", "https://%s/guide/publishing" % host, "Upload the built site", "p.html")],
        [(None, "check_invalid", None), ("x2", "check_invalid", None), ("x3", "check_invalid", None),
         ("x4", "check_invalid", None), ("x5", "check_invalid", None), ("x6", "gone", None),
         ("x7", "quote_missing", None)])

assert len(cases) == 28 and len({c["id"] for c in cases}) == 28
for b in "abcdefg":
    assert sum(c["bullet"] == b for c in cases) == 4
key = {"version": 2, "round": 36, "claim": "C1", "target": 25, "cases": cases}
Path(__file__).with_name("cases.json").write_text(json.dumps(key, indent=1, sort_keys=True) + "\n", encoding="utf-8")
print("wrote", len(cases))
