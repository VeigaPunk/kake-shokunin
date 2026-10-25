# CriticJunkC2

ATTACKS: claim C2 (`met: conditions_passed == 8 of 8`) as implemented by `.ufo/waves/round-55/c55_quote_truth.py`
at a7a548e102b71bd16b0a6ddafa469393a2c98b69 — the three entries
`corpus/knowledge/yahoo-japan-robots-txt-{refusal-rules,pattern-syntax,basics}.md`, `corpus/SOURCES.md` rows
S372/S373/S418, `.ufo/waves/round-55/sources/receipts.json`, `corpus/lessons/round-55.md` §Gate, and the frozen
wording of `contract.md` §C2 (Before/After, quote ceiling, junk controls, sourced-claim ledger).

Method (scratch only): `D=$(mktemp -d /tmp/cj2.XXXXXX) && git clone -q --no-hardlinks <lane> "$D" &&
git -C "$D" checkout -q a7a548e…`; `git -C "$D" rev-parse --show-toplevel` → `/tmp/cj2.4Giw1b` (= `$D`).
Per variant: `git -C "$D" checkout -q -f -B <name> a7a548e…`, mutate, commit under
`-c user.name=criticjunkc2 -c user.email=criticjunkc2@local`, then
`python3 -B "$D"/.ufo/waves/round-55/c55_quote_truth.py --root "$D" --revision <rev>`.
Only `$D` and `/tmp` were written; the lane was read with `git show`/`git ls-tree`/`git diff` only, and only
this report file was written inside the lane. No install, no pacman transaction. Baseline at the measured
revision: `C2 quote-truth 8/8 met=True`, `EXIT=0`.

## VARIANTS:

Counter column = the run's own first line and exit. "Reviewers" = the W2 entry reviewers' six checks as written
in `w2-spec.json` (1 substring+fidelity, 2 untagged beyond-page statements, 3 cross-link claims, 4 runnable
`recheck:` command, 5 scope note, 6 unit counts). The W1 pair (`ReviewerC2CounterCode`, `CriticC2Contract`)
reviewed code/contract before any data and read no entry text, so no variant here can fool or un-fool them.

| variant | what I wrote | rev | counter | reviewers |
|---|---|---|---|---|
| V1 | S418 entry: 4 sidebar link labels only + an openly unsupported false claim | 70f078e4c3 | 8/8, exit 0 | caught: (2) claim not stated by page, (4) `recheck:` has no command |
| V2 | all 3 entries, renderings inverted, quotes untouched ("deemed unrestricted"→"deemed fully refused"; "prefix"→"suffix"; "first…root"→"last…subdirectory") | b034ad7eea | 8/8, exit 0 | caught: (1) fidelity |
| V3 | lossy: "normally"→"always", drop "on every crawl", drop "first", drop そのサイトに対する/みなして, "every…containing"→"confined to a path that begins" | 341a237402 | 8/8, exit 0 | caught: (1), whose prompt names exactly those words |
| V4a | S372's entry body under S373 (S372→S373 renamed) | 6b52f7358c | 7/8, exit 1, C5: 19 × "not a raw substring of the retained body" | n/a — counter catches it |
| V4b | S373 entry whose claim is S372's, carried on 3 template strings both pages print (footer links) + 3 S373-only padding spans | b5335005c1 | 8/8, exit 0 | caught: (2)/(3) |
| V5 | `receipts.json` S372/S373 replaced by the round-53 receipts verbatim (`fetchedAt 2026-10-25T11:29:11+00:00`, UA `…round53`) | b1dfc4b0b1 | 8/8, exit 0 | invisible: no reviewer reads receipts |
| V5b | S372 `fetchedAt = 2026-10-24T20:00:00-05:00` (stale, different offset) | 9603efb2ef | 7/8, exit 1, C6 "not a UTC stamp on 2026-10-25" | n/a |
| V5c | S372 `fetchedAt = 2026-10-25T09:00:00+09:00` (same instant, on the round date) | 9c25080e5e | 7/8, exit 1, same C6 note | n/a — offset-rigid in both directions |
| V6 | S418 entry + 4 fabricated quotes of <6 units (`"Disallow: /secret"`, `"User-agent: Yahoo"`, `"拒否します"`, `"the crawler ignores this file"`), none in the body | 34a1defea0 | 8/8, exit 0 | caught: (1) |
| V6b | the same fabrication at exactly 6 units (`"巡回しません"`) | 7681023c5e | 7/8, exit 1, C5 | n/a — the 6-unit floor is the boundary |
| V7 | honest entries; S418 row cells 1/4/5/6 replaced by `junk row — メタタグとは？ — <url>`, `REJECTED framing…`, "the sidebar only", "an absent file means full refusal…" | e584a2e5bf | 8/8, exit 0 | outside the entry reviewers' target (entry bytes unchanged) |
| V8b | S418 entry quoting 3 spans that each occur **twice** in the page, one of them raw markup (`"と検索エンジン</a></li>"`), + false claim | 7b9bc670fe | 8/8, exit 0 | caught: (2) |
| V9 | §Gate S418 line prefixed with a 6-unit quote shared by all three bodies (`"更新日 2010年11月24日"`) | dcea6ee106 | 8/8, exit 0 | LessonGate only; entry reviewers never see the lesson |
| V10 | **true, faithful, and empty**: S418 entry quoting 4 sidebar sibling labels + `"「基本事項」カテゴリ"`, a runnable `recheck:` (`grep -F -c` → observed 1), a scope note, no claim about robots.txt | 9fde995558 | 8/8, exit 0 | **not caught by (1)–(6)** |
| V1u | V1 with the validate mirror left honest | 05c32ac2dc | 7/8, exit 1, C7 "validated scratch entry differs from the landed entry" | n/a — proves C7 binds entry bytes to a self-asserted copy |

(V8 was my first attempt at the duplicate-span case; it failed on C2 because my fixture cited the id only in the
first 8 lines — my fixture's defect, not a counter finding. V8b is the corrected run.)

**V10 is the counterexample the predicate cannot refuse.** Its whole quotation set is navigation: four sibling
link labels and a sidebar heading. `QUALITY.md` round-55 criterion 2 states the purpose of the uniqueness term as
"at least three page-unique spans per entry keep a navigation string from passing as a rule quote" (committed
at a7a548e). V10 is exactly a navigation string passing, and it meets `conditions_passed == 8 of 8`.

## WHAT THE COUNTER CANNOT SEE:

Each line names the code site (line numbers at a7a548e) and the variant that demonstrates it.

1. **`in_content` means "after the first `<h2`"** (172–179: `h2 = text.find("<h2")`), so the sidebar, tag area,
   footer and template links count as "the page's content block". V1/V10/V8b quote nothing but those regions and
   pass. *Smallest fix*: bound the block to the article container (from the first `<h2` to `class="tag-area"` /
   `class="para-sub"`), or to the row's declared `anchor` cell region.
2. **"page-unique" means "absent from the other two retained bodies"** (386:
   `not any(span in t for t in others)`), not "occurs once in the page". V8b's `"robots.txtは、検索エンジン"`
   occurs twice in S418 (`t.count(span) == 2`, my scan) and still counts toward the 3. *Smallest fix*:
   `text.count(span) == 1` in the entry's own body as well.
3. **Quoted spans under 6 units are never examined** (381: `if units(span) < 6: continue`), so fabrication is
   free below the floor: V6 passes with four invented quotes; V6b fails only because it reaches 6 units.
   *Smallest fix*: check every span of ≥1 unit for substring membership and ceiling; keep the 6-unit floor only
   as the minimum for the located Gate quote.
4. **No relevance or semantic term exists.** Nothing tests that an entry's claim is supported by its quotes, that
   a rendering is faithful, or that the entry covers any rule of the page: V2, V3, V8b and V10 all pass. The
   predicate's "quote-true" is implemented as quote-*literal*. *Smallest fix*: require at least one quoted span
   inside the page's declared anchor region and at least one quoted span containing a directive token for rows
   whose scope is rules; state in the contract that fidelity is the reviewers' term, not the counter's.
5. **The new row's own metadata is unconstrained.** C3 compares cells 0–9 to base only for held rows (295), so
   S418's `source`/`scope`/`anchor`/`teaches` cells are free prose, and the body-title identity check reads the
   row's *own* title cell — V7 sets the title cell to `メタタグとは？`, a sidebar label, and the check passes.
   *Smallest fix*: require the new row's `anchor` cell string to occur in the retained body, and require the
   `teaches` cell to share ≥5 words with the entry's H1; or diff the new row against the staged row.
6. **C6 sees a calendar date in one spelling, not freshness** (422). A receipt copied from round 53 passes
   unchanged (V5), because the body bytes are identical (`sha256` S372 `ee8c9def…`, S373 `3173d961…` in both
   rounds). Nothing binds `fetchedAt` to this round. *Smallest fix*: require `fetchedAt` to be later than the
   round-55 contract commit time and the receipt `userAgent` to carry the round tag, or drop "freshness" from
   what C2 claims and call the axis "re-fetch corroboration".
7. **C7 is a receipt of agreement** (its own docstring says so): it catches an unsynced entry (V1u) but is
   satisfied by copying the junk bytes into `assimilation/validate/` — every passing variant above did exactly
   that. The census never runs in the counter.
8. **Gate-line uniqueness is checked on the last span only** (367: `spans[-1:]`), so V9's shared first quote
   passes. *Smallest fix*: apply the uniqueness test to every span on the Gate line, or require exactly one.

## WORDING:

- **"After: … quote-true spans"** (contract.md §C2) is not what C5 tests. C5 tests: raw substring, ≤25 units,
  inside "content", ≥3 spans absent from the other two bodies. V2 and V3 are quote-literal and quote-false at
  the same time, and both score 8/8. The predicate is necessary, not sufficient; the fidelity term lives only in
  the reviewer seats.
- **"every Gate quote and every quoted entry span"** is false as a universal for entry spans: spans of <6 units
  are not examined at all (V6 vs V6b). For Gate lines the universal does hold (all spans are checked).
- **"≤25 units … satisfies the CORPUS.md ≤25-word rule under any segmentation"** is untested by the counter,
  which runs one segmentation. I recomputed all 39 quoted spans (entries + Gate) under the defensible strict
  bound (each CJK character 1, each ASCII word-run 1): max = 25, so the clause holds for landed material — but
  only a count that charges CJK punctuation as words exceeds it (`巡回の拒否（Disallow:）、…` = 22 canonical,
  24 strict, 32 if punctuation is charged). The clause is true-for-this-material, not "any segmentation".
- **"Junk controls (selftest, 30 fixtures run after landing against the real evidence)"** does not match the
  committed counter: `grep -c '@case(' …/c55_quote_truth.py` → `46`, plus the `pass` case = 47 fixtures. The
  number is stale (QUALITY.md's own seat brief says "47 + 3"). More important: every fixture is a **one-point
  mutation of the landed evidence** (`variant(fn)` = real files + one edit), so a coherent junk *set* is outside
  the fixture space — V10 is that set.
- **The do-nothing control** is sound but narrow: I reproduced it byte-for-byte —
  `python3 -B …/c55_quote_truth.py --root "$D" --revision fcaf4b8…` → `0/8 met=False`, `EXIT=1`, and
  `diff` against `controls/base-c2-quote-truth-v2.txt` is empty. It establishes that *absence* fails; it says
  nothing about junk that is present, which is the failure mode above.
- **Before/After facts check out**: at fcaf4b8 `git ls-tree … .ufo/waves/round-55/sources/` is empty, all three
  entries are absent, base registry parses to 155 rows (`mirror-pin.json` `rows: 155`), measured to 156;
  `git diff fcaf4b8 a7a548e -- corpus/SOURCES.md` → `3 insertions(+), 2 deletions(-)` (3 `+` lines for the three
  ids, 2 `-` lines for the two held ids, so S418 is the only pure addition), and the S372/S373 cells 0–9 equal the
  base cells (base `opened`/`recheck` = `2026-10-25`/`180d`).
- **C3's `opened == ROUND_DATE` is satisfiable for the held rows only because round 53 and round 55 fall on the
  same date** (base row S372 `opened` = `2026-10-25`). Had round 53 been a day earlier, "opened = round date" and
  "differ from base in `used-by` only" would be jointly unsatisfiable. The contract should say this is a same-day
  coincidence, not a property of the check.
- **Smallest fixes**: replace "quote-true" with "quote-literal (substring + ≤25 units + 3 cross-body-unique
  spans), fidelity reviewed separately"; replace "30 fixtures" with the counted number; add "the new row's
  metadata cells are unconstrained by this predicate"; add "freshness is receipt-asserted, not verified".

## SOURCED-CLAIM HONESTY:

Observed: round-53 `receipts.json` carries S372/S373 with `fetchedAt 2026-10-25T11:29:11+00:00`,
`userAgent kake-shokunin-round53`, `sha256 ee8c9def…`/`3173d961…`; round-55 carries the **same** sha256 and bytes
with `fetchedAt 20:40:13/14+00:00`, `userAgent kake-shokunin-round55`. The two W1 scouts record their own GETs at
~20:48Z. So: S418 is the only page newly opened this round; S372/S373 are the same bytes re-fetched, and the
counter cannot distinguish a re-fetch from a re-save (V5 passes with the round-53 receipts verbatim).

The contract sentence "C2 rests on three rows opened this round (S372, S373 re-opened; S418 new)" is half
honest: the parenthetical is exact, the main clause is not — and the registry cannot repair it, because S372/S373
carry `opened = 2026-10-25` (round 53's date) and C3 *requires* that value. A registry-only reader would conclude
all three were opened this round. The lesson's own wording ("S372 and S373 are held rows (opened round 53); this
round re-opened both against fresh GETs") is the honest form and should be the contract's.

Recommended phrasing for the report: *"C2's sourced claim rests on one page opened this round (S418, new row) plus
two held rows re-opened against fresh GETs whose bytes are unchanged from round 53 (sha256 equal), evidenced by
`w1/ScoutFreshS372.md`/`S373.md` and the receipt timestamps; the counter verifies the pins, not the fetch."*
Also: what is fresh is the fetch, not the content — both pages print 更新日 2010年11月24日 and the bytes are
round-53 identical, so no content-freshness claim should be made under the freshness axis.

VERDICT: junk and mis-glossed sets do meet 8/8 — V10 (navigation-only but true and review-proof), V1/V2/V3/V6/V8b (false or lossy, caught only by the reviewers), V5 (round-53 receipts) and V7 (junk new-row metadata) all exit 0; the predicate is a literal-quote floor, not a quote-truth gate, and the contract's "quote-true", "every span", "30 fixtures" and "three rows opened this round" overstate what it measures.
