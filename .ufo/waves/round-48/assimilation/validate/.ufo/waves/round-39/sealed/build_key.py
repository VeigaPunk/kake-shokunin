#!/usr/bin/env python3
"""Round-39 C1 sealed key (L1, hand-written expectations). Writes cases.json next to this file."""
import base64, json, os

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
H = '<?xml version="1.0" encoding="UTF-8"?>\n'


def us(*entries, root="urlset", extra=""):
    return H + f'<{root} xmlns="{NS}">' + extra + "".join(entries) + f"</{root}>\n"


def u(loc, *more):
    return "<url><loc>" + loc + "</loc>" + "".join(more) + "</url>"


def sm(loc, *more):
    return "<sitemap><loc>" + loc + "</loc>" + "".join(more) + "</sitemap>"


def T(s):
    return {"text": s}


def B(b):
    return {"b64": base64.b64encode(b).decode()}


def C(cid, sitemap, file):
    return {"id": cid, "file": file, "sitemapUrl": sitemap}


def X(status, *fs, error=None):
    return {"status": status, "error": error, "findings": [[c, n] for c, n in fs]}


CLEAN = X("clean")
S = "https://ex.test/sitemap.xml"
cases = []


def case(cid, files, checks, expect_checks, exit_code, verdict, rule):
    seen, lst = {}, []
    for c in checks:
        k = c.get("id")
        seen[k] = seen.get(k, 0) + 1
        key = k if seen[k] == 1 else f"{k}#{seen[k]}"
        e = expect_checks[key]
        lst.append({"id": k, "status": e["status"], "error": e["error"], "findings": e["findings"]})
    assert len(lst) == len(expect_checks), cid
    cases.append({"id": cid, "rule": rule, "files": files,
                  "manifest": {"version": 1, "checks": checks},
                  "expect": {"exit": exit_code, "verdict": verdict, "checks": lst}})


ok1 = us(u("https://ex.test/a"))

# 1 (a) encoding: UTF-16, BOM + lowercase utf-8 decl, ISO-8859-1 decl on ASCII bytes, utf8 spelling
case("k01", {
    "f1.xml": B(("\ufeff" + ok1.replace('encoding="UTF-8"', 'encoding="UTF-16"')).encode("utf-16-le")),
    "f2.xml": B(b"\xef\xbb\xbf" + ok1.replace('encoding="UTF-8"', 'encoding="utf-8"').encode()),
    "f3.xml": T(ok1.replace('encoding="UTF-8"', 'encoding="ISO-8859-1"')),
    "f4.xml": T(ok1.replace('encoding="UTF-8"', "encoding='utf8'")),
    "f5.xml": T(us(u("https://ex.test/%C3%BCmlat?q=1&amp;r=2"))),
}, [C("r7", S, "f1.xml"), C("b2", S, "f2.xml"), C("m9", S, "f3.xml"), C("p4", S, "f4.xml"), C("z1", S, "f5.xml")],
    {"r7": X("findings", ["encoding_invalid", None]), "b2": CLEAN,
     "m9": X("findings", ["encoding_invalid", None]), "p4": X("findings", ["encoding_invalid", None]),
     "z1": CLEAN}, 1, "failed-policy", "a")

# 2 (a)/(b): invalid UTF-8 byte, raw ampersand, non-ASCII loc in UTF-8, no XML declaration
case("k02", {
    "a.xml": B(ok1.replace("/a<", "/\xfc<").encode("latin-1")),
    "b.xml": T(us(u("https://ex.test/x?a=1&b=2"))),
    "c.xml": T(us(u("https://ex.test/\u00fcmlat"))),
    "d.xml": T(f'<urlset xmlns="{NS}"><url><loc>https://ex.test/n</loc></url></urlset>'),
}, [C("q1", S, "a.xml"), C("q2", S, "b.xml"), C("q3", S, "c.xml"), C("q4", S, "d.xml")],
    {"q1": X("findings", ["encoding_invalid", None]), "q2": X("findings", ["xml_malformed", None]),
     "q3": CLEAN, "q4": CLEAN}, 1, "failed-policy", "a,b")

# 3 (b): DOCTYPE vs comment + PI; truncated document; mismatched tags
case("k03", {
    "d.xml": T(H + f'<!DOCTYPE urlset [<!ENTITY e "https://ex.test/e">]><urlset xmlns="{NS}"><url><loc>&e;</loc></url></urlset>'),
    "c.xml": T(H + f'<!-- generated --><?pi data?><urlset xmlns="{NS}"><!-- x --><url><loc>https://ex.test/c</loc></url></urlset>'),
    "t.xml": T(H + f'<urlset xmlns="{NS}"><url><loc>https://ex.test/t</loc></url>'),
    "e.xml": T(H + f'<urlset xmlns="{NS}"><url><loc>https://ex.test/e</url></loc></urlset>'),
}, [C("w1", S, "d.xml"), C("w2", S, "c.xml"), C("w3", S, "t.xml"), C("w4", S, "e.xml")],
    {"w1": X("findings", ["doctype_present", None]), "w2": CLEAN,
     "w3": X("findings", ["xml_malformed", None]), "w4": X("findings", ["xml_malformed", None])},
    1, "failed-policy", "b")

# 4 (c) root: wrong ns, no ns, prefixed right ns, sitemapindex, wrong local name
case("k04", {
    "1.xml": T(H + '<urlset xmlns="http://www.google.com/schemas/sitemap/0.84"><url><loc>https://ex.test/a</loc></url></urlset>'),
    "2.xml": T(H + '<urlset><url><loc>https://ex.test/a</loc></url></urlset>'),
    "3.xml": T(H + f'<sm:urlset xmlns:sm="{NS}"><sm:url><sm:loc>https://ex.test/p</sm:loc></sm:url></sm:urlset>'),
    "4.xml": T(us(sm("https://ex.test/s1.xml"), root="sitemapindex")),
    "5.xml": T(H + f'<urlSet xmlns="{NS}"><url><loc>https://ex.test/a</loc></url></urlSet>'),
    "6.xml": T(H + f'<x:urlset xmlns:x="http://other.test/ns" xmlns="{NS}"><url><loc>https://ex.test/a</loc></url></x:urlset>'),
}, [C("a1", S, "1.xml"), C("a2", S, "2.xml"), C("a3", S, "3.xml"), C("a4", S, "4.xml"),
    C("a5", S, "5.xml"), C("a6", S, "6.xml")],
    {"a1": X("findings", ["root_invalid", None]), "a2": X("findings", ["root_invalid", None]),
     "a3": CLEAN, "a4": CLEAN, "a5": X("findings", ["root_invalid", None]),
     "a6": X("findings", ["root_invalid", None])}, 1, "failed-policy", "c")

# 5 (d) entries: empty, extension-only root child, one entry, index with url children
case("k05", {
    "e.xml": T(H + f'<urlset xmlns="{NS}"></urlset>'),
    "x.xml": T(H + f'<urlset xmlns="{NS}" xmlns:i="http://img.test/1"><i:image>https://ex.test/i.png</i:image></urlset>'),
    "o.xml": T(us(u("https://ex.test/o"), extra='<i:meta xmlns:i="http://img.test/1">m</i:meta>')),
    "w.xml": T(H + f'<sitemapindex xmlns="{NS}"><url><loc>https://ex.test/u</loc></url></sitemapindex>'),
}, [C("e1", S, "e.xml"), C("e2", S, "x.xml"), C("e3", S, "o.xml"), C("e4", S, "w.xml")],
    {"e1": X("findings", ["no_entries", None]), "e2": X("findings", ["no_entries", None]), "e3": CLEAN,
     "e4": X("findings", ["element_unexpected", None], ["no_entries", None])}, 1, "failed-policy", "d")

# 6 (d)/(e) unexpected elements: sitemap child in urlset; sitemap-ns child in entry; index entry changefreq;
#   extension children inside an entry ignored; entry numbering skips non-entries
case("k06", {
    "m.xml": T(us(u("https://ex.test/1"), sm("https://ex.test/s.xml"), u("https://ex.test/2", "<title>t</title>"))),
    "g.xml": T(us(u("https://ex.test/g", '<image:image xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"><image:loc>https://cdn.other.test/i.png</image:loc></image:image>'))),
    "i.xml": T(us(sm("https://ex.test/a.xml"), sm("https://ex.test/b.xml", "<changefreq>daily</changefreq>"), root="sitemapindex")),
    "p.xml": T(us(sm("https://ex.test/c.xml", "<priority>0.5</priority>", "<lastmod>2024-01-01</lastmod>"), root="sitemapindex")),
}, [C("u1", S, "m.xml"), C("u2", S, "g.xml"), C("u3", S, "i.xml"), C("u4", S, "p.xml")],
    {"u1": X("findings", ["element_unexpected", None], ["element_unexpected", 2]), "u2": CLEAN,
     "u3": X("findings", ["element_unexpected", 2]), "u4": X("findings", ["element_unexpected", 1])},
    1, "failed-policy", "d,e")

# 7 (e) loc missing / repeated / loc in another namespace / prefixed loc
case("k07", {
    "l.xml": T(us(u("https://ex.test/1"), "<url><lastmod>2024-01-01</lastmod></url>",
                  "<url><loc>https://ex.test/3</loc><loc>https://ex.test/3b</loc></url>",
                  '<url><o:loc xmlns:o="http://other.test/ns">https://ex.test/4</o:loc></url>')),
    "q.xml": T(H + f'<urlset xmlns="{NS}" xmlns:s="{NS}"><url><s:loc>https://ex.test/q</s:loc></url></urlset>'),
    "r.xml": T(us("<url><loc>ftp://bad</loc><loc>https://ex.test/r</loc></url>")),
}, [C("v1", S, "l.xml"), C("v2", S, "q.xml"), C("v3", S, "r.xml")],
    {"v1": X("findings", ["loc_missing", 2], ["loc_repeated", 3], ["loc_missing", 4]), "v2": CLEAN,
     "v3": X("findings", ["loc_repeated", 1])}, 1, "failed-policy", "e")

# 8 (e) field_repeated skips value rule; order not checked
case("k08", {
    "r.xml": T(us(u("https://ex.test/1", "<lastmod>bad</lastmod>", "<lastmod>worse</lastmod>"),
                  u("https://ex.test/2", "<priority>0.1</priority>", "<priority>0.2</priority>"),
                  u("https://ex.test/3", "<changefreq>daily</changefreq>", "<changefreq>daily</changefreq>"))),
    "o.xml": T(us("<url><priority>0.4</priority><changefreq>never</changefreq><lastmod>2020-02-29</lastmod><loc>https://ex.test/o</loc></url>")),
    "i.xml": T(us(sm("https://ex.test/s.xml", "<lastmod>2024-01-01</lastmod>", "<lastmod>2024-01-02</lastmod>"), root="sitemapindex")),
}, [C("f1", S, "r.xml"), C("f2", S, "o.xml"), C("f3", S, "i.xml")],
    {"f1": X("findings", ["field_repeated", 1], ["field_repeated", 2], ["field_repeated", 3]), "f2": CLEAN,
     "f3": X("findings", ["field_repeated", 1])}, 1, "failed-policy", "e")

# 9 (f) entry count: 50,000 clean, 50,001 finding (generated)
case("k09", {
    "n0.xml": {"gen": {"kind": "entries", "n": 50000, "base": "https://ex.test/p/"}},
    "n1.xml": {"gen": {"kind": "entries", "n": 50001, "base": "https://ex.test/p/"}},
}, [C("c0", S, "n0.xml"), C("c1", S, "n1.xml")],
    {"c0": CLEAN, "c1": X("findings", ["too_many_entries", None])}, 1, "failed-policy", "f")

# 10 (f) size: exactly 52,428,800 bytes clean; one byte more gives too_large only (even with a bad entry)
case("k10", {
    "s0.xml": {"gen": {"kind": "padded", "bytes": 52428800, "body": us(u("https://ex.test/s0"))}},
    "s1.xml": {"gen": {"kind": "padded", "bytes": 52428801, "body": us(u("ftp://bad"))}},
}, [C("g0", S, "s0.xml"), C("g1", S, "s1.xml")],
    {"g0": CLEAN, "g1": X("findings", ["too_large", None])}, 1, "failed-policy", "f")

# 11 (g) absolute: relative, ftp, upper-case scheme/host, empty host, bad port, whitespace around
case("k11", {
    "a.xml": T(us(u("/rel"), u("ftp://ex.test/f"), u("HTTPS://EX.test/up"), u("https:///nohost"),
                  u("\n\t https://ex.test/ws \r\n"), u("ex.test/noscheme"))),
}, [C("h1", S, "a.xml")],
    {"h1": X("findings", ["loc_not_absolute", 1], ["loc_not_absolute", 2], ["loc_not_absolute", 4],
             ["loc_not_absolute", 6])}, 1, "failed-policy", "g")

# 12 (g) length: 2047 chars clean (also with non-ASCII, >2048 bytes), 2048 chars finding, whitespace not counted
base = "https://ex.test/"
case("k12", {
    "l.xml": T(us(u(base + "a" * (2047 - len(base))), u(base + "b" * (2048 - len(base))),
                  u(base + "\u00e9" * (2047 - len(base))), u("  " + base + "c" * (2047 - len(base)) + "  "),
                  u(base + "d" * (3000 - len(base))))),
    "k.xml": T(us(u(base + "k"))),
}, [C("L1", S, "l.xml"), C("L2", S, "k.xml")],
    {"L1": X("findings", ["loc_too_long", 2], ["loc_too_long", 5]), "L2": CLEAN}, 1, "failed-policy", "g")

# 13 (h) scope in a directory urlset
S13 = "http://ex.test/cat/sitemap.xml"
case("k13", {
    "s.xml": T(us(u("http://ex.test/cat/x"), u("http://ex.test/catalog/x"), u("http://EX.test:80/cat/y"),
                  u("https://ex.test/cat/z"), u("http://sub.ex.test/cat/"), u("http://ex.test/Cat/x"),
                  u("http://ex.test:8080/cat/x"), u("http://ex.test/cat/"), u("http://ex.test/cat"),
                  u("http://ex.test/cat/../img/x"), u("http://ex.test/%63at/x"))),
}, [C("s1", S13, "s.xml")],
    {"s1": X("findings", ["loc_out_of_scope", 2], ["loc_out_of_scope", 4], ["loc_out_of_scope", 5],
             ["loc_out_of_scope", 6], ["loc_out_of_scope", 7], ["loc_out_of_scope", 9],
             ["loc_out_of_scope", 11])}, 1, "failed-policy", "h")

# 14 (h) root sitemap, default ports, empty path, query on sitemapUrl
S14 = "https://ex.test/sitemap.xml?v=2"
case("k14", {
    "r.xml": T(us(u("https://ex.test"), u("https://ex.test:443/a"), u("http://ex.test/a"),
                  u("https://ex.test:80/a"), u("https://ex.test/deep/er/x?y=1"))),
    "p.xml": T(us(u("http://ex.test:8443/m/a"), u("http://ex.test/m/b"))),
}, [C("t1", S14, "r.xml"), C("t2", "http://ex.test:8443/m/s.xml", "p.xml")],
    {"t1": X("findings", ["loc_out_of_scope", 3], ["loc_out_of_scope", 4]),
     "t2": X("findings", ["loc_out_of_scope", 2])}, 1, "failed-policy", "h")

# 15 (h) sitemapindex: host-only scope; directory not required
S15 = "https://ex.test/maps/index.xml"
case("k15", {
    "i.xml": T(us(sm("https://ex.test/other/s.xml"), sm("https://cdn.ex.test/s.xml"), sm("https://ex.test/maps/s2.xml"),
                  sm("http://ex.test/maps/s3.xml"), root="sitemapindex")),
    "j.xml": T(us(sm("https://EX.TEST:443/z.xml"), root="sitemapindex")),
}, [C("i1", S15, "i.xml"), C("i2", S15, "j.xml")],
    {"i1": X("findings", ["loc_out_of_scope", 2], ["loc_out_of_scope", 4]), "i2": CLEAN}, 1, "failed-policy", "h")

# 16 (i) lastmod forms
lm_ok = ["2024-02-29", "2005-01-01T18:00+00:00", "2004-12-23T18:00:15Z", "1997-07-16T19:20:30.45+01:00",
         " 2000-02-29T23:59:59-12:30 ", "2005-01-01T00:00:00.1Z"]
lm_bad = ["2023-02-29", "2005-01", "2005", "2005-01-01T18:00:15", "2005-13-01", "2005-01-01T24:00Z",
          "1900-02-29", "2005-01-01T18:60Z", "2005-01-01T18:00:60Z", "2005-01-01T18:00+0100",
          "2005-1-01", "2005-01-01 18:00Z", "2005-04-31", "2005-01-01T18:00:15.Z"]
ents = [u(f"https://ex.test/l{i}", f"<lastmod>{v}</lastmod>") for i, v in enumerate(lm_ok + lm_bad)]
case("k16", {
    "l.xml": T(us(*ents)),
    "i.xml": T(us(sm("https://ex.test/a.xml", "<lastmod>2005-01</lastmod>"), sm("https://ex.test/b.xml", "<lastmod>2005-01-01</lastmod>"), root="sitemapindex")),
}, [C("d1", S, "l.xml"), C("d2", S, "i.xml")],
    {"d1": X("findings", *[["lastmod_invalid", len(lm_ok) + j + 1] for j in range(len(lm_bad))]),
     "d2": X("findings", ["lastmod_invalid", 1])}, 1, "failed-policy", "i")

# 17 (j) changefreq
cf = ["weekly", " daily\n", "Daily", "fortnightly", "never", "weekly\u00a0", "", "always", "HOURLY"]
case("k17", {
    "c.xml": T(us(*[u(f"https://ex.test/c{i}", f"<changefreq>{v}</changefreq>") for i, v in enumerate(cf)])),
}, [C("j1", S, "c.xml")],
    {"j1": X("findings", ["changefreq_invalid", 3], ["changefreq_invalid", 4], ["changefreq_invalid", 6],
             ["changefreq_invalid", 7], ["changefreq_invalid", 9])}, 1, "failed-policy", "j")

# 18 (k) priority
pr = ["1.0", ".5", "1.", "+0.3", "1.01", "-0.1", "1e-1", " 0.5 ", "NaN", "-0.0", "1.0000000000000000001",
      "0", "", "0,5", "1.00000"]
case("k18", {
    "p.xml": T(us(*[u(f"https://ex.test/p{i}", f"<priority>{v}</priority>") for i, v in enumerate(pr)])),
}, [C("y1", S, "p.xml")],
    {"y1": X("findings", ["priority_invalid", 5], ["priority_invalid", 6], ["priority_invalid", 7],
             ["priority_invalid", 9], ["priority_invalid", 11], ["priority_invalid", 13],
             ["priority_invalid", 14])}, 1, "failed-policy", "k")

# 19 errors: missing file, relative sitemapUrl, duplicate id, '..' path, non-string member; clean checks alongside
case("k19", {
    "ok.xml": T(us(u("https://ex.test/ok"))),
    "sub/n.xml": T(us(u("https://ex.test/n"))),
}, [C("o1", S, "ok.xml"), C("o2", S, "missing.xml"), C("o3", "/sitemap.xml", "ok.xml"), C("o1", S, "ok.xml"),
    C("o5", S, "sub/../ok.xml"), {"id": "o6", "file": "ok.xml", "sitemapUrl": 5}, C("o7", S, "sub/n.xml")],
    {"o1": CLEAN, "o2": X("error", error="file_unreadable"), "o3": X("error", error="check_invalid"),
     "o1#2": X("error", error="check_invalid"), "o5": X("error", error="check_invalid"),
     "o6": X("error", error="check_invalid"), "o7": CLEAN}, 2, "could-not-evaluate", "manifest")

# 20 manifest input_invalid (version 2)
cases.append({"id": "k20", "rule": "manifest", "files": {"ok.xml": T(ok1)},
              "manifest": {"version": 2, "checks": [C("x1", S, "ok.xml")]},
              "expect": {"exit": 2, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}})

# 21 clean verdict: all checks clean -> exit 0
case("k21", {
    "a.xml": T(us(u("https://ex.test/a", "<lastmod>2024-01-01</lastmod>", "<changefreq>daily</changefreq>", "<priority>0.8</priority>"))),
    "b.xml": T(us(sm("https://ex.test/a.xml", "<lastmod>2024-01-01T10:00:00Z</lastmod>"), root="sitemapindex")),
}, [C("n1", S, "a.xml"), C("n2", S, "b.xml")], {"n1": CLEAN, "n2": CLEAN}, 0, "clean", "verdict")

# 22 manifest not JSON; 23 empty checks; 24 usage error (no manifest path)
cases.append({"id": "k22", "rule": "manifest", "files": {"ok.xml": T(ok1)}, "manifestRaw": "{version: 1, checks: []",
              "expect": {"exit": 2, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}})
cases.append({"id": "k23", "rule": "manifest", "files": {"ok.xml": T(ok1)}, "manifest": {"version": 1, "checks": []},
              "expect": {"exit": 2, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}})
cases.append({"id": "k24", "rule": "usage", "files": {"ok.xml": T(ok1)}, "manifest": {"version": 1, "checks": [C("x", S, "ok.xml")]},
              "argv": ["--manifest"], "expect": {"exit": 64}})

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cases.json")
with open(out, "w") as fh:
    json.dump({"version": 1, "cases": cases}, fh, indent=1, sort_keys=True)
print(out, len(cases))
