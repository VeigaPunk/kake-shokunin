# kake round 69 — frozen contract (attempt 1)

Base: `4d188f9477b4301a2c93c8ef5c13bc6c6f4bb6e4` (lane `master` tip at round open; `jj-lane.sh state` ahead=0 behind=0).
Scores at open: calibration 2 (lowest owned non-retired axis), operability 10, freshness 10 (HOLD). The stagnation nudge does not apply (calibration sits below the saturation line), so the lowest-axis obligation binds.
Census at round start: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` exit 0 (16 W04 duplicate-url warnings, `kake ok`).

Two claims, one axis each, causally separable (C1 touches no file C2 touches and vice versa; verified by ConnW1 and the counters, which each run without the other). No exploratory claim. No capability row is claimed.

## C1 — calibration (2 → 2, HOLD). Recorded counts re-derive or are relabelled.

Claim: every integer count that the round-67 and round-68 records attribute to a shell command at a named revision either re-derives at that revision, or is relabelled by a correction row that names the pair id and the re-derived value.

Predicate (identical sentence in this plan, the counter's code and the receipt label): **C1 is met iff `python3 -B .ufo/waves/round-69/c69_recorded_counts.py --root <lane> --revision <rev> --pairs .ufo/waves/round-69/c1/pairs.json` prints `unrelabelled=0` and exits 0.**

- Frozen pair set: `.ufo/waves/round-69/c1/pairs.json`, produced by ScoutC1Pairs and committed by the L1 **before** the base run. Recorded values in that file are frozen; no seat or later step edits them. A pair discovered after freezing is a round-70 item.
- Correction rule (the only resolution): a mismatching pair is cleared solely by a correction row appended in `corpus/lessons/round-69.md` §Corrections that names the pair `id` and the re-derived value. Original record lines are never edited (append-only; `corpus/QUALITY.md` ruling of round 20).
- Do-nothing control: the base revision `4d188f94` run with the same pairs file. Kill rule: if the base already meets the predicate, the counter or the pair set is wrong and C1 lands `unprovable` with no credit.
- Known pair: the round-67 ledger pre-value "5 → 1" for `corpus/knowledge/gate-status-ledger.md` (records: `corpus/lessons/round-67.md:54`, `LOG.md:2319`); the round-68 spot-check re-measured 2 at base `3961281` and at `099923320` (`corpus/lessons/round-68-verifier-spotcheck.md` §2 C1 table).
- Measured: base run (expected `unrelabelled ≥ 1`), then tip T1 after the correction row lands (expected `unrelabelled=0`).

## C2 — operability (10 → 10, HOLD). The lane gate honours TMPDIR and holds no /tmp root.

Claim: `scripts/freshness-sweep.mjs` carries no literal `/tmp` path in code (two sites at base: line 108 `R15_SNAPSHOT_DEFAULT`, line 1204 selftest default `KAKE_SELFTEST_DIR || '/tmp/kake-r16/selftest'`), and its `--selftest` writes its fixture directory under `$TMPDIR` when `KAKE_SELFTEST_DIR` is unset.

Predicate (same sentence in plan, counter and receipt): **C2 is met iff `python3 -B .ufo/waves/round-69/c69_tmp_honour.py --root <lane> --revision <rev> --work <scratch dir>` prints `tmp_literals=0 selftest_under_tmpdir=true offline_exit=0` and exits 0.**

- `tmp_literals`: code lines (not `//` or `*` comment lines) of `scripts/freshness-sweep.mjs` at the revision that contain a `/tmp` path literal.
- `selftest_under_tmpdir`: run `node scripts/freshness-sweep.mjs --selftest` with `TMPDIR=<fresh empty dir>`, `HOME=<fresh dir>`, `KAKE_SELFTEST_DIR` unset; exit 0 and the fresh TMPDIR now contains the fixture directory.
- `offline_exit`: `node scripts/freshness-sweep.mjs --offline` exits 0 at the revision (the standing offline gate must not regress; the R15 snapshot default removal must keep the snapshot-absent branch).
- Behavioural, not textual: the kill rule is that a pure rename or a comment-only edit must NOT pass. The selftest-under-TMPDIR check is what fails a renamed literal.
- Base measurement: `tmp_literals=2 selftest_under_tmpdir=false`, exit 1 (do-nothing control).
- Sourced: the claim's TMPDIR precedence rests on S436 (Node.js `os.tmpdir()`) and S437 (Python `tempfile.gettempdir()`), both opened this round (see Frontier step).

## Frontier step (child-lane duty, not a claim)

- SOURCES: add S436 (Node.js os.tmpdir documentation) and S437 (Python tempfile documentation). Opened 2026-11-03 with one GET each; rows are appended only after the registry id-collision guard is proven (ExecCensusMirror) and the scratch mirror passes `sources-census.sh validate --file`. Expected registry 173 → 175 rows, census exit 0. Status `mined`; used-by names the round-69 lesson.
- Mistakes (mined into `corpus/lessons/round-69.md` `## Mistakes`):
  - M1 — unreproduced recorded pre-value (class: record/observed drift). Evidence: `corpus/lessons/round-67.md:54`, `corpus/lessons/round-68-verifier-spotcheck.md` §2. Captured-by: none. Fix: C1 counter (red on the base record, shown by the base run).
  - M2 — a receipt that reads a `/tmp` path: `.ufo/waves/round-68/controls/wordcounts-d3-r68.txt` ends in a traceback on `/tmp/q133.txt` (round-68 spot-check §7.3). Captured-by: none. Fix: receipt re-run against committed bytes at `.ufo/waves/round-69/controls/` (ScoutR68Receipt); the able-to-fail check is `grep -c '/tmp' .ufo/waves/round-68/controls/wordcounts-d3-r68.txt` = 1 red vs `grep -c '/tmp' .ufo/waves/round-69/controls/wordcounts-r68-rerun.txt` = 0 green.
- QUALITY criteria: one grounded criterion per mistake that no criterion caught (`LEARNING.md` §Understanding), appended to `corpus/QUALITY.md` as an end-of-file addendum citing the lesson.

## Assimilation

Decided by ConnW1 (considerthese scan, shokuknow `merge/kake/` read). Default: `Assimilation: none` unless a theme matches a round claim and passes the quarantine and id-collision rules in the operator's §10 contract.

## Round shape

- W1 (build and first design attacks): one v1 wave of 12 seats under `scripts/hyaku/ufo-wave-policy.json` (band 8–16). Attack seats in W1: reviewer, critic, mutation-tester (3 of 12 = 25 %). Connector seats: 1.
- W1R (residual falsifiers, after W1 settles and the patches are landed in scratch): ≤4 seats in one residual wave, all attack roles. Round total ≤ 16. The residual is written as its own `.ready` file.
- No planner seat (the L1 holds the planner role, per the orchestrator ruling of 2026-10-19).

## Write scope and discipline

- Writer seats (ExecC1Counter, ExecC2Fix, ExecCensusMirror) work in scratch clones under `/fast/scratch/hyaku/kake-r69/<seat>/` and deliver patch or new-file outputs into `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-69/<seat>/`. The integration owner (the L1) applies patches to the lane tree and commits through `jj-lane.sh` only.
- Non-writer seats write only new files under their own `.ufo/waves/round-69/<SeatName>/` directory and never edit tracked files.
- No seat commits, pushes, or runs a mutating git or jj command. No seat writes into the fleet root or into `/home/vgpnk/Projects/shokunin/.scratch/`.
- Every scratch tree is removed on exit; `/tmp` only for files under 50 MB.

## Amendment 1 — recorded after W1 attacks, before any after-state measurement

Recorded by the L1 on 2026-11-03 after the W1 build and attack reports
(`.ufo/waves/round-69/w1/ReviewerDesign.md`, `CriticDesign.md`, `ScoutC1Pairs.md`) and before
any after-state, residual or tip measurement. The base receipts of the pre-amendment counters
(`w1/ExecC1Counter/base-run.txt`, unamended) are kept as history. Predicates keep their sentences;
these lines define the terms they use.

C1 (frozen pair set, sha256 recorded when committed in `.ufo/waves/round-69/c1/pairs.json`):
- The set is the 20 pairs in `w1/ScoutC1Pairs/pairs-candidate.json`, unchanged in id, rev, path,
  command and recorded_value; the pairs file adds `correction_locus: corpus/lessons/round-69.md`
  and `correction_id: <pair id>` to every row. Frozen input.
- Recorded pre-value fact (corrects the contract's "known pair" sentence): the round-67 record's
  "5" reproduces at its own base `6ff73edd` (C1-01 = 5). The mismatch is the post-value: the
  round-67 record says 1 at `4b03efe1` (C1-02); observed 2 (`ScoutC1Pairs.md`).
- Relabel rule, exact: a mismatching pair is relabelled only if a line of `correction_locus` read
  at `--revision` matches `^\|\s*<correction_id>\s*\|\s*<observed integer>\s*\|` (exact id token and
  the re-derived integer). A row naming another integer, or an id that is only a substring of another
  id, relabels nothing.
- Expected base exit: 1 (`unrelabelled=1`, C1-02). Mirror kill rule: if base exits 0, C1 is unprovable.

C2:
- `tmp_literals` counts code lines (not `//` or `*` comment lines) containing a quote-adjacent
  path literal, regex `['"\`]/tmp`. Help text (line 182) and prose (line 899) are not path literals
  and are not counted. Expected base value: 2 (lines 108 and 1204).
- `offline_exit=0` is replaced by `offline_unchanged=true`: the `--offline` exit code and its
  VERDICT line at the measured revision equal those of the base revision on the same host. Reason:
  at base on this Linux host `--offline` already exits 1 (`~/projects` lowercase citation at
  `corpus/lessons/round-66-verifier-spotcheck.md:101-102` and `round-66.md:69`, unannotated and not
  pinned; ReviewerDesign F2). That red is host-bound debt routed to L0; it is not C2's to cure.
- `selftest_under_tmpdir` uses two distinct fresh directories: TMPDIR for the fixture root, HOME for
  everything else. True iff the fixture directory (`kake-r16/selftest`) appears under TMPDIR, does
  not appear under HOME, and is not a symlink (lstat).
- Output line: `tmp_literals=N selftest_under_tmpdir=true|false offline_unchanged=true|false`.
  Exit 0 iff tmp_literals==0 and selftest_under_tmpdir and offline_unchanged.
- Expected base: `tmp_literals=2 selftest_under_tmpdir=false offline_unchanged=(baseline)`, exit 1.
- Mirror kill rule: if the base already prints exit 0, the counter or its inputs are wrong; C2 unprovable.
- Known residual, named, not claimed as closed: a TMPDIR-unset fallback to `os.tmpdir()` (POSIX
  `/tmp`) is documented behaviour (S436, S437) and is not a literal; a reviewer must confirm the patch
  takes its default from `os.tmpdir()` (residual wave).

Frontier: the M2 wording is corrected: the round-68 receipt's quote-truth block ends in a
`FileNotFoundError` on `\tmp\q133.txt` (line-mid, `wordcounts-d3-r68.txt`); the file continues after it.
`grep -c '/tmp'` on that file is 1 (ReviewerDesign F6). The able-to-fail pair is unchanged.
