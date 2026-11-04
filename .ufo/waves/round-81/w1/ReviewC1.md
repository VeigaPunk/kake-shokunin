# ReviewC1 — round 81 w1, attack of C1 (`c81_defect_queue.py`)

**Verdict: the counter is arithmetically honest and every receipt verifies, but the claim is
gradeable-to-green without doing the routed work — all six items close on do-nothing trees, a
composite do-nothing tree reads `open=0 met=true exit=0`, and the committed junk control is
byte-reproducible from an empty directory, so the kill rule cannot fire against the one vector
(prose over real substrate) that actually defeats the counter.**

Attacked counter: worktree bytes `eae0c5780af6609671192f73aed0f26f18309f593ee27216ef5c2a2addcfaaad`
(= HEAD `e93d26b7`, clean; the freeze-commit counter `a77b8a19` is `d4b0fa80…`, differing only by
amendment 1 — see F7). I edited no counter, no contract, no receipt, no production file. No tools
installed (operator tooling authorization unused). Scratch deleted; receipts retained under
`.ufo/waves/round-81/w1/ReviewC1/` (sha256s in `MANIFEST.sha256` there).

## 0. Re-runs (all verbatim, with exit codes)

| Check | Command (cwd = lane repo) | rc | Matches committed bytes? |
|---|---|---|---|
| selftest | `python3 -B .ufo/waves/round-81/c81_defect_queue.py --selftest --work <scratch>` | 0 | yes — `selftest: 15/15 passed`, line-identical to `controls/c81-selftest-c1.txt` |
| base control | `python3 -B .ufo/waves/round-81/c81_defect_queue.py --root . --revision 2e11925500dd5a739376c9108c94616243af0cd4 --work <scratch>` | 1 | yes — every verdict/C1v1 line byte-identical to `controls/base-c81-defect-queue.txt` (`open=6 met=false`) |
| junk control | counter over my empty-dir repro, `--root <empty>` | 1 | yes — byte-identical to `controls/ctl-c81-junk-queue.txt` (see F4) |
| worktree mode | same counter, no `--revision` | 1 | n/a — reads `open=2 closed=4` (R80-1/2/3/5 already close in the live worktree) |

**Base control genuinely reads the base revision, not the worktree:** with `--revision` the C1v1
line carries the hash and R80-5 says `junk_tree_build.py absent` — true only of `2e11925`, since
the same counter without `--revision` runs the worktree builder and closes R80-5
(`receipts/base-rerun.txt` vs `receipts/worktree-run.txt`). The `--revision` flag is load-bearing.

## 1. Per-item do-nothing controls (fixtures scored with the counter)

Cheapest tree per item = base-revision bytes (`2e11925`, materialised via the counter's own
`materialise`) plus only what that item's predicate reads. Fixture outputs retained as
`receipts/r80*.txt`.

| Item | Cheapest do-nothing tree | Counter verdict | Closes? | Finding |
|---|---|---|---|---|
| R80-1 | one prose row in `corpus/lessons/round-81.md` naming `corpus/SOURCES.md:200` + `S453`; registry untouched; `corpus/lessons/round-80.md:51` still asserts `:201`; the routed erratum in `.ufo/reports/round-80/kake.md` unwritten (that file is not even in the lane repo) | `R80-1 closed … names corpus/SOURCES.md:200` (open=5) | **YES** | F1, F2 |
| R80-2 | one prose row carrying `constants_failed=4/4, 47/48, 11/12` copied from the committed round-80 receipt; `LOG.md:2726` "fail 12/12 each" left standing | `R80-2 closed … re-derives 4/4, 47/48, 11/12` | **YES** | F2 |
| R80-3 | one prose row `rfc9110.txt rows=3; rfc9110.html rows=3`; `corpus/README.md` wrong "second scope" prose left standing | `R80-3 closed … rows=3 and rows=3` | **YES** | F2 |
| R80-4 | hand-written spec + **one fabricated results row** (a reviewer, non-empty) + matching accounting record | `settled attack share 1.000 (1/1)` | **YES** | F5, F6 |
| R80-4 (error variant) | same, output = `"Traceback … exit 1 provider 429"` | `settled attack share 0.250 (1/4)` | **YES** — a crash traceback counts as settled attack work | F5 |
| R80-5 | the committed builder+spec pair; double-run digests identical (`r805-double-run.txt`); round-80's own counter reads `open=5 closed=1 met=false` exit 1 | `R80-5 closed … deterministically (1 files)` | **YES** | L1 (limit) |
| R80-6 | ship the recorder, run it once over hand-written results; the committed record *is* the re-derivation; `exit="unknown"`, `error="not recorded in w1-results.json"` are constants | `R80-6 closed … record equals re-derivation` | **YES** | F3 |
| **all six at once** | composite of the above | **`C1v1 … open=0 closed=6 met=true`, `exit=0`** (`receipts/all.txt`) | **YES — entire queue** | F2 |

No unsatisfiable conjunct exists — the opposite: **every item is closable without its routed fix.**
In the composite, `corpus/lessons/round-80.md` still says `:201`, `LOG.md` still says "12/12 each",
`corpus/README.md` still carries the wrong scope prose, no erratum exists anywhere, no real wave
ran, and the counter reports the calibration claim met.

## 2. Findings

- **F1 (high) — R80-1's condition never reads either routed document.** §6 routes R80-1 at
  `.ufo/reports/round-80/kake.md:158` and `corpus/lessons/round-80.md:51`. The counter reads
  neither: the report is a *fleet*-repo byte (`git show 2e11925:.ufo/reports/round-80/kake.md`
  → "does not exist" in the lane repo — the lane counter structurally cannot verify its
  correction), and the round-80 lesson is only read by predicates that don't look at it. Fixture
  r801 closes with both wrong pointers intact.
- **F2 (high) — the contract's do-nothing paragraph is refuted by execution.** contract §C1 says
  a words-only round "also fails, because every condition reads lane bytes the report cannot
  forge (registry line numbers, receipt arithmetic, a re-run of round-80's counter, a canonical
  record re-derivation)". Each "unforgeable" anchor binds prose to *existing bytes*, not to a
  *fix*: the line number is the counter's own output, the receipt arithmetic is copyable from the
  committed receipt, the counter re-run passes because the round ships a fixture built to pass it,
  and the canonical re-derivation is produced by running the shipped recorder. Composite: met=true.
- **F3 (high) — R80-6 closes on a record that declares the routed ask unmet.** §6's ask:
  "Record status, exit and error **at dispatch time in the next results schema** so a dead seat's
  cause is citable." `w1-results.json` still carries only name/agent/output; the recorder writes
  `exit:"unknown"` and `error:"not recorded in w1-results.json"` for every seat and names that
  limit as its `schema_limit` — and naming the limit is itself a closing conjunct. The defect's
  substance (a citable cause) remains unmet by the record's own bytes, yet the item closes.
- **F4 (high) — the committed junk control does not exercise the kill rule it exists for.**
  `controls/ctl-c81-junk-queue.txt` is byte-reproducible from an **empty directory**
  (`receipts/empty-junk.txt`; every item opens on absence, not on fabricated-words-rejected). The
  contract declares the junk tree "fabricates closure in words"; the committed receipt shows no
  words were exercised. My composite proves the words-over-real-substrate vector drives the counter
  to met=true — so the kill rule ("junk control reads met=true ⇒ counter wrong") can never fire on
  the counter's actual weak point. A junk control that would bite = base tree + the three prose
  rows (it would read open=3 met=false only because R80-4/5/6 substrates are absent — and open=0
  if those are shipped too, which is exactly F2).
- **F5 (medium) — "settled" means vocal, not successful; no minimum population.** Post-amendment-1
  `settled` = results row with non-empty output. One fabricated row ⇒ share 1.000 (r804a); a
  traceback counts (r804b). `total == 0` is the only population floor. Round-80's empty-seat
  failure mode is genuinely fixed, but the share is a share of *reporting* seats; combined with
  F3's schema limit, no outside verifier can distinguish "settled" from "crashed loudly" from
  lane bytes. Non-attack seats dying empty also *raise* the share (denominator shrinks faster) —
  the metric rewards silence, within limits.
- **F6 (medium) — R80-4/R80-6 are graded entirely on round-81-authored bytes.** Their predicates
  re-derive from `w1-spec.json`, `w1-results.json`, `w1-accounting.json`, `seat-failures.json` —
  all authored this round. The counter never reads `w1-dispatch.json` or `w1.ready.dispatched`
  (not in EXPORT_PATHS), so nothing binds the results to what was actually dispatched; a hand-edited
  results file re-derives consistently. The real anchors — registry line (R80-1), committed round-80
  receipt (R80-2), registry counts (R80-3), round-80's own counter (R80-5) — cover four items;
  the two accounting items have none. Hardening: accounting record should carry
  `results_sha256` + dispatch digest, and the counter should cross-check seat names against
  `w1-dispatch.json`.
- **F7 (low, process) — two post-freeze amendments moved the instrument and one C1 receipt.**
  Freeze `a77b8a19` shipped a counter (`d4b0fa80…`, selftest 13/13) whose `p_r80_4` counted
  empty-output seats as settled, contradicting the frozen contract's own sentence; amendment 1
  (`0a27045e`, before any after-state) fixed the counter to match the contract sentence and
  re-cut `c81-selftest-c1.txt` (13/13→15/15), disclosed in `.ufo/waves/round-58/receipt-rewrites.json`
  and commit `bec3ecf7`. Amendment 2 (`eccd0f9c`) similarly moved the C2 counter and two C2
  receipts (12/12→18/18) — outside my scope, noted for ReviewC2. The direction (instrument →
  contract sentence) is defensible and the timing/discipline are clean, but the clause "an
  amendment may only clarify a term the counter cannot evaluate" is strained: `settled` was
  evaluable; the counter evaluated it wrongly. The wave brief's tallies (13/13, 12/12) are stale
  against the committed receipts for this reason.
- **F8 (low, latent) — name-collision edges, no live trigger.** `p_r80_4`'s `role_of` dedups by
  seat name (last wins): duplicate spec names collapse `requested_attack` (probe: 3 items, dup
  name ⇒ requested_attack=0, record must match ⇒ consistent). The recorder silently last-wins on
  duplicate results rows (`r806-dup.txt`). Real spec has 15 distinct names; untriggered.
- **F9 (info) — R80-5 verdict-equivalence limit.** The rebuilt junk tree provably matches only
  round-80's counter *verdict* (`open=5 closed=1`), not the lost scratch tree; fidelity is
  unprovable and the frozen condition is verdict-shaped. The builder itself is honestly
  deterministic (no timestamps, relative paths only, `..`/absolute rejected; two runs
  byte-identical) and R80-6's recorder output is byte-stable under results-row reordering
  (`sort_keys` + sorted lists; `r806-order.txt`). These checks pass.

## 3. Predicate-level statement (step 4)

`met <=> open == 0` over six items whose closure conditions the L1 also authored. Four items have
a real external anchor (registry bytes ×2, committed round-80 receipt, round-80's committed
counter); R80-4 and R80-6 have none — they are closed by records derived from the same round's
own bytes (F6), so the round grades its own homework on exactly the two items born from the
round-80 accounting defect. **What an outside verifier must re-run:** (a) the counter over the
committed after-tree with `--revision <after>` (covers all six mechanically, ~seconds); (b) for
R80-4/R80-6 provenance, which the counter cannot decide: compare `w1-results.json` seat
names/outputs against the orchestrator's dispatch/session logs — bytes outside the lane repo;
(c) confirm the three prose corrections in `corpus/lessons/round-81.md` against
`corpus/SOURCES.md:200` and `controls/ctl-c80-constants.txt` (counter does this). I believe no
conjunct cannot pass; I believe equally that none of the six requires the routed work to pass.

## 4. Hygiene

Read-only everywhere except this report and `w1/ReviewC1/`; no git/jj mutation; no counter,
contract, control, or lesson edit; fixtures and double-runs under
`/fast/scratch/hyaku/kake-r81/ReviewC1/` (deleted at yield); no tool installs. Worktree drift
during audit: HEAD advanced `bec3ecf7`→`eccd0f9c`→`e93d26b7` (amendment-2 commits, C2-scoped);
C1 counter bytes unchanged throughout (`eae0c578`).
