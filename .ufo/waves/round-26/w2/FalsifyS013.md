# Falsify S013 — round-26 C1 freshness recheck (receipt HOLD)

Seat: `KakeR26-2.FalsifyS013` (leaf member — no subagent dispatch). Milestone `r26-recheck-falsify`. Axis: **freshness**.
Target: `.ufo/waves/round-26/rechecks/S013.json` (verdict HOLD) and the SOURCES row `corpus/SOURCES.md:21`.

Goal: try to show the receipt is WRONG — (a) the quote does not ground this row's `teaches` (page chrome / neighbouring clause instead), (b) the `anchorObserved` is mislocated in the raw bytes, (c) content or version changed in a way the receipt missed.

**Verdict: AGREE** — the receipt survives every falsification attempt I ran. Severity of residual observations: **low**; **no change to the receipt or to any corpus byte is required**.

## The row and the receipt under attack

`corpus/SOURCES.md:21` — byte-identical at base `97404de4` and candidate `e28312b1` (the only SOURCES.md delta in this round is the appended round-26 note at lines 79-80):

```
| S013 | Google Search Central: Build and submit a sitemap — https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap | docs | A | Google's sitemap-location and metadata handling | Sitemap best practices; last updated 2026-07-08 UTC | Unless submitted through Search Console, Google applies a sitemap only to descendants of its parent directory | mined | 2026-10-19 | 90d | corpus/knowledge/crawl-scope-per-host.md |
```

- teaches: *“Unless submitted through Search Console, Google applies a sitemap only to descendants of its parent directory”*
- anchor: *“Sitemap best practices; last updated 2026-07-08 UTC”* — two named coordinates (a section, a date pin).
- scope: *“Google's sitemap-location and metadata handling”*.

Receipt under attack (`.ufo/waves/round-26/rechecks/S013.json`, 9 lines / 810 B; sha256 `cf170d92029c68e07e4f9f26fd96e8f56f03471dc0c5680044bf7f0a25e696c8` — identical in the worktree and as the blob at `e28312b1`):

```json
{"id":"S013","verdict":"HOLD","fetchIndex":1,
 "quote":"unless you submit your sitemap through Search Console, a sitemap affects only descendants of the parent directory",
 "anchorObserved":"Build and submit a sitemap > 'Sitemap best practices' heading, paragraph 'Sitemap file encoding and location'; footer 'Last updated 2026-07-08 UTC'",
 "reason":"The teaches sentence is reproduced verbatim in the current page's 'Sitemap file encoding and location' paragraph, so the parent-directory scope rule is unchanged. The anchor heading is still present and the displayed update pin is still 2026-07-08 UTC (echoed by HTTP Last-Modified 2026-07-08 15:47:49 GMT), so scope (sitemap location plus metadata handling, e.g. lastmod, priority/changefreq ignored) still holds.",
 "correction":null}
```

## Attack 1 — Does the quote ground THIS row's `teaches` (not page chrome, not a neighbouring clause)? → NO DEFECT

Retained bytes `fetched/S013-1.raw.gz` decompress to **191 341 B, sha256 `492e22cf133333d6202bbfd6c47370eac981612d7952b1e851d31e06dd78920b`** — the same digest recorded in `fetched/manifest.json` (row S013, index 1) and pinned in `.ufo/waves/round-26/population.json` (S013 → `fetches[0].sha256` = same, `file` = `fetched/S013-1.raw.gz`). The committed blob at `e28312b1` for that path hashes `62979b08bb9c22aa0aa26fa720b804f48224c10453334864aae5d5dee502f124`, identical to the worktree file.

The quote is real body prose, in the **main content**, in the exact section the row's anchor names:

- `<main` at 131571, `<article` at 132374, `<devsite-content>` at 132319 → the quote is **not** nav/sidebar chrome.
- The enclosing section is `<h2 id="general-guidelines" data-text="Sitemap best practices" tabindex="-1">Sitemap best practices</h2>` at **141784**; the next `<h2>` is `id="xml"` (“XML sitemap”) at **144431** → the quote at **143000** sits inside “Sitemap best practices”, which is the anchor's own section name. The document has exactly 8 `<h2>`s; “Sitemap best practices” occurs only at 141823/141861 (the same tag's `data-text` and its text node), so the anchor resolves uniquely.
- The paragraph itself (raw bytes 142756–143270) reads:

```html
<p>
  <b>Sitemap file encoding and location:</b>
  The sitemap file must be UTF-8 encoded. You can host your sitemaps anywhere on your site, but
  unless you submit your sitemap through <a href="#addsitemap">Search Console</a>, a sitemap
  affects only descendants of the parent directory. Therefore, a sitemap posted at the site root
  can affect all files on the site, which is where we recommend posting your sitemaps.
</p>
```

So the quote is a contiguous, verbatim slice of the sentence that carries the row's whole teaches claim — not page chrome, not a neighbouring clause, and not the second half (“a sitemap posted at the site root can affect all files on the site”), which the receipt does not need. The word “descendants of the parent directory” occurs **once** in the whole 191 341-byte document (offset 143000), so there is no second, contradicting instance.

Counter-rule replay (`measure.py:386-392`): `tokens = len(re.findall(r"[^\W_]+", quote)) = 17 ≥ 6`; `words = len(quote.split()) = 17 ≤ 25` → passes `quote_word_count`; `quote_in_text` under the counter's own `normalize` + `(?<!\w)…(?!\w)` rule → **match** in the effective fetch text. Row specificity (contract-amendment: a decided quote must not occur in another row's text): scanning all 34 committed text views `fetched/text/*.txt` for the quote returns **only `S013-1.txt`** → `quote_not_row_specific` cannot fire.

## Attack 2 — Is `anchorObserved` correct in the raw bytes? → NO DEFECT

Every locator in `anchorObserved` was checked against the decompressed retained bytes (0-based offsets):

| claim | raw evidence | verdict |
|---|---|---|
| “Build and submit a sitemap” | `<h1>` at 137486, text `Build and submit a sitemap`; `<title>` = `Build and Submit a Sitemap \| Google Search Central \| Documentation \| Google for Developers` | ✓ |
| “'Sitemap best practices' heading” | `<h2 id="general-guidelines" data-text="Sitemap best practices">` at 141784; unique in the document | ✓ |
| “paragraph 'Sitemap file encoding and location'” | `<b>Sitemap file encoding and location:</b>` at 142756, the bold lead-in of the `<p>` that contains the quote at 143000 | ✓ |
| “footer 'Last updated 2026-07-08 UTC'” | `<devsite-content-footer>` opens at 159576; `<p>Last updated 2026-07-08 UTC.</p>` at **160117**; the same pin repeats in the page's own metadata blob `devsite-content-data` at 161557 | ✓ |

The row's two anchor coordinates therefore both still resolve: section “Sitemap best practices” (141784) and the date pin “Last updated 2026-07-08 UTC” (160117).

## Attack 3 — Did content or version change in a way the receipt missed? → NO DEFECT

1. **Independent live GET** of the URL already in `corpus/SOURCES.md` (one plain GET, `curl 8.23.0` / OpenSSL 3.6.5, 2026-10-21 ~16:29 UTC, ~79 min after the wave's 15:10:40Z fetch): body **191 337 B, sha256 `eaa0c738e61f5372bff63eb8f6a323996ffa78fbb0d4a653a6966d67354d28ec`**; HTTP `last-modified: Wed, 08 Jul 2026 15:47:49 GMT` — identical to the retained manifest's header. The 4-byte size delta is devsite chrome only: the **content region `<main>`…`<devsite-content-footer>` is byte-identical** to the retained bytes (28 006 B == 28 006 B, `region identical: True`). Every diff hunk outside that region is devsite feature-flag/analytics attribute churn (`MiscFeatureFlags__…`, `data-category` attribute ordering, an analytics `dimension6` key), i.e. no editorial content.
2. **Version semantics unchanged.** The page's own pin “Last updated 2026-07-08 UTC” (160117) and the HTTP `Last-Modified` (2026-07-08 15:47:49 GMT) both still read exactly what the corpus recorded at the 2026-10-19 opening (`corpus/knowledge/crawl-scope-per-host.md:2` — “Google docs updated 2026-07-08”; `corpus/lessons/round-20.md:215` — “page last updated 2026-07-08 UTC”). No version bump to miss.
3. **Content pinned at the fetch.** Manifest row S013/index 1: `status 200`, `error null`, `bytes 191341`, `sha256 492e22cf…78920b`, `last-modified: Wed, 08 Jul 2026 15:47:49 GMT`, `fetchedAt 2026-10-21T15:10:40.699115+00:00`. `manifest-retry.json` contains **no S013 record** (its only row is S008), so the effective fetch is the one the receipt cites. Population pin == manifest pin == decompressed digest ✓.
4. **Text view is faithful.** Regenerating `fetched/text/S013-1.txt` from the retained bytes with the committed `.ufo/waves/round-26/source_text.py` reproduces the committed view exactly (`regen == stored.rstrip('\n')` → `True`; the only delta is the file's trailing newline). I ran this over **all 34 committed views**: every one reproduces (`views NOT reproducible … : []`). So the view the receipt was judged against is a faithful rendering of the retained bytes.
5. **Receipt shape and counter verdict.** Exactly the 7 required keys (`id, verdict, fetchIndex, quote, anchorObserved, reason, correction`), `id == "S013"`, `verdict == "HOLD"`, non-empty `reason` and `anchorObserved`, `correction: null` (required for HOLD by `measure.py:396-398`), `fetchIndex 1` = the row's only population fetch. Re-running the wave counter read-only (`python3 -B .ufo/waves/round-26/measure.py --root . --revision e28312b1…`) gives **decided 32 / hold 32 / stale 0 / unverifiable 0, statements 276, statementsStale 8, statementCorrections 8, findings `[]`, exit 0**; the base revision gives **decided 0, findings `['receipts_absent']`, exit 1** — matching the wave's stated before/after.
6. **No correction owed for this row.** `statements.json` records S013 → `crawl-scope-per-host.md`, `statements 14, seatStale 1, stale 0`; `grep -rn "\[r26-recheck S013 STALE\]" corpus/` → no match, and none is required (`stale == 0`). The corpus entry's own round-26 tail (`corpus/knowledge/crawl-scope-per-host.md:57`) and the S013 line in `corpus/lessons/round-26.md:36` reproduce the receipt's quote and anchor verbatim.

## Findings

No finding changes the HOLD verdict. Two low-severity precision notes, both confined to the receipt's `reason` prose (no corpus byte, no counter finding, no verdict impact):

**F1 (low) — the `reason` parenthetical mis-groups `<lastmod>` with the ignored tags.** The receipt says scope holds “*e.g. lastmod, priority/changefreq ignored*”. The retained bytes say the opposite for `<lastmod>` (raw 146088 and 146246): “**Google ignores `<priority>` and `<changefreq>` values. Google uses the `<lastmod>` value if it's consistently and verifiably (for example by comparing to the last modification of the page) accurate.**” A reader of the receipt alone can take “lastmod … ignored” as a claim that Google discards `<lastmod>`; the source says Google *uses* it when it is verifiably accurate. The seat's own caveats got this right (`w1/RowS013.md`: “Scope 'metadata handling' is covered on-page by lastmod use and by Google ignoring priority/changefreq; unchanged”), so the receipt's compression is the only place the distinction is lost. **Minimal correction (optional, receipt text only):** replace “e.g. lastmod, priority/changefreq ignored” with “e.g. priority/changefreq ignored and `<lastmod>` used when verifiably accurate”. No corpus statement depends on this detail — `grep -rn "lastmod\|priority\|changefreq" corpus/knowledge/ corpus/lessons/` finds no sitemap-metadata claim, so nothing in the corpus inherits the ambiguity.

**F2 (low) — “the teaches sentence is reproduced verbatim” is imprecise about which sentence is verbatim.** The SOURCES `teaches` cell is a **paraphrase** (“Google applies a sitemap only to descendants of its parent directory”); the verbatim text is the receipt's own `quote` (“…a sitemap affects only descendants of the parent directory”). The page's wording is *affects*, not *applies*. Every registry `teaches` cell is a paraphrase, so this is a wording issue in the receipt's justification, not a fidelity defect in the row.

## Residual risk / scope-completeness observation (no verdict impact)

**R1 — the page names two submission routes for cross-site hosting; the corpus clause names one.** The “Sitemap best practices” rule the receipt pins is scoped by its own sentence: “*You can host your sitemaps anywhere on your site*, but unless you submit your sitemap through Search Console, a sitemap affects only descendants of the parent directory.” The same page's *“How to cross-submit sitemaps for multiple sites”* section (h2 `id="cross-submit"` at 153979) says: “**To submit cross-site sitemaps that are hosted in a single location, you can either use Search Console or robots.txt**” (raw 155823), and then demonstrates hosting site B's sitemap at `https://sitemaps.example.com/sitemap-example-com.xml` and referencing it from `https://example.com/robots.txt` (raw 156934-158000) — a sitemap that affects another site's URLs, i.e. URLs outside its own parent-directory descendants, without Search Console submission. The corpus clause at `corpus/knowledge/crawl-scope-per-host.md:16` — “unless submitted through Search Console, a sitemap affects only URLs under its parent directory” — therefore states the best-practices rule as if Search Console were the sole escape; the entry's next sentence does name the robots.txt route (“A `Sitemap:` line in the host-root robots file is a supported discovery route”, grounded at raw 153320/153469) but frames it as discovery only. **This is not a freshness defect and does not touch the receipt's verdict:** the bytes are identical to the base reading (the whole page is byte-identical between the retained 2026-10-21 fetch and my live 2026-10-21 GET, and the page's own pin is still 2026-07-08), and no statement was adjudicated STALE for S013 (`statements.json`: `stale 0`). I flag it because the row's `teaches` cell inherits the same narrowing, and a reader modelling cross-site hosting from it alone would miss the robots.txt route the very same page documents. Routed to the statement seat, not to this lane.

## Verification gaps / limits of this attack

- I could not diff against a *retained 2026-10-19* body: no bytes from that date exist in the lane. “Unchanged since the row's 2026-10-19 opening” rests on (a) the page pin and HTTP `Last-Modified` still reading 2026-07-08, (b) the corpus's own 2026-10-19 record of the same sentence and date (`crawl-scope-per-host.md:2`, `:33-35`; `lessons/round-20.md:215`), and (c) the live content region being byte-identical to the retained 2026-10-21 bytes. All three agree.
- The cross-submission carve-out (R1) is a *scope-completeness* question about the corpus clause and the row's `teaches` cell; it is not a statement the round-26 ledger adjudicated, and it is unchanged since base, so I did not treat it as stale.
- Per the lane bounds I did not read, run, retry or re-route round-24 material, did not probe any property, used no browser or account, and touched no corpus byte, script, fleet repo, sibling lane, or the lane Git index/jj. The only file I wrote is this report.

## Tooling

No tools installed or upgraded; no pacman/uv/cargo/npm transaction (host-wide pacman pause untouched). Used, all pre-installed: `curl 8.23.0` (OpenSSL 3.6.5, zlib 1.3.2), `python3 3.14.8`, `gzip 1.15`, `git 2.56.0` (read-only: `show`, `cat-file`, `diff`, `ls-tree`, `status`, `log`). Python was invoked with `-B` for the counter runs. `importlib` module loads of the committed `source_text.py` can emit untracked bytecode caches under `.ufo/waves/round-26/__pycache__/` and `.ufo/waves/round-26/before/__pycache__/` (dated 13:54:16 / 13:54:59, inside this wave's activity window); no tracked file was added, changed or deleted (`git status --porcelain` shows only untracked entries), and I left those caches untouched rather than mutate the wave tree further.

**Bound-compliance disclosure (two deviations, both self-corrected).** (1) My first live GET wrote the body and headers to `/tmp/s013_live.html` and `/tmp/s013_headers.txt`; the lane bound says never write outside my report and keep scratch in memory. I deleted both files immediately (`ls: cannot access '/tmp/s013_live.html': No such file or directory`) and redid the comparison in memory via `urllib`; the pre-existing `/tmp/s013*.out`, `/tmp/s013.html` and `/tmp/s013probe/` entries in that directory are other lanes' files from 2026-10-20/21 00:5x, not mine. (2) The `importlib` loads named above can leave untracked `__pycache__` bytecode caches in the wave directory. No corpus byte, script, fleet repo, sibling lane, or Git index/jj was touched.

```json
{"target":".ufo/waves/round-26/rechecks/S013.json","verdict":"AGREE","severity":"low"}
```
