# ExecC2Fix — round 69 W1, C2 build seat

Writer seat. Repaired `scripts/freshness-sweep.mjs` and wrote the C2 counter in a scratch clone
(`/fast/scratch/hyaku/kake-r69/ExecC2Fix/clone`, `--shared` from the lane, checkout `4d188f94`).
Applied **amendment 1** terms (L1 amendment message + `contract.md` §Amendment 1).

- Base: `4d188f9477b4301a2c93c8ef5c13bc6c6f4bb6e4` (lane `master` at round open).
- AFTER clone commit: `35025609a1f9bf9eadcd3d10eaf0c8a632b48152` (`-c user.name=kake-seat -c user.email=seat@fixture`).
- Nothing was committed/added/stashed/checked-out in the lane; the lane's tracked bytes are unchanged
  (`M .ufo/waves/round-69/contract.md` is the L1's own amendment, not mine).

## Patch (2 code sites + the two texts they name; no other logic)

| site | base | after |
| --- | --- | --- |
| ~108 `R15_SNAPSHOT_DEFAULT` | `'/tmp/kake-r15/charter-live.html'` | constant deleted; `const snap = process.env.KAKE_R15_SNAPSHOT` only |
| ~890 snapshot guard | `if (fs.existsSync(snap))` | `if (snap && fs.existsSync(snap))` — absent-env now takes the existing skipped branch instead of a doomed `existsSync` on a literal |
| ~899 skipped message | `'… once landed: /tmp is not durable'` | `'snapshot absent (no env override; the r15 capture was a temp file and is not durable)'` (same meaning, no `/tmp`); `file` reports `(no KAKE_R15_SNAPSHOT)` |
| ~1204 selftest dir | `process.env.KAKE_SELFTEST_DIR \|\| '/tmp/kake-r16/selftest'` | `process.env.KAKE_SELFTEST_DIR \|\| path.join(os.tmpdir(), 'kake-r16', 'selftest')` |
| ~20 top comment, ~182 help | name the `/tmp` default | name `$TMPDIR/kake-r16/selftest` (or `$KAKE_SELFTEST_DIR`) |

`os` and `path` were already imported (lines 39–40); no import was added. Mechanism kept: the env
override still wins, and only the built-in path is gone.

## Measured (all on committed bytes, `git archive`d into scratch; never the working tree)

`--selftest` with distinct fresh TMPDIR/HOME, `KAKE_SELFTEST_DIR` unset, `/tmp/kake-r16` cleared first:
base 36/36 exit 0 but fixture lands in **/tmp/kake-r16** (TMPDIR: no) · after 36/36 exit 0, fixture
under **TMPDIR** (real /tmp untouched). `--offline`: exit 1 + identical VERDICT at both endpoints.

Counter, `--root … --revision … --work …`:
- base `4d188f94`: `tmp_literals=2 selftest_under_tmpdir=false offline_unchanged=true`, exit **1**
- after `35025609`: `tmp_literals=0 selftest_under_tmpdir=true offline_unchanged=true`, exit **0**

Literal regex `['"\`]/tmp` on non-comment lines gives exactly the amendment's base value 2
(lines 108, 1204) and 0 after; `grep -n '/tmp'` on the after file exits 1 (no match anywhere).

## Attacks run (all rejected)

- **M1 rename-only** (`'/tm'+'p/…'`, same destination): literals 0 but `selftest_under_tmpdir=false` → exit 1.
- **M2 relative path** (`path.join('kake-r16','selftest')`): literals 0, placement false → exit 1.
- **M3 dead-code literal** (honest fix + unreachable `'/tmp/never-used'`): literals 2 → exit 1.
- **M4 symlinked fixture root**: rejected. `fixture_placement()` unit probe: real-under-TMPDIR accepted;
  symlink-under-TMPDIR rejected (lstat); only-under-HOME rejected.
- Kill rule holds: base exits 1 (not vacuous). Patch neutrality proven two ways — unrepaired outputs
  byte-identical base vs after; with a scratch-only sidecar+pin repair both exit 0, `VERDICT: OK`, identical.
- 36/36 selftest preserved at both endpoints (the e2 write-confinement mutation proof still passes);
  `node --check` exit 0; snapshot cross-check still fires when `KAKE_R15_SNAPSHOT` is set (MISMATCH → ANOMALY).

## Retained evidence

`.ufo/waves/round-69/w1/ExecC2Fix/`: `patch.diff` (base→after, `git apply --check` clean and reproduces
the after blob byte-for-byte, sha256 `4bd99b04…`), `c69_tmp_honour.py` (byte-identical to the measured
file), `measure.txt` (every command, exit code and output above).

## Risks / blockers

1. **`offline_unchanged` is a no-regression reading, not a green gate.** At base on this host
   `--offline` is already exit 1 (lowercase `~/projects` cites at `corpus/lessons/round-66-verifier-spotcheck.md:101,102`
   and `round-66.md:69`, unannotated and unpinned). Confirmed pre-existing across `a26fd6a5 · f2b9e081 ·
   4b03efe1 · 39612819 · d69b720b · 4d188f94` (all exit 1). Per amendment 1 this is host debt routed to L0;
   my patch neither introduces nor masks it (verified both with and without a scratch-only data repair).
2. The comparison is VERDICT-text equality, so an after-tip that adds a *different* fault also reads
   "unchanged". Probed with a synthetic round-69 lesson: no movement. This limit is inherent to the
   amended predicate, not to the counter's implementation.
3. Residual named by the amendment, not closed: TMPDIR-unset falls back to `os.tmpdir()` (POSIX `/tmp`);
   the patch does take its default from `os.tmpdir()`.
4. Disclosed side effect: a discriminating run/cleanup removed `/tmp/kake-r16` on this host (it was
   recreated by base runs and is recreated by any `--selftest`). No lane, fleet-root or sibling-scratch
   bytes touched.
5. No tool installs or upgrades were needed (node v24.21.0, Python 3.14.8). Scratch tree removed.
