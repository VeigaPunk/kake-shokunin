# Critic report — C1 source-quote identity (S374)

Seat: L1Kake54.CriticC1SourceQuote — findings only; no admission claim.
Scope: (a) does the correction's source quote occur in the retained S374 body;
(b) is it located in its content paragraph; (c) are source semantics overstated.

## Surfaces

- Correction block: `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` lines 52–68
  (uncommitted working-tree append; `git status` shows the file modified vs HEAD `acae1dcc`).
- Retained body: `.ufo/waves/round-52/sources/S374.html`, sha256
  `3ad358bdbe7a74798df151c282e4b57af7475686dc405b3f8bad08f68881aecb` (8153 bytes;
  matches contract.md and the correction's pinned hash — recomputed this round).

## (a) Quote occurrence in retained body — CONFIRMED

- The correction's bracketed quote 「このリンク先のウェブページの巡回を推奨していない」
  is byte-identical to the body substring (Python `==` on raw bytes; quote at body
  byte offset 3157).
- Occurrences: exactly **1** in the body (`body.count(q) == 1`), matching the
  correction's own claim "occurs once" and `source-reopen.txt`'s
  `quote-occurrences-in-body=1`.
- No encoding normalization needed; the body carries it verbatim inside one
  continuous sentence.

## (b) Location inside content paragraph — CONFIRMED

- The quote sits inside `<div class="asset-content entry-content">` →
  `<div class="asset-body">` → the **first `<p>`** (line 104 of the retained file).
- That `<p>` is the rel=nofollow paragraph: it opens
  `&lt;a&gt;タグに属性rel=&quot;nofollow&quot;が指定された場合、` and continues after
  the quote with `、あるいは信頼できるリンクではないとサイト管理者
  （ウェブマスターやブログのオーナー）が考えているとみなします。` — one sentence,
  attribution to the site administrator, crawler deeming.
- The correction's claim "the exact quote occurs once at the source's
  rel=nofollow paragraph" is accurate. It is not in a heading, nav, sidebar,
  meta description, or footer.

## (c) Semantics — no overstatement found; evidence check per correction assertion

Correction asserts, checked against the source sentence/paragraph:

1. "earlier rendering glosses … as only an endorsement statement" — accurate:
   the live `(rendered:)` cell (lines 13–14) uses "does not recommend" /
   "cannot vouch for" with no crawl token.
2. "the phrase includes a crawl qualifier … not recommend the crawling of the
   link target's web page" — accurate: 巡回 = crawl; 推奨していない = does not
   recommend; リンク先のウェブページ = the linked-to web page. The qualifier the
   old gloss dropped is exactly 巡回.
3. "(or to consider the link untrustworthy)" — supported by the SAME source
   sentence's second disjunct (あるいは信頼できるリンクではない…と考えている).
   Caveat: that clause is outside the quoted substring itself but inside the
   same sentence; presented as the phrase's meaning, not as quote bytes. Minor,
   not an overstatement.
4. "subject is crawl restriction of linked pages, as also stated in the source
   title リンク先のウェブページの巡回制限" — accurate: `<title>` and `<h2>` (lines
   33, 100) carry that exact text; meta description (line 13) concurs.
5. "does **not** assert that the crawler refuses to fetch the URL" — accurate:
   the paragraph's continuation says the URL `は、新しいウェブページを見つける
   ために利用されます` (is used to find new web pages); the source makes no
   fetch-refusal claim.
6. "the URL may be used to discover new pages" — if anything an *under*statement
   ("may" vs. the source's declarative 利用されます "is used"). Conservative,
   opposite direction from overstatement.

Attribution preserved: correction keeps "is taken to" / deeming framing
(みなします), same as the source — no upgrade of publisher intent to engine
behavior beyond what the source states.

## Counter evidence (read-only, named command)

`python3 -B .ufo/waves/round-54/c54_s374_calib.py --root . --revision HEAD`:

```
  PASS C1.1_body: occurrences=1
  PASS C1.2_cells: suspect_cells=1
  FAIL C1.3_correction: no valid r54 correction block (block_offset=-1)
  FAIL C1.4_mismatch: mismatches=1
mismatches=1 met=False  EXIT=1
```

Expected, not a counterexample to this challenge: the counter reads committed
bytes only (`git show <rev>:<path>`) and the correction block is an
uncommitted working-tree append (git status: ` M …nofollow-semantics.md`,
HEAD `acae1dcc` still the round-52 commit). The working-tree file itself
satisfies C1.3's content requirements (mark `[r54-correction 2026-10-25]` at
line 54, exact quote in-block, English crawl vocabulary). Commit status is
outside this seat's quote/source-identity scope — flagged for the lane.

## Strongest counterexample attempted and result

Attempted: (i) quote absent/normalized in body → false (byte-exact, 1
occurrence); (ii) quote in boilerplate rather than article content → false
(first `asset-body` paragraph); (iii) correction inflates semantics → false
(deeming, disjunction, no-refusal, and discovery clauses all trace to the same
sentence/paragraph; the "untrustworthy" gloss cites the same sentence, just
outside the quoted substring — noted as a minor precision nit, not a defect).

## Bottom line

Quote identity, location, and semantics all hold against the retained body.
No counterexample to C1's quote/source identity survives local evidence.

Installs: none (read-only wave; no tools installed).
