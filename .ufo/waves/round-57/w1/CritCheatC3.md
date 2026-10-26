# CritCheatC3

Attack on C3 (`c57_quote_truth.py`, predicate `conditions_passed == 8 of 8`). Hypothesis: a do-nothing-shaped
change (no re-fetch, no reading of the pages for claims) reaches 8/8 with placeholder entries and junk spans.

**Result: hypothesis confirmed three times.** Scratch lane clone of the lane at `b9a5d012f7fd`, all work inside
`$D` only (`git -C "$D" rev-parse --show-toplevel` == `$D`), commits made with
`-c user.name=selftest -c user.email=selftest@local`, counter run as
`python3 -B .ufo/waves/round-57/c57_quote_truth.py --root $D --revision <tip>`. `sources-census.sh` was never run.

| run | commit in `$D` | tree | counter |
|---|---|---|---|
| A0 | `a28ee34634d7` | real retained bodies, junk quotes | 7/8, exit 1 (C2: entry only 7 lines, so `lines[8:]` has no citation) |
| A  | `c6d766c1747b` | same + 3 padding lines in each entry | **8/8, exit 0** |
| B  | `24c3d85dd695` | bodies replaced by 1.5 KB synthetic HTML pages, receipts rewritten | **8/8, exit 0** |
| C  | `93f55f69e80c` | bodies replaced by ~1.2 KB **tagless plain text** with the two marker strings | **8/8, exit 0** |

## PER-CONDITION RESULT:

- **C1_entries_exist — pass.** Two files written from scratch: `corpus/knowledge/baidu-dead-link-types.md` (294 B),
  `.../baidu-spider3-dead-link-model.md` (321 B). The staged names were simply never created. Nothing checks that the
  entry text derives from the page.
- **C2_entry_provenance — pass** (second attempt). Header `source: S421 — <url>`, `verified-at: 2026-10-25`,
  `recheck: 180d`; one line below the header repeats the id. Only structural regexes; entry prose is one sentence.
  The 7-line entry failed only because the citation must sit at index >= 8 — a line-count artefact, not provenance.
- **C3_row_shape — pass.** Two 11-cell rows appended after S420: kind `docs`, tier `A`, status `mined`,
  opened `2026-10-25`, recheck `180d`, exact URL. `scope` and `teaches` cells are the literal placeholder
  `placeholder scope text that is long enough to pass the length gate` (66 chars) — only a 20-char floor is checked.
- **C4_used_by — pass.** `used-by` = exactly the entry path.
- **C5_quote_truth — pass, and this is the core finding.** Each entry carries three quoted spans that are raw
  substrings, inside the article block, page-unique — and are pure boilerplate: S421 quotes FAQ headings
  `Q：死链是如何产生的？` (8u), `A：死链可能存在以下来源：` (10u), `为什么要及时处理死链&nbsp;？` (10u);
  S422 quotes section headings `『死链处理更及时—被黑低质页面全屏蔽』` (16u),
  `『链接提交更好用—站点提交链接会更易收录』` (18u), `有兴趣的站点可以参加：` (10u). The Gate lines carry one of
  these plus URL and date. None of these spans states a dead-link definition, a cause or a crawl rule.
  The "page title" cell was set to `百度开发者中心` — the site brand, not the page `<title>` — and the "anchor heading"
  to `推荐阅读`, a navigation label; both pass because the check is `substring in body`. With fabricated bodies
  (runs B/C) the three spans are whatever the seat writes between `class="article-info"`/`class="zz_dldes_content`
  and `class="footer"`; the article block is a `str.find` pair, not a DOM parse, so the bodies need not even be HTML.
- **C6_receipt_pins — pass.** `receipts.json` rewritten by hand from the seat's own bytes: matching sha256/bytes,
  `httpStatus: 200`, `fetchedAt: 2026-10-25T00:00:00Z`, `userAgent: kake-shokunin-round57`, `url` = the registry URL.
  For NEW_ROWS `HELD_BODY_SHA256` is empty, so no pinned digest exists to compare against; the receipt is the only
  authority on the body and the seat writes both.
- **C7_validate_before_append — pass.** Four handwritten files (`census-argv.txt` naming `--file` and
  `sources-census.sh`, `census-stdout.txt` = one line `file<TAB>ok<TAB><validate registry>`, `census-exit.txt` =
  `exit=0`) plus byte-identical copies of the landed registry and both entries. No census invocation; the receipt
  and the append are in the *same* commit, so "validated before the append" is not ordered.
- **C8_mirror_bytes — pass for free.** The mirror and `mirror-pin.json` already exist at the contract commit
  `b9a5d01` (ancestor of every measured tip) and already equal the base registry (`010af792…`, 158 rows), so the
  strict-ancestor rule is satisfied without any work. Only rows 160 = 158 + 2 and the removal-equality check had to
  be met, which the append at the end of the `## Registry` table satisfies byte-exactly.

## MINIMAL JUNK TREE:

Run C (cheapest that passed), 13 files, 4 of them copies:

```
  148075 B  corpus/SOURCES.md                                    (+2 rows, 671 B added; everything else byte-identical to base)
     294 B  corpus/knowledge/baidu-dead-link-types.md             (10 lines, one quoted sentence)
     321 B  corpus/knowledge/baidu-spider3-dead-link-model.md     (10 lines, one quoted sentence)
     271 B  corpus/lessons/round-57.md                            (## Gate, two lines)
    1192 B  .ufo/waves/round-57/sources/S421.html                 (tagless text: 2 marker strings + 3 spans + filler)
    1271 B  .ufo/waves/round-57/sources/S422.html                 (same)
     611 B  .ufo/waves/round-57/sources/receipts.json             (rewritten: sha256/bytes/200/date/UA/url)
     132 B  .ufo/waves/round-57/assimilation/validate/census-argv.txt
      68 B  .ufo/waves/round-57/assimilation/validate/census-stdout.txt
       7 B  .ufo/waves/round-57/assimilation/validate/census-exit.txt
  148075 B  .ufo/waves/round-57/assimilation/validate/corpus/SOURCES.md              (copy of the landed registry)
     294 B  .ufo/waves/round-57/assimilation/validate/corpus/knowledge/baidu-dead-link-types.md        (copy)
     321 B  .ufo/waves/round-57/assimilation/validate/corpus/knowledge/baidu-spider3-dead-link-model.md (copy)
```

No mirror, pin, lesson fixture or control had to be authored. The two "retained bodies" total 2.4 KB of invented
text and the entries total 615 B; the two rows add 671 B. Symlinks cannot shrink the C7 copies (`git show` returns
the link target, not content), so 13 files is the floor for this shape. Run A is the same tree minus the body/receipt
rewrite, using the real 34 KB/27 KB pages and the real receipts — i.e. **even an honest seat passes by quoting
headings and navigation labels.**

## WHAT THE COUNTER CANNOT SEE:

1. **Body authenticity.** For S421/S422 nothing anchors the retained body to a fetch: no pinned digest, no
   independent copy, and the receipt is written by the same commit that writes the body. C5+C6 therefore prove only
   that two strings the seat authored are self-consistent. The contract's "retained bodies … with sha256 receipts"
   reads as provenance the counter does not deliver.
2. **Title / heading / printed date identity.** `title in body`, `anchor in body`, `发布日期：<date> in body` are
   substring tests over attacker-chosen strings; a nav brand and a nav label pass, and a fabricated body can print
   any date. No comparison with the page `<title>`, no heading-level check, no section-containment check.
3. **Relevance / support.** Any 6-unit substring between the markers qualifies, including FAQ questions, list
   lead-ins, section headings and the `推荐阅读` block that sits inside the S421 article window (offset 21251 of
   9346..21828). The contract discloses "substring truth, not support" — the demonstrated cost is zero reading.
4. **Rendering fidelity.** Markup is never parsed; tagless text passes, so nothing about `<h2>`/`<p>`/`<li>` structure,
   entity rendering or what a reader would see is constrained.
5. **Row prose.** `scope`/`teaches` only need 20 characters; the placeholder text passed.
6. **Ordering of C7.** The census receipt and the append can be one commit; "validated before the append" is a file
   convention. (Disclosed in the contract, but the counter accepts the same-commit shortcut.)
7. **C8 provenance.** The mirror and its pin were authored by the same planner/seat lineage at the contract commit;
   the "strictly earlier" rule is satisfied by construction, so C8 constrains the registry diff only.
8. **Independent counting.** The counter is a file the seat can read; nothing prevents a seat from iterating against
   it (I did, in two minutes, from 7/8 to 8/8), and `--selftest` is still a stub (exit 2).

## RECOMMENDED COUNTER CHANGES:

1. **Pin new-row bodies in the frozen contract.** Move `HELD_BODY_SHA256` from `{}` to the two digests taken from
   `sources/receipts.json` at the contract commit, and have C6 require body sha256 ∈ that pin for *every* adopted
   row (held and new). This alone kills runs B and C and is a one-line data change — the strongest, cheapest fix.
2. **Make C6 receipt-vs-pin, not receipt-vs-body.** Require the receipt's `sha256`/`bytes` to equal the pinned value
   *and* the fetched body, so a rewritten receipt cannot re-anchor a rewritten body. If the pin must be set after the
   fetch, put it in a commit that is a strict ancestor of the measured revision (the C8 pattern).
3. **Order C7 like C8.** Require the `assimilation/validate` tree to be added in a commit that is a strict ancestor
   of the measured revision and whose registry blob is byte-equal to the *mirror* (pre-append) rather than to the
   landed registry; then require the landed registry to differ from that blob by exactly the two new rows. Fabrication
   stays possible, but post-hoc receipt writing in the append commit stops working.
4. **Constrain the quote to prose, not to a string find.** Require each Gate/entry span to be (a) not the text of any
   `<h1..<h6>`/`<a>`/`<li>` node and (b) not inside a `推荐阅读`/nav container — i.e. parse the block (even
   `html.parser`) and locate the span in a text node of the article container. Cheap, and it removes headings and the
   recommendation list as quote sources.
5. **Bind the row's identity cells to the page.** Check `title` against the body's `<title>` (normalised, minus the
   site suffix), require the anchor heading to match an actual heading node inside the block at a stated level, and
   require the `发布日期` value to come from the page's own date field, not from any occurrence in the body.
6. **Refuse placeholder prose.** Require `scope`/`teaches` to contain at least one span that is also a quoted,
   page-unique entry span, or at minimum reject cells whose content repeats between the two new rows.
7. **Ship the selftest.** The contract promises wave-1 fixtures; `--selftest` returning 2 means no seat can prove the
   counter fails a junk tree. A minimal fixture is exactly run C above (13 files) with an expected `8/8` and a
   one-field mutation (body sha256 changed) with an expected `<8/8`.

## Notes

- No tool installs were needed; nothing was written outside `$D` and this report.
- Lane jj/Git state and sibling lanes untouched; read-only `git show/log/ls-tree` only, in `$D` for writes.
- Not run by me: `sources-census.sh`, `validate_append.sh`, `span_tools.py` checks are read-only helper runs on the
  real bodies only (used to pick run A's spans).

VERDICT: C3 reaches 8/8 from junk — 13 files, 2.4 KB of invented "retained" text, junk headings as quotes, a hand-written census receipt and a mirror it gets for free; C5/C6 have no body-authenticity anchor for new rows.
