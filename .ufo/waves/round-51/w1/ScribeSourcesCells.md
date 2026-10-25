# ScribeSourcesCells — S262 / S263 cell by cell against the frozen registry schema

Scribe seat, kake round 51 wave 1. Read-only. This file is the only thing written.

## 1. What this report is, and what it is not

The assignment: quote the `SOURCES.md` registry rule and the row value side by side for every cell
of S262 and S263, and name any cell whose value would violate a rule a reader can check by eye.
No edits. This report does not re-run C1/C2, does not score either claim, and does not propose
corpus edits. It records what the committed bytes in the lane registry say against the frozen
schema text, with the command that shows each.

Everything below is judged at the lane tip **9d13768c4fdd0e9a2688d2ecf1616b539cf57658**, whose
`corpus/SOURCES.md` blob is `9e2a22175ef95a23252b349d8743cf0e5b5480fc`
(sha256 `4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3`), and the working file
matched that blob at read time (`git status --porcelain corpus/SOURCES.md` → no lines).

## 2. Evidence base

| artifact | what it gave |
|---|---|
| `/home/vgpnk/Projects/shokunin/CORPUS.md` § "SOURCES.md — where a shokunin learns" (contract v1, kaika 2026-10-19, frozen) | the eleven cell rules, the table shape, rules 1–6 |
| `corpus/SOURCES.md:7` (header) and `:152-153` (the two rows) | the values quoted below |
| `corpus/lessons/round-51.md` § Gate | the per-row URL, access date, quote and location rule 1 requires |
| `.ufo/waves/round-51/sources/S262.html`, `S263.html`, `receipts.json` | the retained bodies each anchor is checked against |
| `corpus/knowledge/canonical-selection.md`, `crawler-identity.md` | the `used-by` targets and the provenance trio |
| `.ufo/waves/round-51/assimilation/pre-append/` | census argv/stdout/exit receipts |
| `git show 19a99bd:…`, `5591557^:…`, `9d13768:…` for `corpus/SOURCES.md` | the registry state before and after the append |

Independent hash of the retained bodies (re-derived here, not copied from the receipt):

```
$ sha256sum .ufo/waves/round-51/sources/S262.html .ufo/waves/round-51/sources/S263.html
792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b  …/S262.html
6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de  …/S263.html
$ stat -c '%n %s bytes' …/S262.html …/S263.html
…/S262.html 174926 bytes
…/S263.html 175561 bytes
```

Both match `receipts.json` (`bytes` and `sha256`), so the body an anchor is checked against is the
round's own re-grounded body, not a later fetch.

## 3. The rules, quoted verbatim

From `/home/vgpnk/Projects/shokunin/CORPUS.md`, contract v1 section (frozen; "A change is a new
contract version, never an edit to this section"):

- `id` — "`S` + 3 or more digits, the next unused; never reused. No `|` inside any cell."
- `source` — "title — canonical URL or DOI (a repo path or command for `own-work`)."
- `kind` — "`spec` · `docs` · `paper` · `code` · `tool` · `dataset` · `talk` · `book` · `community` · `own-work`."
- `tier` — "scoped to `scope`, never global. **A**: primary or authoritative for that scope (spec, official docs, source code, original paper, maintainer statement, the lane's own re-runnable gate output). **B**: strong secondary … **C**: lead only — never sole support for an admitted entry. `community` is never A."
- `scope` — "the claim or topic the tier applies to."
- `anchor` — "exact section / heading / page / line plus revision (version, commit, or publication date). Never a bare homepage."
- `teaches` — "one grounded learner benefit. Rejected rows read `REJECTED: <reason>; flip: <what would change the verdict>`."
- `status` — "`queued` (opened, worth mining) · `mined` (cited by ≥1 path in `used-by`) · `rejected` (kept — a rejection is evidence of taste)."
- `opened` — "ISO date the row's author opened the source."
- `recheck` — "ISO date or cadence (`90d`, `180d`, `on-release`)."
- `used-by` — "repo-relative paths of the knowledge entries or lessons citing the row, comma-separated, or `—`."

Shape: "`## Search log` one prose note per bounded search (rule 5)"; "`## Leads (unopened)` bullets; a lead is not evidence and never a row".

Rule 1: "**A row is a claim.** Write it only after opening the source in the round that writes the
row. The round lesson's `## Gate` records, for every new row, the URL, the access date, and a
≤25-word quote with its location grounding `teaches`."

Rule 5: "**Search log.** PRISMA-inspired, not PRISMA-compliant: question/query, where searched,
date, identified / screened / included / excluded counts, exclusion reasons, stop rationale. A
negative claim carries its sweep."

Corpus-wide rule that the `anchor`/`teaches` pair also answers to: "**A quote names its location.**
Frontmatter vs body, header comment vs code, script vs installed skill."

## 4. Cell matrix — S262

| # | cell | rule (quoted) | value (verbatim) | check a reader can run | verdict |
|---|---|---|---|---|---|
| 1 | id | "`S` + 3 or more digits, the next unused; never reused." | `S262` | below | **VIOLATION of "the next unused"** (V1) |
| 2 | source | "title — canonical URL or DOI" | `Google Search Central — What is URL canonicalization — https://developers.google.com/search/docs/crawling-indexing/canonicalization` | title + absolute URL present, no pipe character | pass; note N2 (three names for one page) |
| 3 | kind | enum of ten | `docs` | in enum | pass |
| 4 | tier | "scoped to `scope`, never global"; A = "primary or authoritative for that scope" | `A` | vendor's own doc, scope = vendor's own selection mechanism | pass; no `community`-A inflation |
| 5 | scope | "the claim or topic the tier applies to" | `Google's canonical selection mechanism — the ground the lane's held static preflight explicitly disclaims` | second clause checked against `corpus/knowledge/static-canonical-preflight.md:7-9` = "publisher-side static-file validation, not browser crawling or search-engine canonical selection." | pass |
| 6 | anchor | "exact section / heading / page / line plus revision … Never a bare homepage." | `§ "What is URL canonicalization" (doc rev. Last updated 2026-08-20 UTC)` | below | **VIOLATION: not a heading** (V2). Revision half is present and verified in the body |
| 7 | teaches | "one grounded learner benefit" | `a declared canonical is a hint, not a rule; Google chooses the page that is objectively the most complete and useful for search users, weighing HTTP/HTTPS, redirects, sitemap presence and rel=canonical annotations` | both halves found in the body (`indicating a canonical preference is a hint, not a rule`; `There are a handful of factors that play a role in canonicalization: whether the page is served over HTTP or HTTPS, redirects, presence of the URL in a sitemap, and rel="canonical" link annotations`) | pass on grounding; note N5 (Gate quote covers the headline only) |
| 8 | status | `queued` · `mined` (cited by ≥1 path in `used-by`) · `rejected` | `mined` | in enum; `used-by` non-`—` and the path exists | pass |
| 9 | opened | "ISO date the row's author opened the source" | `2026-10-24` | ISO `YYYY-MM-DD`; matches `receipts.json.fetchedAt` `2026-10-24T23:16:49-03:00` | pass; note N3 (UTC is 2026-10-25) |
| 10 | recheck | "ISO date or cadence (`90d`, `180d`, `on-release`)" | `180d` | matches the `NNd` form and the lane's other Google rows (S137/S138/S139/S273/S274/S286) | pass; note N4 |
| 11 | used-by | "repo-relative paths …, or `—`" | `corpus/knowledge/canonical-selection.md` | `[ -e ]` → exists | pass; exactly one path, which C4 expects |

Row shape: 11 cells (`NF=13` including the two edge pipes), no literal or escaped pipe.

## 5. Cell matrix — S263

| # | cell | rule (quoted) | value (verbatim) | check a reader can run | verdict |
|---|---|---|---|---|---|
| 1 | id | "the next unused; never reused" | `S263` | below | **VIOLATION of "the next unused"** (V1) |
| 2 | source | "title — canonical URL or DOI" | `Google Search Central — Googlebot — https://developers.google.com/search/docs/crawling-indexing/googlebot` | title + absolute URL, no pipe character | pass (page `<title>` is "What Is Googlebot …"; H1 is "Googlebot") |
| 3 | kind | enum of ten | `docs` | in enum | pass |
| 4 | tier | A = "primary or authoritative for that scope" | `A` | vendor's own crawler doc, scope limited to crawler identity | pass; no tier inflation |
| 5 | scope | "the claim or topic the tier applies to" | `The identity of Google's crawler on the wire — which user-agent a publisher meets per device class and how to tell the subtypes apart` | body names the two types and the header-based identification | pass |
| 6 | anchor | "exact section / heading / page / line plus revision" | `§ "Googlebot is the generic name for two types of web crawlers used by Google Search" (doc rev. Last updated 2026-02-03 UTC)` | below | **VIOLATION: body sentence, not a heading; not an exact line** (V3). Revision half present and verified |
| 7 | teaches | "one grounded learner benefit" | `Googlebot is a generic name covering Googlebot Smartphone and Googlebot Desktop; the subtype is identified from the HTTP user-agent request header, and both obey the same robots product token` | all three clauses found in the body (paragraph + `<ul>`; "identify the subtype … HTTP user-agent request header"; "both crawler types obey the same product token (user agent token) in robots.txt") | pass on grounding; note N5 |
| 8 | status | `queued` · `mined` · `rejected` | `mined` | in enum; `used-by` cites one existing path | pass |
| 9 | opened | "ISO date the row's author opened the source" | `2026-10-24` | same receipt `fetchedAt` | pass; note N3 |
| 10 | recheck | "ISO date or cadence (`90d`, `180d`, `on-release`)" | `180d` | matches `NNd` | pass; note N4 (baseline already past at writing) |
| 11 | used-by | repo-relative paths or `—` | `corpus/knowledge/crawler-identity.md` | `[ -e ]` → exists | pass; exactly one path |

Row shape: 11 cells, no literal or escaped pipe.

## 6. Named violations

### V1 — `id` (both rows): not "the next unused" at the moment of the append

Rule: "`S` + 3 or more digits, the next unused; never reused."

Committed state of the registry immediately before the append (`5591557^` = `19a99bd`):

```
$ git show 19a99bd:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
143
$ git show 19a99bd:corpus/SOURCES.md | awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); sub(/^S/,"",i); if(i+0>m)m=i+0} END{print "max=S"m}'
max=S286
$ git show 19a99bd:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S287[[:space:]]*\|'
0
```

The highest id held before the append was **S286**, and **S287 was free**. The rows were written as
**S262 and S263** — below the high-water mark, so at write time they were not "the next unused".
The other half of the rule holds: neither id existed before (`duplicate ids` sweep prints nothing),
so nothing was *reused*, and the table now reads `… S273, S274, S286, S262, S263`, i.e. out of
numeric order.

The round lesson's own "Id collision check" states the test it ran: "The staged ids that overlap
the lane registry are S273, S274 and S286 — none of them is adopted this round. The adopted ids
S262 and S263 are unused in the lane registry". That is a collision test, not the allocation test
the schema states. The round's `assimilation/staged-ids` is a prospective range (S250 … S370) that
also contains ids already adopted in earlier rounds (S273, S274, S286), so it is not evidence that
S262/S263 were reserved before S287 became the next free number.

### V2 — `anchor` S262: the `§` names a left-nav label, not a heading

Rule: "exact section / heading / page / line plus revision … Never a bare homepage."

Value: `§ "What is URL canonicalization" (doc rev. Last updated 2026-08-20 UTC)`

In the retained body, `S262.html`:

```
$ python3 -c "b=open('.ufo/waves/round-51/sources/S262.html').read(); print(b.count('What is URL canonicalization'))"
1
```

The single occurrence is inside the left navigation, not the article:

```html
<span class="devsite-nav-text" tooltip>What is URL canonicalization</span>
```

The article's own heading and the body:

```html
<h1 class="page-title" id="what-is-canonicalization" data-text="What is canonicalization" tabindex="-1">What is canonicalization</h1>
```

Article headings in the retained body: `h1 What is canonicalization`, `h3 How Google indexes and
chooses the canonical URL` (the remaining `h3`s are footer link boxes). Occurrences of the anchor
string inside the article body: **0**. The document `<title>` element holds "What is URL
Canonicalization | Google Search Central &nbsp;|&nbsp; Documentation &nbsp;|&nbsp; Google for
Developers" (capital `C`; the `&nbsp;` entities are the separators), so the row's string is the nav
label, matching case and all.

A reader who follows the anchor and looks for the quoted section will not find it: the page says
"What is canonicalization". This is the class the corpus rule "A quote names its location" exists
for, applied to a heading rather than to a prose quote.

### V3 — `anchor` S263: the `§` names the first body sentence, truncated

Rule: same `anchor` rule.

Value: `§ "Googlebot is the generic name for two types of web crawlers used by Google Search" (doc rev. Last updated 2026-02-03 UTC)`

In the retained body, `S263.html`:

```
$ python3 -c "b=open('.ufo/waves/round-51/sources/S263.html').read(); print(b.count('Googlebot is the generic name for two types of'))"
1
```

The one occurrence is the article's opening paragraph, split by a link, and it does not end where
the anchor quote ends:

```html
<p> Googlebot is the generic name for two types of <a href="/search/docs/fundamentals/how-search-works">web crawlers</a> used by Google Search: </p>
<ul> <li> … <b>Googlebot Smartphone</b>… </li> <li> … <b>Googlebot Desktop</b>… </li> </ul>
```

Article headings in the retained body: `h1 Googlebot`, `h2 How Googlebot accesses your site`,
`h2 Blocking Googlebot from visiting your site`, `h2 Verifying Googlebot` (the `h3`s are footer
link boxes). There is no heading carrying the quoted sentence.

So the locator is wrong twice over: `§` asserts a section that does not exist, and the quoted
string stops before the colon and the two-item list, so it is not an exact "line" either. The
string is an exact substring only after the `<a>` tag is removed or whitespace-collapsed (the row
itself is silent about that). The revision half (`Last updated 2026-02-03 UTC.`) is present
verbatim in the body.

### V4 — Search log: no round-51 note (registry-level, not a cell)

Shape: "`## Search log` one prose note per bounded search (rule 5)".

```
$ grep -c 'Round 51\|round 51\|Round-51\|round-51' corpus/SOURCES.md
0
$ awk 'NR>=170 && NR<=207' corpus/SOURCES.md | grep -o 'Round [0-9]*' | sort -u -V | tr '\n' ' '
Round 21 Round 22 Round 23 Round 24 Round 25 Round 26 Round 28 Round 29 Round 30 Round 47
```

The round did run a bounded search and did screen and exclude: `corpus/lessons/round-51.md` records
two fetched URLs, their access time, two retained bodies, and two refused staged entries with
reasons and flips ("Refused entries (reason and flip)"). Rule 5 asks for the query, where searched,
date, identified / screened / included / excluded counts, exclusion reasons and stop rationale.
None of that is in the Search log; the section's last note is round 47, so rounds 48–51 are all
unrepresented. This is an omission a reader sees by eye (the section has no round-51 paragraph),
not a malformed cell.

## 7. Cells that pass, with the caveat a reader should still see

**N2 — `source` (S262): three names for one page.** Nav label `What is URL canonicalization`;
`<title>` `What is URL Canonicalization …`; H1 `What is canonicalization`. The cell's choice is
defensible as "title" (it matches the nav/title text), but it is the same string that fails V2 as
a heading. One row, three names, one of them used as a `§`.

**N3 — `opened` (both rows): local date, UTC is the next day.** The cell says `2026-10-24`; the
only timestamp behind it is `receipts.json.fetchedAt = 2026-10-24T23:16:49-03:00`:

```
$ TZ=UTC date -d '2026-10-24T23:16:49-03:00' '+%Y-%m-%dT%H:%M:%SZ'
2026-10-25T02:16:49Z
```

The append commit is `2026-10-24 23:20:56 -0300` = `2026-10-25T02:20:56Z`; the wave's own start
stamp is `2026-10-25T06:32:17Z`. The rule says "ISO date the row's author opened the source", so
the author's date is the textually correct reading and the cell is not malformed. But the same row
writes its revision dates with an explicit `UTC`, and the C2 counter's `ROUND_DATE` constant is the
hard-coded literal `"2026-10-24"` (`c51_quote_truth.py:46`), so the check and the row agree only
because both chose the same zone. A reader comparing `opened` to the receipt must apply `-03:00`
or conclude the row is a day early.

**N4 — `recheck: 180d` (both rows): valid cadence, different freshness baselines.** `180d` matches
the allowed `NNd` form and every other Google row in the registry. Measured from the vendor
revision each row cites:

- S262: revision `2026-08-20` → opened `2026-10-24` = **65 days** old at admission; cadence expires
  `2026-10-24 + 180d = 2027-04-22`.
- S263: revision `2026-02-03` → opened `2026-10-24` = **263 days** old at admission. `180d` from
  that revision is `2026-08-02`, i.e. already past on the day the row was written; only if the
  cadence is counted from `opened` (`2027-04-22`) is the row fresh.

The frozen contract does not pin the baseline, so neither cell is malformed. It is the one place on
the freshness axis where a reader sees a number (`2026-02-03`) older than the row's own cadence at
the moment of writing. "Re-grounded this round" is true of the bytes (hashes above match) and false
of the vendor's revision: the page has not changed since February. These are different claims and
the row states only the first.

**N5 — `teaches` (both rows): body-grounded, but the Gate quote grounds only the headline.** Rule 1
requires the Gate's ≤25-word quote to ground `teaches`. The Gate quotes are 10 and 9 words:

- S262: `indicating a canonical preference is a hint, not a rule` — grounds clause 1 of the cell;
  clause 2 (the four weighed signals) is in the body but not in the Gate quote.
- S263: `Googlebot is the generic name for two types of` — grounds clause 1; the user-agent-header
  clause and the shared-product-token clause are in the body but not in the Gate quote.

Both quotes are exact raw substrings of the retained bodies (`grep -c` → 1 each) and both are
inside the 6–25 word band the counter enforces. I record this as a scope note, not a violation:
the rule asks for a quote "grounding `teaches`", and the quotes ground its headline claim.

**Other passes, briefly.** `kind: docs` and `tier: A` are consistent with each other and with the
scope (the vendor describing its own mechanism; the census reports `FLEET tier.invalid 0`, so this
is not a `community`-A row). `status: mined` is a
legal value and is earned under the rule's own definition ("cited by ≥1 path in `used-by`"): both
`used-by` paths exist and each row names exactly one. `scope` for S262 carries a lane-internal
claim that I verified against the held preflight file, not just accepted. Neither row appears in
any `## Paths` sequence; rule 3 does not require it and rule 4 counts entries, not path coverage,
so that is not a violation either.

## 8. Row shape and the registry's own census

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
145
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
(no output)
```

Maintained census on the lane registry (read-only, from the fleet root):

```
$ ./scripts/sources-census.sh --file /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
file	rows	145
file	tier.A	122
file	tier.B	6
file	tier.C	17
file	status.mined	115
file	status.queued	8
file	status.rejected	22
FLEET	rows	145
FLEET	tier.A	122
FLEET	tier.B	6
FLEET	tier.C	17
FLEET	tier.invalid	0
FLEET	status.queued	8
FLEET	status.mined	115
FLEET	status.rejected	22
FLEET	status.invalid	0
FLEET	missing	0
exit=0
```

No E03 (malformed row) and no E04 (within-scope duplicate) for either row; the pre-append receipt
in `.ufo/waves/round-51/assimilation/pre-append/` shows the same for the staged registry
(`census-argv.txt` = `… sources-census.sh validate --file …/pre-append/corpus/SOURCES.md`, no
`--root`; `census-exit.txt` = `0`; stdout ends `file	ok	…/pre-append/corpus/SOURCES.md`; its only
findings are twelve pre-existing `W04` duplicate-URL warnings on older rows).

The append itself is two insertions and nothing else:

```
$ git show --stat --oneline 5591557
 LOG.md                                  |   9 +++
 corpus/SOURCES.md                       |   2 +
 corpus/knowledge/canonical-selection.md |  77 +++++
 corpus/knowledge/crawler-identity.md    |  54 ++++
 corpus/lessons/round-51.md              | 116 +++++
```

No existing registry row was edited, so rule 2's in-place latitude is not exercised.

## 9. Adjacent committed-bytes conflict (outside the cell scope; for the canonical judge)

Not a cell and not my claim to adjudicate. Recorded verbatim because it is visible in the bytes and
it concerns these two rows.

`contract.json` C2 condition C8 reads: "the pre-append mirror commit is a strict ancestor of the
measured revision, **the mirror's registry carries none of the adopted ids** and the measured
revision's registry carries all of them".

The mirror file itself, at its only commit `19a99bd`, carries both adopted rows:

```
$ git show 19a99bd:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S26[23][[:space:]]*\|'
2
$ git rev-parse 19a99bd:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md 5591557:corpus/SOURCES.md
9e2a22175ef95a23252b349d8743cf0e5b5480fc
9e2a22175ef95a23252b349d8743cf0e5b5480fc
```

The counter does not read the mirror file's registry for that condition; it reads `REGISTRY`
(`corpus/SOURCES.md`) at the mirror commit, where the count is 0:

```
$ git show 19a99bd:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S26[23][[:space:]]*\|'
0
```

`c51_quote_truth.py:266-284` (`mirror_registry = show(root, mirror_commit, REGISTRY)`) matches that
narrower reading, so C8 passes. Under the contract sentence taken literally, C8 is false on
committed bytes. The pre-append census receipt is coherent with the mirror being the staged payload
(it validates 145 rows, i.e. the post-append shape, before it is copied into `corpus/`), so the
conflict is in the word "mirror's registry", not in the receipt. Reported, not resolved.

## 10. Live working-tree note (not committed, not attributed)

While this was being read, the lane working tree carried edits to the same pre-append artifacts
(`git status --porcelain` → 26 lines overall, including `.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md`
and `…/census-exit.txt`). At the instant of reading:

```
$ git diff --stat -- .ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md
 .../pre-append/corpus/SOURCES.md | 2 --
 1 file changed, 2 deletions(-)
$ git diff -- .ufo/waves/round-51/assimilation/pre-append/census-exit.txt
-0
+exit=0
```

The two deleted lines are the S262 and S263 rows exactly as quoted in §4–§5
(`git diff … | grep -c '^-| S26'` → 2, read at the same instant).

I did not write these and do not attribute them. Two consequences for whoever lands the wave: (a)
the HEAD bytes I judged are unchanged (`git rev-parse HEAD:corpus/SOURCES.md` =
`9e2a221…`; `git status --porcelain corpus/SOURCES.md` → 0 lines), and (b) if that `census-exit.txt`
text were committed as-is, C7's `exit_text.strip() != "0"` comparison would no longer see `0`.
One read of `corpus/SOURCES.md` returned 147 rows mid-session; two later reads returned 145 and the
file matched HEAD, so I treat 145 as the committed count and the 147 reading as an unreproduced
transient.

## 11. Limits

- **No network.** I did not re-fetch either URL. The anchor findings (V2, V3) are assertions about
  the round's own retained bodies, which are hash-pinned to `receipts.json`. Whether Google's live
  page carries a heading titled "What is URL canonicalization" today is untested here; the round's
  evidence says it does not.
- I did not run `c51_quote_truth.py` or `c51_wave_ledger.py`; C2's score is not re-derived here,
  and no statement above depends on a score.
- I did not read the `>1MiB` round-48 validate copies, `considerthese/`, or the round-46 residual
  directory beyond `git status` naming it. Nothing in this report rests on them.
- No tool was installed or upgraded (tooling directive: nothing to record).
- Scratch: none; the inline `python3` heredocs needed no files, and nothing under `/tmp` was
  written.

## 12. Bottom line for the L1

| item | state |
|---|---|
| 22 cells across the two rows | 18 conform; 4 do not (2 × `id`, 2 × `anchor`) |
| V1 `id` ×2 | not "the next unused" (max held id was S286, S287 free); no reuse, no duplicate |
| V2 `anchor` S262 | `§` string is a left-nav label; H1 is "What is canonicalization"; 0 in-body occurrences |
| V3 `anchor` S263 | `§` string is the opening body sentence, split by a link and truncated before its colon/list; no such heading |
| V4 Search log | no round-51 note at all; last note is round 47 |
| dates / cadence / tier / status / kind / used-by / shape | conform; caveats N2–N5 above |
| retained bodies | sha256 and byte counts independently re-derived and matching the receipts |

Writable surface: this file only. Nothing else in the lane was created, edited, staged, committed
or checked out.
