# Round 89 — routed round-88 defects and a conservative cache-key constructor

Lane: kake. Base `76225160d0dff8d2042fbcd037bd08b0971d5e07`. Freeze commit
`08ab46a130a6355a7b19e2bfa83ffb7e116db803` (both counters, the contract, the
frozen cases and the base controls). Dispatch evidence `2e700b9a` (wave-1 spec,
validated payload, ready marker). Counter amendment `46a43e94` (freeze v2),
after dispatch and disclosed below. Candidate `9784ad54`. Measurement base for
the controls count: `2177058662d8778f1d1a685613f57deccb51ef01`.

Claims, as frozen in `.ufo/waves/round-89/freeze.md`:

- **C1 calibration (lowest owned axis, 2 HOLD).** Six defects the round-88
  outside spot-check routed (R88-A…F). Predicate: `open=0 closed=6 met=true`.
  Measured `open=5 closed=1 met=false` at `f62e7954`; the markers this lesson
  carries close B, C, D and F and leave A open (see Mistakes, row 5).
- **C2 freshness (10 HOLD, bounded capability).** Conservative Vary-nominated
  cache-key construction. Predicate: `frozen=16/16 props=200/200 refuse=9/9
  controls=5/5 met=true`. Measured `met=true` at `9784ad54` under the frozen v1
  counter (`controls/c2-carrier-frozen-v1.txt`) and under the committed v2
  counter (`controls/c2-carrier-v2.txt`). Admission is withheld: the instrument
  also admits seven non-conforming candidates (Mistakes, row 4).

## Gate

Sources opened this round (one unauthenticated GET each; no cookies, no
credentials, no query tokens):

| URL | HTTP | bytes | sha256 | accessed (UTC) |
|---|---|---|---|---|
| `https://www.rfc-editor.org/rfc/rfc9111.txt` | 200 | 84 477 | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` | 2026-11-04T21:16:51Z |
| `https://www.rfc-editor.org/rfc/rfc9110.txt` | 200 | 502 941 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | 2026-11-04T21:16:52Z |

Retained at `.ufo/waves/round-89/L1/src/rfc9111.txt` and `…/rfc9110.txt`. The
RFC 9111 digest equals the round-87 and round-88 retained copies of the same URL.

Decision table for this round's source-backed candidates (the `## Gate` of the
round-88 lesson is re-read by C1 item B; this table is this round's own):

| Candidate | Decision | URL, access date, located quote (≤25 words), line | Reason and flip |
|---|---|---|---|
| RFC 9111 §4.1 section title and reuse condition as the ground of the key-construction row (S464) | **admit**, tier A, scope-limited | `rfc9111.txt`, 2026-11-04, line 530: "the cache MUST NOT use that stored response without revalidation unless all the presented request header fields nominated by that Vary field value match" (24 words); title at line 526 | The section is titled as cache-key calculation and conditions reuse on the nominated fields. The row supports the construction half only. Flip: a §4.1 revision that moves the key definition out of the section, or a reader that starts deciding storage or reuse. |
| RFC 9110 §5.6.2 token alphabet for Vary members and field names (S465) | **admit**, tier A, scope-limited | `rfc9110.txt`, 2026-11-04, line 1730: "Tokens are short textual identifiers that do not include whitespace or delimiters." (12 words) | Grounds the member and name alphabet the constructor refuses outside. Flip: an RFC revision of the token production, or a constructor that accepts a non-token member. |
| "the C2 pass shows the reader implements RFC 9111 §4.1" | **reject** (proposition) | same line 530 read as the reuse precondition | A counter pass shows agreement with a declared canonical form, not with the RFC. The contract's escaping, sort and absent marker are adapter conventions, declared as such in `c2-contract.md`. Flip: a separately bounded procedure that the RFC itself specifies byte-for-byte. |
| "refusing `Vary: a,` is an RFC requirement" | **reject** (proposition) | `rfc9110.txt`, 2026-11-04, line 1696: "A recipient MUST parse and ignore a reasonable number of empty list elements" (13 words) | The RFC says to ignore empty elements, so a zero-member remainder nominates nothing. Refusal is this lane's convention, chosen because a silent empty member set would collapse every request for a URI onto one key. Flip: an RFC sentence that requires refusal. |

Registry: `corpus/SOURCES.md` gains S464 and S465 (201 → 203 rows, 0 existing
rows edited). Knowledge: `corpus/knowledge/cache-key-construction.md` cites
both. The row shapes were gated in scratch on a full mirror of the lane before
the append (`validate --file` exit 0 with only the expected W04 duplicate-URL
notes; the census of the live lane is exit 0 after the append).

## Mistakes

Mined from this round's own work and from the round-88 spot-check. A fix counts
only with a witness that reddens without it.

| Class | Evidence pointer | Captured-by | Fix | Witness |
|---|---|---|---|---|
| Filed bytes edited in place: I changed round-88 SCORECARD cells (`22/22` → `35/35`) and round-88 lesson line 265 before revert | `git diff` in the lane before revert; ExecDefects finding 5; `corpus/QUALITY.md` "Append-only tails" row | none at edit time; the QUALITY row existed and I did not consult it before editing | Reverted both files to base (`git show 76225160:<path>`); corrections are appended tails carrying `[r89-correction …]` (`corpus/lessons/round-88.md`, 10 appended lines) | `git diff --stat -- SCORECARD.md corpus/lessons/round-88.md` at `f62e7954` shows no SCORECARD change and only insertions in the lesson; red-before was the in-place diff |
| Counter amended after dispatch: freeze v2 `46a43e94` changed `c89_key.py` after `2e700b9a` dispatch | `git log -- .ufo/waves/round-89/c89_key.py`; ExecKey finding "counter drift" | item E of C1 checks only the first add of the counter, so it passes | Disclosed here and in the report. The verdict was re-measured under the frozen v1 counter extracted from `08ab46a1`; both give `met=true` for the integrated candidate (`controls/c2-carrier-frozen-v1.txt`, `controls/c2-carrier-v2.txt`), so the amendment does not decide C2 | Witness that the amendment is not verdict-deciding: the integrated candidate `9784ad54` meets the frozen v1 counter exit 0 (`controls/c2-carrier-frozen-v1.txt`); the v2 change only removed the false positive that refused the L1 reference candidate |
| Shortcut guard false positive: a correct candidate that names a contract path in its docstring is refused | `ExecKey.md` finding 1; my first L1 candidate (`.ufo/waves/round-89/w1/L1/cache_key.py`, guard reason `'.ufo/waves'`) | none — the frozen counter's selftest has no positive case with a path in a comment | Narrowed the guard to `c89_key`, `c89_defect_queue`, `c2-cases` plus an `open(` check on `.ufo` (freeze v2) | Red: the v1 guard rejects the L1 reference candidate (commit `dbe09859`, scratch clone) on the `.ufo/waves` docstring token. Green: the v2 guard accepts it, and the controls `ctl-oracle-import` and `ctl-table` stay rejected (`controls/c2-carrier-v2.txt`) |
| C2 counter admits non-conforming candidates: seven contract clauses (duplicate member refusal, URI escaping, name escaping, CR-only refusal, missing `request_headers`, malformed JSON, case-sensitive member order) have no frozen case or property class | `.ufo/waves/round-89/w1/ExecControls.md` (seven `met=true` stubs; receipts `w1/ExecControls/scoring-receipt.txt`, `scoring-detail.txt`) | none — the frozen cases and property classes were chosen by hand and did not enumerate every clause | Routed to round 90 (R89-2): add one frozen or refusal item per clause, as ExecControls suggests. Not applied this round, because the counter is frozen and the claim's rule must not change after scoring | Red: the seven stubs score `met=true` under the frozen counter; the routed fix must make each of them `met=false` in a re-run before C2 can be admitted |
| Item A demands an in-line tag on filed bytes: a stale selftest count that the append-only rule forbids touching | `c89_defect_queue.py` item A stale-line window; base receipt `controls/base-c1.txt`; `corpus/QUALITY.md` "Append-only tails" | none — the counter was written without the append-only rule in view | Left open; routed to round 90 (R89-1): item A should accept an appended `[r89-correction]` tail naming the stale line numbers. Not applied this round | Red: at `f62e7954` item A reports the two round-88 SCORECARD lines and the lesson line 265 as stale, with no tag, while the tail correction exists |
| Receipt pointer short form invisible to C item C: round-88 SCORECARD names `controls/integrated-selftest.txt` (singular, absent) | `ExecDefects.md` finding 1; `SCORECARD.md` round-88 rows | none — `CTRL_RE` requires the full `.ufo/waves/round-88/controls/` prefix | Routed to round 90 (R89-3) | Red: the short form resolves to no file at base and the counter does not report it |

## Claims and what this round measured

**C1 — calibration, six routed round-88 defects.** Counter
`.ufo/waves/round-89/c89_defect_queue.py` (selftest 12/12,
`controls/c1-selftest.txt`). Base `76225160`: `open=6 closed=0 met=false`, exit 1
(`controls/base-c1.txt`). Carrier `f62e7954`: `open=5 closed=1 met=false`, exit 1
(item A open; B, C, D, E, F closed). Items closed, with the marker that closes
each:

- B `gate-sample: admits=2 rejects=2` and `r88-gate-summary-correction:
  admits=2 rejects=2`. The round-88 `## Gate` table parses 2 admit and 2 reject
  rows (lines 33–36 of `corpus/lessons/round-88.md` at base).
- C `r88-c-rerun: retracted`. The round-88 claim "re-run at `edcb2980`" had no
  committed receipt. Retracted here. The carrier re-run is committed as
  `controls/r88-c1-rerun-at-55d67f15.txt` (`items=3 open=0 closed=3 met=true`,
  exit 0), which is evidence of a different revision and not a retraction of
  the round-88 instrument.
- D `controls-count: 1604@2177058662d8778f1d1a685613f57deccb51ef01` (recount
  `git ls-tree -r --name-only <rev> | grep -c '/controls/'`).
- E no content edit. The item passes on ancestry and committer times for the
  first adds, and it does not see the post-dispatch amendment (Mistakes, row 2).
- F `## Mistakes` above with the five columns; the round-88 `## L1 mistakes`
  pointer tagged in `corpus/lessons/round-88.md` line 329.
- A `integrated-selftest: 35/35` in the round-89 SCORECARD section. The round-88
  SCORECARD rows and lesson line 265 still state the superseded count, and the
  append-only tails do not tag those lines in place: item A stays open
  (Mistakes, row 5). The tool prints `selftest: 35/35 passed` at base and at
  the carrier.

**C2 — freshness, conservative Vary-nominated cache-key construction.** Candidate
`scripts/cache_key.py` (`9784ad54`; 132 lines; stdlib; reads one JSON object on
stdin; writes `{"key": …}` or refuses `invalid_input: …` with exit 1). The
candidate is the ExecKey seat's final bytes, integrated unchanged. Counter
results:

- frozen v1 (`08ab46a1`, extracted to a scratch tree):
  `frozen=16/16 props=200/200 refuse=9/9 controls=5/5 met=true`, exit 0
  (`controls/c2-carrier-frozen-v1.txt`).
- committed v2 (`46a43e94`): the same line, exit 0 (`controls/c2-carrier-v2.txt`).
- base `76225160`: `candidate absent`, `frozen=0/16 props=0/200 refuse=0/9
  controls=5/5 met=false`, exit 1 (`controls/base-c2.txt`).

The counter's seven false greens (Mistakes, row 4) mean the `met=true` result
does not establish conformance to the whole contract. The round does not admit
it.

**Real-data trial (ExecTrial).** Six recorded cases (R1–R6) from the round-61 and
round-81 captures; the round-23 captures carry no response headers. Recorded
`vary` values (`Accept-Encoding`, `Accept-Encoding, Origin`) map to keys; a
repo-wide scan of `response.json` and `fetch.json` found no `*` wildcard, so the
refusal path was exercised only by the frozen cases. The trial establishes key
construction over recorded header lines. It does not show what any server or
cache stores (`w1/ExecTrial.md`, `w1/ExecTrial/`).

**Shortcut stubs (ExecControls).** Fifteen stubs, one defect each: the five
mandated semantic shortcuts all fail on their mapped property class; seven
non-conforming stubs reach `met=true` (Mistakes, row 4).

## Considerthese and assimilation

- `considerthese/2026-10-26.md` proposal 5 (historical-gate list) is already
  adopted: `corpus/knowledge/gate-status-ledger.md:7` names it. Proposal 2
  (receipt-rewrite watch) was adopted in round 88. No considerthese proposal is
  taken this round; proposals 1 and 3 are not mined.
- `merge/kake/` collides on eight ids (S312, S329, S367, S372, S373, S374, S390,
  S409) at this round's base; the collision list and the id check are at
  `.ufo/waves/round-89/assimilation/` (`reg-ids`, `staged-ids`, `collisions`).
  Nothing is adopted from the package this round. The campaign package is not a
  source of this round's knowledge.

## Limits

- The C2 counter's textual shortcut guard is not a sandbox. A candidate that
  imports the reference through a runtime-built path, reads a file by another
  means, or re-implements the reference would not be refused by the guard.
- The seven false greens above are counter defects. This round did not repair
  them: the frozen counter cannot change after its own scoring in this round.
- Item A is open for the reason in Mistakes row 5. The round is not admitted.
- No storability, freshness, revalidation, reuse or serving claim is made, and
  no live surface is asserted clean.
