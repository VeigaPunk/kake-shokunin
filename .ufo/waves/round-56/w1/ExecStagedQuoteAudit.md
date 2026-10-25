# ExecStagedQuoteAudit

Scope: the three staged entries under `/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/`
(read-only; nothing there was written), tested against the retained round-56 bodies in
`.ufo/waves/round-56/sources/`. Mapping used (contract renumber map): link-target -> S367 (held row),
deleted-url (staged S375) -> S419, soft-404 (staged S376) -> S420.

Method: one python script, run twice (verbose then compact form) with identical measured output; it reuses
`span_tools.py`'s `units()`, `window()` and `in_content()` semantics, extracts every ASCII double-quoted span
of each entry, the single-quoted argument of the `recheck:` line's `grep -F -c`, and the `source:` section
text, and runs the real `grep -F -c` binary on the retained body per recheck string. `page-unique` = occurs
once in its own body and in neither of the other two adopted bodies. `norm` is diagnostic only: the four
entities the bodies carry (`&quot; &lt; &gt; &amp;`) decoded, all whitespace dropped.

Body integrity: sha256 of all three bodies matches `sources/receipts.json` (S367 `0188de9d…`, S419
`6172d5d1…`, S420 `a860d4f3…`), byte counts 8051 / 7428 / 7332 as recorded.

## SCRIPT:

```python
#!/usr/bin/env python3
# ExecStagedQuoteAudit (round-56 W1, read-only): staged entries vs retained bodies.
import re, subprocess
SRC = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-56/sources"
KNW = "/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge"
IDS = ("S367", "S419", "S420")
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]")
PAIRS = (("yahoo-japan-link-target-crawl-restriction.md", "S367"),
         ("yahoo-japan-deleted-url-recrawl.md", "S419"),
         ("yahoo-japan-soft-404-recrawl.md", "S420"))

def units(t):                      # the counter's rule: 1 per CJK char, 1 per non-CJK whitespace token
    return len(CJK.findall(t)) + len([w for w in t.split() if not CJK.search(w)])

def body(sid):
    return open(f"{SRC}/{sid}.html", encoding="utf-8", newline="").read()

def window(t):                     # first <h2> .. 個別リンクURL widget
    lo, hi, h2 = t.find("更新日"), t.find("個別リンクURL"), t.find("<h2")
    return (h2, hi) if min(lo, hi, h2) >= 0 and hi > lo else None

def in_content(t, s):
    w = window(t); i = t.find(s)
    while i >= 0:
        if w[0] <= i < w[1]: return True
        i = t.find(s, i + 1)
    return False

def norm(s):                       # diagnostic only: decode the 4 entities the bodies carry, drop whitespace
    for a, b in (("&quot;", '"'), ("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&")): s = s.replace(a, b)
    return re.sub(r"\s+", "", s)

def grep_count(pat, path):
    p = subprocess.run(["grep", "-F", "-c", "--", pat, path], capture_output=True, text=True)
    return p.stdout.strip(), p.returncode

rows = []
for fname, sid in PAIRS:
    md, t = open(f"{KNW}/{fname}", encoding="utf-8").read(), body(sid)
    others = [body(k) for k in IDS if k != sid]
    print(f"\n=== {fname} -> body {sid} ({len(t)} chars)")
    spans = [m.group(1) for m in re.finditer(r'"([^"]*)"', md)]
    print(f"double-quoted spans found: {len(spans)} (all listed; >=2u is the audited set)")
    for s in spans:
        u, raw, w = units(s), s in t, window(t)
        r = {"file": fname, "body": sid, "span": s, "units": u, "raw": raw,
             "in_article": in_content(t, s) if raw else False, "count": t.count(s),
             "count_article": t[w[0]:w[1]].count(s), "over25": u > 25,
             "unique": raw and t.count(s) == 1 and not any(s in o for o in others),
             "norm_hit": norm(s) in norm(t)}
        rows.append(r)
        print(f"  Q units={u:<3} raw={'yes' if raw else 'no ':<3} in_article={'yes' if r['in_article'] else 'no ':<3}"
              f" count={r['count']} (article {r['count_article']}) unique={'yes' if r['unique'] else 'no ':<3}"
              f" over25={'yes' if r['over25'] else 'no ':<3} norm_hit={'yes' if r['norm_hit'] else 'no'} | {s!r}")
    rec = [l for l in md.splitlines() if l.startswith("recheck:")][0]
    m = re.search(r"grep -F -c '([^']*)'", rec)
    pat = m.group(1)
    cnt, rc = grep_count(pat, f"{SRC}/{sid}.html")
    print(f"  RECHECK grep -F -c units={units(pat)} raw={'yes' if pat in t else 'no'} count={cnt} rc={rc}"
          f" over25={'yes' if units(pat) > 25 else 'no'} | {pat!r}")
    src = [l for l in md.splitlines() if l.startswith("source:")][0]
    sect = src.split("§ ", 1)[1].split(" (更新日", 1)[0]
    print(f"  SOURCE label section: {sect!r}")
    print(f"    raw count={t.count(sect)}  whitespace-stripped count={norm(t).count(norm(sect))}")
    for seg in [x for x in sect.split(" → ") if x.strip()]:
        print(f"    segment {seg!r}: raw={t.count(seg)} norm={norm(t).count(norm(seg))}")
    print(f"    url {re.search(r'(https?://\S+)', src).group(1)} in body={'yes' if re.search(r'(https?://\S+)', src).group(1) in t else 'no'}")

aud = [r for r in rows if r["units"] >= 2]
print("\n=== SUMMARY")
print(f"spans_total={len(rows)} spans_audited(>=2u)={len(aud)} over25={sum(r['over25'] for r in aud)}"
      f" non_substring={sum(not r['raw'] for r in aud)} not_in_article={sum(r['raw'] and not r['in_article'] for r in aud)}"
      f" not_page_unique={sum(not r['unique'] for r in aud)}")
for r in aud:
    if r["over25"] or not r["raw"]:
        print(f"  FLAG {r['body']} units={r['units']} over25={r['over25']} raw={r['raw']} | {r['span']!r}")
```

## RESULTS:

Measured output (compact run, rc=0; the earlier verbose run printed the same numbers):

| body | kind | span | units | raw | in article | page-unique | over 25 |
|---|---|---|---|---|---|---|---|
| S367 | quote | `"X-Robots-Tag: NOFOLLOW"` | 2 | yes (count 1, article 1) | yes (offset 3266 in window 2499..3348, under `<h3>サーバーで設定する方法</h3>` at 3194) | yes | no |
| S367 | quote | `"robots"` (1st) | 1 | yes (count 7, article 2) | yes | no | no |
| S367 | quote | `"index,nofollow"` | 1 | yes (count 2, article 2) | yes | no | no |
| S367 | quote | `"robots"` (2nd) | 1 | yes (count 7, article 2) | yes | no | no |
| S367 | quote | `"noindex,nofollow"` | 1 | yes (count 1, article 1) | yes | yes | no |
| S419 | quote | `"クローラーは削除されたウェブページと認識できず、そのウェブページを巡回し続ける可能性があります"` | **46** | yes (count 1, article 1) | yes (first `<p>` under `<h2>削除したウェブページが巡回され続ける</h2>`) | yes | **yes** |
| S420 | quote | `"サーバーが「HTTP 404 Not Found」のステータスを返すように設定を行ってください"` | **29** | yes (count 1, article 1) | yes (first `<p>` under `<h2>存在しないウェブページが巡回される</h2>`) | yes | **yes** |

The five 1-unit spans are inside the backticked `<meta name="robots" content="…">` examples of the S367
entry; they are below the 2-unit floor and are listed for completeness, not audited.

Recheck `grep -F -c` run against the retained body:

| body | recheck pattern | units | raw substring | grep -F -c | rc |
|---|---|---|---|---|---|
| S367 | `X-Robots-Tag: NOFOLLOW` | 2 | yes | 1 | 0 |
| S419 | `クローラーは削除されたウェブページと認識できず、…可能性があります` (full staged string) | 46 | yes | 1 | 0 |
| S420 | `サーバーが「HTTP 404 Not Found」のステータスを返すように設定を行ってください` | 29 | yes | 1 | 0 |

`source:` label section text against the body:

| body | label section text | raw count | whitespace-stripped count | segments |
|---|---|---|---|---|
| S367 | `リンク先のウェブページの巡回制限 ― ウェブページ内やサーバーでの設定 → サーバーで設定する方法` | **0** | **0** | h2 segment raw 0 / norm 3; `サーバーで設定する方法` raw 1 |
| S419 | `削除したウェブページが巡回され続ける` | 3 | 3 | title, `<h2>`, category `<strong>` |
| S420 | `存在しないウェブページが巡回される` | 3 | 3 | title, `<h2>`, category `<strong>` |

S367 label detail: the body writes `巡回制限` + U+3000 + `―` (title 749, `<h2>` 2503, category `<strong>` 4324),
the staged label writes U+0020 + U+2015 + U+0020 and appends `→ サーバーで設定する方法`, a composite the body
does not carry contiguously (`→` occurs 0 times); hence 0 raw and 0 whitespace-stripped hits. The page's own h2
matches 3x with whitespace dropped, and the sub-heading `サーバーで設定する方法` is `<h3>` at 3194, once. Each
`source:` URL occurs in its body (yes, yes, yes).

## SUMMARY:

- Spans: 7 ASCII double-quoted spans total, 3 at or above the 2-unit floor (S367 1, S419 1, S420 1).
- Over-ceiling: 2 of 3 audited spans exceed 25 units (S419 46 units = 46 CJK chars; S420 29 units = 27 CJK
  chars + tokens `404`, `Not`). Both are quote-true and page-unique, but as written they violate the frozen
  contract's "every quoted entry span is <= 25 units" and would fail C2's ceiling condition until re-cut.
- Non-substring: 0 of 3 audited spans (0 of 7 spans overall). Every quote is a raw substring of its retained
  body, HTML entities as written; 0 spans fall outside the article block.
- Labels with 0 hits: 1 — the S367 label (0 raw, 0 whitespace-stripped); the two new-row labels hit 3x raw.
  The S367 miss is a formatting/join artifact (U+3000 vs U+0020 around U+2015, plus a `→` composite).
- Recheck: all three staged `grep -F -c` strings are raw substrings of their body and each counts 1, rc 0. The
  S419 and S420 patterns are 46 and 29 units, but they are backticked grep patterns, not quoted entry spans,
  so no ceiling claim is made against them.
- Provenance observations (not quote defects): the staged `source:` lines still carry staged ids S375 / S376
  and `fetched 2026-10-24`, whereas `receipts.json` records S419 / S420 fetched 2026-10-25T22:02:4xZ, so the
  labels need re-cutting. The S367 entry quotes 2 units, so round-53's 31-unit S367 quote is not carried.
- Unrun: no network fetch, no live-URL recheck, no crawl observation — the audit is body-only by assignment.

VERDICT: 3 audited quotes are all raw, in-article and page-unique, but 2 exceed the 25-unit ceiling (S419 46u, S420 29u) and the S367 `source:` label has 0 raw hits (U+3000/`→` formatting) — the staged package is not landable as written.
