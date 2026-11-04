#!/usr/bin/env python3
"""ReviewerC2-7 attack driver, v2: 47 fixtures against the PINNED delivered tool,
expectations re-derived from contract C2 + amendments 1-2 (A1-A16).

Usage: driver_reviewerc2.py <tool-path> <tag>
Writes ONLY under .../round-76/w1/ReviewerC2/ (fixtures/, receipts/).
"""
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-76/w1/ReviewerC2"
S = "/fast/scratch/hyaku/kake-r76/ReviewerC2-7"
TOOL = sys.argv[1] if len(sys.argv) > 1 else S + "/pinned/hreflang_audit.py"
TAG = sys.argv[2] if len(sys.argv) > 2 else "pinned"
FIX = LANE + "/fixtures"
REC = LANE + "/receipts"

INV = "hreflang_invalid_tag"
DUP = "hreflang_duplicate_pair"
MXD = "hreflang_multiple_xdefault"
REL = "hreflang_relative_href"
SELF = "hreflang_self_missing"
NON = "hreflang_nonreciprocal"
CAN = "hreflang_canonical_not_self"
MIS = "hreflang_missing_value"
IU = "input_unreadable"
DU = "input_duplicate_url"
NA = "input_url_not_absolute"


def alt(tag, href, quoted=True):
    if quoted:
        return '<link rel="alternate" hreflang="%s" href="%s">' % (tag, href)
    return '<link rel=alternate hreflang=%s href=%s>' % (tag, href)


def canon(href):
    return '<link rel="canonical" href="%s">' % href


A_URL = "https://example.com/en"
B_URL = "https://example.com/fr"
C_URL = "https://example.com/de"

CASES = []


def case(cid, pages, exp_exit, exp_ids, ambiguous=None, version=1, extra_files=None,
         undecidable=False):
    CASES.append(dict(id=cid, pages=pages, exp_exit=exp_exit, exp_ids=sorted(exp_ids),
                      ambiguous=ambiguous, version=version, extra_files=extra_files or {},
                      undecidable=undecidable))


def page(pid, url, html, fname=None, omit=False):
    return dict(id=pid, url=url, html=html, file=fname or (pid + ".html"), omit=omit)


# --- tag grammar (contract grammar; derivable) -----------------------------
case("T01", [page("en", A_URL, alt("en-GB-oed", "https://example.com/en-GB-oed") + alt("en", A_URL) + canon(A_URL))],
     1, [INV], "grammar-limit: oed is a registered (deprecated) IANA variant; frozen grammar rejects 3-char variants")
case("T02", [page("en", A_URL, alt("zh-yue-HK", "https://example.com/yue") + alt("en", A_URL) + canon(A_URL))],
     1, [INV], "grammar-limit: zh-yue alone is a grandfathered BCP-47 tag; frozen grammar rejects")
case("T03", [page("en", A_URL, alt("sgn-BE-FR", "https://example.com/sf") + alt("en", A_URL) + canon(A_URL))],
     1, [INV], "grammar-limit: trailing FR is 2 chars; RFC 5646 variant grammar also rejects")
case("T04", [page("en", A_URL, alt("en-u-ca-gregory", "https://example.com/en-greg") + alt("en", A_URL) + canon(A_URL))],
     1, [INV], "grammar-limit: extension singleton u rejected by frozen grammar though valid BCP-47; verdict derivable")
case("T05", [page("en", A_URL, alt("X-DEFAULT", A_URL) + canon(A_URL))],
     0, [], "decided by A11: x-default compared ASCII case-insensitively")
case("T06", [page("en", A_URL, alt("X-DEFAULT", A_URL) + alt("X-DEFAULT", A_URL) + canon(A_URL))],
     1, [DUP, MXD, MXD], "A11 + A2 per-annotation: duplicate_pair once + multiple_xdefault per element")
case("T07", [page("en", A_URL, alt("en--GB", "https://example.com/double") + alt("en", A_URL) + canon(A_URL))],
     1, [INV], None)
case("T08", [page("en", A_URL, alt("en-", "https://example.com/dash") + alt("en", A_URL) + canon(A_URL))],
     1, [INV], None)
case("T09", [page("en", A_URL, alt(" en ", A_URL) + alt("en", A_URL) + canon(A_URL))],
     1, [INV], "REMAINING-UNDECIDED class (named): whitespace normalization of the hreflang value before the grammar check; literal anchored-grammar reading = invalid_tag, tool strips = clean (and then sees duplicate_pair)",
     undecidable=True)
case("T11", [page("en", A_URL, alt("en_GB", "https://example.com/under") + alt("en", A_URL) + canon(A_URL))],
     1, [INV], "contract-explicit: underscore never accepted")
case("T12", [page("en", A_URL, alt("EN-GB", A_URL) + alt("en-gb", A_URL) + canon(A_URL))],
     1, [DUP], "A3: tag equality ASCII case-insensitive")
case("T13", [page("en", A_URL, alt("es-419", A_URL) + alt("en", A_URL) + canon(A_URL))],
     0, [], "positive control: 3-digit region accepted")

# --- href ------------------------------------------------------------------
case("H01", [
    page("en", "https://example.com/en?p=1",
         canon("https://example.com/en?p=1") + alt("en", "https://example.com/en?p=1")
         + alt("fr", "https://example.com/fr?p=1&amp;x=2")),
    page("fr", "https://example.com/fr?p=1&x=2",
         canon("https://example.com/fr?p=1&x=2") + alt("fr", "https://example.com/en?p=1")
         + alt("de", "https://example.com/fr?p=1&x=2")),
    ], 0, [], "A13: entities decoded before comparison; a non-decoder flags nonreciprocal here")

case("H02", [
    page("en", A_URL, canon(A_URL) + alt("en", "HTTPS://EXAMPLE.COM/en") + alt("fr", B_URL)),
    page("fr", B_URL, canon(B_URL) + alt("fr", A_URL) + alt("en", B_URL)),
    ], 0, [], "A3: scheme/host lowercased in URL identity; strict-string impl flags self_missing + external")

case("H03", [page("en", A_URL, canon(A_URL) + alt("en", A_URL) + alt("fr", "mailto:webmaster@example.com"))],
     1, [REL], "A12: scheme without authority is not absolute")
case("H04", [page("en", A_URL, canon(A_URL) + alt("en", A_URL) + alt("fr", "tel:+1234567890"))],
     1, [REL], "A12: same as H03")
case("H05", [page("en", A_URL, canon(A_URL) + alt("en", A_URL) + alt("fr", "#top"))],
     1, [REL], None)
case("H05b", [page("en", A_URL, canon(A_URL) + alt("en", A_URL + "#top"))],
     1, [SELF], "A3 preserves fragments: .../en#top != .../en; external info is exit-neutral (A1)")
case("H06", [
    page("en", A_URL, canon(A_URL) + alt("en", " " + A_URL + " ") + alt("fr", B_URL)),
    page("fr", B_URL, canon(B_URL) + alt("fr", A_URL) + alt("en", B_URL)),
    ], 1, [REL, SELF],
     "REMAINING-UNDECIDED class (named, same family as T09): whitespace around the href value; literal A12 RFC-3986 parse of ' https://...' fails = relative_href and (A4) it cannot self-satisfy, so self_missing too; WHATWG-strip reading = clean; tool strips",
     undecidable=True)

# --- structure -------------------------------------------------------------
case("S01", [
    page("en", A_URL, canon(A_URL) + alt("en", A_URL) + alt("fr", B_URL)),
    page("fr", B_URL, canon(B_URL) + alt("fr", A_URL) + alt("en", B_URL)),
    ], 0, [], "cross-clean pair on one line: both alternates on one line must be seen")
case("S02", [
    page("en", A_URL,
         '<link rel="alternate"\n  hreflang="en"\n  href="' + A_URL + '">\n'
         '<link rel="alternate"\n  hreflang="fr"\n  href="' + B_URL + '">'),
    page("fr", B_URL, canon(B_URL) + alt("fr", A_URL) + alt("en", B_URL)),
    ], 0, [], "links split across lines must both be seen")
case("S03", [
    page("en", A_URL, canon(A_URL) + alt("en", A_URL) + '<link rel=alternate hreflang=fr href=' + B_URL + '>'),
    page("fr", B_URL, canon(B_URL) + alt("fr", A_URL) + alt("en", B_URL)),
    ], 0, [], "unquoted attributes must parse")
case("S04", [
    page("en", A_URL,
         canon(A_URL) + alt("en", A_URL)
         + '<template><link rel="alternate" hreflang="en" href="' + A_URL + '"></template>'),
    ], 0, [], "A13: template subtrees are not scanned; a template-blind impl flags duplicate_pair")
case("S05", [
    page("en", A_URL, canon(A_URL) + alt("en", A_URL)
         + '<svg><a xlink:href="' + B_URL + '"><text>fr</text></a></svg>'),
    ], 0, [], "an xlink anchor inside svg is not a link element")
case("S05b", [
    page("en", A_URL, canon(A_URL) + alt("en", A_URL)
         + '<svg><link rel="alternate" hreflang="de" xlink:href="' + C_URL + '"></svg>'),
    ], 0, [], "A13: svg subtrees are not scanned; a namespace-blind impl reports the svg link")
case("S06", [
    page("en", A_URL, canon(A_URL) + alt("en", A_URL)
         + '<noscript><link rel="alternate" hreflang="en" href="' + A_URL + '"></noscript>'),
    ], 1, [DUP], "A14: noscript content scanned as markup")
case("S07", [
    page("en", A_URL,
         '<link rel="canonical" rel="alternate" hreflang="en" href="https://example.com/other.html">'
         + alt("en", A_URL)),
    ], 1, [CAN], "HTML duplicate-attribute rule: first occurrence wins (rel=canonical)")

# --- reciprocity -----------------------------------------------------------
ALLPAIRS = "".join(alt(t, u) for t in ("en", "fr", "de")
                   for u in (A_URL, B_URL, C_URL))
case("R01", [
    page("en", A_URL, canon(A_URL) + ALLPAIRS),
    page("fr", B_URL, canon(B_URL) + ALLPAIRS),
    page("de", C_URL, canon(C_URL) + ALLPAIRS),
    ], 0, [], "3-page cluster where every page declares every (tag, page) pair: fully reciprocal")
case("R02", [
    page("en", A_URL, canon(A_URL) + alt("en", B_URL)),
    page("fr", B_URL, canon(B_URL) + alt("en", C_URL)),
    page("de", C_URL, canon(C_URL) + alt("en", A_URL)),
    ], 1, [SELF] * 3 + [NON] * 3,
     "one-way cycle: multiset 3x self_missing + 3x nonreciprocal (A2 per page / per annotation)")
case("R03", [page("en", A_URL, canon(A_URL) + alt("en", A_URL) + alt("de", "https://external.example/de"))],
     0, [], "A1: external partner informational, exit-neutral")
case("R04", [
    page("a", A_URL, canon(A_URL) + alt("en", A_URL)),
    page("b", A_URL, canon(A_URL) + alt("en", A_URL), fname="b.html"),
    ], 2, [DU], None)
case("R05", [page("en", "/en", alt("en", A_URL))], 2, [NA], None)
case("R06", [page("en", A_URL, alt("en", A_URL), fname="missing.html", omit=True)], 2, [IU], None)
case("R07", [page("en", A_URL, alt("en", A_URL))], 64, [],
     "A15: version != 1 is exit 64", version=2)
case("R08", [
    page("a", A_URL, canon(A_URL) + alt("en_GB", A_URL)),
    page("b", A_URL, alt("en", A_URL), fname="b.html"),
    ], 2, [INV, DU], "A8: input fault present AND findings from the readable page still listed; exit 2")

# --- canonical -------------------------------------------------------------
case("C01", [
    page("en", "https://example.com/en/page.html",
         canon("page.html") + alt("en", "https://example.com/en/page.html")
         + alt("fr", "https://example.com/fr/page.html")),
    page("fr", "https://example.com/fr/page.html",
         canon("page.html") + alt("fr", "https://example.com/en/page.html")
         + alt("en", "https://example.com/fr/page.html")),
    ], 0, [], "relative canonical resolving to the page itself; cross-clean reciprocity")
case("C02", [
    page("en", "https://example.com/en/page.html",
         canon("https://example.com/en/page.html/")
         + alt("en", "https://example.com/en/page.html")
         + alt("fr", "https://example.com/fr/page.html")),
    page("fr", "https://example.com/fr/page.html",
         canon("page.html") + alt("fr", "https://example.com/en/page.html")
         + alt("en", "https://example.com/fr/page.html")),
    ], 1, [CAN], "A3: trailing slash is significant")
case("C03", [
    page("en", "https://example.com/en/page.html",
         canon("page.html") + canon("/other.html")
         + alt("en", "https://example.com/en/page.html")),
    ], 0, [], "A6: first canonical in document order wins")
case("B01", [
    page("en", A_URL,
         '<base href="https://example.com/alt/">' + canon("") + alt("en", A_URL)),
    ], 0, [], "empty canonical href resolves to the page; <base> is not consulted")

# --- amendment-targeted attack fixtures ------------------------------------
case("X01", [
    page("en", A_URL,
         canon(A_URL) + alt("en", A_URL)
         + '<link rel="ALTERNATE" hreflang="en-GB-oed" href="' + A_URL + '">'),
    ], 1, [INV],
     "A13: rel is a case-insensitive token set, so the ALTERNATE link is an alternate carrying an invalid tag; a rel-value-case-blind impl sees nothing (tool defect candidate)")
case("X02", [
    page("en", A_URL, canon(A_URL) + alt("en", A_URL)
         + '<link rel="alternate stylesheet" title="wide" href="https://example.com/w.css">'),
    ], 0, [], "A13: rel containing stylesheet alongside alternate is NOT an alternate -> clean")
case("X03", [
    page("en", A_URL, canon(A_URL) + alt("en", A_URL)
         + '<link rel="alternate" hreflang="en">'),
    ], 0, [], "A9: a link without href is not an alternate and is not reported")
case("X04", [
    page("en", "https://a.example",
         canon("https://a.example/") + alt("en", "https://a.example:443/") + alt("fr", "https://b.example/fr")),
    page("fr", "https://b.example/fr",
         canon("https://b.example/fr") + alt("fr", "https://a.example/dir/..") + alt("en", "https://b.example/fr")),
    ], 0, [], "A3: default port dropped, dot-segments removed, empty path -> / ; strict-string impl flags externals")
case("X05", [
    page("en", "https://a.example/dir/page",
         canon("https://a.example/dir/page") + alt("en", "page") + alt("fr", "https://b.example/fr")),
    page("fr", "https://b.example/fr",
         canon("https://b.example/fr") + alt("fr", "https://a.example/dir/page") + alt("en", "https://b.example/fr")),
    ], 1, [REL, SELF],
     "A4: the relative href is not resolved, so it cannot satisfy the self-reference; self_missing must still fire")
case("X06", [
    page("en", A_URL, canon(A_URL) + alt("en", A_URL) + alt("en", "//b.example/")),
    ], 1, [REL],
     "A4: a non-absolute href contributes to NO other finding, including the informational external target")
case("X07", [
    page("en", A_URL, alt("en", A_URL) + canon(A_URL), fname="link.html"),
    ], 2, [IU], "A15: a symlinked page file is input_unreadable",
     extra_files={"link.html": ("symlink", "../X07-outside/real.html")})
case("X08", [
    page("a", A_URL, alt("en", A_URL) + canon(A_URL), fname="shared.html"),
    page("b", "https://example.com/fr", alt("fr", "https://example.com/fr") + canon("https://example.com/fr"),
         fname="shared.html"),
    ], 2, [CAN, SELF, IU],
     "A15 duplicate file faults the second entry; A8: the faulted page contributes no policy findings, the valid page is still audited against the shared bytes (its content is page b's html: self_missing + canonical_not_self + external info)")
case("X10", [
    page("en", A_URL, canon(A_URL) + alt("en", A_URL) + alt("en", A_URL) + alt("en", A_URL)),
    ], 1, [DUP, DUP], "A2: duplicate_pair is one finding per repeat occurrence (3 identical links = 2 findings)")

# G01: Google's canonical mixed-language cluster (Google, google-localized-versions:
# "If page X links to page Y, page Y must link back to page X." -- a return link,
# not a same-tag link). The as-written contract rule demands the SAME tag on the
# return, so this Google-clean cluster is flagged 2x nonreciprocal.
case("G01", [
    page("en", A_URL, canon(A_URL) + alt("en", A_URL) + alt("fr", B_URL)),
    page("fr", B_URL, canon(B_URL) + alt("en", A_URL) + alt("fr", B_URL)),
    ], 1, [NON, NON],
     "CONTRADICTION-WITH-SOURCE (open, L1 decision needed): Google-pattern cluster flagged nonreciprocal x2 by the as-written same-tag rule")


def observed(res):
    """Merge ids generically across the delivered tool's schema and mine."""
    ids, info = [], []
    for row in res.get("findings", []) or []:
        fid = row.get("id") if isinstance(row, dict) else row
        sev = row.get("severity") or row.get("class")
        if fid == "hreflang_external_target" or sev == "info" or sev == "informational":
            info.append(fid)
        else:
            ids.append(fid)
    for row in res.get("input_faults", []) or []:
        ids.append(row.get("id") if isinstance(row, dict) else row)
    return sorted(i for i in ids if i), sorted(i for i in info if i)


def main():
    os.makedirs(REC, exist_ok=True)
    rows = []
    for c in CASES:
        cdir = os.path.join(FIX, c["id"])
        if os.path.exists(cdir):
            import shutil
            shutil.rmtree(cdir)
        os.makedirs(cdir)
        manifest_pages = []
        for p in c["pages"]:
            if not p.get("omit"):
                with open(os.path.join(cdir, p["file"]), "w", encoding="utf-8") as f:
                    f.write(p["html"])
            manifest_pages.append({"id": p["id"], "file": p["file"], "url": p["url"]})
        for name, spec in c["extra_files"].items():
            target = os.path.join(cdir, name)
            if spec[0] == "symlink":
                if os.path.lexists(target):
                    os.remove(target)
                outside = os.path.join(LANE, "fixtures", c["id"] + "-outside")
                os.makedirs(outside, exist_ok=True)
                real = os.path.join(outside, "real.html")
                with open(real, "w", encoding="utf-8") as f:
                    f.write(c["pages"][0]["html"])
                os.symlink(os.path.relpath(real, cdir), target)
            else:
                with open(target, "w", encoding="utf-8") as f:
                    f.write(c["pages"][1]["html"])
        mpath = os.path.join(cdir, "manifest.json")
        with open(mpath, "w", encoding="utf-8") as f:
            json.dump({"version": c["version"], "pages": manifest_pages}, f, indent=1)

        cmd = [sys.executable, "-B", TOOL, "--manifest", mpath, "--root", cdir, "--json"]
        env = dict(os.environ, TMPDIR=S + "/tmp")
        proc = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=S)
        receipt = os.path.join(REC, "case-%s.txt" % c["id"])
        with open(receipt, "w", encoding="utf-8") as f:
            f.write("case: %s\n" % c["id"])
            f.write("tool: %s\n" % TOOL)
            f.write("command: TMPDIR=%s python3 -B %s --manifest %s --root %s --json\n"
                    % (S + "/tmp", TOOL, mpath, cdir))
            f.write("--- stdout ---\n%s" % proc.stdout)
            if proc.stderr:
                f.write("--- stderr ---\n%s" % proc.stderr)
            f.write("exit: %d\n" % proc.returncode)

        obs_exit = proc.returncode
        try:
            res = json.loads(proc.stdout)
            obs_ids, obs_info = observed(res)
            pages_scanned = res.get("pages", -1)
        except Exception:
            obs_ids, obs_info, pages_scanned = ["<unparseable>"], [], -1

        ok = obs_exit == c["exp_exit"] and obs_ids == c["exp_ids"]
        if ok:
            status = "AMBIG-CONF" if c["ambiguous"] else "CONFIRMED"
        elif c["undecidable"]:
            status = "AMBIG-DIV"
        else:
            status = "MISMATCH"
        rows.append((c["id"], obs_exit, c["exp_exit"], ",".join(obs_ids),
                     ",".join(c["exp_ids"]), ",".join(obs_info), pages_scanned, status,
                     c["ambiguous"] or ""))
        print("%-5s exit=%s(exp %s) ids=[%s] exp=[%s] info=[%s] pages=%s %s"
              % (c["id"], obs_exit, c["exp_exit"], ",".join(obs_ids),
                 ",".join(c["exp_ids"]), ",".join(obs_info), pages_scanned, status))

    n_conf = sum(1 for r in rows if r[7] == "CONFIRMED")
    n_ac = sum(1 for r in rows if r[7] == "AMBIG-CONF")
    n_ad = sum(1 for r in rows if r[7] == "AMBIG-DIV")
    n_mis = sum(1 for r in rows if r[7] == "MISMATCH")
    print("DRIVER-SUMMARY tag=%s cases=%d confirmed=%d ambiguous_conf=%d ambiguous_div=%d mismatch=%d"
          % (TAG, len(rows), n_conf, n_ac, n_ad, n_mis))
    with open(os.path.join(REC, "verdicts-%s.json" % TAG), "w", encoding="utf-8") as f:
        json.dump([dict(id=r[0], observed_exit=r[1], expected_exit=r[2],
                        observed_ids=r[3], expected_ids=r[4], observed_info=r[5],
                        pages=r[6], status=r[7], note=r[8]) for r in rows], f, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
