#!/usr/bin/env python3
"""Round-59 C3 mutation test — fixture builder (v2, against the wave-1 counter snapshot).

Fixture repo D (scratch): one base commit + one commit per measured variant.
  - the base commits carry the real base registry + the real base
    corpus/knowledge/crawler-identity.md bytes from fd6303ce, the pre-append mirror,
    the retained bodies and their receipts.
  - every variant commit is a *measured* revision the counter can be run against.
"""
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess

S = "/fast/scratch/hyaku/kake-r59/MutC3Counter"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
COUNTER = f"{LANE}/.ufo/waves/round-59/c59_quote_truth.py"
BASE_REV = "fd6303ce5c14b3f892dec586297a942ab6e4193b"
D = f"{S}/D"

ROUND_DATE = "2026-10-27"
URL_S425 = "https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers"
URL_S426 = "https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests"
STALE_LINE = "- **A user-agent string is the only thing a server log records about the crawler.** Two"
TAG = f"[r59-correction {ROUND_DATE}]"
VALIDATE = ".ufo/waves/round-59/assimilation/validate"
VALIDATE_REG = f"{VALIDATE}/corpus/SOURCES.md"


def git(*args, cwd=None):
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def read_bytes(p):
    with open(p, "rb") as fh:
        return fh.read()


def lane_show(rev, path):
    p = subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"], capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f"cannot read {rev}:{path}")
    return p.stdout


spec = importlib.util.spec_from_file_location("c59qt", COUNTER)
qt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qt)

BODIES = {sid: read_bytes(f"{LANE}/.ufo/waves/round-59/sources/{sid}.html") for sid in ("S425", "S426")}
TEXTS = {sid: re.sub(r"\s+", " ", raw.decode("utf-8")) for sid, raw in BODIES.items()}


def span_ok(sid, span, topic=None):
    text = TEXTS[sid]
    others = [TEXTS[o] for o in ("S425", "S426") if o != sid]
    if span not in text or not qt.in_content(text, span, sid):
        return False
    if not (6 <= qt.units(span) <= 25) or len(span) > 160:
        return False
    if text.count(span) != 1 or any(span in o for o in others):
        return False
    return not (topic and topic not in span)


BASE_SOURCES = lane_show(BASE_REV, "corpus/SOURCES.md").decode("utf-8")
BASE_DOC = lane_show(BASE_REV, "corpus/knowledge/crawler-identity.md").decode("utf-8")
BASE_LINES = BASE_DOC.split("\n")
STALE_IDX = [i for i, ln in enumerate(BASE_LINES) if ln == STALE_LINE]
assert len(STALE_IDX) == 1
STALE_IDX = STALE_IDX[0]


def bullet_end(lines, s):
    end = s + 1
    while end < len(lines) and lines[end].strip() and not re.match(r"^\s{0,3}[-*+] ", lines[end]):
        end += 1
    return end


END = bullet_end(BASE_LINES, STALE_IDX)
print(f"stale line index {STALE_IDX}, bullet ends at base line {END} (distance {END - STALE_IDX})")

S425_SPANS = [
    "The source IP address of the request.",
    "Google's crawlers identify themselves in three ways:",
    "response header fields are present in the HTTP response, Google's crawlers use the",
    "HTTP status code when Google attempts to access your site over HTTP/2. If that's not feasible, you",
]
S426_SPANS = [
    "Run a reverse DNS lookup on the accessing IP address from your logs, using the",
    "Verify that it's the same as the original accessing IP address from your logs.",
    "There are two methods for verifying requests from Google:",
    "Alternatively, you can identify Googlebot by IP address by matching the crawler's IP address to the",
]
for sp in S425_SPANS:
    assert span_ok("S425", sp), sp
for sp in S426_SPANS:
    assert span_ok("S426", sp), sp
assert span_ok("S425", S425_SPANS[0], topic="IP address")
assert span_ok("S426", S426_SPANS[0], topic="reverse DNS")

NL_SPAN = ("Google's crawlers and fetchers are designed to be run simultaneously by thousands of "
           "machines to improve performance and scale as the web grows.")
assert NL_SPAN in TEXTS["S425"] and NL_SPAN not in BODIES["S425"].decode("utf-8")
assert TEXTS["S425"].count(NL_SPAN) == 1

LONG_SPAN = ("crawling performance and may switch protocols between crawling sessions depending on "
             "previous crawling statistics. The default protocol version used by Google's crawlers ")
assert qt.units(LONG_SPAN) <= 25 and len(LONG_SPAN) > 160 and TEXTS["S425"].count(LONG_SPAN) == 1

IP26_SPAN = ("near the sites that they might access. Therefore, your logs may show visits from several "
             "IP addresses. Google egresses primarily from IP addresses in the United")
assert qt.units(IP26_SPAN) > 25 and len(IP26_SPAN) <= 160 and TEXTS["S425"].count(IP26_SPAN) == 1

FOOTER_SPAN = "Java is a registered trademark of Oracle and/or its affiliates."
assert FOOTER_SPAN in TEXTS["S425"]
SHARED_SPAN = "and product functions where the end user triggers a fetch. For example,"
assert TEXTS["S425"].count(SHARED_SPAN) == 1 and SHARED_SPAN in TEXTS["S426"]
assert qt.in_content(TEXTS["S425"], SHARED_SPAN, "S425") and qt.units(SHARED_SPAN) >= 6

ANCHOR_S425 = "Technical properties of Google's crawlers and fetchers"
ANCHOR_S426 = "Use command line tools"
H1_S425 = "Overview of Google crawlers and fetchers (user agents)"
FAKE_ANCHOR = "Sample heading for tests"
assert ANCHOR_S425 in qt.article_headings(TEXTS["S425"], "S425")
assert ANCHOR_S426 in qt.article_headings(TEXTS["S426"], "S426")
assert H1_S425 not in qt.article_headings(TEXTS["S425"], "S425")

TITLE_S425 = "Google Crawler (User Agent) Overview"
TITLE_S426 = "Verify Requests from Google Crawlers and Fetchers"
DATE_S425 = "2026-06-12"
DATE_S426 = "2026-03-20"


def rows_default():
    return {
        "S425": (f"| S425 | Google Crawling Infrastructure — {TITLE_S425} — {URL_S425} | docs | A | "
                 "Which signals a server log carries about Google's crawlers and fetchers | "
                 f"§ {ANCHOR_S425} (Last updated {DATE_S425} UTC) | "
                 "Google's crawlers identify themselves by user-agent, source IP address and reverse DNS | "
                 f"mined | {ROUND_DATE} | 180d | "
                 "corpus/knowledge/crawler-identity-signals.md, corpus/knowledge/crawler-identity.md |"),
        "S426": (f"| S426 | Google Crawling Infrastructure — {TITLE_S426} — {URL_S426} | docs | A | "
                 "How to verify that a request really came from Google's crawlers and fetchers | "
                 f"§ {ANCHOR_S426} (Last updated {DATE_S426} UTC) | "
                 "A crawler can be verified by reverse DNS on the accessing IP address or by matching the IP ranges | "
                 f"mined | {ROUND_DATE} | 180d | "
                 "corpus/knowledge/googlebot-verification.md |"),
    }


def registry(rows):
    lines = BASE_SOURCES.split("\n")
    last = max(i for i, ln in enumerate(lines) if re.match(r"^ *\| *S[0-9]{3,} *\|", ln))
    return "\n".join(lines[:last + 1] + [rows["S425"], rows["S426"]] + lines[last + 1:])


def doc(lines, insert, at=None, delete_at=None):
    lines = list(lines)
    if delete_at is not None:
        del lines[delete_at]
    pos = bullet_end(lines, STALE_IDX) if at is None else at
    return "\n".join(lines[:pos] + list(insert) + lines[pos:])


def corr(span, cite="S425", tag=TAG, tail="", curly=False, code=False):
    q = f'"{span}"'
    if code:
        q = f"`{q}`"
    out = f"- {tag} Correction: the log carries more than the user-agent string [{cite}]: {q}"
    if tail:
        out += f" {tail}"
    if curly:
        out += " The page says “the source IP address of the request” in prose."
    return out


ENTRY_S425 = f"""# Google crawler identity: three signals

source: S425 — {URL_S425}
verified-at: {ROUND_DATE}
recheck: 180d
ground: which signals a server log carries about the crawler — user-agent, source IP address, reverse DNS

## What the page states

The page says Google's crawlers identify themselves in three ways [S425]:

> "{S425_SPANS[1]}"

> "{S425_SPANS[0]}"

> "{S425_SPANS[2]}"

> "{S425_SPANS[3]}"
"""

ENTRY_S426 = f"""# Verifying Google's crawlers and fetchers

source: S426 — {URL_S426}
verified-at: {ROUND_DATE}
recheck: 180d
ground: how to confirm that a request came from Google rather than from a name in the user-agent string

## What the page states

The page gives two verification routes [S426]:

> "{S426_SPANS[2]}"

> "{S426_SPANS[0]}"

> "{S426_SPANS[1]}"

> "{S426_SPANS[3]}"
"""


def gate_line(sid, url, digest, nbytes, anchor, spans):
    parts = [f"- {sid} {url} — {ROUND_DATE} — sha256 {digest} — {nbytes} bytes — {anchor}"]
    for sp in spans:
        parts.append(f'"{sp}" ({qt.units(sp)} units)')
    return " ".join(parts)


def gate_default(spans425=None, spans426=None, anchor425=None):
    s425 = spans425 if spans425 is not None else S425_SPANS
    a425 = anchor425 or ANCHOR_S425
    return [
        gate_line("S425", URL_S425, hashlib.sha256(BODIES["S425"]).hexdigest(), len(BODIES["S425"]),
                  f"§ {a425} (Last updated {DATE_S425} UTC)", s425),
        gate_line("S426", URL_S426, hashlib.sha256(BODIES["S426"]).hexdigest(), len(BODIES["S426"]),
                  f"§ {ANCHOR_S426} (Last updated {DATE_S426} UTC)", S426_SPANS),
    ]


CENSUS_ARGV = f"bash scripts/sources-census.sh --file {VALIDATE_REG}\n"
CENSUS_STDOUT = f"file\tok\t{VALIDATE_REG}\n"
CENSUS_EXIT = "exit=0\n"


def write_tree(parent, files, msg):
    if parent is not None:
        rc, _, err = git("reset", "--hard", "-q", parent, cwd=D)
        assert rc == 0, err
        rc, _, err = git("clean", "-qfd", cwd=D)
        assert rc == 0, err
    for path, content in files.items():
        full = os.path.join(D, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        if isinstance(content, str):
            content = content.encode("utf-8")
        with open(full, "wb") as fh:
            fh.write(content)
    assert git("add", "-A", cwd=D)[0] == 0
    rc, _, err = git("-c", "user.name=selftest", "-c", "user.email=selftest@local",
                     "commit", "-q", "-m", msg, cwd=D)
    assert rc == 0, err
    return git("rev-parse", "HEAD", cwd=D)[1].strip()


def measured(doc_text, rows=None, entry425=None, entry426=None, gate=None, bodies=None):
    rows = rows or rows_default()
    reg = registry(rows)
    e425 = entry425 if entry425 is not None else ENTRY_S425
    e426 = entry426 if entry426 is not None else ENTRY_S426
    g = gate if gate is not None else gate_default()
    files = {
        "corpus/SOURCES.md": reg,
        "corpus/knowledge/crawler-identity.md": doc_text,
        "corpus/knowledge/crawler-identity-signals.md": e425,
        "corpus/knowledge/googlebot-verification.md": e426,
        "corpus/lessons/round-59.md": "# round-59 — quote truth\n\n## Gate\n\n" + "\n".join(g) + "\n",
        f"{VALIDATE}/census-argv.txt": CENSUS_ARGV,
        f"{VALIDATE}/census-stdout.txt": CENSUS_STDOUT,
        f"{VALIDATE}/census-exit.txt": CENSUS_EXIT,
        f"{VALIDATE}/corpus/SOURCES.md": reg,
        f"{VALIDATE}/corpus/knowledge/crawler-identity-signals.md": e425,
        f"{VALIDATE}/corpus/knowledge/googlebot-verification.md": e426,
    }
    if bodies:
        files.update(bodies)
    return files


def build():
    if os.path.exists(D):
        shutil.rmtree(D)
    os.makedirs(D)
    assert git("init", "-q", "-b", "main", cwd=D)[0] == 0
    rc, out, _ = git("-C", D, "rev-parse", "--show-toplevel")
    assert rc == 0 and os.path.realpath(out.strip()) == os.path.realpath(D), out

    base_files = {
        "corpus/SOURCES.md": BASE_SOURCES,
        "corpus/knowledge/crawler-identity.md": BASE_DOC,
        ".ufo/waves/round-59/assimilation/pre-append/corpus/SOURCES.md": BASE_SOURCES,
        ".ufo/waves/round-59/sources/S425.html": BODIES["S425"],
        ".ufo/waves/round-59/sources/S426.html": BODIES["S426"],
        ".ufo/waves/round-59/sources/receipts.json":
            read_bytes(f"{LANE}/.ufo/waves/round-59/sources/receipts.json"),
    }
    base_rows = qt.parse_registry(BASE_SOURCES)
    base_files[".ufo/waves/round-59/assimilation/mirror-pin.json"] = json.dumps(
        {"sha256": hashlib.sha256(BASE_SOURCES.encode("utf-8")).hexdigest(), "rows": len(base_rows)}, indent=1)
    B0 = write_tree(None, base_files, "base: real base registry + real base knowledge doc + retained bodies")
    print("base", B0, "rows", len(base_rows))

    # extra bases with a longer stale bullet (window probes)
    b2_lines = list(BASE_LINES)
    extra = ["  continued bullet line %d of the stale claim, still inside the same bullet." % i for i in range(10)]
    b2_doc = "\n".join(b2_lines[:END] + extra + b2_lines[END:])
    B_LONG = write_tree(B0, {"corpus/knowledge/crawler-identity.md": b2_doc},
                        "base-long: stale bullet extended by ten lines")
    b3_lines = list(BASE_LINES)
    extra3 = ["  continued bullet line %d of the stale claim, still inside the same bullet." % i for i in range(5)]
    b3_doc = "\n".join(b3_lines[:END] + extra3 + b3_lines[END:])
    B_MID = write_tree(B0, {"corpus/knowledge/crawler-identity.md": b3_doc},
                       "base-mid: stale bullet extended by five lines")

    V = {}

    def add(name, parent, files, msg):
        V[name] = {"base": parent, "rev": write_tree(parent, files, msg)}

    good_doc = doc(BASE_LINES, [corr(S425_SPANS[0])])

    add("V0_positive", B0, measured(good_doc), "V0 positive control")

    add("V1_stale_twice", B0, measured(doc(BASE_LINES, [corr(S425_SPANS[0]), STALE_LINE])),
        "V1 stale sentence duplicated")

    add("V2_position_16", B0, measured(doc(BASE_LINES, [corr(S425_SPANS[0])], at=END + 16)),
        "V2 correction inserted 16 base lines after the bullet end")

    add("V3_line_deleted", B0, measured(doc(BASE_LINES, [corr(S425_SPANS[0])], delete_at=STALE_IDX + 30)),
        "V3 a base line deleted")

    add("V4_wrong_tag", B0, measured(doc(BASE_LINES, [corr(S425_SPANS[0], tag="[r59-correction 2026-10-26]")])),
        "V4 wrong correction tag date")

    add("V5_wrong_id", B0, measured(doc(BASE_LINES, [corr(S425_SPANS[0], cite="S426", tail="See also [S426].")])),
        "V5 correction cites S426")

    add("V6_no_topic", B0, measured(doc(BASE_LINES, [corr(S425_SPANS[1])])),
        "V6 correction quote without the topic")

    e425 = ENTRY_S425.replace("## What the page states\n", f'## What the page states\n\n> "{LONG_SPAN}"\n')
    add("V7_long_quote", B0, measured(good_doc, entry425=e425), "V7 entry quote over 160 characters")

    raw = BODIES["S425"].decode("utf-8")
    body8 = raw.replace(f"<p>Last updated {DATE_S425} UTC.</p>",
                        f'<p data-revision="Last updated {DATE_S425} UTC">.</p>')
    body8 = body8.replace(f'["Last updated {DATE_S425} UTC."]', "[]")
    assert f"<p>Last updated {DATE_S425} UTC.</p>" not in body8
    assert f'["Last updated {DATE_S425} UTC."]' not in body8
    add("V8_date_in_attribute", B0,
        measured(good_doc, bodies={".ufo/waves/round-59/sources/S425.html": body8}),
        "V8 printed revision only inside an attribute")

    e425 = ENTRY_S425.replace("## What the page states\n", f'## What the page states\n\n> "{FOOTER_SPAN}"\n')
    add("V9_footer_quote", B0, measured(good_doc, entry425=e425), "V9 entry quote from the page footer")

    rows = rows_default()
    rows["S425"] = rows["S425"].replace(f"§ {ANCHOR_S425} (Last updated", f"§ {H1_S425} (Last updated")
    add("V10_h1_anchor", B0,
        measured(good_doc, rows=rows, gate=gate_default(anchor425=H1_S425)), "V10 row anchor is the page h1")

    rows = rows_default()
    rows["S425"] = rows["S425"].replace(
        "corpus/knowledge/crawler-identity-signals.md, corpus/knowledge/crawler-identity.md",
        "corpus/knowledge/crawler-identity.md, corpus/knowledge/crawler-identity-signals.md")
    add("V11_used_by_order", B0, measured(good_doc, rows=rows), "V11 used-by cell order swapped")

    add("V12_curly_quotes", B0, measured(doc(BASE_LINES, [corr(S425_SPANS[0], curly=True)])),
        "V12 correction with curly quotes")

    add("V13_short_quote", B0, measured(doc(BASE_LINES, [corr("The source IP address")])),
        "V13 correction quote of 4 units that still carries the topic")

    add("V14_over_unit_ceiling", B0, measured(doc(BASE_LINES, [corr(IP26_SPAN)])),
        "V14 correction quote over 25 units")

    e425 = f"""# Google crawler identity: three signals

source: S425 — {URL_S425}
verified-at: {ROUND_DATE}
recheck: 180d
ground: which signals a server log carries about the crawler

## What the page states

The page says Google's crawlers identify themselves in three ways [S425]:

> "{S425_SPANS[0]}"
"""
    add("V15_one_span", B0, measured(good_doc, entry425=e425), "V15 entry with a single unique span")

    add("V16_shared_span", B0, measured(good_doc, gate=gate_default(spans425=[SHARED_SPAN] + S425_SPANS)),
        "V16 Gate quote present in both bodies")

    gate = gate_default()
    gate[0] = re.sub(r" \(\d+ units\)", "", gate[0])
    add("V17_no_unit_count", B0, measured(good_doc, gate=gate), "V17 Gate line without unit counts")

    add("V18_newline_span", B0, measured(good_doc, gate=gate_default(spans425=[NL_SPAN] + S425_SPANS)),
        "V18 Gate quote across a raw newline")

    body20 = raw.replace('class="devsite-article-body clearfix', 'class="devsite-body clearfix')
    assert 'class="devsite-article-body' not in body20
    add("V20_no_article_block", B0,
        measured(good_doc, bodies={".ufo/waves/round-59/sources/S425.html": body20}),
        "V20 retained body without the article block marker")

    add("V21_code_span_quote", B0, measured(doc(BASE_LINES, [corr(S425_SPANS[0], code=True)])),
        "V21 correction quote inside a code span")

    body22 = raw.replace('<h2 id="crawl-verify-crawler"',
                         '<pre><h2 id="fake-sample">' + FAKE_ANCHOR + '</h2></pre>\n<h2 id="crawl-verify-crawler"',
                         1)
    assert FAKE_ANCHOR in body22
    rows = rows_default()
    rows["S425"] = rows["S425"].replace(f"§ {ANCHOR_S425} (Last updated", f"§ {FAKE_ANCHOR} (Last updated")
    add("V22_fake_heading_in_pre", B0,
        measured(good_doc, rows=rows, gate=gate_default(anchor425=FAKE_ANCHOR),
                 bodies={".ufo/waves/round-59/sources/S425.html": body22}),
        "V22 row anchor heading lives inside a code sample")

    add("V25_inside_bullet", B0, measured(doc(BASE_LINES, [corr(S425_SPANS[0])], at=STALE_IDX + 1)),
        "V25 correction inserted inside the stale bullet")

    CROSS_SPAN = "Run a reverse DNS lookup on the accessing IP address from your logs, using the"
    assert CROSS_SPAN in TEXTS["S426"] and qt.units(CROSS_SPAN) <= 25
    body26 = raw.replace("<devsite-content-footer",
                         f"<p>{CROSS_SPAN}</p>\n<devsite-content-footer", 1)
    assert body26.count(CROSS_SPAN) == 1
    add("V26_cross_body_span", B0,
        measured(doc(BASE_LINES, [corr(CROSS_SPAN)]),
                 bodies={".ufo/waves/round-59/sources/S425.html": body26}),
        "V26 correction quotes a span that also occurs in S426")

    CHROME_SPAN = "Looking for the latest updates to this page?"
    assert TEXTS["S425"].count(CHROME_SPAN) == 1 and CHROME_SPAN not in TEXTS["S426"]
    assert not qt.in_content(TEXTS["S425"], CHROME_SPAN, "S425")
    e425 = ENTRY_S425.replace("## What the page states\n",
                              f'## What the page states\n\n> "{CHROME_SPAN}"\n')
    add("V27_chrome_quote", B0, measured(good_doc, entry425=e425),
        "V27 entry quotes page chrome that sits inside the article window")

    attr_line = (f'- {TAG} Correction [S425]: <span data-note="{S425_SPANS[0]}">see the page</span>')
    add("V28_attr_hidden_quote", B0, measured(doc(BASE_LINES, [attr_line])),
        "V28 correction hides its quote inside an HTML attribute")

    # long-bullet window probes
    long_lines = b2_doc.split("\n")
    long_doc = doc(long_lines, [corr(S425_SPANS[0])])
    add("V23_long_bullet", B_LONG, measured(long_doc), "V23 correction at the end of a 14-line bullet")

    mid_lines = b3_doc.split("\n")
    mid_doc = doc(mid_lines, [corr(S425_SPANS[0])])
    add("V24_mid_bullet", B_MID, measured(mid_doc), "V24 correction at the end of a 9-line bullet")

    meta = {"base": B0, "bases": {"B0": B0, "B_LONG": B_LONG, "B_MID": B_MID},
            "end": END, "stale_idx": STALE_IDX, "variants": V}
    with open(f"{S}/variants.json", "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
    for k, v in V.items():
        print(f"  {k:24s} base={v['base'][:8]} rev={v['rev'][:8]}")
    return meta


if __name__ == "__main__":
    build()
