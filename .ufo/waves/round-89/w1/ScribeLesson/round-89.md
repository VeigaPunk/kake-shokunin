# Round 89 — routed round-88 defects (C1) and a Vary cache-key constructor the counter admits by table (C2)

Seat: `ScribeLesson` (scribe, leaf member, no subagent dispatch). Lane root
`/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE). Draft for L1 to integrate;
nothing here is an outside admission. Base `76225160d0dff8d2042fbcd037bd08b0971d5e07`.
Freeze commit `08ab46a130a6355a7b19e2bfa83ffb7e116db803` (first add of
`c89_key.py`). Dispatch marker `2e700b9a94a3c8ce3c0d6b1cc9e84e7b17eee683`
(first add of `w1.ready`). Freeze v2 `46a43e94` (`c89_key.py` amended) landed
after that dispatch. Lane HEAD this seat measured: `acc69ba59af9ddff84a704331087b9147cc0aa1b`.
Candidate `scripts/cache_key.py` at `9784ad54c6e2089eed93a02dd44e4981d5074cc4`.

Claims, as frozen in `.ufo/waves/round-89/freeze.md`:

- **C1 calibration (lowest owned axis, 2 HOLD).** Six round-88 defects R88-A…F
  close, re-derived by `c89_defect_queue.py`. Predicate `open=0 closed=6 met=true`.
- **C2 freshness (10 HOLD, bounded capability).** Conservative Vary-nominated
  cache-key construction, scored by `c89_key.py`. Predicate
  `frozen=16/16 props=200/200 refuse=9/9 controls=5/5 met=true`.

## Gate

Sources opened this round. Each was one unauthenticated GET from this seat with
no cookies, no Authorization header and no query token. Bodies and response
headers are retained under `.ufo/waves/round-89/w1/ScribeLesson/receipts/`.

| URL | HTTP | bytes | sha256 | accessed (UTC, response Date) |
|---|---|---|---|---|
| `https://www.rfc-editor.org/rfc/rfc9111.txt` | 200 | 84 477 | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` | 2026-11-04T21:22:57Z |
| `https://www.rfc-editor.org/rfc/rfc9110.txt` | 200 | 502 941 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | 2026-11-04T21:23:41Z |

Both digests equal the retained copies committed for round 88
(`.ufo/waves/round-88/w1/ScribeLesson/receipts/rfc9111.txt`, `rfc9110.txt`),
compared by `git show HEAD:<path> | sha256sum`. Each response carried a
`set-cookie` header; it was not sent back. The round-88 retained copies were
compared by digest only and are not counted as sources opened this round.

| Candidate | Decision | URL, access date, located quote (≤25 words), line range | Reason and flip condition |
|---|---|---|---|
| RFC 9111 §4.1 section "Calculating Cache Keys with the Vary Header Field" as the ground for the key-form row (construction half only) | **admit**, tier A, scope-limited | `rfc9111.txt`, 2026-11-04T21:22:57Z, lines 530–532: "the cache MUST NOT use that stored response without revalidation unless all the presented request header fields nominated by that Vary field value match" (24 words); section title at line 526 | The section is titled as cache-key calculation and states which nominated fields must participate in matching, which is what the constructor's key carries. The row supports which fields enter the key only. Storage, freshness, revalidation and serving stay out. Flip: a §4.1 revision that moves the key definition out of the section, or a constructor used to decide reuse, which requires re-deriving the scope rather than widening it. |
| RFC 9110 §5.6.2 "Tokens" as the ground for the member and name alphabet | **admit**, tier A, scope-limited | `rfc9110.txt`, 2026-11-04T21:23:41Z, lines 1730–1731: "Tokens are short textual identifiers that do not include whitespace or delimiters." (12 words) | The sentence grounds the "no whitespace, no delimiters" half of the member rule. The character set itself is the tchar production, which this quote does not state, so the constructor's TCHARS string is cited to the production, not to this sentence. Flip: an RFC revision of the token production, or a constructor that accepts a non-token member. |
| "The counter's met=true shows the constructor implements RFC 9111 §4.1" | **reject** (proposition) | same `rfc9111.txt` lines 530–532 as above, read as a precondition on reuse | The sentence states a reuse condition, not a key procedure. The counter's escaping, sorting, absent marker and refusal list are the lane's declared adapter conventions (`c2-contract.md`), and the counter reaches `met=true` on a table over its own committed seed population (Mistakes, row 1). A pass shows agreement with the lane's counter, not with the RFC. Flip: a bounded, RFC-specified procedure whose counter a table cannot reach. |
| "Refusing `Vary: a,` (trailing comma) is an RFC requirement" | **reject** (proposition) | `rfc9110.txt`, 2026-11-04T21:23:41Z, lines 1695–1697: "A recipient MUST parse and ignore a reasonable number of empty list elements" (13 words) | The RFC says to parse and ignore empty list elements. A zero-member remainder nominates nothing, so refusal is an adapter convention, declared as such in `c2-contract.md`. Flip: an RFC sentence that requires refusal of an empty member. |

## Mistakes

Mined from this round's measurements and from the round-88 spot-check. A fix
counts only with a witness that reddens without it. Where no fix is applied in
this draft, the row says so and names the witness that must turn red once one is.

| Class | Evidence pointer | Captured-by | Fix | Witness |
|---|---|---|---|---|
| C2 counter admits a table over its own committed seed population (met=true) | `.ufo/waves/round-89/w1/ScribeLesson/receipts/probes-c2.json` key `E_table_over_committed_seed_population` (421 entries, 16/200/9, guard null); `probes/probe_all.py` case E; `c89_key.py` `SEED = 89089` and `guard()` | this seat, probe E; consistent with the lane's own wave review (`ReviewCounterC2`, `CriticClaims`) | Not applied in this draft. Routed: population the candidate cannot read, such as a keyed digest revealed at scoring | Not yet reddening: probe E prints met=true at the frozen counter. The witness after a fix is `probe_all.py` case E scoring below 200/200 props |
| C2 counter's textual guard accepts a runtime-built import of the committed reference | `receipts/probes-c2.json` key `D_runtime_built_reference_import` (16/200/9, guard null); `probes/probe_all.py` case D builds the module path at run time | this seat, probe D | Not applied. Routed with row 1 | Not yet reddening: case D prints 16/200/9 with guard null. After a fix, case D must report a guard refusal or below-target counts |
| Escape clause with no witness: omitting the `%1D` escape still scores full | `probes/probe_1d.py` output `(16, 200, 9)`; `c2-contract.md` §4 names `%1D`; no frozen case and no property input contains U+001D (both checked in the probe) | this seat, probe 1d | Not applied. Routed to a frozen case that carries U+001D | Not yet reddening: the no-`%1D` mutant scores 16/200/9. After a frozen case is added, that mutant must score below 16/16 |
| URI not escaped: two distinct requests collide, and the counter does not see it | `receipts/probes-c2.json` key `collision_demo`: the `uri` escape removed gives the same key `https://e.test/a\u001fb\u001ex` for requests R1 (header `b`, Vary `b`) and R2 (URI carrying US and RS, empty Vary); canonical keys differ (`…%1Fb%1Ex`); the mutant still scores 16/200/9 | this seat, probe B and the collision demo | Not applied. Routed: a frozen case where a URI contains `%` or a separator | Not yet reddening: the mutant scores 16/200/9 with a live collision. After a case is added, the mutant must score below target |
| Counter item E blind to a post-dispatch amendment (the R88-E class again) | `git log -- .ufo/waves/round-89/c89_key.py` shows `46a43e94` at 2026-11-04 18:16:18 -0300, after dispatch `2e700b9a` at 18:13:04 -0300; `c89_defect_queue.py` at `acc69ba5` prints `E-freeze-before-dispatch: []` | this seat (verified by two commit times and the item's output); lane RC-2 | Not applied. A claim decision for L1 and round 90 | Not yet reddening: item E is green on the amended counter. Red-before witness that exists: the counter's own selftest "E fails when dispatch is committed first", which does not cover an edit after dispatch |
| Round-88 summary stale: report says "one admit and three rejects" while the committed `## Gate` has two and two | `.ufo/reports/round-88/kake.md` Gate summary; `corpus/lessons/round-88-verifier-spotcheck.md` R88-B; tagged correction `[r89-correction 2026-11-04]` at `corpus/lessons/round-88.md` lines 334–337 | round-88 outside spot-check (hyaku) | Appended tagged correction tail (append-only; the filed table is untouched); C1 item B reads the parsed table | Witness that reddens: the counter's selftest mutant "Gate table edit reopens B" passes in `receipts/c1-selftest-rerun.txt` (12/12, exit 0) |
| Round-88 re-run claim with no committed receipt ("re-run at `edcb2980`") | `.ufo/reports/round-88/kake.md:103`; no file in lane git names `edcb2980`; this seat's uncommitted re-run prints met=true at `edcb2980` (`receipts/r88-c1-at-edcb2980.txt`, `receipts/r88-c2-at-edcb2980.txt`) | round-88 outside spot-check R88-C | Marker `r88-c-rerun` in this draft is a placeholder for L1: commit the receipt and name it, or retract | Witness that reddens: selftest mutant "r88-c-rerun pointing at a missing receipt reopens C" passes in `receipts/c1-selftest-rerun.txt` |
| Stale selftest number left unchanged in filed bytes (R88-A), and the append-only rule is in conflict with item A | at `acc69ba5`, `c89_defect_queue.py` prints `A-selftest-number` naming `SCORECARD.md:5469`, `SCORECARD.md:5488` and `corpus/lessons/round-88.md:265` with no `[r89-correction` tag | round-88 outside spot-check R88-A; this seat's C1 run at `acc69ba5` (`receipts/c1-at-head-acc69ba5.txt`) | Not applied to filed bytes. Routed: item A should accept an appended tagged tail that names the stale line | Witness that reddens: `receipts/c1-at-head-acc69ba5.txt` prints `open=1 closed=5 met=false` with item A as the only open item |

## Claims and what this seat measured

**C1 — calibration, six routed round-88 defects.** Counter
`.ufo/waves/round-89/c89_defect_queue.py`, run by this seat at four revisions:

| Revision | Output (verbatim) | Exit | Receipt |
|---|---|---|---|
| `76225160` (base) | `items=6 open=5 closed=1 met=false` | 1 | `receipts/base-c1-rerun.txt` |
| `2e700b9a` (dispatch) | `items=6 open=5 closed=1 met=false` | 1 | `receipts/head-c1.txt` |
| `2177058662` | `items=6 open=5 closed=1 met=false` | 1 | `receipts/c1-at-carrier-21770586.txt` |
| `acc69ba5` (HEAD this seat) | `items=6 open=1 closed=5 met=false` | 1 | `receipts/c1-at-head-acc69ba5.txt` |

- The predicate's do-nothing control is stated as `open=6 closed=0 met=false` at
  base. **This seat did not reproduce that line.** At base the counter prints
  `open=5`, because item E reads the checked-out HEAD, not `--revision`, and
  HEAD already contains the freeze and dispatch commits (Limits). The committed
  receipt `controls/base-c1.txt` is therefore not a pure base measurement.
- At `acc69ba5` the items B, C, D, E and F are closed by the markers below. Item A
  is open on three stale `22/22` lines (Mistakes, row 8).
- Counter selftest, this seat: `selftest: 12/12 passed`, exit 0
  (`receipts/c1-selftest-rerun.txt`).
- Round-88 claim re-derived: `c88_defect_queue.py` at `edcb2980` prints
  `C1v1 revision=edcb2980… items=3 open=0 closed=3 met=true`, exit 0
  (`receipts/r88-c1-at-edcb2980.txt`). This reproduces the number; it does not
  make the round-88 claim admissible, which needs a committed receipt.
- Round-88 `## Gate`, parsed by this seat at base and at HEAD: two `**admit**`
  rows and two `**reject**` rows (`admits=2 rejects=2` in both).
- `controls-count`: recount `git ls-tree -r --name-only <rev> | grep -c '/controls/'`
  gives 1590 at `76225160`, 1604 at `2177058662`, 1609 at `acc69ba5`. The marker
  pins `2177058662`, the revision L1 chose and this seat re-counted.

**C2 — freshness, conservative Vary-nominated cache-key construction.** Counter
`.ufo/waves/round-89/c89_key.py`, candidate `scripts/cache_key.py`.

- Base `76225160`, candidate absent: `frozen=0/16 props=0/200 refuse=0/9
  controls=5/5 met=false`, exit 1 (`receipts/base-c2-rerun-worktree-counter.txt`).
  Matches `controls/base-c2.txt`.
- Integrated candidate `9784ad54`, scored by the frozen v1 counter and by the
  committed v2 counter: `frozen=16/16 props=200/200 refuse=9/9 controls=5/5
  met=true`, exit 0 under both (`receipts/c2-v1-counter-vs-integrated-candidate.txt`,
  `receipts/c2-v2-counter-vs-integrated-candidate.txt`). The v1-to-v2 diff
  (`git diff 08ab46a1 HEAD -- .ufo/waves/round-89/c89_key.py`) narrows the guard's
  `FORBIDDEN` tuple, adds an `open(` check on `.ufo` paths, and edits the guard
  docstring. The `ctl-table.py` refusal reason moves from `'.ufo/waves'` to
  `'c2-cases'` as a result. The candidate's score does not move.
- Counter selftest, this seat: `selftest: 43/43 passed`, exit 0, run from the
  lane with `controls/` beside the counter (`receipts/c2-selftest-rerun.txt`).
  Run with the counter file alone, it prints `selftest: 40/43` and exits 1
  (`receipts/c2-selftest-counter-alone-no-controls.txt`), because its controls
  are resolved from a sibling directory.
- Integrated candidate, probe A (`receipts/probes-c2.json`): 16/200/9, no failures.
- Shortcut and mutant probes (all in `probes/probe_all.py`, scored by the frozen
  v2 counter's own `score_candidate` and `guard`):

  | Case | Construction | Guard | frozen/props/refuse | Counter verdict |
  |---|---|---|---|---|
  | B | URI not escaped | null | 16/200/9 | met=true (should refuse by §4) |
  | C | trims SP, HTAB, LF, VT, FF, CR (contract: SP and HTAB) | null | 16/200/9 | met=true (should fail) |
  | D | runtime-built import of `c89_key.py` | null | 16/200/9 | met=true (shortcut) |
  | E | exact table over the committed seed population (421 entries) | null | 16/200/9 | met=true (shortcut) |

  Case 1d (`probes/probe_1d.py`): omitting the `%1D` escape gives 16/200/9.
- Collision (`collision_demo`): under case B, two requests with different
  logical inputs map to one key. The canonical constructor does not.

## Limits

- **The counter's shortcut guard is textual and is weak.** It refuses the literal
  names `c89_key`, `c89_defect_queue` and `c2-cases`, and any `open(` of a
  `.ufo` path. Case D reaches met=true through a path built at run time, and case
  E reaches met=true with a table that contains no such token. The guard is
  disclosed as textual in `c89_key.py`; the disclosure is accurate and the defect
  is real.
- **The property population's seed is a committed constant.** `SEED = 89089` is
  in `c89_key.py`, and the population is a pure function of the committed bytes.
  The freeze text says the population is "generated at scoring time from the seed
  printed in the receipt". That is true of the code path, but the seed is public,
  so a table built from it (case E, 421 entries) reaches 200/200 properties and
  met=true. The population is reproducible from the repository; it is not
  unreachable.
- **The counter does not cover several contract clauses.** Its frozen cases and
  property classes leave the `%1D` escape (case 1d), the URI escape (case B), and
  the whitespace set (case C) without a witness. The lane's wave review reports
  seven such clauses in total (`ExecControls`, `ReviewCounterC2`).
- **C1 item E is not revision-pinned and does not see amendments after dispatch.**
  It reads HEAD, so the base do-nothing control does not reproduce (Claims, C1),
  and freeze v2 `46a43e94` landed after dispatch `2e700b9a` (Mistakes, row 5).
- **Item A cannot accept an appended correction.** At `acc69ba5` it stays open on
  three stale lines that the append-only rule forbids editing in place (Mistakes, row 8).
- **No storability, freshness, revalidation, reuse or serving claim is made.**
  The constructor decides key construction for a supplied request header map and
  `Vary` value. It does not decide what any server, cache or browser stores,
  revalidates, reuses or serves, and no live surface is asserted clean. The
  C2 freshness claim is bounded to key construction and is not a freshness result.
- Candidate branch coverage, mutation coverage and the real-capture trial are not
  re-measured by this seat; they are the lane's other seats' work and are not
  cited as this seat's evidence.

## Markers

Read by `.ufo/waves/round-89/c89_defect_queue.py` (C1 items B, C and D). Values
verified by this seat except where marked.

gate-sample: admits=2 rejects=2
r88-gate-summary-correction: admits=2 rejects=2
r88-c-rerun: PLACEHOLDER L1 must fill: receipt=<committed path> or retracted
controls-count: 1604@2177058662d8778f1d1a685613f57deccb51ef01
