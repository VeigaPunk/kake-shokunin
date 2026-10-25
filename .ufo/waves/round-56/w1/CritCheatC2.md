# CritCheatC2

Attack: a do-nothing change meets the C2 predicate `conditions_passed == 8 of 8` with placeholder entries.

Counter run: `.ufo/waves/round-56/c56_quote_truth.py` (lane working copy, v1.1) with
`python3 -B <counter> --root $D --revision <tip> --json`. `git diff 2d308e808bfd -- <counter>` shows two hunks only
(`@@ -1,7 +1,8 @@` docstring, `@@ -543,9 +544,322 @@` selftest); `run_checks` is byte-identical to the contract
revision, so the frozen conditions were measured.

Scratch: `D=$(mktemp -d); git clone -q --no-checkout <lane> "$D"; git -C "$D" checkout -q <rev>`; toplevel asserted
equal to `$D`; every commit `git -C "$D" -c user.name=selftest -c user.email=selftest@local commit`. No lane path,
jj state or lane index touched; the lane's tracked diff (`c56_quote_truth.py`, `c56_selftally.py`) predates this seat.

Variants measured (all trees built in `$D` only):

| var | construction | parent | result |
|-----|--------------|--------|--------|
| A | junk tree, one commit; mirror + pin inherited untouched | 2d308e808bfd | **8/8, exit 0, met=True** (tip cc36c6b8c373) |
| B | same tree + mirror written in the same commit | e48354b | 7/8 — C8 only: `mirror add-commit is the measured revision (not strictly earlier)` |
| C | mirror deleted, junk appended, mirror re-added, empty tip commit | 2d308e808bfd | **8/8** (tip 3a41313a2a08) |
| D | A, but S419's three spans inside `<!-- hidden nav: … -->` inside the window, plus entry line `> "zzznotinbody"` | 2d308e808bfd | **8/8** (tip bec0bb6d65b1) |
| E | inherit the contract revision's real bodies + real receipts; 12 authored files | 2d308e808bfd | 7/8 — C5 only: `S367: retained body does not carry the row's page title 'リンク先のウェブページの巡回制限（ウェブページ内やサーバーでの設定）'` |

## PER-CONDITION RESULT:

| condition | A | B | C | D | E | what a junk tree needs |
|-----------|---|---|---|---|---|------------------------|
| C1_entries_exist | pass | pass | pass | pass | pass | three files at the three paths; 171 B each |
| C2_entry_provenance | pass | pass | pass | pass | pass | `source:`/`verified-at:`/`recheck:` in 8 lines, id on the `source:` line and again on line 9 |
| C3_row_shape | pass | pass | pass | pass | pass | hand-typed 11-cell rows; only the base registry bytes are real |
| C4_used_by | pass | pass | pass | pass | pass | typed cells |
| C5_quote_truth | pass | pass | pass | pass | **fail** | three 6-kana spans per body, inside the byte window |
| C6_receipt_pins | pass | pass | pass | pass | pass | receipt self-signed over the junk body |
| C7_validate_before_append | pass | pass | pass | pass | pass | three typed text files; no census ran |
| C8_mirror_bytes | pass | **fail** | pass | pass | pass | inherited from the contract commit |

No condition stopped a junk tree. A reaches 8/8 in one commit of 16 files; nothing in the tree is a page, a fetch or
a reading. B and E are the only 7/8 outcomes, and neither is about content: B is the mirror-first-add ordering in a
root not descended from the contract commit, E is the real page's punctuation against the frozen row.

C5/C3 conflict (the sharpest finding): the frozen base row for S367 carries
`リンク先のウェブページの巡回制限（ウェブページ内やサーバーでの設定）` (U+FF08/U+FF09). The retained real body
`2d308e808bfd:.ufo/waves/round-56/sources/S367.html` carries `リンク先のウェブページの巡回制限　― ウェブページ内やサーバーでの設定`
(U+3000 + U+2015) at 4 sites and the row's string at 0 sites. C3 freezes `row[:10]` for S367, so `row[1]` cannot be
corrected; C5 requires the row title to be a substring of the body. The honest body therefore caps at 7/8 (E), and
the only route to 8/8 for S367 is a body containing the registry's own punctuation — i.e. bytes that are not the
page's. Variant A passes precisely because its fabricated body types that string in.

## MINIMAL JUNK TREE:

Variant A, one commit `cc36c6b8c373` on `2d308e808bfd`; diffstat `16 files changed, 413 insertions(+), 1254 deletions(-)`
(the deletions are the three real retained bodies and the real receipts). Mirror and `mirror-pin.json` are inherited
untouched — the commit touches no path under `assimilation/pre-append/`.

```
   337  corpus/lessons/round-56.md                     # 1 heading, 3 Gate lines, "junk"
   171  corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md
   171  corpus/knowledge/yahoo-japan-deleted-url-recrawl.md
   171  corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md
1756  .ufo/waves/round-56/sources/S367.html           # 1300 B of it is one filler comment
1668  .ufo/waves/round-56/sources/S419.html
1668  .ufo/waves/round-56/sources/S420.html
   854  .ufo/waves/round-56/sources/receipts.json     # sha256 computed over the junk bodies
   104  .ufo/waves/round-56/assimilation/validate/census-argv.txt
    82  .ufo/waves/round-56/assimilation/validate/census-stdout.txt
     7  .ufo/waves/round-56/assimilation/validate/census-exit.txt
   171  .ufo/waves/round-56/assimilation/validate/corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md
   171  .ufo/waves/round-56/assimilation/validate/corpus/knowledge/yahoo-japan-deleted-url-recrawl.md
   171  .ufo/waves/round-56/assimilation/validate/corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md
146003  corpus/SOURCES.md                             # base registry + 2 rows, 1 used-by cell
146003  .ufo/waves/round-56/assimilation/validate/corpus/SOURCES.md
```

Authored junk outside the two registry copies: 7,502 B, of which 3,900 B is filler comments. Each "knowledge entry"
is 4 header lines, 4 blank lines, one sentence (`S419 placeholder; no page was read.`) and three 6-kana spans
(`"かかかかかか"` etc.). Each body is `<h2>`, one `更新日` line, three `<p>` spans, one `value="<row url>"` input,
one `個別リンクURL` line, filler. The two new rows read `| S419 | Junk — JUNK TITLE 419 — <url> | docs | A | junk
description cell | § JH419 (更新日 2026-10-25) | junk quote cell | mined | 2026-10-25 | 30d | <entry> |`.

Cheaper still: variant E needs only 12 authored files (1,628 B outside the registry) over the inherited real bodies
and receipts — but it lands at 7/8 because of the S367 title clause, so 8/8 does require rewriting the S367 body.

## WHAT THE COUNTER CANNOT SEE:

- Body provenance. C6's pin is self-signed: the sha256 is computed over whatever bytes ship, and the builder computed
  it. A 1,668-byte synthetic document passes exactly as the 7,428-byte page does. No fetch, no response headers, no
  cross-check of body bytes against the row URL or the receipt URL beyond string equality of two typed fields.
- Rendering fidelity. `content_window` is a byte-offset pair (first `<h2`, first `個別リンクURL`); nothing is parsed or
  rendered. Variant D puts all three spans — including the Gate quote — inside `<!-- hidden nav: … -->` and still
  passes C5. Script/style/attribute placement was not run but follows from the same byte-window test.
- Relevance. No condition relates a quoted span to the row's description cell, the entry's claim, or the page's
  subject. In E the accepted spans are fragments (`ージの巡回制限は`, `のウェブページに`, `ステータスを返し`) inside
  entries that assert nothing; in A the spans are six kana with no meaning at all. `junk description cell` passes C3.
- Quote coverage. `if units(span) < 2: continue` exempts every single-token non-CJK quote from verification; D's
  `> "zzznotinbody"` is accepted. Duplicates inside the window are also accepted: the uniqueness test is
  `text.count(span) != 1 and not in_content(...)`, so a span appearing N times inside the block passes verification
  (it merely cannot count toward the three unique spans).
- Title identity. The title is read from `row[1]` and then required to occur in the body — both sides authored by the
  same seat. The check rejects the real page (E) and accepts a body that copies the row's punctuation (A).
- C7. The docstring calls it "a receipt check, not proof that the run happened"; it is exactly that. argv, stdout and
  exit were typed by hand, and the validated scratch registry is a byte copy of the landed one.
- C8 ordering. `git log --diff-filter=A` is newest-first and the code takes `commits[-1]`, the OLDEST add — for any
  tree descended from the contract commit that is `2d308e808bfd`, which already ships a mirror byte-equal to the base
  registry and a matching pin. Variant C deletes the mirror, appends, re-adds the mirror and adds an empty tip commit:
  still 8/8, the counter still points at `2d308e808bfd`. "Strictly earlier" only bites when the measured revision is
  the first-ever add (B).
- Novelty. Nothing checks that a new row is about a different page or a different mechanism; the new rows' content
  cells are unconstrained strings and no condition reads them.

Not run: script/style/attribute span placement, duplicate-span variants, a real `sources-census.sh` cross-check.

## IMPACTED AXES / SMALLEST SAFE CORRECTION

Axes: C2 predicate integrity (8/8 reachable with zero research), C5 quote truth (substring + byte window only),
C8 pre-append ordering (inherited, never re-derived), C7 census receipt (typed).

- C5 title: normalise both sides (U+3000, U+2015/―, full-width parens) and compare against the body's own
  `<h1>`/`<title>`, not against a typed row cell. This makes the real S367 body pass and removes the forced
  body-rewrite that A exploits.
- C5 quotes: verify every quoted span — drop the `units < 2` exemption — and require each of the three unique spans
  to sit in a text node outside `<!--`, `<script>`, `<style>` and attribute values (closes D).
- C7: have the counter run `sources-census.sh --file <validated registry>` against the measured tree itself and
  compare, instead of reading a typed stdout (closes the whole of A's validate block).
- C8: require the mirror add-commit to be an ancestor of the commit that first introduces the S419/S420 row lines
  (`git log -S` on the registry), not merely of the measured revision (closes C).
- C6: pin the body to an artifact the seat cannot author alone — a fetch log committed by the fetcher with response
  headers and a sha256 recomputed by the counter from the same file, or a cross-seat re-fetch.

VERDICT: A one-commit, 7.5 KB junk tree — fabricated 1.7 KB "pages", three 171-byte placeholder entries, a self-signed receipt and a typed census receipt — reaches 8/8, while the honest retained bodies cap at 7/8 on a C3/C5 punctuation conflict; the counter measures self-consistency, not provenance, rendering or relevance.
