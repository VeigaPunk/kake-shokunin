# ScribeRowsGate

Round-60 w1, claim **C3** (freshness, sourced). Lane repo read-only: this seat wrote only
`.ufo/waves/round-60/w1/ScribeRowsGate.md` and `.ufo/waves/round-60/w1/ScribeRowsGate.files/`. The C3 counter
(`c60_quote_truth.py`), the two entries and the assembled lesson do not exist yet, so nothing below is an after-state
score; all checks are the author's own pre-checks against the frozen rules.

## Behavior

- Read `contract.md`, `contract.json`, `sources/receipts.json` and the three retained bodies. Bodies were **not**
  re-fetched; provenance was re-verified locally (`sha256sum` + `stat`): S427 `d70ce6f5…2175` / 74477 B, S428
  `0f296b86…d3b2` / 76197 B, S429 `423d99c5…9edd` / 178797 B — all equal to `receipts.json` (fetchedAt
  2026-10-27T04:0xZ, HTTP 200, userAgent `kake-shokunin-round60`).
- Applied the L1 anchor ruling of 2026-10-27 (received mid-task): the anchor cell names the nearest article-block
  heading that precedes the row's Gate quote, h1 included. S427's and S428's posture sentences sit in the page lead
  above the first `<h2>`, so both anchors are the article h1; S429's quote sits under an h2.
- Drafted the three rows in the S425/S426 cell style, the three Gate bullets, the S425 erratum and the
  `## Registry changes (old → new)` block (`rows.md`, `gate.md`).
- Quote pre-check used `span60.py`, which imports `.ufo/waves/round-59/c59_quote_truth.py` read-only and extends only
  its id-keyed `ARTICLE_START`/`ARTICLE_END` maps, so unit counts, article-block text nodes and page-uniqueness are the
  round-59 counter's own code, not a re-implementation.

## ROWS:

Three 11-cell rows (`|`-split field count 13 each, 0 escaped pipes, no cell carries a pipe). Titles equal each page's
`<title>` text before ` | ` and are 3+ units (5 / 3 / 4), so the C5 title clause holds for all three.

- **S427** — `Google for Developers — Google Crawler (User Agent) Overview — https://…/overview-google-crawlers`;
  `docs` / `A`; anchor `§ Overview of Google crawlers and fetchers (user agents) (Last updated 2026-06-12 UTC)`;
  `teaches` opens exactly `supersedes S425 — `; scope contains `common crawlers` and `special-case crawlers` and does
  **not** contain `their robots.txt posture` (checked mechanically); `mined` / 2026-10-27 / `180d` / used-by
  `corpus/lessons/round-60.md`.
- **S428** — `Google User-Triggered Fetchers` (`…/google-user-triggered-fetchers`); anchor
  `§ List of Google user-triggered fetchers (Last updated 2026-08-19 UTC)`; used-by exactly
  `corpus/knowledge/google-user-triggered-fetchers.md, corpus/knowledge/googlebot-verification.md`.
- **S429** — `Robots.txt Introduction and Guide` (`…/crawling-indexing/robots/intro`); anchor
  `§ Understand the limitations of a robots.txt file (Last updated 2025-12-10 UTC)`; used-by exactly
  `corpus/knowledge/robots-txt-limits.md`.

Scope content is page-bounded: S427's posture lines are the `crawler-types` table's common-crawlers sentence and the
AdsBot/global-user-agent sentence, with the user-triggered fetchers cell recorded as carrying **no** robots.txt clause;
S428 says `generally ignore` and declares its UA list not exhaustive; S429's limits are the non-enforcement sentence,
`it's up to the crawler to obey them`, and the disallowed-but-linked indexing sentence. No cross-document attribution
in any cell.

## GATE:

Three `- <id> —` bullets in `gate.md`; each carries the row URL, `accessed 2026-10-27`, the row's anchor cell
verbatim, the body sha256 and byte count, and two 6..25-unit spans with their unit counts. All six spans were checked
as raw substrings of **one** whitespace-collapsed text node of the article block (`class="devsite-article-body` ..
`<devsite-content-footer`), page-unique across the three bodies, and — under the L1 positional rule the C3 counter
implements — each sits in the anchored heading's own section (below the anchor heading, above the next one):

| id | span | units | chars | topic clause |
|---|---|---|---|---|
| S427 | `They always respect robots.txt rules for automatic crawls.` | 8 | 58 | carries `automatic crawls` |
| S427 | `User-triggered fetchers are part of tools and product functions where the end user triggers a fetch.` | 16 | 100 | — |
| S428 | `these fetchers generally ignore robots.txt rules` | 6 | 48 | carries `generally ignore` |
| S428 | `it only covers the requestors that are more likely to show up in log files` | 15 | 74 | — |
| S429 | `The instructions in robots.txt files cannot enforce crawler behavior to your site` | 12 | 81 | carries `cannot enforce` |
| S429 | `A page that's disallowed in robots.txt can still be indexed if linked to from other sites.` | 16 | 90 | — |

R59-D3 placement re-read on all three bodies: `Last updated <date> UTC` occurs twice per body and both occurrences
lie **after** `<devsite-content-footer` (offsets: S427 45212→45753/47188, S428 46928→47469/48904, S429
147029→147570/149010). `check_gate.py` (a mechanical C5 pre-check: URL, date, anchor verbatim, sha/bytes, span
ceilings, uniqueness, per-span unit statement, ASCII quotes, h1/h2/h3 anchor membership) prints **3/3 clean**.

## ERRATUM:

`gate.md` carries the R59-D4 paragraph. Substance: S425's `scope` cell asserts `the three crawler categories and
their robots.txt posture`; the page states posture for **common crawlers** (`They always respect robots.txt rules for
automatic crawls.`) and **special-case crawlers** (the AdsBot example, `ignores the global robots.txt user agent (`
… `) with the ad publisher's permission.` — split by an inline-code token), and its user-triggered fetchers cell has no
robots.txt clause at all (`User-triggered fetchers are part of tools and product functions where the end user triggers
a fetch.`, closing on `acts on the request of a user.` for Google Site Verifier). Superseded by S427 on the same URL,
whose `teaches` opens `supersedes S425 —`. S425 is left in place as a pure addition (no existing row's status,
recheck or used-by changed).

## CENSUS:

Scratch copy = base `corpus/SOURCES.md` + the three draft rows, run through the frozen census awk formulas
(`NF!=13` defect counter, duplicate-id, tier/kind/status enum, `used-by` existence):

- rows 164 → **167**; malformed (`NF!=13`) **0**; escaped pipes **0**; duplicate ids **none**; enum violations **none**
  (one line printed per violation; none printed).
- status histogram `mined=137 queued=8 rejected=22` (base 134/8/22, +3 mined); tier `A=144 B=6 C=17` (base 141/6/17);
  kind `docs=90 dataset=5 community=12 spec=42 tool=1 own-work=6 code=11`.
- base checks: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` = 164 at base; `grep -cE '^ *\| *S42[789] *\|'`
  = 0, so all three ids are absent from the base registry.
- `used-by` existence prints three missing paths — `corpus/knowledge/google-user-triggered-fetchers.md`,
  `corpus/knowledge/robots-txt-limits.md`, `corpus/lessons/round-60.md` — expected: this round's entry and lesson
  deliverables; every other mined row's used-by path resolves.

## Findings / limits

- **Counter conflict (reported verbatim to KakeR60 and ExecC3Derive).** The L1 anchor ruling requires h1 anchors, but
  the frozen C5 clause says `an <h2>/<h3> of the article block`, `c59_quote_truth.py`'s `article_headings()` reads only
  h2/h3, and its selftest control `fail_anchor_not_h2_or_h3` asserts that S427's h1 anchor **must fail**. A straight
  derivation of `c60_quote_truth.py` therefore fails C5 on S427 and S428 by construction. Counter version 1 must widen
  `article_headings` to h1/h2/h3 and retarget that control at a text that is no heading at all.
- S427's anchor deliberately differs from S425's (`§ Verify Google's crawlers and fetchers`): the S427 quotes that carry
  the posture material (`automatic crawls`) are in the page lead, and the ruling anchors a row at the heading preceding
  its quote. The identification sentence's h2 section is therefore quoted nowhere on the Gate line; the row's `teaches`
  cell still carries the three-signal statement, and S425 holds the same page's h2-anchored history.
- S428's anchor names the article h1 (the page has 9 per-fetcher h2s and no h2 over the lead), so it names the page,
  not a section; its Gate quote is the lead sentence. This is a deliberate consequence of the ruling, not an oversight.
- The erratum paragraph quotes the AdsBot sentence with an ellipsis for the inline-code `*` token; it is lesson prose,
  not a Gate quote, and no double-quoted span there is presented as a single-node span.
- Unrun: the C3 counter (absent), the two entries and the lesson assembly (other seats). No after-state score exists.

## Artifacts

- `.ufo/waves/round-60/w1/ScribeRowsGate.files/rows.md` — the three draft rows (sha256 `05360bdf6d48c3447eb1c74ea0b604e42f245ec355b0da130b61509660d4660c`).
- `.ufo/waves/round-60/w1/ScribeRowsGate.files/gate.md` — Gate prose + 3 bullets, erratum, registry-changes block (sha256 `e5d2094ba42a547863f72d80167e227e4177cda915e9300ab96200ed95d7c3de6`).
- `.ufo/waves/round-60/w1/ScribeRowsGate.files/span60.py` — read-only span/unit helper over the round-60 bodies.
- `.ufo/waves/round-60/w1/ScribeRowsGate.files/check_gate.py` — mechanical C5 pre-check, including the positional
  anchor rule (`3/3 clean`).
- No tool installs, no lane git/jj mutation, no files outside the two paths above plus scratch.

VERDICT: three C3 rows, three Gate bullets, the S425 erratum and the 164 → 167 registry-changes block are drafted and census-clean (167 rows, NF!=13 0); counter C5 must accept h1 anchors or C3 fails on S427/S428 by construction.
