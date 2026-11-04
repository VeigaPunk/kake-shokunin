# ReviewC1 — adversarial review of C1 (round 78, w1)

**Verdict: the C1 counter and both controls hold under every prescribed attack (8/8 fixtures behaved as contracted; one invalid probe of mine disclosed below); three findings — recorded-value freshness (applied), duplicate-id false green (routed), working-tree c77 unpinned (routed) — and two disclosure items for the lesson.**

Revisions measured: base `fe50945399a386b48678b1f2051fdbe8a77b10bd`, freeze `78711a62`, carrier `c758904c` (L1 amendment 1; `git diff 78711a62..c758904c -- corpus/knowledge/shonen-ledger.json SHONEN.md .ufo/waves/round-78/c78_shonen_population.py` is empty, so all three carry identical C1 inputs). Round-77 counter unchanged base→working tree (`git diff fe509453 -- .ufo/waves/round-77/c77_shonen_ledger.py` = 0 lines). No edits made to lane tracked files; fixtures ran in `/fast/scratch/hyaku/kake-r78/ReviewC1/` (deleted before yield, see §6).

## 1. Independent re-derivation (own code, not the counter)

I reimplemented every ledger measure in my own driver (`w1/ReviewC1/driver.py`, retained; transcript `attacks.log` PART 1) and derived directly from `git show`/`git ls-tree` at base and carrier. Recorded vs mine:

| check | recorded | mine @base | mine @carrier |
|---|---|---|---|
| b1-ids {ids,resolved,unresolved} | {77,77,0} | {77,77,0} | {77,77,0} |
| b1-tables | 18 | 18 | 18 |
| b1-registry | 105 | 105 | 105 |
| b1-checklist | 1 | 1 | 1 |
| b2-rounds | 56 | **57** | **57** |
| b2-receipts | 98 | **100** | **100** |
| b2-missing | 1 | 1 | 1 |
| b3-scripts / b3-invocations | 0 / 0 | 0 / 0 | 0 / 0 |
| b4-lanes | 0 | 0 | 0 |
| box-4 population (`corpus/knowledge/*.md`) | *not declared* | **64** | **64** |

- Every count matches except `b2-rounds` 56→57 and `b2-receipts` 98→100 — exactly the two `tolerated growth` lines in `controls/base-c1-population.txt`. So the base receipt is not hiding any drift beyond what it prints.
- **Box-4 note number: does not match.** My count is **64** at base and carrier; `SHONEN.md` box-4 says "0 of **63** entries" and the ledger's own `b4-lanes.note` says "**63** knowledge `.md` files are scanned at the revision". The contract's premise ("not the stale 63") is confirmed — but the stale 63 also sits **inside the ledger row's note**, which the deliverables text does not name (finding F3).
- Populations: 0/4 declared at base and carrier — `rows_with_population=0 undeclared=4`, `met=false`. Correct pre-work state; F0 below proves the gate is reachable.

## 2. Attacks on the counter (fixtures, throwaway identity, scratch only)

Method: `git archive fe509453 | tar -x` into a scratch dir, `git init`, toplevel asserted, edit, commit, then `python3 -B .ufo/waves/round-78/c78_shonen_population.py --root <fixture> --revision <rev>`. Full outputs retained in `w1/ReviewC1/attacks.log`.

| fixture | edit | exit | result |
|---|---|---|---|
| f0 green baseline | 4 populations declared with my counts (64) | **0** | `met=true`, growth_tolerated=2 — predicate satisfiable |
| f1 wrong count | box-4 count 63 vs true 64 | **1** | `S1 box 4: declared=63 derived=64` — red |
| f2 delete key | `population` removed from box 2 | **1** | `S2 box 2: no population declaration` — red |
| f3 fifth row | valid 5th row, box 5 | **1** | `rows=5` AND `S3 exact: box-out-of-range box 5` — red on two independent mechanisms |
| f4 shrink | LOG.md: 2 round headings deleted (57→55) | **1** | `S4 floor: recorded 56 but re-derived 55` — shrinkage is drift |
| f4b shrink-to-record | 1 heading deleted (57→56) | **0** | `met=true`, growth_tolerated=1 — floor closes exactly at the recorded value |
| f5 grow | 2 fake round headings (57→59) | **0** | `met=true`, `tolerated growth: recorded 56 but re-derived 59` — the floor rule, as contracted |
| ctl note-only | SHONEN.md 63→64 + green c77 stub (`findings: []`), no populations | **1** | `rows_with_population=0 undeclared=4 … met=false` — identical counts to `controls/ctl-c1-note-only.txt` |

Selftest: `--selftest --work <scratch>` → `selftest: 9/9 passed`, exit 0. An incidental extra attack fell out of a bug in my own first f6 attempt: a population dict **without a `count` key** grades `S1 box 4: declared=None derived=64` — red, correctly.

## 3. The floor rule — legitimate or loosening?

**Wording check (verbatim).**
- Contract §C1: "`count_at_least` = dated floor: growth is not drift, shrinkage is; everything else exact"; body: "where the re-derived value is **below** the recorded one. Growth is not drift … Shrinkage is drift."
- Counter docstring (`c78_shonen_population.py:6-8`): "`count_at_least` observations are dated floors (growth is not drift, shrinkage is), every other observation is exact." — same words modulo inflection. ✔
- SKILL.md:199-202 actual words: "Counts of files that grow **on a timer** (probe-history rows, full/spot splits, era families) are floors or dated measurements, never constants". The contract's attribution says "counts that grow **with the corpus**" — a deliberate generalization (timer-grown freshness files → corpus counts), a paraphrase rather than a quote. Also note SKILL.md's second clause ("verb-outcome samples … MUST be re-run before being cited") is *not* carried into C1; b2-rounds/b2-receipts are classified as floors, so no re-run duty attaches. Defensible; say so explicitly in `corpus/lessons/round-78.md` (finding F5).

**Legitimacy.** A `count_at_least` recorded value is a dated floor claim ("≥56 at vintage a2cc5f51"); growth keeps the claim true, so re-grading growth as clean is semantically honest, contracted, and self-tested (s5/s6). But two honest disclosures are required:

- **It is load-bearing.** Relative to round-77's exact grading it tolerates two currently-stale observations to reach green: without the floor rule `exact_mismatches` would be 2 at base and populations alone could not flip C1. `growth_tolerated=2` at claim time is the expected shape, not a hidden pass — the lesson must state this.
- **Counter coexistence.** At base, `c77` itself prints `mismatches=2 met=false` (exit 1, run verbatim: `C1 revision=fe509453… boxes=4 evidenced=3 gap=0 unexamined=0 mismatches=2 met=false`). After C1 lands, **c78 will say met=true while the unchanged measure authority c77 still says met=false** on the same two findings. Anyone re-running c77 bare post-C1 sees red. Disclose in the lesson (finding F5).

**Strongest counter-examples.**
1. **Falsified-ledger false green (found, reproduced).** c77's schema has no check-id uniqueness rule (`_check_schema_problem`, c77:438-465; only `duplicate-row` for rows per box). `classify()` builds `kinds[id]=kind` from the ledger under test with last-row-wins (c78:88-91). Fixture f6b: box-2 `b2-missing` recorded `observed: 0` while the tree re-derives 1 (a *missing receipt growing* — a defect count), plus box-4's check re-typed `count_at_least` with the same id `b2-missing` (schema-valid under c77). Result at `ed4fb0a7`: `exact_mismatches=0 … growth_tolerated=3 met=true`, `tolerated growth: recorded 0 but re-derived 1`, **exit 0 — false green** (transcript `attacks-f6.log`). The contract says observations are graded "by its **measure's shape**"; the implementation grades by the **kind label in the policed bytes**. Reachable only by editing ledger checks (outside this round's write scope), but the counter exists to police exactly those bytes. Verdict: **routed** — one-line hardening (grade as exact any mismatch whose id is not a unique frozen `count_at_least` id, or flag duplicate ids).
2. **Glob padding within the unmodified ledger.** `b2-receipts` counts globs and `b2-missing` ignores `*` tokens, so LOG.md padded with glob paths grows the tolerated number unchecked — but non-glob missing receipts are still caught exactly (b2-mismatch → S3), so the defect class that matters stays covered. No action.

## 4. Receipt verification

- `controls/base-c1-population.txt` **reproduced byte-identical**: `python3 -B .ufo/waves/round-78/c78_shonen_population.py --root . --revision fe509453…` (counter exit 1 as prescribed) then `diff` vs the receipt → empty, `BASE_RECEIPT_BYTE_IDENTICAL`. Reproducible because the working-tree c77 equals base's c77 (0-line diff) — see F4 for why that is a precondition.
- `controls/ctl-c1-note-only.txt` **reproduced**: my ctl fixture output matches the receipt's counter lines exactly (`rows=4 rows_with_population=0 undeclared=4 stale_populations=0 exact_mismatches=0 floor_violations=0 growth_tolerated=0 met=false`, four `S2` lines, exit 1); only the embedded fixture hash differs (receipt `9d84288…`, mine `d15bbce…` — the receipt documents its own fixture, so byte-identity is not expected across fixtures). The cheap fix provably stays red.

## Findings

- **F1 (applied) — recorded values not refreshed.** Contract deliverable says the ledger gains "a `population` object per row **and current recorded values**". `b2-rounds` 56 (tree 57) and `b2-receipts` 98 (tree 100), mirrored by SHONEN.md box-2 prose, are tolerated rather than refreshed. Refresh to the values at the revision the predicate will be evaluated at (note: integration itself adds a round-78 LOG.md section, so measure at the integration revision or accept `growth_tolerated≥1` at claim time — still green, but not "current"). Zero-cost; also empties the tolerated class.
- **F2 (routed) — duplicate-id false green.** See §3.1; harden `classify()` against duplicate ids / defect-shaped `count_at_least` labels.
- **F3 (applied) — stale "63" inside the ledger.** `shonen-ledger.json` b4-lanes note says 63; the population re-derives to 64. If left, the ledger contradicts itself on the same row (population.count=64, note=63) — the exact class C1 kills. Update the note with the population work (SHONEN.md box-4 is already in the deliverables).
- **F4 (routed) — c78 runs the working-tree c77, not the revision's.** `c77_findings()` executes `root / ".ufo/waves/round-77/c77_shonen_ledger.py"` (`c78_shonen_population.py:70-71`). Receipts at old revisions are only reproducible while c77 is unchanged (true today). Pin via `git show <rev>:<C77_REL>` to a temp file. No change demanded this round.
- **F5 (applied, disclosure) — lesson must state:** (a) the contract's SKILL.md attribution is a paraphrase/generalization, not a quote; (b) `growth_tolerated=2` at claim time is expected and load-bearing; (c) post-C1, c77 bare still prints `met=false` (mismatches=2) by design — c78 re-grades, c77 does not.
- **F6 (rejected as a defect; footgun note) — exclude-pattern conventions differ.** c78 matches population `exclude` against path **basenames** (`fnmatch(Path(n).name, pat)`), c77's b4-lanes check against **full paths**. With `suffix: ".md"` the `freshness-*.json` exclusion is vacuous in both (suffix already excludes .json). If a future spec uses `suffix: ""` and copies the check's full-path exclude string, c78 silently fails to exclude — visible as stale/red, never silent-green. Executors: use basename patterns in population excludes (as selftest s4 does).

## Residual risk / gaps

- The predicate cannot verify that a population *spec* measures the semantically right thing (a wrong dir with a matching count is green); the declaration's meaning is review-asserted only — frozen by contract.
- f6b's false green required ledger-check edits; I did not fuzz other c77 finding classes flowing through `classify` beyond `row-invalid` (selftest s8) — all non-`observation-differs` classes hard-code to exact, so exposure is limited to the misgrading shown.
- Carrier may move again before integration; C1 inputs were identical at all three revisions I measured, but the ledger/SHONEN.md work had not landed when I reviewed (populations still 0/4 at `c758904c`).

## Artifacts & hygiene

Retained under `.ufo/waves/round-78/w1/ReviewC1/`: `base-repro.txt` (bb3ddcda…), `attacks.log` (da175090…), `attacks-f6.log` (062d8af3…), `driver.py` (d64d6c36…). Scratch `/fast/scratch/hyaku/kake-r78/ReviewC1/` deleted and verified absent (`SCRATCH_CLEAN`). No tools installed (operator authorization unused). Ledger, counter, SHONEN.md untouched; git usage read-only plus fixture-local commits in scratch with throwaway identity `review-c1-attack`.
