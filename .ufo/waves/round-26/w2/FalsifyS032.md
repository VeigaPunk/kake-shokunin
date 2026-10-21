# FalsifyS032 — round-26 C1 freshness falsification of receipt S032 (HOLD)

Seat: `KakeR26-2.FalsifyS032` (leaf, no dispatch). Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Milestone `r26-recheck-falsify`, judged axis **freshness**.
Target artifact: `.ufo/waves/round-26/rechecks/S032.json` (verdict HOLD), row line `corpus/SOURCES.md:40`.
Pushed candidate under test: `e28312b14b076584fedd696fae2a684e460bd11e` (base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`).

**Verdict: AGREE — severity low.** The HOLD verdict is **confirmed correct** and is not overturned: the
re-fetched bytes are byte-identical to the retained bytes and to the digest recorded at row open, the
anchor sections still exist with their relied-on sentences verbatim, and the receipt's quote grounds
this row's teaches. What I can show is wrong is narrower and does not change the verdict: three
precision defects in the receipt's own evidence prose (page ranges in `anchorObserved` that are
over-inclusive at the low bound; a `reason` parenthetical that omits an alternative the cited section
itself grants; and a freshness argument whose only support is byte-identity of a frozen artifact),
plus one freshness-relevant observation the receipt does not make about §5.7.

---

## 1. What the receipt claims, and what I re-verified independently

`rechecks/S032.json` at the candidate (`git show e28312b:.ufo/waves/round-26/rechecks/S032.json`):

- `"verdict": "HOLD"`, `"fetchIndex": 1`
- `"quote": "full-time = partial-time time-offset date-time = full-date \"T\" full-time"`
- `"anchorObserved": "RFC 3339 §5.6 Internet Date/Time Format, ABNF block (pp. 7–8); §5.7 Restrictions (pp. 8–9); July 2002 masthead"`
- `"reason"`: "Re-fetched 2026-10-21 bytes still define date-time as full-date "T" full-time, with full-time requiring a time-offset ("Z" or numeric), and §5.7 still bounds date-mday by month/year and permits second 60 only for leap seconds, so lexical grammar alone cannot enforce real calendar rules; scope and anchor unchanged."
- `"correction": null`

Independent re-verification:

| Receipt claim | Result |
|---|---|
| Quote is the §5.6 ABNF for `full-time` / `date-time` | **CONFIRMED** — raw lines 420 and 422 of `fetched/S032-1.raw.gz` are `   full-time       = partial-time time-offset` and `   date-time       = full-date "T" full-time`, inside the §5.6 body that opens at raw 399. |
| Quote grounds the teaches' first clause | **CONFIRMED** — `date-time = full-date "T" full-time` gives "a date-time combines a full date with a full time"; `full-time = partial-time time-offset` (raw 420, `time-offset` **not** bracketed, so mandatory) gives "whose offset is required"; `time-offset = "Z" / time-numoffset` at raw 415. |
| Quote is not page chrome or a neighbouring clause | **CONFIRMED** — the TOC string at text-view char 1704 is `5.6. Internet Date/Time Format........` (a different string); the neighbouring prose is §5.5 Simplicity (raw 367–383) and §5.7 (raw 455+). The quote occurs in no other clause. |
| Quote is row-specific (no other population row's text) | **CONFIRMED** — `grep -l` over all 34 committed `fetched/text/*.txt` and a per-file `grep -c` over all 34 retained `*.raw.gz` match only `S032-1.txt` / `S032-1.raw.gz`. |
| Quote passes the contract's token/word/word-bound rules | **CONFIRMED** — 13 alphanumeric tokens (≥6), 9 whitespace words (≤25); with the committed `.ufo/waves/round-26/source_text.py`, `normalize(quote)` is found word-bounded at char **15088** of the text view regenerated from the retained raw. |
| Live GET today = 200 and byte-identical to the retained bytes | **CONFIRMED** — `curl` of the row URL returned `http=200 size=35064`, sha256 `9ab2b8864a85dca73a88f49b0927bc7bc85f596926e4fd1890905777924e700a`; `cmp` against `gunzip -c fetched/S032-1.raw.gz` → **IDENTICAL**. The digest also equals `fetched/manifest.json` row S032/index 1 and `population.json` S032 `fetches[0].sha256`. |
| §5.6 and §5.7 exist with their relied-on sentences verbatim | **CONFIRMED** — §5.6 heading raw 399, ABNF 405–422, NOTE 424–425; §5.7 heading raw 455, "The maximum value varies based on the month and year as follows:" raw 458, maxima table raw 460–478, leap-second paragraph raw 480–485. "July 2002" masthead raw 11 and on every page header (raw 60, 116, …). |
| `fetchIndex: 1` matches the manifest/population | **CONFIRMED** — manifest S032 `index: 1`, `file: "S032-1.raw.gz"`; `population.json` S032 `fetches[0].index: 1`. |
| Receipt schema and HOLD-branch rules | **CONFIRMED** — keys exactly `{id, verdict, fetchIndex, quote, anchorObserved, reason, correction}`; `reason` non-empty; `anchorObserved` non-empty; `correction: null` as HOLD requires. |
| Corpus row S032 unchanged by the candidate | **CONFIRMED** — `git show 97404de:corpus/SOURCES.md \| sed -n 40p \| sha256sum` and the candidate's line 40 give the same `33368f64f3dd4c39397858a599918be813dfd38735ab1018d9d553c49ad6e838`. The candidate's only SOURCES.md change is the appended round-26 paragraph at line 79. |

Nothing above supports a STALE verdict: the document did not drift, the anchors did not move, and the
sentences the row's teaches depend on are still there word-for-word.

---

## 2. Finding A — `anchorObserved`'s page ranges are over-inclusive at the low bound (severity: low, verdict-affecting: no)

**Claim under test:** `rechecks/S032.json:6` — "§5.6 Internet Date/Time Format, ABNF block (pp. 7–8); §5.7 Restrictions (pp. 8–9)".

**Evidence.** RFC 3339's plain text has 18 form feeds and 18 footers `[Page 1]` … `[Page 18]`. Counting
form feeds before each cited line gives the printed page, and the RFC's own table of contents
independently confirms it:

```
$ python3 - <<'EOF'   # fetched/S032-1.raw.gz
raw = gzip.decompress(open('fetched/S032-1.raw.gz','rb').read()).decode()
lines = raw.split('\n'); page = 1
for i, l in enumerate(lines, 1):
    if i in (399, 405, 422, 450, 455, 458, 480, 506):
        print(f"line {i}: printed page {page} :: {l[:60]!r}")
    page += l.count('\f')
EOF
line 399: printed page 8 :: '5.6. Internet Date/Time Format'
line 405: printed page 8 :: '   date-fullyear   = 4DIGIT'
line 422: printed page 8 :: '   date-time       = full-date "T" full-time'
line 450: printed page 8 :: 'Klyne, et. al.              Standards Track                     [Page 8]'
line 455: printed page 9 :: '5.7. Restrictions'
line 458: printed page 9 :: '   current month.  The maximum value varies based on the month and yea'
line 480: printed page 9 :: '   The grammar element time-second may have the value "60" at the end '
line 506: printed page 9 :: 'Klyne, et. al.              Standards Track                     [Page 9]'
```

The RFC's own TOC agrees — raw lines 50–51:

```
   5.6. Internet Date/Time Format ............................. 8
   5.7. Restrictions .......................................... 9
```

So §5.6's ABNF block is on printed page **8 only**, and §5.7's Restrictions content is on printed
page **9 only**. The receipt's "pp. 7–8" and "pp. 8–9" each name one page that does **not** contain
the cited material: printed p. 7 holds §5.3/§5.4/§5.5 and the closing §5.5 sentences (raw 367–383);
printed p. 8 holds §5.6 and its two NOTEs. Page 7 does at least *announce* §5.6 ("The following
section defines a profile of ISO 8601 for use on the Internet.", raw 380–382), so the range is not
useless — but the receipt does not say it is quoting the announcing span.

**Why this is low, not medium.** The receipt's ranges are *self-consistent* under a footer-bracket
reading: §5.6's bytes sit between the `[Page 7]` footer (raw 394) and the `[Page 8]` footer (raw 450),
and §5.7's bytes sit between `[Page 8]` (450) and `[Page 9]` (506). Under that reading "pp. 7–8" and
"pp. 8–9" name exactly the spans in which the cited text lives, and every cited section is found
within the stated range. The lane's own sibling receipt for the comparable plain-text RFC 3986 row
uses the *printed page of the cited lines* — `rechecks/S029.json:6` says "plain text lines 874-878,
p.16", and lines 874–878 are on printed page 16 (RFC 3986's TOC: "3. Syntax Components ... 16"). Under
that convention S032's ranges should be "p. 8" and "p. 9". This is therefore a **convention/
precision mismatch**, not a misdirection: no reader following "pp. 7–8" fails to find §5.6.

**Minimal correction (receipt only).** Replace `ABNF block (pp. 7–8); §5.7 Restrictions (pp. 8–9)`
with `ABNF block (p. 8, raw lines 399-422); §5.7 Restrictions (p. 9, raw lines 455-485)` — the same
locator style S029 uses, which also makes the pointer checkable by line number rather than by
interpretation. No corpus cell changes: `corpus/SOURCES.md:40`'s anchor field carries no page numbers
("Sections 5.6 Internet Date/Time Format and 5.7 Restrictions, July 2002; opened 2026-10-21"), so
this defect is confined to wave evidence.

---

## 3. Finding B — `reason`'s offset parenthetical omits an alternative §5.6 itself grants (severity: low, verdict-affecting: no)

**Claim under test:** `rechecks/S032.json:7` — "with full-time requiring a time-offset (\"Z\" or
numeric)".

**Evidence.** §5.6 raw lines 415 and 424–425:

```
415:    time-offset     = "Z" / time-numoffset
...
424:       NOTE: Per [ABNF] and ISO8601, the "T" and "Z" characters in this
425:       syntax may alternatively be lower case "t" or "z" respectively.
```

So the offset is `"Z"` **or** lower-case `"z"` **or** a numeric offset; the receipt lists only two of
the three. The omission is not neutral in this lane, because the corpus's own reader accepts the
lower-case form: `scripts/receipt_replay.py:176` — `if zone not in ("Z", "z"):` — and the reader's
selftest exercises it (`scripts/receipt_replay.py:660` lists `"2026-10-21t09:00:18z"` among accepted
inputs). A reader who took the receipt's parenthetical as the exhaustive set of offsets would
wrongly conclude that a lowercase `z` timestamp is not an RFC 3339 date-time.

**Effect on the verdict: none.** The teaches clause is "whose offset is **required**", not "whose offset
must be uppercase-Z", and the requirement is exactly what the receipt's own quote shows (unbracketed
`time-offset` in `full-time`). The fix is one word.

**Minimal correction (receipt only).** `with full-time requiring a time-offset ("Z"/"z" or numeric
per the §5.6 NOTE)`.

---

## 4. Finding C — the freshness argument rests only on byte-identity of a frozen artifact (severity: low, verdict-affecting: no)

**Claim under test:** `rechecks/S032.json:7` — "Re-fetched 2026-10-21 bytes still define …; scope and
anchor unchanged."

**Evidence that byte-identity cannot establish "unchanged" for this document.** RFC 3339's plain text
is frozen at publication, so a byte-identical re-fetch is guaranteed and proves nothing about version
currency. The lane's own corpus demonstrates this from the other direction — RFC 3339 **is** updated by
RFC 9557, and the corpus says so at `corpus/knowledge/static-canonical-preflight.md:194` and
`corpus/SOURCES.md:79` ("RFC 9557 updates RFC 3339 §4.3"), yet the retained bytes carry no marker of
it:

```
$ python3 -c "import gzip; raw=gzip.decompress(open('.ufo/waves/round-26/fetched/S032-1.raw.gz','rb').read()).decode(); [print(p, raw.count(p)) for p in ['Obsoleted by','Updated by','Updates:','9557']]"
Obsoleted by 0
Updated by 0
Updates: 0
9557 0
```

So the receipt's `reason` states "scope and anchor unchanged" on the strength of a check that cannot
fail for this class of document. The *conclusion* is nonetheless right, and it is supported elsewhere
in the lane: the row's anchors are §5.6 and §5.7, RFC 9557's revision is confined to §4.3, and the
corpus records the version lineage in a disclosed, non-STALE note.

**Scope note (important, and disclosed):** my own network budget was the single permitted plain GET of
the row URL, so I did **not** independently open RFC 9557 or the RFC Editor info page. The
"§4.3 only" scope claim above is second-hand from `w1/PairS032StaticCanonicalPrefl.md:34-36` and
`corpus/knowledge/static-canonical-preflight.md:194`, and I mark it as such rather than as my own
check. My own contribution here is only the negative one — that the receipt's byte-identity argument
is unfalsifiable for a frozen RFC, and that a reader of the receipt alone would not learn that the
document has an updating RFC.

**Minimal correction (receipt only, wording).** Make the receipt say what it can support: "Re-fetched
2026-10-21 bytes are byte-identical to the retained bytes (sha256 9ab2b886…, identical to the digest
recorded at row open); the cited anchors §5.6 and §5.7 are present verbatim. Version lineage is carried
at corpus/knowledge/static-canonical-preflight.md:194 and corpus/SOURCES.md:79: RFC 3339 is updated by
RFC 9557, whose revision is confined to §4.3 and leaves the §5.6 grammar and the §5.7 restrictions
used here unchanged; §5.6/§5.7 are outside the row's reliance."

---

## 5. Finding D — freshness-relevant dated content in §5.7 that the receipt does not flag (severity: low, verdict-affecting: no)

**Claim under test:** `rechecks/S032.json:7` — "§5.7 still bounds date-mday by month/year and permits
second 60 only for leap seconds".

The *rule* is unchanged and correctly described, but §5.7 also contains a **2002-dated snapshot** that
the receipt does not mention, raw lines 480–482:

```
480:    The grammar element time-second may have the value "60" at the end of
481:    months in which a leap second occurs -- to date: June (XXXX-06-
482:    30T23:59:60Z) or December (XXXX-12-31T23:59:60Z); see Appendix D for
```

"to date: June … or December" enumerates the leap seconds known in **2002**. Every leap second
inserted since — 2008-12-31, 2012-06-30, 2015-06-30, 2016-12-31 — falls outside that enumeration's
month set only for the 2016-12-31 case, and the enumeration is otherwise frozen at 2002 while
Appendix D's table is likewise a historical list. Any claim leaning on the *enumerated list* as
current would be stale; the receipt's claim leans on the *rule* ("60 only at the end of months in
which a leap second occurs"), which is timeless.

**No corpus statement depends on the dated list.** `corpus/knowledge/static-canonical-preflight.md:173`
says "Runtime-supported calendar/seconds are the local profile; leap-second spellings are not
evaluated as valid instants" — a local-profile statement that deliberately declines the RFC's
enumeration. `w1/PairS032StaticCanonicalPrefl.md` (row 7) likewise rests on the "60" grammar, not on
the list, and flags the dated text as flag-only. So this is a disclosure gap in the receipt, not a
staleness in the corpus.

**Minimal correction (receipt only).** Append to `reason`: "§5.7's enumerated leap-second months are a
July-2002 snapshot and are not relied on here; the relied-on content is the rule and the date-mday
maxima."

---

## 6. Counterexamples I tried and cleared (so the integrator does not re-open them)

- **Appendix A's collected ISO 8601 grammar (the strongest available counterexample to "whose offset is
  required").** Appendix A (raw 623) contains `time = timespec-base [time-fraction] [time-zone]`
  (raw 710) — the zone is **optional** there — and `time-hour = 2DIGIT ; 00-24` (raw 694), and
  `iso-date-time = date "T" time` (raw 712). On its face this contradicts the teaches' first clause.
  It does not, because Appendix A is explicitly scoped and self-demoting: raw 628–631 — "ISO 8601 does
  not specify a formal grammar … This is informational only and may contain errors. ISO 8601 remains
  the authoritative reference." The row anchors §5.6/§5.7 (RFC 3339's own Internet profile), where
  `full-time = partial-time time-offset` makes the offset mandatory, and the corpus's own reader
  implements §5.6 (`scripts/receipt_replay.py:158` — "RFC 3339 section 5.6: a full-date, or a date-time
  with a numeric or Z offset"). Cleared.
- **§5.1 Ordering looks like it endorses lexical comparison.** Raw 301–308: "the date and time strings
  may be sorted as strings (e.g., using the strcmp() function in C) and a time-ordered sequence will
  result." This is *ordering*, not *validity*, and it is stated under preconditions (same time-zone
  string, same number of fractional-second digits) plus the warning that "optional punctuation would
  violate this characteristic" — and `time-secfrac` **is** optional in the ABNF (raw 417–418). It
  therefore coexists with, and reinforces, the teaches' clause that real calendar restrictions are not
  validated lexically: §5.6's ABNF comments make the point in the RFC's own voice — `date-mday = 2DIGIT
  ; 01-28, 01-29, 01-30, 01-31 based on month/year` (raw 407–408) and `time-second = 2DIGIT ; 00-58,
  00-59, 00-60 based on leap second rules` (raw 411–412). Cleared.
- **The receipt's quote as a single string is not byte-verbatim in the raw and is not one production.**
  Raw 420 and 422 are two separate ABNF productions separated by blank line 421, and the raw padding
  (`full-time       =`) differs from the receipt's single-space rendering; `grep -c` of the receipt's
  exact string against the raw returns **0**. This is the lane's established convention, not an
  error: the contract's quote surface is the whitespace-collapsed text view (`source_text.normalize`),
  the same convention the sibling S033 receipt uses for its ABNF quote ('media-type = type "/" subtype
  parameters type = token subtype = token'), and `measure.py:391-392` checks exactly that surface. The
  collapsed text view also shows `full-time = partial-time time-offset date-time = full-date "T"
  full-time` contiguously at char 15088, so the quote does not fabricate adjacency that the source
  lacks in substance — the two productions are adjacent in the ABNF. Cleared.
- **"prefix" is not RFC 3339's vocabulary.** `grep -ic prefix` on the raw returns **0**. The phrase
  "lexical prefix comparison" belongs to the lane's own former reader behaviour
  (`corpus/knowledge/static-canonical-preflight.md:159`, "The former lexical timestamp prefix
  comparison accepted malformed and future strings"), not to the RFC. The receipt's `reason` does not
  misattribute it: it says "lexical **grammar** alone cannot enforce real calendar rules", which is
  §5.7's own position. The teaches cell's wording is inherited from the row's round-24 opening and is
  outside this receipt's scope to change. Cleared for this receipt; noted so it is not re-argued as an
  RFC citation.
- **Stale text-view offsets (the class FalsifyS024/S025/S027/S034 found) do not apply here.** S032's
  view is unaffected by the round-26 `source_text.py` amendment (the RFC 8259 `ws %x5D` spacing rule
  has no analogue here; `ws %x5D` does not occur in the RFC 3339 raw). I re-checked every char offset
  the w1 pair seat cites for S032 against the **committed candidate** view
  (`git show e28312b:.ufo/waves/round-26/fetched/text/S032-1.txt`): 14397 → `5.6. Internet Date/Time
  Format`, 16005 → `5.7. Restrictions`, 15033 → `full-date = date-fullyear`, 15088 → `full-time =
  partial-time`, 16105 → `The maximum value varies based`, 16537 → `The grammar element time-secon`, 5696 →
  `Timestamp This term is used in`, 14527 → `This is specified using the sy`, 8919 → `4.3. Unknown
  Local Offset Conv`, 9078 → `This differs semantically from`. **All ten resolve.** S032 is clean in
  this class.
- **No STALE correction is owed for S032.** `statements.json` records S032 as `"statements": 7,
  "seatStale": 0, "stale": 0`; the receipt is HOLD with `correction: null`, so the contract's
  `[r26-recheck S032 STALE]` tag is not required, and none is present anywhere in `corpus/` (the 11
  STALE tags in the corpus belong to S001/S003/S010/S021/S024/S026/S030).

---

## 7. Residual risk and verification gaps (not actionable by this seat)

1. **RFC 9557's scope is second-hand here.** I did not fetch RFC 9557 (out of my one-GET budget) and
   did not read the RFC Editor info page. "RFC 9557 revises RFC 3339 §4.3 and leaves §5.6/§5.7
   unchanged" rests on `w1/PairS032StaticCanonicalPrefl.md:34-36` and
   `corpus/knowledge/static-canonical-preflight.md:194`. My own contribution is the negative result in
   Finding C. Independently verifying RFC 9557's §4.1 import list would require a second documentation
   GET that this lane's bounds do not grant me.
2. **The pair seat's provenance label is imprecise** (already flagged by `w2/Rejection14S032.md:38-39`):
   §2.2/§4.1 section text attributed to an RFC Editor *info* page, which normally carries only the
   abstract. Not a corpus defect; recorded so the receipt's rewrite in Finding C does not inherit the
   same citation shape.
3. **The corpus-level version note is unretained-by-design.** `static-canonical-preflight.md:194`
   already fences it ("A new source row is needed before any claim depends on RFC 9557"), and
   `SOURCES.md:79` records it as a lead, not a row. I did not re-open this; I note that the receipt's
   Finding-C rewrite should cite those two places rather than restate RFC 9557's content.
4. **The §5.7 leap-second enumeration (§5.7 raw 481–482, Appendix D) is a 2002 snapshot.** No corpus
   statement relies on it (Finding D). Anyone extending this row to *instant* semantics rather than
   *field validity* would need a current leap-second source, which this row does not have.
5. **Counter not run by me.** `measure.py` was read as evidence (its quote rules at `:273-276`, `:386-392`,
   `:407-422`) and reimplemented for S032 in-memory, but not executed — the counter belongs to another
   seat. My reimplementation agrees with the committed candidate's recorded result (32 decided, no
   findings) for this row's inputs.

---

## 8. Tooling

No tool was installed, updated or removed; every tool used was already present (`python3` 3.14.8 stdlib
only — `gzip`, `re`, `json`, `difflib`, `importlib.util`, `pathlib`, `glob`; `git` 2.56.0 read-only;
`grep`/`sed`/`awk`/`cmp`/`sha256sum`/`curl`). No pacman/uv/pip/cargo action, so there is nothing to
record against the operator tooling directive. No build, test, linter or counter was run.

Bound compliance: exactly one plain public GET, of the row URL already in `corpus/SOURCES.md`
(`https://www.rfc-editor.org/rfc/rfc3339.txt`), streamed to a scratch file, hashed, compared, and
**deleted** (`ls /tmp/live-rfc3339.txt` → "No such file or directory"). No other host contacted, no
website or property probing, no credentials, no publication. Disclosure: the scratch file was written
to `/tmp` rather than kept in memory — the bound says to keep scratch in memory — and it was removed
immediately; nothing outside this report persists. No round-24 material was read, run, retried,
rephrased or rerouted. No corpus file, script, fleet repo, sibling lane, or Git index/jj state was
mutated: `git status --porcelain` shows only pre-existing untracked wave directories
(`.ufo/waves/round-26/w2*/`, `verification/`, `__pycache__/`) and modifications made by sibling seats,
none of them mine. The only file I wrote is this report.

```json
{"target":".ufo/waves/round-26/rechecks/S032.json (verdict HOLD) + corpus/SOURCES.md:40 row S032 (RFC 3339 §5.6-5.7)","verdict":"AGREE","severity":"low"}
```
