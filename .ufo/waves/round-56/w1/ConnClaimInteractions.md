# ConnClaimInteractions

## SEPARABILITY:

C1 (SKILL.md tallies) and C2 (three Yahoo! JAPAN crawl-handling entries) are causally and mechanically separable: either can be verified on an isolated commit without the other landing.

1. **C1 verified without C2**:
   - C1 counter `c56_selftally.py` reads only `<rev>:SKILL.md`, pins 10 script blobs to `BASE_REV` (`e48354b7c26b`), and runs each documented command in an isolated `mktemp -d` clone.
   - It reads no C2 files (`corpus/knowledge/yahoo-japan-*.md`, `corpus/SOURCES.md` S419/S420 rows, `corpus/lessons/round-56.md`, `.ufo/waves/round-56/sources/`).
   - If C1 lands alone, `corpus/SOURCES.md` remains at 156 rows, so `c55_quote_truth.py --selftest` runs cleanly at HEAD (54/54 exit 0) even if unpinned.
   - An isolated commit updating `SKILL.md` (tallies + `VAR=value` pins) meets the C1 predicate (`tally_mismatches=0 rows_checked=10`).

2. **C2 verified without C1**:
   - C2 counter `c56_quote_truth.py` verifies conditions C1..C8 over `corpus/knowledge/`, `corpus/SOURCES.md`, `corpus/lessons/round-56.md`, and round-56 evidence artifacts.
   - It does not read `SKILL.md` directly. In C7, `validate_append.sh` copies `SKILL.md` to `$V/SKILL.md` because historical row S124 cites `SKILL.md` in `used-by`; census validation requires only that `SKILL.md` exists and is syntactically valid.
   - C2 conditions do not depend on `SKILL.md` fixture tallies or on C1 landing.

3. **Causal coupling / Order hazard**:
   - While separable in isolation, landing C2 *before* C1 creates an immediate regression in C1's sub-commands: C2 mutates `corpus/SOURCES.md` (158 rows), causing unpinned `c55_quote_truth.py --selftest` at HEAD to drop from 54/54 to 51/54 (exit 1, failing C7/C8).
   - Therefore, if committed in sequence, C1 must land first or C1's `SKILL.md` row must carry the explicit env pin before C2 lands.

## REGRESSION SURFACE:

| Counter | Command | Current result at base (`e48354b`) | Risk when round 56 lands |
|---|---|---|---|
| `c55_readme_index.py` | `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision <rev>` | `index_mismatches=0 knowledge_files=49 met=True` (exit 0) | **High**: C2 adds 3 files under `corpus/knowledge/`. Without 3 corresponding rows in `corpus/README.md` §Coverage map, `unindexed` jumps to 3, regressing counter to `met=False` (exit 1). |
| `c55_quote_truth.py` (selftest) | `python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` | `54/54 passed` (exit 0; fixture rev `e48354b7c26b`) | **High**: Selftest resolves `rev = HEAD`. At round-56 HEAD with 158 registry rows, C7 and C8 fail, dropping to 51/54 (exit 1). Regresses C1 row `yahoo-robots-quote-truth-counter` to `selftest_failed`. |
| `c55_quote_truth.py` (normal) | `python3 -B .ufo/waves/round-55/c55_quote_truth.py --root . --revision <rev>` | `8/8 met=True` (exit 0) | **Certain fail**: C8 expects 156 rows and round-55 mirror. At round 56 (158 rows), C8 fails (`registry rows 158 != mirror rows 155 + 1`). Expected: round-55 counter is frozen for round 55. |
| `c52_quote_truth.py` (selftest) | `python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` | `17/18 passed` (exit 1; unpinned at `e48354b7c26b`) | **Stays broken**: Unpinned HEAD has >155 rows, failing C8. With `KAKE_R52_SELFTEST_REV=3994101` (or `5422ff3`), it passes 18/18 (exit 0). C1 row `quote-truth-counter` needs this pin. |
| `c52_gate_registry.py` | `python3 -B .ufo/waves/round-52/c52_gate_registry.py --root . --revision <rev>` | `met=False` (exit 1; pinned input `LOG.md` hash mismatch) | **None (already red)**: Archival round-52 counter; failure is historical drift in `LOG.md`. |
| `c52_wave_ledger.py` (selftest) | `python3 -B .ufo/waves/round-52/c52_wave_ledger.py --selftest` | `19/19 passed` (exit 0) | **None**: Hardcodes revision `907790c78008819fc95c988431188f90b81f0d5f`; immune to HEAD changes. |
| `c55_readme_index.py` (selftest) | `python3 -B .ufo/waves/round-55/c55_readme_index.py --selftest` | `44/44 passed` (exit 0) | **None**: Runs on generated synthetic sandbox repositories; immune to HEAD changes. |
| `c56_selftally.py` (blob pins) | `python3 -B .ufo/waves/round-56/c56_selftally.py --root . --revision <rev>` | `tally_mismatches=7 rows_checked=10 met=False` (exit 1) | **High**: Pins blobs of all 10 scripts to `BASE_REV`. Modifying any script (e.g. attempting to patch selftest HEAD-dependence) fires `tool_changed` and fails C1. |
| `citation_lint.py` | `python3 -B scripts/citation_lint.py --root . --revision <rev>` | `exit 0` (clean adjudicated) | **Low**: Checks `SCORECARD.md` and `LOG.md`. Stays clean unless new unadjudicated hex tokens are added. |
| `sources-census.sh` | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate ...` | `exit 0` (kake ok) | **Medium**: Requires all `used-by` paths to exist; C2 new rows must point to valid knowledge entry files. |

## SHARED FILES:

1. `SKILL.md`:
   - **Readers**: Read by C1 counter `c56_selftally.py` (parses gate registry table rows), `c54_ops_debt.py` (checks `c53_gate_truth.py` row), `c52_gate_registry.py`, and copied by `validate_append.sh` for census validation.
   - **Writers**: C1 edits 10 gate registry rows to update self-test tallies. Wave maintenance (`ScribeSkillRows`) adds section `### Round 56 gate registry additions` with two new rows (`selftest-tally-counter`, `yahoo-crawl-handling-quote-truth-counter`).
   - **Interaction**: `c56_selftally.py` matches table rows by first cell (`cells[0]`) and checks only `POP` names. Adding the round-56 rows does not trigger collisions or alter `rows_checked=10`. However, edits must not introduce Markdown table syntax corruption.

2. `corpus/SOURCES.md`:
   - **Readers**: Read by C2 counter `c56_quote_truth.py`, but ALSO read at `HEAD` by `c55_quote_truth.py --selftest` and `c52_quote_truth.py --selftest` when invoked by C1.
   - **Writers**: C2 appends rows S419 and S420, and modifies S367 `used-by`.
   - **Interaction**: C2's edit mutates `corpus/SOURCES.md` from 156 to 158 rows, directly breaking unpinned C1 sub-selftests at HEAD.

3. `corpus/knowledge/`:
   - **Readers**: C2 counter checks existence and headers of the 3 admitted entries; `c55_readme_index.py` enumerates the entire tree.
   - **Writers**: C2 creates 3 new files.
   - **Interaction**: Triggers `unindexed=3` in `c55_readme_index.py` unless `corpus/README.md` is updated.

## RECOMMENDATIONS:

1. **Pin Environment Variables in SKILL.md Documented Commands**:
   - Row 1216 (`quote-truth-counter`): update documented command to:
     `` `KAKE_R52_SELFTEST_REV=3994101 python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` `` with claim `(18 fixtures)`.
   - Row 1234 (`yahoo-robots-quote-truth-counter`): update documented command to:
     `` `KAKE_R55_SELFTEST_REV=e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6 python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` `` with claim `(54 fixtures)`.
   - `c56_selftally.py` supports leading `VAR=value` words in documented commands (`run_command` sets them into the subprocess environment).

2. **Update README Coverage Map Concurrently with C2**:
   - When C2's 3 knowledge entries land, L1 must append 3 descriptive rows to `corpus/README.md` §Coverage map for `knowledge/yahoo-japan-link-target-crawl-restriction.md`, `knowledge/yahoo-japan-deleted-url-recrawl.md`, and `knowledge/yahoo-japan-nonexistent-url-recrawl.md` (each >= 5 tokens, sharing a 5+ letter word or CJK bigram with the entry's head, no duplicate text, no dangling backticks) to prevent `c55_readme_index.py` regression.

3. **Preserve Script Blobs Byte-for-Byte**:
   - Do NOT edit `.ufo/waves/round-55/c55_quote_truth.py` or `.ufo/waves/round-52/c52_quote_truth.py` to fix their HEAD sensitivity. `c56_selftally.py` pins both blobs to `BASE_REV`; any code change triggers `tool_changed` and fails C1.

4. **Integration Order**:
   - If landing as separate commits, land C1's `SKILL.md` updates first, or ensure the `KAKE_R55_SELFTEST_REV` pin is present before C2's `corpus/SOURCES.md` append lands.

VERDICT: C1 and C2 are causally separable in isolation, but C2's registry append regresses C1's unpinned r55 selftest and r55 C1 coverage counter unless L1 applies SKILL.md env pins and updates README coverage rows.
