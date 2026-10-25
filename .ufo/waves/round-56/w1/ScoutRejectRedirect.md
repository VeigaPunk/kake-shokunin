# ScoutRejectRedirect

Subject: staged `merge/kake/knowledge/corpus/knowledge/yahoo-japan-redirect-indexed-url.md` (row S389, page archives/002865.php).
Body: `.ufo/waves/round-56/sources/S389.html`, 6440 bytes, receipt sha256 `ef304c4d…c34ba0`, HTTP 200, fetchedAt 2026-10-25T22:02:44Z. The candidate was staged on 2026-10-24; this round's retained body is a later fetch. Nothing was run against live; every test below reads the retained body. Not run: `c56_quote_truth.py` (its conditions cover only S367/S419/S420, so S389 is outside its ADOPTED set; I applied the same conditions by hand).

## TESTS:

1. `source:` section label `§ 本文（リダイレクトの設定とインデックスに登録されるURL）`.
   - The heading text `リダイレクトの設定とインデックスに登録されるURL` occurs 3 times: `<title>` (offset 765), `<h2>` (offset 2513, the article heading) and the sidebar `<strong>` nav item (offset 3512).
   - `本文` occurs 3 times, all in image alt-text chrome (`このページの本文へ`, `ここから本文です`, `本文はここまでです`). None is a section heading.
   - So the label is a constructed composite: the real heading is the `<h2>`, and `本文（…）` is an invented wrapper.
   - Under the round-56 anchor test (`c56_quote_truth.py` C5, `anchor = row[5].split("§")[1]…`, then `anchor in text`), the anchor `本文（リダイレクトの設定…URL）` would be absent, so it fails. The same pattern appears in the staged S388 entry.
   - The article does carry `更新日 2010年11月24日` (1 occurrence), so the date part of the label is true.
2. `recheck:` grep string.
   - Command: `grep -F -c '<string>' sources/S389.html` → **1** (line count). It occurs once as a substring and sits in the article block, immediately after the `<a …>リダイレクト</a>` link.
   - Unit count (one per CJK char, one per non-CJK whitespace token, same rule as `c56_quote_truth.units`): **90 units**, over the 25 ceiling. The ceiling applies to double-quoted spans; this string is single-quoted inside a backticked shell command, so C5's `"([^"]+)"` scan never sees it. It does not fail the counter, but it is a 90-unit verbatim copy, 3.6x the ceiling, which the ceiling exists to prevent. (The staged S388 sibling does the same.)
   - `-> 1 (ran 2026-10-24)`: the count is valid for the retained 2026-10-25 body too (1), but the entry's run date is a day older than this round's fetch.
3. Quoted spans in the entry body.
   - Double-quoted spans: **0**. The only quoted strings are the recheck argument and the `source:` label (neither is a quote of the page in the C5 sense). There is nothing to check as raw substring, units or article block.
   - Condition C5 requires 3+ page-unique quoted spans of 6–25 units. At 0 this entry fails that bar outright.
   - Condition C2 (entry cites its id below the 8-line header): `S389` appears only in line 2; lines 9–17 never cite `[S389]`. Fails by the same test.
   - Every prose claim below is therefore an unquoted paraphrase of a page whose only operative sentence is one 90-unit sentence plus a two-row table.
4. What the page actually contains (article block, between `<h2>` and `個別リンクURL`): one sentence ("when a redirect is set on a page, the crawler decides from the following status codes whether to register the redirect-target URL or the redirect-source page") and a table `種類 / 説明` with two rows: `301リダイレクト | 永久的なリダイレクト` and `302リダイレクト | 一時的なリダイレクト`. Nothing else. The words canonical, 正規, 優先, 評価 occur 0 times.

## CLAIMS:

| # | Entry claim | Verdict | Why |
|---|---|---|---|
| 1 | Title / ¶1: "The status code decides which URL is registered… the crawler decides — from the status code — whether the URL it registers is the redirect's target or the page that carried the redirect" | SUPPORTED | Paraphrases the page sentence. Note the page says the *crawler* decides *based on* the code. It does not say which code yields which outcome. |
| 2 | "The operator's page states the rule" | INFERENCE (overstated) | The page states that a decision exists and what it depends on. It states no mapping (301 → target, 302 → source), so no "rule" in the outcome sense. |
| 3 | "its table enumerates the two kinds it recognises: 301 as a permanent redirect, 302 as a temporary one" | SUPPORTED for the rows; "it recognises" is INFERENCE | The two rows and their glosses (`永久的`, `一時的`) match. The page never says other codes are unrecognised. The table is the page's complete list under `次のステータスコード`, but exhaustiveness of the crawler's behaviour is not stated. No `[INFERENCE]` mark, which the lane's round-31 "qualifier a source does not state is marked" row requires. |
| 4 | "Read with the canonical entry beside it, the two documents say the same thing from two sides" | INFERENCE, out-of-page | The page has no canonical content. The "canonical entry" is the staged S388 entry, which is not in the lane (the lane has Google-based `canonical-selection.md` / `static-canonical-preflight.md`) and is itself a reject-evidence row in this round. The claim rests on an unadmitted sibling. |
| 5 | "The canonical tag is a preference the engine weighs" | Not from S389 | Comes from S388. Cross-page claim stated under the S389 header. |
| 6 | "a redirect is a transfer the engine follows, and the transfer decides for itself which URL survives" | **WRONG** against the page | The page says the **crawler** decides, using the status code as an input; the redirect does not "decide for itself". The clause also contradicts the entry's own title and ¶1 ("the crawler decides"). Further, "follows" is not on the page. |
| 7 | "A publisher who wants one URL registered has two instruments, and they do not carry the same weight" | INFERENCE, unsupported | Nothing on the page about weights or about canonical as an instrument. By the page's own sentence the redirect outcome is also an engine judgement (it "判定します"), which weakens the contrast with the canonical's "engine decides" the entry draws from S388. |
| 8 | `ground:` "which of the two URLs a redirect leaves behind is the one that gets registered" | INFERENCE | Restates the question the page poses, not an answer the page gives. |

Tally: 2 SUPPORTED (1, 3 rows), 4 INFERENCE (2, 3-qualifier, 7, 8), 1 cross-page (4/5), 1 WRONG (6).

Overlap with the lane entry `corpus/knowledge/redirect-rewrite-rules.md`: **none of substance**.
- The lane entry is about static-host rule precedence (Render vs Cloudflare Pages; first match, `resourcePrecedence`, `defaultStatus`) for an offline expectation audit, and states "Nothing here is a live serving claim".
- The only shared vocabulary is 301/302 as HTTP status labels.
- It says nothing about which URL a crawler registers, so S389 would not be a duplicate.
- The S389 page's content is also not already held elsewhere: grep of `corpus/knowledge` finds no entry citing S389 or 002865.

## DECISION:

**REJECT as staged.** Under `corpus/QUALITY.md` (round-31 "A qualifier a source does not state is marked [INFERENCE]"; round-26 row-specific located quote; round-56 quote-truth conditions applied by hand):

1. Zero located quotes (0 of the required 3 page-unique spans), and the id is never cited below the header.
2. The `source:` label's `本文（…）` wrapper is not a heading in the body; the real `<h2>` is the only true anchor.
3. One prose claim contradicts the page (claim 6: the transfer, rather than the crawler, decides), and the closing contrast ("two instruments, not the same weight") is an unmarked inference built on an unadmitted S388 entry.
4. The recheck string is 90 units against a 25-unit ceiling (not caught by the counter because it is single-quoted).

Merit rejection: **a procedural-plus-accuracy rejection exists, but there is no merit rejection of the page.** The page is a real, retained, HTTP-200, operator-authored statement that the crawler uses 301/302 to choose the registered URL, and the lane holds nothing on it. Admission on merit stands once the defects are fixed. (Out of this round's theme either way; C2 covers only S367/S419/S420.)

Flip condition: ADMIT if a rewrite (a) cites `[S389]` in the body; (b) anchors `source:` to the true heading `リダイレクトの設定とインデックスに登録されるURL` (drops `本文（…）`); (c) carries 3+ page-unique double-quoted spans of 6–25 units, e.g. the `301リダイレクト`/`永久的なリダイレクト` and `302リダイレクト`/`一時的なリダイレクト` table cells and clauses of the sentence (each cut to ≤25 units), each checked with the helper-equivalent for S389; (d) shortens the recheck grep to ≤25 units (e.g. `ステータスコードをもとに、リダイレクト先のURLをインデックスに登録するか` — verify count first, not run here); (e) deletes claim 6, or restates it as "the crawler decides, using the code" and marks claims 2/3-qualifier/7/8 `[INFERENCE]`; (f) drops the S388 cross-reading, or admits S388 first and cites it as a separate row; (g) updates `verified-at`/`fetched` to the retained 2026-10-25 body.

VERDICT: REJECT as staged (0 quoted spans, label `本文（…）` absent from body, claim "the transfer decides for itself" contradicts the page, recheck string 90 units, id never cited); no overlap with redirect-rewrite-rules.md; no merit rejection of the page itself, flips to ADMIT on the seven fixes listed.
