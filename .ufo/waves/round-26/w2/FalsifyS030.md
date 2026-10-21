# Falsify S030 — round-26 C1 freshness recheck (receipt HOLD)

- Seat: `KakeR26-2.FalsifyS030` (reviewer, leaf member — no dispatch). Milestone `r26-recheck-falsify`. Axis: **freshness**. Checked 2026-10-21.
- Target: receipt `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-26/rechecks/S030.json` (verdict **HOLD**, `fetchIndex 1`, `correction null`) and the row line `corpus/SOURCES.md:38` (S030 — WHATWG HTML: The HTML syntax, void elements and start tags; teaches «A slash is allowed only on void or foreign elements and has no effect on void elements; the void list has 13 names»; anchor «Section 13.1.2.1 start tags step 6 and 13.1.2 void elements list; Living Standard last updated 20 October 2026, opened 2026-10-21»).
- Retained bytes: `.ufo/waves/round-26/fetched/S030-1.raw.gz` (89,196 B decompressed, sha256 `04b65bf0…9a52d`); retained view `.ufo/waves/round-26/fetched/text/S030-1.txt` (31,812 B, one content line + trailing newline, sha256 `971362b0…fde043`); provenance `.ufo/waves/round-26/fetched/manifest.json` (row `S030`, index 1, status 200).
- Candidate under review: `e28312b14b076584fedd696fae2a684e460bd11e` (base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`). The receipt blob at the candidate is byte-identical to the worktree file (`git show e28312b1:.ufo/waves/round-26/rechecks/S030.json | sha256sum` → `696cf2cc…4543` = worktree sha256).

## Verdict: **AGREE** (severity **low**) — the HOLD is correct and the source has not drifted at all; the defect is confined to the receipt's raw-byte locators in `anchorObserved`

The substantive freshness attack **fails**: the document served today is byte-identical to the retained fetch, the quote is verbatim and uniquely located inside §13.1.2.1 step 6, the void list still names exactly 13 elements, and the row's `teaches` is fully grounded. One **low-severity** defect survives: `anchorObserved` misdescribes the anchor's element level and its raw offsets (one element name is false, one offset is false by 382 characters, and two "byte" offsets are actually character offsets). This is locator metadata only — it changes no verdict, no corpus statement, and no counter result.

---

## Attack 1 — Does the quote ground THIS row's `teaches` (not page chrome, not a neighbouring clause)? → **NO DEFECT**

Receipt quote (23 words / 24 tokens):

> `On void elements, it does not mark the start tag as self-closing but instead is unnecessary and has no effect of any kind.`

Verified against the retained view and the retained raw:

```
$ python3 - <<'EOF'   # fetched/text/S030-1.txt
quote char offset: 9514   word-bounded: True   words: 23   tokens: 24
```

- **Verbatim and unique.** `t.count(q) == 1` in `fetched/text/S030-1.txt`; the normalized quote occurs in **no other row's text view** (`fetched/text/*.txt` scan → only `S030-1.txt`), so it is not boilerplate and passes the counter's row-specificity rule.
- **It is the normative clause, not chrome.** In the raw, the sentence sits inside the start-tag grammar's step 6, immediately after the sentence that grants the solidus:

```
raw char 25419: <li>Then, if the element is one of the <a href=#void-elements …>void elements</a>,
                 or if the element is a <a href=#foreign-elements …>foreign element</a>, then there may be a
                 single U+002F SOLIDUS character (/), which on … foreign elements … marks the start tag as
                 self-closing. On … void elements …, it does not mark the start tag as self-closing but instead
                 is unnecessary and has no effect of any kind. For such void elements, it should be used only
                 with caution — especially since, if directly preceded by an unquoted attribute value, it becomes
                 part of the attribute value rather than being discarded by the parser.<li>Finally, start tags
                 must be closed by a U+003E GREATER-THAN SIGN character (>).</ol>
```

  The raw HTML never contains the quote as a contiguous string (the anchor tags split it), but tag-stripped the sentence is character-for-character the receipt's quote.
- **Both clauses of `teaches` are grounded.** The receipt's *reason* covers the rest, and each part verifies:
  - "A slash is allowed only on void or foreign elements" → the same step 6, preceding sentence: “Then, if the element is one of the void elements, or if the element is a foreign element, then there may be a single U+002F SOLIDUS character (/)” (text view @9394).
  - "has no effect on void elements" → the receipt's quote (text view @9514), verbatim.
  - "the void list has 13 names" → §13.1.2, the void `<dd>` (raw char 12260–13568), exactly **13** `<code id=elements-2:the-…-element>` names before the next `<dt>`: `['area','base','br','col','embed','hr','img','input','link','meta','source','track','wbr']` — the same 13 in the same order the receipt names them.
  - The row's own precision caveat is preserved and still in force: `corpus/SOURCES.md:104` (round-23 note: the solidus after an unquoted attribute value belongs to the value) — and the retained step 6 still says so (“if directly preceded by an unquoted attribute value, it becomes part of the attribute value rather than being discarded by the parser”, text view @9717).
- **The step numbering is right.** The start-tag grammar `<ol>` (raw char 24124–26329) contains exactly **7** `<li>` items; item 6 is the solidus step. The receipt's "ordered-list step 6 of 7" is correct.

## Attack 2 — Is the anchor observed correct in the raw bytes? → **LOW-SEVERITY DEFECT FOUND**

`rechecks/S030.json` `anchorObserved` says:

> “§13.1.2.1 Start tags, ordered-list step 6 of 7 (raw **`<h4 id=start-tags>` at byte 23907**, `<ol>` at 24124, **item 6 begins 25801**); §13.1.2 Elements void-element **`<dfn id=void-elements>` at byte 12265**; text view fetched/text/S030-1.txt line 1, quote at offset 9514”

Measured against `fetched/S030-1.raw.gz` (89,196 B / 89,124 chars; the file is UTF-8 with multi-byte characters, so byte offsets and char offsets differ):

```
'<h4 id=start-tags' in raw -> False
all h4 ids: ['the-doctype', 'elements-2', 'text-2', 'character-references', 'cdata-sections', 'comments', 'processing-instructions']
actual    : '<h5 id=start-tags><span cl'

  h5 start-tags        claim=23907 (byte     ) char=23903  byte=23917  claim-char=+4
  ol                   claim=24124 (unlabelled) char=24124  byte=24138  claim-char=+0
  step-6 li            claim=25801 (unlabelled) char=25419  byte=25433  claim-char=+382
  dfn void-elements    claim=12265 (byte     ) char=12260  byte=12270  claim-char=+5

what claim 23907 lands on : 'id=start-tags><span class=secno>13'
what claim 12265 lands on : 'id=void-elements>Void elements</df'
what claim 25801 lands on : 'self-closing. On\n   <a href=#void-'
real step-6 li start      : '<li>Then, if the element is on'
```

Three concrete inaccuracies, all reproducible:

1. **Wrong element level (false as written).** The start-tags heading is **`<h5 id=start-tags>`** — §13.1.2.1 is a sub-subsection, so it is an `h5` under the `h4` §13.1.2 (`<h4 id=elements-2>`). There is **no `<h4 id=start-tags>` anywhere in the retained bytes** (`'<h4 id=start-tags' in raw -> False`; the complete list of `h4` ids is printed above). The receipt's literal locator names an element that does not exist.
2. **“item 6 begins 25801” is off by 382 characters** and lands *mid-sentence* inside item 6, at “marks the start tag as self-closing. On”. Item 6 begins at char **25419** / byte **25433** (`<li>Then, if the element is one of the …`). A verifier re-deriving “item 6” from the receipt's own locator would land on the wrong text.
3. **“at byte …” is the wrong unit for two of the four numbers.** 23907 and 12265 are *character* offsets of the `id=` attribute values (`id=start-tags`, `id=void-elements`); the elements' byte offsets are 23917 and 12270. The unlabelled 24124 is the *character* offset of `<ol>` (byte 24138). No single convention (raw chars, raw bytes, tag-stripped, whitespace-collapsed, head-stripped) reproduces all four numbers, so the four locators were not measured consistently.

**What is *not* defective.** The section identifiers — `§13.1.2.1` (raw `<h5 id=start-tags><span class=secno>13.1.2.1</span> Start tags`), `§13.1.2` (raw `<h4 id=elements-2><span class=secno>13.1.2</span> Elements`), the void `<dfn id=void-elements>` and its 13 names, “step 6 of 7”, and the text-view locator (line 1, quote at 9514, word-bounded) are all **exactly correct**. The defect is confined to the element-level word and the four raw offsets.

**Blast radius: none.** `measure.py` treats `anchorObserved` as an opaque non-empty string for HOLD receipts (`anchor_missing` only fires on an empty string; the checker never parses offsets). No corpus statement, lesson, or counter output depends on these numbers.

## Attack 3 — Did content/version change in a way the receipt missed? → **NO DEFECT (zero drift, proven three ways)**

**(a) A plain public GET of the row URL today is byte-identical to the retained fetch** (body piped straight into memory; nothing written to disk on this run):

```
$ curl -sS --max-time 45 -A 'Mozilla/5.0' -D - 'https://html.spec.whatwg.org/multipage/syntax.html#start-tags' | python3 -c "…"
HTTP/2 200
date: Wed, 21 Oct 2026 16:50:54 GMT
content-length: 89196
last-modified: Tue, 20 Oct 2026 12:58:33 GMT
etag: "6ad76579-15c6c"
body bytes 89196 sha256 04b65bf0b4b5f3bb3815999ab499af980fa09b8832f02c1686c544ab8e79a52d
```

That digest equals the retained bytes and the manifest entry for (`S030`, 1): `sha256 04b65bf0b4b5f3bb3815999ab499af980fa09b8832f02c1686c544ab8e79a52d`, `bytes 89196`, `last-modified: Tue, 20 Oct 2026 12:58:33 GMT`, `etag "6ad76579-15c6c"`, `fetchedAt 2026-10-21T15:10:50Z`. Same `Last-Modified`, same `ETag`, same length, same hash → **no content change and no version change** since the fetch, and none since the row was opened.

**(b) The bytes are also identical to the digest the round-23 lesson records as S030's correct response digest.** `corpus/lessons/round-23.md:206-207` (the appended authoritative errata):

> `S030 correct response digest:` `04b65bf0b4b5f3bb3815999ab499af980fa09b8832f02c1686c544ab8e79a52d`.

The receipt's reason says "response sha256 equals round-23's recorded S030 digest, so no drift at all" — true under that errata reading. (Caveat for the reader: `corpus/lessons/round-23.md:60` still shows the cross-assigned `a11dcf17…` for S030; `w1/RowS030.md` caveat 2 spells this out correctly, the receipt does not. Loose phrasing, not a false claim.)

**(c) The version marker in the row's anchor still holds.** The retained raw's own masthead reads `Living Standard — Last Updated <span class=pubdate>20 October 2026</span>` (raw char ~1372), matching the row's “last updated 20 October 2026”; the fetch date 2026-10-21 matches the row's “opened 2026-10-21” and the 90-day recheck cadence (next due 2027-01-19).

## Attack 4 — Downstream consistency of a HOLD → **NO DEFECT**

- The row's `usedBy` paths exist and cite S030: `corpus/knowledge/static-canonical-preflight.md` (lines 98-99, 110-111, 151) and `corpus/lessons/round-23.md:60`.
- `corpus/knowledge/static-canonical-preflight.md` carries exactly two `[r26-recheck S030 STALE]` corrections (lines 190 and 192), matching the two STALE statements attributed to S030 in `.ufo/waves/round-26/statements.json` (`statements 8, seatStale 2, stale 2`) — the ledger is consistent with a HOLD receipt (`correction: null`).
- `scripts/canonical_audit.py:38-40` `HTML_VOID_ELEMENTS` equals the same 13 names.
- No row or lesson claim is left stale by a HOLD: the taught content (void list of 13, solidus permitted only on void/foreign, no effect on void elements) is still literally true in the bytes.

## Residual risk / verification gaps

1. **Residual risk (lane-wide, low, not row-specific):** the shared extractor `.ufo/waves/round-26/source_text.py` was edited at 13:02:13 and every text view was re-extracted at 13:02:14, after the w1 reports (12:37) were written. The S030 w1 report's *file-statistics* line is consequently stale: `w1/PairS030StaticCanonicalPrefl.md` says “Text view `fetched/text/S030-1.txt`: 31,810 bytes, one line, sha256 `c7228ee1…`”, while the file on disk is **31,812 bytes, sha256 `971362b0…`**. I reproduced both: `before/source_text.py` output + `"\n"` = 31,810 B / `c7228ee1…`; current `source_text.py` output + `"\n"` = 31,812 B / `971362b0…` (= the file). The w1 report's **offsets are unaffected** — all seven (@4059, @4242, @8607, @9394, @9514, @9717, @12167) still land exactly where the report says in the current file. This is a w1 metadata defect, outside my receipt target, flagged for the owning seat.
2. **Offsets are a locator convenience only.** The quote, the section labels, the step number, the 13-name list, and the version marker all verify independently, so no statement or counter result depends on them.
3. **Verification gaps I did not exercise:** I did not GET the `#start-tags` fragment URL itself (the fragment is client-side only; the section id was confirmed in the byte-identical document); I did not verify §13.2 (parsing.html — S031's document) beyond what the retained S031 view is used for elsewhere; I ran no counter and no tests, per lane bounds.
4. **Honest deviation to disclose:** my first plain GET wrote the body and headers to `/tmp/s030live.html` and `/tmp/s030h.txt` before I switched to the in-memory pipe. Both files were deleted immediately (`rm -f /tmp/s030live.html /tmp/s030h.txt`, verified gone) and every subsequent GET was piped in memory only. No corpus, script, fleet-repo, sibling-lane, or lane Git-index/jj state was mutated; the only file I wrote is this report.

## Minimal correction (metadata only — no verdict change, no `correction` field needed)

Replace the `anchorObserved` value in `.ufo/waves/round-26/rechecks/S030.json` with:

> `§13.1.2.1 Start tags, ordered-list step 6 of 7 (raw <h5 id=start-tags> at char 23903 / byte 23917, start-tag grammar <ol> at char 24124 / byte 24138, step-6 <li> at char 25419 / byte 25433); §13.1.2 Elements void-element <dfn id=void-elements> at char 12260 / byte 12270; text view fetched/text/S030-1.txt line 1, quote at offset 9514`

and, in `w1/PairS030StaticCanonicalPrefl.md`, “31,810 bytes, one line, sha256 `c7228ee1…`” → “31,812 bytes, one content line plus trailing newline, sha256 `971362b0…`”. The `quote`, the `reason`, the `HOLD` verdict, `fetchIndex 1`, and `correction: null` all stand as they are.

## Reproduction commands (read-only)

```
python3 - <<'EOF'
import gzip,pathlib,re
raw=gzip.decompress(pathlib.Path('.ufo/waves/round-26/fetched/S030-1.raw.gz').read_bytes()); s=raw.decode('utf-8')
print('<h4 id=start-tags' in s)                                  # False
print(re.findall(r'<h4 id=([a-z0-9-]+)', s))                      # h4 id list
for pat,claim in [('<h5 id=start-tags>',23907),('<ol>',24124),
                   ('<li>Then, if the element',25801),('<dfn id=void-elements>',12265)]:
    print(pat, 'char', s.find(pat,23000), 'byte', raw.find(pat.encode(),23000), 'claim', claim)
i=s.find('<dfn id=void-elements>'); j=s.find('<dt>',i)
print(len(re.findall(r'<code id=elements-2:the-([a-z0-9-]+)-element>', s[i:j])))   # 13
EOF
curl -sS --max-time 45 -A 'Mozilla/5.0' -D - 'https://html.spec.whatwg.org/multipage/syntax.html#start-tags' \
  | python3 -c "import sys,hashlib; d=sys.stdin.buffer.read(); h,_,b=d.partition(b'\r\n\r\n'); print(h.decode('latin-1')); print(len(b), hashlib.sha256(b).hexdigest())"
```

## Tooling

No tool was installed or upgraded this run (`curl`, `python3` stdlib, and the repo's own scripts were already present). Per the operator directive, **no pacman transaction was performed** — the host-wide pacman pause is respected — and no host service or system change was made.

```json
{"target":".ufo/waves/round-26/rechecks/S030.json","verdict":"AGREE","severity":"low"}
```
