# FalsifyS031 — attack receipt `rechecks/S031.json` (verdict HOLD)

- Seat: `KakeR26-2.FalsifyS031` (reviewer, leaf — no dispatch). Axis: **freshness**. Milestone: `r26-recheck-falsify`. Checked 2026-10-21.
- Target: receipt `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-26/rechecks/S031.json` (HOLD, fetchIndex 1) and row line `corpus/SOURCES.md:39` (S031 — WHATWG HTML: Parsing HTML documents, in body and foreign content; teaches «In-body svg/math insert foreign elements; ordinary children take the foreign namespace, but breakout tags and integration points return to HTML rules»; anchor «13.2.6.4.7 in body (svg/math start tags) and 13.2.6.5 foreign content (any other start tag; breakout list incl. head); Living Standard last updated 20 October 2026, opened 2026-10-21»).
- Retained bytes `.ufo/waves/round-26/fetched/S031-1.raw.gz`; retained view `fetched/text/S031-1.txt`; provenance `fetched/manifest.json`; extractor `source_text.py` with pre-amendment copy `before/source_text.py`.
- Tooling: **no tool installed or upgraded this run** (no pacman/uv/pip/cargo action). Read-only checks used `python3` 3 stdlib (`gzip`, `hashlib`, `re`, `html.parser`), `sha256sum`, `wc`, `stat`, `git show`/`diff` (read-only), and **one plain public GET** of the row URL (bytes streamed in memory, not saved). No file outside this report was written; no corpus, script, fleet repo, sibling lane, Git index or jj state was touched.

## Verdict: AGREE (low) — the HOLD stands on freshness; two low-severity metadata/coverage defects survive

The substantive attack failed: the document has **not drifted at all** (byte-identical to the retained fetch, to the round-23 registered digest, and to today's live response), the quote is verbatim, unique, and it grounds the row's `teaches` inside the exact clause family the row's anchor names. What survives is (a) **stale text-view character offsets in `anchorObserved`**, measured against the pre-amendment extractor view, and (b) one clause of the `teaches` cell that the receipt asserts but does not locate.

---

## 1. Did content/version change in a way the receipt missed? — No. Zero drift, provable three ways.

**(a) Live GET today is byte-identical to the retained fetch.** One plain public GET of the row URL's document (`https://html.spec.whatwg.org/multipage/parsing.html`, the document of the recorded URL `…/parsing.html#parsing-main-inforeign`; bytes held in memory only, not saved):

```
$ python3 -c "urllib GET …"
status 200
headers {'Last-Modified': 'Tue, 20 Oct 2026 12:58:33 GMT', 'ETag': 'W/"6ad76579-c9b8f"',
         'Content-Type': 'text/html; charset=utf-8', 'Date': 'Wed, 21 Oct 2026 16:32:20 GMT'}
bytes 826255 sha256 a11dcf1768a76e24cdf7e16060f54bcb149c529aa8bcb9297b8d1ab633b26f13
Last Updated <span class=pubdate>20 October 2026</span>   (raw char 1372 of the same bytes)
```

That digest equals the retained bytes and the manifest entry for S031 (`fetched/manifest.json`: `row S031, index 1, status 200, bytes 826255, sha256 a11dcf1768a76e24cdf7e16060f54bcb149c529aa8bcb9297b8d1ab633b26f13, last-modified Tue, 20 Oct 2026 12:58:33 GMT, etag "6ad76579-c9b8f", fetchedAt 2026-10-21T15:10:50.839991+00:00`).

```
$ python3 -c "gzip.decompress(open('fetched/S031-1.raw.gz','rb').read())"
decoded 826255 sha256 a11dcf1768a76e24cdf7e16060f54bcb149c529aa8bcb9297b8d1ab633b26f13
```

**(b) The ETag strength flip is a content-coding artifact, not a version change.** The live response carried the **weak** validator `W/"6ad76579-c9b8f"` where the manifest recorded the strong `"6ad76579-c9b8f"`. Re-fetching with and without `Accept-Encoding: gzip` shows the strength follows the content coding while the payload is invariant:

```
Accept-Encoding None -> status 200 etag "6ad76579-c9b8f"     bytes 826255 sha256 a11dcf1768a76e24cdf7e160
Accept-Encoding gzip -> status 200 etag W/"6ad76579-c9b8f"    bytes 826255 sha256 a11dcf1768a76e24cdf7e160
```

So the ETag difference is not evidence of a newer document, and the receipt's digest-level argument is the right one.

**(c) The round-23 pin holds, and the receipt avoided the digest-swap trap.** The receipt states the decoded digest "equals round-23's registered S031 digest". That is true of round-23's *appended correcting register*, `corpus/lessons/round-23.md:206-212`:

> `- S031 correct response digest: a11dcf1768a76e24cdf7e16060f54bcb149c529aa8bcb9297b8d1ab633b26f13.`

(the same digest is at `.ufo/waves/round-23/residual/FixDocsEvidence.md:19` for `parsing.html`). The **table** row at `corpus/lessons/round-23.md:61` still prints `sha256 04b65bf0…` for S031 — the cross-assigned digest the lesson itself corrects at lines 206-212 and that `w1/ClaimCritic.md:66` flags. The receipt used the *correct* digest (`a11dcf17…`, verified live above), so the trap was not sprung.

**(d) No version bump is visible.** The masthead still reads `Last Updated 20 October 2026`, and `Last-Modified` is still `Tue, 20 Oct 2026 12:58:33 GMT` — the row's anchor cell ("Living Standard last updated 20 October 2026") is true of today's bytes.

## 2. Does the quote really ground THIS row's `teaches`, or is it page chrome / a neighbouring clause?

It grounds it, inside the clause family the row's anchor cell names, and it is unique.

- **Verbatim and unique.** In the committed text view the quote occurs exactly **once** (`[236219]`), and in the retained bytes the *normalized* string occurs once. It is not page furniture: it sits inside the `<dd>` of §13.2.6.5, inside the `<dl>` of "The rules for parsing tokens in foreign content", and the section id `parsing-main-inforeign` occurs exactly once in the raw (`len(re.findall(r'(?<![:\w-])id=parsing-main-inforeign(?![:\w-])', raw)) == 1`).
- **The `dd` it lives in is exactly the one the row's anchor names.** Raw markup, verbatim (unquoted `id=`, no `</dd>` closers in this document):

```
<dt>A start tag whose tag name is one of:  "b", "big", "blockquote", "body", "br", "center", "code", "dd",
   "div", "dl", "dt", "em", "embed", "h1", "h2", "h3", "h4", "h5", "h6", "head", "hr", "i", "img",
   "li", "listing", "menu", "meta", "nobr", "ol", "p", "pre", "ruby", "s", "small", "span", "strong", "strike",
   "sub", "sup", "table", "tt", "u", "ul", "var"<dt>A start tag whose tag name is "font", if the token has any
   attributes named "color", "face", or "size"<dt>An end tag whose tag name is "br", "p"<dd>
    <p>Parse error</p>
    <p>While the current node is not a MathML text integration point, an HTML integration point, or an element
       in the HTML namespace, pop elements from the stack of open elements.</p>
    <p>Reprocess the token according to the rules given in the section corresponding to the current insertion
       mode in HTML content.</p>
   <dt>Any other start tag<dd>
```

Three `dt`s share one `dd`, exactly as the receipt's `anchorObserved` says ("dd shared by the breakout start-tag list (b/big/…/head/…/var), the font-with-attrs start tag and the br/p end tag"). The breakout list contains **both `head` and `body`**, matching the row's anchor phrase "breakout list incl. head". The quoted sentence is the *operative consequence* of the breakout list — "breakout tags … return to HTML rules" — not a neighbouring clause: the next `dt` ("Any other start tag") is the foreign-insert branch, and the quote sits in the breakout branch's own `dd`.
- **The `teaches` clauses check out against the bytes.** Current-view offsets:
  - *in-body svg/math insert foreign elements* — §13.2.6.4.7: `A start tag whose tag name is "math"` @198156 → `Insert a foreign element for the token, with MathML namespace.` @198465; `"svg"` @198671 → `Insert a foreign element for the token, with SVG namespace.` @198980. (Both inside 13.2.6.4.7, whose heading is @176385 and which ends before 13.2.6.5 @234829.)
  - *ordinary children take the foreign namespace* — §13.2.6.5 "Any other start tag": `Insert a foreign element for the token, with the adjusted current node 's namespace.` @238062 (raw: `with the <a …>adjusted current node</a>'s namespace.`). The adjusted current node of an ordinary child of `<svg>`/`<math>` is the enclosing foreign element, so the child does take the foreign namespace. (The text view renders `node 's` with a space — an extractor artifact at the `</a>` boundary, not a document change; the w1 draft caveat already flags it.)
  - *breakout tags and integration points return to HTML rules* — the quoted sentence, plus the dispatcher branch `If the adjusted current node is an HTML integration point and the token is a start tag` @129172 → `Process the token according to the rules given in the section corresponding to the current insertion mode in HTML content.`
- **Row-specificity (the counter's own rule) holds.** The normalized quote occurs in exactly one retained view: `fetched/text/S031-1.txt`. S031 is not in `measure.py`'s document group `{S010,S028,S033}`, so no group exception is needed.

## 3. Falsify the anchor as recorded — LOW-severity defect #1 found

`rechecks/S031.json` `anchorObserved` claims:

> "… single-line text view char **236181**, immediately before the "Any other start tag" dt (raw HTML id=parsing-main-inforeign at **664526**); heading also in TOC char **5259** and body char **234791**"

The **raw-bytes** half is accurate, and the *relational* claim ("immediately before the 'Any other start tag' dt") holds in the committed view (quote ends 236343; `Any other start tag` starts 236344). The **text-view character offsets are stale**: they are the pre-amendment extractor's numbers, not the committed ones.

```
$ python3 -c "… source_text.text_of(load_gz('fetched/S031-1.raw.gz'),'text/html; charset=utf-8')"
committed view (source_text.py):  len 280111   quote at 236219..236343
committed file fetched/text/S031-1.txt:      280112 chars  quote at 236219..236343
pre-amendment view (before/source_text.py): len 280050   quote at 236181..236305
```

- Stated `236181` → actual **236219**; the asserted range 236181–236305 lands mid-word and does **not** contain the full quote:

```
view[236181:236305] = 'ents from the stack of open elements. Reprocess the token according to the rules given in the section corresponding to the c'
word-bounded match of the quote inside view[236181:236305] -> False
```

- Stated body heading `234791` → actual **234829** (234791 is 38 chars early, landing on `…Parse error. Ignore the token. 13.2.6.5 The rules for`).
- Stated TOC `5259` is **correct** (5259 in both views; the extractor change first bites at char 11407).

**Root cause (evidence, not speculation).** `source_text.py` was edited at 13:02:13 and all text views were re-extracted at 13:02:14; the offsets were measured before that and carried forward afterwards:

```
$ stat -c '%y %n' source_text.py before/source_text.py fetched/text/S031-1.txt w1/RowS031.md rechecks/S031.json
2026-10-21 13:02:13.677061524 -0300 source_text.py
2026-10-21 13:02:13.676671454 -0300 before/source_text.py
2026-10-21 13:02:14.249091818 -0300 fetched/text/S031-1.txt
2026-10-21 12:31:26.256392853 -0300 w1/RowS031.md
2026-10-21 13:04:31.603211455 -0300 rechecks/S031.json
```

The amendment is exactly the cause — `before/source_text.py` drops `]` from the no-space-before-punctuation rule and drops the second `html.unescape`:

```
-    return re.sub(r'(\()\s+', r'\1', re.sub(r'\s+([,.;:)\]])', r'\1', text))
+    return re.sub(r'(\()\s+', r'\1', re.sub(r'\s+([,.;:)])', r'\1', text))
-    return normalize(html.unescape(decoded) if looks_html else decoded)
+    return normalize(decoded)  # HTMLParser(convert_charrefs=True) already decoded references once
```

The first divergence between the two views is at char 11407 (`trailing "]] "` vs `trailing " ]] "`), and the accumulated drift is +38 chars by the quote. `w1/RowS031.md`'s own numbers (13.2.6.4.7 heading @176352, math branch @198123, svg branch @198638) are the *pre-amendment* values too — the draft was written at 12:31, before the extractor change, and the receipt (13:04) inherited them without re-measuring. The same pre-amendment numbers appear in `w1/PairS031StaticCanonicalPrefl.md` (198947 / 236008 / 129146 / 238024 / 235666 / 239665) and that report's file claim ("280,153 bytes, sha256 36d5001a…") — the committed file is **280,206 bytes, sha256 6ac17696dbda9eaa…**. Those two files are other seats' artifacts and outside this leaf's scope; I record them only as the same-root-cause cross-reference.

**Effect on the counter: none.** `measure.py` checks `anchorObserved` only for being a non-empty string (`measure.py:361-370`); it does not validate offsets. The committed candidate therefore still measures 32/32, exit 0 (`verification/measure-candidate.json`: `decided 32, hold 32, stale 0, unverifiable 0, findings []`), and the receipt's `quote` still passes `quote_in_text` under the committed extractor (`re.search(r'(?<!\w)'+escape(normalize(quote))+r'(?!\w)', text)` → True).

**Minimal correction** (metadata only — no verdict change, no `correction` field; HOLD receipts must carry `correction: null`):

> `anchorObserved`: "13.2.6.5 The rules for parsing tokens in foreign content — dd shared by the breakout start-tag list (b/big/…/head/…/var), the font-with-attrs start tag and the br/p end tag; single-line text view char **236219** (quote span 236219-236343), immediately before the "Any other start tag" dt (raw HTML id=parsing-main-inforeign at **664526**); heading also in TOC char 5259 and body char **234829**"

## 4. LOW-severity defect #2 — one `teaches` clause is asserted but not located

The `teaches` cell has three clauses. The receipt's `reason` locates two of them (in-body math/svg foreign insertion; breakout list incl. head/body; integration-point start tags routed to HTML content) but never locates the middle one, *"ordinary children take the foreign namespace"*, which lives in a different `dd` — §13.2.6.5 "Any other start tag" (`Insert a foreign element for the token, with the adjusted current node's namespace.`, current-view char 238062). The receipt's blanket "Scope, teaches and anchor all hold" therefore rests on that clause unquoted, and its `anchorObserved` mentions the "Any other start tag" `dt` only as a boundary marker, not as the source of the foreign-namespace rule.

I checked the clause against today's bytes and it **holds** (`adjusted current node` of an ordinary child of a foreign element is that foreign element, so the child is in the foreign namespace), so this is a coverage gap in the receipt's justification, not a STALE finding and not a verdict change.

**Minimal correction** (append one clause to `reason`; `correction` stays `null`):

> "… and §13.2.6.5's 'Any other start tag' branch still inserts ordinary foreign children with the adjusted current node's namespace ('Insert a foreign element for the token, with the adjusted current node's namespace.'), so ordinary children take the foreign namespace."

## 5. Precision notes (no verdict effect, no correction)

- The receipt's `reason` says breakout tokens "are reprocessed under the HTML insertion mode". The spec text is "Reprocess the token according to the rules given in the section corresponding to the current insertion mode **in HTML content**." There is no "HTML insertion mode"; the operative qualifier is *in HTML content* (i.e. HTML, not foreign, interpretation under the current mode's rules). The paraphrase does not change the meaning but is looser than the quoted text.
- The raw locator "id=parsing-main-inforeign at 664526" is a **decoded-character** offset (byte offset in the decoded body is 664620; the `<h5 id=parsing-main-inforeign>` tag starts at 664522). It is accurate as stated because no unit is claimed, but pinning the unit would avoid the ambiguity that `w1/RowS030.md`'s parallel raw locator ("byte 23907", a char offset) creates lane-wide.
- `measure.py`'s token/word rule is satisfied by this quote: 20 alphanumeric tokens (≥6 required) and 20 whitespace words (≤25 required).

## 6. Residual risk / verification gaps

- **Residual risk (low, lane-wide, not row-specific):** the shared extractor `source_text.py` changed mid-wave and every text view was re-extracted at 13:02:14, so *any* receipt citing text-view character offsets measured before that is stale in the same way. Scanning all 32 receipts against the committed view, the materially stale ones are S011 (14663→14677), S024 (10160→10172), S025 (62596→62638), S031 (236181→236219) and S034 (8863→8864); S018/S021/S030 happen to cite offsets that the extractor change did not move. Other Falsify seats own their rows; I report only S031.
- **The offsets are a locator convenience only.** The quote string, the section identity, the raw-bytes anchor, the digest pin and the `HOLD` verdict all verify independently against retained and live bytes, so no ledger statement, corpus lesson, `SOURCES.md` cell or counter result is affected.
- **Living Standard is a rolling document.** The row pins "last updated 20 October 2026", true of today's bytes; the same URL will serve different bytes once the standard rolls, so the row's `recheck 90d` cell — not this receipt — is the mechanism that re-establishes the pin. This receipt's HOLD is a statement about the 2026-10-21 bytes, and it is correct for them.
- **Verification gaps:** (i) I did not fetch the `#parsing-main-inforeign` fragment URL itself (the fragment is client-side only); I confirmed the section id occurs exactly once in the byte-identical document. (ii) I did not re-run `measure.py` (owned by another seat); I reimplemented its S031-relevant rules (`quote_in_text`, token/word counts, row specificity, key set, HOLD⇒`correction: null`) directly and read the committed `verification/measure-candidate.json`. (iii) The corpus-level statements citing S031 (`corpus/knowledge/static-canonical-preflight.md:98-117`) were adjudicated by the pair seat (8 statements, 0 STALE) and are outside this leaf's scope; the three spec facts they rest on were re-verified here against today's bytes (§2).

## 7. Bottom line

The freshness attack fails: today's live response is byte-for-byte the document read on 2026-10-21 and on 2026-10-20 (sha256 `a11dcf17…`, 826,255 bytes, `Last Updated 20 October 2026`), the §13.2.6.5 breakout `dd` and its `head`-containing list are unchanged and unique, and the quote carries the row's `teaches` rather than chrome or a neighbouring clause. The receipt's `HOLD` is correct. Two low-severity items are actionable: restate the `anchorObserved` text-view offsets as **236219** (quote span 236219-236343) and **234829** (13.2.6.5 body heading) instead of 236181/234791, and add one clause to `reason` locating the "ordinary children take the foreign namespace" rule at §13.2.6.5 "Any other start tag" (`Insert a foreign element for the token, with the adjusted current node's namespace.`). Neither changes the verdict, the quote, `correction: null`, or any counter result.

```json
{"target":".ufo/waves/round-26/rechecks/S031.json","verdict":"AGREE","severity":"low"}
```
