# CriticMistakes

Round-56 W2, lane `kake-shokunin`. Attack surface: `corpus/lessons/round-56.md` §Mistakes rows (lines 89–92) and
`corpus/QUALITY.md` §Round-56 criteria (lines 1190–1217), against `CORPUS.md` rules "a fix is shown able to fail before it
counts" and the class vocabulary (`/home/vgpnk/Projects/shokunin/CORPUS.md:173–183`). Every run below happened in a
`mktemp -d` clone of the lane at `a450e43e696d032e3ac308383f6b3394e0c92860` (toplevel == clone verified); edits were
committed there with `-c user.name=selftest -c user.email=selftest@local`; no lane file, index or jj state touched.

## RED-BEFORE CHECKS:

Controls first. Pristine tip: `python3 -B .ufo/waves/round-56/c56_selftally.py --root <clone> --revision a450e43e…` →
`tally_mismatches=0 rows_checked=10 met=True`, EXIT=0 (10/10 rows print their claimed totals). Its `--selftest` →
`c56 selftally selftest: 47/47`, exit 0 (matches the 47 in `SKILL.md:1253`). Committed base control reproduced: the tip
counter bytes at `--revision e48354b7…` print exactly `controls/base-c1-selftally-v2.txt` (byte-equal, EXIT=1, 7
mismatches) — the control is still valid after the v2 edit at `3691e96`.

1. **number-drift (`round-56.md:89`) — PASS.** Red-before committed: `controls/base-c1-selftally-v2.txt` (EXIT=1,
   `claim_ne_observed` ×6 + `selftest_failed` ×1) and `controls/base-c1-selftally.txt` (same bytes). I re-ran the named
   falsifier at the tip with **one** `SKILL.md` tally reverted to its base value (`robots-expectation-audit`
   `(204 fixtures)`→`(137 fixtures)`, clone commit `9c96b0073ab5…`): exit 1,
   `robots-expectation-audit: claim=137 observed=204/204 MISMATCH claim_ne_observed`, every other row OK. The cell is the
   only delta between this run and the green control; the counter reads no other file for this claim. Red-before exists
   for the named reason, with the fix as the only delta.
2. **stale-premise (`round-56.md:90`) — PASS.** Red-before committed: `w1/ExecPinProof.md` RUNS table — same
   `c52_quote_truth.py --selftest`, unpinned → 17/18 exit 1 at base, pinned `KAKE_R52_SELFTEST_REV=1ae8de5d4dee` → 18/18
   exit 0; the pin is the only delta. I ran the same falsifier at the counter level: tip green (18/18), and with only the
   word `KAKE_R52_SELFTEST_REV=1ae8de5d4dee ` removed from the `quote-truth-counter` row (`SKILL.md:1216`, clone commit
   `4ebfabf45a52…`) → exit 1, `quote-truth-counter: claim=18 observed=17/18 MISMATCH selftest_failed`, all nine other
   rows OK. Note the committed red-before is a direct selftest run, not the counter run; ExecPinProof says so explicitly.
3. **vacuous (`round-56.md:91`) — PARTIAL.** Red-before committed: `w1/CriticC1Contract.md` A1–A9 (each observed **exit
   0** against v1), `w1/CritCheatC1.md` e5/e6/e7/e8 (v1 `met=True`), `w1/MutC1Counter.md` (6 of 16 mutants survived the
   v1 20-check selftest). Fix = counter v2. I re-ran all six v1 survivors as exact single substitutions against the
   committed v2 selftest: M03, M07, M09, M12, M16 → exit 1 (46/47, each failing its named case); **M13 ("no clone":
   `clone = clone_at(root, rev)` → `clone = root`) → exit 0, `47/47`** — the same selftest, same verdict as before the
   fix. So one red-before state has no red-after: `contract.md:96` ("Selftest 20 -> 47 checks … includes the six mutants
   that survived v1") is false for M13, and the round-55 rule at `QUALITY.md:1183` ("a survivor becomes a selftest
   fixture in the same round") is unmet for it. M13 is operationally real: without the clone the ten documented
   commands run in the measured root's worktree, not at `--revision`, which is exactly how the base control is produced
   (`w1/ExecBaseControls.md` runs the counter from a `2d308e8` clone against base). Smallest safe correction: add
   MutC1Counter's proposed F13 case (three-commit sandbox; `measure(d, tip1)` while HEAD is `tip2`).
4. **attribution (`round-56.md:92`) — FAIL.** The row has no evidence instance ("See `settlement.md` for any W1/W2
   seat…"), no command and no exit code; its fix ("seat output not used when it names another lane's evidence") has no
   mechanism to show failing. The pointer does not resolve: `settlement.md:4–5` claims the check was "the fleet-root
   misroot sweep recorded in the report", but no round-56 report contains a misroot sweep — `grep -rn misroot` over
   `.ufo/waves/round-56/` hits only the imported `assimilation/validate/` corpus mirror; the sweep exists only as the
   unrun W2 assignment in `w2-spec.json:104`. Captured-by "settlement check" is neither a `QUALITY.md` criterion nor a
   named protocol rule, which `CORPUS.md:173–174` requires (`none` is the allowed alternative). Smallest safe
   correction: name the sweep command (`git -C <fleet> status --porcelain`) with its observed output/exit and the report
   path that carries it, or set captured-by `none` and record the row as unenforced.

## CRITERION GROUNDING:

| criterion | lesson row | falsifier command | verdict |
|---|---|---|---|
| `QUALITY.md:1190` tally = printed tally | `round-56.md:89` number-drift ✓ | `python3 -B .ufo/waves/round-56/c56_selftally.py --root . --revision <commit>` ✓ run (green at tip, red on the reverted cell) | grounded |
| `QUALITY.md:1199` HEAD-rebuilding selftest names its pin | `round-56.md:90` stale-premise ✓ (line 1202) | none named — the criterion cites `ExecPinProof.md` and the lesson's case name `env_pin_removed` but gives no argv; that case is runnable via `c56_selftally.py --selftest` | partial: lesson ✓, falsifier unnamed |
| `QUALITY.md:1203` held row pinned by body sha256 | none — grounds on `w1/CriticC2Contract.md` WR-1/A1, `CritCheatC2.md`, "counter C5 `HELD_BODY_SHA256`" | none named; a runnable one exists (`c56_quote_truth.py --selftest` carries `fail_held_body_edited`, `fail_held_row_cell_changed`, `fail_staged_name_survives`, lines 674/875/902) | gap: no lesson row, no command |
| `QUALITY.md:1207` page-unique spans | none (`w1/EntryDeletedUrl.md`, `CriticControls.md`) | none named | gap |
| `QUALITY.md:1211` staged candidate re-derived | none (`w1/ScoutClaimsAudit.md`, `ReviewerStaged.md`, `CritCheatC2.md`) | none named | gap |
| `QUALITY.md:1215` no quote from a raw-double-quote line | none (`w1/CriticC2Contract.md` A6/WR-2) | none named | gap |

Criterion 1's own falsifier is the only one the assignment can execute as written; it is also the only one that states
its green state (`tally_mismatches=0`) and its red state (the junk cases in `--selftest`). The six cases criterion 1
promises are all present in the committed selftest: `fake_command_c_only`/`fake_command_c_shadowing_honest`,
`duplicate_row_earlier`, `sum_row_padded_to_three_claims`, `command_in_other_column_shadows_selftest_cell`,
`tool_replaced_by_fake_print`/`helper_beside_script_changed`, `env_pin_removed`. I also re-tested CritCheatC1's
still-open v2 cheat e8 (command+claim in the Entry-command column, stale `137` left in Self-test): against the committed
v2 `documented_command` the claim is read from the `self-test` column only (`['137']`), and an entry-only span returns
`None` → `command_missing`; e8 is closed by the final bytes, so `contract.md:98`'s "experiments 5-8 … closed" holds for
the committed counter (CritCheatC1's 8b ran an intermediate v2).

## CLASS VOCABULARY:

Rows name `number-drift`, `stale-premise`, `vacuous`, `attribution` — all four are in the `CORPUS.md:174–176` list
(`vacuous`, `survivor`, `stale-premise`, `reference-drift`, `number-drift`, `scope`, `attribution`, `landing`,
`provider`). No class outside the vocabulary, no synonym (`stale` alone, `count-drift`) in the table. Unused members
(`survivor`, `reference-drift`, `scope`, `landing`, `provider`) are allowed; note that M13 is a *survivor* defect
reported under `vacuous` (the mutant survived the counter's selftest, not a counter verdict), which the vocabulary would
name more precisely but the class is still in-vocabulary.

## GAPS:

- **M13 red-after missing** (`contract.md:96`, `QUALITY.md:1183`, `round-56.md:91`): v2's selftest exits 0 on the
  no-clone mutant; the contract claims all six v1 survivors are included. Add the F13 three-commit case (above).
- **Attribution row unenforced** (`round-56.md:92`, `settlement.md:4–5`): no red-before, no command, pointer to an
  absent sweep; captured-by is not a QUALITY criterion or named rule.
- **Criteria 3–6 cite no lesson row** (`QUALITY.md:1203,1207,1211,1215`): each cites only W1 seat reports; the
  motivating `§Mistakes` row is never named, so a reader cannot tie the criterion to the mistake it prevents.
- **Criteria 2–6 name no falsifier command** (`QUALITY.md:1199–1217`): only criterion 1 has a `Falsifier:` line with
  argv. Criteria 3–6 do name constants/files that imply a command, but not a runnable one; criterion 2's case
  `env_pin_removed` is named only in the lesson row's Fix, not in the criterion.
- **Control receipt is not self-binding** (`controls/base-c1-selftally-v2.txt`): no argv, no counter sha256, no
  population digest. It also is byte-identical to `base-c1-selftally.txt` (both sha256
  `155ab35c7c5808c0100b7fad121d22a39f6fb3cdcab7346a5385d45972b7bfb6`), so the file cannot show it was a v2 re-run
  rather than a copy. I closed the question for this revision by re-running the final counter bytes (byte-equal), but
  the artifact itself fails the "Replayable claim" bar (`QUALITY.md:10`, exact argv + digest). Smallest safe correction:
  append the argv and the counter's sha256 to the receipt, or cite the counter blob in criterion 1.
- Not a gap, verified: the C2 half of the vacuous fix has red cases (`fail_held_body_edited`,
  `fail_held_row_cell_changed`, `fail_staged_name_survives`) and the pinned rows' tallies match their commands
  (47/47 and the ten green rows at the tip).

VERDICT: 2 of 4 mistake rows (number-drift, stale-premise) have a committed red-before reproduced green→red with the fix as the only delta; vacuous is partial (M13 survives v2's selftest, contradicting contract.md:96); attribution has no red-before or resolving pointer; all four classes are in-vocabulary; criteria 3–6 cite no lesson row and criteria 2–6 name no runnable falsifier.
