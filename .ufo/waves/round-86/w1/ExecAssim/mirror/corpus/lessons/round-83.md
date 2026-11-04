# Round 83 — lessons (kake, attempt 1)

Lane kake-shokunin, base measured revision `826b0061f233ce1dffb9bd6874abc1342a864247` (lane
`master` tip at round open, 2026-11-04 — the round-82 verifier spot-check commit), round freeze
`64b7199281e5457df0e08652977f698c4f34f46e` — the commit that carries this round's contract, both
counters, the header-change classifier, the junk and control-pair builders, and the base and control
receipts. The wave shape is **one v1 wave, 14 seats** (scout 2, executor 4, scribe 3, reviewer 2,
critic 1, mutation-tester 2), with no second wave and no residual call; the requested attack share is
5/14 = 35.7 % over the four directive roles (reviewer, critic, mutation-tester, labrat), the L1
holding the planner seat. Two claim axes are worked and both are **held**: `calibration` (2, the
lowest non-retired axis) carries C1, and `freshness` (10, held) carries C2. A claim moves evidence
this round, not a scalar. Everything below is author-side: admission belongs to the non-author
closure, which is not this seat.

## Claims

**C1 — calibration: the round-82 routed-defect queue closes.** Population: the six items `D1` … `D6`
filed by the non-author round-82 closure at `corpus/lessons/round-82-verifier-spotcheck.md` §6; none
added or dropped after the freeze. Frozen predicate:

    met <=> open == 0

decided from bytes by

    python3 -B .ufo/waves/round-83/c83_defect_queue.py --root <tree> [--revision <rev>] [--fleet <dir>]

which reads the measured lane tree (an exported revision in `--revision` mode) and the fleet repo
read-only. No item is decided by a sentence that merely says "closed": each carries a state conjunct
re-derived from a non-lesson file — the wave accounting re-computed from `w1-spec.json` plus
`w1-results.json`, UTF-8 byte lengths, an instrument receipt's own fields, the fleet diff that
removed the superseded lines, an executable killer suite, and a standing `corpus/QUALITY.md`
criterion — beside a row conjunct that only prose can carry. Controls, all committed before the
after-state: `controls/base-c83-defect-queue.txt` reads
`C1v1 revision=826b0061f233ce1dffb9bd6874abc1342a864247 items=6 open=6 closed=0 met=false`, exit 1;
`controls/ctl-c83-junk-queue.txt`, a tree whose lesson asserts all six items closed in prose, reads
`items=6 open=6 closed=0 met=false`, exit 1; `controls/c83-selftest-c1.txt` ends
`selftest: 9/9 passed`, exit 0, over one green all-six-closed fixture, one junk-prose fixture, one
mutant per item and a missing-tree fixture.

**C2 — freshness: the drift gate's header changes are classified, and the verdict re-derives.**
Declared surfaces: the three ids and urls frozen at `.ufo/waves/round-81/capture-expectations.json`
(`ds4cc-primary` `https://ds4cc.com/`, `ds4cc-robots` `https://ds4cc.com/robots.txt`,
`ds4cc-sitemap` `https://ds4cc.com/sitemap.xml`). Capture A is `.ufo/waves/round-81/capture` and
capture B is `.ufo/waves/round-82/capture`; no network call is made by the tool or the counter.
Frozen predicate:

    met <=> declared == 3
        and surfaces_a == 3 and surfaces_b == 3
        and receipts_ok      (GET, integer status 100..599, bytes == body length, sha256 == body
                              digest, truncated false)
        and diffs > 0 and validator == 0 and representation == 0 and unknown == 0
        and verdict == same-object
        and record_equal     (the committed record equals a fresh run's stdout after stripping one
                              trailing newline per side)
        and determinism      (two fresh runs print identical bytes)
        and control_ok       (.ufo/waves/round-83/capture-control/{a,b}: receipts verify and the
                              classifier prints verdict=representation-changed with validator >= 1)
        and tool_offline     (no socket, urllib, requests or http.client import in
                              scripts/header_change_class.py outside its docstring)
        and selftest_ok      (the tool's selftest exits 0)

decided by

    python3 -B .ufo/waves/round-83/c83_drift_class.py --root <tree> [--revision <rev>]

which prints one `surface=` line per declared surface in declared order, then one `summary=` line,
with the frozen header-class table (`per-request`, `validator`, `representation`, `policy`, and
`unknown` for a changed header absent from the table). Controls, committed before the after-state:
`controls/base-c83-drift-class.txt` reads `tool_absent=1 met=false`, exit 1;
`controls/ctl-c83-control-class.txt`, the counter over a tree whose control pair is replaced by an
identical pair, reads `control_ok=0 met=false` with `# control=verdict=same-object validator=0`,
exit 1; `controls/c83-selftest-c2.txt` ends `selftest: 9/9 passed`, exit 0 over nine fixtures
(green, body-changed, validator-changed, record-mismatch, control-does-not-flip, tool-absent,
declared-dropped, capture-a-dropped-surface, tool-network-import).

The freeze-time reading of the two committed captures is
`controls/after-c2-classes.txt`: `summary surfaces=3 diffs=14 per_request=14 validator=0
representation=0 policy=0 unknown=0 verdict=same-object`. It is the *before* state — every changed
header on all three surfaces is per-request — not this wave's after receipt, which this file does not
anticipate.

## Corrections

The six routed defects of the round-82 non-author closure are corrected here, one line each. Each row
states the correction the item requires and names the file that re-derives it; a row whose named file
is absent or red is a row the counter reads `open`, so nothing in this section can close an item by
itself.

Measured at this writing (`python3 -B .ufo/waves/round-83/c83_defect_queue.py --root . --fleet
/home/vgpnk/Projects/shokunin`, 2026-11-04T13:34:24Z): `C1v1 revision=worktree items=6 open=2
closed=4 met=false`, exit 1 — `D3`, `D5` and `D6` closed from their own files, `D1` and `D2` reading
`open spec or results absent/unreadable` because their state conjuncts need `w1-results.json` and
`w1-accounting.json`, which only WAVE-DONE produces
(`.ufo/waves/round-83/w1/ScribeLesson/counter-worktree-after-lesson.txt`). The after receipt at the
after-state is the reading of record; this note cannot stand in for it.

**D1 — attack floor.** Round 82 settled attack share `0/7` (0.0 %) against the run-15 ≥ 25 % floor; round 83 records this wave's own settlement in `.ufo/waves/round-83/w1-accounting.json`, whose `settled_attack=` field the frozen counter re-derives from `w1-spec.json` plus `w1-results.json` and requires ≥ 2 and ≥ 0.25 of settled — the number is a derivation over this wave's results rows, never a relabelling of a requested shape.

**D2 — units.** Round 82's wave prose printed character counts where the accounting records UTF-8 bytes; round 83's `.ufo/waves/round-83/w1-accounting.json` carries `bytes_basis: "utf-8"` and one `output_bytes` per seat, each re-derived by the frozen counter as `len(output.encode("utf-8"))` from `w1-results.json`, so a non-ASCII output can no longer be reported two ways.

**D3 — instrument receipt.** The standing instrument-receipt gate now has its own receipt, `.ufo/waves/round-83/controls/after-c83-instrument-check.txt`, written from a real `python3 -B scripts/instrument_receipts.py --check` run at carrier `64b71992` and reading `C2v1 revision=64b7199281e5457df0e08652977f698c4f34f46e population=30 bound=30 mismatches=0 met=true`; the frozen counter requires one `C2v1 revision=<40 hex>` line with `bound` equal to `population`, `mismatches=0` and `met=true`, so a red gate reopens the item instead of being narrated green — and the receipt's non-fatal `revision_match=false` is the documented subject-vs-carrier case (subject `70c8241b`, an ancestor of the carrier), disclosed in `w1/ExecInstrument.md` rather than suppressed.

**D4 — superseded text quoted.** The round-81 report was rewritten in place at fleet commit `7678247a3c13b1dc03ed1cb8f80d2dba603ee0ca`, which removed five physical lines from `.ufo/reports/round-81/kake.md`; §Erratum below is that erratum: it quotes them as raw `> ` lines, and the frozen counter re-derives the commit, its parent, the removed set and the quote count from fleet bytes, requiring at least four raw substrings.

**D5 — mutation survivors.** The five round-82 survivors (C1 `m3`, C1 `m5`, C2 `m2`, C2 `m4`, C2 `m5`) are guarded by `.ufo/waves/round-83/killers/run_killers.py`, which `--check` runs in-process against copies of the frozen counters and exits 0 printing `distinguished=5/5`: rows `C1-m3`, `C1-m5`, `C2-m2` and `C2-m4` read `killed` on their named fixtures with the pristine and mutant readings printed side by side, and `C2-m5` reads `equivalent` with the guarding source line `c82_capture_delta.py:239` and a one-line proof; four kills and one guarded equivalence, no survivor left unguarded (`.ufo/waves/round-83/w1/ExecKillers/rows.txt`, run reproduced by this seat at exit 0).

**D6 — Gate provenance.** `corpus/QUALITY.md:1701` now carries the criterion that a Gate summary must cite the lesson section it summarises (`corpus/lessons/round-82.md` §Gate), so a later report's prose cannot name a category where the lesson has a row; the frozen counter re-derives that criterion line and requires it to carry `corpus/lessons/round-82.md`, `Gate` and `round-83` — the round-82 report's prose named "the `merge/kake` package" among the Gate's rejects where the lesson has an assimilation row, which is exactly the class the criterion forbids.

## Erratum

**[r83-erratum 2026-11-04]** The round-81 report `.ufo/reports/round-81/kake.md` was rewritten in
place at fleet `7678247a3c13b1dc03ed1cb8f80d2dba603ee0ca` (parent `cb02b705`), against a report that
was already a record. `git -C /home/vgpnk/Projects/shokunin diff cb02b705 7678247a --
.ufo/reports/round-81/kake.md` removes exactly five physical lines longer than 40 characters; they
are quoted below as raw bytes, prefix `> ` added and nothing else. Each is absent from the amended
blob. The counter re-derives this set from fleet history and counts the matches in this file, so a
transcription error here shows up as `quoted<4`, not as an argument.

> · lane tip at filing `2b46f5c4db418c9a79e1990940da1a5029ff7e5b` (pushed; `ls-remote` agrees) · date 2026-11-04.

>   5/14 = 35.7 %; one seat (`ReviewRegression`, reviewer) returned empty output and is reported dead,

>   not replaced. The L1 held the planner seat (the validator refuses `planner` as a swarm role); the

>   bounded planning data-walk rode `ScoutRecon`. Round total: 15 seats.

> | C1 calibration: the round-80 routed-defect queue closes | `python3 -B .ufo/waves/round-81/c81_defect_queue.py --root . --revision <rev>` | `C1v1 revision=2e11925500dd5a739376c9108c94616243af0cd4 items=6 open=6 closed=0 met=false`, exit 1 (`controls/base-c81-defect-queue.txt`) | `C1v1 revision=2b46f5c4db418c9a79e1990940da1a5029ff7e5b items=6 open=0 closed=6 met=true`, exit 0 (`controls/after-c1-final.txt`); first measured at `e84c354e` (`controls/after-c1.txt`) | `2b46f5c4…` (final), `e84c354e…` (first carrier) |

The amendment replaced those bytes with a corrected tip line, a two-dead-seat disclosure with a
second substantive share, one landed-changes row and a narrowed claim row. Nothing else in the round
80/81 record is rewritten: the erratum is an append that points, and the original report's authority
ends where the quoted bytes end.

## Gate

**Candidate — `S456`, RFC 9111 *HTTP Caching*: entry landed, registry row pending at this writing.**
The proposed ground is the classifier's split of a changed header into `per-request`, `validator`,
`representation` and `policy`: RFC 9111 defines validators, representation metadata and the fields
that govern reuse. `ScoutSources` opened the source this round, GET-only, and retained it at
`.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt` — 84,477 bytes, sha256
`aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`, HTTP 200, no redirect,
`2026-11-04T13:29:41Z`, UTF-8 with BOM; this seat recomputed that digest and read the cited lines
itself. The doc-side carrier has landed as `corpus/knowledge/header-change-classes.md`, whose
`source:` line cites `S456`, the retained file and this digest, and whose `scope:` line already
excludes the class-name table from what the source settles. The registry row is `ScribeKnowledge`'s
production target and `grep -n 'S456' corpus/SOURCES.md` returned no match at this writing, so this
section records the candidate, its retained bytes and the reasons its anchors are chosen — **not** an
admission.

**Anchor candidates, measured in the retained bytes** (`w1/ScoutSources/quotes.tsv`; line numbers and
word counts are the scout's, and this seat re-read all four spans):

- `:583-585`, 23 words — "A "fresh" response is one whose age has not yet exceeded its freshness
  lifetime. Conversely, a "stale" response is one where it has." Raw substring, one occurrence.
- `:597-599`, 21 words — "When a response is fresh, it can be used to satisfy subsequent requests
  without contacting the origin server, thereby improving efficiency." Raw substring, one
  occurrence; `raw-checks.txt` shows the sentence collapses at the 72-column wrap and the raw
  `grep -F` of the collapsed sentence exits 1, so the span, not the sentence, is the quotable unit.
- `:468-469`, 14 words — "When presented with a request, a cache MUST NOT reuse a stored response
  unless:" Raw substring, one occurrence; the reuse precondition, not a freshness statement.
- `:838-839` with `:840-844`, 22 + 44 words — the entity tag as "another validator". Raw substrings,
  one occurrence each, and the anchor this row must *not* take (below).

All four quotes above are wrap-joined — the wrap's indentation removed and the double sentence space
collapsed. Checked, not asserted: a whitespace-normalized substring test against the retained file
passes on all four spans (word counts 14 / 23 / 21 / 48) and the retained file's digest recomputes to
the sha256 above (`w1/ScribeLesson/gate-quote-check.txt`); the strictly raw forms and the `grep -Pzo`
receipts are the scout's `raw-checks.txt`.

**Reject — the 65-word `:587-592` freshness-lifetime paragraph as the admission quote.** It is a raw
substring and the fuller definition, but 65 words is past the lane's ≤ 25-word admission cap, and it
restates what `:583-585` already fixes; admitting it would either break the cap or invite a
truncation that no longer matches the bytes.

**Reject — `:838-839` / `:840-844` (entity tag as "another validator") as an anchor for this row.**
`S455` already owns validator semantics at `corpus/SOURCES.md:202` (§8.8.1 plus §8.8.3 of RFC 9110,
admitted at round 82). The classifier's `validator` class is a naming decision over two field names,
not a claim about validator strength, and re-anchoring it here would count one source twice.

**Reject — RFC 9111's *Invalidating Stored Responses* and *Common Cache-Control Directives* sections
as anchors.** The first governs invalidation after an unsafe method, the second governs directive
semantics; `scripts/header_change_class.py` compares two GET captures, evaluates no directive and
models no store, so either anchor would claim a rule the code does not implement. Cited by title, not
by line number, because neither section is part of the proposed quote set.

**Owed to the closure.** This Gate is author-side and decides nothing. The non-author spot-check owes
the independent re-open of the retained RFC 9111 bytes, the line-level quote check for whatever row is
admitted, and a decision on whether the three rejects hold — the load the round-82 closure carried
for `S455` at `corpus/lessons/round-82-verifier-spotcheck.md` §4.

## Mistakes

Rows are `class · evidence pointer · captured-by · fix`; each fix names the check that can fail.

- **mutant-harness-path** · `corpus/lessons/round-82.md:289` — the first C2 mutant run scored every
  mutant red for the wrong reason: the counter's selftest resolves the tool as
  `Path(__file__).resolve().parents[3] / TOOL`, the mutant copies sat three levels below the scratch
  root, so the tool was absent and every fixture failed on that rather than on the mutation ·
  **captured-by:** no seat; disclosed by the L1 in round 82 after the readings were discarded ·
  **fix:** score a mutant only in a tree at the counter's own depth, with the tool copied under
  `scripts/`, and read the pristine counter on the same fixture before trusting a kill. Shown able to
  fail in this seat's scratch, on the same frozen file: the unmodified `c83_drift_class.py` copied to
  `<scratch>/shallow/.ufo/waves/round-83/` exits 1 printing `FAIL no tool at
  …/shallow/scripts/header_change_class.py` before a single fixture runs; the same bytes in the fixed
  layout print `selftest: 9/9 passed`, exit 0; and the same file with one real conjunct dropped
  (`tool_offline`) prints `FAIL tool-network-import — met=True expect=False` with `selftest: 8/9
  passed`, exit 1 — so the layout decides whether a mutation is visible at all
  (`.ufo/waves/round-83/w1/ScribeLesson/harness-path-repro.txt`, three runs, exits 1/0/1).
- **units-drift** · the round-82 report's §Wave printed `(4,871 B)`, `(7,888 B)`, `(6,392 B)`,
  `(6,664 B)`, `(3,811 B)` where the committed `w1-accounting.json` recorded UTF-8 bytes `4,899`,
  `7,902`, `6,402`, `6,669`, `3,813` (`len(output.encode("utf-8"))`) ·
  **captured-by:** the non-author round-82 closure, `corpus/lessons/round-82-verifier-spotcheck.md`
  §6 item 2 · **fix:** the accounting tool emits `bytes_basis: "utf-8"` and per-seat `output_bytes`,
  and the counter re-derives every settled seat's length from `w1-results.json`; it is shown able to
  fail by the `d2-byte-count-drift` fixture in `controls/c83-selftest-c1.txt`, which mutates one
  recorded length by one byte and turns `open=0` into `open=1`.
- **prose-provenance** · the round-82 report's Sources & frontier listed "the `merge/kake` package"
  among the Gate's rejects while `corpus/lessons/round-82.md` §Gate's rejects were two S455 anchor
  spans and the package was an assimilation non-adoption ·
  **captured-by:** the non-author round-82 closure, `corpus/lessons/round-82-verifier-spotcheck.md`
  §6 item 6 · **fix:** the standing `corpus/QUALITY.md` criterion that a Gate summary cites the
  lesson section it summarises (this round's D6), shown able to fail by the `d6-missing-criterion`
  fixture, which deletes the criterion line and turns `open=0` into `open=1`.

## Dead seats

Filled by the L1 after WAVE-DONE from `.ufo/waves/round-83/w1-results.json`. This seat writes no seat
result and no byte count; a seat that returned empty output is reported dead, not replaced (the
round-80 correction), and settlement is recorded rather than relabelled.

| Seat | Role | State | Evidence |
|---|---|---|---|
| — | — | no dead seat | all 14 `w1-results.json` rows carry non-empty output; `w1-accounting.json` records `empty_output` as empty |

Empty-output seats, if any, are also named in the round report's §Wave and carry the frozen
attack-share consequence for C1's D1 state conjunct.

## Wave

Filled by the L1 after WAVE-DONE; one row per results row, and the byte column is the UTF-8
`output_bytes` from `.ufo/waves/round-83/w1-accounting.json`, never a character count (this round's
D2). Requested shape: 14 seats, attack 5/14 requested; settled shape is whatever the results file
measures.

| Seat | Role | Output (UTF-8 bytes) | Report |
|---|---|---|---|
| `CriticClaims` | `critic` | 7,799 | `w1/CriticClaims.md` |
| `ExecAccounting` | `executor` | 3,874 | `w1/ExecAccounting.md` |
| `ExecControlPair` | `executor` | 4,709 | `w1/ExecControlPair.md` |
| `ExecInstrument` | `executor` | 3,581 | `w1/ExecInstrument.md` |
| `ExecKillers` | `executor` | 5,387 | `w1/ExecKillers.md` |
| `MutC` | `mutation-tester` | 8,614 | `w1/MutC.md` |
| `MutKillers` | `mutation-tester` | 3,730 | `w1/MutKillers.md` |
| `ReviewC1` | `reviewer` | 5,379 | `w1/ReviewC1.md` |
| `ReviewC2` | `reviewer` | 9,032 | `w1/ReviewC2.md` |
| `ScoutRecon` | `scout` | 5,736 | `w1/ScoutRecon.md` |
| `ScoutSources` | `scout` | 10,367 | `w1/ScoutSources.md` |
| `ScribeKnowledge` | `scribe` | 5,405 | `w1/ScribeKnowledge.md` |
| `ScribeLesson` | `scribe` | 4,370 | `w1/ScribeLesson.md` |
| `ScribeRecord` | `scribe` | 3,771 | `w1/ScribeRecord.md` |
| **total** | | **81,754** | 14 settled of 14; empty `-` |

Settlement: all 14 seats returned non-empty output; the smallest output is 3,581 bytes and the frozen substantive floor (200 bytes) is cleared by every seat. Requested attack share 5/14 = 35.7 %; settled attack share 5/14 = 35.7 % by the round-81 frozen rule (a row with non-empty output is settled), and 5/14 = 35.7 % on deliverables only — the round-82 routed defect D1 asked for settled adversarial seats and this wave records five, with no dead seat and no replacement.

## Verdict

C1's row file is the six rows of `## Corrections`; the claim is scored by
`c83_defect_queue.py --root . --revision <rev>` at the after-state, not by anything written here. C2
is scored by `c83_drift_class.py` under the same rule. Both rows are author-side and provisional
until the non-author closure re-derives them from committed bytes.
