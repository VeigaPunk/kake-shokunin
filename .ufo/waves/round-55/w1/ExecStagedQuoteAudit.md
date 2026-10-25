# ExecStagedQuoteAudit

Round-55 W1, lane `kake-shokunin`, base `fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`, round date 2026-10-25.
Read-only audit of the three staged entries under
`/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/` against the retained bodies in
`.ufo/waves/round-55/sources/`. Only this report was written; no shokuknow, fleet, lane-jj or lane-index
state was touched.

Body selection is by the staged entry's own `source:` URL, not its claimed row id (the basics entry
claims `S380`, whose URL `002885.php` is retained as `S418.html` per the contract renumber map):
`002849.php` -> `S372.html`, `002850.php` -> `S373.html`, `002885.php` -> `S418.html`.

## SCRIPT:

```python
import re, subprocess

KN  = "/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge"
SRC = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-55/sources"
FILES = ["yahoo-japan-robots-txt-refusal-rules.md",
         "yahoo-japan-robots-pattern-syntax.md",
         "yahoo-japan-robots-txt-basics.md"]
URL2BODY = {"002849.php": "S372.html", "002850.php": "S373.html", "002885.php": "S418.html"}

CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
def units_counter(t):            # lane counter rule: c55_quote_truth.py:87,137-139
    return len(CJK_RE.findall(t)) + len([x for x in t.split() if not CJK_RE.search(x)])

def is_cjk(ch):                  # strict rule: kana/kanji + CJK punct + fullwidth forms
    o = ord(ch)
    return (0x3000 <= o <= 0x303F or 0x3040 <= o <= 0x30FF or 0x3400 <= o <= 0x4DBF
            or 0x4E00 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF or 0xFF00 <= o <= 0xFFEF)
def units_strict(s):
    n, buf = 0, ""
    for ch in s:
        if is_cjk(ch):
            if buf: n += 1
            buf = ""; n += 1
        elif ch.isspace():
            if buf: n += 1
            buf = ""
        else:
            buf += ch
    return n + (1 if buf else 0)

rows = []
for fn in FILES:
    text = open(f"{KN}/{fn}", encoding="utf-8").read()
    bn = URL2BODY[re.search(r"archives/(\d{6}\.php)", text).group(1)]
    body = open(f"{SRC}/{bn}", encoding="utf-8").read()
    q = re.findall(r'"([^"\n]*)"', text)[0]
    g = re.search(r"grep -F -c '([^']*)'", text).group(1)
    rc = subprocess.run(["grep", "-F", "-c", g, f"{SRC}/{bn}"], capture_output=True, text=True)
    rows += [("quote", fn, bn, q, body, None),
             ("recheck-grep", fn, bn, g, body, int(rc.stdout.strip() or 0))]

print(f"{'entry':40s} {'kind':12s} {'body':9s} {'u_cnt':5s} {'u_str':5s} {'substr':6s} {'>25':4s} {'grep -F -c':10s}")
for kind, fn, bn, s, body, gc in rows:
    uc, us = units_counter(s), units_strict(s)
    print(f"{fn[:40]:40s} {kind:12s} {bn:9s} {uc:<5d} {us:<5d} "
          f"{'yes' if s in body else 'NO':6s} {'YES' if min(uc, us) > 25 else 'no':4s} {str(gc) if gc is not None else '-':10s}")

qs = [r for r in rows if r[0] == "quote"]; gs = [r for r in rows if r[0] == "recheck-grep"]
print()
print("SUMMARY spans=%d (quotes=%d recheck_greps=%d) over_25_units=%d non_substring=%d grep_nonzero=%d" % (
    len(rows), len(qs), len(gs),
    sum(1 for r in rows if min(units_counter(r[3]), units_strict(r[3])) > 25),
    sum(1 for r in rows if r[3] not in r[4]),
    sum(1 for r in gs if (r[5] or 0) < 1)))
```

That run's own summary line, verbatim:
`SUMMARY spans=6 (quotes=3 recheck_greps=3) over_25_units=6 non_substring=0 grep_nonzero=0`

Two unit readings are reported: `u_cnt` = the lane counter's `CJK_RE` (kana/kanji only,
`c55_quote_truth.py:87`), `u_str` = the contract's wider rule with CJK punctuation and fullwidth forms
counted too. Every span exceeds 25 under both, so the verdict does not depend on the reading chosen.

Extraction completeness: each staged file holds exactly two ASCII `"` characters (one paired span) and
zero typographic quotes, so the spans below are the complete double-quoted population; each file's
`recheck:` `grep -F` string is byte-equal to its blockquote (`quote==grep=True`).

## RESULTS:

| # | entry | kind | body | units (cnt/str) | raw substring | > 25 units | staged `grep -F -c` |
|---|---|---|---|---|---|---|---|
| Q1 | refusal-rules | quoted span | S372.html | 48 / 58 | yes | **YES** | – |
| G1 | refusal-rules | `recheck` grep -F | S372.html | 48 / 58 | yes | **YES** | 1 (rc 0) |
| Q2 | pattern-syntax | quoted span | S373.html | 41 / 45 | yes | **YES** | – |
| G2 | pattern-syntax | `recheck` grep -F | S373.html | 41 / 45 | yes | **YES** | 1 (rc 0) |
| Q3 | txt-basics | quoted span | S418.html | 46 / 50 | yes | **YES** | – |
| G3 | txt-basics | `recheck` grep -F | S418.html | 46 / 50 | yes | **YES** | 1 (rc 0) |

Spans, verbatim (ASCII double quotes, each a raw substring of the named body):

- Q1/G1 -> `S372.html`, § 大文字と小文字の区別:
  "Disallow（拒否）、Allow（許可）のあとに記述されたディレクトリ名は、大文字と小文字の違いがあった場合、別のものとして扱います。"
- Q2/G2 -> `S373.html`, § 「$」記号:
  "クローラーはプリフィクス（接頭辞）として扱い、記述された文字列を含むURLがすべてマッチします"
- Q3/G3 -> `S418.html`:
  "クローラーによる巡回の際は、まずサイトのルートディレクトリ（サイトの一番上の階層）にあるrobots.txtを探します"

The three `recheck` grep strings were run as real `grep -F -c` against the retained body file: each
returns `1`, exit 0 — the recheck command as written would pass against the retained bodies. Byte-level
containment (`s.encode() in body.encode()`) is also true for all three, so no decode/entity artefact.

## SUMMARY:

- Spans audited: **6** (3 double-quoted entry spans of >= 6 units + 3 `recheck` `grep -F` strings).
- Over the 25-unit ceiling: **6 of 6** (48/58, 48/58, 41/45, 41/45, 46/50, 46/50 under the two readings).
- Non-substring (fabricated/paraphrased): **0 of 6** — all six are raw substrings of the retained body.
- `recheck` greps with a zero count: **0 of 3**; all three count 1, exit 0.

Consequence for the frozen predicate: the staged entries are quote-true but over-ceiling. Counter C5
(`c55_quote_truth.py` docstring) requires every double-quoted span of 6+ units below an entry header to
be **at most 25 units**, so landing these three entries byte-for-byte would fail C5 and therefore C2
(`conditions_passed == 8 of 8`). The staged package needs re-cut quotes (or the ceiling ruling changed
by the operator) before it can land.

## PROVENANCE CHECKS (same run set, read-only):

- All three staged entries carry `fetched 2026-10-24` / `ran 2026-10-24`, while the retained bodies'
  receipts (`sources/receipts.json`) record `fetchedAt` 2026-10-25T20:40:13Z / :14Z / :14Z and the round
  date is 2026-10-25 — the staged access dates do not describe the bodies the rechecks were run against
  (C6 requires `fetchedAt` on the round date).
- `yahoo-japan-robots-txt-basics.md` opens `source: S380`; its URL is `002885.php`, retained as `S418`
  (contract: staged S380 -> S418) — the pre-renumber id, while C2 requires the `source:` line to name the
  row id.
- Claimed section headings vs body: `大文字と小文字の区別` -> 1 hit in `S372.html`; `「$」記号` -> 4 hits
  in `S373.html`; `本文（クローラーによる巡回時の robots.txt の参照手順）` -> **0 hits** in `S418.html`
  (its H2s are `robots.txtとは？` and category headings). The quote is present; only the section label is
  ungrounded.

## ADVISORY — trim candidates (each substring-tested against the same body, <= 25 units both readings):

- S372: "Allow（許可）のあとに記述されたディレクトリ名は、" (19/23);
  "大文字と小文字の違いがあった場合、" (16/17); "別のものとして扱います。" (11/12).
  ("Disallow（拒否）、" is 2/6 — raw substring but below the 6-unit scan floor under the counter rule.)
- S373: "クローラーはプリフィクス（接頭辞）として扱い、" (20/23);
  "記述された文字列を含むURLがすべてマッチします" (21/22).
- S418: "クローラーによる巡回の際は、" (13/14); "サイトのルートディレクトリ（サイトの一番上の階層）"
  (23/25); "robots.txtを探します" (5/6). The second 、-clause has no internal 、, and its whole form
  "まずサイトのルートディレクトリ（サイトの一番上の階層）にあるrobots.txtを探します" is 33/36 and even
  trimmed of "まず" still 31/34 — so that clause must lose either the parenthetical or the URL token to
  fit, i.e. it cannot be carried as one span.

## RISKS / BLOCKERS:

- Blocker for the landing seat, not for this audit: no staged span can be landed under C5 without a
  re-cut. Re-cutting is an editorial decision outside this seat's scope; this report supplies measured
  candidates only.
- Unrun here by design: no build/lint/test/census run, no network fetch, no lane revision check, no
  counter execution (the counter reads committed bytes only and needs the entries to exist). Every figure
  above comes from the script shown plus four auxiliary one-liners run in the same session: quote
  inventory (`"`/typographic/single-quote counts), byte-level containment, heading hit counts, and the
  S418 fragment measurements used in ADVISORY.
- Not claimed: entry prose/scope quality; only quote truth, unit ceiling, recheck counts, provenance.

VERDICT: 6/6 staged spans are raw substrings of their retained bodies and 3/3 recheck greps count 1, but 6/6 exceed the 25-unit ceiling — the staged package is quote-true and cannot land as written under C5.
