# FalsifyS025 — attack receipt `rechecks/S025.json` (verdict HOLD)

- Seat: `KakeR26-2.FalsifyS025` (reviewer, leaf — no dispatch). Axis: **freshness**. Milestone: `r26-recheck-falsify`. Checked 2026-10-21.
- Target: receipt `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-26/rechecks/S025.json` (HOLD, fetchIndex 1) and row line `corpus/SOURCES.md:33` (S025 — WHATWG HTML: The template element; teaches «Template contents are not children of the template element itself and do not supply document-head canonical links»; anchor «Section 4.12.3, template contents paragraph; Living Standard accessed 2026-10-20»).
- Retained bytes: `.ufo/waves/round-26/fetched/S025-1.raw.gz`; retained view `.ufo/waves/round-26/fetched/text/S025-1.txt`; provenance `.ufo/waves/round-26/fetched/manifest.json` (`row: S025`, `index: 1`, `status: 200`, `bytes: 276128`, `sha256: 5854951b…9abe43`, `last-modified: Tue, 20 Oct 2026 12:58:32 GMT`, `etag: "6ad76578-436a0"`, `fetchedAt: 2026-10-21T15:10:47Z`).
- Tooling: **no tool installed or upgraded this run** (Python 3.14.8 stdlib only — `urllib`, `gzip`, `hashlib`, `importlib.util`, `json`, `re`; `git` for revision reads). Channel: none — no install was needed. All checks read-only; no corpus, script, lane-Git or jj mutation; only this report file was written.

## Verdict: DISAGREE (low) — the HOLD conclusion is right, but the receipt's `anchorObserved` misstates where its anchors are, and the raw half names the wrong element

The **freshness** attack failed: the document served today is byte-for-byte the document read on 2026-10-20, the quote is verbatim and unique inside §4.12.3, and it does ground this row's `teaches`. The **locator** attack succeeded: both coordinate halves of `anchorObserved` are wrong against the artifacts they name, and the raw half is wrong in kind, not only by a shift — byte 211509 is not a `<p>` at all.

Minimal correction is metadata-only (restated at §5): `verdict` (HOLD), `quote`, `reason` and `correction` (`null`) all stand.

---

## 1. Did content/version change in a way the receipt missed? — No. Zero drift, provable three ways.

**(a) Live GET today is byte-identical to the retained fetch.** One plain public GET of the row URL's document (`https://html.spec.whatwg.org/multipage/scripting.html`, the row URL's document; fetched in memory only, not saved):

```
status 200  len 276128  last-modified Tue, 20 Oct 2026 12:58:32 GMT  etag "6ad76578-436a0"
live     sha256 5854951bbabbdca6b5ea365edd1e2f14e342bc51e77353469d21e46f859abe43
retained sha256 5854951bbabbdca6b5ea365edd1e2f14e342bc51e77353469d21e46f859abe43
bytes identical: True
```

`Last-Modified`, `etag` and `content-length` are unchanged from `fetched/manifest.json`. The retained raw's own masthead still reads `Last Updated <span class=pubdate>20 October 2026</span>` (raw offset 1374), so the living-standard generation behind the row's `accessed 2026-10-20` is the generation served today.

**(b) The document is also byte-identical to the original 2026-10-20 read — so the row's access date pins the live bytes exactly.** `.ufo/waves/round-22/w1/HTMLTemplate.md:10-17` records the round-22 fetch of this same URL:

> `- Access date: 2026-10-20` … `- Fetch provenance: 276,128 bytes, sha256 5854951bbabbdca6b5ea365edd1e2f14e342bc51e77353469d21e46f859abe43`, scratch copy `/tmp/r22-scripting.html` (outside the lane).`

That scratch copy still exists and is byte-identical to the round-26 retained bytes:

```
r22 vs r26 retained identical: True  5854951bbabbdca6b5ea365edd1e2f14e342bc51e77353469d21e46f859abe43
```

Stronger than the receipt's date-level argument ("Last-Modified date equals the access date"): the *content* digest recorded at the original access date is the content digest served today. No content or version drift exists that the receipt missed.

**(c) The section number and the fragment anchor are unchanged.** In the retained raw, the section heading is byte-identical to the live bytes:

```
raw 194041: <h4 id=the-template-element><span class=secno>4.12.3</span> The <dfn data-dfn-type=element><code>template</code></dfn> element<a href=#the-template-element class=self-link></a></h4>
```

`<span class=secno>4.12.3</span>` occurs exactly twice in the file (TOC at 2736, body at 194069), so §4.12.3 is still “The template element” and the URL fragment `#the-template-element` still resolves into it. The quoted paragraph sits inside that section (`194041 < 211372 < 251073`, next `<h4>` = §4.12.4 “The slot element”).

## 2. Does the quote ground THIS row's `teaches`, or is it page chrome / a neighbouring clause?

It grounds it, and it is uniquely located inside the section.

- **Not chrome, not a neighbour.** The sentence is the body of a standalone `<p>` inside §4.12.3: opening tag at raw **211372** (`<p>The <a href=#template-contents id=the-template-element:template-contents>template contents</a> of a <code …>template</code> element <a href=syntax.html#template-syntax>are not children of the element itself</a>.`), closing `</p>` at **211665**. The immediately following block is the note at **211673** (`<p class=note>It is also possible, as a result of DOM manipulation…`). The receipt's structural description — “template contents paragraph after the shadowroot* content-attribute paragraphs” — is verified: the `shadowrootcustomelementregistry` / `shadowrootclonable` / `shadowrootslotassignment` attribute paragraphs occupy raw 200471–211226, i.e. they precede the quoted paragraph, which follows them.
- **Verbatim and unique.** The full sentence occurs **once** in the raw (`raw.count(b'are not children of the element itself')` → 1) and **once** in the retained view; and the phrase “not children of the element itself” occurs in **no other** retained view of the round-26 population (`fetched/text/*.txt` scan → only `S025-1.txt`). The quote matches `corpus/lessons/round-22.md:48` and the `[r23-correction]` paraphrase in `corpus/knowledge/static-canonical-preflight.md:143-146`.
- **The teaches' first clause is the sentence itself** (“Template contents are not children of the template element itself”). The second clause (“do not supply document-head canonical links”) is *entailed*, not literally on the page — and the entailment is supplied by the same section, in the same retained bytes:
  - “The p element in the template is not a child of the template in the DOM; it is a child of the DocumentFragment returned by the template element's content IDL attribute.” (view offset 63489)
  - “Create a DocumentFragment object whose node document is document and host is the template element.” (view 64577)
  - “its browsing context is null” (view 65122) and “so that they aren't in a browsing context and thus remain inert (e.g. scripts do not run)” (view 65649)
  - content model: raw **198832** `Content model:` → `Nothing (for clarification, …)`, inside §4.12.3's info box (`194041 < 198832 < 251073`).
  So the receipt's `reason` — “the section's template content model is still Nothing and the contents remain a DocumentFragment owned by the inert template-contents owner document with null browsing context, so links written inside template contents sit outside the document tree and cannot supply a document-head canonical” — is each clause present in the retained bytes. **No drift, no over-statement beyond the entailment the corpus already bounds to static input bytes** (`corpus/knowledge/static-canonical-preflight.md:143-146`: “it holds for the static input bytes only, not for script-cloned template content”). The `90d` cadence on `corpus/SOURCES.md:33` is unchanged and appropriate for a living standard.
- **Counter-attacks tried and failed.** (i) *Is the quote page chrome?* No — it is a normative-content paragraph inside the element's own section. (ii) *Is it a neighbouring clause standing in for the real rule?* No — the real rule (DocumentFragment ownership, inert owner document) is in the same section and the same retained bytes. (iii) *Did the spec renumber the section, so the row's “Section 4.12.3” label is stale?* No — secno 4.12.3 is the body heading at raw 194041 in the bytes served today. (iv) *Does the quote still occur only once, i.e. is it row-specific enough to ground this row?* Yes (1 in raw, 1 in the view, 0 elsewhere in the population).

## 3. Falsify the anchor as recorded — LOW-severity defect found (two coordinate halves, both wrong)

`rechecks/S025.json:6` `anchorObserved` says:

> “§4.12.3 The template element — template contents paragraph after the shadowroot* content-attribute paragraphs; **text view S025-1.txt line 1 at offset 62596**; **raw `<p>` at byte 211509** under `<h4 id=the-template-element>` (secno 4.12.3)”

### 3.1 The text-view offset does not point at the quote

Against the **committed** retained view `fetched/text/S025-1.txt` (79,117 bytes, one LF-terminated line), the quoted sentence occupies **char 62638–62720** (83 chars) / **byte 62755–62837**:

```
quote char offset in committed view : 62638   (byte 62755, file len 79117)
committed[62596:62640] : b'he Named state. The shadowrootcustomelementregistry conte'
committed[62638:62721] : b'tent attribute is a boolean attribute. The shadowrootcustomelementregistry content '
```

So the stated 62596 lands **42 characters before** the sentence, inside the tail of the *preceding* `shadowrootcustomelementregistry` sentence (“…are both the Named state.”). It is not word-bounded and does not contain the quote. The same off-by-42 is reproduced exactly by the **pre-amendment** extractor retained at `before/source_text.py`:

```
old extractor (before/source_text.py) quote@ 62596
new extractor (source_text.py)        quote@ 62638
committed fetched/text/S025-1.txt    quote@ 62638
old[62596:62679] = 'The template contents of a template element are not children of the element itself.'
```

**Root cause (evidence, not speculation).** The shared extractor was edited and every text view was re-extracted *after* the offsets were measured and *before* the receipt was written:

```
$ stat -c '%y  %n' source_text.py before/source_text.py fetched/text/S025-1.txt w1/RowS025.md rechecks/S025.json
2026-10-21 13:02:13  source_text.py
2026-10-21 13:02:13  before/source_text.py
2026-10-21 13:02:14  fetched/text/S025-1.txt
2026-10-21 12:29:45  w1/RowS025.md
2026-10-21 13:04:31  rechecks/S025.json
```

`w1/RowS025.md` (12:29:45) measured the *older* view; `rechecks/S025.json` (13:04:31) inherited its coordinates without re-measuring. The committed file is self-consistent with the committed extractor (`source_text.text_of(load_gz('fetched/S025-1.raw.gz'))` → 78,975 chars = file minus the trailing LF; quote at 62638 in both).

### 3.2 The raw byte does not point at a `<p>` — it points inside an id attribute

The receipt says the paragraph is the “raw `<p>` at byte 211509”. It is not:

```
raw[211509:211512] = b'tem'      is <p>? False
raw <p> opening the quote paragraph : 211372   (<p>The <a href=#template-contents id=the-template-element:template-contents>…)
raw quoted clause "are not children of the element itself" : 211622
inline <code id=the-template-element:the-template-element-4> : 211475
closing </a> of the quoted clause : 211660 ; paragraph </p> : 211665
```

Byte 211509 falls **inside the id attribute value** of the inline `<code>` element (`…:the-template-element:the-template-element-4` — the substring `template-element-4` starts exactly at 211509). It is 137 bytes past the real `<p>` and 113 bytes before the quoted clause. So the raw half of the locator does not merely point to a shifted spot: it points at a **different element** than the one it names. (The receipt's half-true companion claim — that a bare-sentence search of the raw bytes fails because the sentence is wrapped in inline `<a>`/`<code>` markup — is correct: `raw.count(b'The template contents of a template element are not children of the element itself.')` → 0, because the raw reads `…<a href=#template-contents id=…>template contents</a> of a <code id=…>template</code> element <a href=syntax.html#template-syntax>are not children of the element itself</a>.`)

The same two wrong coordinates are carried in the authoring seat's report, `.ufo/waves/round-26/w1/RowS025.md:11` (caveat 3): “Quote sits at text-view line 1 offset 62596; raw HTML wraps the same sentence in inline `<a>`/`<code>` markup (raw byte 211509)”. The reasoning there is sound; the coordinates are not.

### 3.3 Why the counter did not catch it

`measure.py` never validates `anchorObserved` coordinates — `measure.py:366-370` only requires a non-empty string, and the string “offset” never appears in `measure.py` (`src.count('offset')` → 0). Hence the round-26 counter can report 32/32 exit 0 while a locator is wrong. This is the same shared root cause the S027 seat flagged lane-wide; S025 is the most misleading instance of the class, because its stated text offset no longer sits on the quoted sentence at all and its stated raw byte names the wrong element.

## 4. Verdict rationale and severity

- **The receipt's decision is correct.** HOLD is the right adjudication: the source has not drifted (byte-identical to the 2026-10-20 read), the quote is verbatim, unique, in-section, and grounds the row's `teaches`; the `reason`'s every factual clause is present in the retained bytes; `correction: null` is right (nothing to correct in the corpus for this row).
- **The receipt's evidence record is wrong in a checkable way.** Both coordinates in `anchorObserved` fail against the artifacts they name; one of them is wrong in kind, not by a shift. A re-verifier who follows `raw <p> at byte 211509` lands inside an `id` attribute value, and one who follows `offset 62596` lands 42 characters short, in the preceding attribute sentence. That is why this is **DISAGREE** and not AGREE.
- **Severity is low, not medium/high**, because: no ledger statement, corpus lesson, counter result, or corpus cell is affected; the quote string, section label, `teaches` grounding, `HOLD` verdict and `correction: null` are all independently verified correct; and both correct coordinates sit in the immediate neighbourhood (42 chars / 137 bytes), so the anchor remains recoverable by a reader who follows the described structure. Escalating to medium would require the locator to name the wrong section or the wrong source, which is not the case here.

## 5. Minimal correction (metadata only — no verdict, quote, reason or corpus change)

In `.ufo/waves/round-26/rechecks/S025.json`, `anchorObserved` only, replace:

- `text view S025-1.txt line 1 at offset 62596` → `text view S025-1.txt line 1 at offset 62638 (byte 62755 in the 79,117-byte view)`
- `raw <p> at byte 211509` → `raw <p> at byte 211372 (quoted clause "are not children of the element itself" at byte 211622; paragraph </p> at 211665)`

And, for consistency, in `.ufo/waves/round-26/w1/RowS025.md` caveat 3 (line 11):

- `text-view line 1 offset 62596` → `text-view line 1 offset 62638`
- `raw byte 211509` → `raw byte 211372` (the sentence is wrapped by `<a href=#template-contents …>` at 211379, `<code id=the-template-element:the-template-element-4>` at 211475 and `<a href=syntax.html#template-syntax>` at 211586)

Unchanged: `verdict` = HOLD, `quote`, `reason`, `correction` = null; `corpus/SOURCES.md:33`; `corpus/knowledge/static-canonical-preflight.md` (no STALE block needed — the S025-derived `[r23-correction]` at lines 143-146 remains accurate); the round-26 counter (32/32) and its exit code.

## 6. Residual risk / verification gaps

- **Residual risk (low, lane-wide, not row-specific):** because `source_text.py` was edited mid-wave and every text view was re-extracted at 13:02:14, *any* receipt whose `anchorObserved` cites text-view character offsets may be stale the same way. Verified in this lane: S024 (old 10160 → committed 10172), S027 (7269 → 7274), S034 (8863 → 8864), S011 (14663 → 14677), S012 (12124 → 12164) — while S018, S021, S030 are unaffected (their offsets coincide in both extractors). S025's shift (+42) and S012's (+40) are the largest. Sibling Falsify seats own their rows; this is a shared-root-cause signal, not four independent defects.
- **Registry-cell observation (out of this seat's scope, flagged for the coordinator):** `corpus/SOURCES.md:33` lists `used-by` = `corpus/lessons/round-22.md` only, but `corpus/knowledge/static-canonical-preflight.md:144` also relies on S025 (and `:101`, `:117` rely on S024, whose row at `corpus/SOURCES.md:32` likewise lists only the lessons file). Compare S020/S021/S026, whose `used-by` cells list both files. This is a registry-completeness question about the `used-by` cell, not a freshness defect in the receipt, and the round-26 contract leaves that cell unchanged.
- **Verification gaps:** (i) I did not fetch `syntax.html#template-syntax` (the link target the sentence points at) — it is not a `corpus/SOURCES.md` row URL, and the *statement* is present verbatim in the retained S025 bytes, so the row does not depend on that page. (ii) The fragment URL `#the-template-element` is client-side only; the section id was confirmed in the byte-identical document rather than by navigating to the fragment. (iii) `/tmp/r22-scripting.html` is an out-of-lane scratch copy from round 22; I read it read-only for the digest comparison and did not write it.

## 7. Bottom line

The freshness attack fails and the HOLD stands: the Living Standard document served on 2026-10-21 is byte-for-byte the document read on 2026-10-20 (`sha256 5854951b…9abe43`), §4.12.3 keeps its number, and the quoted sentence is verbatim, unique and section-bound, and it does ground the row's `teaches` (with the “canonical” clause entailed by the same section's DocumentFragment / inert-owner-document prose and already bounded to static bytes in the corpus). The actionable defect is the receipt's locator: `text view … offset 62596` should be `62638` (byte 62755), and `raw <p> at byte 211509` should be `211372` (quoted clause at 211622) — the latter names the wrong element, byte 211509 being inside the `id` attribute of the inline `<code>` wrapper.

```json
{"target":".ufo/waves/round-26/rechecks/S025.json (S025 receipt, verdict HOLD) + corpus/SOURCES.md:33 (S025 row)","verdict":"DISAGREE","severity":"low"}
```
