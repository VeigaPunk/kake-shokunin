#!/usr/bin/env python3
"""ExecSpanTools / round-57 W1 / claim C3: structural characterisation of the two retained Baidu bodies.

Read-only. Reads sources/S421.html and sources/S422.html byte-exact (UTF-8 strict, no newline translation),
replicates c57_quote_truth.content_window (min offset of the two article-container markers -> first
`class="footer"`), and prints:

  1. byte / decoded-char lengths, line count, BOM;
  2. every marker offset (char and byte) for the article containers, footer, <h1>/<h2>/<h3>/<strong>, <title>;
  3. the exact <title> inner string (repr, so spacing is visible) and the `发布日期：` line;
  4. the article block bounds, its stripped text size, and whether the page's main prose lies inside it
     (prose = text nodes with >= 20 CJK chars; anything outside is listed);
  5. the pre-window (header / nav / breadcrumb) text and whether it would fall inside a looser window,
     plus how many of the helper's own candidate spans occur before the window;
  6. every heading inside the article block with char/byte offset, unit count, page-wide occurrence count and
     whether the stripped heading text is a raw substring (inline <span> wrappers split most of them, which
     matters because the counter's row-anchor test is `anchor in body`), plus the 『…』 pseudo-headings S422 uses;
  7. occurrence counts of the two staged recheck strings in BOTH bodies, their unit/char counts against the
     25-unit / 40-character ceilings, and whether their occurrence is inside the article block.

  python3 -B inspect.py
"""
import re
import subprocess
import sys

SRC = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-57/sources"
TOOLS = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-57/span_tools.py"
IDS = ("S421", "S422")
ARTICLE_START = {"S421": 'class="article-info"', "S422": 'class="zz_dldes_content'}
ARTICLE_END = 'class="footer"'
STAGED = (
    "死链一般是指页面已经无效，无法对用户提供任何有价值信息的页面。",
    "启用了全新的死链识别模型，能识别协议死链，以及大多数内容死链、跳转死链等低质网页",
)
# structural markers used only to label sub-regions of the window (not by the counter)
SUBREGION = {
    "S421": ('往期回顾', 'class="list-right"', 'class="recommand-news"', 'class="pager'),
    "S422": ('id="wiki-foot-right"', 'class="clr"'),
}
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]")
TAGS = re.compile(r"<[^>]+>")
SCRIPT_STYLE = re.compile(r"<script\b.*?</script\s*>|<style\b.*?</style\s*>", re.S)
PUNCT_EDGE = "、，：；。？！）」』“"


def units(t):
    """span_tools / counter unit rule: one unit per CJK char, one per non-CJK whitespace token."""
    return len(CJK.findall(t)) + len([w for w in t.split() if not CJK.search(w)])


class Page:
    def __init__(self, sid):
        self.sid = sid
        self.raw = open(f"{SRC}/{sid}.html", "rb").read()
        self.text = self.raw.decode("utf-8")          # strict: raises on malformed bytes
        self.boff = [0] * (len(self.text) + 1)
        for i, ch in enumerate(self.text):
            self.boff[i + 1] = self.boff[i] + len(ch.encode("utf-8"))

    def byte(self, i):
        return self.boff[i]

    def find_all(self, needle):
        out, i = [], self.text.find(needle)
        while i >= 0:
            out.append(i)
            i = self.text.find(needle, i + 1)
        return out

    def window(self):
        """Exact replica of c57_quote_truth.content_window()."""
        starts = [self.text.find(m) for m in ARTICLE_START.values() if self.text.find(m) >= 0]
        hi = self.text.find(ARTICLE_END)
        if not starts or hi < 0:
            return None
        lo = min(starts)
        return (lo, hi) if lo < hi else None

    def strip(self, seg, drop_script_style=False):
        if drop_script_style:
            seg = SCRIPT_STYLE.sub(" ", seg)
        return TAGS.sub("", seg)

    def prose(self, minimum_cjk=20):
        """Text nodes with >= minimum_cjk CJK chars: article prose, as opposed to nav labels."""
        out = []
        for m in re.finditer(r"[^<>]+", self.text):
            t = m.group(0)
            if len(CJK.findall(t)) >= minimum_cjk:
                out.append((m.start(), t.strip()))
        return out


def marker_table(p):
    print("-- markers: count and char/byte offsets --")
    for m in (ARTICLE_START["S421"], ARTICLE_START["S422"], ARTICLE_END,
              "<h1", "<h2", "<h3", "<strong", "<title>"):
        hits = p.find_all(m)
        print(f"  {m:<26} n={len(hits)}  " + (" ".join(f"{i}/{p.byte(i)}" for i in hits) or "-"))
    print(f"  {'发布日期':<26} n={len(p.find_all('发布日期'))}  "
          + " ".join(f"{i}/{p.byte(i)}" for i in p.find_all("发布日期")))


def title_and_date(p):
    m = re.search(r"<title[^>]*>(.*?)</title\s*>", p.text, re.S)
    tag_at = p.text.find("<title")
    inner = m.group(1)
    print(f"  raw     : {m.group(0)!r}")
    print(f"  inner   : {inner!r}")
    print(f"  measures: {len(inner)} chars, {units(inner)} units, "
          f"ascii-space={inner.count(' ')}, double-space={'  ' in inner}, "
          f"tab={chr(9) in inner}, nbsp-entity={'&nbsp;' in inner}")
    print(f"  offsets : <title> char {tag_at} / byte {p.byte(tag_at)}; "
          f"inner char {m.start(1)} / byte {p.byte(m.start(1))}")
    w = p.window()
    for i in p.find_all("发布日期"):
        lo, hi = max(0, i - 70), min(len(p.text), i + 70)
        print(f"  发布日期 char {i} / byte {p.byte(i)}: …{p.text[lo:hi]!r}…")
        near = re.search(r"\d{4}-\d{2}-\d{2}", p.text[i:i + 200])
        date = near.group(0) if near else None
        line = f"发布日期：{date}" if date else None
        print(f"    date={date} at char {i + near.start() if near else None} / "
              f"byte {p.byte(i + near.start()) if near else None}; "
              f"line {line!r} in body={line in p.text if line else None} "
              f"in_window={bool(w) and w[0] <= i < w[1] if w else None}")
    if not p.find_all("发布日期"):
        print("  发布日期: ABSENT")


def window_check(p):
    w = p.window()
    if w is None:
        print("  window: None (no article block)")
        return None
    lo, hi = w
    seg = p.text[lo:hi]
    prose = p.prose()
    inside = [r for r in prose if lo <= r[0] < hi]
    outside = [r for r in prose if not (lo <= r[0] < hi)]
    print(f"  window char [{lo}, {hi})  byte [{p.byte(lo)}, {p.byte(hi)})  "
          f"= {hi - lo} chars / {p.byte(hi) - p.byte(lo)} bytes")
    print(f"  window text stripped = {len(p.strip(seg))} chars; "
          f"with <script>/<style> removed = {len(p.strip(seg, True))} chars "
          f"(script/style chars inside window = {len(p.strip(seg)) - len(p.strip(seg, True))})")
    print(f"  whole page stripped = {len(p.strip(p.text, True))} chars of {len(p.text)} decoded chars")
    print(f"  prose nodes (>=20 CJK): page={len(prose)} inside={len(inside)} outside={len(outside)}")
    for off, t in outside:
        print(f"    OUTSIDE char {off} / byte {p.byte(off)}: {t[:80]!r}")
    if inside:
        f, l = inside[0], inside[-1]
        print(f"  first prose inside char {f[0]} / byte {p.byte(f[0])}: {f[1][:60]!r}")
        print(f"  last  prose inside char {l[0]} / byte {p.byte(l[0])}: {l[1][:60]!r}")
    for m in SUBREGION[p.sid]:
        hits = p.find_all(m)
        print(f"  subregion marker {m!r}: n={len(hits)} "
              + " ".join(f"{i}/{p.byte(i)}{'(in)' if lo <= i < hi else '(out)'}" for i in hits))
    return w


def looser(p, w):
    lo, hi = w
    pre = p.text[:lo]
    pre_text = re.sub(r"\s+", " ", p.strip(pre, True)).strip()
    print(f"  pre-window region char [0, {lo}) = {len(pre)} chars / {p.byte(lo)} bytes; "
          f"stripped text {len(pre_text)} chars")
    print(f"  pre-window text: {pre_text[:700]!r}")
    proc = subprocess.run([sys.executable, "-B", TOOLS, "spans", p.sid],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    spans = []
    for line in proc.stdout.splitlines():
        m = re.match(r"\s*(\d+)u\s+(.*)$", line)
        if m:
            spans.append((int(m.group(1)), m.group(2)))
    dup = [(u, s, p.text.count(s), pre.count(s)) for u, s in spans if pre.count(s)]
    print(f"  helper spans for {p.sid}: {len(spans)}; occurring before the window: {len(dup)}")
    for u, s, n_all, n_pre in dup:
        print(f"    {u}u page={n_all} pre={n_pre}  {s}")
    tm = re.search(r"<title[^>]*>(.*?)</title\s*>", p.text, re.S)
    print(f"  <title> text before window? {tm.group(1) in pre}; "
          f"发布日期 before window? {'发布日期' in pre}")
    for label, lo2 in (("start-of-document", 0), ("<body>", p.text.find("<body")),
                       ("first <div", p.text.find("<div"))):
        if lo2 < 0:
            print(f"  looser[{label}]: marker absent")
            continue
        seg = p.strip(p.text[lo2:hi], True)
        print(f"  looser[{label}] from char {lo2}: stripped window text {len(seg)} chars "
              f"(vs {len(p.strip(p.text[lo:hi], True))} for the article-only window)")
    # where does each helper span land: article prose, recap/recommendation block, or outside prose
    article_end = None
    for off, t in p.prose():
        if lo <= off < hi:
            article_end = off + len(t)
    sub = [p.text.find(m) for m in SUBREGION[p.sid] if p.text.find(m) >= 0]
    cut = min([s for s in sub if lo <= s < hi], default=hi)
    buckets = {"article-prose": 0, "after-prose": 0, "fragment": 0}
    frag, after = [], []
    for u, s in spans:
        first = p.text.find(s)
        if first >= cut:
            buckets["after-prose"] += 1
            after.append((u, s))
        elif s[0] in PUNCT_EDGE or s[-1] in "、，：；":
            buckets["fragment"] += 1
            frag.append((u, s))
        else:
            buckets["article-prose"] += 1
    print(f"  span placement (article prose ends {article_end}, later block starts {cut}): {buckets}")
    for u, s in after:
        print(f"    AFTER-PROSE {u}u  {s}")
    for u, s in frag:
        print(f"    FRAGMENT   {u}u  {s}")


def headings(p, w):
    lo, hi = w
    rows = []
    for m in re.finditer(r"<(h1|h2|h3|strong)\b([^>]*)>(.*?)</\1\s*>", p.text, re.S | re.I):
        tag, attrs, inner = m.group(1).lower(), m.group(2).strip(), m.group(3)
        txt = re.sub(r"\s+", " ", p.strip(inner)).strip()
        inside = lo <= m.start() < hi
        n = p.text.count(txt) if txt else 0
        rows.append((tag, m.start(), p.byte(m.start()), inside, txt, units(txt), n,
                     txt in p.text, attrs[:46], inner[:60]))
    bare = [(t, i) for t in ("<h1", "<h2", "<h3", "<strong")
            for i in p.find_all(t) if not any(r[0] == t[1:] and r[1] == i for r in rows)]
    print(f"  closed heading elements={len(rows)}  unmatched openers={len(bare)}"
          + (f" {[(t, i, p.byte(i), lo <= i < hi) for t, i in bare]}" if bare else ""))
    print(f"  {'tag':<6}{'char':>7}{'byte':>8}{'in':>5}{'units':>7}{'pageN':>7}{'raw':>6}  text | attrs | raw-inner")
    for tag, c, b, ins, txt, u, n, raw_ok, attrs, inner in rows:
        print(f"  {tag:<6}{c:>7}{b:>8}{'yes' if ins else 'NO':>5}{u:>7}{n:>7}{'yes' if raw_ok else 'NO':>6}"
              f"  {txt!r} | {attrs!r} | {inner!r}")
    br = []
    for m in re.finditer(r"『[^』]{1,80}』", p.text):
        if lo <= m.start() < hi:
            br.append((m.start(), p.byte(m.start()), m.group(0), units(m.group(0)),
                       p.text.count(m.group(0))))
    print(f"  『…』 pseudo-headings inside window: {len(br)}")
    for c, b, txt, u, n in br:
        print(f"    char {c} / byte {b}  {u}u pageN={n}  {txt}")


def staged(p, others):
    print("-- staged recheck strings --")
    w = p.window()
    for s in STAGED:
        own = p.find_all(s)
        print(f"  {s}")
        print(f"    len={len(s)} chars units={units(s)} "
              f"units<=25={units(s) <= 25} chars<=40={len(s) <= 40}")
        print(f"    own({p.sid}): n={len(own)} offsets(char/byte)="
              f"{[f'{i}/{p.byte(i)}' for i in own] or '-'} "
              f"in_window={[bool(w) and w[0] <= i < w[1] for i in own]}")
        for sid, ot in others:
            print(f"    other({sid}): n={ot.count(s)} raw_substring={s in ot}")
        print(f"    entity-in-string={'&' in s}; curly-quote-in-string={any(ch in s for ch in '“”‘’')}")


def main():
    pages = {sid: Page(sid) for sid in IDS}
    for sid, p in pages.items():
        print(f"===== {sid} =====")
        print(f"  file {SRC}/{sid}.html")
        print(f"  bytes={len(p.raw)} decoded_chars={len(p.text)} lines={p.text.count(chr(10)) + 1} "
              f"BOM={p.raw[:3] == b'\\xef\\xbb\\xbf'} trailing_nl={p.raw.endswith(b'\\n')}")
        marker_table(p)
        print("-- title / publication date --")
        title_and_date(p)
        print("-- article block (content_window) --")
        w = window_check(p)
        print("-- pre-window text and looser windows --")
        if w:
            looser(p, w)
        print("-- headings inside the article block --")
        if w:
            headings(p, w)
        staged(p, [(k, q.text) for k, q in pages.items() if k != sid])
        print()


if __name__ == "__main__":
    main()
