#!/usr/bin/env python3
"""make_cases.py -- emit the frozen C3 case corpus (kake round 78).

Round-78 C3 as amended by contract-amendment-1.md (A1..A5),
contract-amendment-2.md (B1..B6) and contract-amendment-3.md (C1..C6).
Directory shape (C5): <out>/<id>/ with

    page.html      the local page the audit reads (absent only for g34)
    manifest.json  kake-meta-robots-manifest/v1, NO `expect` (B1)
    expect.json    C4's row: {exit, effective, findings} or {exit, error}

The effective/finding table below is amendment 3 C4 verbatim; expectation()
applies amendment 4's finding-case exits. Count: 36 (amendment 3 C1).

Usage:
    python3 make_cases.py --out /abs/path/.ufo/waves/round-78/cases
"""

import argparse
import json
import os
import shutil
import sys

PAGE = ("<!doctype html>\n<html>\n<head>\n<meta charset=\"utf-8\">\n"
        "<title>%s</title>\n%s</head>\n<body>\n<p>case page</p>\n%s"
        "</body>\n</html>\n")


def meta(content, name="robots"):
    return '<meta name="%s" content="%s">\n' % (name, content)


DEFAULT = ["follow", "index"]

CASES = [
    dict(id="g01_absent_tag", agents=["robots"], head="", body="",
         effective=DEFAULT, findings=[], exit=0,
         derivation="C4 row g01; C2.6 default: no matching element."),
    dict(id="g02_noindex", agents=["robots"], head=meta("noindex"),
         effective=["noindex"], findings=[], exit=0,
         derivation="C4 row g02; C2.2 collapse over declared values only."),
    dict(id="g03_none_expansion", agents=["robots"], head=meta("none"),
         effective=["nofollow", "noindex"], findings=[], exit=0,
         derivation="C4 row g03; C2.2 'none expands to noindex + nofollow'."),
    dict(id="g04_all_default", agents=["robots"], head=meta("all"),
         effective=["follow", "index"], findings=[], exit=0,
         derivation="C4 row g04; C2.2 'all expands to index + follow'."),
    dict(id="g05_index_follow_one", agents=["robots"],
         head=meta("index, follow"), effective=["follow", "index"],
         findings=[], exit=0,
         derivation="C4 row g05; comma split + whitespace trim."),
    dict(id="g06_conflicting_noindex", agents=["robots"],
         head=meta("index") + meta("noindex"), effective=["noindex"],
         findings=[], exit=0,
         derivation="C4 row g06; C2.2 noindex beats index."),
    dict(id="g07_conflicting_nofollow", agents=["robots"],
         head=meta("follow") + meta("nofollow"), effective=["nofollow"],
         findings=[], exit=0,
         derivation="C4 row g07; C2.2 nofollow beats follow."),
    dict(id="g08_max_snippet_two", agents=["robots"],
         head=meta("max-snippet:50") + meta("max-snippet:20"),
         effective=["max-snippet:20"], findings=[], exit=0,
         derivation="C4 row g08; C2.4 smallest non-negative integer."),
    dict(id="g09_max_image_preview_two", agents=["robots"],
         head=meta("max-image-preview:large")
         + meta("max-image-preview:standard"),
         effective=["max-image-preview:standard"], findings=[], exit=0,
         derivation="C4 row g09; C2.4 order none < standard < large."),
    dict(id="g10_max_video_no_limit", agents=["robots"],
         head=meta("max-video-preview:-1") + meta("max-video-preview:30"),
         effective=["max-video-preview:30"], findings=[], exit=0,
         derivation="C4 row g10; C2.4 -1 loses to a non-negative value."),
    dict(id="g11_max_snippet_invalid", agents=["robots"],
         head=meta("max-snippet:abc"), effective=DEFAULT,
         findings=["meta_robots_invalid_value"], exit=0,
         derivation="C4 row g11; C2.6 default when only invalid tokens; "
                    "A4 invalid value is ignored for effect."),
    dict(id="g12a_unavailable_datetime", agents=["robots"],
         head=meta("unavailable_after: 2020-09-21T15:00:00Z"),
         effective=["unavailable_after:2020-09-21T15:00:00Z"], findings=[],
         exit=0,
         derivation="C4 row g12a; C2.7 input trimmed as written, RFC 3339 "
                    "date-time (A2 form i)."),
    dict(id="g12b_unavailable_date", agents=["robots"],
         head=meta("unavailable_after: 2020-09-21"),
         effective=["unavailable_after:2020-09-21"], findings=[], exit=0,
         derivation="C4 row g12b; C2.7; A2 form i full-date, the source's "
                    "own example."),
    dict(id="g12c_unavailable_rfc822", agents=["robots"],
         head=meta("unavailable_after: 25 Jun 2010 15:00:00 PST"),
         effective=["unavailable_after:25 Jun 2010 15:00:00 PST"],
         findings=[], exit=0,
         derivation="C4 row g12c; C2.7; A2 form ii RFC 822-style, B6 zone "
                    "list."),
    dict(id="g13_unavailable_invalid", agents=["robots"],
         head=meta("unavailable_after: 2020-13-40"), effective=DEFAULT,
         findings=["meta_robots_invalid_value"], exit=0,
         derivation="C4 row g13; A2 invalid date ignored for effect; C2.6 "
                    "default."),
    dict(id="g14_uppercase", agents=["robots"],
         head='<META NAME="ROBOTS" CONTENT="NOINDEX">\n',
         effective=["noindex"], findings=[], exit=0,
         derivation="C4 row g14; name and tokens are ASCII-case-insensitive; "
                    "effective vocabulary is lower case."),
    dict(id="g15_empty_content", agents=["robots"], head=meta(""),
         effective=DEFAULT, findings=["meta_robots_empty_content"], exit=0,
         derivation="C4 row g15; C2.6/I empty content, default effective."),
    dict(id="g16_unknown_directive", agents=["robots"], head=meta("nosuchthing"),
         effective=DEFAULT,
         findings=["meta_robots_unknown_directive"], exit=0,
         derivation="C4 row g16; C2.6/A4 unknown token ignored, default."),
    dict(id="g17_googlebot_ignored", agents=["robots"],
         head=meta("noindex", name="googlebot"), effective=DEFAULT,
         findings=[], exit=0,
         derivation="C4 row g17; name googlebot is not in agents, so no "
                    "matching element and no finding."),
    dict(id="g18_googlebot_with_agents", agents=["robots", "googlebot"],
         head=meta("noindex", name="googlebot"), effective=["noindex"],
         findings=[], exit=0,
         derivation="C4 row g18; googlebot is a configured agent, so the "
                    "element matches."),
    dict(id="g19_body_tag_respected", agents=["robots"], head="",
         body=meta("noindex"), effective=["noindex"],
         findings=["meta_robots_tag_outside_head"], exit=0,
         derivation="C4 row g19; A1 body tags join the effective set and are "
                    "reported as lane hygiene."),
    dict(id="g21_self_closing", agents=["robots"],
         head='<meta name="robots" content="noindex" />\n',
         effective=["noindex"], findings=[], exit=0,
         derivation="C4 row g21; self-closing meta parses normally."),
    dict(id="g22_single_quotes", agents=["robots"],
         head="<meta name='robots' content='noindex'>\n",
         effective=["noindex"], findings=[], exit=0,
         derivation="C4 row g22; attribute parsing, not text matching."),
    dict(id="g23_noarchive_ignored", agents=["robots"],
         head=meta("noarchive") + meta("nosnippet"),
         effective=["nosnippet"], findings=["meta_robots_ignored_rule"],
         exit=0,
         derivation="C4 row g23; A3 noarchive is an ignored rule, nosnippet "
                    "is effective."),
    dict(id="g24_trailing_comma", agents=["robots"], head=meta("noindex,"),
         effective=["noindex"], findings=[], exit=0,
         derivation="C4 row g24; empty tokens are ignored (not all-empty)."),
    dict(id="g25_nosnippet_dominates", agents=["robots"],
         head=meta("nosnippet") + meta("max-snippet:50"),
         effective=["nosnippet"], findings=[], exit=0,
         derivation="C4 row g25; A5 explicit nosnippet drops numeric "
                    "max-snippet."),
    dict(id="g26_max_snippet_zero_video_minus_one", agents=["robots"],
         head=meta("max-snippet:0, max-video-preview:-1"),
         effective=["max-video-preview:-1", "nosnippet"], findings=[], exit=0,
         derivation="C4 row g26; A5 max-snippet:0 renders nosnippet and "
                    "drops the max-snippet numeric, but max-video-preview:-1 "
                    "is the only declared value of its family and survives "
                    "(C2.4)."),
    dict(id="g27_indexifembedded", agents=["robots"],
         head=meta("noindex, indexifembedded"),
         effective=["indexifembedded", "noindex"], findings=[], exit=0,
         derivation="C4 row g27; indexifembedded is non-collapsing, noindex "
                    "still wins its own pair."),
    dict(id="g28_within_content_conflict", agents=["robots"],
         head=meta("index, noindex"), effective=["noindex"], findings=[],
         exit=0,
         derivation="C4 row g28; C2.2 collapse applies inside one content."),
    dict(id="g29_max_image_preview_none", agents=["robots"],
         head=meta("max-image-preview:none"),
         effective=["max-image-preview:none"], findings=[], exit=0,
         derivation="C4 row g29; C2.4 none is a valid setting and wins the "
                    "order."),
    dict(id="g30_max_snippet_minus_one", agents=["robots"],
         head=meta("max-snippet:-1"), effective=["max-snippet:-1"],
         findings=[], exit=0,
         derivation="C4 row g30; C2.4 -1 is emitted when it is the only "
                    "declared value of its family."),
    dict(id="g31_missing_content", agents=["robots"],
         head='<meta name="robots">\n', effective=DEFAULT,
         findings=["meta_robots_empty_content"], exit=0,
         derivation="C4 row g31; B6 missing content is equivalent to empty "
                    "content, default effective."),
    dict(id="g32_nocache_ignored", agents=["robots"], head=meta("nocache"),
         effective=DEFAULT, findings=["meta_robots_ignored_rule"], exit=0,
         derivation="C4 row g32; A3 nocache is an ignored rule; C2.6 default."),
    dict(id="g33_lowercase_t_z", agents=["robots"],
         head=meta("unavailable_after: 2020-09-21t15:00:00z"),
         effective=["unavailable_after:2020-09-21t15:00:00z"], findings=[],
         exit=0,
         derivation="C4 row g33; B6 RFC 3339 lowercase t and z are accepted, "
                    "rendered as written."),
    dict(id="g34_missing_file_exit2", agents=["robots"], exists=False,
         head=None, effective=None, findings=None, exit=2,
         error="missing_file",
         derivation="C4 row g34; C3/C5 the check names page.html in a dir "
                    "where that file does not exist -> fault."),
    dict(id="g35_duplicate_id_exit2", agents=["robots"], duplicate=True,
         head=meta("noindex"), effective=None, findings=None, exit=2,
         error="duplicate_check_id",
         derivation="C4 row g35; C3/C5 two checks share one id -> fault."),
]


def page(case):
    return PAGE % (case["id"], case.get("head") or "",
                   case.get("body") or "")


def manifest(case):
    check = {"id": case["id"], "path": "page.html",
             "url": "https://example.kake.test/%s" % case["id"]}
    checks = [check]
    if case.get("duplicate"):
        checks.append(dict(check))
    return {"schema": "kake-meta-robots-manifest/v1",
            "agents": list(case["agents"]), "checks": checks}


def expectation(case):
    if case["exit"] == 2:
        return {"exit": 2, "error": case["error"]}
    return {"exit": 1 if case["findings"] else 0,
            "effective": sorted(case["effective"]),
            "findings": sorted(case["findings"])}


def main(argv):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--out", required=True)
    opts = parser.parse_args(argv)
    out = os.path.abspath(opts.out)
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    seen = set()
    for case in CASES:
        if case["id"] in seen:
            raise SystemExit("duplicate case id %s" % case["id"])
        seen.add(case["id"])
        target = os.path.join(out, case["id"])
        os.makedirs(target)
        if case.get("exists", True):
            with open(os.path.join(target, "page.html"), "w",
                      encoding="utf-8") as handle:
                handle.write(page(case))
        with open(os.path.join(target, "manifest.json"), "w",
                  encoding="utf-8") as handle:
            json.dump(manifest(case), handle, indent=1, sort_keys=True)
            handle.write("\n")
        expect = expectation(case)
        with open(os.path.join(target, "expect.json"), "w",
                  encoding="utf-8") as handle:
            json.dump(expect, handle, indent=1, sort_keys=True)
            handle.write("\n")
        print("%s\texit=%d\teffective=%s\tfindings=%s"
              % (case["id"], expect["exit"],
                 ",".join(expect.get("effective", [])) or "-",
                 ",".join(expect.get("findings", [])) or "-"))
    print("cases=%d out=%s" % (len(CASES), out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
