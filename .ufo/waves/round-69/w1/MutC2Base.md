# MutC2Base — mutation probe of the C2 predicate (round 69, kake, W1)

Base `4d188f94`. Contract: `.ufo/waves/round-69/contract.md` §C2. Scratch (deleted on exit): `/fast/scratch/hyaku/kake-r69/MutC2Base`.
Base file `scripts/freshness-sweep.mjs` sha256 `84c7554e…c6e042` (identical in lane tree and in `git show 4d188f94:`).
No counter exists at base (`.ufo/waves/round-69/` holds only `contract.md`), so the *contract sentence* was executed as the counter: `tmp_literals=0` (non-comment lines) AND `selftest_under_tmpdir=true` AND `offline_exit=0`.

## Mutants (own shared clone each, `git rev-parse --show-toplevel` asserted per copy)

| id | smallest behavior-bearing change | sha256 after |
|---|---|---|
| P | pristine base (control) | 84c7554e…c6e042 |
| M1 | `'/tm' + 'p/…'` at L108 (`R15_SNAPSHOT_DEFAULT`) and L1204 (selftest default) | a9213f39…a96519 |
| M2 | L1204 → `path.join('kake-r16','selftest')` (cwd-relative) | 9b643ab8…f5ac07 |
| M3 | dead `function __deadMutantScratchPath(){ return '/tmp/x'; }` before `main().catch` (L1681–1682, never called) | 436b27c1…af4bf8 |
| M4 | honest fix as specified: `path.join(os.tmpdir(),'kake-r16','selftest')`; `R15_SNAPSHOT_DEFAULT` deleted, `snap = env||null`, guard `if (snap && fs.existsSync(snap))` | 6c4f08f3…c2c77 |
| M3b | M4 + the same dead function (does `tmp_literals` see dead code?) | 49da2e7f…15466 |
| M4b | M4 **plus** the two *remaining* prose hits at L181 (usage text) and L898 (absent branch, `the temp root is not durable`) | c2930fb3…3b1c8 |
| M5 | M4b minus the whole r15 snapshot cross-check (absent branch **not** kept) | bf25a5b4…334f |

## Measurements

Command per revision (isolation: `TMPDIR`=<fresh>, `HOME`=<fresh>, `KAKE_SELFTEST_DIR` unset, and `/tmp` bind-replaced by an empty dir via `bwrap` so a hostile write cannot be masked by the host's `/tmp`):
`env -u KAKE_SELFTEST_DIR TMPDIR=$d/tmpdir HOME=$d/home bwrap --dev-bind / / --bind $d/iso /tmp --chdir $rep node scripts/freshness-sweep.mjs --selftest` (and the same with `--offline`).

`tmp_literals` counted three ways: **raw** (any non-comment line containing `/tmp`), **concat** (`'/tmp'` reassembled from `'…'+'…'` segments), **detC** (quoted `/tmp/<segment>` string literal — the reading the claim text describes, "lines 108 / 1204").

| rev | tmp_literals raw | detC | concat hits | selftest exit | selftest line | TMPDIR gained `kake-r16` | `/tmp` (sandbox) gained | cwd gained `kake-r16` | offline exit | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| P | 4 — L108,182,899,1204 | 2 — L108,1204 | — | 0 | 36/36 | **false** | **kake-r16** | no | 1 | reject (control) |
| M1 | 2 — L182,899 | **0** | **L108,L1204** | 0 | 36/36 | false | **kake-r16** | no | 1 | **killed** by concat scan + selftest check |
| M2 | 3 — L108,182,899 | 1 — L108 | — | 0 | 36/36 | false | — | **yes** | 1 | **killed** by selftest check |
| M3 | 5 — L108,182,899,1204,1682 | 3 — L108,1204,1682 | — | 0 | 36/36 | false | kake-r16 | no | 1 | **killed** by raw/detC scan |
| M4 | 2 — **L181, L898** | **0** | — | 0 | 36/36 | **true** | — | no | 1 | **rejected — falsification** |
| M3b | 1 — L1681 | 1 — L1681 | — | 0 | 36/36 | true | — | no | 1 | killed by raw/detC (dead code is scanned) |
| M4b | **0** | 0 | — | 0 | 36/36 | true | — | no | 1 | rejected only by `offline_exit` |
| M5 | 0 | 0 | — | 0 | 36/36 | true | — | no | 1 | indistinguishable from M4b |

Restoration: every mutant lives in its own clone; `rep/P/scripts/freshness-sweep.mjs` re-hashed after all runs = `84c7554e…c6e042`, and the lane file `kake-shokunin/scripts/freshness-sweep.mjs` is still `84c7554e…c6e042` with `git status --porcelain` empty. Lane tree never written.

## Findings

1. **FALSIFICATION — the specified honest fix (M4) is not accepted by the predicate.** `tmp_literals≠0` because two *prose* `/tmp` mentions survive it: **M4 L181** `  --selftest       hermetic fixtures under /tmp/kake-r16/selftest; prints a` and **M4 L898** `    pq12.r15Snapshot = { file: snap, skipped: 'snapshot absent (expected once landed: /tmp is not durable)' };`. Both are non-`//` code lines; L898 is a live string literal. Deleting "two sites" (L108, L1204) therefore cannot reach `tmp_literals=0`: the count has to go to 0 by editing usage text and a diagnostic string, which the claim never mentions. Required, and only reachable, via the M4b form.
2. **FALSIFICATION — `offline_exit=0` fails on every revision including pristine (P=1, M1..M5=1) and at the lane tip `dbcfef0b`** (`VERDICT: DRIFT — §paths: 1 unannotated miss · 1 NOT in pins.pathsMissSet (exit 1, partial: offline)`). Cause is pre-existing and outside C2: three unannotated cites of `~/projects` (`corpus/lessons/round-66-verifier-spotcheck.md:101,102`, `corpus/lessons/round-66.md:69`), absent from `pathsMissSet` (93 entries; also identical at base and tip). No mutant can move this conjunct, so it cannot discriminate a mutant and it makes the C2 predicate unreachable. M4 and M4b are rejected *only* by this conjunct — the honest fix is killed by a defect it does not own.
3. **The literal scan is not the gate the claim describes.** With the claim's own reading (detC) M1 scores `tmp_literals=0`, i.e. a rename passes the textual half; only the selftest-under-TMPDIR check catches it (M1 writes real `/tmp`; TMPDIR stays empty). The contract anticipates this ("the selftest-under-TMPDIR check is what fails a renamed literal") — consistent, but it means `tmp_literals=0` alone is not evidence of honesty, and any counter must keep the behavioural conjunct weighted accordingly.
4. **`tmp_literals` as "contains `/tmp`" over-counts by 2 on base** (4 vs the claimed 2) and flags dead code (M3b L1681), which is what the contract wants for M3 — but it also flags the two prose sites, i.e. it is a *textual hygiene* measure, not a root-holding measure. Prefer detC + an explicit prose exclusion, stated in the predicate.
5. **Unkilled mutation of the offline conjunct.** M5 deletes the entire r15 snapshot cross-check (the "absent branch" the claim says must be kept) and is observationally identical to M4b on all three conjuncts (`--section=armed --offline --json`: `pq12.r15Snapshot` is absent in both when the env var is unset). The predicate has no witness for "the absent branch is kept"; M5 is a surviving mutant / coverage gap.
6. Minor: M2's cwd-relative default leaves `rep/M2/kake-r16/` in the repo (fixtures are never removed for the default dir — the selftest only cleans `$HOME` fixtures), so a relative default also pollutes a tracked tree.

## Attack-wise verdicts

| attack | expected | observed | verdict |
|---|---|---|---|
| M1 rename-only | caught | caught by selftest check (and by a concat-aware scanner); detC misses it | killed (predicate honoured) |
| M2 relative path | caught | caught by selftest check (TMPDIR empty, cwd written) | killed (predicate honoured) |
| M3 dead code | caught | caught by literal scan (L1682) | killed (predicate honoured) |
| M3b dead code atop the fix | caught | caught by literal scan (L1681) | killed (predicate honoured) |
| M4 honest fix | accepted | **rejected**: `tmp_literals=2` (L181,L898) and `offline_exit=1` | **FALSIFIED** |
| M4b satisfiable honest fix | accepted | rejected by `offline_exit=1` (P also 1) | **FALSIFIED (offline conjunct)** |
| M5 absent-branch deletion | rejected | identical to M4b | **survived — coverage gap** |

## Exact commands (all exercised, exit codes recorded)

```
git clone --shared /home/vgpnk/Projects/shokunin/kake-shokunin $S/rep/<V>
git -C $S/rep/<V> checkout -q 4d188f9477b4301a2c93c8ef5c13bc6c6f4bb6e4
git -C $S/rep/<V> rev-parse --show-toplevel          # asserted == $S/rep/<V> (7/7)
diff -u rep/P/scripts/freshness-sweep.mjs rep/<V>/scripts/freshness-sweep.mjs
env -u KAKE_SELFTEST_DIR TMPDIR=$d/tmpdir HOME=$d/home bwrap --dev-bind / / --bind $d/iso /tmp \
  --chdir $S/rep/<V> node scripts/freshness-sweep.mjs --selftest      # exits 0 for all revs
env -u KAKE_SELFTEST_DIR TMPDIR=$d/tmpdir HOME=$d/home bwrap ... node scripts/freshness-sweep.mjs --offline
env -u KAKE_SELFTEST_DIR node scripts/freshness-sweep.mjs --section=armed --offline --json   # M4b, M5
env -u KAKE_SELFTEST_DIR node scripts/freshness-sweep.mjs --offline  # in $S/tip @ dbcfef0b, exit 1
sha256sum rep/*/scripts/freshness-sweep.mjs ; git -C <lane> status --porcelain -- scripts/freshness-sweep.mjs
```

Tooling: none installed or upgraded (node v24.21.0, python 3.14.8, bwrap, git already present); `pacman` untouched.
Artifacts: `.ufo/waves/round-69/w1/MutC2Base/` — `M1.patch M2.patch M3.patch M4.patch M3b.patch M4b.patch M5.patch`, `matrix.json`, `measure-isolated-tmpdir.json`, `log-P.txt log-M1.txt log-M4b.txt log-M5.txt log-tip.txt`.
Scratch `/fast/scratch/hyaku/kake-r69/MutC2Base` removed on exit.
