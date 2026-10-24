# FalsifyS026 — attack receipt `rechecks/S026.json` (verdict HOLD)

- Seat: `KakeR26-2.FalsifyS026` (reviewer, leaf — no dispatch). Axis: **freshness**. Milestone: `r26-recheck-falsify`. Checked 2026-10-21.
- Target: receipt `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-26/rechecks/S026.json` (HOLD, fetchIndex 1) and row line `corpus/SOURCES.md:34` (S026 — Python: html.parser; teaches «Tag and attribute names are lowercased and entities decoded, but matching end tags and HTML5 tree construction are not validated»; anchor «HTMLParser introduction and handle_starttag; Python 3.15 documentation accessed 2026-10-20»).
- Retained bytes: `.ufo/waves/round-26/fetched/S026-1.raw.gz` (55,260 bytes decompressed); retained view `fetched/text/S026-1.txt`; provenance `fetched/manifest.json`.
- Tooling: none installed or upgraded this run. Read-only use of `curl`, `python3` (stdlib), `zcat`/`sha256sum`, `git show`, and the read/grep tools. One plain public GET of the `corpus/SOURCES.md` row URL (not saved), plus one HEAD. No corpus, script, lane-state, or Git index mutation.

## Verdict: AGREE (low) — the HOLD stands on freshness; the receipt is accurate about the source but incomplete about its own row's `teaches`

The freshness attack fails hard: the document served today is byte-for-byte the document the receipt fetched, the quoted sentence is verbatim and uniquely located inside the `HTMLParser` class description, and the receipt's `anchorObserved` locator — including both of its neighbouring landmarks — is exact. The 3.15.0 → 3.15.1 label move was caught, not missed.

Four **low-severity** defects survive, all in the receipt's own prose rather than in the source: (1) the receipt does not record that one of the three clauses of *this row's* `teaches` ("HTML5 tree construction … not validated") has **zero** textual support in the source — 0 hits for "HTML5" and 0 for "tree construction" in the retained bytes and in the live page — even though it enumerates the other taught clauses as verified; (2) the receipt's paraphrase misattributes entity-reference replacement to attribute *names* rather than to attribute *values*, against both the page and the lane's own round-22 reading; (3) the receipt's "no taught content changed" is a sentence-presence check, while the whole-page diff against the row's original read is UNVERIFIABLE (the 3.15.0 body is not retained) — a limit the receipt does not state; (4) the receipt's `reason` calls its quote a "sentence" when it is the first conjunct of a two-conjunct source sentence whose omitted half is the clause the same round's `[r26-recheck S026 STALE]` tag turns on.

---

## 1. Did content/version change in a way the receipt missed? — No. Zero drift, provable four ways.

**(a) Live GET today is byte-identical to the retained fetch.** One plain public GET of the row URL from `corpus/SOURCES.md` (in memory only, not saved):

```
$ curl -sS --max-time 45 https://docs.python.org/3/library/html.parser.html | sha256sum
d92217e08486dc9bfedf255f071fdad1ea1a506a1e8a8570c4711a47aad5faa3  -

$ curl -sSI https://docs.python.org/3/library/html.parser.html | tr -d '\r' | grep -iE 'last-modified|etag|content-length|date'
last-modified: Wed, 21 Oct 2026 13:04:30 GMT
etag: "6ad8b85e-d7dc"
date: Wed, 21 Oct 2026 16:41:14 GMT
content-length: 55260
```

That digest equals the retained body and the manifest entry (`fetched/manifest.json`, `row: S026`, `index: 1`, `status: 200`, `bytes: 55260`, `sha256: d92217e0…faa3`, `last-modified: Wed, 21 Oct 2026 13:04:30 GMT`, `etag: "6ad8b85e-d7dc"`). Nothing moved between the 15:10:49Z fetch and the 16:41Z check.

**(b) The live page still carries exactly the strings the receipt and the row rely on.** Live page: title `html.parser — Simple HTML and XHTML parser — Python 3.15.1 documentation`; footer `Last updated on Oct 21, 2026 (13:02 UTC)`; the quote at character offset 14111, preceded by `…override its methods to implement the desired behavior.</p> <p>` and followed by `or call the end-tag handler for elements which are closed implicitly by closing an outer element.</p>`. Identical to the retained bytes (same offsets).

**(c) The version-label move the receipt describes is real and correctly characterised.** The receipt says the page "now labels itself Python 3.15.1 (last updated 2026-10-21 13:02 UTC; last-modified 13:04:30 GMT) versus Python 3.15.0 seen at 06:59 UTC in the round-23 reopen". Verified in the retained bytes: `Python 3.15.1 documentation` ×2 (title + breadcrumb), `3.15.0` ×0, footer `Last updated on Oct 21, 2026 (13:02 UTC)` at raw offset 54911. The round-23 reopen is documented at `.ufo/waves/round-23/w1/ReopenPythonParser.md` ("The reopened page title is `html.parser — Simple HTML and XHTML parser — Python 3.15.0 documentation`… `date: Wed, 21 Oct 2026 06:59:02 GMT`"). The label moved within the pinned 3.15 family and no taught sentence moved with it — the receipt's reasoning is right, and it matches the L1 disposition recorded for this row in `.ufo/waves/round-26/statements.json` (`"l1Disposition": "C1 version label 3.15.0→3.15.1 within the pinned 3.15 family with relied-on sentences unchanged (recorded as a note); C2 accepted."`).

**(d) The taught sentences the row names are all present verbatim in the re-fetched bytes.** From `fetched/S026-1.txt` (all present, each exactly once):

| taught clause | verbatim string in the retained text |
|---|---|
| tag names lowercased | `The tag argument is the name of the tag converted to lower case` |
| attribute names lowercased | `The name will be translated to lower case, and quotes in the value have been removed, and character and entity references have been replaced` |
| entities decoded | `All entity references from html.entities are replaced in the attribute values.` |
| end tags not validated | `This parser does not check that end tags match start tags or call the end-tag handler for elements which are closed implicitly by closing an outer element.` |

The 3.15.0-era quotations in `.ufo/waves/round-22/w1/PythonParser.md` and `.ufo/waves/round-23/w1/ReopenPythonParser.md` re-appear word for word in the 2026-10-21 bytes, so no taught sentence drifted.

## 2. Does the quote ground THIS row's `teaches`, or is it page chrome / a neighbouring clause?

It is neither chrome nor a neighbour — but it grounds **only one of the three** clauses of this row's `teaches`.

**(a) The quote is real, unique, and inside the class description.**

- Raw bytes: `zcat fetched/S026-1.raw.gz | sha256sum` → `d92217e0…faa3`, 55,260 bytes, matching the manifest. The quote sits at **raw byte offset 14127**; the surrounding markup is `…</p> <p>This parser does not check that end tags match start tags or call the end-tag handler for elements which are closed implicitly by closing an outer element.</p> <div class="versionchanged"> <p><span class="versionmodified changed">Changed in version 3.4: </span>…`.
- It is a paragraph in the `HTMLParser` class `<dd>` (class `<dl class="py class">` at char offset 11922, `<dd>` at 12995, `</dd></dl>` at 14833) — not page furniture, not a neighbouring clause.
- Occurrence count: exactly 1 in the raw body and exactly 1 in the text view. It appears in **no other** row's retained text: a scan of all 32 files under `fetched/text/` finds the string only in `S026-1.txt` (so the counter's row-specificity rule is satisfied, and the quote is not boilerplate).
- The receipt's quote passes the counter's own gates: 11 whitespace words / 11 alphanumeric tokens (≥6 tokens, ≤25 words), and `measure.py`'s `quote_in_text` word-bounded check succeeds against `source_text.py`'s normalized view of the retained bytes (verified by re-running the same regex against `source_text.normalize(source_text.text_of(raw, 'text/html'))`; match at offset 1546).

**(b) `anchorObserved` is exact, both neighbours included.** The receipt claims: "'html.parser — Simple HTML and XHTML parser' section > HTMLParser class-description paragraph (module overview, after the callback-overview sentence and immediately before 'Changed in version 3.4'); text view line 1".

- "after the callback-overview sentence" — verified: the immediately preceding `<p>` is `An HTMLParser instance is fed HTML data and calls handler methods when start tags, end tags, text, comments, and other markup elements are encountered. The user should subclass HTMLParser and override its methods to implement the desired behavior.`
- "immediately before 'Changed in version 3.4'" — verified: the next element is `<div class="versionchanged"><p><span class="versionmodified changed">Changed in version 3.4: </span><em>convert_charrefs</em> keyword argument added.` (versionchanged entries at raw offsets 14329 / 14491 / 14748 for 3.4 / 3.5 / 3.14.1).
- "text view line 1" — verified: `fetched/text/S026-1.txt` is a single-line view (11,794 bytes; the only newline is the trailing one at index 11793) and the quote is at character offset 1558 of that line. The `html.parser.HTMLParser.handle_starttag` anchor that the row's anchor cell also names is still present (`id="html.parser.HTMLParser.handle_starttag"` at raw offset 22923; `id="module-html.parser"` also present).

**(c) The receipt's `quote` is a clause-prefix of the source sentence, and the reason calls it a sentence.** The source sentence continues `or call the end-tag handler for elements which are closed implicitly by closing an outer element.` The receipt's `reason` says "the quoted non-validation sentence is verbatim" — the quoted string is verbatim, but it is the first conjunct of a two-conjunct sentence, and the omitted conjunct is exactly the clause the knowledge entry's line 69 over-claim turned on (`.ufo/waves/round-26/w2/Correction6S026.md` argues that correction itself is not established). A reader of the receipt alone therefore gets the sentence without the implicit-closure half. Not a counter failure (the counter only requires a word-bounded substring), but a fidelity nit in the receipt's own framing.

**(d) The taught clause "HTML5 tree construction … not validated" has no support in the source — and the receipt does not say so.** The receipt enumerates what the page documents ("handle_starttag converts tag names to lower case, attribute names are lowercased and their character/entity references replaced, convert_charrefs defaults true, and the quoted non-validation sentence is verbatim") and concludes "no taught content changed", yet never records that the page says nothing about HTML5 or tree construction. Verified: `HTML5` → 0 hits, `html5` → 0, `tree construction` → 0 in the retained raw; the only `tree` hit is the GitHub source path `/tree/3.15/Lib/html/parser.py` (offset ~11500). The same holds live (0 hits, same single `tree` in the GitHub URL).

This is **not** a freshness drift — the clause was equally unsupported when the row was mined, and `.ufo/waves/round-22/w1/PythonParser.md` (limitation 1) already recorded "No HTML5 tree construction or conformance claim appears anywhere on this page … `[INFERENCE]`", as did `.ufo/waves/round-23/w1/ReopenPythonParser.md` (P3). So HOLD at row level is defensible, and the same wave's own adjudication of the analogous knowledge-entry statements agrees: `.ufo/waves/round-26/w1/PairS026StaticCanonicalPrefl.md` marks "it is not an HTML5 DOM/tree builder" (L67–68) and "The tool is still not an HTML5 tree builder" (L103) as **HOLD (inference)**. But those caveats live only in the sibling artifacts (`w1/RowS026.md` caveat 1, `w1/PairS026StaticCanonicalPrefl.md` R1). The receipt itself — the artifact the counter grades and the one a later reader opens first — does not carry the caveat, and `corpus/SOURCES.md:34` still ships the unsupported clause unchanged.

**(e) The receipt's paraphrase puts entity-reference replacement on the wrong element.** Receipt: "attribute names are lowercased and **their** character/entity references replaced". The page: "The name will be translated to lower case, and quotes in the **value** have been removed, and character and entity references have been replaced." plus the explicit "All entity references from html.entities are replaced in the attribute **values**." The lane's own round-22 reading is precise where the receipt is loose — `round-22/w1/PythonParser.md` scoped teaching 3: "Character references are decoded inside attribute **values** regardless of `convert_charrefs`". So the receipt's sentence, read literally, says attribute *names* get their references replaced, which the source contradicts.

## 3. Ledger / counter coupling (checked for consistency, no change proposed)

- `statements.json` records S026 × `corpus/knowledge/static-canonical-preflight.md` as `stale: 1`; the corpus file carries exactly 1 `[r26-recheck S026 STALE]` tag (`corpus/knowledge/static-canonical-preflight.md:188`). `measure.py:450-454` requires `tags ≥ stale` — satisfied. Lane-wide: 276 statements, 8 stale, 8 tags (verified by recount across all ledger pairs).
- Row receipt HOLD with `correction: null` co-existing with a statement-level STALE for the same row is the round's documented two-level design (statement verdicts in `w1/Pair*.md`, row verdicts in `rechecks/S0NN.json`; `corpus/SOURCES.md` round-26 note: "HOLD 32, STALE 0, UNVERIFIABLE 0 at row level"). Consistent — no finding.
- `corpus/SOURCES.md` differs from base `97404de` by 2 inserted lines only (the round-26 bounded-recheck note); the S026 row cell is byte-identical to base, as the contract's append-only rule requires.

## 4. Findings, by severity

1. **LOW — receipt completeness / row-scope.** `rechecks/S026.json` `reason` verifies the lowercasing and entity-decoding clauses and the end-tag clause, then concludes "no taught content changed", without recording that the third clause of `corpus/SOURCES.md:34` ("HTML5 tree construction are not validated") has no textual support in the source (0 "HTML5" / 0 "tree construction" hits in `S026-1.raw.gz` and live). The caveat exists only in `w1/RowS026.md` caveat 1 and `w1/PairS026StaticCanonicalPrefl.md` R1. Minimal correction: append one sentence to the receipt `reason` recording that clause as an inference from the callback-only model (unchanged since round 22), matching the round's own HOLD-(inference) treatment in `w1/PairS026StaticCanonicalPrefl.md` #4/#10.
2. **LOW — paraphrase accuracy in the receipt.** `reason` says attribute names are "lowercased and their character/entity references replaced"; the page replaces references in the attribute **values** ("quotes in the value have been removed…"; "All entity references from html.entities are replaced in the attribute values"), as does `round-22/w1/PythonParser.md` scoped teaching 3. Minimal correction: change "their" to "the attribute values'" in the receipt `reason`.
3. **LOW — overstated drift claim / unstated limit.** `reason` asserts "no taught content changed"; that is verified per taught sentence (see §1(d)), but the whole-page diff against the row's original 2026-10-20 read is UNVERIFIABLE because the 3.15.0 body was not retained — a limit `w1/PairS026StaticCanonicalPrefl.md` states ("Whole-page bytes of those builds are not retained, so a whole-page content diff is UNVERIFIABLE") and the receipt does not. Minimal correction: qualify the claim to the taught sentences.
4. **LOW — quote framing.** `reason` calls the quoted string a "sentence"; it is the first conjunct of a two-conjunct source sentence, and the omitted conjunct is the one the same round's `[r26-recheck S026 STALE]` tag turns on. Minimal correction: describe it as the first clause of the class-description sentence, or extend the `quote` while staying ≤25 words.

None of these four changes the HOLD verdict, the quote, the corpus text, or any counter result.

## 5. Residual risk and verification gaps

- **Residual (lane-wide, not S026-specific):** the same round-24-style half-sentence truncation is what produced the disputed `corpus/knowledge/static-canonical-preflight.md:188` tag; `w2/Correction6S026.md` (DISAGREE, low) argues that tag's "overstates" diagnosis is not established, on the ground that "does not report **all** implicit closures" is a correct entailment of the full sentence. That dispute concerns the corpus tag, not this receipt; my seat independently reaches the same reading of the source sentence, which is why finding 4 above is filed as framing only, and I did not re-litigate the tag.
- **Residual:** `corpus/SOURCES.md:34` still ships "HTML5 tree construction are not validated" as if the page taught it. Finding 1 covers it; the lane has (correctly, for freshness) declined to open a row-level STALE for a pre-existing over-claim, so the row cell is likely to keep it. Flagged for L1, not changed here.
- **Verification gap (i):** no whole-page comparison against the 2026-10-20 3.15.0 read is possible — the 3.15.0 body bytes were never retained (`w1/PairS026StaticCanonicalPrefl.md` records the same limit). The taught-sentence comparison in §1(d) is the strongest available substitute; a sentence present now might in principle have been reworded and reworded back, which nothing retained can exclude.
- **Verification gap (ii):** the exact 3.15.0 wording of the `handle_starttag` reference clause is only pinned by a truncated round-22 quote ("The name will be translated to lower case, and quotes in the value have been removed"), so whether the page read "character references" or "character and entity references have been replaced" on 2026-10-20 cannot be settled from retained bytes. It does not affect the verdict: the row's taught clause ("entities decoded") holds under either wording, and the retained 2026-10-21 bytes say "character and entity references have been replaced".
- **Verification gap (iii):** I did not fetch any other documentation version (`docs.python.org/3.14/…` etc.) — the lane bound permits only a GET of the row URL already in `corpus/SOURCES.md` — and I did not run the local interpreter's `html.parser` (the installed 3.14.8 stdlib ships no docstrings for these methods, so it could not have served as a comparison source anyway).
- **Out of scope for this seat:** the row-level-vs-statement-level verdict split, the S021/S030/S032 corrections, and the counter's own arithmetic (owned by the `CounterCritic` / `MutateCounter` seats).

## 6. Bottom line

The freshness attack fails: today's document is byte-identical to the receipt's fetch (sha256 `d92217e0…faa3`, `Last-Modified Wed, 21 Oct 2026 13:04:30 GMT`), the quote is verbatim, unique across all 32 retained row texts, and located exactly where `anchorObserved` says it is, with both neighbouring landmarks confirmed; the 3.15.0 → 3.15.1 label move was caught and correctly characterised as in-family. The receipt's `HOLD` is correct. The actionable residue is four low-severity prose-completeness defects in the receipt itself (undisclosed unsupported "HTML5 tree construction" clause of its own row; entity-decoding attributed to names instead of values; an unqualified "no taught content changed"; a clause-prefix presented as a whole sentence), each fixable in one or two sentences without touching corpus bytes, quotes, or any counter result.

```json
{"target":".ufo/waves/round-26/rechecks/S026.json","verdict":"AGREE","severity":"low"}
```
