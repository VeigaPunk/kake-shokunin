# ReviewC1 — round 84 wave w1

Axes: calibration (C1 soundness), evidence fidelity, and unchanged production state. C2 is outside this review.

## Findings, by severity

### High — D3 and D4 omit their frozen row conjuncts

`.ufo/waves/round-84/c84_defect_queue.py:161–177` never reads the lesson or SCORECARD. Its returned `row` is merely `len(settled) >= 1`, not the contract's requirement that the round lesson or SCORECARD name the connector seat.
`.ufo/waves/round-84/c84_defect_queue.py:180–196` likewise never reads the lesson: its returned `row` is a positive equal collision count, not the requirement that the round lesson name `controls/census-before.txt`.
The independently constructed `missing-d3-d4-row` fixture has neither SCORECARD nor either required lesson reference, yet prints all four items closed and `met=true`, exit 0. Receipt: `ReviewC1/missing-d3-d4-row.txt`.
This is a concrete false positive against two frozen conjuncts, not a hypothetical interpretation of the selftest. Recommendation: do not rely on counter-green alone to recommend C1 closure; re-derive both prose conjuncts independently and disclose the frozen instrument defect. The counter was not edited.

### Medium — D1 combines different correction lines

At counter lines 125–137, `state` can be established by one correction line containing the four headings, while a different correction line supplies `round-83.md` and `Gate`. The contract requires the correction line to carry the joint citation.
The `split-d1-correction` fixture has no single line satisfying that conjunction; the counter prints `item=D1 closed=1` and `met=true`, exit 0. Receipt: `ReviewC1/split-d1-correction.txt`.
The existential row reference still exists in this example; the defect is failure to bind it to the heading-bearing line, rather than total absence of D1's row words.

### Medium — D3 treats JSON null as non-empty settled output

Counter line 174 coerces output to `str` before checking emptiness. `output: null` becomes `"None"`, so a connector with no textual output counts as settled.
The `nonstring-output` fixture prints `settled_connectors=1`, all closed, and `met=true`, exit 0. Receipt: `ReviewC1/nonstring-output.txt`.
Absent output defaults to an empty string and is rejected; this finding specifically concerns present non-string values (also false, zero, empty objects/lists by the same coercion).

### Medium — D4 receipt checks accept a wrong path and nonzero exit token

Counter line 187 only requires an `ok` line containing `SOURCES.md`, not a `corpus/SOURCES.md` path. A receipt whose path is replaced with `not-corpus-SOURCES.md` still produces `met=true`, exit 0 (`ReviewC1/bad-ok-path.txt`).
Counter line 185 uses substring membership for `census_exit=0`. Replacing that token with `census_exit=01` still produces `met=true`, exit 0 (`ReviewC1/nonzero-exit-substring.txt`), although the receipt no longer records the required zero exit token.
These are state-conjunct weaknesses independent of the missing lesson-reference check.

## Independent worktree re-derivation

The snapshot was taken while the wave was running; it is not a claim about a later integrated tree. `ReviewC1/snapshot.json` records presence, byte lengths, and SHA-256 for every measured input; `ReviewC1/snapshot/` retains the exact present bytes. The lesson and results file were absent at that snapshot.
The command for all four independent derivations was `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/w1/ReviewC1/probe.py`, exit 0. Its complete stdout is retained in `ReviewC1/probe-output.txt`. Derivation precedes importing the counter for comparison; it does not use the counter's item verdicts.

| Item | Independent status | Exact input bytes and reason |
|---|---|---|
| D1 | OPEN | `corpus/lessons/round-84.md` absent. Retained RFC is 84,477 bytes, SHA-256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`; the four heading strings occur at physical lines 1081, 1111, 1203, 1408 (also in its contents). No correction line exists in the measured lesson. |
| D2 | OPEN | Same absent lesson, so no claimed count. The exact RFC lines 838–844 independently count to 66, not 48; full span below. |
| D3 | OPEN | Spec is 28,020 bytes, SHA-256 `c685dc00f577b502d2041bf44febde817e94b0a90c5105bc95d0b862caa8308e`, and has exactly one connector item named `ConnectorSibling`. `.ufo/waves/round-84/w1-results.json` absent, so zero settled connector rows. |
| D4 | OPEN under contract | Census receipt is 1,882 bytes, SHA-256 `5c5a3da2c253c38058c43d6c562f5c0cb0e8f1daaec7dbac1216e9148c168ac0`; registry is 181,343 bytes, SHA-256 `02524d26ecb13cd03c33d46460c7a850b3aabbd63714b078f76aa0700ec53de8`. Receipt records zero exit and the real corpus path; both W04 derivations equal its 22 records. State satisfied, but absent lesson cannot name the receipt. |

The probe's exploratory substring test printed `lesson_or_scorecard_named=True` for D3. Literal follow-up established this is ONLY the historical `ConnectorSiblingOverlap` string at SCORECARD line 2919, not a reference to this round's `ConnectorSibling` seat. It is not semantic evidence of the D3 row conjunct. D3 remains open independently because results are absent.

## D2 arithmetic and exact boundary

Boundary: physical retained-text lines 838 through 844 inclusive; read with `splitlines(keepends=True)[837:844]`, concatenate, then count whitespace-delimited maximal non-whitespace tokens using `len(span.split())`. This independently implements the full-span measure without calling the frozen count function. The final parenthetical is included. Per-line counts are **11, 11, 11, 11, 9, 9, 4**, sum **66**.

```text
   Another validator is the entity tag given in an ETag field
   (Section 8.8.3 of [HTTP]).  One or more entity tags, indicating one
   or more stored responses, can be used in an If-None-Match header
   field for response validation, or in an If-Match or If-Range header
   field for representation selection (i.e., the client is referring
   specifically to one or more previously obtained representations with
   the listed entity tags).
```

The retained snapshot and `SPAN_BYTES_REPR` in `probe-output.txt` preserve indentation, doubled spaces, and final newline. Counter line 157 joins separator-stripped lines with newlines rather than the contract's concatenation of newline-retaining lines; on these actual bytes the token boundaries and resulting count are identical.

## D4 census comparison

I independently parsed the real registry table, tolerating zero through three leading spaces, requiring eleven cells and source IDs, stripping scheme/fragment/one terminal slash, lowercasing the host only, and recording a collision when the normalized URL was seen but its `(url, scope)` pair was new. Input rows: **194**. Independent W04: **22**. Frozen counter `census_w04` on the same snapshot: **22**. Retained census receipt: **22**. All pair-set differences are empty; no divergence on the actual registry.
IDs: S033, S088, S092, S098, S099, S102, S110, S111, S115, S116, S117, S127, S416, S417, S427, S433, S445, S450, S451, S453, S454, S455. Exact normalized URL pairs are printed in `probe-output.txt`; exact parsed rows are in `registry-rows.json`.
The lane contains no `sources-census.sh` implementation (scoped glob returned only historic receipt names). I compared the frozen receipt and contract-defined census rule, not an independently executed live fleet census. No out-of-scope fleet file was read to substitute for that missing lane-local implementation.

## Mandatory words-only attacks

Each invocation is `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/c84_defect_queue.py --root /fast/scratch/hyaku/kake-r84/ReviewC1/<case>`; full command/stdout/exit is in the matching receipt.
- `prose-only`: lesson asserts all four closed and carries valid-looking correction/count strings, but required evidence files are absent. **Exit 1**, `open=4 closed=0 met=false`. Words alone do not close an item.
- `heading-not-retained`: lesson cites all four headings, but every retained occurrence of `5.2.3.  Extension Directives` is removed. **Exit 1**, D1 open, `open=1 closed=3 met=false`. The retained-bytes check defeats this attack.
- `missing-d3-d4-row`, `split-d1-correction`, `nonstring-output`, `bad-ok-path`, `nonzero-exit-substring`: each **exit 0**, `open=0 closed=4 met=true`, with the defects described above. These fixtures use explicitly synthetic connector output; no fixture result is represented as a real settled seat.

## Exhaustive row-conjunct bypass classification

For the four stated row conjuncts, the code paths are exhaustive: D1 requires a correction-line occurrence of both `round-83.md` and `Gate`; D2's successful regex inherently contains `span=838-844`; neither can be entirely absent while its item closes. D1 can mis-bind the row to a different heading line as demonstrated.
D3 may close when BOTH allowed prose carriers omit the connector seat, mention only another seat, or have no current-round connector reference at all, because neither carrier is read. This encompasses absent/unreadable carriers whenever D1/D2 still have a readable lesson and SCORECARD does not establish the reference.
D4 may close when the lesson omits `controls/census-before.txt` or names a different receipt, because the lesson is not read. D3 and D4 omissions may occur separately or together; the combined fixture proves `met=true` with both false. Any further spelling/context variants are instances of these two omitted checks, not additional independent code paths.
D4 also falsely rejects a genuinely matching zero-collision registry because its surrogate `row` requires `len(derived)>0`; the contract's equality requirement allows empty equal sets. This is a static inference from line 196, not an executed fixture.

## Commands, limits, and cleanup

Initial read-only command: `ls -la /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/ && git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse HEAD && git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --short | wc -l`, exit 0; observed HEAD `87cbfd99b677a330c14a68a33f10548f15e6e10c` and three status rows. This was inspection, not a clean-tree assertion.
`git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff fe42ad11eb1084ad2ea68d12c5bbb2922a089868 -- .ufo/waves/round-84/c84_defect_queue.py corpus/lessons/round-84.md`, exit 0: reviewed the new counter and no lesson diff at that time.
LSP prerequisite: `read xd://lsp` returned `No such tool`; no mounted LSP status/reference/definition/diagnostics capability was available. Source inspection and literal search were the fallback, never described as semantic proof.
Source reads covered contract C1, the complete 335-line counter, and routed defects at prior spot-check lines 168–185. No source/counter/production edits, VCS mutations, network requests, tool installations, or subagent dispatches were performed.
All seven counter subprocesses ran concurrently from the retained driver. Scratch was explicitly `/fast/scratch/hyaku/kake-r84/ReviewC1/`; the driver's `finally` removed it and printed `scratch_removed=True`. Receipts and replay driver are retained only in the authorized report subtree.
Verification gap: this is an in-flight snapshot, not a later after-state admission. Runtime rerouting, saturation, and resume continuity are not affected surfaces of this offline file-reading counter and were not claimed verified.
Self-evaluation: accuracy 4 (live fleet census not rerun), completeness 4 (after-state not yet available), clarity 4 (receipt-heavy report), actionability 4 (frozen predicate cannot be silently patched), conciseness 4 (detail retained to make attacks reproducible); average 4.0. Highest-impact next evidence is independent after-state row inspection, not repeating the counter's own green output.

## Verdict

**Recommendation: do not treat C1 counter-green as proof of the frozen contract.** The two mandatory negative controls are red as required, but a valid-evidence fixture missing both D3/D4 row conjuncts returns `met=true`; additional D1/D3/D4 false positives are reproduced. At the inspected worktree snapshot D1–D4 are all open under the contract. This recommendation is not an admission or integration action.
