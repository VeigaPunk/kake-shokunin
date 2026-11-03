# Round 69 W1 — CriticDesign: adversarial pre-data critique of C2 + S436/S437

Base blob read via `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4d188f94:scripts/freshness-sweep.mjs` and a scratch clone (`git rev-parse HEAD` = 4d188f94…, `--show-toplevel` asserted). Node v24.21.0, Python 3.14.8. Line numbers below are base-blob lines. Receipts: `.ufo/waves/round-69/w1/CriticDesign/`. No tools installed (none needed); pacman untouched. Scratch removed on exit.

## (1) Minimal diff satisfying the frozen C2 triple while not honouring TMPDIR — verdict: honest diff EXISTS; frozen text alone admits wrong-reason passes

Honest minimal diff (paper; ~5 lines, no new write APIs so writeConfinement case e stays green):
- `:1204` `process.env.KAKE_SELFTEST_DIR || '/tmp/kake-r16/selftest'` → `|| path.join(os.tmpdir(), 'kake-r16', 'selftest')` (`os` already imported `:38`).
- `:108` delete `R15_SNAPSHOT_DEFAULT`; `:890` → `const snap = process.env.KAKE_R15_SNAPSHOT;` with null-tolerant `if (snap && fs.existsSync(snap))`; reword `:899` `'/tmp is not durable'` and `:182` help text `under /tmp/kake-r16/selftest` (residual text would either count as literals or become doc drift).

tmp_literals definition defect — '/tmp' census at base: `:20`,`:103` are `//` comments; `:108` code; `:182` is INSIDE the `usage()` template literal (runtime-evaluated code, printed by `--help`); `:899` code (`/tmp is` — not a path); `:1204` code. The frozen wording "code lines (not `//`/`*` comments) containing a `/tmp` path literal" plainly counts `:182` → base 3, or with bare-substring matching also `:899` → base 4; only a quote-adjacent reading (`['"\`]/tmp/`) yields exactly {108,1204}=2 as frozen. Correction: counter regex must be quote-adjacent; honest patch must reword `:182`/`:899`.

Attacks (paper diffs to `:1204` unless stated; verdict against the frozen triple):
- A rename to `/var/tmp/…`: tmp_literals≥1 AND selftest false → CAUGHT twice.
- B obfuscated `'/tm'+'p/kake-r16/selftest'`: tmp_literals=0 but fresh TMPDIR stays empty → CAUGHT (the kill rule's behavioural check works).
- C HOME-redirect `path.join(os.homedir(),'kake-r16','selftest')`: tmp_literals=0; fixture persists under HOME (measured: selftest never cleans `dir`; only the $HOME probe fixture, which it deletes pre-exit — measured selhome 0 entries after). PASSES IFF counter conflates HOME≡TMPDIR; contract says "TMPDIR=<fresh empty dir>, HOME=<fresh dir>", not "distinct". Correction: two distinct fresh dirs + assert HOME has no new entries after.
- D direct-read `process.env.KAKE_SELFTEST_DIR || process.env.TMPDIR || '/tm'+'p/…'`: all three green while a /tmp root remains for TMPDIR-unset hosts; diverges from S436 under `TMPDIR=''` (measured: os.tmpdir()→`/tmp`; raw read → relative path → fixture in CWD). Passes the claim's letter ("honours TMPDIR"); only patch review (require os.tmpdir()) closes it.
- E symlink laundering: obfuscated real dir + `fs.symlinkSync(real, TMPDIR/kake-r16)` placed inside a SELFTEST-WRITES region (`symlinkSync` is in writeConfinement's covered list `:1147/:1193`, so case e stays green) → naive `os.path.isdir` counter follows the link → all green, data still rooted in /tmp. Not minimal, but the predicate cannot reject it. Correction: counter lstats new entries (reject symlinks; realpath under realpath(TMPDIR)).
- F pre-existing dir: "fresh empty" + "now contains" requires snapshot-before/diff-after with ≥1 NEW entry; a TMPDIR reused across base/tip runs false-greens tip.
Verdict (1): honest diff exists (so C2 is actionable); counter MUST pin distinct fresh HOME/TMPDIR, before/after diff, lstat-not-follow, quote-adjacent literal regex.

## (2) offline_exit=0 at base — verdict: UNSATISFIABLE as frozen; measured exit 1 at base in two environments

Commands run in the base clone (receipts `offline-clean-exit1.txt`, `offline-ambient-exit1.txt`, `armed-offline-exit0.txt`):
- `env -i PATH=/usr/bin:/bin:/usr/local/bin HOME=$S/offhome TMPDIR=$S/offtmp node scripts/freshness-sweep.mjs --offline` → `VERDICT: DRIFT — §paths: 2 unannotated miss · 3 NOT in pins.pathsMissSet`, EXIT=1 (`~/Projects` 8 cites + `~/projects` 3 cites: round-66-verifier-spotcheck.md:101,102, round-66.md:69; fresh HOME lacks ~/Projects).
- Same with ambient env → EXIT=1; drift 1: `~/projects` (3 cites; `/home/vgpnk/projects` absent, case-sensitive; pins round 67/2026-11-01 show set-delta +3 new lesson files).
- `node scripts/freshness-sweep.mjs --section=armed --offline` → `VERDICT: OK (exit 0)`, EXIT=0, twice.

offline_exit is dominated by §paths corpus state the C2 patch cannot touch; after an honest C2 diff the tip still prints offline_exit=1 → triple unmeetable. Wrong-reason catalogue:
1. Unreachable target: needs a pins re-baseline or corpus annotation — outside C2. Smallest safe correction: scope the probe to `--section=armed --offline` (measured 0 at base, a genuine offline regression smoke) or redefine offline_exit as no-regression vs base (record base value).
2. Dead branch: under `--offline`, `sectionArmed` returns at `:833-841` BEFORE the R15 snapshot cross-check (`:890-900`) — `R15_SNAPSHOT_DEFAULT` is never read offline. offline_exit=0 proves NOTHING about "the R15 snapshot default removal must keep the snapshot-absent branch"; deleting the whole cross-check leaves offline_exit unchanged. Receipt must not claim snapshot-branch coverage; that branch is review-covered only.
3. Env leakage: repo candidates include `KAKE_REPO_ROOT` (`:195`), pins include `KAKE_FRESHNESS_PINS` (`:207`), §history canonical path sits under `os.homedir()` (`:121`), probe-delta child inherits full env (`:1213`). Counter must run under `env -i` (proven workable above).
4. Gutted gate: exit-code-only read; a try/catch→exit-0 patch passes identically — patch review must cover.
5. §history dependence: if webzites is ever restored on a host, §history could drift and flip offline_exit for C2-irrelevant reasons (suspended here in both envs — measured).

## (3) S436/S437 — verdict: ground the knob and the primitive only; prove neither the tool's behaviour nor C2; the two sources differ

- S436 (Node os.tmpdir, mirror `S436-node-os.html:495-497`): "TMPDIR, TMP and TEMP … checked … in the described order … defaults to `/tmp`". Proves: TMPDIR is the first documented override of the primitive an honest patch should use, and why the counter sets TMPDIR. Does NOT prove: the patch uses os.tmpdir() (attack D passes behaviourally without it and is observably different under `TMPDIR=''`); no existence/usability promise (measured v24.21.0: returns nonexistent `probe/no-such` verbatim — counter must pre-create the fresh TMPDIR or selftest's mkdirSync fails for the wrong reason); nothing about literals (tmp_literals is textual).
- S437 (Python tempfile, mirror `S437-python-tempfile.html:510-513`): candidates TMPDIR, TEMP, TMP, platform — tail order TEMP-before-TMP differs from Node's TMP-before-TEMP (harmless here: only TMPDIR is set; but the sources are not interchangeable statements of one precedence). Measured Python 3.14.8: TMPDIR nonexistent → `/tmp`; TMPDIR read-only → `/tmp` — Python silently skips unusable candidates; Node returns env verbatim. S437 supports only "TMPDIR is the conventional cross-toolchain knob", not any claim about this Node tool; citing it as proof the tool honours TMPDIR would be false provenance. The behavioural proof is selftest_under_tmpdir itself plus patch review.
- Status: `grep -r "S43[67]" corpus/` → no matches (rows not yet appended); mirrors exist under `w1/ScoutSources/sources/`; quotes above are from the mirrors.

## Verdicts
1. Honest minimal diff EXISTS; frozen text needs the four counter pins (distinct dirs, before/after diff, lstat, quoted-literal regex) to reject C/D/E/F.
2. offline_exit=0 as frozen is unsatisfiable (measured 1, clean + ambient); smallest correction: `--section=armed --offline` scope or no-regression semantics; drop snapshot-branch coverage from the offline check (dead under `--offline`).
3. S436/S437 ground the knob choice and os.tmpdir() as the honest primitive; they document different precedence tails and different failure semantics (measured); they prove nothing about the tool's actual behaviour.

Receipts: `armed-offline-exit0.txt`, `selftest-base-exit0.txt` (exit 0; fixture tree persists in KAKE_SELFTEST_DIR; TMPDIR/HOME 0 entries after), `offline-clean-exit1.txt`, `offline-ambient-exit1.txt`, `env-probes.txt`.
