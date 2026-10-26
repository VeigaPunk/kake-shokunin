#!/usr/bin/env python3
"""ExecSweepsNegative — negative-claim sweeps over the two round-57 retained Baidu bodies.

Seat: ExecSweepsNegative (W2 falsify, claim C3). Read-only over the lane.

Scope ladder (every count says which one it used):
  RAW    the whole retained body as written (entities such as &nbsp; are not decoded);
  BLOCK  the raw article block slice, located by the counter's constants
         (S421 `class="article-info"` .. `往期回顾`, S422 `class="info-item-time"` .. `wiki-foot-right`);
  TEXT   the article block's text nodes, counted node-by-node — the version-2 rule (a span qualifies only
         when it lies inside one `>...<` node after <style>/<script> removal);
  PAR    a named paragraph slice of TEXT (node range), for claims scoped to "the paragraph";
  NODE:<i> / SENT:<marker>  one text node / one sentence, for claims scoped to "this sentence".
TEXT <= BLOCK <= RAW holds unless a term straddles an inline tag; a term split across nodes is invisible to
TEXT by construction, which is exactly the version-2 rule the entries are written against.

The locators are re-implemented here from the counter's own definitions
(`.ufo/waves/round-57/c57_quote_truth.py` lines 95-96 and `content_window` / `text_segments`), not imported:
an independent extractor cannot inherit the counter's bug.

Usage: python3 -B sweeps.py [--root <lane>] [--json]
Exit:  0 = every claim sweep with an expectation agrees; 1 = at least one disagrees; 2 = a body is missing.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ARTICLE_START = {"S421": 'class="article-info"', "S422": 'class="info-item-time"'}
ARTICLE_END = {"S421": "往期回顾", "S422": "wiki-foot-right"}
BODIES = {"S421": ".ufo/waves/round-57/sources/S421.html", "S422": ".ufo/waves/round-57/sources/S422.html"}
ENTRIES = {"S421": "corpus/knowledge/baidu-dead-link-types.md",
           "S422": "corpus/knowledge/baidu-spider3-dead-link-model.md"}
PAR = {"S421-discovery": ("S421", 63, 70),
       "S422-deadlink": ("S422", 28, 34),   # section incl. the label node 28
       "S422-dl-body": ("S422", 30, 34)}    # the paragraph under the label


# ------------------------------------------------------------------ extraction
def read(root: str, rel: str) -> str:
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return fh.read()


def block(text: str, sid: str) -> str:
    lo = text.find(ARTICLE_START[sid])
    if lo < 0:
        return ""
    hi = text.find(ARTICLE_END[sid], lo + 1)
    return text[lo:hi] if hi > lo else ""


def nodes(text: str, sid: str) -> list[str]:
    raw = block(text, sid)
    return re.findall(r">([^<>]+)(?=<)", re.sub(r"(?is)<(style|script)\b.*?</\1>", "<>", raw)) if raw else []


def count_nodes(ns: list[str], term: str) -> int:
    return sum(n.count(term) for n in ns)


def node_ids(ns: list[str], term: str) -> list[int]:
    return [i for i, n in enumerate(ns) if term in n]


def slice_text(ns: list[str], scope: str) -> str | None:
    if scope.startswith("NODE:"):
        i = int(scope[5:])
        return ns[i] if i < len(ns) else None
    if scope.startswith("SENT:"):
        marker = scope[5:]
        for n in ns:
            if marker in n:
                for sent in re.split(r"(?<=[。！？])", n):
                    if marker in sent:
                        return sent
        return None
    key = scope[4:] if scope.startswith("PAR:") else scope
    if key in PAR:
        _, lo, hi = PAR[key]
        return "\n".join(ns[lo:hi + 1])
    return None


def count(body: str, ns: list[str], sid: str, term: str, scope: str) -> int:
    if scope == "RAW":
        return body.count(term)
    if scope == "BLOCK":
        return block(body, sid).count(term)
    if scope == "TEXT":
        return count_nodes(ns, term)
    chunk = slice_text(ns, scope)
    return 0 if chunk is None else chunk.count(term)


# ------------------------------------------------------------------ claim table
# checks: (term, scope, expected) — expected None means "context only, not part of the verdict".
CLAIMS = [
    dict(id="S421-1", entry="S421", sid="S421",
         claim="the page does not describe either [discovery method] as status-code-only",
         checks=[("状态码", "PAR:S421-discovery", 0), ("页面状态", "PAR:S421-discovery", None),
                 ("状态码", "TEXT", 1)],
         note="页面状态 sits in the crawler-software sentence (node 70) and means 'analyse page status', "
              "not 'status-code-only'; 状态码 occurs once, in the content-dead-link paragraph (node 26)."),
    dict(id="S421-2", entry="S421", sid="S421",
         claim="states nothing about removing a path from internal links",
         checks=[("内链", "TEXT", 0), ("内部链接", "TEXT", 0), ("删除链接", "TEXT", 0),
                 ("移除链接", "TEXT", 0), ("删除", "TEXT", None), ("已删除", "TEXT", None)],
         note="删除 occurs 5x: 已删除 (node 24), site-redesign page deletion (47), resources needing deletion "
              "(87), and the FAQ 'may the tool delete all links under a directory' (126/130) answered 'only "
              "specific links that need deleting may be submitted' — none of these is internal-link removal."),
    dict(id="S421-3", entry="S421", sid="S421",
         claim="The page does not reconcile the two [404] statements",
         checks=[("矛盾", "RAW", None), ("200", "TEXT", 1), ("404", "TEXT", None)],
         note="interpretive: no sweep can settle 'reconcile'. Nearest evidence: no text node holds both 200 and "
              "404 in one sentence-of-record except node 26/27 (the impossibility sentence); 矛盾 occurs 0x."),
    dict(id="S421-4", entry="S421", sid="S421",
         claim="The page states no definition of a monitor or a link checker",
         checks=[("监控", "TEXT", 0), ("检查", "TEXT", 0), ("校验", "TEXT", 0), ("巡检", "TEXT", 0),
                 ("死链检测", "TEXT", 0), ("链接检查", "TEXT", 0), ("检测", "TEXT", None)],
         note="检测 occurs once (node 57: 百度蜘蛛会定期检测网站页面内容价值) — a crawler action, not a monitor "
              "definition; the claim survives on every spelling a reader would grep."),
    dict(id="S421-5", entry="S421", sid="S421",
         claim="no claim that any tool cannot see a content dead link",
         checks=[("看不到", "RAW", 0), ("无法发现", "RAW", 0), ("发现不了", "RAW", 0), ("检测不到", "RAW", 0),
                 ("无法", "TEXT", None)],
         note="无法 occurs 3x, all in other senses (nodes 13, 27, 35)."),
    dict(id="S421-6", entry="S421", sid="S421",
         claim="The page states the 1-2 week effect cycle of submissions",
         checks=[("1-2", "TEXT", 1), ("生效周期", "TEXT", 2)],
         note="affirmative neighbour of the negative claims: the entry's only unquoted page statement."),
    dict(id="S422-1", entry="S422", sid="S422",
         claim="404 and 状态码 occur zero times in the retained body",
         checks=[("404", "RAW", 0), ("状态码", "RAW", 0)],
         note="stated as a command in the entry."),
    dict(id="S422-2", entry="S422", sid="S422",
         claim="屏蔽 occurs once in the whole body, inside this label; the paragraph under it speaks about "
               "dead-link recognition and processing time only",
         checks=[("屏蔽", "RAW", 1), ("屏蔽", "NODE:28", 1), ("屏蔽", "PAR:S422-dl-body", 0)],
         note="stated as a command in the entry plus the undeveloped-second-half sentence."),
    dict(id="S422-3", entry="S422", sid="S422",
         claim="删除, 移除 and 下线 occur zero times in the retained body",
         checks=[("删除", "RAW", 0), ("移除", "RAW", 0), ("下线", "RAW", 0),
                 ("移出", "RAW", 0), ("清除", "RAW", 0), ("去除", "RAW", 0),
                 ("取消收录", "RAW", 0), ("清空", "RAW", 0)],
         note="stated as commands in the entry."),
    dict(id="S422-4", entry="S422", sid="S422",
         claim="the article block's only 索引 occurrences are the two in the index-display sentence",
         checks=[("索引", "TEXT", 2), ("索引", "NODE:22", 1), ("索引", "NODE:26", 0)],
         note="NODE:22 is the index-display sentence ('索引展现时效性提升，原来是'); NODE:26 holds the second "
              "article 索引 inside 搜索引擎 ('search engine'). The count 2 is right; the location is not."),
    dict(id="S422-5", entry="S422", sid="S422",
         claim="the only other mention of 协议死链 on the page is the preference quoted below",
         checks=[("协议死链", "RAW", 2), ("协议死链", "NODE:34", 1)],
         note="node 32 = recognition scope sentence, node 34 = the preference; no third mention."),
    dict(id="S422-6", entry="S422", sid="S422",
         claim="it does not restate the majority qualifier in this sentence",
         checks=[("大多数", "SENT:大约几天内", 0), ("大多数", "PAR:S422-dl-body", 1)],
         note="sentence-level absence is true, but the version-2 TEXT rule puts the few-days sentence and the "
              "recognition sentence in ONE node (32), so a node-level sweep returns 1 where the sentence returns 0."),
    dict(id="S422-7", entry="S422", sid="S422",
         claim="It states no rate, no percentage and no measurement for dead-link handling",
         checks=[("%", "PAR:S422-dl-body", 0), ("％", "RAW", 0), ("百分比", "RAW", 0), ("%", "TEXT", None)],
         note="all 7 text-node percentages sit in nodes 7/9/21/25/56 (fetching, index-building, submission), "
              "none in the dead-link paragraph 28-34."),
    dict(id="S422-8", entry="S422", sid="S422",
         claim="the paragraph names no report, no tool and no status",
         checks=[("报告", "PAR:S422-dl-body", 0), ("工具", "PAR:S422-dl-body", 0),
                 ("状态", "PAR:S422-dl-body", 0), ("平台", "PAR:S422-dl-body", None)],
         note="工具/报告/状态 are all 0 inside nodes 28-34; 站长平台 is named (1) and the entry itself calls it "
              "the submission channel, so 'no tool' holds only under that wording."),
    dict(id="S422-9", entry="S422", sid="S422",
         claim="The page does not say the platform submission became unnecessary",
         checks=[("无需", "RAW", 0), ("不需要", "RAW", 0), ("不必", "RAW", 0), ("不用", "RAW", 0)],
         note=""),
    dict(id="S422-10", entry="S422", sid="S422",
         claim="The page names all three kinds and defines none of them here",
         checks=[("定义", "RAW", 0), ("是指", "RAW", 0), ("指的是", "RAW", 0), ("即", "RAW", 0)],
         note=""),
    dict(id="S422-11", entry="S422", sid="S422",
         claim="It prints no status code and no HTTP term for any of the three kinds",
         checks=[("HTTP", "RAW", 0), ("状态", "RAW", 0), ("404", "RAW", 0), ("状态码", "RAW", 0)],
         note="this also covers 'the page states neither half of that reading' (the [INFERENCE] paragraph)."),
    dict(id="S422-12", entry="S422", sid="S422",
         claim="it does not say the other recognised kinds fail, are rejected, or go unhandled",
         checks=[("失败", "RAW", 0), ("拒绝", "RAW", 0), ("不处理", "RAW", 0),
                 ("无法识别", "RAW", 0), ("忽略", "RAW", 0)],
         note="preference section, node 34"),
    dict(id="S422-13", entry="S422", sid="S422",
         claim="the verb is 处理 (handle), not a removal from an index and not a deletion",
         checks=[("删除索引", "RAW", 0), ("从索引", "RAW", 0), ("移出", "RAW", 0), ("取消", "RAW", 0)],
         note="the removal reading is swept on top of S422-3's 删除/移除/下线"),
]

# ---------------------------------------------------- sweeps a skeptical reader adds
ADDED = [
    dict(id="A1", label="status codes other than 403/404/503/200 in either article"),
    dict(id="A2", label="the words 删除/移除/下线/索引 in S421"),
    dict(id="A3", label="robots in either article"),
    dict(id="A4", label="sitemap in S421's article"),
    dict(id="A5", label="English 'soft 404' wording in either article"),
]
CODE_RE = re.compile(r"(?<![0-9])[1-5][0-9]{2}(?![0-9])")  # ASCII-digit bounded: \b fails beside CJK
ROBOTS_RE = re.compile(r"(?i)robots")
SITEMAP_RE = re.compile(r"(?i)sitemap")
SOFT_RE = re.compile(r"(?i)soft[\s_-]?404|soft\s*error|soft\s*not[\s-]?found")


CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]")


def units(text: str) -> int:
    """Round-57 rule: one unit per CJK character, one per non-CJK whitespace token."""
    return len(CJK.findall(text)) + len([t for t in text.split() if not CJK.search(t)])


def quote_spans(entry: str) -> list[str]:
    out = []
    for line in entry.splitlines():
        if line.lstrip().startswith(">"):
            out.extend(re.findall(r'"([^"]+)"', line))
    return out


def stated_commands(entry: str) -> list[tuple[str, int]]:
    """`grep -o -F '<term>' ... -> <n>` as the entry prints it."""
    out = []
    for m in re.finditer(r"grep -o -F '([^']+)'", entry):
        tail = entry[m.end():m.end() + 220]
        r = re.search(r"->\s*(\d+)", tail)
        if r:
            out.append((m.group(1), int(r.group(1))))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 5)))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    bodies, entries, ns = {}, {}, {}
    for sid, rel in BODIES.items():
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            print(f"MISSING {p}", file=sys.stderr)
            return 2
        bodies[sid] = read(root, rel)
        ns[sid] = nodes(bodies[sid], sid)
    for sid, rel in ENTRIES.items():
        entries[sid] = read(root, rel)

    rows, failures = [], 0
    print("=" * 104)
    print("CLAIM SWEEPS — every 'does not say / zero / not described as' sentence in the two entries")
    print("=" * 104)
    for c in CLAIMS:
        print(f"\n{c['id']}  [{c['entry']} entry]  {c['claim']}")
        if c["note"]:
            print(f"    note: {c['note']}")
        bad = []
        for term, scope, expect in c["checks"]:
            n = count(bodies[c["sid"]], ns[c["sid"]], c["sid"], term, scope)
            exp = "ctx" if expect is None else str(expect)
            flag = ""
            if expect is not None and n != expect:
                flag = "  <-- MISMATCH"
                bad.append(term)
            print(f"    {term!r:14} {scope:18} count={n:<3} claimed={exp}{flag}")
            if expect is None:
                for i in node_ids(ns[c["sid"]], term)[:3]:
                    print(f"        node[{i}] {ns[c['sid']][i].strip()[:96]!r}")
        verdict = "DISAGREES" if bad else "agrees"
        if bad:
            failures += 1
        print(f"    -> {verdict}")
        rows.append({"id": c["id"], "entry": c["entry"], "claim": c["claim"], "verdict": verdict,
                     "mismatch": bad})

    print("\n" + "=" * 104)
    print("STATED-SWEEP AUDIT — negative page claims vs the `grep -o -F` command the entry prints for them")
    print("=" * 104)
    for ekey in ("S421", "S422"):
        stated = stated_commands(entries[ekey])
        neg_lines = [ln.strip() for ln in entries[ekey].splitlines()
                     if re.search(r"does not say|states no|zero times|not described as|occur zero|names no|"
                                  r"states nothing|prints no|occurrences", ln)]
        print(f"\n[{ekey} entry] {len(stated)} `grep -o -F ... -> n` commands printed; "
              f"{len(neg_lines)} negative-claim sentences")
        for term, n in stated:
            got = bodies[ekey].count(term)
            print(f"    printed: {term!r:20} -> {n:<3} recomputed RAW={got:<3}"
                  f"{'  <-- PRINTED VALUE WRONG' if got != n else ''}")
            if got != n:
                failures += 1
        if ekey == "S421":
            print("    NOTE: the S421 entry prints NO page-silence command for any negative page claim "
                  "(its only grep is the presence recheck '协议死链和内容死链' -> 1 and a span_tools check).")

    print("\n" + "=" * 104)
    print("ADDED SWEEPS — not stated by the entries; a skeptical reader would run them")
    print("=" * 104)
    for a in ADDED:
        print(f"\n{a['id']}  {a['label']}")
        for sid in ("S421", "S422"):
            text, nn = bodies[sid], ns[sid]
            if a["id"] == "A1":
                raw = CODE_RE.findall(text)
                blk = CODE_RE.findall(block(text, sid))
                print(f"    {sid}: RAW={len(raw)} BLOCK={len(blk)} distinct_raw={sorted(set(raw))}")
                for i, n in enumerate(nn):
                    for m in CODE_RE.finditer(n):
                        print(f"        TEXT node[{i}] code={m.group(0)!r} in {n.strip()[:84]!r}")
            elif a["id"] == "A2" and sid == "S421":
                for term in ("删除", "移除", "下线", "索引"):
                    print(f"    S421 {term!r:8} RAW={text.count(term)} BLOCK={block(text, sid).count(term)} "
                          f"TEXT={count_nodes(nn, term)} nodes={node_ids(nn, term)}")
                for i in node_ids(nn, "索引"):
                    print(f"        node[{i}] {nn[i].strip()[:96]!r}")
            elif a["id"] == "A3":
                rh = ROBOTS_RE.findall(text)
                print(f"    {sid}: RAW={len(rh)} BLOCK={len(ROBOTS_RE.findall(block(text, sid)))} "
                      f"TEXT={count_nodes(nn, 'robots') + count_nodes(nn, 'Robots')} forms={sorted(set(x.lower() for x in rh))}")
                for m in ROBOTS_RE.finditer(text):
                    print(f"        raw ctx: {text[max(0, m.start() - 45):m.start() + 35]!r}")
                for i, n in enumerate(nn):
                    if ROBOTS_RE.search(n):
                        print(f"        node[{i}] {n.strip()[:96]!r}")
            elif a["id"] == "A4" and sid == "S421":
                sh = SITEMAP_RE.findall(text)
                print(f"    S421: RAW={len(sh)} BLOCK={len(SITEMAP_RE.findall(block(text, sid)))} "
                      f"TEXT={len([x for n in nn for x in SITEMAP_RE.findall(n)])}")
                for i, n in enumerate(nn):
                    if SITEMAP_RE.search(n):
                        print(f"        node[{i}] {n.strip()[:96]!r}")
            elif a["id"] == "A5":
                print(f"    {sid}: RAW={len(SOFT_RE.findall(text))} "
                      f"TEXT={len([x for n in nn for x in SOFT_RE.findall(n)])} "
                      f"plain_soft={len(re.findall(r'(?i)soft', text))}")
                print(f"        English words in TEXT: {sorted(set(re.findall(r'[A-Za-z]{3,}', ' '.join(nn))))[:18]}")

    print("\n" + "=" * 104)
    print("QUOTE-CLASS SWEEP — 'occurs once in that body and in no other retained body' (S422 entry)")
    print("=" * 104)
    qrows = []
    for ekey in ("S422", "S421"):
        spans = quote_spans(entries[ekey])
        print(f"\n[{ekey} entry] {len(spans)} quoted spans; max units={max(units(x) for x in spans)} "
              f"max chars={max(len(x) for x in spans)}")
        for span in spans:
            if span in bodies["S422"]:
                owner, c422, c421 = "S422", bodies["S422"].count(span), bodies["S421"].count(span)
                tx = count_nodes(ns["S422"], span)
                raw_i = bodies["S422"].find(span)
                crosses = bool(re.search(r"<span[^>]*>", bodies["S422"][raw_i:raw_i + len(span)]))
                print(f"    {span!r:50} S422={c422} S421={c421} TEXT422={tx} units={units(span)} "
                      f"chars={len(span)} crosses_tag={crosses}")
                qrows.append({"entry": ekey, "span": span, "S422": c422, "S421": c421, "TEXT422": tx})
            elif span in bodies["S421"]:
                print(f"    {span!r:50} S421={bodies['S421'].count(span)} S422=0 TEXT421="
                      f"{count_nodes(ns['S421'], span)}")
            else:
                print(f"    {span!r:50} in neither retained body (cross-source quote: S419/S420 class) — out of scope")

    if args.json:
        print(json.dumps({"claims": rows, "quotes": qrows}, ensure_ascii=False, indent=1))
    print(f"\nfailures={failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
