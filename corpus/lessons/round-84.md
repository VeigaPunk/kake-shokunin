# Round 84 — lessons (kake, attempt 1)

Lane `kake-shokunin`, round 84, attempt 1. Base revision
`fe42ad11eb1084ad2ea68d12c5bbb2922a089868` (lane `master` tip at round open, 2026-11-04); round
freeze `f358022f7e1b2f3846be8ceacbe3a7ef22edf4be`, which carries this round's contract, both
counters, the control-pair builder, the frozen policy expectations and the base receipts. One v1
wave, 13 seats: scout 2, executor 3, scribe 3, reviewer 2, critic 1, mutation-tester 1, connector 1.
Requested attack share is 4/13 = 30.8 % over {reviewer, critic, mutation-tester, labrat}; the single
`connector` seat is `ConnectorSibling`, which supplies the prompt §3 floor round 83 recorded as
missing.

Two claims on two axes, both author-side:

- **C1 — calibration (score 2, the lowest non-retired axis).** The round-83 routed-defect queue
  closes: `D1` … `D4` filed at `corpus/lessons/round-83-verifier-spotcheck.md` §6, frozen at the
  round open, none added and none dropped. Predicate `met <=> open == 0`, decided by
  `python3 -B .ufo/waves/round-84/c84_defect_queue.py --root <tree> [--revision <rev>]`.
- **C2 — freshness (score 10, held), capability acquisition.** A changed `policy`-class response
  header's **value** is classified, not only its name: a numeric parameter changed, a directive
  added or removed, a directive changed, the field appearing or vanishing, an order-only rewrite,
  or a value that does not parse. Decided by
  `python3 -B .ufo/waves/round-84/c84_policy_values.py --root <tree>` over the frozen capture pairs
  and `scripts/policy_value_class.py`.

Nothing in this file decides either claim. C1's after receipt is taken by the L1 after WAVE-DONE,
and C2's with it; this lesson records corrections, the round's Gate and the mined mistakes, and it
claims no green verdict that a counter has not printed.

## Corrections

The four routed defects of the round-83 non-author closure, one row each. The last column names the
file that re-derives the row: a correction whose named file is absent or reads red is a correction
the frozen counter cannot see, so no sentence in this section closes an item by itself. The three
row conjuncts the counter scans for are printed verbatim after the table.

| Item | Correction | Re-derived by |
|---|---|---|
| `D1` | The round-83 Gate's RFC 9111 citation is corrected: the section title it used (`Common Cache-Control Directives`) is not in the retained bytes, which carry `5.2.  Cache-Control`, `5.2.1.  Request Directives`, `5.2.2.  Response Directives` and `5.2.3.  Extension Directives`; the reject it supported stands, and this round cites only headings the bytes contain. | `.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt` (raw heading bytes) read by `c84_defect_queue.py` item `D1` |
| `D2` | One measurement and one boundary replace round 83's "22 + 44 words" versus "14 / 23 / 21 / 48": the `838-844` span is counted whole, seven physical lines inclusive, and the line below states the count, the boundary and the measure. | `c84_defect_queue.py` item `D2` over `rfc9111.txt` lines 838–844 |
| `D3` | The wave's own shape now carries one `connector` seat (`ConnectorSibling`) and records its sibling-overlap scan, so the prompt §3 floor is met by a seat rather than by a waiver; the item is closed only when the results file carries a non-empty connector row. | `.ufo/waves/round-84/w1-spec.json` and `.ufo/waves/round-84/w1-results.json` read by `c84_defect_queue.py` item `D3` |
| `D4` | The round-start census is a committed receipt, not prose: `controls/census-before.txt` records `census_exit=0` and 22 `W04` lines, and the counter re-derives the same line set from `corpus/SOURCES.md` under the census's own normalization. | `.ufo/waves/round-84/controls/census-before.txt` and `corpus/SOURCES.md` read by `c84_defect_queue.py` item `D4` |

[r84-correction 2026-11-04] `corpus/lessons/round-83.md` §Gate cited a "Common Cache-Control Directives" section that the retained RFC 9111 bytes do not contain; the headings they do contain are `5.2.  Cache-Control`, `5.2.1.  Request Directives`, `5.2.2.  Response Directives` and `5.2.3.  Extension Directives`, each a raw substring of the retained file, and this round's Gate cites only those four.

D2 count=66 span=838-844 measure=words-full-span

D4's receipt is `controls/census-before.txt` (full path `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/controls/census-before.txt`, committed at the freeze): 22 `W04` lines plus `census_exit=0`; the counter re-derives 22 from `corpus/SOURCES.md` at this writing (`item=D4 closed=1 state=1 row=1 receipt_w04=22 derived_w04=22`, `w1/ScribeLesson/counter-worktree-before-lesson.txt`), and the round's `S457` row leaves it at 22 because it anchors the httpwg HTML rendering, a URL `S456` does not hold; `w1/ScribeLesson/d4-census-w04.txt` records the counterfactual — a second row on `S456`'s own URL with a distinct scope reads 23 and would reopen `D4`.

Measured, not asserted: the counter at the worktree before this lesson was written read
`C1v1 revision=worktree items=4 open=3 closed=1 met=false`, exit 1 (`D4` closed, `D1`/`D2` without a
lesson line, `D3` without `w1-results.json`); at the base revision it reads
`items=4 open=4 closed=0 met=false` because the freeze's `controls/` are not in the base tree. The
after-state reading is the L1's and is not anticipated here.

## Gate

**Candidate — `S457`, RFC 9111 *HTTP Caching*: value semantics for a `policy` header — mined.**
Scope as the registry row states it: the value semantics of the `Cache-Control` response field —
freshness as age measured against a freshness lifetime, a response directive as a name with an
optional argument, `max-age` as a `delta-seconds` argument that makes the response stale once its
age exceeds that number, and the rule that a cache ignores directives it does not recognise. The
lane's class names, verdict order and equivalent-rewrite reading are lane policy and are excluded in
the row's scope cell.

URLs and access date. The row's URL is `https://httpwg.org/specs/rfc9111.html`, opened GET-only by
the round's `ScoutSources` seat, HTTP 200, 178,573 bytes, sha256
`999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64`, retained at
`.ufo/waves/round-84/w1/ScoutSources/rfc9111-httpwg.html`. The plain-text rendering is
`https://www.rfc-editor.org/rfc/rfc9111.txt`, already held as `S456` at 84,477 bytes, sha256
`aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`. Access date for both:
**2026-11-04**. The three `ds4cc.com` capture surfaces are unchanged this round and carry no new
row. The scout's `fetch-meta.txt` and `fetch-meta-httpwg.txt` record status, final URL and byte
count but no RFC 3339 fetch stamp and no digest; the digests above are recomputed here from the
retained bodies, and the date rests on the wave's run date and the row's `opened` cell — this seat
made no network call.

Admission quotes, each ≤ 25 words and located in both retained files:

- 24 words — "The max-age response directive indicates that the response is to be considered stale after its age is greater than the specified number of seconds." — `rfc9111.txt` lines 1214–1216; HTML line 282. A raw substring of the `.txt` and of the HTML line; word count and both checks in `w1/ScribeLesson/gate-quote-check.txt`.
- 16 words — "is the length of time between its generation by the origin server and its expiration time" — `rfc9111.txt` lines 587–588; HTML line 269. The HTML marks the term with `<dfn>` and prints no quotation marks, so this clause, not the full `.txt` sentence, is the unit both renderings share.

The row's `anchor` cell names §4.2 *Freshness*, §5.2 *Cache-Control*, §5.2.2 *Response Directives*
with §5.2.2.1 *max-age*, and §5.2.3 *Extension Directives*; every one of those heading strings is a
raw substring of the retained `.txt` (checked, `w1/ScribeLesson/gate-quote-check.txt`), and the
round-83 correction above is the reason that check is stated here rather than assumed.

**Reject — §4.1's normalisation sentence as the ground for the `reordered` class.** The retained
bytes say "reordering field values when order is not significant" (8 words; `.txt` 548–549, HTML
line 269). Reason: §4.1 is *Calculating Cache Keys with the Vary Header Field*, and the sentence
lists the normalisations under which two **request** header sets match; it says nothing about the
order of response `Cache-Control` directives, and the `S457` scope cell excludes exactly that
("not an ordering rule for the directive list, which this row does not quote"). Flip: if the lane
ever compares request-header values across captures — a `Vary`-key drift check — this sentence
becomes the correct anchor for that new row, and the tool would then need a request-side grammar.

**Reject — §5.2.1.1 *max-age* (the request directive) as the anchor.** Its defining sentence is 24
words (`.txt` 1122–1124): "The max-age request directive indicates that the client prefers a
response whose age is less than or equal to the specified number of seconds." Reason: it states a
client preference about a response's age; the lane's captures hold GET **responses**, so reading it
as this row's ground would attribute a request-side rule to a response-side field. Flip: a capture
that retains request headers carrying a `Cache-Control` request directive makes the request half
admissible for that capture's row.

**Reject — the wave spec's `§5.2.2.2` / `max-age` pairing.** `.ufo/waves/round-84/w1-spec.json`'s
`ScoutSources` item pairs `§5.2.2.2` with `max-age`; the retained bytes put `5.2.2.1.  max-age` at
`.txt` line 1208 and `5.2.2.2.  must-revalidate` at line 1222 (both on HTML line 282). Reason: the
pairing is the same class of error as the round-83 title slip, one section number instead of a
title, and the registry row anchors `§5.2.2.1` and says so in its anchor cell. Flip: a later RFC
revision that prints `max-age` under `§5.2.2.2`; the check is `grep -n '^5\.2\.2\.[12]\.  '` over
the retained `.txt`, which prints `1208:5.2.2.1.  max-age` and `1222:5.2.2.2.  must-revalidate`
today.

**Not claimed by this Gate.** The `reordered` class and the `policy-rewritten-equivalent` verdict are
lane readings the retained bytes do not spell out for distinct directives; the source gives the
duplicate case a first-occurrence-or-stale rule (`.txt` 677–680), which the knowledge entry records
as a limit on that class. The Gate also claims no after-state: `S457` is `status=mined` at
`opened=2026-11-04` with `recheck=180d`, and its admission belongs to the non-author closure.

## Mistakes

Rows are `class · evidence pointer · captured-by · fix`; a fix that cannot fail is not a fix, so
each names the check that can turn the row red.

- **citation-title** (D1) · `corpus/lessons/round-83.md` §Gate rejects RFC 9111 anchors under a
  "Common Cache-Control Directives" title the retained bytes do not contain · **captured-by:** the
  non-author round-83 closure, `corpus/lessons/round-83-verifier-spotcheck.md` §6 item 1 ·
  **fix:** the `[r84-correction 2026-11-04]` line above cites the four real headings; the check is
  `c84_defect_queue.py` item `D1`, which requires each heading to be a raw substring of the retained
  `.txt`, so a paraphrased title reopens `D1`.
- **measurement-span** (D2) · `corpus/lessons/round-83.md` §Gate says the `:838-839`/`:840-844`
  quotes are "22 + 44 words" while its own check line records "14 / 23 / 21 / 48"; the whole
  `838-844` span is 66 words under `len(re.findall(r"\S+", "\n".join(lines[837:844])))` ·
  **captured-by:** the non-author round-83 closure, §6 item 2 · **fix:** the single `D2 count=66
  span=838-844 measure=words-full-span` line above; the check is `c84_defect_queue.py` item `D2`,
  which re-derives the count from the same seven lines and reopens `D2` on one word of drift.
- **role-floor** (D3) · round 83's report discloses no connector seat where prompt §3 asks for ≥ 1,
  and no waiver rode the report · **captured-by:** the non-author round-83 closure, §6 item 3 ·
  **fix:** this wave's `w1-spec.json` carries one `connector` item (`ConnectorSibling`) and the
  check is `c84_defect_queue.py` item `D3`, which requires `spec_connectors >= 1` **and** one
  results row with `agent == "connector"` and non-empty output, so an empty seat still reopens it.
- **start-receipt** (D4) · round 83 gave its round-start census as prose ("exit 0, 22 `W04`") while
  only `controls/census-after.txt` was committed · **captured-by:** the non-author round-83 closure,
  §6 item 4 · **fix:** `controls/census-before.txt` is committed at this round's freeze; the check
  is `c84_defect_queue.py` item `D4`, which re-derives the `W04` set from `corpus/SOURCES.md` and
  reopens the item on a missing receipt, a red `census_exit`, or one divergent line.
- **section-number** · `.ufo/waves/round-84/w1-spec.json`'s `ScoutSources` item pairs `§5.2.2.2`
  with `max-age`; the retained bytes put `max-age` at `5.2.2.1.` (line 1208) and `must-revalidate`
  at `5.2.2.2.` (line 1222) · **captured-by:** this seat, while checking the retained bytes for the
  Gate (the registry row's anchor cell records the same correction) · **fix:** cite headings
  verbatim from the retained bytes; the check is `grep -n '^5\.2\.2\.[12]\.  '` over
  `rfc9111.txt`, which prints the two headings in that order.

## Risk

`c84_defect_queue.py` item `D4` compares the frozen `census-before.txt` to the `W04` set re-derived
from the **measured** tree, so a round that adds a registry row on a URL an earlier row already holds,
with a distinct scope, must expect `D4` to reopen. Measured here
(`w1/ScribeLesson/d4-census-w04.txt`): the same-URL counterfactual takes the derived set from 22 to
23 with the new row `S457`, while this round's actual `S457` anchors
`httpwg.org/specs/rfc9111.html`, which no earlier row holds, and the set stays 22. A future round
that adds a second row on an existing URL should either accept `D4` open or have the counter compare
a per-round diff instead of absolute set equality; this lesson does not patch the frozen counter.

## Author-side status

Both claims remain author-side. `S457` is `mined` on a 2026-11-04 access, `D1`–`D4` are corrected
above with their re-derivation files named, and the score cells in `SCORECARD.md` are untouched by
this seat. The non-author closure owes the independent re-open of the retained `.txt` and `.html`,
the line-level quote check for `S457`, the census re-derivation against the real registry, and a
decision on whether the three rejects hold.

## Integration verdict — frozen instruments retained

WAVE-DONE arrived for all 13 seats. The frozen C1 instrument reads open=0, but
`w1/ReviewC1.md` proves that v1 omits the D3/D4 prose conjuncts, joins separate
D1 correction lines, accepts null connector output and accepts census_exit=01.
`c84_defect_queue_v2.py` is a separately named diagnostic repair of the two prose
conjuncts only (10/10 selftest); it does not replace the frozen counter or erase
the remaining findings. Both prose conjuncts are actually present in this lesson.
C1's four requested repairs are delivered; instrument soundness remains qualified.

**C2 verdict: unprovable; honest stop.** A green frozen counter is not semantic
proof. `w1/ReviewC2.md` gives the decisive counterexample: Referrer-Policy chooses
the last recognized policy, so the frozen pair's reversed list can change policy.
The expectations and predicate remain frozen; the claim is not narrowed after
scoring to an easier syntactic claim. No capability credit is awarded this round.
The shipped tool is experimental syntax evidence, not a publication approval.

Additional mined mistake: **scope** · `w1/ReviewC2.md`, frozen equivalence pair ·
captured-by: independent reviewer · fix: the quality criterion below requires a
field-specific order rule; the retained counterexample makes that criterion fail.
The spelling `§5.2.2.2 max-age` in the dispatch is also wrong: max-age is §5.2.2.1.
Source URL selection avoided a mutable-census coupling; this is a disclosed
instrument limitation, not a repair of its frozen comparison.
