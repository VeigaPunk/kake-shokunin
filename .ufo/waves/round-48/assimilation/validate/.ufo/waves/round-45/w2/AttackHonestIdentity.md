# AttackHonestIdentity — honest-leg identity validation attack (kake r45 w2)

Seat: `kake-r45.AttackHonestIdentity`. Axes: operability (assigned), freshness (context).
Target: `run_honest_leg` in `.ufo/waves/round-45/c45_matrix.py` — attacked at committed
bytes sha256 `ebcccd55dcf910f87c14be5b5f8c912731d323b78ad1695284cb4321f642c63b`; the
working tree later became `2e8d9af9476736d2baaa994036c4479d87e454716621298e0ea760eef576fb6f`
(3-line `stage_fixtures` label change only). The extracted `run_honest_leg` body is
byte-identical in both (`diff` → no output; extracted sha `73680739c1e4c894…`), so the
findings apply verbatim to current bytes. Against the frozen C1 honest clause (`SCORECARD.md:3624-3667`): "still certifies the
honest round-44 cohort (all 27 controls witnessed under `--classes v5` and three build
runs met at revision `020bc457`)".

**Verdict on the named attack: SUCCEEDED — the honest-leg validation is NOT complete.**
Every one of the six checks is either self-referential or a self-report by the same
unpinned component it is supposed to validate. Three independent forgeries produce
`MATRIX_AFTER_PASS`, the cheapest in 0.084 s with zero tool executions:
(1) substituted counter (one file, no code edit to matrix/driver) — PASS;
(2) substituted driver (~25 lines) — PASS with `rows: []`, no `run-manifest.json`, no
build receipt files; (3) forged `controls-27.tsv` (27 duplicate rows, sha not the pinned
one) with the real driver and real counter — PASS. The committed wave-1 evidence is
nevertheless internally honest when forensically audited (see §6); the defect is that
the frozen counting command cannot tell the difference, so its PASS is not evidence for
the clause.

Instrument note: `lsp` is not in this seat's tool inventory; caller/definition checks were
done by direct execution/mutation of scratch copies (behavioral proof, not grep).

## 1. The six checks, cited

`c45_matrix.py` lines (read at the sha above):

| # | line | check | independent of summary? |
|---|------|-------|--------------------------|
| 1 | 120-121 | `summary.counterSha256 == sha256(COUNTER_V5)` | yes, but hashes the *same live file the driver just executed*; no pin constant |
| 2 | 122-123 | `summary.controls == 27` | no — driver's TSV row count |
| 3 | 124-125 | `summary.ok is True` | no — driver `expectation_ok` self-report |
| 4 | 126-127 | `summary.witnessed == 27` | no — driver count of semantic witnesses |
| 5 | 128-130 | `len(build)==3 and all met is True` | no — counter-receipt `met`; no revision check, build exit not required to be 0 |
| 6 | 131-132 | `not summary.errors` | no — driver-built list |

The matrix's only non-summary computation is the hash in check 1. It records
`driver_sha256` at line 164 but never compares it to anything; grep of the file for
`f3c3171b`, `5cedaa3b`, or a controls hash returns nothing. `run-manifest.json`
(nonce/started_ns/driver sha) is written by the driver and never read by the matrix.
The per-row `toolSha256` check lives *inside* the driver and is checked against the
same unpinned TSV.

## 2. Baseline (harness fidelity)

Scratch lane skeleton at `/fast/scratch/hyaku/kake-r45/AttackHonestIdentity/root`
(symlinked lane except real copies of `round-44`/`round-45`, `.git` symlink read-only),
driver pinned to committed v2 `f3c3171b…` via
`git show HEAD:.ufo/waves/round-45/c45_audit.py`:

```
$ cd /fast/scratch/hyaku/kake-r45/AttackHonestIdentity/root && time python3 -B .ufo/waves/round-45/c45_matrix.py --stage after
stage=after invalid_accepted=0 rejections_named=3 honest_witnessed=27 honest_build_met=3
MATRIX_AFTER_PASS

real	3m40.661s
BASELINE_EXIT=0
```

## 3. Attack A — counter substitution (defeats checks 1, 4, 5, and "revision")

Replaced only `rootA/.ufo/waves/round-44/c44_count_v5.py` (sha
`74978980e7afa11b…` first attempt; import-safe stub) with a stub that never runs a
tool, never calls git, reports every tool `met:false` with `caughtBy:["G1"]`, and every
`--revision` invocation `met:true`, `equalRuns "21/21"`, revision = the argv string
echoed back. Driver = committed v2 `f3c3171b…`; controls and fixtures untouched.

```
$ cd /fast/scratch/hyaku/kake-r45/AttackHonestIdentity/rootA && time python3 -B .ufo/waves/round-45/c45_matrix.py --stage after
stage=after invalid_accepted=0 rejections_named=3 honest_witnessed=27 honest_build_met=3
MATRIX_AFTER_PASS

real	0m0.477s
ATTACK_A_EXIT=0
```
receipt (`after.json`): `driver_sha256 f3c3171b…`, `honest.valid: true`,
`problems: []`, `witnessed: 27`, `build_met: 3`.
Decisive detail — the accepted summary's counter is *not* the frozen counter:

```
row receipt tools/portlen-v1.json: {'met': False, 'equalRuns': '0/21', 'seed': 1,
  'counterSha256': 'ba1c14a84e845a0251fdf2555a996b3679ef388148ecc646b87d4a60b4864f9f'}
build-1.json: {'met': True, 'revision': '020bc457', 'equalRuns': '21/21', 'seed': 1}
```
`ba1c14a8…` ≠ frozen `5cedaa3b…`, and `revision` is the short argv echo, not
`020bc4574729ed674299f6cab02faac1582d9464`; no git object was read. The matrix accepted
it because `sha256(COUNTER_V5)` is computed from the same substituted file after the
run. Check 1 authenticates self-consistency, not instrument identity; the frozen
claim's "at revision `020bc457`" is unverified (summary build rows strip `revision`
entirely, `c45_audit.py:416-417`).

Cheapest counter forgery therefore costs: one file, no validation-logic change.

## 4. Attack B2 — driver substitution (no driver-identity check)

Replaced only `rootB2/.ufo/waves/round-45/c45_audit.py` (sha
`d7438f2f1ce70e64…`) with a ~25-line fake: if `--controls` basename is
`controls-27.tsv` it writes a summary claiming `controls:27, witnessed:27, ok:true,
errors:[], build:[3× met:true]` and `counterSha256 = sha256(--counter live bytes)`;
otherwise it writes a one-row rejection naming the class matching the fixture dir.
Nothing is executed, no git, no tools.

```
$ cd /fast/scratch/hyaku/kake-r45/AttackHonestIdentity/rootB2 && time python3 -B .ufo/waves/round-45/c45_matrix.py --stage after
stage=after invalid_accepted=0 rejections_named=3 honest_witnessed=27 honest_build_met=3
MATRIX_AFTER_PASS

real	0m0.084s
ATTACK_B2_EXIT=0
```
The forged honest cohort directory contains exactly one file:

```
$ find .../runs/after/honest-3126fca435eb -type f
.../honest-3126fca435eb/after-v5-v2.json
```
i.e. no `run-manifest.json`, no `tools/`, no `build-*.json` — and the summary has
`rows: []`, `predicate: "forged"`, yet the six checks pass. The receipt records
`driver_sha256 d7438f2f…`, which is not the driver the round state and frozen claim
name, and the matrix printed PASS anyway — direct proof checks 2-6 are self-reports and
that `driver_sha256` is decorative. The same code path (lines 140-141) copied this
forged 27/3 summary over the canonical
`verification/honest-regression/after-v5-v2.json` (`1d25120b…` in scratch, predicate
"forged"), unconditionally: the copy is not guarded by `valid`.

## 5. Attack C — cohort identity forgery, real driver + real counter (check 2)

Forged `rootC/.ufo/waves/round-44/controls-27.tsv` to 27 rows (`dup01`..`dup27`) all
pointing at the single real class-diverging control
`.ufo/waves/round-44/controls-r43/portlen-v1-skip-grammar-6plus.py` with its true sha.
Driver = committed `f3c3171b…`; counter = real v5 `5cedaa3b…`.

```
$ cd /fast/scratch/hyaku/kake-r45/AttackHonestIdentity/rootC && time python3 -B .ufo/waves/round-45/c45_matrix.py --stage after
stage=after invalid_accepted=0 rejections_named=3 honest_witnessed=27 honest_build_met=3
MATRIX_AFTER_PASS

real	5m26.376s
ATTACK_C_EXIT=0
```
Honest summary: `controls 27, witnessed 27, rows 27, distinct_paths 1, distinct_names
27, classCaught_rows 27, ok True, errors []`. Forged TSV sha
`7aaf6742c948cde439c0fec26e7eab3c948a3de35888394255df9bede9b04f6b` vs pinned
`a1f0e364dad5ff937666966a16622e6895591a2eb3db714d6ecf3f3948c31bf8` (sha-guard
`before.sha256:103`). The matrix checks row *count*, never distinct identity, never the
TSV bytes; the driver's per-row sha check compares against that same file. So
"honest round-44 cohort" is not established by a PASS. (The driver's newly added
working-tree `expected_tool_sha` binding does not help: the duplicated tool sha is
genuine.)

## 6. Is the validation complete relative to the C1 honest clause?

No. The clause has four identity-bearing parts; the command verifies none of their
identity:

- "honest round-44 cohort": count 27 only; no controls sha, no distinct-path/name
  identity, no per-row TSV↔summary name check (§5).
- "all 27 controls witnessed under `--classes v5`": `witnessed` is a driver count; the
  matrix never checks `witnessedNames` length, never intersects `classCaught` with
  `classKeys`, and never checks `classesMode` (§4 forged `rows: []`).
- "three build runs met at revision `020bc457`": checks only `met is True` on three
  summary entries; revision is stripped from the summary and never read from the build
  receipts on disk; a stub echoing `"020bc457"` passes (§3).
- Named instrument (driver v2 / counter v5): the driver sha is recorded, never
  compared; the counter sha is recomputed from the executed file, so a substituted
  counter with sha `ba1c14a8…` passes (§3). Also kill-rule 1's sha guard is a separate
  artifact that no code in the counting path reads.
- Freshness: no mtime, no manifest-nonce↔summary binding; the uuid is only a directory
  name. A pre-written summary (or forged driver) is indistinguishable from a measured
  one.

Forensic counterpoint (so the disposition is not over-stated): the committed wave-1
artifacts are honest when audited directly. In
`verification/matrix/runs/after/honest-8e7184ba711d`: `build-{1,2,3}.json` all carry
`revision 020bc4574729ed674299f6cab02faac1582d9464` and `toolSha256 914ebdee7bcb…`,
which equals `git show 020bc457:scripts/sitemap_audit.py | sha256sum`
(`914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021`); 27 rows all have
non-empty `classCaught`; `run-manifest.json` has a nonce and the pinned counter/driver
shas. The honest clause holds on that evidence. The finding is about the *counting
command*: its PASS is forgeable and therefore cannot carry the clause as the frozen MET
test. Verdict recorded by the claim (NOT MET as declared) is unaffected; this attack adds
that the bounded repair's certification leg is not evidence of identity either.

## 7. Severity-ordered findings

1. HIGH — `run_honest_leg` accepts a substituted driver: PASS in 0.084 s with zero
   audits, `rows: []`, no manifest, no build receipts (§4). Driver identity is recorded
   (`c45_matrix.py:164`) and ignored; the frozen claim names driver v2, the round state
   names `f3c3171b…`, and both are unenforced.
2. HIGH — check 1 is self-referential: a substituted counter (`counterSha256 =
   ba1c14a8…`, not frozen `5cedaa3b…`) is certified honest because the matrix hashes the
   same file the driver executed (§3). This is the C1 unfalsifiability relocated into
   the honest leg, and it also leaves the driver's hash→exec window (TOCTOU) open.
3. HIGH — "build runs met at revision `020bc457`" is unverified: revision is absent from
   the summary (`c45_audit.py:416-417` strips it), build receipts are never opened, and
   the counter may ignore `--revision` (§3: short echo accepted).
4. MEDIUM — cohort identity is a count: forged 27-row TSV with one distinct control
   passes with the genuine driver and counter; the pinned controls sha (`a1f0e364…`) is
   never consulted (§5).
5. MEDIUM — `honest-regression/after-v5-v2.json` is overwritten by any V2 summary,
   including invalid or forged ones (`c45_matrix.py:140-141`, unguarded by `valid`), so
   the claim's canonical evidence file is not append-only (§4).
6. LOW/OPERABILITY — the named instruments are dirty and moving during the falsify
   wave: committed `c45_audit.py` is `f3c3171b…` (HEAD, `git show HEAD`), but the
   working tree was observed at `53a6b335…` then `6abab9ea…` during this session (mtime
   `2026-10-24 01:01:23`, `git status` ` M`, `+48/−5` vs HEAD); `c45_matrix.py` itself
   changed mid-session from `ebcccd55…` to `2e8d9af9…` (` M`, a 3-line `stage_fixtures`
   label change; `run_honest_leg` byte-identical). The counting command's PASS does not
   depend on which of these bytes ran (§4), so a rerun's receipt and the wave-1 receipt
   can disagree while both print PASS. My attacks pinned HEAD matrix bytes and HEAD
   driver bytes; the honest-leg body attacked is identical in the current working tree.
7. LOW — `c45_audit.py:load_counter` execs counter module-level code inside the driver
   process with the driver's `sys.argv`; a counter that reads `sys.argv` at import
   writes to the driver's `--out` path (observed accidentally: first stub wrote its
   receipt to `after-v5-v2.json` and the driver exited 1). Trust-boundary/robustness
   note, not a live defect with frozen v5 (defs/constants only).

## 8. Smallest corrections (recommendation, not an edit)

Pin in `run_honest_leg` and fail closed: driver sha == `f3c3171b…` (or current intended),
counter sha == `5cedaa3b…`, `controls-27.tsv` sha == `a1f0e364…`; require summary
`rows` length 27 with distinct names/paths equal to the TSV; require
`witnessedNames == [row names with non-empty classCaught]`; read each
`build-*.json` and require full `revision == 020bc4574729…` and `toolSha256 ==
git show 020bc457:scripts/sitemap_audit.py`; require `run-manifest.json` nonce and
manifest driver/counter shas to equal the summary's, and summary mtime inside the cohort
window; copy the canonical honest receipt only when `valid`.

## 9. Reproduction (scratch only)

Each attack root is the scratch skeleton (`root` layout above) with instruments pinned to
`git show HEAD:` bytes; forged artifacts and their hashes:

- counter stub: `/fast/scratch/hyaku/kake-r45/AttackHonestIdentity/stub_counter.py`
  → copied to `rootA/.ufo/waves/round-44/c44_count_v5.py`
  (`sha256 74978980e7afa11b…` at attempt 1; import-safe revision is the one that passed,
  receipt sha `ba1c14a8…` recorded in its own receipts).
- forged driver: `…/forged_driver.py` → `rootB2/.ufo/waves/round-45/c45_audit.py`
  (`sha256 d7438f2f1ce70e64…`).
- forged cohort: `rootC/.ufo/waves/round-44/controls-27.tsv`
  (`sha256 7aaf6742c948cde4…`, 27 duplicate rows; pinned `a1f0e364…`).
- drivers in every attack root: `git -C LANE show HEAD:.ufo/waves/round-45/c45_audit.py > <root>/….py`
  (`f3c3171b…`); matrix bytes are `ebcccd55…` in `root`/`rootA`/`rootC`/`rootB2`.

Rerun is exactly `cd <root> && python3 -B .ufo/waves/round-45/c45_matrix.py --stage after`
(3m40 for a genuine run; 0.1-0.5 s for attacks A/B2; 5m26 for C under load).

## 10. Residual risk / checks not run

- `--stage before` not attacked (out of scope; w1 `CriticC1Predicate.md` covers the
  predicate). Fixture reconstruction was not re-litigated; both fixture legs behaved
  identically in every scratch run.
- Not tested: hash→exec→restore TOCTOU on the counter; concurrent two-matrix runs;
  mtime-boundary falsification; real-lane mutation of any file (bounds; scratch only).
- The prepared `rootB` variant (patched driver + 27 passing-tool rows) was **not run**;
  attack B2 superseded it with a stronger, faster forgery. Reported unrun.
- The working-tree `6abab9ea…` driver (with `expected_tool_sha`) was not re-run; my
  three forgeries are orthogonal to that added binding, but a rerun at that sha is
  unmeasured here.
- One attack run (C) took 5m26 vs 3m40 baseline under host load; timing-ratio build
  `met` could flake under contention in future reruns (freshness/honest-leg fragility).
- Tool installs/updates: none.

## 11. Files written

- `.ufo/waves/round-45/w2/AttackHonestIdentity.md` (this report; **only lane write**).
  I did not modify any other lane file. `git status` at hand-off shows
  ` M .ufo/waves/round-45/c45_audit.py` and ` M .ufo/waves/round-45/c45_matrix.py`
  from another actor (present before/after my read; not touched by this seat).
- Scratch only: `/fast/scratch/hyaku/kake-r45/AttackHonestIdentity/{root,rootA,rootB,rootB2,rootC,stub_counter.py,forged_driver.py}` (roots are symlink skeletons with real `round-44`/`round-45` copies; forged artifacts as cited above).
