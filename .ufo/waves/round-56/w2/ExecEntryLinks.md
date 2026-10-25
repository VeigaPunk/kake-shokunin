# ExecEntryLinks

Reference sweep of the three round-56 entries (`corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md`,
`yahoo-japan-deleted-url-recrawl.md`, `yahoo-japan-nonexistent-url-recrawl.md`). Read-only; no lane file, index or jj state
touched; no selftest/counter run (none is part of this seat's checks). Revisions checked: the revision under attack
`a450e43e696d032e3ac308383f6b3394e0c92860` and the lane tip at sweep time `7ad7db51dfcff2eccea9f7f73726f2437b2ed8de`
(the tip has moved past the dispatch revision; all three entries are tracked at both, and every result below is identical at
both). Base `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`: all three entries absent, registry 156 rows; at `a450e43`/tip the
registry has 158 rows, matching `contract.md:49-52`.

## IDS:

Extracted ids (all `S[0-9]{3}` occurrences, `grep -oE`): entry 1 → S367 (17×), S374 (4×), S372 (2×), S286 (1×);
entry 2 → S419 (13×), S420 (2×), S286 (2×), S273 (2×), S274 (2×), S372 (1×), S374 (1×), S050 (1×), S135 (1×);
entry 3 → S420 (12×), S419 (6×), S372 (2×), S286 (1×). Every id has exactly one registry row at both revisions
(`git show <rev>:corpus/SOURCES.md | grep -cE '^\| S<id> '` → 1 for each of the ten):

| id | corpus/SOURCES.md row (tip) | row at `a450e43` | cited by |
|---|---|---|---|
| S367 | 157 | yes | entry 1 (source) |
| S372 | 158 | yes | entries 1, 2, 3 |
| S374 | 154 | yes | entries 1, 2 |
| S286 | 151 | yes | entries 1, 2, 3 |
| S419 | 165 (new this round) | yes | entry 2 (source), entry 3 |
| S420 | 166 (new this round) | yes | entry 3 (source), entry 2 |
| S273 | 149 | yes | entry 2, entry 3 |
| S274 | 150 | yes | entry 2 |
| S050 | 58 | yes | entry 2 (via redirect-rewrite-rules.md) |
| S135 | 143 | yes | entry 2 (via redirect-rewrite-rules.md) |

Row URLs agree with the entries' source headers and with `sources/receipts.json` (S367 002852, S419 002856, S420 002857).

## PATHS:

Every cited path exists at the tip. `corpus/knowledge/` or bare `*.md` pointers resolve to `corpus/knowledge/<name>.md`:

- entry 1: `yahoo-japan-rel-nofollow-semantics.md` (L8, L113), `yahoo-japan-robots-txt-refusal-rules.md` (L9, L110),
  `crawl-error-status-table.md` (L107) — all present.
- entry 2: `corpus/knowledge/crawl-error-status-table.md` (L8, L44), `corpus/knowledge/crawl-budget-consequences.md`
  (L8, L46), `corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md` (L40), `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`
  (L48), `corpus/knowledge/redirect-rewrite-rules.md` (L48) — all present.
- entry 3: `crawl-error-status-table.md` (L8, L78), `yahoo-japan-robots-txt-refusal-rules.md` (L8, L70),
  `crawl-budget-consequences.md` (L78), `redirect-rewrite-rules.md` (L87), `yahoo-japan-rel-nofollow-semantics.md` (L91) — all present.
- evidence bodies: `.ufo/waves/round-56/sources/S367.html` (entry 1 L119), `S419.html` (entry 2 L60) exist and match their
  stated digests/sizes — `sha256sum`/`wc -c`: S367 `0188de9d…` 8051 B, S419 `6172d5d1…` 7428 B, S420 `a860d4f3…` 7332 B, each
  HTTP 200 in `receipts.json`. Entry 3 names **no** body path (see F2).
- recheck local arms, run against the retained bodies: entry 1 grep → 1, entry 2 grep → 1, entry 3 grep → 1.
- index: `corpus/README.md:70-72` and `:100` list all three entries with the right ids and `knowledge/` paths.

## CROSS-LINK CLAIMS:

`yes` = the other file says what the entry says it says; quoted clause is from the other file.

| entry claim (file:line) | other file:line | accurate |
|---|---|---|
| link-target L8 "the lane holds the per-link attribute (`yahoo-japan-rel-nofollow-semantics.md`, S374)" | rel-nofollow:1, :4 "A link attribute is a statement about endorsement, not a crawl refusal" | yes (surface label only; the entry does not reuse S374's superseded endorsement-only gloss — cf. rel-nofollow:52-66) |
| link-target L8-9 "the refusal file at the site root (S372)" | robots-txt-refusal:15 "> \"サイトのルートディレクトリに設置してください\"" | yes |
| link-target L107 "status ground is a Google page on crawl errors (`crawl-error-status-table.md`, S286)" | crawl-error-status-table:1 source URL = troubleshoot-crawling-errors | yes |
| link-target L110-111 "S372 records this operator telling a site without root write access to use a meta tag for index registration refusal" | robots-txt-refusal:99 "> \"「robots.txt」による巡回拒否はできません\"", :103-104 "> \"メタタグで、\"" / "> \"インデックスへの登録拒否を設定してください\"", :95 heading | yes |
| link-target L113-115 "S374 records that the tagged URL is still used to find new pages and that the attribute is not weighed when the result order is decided [S374, S367]" | rel-nofollow:29 "**The URL is still used to find new pages.**", :17 "> \"検索結果の表示順序を決める要素としては考慮されません\"" | yes for S374; the S367 arm is unsupported (F3) |
| deleted L8 "what an error status does to crawling on Googlebot's side (S286)" | crawl-error-status-table:10 "Googlebot will scale back its crawling if it detects that your servers are having trouble" | yes |
| deleted L8 "what a robots block does to the crawl budget (`crawl-budget-consequences.md`, S273/S274)" | crawl-budget-consequences:11 (S273), :13 (S274) | yes |
| deleted L8 "`grep -n -i -E '200\|soft' …` prints only the status-table disclaimer that a soft-404 remedy is not claimed" | ran it: one hit, crawl-error-status-table:14 "A soft-404 remedy is not claimed from this sentence."; crawl-budget-consequences 0 hits | yes |
| deleted L40 "S372 … a site that cannot place robots.txt is told to set index-registration refusal with a meta tag, and that page names no value either" | robots-txt-refusal:95-106, :106 "The page names no tag value and no scope for that substitute [S372]" | yes (wording note, F4) |
| deleted L44 "crawl-error-status-table.md records one admitted Googlebot sentence: crawling is scaled back … (S286)" | crawl-error-status-table:10 | yes |
| deleted L46 "S273 robots block does not hand the spared fetches to other pages unless the capacity limit is already hit; S274 emergency backoff reduces the crawl rate across the whole hostname" | crawl-budget-consequences:11 "Google won't shift this newly available crawl budget to other pages unless Google is already hitting your site's crawl capacity limit", :13 "the backoff reduces your site's crawl rate across the whole hostname" | yes |
| deleted L48 "S374 covers a link-level attribute" | rel-nofollow:4, :17, :29 | yes |
| deleted L48 "`redirect-rewrite-rules.md` covers publisher-side redirect configuration (S050, S135)" | redirect-rewrite-rules:3-4 sources, :13 "## Render static sites (S050)", :33 "## Cloudflare Pages (S135)" | yes |
| deleted L55 "sibling page 存在しないウェブページが巡回される (002857.php, row S420)" | corpus/SOURCES.md:166 (URL 002857.php); receipts.json S420 url | yes |
| nonexistent L8 "the status layer on the Google side (`crawl-error-status-table.md`, S286)" | crawl-error-status-table:1, :10 | yes |
| nonexistent L8 "the refusal file's own rules (`yahoo-japan-robots-txt-refusal-rules.md`, S372)" | robots-txt-refusal:7 title/scope, :12-15 | yes |
| nonexistent L70 "S372 carries the same fallback for a different condition — a site with no root write access for the refusal file" | robots-txt-refusal:95 heading, :99-106 | yes (wording note, F4) |
| nonexistent L78 "`crawl-error-status-table.md` … claims no soft-404 remedy from it" | crawl-error-status-table:14 | yes |
| nonexistent L78 "`crawl-budget-consequences.md` holds Google's budget statements" | crawl-budget-consequences:11, :13 | yes |
| nonexistent L87 "no redirect rule (`redirect-rewrite-rules.md` is a different surface)" | redirect-rewrite-rules:1, :13, :33 | yes |
| nonexistent L91 "No claim about the per-link attribute (`yahoo-japan-rel-nofollow-semantics.md`)" | rel-nofollow:4; entry 3 body contains no rel/nofollow claim | yes |

## FINDINGS:

**F1 — registry reverse links not extended for five reused held rows** (attacks `corpus/SOURCES.md` `used-by` completeness
for the three entries). `used-by` cells at the tip: S372 (line 158) = `rel-nofollow-semantics.md, robots-txt-refusal-rules.md`;
S374 (154) = `rel-nofollow-semantics.md`; S286 (151) = `crawl-error-status-table.md`; S273 (149) and S274 (150) =
`crawl-budget-consequences.md`; S050 (58) = `render-static-sites.md`. None names the new entries that cite the row, and S050
omits `redirect-rewrite-rules.md`, which names S050 as a source at `redirect-rewrite-rules.md:3`. S367 was extended correctly
(base `used-by` = `rel-nofollow-semantics.md` only; at `a450e43`/tip = `rel-nofollow-semantics.md,
yahoo-japan-link-target-crawl-restriction.md`), and S419/S420 (165/166) name their entries. Standard invoked:
`corpus/QUALITY.md:1170-1173` "A held row reused by a new entry changes `used-by` only … each `used-by` change is logged
old→new"; the round-56 contract names only S367 (`contract.md:46`, `:51-52`), so the gap is contract-silent, not
counter-detectable. Routing decision for L1: extend the five cells (and log old→new) or record that cross-citations are not
mirrored. Precedent for the non-exhaustive reading: S011 (line 19) lists two entries while
`robots-txt-refusal-rules.md` also cites S011.

**F2 — entry 3 names no retained-body path** (attacks `yahoo-japan-nonexistent-url-recrawl.md:82`). The quote-classes line
identifies the body only as "the retained body (sha256 `a860d4f3…`, 7332 bytes, HTTP 200 in `receipts.json`)";
`grep -n '\.ufo/'` over the file returns nothing, so `.ufo/waves/round-56/sources/S420.html` is never named, unlike entry 1
(L119) and entry 2 (L60). The bare `receipts.json` is ambiguous lane-wide: 33 files named `receipts.json` are tracked
(`git ls-files '*receipts.json' | wc -l` → 33). Entry 1 has the same bare `receipts.json` (L120) but names its body path in
the same sentence. Path is resolvable via `receipts.json` key S420, so this is a pointer-hygiene defect, not a dangling ref.

**F3 — compound citation `[S374, S367]` over-attributes** (attacks `yahoo-japan-link-target-crawl-restriction.md:113-115`).
The sentence states two facts about the attribute (tagged URL still used to find new pages; not weighed in result order) and
cites both rows. Both facts are S374's (`rel-nofollow-semantics.md:29`, `:17`); the S367 body states neither —
`grep -c` on `.ufo/waves/round-56/sources/S367.html`: `新しいページ` → 0, `表示順序` → 0 — its only connection is the
`archives/002851.php` href (verified present in the body) that the entry itself describes as a pointer at L27-28. Suggested
shape: cite [S374] for the facts, S367 only for the pointer.

**F4 — fallback condition phrasing drifts from the page clause** (low; attacks `yahoo-japan-deleted-url-recrawl.md:40` and
`yahoo-japan-nonexistent-url-recrawl.md:70`). Both call S372's condition "a site that cannot place robots.txt" / "no root
write access for the refusal file". S372's quoted clause is `robots-txt-refusal:99` "「robots.txt」による巡回拒否はできません"
(the mechanism is unavailable), rendered at `:100` as "the mechanism is unavailable, not merely ineffective"; the write-access
cause is S372's own section heading (`:95`) and its registry `teaches` cell, not a quoted page statement. Accurate to the
entry, but the entries read as if the page states the cause.

No finding on: id coverage (all ten ids single-row at both revisions), path existence, body digests/sizes against
`receipts.json`, the three recheck local arms, README index rows, or any of the twenty-one cross-link descriptions except the
three items above.

VERDICT: All cited ids have registry rows and all cited paths exist at `a450e43` and at tip `7ad7db51`; 18 of 21 cross-link descriptions match the other files verbatim, with 3 findings (5 `used-by` cells not extended, entry 3 missing its retained-body path, one over-broad `[S374, S367]` citation) and 1 low-severity wording drift — no dangling reference or wrong description found.
