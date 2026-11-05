VERDICT: this seat's source work holds — the six drafted registry rows (S471–S476) and the source-seat Gate material are correct and machine-verified, but the L1's already-written Gate list in `corpus/lessons/round-93.md` carries four defects (three quoted line spans that do not contain their quote, one quote over the ≤25-word rule) that I found and appended a corrected re-verification beside, not repaired in place.

Seat: `w1/ScribeSources` (scribe). Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Freeze `bb8012fee38c0e497cdaf36337072737bca0b3cd`, base `10ecbd1ade91d0721e87a9942a66a2b61d5ce8d5`.
No commit, push, stage, or mutating git/jj command was run in the lane. The only git use was a
scratch clone under my own scratch root, deleted before this yield.

## What I did

1. Fetched each of the two named RFC texts myself with one public GET each and retained the bodies
   under my wave directory; recorded status, byte count, sha256, UTC access date; `cmp`'d them
   against the L1's retained bodies.
2. Drafted six registry rows in the fleet 11-column schema, ids S471–S476 continuing after the
   highest existing id S470, in `.ufo/waves/round-93/w1/ScribeSources/rows.append.md`.
3. Wrote the lesson Gate material — ten admits with exact located quotes and three rejects with
   reasons and flip conditions — appended to `corpus/lessons/round-93.md` as a
   `### Source-seat re-verification (w1/ScribeSources)` subsection under the existing `## Gate`
   heading, so the L1's `## Gate` line count stays at exactly 1 (verified) and the E4 Mistakes-table
   contiguity is untouched (verified).
4. Ran the fleet census and pasted it.

## 1. Fetch receipt (one GET per source)

```
$ cd .ufo/waves/round-93/w1/ScribeSources/src
$ curl -sS -o rfc9110.txt -w 'rfc9110 http=%{http_code} bytes=%{size_download}\n' https://www.rfc-editor.org/rfc/rfc9110.txt
rfc9110 http=200 bytes=502941
$ curl -sS -o rfc9111.txt -w 'rfc9111 http=%{http_code} bytes=%{size_download}\n' https://www.rfc-editor.org/rfc/rfc9111.txt
rfc9111 http=200 bytes=84477
$ sha256sum rfc9110.txt rfc9111.txt
21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a  rfc9110.txt
aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e  rfc9111.txt
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-11-05T01:26:51Z
```

`cmp` against the L1's retained bodies — both identical, exit 0:

```
$ cmp .ufo/waves/round-93/L1/src/rfc9110.txt .ufo/waves/round-93/w1/ScribeSources/src/rfc9110.txt   # exit 0
$ cmp .ufo/waves/round-93/L1/src/rfc9111.txt .ufo/waves/round-93/w1/ScribeSources/src/rfc9111.txt   # exit 0
```

`rfc9111.txt` is also byte-identical to the round-92 retained body
(`.ufo/waves/round-92/L1/src/rfc9111.txt`, `cmp` exit 0), so the round-92 §4.2.2 ground is unchanged
at this fetch.

Full receipt: `.ufo/waves/round-93/w1/ScribeSources/receipts.txt`. Retained bodies:
`.ufo/waves/round-93/w1/ScribeSources/src/{rfc9110.txt,rfc9111.txt}`.

## 2. Drafted registry rows

`LANE/.ufo/waves/round-93/w1/ScribeSources/rows.append.md` — six rows, S471–S476, continuing after
the highest existing id (S470, confirmed with `grep -oE '^\| S[0-9]+' corpus/SOURCES.md | sort -t S
-k2 -n | tail -1`). All six: kind `spec`, tier `A`, status `mined`, opened `2026-11-04`, recheck
`180d`, `used-by corpus/knowledge/conditional-request-evaluation.md`.

| id | anchor |
|---|---|
| S471 | RFC 9110 §13.2.2 Precedence of Preconditions — lines 6222 (heading), 6233–6234 (order sentence), 6236–6282 (steps 1–6) |
| S472 | RFC 9110 §13.1.1 If-Match — lines 5785, 5794–5797, 5799, 5820–5829, 5831–5833 |
| S473 | RFC 9110 §13.1.2 If-None-Match — lines 5872, 5880–5883, 5885, 5917–5926, 5928–5932 |
| S474 | RFC 9110 §13.1.3 + §13.1.4 ignore rules — lines 5942, 5956–5958, 5963–5966, 5968–5969, 6006–6011; 6023, 6037–6039, 6043–6045, 6047–6048, 6072–6073 |
| S475 | RFC 9110 §8.8.3.2 Comparison — lines 3643, 3648–3649, 3651–3653, 3658–3668 (Table 3 caption 3670) |
| S476 | RFC 9111 §4.3.2 — lines 866, 881–885, 887–891 |

Schema checks, run mechanically:

```
$ python3 - <<'PY'   # per row: split on '|', count body cells, assert no '|' inside any cell
S471 cells= 11 pipes_in_cells= 0 id_ok= True
S472 cells= 11 pipes_in_cells= 0 id_ok= True
S473 cells= 11 pipes_in_cells= 0 id_ok= True
S474 cells= 11 pipes_in_cells= 0 id_ok= True
S475 cells= 11 pipes_in_cells= 0 id_ok= True
S476 cells= 11 pipes_in_cells= 0 id_ok= True
ALL_ROWS_11_CELLS_NO_PIPE
```

Every scope cell names the earlier rows it is distinct from (S010/S028/S033/S453/S454/S455/S465/S466
for the RFC 9110 rows; S467/S469/S470 for the RFC 9111 row), so a within-lane duplicate is visible
from the cell text alone. The census W04 advisories for the two RFC URLs are the pre-existing class
(S453/S454/S455/S465/S466 already carry it for `rfc9110.txt`), not a new defect class.

**Census validation of the drafted rows** — the six rows were inserted into a scratch clone's
registry (clone of the lane at the frozen revision, `refs/heads/master` re-pointed at the lane's
master) and the fleet census run against that file:

```
$ scripts/sources-census.sh validate --file $S/clone/corpus/SOURCES.md --today 2026-11-05
file	W04	S471 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
file	W04	S472 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
file	W04	S473 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
file	W04	S474 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
file	W04	S475 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
file	W04	S476 duplicate url www.rfc-editor.org/rfc/rfc9111.txt across scopes
file	ok	$S/clone/corpus/SOURCES.md
exit=0
```

W04 31 → 37, exactly the six new rows re-scoping the two RFC URLs. No E-code: no duplicate id, no
duplicate URL-within-scope, every `recheck` and `opened` valid, `used-by` path resolvable.

**The lane's registry is untouched.** `corpus/SOURCES.md` is unmodified (`git status --porcelain`
shows it clean); the L1 appends these rows.

## 3. Lesson Gate material

Appended to `corpus/lessons/round-93.md` as `### Source-seat re-verification (w1/ScribeSources)`,
immediately under the existing `## Gate` heading and before `## Registry` — append-only, no existing
line rewritten or reordered. Ten admits, each with the exact quote, its located plain-text line span
and its word count; three rejects, each with the reason and the flip condition:

- **§13.2.2 lines 6233–6234** — "A recipient cache or origin server MUST evaluate the request
  preconditions defined by this specification in the following order" (19 words).
- **§13.1.1 lines 5794–5795** — "An origin server MUST use the strong comparison function when
  comparing entity tags for If-Match" (15 words).
- **§13.1.2 lines 5880–5881** — "A recipient MUST use the weak comparison function when comparing
  entity tags for If-None-Match" (14 words).
- **§8.8.3.2 lines 3648–3649** — "two entity tags are equivalent if both are not weak and their
  opaque-tags match character-by-character" (15 words).
- **§13.1.2 lines 5930–5931** — "the origin server MUST respond with either a) the 304 (Not
  Modified) status code if the request method is GET or HEAD" (22 words).
- **§13.1.3 lines 5956–5957** — "A recipient MUST ignore If-Modified-Since if the request contains
  an If-None-Match header field" (13 words).
- **§13.1.3 lines 5963–5966** — "the request method is neither GET nor HEAD" (8 words).
- **§13.1.4 lines 6037–6038** — "A recipient MUST ignore If-Unmodified-Since if the request contains
  an If-Match header field" (13 words).
- **§13.1.4 lines 6072–6073** — "earlier than or equal to the date provided in the field value, the
  condition is true" (16 words).
- **RFC 9111 §4.3.2 lines 889–890** — "the If-Match and If-Unmodified-Since conditional header
  fields are not applicable to a cache" (13 words).

Rejects (with reason and flip condition, as the item requires):

1. **The RFC-Editor errata pages as a grounding row.** The RFC 9110 listing carries 14 records and
   none targets a section in 13.x or 8.8.3.x; the RFC 9111 listing carries 4 records — 2 *Reported*
   (eid 9004 §3.5, eid 9185 §4.3.4), 1 *Held for Document Update* (eid 9166 §5.2.3), 1 *Rejected*
   (eid 7695 §4.3.2). No accepted change touches §13.1.x, §13.2.2, §8.8.3.2 or §4.3.2. Flip: an
   erratum in *Verified* or *Held for Document Update* status touching one of those sections.
2. **A secondary explainer for the precedence order.** Tier inflation; the specification text grounds
   the order directly at tier A. Flip: a precedence point the RFC leaves unstated that the secondary
   source documents with a locator.
3. **The proposition "the RFC fixes the 304 body content".** §15.4.5 lines 7477–7478 says a 304
   response "is terminated by the end of the header section; it cannot contain content or trailers",
   and §15.4.5 lines 7456–7462 lists the header fields the sender must or should regenerate. The RFC
   fixes which *metadata* a 304 carries, not the body of the stored representation. Flip: a section
   that states the 304's body content.

Every quote was checked mechanically against the bodies this seat fetched, not by eye:

```
$ cd .ufo/waves/round-93/w1/ScribeSources && python3 -B verify_quotes.py
9110 §13.2.2 lines 6233-6234  words=19 <=25: True  exact:True
9110 §13.1.1 lines 5794-5795  words=15 <=25: True  exact:True
9110 §13.1.2 lines 5880-5881  words=14 <=25: True  exact:True
9110 §13.1.3 lines 5956-5957  words=13 <=25: True  exact:True
9110 §13.1.3 lines 5963-5966  words= 8 <=25: True  exact:True
9110 §13.1.4 lines 6037-6038  words=13 <=25: True  exact:True
9110 §13.1.4 lines 6072-6073  words=16 <=25: True  exact:True
9110 §13.1.2 lines 5930-5931  words=22 <=25: True  exact:True
9110 §8.8.3.2 lines 3648-3649  words=15 <=25: True  exact:True
9111 §4.3.2 lines  889-890  words=13 <=25: True  exact:True
9110 §15.4.5 lines 7477-7478  words=18 <=25: True  exact:True
ALL_OK
exit=0
```

Receipt: `quotes.json` (`all_ok=true`). Script: `verify_quotes.py` (my own, in my wave directory).

Post-edit structural checks on the lesson: `grep -c '^## Gate$' corpus/lessons/round-93.md` → **1**
(E1 satisfied, no duplicated heading); the `## Mistakes` table has no blank line between two `|`
rows (E4 satisfied).

## 4. Census (the required command, pasted)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
kake	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
kake	W04	S110 duplicate url www.w3.org/TR/xml across scopes
kake	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	W04	S416 duplicate url ziyuan.baidu.com/college/courseinfo?id=1399 across scopes
kake	W04	S417 duplicate url ziyuan.baidu.com/college/courseinfo?id=267&page=15 across scopes
kake	W04	S427 duplicate url developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers across scopes
kake	W04	S433 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S445 duplicate url html.spec.whatwg.org/multipage/links.html across scopes
kake	W04	S450 duplicate url html.spec.whatwg.org/multipage/semantics.html across scopes
kake	W04	S451 duplicate url www.rfc-editor.org/rfc/rfc3339.txt across scopes
kake	W04	S453 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S454 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S455 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S461 duplicate url httpwg.org/specs/rfc9111.html across scopes
kake	W04	S462 duplicate url httpwg.org/specs/rfc9111.html across scopes
kake	W04	S463 duplicate url httpwg.org/specs/rfc9111.html across scopes
kake	W04	S465 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S466 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S467 duplicate url www.rfc-editor.org/rfc/rfc9111.txt across scopes
kake	W04	S468 duplicate url www.rfc-editor.org/rfc/rfc8259.txt across scopes
kake	W04	S469 duplicate url www.rfc-editor.org/rfc/rfc9111.txt across scopes
kake	W04	S470 duplicate url www.rfc-editor.org/rfc/rfc9111.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
exit=0
```

Exit 0, 31 W04 advisories, no E-code. Saved at `.ufo/waves/round-93/w1/ScribeSources/census.txt`.
The census reads the lane's registry, which does not yet contain the drafted rows; the projected
post-append reading (six rows inserted) is the scratch-clone run quoted in §2 — exit 0, W04 31 → 37.
Note the L1's own `## Registry` section of the lesson already states "W04 advisories 31 → 37", which
matches my measurement exactly.

## 5. Findings

**F1 (source-seat, status-neutral, in the round's own material). Four defects in the L1's Gate
quote list in `corpus/lessons/round-93.md`.** The L1's Gate cites a line span that does not contain
the quote in three cases, and one quote exceeds the ≤25-word rule. Machine receipt
(`l1-gate-audit.json`, script `check_l1_gate.py`, exit 1):

| Gate entry | cited span | quote actually at | defect |
|---|---|---|---|
| §13.2.2 "A recipient cache or origin server MUST evaluate…" | 6229–6231 | **6233–6234** | cited span carries the "lost update preconditions" rationale, not the quoted sentence |
| §13.1.3 "the request method is neither GET nor HEAD" | 5963–5965 | **5963–5966** | the phrase crosses into line 5966 ("HEAD."), so the quote is not wholly inside the cited span |
| §8.8.3.2 weak comparison "…tagged as 'weak'" | 3648–3653 | 3651–3653 | the RFC splits "opaque-tags" across lines 3651/3652 by hyphenation, so the quote as printed is not a literal substring of any contiguous span |
| §13.1.2 304-vs-412 quote | 5930–5933 | 5928–5932 | the quote is **26 words** against the ≤25-word rule the Gate itself states; the L1 counts it as 23 |

The quoted *text* of the first two is right and the sentences exist; only the cited line spans are
wrong. The third is a rendering issue: the L1's quote de-hyphenates "opaque-tags" and uses single
quotes for `"weak"`, so it is a faithful paraphrase but not a literal substring. I did **not** repair
the L1's lines; I appended a corrected re-verification block beside them, in the lane's append-only
form, and named the defects there. This is a lesson-material defect, not a counter or contract
defect, and it does not change any claim's status. Route it with the round's other findings.

**F2 (observation, already consistent). The knowledge entry's id set agrees with my rows.**
`corpus/knowledge/conditional-request-evaluation.md` (landed by ScribeEntry, not by me) carries
`source: S471 S472 S473 S474 S475 S476` naming the same seven anchors in the same order, and
`recheck: 180d`. I matched both, so the entry's ids and my drafted rows agree; the entry's `source:`
line will resolve under E3 once the L1 appends the rows.

**F3 (limitation, honest). The L1's Gate admits are not all literal substrings as printed, and I
could not tell from the file whether the L1 intended a normalized quotation convention.** My
verification normalizes whitespace and requires the quote to be a substring of the cited span after
that normalization. Under that convention the L1's weak-comparison quote fails. If the lane intends
"normalized quotation with line-wrap de-hyphenation" as admissible, then F1's third row is a
convention question rather than a defect; the first two rows and the word-count row are defects
under any convention. This is stated so the outside closure can judge on the lane's own convention
rather than mine.

**F4 (limitations of this seat's reach).** I did not run the round's frozen counters to score any
claim; my seat is not a counter seat and both counters are frozen. The census is the only gate I
ran. My rows' anchors are verified against the retained bodies, but I did not independently confirm
that the contract's clause wording is a faithful reading of those anchors — that is `ScoutContract`
and `ReviewC2`'s seat, and I flagged the reading to them only through the shared lesson file.

**F5 (independent confirmation, not a finding).** The sibling scope seat `ConnectorScope-17` audited
these six rows against `corpus/SOURCES.md` and `sources-census.sh validate` on its own and reported
**E04 = 0** (the scopes are distinct), **tier inflation = 0** (all tier A, kind `spec`),
**W04 advisories 31 → 37**, **exit 0** — matching my own scratch-clone census run exactly. Its
receipts are filed at `.ufo/waves/round-93/w1/ConnectorScope/ConnectorScope.md`. So the drafted rows
are not a within-lane duplication of any existing scope, and the W04 rise is the pre-existing
same-URL re-scope advisory class, not a new defect.

**F6 (no defect; recorded for the round). The errata evidence for the reject rests on the L1's own
retained copies.** I fetched both errata listings myself (`/errata/rfc9110`, `/errata/rfc9111`;
HTTP 200 after the redirect to `errata.rfc-editor.org/search/`) and both are byte-identical to
`.ufo/waves/round-93/L1/src/errata-9110.html` and `errata-9111.html` (`cmp` exit 0), so the reject's
record counts (14 for 9110; 4 for 9111) are confirmed from my own bodies, not inherited.

## 6. Out of scope / not done

- No commit, push, stage, or mutating git/jj command in the lane. `corpus/SOURCES.md` is not
  touched — the six rows stay as a draft for the L1 to append.
- No frozen instrument read for behaviour, edited, or run for scoring: `c1-predicate.md`,
  `c2-contract.md`, `c93_selfassess.py`, `c93_conditional.py`, `frozen/`, `controls/` are untouched.
- No subagent dispatch (leaf seat). No message to `agent://all`.
- The scratch root `/fast/scratch/hyaku/kake-r93/ScribeSources/` was created explicitly, held one
  clone, and was **deleted** before this yield; every receipt cited above was copied into the wave
  directory first. No tree was written under `/tmp`.

## 7. Tooling

No tool was installed or upgraded by this seat; the task needed only `curl`, `sha256sum`, `cmp`,
`git`, `python3` and `bash`, all present. Nothing to record on the tooling directive.

## 8. Artifact paths (all relative to `/home/vgpnk/Projects/shokunin/kake-shokunin`)

- `.ufo/waves/round-93/w1/ScribeSources/rows.append.md` — the six drafted rows for the L1 to append.
- `.ufo/waves/round-93/w1/ScribeSources/gate.append.md` — the Gate material as a standalone block
  (same content as the appended lesson subsection, kept separately so the L1 can re-apply it).
- `.ufo/waves/round-93/w1/ScribeSources/ScribeSources.md` — this report.
- `.ufo/waves/round-93/w1/ScribeSources/receipts.txt` — fetch, cmp, errata, verification and census
  receipts with commands and exit codes.
- `.ufo/waves/round-93/w1/ScribeSources/quotes.json` — per-quote word count and substring receipt
  (`all_ok=true`).
- `.ufo/waves/round-93/w1/ScribeSources/l1-gate-audit.json` — per-pair audit of the L1's Gate quotes.
- `.ufo/waves/round-93/w1/ScribeSources/verify_quotes.py`, `check_l1_gate.py` — my own verification
  scripts (re-runnable, read-only, stdlib only).
- `.ufo/waves/round-93/w1/ScribeSources/census.txt` — the pasted census output.
- `.ufo/waves/round-93/w1/ScribeSources/src/` — the two RFC bodies I fetched, plus the two errata
  listings.
- `corpus/lessons/round-93.md` — the only lane file I edited (append-only, one added subsection).

## 9. Checks the main agent should run

1. `grep -c '^## Gate$' corpus/lessons/round-93.md` → expect `1`.
2. `git diff corpus/lessons/round-93.md` → expect only the added `### Source-seat re-verification`
   subsection, no rewritten or reordered L1 lines.
3. Append `rows.append.md`'s six rows after the S470 row inside the `## Registry` section of
   `corpus/SOURCES.md`, then re-run the census: expect exit 0 and W04 31 → 37.
4. `python3 -B .ufo/waves/round-93/c93_selfassess.py --root . --revision master` — expect E3 to
   clear for `corpus/knowledge/conditional-request-evaluation.md` once the rows exist, and E1 to
   remain cleared for `corpus/lessons/round-93.md` (the `## Gate` heading count is unchanged at 1).
