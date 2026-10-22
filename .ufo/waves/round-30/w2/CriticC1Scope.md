# KakeR30.CriticC1Scope: does "the round-27 failure families left open by round 28 are repaired" overclaim?

Seat: leaf critic, wave 2 (falsify), axis operability. The attacked item is the C1 wording in `SCORECARD.md:689` (declaration `4580c78`), repeated in `corpus/lessons/round-30.md:10-12` and `:84-87`. Lane tip `451e98f`; `git log 71c6bfa..master -- scripts/` is empty, so the gate measured is `git show 71c6bfa:scripts/citing_set.py` (sha256 `dbfade45…7f02`); base gate `0356681` (sha256 `d7e79ba1…9d48`). Sandbox `/fast/scratch/hyaku/kake-r30/w2/CriticC1Scope/` (TMPDIR there). No network, no installs, no lane writes other than this file. Python 3.14.8.

## Verdict

**Overclaim, fixable by disclosure.** Round 28 named its left-open set explicitly. Its declaration says "Duplicate-key and nonfinite JSON profiles, identity-path spelling and retention boundaries are outside C1 and stay open" (`SCORECARD.md:593-596`; also `corpus/lessons/round-28.md:122-124`). Round 30 repairs the first two and the sub-items of round-28 routed defect 2 (`round-28-verifier-spotcheck.md:216-222`). It leaves identity-path spelling and both retention families untouched, and no round-30 text says so. The 14/14 measure is not in question: the counter F01–F06 checks exactly the routed-defect-2 items. The unqualified family-level wording is what overreaches. The literal phrase "repaired in `scripts/citing_set.py`" also cannot cover the retention families, because their code is `.ufo/waves/round-27/fetch_group.py` (`round-27/w2/ReviewRetentionBoundary.md:32`, `ReviewInputSafety.md:54`).

## Per-family outcome (all ids in `.ufo/waves/round-27/unresolved-acceptance.json`)

| Round-27 family | Left open by round 28? | Status at `71c6bfa` | Round-30 text |
|---|---|---|---|
| JSON-PROTOCOL: duplicate keys, non-finite | yes (`SCORECARD.md:594-595`) | **repaired**: duplicate keys, NaN and `1e999` give exit 2 with `document_duplicate_key` / `document_nonfinite_number`; base gives exit 0 `clean` | claimed (F01, F02) |
| JSON-PROTOCOL: stack-dependent depth limit | yes (`round-28.md:114-115`) | deep JSON (depth 100000) returns JSON, exit 2, `document_not_json`; the stack-size dependence was **not exercised** | not mentioned |
| CLI-SCOPE-FALSE-GREEN: `S01`-style ids | yes (`round-28.md:97-98`) | **repaired**: population `S01`,`S02` gives exit 2 `population_id_unreachable` (base: exit 0 `clean`) | claimed (F03) |
| CLI-SCOPE-FALSE-GREEN: repeated options (round-27 `w2/CliUsage.md:34-45`) | yes | **repaired** for `--root` twice (exit 64, usage JSON; base: exit 0 `clean`); other spellings rest on the strict receipt, not re-run here | claimed (F04) |
| IDENTITY-PATHS | yes (`SCORECARD.md:595` "identity-path spelling") | **still open**: see probes I1–I3; output is byte-for-byte the same at base and at `71c6bfa` | **still open and not disclosed** |
| RETENTION-FRAGMENT | yes (`SCORECARD.md:595-596`) | **still open**: `fetch_group.py` is not touched by round 30 | **not disclosed** in round 30 (only round-27 history at `SKILL.md:670`, `QUALITY.md:288`) |
| RETENTION-TRUST-BOUNDARY | yes (same) | **still open**: same code, untouched | **not disclosed** in round 30 |
| ORACLE-GRANULARITY | not named by round 28, not repaired by it | **partly repaired**: the runner now compares (id, reason); rows, files and counts are still not compared | **open and disclosed**: `round-30.md:22-24` ("Rows, files and counts are not compared by the runner") |
| C1-UNIT-OVERRIDE (7 unknown units) | yes (`round-28.md:125-126` "unchanged") | **still open**: it concerns the round-27 counter and ledger, not the gate | not disclosed in round 30 |
| CLI-FIFO | no: repaired by round 28 (`document_not_regular_file`) | holds | n/a |
| C2-CONSTANT-PREDICATE | no: turned into a criterion in round 28 (`round-28-verifier-spotcheck.md:191-196`) | criterion holds; round 30 uses constant stubs | n/a |

Two further round-28 residual findings, recorded in the same open-findings bullet as `O_NOCTTY` (`round-28.md:111-115`): "a socket is labelled unreadable" is **still open and not disclosed** (probe R1). The deep-corpus and `O_NOCTTY` items are claimed repaired; I did not re-run them.

## False provenance (minor)

`SCORECARD.md:701-702` ("F01–F06 are the round-27 families") and `PROVINCE.md:103-106` ("the round-27 input families (… deep corpus, `O_NOCTTY`)") label F05 and F06 as round-27 families. Neither appears in `unresolved-acceptance.json` or in any round-27 report (`rg -i 'NOCTTY|recursive walk' .ufo/waves/round-27` finds no match). Round 28's own seats found both as pre-existing defects (`round-28/w1a3/ReviewCorpusMissingEmpty.md:22`, `ReviewNonBlockingRead.md:31`), and round 29 grouped them under routed defect 2 (`round-29.md:118-122`). F05 and F06 should be credited as round-28 findings.

## Counterexamples (probe `/fast/scratch/hyaku/kake-r30/w2/CriticC1Scope/probe_identity.py`, sha256 `81f57952…15b0`)

Command: `TMPDIR=$S/tmp python3 -B probe_identity.py <gate> $S/work` against both exported gates. Exit 0 both times; the per-probe results are identical at `71c6bfa` and `0356681`:

- **I1 (identity-path, outside-population row).** Population `S001`; the ledger adjudicates `S001` and `S019` on one cited file. Observed: exit 1, `ledger_pair_not_cited` with `row: "19"`, so the `S` prefix is lost. Cause: the fallback `str(key[1])` at `citing_set.py@71c6bfa:713,725,738`.
- **I2 (identity-path, backslash filename).** The corpus file is `corpus/knowledge/back\slash.md` and the ledger names it exactly. Observed: exit 1 with two findings, `ledger_pair_not_cited` with file `back/slash.md` and `unadjudicated_citing_pair` with file `back\slash.md`. This is an unfixable false red. Cause: `normalize_ledger_file` rewrites `\` to `/` on the ledger side only (`:246-252`).
- **I3 (identity-path, duplicate slash).** The ledger names `corpus/knowledge//a.md` for a real cited `a.md`. Observed: exit 1 with two findings for one file, a double false positive. Cause: `normalize_ledger_file` does not collapse empty segments, while `normalize_relative` does (`:231-243`).
- **R1 (socket as ledger document).** Observed: exit 2 with reason `document_unreadable`, not `document_not_regular_file`. Cause: `os.open` on a socket fails before the `S_ISREG` check (`:290-296`).
- **R2 (ledger JSON 100000 levels deep).** Observed: exit 2 with `document_not_json`, JSON on stdout and no traceback. This holds.

Inline spot-check of the claimed families, under `$S/work2/k`, against both gates:
- At `71c6bfa`: `S01` ids give exit 2 `population_id_unreachable`; a duplicate member gives exit 2 `document_duplicate_key`; NaN and `1e999` each give exit 2 `document_nonfinite_number`; `--root /nonexistent --root <tree>` gives exit 64 with the usage JSON.
- At base: all five give exit 0 `clean`.

## Impacted axes

- **Operability:** the claim scope is accurate for F01–F06 but overstated at the family level. Three gate defects (I1–I3) and one wrong reason label (R1) remain live.
- **Calibration and provenance:** retention is presented as repaired by omission. F05 and F06 are mislabelled as round-27 families.
- **Not impacted:** the declared measure. The 14/14 and 6/6 receipts were not re-run here; this seat did not attack them.

## Smallest safe correction

Leave the frozen declaration row as it is. Append a sentence to the round-30 measured results and lesson, for example in a "What this round does not claim" list. It should say:
- C1 repairs the routed-defect-2 items: duplicate keys, non-finite numbers, short ids, repeated options, plus the round-28 findings deep corpus and `O_NOCTTY`.
- Still open: IDENTITY-PATHS (outside-population row prefix, ledger backslash, ledger `//`), RETENTION-FRAGMENT and RETENTION-TRUST-BOUNDARY (`fetch_group.py`), C1-UNIT-OVERRIDE, the socket label, the stack-dependent JSON depth limit, and runner granularity for rows, files and counts.

Correct `PROVINCE.md:103-106` so deep corpus and `O_NOCTTY` are not called round-27 families. A closure that admits C1 should quote the qualified scope, not the unqualified clause. This is a disclosure defect, not a tradeoff the judge must reject.

## Not verified

I did not re-run either C1 counter. I did not re-run the deep-corpus, `O_NOCTTY`, or `--name=value` and abbreviated-repeat spellings. I did not probe stack-size dependence or `--revision` (Git-blob) mode for I1–I3. I did not exercise the retention families. Their open status is static: `git diff --stat 0356681 451e98f -- .ufo/waves/round-27/` is empty (exit 0), so the tracked `fetch_group.py` is unchanged.
