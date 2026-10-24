# Falsify S012 — attack receipt `rechecks/S012.json` (verdict HOLD)

- Seat: `KakeR26-2.FalsifyS012` (reviewer, leaf member — no dispatch). Axis: **freshness**. Milestone: `r26-recheck-falsify`. Checked 2026-10-21.
- Target: receipt `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-26/rechecks/S012.json` (HOLD, fetchIndex 1) and row line `corpus/SOURCES.md:20` (S012 — sitemaps.org: Sitemaps XML format; teaches «A sitemap's location limits the set of URLs it may include»; anchor «Sitemap file location section; fetched 2026-10-19»).
- Bytes: `.ufo/waves/round-26/fetched/S012-1.raw.gz`; view `.ufo/waves/round-26/fetched/text/S012-1.txt`; provenance `.ufo/waves/round-26/fetched/manifest.json` (S012 entry, lines 243–261) and `.ufo/waves/round-26/population.json` (S012 row).
- Tools: none installed or upgraded this run (Python 3 stdlib, `git`, `gzip`; all already present). Every command was read-only; no corpus, script, lane state, or Git index was mutated. Round-24 material was not read.

## Verdict: AGREE (low) — the HOLD is correct; the receipt needs no correction

I attacked the receipt on all three axes named in the item — (a) does the quote really ground **this** row's `teaches`, (b) is the `anchorObserved` locator correct against the retained raw bytes, (c) did content/version change in a way the receipt missed. All three attacks failed: the source has not drifted by a single byte since the row was opened, the quote is verbatim, unique, and is the *first sentence of the very section the row's anchor names*, and the locator is correct in the raw bytes.

Two non-blocking observations survive (§5): the receipt's only version evidence is an HTTP `Last-Modified` (2022-12-15) that is not the document's own content date (the page footer reads "Last Updated: Monday, November 21, 2016"), and the row's anchor cell "fetched 2026-10-19" is now superseded by this round's 2026-10-21 fetch without any note. Neither creates a false claim; severity **low**, no correction to the receipt is required.

---

## 1. What the row claims (the ground truth I attacked)

`corpus/SOURCES.md:20` (byte-identical at base `97404de` and candidate `e28312b` — `md5sum` of line 20 is `704de0c92ba833e9b1a7a70154ac2420` at both revisions):

```
| S012 | sitemaps.org: Sitemaps XML format — https://www.sitemaps.org/protocol.html | spec | A | Sitemap file location and the URLs it can list | Sitemap file location section; fetched 2026-10-19 | A sitemap's location limits the set of URLs it may include | mined | 2026-10-19 | 365d | corpus/knowledge/crawl-scope-per-host.md |
```

Receipt under attack (`rechecks/S012.json`; byte-identical to the JSON block inside `w1/RowS012.md` — the two parsed objects compare equal):

```json
{"id":"S012","verdict":"HOLD","fetchIndex":1,
 "quote":"The location of a Sitemap file determines the set of URLs that can be included in that Sitemap.",
 "anchorObserved":"Sitemap file location section, heading immediately followed by this sentence (protocol.html, after the 'Other Sitemap formats' section)",
 "reason":"HTTP 200 re-fetch on 2026-10-21 (Last-Modified Thu, 15 Dec 2022) still carries the 'Sitemap file location' heading and the identical first sentence, followed by the same /catalog/ vs /images/ example and protocol/host restriction; scope, anchor and teaches are unchanged and remain supported.",
 "correction":null}
```

---

## 2. Attack A — does the quote really ground THIS row's `teaches`? → NO DEFECT

The row teaches «A sitemap's location limits the set of URLs it may include». The receipt quotes the spec's own first sentence of the "Sitemap file location" section. This is normative body text, not chrome and not a neighbouring clause:

- Raw HTML `fetched/S012-1.raw.gz` (decompressed sha256 `5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654`, 45 292 B, equal to `manifest.json:258-259`), around raw byte **30201** (raw lines 1055–1063):

```html
            <h2>
                <a name="location" id="location"></a>Sitemap file location</h2>
            <p>
                The location of a Sitemap file determines the set of URLs that can be included in
                that Sitemap. A Sitemap file located at http://example.com/catalog/sitemap.xml can
                include any URLs starting with http://example.com/catalog/ but can not include URLs
                starting with http://example.com/images/.</p>
```

- The heading `<a name="location" id="location"></a>Sitemap file location</h2>` is at raw byte **30136** (raw line 1053); the quoted sentence is the **first sentence of the first paragraph of that section** — the tightest possible grounding of the teaches.
- Not chrome: the page's nav/TOC occurrences of the string "Sitemap file location" (raw lines 70 and 124) are jump-links; the section anchor is the only `<h2>`.
- Not boilerplate: the sentence occurs **once** in the raw (`raw.count(b'determines the set of URLs')` → 1) and **once** in the committed text view (`t.count(q)` → 1). The whole-page text view contains it at char index 12164 (file byte 12170; 12167 after the 3-byte BOM).
- Cross-row uniqueness (the counter's `quote_not_row_specific` rule): the quote occurs in **exactly one** of the 34 retained views — `S012-1.txt` alone.
- Quote admissibility under the amendment's rule: 18 whitespace words (≤25) and 18 alphanumeric tokens (≥6). Word-bounded match in the committed view under the counter's own regex `(?<!\w)…(?<!\w)`: **True**.
- The row's `scope` ("Sitemap file location and the URLs it can list") is exactly the section quoted, and the receipt's two corroborating details are real: the `/catalog/` vs `/images/` example (raw byte 30467, raw lines 1060–1063) and the protocol/host restriction (raw byte 31518, raw lines 1099–1104: "all URLs listed in the Sitemap must use the same protocol (http, in this example) and reside on the same host as the Sitemap"). Both are inside the same `#location` section (the next `<h2>`, "Validating your Sitemap", is at raw line 1223).

## 3. Attack B — is the `anchorObserved` locator correct in the retained raw bytes? → NO DEFECT

The locator makes three checkable claims; all three hold against `S012-1.raw.gz`:

1. **"Sitemap file location section"** — the `<h2>` with `name="location" id="location"` at raw byte 30136 / raw line 1053. ✓
2. **"heading immediately followed by this sentence"** — the very next element is the `<p>` whose first sentence is the quote (raw lines 1055–1057, raw byte 30201). ✓
3. **"after the 'Other Sitemap formats' section"** — body heading order is `XML tag definitions` (raw 166) → `Entity escaping` (425) → `Using Sitemap index files` (681) → `Other Sitemap formats` (939) → `Sitemap file location` (1053) → `Validating your Sitemap` (1225). The same order holds in the page's "Jump to:" list (raw lines 68–72). ✓

**No stale-locator defect in this receipt.** Unlike the lane-wide class found on other rows (e.g. `w2/FalsifyS024.md`, `w2/FalsifyS027.md`), the S012 `anchorObserved` cites **no** text-view character offsets, so it cannot be stale; the locator is stated in section/heading terms and is correct against the raw bytes. The receipt's own metadata is therefore self-consistent with the committed view.

**Adjacent, not a receipt defect (already reported by a sibling lane):** the *seat* artifact `w1/PairS012CrawlScopePerHost.md:9` still describes the text view as "21,172 B, one line, sha256 `3dac1076…`" and cites byte offsets (12127, 12105, 12288, 13351, 15996, 18858, 18914, 21108) that do not index the committed file (21 212 B, sha256 `3008775cba806d52e3b4cb846ab066573ad9b3850ac13ccd70c397ce021eaf5b`). I reproduced the seat's numbers exactly from the pre-amendment extractor (`before/source_text.py` + trailing newline → 21 172 B, sha `3dac1076…`), so the seat measured the pre-amendment view. `w1/RowS012.md:8` carries the same staleness ("one minified line (21,165 chars)" — the pre-amendment char count; the committed view is 21 206 chars). `w2/Rejection06S012.md` already logged this class for S012 and correctly assigned it to the seat/text-view owner, not to the receipt. I re-verified it independently so the coordinator has the number: the committed quote sits at byte **12170** (12167 after BOM), **+43 bytes** from the seat's 12127.

## 4. Attack C — did content/version change in a way the receipt missed? → NO DEFECT (zero drift, provable three ways)

**(a) Live GET today is byte-identical to the retained fetch.** One plain public GET of the row URL (documentation GET, in memory only, not saved):

```
url        = https://www.sitemaps.org/protocol.html
status     = 200
last-modified = Thu, 15 Dec 2022 10:54:02 GMT      (unchanged)
live sha256    = 5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654
retained sha256= 5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654
live bytes = 45 292   retained bytes = 45 292   → identical
```

`normalize(text_of(live))` == `normalize(text_of(retained))` → **True**; the live text still contains the quote verbatim and the `#location` heading.

**(b) The receipt's "identical first sentence" is verifiable against the corpus, not just against itself.** The 2026-10-19 readings recorded in the corpus still match the 2026-10-21 bytes after whitespace normalization:
- `corpus/knowledge/crawl-scope-per-host.md:30-31` — "The location of a Sitemap file determines the set of URLs that can be included in that Sitemap." → normalized match **True**.
- `corpus/lessons/round-20.md:214` — same sentence, same anchor "Sitemap file location" → normalized match **True**.
- The entry's dependent claim "It gives `/catalog/sitemap.xml` as including `/catalog/` URLs, not `/images/`" matches the raw prose exactly (the prose uses `/images/`; the separate "not considered valid" example list uses singular `/image/` — the entry quotes the prose, so it is correct).

**(c) The receipt's version evidence is accurate as stated.** `manifest.json:250-259` records `status: 200`, `last-modified: Thu, 15 Dec 2022 10:54:02 GMT`, `etag: "6b6deb8a7310d91:0"`, `bytes: 45292`, and the same sha256 I recomputed over the decompressed gzip (`gunzip -c S012-1.raw.gz | sha256sum` → `5e757059…f471654`; `gunzip -t` OK). The receipt's "HTTP 200 re-fetch on 2026-10-21 (Last-Modified Thu, 15 Dec 2022)" is therefore true, and the page's own footer still reads "Last Updated: Monday, November 21, 2016" (raw line 1511, raw byte 44983) — i.e. **no version drift either**.

**(d) Downstream honesty of the HOLD (does it leave a stale claim behind?).** No:
- `corpus/knowledge/crawl-scope-per-host.md` gained only an append-only `## Round-26 source recheck` section (diff base→candidate: 6 changed lines, 4 added, 0 deleted, original lines byte-preserved).
- That section says S011/S012/S013 "were re-fetched by one public GET each … and judged HOLD at their anchors against the retained bytes" — true (manifest holds exactly one S012 entry, index 1, `fetchedAt 2026-10-21T15:10:39Z`).
- The seat's rejected "STALE" proposal for S012 (row 7, anchor drift at `freshness-sweep.md:58`) is *not* carried into the corpus; `statements.json:118-126` records `seatStale: 1, stale: 0` for S012, and `corpus/lessons/round-26.md:55-57` records the rejection ("anchor drift in pointers explicitly scoped 'at base cb807bc' (S001×3, S005, S011, S012, S013)"). The ledger and the corpus agree (0 `[r26-recheck S012 STALE]` tags in `crawl-scope-per-host.md`, as required for `stale: 0`).
- Ledger consistency for the whole round: `statements.json` totals 276 statements / 8 stale, and the corpus carries exactly 8 `[r26-recheck S0NN STALE]` tags (ghp-etag-anatomy 2, ghp-served-set 2, static-canonical-preflight 4) — matching `corpus/SOURCES.md:79` ("HOLD 32, STALE 0, UNVERIFIABLE 0 at row level", "Knowledge-statement corrections (8)"). All 32 committed receipts are `HOLD` with `correction: null` (I parsed all of them; `Counter({'HOLD': 32})`), and the S012 receipt's key set is exactly the counter's `RECEIPT_KEYS`.

## 5. Findings by severity

**No defect that changes a verdict, a count, a corpus cell, or a counter result.**

- **(low, non-blocking) Version evidence is one-sided.** The receipt's only version datum is the HTTP `Last-Modified: Thu, 15 Dec 2022` — a server file mtime — while the document's own content date is "Last Updated: Monday, November 21, 2016" (raw line 1511). Nothing in the row claims a version (its anchor is "Sitemap file location section; fetched 2026-10-19"), so no stale claim results, and the HOLD is unaffected. Compare the sibling S013 receipt, which explicitly cross-checks the page's *displayed* update pin against the header. Optional one-line addition to the receipt's `reason`: name the page's own "Last Updated: Monday, November 21, 2016" so the 2022 header cannot be read as a content revision. No correction is needed for the receipt to remain valid.
- **(low, non-blocking) The row's retrieval date is superseded but not noted.** `corpus/SOURCES.md:20` still says "fetched 2026-10-19" although this round re-fetched on 2026-10-21 with identical bytes. The contract forbids changing the anchor cell ("SOURCES row cells unchanged except allowed status/recheck/used-by (logged)"), the round log at `corpus/SOURCES.md:79` records the re-check round-wide, and the knowledge entry states that "Older verified-at/reopened dates in this entry remain the historical record of the earlier reading; they are not rewritten." So the corpus is self-consistent; only the row cell reads older than the evidence. No action required; noted so the coordinator is not surprised if the row's `recheck` cell is expected to show a date (it holds the cadence `365d`, as for every other row).
- **(informational, cross-seat, already owned elsewhere)** The `w1/PairS012CrawlScopePerHost.md` / `w1/RowS012.md` text-view size/hash/offset claims are pre-amendment (§3 above); `w2/Rejection06S012.md` already logged this.

## 6. Residual risk and verification gaps

- **Residual risk (low, lane-wide):** the shared extractor `source_text.py` was changed mid-wave and all 34 views were re-extracted, so any receipt or seat report that cites *text-view character offsets* may be stale. The S012 receipt itself is immune (it cites no offsets), but the S012 seat report is not — and I confirmed the seat's numbers are exactly reproducible from `before/source_text.py`, so no live drift is involved. Other rows' receipts are owned by their own falsify seats.
- **Residual risk (low, semantic):** the anchor section also contains the `<h3>` "Sitemaps & Cross Submits" (raw lines 1131–1143, anchor `sitemaps_cross_submits` at raw byte 32821) which documents that a sitemap hosted on another host may serve a host's URLs once ownership is proven through that host's robots.txt. The spec's own prose rule ("must … reside on the same host as the Sitemap", raw line 1100) is what the row and the corpus rely on, and the pair seat already recorded this nuance for the affected statement; no corpus sentence is false and no receipt statement is contradicted. Flagged so that nobody reads the receipt's "protocol/host restriction" as absolute.
- **Verification gaps (honest bounds):** I verified the *row* seat of S012 only. I did not re-adjudicate the knowledge-seat statement ledger for S012 (owned by `w2/Rejection05S011.md` / `w2/Rejection06S012.md`, both AGREE); I only checked that the ledger, the corpus tags, and the appended correction blocks are mutually consistent (they are: `stale: 0` ⇒ 0 tags, 8 tags ledger-wide = 8 in corpus). I did not run `measure.py` (not this leaf's item; the counter is owned by the counter lanes) — instead I applied the counter's own S012-relevant rules by hand: word-bounded quote presence in the effective view (True), 6–25 word/token bounds (18/18), cross-row quote specificity (only `S012-1.txt`), receipt key set (exact), `correction: null` for HOLD (present), manifest sha/bytes match (match).

## 7. Minimal correction

None required. The receipt's verdict, quote, locator, and reason all survive the attack; the candidate's row cell, ledger, and corpus append are mutually consistent. Optional (non-blocking): append the page's own "Last Updated: Monday, November 21, 2016" to the receipt's `reason` so the 2022-12-15 header is not read as a content revision date, and have the S012 seat restate its text-view provenance against the committed view (21 212 B, sha256 `3008775c…`, quote at byte 12170 / 12167 after BOM).

```json
{"target":".ufo/waves/round-26/rechecks/S012.json (S012 receipt, verdict HOLD) + corpus/SOURCES.md:20 row S012","verdict":"AGREE","severity":"low"}
```
