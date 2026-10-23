#!/usr/bin/env python3
"""Fixture acceptance suite for sitemap_audit.py (round 39, claim C1).

Rule of record: .ufo/waves/round-39/c1-contract.md, sentences 1-34.
Retained sources: corpus/SOURCES.md S102 (sitemaps.org protocol text),
S103 (sitemap.xsd and siteindex.xsd), S104 (W3C NOTE-datetime).

Usage:
    python3 -B sitemap_audit_selftest.py --tool <path> [--fault-injection]
    python3 -B sitemap_audit_selftest.py --map

The suite materialises one small fixture directory per case (manifest plus the
files it names), runs the tool under test as a subprocess, and compares exit
status, verdict, per-check error and the finding set.  Every sentence 1-34 and
both polarities of rules (a)-(k) are covered; coverage is enforced before the
run is declared PASS.

--fault-injection additionally builds a tool that prints nothing and a
constant-clean tool, runs the same suite against each, and requires both to be
rejected.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
DECL = '<?xml version="1.0" encoding="UTF-8"?>\n'
SENTENCES = tuple(range(1, 35))
RULES = "abcdefghijk"


# --------------------------------------------------------------------------
# Fixture builders
# --------------------------------------------------------------------------

def doc(root, inner, xmlns=NS, decl=DECL):
    attr = "" if xmlns is None else ' xmlns="%s"' % xmlns
    return (decl + "<%s%s>" % (root, attr) + inner + "</%s>" % root).encode("utf-8")


def urlset(inner, **kwargs):
    return doc("urlset", inner, **kwargs)


def index(inner, **kwargs):
    return doc("sitemapindex", inner, **kwargs)


def url(*children):
    return "<url>%s</url>" % "".join(children)


def smap(*children):
    return "<sitemap>%s</sitemap>" % "".join(children)


def L(value):
    return "<loc>%s</loc>" % value


def ck(cid, file, sitemap_url="http://example.com/"):
    return {"id": cid, "file": file, "sitemapUrl": sitemap_url}


def mf(*checks, version=1):
    return {"version": version, "checks": list(checks)}


def E(cid, status, error=None, findings=()):
    return (cid, status, error, set(findings))


def _many_entries(count):
    body = "".join(
        '<url><loc>http://example.com/p%d</loc></url>' % number
        for number in range(count)
    )
    return urlset(body)


def _write_many(count, bad_last=False):
    if bad_last:
        body = "".join(
            '<url><loc>http://example.com/p%d</loc></url>' % number
            for number in range(count - 1)
        ) + "<url><loc>relative</loc></url>"
        payload = urlset(body)
    else:
        payload = _many_entries(count)

    def writer(path):
        with open(path, "wb") as handle:
            handle.write(payload)

    return writer


def _oversized(path):
    with open(path, "wb") as handle:
        handle.write(b'<?xml version="1.0"?>')
        handle.write(('<urlset xmlns="%s">' % NS).encode("utf-8"))
        handle.seek(52428800)
        handle.write(b" ")


# --------------------------------------------------------------------------
# Case table
# --------------------------------------------------------------------------

def build_cases():
    cases = []

    def add(name, files, sentences, rules=(), manifest=None, argv=None,
            expect_exit=0, verdict=None, error=None, checks=None,
            manifest_path="manifest.json", usage=False):
        cases.append({
            "name": name,
            "files": files,
            "sentences": list(sentences),
            "rules": list(rules),
            "manifest": manifest,
            "manifest_path": manifest_path,
            "argv": argv,
            "expect_exit": expect_exit,
            "verdict": verdict,
            "error": error,
            "checks": checks,
            "usage": usage,
        })

    clean_url = urlset(url(L("http://example.com/a")))
    clean_case_files = {"a.xml": clean_url}

    # --- sentence 1: invocation, one JSON document, nothing else -----------
    add("cli_clean_roundtrip", clean_case_files, [1, 33, 34],
        manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("cli_single_document_findings",
        {"bad.xml": urlset(url())}, [1, 33, 34],
        manifest=mf(ck("a", "bad.xml")), expect_exit=1,
        verdict="failed-policy", checks=[E("a", "findings", None, [("loc_missing", 1)])])

    # --- sentence 2: usage errors -----------------------------------------
    add("cli_no_args", {}, [2], argv=[], expect_exit=64, usage=True)
    add("cli_help", {}, [2], argv=["--help"], expect_exit=64, usage=True)
    add("cli_manifest_without_value", {}, [2], argv=["--manifest"], expect_exit=64,
        usage=True)
    add("cli_extra_argument", clean_case_files, [2], manifest=mf(ck("a", "a.xml")),
        argv=["--manifest", "manifest.json", "extra"], expect_exit=64, usage=True)
    add("cli_equals_form", clean_case_files, [2], manifest=mf(ck("a", "a.xml")),
        argv=["--manifest=manifest.json"], expect_exit=64, usage=True)
    add("cli_repeated_option", clean_case_files, [2], manifest=mf(ck("a", "a.xml")),
        argv=["--manifest", "manifest.json", "--manifest", "manifest.json"],
        expect_exit=64, usage=True)

    # --- sentence 3: manifest shape ---------------------------------------
    invalid_out = dict(expect_exit=2, verdict="could-not-evaluate",
                       error="input_invalid", checks=[])
    add("man_unreadable_file", {}, [3],
        argv=["--manifest", "nope.json"], **invalid_out)
    add("man_invalid_json", {}, [3], manifest=b"{", **invalid_out)
    add("man_not_object", {}, [3], manifest=b"[]", **invalid_out)
    add("man_version_two", {}, [3], manifest={"version": 2, "checks": [ck("a", "a.xml")]},
        **invalid_out)
    add("man_version_string", {}, [3],
        manifest={"version": "1", "checks": [ck("a", "a.xml")]}, **invalid_out)
    add("man_version_float", {}, [3],
        manifest={"version": 1.0, "checks": [ck("a", "a.xml")]}, **invalid_out)
    add("man_version_bool", {}, [3],
        manifest={"version": True, "checks": [ck("a", "a.xml")]}, **invalid_out)
    add("man_checks_missing", {}, [3], manifest={"version": 1}, **invalid_out)
    add("man_checks_not_array", {}, [3], manifest={"version": 1, "checks": {}},
        **invalid_out)
    add("man_checks_empty", {}, [3], manifest={"version": 1, "checks": []}, **invalid_out)
    add("man_invalid_utf8", {}, [3], manifest=b'\xff\xfe{"version": 1}', **invalid_out)

    # --- sentence 4: per-check validity -----------------------------------
    add("chk_not_object", {}, [4], manifest=mf("x"), expect_exit=2,
        verdict="could-not-evaluate",
        checks=[E(None, "error", "check_invalid")])
    add("chk_missing_member", {}, [4],
        manifest={"version": 1, "checks": [{"id": "a", "file": "a.xml"}]},
        expect_exit=2, verdict="could-not-evaluate",
        checks=[E("a", "error", "check_invalid")])
    add("chk_nonstring_id", {}, [4],
        manifest={"version": 1,
                  "checks": [{"id": 7, "file": "a.xml", "sitemapUrl": "http://example.com/"}]},
        expect_exit=2, verdict="could-not-evaluate",
        checks=[E(None, "error", "check_invalid")])
    add("chk_id_null", {}, [4],
        manifest={"version": 1,
                  "checks": [{"id": None, "file": "a.xml", "sitemapUrl": "http://example.com/"}]},
        expect_exit=2, verdict="could-not-evaluate",
        checks=[E(None, "error", "check_invalid")])
    add("chk_nonstring_file", {}, [4],
        manifest={"version": 1,
                  "checks": [{"id": "a", "file": 7, "sitemapUrl": "http://example.com/"}]},
        expect_exit=2, verdict="could-not-evaluate",
        checks=[E("a", "error", "check_invalid")])
    add("chk_duplicate_id", clean_case_files, [4],
        manifest=mf(ck("a", "a.xml"), ck("a", "a.xml")),
        expect_exit=2, verdict="could-not-evaluate",
        checks=[E("a", "clean"), E("a", "error", "check_invalid")])
    add("chk_absolute_file", clean_case_files, [4],
        manifest=mf(ck("a", "/etc/passwd")), expect_exit=2,
        verdict="could-not-evaluate",
        checks=[E("a", "error", "check_invalid")])
    add("chk_dotdot_file", clean_case_files, [4],
        manifest=mf(ck("a", "sub/../a.xml")), expect_exit=2,
        verdict="could-not-evaluate",
        checks=[E("a", "error", "check_invalid")])
    add("chk_url_relative", clean_case_files, [4],
        manifest=mf(ck("a", "a.xml", "sitemap.xml")), expect_exit=2,
        verdict="could-not-evaluate",
        checks=[E("a", "error", "check_invalid")])
    add("chk_url_ftp", clean_case_files, [4],
        manifest=mf(ck("a", "a.xml", "ftp://example.com/")), expect_exit=2,
        verdict="could-not-evaluate",
        checks=[E("a", "error", "check_invalid")])
    add("chk_url_no_host", clean_case_files, [4],
        manifest=mf(ck("a", "a.xml", "http:///x")), expect_exit=2,
        verdict="could-not-evaluate",
        checks=[E("a", "error", "check_invalid")])
    add("chk_url_scheme_case", clean_case_files, [4, 24],
        manifest=mf(ck("a", "a.xml", "HTTP://Example.COM/")), verdict="clean",
        checks=[E("a", "clean")])

    # --- sentence 5: file resolution --------------------------------------
    add("file_unreadable", {}, [5],
        manifest=mf(ck("a", "missing.xml")), expect_exit=2,
        verdict="could-not-evaluate", checks=[E("a", "error", "file_unreadable")])
    add("file_is_directory", {"d/keep.txt": b"x"}, [5],
        manifest=mf(ck("a", "d")), expect_exit=2,
        verdict="could-not-evaluate", checks=[E("a", "error", "file_unreadable")])
    add("file_relative_to_manifest_dir", {"sub/a.xml": clean_url}, [5],
        manifest=mf(ck("a", "a.xml")), manifest_path="sub/manifest.json",
        argv=["--manifest", "sub/manifest.json"], verdict="clean",
        checks=[E("a", "clean")])

    # --- rules (a): encoding ----------------------------------------------
    add("enc_utf8_bom_allowed", {"a.xml": b"\xef\xbb\xbf" + clean_url}, [6],
        rules=[("a", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("enc_utf8_bytes", {"a.xml": urlset(url(L("http://example.com/\u00fcmlat")))},
        [6], rules=[("a", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("enc_invalid_bytes",
        {"a.xml": b'<urlset xmlns="' + NS.encode() + b'"><url><loc>http://example.com/\xfc</loc></url></urlset>'},
        [6], rules=[("a", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("encoding_invalid", None)])])
    add("enc_decl_latin1",
        {"a.xml": ('<?xml version="1.0" encoding="ISO-8859-1"?>' +
                   urlset(url(L("http://example.com/a")), decl="").decode()).encode()},
        [7], rules=[("a", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("encoding_invalid", None)])])
    add("enc_decl_utf16",
        {"a.xml": ('<?xml version="1.0" encoding="UTF-16"?>' +
                   urlset(url(L("http://example.com/a")), decl="").decode()).encode()},
        [7], rules=[("a", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("encoding_invalid", None)])])
    add("enc_decl_lowercase_utf8",
        {"a.xml": ('<?xml version="1.0" encoding="utf-8"?>' +
                   urlset(url(L("http://example.com/a")), decl="").decode()).encode()},
        [7], rules=[("a", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("enc_decl_mixed_case_utf8",
        {"a.xml": ('<?xml version="1.0" encoding="Utf-8"?>' +
                   urlset(url(L("http://example.com/a")), decl="").decode()).encode()},
        [7], rules=[("a", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("enc_invalid_suppresses_findings",
        {"a.xml": ('<?xml version="1.0" encoding="ISO-8859-1"?>' +
                   urlset(url(L("http://other.com/x")), decl="").decode()).encode()},
        [7], rules=[("a", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("encoding_invalid", None)])])

    # --- rules (b): well-formedness and doctype ---------------------------
    add("wf_valid_minimal", clean_case_files, [8], rules=[("b", "pos")],
        manifest=mf(ck("a", "a.xml")), verdict="clean", checks=[E("a", "clean")])
    add("wf_cdata_loc",
        {"a.xml": urlset(url("<loc><![CDATA[http://example.com/a]]></loc>"))},
        [8], rules=[("b", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("wf_malformed",
        {"a.xml": ('<urlset xmlns="%s"><url><loc>http://example.com/a</loc></urlset>' % NS).encode()},
        [8], rules=[("b", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("xml_malformed", None)])])
    add("wf_malformed_suppresses_findings",
        {"a.xml": ('<urlset xmlns="%s"><url><loc>relative</loc></urlset>' % NS).encode()},
        [8], rules=[("b", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("xml_malformed", None)])])
    add("wf_doctype",
        {"a.xml": ('<?xml version="1.0" encoding="UTF-8"?>'
                   '<!DOCTYPE urlset SYSTEM "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'
                   + urlset(url(L("http://example.com/a")), decl="").decode()).encode()},
        [9], rules=[("b", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("doctype_present", None)])])
    add("wf_doctype_internal_subset",
        {"a.xml": ('<?xml version="1.0" encoding="UTF-8"?>'
                   '<!DOCTYPE urlset [ <!ENTITY x "y"> ]>'
                   + urlset(url(L("http://example.com/a")), decl="").decode()).encode()},
        [9], rules=[("b", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("doctype_present", None)])])
    add("wf_doctype_suppresses_root",
        {"a.xml": ('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE feed>'
                   '<feed xmlns="%s"></feed>' % NS).encode()},
        [9], rules=[("b", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("doctype_present", None)])])

    # --- rules (c): root --------------------------------------------------
    add("root_default_namespace", clean_case_files, [10], rules=[("c", "pos")],
        manifest=mf(ck("a", "a.xml")), verdict="clean", checks=[E("a", "clean")])
    add("root_sitemapindex",
        {"a.xml": index(smap(L("http://example.com/x.xml")))}, [10, 27],
        rules=[("c", "pos"), ("h", "pos")], manifest=mf(ck("a", "a.xml")),
        verdict="clean", checks=[E("a", "clean")])
    add("root_prefixed",
        {"a.xml": ('<s:urlset xmlns:s="%s"><s:url><s:loc>http://example.com/a</s:loc>'
                   '</s:url></s:urlset>' % NS).encode()}, [10, 11],
        rules=[("c", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("root_no_namespace",
        {"a.xml": b"<urlset><url><loc>http://example.com/a</loc></url></urlset>"},
        [10], rules=[("c", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("root_invalid", None)])])
    add("root_wrong_local",
        {"a.xml": doc("feed", url(L("http://example.com/a")))}, [10],
        rules=[("c", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("root_invalid", None)])])
    add("root_wrong_namespace",
        {"a.xml": urlset(url(L("http://example.com/a")), xmlns="http://example.com/")},
        [10], rules=[("c", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("root_invalid", None)])])
    add("root_invalid_suppresses_entries",
        {"a.xml": doc("feed", url(L("relative")))}, [10],
        rules=[("c", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("root_invalid", None)])])

    # --- rules (d): entries -----------------------------------------------
    add("ent_zero_entries", {"a.xml": urlset("")}, [12], rules=[("d", "neg")],
        manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("no_entries", None)])])
    add("ent_unexpected_root_child",
        {"a.xml": urlset("<foo/>" + url(L("http://example.com/a")))}, [13],
        rules=[("d", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("element_unexpected", None)])])
    add("ent_unexpected_root_child_only", {"a.xml": urlset("<foo/>")}, [12, 13],
        rules=[("d", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None,
                  [("no_entries", None), ("element_unexpected", None)])])
    add("ent_numbering_counts_entries_only",
        {"a.xml": urlset("<foo/>" + url(L("relative")))}, [11, 13],
        rules=[("d", "pos")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None,
                  [("element_unexpected", None), ("loc_not_absolute", 1)])])
    add("ent_other_namespace_root_child",
        {"a.xml": urlset('<x:extra xmlns:x="urn:x"/><x:more xmlns:x="urn:x">'
                         'text</x:more>' + url(L("http://example.com/a")))},
        [14], rules=[("d", "pos")], manifest=mf(ck("a", "a.xml")),
        verdict="clean", checks=[E("a", "clean")])
    add("ent_other_namespace_entry_child",
        {"a.xml": urlset(url(L("http://example.com/a"),
                             '<x:data xmlns:x="urn:x">junk</x:data>'))},
        [14], rules=[("d", "pos"), ("e", "pos")], manifest=mf(ck("a", "a.xml")),
        verdict="clean", checks=[E("a", "clean")])
    add("ent_sitemap_in_urlset",
        {"a.xml": urlset(smap(L("http://example.com/x.xml")))}, [11, 13],
        rules=[("d", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None,
                  [("no_entries", None), ("element_unexpected", None)])])
    add("ent_url_in_sitemapindex",
        {"a.xml": index(url(L("http://example.com/a")))}, [11, 13],
        rules=[("d", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None,
                  [("no_entries", None), ("element_unexpected", None)])])
    add("ent_prefixed_entries",
        {"a.xml": ('<s:sitemapindex xmlns:s="%s"><s:sitemap><s:loc>'
                   'http://example.com/x.xml</s:loc></s:sitemap></s:sitemapindex>'
                   % NS).encode()}, [11], rules=[("d", "pos")],
        manifest=mf(ck("a", "a.xml")), verdict="clean", checks=[E("a", "clean")])

    # --- rules (e): entry children ----------------------------------------
    add("ec_each_field_once",
        {"a.xml": urlset(url(L("http://example.com/a"),
                             "<lastmod>2020-01-01</lastmod>",
                             "<changefreq>daily</changefreq>",
                             "<priority>0.5</priority>"))}, [15, 16],
        rules=[("e", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("ec_order_not_checked",
        {"a.xml": urlset(url("<priority>0.5</priority>",
                             "<changefreq>daily</changefreq>",
                             "<lastmod>2020-01-01</lastmod>",
                             L("http://example.com/a")))}, [18],
        rules=[("e", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("ec_loc_missing",
        {"a.xml": urlset(url("<lastmod>2020-01-01</lastmod>"))}, [15],
        rules=[("e", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_missing", 1)])])
    add("ec_loc_missing_still_checks_lastmod",
        {"a.xml": urlset(url("<lastmod>2020-13-01</lastmod>"))}, [15],
        rules=[("e", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None,
                  [("loc_missing", 1), ("lastmod_invalid", 1)])])
    add("ec_loc_repeated",
        {"a.xml": urlset(url(L("http://example.com/a"), L("http://other.com/b")))},
        [15], rules=[("e", "neg"), ("h", "pos")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_repeated", 1)])])
    add("ec_field_repeated_lastmod_urlset",
        {"a.xml": urlset(url(L("http://example.com/a"),
                             "<lastmod>nope</lastmod>",
                             "<lastmod>2020-01-01</lastmod>"))}, [16],
        rules=[("e", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("field_repeated", 1)])])
    add("ec_field_repeated_changefreq",
        {"a.xml": urlset(url(L("http://example.com/a"),
                             "<changefreq>weekly</changefreq>",
                             "<changefreq>bogus</changefreq>"))}, [16],
        rules=[("e", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("field_repeated", 1)])])
    add("ec_field_repeated_lastmod_index",
        {"a.xml": index(smap(L("http://example.com/x.xml"),
                             "<lastmod>2020-01-01</lastmod>",
                             "<lastmod>2021-01-01</lastmod>"))}, [16],
        rules=[("e", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("field_repeated", 1)])])
    add("ec_dup_loc_and_field",
        {"a.xml": urlset(url(L("http://example.com/a"), L("http://example.com/b"),
                             "<lastmod>x</lastmod>", "<lastmod>y</lastmod>"))},
        [15, 16], rules=[("e", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None,
                  [("field_repeated", 1), ("loc_repeated", 1)])])
    add("ec_unknown_entry_child",
        {"a.xml": urlset(url(L("http://example.com/a"), "<foo/>", "<bar/>"))}, [17],
        rules=[("e", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("element_unexpected", 1)])])
    add("ec_changefreq_in_sitemapindex",
        {"a.xml": index(smap(L("http://example.com/x.xml"),
                             "<changefreq>weekly</changefreq>"))}, [17],
        rules=[("e", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("element_unexpected", 1)])])
    add("ec_priority_in_sitemapindex",
        {"a.xml": index(smap(L("http://example.com/x.xml"),
                             "<priority>0.5</priority>"))}, [17],
        rules=[("e", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("element_unexpected", 1)])])

    add("ec_element_unexpected_both_levels",
        {"a.xml": urlset("<foo/>" + url(L("http://example.com/a"), "<bar/>"))},
        [13, 17], rules=[("e", "neg"), ("d", "neg")],
        manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None,
                  [("element_unexpected", None), ("element_unexpected", 1)])])

    # --- rules (f): limits ------------------------------------------------
    add("lim_too_large", {"a.xml": _oversized}, [19], rules=[("f", "pos")],
        manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("too_large", None)])])
    add("lim_normal_size", clean_case_files, [19], rules=[("f", "neg")],
        manifest=mf(ck("a", "a.xml")), verdict="clean", checks=[E("a", "clean")])
    add("lim_too_many_entries", {"a.xml": _write_many(50001)},
        [20], rules=[("f", "pos")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("too_many_entries", None)])])
    add("lim_too_many_with_entry_findings",
        {"a.xml": _write_many(50001, bad_last=True)}, [20],
        rules=[("f", "pos")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None,
                  [("too_many_entries", None), ("loc_not_absolute", 50001)])])
    add("lim_exactly_50000_entries",
        {"a.xml": _write_many(50000)},
        [20], rules=[("f", "neg")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])

    # --- rules (g): loc form ----------------------------------------------
    add("loc_xml_whitespace_stripped",
        {"a.xml": urlset(url("<loc>\n\t http://example.com/a \r\n</loc>"))}, [21],
        rules=[("g", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("loc_nbsp_not_stripped",
        {"a.xml": urlset(url(L("\u00a0http://example.com/a")))}, [21],
        rules=[("g", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_not_absolute", 1)])])
    add("loc_relative_path",
        {"a.xml": urlset(url(L("/a")))}, [22], rules=[("g", "neg")],
        manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_not_absolute", 1)])])
    add("loc_host_without_scheme",
        {"a.xml": urlset(url(L("example.com/a")))}, [22], rules=[("g", "neg")],
        manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_not_absolute", 1)])])
    add("loc_ftp_scheme",
        {"a.xml": urlset(url(L("ftp://example.com/a")))}, [22], rules=[("g", "neg")],
        manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_not_absolute", 1)])])
    add("loc_empty_host",
        {"a.xml": urlset(url(L("http:///a")))}, [22], rules=[("g", "neg")],
        manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_not_absolute", 1)])])
    add("loc_2047_accepted",
        {"a.xml": urlset(url(L("http://example.com/" + "a" * (2047 - len("http://example.com/")))))},
        [23], rules=[("g", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("loc_2048_too_long",
        {"a.xml": urlset(url(L("http://example.com/" + "a" * (2048 - len("http://example.com/")))))},
        [23], rules=[("g", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_too_long", 1)])])
    add("loc_counts_codepoints_not_bytes",
        {"a.xml": urlset(url(L("http://example.com/" + "\u00e9" * 1100)))}, [23],
        rules=[("g", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("loc_too_long_and_out_of_scope",
        {"a.xml": urlset(url(L("http://other.com/" + "a" * (2048 - len("http://other.com/")))))},
        [23, 25], rules=[("g", "neg"), ("h", "neg")],
        manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None,
                  [("loc_too_long", 1), ("loc_out_of_scope", 1)])])
    add("loc_relative_and_too_long",
        {"a.xml": urlset(url(L("x" * 2048)))}, [22, 23], rules=[("g", "neg")],
        manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None,
                  [("loc_not_absolute", 1), ("loc_too_long", 1)])])

    # --- rules (h): scope -------------------------------------------------
    add("scope_path_prefix_ok",
        {"a.xml": urlset(url(L("http://example.com/catalog/x")))},
        [25], rules=[("h", "pos")],
        manifest=mf(ck("a", "a.xml", "http://example.com/catalog/sitemap.xml")),
        verdict="clean", checks=[E("a", "clean")])
    add("scope_host_case_insensitive",
        {"a.xml": urlset(url(L("http://EXAMPLE.com/a")))}, [24],
        rules=[("h", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("scope_scheme_case_insensitive",
        {"a.xml": urlset(url(L("http://example.com/a")))}, [24],
        rules=[("h", "pos")], manifest=mf(ck("a", "a.xml", "HTTP://Example.COM/")),
        verdict="clean", checks=[E("a", "clean")])
    add("scope_explicit_default_port",
        {"a.xml": urlset(url(L("https://example.com:443/a")))}, [24],
        rules=[("h", "pos")], manifest=mf(ck("a", "a.xml", "https://example.com/s.xml")),
        verdict="clean", checks=[E("a", "clean")])
    add("scope_empty_loc_path_is_root",
        {"a.xml": urlset(url(L("http://example.com")))}, [25],
        rules=[("h", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("scope_port_mismatch",
        {"a.xml": urlset(url(L("http://example.com:8080/a")))}, [25],
        rules=[("h", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_out_of_scope", 1)])])
    add("scope_host_mismatch",
        {"a.xml": urlset(url(L("http://other.com/a")))}, [25],
        rules=[("h", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_out_of_scope", 1)])])
    add("scope_scheme_mismatch",
        {"a.xml": urlset(url(L("https://example.com/a")))}, [25],
        rules=[("h", "neg")], manifest=mf(ck("a", "a.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_out_of_scope", 1)])])
    add("scope_path_prefix_rejected",
        {"a.xml": urlset(url(L("http://example.com/catalogue/x")))}, [25],
        rules=[("h", "neg")],
        manifest=mf(ck("a", "a.xml", "http://example.com/catalog/sitemap.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_out_of_scope", 1)])])
    add("scope_path_case_sensitive",
        {"a.xml": urlset(url(L("http://example.com/Catalog/x")))}, [26],
        rules=[("h", "neg")],
        manifest=mf(ck("a", "a.xml", "http://example.com/catalog/sitemap.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_out_of_scope", 1)])])
    add("scope_percent_not_decoded",
        {"a.xml": urlset(url(L("http://example.com/a%2Fb/")))}, [26],
        rules=[("h", "neg")], manifest=mf(ck("a", "a.xml", "http://example.com/a/s.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_out_of_scope", 1)])])
    add("scope_dot_segments_not_removed",
        {"a.xml": urlset(url(L("http://example.com/catalog/../images/x")))}, [26],
        rules=[("h", "pos")],
        manifest=mf(ck("a", "a.xml", "http://example.com/catalog/sitemap.xml")),
        verdict="clean", checks=[E("a", "clean")])
    add("scope_index_path_ignored",
        {"a.xml": index(smap(L("http://example.com/deep/sm.xml")))}, [27],
        rules=[("h", "pos")],
        manifest=mf(ck("a", "a.xml", "http://example.com/idx.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("scope_index_host_mismatch",
        {"a.xml": index(smap(L("http://other.com/sm.xml")))}, [27],
        rules=[("h", "neg")],
        manifest=mf(ck("a", "a.xml", "http://example.com/idx.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_out_of_scope", 1)])])
    add("scope_index_port_mismatch",
        {"a.xml": index(smap(L("http://example.com:8080/sm.xml")))}, [27],
        rules=[("h", "neg")],
        manifest=mf(ck("a", "a.xml", "http://example.com/idx.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_out_of_scope", 1)])])

    # --- rules (i): lastmod -----------------------------------------------
    def lastmod_case(name, value, valid, sentences=(28, 29), root="urlset"):
        if root == "urlset":
            body = urlset(url(L("http://example.com/a"), "<lastmod>%s</lastmod>" % value))
        else:
            body = index(smap(L("http://example.com/x.xml"),
                              "<lastmod>%s</lastmod>" % value))
        if valid:
            add(name, {"a.xml": body}, list(sentences), rules=[("i", "pos")],
                manifest=mf(ck("a", "a.xml")), verdict="clean",
                checks=[E("a", "clean")])
        else:
            add(name, {"a.xml": body}, list(sentences), rules=[("i", "neg")],
                manifest=mf(ck("a", "a.xml")), expect_exit=1,
                verdict="failed-policy",
                checks=[E("a", "findings", None, [("lastmod_invalid", 1)])])

    lastmod_case("lm_complete_date", "2020-01-01", True)
    lastmod_case("lm_minutes_utc", "2020-01-01T10:30Z", True)
    lastmod_case("lm_seconds_offset", "2020-01-01T10:30:45+05:30", True)
    lastmod_case("lm_fraction", "2020-01-01T10:30:45.123Z", True)
    lastmod_case("lm_leap_day", "2020-02-29", True)
    lastmod_case("lm_index_date", "2020-01-01", True, sentences=(28, 29, 30),
                 root="sitemapindex")
    lastmod_case("lm_index_invalid", "2020", False, sentences=(28, 30),
                 root="sitemapindex")
    lastmod_case("lm_nonleap_day", "2021-02-29", False)
    lastmod_case("lm_month_13", "2020-13-01", False)
    lastmod_case("lm_day_32", "2020-01-32", False)
    lastmod_case("lm_hour_24", "2020-01-01T24:00Z", False)
    lastmod_case("lm_minute_60", "2020-01-01T10:60Z", False)
    lastmod_case("lm_second_60", "2020-01-01T10:30:60Z", False)
    lastmod_case("lm_year_only", "2020", False, sentences=(28, 30))
    lastmod_case("lm_year_month", "2020-01", False, sentences=(28, 30))
    lastmod_case("lm_time_without_tzd", "2020-01-01T10:30", False, sentences=(28, 30))
    lastmod_case("lm_tzd_hour_24", "2020-01-01T10:30+24:00", False)
    lastmod_case("lm_lowercase_z", "2020-01-01T10:30z", False)
    lastmod_case("lm_fraction_empty", "2020-01-01T10:30:45.Z", False)
    add("lm_whitespace_stripped",
        {"a.xml": urlset(url(L("http://example.com/a"),
                             "<lastmod>\n 2020-01-01 \n</lastmod>"))}, [21, 28],
        rules=[("i", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])

    # --- rules (j): changefreq --------------------------------------------
    add("cf_all_valid",
        {"a.xml": urlset("".join(
            url(L("http://example.com/p%d" % number),
                "<changefreq>%s</changefreq>" % value)
            for number, value in enumerate(
                ("always", "hourly", "daily", "weekly", "monthly", "yearly", "never"))))},
        [31], rules=[("j", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("cf_whitespace_stripped",
        {"a.xml": urlset(url(L("http://example.com/a"),
                             "<changefreq>\n weekly \n</changefreq>"))}, [21, 31],
        rules=[("j", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("cf_case_sensitive",
        {"a.xml": urlset(url(L("http://example.com/a"),
                             "<changefreq>Monthly</changefreq>"))}, [31],
        rules=[("j", "neg")], manifest=mf(ck("a", "a.xml")), expect_exit=1,
        verdict="failed-policy",
        checks=[E("a", "findings", None, [("changefreq_invalid", 1)])])
    add("cf_unknown_value",
        {"a.xml": urlset(url(L("http://example.com/a"),
                             "<changefreq>often</changefreq>"))}, [31],
        rules=[("j", "neg")], manifest=mf(ck("a", "a.xml")), expect_exit=1,
        verdict="failed-policy",
        checks=[E("a", "findings", None, [("changefreq_invalid", 1)])])

    # --- rules (k): priority ----------------------------------------------
    add("pr_valid_forms",
        {"a.xml": urlset("".join(
            url(L("http://example.com/p%d" % number),
                "<priority>%s</priority>" % value)
            for number, value in enumerate(
                ("0", "1", "0.5", ".5", "+1", "0.000", "1."))))},
        [32], rules=[("k", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])
    add("pr_out_of_range",
        {"a.xml": urlset(url(L("http://example.com/a"), "<priority>1.1</priority>"))},
        [32], rules=[("k", "neg")], manifest=mf(ck("a", "a.xml")), expect_exit=1,
        verdict="failed-policy",
        checks=[E("a", "findings", None, [("priority_invalid", 1)])])
    add("pr_negative",
        {"a.xml": urlset(url(L("http://example.com/a"), "<priority>-0.1</priority>"))},
        [32], rules=[("k", "neg")], manifest=mf(ck("a", "a.xml")), expect_exit=1,
        verdict="failed-policy",
        checks=[E("a", "findings", None, [("priority_invalid", 1)])])
    add("pr_exponent",
        {"a.xml": urlset(url(L("http://example.com/a"), "<priority>1e-1</priority>"))},
        [32], rules=[("k", "neg")], manifest=mf(ck("a", "a.xml")), expect_exit=1,
        verdict="failed-policy",
        checks=[E("a", "findings", None, [("priority_invalid", 1)])])
    add("pr_empty",
        {"a.xml": urlset(url(L("http://example.com/a"), "<priority></priority>"))},
        [32], rules=[("k", "neg")], manifest=mf(ck("a", "a.xml")), expect_exit=1,
        verdict="failed-policy",
        checks=[E("a", "findings", None, [("priority_invalid", 1)])])
    add("pr_comma",
        {"a.xml": urlset(url(L("http://example.com/a"), "<priority>0,5</priority>"))},
        [32], rules=[("k", "neg")], manifest=mf(ck("a", "a.xml")), expect_exit=1,
        verdict="failed-policy",
        checks=[E("a", "findings", None, [("priority_invalid", 1)])])
    add("pr_bare_dot",
        {"a.xml": urlset(url(L("http://example.com/a"), "<priority>.</priority>"))},
        [32], rules=[("k", "neg")], manifest=mf(ck("a", "a.xml")), expect_exit=1,
        verdict="failed-policy",
        checks=[E("a", "findings", None, [("priority_invalid", 1)])])
    add("pr_whitespace_stripped",
        {"a.xml": urlset(url(L("http://example.com/a"),
                             "<priority> 0.5 </priority>"))}, [21, 32],
        rules=[("k", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean",
        checks=[E("a", "clean")])

    # --- sentences 33-34: output shape and verdict -------------------------
    add("out_clean_item_shape", clean_case_files, [33], manifest=mf(ck("a", "a.xml")),
        verdict="clean", checks=[E("a", "clean")])
    add("out_findings_item_shape", {"a.xml": urlset(url())}, [33],
        manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_missing", 1)])])
    add("out_error_item_shape", {}, [33, 34],
        manifest=mf(ck("a", "missing.xml")), expect_exit=2,
        verdict="could-not-evaluate", checks=[E("a", "error", "file_unreadable")])
    add("out_mixed_error_wins",
        {"a.xml": clean_url}, [34],
        manifest=mf(ck("clean", "a.xml"), ck("gone", "missing.xml")),
        expect_exit=2, verdict="could-not-evaluate",
        checks=[E("clean", "clean"), E("gone", "error", "file_unreadable")])
    add("out_manifest_order_preserved",
        {"a.xml": clean_url, "b.xml": urlset(url()), "c.xml": clean_url}, [33],
        manifest=mf(ck("z", "a.xml"), ck("y", "b.xml"), ck("x", "c.xml")),
        expect_exit=1, verdict="failed-policy",
        checks=[E("z", "clean"), E("y", "findings", None, [("loc_missing", 1)]),
                E("x", "clean")])
    add("out_all_clean_exit_zero", clean_case_files, [34],
        manifest=mf(ck("a", "a.xml")), verdict="clean", expect_exit=0,
        checks=[E("a", "clean")])
    add("out_multiple_findings_exit_one", {"a.xml": urlset(url())}, [34],
        manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("loc_missing", 1)])])
    add("out_all_statuses",
        {"a.xml": clean_url, "b.xml": urlset(url())}, [33, 34],
        manifest=mf(ck("first", "a.xml"), ck("second", "b.xml"),
                    ck("third", "missing.xml")),
        expect_exit=2, verdict="could-not-evaluate",
        checks=[E("first", "clean"),
                E("second", "findings", None, [("loc_missing", 1)]),
                E("third", "error", "file_unreadable")])
    add("out_findings_deduplicated",
        {"a.xml": urlset(url(L("http://example.com/a"), "<foo/>", "<bar/>"))}, [33],
        manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("element_unexpected", 1)])])


    # --- round 40: repairs E, U, R (spot-check routed defect 2) and the D1 reading ----------
    # E: UTF-16 without a BOM decodes as UTF-8 but carries U+0000, not an XML Char (S110).
    u8_text = clean_url.decode("utf-8")
    nodecl = urlset(url(L("http://example.com/a")), decl="").decode("utf-8")
    for tag, data in (("le", u8_text.encode("utf-16-le")), ("be", u8_text.encode("utf-16-be")),
                      ("le_nodecl", nodecl.encode("utf-16-le")), ("be_nodecl", nodecl.encode("utf-16-be"))):
        add("r40_e_utf16_%s_without_bom" % tag, {"a.xml": data}, [6, 8], [("b", "neg")],
            manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
            checks=[E("a", "findings", None, [("xml_malformed", None)])])
    add("r40_e_utf16_with_bom_unchanged", {"a.xml": b"\xff\xfe" + u8_text.encode("utf-16-le")}, [6],
        [("a", "neg")], manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("encoding_invalid", None)])])
    # U: values urlsplit would alter are judged as written (S111).
    for tag, loc in (("tab", "http://example.com/a\tb"), ("lf", "http://example.com/a\nb"),
                     ("cr_ref", "http://example.com/a&#13;b"), ("host_tab", "http://exa\tmple.com/a")):
        add("r40_u_loc_%s" % tag, {"a.xml": urlset(url(L(loc)))}, [21, 22], [("g", "neg")],
            manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
            checks=[E("a", "findings", None, [("loc_not_absolute", 1)])])
    add("r40_u_loc_strip_set_still_clean", {"a.xml": urlset(url(L("\thttp://example.com/a\r\n")))},
        [21, 22], [("g", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean", checks=[E("a", "clean")])
    for tag, su in (("tab", "http://example.com/\tsitemap.xml"), ("cr", "http://example.com/site\rmap.xml"),
                    ("leading_space", " http://example.com/"), ("leading_c0", "\x01http://example.com/")):
        add("r40_u_sitemapurl_%s" % tag, clean_case_files, [4],
            manifest=mf(ck("a", "a.xml", su)), expect_exit=2, verdict="could-not-evaluate",
            checks=[E("a", "error", "check_invalid")])
    # R: a repeat of an earlier invalid check's string id (sentence 4).
    add("r40_r_repeat_of_invalid_check", clean_case_files, [4],
        manifest={"version": 1, "checks": [{"id": "a", "sitemapUrl": "http://example.com/"},
                                           ck("a", "a.xml")]},
        expect_exit=2, verdict="could-not-evaluate",
        checks=[E("a", "error", "check_invalid"), E("a", "error", "check_invalid")])
    add("r40_r_integer_id_then_string_clean", clean_case_files, [4],
        manifest={"version": 1, "checks": [{"id": 7, "file": "a.xml", "sitemapUrl": "http://example.com/"},
                                           ck("7", "a.xml")]},
        expect_exit=2, verdict="could-not-evaluate",
        checks=[E(None, "error", "check_invalid"), E("7", "clean")])
    # D1 is not a deviation: an XML 1.0 processor reads a 1.x declaration as 1.0 (S110 §2.8).
    add("r40_d1_version_1_1_clean",
        {"a.xml": urlset(url(L("http://example.com/a")), decl='<?xml version="1.1" encoding="UTF-8"?>\n')},
        [8], [("b", "pos")], manifest=mf(ck("a", "a.xml")), verdict="clean", checks=[E("a", "clean")])
    # Sub-shapes the round-40 wave-1 controls showed the 30 witnesses did not sample.
    for tag, su in (("lf", "http://example.com/site\nmap.xml"), ("leading_nul", "\x00http://example.com/"),
                    ("leading_unit_separator", "\x1fhttp://example.com/"), ("query_tab", "http://example.com/?a\tb"),
                    ("fragment_lf", "http://example.com/#a\nb")):
        add("r40_u_sitemapurl_more_%s" % tag, clean_case_files, [4],
            manifest=mf(ck("a", "a.xml", su)), expect_exit=2, verdict="could-not-evaluate",
            checks=[E("a", "error", "check_invalid")])
    for tag, loc in (("query_tab", "http://example.com/a?x\ty"), ("fragment_lf", "http://example.com/a#x\ny"),
                     ("https_tab", "https://example.com/a\tb")):
        add("r40_u_loc_more_%s" % tag, {"a.xml": urlset(url(L(loc)))}, [21, 22], [("g", "neg")],
            manifest=mf(ck("a", "a.xml", "https://example.com/" if tag == "https_tab" else "http://example.com/")),
            expect_exit=1, verdict="failed-policy",
            checks=[E("a", "findings", None, [("loc_not_absolute", 1)])])
    index_text = index(smap(L("http://example.com/s.xml"))).decode("utf-8")
    add("r40_e_utf16_index_without_bom", {"a.xml": index_text.encode("utf-16-le")}, [6, 8], [("b", "neg")],
        manifest=mf(ck("a", "a.xml")), expect_exit=1, verdict="failed-policy",
        checks=[E("a", "findings", None, [("xml_malformed", None)])])
    for tag, first in (("absolute_file", {"id": "a", "file": "/a.xml", "sitemapUrl": "http://example.com/"}),
                       ("bad_url", {"id": "a", "file": "a.xml", "sitemapUrl": "ftp://example.com/"}),
                       ("upper_id", {"id": "A", "sitemapUrl": "http://example.com/"})):
        rid = first["id"]
        add("r40_r_repeat_after_%s" % tag, clean_case_files, [4],
            manifest={"version": 1, "checks": [first, ck(rid, "a.xml")]},
            expect_exit=2, verdict="could-not-evaluate",
            checks=[E(rid, "error", "check_invalid"), E(rid, "error", "check_invalid")])

    return cases


# --------------------------------------------------------------------------
# Fault-injection tools (generated, never imported)
# --------------------------------------------------------------------------

SILENT_TOOL = """#!/usr/bin/env python3
import sys
sys.exit(0)
"""

CONSTANT_CLEAN_TOOL = """#!/usr/bin/env python3
import json
import sys


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return 64
    try:
        with open(argv[2], "r", encoding="utf-8") as handle:
            document = json.load(handle)
    except Exception:
        document = None
    if not isinstance(document, dict) or document.get("version") != 1:
        sys.stdout.write(json.dumps({"version": 1, "verdict": "could-not-evaluate",
                                     "error": "input_invalid", "checks": []}) + "\\n")
        return 2
    checks = document.get("checks")
    if not isinstance(checks, list) or not checks:
        sys.stdout.write(json.dumps({"version": 1, "verdict": "could-not-evaluate",
                                     "error": "input_invalid", "checks": []}) + "\\n")
        return 2
    items = []
    for raw in checks:
        ident = raw.get("id") if isinstance(raw, dict) else None
        items.append({"id": ident if isinstance(ident, str) else None,
                      "status": "clean", "error": None, "findings": []})
    sys.stdout.write(json.dumps({"version": 1, "verdict": "clean",
                                 "checks": items}) + "\\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
"""


# --------------------------------------------------------------------------
# Runner
# --------------------------------------------------------------------------

def materialize(root, case):
    directory = os.path.join(root, case["name"])
    os.makedirs(directory, exist_ok=True)
    for relative, content in case["files"].items():
        path = os.path.join(directory, relative)
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        if callable(content):
            content(path)
        else:
            with open(path, "wb") as handle:
                handle.write(content)
    manifest = case["manifest"]
    if manifest is not None:
        if isinstance(manifest, bytes):
            payload = manifest
        else:
            payload = json.dumps(manifest).encode("utf-8")
        path = os.path.join(directory, case["manifest_path"])
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(payload)
    return directory


def run_tool(tool, argv, cwd):
    command = [sys.executable, "-B", tool] + list(argv)
    return subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=300)


def _ordered(findings):
    return sorted(findings, key=lambda item: (-1 if item[1] is None else item[1], item[0]))


def check_case(case, completed):
    problems = []
    if completed.returncode != case["expect_exit"]:
        problems.append("exit %d != %d" % (completed.returncode, case["expect_exit"]))
    if completed.stderr:
        problems.append("stderr not empty: %r" % completed.stderr[:160])
    if case["usage"]:
        return problems
    try:
        document = json.loads(completed.stdout.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        problems.append("stdout is not one JSON document: %s" % (exc,))
        return problems
    if not isinstance(document, dict):
        problems.append("stdout JSON is not an object")
        return problems

    expected_error = case["error"]
    expected_keys = ({"version", "verdict", "checks"} if expected_error is None
                     else {"version", "verdict", "error", "checks"})
    if set(document) != expected_keys:
        problems.append("top-level keys %s != %s"
                        % (sorted(document), sorted(expected_keys)))
    if document.get("version") != 1:
        problems.append("version %r != 1" % (document.get("version"),))
    if case["verdict"] is not None and document.get("verdict") != case["verdict"]:
        problems.append("verdict %r != %r" % (document.get("verdict"), case["verdict"]))
    if expected_error is not None and document.get("error") != expected_error:
        problems.append("error %r != %r" % (document.get("error"), expected_error))

    expected_checks = case["checks"] or []
    got_checks = document.get("checks")
    if not isinstance(got_checks, list):
        problems.append("checks is not an array")
        return problems
    if len(got_checks) != len(expected_checks):
        problems.append("check count %d != %d" % (len(got_checks), len(expected_checks)))
        return problems
    for position, (item, expected) in enumerate(zip(got_checks, expected_checks), 1):
        if not isinstance(item, dict):
            problems.append("check %d is not an object" % position)
            continue
        if set(item) != {"id", "status", "error", "findings"}:
            problems.append("check %d keys %s" % (position, sorted(item)))
        expected_id, expected_status, expected_item_error, expected_findings = expected
        if item.get("id") != expected_id:
            problems.append("check %d id %r != %r"
                            % (position, item.get("id"), expected_id))
        if item.get("status") != expected_status:
            problems.append("check %d status %r != %r"
                            % (position, item.get("status"), expected_status))
        if item.get("error") != expected_item_error:
            problems.append("check %d error %r != %r"
                            % (position, item.get("error"), expected_item_error))
        raw_findings = item.get("findings")
        if not isinstance(raw_findings, list):
            problems.append("check %d findings is not an array" % position)
            continue
        got = set()
        for finding in raw_findings:
            if not isinstance(finding, dict) or set(finding) != {"code", "entry"}:
                problems.append("check %d finding has wrong shape: %r"
                                % (position, finding))
                continue
            got.add((finding["code"], finding["entry"]))
        if got != expected_findings:
            problems.append("check %d findings %s != %s"
                            % (position, _ordered(got), _ordered(expected_findings)))
    return problems


def run_suite(tool, cases, keep_root=None):
    failures = []
    passed = 0
    for case in cases:
        root = keep_root or tempfile.mkdtemp(prefix="sitemap-audit-case-")
        try:
            directory = materialize(root, case)
            argv = case["argv"]
            if argv is None:
                argv = ["--manifest", case["manifest_path"]]
            completed = run_tool(tool, argv, directory)
            problems = check_case(case, completed)
        finally:
            if keep_root is None:
                shutil.rmtree(root, ignore_errors=True)
        if problems:
            failures.append((case["name"], problems))
        else:
            passed += 1
    return passed, failures


def coverage(cases):
    seen_sentences = set()
    polarity = {letter: {"pos": set(), "neg": set()} for letter in RULES}
    for case in cases:
        seen_sentences.update(case["sentences"])
        for letter, sign in case["rules"]:
            polarity[letter][sign].add(case["name"])
    missing = [number for number in SENTENCES if number not in seen_sentences]
    gaps = []
    for letter in RULES:
        for sign in ("pos", "neg"):
            if not polarity[letter][sign]:
                gaps.append("%s:%s" % (letter, sign))
    return missing, gaps, seen_sentences, polarity


def print_map(cases):
    missing, gaps, seen_sentences, polarity = coverage(cases)
    print("case count: %d" % len(cases))
    print("sentence coverage: %d/%d" % (len(seen_sentences), len(SENTENCES)))
    for number in SENTENCES:
        names = sorted(case["name"] for case in cases if number in case["sentences"])
        print("sentence %2d: %s" % (number, ", ".join(names)))
    for letter in RULES:
        positive = sorted(polarity[letter]["pos"])
        negative = sorted(polarity[letter]["neg"])
        print("rule (%s): pos=%s | neg=%s"
              % (letter, ", ".join(positive) or "-", ", ".join(negative) or "-"))
    return 0 if not missing and not gaps else 1


def main(argv):
    tool = None
    fault_injection = False
    show_map = False
    index = 1
    while index < len(argv):
        argument = argv[index]
        if argument == "--tool" and index + 1 < len(argv) and tool is None:
            tool = argv[index + 1]
            index += 2
        elif argument == "--fault-injection":
            fault_injection = True
            index += 1
        elif argument == "--map":
            show_map = True
            index += 1
        else:
            sys.stderr.write("usage: sitemap_audit_selftest.py --tool <path> "
                             "[--fault-injection] | --map\n")
            return 64

    cases = build_cases()
    missing, gaps, _seen, _polarity = coverage(cases)
    if show_map:
        return print_map(cases)
    if tool is None:
        sys.stderr.write("usage: sitemap_audit_selftest.py --tool <path>\n")
        return 64
    tool = os.path.abspath(tool)
    if not os.path.isfile(tool):
        sys.stderr.write("tool not found: %s\n" % tool)
        return 64

    failed = False
    if missing:
        print("COVERAGE FAIL: sentences without a fixture: %s" % missing)
        failed = True
    if gaps:
        print("COVERAGE FAIL: rule polarities without a fixture: %s" % gaps)
        failed = True

    total = len(cases)
    passed, failures = run_suite(tool, cases)
    for name, problems in failures:
        print("FAIL %s" % name)
        for problem in problems:
            print("     %s" % problem)
    print("PASS %d/%d" % (passed, total))
    if failures or missing or gaps:
        failed = True

    if fault_injection:
        with tempfile.TemporaryDirectory(prefix="sitemap-audit-faults-") as scratch:
            for label, source in (("silent", SILENT_TOOL),
                                  ("constant-clean", CONSTANT_CLEAN_TOOL)):
                path = os.path.join(scratch, label.replace("-", "_") + ".py")
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(source)
                fault_passed, _fault_failures = run_suite(path, cases)
                rejected = fault_passed < total
                print("FAULT %s: %s (%d/%d cases accepted)"
                      % (label, "rejected as expected" if rejected else "NOT REJECTED",
                         fault_passed, total))
                if not rejected:
                    failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
