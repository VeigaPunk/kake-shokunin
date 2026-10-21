# FalsifyS024 — attack receipt `rechecks/S024.json` (verdict HOLD)

- Seat: `KakeR26-2.FalsifyS024` (reviewer, leaf — no dispatch). Axis: **freshness**. Milestone: `r26-recheck-falsify`. Checked 2026-10-21.
- Target: receipt `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-26/rechecks/S024.json` (HOLD, fetchIndex 1) and row line `corpus/SOURCES.md:32` (S024 — WHATWG HTML: The base element; teaches «Only the first base element with href supplies the base; later base href values are ignored»; anchor «Section 4.2.3, multiple base href paragraph; Living Standard accessed 2026-10-20»).
- Retained bytes: `.ufo/waves/round-26/fetched/S024-1.raw.gz`; retained view `.ufo/waves/round-26/fetched/text/S024-1.txt`; provenance `.ufo/waves/round-26/fetched/manifest.json`.
- Tooling: none installed or upgraded this run (only `curl`, `python3` stdlib, and repo tools already present). All checks are read-only; no corpus, script, or lane-state mutation.

## Verdict: AGREE (low) — the HOLD stands on freshness; one stale locator in the receipt metadata

The substantive attack failed: the source has not drifted at all (not even one byte since the row was opened), the quote is verbatim and uniquely located inside §4.2.3, and it does ground this row's `teaches`. One **low-severity** defect survives: `anchorObserved` quotes text-view character offsets that no longer match the retained text view, and the range it asserts is not word-bounded against that file.

---

## 1. Did content/version change in a way the receipt missed? — No. Zero drift, provable three ways.

**(a) Live GET today is byte-identical to the retained fetch.** One plain public GET of the row URL's document (`https://html.spec.whatwg.org/multipage/semantics.html`, the row URL's document, fetched in memory only, not saved):

```
$ curl -sS --max-time 45 -D - https://html.spec.whatwg.org/multipage/semantics.html | python3 -c "…"
HTTP/2 200
date: Wed, 21 Oct 2026 16:29:07 GMT
content-type: text/html; charset=utf-8
content-length: 333092
last-modified: Tue, 20 Oct 2026 12:58:32 GMT
etag: "6ad76578-51524"
body bytes 333092 sha256 fd9ae4b6a2e12472ae6f61c52b4ef32751e63f8262cea997d8c6056eba2db959
```

That digest equals the retained bytes and the manifest entry for S024 (`fetched/manifest.json`, `row: S024`, `index: 1`, `status: 200`, `bytes: 333092`, `sha256: fd9ae4b6…2db959`, `last-modified: Tue, 20 Oct 2026 12:58:32 GMT`, `etag: "6ad76578-51524"`). `Last-Modified` is unchanged (20 Oct 2026 12:58:32 GMT) and the retained raw's own masthead still reads `Last Updated <span class=pubdate>20 October 2026</span>`.

**(b) The page is also byte-identical to the original 2026-10-20 read.** `corpus/lessons/round-22.md` and `.ufo/waves/round-22/w1/Case06.md:388` record the round-22 fetch digest for this exact document:

> `| S024 | WHATWG HTML §4.2.3, https://html.spec.whatwg.org/multipage/semantics.html#the-base-element | "If there are multiple base elements with href attributes, all but the first are ignored." | fd9ae4b6a2e12472ae6f61c52b4ef32751e63f8262cea997d8c6056eba2db959 (html-semantics.html) |`

with `Case06.md:382` stating “Primary, opened this session, access date 2026-10-20”. The digest at the original access date is the digest served today. The row's `accessed 2026-10-20` therefore still pins the live bytes exactly — stronger than the receipt's date-level argument (“Last-Modified date equals the access date”). No version or content drift exists that the receipt missed.

**(c) The fragment still resolves and the section number is unchanged.** In the retained raw (`gzip -c` → 333,092 bytes) the anchor element is present verbatim:

```
raw offset 33386: <h4 id=the-base-element><span class=secno>4.2.3</span> The <dfn …><code>base</code></dfn> element…
```

so `…/semantics.html#the-base-element` still lands on §4.2.3, and the row's “Section 4.2.3” label is correct in the live bytes too (identical bytes).

## 2. Does the quote ground THIS row's `teaches`, or is it page chrome / a neighbouring clause?

It grounds it, and it is uniquely located inside the section.

- **Not chrome, not a neighbour.** The sentence is a `<p class=note>` *inside* §4.2.3, not page furniture: the note starts at raw offset **42408**, the section heading `<h4 id=the-base-element>` is at **33386**, and the next `<h4>` (secno **4.2.4 The link element**) is at **53543** → `33386 < 42408 < 53543`. There is exactly one such note (`h.count('<p class=note>If there are multiple <code id=the-base-element:the-base-element-6>')` → 1) and exactly one occurrence of the sentence in the raw and in the text view (count → 1 each).
- **Verbatim.** Raw (tags stripped) reads exactly: `If there are multiple base elements with href attributes, all but the first are ignored.` — identical to `rechecks/S024.json` `quote`, and to `corpus/lessons/round-22.md:47`.
- **It is a note, but the same section supplies the normative backing the receipt claims.** In §4.2.3 itself: “There must be no more than one `base` element per document.” (text-view offset 9795; raw offset ≈41079) and, at raw offset 45876, “A `base` element that is the **first `base` element with an `href` content attribute** in a document tree has a **frozen base URL**”, with the frozen-base-URL trigger list specifying “the first `base` element **in tree order** with an `href` content attribute in its Document”. That is exactly the row's concept column (“First base href in document tree order”) and exactly what the receipt's `reason` asserts.
- **The `teaches` wording is faithful, not over-stated.** “Only the first base element with href supplies the base; later base href values are ignored” = the note’s “all but the first are ignored” + the frozen-base-URL rule (only the first `base` with `href` in a document tree ever has a frozen base URL, so later `href` values cannot affect the document base URL). Round-22 additionally pinned the companion algorithm “return the frozen base URL of the first such base element in tree order” (`urls-and-fetching.html#document-base-urls`, digest `6df35203…650def` in `Case06.md`), which is the same rule seen from the document-base-URL side. **Strongest counterexample tried:** the note is non-normative, so maybe `teaches` rests on a non-normative restatement. It does not: the normative “first base element with href in tree order → frozen base URL” prose is in the same section and is quoted in the receipt’s `reason`. No over-claim found.

## 3. Falsify the anchor as recorded — LOW-severity defect found

`rechecks/S024.json` `anchorObserved` says:

> “§4.2.3 The base element, note paragraph on multiple base href (**text-view char offsets 10160-10248**; **§4.2.3 heading at offset 8390**; raw `<h4 id=the-base-element><span class=secno>4.2.3</span>`)”

The **raw-bytes** half is accurate (see §2). The **text-view offsets** are stale: against the retained view `fetched/text/S024-1.txt` the quote occupies **10172–10260** (88 chars) and the body heading `4.2.3 The base element` is at **8398** (the first occurrence, 296, is the table-of-contents entry).

```
$ python3 -c "t=open('fetched/text/S024-1.txt',encoding='utf-8').read(); …"
quote span 10172 10260
'4.2.3 The base element' occurrences -> 296 (TOC), 8398 (body)
text[10160:10249] == 'aking URLs. If there are multiple base elements with href attributes, all but the first a'
```

So the asserted range starts mid-word (`aking` of “taking”) and ends mid-word (`a` of “are”), i.e. it is **not** word-bounded and does **not** contain the full quote, contrary to `w1/RowS024.md` caveat 2 (“quote is at 10160-10248 and is contiguous and word-bounded in fetched/text/S024-1.txt”). The same staleness hits that caveat’s file-size claim: it states “96,598 bytes, 96,469 chars”; the retained file is **96,642 bytes / 96,513 chars** (`wc -c` → 96642).

**Root cause (evidence, not speculation).** The retained text view was regenerated *after* the offsets were measured and *before* the receipt was written:

```
$ stat -c '%y %n' fetched/text/S024-1.txt source_text.py w1/RowS024.md rechecks/S024.json
2026-10-21 13:02:14 fetched/text/S024-1.txt
2026-10-21 13:02:13 source_text.py
2026-10-21 12:29:31 w1/RowS024.md
2026-10-21 13:04:31 rechecks/S024.json
```

`source_text.py` changed at 13:02:13 and the text views were re-extracted at 13:02:14; `w1/RowS024.md` (12:29:31) measured the **older** view, and `rechecks/S024.json` (13:04:31) inherited its offsets without re-measuring. The current file is self-consistent with the current extractor (`source_text.text_of(load_gz('fetched/S024-1.raw.gz'))` → 96,512 chars, equal to the file minus one trailing newline; quote at 10172 in both). I could not reproduce the old offsets with any normalization variant of the current extractor (tried: current `A` → quote 10172 / 96,512 chars; split-only `B` → 10247 / 97,140; space-after-paren `C` → 10247 / 97,130; space-before-punct `D` → 10172 / 96,522) — none yields 96,469 chars / 10160, so the old view was produced by a materially different extractor, and the stale numbers are structural, not a rounding artefact.

**Minimal correction** (metadata only — no corpus text, no verdict change, no `correction` field needed):

> `anchorObserved`: “§4.2.3 The base element, note paragraph on multiple base href (text-view char offsets **10172-10260**; §4.2.3 heading at offset **8398**; raw `<h4 id=the-base-element><span class=secno>4.2.3</span>`)”

and, in `w1/RowS024.md` caveat 2, “96,598 bytes, 96,469 chars” → “96,642 bytes, 96,513 chars”. The quote string, the section label, the raw locator, the `HOLD` verdict, and `correction: null` all stand as they are.

## 4. Residual risk / verification gaps

- **Residual risk (low, lane-wide, not row-specific):** because the shared extractor `source_text.py` was edited mid-wave and every text view was re-extracted at 13:02:14, *any* receipt whose `anchorObserved` cites text-view character offsets may be stale in the same way. S024’s is; whether other rows’ are, is outside this leaf’s scope (other Falsify seats own their rows).
- The offsets are a **locator convenience only**: the quote, section, and raw-bytes anchor all verify independently, so no ledger statement, corpus lesson, or counter result is affected.
- **Verification gaps:** (i) I did not GET `urls-and-fetching.html#document-base-urls` (it is not a `corpus/SOURCES.md` row URL), so the companion algorithm quote “return the frozen base URL of the first such base element in tree order” is taken from the round-22 record rather than re-read today; the in-section frozen-base-URL prose was re-read and does confirm the same rule. (ii) I did not fetch the `#the-base-element` fragment URL itself (the fragment is client-side only); the section id was confirmed in the byte-identical document.

## 5. Bottom line

The freshness attack fails: the document served today is byte-for-byte the document read on 2026-10-20 (sha256 `fd9ae4b6…2db959`), the §4.2.3 anchor and the multiple-base-href note are unchanged and unique, and the note plus the section’s normative frozen-base-URL prose do ground the row’s `teaches`. The receipt’s `HOLD` is correct. The only actionable item is the stale text-view offsets in `anchorObserved` (and the matching stale size claim in `w1/RowS024.md` caveat 2), correctable by restating `10172-10260` / `8398` / `96,642 bytes, 96,513 chars`.

```json
{"target":".ufo/waves/round-26/rechecks/S024.json","verdict":"AGREE","severity":"low"}
```
