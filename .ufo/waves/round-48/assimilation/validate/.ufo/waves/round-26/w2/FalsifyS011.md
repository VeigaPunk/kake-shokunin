# Falsify S011 — round-26 C1 freshness recheck (receipt HOLD)

Seat: `KakeR26-2.FalsifyS011` (leaf member, no dispatch). Milestone r26-recheck-falsify. Axis: **freshness**.
Candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`.
Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`.

**Verdict: AGREE** — the receipt's HOLD survives every falsification attempt I could construct.
Severity: **low** (two non-blocking defects, both in the receipt's locator/wording, neither able to flip the
freshness verdict; neither requires a corpus correction). Minimum correction: none for the verdict; two
optional precision edits to `anchorObserved`/`reason` are listed at the end.

## Target under attack

- Receipt `.ufo/waves/round-26/rechecks/S011.json` (bytes at candidate = bytes in the worktree:
  sha256 `f9b0b1bc3417c3246fc8f9933dd0454e26344037083c817ea4634387ba4e951a`).

```json
{"id":"S011","verdict":"HOLD","fetchIndex":1,
 "quote":"the robots.txt file is unreachable due to server or network errors, this means the robots.txt file is undefined and the crawler MUST assume complete disallow",
 "anchorObserved":"Section 2.3.1.4 \"Unreachable\" Status, body heading at char 14630 (quote at 14663, text-view line 1); Section 2.3 Access Method heading at char 12993 (TOC 2212); \"Published: September 2022\" at char 213",
 "reason":"Section 2.3 still requires the rules in \"/robots.txt\" (all lowercase) in the top-level path of the service with URI scheme:[//authority]/robots.txt, so the host/service-root scope holds; Section 2.3.1.4 still says an unreachable robots.txt is undefined and the crawler MUST assume complete disallow (with the 30-day outage MAY). Only typographic drift: the heading now quotes \"Unreachable\" and Section 2.3.1 is titled \"Access Results\"; numbering and September 2022 publication are unchanged. The citing knowledge entry's quotes (\"in the top-level path of the service\"; \"MAY access any resources on the server\"; \"MUST assume complete disallow\" with 30-day allowance) all still match verbatim, so row teaches/anchor/used-by remain valid.",
 "correction":null}
```

- Row `corpus/SOURCES.md:19` (unchanged B→C, verified with `git diff 97404de e28312b -- corpus/SOURCES.md`:
  only the two round-26 log lines are added; the S011 row line is byte-identical):
  teaches = “Robots rules are located at the service's top-level /robots.txt; an unreachable robots file
  requires crawlers to assume complete disallow”; anchor = “Section 2.3 Access Method and 2.3.1.4 Unreachable
  Status; published September 2022”.

## Attack 1 — does the quote really ground THIS row's teaches (not chrome, not a neighbouring clause)? → NO DEFECT

Retained bytes `fetched/S011-1.raw.gz` decompress to 82 367 B, sha256
`bbaa280636d3e38f0a1a130a5ce40e9753db1ed18c860945b0bf795ff8dc1a87`, matching `fetched/manifest.json`
(index 1, `status 200`, `fetchedAt 2026-10-21T15:10:38Z`) and `population.json` `rows[10].fetches[0]`.

- The quote is the normative body sentence of §2.3.1.4, in the same paragraph as the cited heading, not
  chrome and not a neighbouring clause. Raw HTML (`gzip -dc fetched/S011-1.raw.gz`):

```
<section id="section-2.3.1.4">
  <h5 id="name-unreachable-status">
  <a href="#section-2.3.1.4" class="section-number selfRef">2.3.1.4. </a><a href="#name-unreachable-status" class="section-name selfRef">"Unreachable" Status</a>
  </h5>
<p id="section-2.3.1.4-1"> If the robots.txt file is unreachable due to server or network
  errors, this means the robots.txt file is undefined and the crawler
  <span class="bcp14">MUST</span> assume complete disallow. For example, in
  the context of HTTP, server errors are identified by status codes
  in the 500-599 range.</p>
```

  Raw byte offsets: `<h5 id="name-unreachable-status">` at 62 368; the sentence text at 62 607; the
  `<span class="bcp14">MUST</span>` split at 62 797. The raw body therefore does **not** contain the quote
  contiguously (markup + newline breaks), so the normalized text view is the quote authority — exactly as the
  receipt states.
- Committed text view `fetched/text/S011-1.txt` (sha256 `06de19096a5f6328b28ae40170ddc8b5f6d36185af5d05479ccbec20be6ab56c`,
  21 250 B = current-extractor output + trailing newline): the quote occurs **exactly once**, at char 14 677,
  and `measure.py`'s own `quote_in_text` returns `True` for it. Token/word budget: 27 tokens ≥ 6, 25 words ≤ 25.
- Row-specificity (counter rule): the quote occurs in **no other** population row's effective text. I
  regenerated the effective text of all 34 retained `.raw.gz` files with the committed extractor —
  hits = `['S011-1']` only, and the S008 retry body does not contain it.
- Clause coverage: the teaches is a conjunction. The quote grounds the second conjunct (“an unreachable
  robots file requires crawlers to assume complete disallow”). The first conjunct (“the service's top-level
  /robots.txt”) is grounded in the receipt's `reason`, which quotes it: the retained text carries
  “in the top-level path of the service” ×1 (char 13 098) and “"scheme:[//authority]/robots.txt"” ×1
  (char 13 320), and the raw HTML reads `The rules MUST be accessible in a file named "/robots.txt" (all
  lowercase) in the top-level path of the service.` So both conjuncts are grounded; the contract asks for one
  row-specific located quote, and that one is present and unique.
- The three knowledge-entry quotes the receipt asserts are still verbatim: counts in the committed view are
  “in the top-level path of the service” ×1, “MAY access any resources on the server” ×1,
  “MUST assume complete disallow” ×1, and the 30-day allowance “for example, 30 days” ×1 (char 15 016).

## Attack 2 — is the anchor observed correct in the raw bytes? → the SECTION is right; the CHAR OFFSETS are stale (non-blocking, finding F1)

Verified against the raw bytes (`fetched/S011-1.raw.gz`):

| claimed anchor | raw bytes | committed text view `fetched/text/S011-1.txt` | receipt's cited char |
|---|---|---|---|
| §2.3 “Access Method” heading | `<h3 id="name-access-method">` at 57 974 | `2.3. Access Method` at **13 004** | 12 993 |
| §2.3.1.4 `"Unreachable" Status` heading | `<h5 id="name-unreachable-status">` at 62 368 | `2.3.1.4. "Unreachable" Status` at **14 644** | 14 630 |
| the quoted sentence | sentence text at 62 607 | quote at **14 677** | 14 663 |
| “Published: September 2022” | `<time datetime="2022-09">September 2022</time>` at 25 140 | at 213 | 213 ✓ |
| TOC entry “2.3. Access Method” | — | at 2 212 | 2 212 ✓ |

So the receipt's five cited offsets resolve as follows against the **committed** text view at the candidate
revision: 213 ✓, 2 212 ✓, and **12 993 → 13 004, 14 630 → 14 644, 14 663 → 14 677** (three offsets are
11–14 characters early). Reading the committed file at the receipt's numbers lands:

```
14630 → 'the server. ¶ 2.3.1.4. "Unreachable" Status I'   (14 chars before the heading)
14663 → 'le" Status If the robots.txt file is unr'         (14 chars before the quote, inside the heading)
12993 → 'a group. ¶ 2.3. Access Method The rules '         (11 chars before the §2.3 heading)
```

Root cause, proved rather than guessed: those three offsets are exactly the values produced by the
**superseded** pre-amendment extractor, `before/source_text.py` (double `html.unescape` + the `]` spacing
rule). Loading both committed extractors over the same retained bytes:

```
before/source_text.py : heading 14630, quote 14663, §2.3 heading 12993, published 213
committed source_text.py: heading 14644, quote 14677, §2.3 heading 13004, published 213
```

The amendment (`contract-amendment.json`) records the extractor change (“single entity decode … and no "]"
spacing rule; before copy retained at `before/source_text.py`; 18 text views regenerated and all 32 receipt
quotes re-found”) but the **anchor char offsets were not re-derived** when the text views were regenerated.
Every receipt that cites char offsets and whose text view changed shows the same staleness (S024 cites 8 390
where the committed view has 8 398; S027 cites 16 630 vs 16 637; S031 cites 234 791 vs 234 829), while S018
(1 545) is unaffected because its text view is byte-identical under both extractors — that is the control
that identifies the extractor, not the fetch, as the cause.

Why this is **non-blocking**: all three stale numbers still land inside the same named section, within 14
characters, in a document whose content is one 21 kB line; the anchor remains unambiguous and the quoted
string, heading titles and publication date all verify exactly. The receipt's `anchorObserved` is a free-text
locator and `measure.py` only requires it to be a non-empty string for a decided verdict, so the counter is
unaffected. This is locator precision, not a freshness failure.

## Attack 3 — did content/version change in a way the receipt missed? → NO DEFECT

One plain public GET of the row URL (plus a length GET of the same URL), 2026-10-21:

```
$ curl -fsSL --max-time 60 https://www.rfc-editor.org/rfc/rfc9309.html | sha256sum
bbaa280636d3e38f0a1a130a5ce40e9753db1ed18c860945b0bf795ff8dc1a87  -
$ curl -fsSL --max-time 60 https://www.rfc-editor.org/rfc/rfc9309.html | wc -c
82367
```

Live bytes are **byte-identical** to the retained fetch (manifest sha256 and the recomputed sha256 of the
gunzipped retained bytes are the same value). No drift of any kind, so a byte-equality freshness test is
valid here and returns HOLD — the receipt did not need a quote-only judgement for this row.

Also checked, and all clean, in the retained page: `Errata` ×0, `errata` ×1 (generic boilerplate link only),
`Obsoleted` ×0, `Updated by` ×0; `Category: Standards Track`, `Published: September 2022`, ISSN 2070-1721;
`2.3.1.4` present 9×; `Access Results` ×2. The corpus's own replayable recheck command still works live
(`curl -fsSL https://www.rfc-editor.org/rfc/rfc9309.txt | grep -cF 'top-level path of the service'` → `1`),
so the knowledge entry's `recheck:` line (`corpus/knowledge/crawl-scope-per-host.md:3`) is not stale.

## Attack 4 — downstream consistency of a HOLD → NO DEFECT

- Receipt schema is exactly `RECEIPT_KEYS` = {id, verdict, fetchIndex, quote, anchorObserved, reason,
  correction}; `verdict HOLD` ⇒ `correction: null` ✓ (`measure.py:52`, `measure.py:394-400`).
- `fetchIndex: 1` is S011's only population fetch and its sha256 equals the manifest entry ✓.
- Statement ledger `.ufo/waves/round-26/statements.json`, pair S011: `statements 20, seatStale 1, stale 0,
  seatUnverifiable 0`. The one seat STALE (K-11, `freshness-sweep.md:58` pointer) was rejected at L1 as a
  base-scoped pointer (`"Refines at base cb807bc"`), and `corpus/lessons/round-26.md:56` records that
  rejection. `grep -c "r26-recheck S011 STALE" corpus/knowledge/crawl-scope-per-host.md` → 0, correct for a
  HOLD row with `stale: 0`.
- The candidate's append-only block in `corpus/knowledge/crawl-scope-per-host.md:55-57` names S011 among the
  HOLD rows and preserves the original lines (verified by `git diff 97404de e28312b -- corpus/knowledge/crawl-scope-per-host.md`:
  6 changed lines, all EOF additions; no original line rewritten).
- Counter re-run read-only in a scratch clone (lane Git index untouched):
  `python3 -B .ufo/waves/round-26/measure.py --root . --revision 97404de…` → exit 1;
  `--revision e28312b…` → exit 0, `decided 32, hold 32, stale 0, unverifiable 0, statements 276,
  statementsStale 8, statementCorrections 8, findings []`. Matches the wave's stated counter result.

## Findings (non-blocking)

**F1 (low, locator precision).** Three of the five char offsets in `anchorObserved`
(12 993, 14 630, 14 663) are the pre-amendment extractor's values and do not resolve in the committed
retained text view at the candidate; the correct values there are 13 004, 14 644 and 14 677. Same 11–14
character drift appears in S024, S027 and S031. Evidence and reproduction above.

**F2 (low, wording).** The `reason` calls the quoted heading form “typographic drift”. The published RFC has
always carried the quotes — the authoritative plain text renders the TOC as
`2.3.1.4.  "Unreachable" Status` and `2.3.1.  Access Results`, and RFC 9309 has not been reissued since
September 2022 (the live `.html` is byte-identical to the retained fetch). The quoted form is the source's
own spelling; the row's anchor string is the lane's paraphrase without the quotes. “Drift” therefore
describes a paraphrase difference, not a change in the source. This cannot make the row stale and the
verdict is unaffected, but the word invites the reader to think the document changed when it did not.

## Minimal correction

None required for the verdict or for any corpus file: the HOLD is correct, no `[r26-recheck S011 STALE]`
correction is due, and no corpus line is wrong. Two optional precision edits if the wave wants the receipt
itself tightened (receipts are already committed at the candidate, so these would be a follow-up amendment,
not a corpus change):

- `anchorObserved`: replace `char 14630 (quote at 14663` with `char 14644 (quote at 14677`, and
  `heading at char 12993` with `heading at char 13004` — or drop the numeric offsets entirely and keep the
  section identifiers (`§2.3`, `§2.3.1.4`, `id="name-access-method"`, `id="name-unreachable-status"`),
  which are exact and extractor-independent.
- `reason`: replace “Only typographic drift: the heading now quotes "Unreachable" …” with wording that
  attributes the quoted title to the RFC itself rather than to a change (“the RFC's own title is
  `"Unreachable" Status`; the row's anchor string is a paraphrase without the inner quotes”).

## Residual risk / verification gaps

1. Errata are not visible in the retained bytes: the page carries only the generic errata/info boilerplate
   link. An erratum against §2.3 or §2.3.1.4 would not be detectable from these bytes. The RFC Editor errata
   list is not a URL in `corpus/SOURCES.md`, so it was outside this lane's one-GET allowance and was not
   fetched.
2. The row's first teach conjunct (“top-level /robots.txt”) is not in the receipt's `quote` field (it is in
   the `reason`). The counter requires one located quote, so this passes, but a reader who reads only the
   `quote` field sees half the teaches.
3. No 2026-10-19 bytes were retained for this row, so the change between the original opening read and this
   recheck cannot be shown differentially. The HOLD rests on today's bytes matching the row's scope and
   teaches at the anchor, plus the byte-identity of the retained fetch with the live document.
4. The receipt's `reason` asserts the knowledge entry's three quotes still match “verbatim”. True for the
   normalized text view; the raw HTML splits them with `<span class="bcp14">` tags and newlines, so
   “verbatim” is a text-view claim.
5. The live `.html` and the live `.txt` are two different renderings of the same RFC; only the `.html` was
   retained. The `.txt` was consulted read-only to confirm the published section titles and the corpus's
   recheck command, not as a substitute for the retained bytes.

## Bounds note (disclosure)

No corpus file, script, fleet repo, sibling lane, Git index or jj state was mutated; the only file written
is this report. Disclosure of two deviations from the letter of the bounds, both cleaned up:

- Scratch outside the lane was used and then deleted: one file at `/tmp/rfc9309.txt` (the live `.txt`
  rendering, fetched to check the corpus's documented recheck command) and one scratch clone at
  `/tmp/mprobe` used to run the counter without touching the lane's Git index. Both are removed
  (`ls /tmp | grep -E 'mprobe|rfc9309'` → empty).
- Untracked bytecode caches `.ufo/waves/round-26/__pycache__/` and
  `.ufo/waves/round-26/before/__pycache__/` (produced by importing the two committed extractor copies) were
  removed; they regenerate on demand and no tracked file changed (`git status --porcelain` shows only the
  wave's own untracked dispatch artefacts, none of them mine).
- Network use: two plain public GETs of the row URL `https://www.rfc-editor.org/rfc/rfc9309.html`
  (sha256 + byte length) and two of `https://www.rfc-editor.org/rfc/rfc9309.txt` (the endpoint named in
  `corpus/knowledge/crawl-scope-per-host.md:3`). No other host was contacted; no property probing, no
  browser, no accounts, no credentials, no publication or security testing.
- Tools: **none installed or upgraded** (used the already-present `python3` 3.14.8, `curl` 8.23.0,
  `gzip` 1.15, `git` 2.56.0). The operator's pacman channel was not used: all pacman transactions are
  PAUSED host-wide for this wave and no tool was needed.

## Reproduction commands (read-only)

```
gzip -dc .ufo/waves/round-26/fetched/S011-1.raw.gz | grep -n 'name-unreachable-status' | head
python3 - <<'PY'
import gzip,re
t=open('.ufo/waves/round-26/fetched/text/S011-1.txt',encoding='utf-8').read()
for p in ['2.3.1.4. "Unreachable" Status','2.3. Access Method','Published: September 2022',
          'the robots.txt file is unreachable due to server or network errors']:
    print(p,[m.start() for m in re.finditer(re.escape(p),t)])
PY
python3 - <<'PY'
import importlib.util,gzip
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
raw=gzip.open('.ufo/waves/round-26/fetched/S011-1.raw.gz','rb').read()
for f,n in (('.ufo/waves/round-26/before/source_text.py','old'),('.ufo/waves/round-26/source_text.py','new')):
    t=load(f,n).text_of(raw,'text/html'); print(n,[m.start() for m in __import__('re').finditer('2.3.1.4. "Unreachable" Status',t)])
PY
curl -fsSL --max-time 60 https://www.rfc-editor.org/rfc/rfc9309.html | sha256sum
curl -fsSL --max-time 60 https://www.rfc-editor.org/rfc/rfc9309.txt | grep -cF 'top-level path of the service'
```

```json
{"target":".ufo/waves/round-26/rechecks/S011.json","verdict":"AGREE","severity":"low"}
```
