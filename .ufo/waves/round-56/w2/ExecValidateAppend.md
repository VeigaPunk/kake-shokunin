# ExecValidateAppend

Scope: re-run the round-56 append validation in my own clone of the lane tip and diff the regenerated receipts/mirror against
the committed ones; judge C7 readiness. Nothing ran inside the lane: the lane's tracked tree is clean and
`.ufo/waves/round-56/assimilation/validate/census-stdout.txt` still carries mtime 19:46:03.

Facts: lane tip `7ad7db51dfcff2eccea9f7f73726f2437b2ed8de` (W2 spec/dispatch), revision under attack
`a450e43e696d032e3ac308383f6b3394e0c92860`, base `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`, round date 2026-10-25.
Clone `D=/tmp/kake-validate-clone-swuuivut` (`git -C $D rev-parse --show-toplevel` == `$D`); committed-mirror snapshot `$R`
taken with `git archive` before regeneration (the script `rm -rf`s the directory). No tool installed (pacman paused, none needed).

## COMMANDS:

1. `D=$(mktemp -d); git clone -q --no-checkout <lane> "$D"; git -C "$D" checkout -q 7ad7db51dfcff2eccea9f7f73726f2437b2ed8de`.
2. `git -C "$D" archive 7ad7db51 .ufo/waves/round-56/assimilation/validate | tar -x -C "$R"` — the committed receipts.
3. Adapted runner: `validate_append.sh` copied to `$R/validate_append.adapted.sh`; the only edit is line 6 `LANE=<clone>`
   (verified: normalizing that one line reproduces the lane script byte-for-byte). `bash $R/validate_append.adapted.sh`
   → rc 0, stdout `exit=0` + `file<TAB>ok<TAB><clone>/…/assimilation/validate/corpus/SOURCES.md`.
4. Diff: `cmp`/`sha256sum`/`difflib.unified_diff` per file, plus whole-tree member-set and content diff of `$R/.ufo/.../validate`
   vs `$D/.ufo/.../validate`.
5. Census cross-checks in the clone: mirror form (step 3); direct `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
   validate --file corpus/SOURCES.md` (rc 0); contract form `… validate --root /home/vgpnk/Projects/shokunin kake` (rc 0).
6. C7 cross-check (read-only, not this seat's claim): `python3 -B .ufo/waves/round-56/c56_quote_truth.py --root . --revision
   <rev> --json` at `a450e43` and at tip.
7. C7 mutant sweep: 12 single-file mutants, each committed inside the clone (`-c user.name=selftest -c user.email=selftest@local`),
   counter re-run at that mutant commit, then `git reset --hard <tip>`; clone restored to tip. No lane index, jj or file mutation.

## DIFFS:

| artifact | committed sha256 | fresh sha256 | verdict |
|---|---|---|---|
| `census-argv.txt` | `1191215f2a32d3396063…` | `1191215f2a32d3396063…` | byte-equal |
| `census-stdout.txt` | `906768171b7c9f24ab23…` | `f466b7823440fbe0ddcc…` | equal except one path line |
| `census-exit.txt` | `19eaf43821a7660ec323…` | `19eaf43821a7660ec323…` | byte-equal (`exit=0`) |
| `census-stderr.txt` | `e3b0c44298fc1c149afb…` | `e3b0c44298fc1c149afb…` | byte-equal (empty) |
| mirror `corpus/SOURCES.md` | `483b5d1341f52b043c3a…` | `483b5d1341f52b043c3a…` | byte-equal, and byte-equal to tip `corpus/SOURCES.md` |
| `yahoo-japan-link-target-crawl-restriction.md` | `85f234bf1ed49e32d599…` | `85f234bf1ed49e32d599…` | byte-equal (also == tip) |
| `yahoo-japan-deleted-url-recrawl.md` | `82c08f69c35b2df906e2…` | `82c08f69c35b2df906e2…` | byte-equal (also == tip) |
| `yahoo-japan-nonexistent-url-recrawl.md` | `9dc271a6537bf5c0c059…` | `9dc271a6537bf5c0c059…` | byte-equal (also == tip) |

- **F1 receipt reproducibility** (attacks `validate_append.sh:14-17` and C7's byte-equality clauses): the committed receipts are
  byte-equal to a fresh run, and `census-argv.txt` is *exactly* equal, not merely path-normalized — line 8/14 write `V` relative,
  so the receipt embeds no tree path at all (only the fleet path `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, outside
  the lane). `census-stdout.txt` has 15 lines both times; the 14 `W04` lines are identical (S033, S088, S092, S098, S099, S102,
  S110, S111, S115, S116, S117, S127, S416, S417); line 15 differs only in the `realpath` of the registry
  (`sources-census.sh:500`): `<lane>/…` committed vs `<clone>/…` fresh. Normalized (root → `<ROOT>`) the files are equal.
  The committed receipts were produced at commit `d5afc48` and the registry blob is the same `30d4bbcc…` at `d5afc48`,
  `a450e43` and tip, so the equality is a property of the registry, not a coincidence of the tip.
- **F2 the mirror is not a tip snapshot** (attacks committed `assimilation/validate/SKILL.md` and
  `assimilation/validate/corpus/QUALITY.md`, against the re-run rule at `validate_append.sh:2-3`): both are the `d5afc48`
  copies; at `a450e43` tip `SKILL.md` gained 20 lines ("### Round 56 gate registry additions") and `corpus/QUALITY.md` gained
  31 lines ("## Round-56 criteria"). A re-run at tip therefore rewrites them: the clone's `git status` after step 3 shows exactly
  `M validate/SKILL.md`, `M validate/corpus/QUALITY.md`, `M validate/census-stdout.txt`. Not a C7 failure — the census reads only
  the registry and used-by *existence* (`sources-census.sh:567`), so companion content is inert and the receipts stay byte-equal —
  but if the L1 re-runs the script in the lane for W2, exactly those two mirror files go dirty, and the committed mirror stays a
  `d5afc48` snapshot until re-committed.
- **F3 the script does not propagate the gate's exit status** (attacks `validate_append.sh:18`): the last command is `tail -2`, so
  the script's own status is tail's 0. Demonstrated in the clone: with a deliberately broken working-tree registry the census wrote
  `exit=1` (`file<TAB>E12<TAB>S999 row outside Registry section`) while the script still returned rc 0. C7 reads
  `census-exit.txt`, not the script rc, so the claim is unaffected; the risk is a caller keying on the script's status.
- **F4 registry equality and used-by coverage**: the validated registry is byte-equal to `corpus/SOURCES.md` at tip
  (`483b5d13…`, 147221 bytes, 158 rows = base 156 + S419 + S420, none removed). Of 63 distinct used-by cell values, 61 are paths
  (56 under `corpus/`, 5 outside) and 2 are the no-target markers `-`/`—`; all 61 resolve inside the fresh mirror, and the 5
  non-corpus paths are exactly the copy list at `validate_append.sh:11-13` — no latent E11 for the current registry. The 14 `W04`
  ids all pre-exist at base (independently matches `.ufo/waves/round-56/w2/ExecCensus.md`), so the append introduced no warning.

## C7 READINESS:

All eight C7 clauses (`c56_quote_truth.py:467-504`) hold on the tip evidence, and identically at the revision under attack: the
validate dir is byte-identical between `a450e43` and tip (`git diff --stat a450e43 tip -- corpus/SOURCES.md <3 entries>
.ufo/waves/round-56/assimilation` is empty).

| C7 clause | evidence |
|---|---|
| argv names `--file` and the scratch registry, not `--root` | token `--file`, target `.ufo/waves/round-56/assimilation/validate/corpus/SOURCES.md` == `VALIDATE_REG` exactly; no `--root` |
| argv runs `sources-census.sh` | yes, fleet path |
| exit 0 | `census-exit.txt` = `exit=0` |
| no E03/E04 | stdout carries 14 `W04` warnings only, no E-codes |
| last stdout line `file<TAB>ok<TAB><registry>` | line 15, path ends `/assimilation/validate/corpus/SOURCES.md` |
| scratch registry byte-equal to landed | `483b5d13…` == tip `corpus/SOURCES.md` |
| three scratch entries byte-equal to landed | `85f234bf…` / `82c08f69…` / `9dc271a6…` |

- Counter cross-check: `c56_quote_truth.py --root . --revision a450e43e696d032e3ac308383f6b3394e0c92860 --json` → exit 0,
  `conditions_passed 8`, `met true`, `C7_validate_before_append` pass; same at tip `7ad7db51`. C7 passes today; the other seven
  conditions belong to other seats.
- C7 mutant sensitivity (12 committed mutants, one per commit; counter re-run each time). Killed — C7 false, 7/8 — by: `exit=1`;
  scratch registry +1 byte; scratch entry S419 +1 line; scratch entry S367 +1 line; landed registry +1 byte; argv `--file`→`--root`;
  argv carrying both `--root` and `--file`; argv target retargeted to `corpus/SOURCES.md`; argv script swapped away from
  `sources-census.sh`; stdout +`E04` line; stdout emptied. Survived: the `ok` line's root replaced with a foreign tree
  (`/x/y/…/validate/corpus/SOURCES.md`) — the clause accepts any path whose suffix is `VALIDATE_REG`, so C7 cannot tell which tree
  produced the receipt. That matches the declared scope ("a receipt check, not proof that the run happened") and is why my clone's
  `ok` line is C7-equivalent to the committed lane line.
- Readiness for an L1 re-run in the lane: the gate is clean and reproducible, so a re-run is safe, but it will dirty
  `validate/SKILL.md`, `validate/corpus/QUALITY.md` and the `ok` path line in `validate/census-stdout.txt` (F2) and its own exit
  status is always 0 (F3) — read `census-exit.txt`, not the script rc.

VERDICT: committed append receipts are byte-equal to a fresh clone run of the tip (argv exactly, exit/stderr exactly, stdout only in the resolved registry path) and the validated registry is byte-equal to tip `corpus/SOURCES.md` (158 rows); C7 passes 8/8 at `a450e43` and tip, with two non-blocking hygiene findings (stale mirror companions SKILL.md/QUALITY.md, no exit-status propagation in `validate_append.sh:18`).
