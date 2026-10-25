# Scribe — entry audit of S262/S263 (round 51, wave 1)

Seat: `L1Kake51.ScribeEntryAudit-2`. Scope: read the two assimilated entries as prose,
test every quote against the retained bodies I scanned myself, test every assertion
against the row it cites, and propose append-ready wording. Entries were **not edited**.
Only this file was written. Scratch lived in `/tmp/sa/` (`audit.py`, `s262_body.txt`,
`s263_body.txt`); the scan script is inlined in §11, so nothing here depends on that
scratch surviving an external sweep.

Frozen claims I was asked to attack: C1 (wave-evidence ledger, operability) and C2
(two entries on rows S262/S263, freshness). Judged axis: freshness.

**Revision audited: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` (committed bytes).**
`git show 9d13768:corpus/knowledge/canonical-selection.md | sed -n '37p'` and
`… crawler-identity.md | sed -n '12,13p'` reproduce the strings quoted below verbatim, so
every line number in §2-§6 is a line of the measured revision.

---

## 0. Bottom line

| Question | Result |
|---|---|
| Are the two Gate quotes raw substrings? | **Yes** — both. `"indicating a canonical preference is a hint, not a rule"` at S262 byte offset 140571; `"Googlebot is the generic name for two types of"` at S263 byte offset 137277. |
| Are the entries' other quotes faithful? | **No.** 7 of 15 quoted spans are not substrings of the retained bytes raw, whitespace-collapsed, **or** tag-stripped. They exist only if every HTML tag is replaced by a space — an artifact that changes the page's punctuation. |
| Do the entries' class labels match a scan? | **No.** 10 of 13 labelled spans carry a label that my scan contradicts; 2 spans carry two mutually exclusive labels (raw *and* collapsed-only). |
| Do the entries' prose assertions exceed their cited row? | **Yes — 16 findings** (7 in `canonical-selection.md`, 9 in `crawler-identity.md`); three of them are contradicted by the cited page itself. |
| Are the entry headers' `§` citations real sections? | **No**, in both entries: S262's `§` is a devsite nav label (the page's `h1` is "What is canonicalization"); S263's `§` is the page's first sentence, not a heading. |
| Does C2's 8/8 cover any of this? | **No.** `c51_quote_truth.py` checks only the two lesson Gate quotes (C5) plus row shape/receipts/mirror ordering. Every defect below is scored as a pass. |
| Is the "pre-append mirror" pre-append? | **No.** It is byte-identical to the post-append corpus (details in §5). |

None of the defects requires rewriting the entries' theses. The theses are supported;
the quotations and the derived rules are not.

---

## 1. Bytes I pinned and the scan I ran

```
sha256sum .ufo/waves/round-51/sources/S262.html
792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b   (174926 B)
sha256sum .ufo/waves/round-51/sources/S263.html
6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de   (175561 B)
```

Both match `.ufo/waves/round-51/sources/receipts.json` exactly (sha256 and byte count).
No `.txt` blob and no class ledger exist for round 51: `sources/` holds only
`S262.html`, `S263.html`, `receipts.json`.

Scan semantics used below (my instrument, reproduced verbatim in §11, not the lane's):

1. `raw` — the quoted string is a byte substring of the retained `.html`.
2. `ws-collapsed` — not raw, but present after `re.sub(r"\s+", " ", body)` (line wraps only).
3. `tag-stripped` — not either of the above, but present after deleting tags **without
   inserting anything** (`re.sub(r"<[^>]+>", "", body)`), unescaping entities, collapsing
   whitespace. This is the text a browser renders for inline markup: HTML does not
   synthesize a space at a tag boundary.
4. `tag-space` — present only if each tag is replaced by a space. This is a **misquote**:
   the inserted space appears in the quoted string as punctuation the page does not have.

The lane's own taxonomy (`corpus/QUALITY.md:1100-1106`) allows exactly two classes:
`raw-substring` (substring of the retained HTML) and `collapsed-only` ("survives only
whitespace collapse"). `c50_quote_class.py:101-107` implements it as
`if quote in raw -> raw-substring; elif quote in text -> collapsed-only`, where `text`
is a committed `.txt` blob (`BLOBS`, lines 49-53) and the result is pinned in
`quote-classes.json`. Round 51 commits neither a `.txt` blob nor a class ledger, so
**no class label in either entry is re-derivable by the lane's own instrument.**

---

## 2. `corpus/knowledge/canonical-selection.md` — quotes

| # | Line | Quoted span (abridged) | Entry's label | My derived class | Verdict |
|---|---|---|---|---|---|
| 1 | 15 | `indicating a canonical preference is a hint, not a rule.` | none ("quoted from the section") | `raw` | OK; the **section name is wrong** (see §4) |
| 2 | 21 | `There are a handful of factors … rel="canonical" link annotations.` | `collapsed-only` + "the source breaks the sentence across lines" | `tag-stripped` | text OK, **class wrong** (two `code` elements interrupt; collapse alone cannot yield it) |
| 3 | 27 | `… based on the factors (or signals ) the indexing process …` | `collapsed-only` | `tag-space` | **MISQUOTE** — page text is `(or signals)`; the space comes from `<em>signals</em>` |
| 4 | 32 | `You can indicate your preference to Google using these techniques …` | `collapsed-only` | `tag-stripped` | text OK, **class wrong** (`<a>` around "indicate your preference to Google") |
| 5 | 39 | `Device variants : for example …` | group label "each quoted **raw** from the page" | `tag-space` | **MISQUOTE** — page text is `Device variants:` (`<b>` boundary); label also false |
| 6 | 40 | `Protocol variants : for example …` | group label "raw" | `tag-space` | **MISQUOTE**; label false |
| 7 | 41 | `Site functions : for example … category page` | group "raw" **and** `(collapsed-only quote)` | `tag-space` | **MISQUOTE**; two contradictory labels on one span |
| 8 | 43 | `Accidental variants : for example …` | group "raw" **and** `(collapsed-only quote)` | `tag-space` | **MISQUOTE**; two contradictory labels on one span |
| 9 | 49 | `the search result will probably point to the mobile page …` | `collapsed-only` | `ws-collapsed` | **OK** — the only correctly classed quote in this entry |
| 10 | 60 | `objectively the most complete and useful for search users` | none (inline) | `raw` | OK |

Notes on the source, byte-verified:

- `rel="canonical"</code> <code …>link</code>` — two adjacent code elements; the rendered
  span keeps a single space, so quote 2's *text* is right while its stated derivation
  (line break only) is wrong.
- `(or <em>signals</em>)` — quote 3 is the tag-space artifact, not the page.
- `<b>Device variants</b>: for example, …` — the colon abuts `</b>`; there is no space
  before any of the four colons. Same for `Protocol variants`, `Site functions`,
  `Accidental variants`.
- `For example, the search result will probably point to the\n  mobile page …` — quote 9
  is genuinely a line-wrap-only span.

**Contradiction inside the entry.** Line 37 says "each quoted raw from the page" for all
four bullets; lines 42 and 44 then label two of those same bullets `collapsed-only`.
The same rule forbids that: "a collapsed-only span is never described as a raw
substring nor the reverse".

---

## 3. `corpus/knowledge/crawler-identity.md` — quotes

| # | Line | Quoted span (abridged) | Entry's label | My derived class | Verdict |
|---|---|---|---|---|---|
| 11 | 10 | `Googlebot is the generic name for two types of` | `quoted raw from the page` | `raw` | **OK** (the raw line break falls after "of") |
| 12 | 15 | `Googlebot Smartphone : a mobile crawler … mobile device` | `collapsed-only` + "the source puts a space before the colon and breaks the lines" | `tag-space` | **MISQUOTE** — page text is `Googlebot Smartphone:` (`</a>:`); the "space before the colon" explanation is **false** |
| 13 | 17 | `Googlebot Desktop : a desktop crawler … on desktop` | same label | `tag-space` | **MISQUOTE**; same false explanation |
| 14 | 21 | `You can identify the subtype of Googlebot by looking at the HTTP user-agent request header …` | `collapsed-only` | `tag-stripped` | text OK, **class wrong** (`<a>` + `<code>user-agent</code>`) |
| 15 | 26 | `both crawler types obey the same product token (user agent token) in robots.txt` | `collapsed-only` | `ws-collapsed` | **OK** |

Byte-verified source for 12/13:

```
<a href="…google-common-crawlers#googlebot-smartphone"><b>Googlebot Smartphone</b></a>:
    a mobile crawler that simulates a user on a mobile device.
```

There is no whitespace between `</a>` and `:`. The newline is **after** the colon. The
entry's claim that "the source puts a space before the colon" is a misreading of the
tag-space artifact its own extraction produced.

---

## 4. `§` citations in both headers

**S262** (line 1, and registry row S262's anchor cell):
`§ "What is URL canonicalization"`. That string occurs **once** in the retained body, at
offset 73,197, inside `<span class="devsite-nav-text" tooltip>What is URL canonicalization</span>`
— a navigation label. The document's `h1` (offset 137,274) is
`<h1 class="page-title" id="what-is-canonicalization" …>What is canonicalization</h1>`.
The paragraphs the entry quotes sit under the `h3`
`"How Google indexes and chooses the canonical URL"` (heading text at offset 139,140) — except the
duplicate-content list (intro at offset 137,826), which sits in the page intro above that heading.
So the `§` names neither the page title nor the section that contains the quotes.

**S263** (line 1, and registry row S263's anchor cell):
`§ "Googlebot is the generic name for two types of web crawlers used by Google Search"`.
This is the page's first body sentence, not a heading. The page's headings are `h1`
"Googlebot", `h2` "How Googlebot accesses your site", `h2` "Blocking Googlebot from
visiting your site", `h2` "Verifying Googlebot". The sentence is also **not** a raw span:
its subject complement is wrapped, `<a …>web crawlers</a> used by Google Search:`.

---

## 5. Provenance: the "pre-append mirror" is a post-append copy

This is my strongest freshness finding and it is entirely mechanical.

```
$ git show 19a99bd:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md | grep -c '^| S262 '
1
$ git show 19a99bd:corpus/SOURCES.md | grep -c '^| S262 '
0
$ git rev-parse 19a99bd:.ufo/waves/round-51/…/pre-append/corpus/SOURCES.md
9e2a22175ef95a23252b349d8743cf0e5b5480fc
$ git rev-parse 5591557:corpus/SOURCES.md
9e2a22175ef95a23252b349d8743cf0e5b5480fc
$ git rev-parse 19a99bd:.ufo/waves/round-51/…/pre-append/corpus/lessons/round-51.md
dc9ab00ab051a232ead917068bda21b52fbb1f0c
$ git rev-parse 5591557:corpus/lessons/round-51.md
dc9ab00ab051a232ead917068bda21b52fbb1f0c
```

- The mirror's `corpus/SOURCES.md` **is the same blob** as the post-append root registry
  (commit `5591557`) and carries both S262 and S263 rows.
- The mirror's `corpus/knowledge/canonical-selection.md` and `crawler-identity.md` are
  byte-identical to the landed entries (`diff` empty for both).
- The mirror also carries `corpus/lessons/round-51.md` — a file whose only root-side
  introduction is the append commit itself.
- Both artifacts are committed in `19a99bd`, which `git log --diff-filter=A` reports as
  the mirror's adding commit and which C8 uses as `mirror_commit`.

Consequences, stated as bytes, not inference:

1. The census receipt (`census-argv.txt` → `sources-census.sh validate --file …/pre-append/corpus/SOURCES.md`,
   exit 0, stdout ending `ok …/pre-append/corpus/SOURCES.md`, no E03/E04) validates a
   registry that **already contains** the rows being appended. It cannot evidence that
   the append introduced no census defect.
2. C2's prose condition C8 says "the registry at that mirror carries none of the adopted
   ids". Of the mirror *file*, that is **false**. It passes only because
   `c51_quote_truth.py:277` reads `show(root, mirror_commit, REGISTRY)` where
   `REGISTRY = "corpus/SOURCES.md"` — the **root** path at the mirror commit — and never
   reads `MIRROR`. C7 reads the mirror path; C8 does not. The two conditions therefore
   inspect different files, and the provenance sentence the lesson relies on
   ("the mirror census-validated with `--file` before the append") is not what the
   committed bytes show.

I did not evaluate C1 (wave-evidence ledger). I make no claim about it.

---

## 6. Sentences that assert more than the cited row supports

Line numbers are the entry's. "Row" = the SOURCES.md row the entry cites (S262 or S263);
"held entry" is named where the entry asserts something about lane holdings.

### `canonical-selection.md`

| Line | Sentence (abridged) | Why it exceeds the row |
|---|---|---|
| 12-13 | "quoted from the section 'What is URL canonicalization'" | Not a section; nav label. See §4. |
| 17-18 | label: "the source breaks the sentence across lines" | Omits that two `code` elements split the sentence; line breaks alone do not yield the span. |
| 37 | "The page lists the variant classes it recognises, each quoted raw from the page" | (a) the page's own frame is "There are many reasons why a site may have duplicate content" (offset 137,826), not "variant classes it recognises"; (b) the list has **five** items — `Region variants` (offset 137,908) is omitted; (c) "raw" is false for all four quoted items. |
| 54-57 | "A declared canonical can be ignored, and **a page with no declaration still gets one**." | First clause is supported ("Google may choose a different page as canonical than you do"). The second is nowhere in S262. The nearest support is an inference from "factors … whether the page is served over HTTP or HTTPS, redirects, presence of the URL in a sitemap, and rel=canonical link annotations". |
| 58-61 | "The steering signals are the ones **the lane already owns**: HTTPS, redirects, sitemap inclusion and the canonical element." | Uncited ownership claim. Verified: redirects → `corpus/knowledge/redirect-rewrite-rules.md` (S050/S135); sitemap → `corpus/knowledge/sitemap-orphan-audit.md`; canonical element → `corpus/knowledge/static-canonical-preflight.md` (S021); **HTTPS** → no held entry matched `grep -rl "enforce HTTPS\|Enforce HTTPS\|HTTPS enforcement" corpus/knowledge/*.md` (0 files). |
| 62-64 | "With S021 … and S022 … the lane already held two of Google's three canonicalization pages; S262 supplies the frame those two assume." | The three-page grouping is real, but only as a devsite nav group (three items: `canonicalization`, `consolidate-duplicate-urls`, `canonicalization-troubleshooting`), not as prose. S021/S022 identification matches rows 29-30. "S262 supplies the frame those two assume" is a claim about two other entries that S262 cannot support. |
| 68-69 | "Baidu publishes a different account (a quality comparison)" | `grep -ci baidu corpus/SOURCES.md` → **0**. No Baidu row exists in this lane; the scope note asserts an unretained vendor fact. |

Verified as supported (no change needed): lines 8-10 vs
`static-canonical-preflight.md:8-9` ("This entry owns publisher-side static-file
validation, not browser crawling or search-engine canonical selection"); line 75-77
revision line — the body contains `<p>Last updated 2026-08-20 UTC.</p>` at offset 143,657.

### `crawler-identity.md`

| Line | Sentence (abridged) | Why it exceeds the row |
|---|---|---|
| 8-13 | header `§` + "the source puts a space before the colon and breaks the lines" | § is not a heading; and there is no space before the colon in the source (`</a>:`), so the stated reason is false. |
| 30-33 | "**A user-agent string is the only thing a server log records about the crawler.**" | Not in S263, and **contradicted by it**. S263's "Verifying Googlebot" section says the UA "is often spoofed by other crawlers" and "The best way to verify that a request actually comes from Googlebot is to use a reverse DNS lookup on the source IP of the request, or to match the source IP against the Googlebot IP ranges." A server log records that source IP. The page's own answer to "who is on the wire" is IP-based, and the entry omits the section entirely. |
| 31-33 | "a log line saying 'Googlebot' does not say whether the fetch was the mobile or the desktop variant" | Contradicted by the sentence the entry itself quotes two blocks earlier: "You can identify the subtype of Googlebot by looking at the HTTP user-agent request header in the request." True only for a log that stores the bare token instead of the header. |
| 32-33 | "and therefore does not say which **viewport** the fetched HTML was produced for" | S263 never discusses viewports. Its adjacent claims are "Google Search primarily indexes the mobile version of the content" and "the majority of Googlebot crawl requests will be made using the mobile crawler" (offset 138,437). The viewport sentence is the entry's inference. |
| 34-37 | "The same page can be crawled twice by the same engine under two names." | Not asserted anywhere in S263. Plausible, but unsourced. |
| 36-37 | "a canonical conclusion drawn from a declared element is ambiguous" | Cross-entry analogy with no citation, and it misstates the sister entry: a declared canonical is not "ambiguous", it is non-binding (S262: "a hint, not a rule"). |
| 38-40 | "a fact the lane's own robots reading **(S011)** and Google's robots interpretation (S095) do not answer" | Category error: S011 is an RFC 9309 **row**, not an entry. The lane's held robots reading is `corpus/knowledge/robots-txt-rules.md`, which cites S011/S095/S096. The substantive negative holds: that entry contains no Smartphone/Desktop mention (`grep` → 0 matches). |
| 47-48 | "It does not establish Google's crawl rate, its scheduling" | Misleading scope note: the page **does** state a crawl rate ("shouldn't access your site more than once every few seconds on average"), a 2 MB/64 MB fetch limit, and the Pacific Time crawl timezone. Honest only if read as "this entry does not restate", which the sentence does not say. |
| 49-50 | "the page lists them" (non-Google bots) | False about the page: 0 occurrences of `Googlebot-Image`, `Googlebot-News`, `AdsBot`, `Storebot`, `GoogleOther`, `Google-InspectionTool`, `Feedfetcher`. The page links twice to `google-common-crawlers` (for its own two subtypes), it does not enumerate other bots. |

Verified as supported: line 41-43 `S096` characterisation (row S096: "Google's released
robots.txt parser and matcher library … not all crawler policy outside parsing and
matching"); lines 53-54 revision line (`<p>Last updated 2026-02-03 UTC.</p>` at offset 144,362).

---

## 7. Append-ready wording (proposed, not applied)

### 7.1 Quote blocks — corrected text and honest class labels

`canonical-selection.md`, replacing lines 17-44:

```
The page then states what the hint is weighed against [S262]. The span is not in the raw
HTML: two `code` elements and a line break interrupt it, and it appears only after the
elements are removed (a rendered-text quote, not a whitespace-collapse quote):

> "There are a handful of factors that play a role in canonicalization: whether the page is
> served over HTTP or HTTPS, redirects, presence of the URL in a sitemap, and
> rel="canonical" link annotations."

and what the outcome is [S262] (rendered-text quote, same derivation):

> "Google then chooses the page that, based on the factors (or signals) the indexing
> process collected, is objectively the most complete and useful for search users, and
> marks it as the canonical."

The page also says plainly [S262] (rendered-text quote; an `<a>` element splits the first
clause):

> "You can indicate your preference to Google using these techniques, but Google may choose
> a different page as canonical than you do, for various reasons."

## Why duplicates exist at all [S262]

The page's own frame is a list of reasons rather than a taxonomy. It introduces five
items with "There are many reasons why a site may have duplicate content:" — all five are
rendered-text quotes (each label is wrapped in `<b>`):

- "Region variants: for example, separate USA and UK URLs with hreflang, but essentially
  the same content in the same language"
- "Device variants: for example, a page with both a mobile and a desktop version"
- "Protocol variants: for example, the HTTP and HTTPS versions of a site"
- "Site functions: for example, the results of sorting and filtering functions of a
  category page"
- "Accidental variants: for example, the demo version of the site is accidentally left
  accessible to crawlers"
```

The mobile/desktop passage (line 49) needs no change; it is the one `collapsed-only`
span in the entry and the label is correct.

`crawler-identity.md`, replacing lines 12-26:

```
and names the two types beneath it [S263] (rendered-text quotes: each name is wrapped in
an `<a>` around a `<b>`, and the newline falls after the colon — there is no space before
the colon):

> "Googlebot Smartphone: a mobile crawler that simulates a user on a mobile device."

> "Googlebot Desktop: a desktop crawler that simulates a user on desktop."

The page says how the two are told apart [S263] (rendered-text quote; an `<a>` and an
inline `<code>user-agent</code>` interrupt the sentence):

> "You can identify the subtype of Googlebot by looking at the HTTP user-agent request
> header in the request"

and states the consequence for robots.txt [S263] (collapsed-only quote — a line break is
the only interruption):

> "both crawler types obey the same product token (user agent token) in robots.txt"
```

### 7.2 Derived rules — rewrites

`crawler-identity.md`, replacing lines 30-43:

```
- **The full user-agent header names the subtype; the bare token does not.** The page says
  the subtype is identified by "looking at the HTTP user-agent request header in the
  request" [S263]. A log line that stores only "Googlebot" therefore does not say whether
  the fetch was the mobile or the desktop crawler; one that stores the header does.
- **The header is not proof of origin.** The page's "Verifying Googlebot" section says the
  HTTP user-agent request header "is often spoofed by other crawlers", and that the best
  verification is "a reverse DNS lookup on the source IP of the request, or … match the
  source IP against the Googlebot IP ranges" [S263]. For a publisher reading a crawl log,
  identity rests on the source IP, not on the UA string.
- **Search prefers the mobile crawler.** The page says Google Search "primarily indexes the
  mobile version of the content" and that "the majority of Googlebot crawl requests will be
  made using the mobile crawler" [S263]; a per-device conclusion drawn from request volume
  alone therefore over-counts the mobile crawler by design.
- **The robots product token does not separate them.** Both types obey the same product
  token, "and so you cannot selectively target either Googlebot Smartphone or Googlebot
  Desktop using robots.txt" [S263]. The lane's held robots entry
  (`corpus/knowledge/robots-txt-rules.md`, rows S011 and S095) and S096's parser both stop
  at rule evaluation; neither answers agent identity.
```

`crawler-identity.md`, replacing lines 47-50:

```
- It does not restate the page's crawl-rate, fetch-size or timezone statements (the page
  gives "not … more than once every few seconds on average", a 2 MB file / 64 MB PDF fetch
  limit, and Pacific Time); those belong to the held crawl-budget entry (S273, S274).
- It does not enumerate the other Google crawlers; the page links to
  `google-common-crawlers` for that list rather than listing them itself.
```

`canonical-selection.md`, replacing lines 54-64:

```
1. **Declaration and selection are two different acts.** Google may choose a page other
   than the declared one [S262], so any check that treats the declared value as the indexed
   value is wrong — which is why the held preflight is a *preflight* and not a selection
   claim. S262 does not state what happens when a page carries no declaration at all; that
   case is outside this row.
2. **The steering signals are the ones the lane already holds.** Redirects are held in
   `corpus/knowledge/redirect-rewrite-rules.md` (S050/S135), sitemap inclusion in
   `corpus/knowledge/sitemap-orphan-audit.md`, and the canonical element in
   `corpus/knowledge/static-canonical-preflight.md` (S021). HTTPS is not currently held as
   an entry, so this entry does not claim it. The new ground here is that the signals are
   "factors [that] play a role" and the outcome is "objectively the most complete and
   useful for search users", not a declared preference.
3. **This is the third page in Google's canonicalization nav group.** The retained body's
   navigation lists exactly three items under Canonicalization — this page, "How to specify
   a canonical URL with rel=canonical" (the lane's S021) and "Fix canonicalization issues"
   (S022). Whether S021 and S022 assume S262's frame is their own claim (S022's recorded
   scope is "Declared canonical versus Google-selected canonical"); it does not follow from
   S262.
```

`canonical-selection.md`, replacing lines 68-69:

```
- It does not establish the selection rule for any other engine. S262 does not discuss any
  other engine, and this lane holds no Baidu row (`corpus/SOURCES.md` has none), so no
  cross-engine comparison is made here.
```

### 7.3 Headers and registry anchors

Entry line 1 of `canonical-selection.md`:

```
source: S262 — https://developers.google.com/search/docs/crawling-indexing/canonicalization — page "What is canonicalization" (nav label "What is URL canonicalization"); the selection quotes are § "How Google indexes and chooses the canonical URL" and the duplicate-content list is the page intro (doc rev. Last updated 2026-08-20 UTC) — fetched 2026-10-24
```

Entry line 1 of `crawler-identity.md`:

```
source: S263 — https://developers.google.com/search/docs/crawling-indexing/googlebot — page "Googlebot"; § page body, first paragraph, and § "Verifying Googlebot" (doc rev. Last updated 2026-02-03 UTC) — fetched 2026-10-24
```

`corpus/SOURCES.md` row S262 anchor cell (repeat of the same error):

```
§ "How Google indexes and chooses the canonical URL"; page "What is canonicalization" (doc rev. Last updated 2026-08-20 UTC)
```

`corpus/SOURCES.md` row S262 teaches cell — the phrase "a declared canonical is a hint, not
a rule" is **not** a substring of the body (`q in raw` → False); substitution:

```
indicating a canonical preference is a hint, not a rule; Google chooses the page that is objectively the most complete and useful for search users, weighing HTTP/HTTPS, redirects, sitemap presence and rel="canonical" link annotations
```

`corpus/SOURCES.md` row S263 anchor cell:

```
§ page body, first paragraph ("Googlebot is the generic name for two types of web crawlers used by Google Search"); page "Googlebot" (doc rev. Last updated 2026-02-03 UTC)
```

`corpus/SOURCES.md` row S263 teaches cell — add the consequence the row currently drops:

```
Googlebot is a generic name covering Googlebot Smartphone and Googlebot Desktop; the subtype is identified from the HTTP user-agent request header; both obey the same robots product token, so robots.txt cannot target one subtype
```

### 7.4 Taxonomy option (if the entries keep any tag-interrupted quote)

The two-class vocabulary cannot express these spans. Either (a) restrict entries to spans
that are `raw-substring` or `collapsed-only` in the lane's sense, or (b) add a third derived
class — `rendered-only`: present in the tag-stripped text, absent from both the raw HTML
and the whitespace-collapsed raw — with its own committed `.txt` blob and sha256, and
extend `c50_quote_class.py`'s `classify()` so a swapped label still fails. Option (b) is
what the round-51 quotes actually need, but it is a `QUALITY.md` + instrument change, not
an entry-only edit.

---

## 8. Commands run (read-only) and observed output

```
python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 9d13768c4fdd0e9a2688d2ecf1616b539cf57658
C2 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)
  C1_entries_exist pass
  C2_entry_cites_id pass
  C3_row_shape pass
  C4_used_by pass
  C5_gate_quote_truth pass
  C6_receipt_pins pass
  C7_validate_before_append pass
  C8_append_after_mirror pass
exit=0
```

C5's implementation (`c51_quote_truth.py:193-220`) reads the two lesson Gate quotes only;
no entry quote is parsed, and no class label is tested. That is why the defects in §2-§3
and §6 score as passes.

Other read-only probes used: `sha256sum`, `git show <rev>:<path>` (blob hashes, registry
row counts), `git rev-parse <rev>:<path>`, `git log --diff-filter=A`, `grep`/`sed`/`wc`,
and a Python scan (reproduced in §11). No mutating git or `jj` command; no network; no
package install or upgrade (nothing was needed).

One contract-shape note: the frozen C2 condition says "below its **8-line** metadata
header", while both entries carry 4 metadata lines (`source`, `verified-at`, `recheck`,
`ground`) before the `h1`. The counter implements the condition as "the id appears after
line 8", so both pass regardless; the condition text and the entries' house style do not
agree on what an 8-line header is.

## 9. What I could not read / did not run

- C1's ledger: not evaluated by this seat; no claim made.
- No `.txt` blobs or class ledger exist for S262/S263, so the lane's own class instrument
  could not be run against these ids even in principle (§1).
- Live HTTP verification of either URL was not attempted: this seat audits committed
  bytes, and the receipts' sha256/URL pairs already tie the bodies to the rows.

## 10. Working-tree observation (not my edit)

Both entries were modified in the working tree at `03:39:51 -0300` by a sibling seat
(`ExecQuoteRawScan`), after this seat had read them and before this report was written.
`git status --porcelain`:

```
 M corpus/knowledge/canonical-selection.md
 M corpus/knowledge/crawler-identity.md
```

I did not make or revert those edits. They are uncommitted, so they do not affect the
measured revision's score. Their substance agrees with §2-§3 on the counts (15 body
quotations; 3 raw, 2 collapse-only, 10 needing markup removal; 7 not recoverable as
rendered text), and the new "Quote classes" sections retract the "raw"/"collapsed-only"
labels that §2 and §3 flag.

One divergence remains. The working-tree text keeps the literal strings
`"Device variants :"`, `"Protocol variants :"`, `"Site functions :"`,
`"Accidental variants :"`, `"Googlebot Smartphone :"`, `"Googlebot Desktop :"` and
`"(or signals )"`, and describes the space as "this entry's rendering". An HTML tag
boundary emits no character, so the page renders `Device variants:` and `(or signals)`;
the space is a property of a tag-to-space extraction, not of any rendering a reader sees.
§7.1 therefore proposes the colon-adjacent forms rather than only relabelling the strings.

## 11. Appendix — the scan, inline

Scratch is not evidence, and this report cites no scratch tree: the appendix is the
evidence locus. The script below is the one that produced the "My derived class" column of
§2-§3; it reads the two committed bodies by their repo-relative paths, and the quote list is
a transcription of the strings in the entries at revision `9d13768`. Run it from the lane
root (`python3 -B audit.py`) to reproduce the classification.

**Provenance of the block: original bytes, not a reconstruction.** The source file was never
lost, and the fenced block below was extracted back out of this report and hashed:
`sha256 7bf8cf232e690a25e099f049d464261eb07305d3d64207acd81dfa1876a0d5b4`, 3391 B, equal
to the source on both counts (`diff` empty). A rebuild would not be evidence; this is not
one.

```python
import re,html,json
def load(p):
    b=open(p,encoding="utf-8",errors="replace").read(); return b
def collapse(s): return re.sub(r"\s+"," ",s)
def strip_nospace(s):
    s=re.sub(r"<script.*?</script>","",s,flags=re.S); s=re.sub(r"<style.*?</style>","",s,flags=re.S)
    s=re.sub(r"<[^>]+>","",s); return collapse(html.unescape(s))
def strip_space(s):
    s=re.sub(r"<script.*?</script>","",s,flags=re.S); s=re.sub(r"<style.*?</style>","",s,flags=re.S)
    s=re.sub(r"<[^>]+>"," ",s); return collapse(html.unescape(s))
bodies={s:load(f".ufo/waves/round-51/sources/{s}.html") for s in ("S262","S263")}
def probe(q):
    out={}
    for s,b in bodies.items():
        out[s]=dict(raw=q in b, ws=q in collapse(b), tag=q in strip_nospace(b), tagsp=q in strip_space(b))
    return out
def mode(p):
    for s,v in p.items():
        if v["raw"]: return s,"raw"
    for s,v in p.items():
        if v["ws"]: return s,"ws-collapsed"
    for s,v in p.items():
        if v["tag"]: return s,"tag-stripped(correct)"
    for s,v in p.items():
        if v["tagsp"]: return s,"tag-space(misquote)"
    return "-","ABSENT"
quotes=[
("canonical-selection.md",15,"indicating a canonical preference is a hint, not a rule."),
("canonical-selection.md",21,"There are a handful of factors that play a role in canonicalization: whether the page is served over HTTP or HTTPS, redirects, presence of the URL in a sitemap, and rel=\"canonical\" link annotations."),
("canonical-selection.md",27,"Google then chooses the page that, based on the factors (or signals ) the indexing process collected, is objectively the most complete and useful for search users, and marks it as the canonical."),
("canonical-selection.md",32,"You can indicate your preference to Google using these techniques, but Google may choose a different page as canonical than you do, for various reasons."),
("canonical-selection.md",39,"Device variants : for example, a page with both a mobile and a desktop version"),
("canonical-selection.md",40,"Protocol variants : for example, the HTTP and HTTPS versions of a site"),
("canonical-selection.md",41,"Site functions : for example, the results of sorting and filtering functions of a category page"),
("canonical-selection.md",43,"Accidental variants : for example, the demo version of the site is accidentally left accessible to crawlers"),
("canonical-selection.md",49,"the search result will probably point to the mobile page if the user is on a mobile device, even if the desktop page is the canonical"),
("canonical-selection.md",60,"objectively the most complete and useful for search users"),
("crawler-identity.md",10,"Googlebot is the generic name for two types of"),
("crawler-identity.md",15,"Googlebot Smartphone : a mobile crawler that simulates a user on a mobile device"),
("crawler-identity.md",17,"Googlebot Desktop : a desktop crawler that simulates a user on desktop"),
("crawler-identity.md",21,"You can identify the subtype of Googlebot by looking at the HTTP user-agent request header in the request"),
("crawler-identity.md",26,"both crawler types obey the same product token (user agent token) in robots.txt"),
]
rows=[]
for entry,line,q in quotes:
    p=probe(q); src,cls=mode(p)
    rows.append(dict(entry=entry,line=line,src=src,derived=cls,quote=q[:70]))
print(json.dumps(rows,indent=1))
from collections import Counter
print(Counter((r["derived"]) for r in rows))
```

Its observed output ends:

```
Counter({'tag-space(misquote)': 7, 'raw': 3, 'tag-stripped(correct)': 3, 'ws-collapsed': 2})
```

which is the 15/3/2/3/7 split reported in §0-§3. The per-quote JSON lines above that
counter are the same `(entry, line, src, derived)` tuples as the tables in §2 and §3.
