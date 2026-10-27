# CriticC1Cheat

Scope: attack the c61 counter/tool design from the frozen contract text
(round-61 contract.md + contract.json, base 9f07731a873585e655a6518233ea39f5d9fb8204).
The w1 tool/counter sources are not yet in the lane, so each cheat was built and
run in scratch against contract-conformant fixture models; demos + captured
output are in `.ufo/waves/round-61/w1/CriticC1Cheat.files/`
(`build_fixture.py`, `sniff.py`, `skeleton.py`, `case_twist.py`,
`worktree_vs_committed.sh`, `poplist_demo.py`, `evidence.log`).
No installs this seat (python3 stdlib + git only). Scratch dir removed.

## CHEATS:

1. **Tool sniffs fixture repos via environment shape; goes honest only on the real lane.**
   Demo: `sniff.py` classifies 3/3 seeded fixtures (seeds 101/202/303) as FIXTURE and the
   real lane at base as REAL-LANE, using only committed-bytes plumbing (`git ls-tree`,
   `git rev-list`, `git log` — the same surface an honest `receipt_lineage.py` may touch).
   Observable gap (evidence.log): fixtures have 1 root entry (`.ufo`) vs 13 in the lane
   (`SKILL.md`, `scripts/`, `corpus/`, …), 2 commits vs 374, single author `selftest@local`
   vs 8 identities, single-day date span vs 2026-09-28..10-27, no `round-61` dir, ≤3 refs
   vs 1355. Seeded ids do not touch any of these signals.
   **Caught? NO (only partially).** The frozen rule "ids drawn from the seed so a
   fixture-keyed tool cannot recognise them" defeats content keying only. The sole frozen
   defense is the counter selftest control "fixture-sniffing composite", but only its
   existence is frozen, not its mechanism — and a single real-lane run cannot catch a tool
   that lies on the lane: R2 expects `undisclosed=0`, which is exactly what a lane-lying
   tool prints, clean lane or not. The dishonest branch only fires if some input is
   lane-shaped, which no plain fixture is.

2. **Counter reads the worktree instead of committed bytes at `--revision`.**
   Demo: `worktree_vs_committed.sh` — one repo, three views: committed bytes at HEAD carry
   `revision: r90-2`; the dirty worktree carries `revision: r90-3-UNCOMMITTED` (an "event"
   that never existed in history); at base the file is absent from committed bytes.
   **Caught? CONDITIONALLY.** Frozen rules "the counter runs the tool as committed at the
   revision" (extracted via `git show <rev>:scripts/receipt_lineage.py`) + do-nothing
   control "base → 0/18" catch it only if the control is run with worktree ≠ `--revision`
   (e.g. `--revision base` while the worktree holds the measured revision, whereupon R1
   sees the tool present and the expected 0/18 vector breaks). Nothing freezes that run
   mode; in a clean clone checked out at `--revision`, all controls pass either way.

3. **Counter's frozen population list is the measured revision's list, not the base list.**
   Demo: `poplist_demo.py` — same fixture (base: population files receipt-a/b; measured
   rev: receipt-a mutated + receipt-c added). Strategy A (list frozen from base) reports
   `member_changed=[receipt-a]`, `extra_member=[receipt-c]` → L10=1, L11=1 (pass).
   Strategy B (list re-derived from the measured revision's own tree) reports both empty
   → L10=0, L11=0 (fail its own cases).
   **Caught? YES.** L10/L11 expected results are only achievable with the base-frozen
   list, and the contract freezes provenance: "the population is frozen by path list in
   the counter at base (144 files at 9f07731a, enumerated in population-144.txt,
   committed before any seat runs)". Residual hybrid (embedded list in fixtures, lazy read
   on the real lane) is only reachable via cheat 1's sniffing — see T4 for the cheap freeze.

4. **Tool hard-codes the 16 expected fixture shapes.**
   Demo: `skeleton.py` — L2 fixtures at seeds 101 and 202 (different ids, paths, commits,
   content tokens) yield the identical structural fingerprint `[n_commits=2, n_files=1,
   span-pattern {# receipt:, revision:} × 2 commits]`. The case table is frozen, so every
   fixture's skeleton — commit count, population-file count, which span lines appear in
   which commit, disclosures-flag presence — is constant across seeds; only content ids
   jitter. A tool can key on the skeleton and replay per-case verdicts.
   **Caught? PARTIALLY, same gap as cheat 1.** The frozen seed rule randomizes ids, not
   structure; multi-seed reruns defeat only content-keyed tools. The "fixture-sniffing
   composite" control could catch a skeleton-keyed tool only if built to jitter structure
   or to re-run cases lane-skinned — mechanism not frozen.

5. **Tool treats disclosure entries with wrong case as covering.**
   Demo: `case_twist.py` — five disclosure entries naming the SAME real rewrite event
   (clean entry; path dir case-twist `.ufo/WAVES/…`; `Controls`-twist; upper-cased commit
   hex; both twisted). Strict equality covers only the clean entry; a case-insensitive
   matcher covers all five. No frozen fixture (L3/L8/L13) feeds a twisted entry, so the
   loose tool still scores 18/18 while turning twisted real-lane disclosures into silent
   false negatives (`undisclosed=0` → met).
   **Caught? NO.** "holds an entry with equal path and commit" does not freeze the case
   semantics of `equal`, and no case exercises it. Cheapest closed in w1, before the L1
   freezes the counters; a v2 fix would be a named tightening anyway.

## TIGHTENINGS:

- **T1 (cheats 1, 4).** Freeze the composite control's mechanism: build every fixture case
  twice — plain and lane-skinned (lane's committed bytes at base with fixture commits
  grafted on: full root tree incl. `SKILL.md`/`scripts/`/`corpus/`, backdated multi-author
  history, ≥300 commits, refs, packed objects, `round-61/` dir) — and require the tool's
  verdict stream to be byte-identical across both builds; any divergence fails the case.
  Draw structural jitter from the same seed: decoy population-file counts, no-op history
  padding, disclosure-note prose.
- **T2 (cheat 2).** Freeze a committed-bytes selftest control: run the counter against a
  scratch clone at `--revision base` with a deliberately dirty worktree (uncommitted edits
  to the tool file, disclosures JSON, and population files) and assert verdicts identical
  to the clean run; any worktree sensitivity fails the control.
- **T3 (cheat 5).** Freeze disclosure-match semantics: `path` byte equality; `commit`
  compared after lowercasing both sides (git emits lowercase hex). Add one case-twist
  fixture (twisted entry, same event) expecting the undisclosed finding.
- **T4 (cheat 3, belt-and-braces).** Freeze that the counter embeds the 144-path list as a
  source literal hash-equal to `population-144.txt` at base, and that L10/L11 fixtures
  carry the base `population-144.txt` in-tree so a lazily reading counter fails its own
  cases.

All four tighten C1 only; C2/C3 surfaces untouched (causal separability preserved).

VERDICT: cheats 1, 4, 5 pass all 18 frozen cases today; 2 is caught only conditionally; 3
is caught — freeze T1–T3 (T4 optional) before the L1 freezes the counters.
