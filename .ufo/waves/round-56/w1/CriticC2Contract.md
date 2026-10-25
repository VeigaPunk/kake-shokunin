# CriticC2Contract

Seat: leaf critic, claim C2 (freshness), pre-build. Lane HEAD `6b3df99d694f5`; base `e48354b7c26b`.

Read: `contract.md`, `c56_quote_truth.py` (903 lines), `derive_c56_quote_truth.py`, `span_tools.py`,
`sources/*.html` + `receipts.json`, `assimilation/mirror-pin.json`, base registry at `e48354b7c26b`, the
round-55 counter at base. Selftest state: at HEAD the r56 `--selftest` is the stub (0 fixtures); the
working tree carries an **uncommitted** +317-line port (55 `@case` fixtures + `pass` + 3 unit checks =
59 checks) from the untracked `derive_c56_selftest.py`. Committed evidence remains r55's 54 checks.

Method: imported the counter and drove its own `_build`/`run_checks` in `mktemp` repos (throwaway
identity only inside `$D`; lane and jj untouched, no writes outside this report). Fixture = base
registry bytes + S419/S420 rows + S367 `used-by` extended + the real bodies/receipts + `## Gate` lines
+ census receipts + three entries. The condition code C1..C8 I measured is byte-identical to the
frozen HEAD counter (`git diff -U0` touches only the docstring and the selftest block, line 545+);
`_build` is the sandbox builder from the uncommitted port. Every number below is from a run;
`[INFERENCE]` marks the one unrun claim. No tools installed.

Headline: **the frozen predicate is unsatisfiable on a truthful build (7/8) and satisfiable by a
3-character edit to the retained body (8/8).**

## ATTACKS:

Each attack was run twice — on the frozen counter with A1's body edit (the enabler that clears C5's
S367 title line), and isolated on a counter with only line 320 restricted to `NEW_ROWS`. All 8/8, exit 0.

**A1 — frozen 8/8 with no truthful entry (decisive).** Edit `sources/S367.html`: replace the `<h2>`
separator `\u3000―` with `（`…`）` so the held row's `source` cell becomes a substring (3 chars net);
recompute the S367 receipt (`sha256`, `bytes`); leave the entries as three bare-quote stubs
(A3) and the new-row cells as A9. Result on the **unmodified** counter: `8/8 exit=0`. The contract's
pinned body sha256 (`0188de9d…`) is nowhere in C1..C8; C6 only compares the receipt with the body it
was written beside, so the "retained body" pin is self-referential. Selftest: not covered —
`fail_body_swapped` swaps a whole body (caught by title/URL), `fail_empty_body` empties it; no case
edits a heading.

**A2 — junk entry accepted.** 12-line entry: `source: <sid>` / `verified-at:` / `recheck:` / blank /
three bare quoted spans / the id. No claim, no prose, no synthesis. `8/8`. Selftest: no case (no
"entry asserts nothing" fixture).

**A3 — false provenance header.** Same stub with `verified-at: 1999-01-01` and `recheck: 999999d`.
`8/8`. C2 (line 249) only requires a non-empty token; the round date is never compared. Selftest: no
case (`fail_no_source_header` checks presence only).

**A4 — page-unique is sibling-only.** S419 entry quoting `が設定されている場合、クローラーは`
(16 u, count 1, in content) — verbatim also in retained `S389.html`. `8/8`. `others` (line 334) holds
only the other two adopted bodies, so uniqueness is relative to S419/S420/S367. Selftest: no case
(`fail_gate_quote_shared_with_sibling`, `fail_entry_only_sibling_shared_spans` use the sibling only).

**A5 — fabricated quote of 52 chars, never checked.** Entry line
`> "&quot;fabricated-claim-that-appears-in-no-body-at-all&quot;"` — one non-CJK token = 1 unit, so
line 377 skips it before the substring test. `8/8`. Selftest: no case (`fail_short_span_fabricated`
uses a 5-unit CJK span; `pass_entity_span_raw` uses a real entity span ≥6 units).

**A6 — the page's own instruction can be misstated.** `> "&lt;meta name="robots" content=&quot;index,follow&quot;&gt;"`
is not a substring of S367 (`index,follow` never occurs). The raw `"` splits it into
`&lt;meta name=` (2 u, a real substring → passes) and ` content=&quot;index,follow&quot;&gt;` (1 u →
skipped), so the value-bearing piece is never checked. `8/8`. Selftest: no case.

**A7 — staged name survives.** Landed entry's H1 kept as `yahoo-japan-soft-404-recrawl` and
`corpus/knowledge/yahoo-japan-soft-404-recrawl.md` left beside the landed entry with different
content. `8/8`. Nothing checks the staged name's absence or the H1/filename agreement. Selftest: no
case (the staged path is never a fixture key).

**A8 — ceiling is 44 characters, not 25 units.** S419 entry quoting
`続けるときには、サーバーが「HTTP 404 Not Found」のステータスを返すよう` — len 44, counter units 25,
strict CJK-character units 28. `8/8`. `units()` (lines 150-152) counts only `CJK_RE` (line 89), which
omits U+3000–U+303F and U+FF01–U+FF60, so `、。「」` cost 0; a 41-char entity fragment
(` content=&quot;noindex,nofollow&quot;&gt;`) costs 1. Selftest: `fail_entry_quote_over_ceiling` uses
40 kana = 40 units → caught; no punctuation or markup case.

**A9 — row cells that assert nothing.** New rows with `kind=spec`, `tier=Z`, `scope=—`, `teaches=—`:
`8/8`; C3 (lines 259-289) pins only cell count, `status`, `opened`, `recheck`, URL and (held row)
`row[:10]`. Selftest: no case.

**A10 — junk recheck passes the regex.** `recheck=0000-00-00` and `recheck=999999d`: `8/8` (line 276).
Selftest: no case.

**A11 — S367's second sub-section only.** Entry quoting `サーバーで設定する方法`,
`ウェブページをホスティングしているサーバーで、`, `次のようなディレクティブ設定をします` while the
row's anchor names メタタグ first: `8/8`. The anchor check (line 326) is new-row-only, and the held
row's anchor is not literal anyway: `§ リンク先のウェブページの巡回制限 ― ウェブページ内や…` (U+2014,
ASCII space) vs the body's `…巡回制限\u3000― ウェブページ内…` (U+3000, U+2015) — `anchor_part in body`
is False, so the same anchor would fail as a new row. Selftest: `fail_anchor_heading_not_in_body` is
new-row-only.

**A12 — C7 receipts are self-authored (disclosed).** My fixtures fabricated `census-argv.txt`,
`census-stdout.txt`, `census-exit.txt` and the scratch registry; C7 passed every time — matching the
contract's own "a receipt check, not proof that the run happened". Recorded, not scored.

**Held-row notes (no attack needed).** C3's `row[:10] != base[:10]` and C4's exact `used-by` did hold
under every variant I tried (row reorder, dropped prior, `;` separators, extra cell). But the base
S367 row already carries `opened = 2026-10-25` (= `ROUND_DATE`), so C3's opened check gives no
evidence that S367 was re-opened this round; only the `used-by` extension does.

## WRONG-REJECT:

**WR-1 (blocking). C5 rejects every truthful build.** Line 319 builds
`title = " — ".join(row[1].split(" — ")[1:-1])` = `リンク先のウェブページの巡回制限（ウェブページ内や
サーバーでの設定）` (U+FF08/U+FF09, U+2014 separators). The retained body's `<title>` and `<h2>` say
`…巡回制限\u3000― ウェブページ内やサーバーでの設定` (U+3000, U+2015); `title in body` is False. The
truthful fixture — three real entries, real quotes, real receipts — returns **7/8**, its only note:
`S367: retained body does not carry the row's page title 'リンク先のウェブページの巡回制限（…）'`.
The truthful repair (correcting the row to the page's own heading) returns **6/8**:
`C3_row_shape: a cell other than used-by differs from the base row` and `C8_mirror_bytes: … != mirror
bytes`. So C5 (line 320) and C3 (line 287)/C8 forbid each other; only A1's body edit or a counter
amendment reaches 8/8. Contract facts that close the escape: the body is pinned at sha256 `0188de9d…`
and "S367 differs from its base row in `used-by` only".

**WR-2. The most probative S367 quote cannot be verified.** The page's instruction
`&lt;meta name="robots" content=&quot;index,nofollow&quot;&gt;` contains a raw `"` around `robots`; the
ASCII-double-quote representation splits it, and the value-bearing piece is 1 unit, so line 377 skips
it. A builder who wants the counter to check the instruction cannot: quoting it correctly and quoting
`index,follow` both return 8/8 (A6). This is the same defect as A5/A8 seen from the honest side.

**WR-3 (minor).** A span crossing a newline cannot be written at all: `re.findall` runs per line
(lines 356, 376). The `<pre>` blocks and the tag boundaries in S367 are exactly such spans.

**Selftest consequence.** `[INFERENCE]` the ported `pass` fixture reads the real landed files and so
would also return 7/8 on a truthful build; the L1 must not "fix" it by editing the S367 row (C3) or by
weakening the fixture.

## RECOMMENDED COUNTER CHANGES:

1. **Line 320** (title): restrict to new rows and add a held-row title check that survives the
   transcription difference, e.g. `if sid in NEW_ROWS and (not title or title not in texts[sid]):`
   plus, for `sid in PRIOR_USED_BY`, require `title.split("（")[0].split("\u3000")[0].strip() in texts[sid]`
   (`リンク先のウェブページの巡回制限` is in the body and in neither sibling). Without this, C2 is
   unmeetable.
2. **Line 89** (`CJK_RE`, used by `units()` at 150-152): add `\u3000-\u303f` and `\uff01-\uff60` so
   `、。「」（）` cost 1 each; then A8's 44-char span is 28 units and is rejected, and the ceiling means
   25 Japanese characters.
3. **Lines 376-377** (entry spans): drop the unit threshold — `if len(span) < 2: continue` — and run
   `verify()` for every non-empty span before any unit test. This alone kills A5 and A6 (the
   ` content=&quot;index,follow&quot;&gt;` piece fails the substring test).
4. **Line 334** (`others`): load every retained body under `SOURCES_DIR` (S367, S387, S388, S389,
   S419, S420), not just the two adopted siblings, so "page-unique" is unique among all retained
   bodies. Kills A4.
5. **Line 326** (anchor): apply to every adopted row, and require each `/`-separated sub-heading in
   the `§` cell to occur in the body (`メタタグを使用する方法`, `サーバーで設定する方法` both do). Kills
   A11 and would have surfaced the non-literal S367 anchor.
6. **Line 249** (C2 header): require `verified-at:` to equal `ROUND_DATE` (currently any token). Kills
   A3.
7. **Line 276** (C3 recheck): `\d{1,3}d` and a real calendar date; `0000-00-00`/`999999d` must fail.
   Kills A10.
8. **After line 240** (C1): require `corpus/knowledge/yahoo-japan-soft-404-recrawl.md` to be absent at
   the measured revision and each entry's first heading to match its filename. Kills A7.
9. **C3 for new rows**: pin `kind=docs`, `tier=A`, and require `scope`/`teaches` to be non-`—`. Kills
   A9.
10. **C6/C2 content**: add a contract-level body requirement (one non-quoted prose line of ≥40
    characters below the header) so a three-quote stub is not an "entry" (A2), and state in the
    contract that the retained-body sha256 is checked against `contract.json` — not just against the
    receipt beside it (A1). Both are scope decisions for the L1, not counter-local fixes.

VERDICT: C2 as frozen cannot be met by a truthful build (7/8, C5 line 320 vs C3 line 287) and reaches 8/8 by a 3-character edit to the retained S367 heading plus junk entries — amend line 320 (and 150-152, 376-377, 334) before any build scores.
