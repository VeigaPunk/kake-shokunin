# Round 62 — w1 trend verdicts (ScribeTrendVerdicts)

Advisory scribe, leaf seat (no dispatch). Assignment: derive **possible**
expansion, quality and discernment trends from the frozen task and the
baseline only; separate evidence still owed from verdicts; assert no
after-state. Claim, counter, criteria and scores were not altered. Nothing was
written outside this report path; lane Git/jj/index, fleet repo, sibling repos,
source trees and operator config were not touched.

Owner of the frozen C1 claim is the L1/executor path, not this seat. Every
statement below is either a measured baseline fact, a verbatim inherited
record, or an explicitly marked possible direction.

## 1. Freeze and baseline verification

All commands run read-only from the lane root
`/home/vgpnk/Projects/shokunin/kake-shokunin`.

| Check | Command | Output |
|---|---|---|
| lane HEAD | `git rev-parse HEAD` | `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13` |
| worktree state before reading | `git status --porcelain` | `?? .ufo/waves/round-62/` (only line) |
| counter digest | `sha256sum .ufo/waves/round-62/c62_calibration.py` | `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d  .ufo/waves/round-62/c62_calibration.py` |
| base control at base revision | `python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13` | `revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false`, `exit=1` |
| counter committed at base? | `git cat-file -e c341a7a:.ufo/waves/round-62/c62_calibration.py` | `fatal: path '.ufo/waves/round-62/c62_calibration.py' exists on disk, but not in 'c341a7a'`, exit 128 |
| wave dir tracked at base? | `git ls-files .ufo/waves/round-62/` | `0` |
| r61 retained body committed at base? | `git cat-file -e c341a7a:.ufo/waves/round-61/sources/S432.html` | exit `0` |

The base-control line reproduces the pre-wave receipt quoted in the lane
prompt exactly (`unresolved=1 quote_correction=0 criterion=0 lesson_gate=0
source_row=1 met=false`, exit 1). It is the same frozen revision, so this is
not a new score, only confirmation that the numbers I derive from are the
numbers the wave was frozen against.

Provenance limit (no ruling, just what a later re-run can anchor to): the
counter's identity at baseline is the worktree digest above plus the wave
prompt; it is not a committed blob. The retained source body it is about *is*
committed at base.

## 2. Baseline per counter surface

`c62_calibration.py` paths: `spot`, `knowledge`, `quality`, `lesson`,
`sources` (`:16-22`). Measured at base revision:

| Surface | Blob at base | Measured baseline state |
|---|---|---|
| `corpus/lessons/round-61-verifier-spotcheck.md` | present | exactly one line carries both `S432` and `Disagree`: line 33, decision `Disagree`, reason “Web developers and conformance checkers must use the following” is only a generic lead-in, not substantive evidence. Lines 36, 41, 42 record the disagreement as **quality harmed** / **discernment harmed**; line 46 routes the fix to this round. `disagreements=1`. |
| `corpus/knowledge/response-header-expectations.md` | present, 216 lines | `## xcto_nosniff_value` at line 69; citation `[S432 §3.6]` at 75; quoted spans at 77 (`"can be used to require checking of a"`) and 79 (`"Web developers and conformance checkers must use the following"`); ABNF value block described (not quoted) at 81–86 with `(S432 §3.6)` at 86; receipt line 3 cites S432 sha256 `63b0a018…bad911b`. `"Round-62 correction"` occurrences: 0. |
| `corpus/QUALITY.md` | present, 1408 lines | 113 `- **` criterion bullets; `"substantive located quote"` occurrences: 0; `round-61-verifier-spotcheck` occurrences: 0. Nearest existing criteria: line 20 `Append-only tails (r20 resume)`; line 375 `A Gate quote is found in retained source text`; line 1398 `A quoted span in a knowledge entry is attributed to the location its page places it`. |
| `corpus/lessons/round-62.md` | **absent** | `git show c341a7a:corpus/lessons/round-62.md` fails; counter's `blob()` returns `""`; `lesson_gate=0`. |
| `corpus/SOURCES.md` | present, 287 lines | `| S432 |` at line 178, status `mined`, opened `2026-10-27`, entry pointer `corpus/knowledge/response-header-expectations.md`. Registry row count (`grep -c '^| S[0-9]'`): **171**, matching contract line 15's “Contract-v1 census counted 171 rows”. `source_row=1`. |
| `corpus/knowledge/*.md` count | — | 58 entries (baseline corpus size). |

The round-61 Gate already admits S432 on the generic lead-in: lesson
`corpus/lessons/round-61.md:43` records `§3.6 — "Web developers and
conformance checkers must use the following" (9 units; …sha256 63b0a018…bad911b,
1854393 bytes, HTTP 200)`. The contract keeps that row (`contract.md:7`,
“Preserve the old knowledge prose, source row, and verifier record; append
only”).

## 3. Source-location evidence present at baseline

Measured against the committed retained body
`.ufo/waves/round-61/sources/S432.html` (sha256
`63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`, 1,854,393
bytes, 18,915 lines; equals `receipts.json` S432 `status: 200`, `bytes`,
`sha256` and the entry's line-3 receipt):

- §3.6 heading at line 6149 (`<h3 … data-level="3.6" id="x-content-type-options-header">`).
- The paragraph runs 6150–6156; the sentence the contract names spans **6151–6154**:
  6151 opens the `X-Content-Type-Options` dfn, 6152 `response … header can be
  used to require checking of a … response’s`, 6153 `Content-Type … header
  against the … destination of a`, 6154 `request`.
- The verifier-rejected generic lead-in sits at **6183**, still inside §3.6,
  immediately before the ABNF block at 6187 (`X-Content-Type-Options =
  "nosniff" ; case-insensitive`). So at baseline the entry's two quoted
  pieces are, respectively, a sentence fragment of the purpose sentence and a
  value-grammar lead-in — the entry already cites the ABNF by location (81–86).
- Exact-string results for the counter's `QUOTE` constant
  (`c62_calibration.py:21`, 120 chars, 19 whitespace tokens):
  raw body `0`; tag-stripped, whitespace-collapsed body `0`; the same
  sentence **with** the body's literal inline-code backticks
  (`response’s `Content-Type` header`) collapses to exactly **1**
  page-unique occurrence. The QUOTE constant therefore cannot occur verbatim
  in the retained file; writing it into the entry means dropping the inline
  `<code>` backticks.
- No round-61 visible-text artifact exists to compare against: `ls
  .ufo/waves/round-61/sources/` lists four `.html` files plus `receipts.json`
  only (`*.txt` count 0).
- Word/char limits of the lane's own gate convention (round-61 lesson line 37:
  6..25 units, ≤160 chars, one collapsed text node, page-unique) are met by
  the contract's sentence (19 units, 120 chars, unique after backtick-preserving
  collapse).

What this buys: the *source-side* grounding of the contract's correction is
established at baseline. It says nothing about whether any correction has
been written, and it does not by itself satisfy the frozen counter.

## 4. Trend derivations — possible directions only

Trend definitions are quoted from canonical `LEARNING.md` (`:33-35`) and the
axis mapping from `AXES.md` (`:19`): expansion ↔ coverage + adjacency, quality
↔ depth + freshness + operability, discernment ↔ calibration.

### 4.1 Expansion (coverage + adjacency)

Observable (`LEARNING.md:33`): net new admitted `knowledge/` entries on ground
the coverage map did not hold, each `source:` citing a `mined` SOURCES row;
frontier areas entered; new kinds of source; a capability admitted to
SCORECARD. Failure signal: an admitted entry fails the bar it was admitted
under.

Baseline: 58 knowledge entries; 171 SOURCES rows; S432 already a `mined` row
(SOURCES:178) pointing at the existing entry; the entry already governs the
`xcto_nosniff_value` class (entry:69-94). The round's source is the *same*
page already admitted in round 61, and `contract.md:15` fixes
“Keep assimilation none unless a qualifying source package is actually
opened”; `contract.md:11` fixes “No second claim is frozen; any extra axis
work is reported separately and cannot be promoted as a claim.”

Possible direction under the frozen task: **none that can read `improved`.**
The two mandated appends land on already-covered ground (an existing entry,
an existing section of the quality bar), so there is neither a net-new entry
nor a new source kind, and the counter contains no expansion predicate at all.

Evidence still owed *if anyone claimed expansion*: (a) an after-revision
knowledge-entry count above the 58 baseline with a new ground claim;
(b) a new/changed `mined` SOURCES row with census `ok`; (c) a PROVINCE or
capability-table entry with a passing demonstration. None of these is in the
frozen predicate, so no verdict can be derived from the counter.

Verdict available now: **none.** “Unchanged” is the only expansion-consistent
outcome, and even that is not yet measured — it is owed to a post-integration
count, not asserted here.

### 4.2 Quality (depth + freshness + operability)

Observable (`LEARNING.md:34`): a weaker entry superseded by a stronger one, or
stale entries re-verified, with no admitted entry failing its re-check.

Baseline: an admitted entry currently fails the bar it was admitted under —
the non-author record at `round-61-verifier-spotcheck.md:33` rejects the
entry's S432 quote, and `:41` states the quality verdict “harmed … S432 fails
the quote-quality spot-check and remains admitted”. Freshness metadata already
reads `verified-at: 2026-10-27` with `recheck: 180d` (entry:2-3) and four
2026-10-27 receipts; operability is not in play (no new tool is frozen).

Possible direction: the frozen task *can* move depth — the contract names a
substantive quote for the entry's purpose sentence and a QUALITY criterion for
quote support. It can only read `improved` if the stronger grounding is
committed **in place of / above** the rejected piece and the old prose still
survives; the counter proves neither.

Evidence still owed for any quality verdict:

1. After-state counter at the *committed* measured revision printing
   `quote_correction=1` and `criterion=1` (counter reads committed blobs only,
   `:26-29`; wave artifacts do not count until committed).
2. Append/preservation proof. The counter has no preservation check; the
   existing instruments are `scripts/append_guard.py` (interface: `--root
   --base --revision --scope --json --selftest`; exits 0 clean / 1 findings /
   2 could-not-evaluate / 64 usage; non-EOF inserted runs must open with
   `[rNN-correction YYYY-MM-DD]`; EOF append may be untagged) and the
   QUALITY:20 criterion “every base line survives byte-for-byte once the tails
   are stripped”. Note the spelling difference: the counter requires the
   literal `Round-62 correction` (`:33`), while append_guard requires
   `\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]`; a single appended line
   cannot satisfy both spellings, so the after build must carry both forms or
   an EOF append plus a tagged run.
3. Quote-truth location receipt. QUALITY:375 (“A Gate quote is found in
   retained source text”, whitespace-collapsed exact substring) cannot be
   satisfied by the counter's backtick-free QUOTE against the retained body
   (0 occurrences measured). Reconciliation — a stated normalization for the
   inline `<code>` backticks, or a retained visible-text artifact with its own
   digest — is owed and is not in the frozen predicate.
4. Freshness: the entry's `verified-at` already carries 2026-10-27 and the
   round's source read reuses the same 2026-10-27 digest. No freshness pin
   moves unless a new recheck receipt is appended; the frozen predicate has no
   freshness condition, so no freshness verdict is derivable.

Verdict available now: **none.** A quality *improvement is possible*; the
baseline condition that makes it meaningful (an admitted entry failing its
bar) is recorded by a non-author, and that is the only quality statement the
baseline supports.

### 4.3 Discernment (calibration)

Observable (`LEARNING.md:35`): `improved` when the outside spot-check agrees
with the gate on admits *and* rejects, **or** a disagreement becomes a lesson
that adds a grounded `QUALITY.md` criterion; `harmed` when a disagreement is
left unlearned, or a criterion is added with no lesson behind it.

Baseline: one recorded `Disagree` (spot:33) with a written reason; the
verifier's own axis row says `calibration: unprovable` with “c61 distinct
counter absent” (spot:26); spot:42 says “Discernment: **harmed** — external
check disagrees with S432 admission and the disagreement is not yet learned
into QUALITY.md”; the lane's calibration score is **2**
(`SCORECARD.md:19`), and contract `:7` caps this: “Do not claim to resolve
every corpus disagreement or raise calibration above its ceiling.”

Possible direction: the **second** clause of `improved` is exactly what the
frozen task targets (correction + grounded criterion + round-62 Gate lesson
recording the candidate decisions). The **first** clause is out of reach: the
frozen predicate contains no new non-author judgment.

Evidence still owed for any discernment verdict:

1. After-state counter at the committed revision printing
   `unresolved=0`, `criterion=1`, `lesson_gate=1` (and `met=true`). Note the
   counter's arithmetic (`:39-41`): `unresolved = disagreements if not resolved
   else 0`. The standing `Disagree` row may remain — the contract forbids
   rejecting it — and `unresolved=0` is then a *derived* state, not the
   verifier withdrawing the disagreement.
2. A new outside spot-check of this round's admit/reject decisions, per
   `LEARNING.md` §“Discernment is checked from outside” (a lane-dispatched
   subagent does not count). The frozen predicate neither requires nor can
   produce this; therefore no `agrees on admits and rejects` claim is derivable
   this round, regardless of the counter.
3. The criterion must be *grounded* and cite the verifier finding (contract
   `:7`) and must not duplicate QUALITY:375 (quote found) or QUALITY:1398
   (quote attributed to its location) — the new property is *substantive
   support for the associated claim*. The counter checks only the two literals
   `substantive located quote` and `round-61-verifier-spotcheck.md` (`:24-25`,
   `:35`), so grounding is owed to the lesson/verifier, not to the counter.
4. The lesson Gate must carry candidates with Agree/Reject decisions; the
   counter checks only the four literals `## Gate`, `S432`, `Agree`, `Reject`
   (`:36-37`), so a Gate that mentions those words without a candidate
   decision would still pass.

Verdict available now: **none for round 62.** The inherited *harmed* state is
recorded evidence from round 61 (spot:42), not a round-62 verdict; this seat
does not re-score it. The maximum reachable claim this round is “disagreement
learned into lesson + criterion”, which is exactly the counter's second
clause — but it is only a possible direction until the after-state exists.

## 5. Evidence owed vs verdicts — ledger

Verdicts derivable at baseline: **0 / 3 trends.** Possible directions: **3**
(expansion: none-improved path; quality: improved-possible; discernment:
improved-possible via the lesson+criterion clause only). Owed evidence items:

| # | Owed evidence | Would be produced by | Why the frozen counter cannot supply it |
|---|---|---|---|
| E1 | after-state run of the frozen counter at the committed measured revision | L1/integrator, post-integration | it is the counter; baseline only exists before the fact |
| E2 | byte-level append/preservation proof for the entry (base lines survive) | `scripts/append_guard.py --base c341a7a --revision <rev>` + QUALITY:20 | counter never diffs old vs new bytes |
| E3 | quote-location receipt: the substantive sentence located at §3.6 lines 6151–6154, with the inline-backtick normalization stated | author + verifier | counter only tests the QUOTE literal's presence in the entry blob |
| E4 | one new outside spot-check of this round's admit/reject decisions, with reasons | non-author reviewer (LEARNING.md) | no outside judgment is in the predicate; `unresolved` is arithmetic |
| E5 | criterion grounding: the new QUALITY criterion cites the round-61 verifier finding and names the property it adds (substantive support, distinct from QUALITY:375/1398) | author + verifier | counter tests two filename/token strings |
| E6 | round-62 lesson `## Gate` with real candidate decisions and a round-mistake row with its criterion | author lane (contract:15) | counter tests four literal tokens |
| E7 | SOURCES row 178 unchanged (status/date/pointer) and census state at the after revision | census + `git diff` | counter tests only `| S432 |` |
| E8 | expansion-side counts if anyone reports expansion (entry count vs 58, new rows vs 171) | integrator | no expansion predicate exists |
| E9 | freshness decision if anyone reports freshness (pin/receipt movement) | author | no freshness predicate exists |
| E10 | reconciliation of the two correction-tag spellings (counter `Round-62 correction` vs append_guard `[r62-correction YYYY-MM-DD]`) | after build | counter and guard are separate instruments |
| E11 | provenance anchor for the counter itself (digest-only, untracked at base) | integrator if it matters for audit | counter cannot report its own commit status |

Related but explicitly outside this seat: what the after revision's
SCORECARD/LOG rows will read; whether calibration rises; whether any second
axis is promoted (contract:11 forbids promotion of extra work as a claim).

## 6. Findings (measured facts, no ruling)

- **F1 — `unresolved` is conditional, not adjudicated.** `c62_calibration.py:39-40`
  sets `unresolved = disagreements if not resolved else 0`. Once the other
  three literals pass, a still-standing `Disagree` row yields `unresolved=0`.
  That is consistent with contract:7 (“do not mark it rejected”), but it means
  the printed `unresolved=0` is not evidence of agreement.
- **F2 — `correction` is three literals in the knowledge blob** (`:33-34`):
  the QUOTE, `S432 §3.6`, `Round-62 correction`. It does not check that the
  quote appears in the retained body, that it supersedes the generic lead-in,
  or that the old prose survives.
- **F3 — `criterion` is two literals** (`:35`): `substantive located quote`
  and `round-61-verifier-spotcheck.md`. A criterion row containing those
  strings passes even if it is not grounded.
- **F4 — `lesson_gate` is four literals** (`:36-37`): `## Gate`, `S432`,
  `Agree`, `Reject`, in any arrangement.
- **F5 — `source_row` is one literal** (`:38`): `| S432 |`; status, date and
  entry pointer are unread.
- **F6 — contract prose vs counter.** Contract:7 says the counter “verifies
  old-row preservation and criterion/lesson/source pointers”; the literal
  checks in F2–F5 are narrower than that sentence. The instruments that
  actually test preservation are `scripts/append_guard.py` and QUALITY:20,
  neither of which the frozen counter invokes.
- **F7 — backtick tension.** The retained body carries literal backticks
  inside `<code>` (`response’s `Content-Type` header`); the counter's QUOTE has
  none. Measured occurrences: 0 without backticks (raw and collapsed), 1 with
  backticks (collapsed, page-unique). Counter green and a QUALITY:375-style
  substring check therefore pull in opposite directions on spelling; the
  reconciliation (normalization statement or visible-text artifact with its own
  digest) is owed — no round-61 `.txt` visible artifact exists.
- **F8 — the generic lead-in is in the same section.** It sits at 6183, after
  the `determine nosniff` algorithm and immediately before the ABNF block
  (6187). It grounds the value grammar, which the entry already cites by
  location (entry:81-86); the contract's sentence grounds the field's purpose.
  Neither quote grounds both, which is why the verifier's objection is about
  support, not about section placement.
- **F9 — the correction tag spellings differ.** See E10: counter (`:33`)
  wants `Round-62 correction`; append_guard wants
  `\[r[0-9]+-correction YYYY-MM-DD\]` for non-EOF insertion. Both can hold
  only if the appended run carries both (tag line first, prose naming the
  correction) or is an EOF append with the prose form.
- **F10 — counter provenance.** `git cat-file -e` fails and
  `git ls-files .ufo/waves/round-62/` is 0: the frozen counter and contract
  exist only as untracked worktree bytes at base, identified by the digest in
  the wave prompt (`ba7b77…8548d`). Its output is reproducible; its commit
  lineage is not yet a thing.
- **F11 — census not re-run by this seat.** The 171-row count I report is a
  direct `grep` on the base blob and agrees with contract:15's contract-v1
  count; I did not re-execute `scripts/sources-census.sh`, so its `exit 0` and
  the 16 W04 warnings remain a quoted contract record, not my measurement.

## 7. Out of scope / untouched

- No changes to the claim text, the frozen counter, `corpus/QUALITY.md`,
  `corpus/knowledge/response-header-expectations.md`,
  `corpus/lessons/round-62.md`, `corpus/SOURCES.md`, `SCORECARD.md`, `LOG.md`,
  `SHONEN.md` or any score.
- No fetch, no source-package assimilation, no expansion claim, no second
  claim, no scorecard promotion.
- No commits, pushes, Git/jj index operations, fixture git operations, or
  writes to fleet-root tracked files.
- No package manager transactions; nothing installed.
- Scratch: `/fast/scratch/hyaku/kake-r62/ScribeTrendVerdicts/` created and
  removed; no scratch file was needed.

## 8. Artifact paths

- This report: `.ufo/waves/round-62/w1/ScribeTrendVerdicts.md`
- Frozen counter: `.ufo/waves/round-62/c62_calibration.py` (sha256 `ba7b77…8548d`)
- Contract: `.ufo/waves/round-62/contract.md` (lines 7, 11, 15)
- Baseline surfaces: `corpus/lessons/round-61-verifier-spotcheck.md:33,36,41,42,46`;
  `corpus/knowledge/response-header-expectations.md:2-3,69-94`;
  `corpus/QUALITY.md:20,375,1398`; `corpus/SOURCES.md:178`;
  `corpus/lessons/round-61.md:37,43`; `SCORECARD.md:19`
- Retained source body: `.ufo/waves/round-61/sources/S432.html` (6149–6156,
  6183–6187; sha256 `63b0a018…bad911b`), `receipts.json` S432 entry
- Prior instrument for append evidence: `scripts/append_guard.py`
- Canonical trend definitions: `/home/vgpnk/Projects/shokunin/LEARNING.md:33-35`;
  axis mapping `AXES.md:19`
