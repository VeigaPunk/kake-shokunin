# ConnW2Cross

ATTACKS: Evaluated cross-claim interactions at build B1 (8b33fd24 vs base 97cdc122): tested C3's in-file correction under C2's append_guard; audited C1's c59_quote_truth relabel dependency and disclosure in SKILL.md; conducted scratch revert tests in isolated shared clones for partial (rows only) and full C3 reverts; evaluated repeated patterns from rounds 55–59 spotchecks.

INTERACTIONS:
- C3 -> C2: Ran `python3 -B scripts/append_guard.py --root . --base 97cdc122379711c2b02a8970752c8782da3ac81d --revision 8b33fd248d126b48d838af5c38bc175850f41a09`. Output: `files=55 findings=0`, exit 0 (`ConnW2Cross.files/c2_append_guard_b1.txt`). C3's in-file insertion in `corpus/knowledge/googlebot-verification.md` starts with `  **[r60-correction 2026-10-27]**`, matches TAG_RE outside comments/code, and preserves all base lines in ordered subsequence. The two new knowledge entries are new paths at revision and skipped per rule K11.
- C3 -> C1: In B1, `crawler-identity-quote-truth-counter` (`c59_quote_truth.py`) was relabelled `historical` (pin `b322ccabe1628fc0cfe80c2dddca03ed154d1349`). At base it was live and green (exit 0). At B1 it turns red (exit 1).
- Incomplete Disclosure in SKILL.md: Line 1309 attributes reddening solely to C8 ("C8 requires the registry minus S425/S426 to equal the 162-row pre-append mirror, and round 60 appends S427-S429"). However, running `c59_quote_truth.py` on B1 reveals that condition C5 also fails (`S426: entry line 40 quotes 'Because the fetch was requested by a use'… which is not a raw substring of the retained body`) because S426's entry carries an S428 quote, and C7 fails because the scratch entry differs from the landed file (`ConnW2Cross.files/c59_quote_truth_runs.txt`). The semantic quote breakage caused by C3 is undisclosed.

REVERT TEST:
- Scratch clone revert experiments (`ConnW2Cross.files/revert_tests.txt`):
  1. Reverting ONLY C3 rows S427–S429 in `corpus/SOURCES.md` (commit `1b676115`): `c60_gate_status.py` fails with exit 1 (`members=28 mismatches=3 met=False`). Mismatches: `c57_idresolver_gate.py`, `c58_resolver_cases.py`, and `c59_resolver_cases.py` all fail with `live_not_green` because `google-user-triggered-fetchers.md`, `robots-txt-limits.md`, and `googlebot-verification.md` cite S428/S429 which become dangling IDs absent from the registry.
  2. Reverting ALL C3 changes (rows, entries, and in-file correction, commit `da7aaaff`): `c60_gate_status.py` fails with exit 1 (`members=28 mismatches=1 met=False`). Mismatch: `c59_quote_truth.py` runs green (exit 0) at the revision, triggering `historical_but_green`.
- Result: C1 cannot stay met if C3 is reverted or decoupled. The claims are strictly coupled at B1; contract §Axis declaration's claim of "causal separability" does not hold under isolation testing.

PATTERNS:
- Repeated failure patterns from rounds 55–59 spotchecks:
  1. Recurrence of R59-D1 (in-file correction breaks predecessor gate): In round 59, an in-file correction in `crawler-identity.md` broke `c55_readme_index.py` (`head_changed`). In round 60, C2's `append_guard.py` accommodates tagged insertions, but C3's in-file insertion in `googlebot-verification.md` broke `c59_quote_truth.py`'s C5 quote parser because the quote scanner does not recognize tagged correction blocks and tests cross-source quotes against the host file's primary source.
  2. Incomplete gate failure attribution (rounds 57/58 D3): Documenting only the mirror row count (C8) while omitting semantic quote-truth and entry validation failures (C5, C7).
  3. False causal separability: Claiming independent claim verifiability while C1's gate status is strictly dependent on C3's mutations.

PROPOSED MOVE:
- Evidence: `c59_quote_truth.py` fails C5 on S428 quotes inside S426's entry, while `c60_quote_truth.py` lines 534–546 duplicates the same span extraction over `markdown_prose_lines(body)` without isolating `[rNN-correction]` tagged runs.
- Affected axes: `calibration` (score 2) and `operability` (score 10); neutral to `freshness` (score 10).
- Proposed move: Harmonize tag recognition between `scripts/append_guard.py` and quote-truth counters by stripping `\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]` blocks from primary-source quote evaluation (treating tagged in-file corrections as secondary provenance), and update `SKILL.md` line 1309 to disclose both C5 and C8 mechanisms.
- Risks: Quote scanners could allow unverified quotes in tagged blocks unless the tagged block is independently bound to its cited source (as C3 C9 did specifically for S428).
- Verification: Run `c60_quote_truth.py --selftest` and verify 9/9 conditions pass; verify `c59_quote_truth.py` failure trace matches documentation.

FINDINGS:
| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| medium | SKILL.md:1309 | Incomplete disclosure of reddening mechanisms: Kind cell only cites C8 mirror row append, ignoring C5 quote failure and C7 validate failure caused by C3's in-file insertion in `googlebot-verification.md`. | `python3 -B .ufo/waves/round-59/c59_quote_truth.py --root . --revision 8b33fd248d126b48d838af5c38bc175850f41a09` (C5/C7/C8 FAIL) | Update SKILL.md row to disclose both C8 row-count mismatch and C5/C7 in-file correction quote-collision. |
| medium | .ufo/waves/round-60/contract.md:41 | Overclaimed causal separability: C1 cannot verify if C3 is omitted or reverted (revert test proves C1 fails with `historical_but_green` or `live_not_green`). | `python3 -B .ufo/waves/round-60/c60_gate_status.py --root lane-clone --revision da7aaaff` (mismatches=1, c59 historical_but_green) | Document in lesson/contract that claim verifiability is atomically coupled at B1 rather than causally separable. |
| low | .ufo/waves/round-60/c60_quote_truth.py:534 | Quote scanner does not isolate tagged correction blocks, risking future R59-D1-style quote collisions when entries are corrected in-file. | Inspect `markdown_prose_lines()` in `c60_quote_truth.py:534-546` | Exclude `[rNN-correction]` tagged blocks from primary-source C5 quote verification. |

VERDICT: C3's correction cleanly passes C2's guard, but tightly couples with C1 (revert test breaks C1); SKILL.md incompletely discloses c59's failure mechanism, repeating the R59-D1 collision pattern.
