# ExecMutVerify — R94-4 mutant-scan re-derivation at the freeze commit

Freeze commit: `8f638b591e739e1863f5fa22334d5e15178189ed` (round-95 claims freeze).
Seat: ExecMutVerify (leaf, executor-role verification). Read-only against the lane;
no git mutation; no subagent dispatch; no edits to any frozen file.

VERDICT: **MUT-VERIFY killed=40/40 survivors=none**

Survivor set matches the freeze's zero-survivor determination
(`controls/mutant-scan-v2-result.json`: killed 40, survivors []). **No freeze-falsifying finding.**

## What was run

| Step | Command | Observed |
|---|---|---|
| Extract frozen bytes | `git show 8f638b59:<path>` for the 10 named files plus `c2-contract-v2.md`, the six `round-93/frozen/neg-*.py` forgeries, `controls/instrument-sha256.txt`, `frozen/c1-surfaces.json` and `controls/mutant-scan-v2*` | all present at freeze bytes |
| Instrument pins | `sha256sum -c` over `controls/instrument-sha256.txt` (8 paths) | rc=0, 8/8 OK; `c95_conditional.py` = `f09f8409…312`, `c95_selfassess.py` = `8fd27d62…b193`, both match the task digests |
| Population pins | `sha256sum -c frozen/c2-population.sha256` (12 paths) | rc=0, 12/12 OK, including `mutants-posgood.json` = `b09e011e…567` and `pos-good.py` = `0fe018a8…68e4` |
| Equivalence receipts | `frozen/c2-equiv-receipts.json` | `[]` (empty, as declared) |
| Counter selftest at freeze bytes | `python3 -B .ufo/waves/round-95/c95_conditional.py --selftest` (module digest re-checked before run) | rc=0; `selftest 8/8 fixtures scored as declared; drifted-reference cases=5; M11 killed=True` |
| Mutant battery | `python3 -B battery_driver.py` (imports the frozen module via `importlib` read-only, asserts its digest, then calls the counter's own `mutant_cases()` with its `SANDBOX`, `hand_cases()` (66) and `generate(95,120)` windowed to `[:40]`, exactly as the counter's `main()` builds them) | rc=0; `MUT-VERIFY killed=40/40 survivors=none`; ~58 s |
| Freeze-control comparison | driver compares kill set and survivor set against `controls/mutant-scan-v2-result.json` | identical kill set and identical (empty) survivor set |
| Per-note comparison | first-failure string vs the freeze's `notes` | 40/40 prefix-identical (100 chars) |
| Cross-check of counter `main()` at freeze revision | `python3 -B c95_conditional.py --root <lane> --revision 8f638b59 --work <scratch>` | rc=1; `C2v95 revision=8f638b59… candidate=present hand=57/66 generated=79/120 forgeries_refused=7/7 positive=admitted mutants=40/40 survivors=none anti_table=ok population=ok seed=95 met=false` |

Background job `bg_6944` is reported as "failed": that was the main() cross-check exiting 1 with
`met=false`, as expected at this revision. Its stdout is complete. It was not a crash.

Tool use: stdlib only. Python 3.14.8, `git` (read-only subcommands), `sha256sum`.
Nothing was installed, upgraded or removed on the host. `pacman` was not used.

## Per-mutant result (`mutants-v3.json`, 40 rows)

Every row has `id`, `killed`, `first_failure`. All 40 are `killed: true`; none has an empty `first_failure`.

Kill mechanism, classified from the first failure:

- 35 wrong decision on a valid or refusal case (e.g. M01, M02, M16, M17, M31)
- 4 refused as `invalid_input` where the reference decides (M11, M19, M20, M40). M11 is the round-94 survivor, killed by `inm/empty-member-middle-ignored` (contract v2 clause 1).
- 1 runtime exception on a valid input: M33. The mutant removes the guard `if tag is None or not exists:` to `if not exists:`. It then raises `TypeError: 'NoneType' object is not subscriptable` at `weak()` on `inm/ignored-when-current-etag-absent`, where the reference answers 200. This is a real behavioural defect, not a syntax artefact.

Compile check: all 40 mutated sources compile (`compile()` clean). **No kill is a syntax-only kill.**

M11 detail: `inm/empty-member-middle-ignored: expected {'decision': '304', ...} got None (rc=1 invalid_input: empty member)`.

## Cross-check against the freeze control

- Kill and survivor sets agree with the freeze's `mutant-scan-v2-result.json` (40/40, no survivors).
- All 40 first-failure strings agree in their first 100 characters with the freeze's `notes`.
- The counter's `main()` at `8f638b59` reproduces the freeze base-control numbers (`hand=57/66 generated=79/120 forgeries_refused=7/7 positive=admitted mutants=40/40`). It is `met=false` at this revision, as it must be: the candidate bytes are unchanged from the round base and the instruments commit (`scripts/conditional_eval.py` = `d3bac7de…cac5`, identical at `fdd5fdbe`, `43cdd9fc` and `8f638b59`). The freeze commit ships no candidate change. This is information for the L1, not a verdict on C2.

## Caveats (for the L1's reading of the zero-survivor claim)

1. **Independence limit.** The driver calls the counter's own `mutant_cases()`, `score_subject()`, `reference()` and `SANDBOX`. What is independently re-derived here is the input chain (digests, population base, mutant application, generated windows, sandbox) and the separate kill-type and compile analyses. The scoring code is not an independent second implementation.
2. **Window direction.** Kills use `hand_cases()` plus only the first 40 of the 120 generated cases (`gen_limit=40`). A larger window can only add kills. So zero survivors under the 40-case window implies zero survivors under the full 120. The window does not weaken the zero-survivor result.
3. **Kill is not equivalence.** "Killed" means the mutant's output differs from the v2 reference on some case. M11's kill depends on contract v2 clause 1 (empty members accepted). If that clause changes, M11's status changes too, which is the reason the R94-4 receipts rule stays in force.
4. **Population base.** The 40 mutants patch the round-93 `pos-good.py` bytes, not the scored candidate (the freeze already says so). The zero-survivor result is a statement about this instrument population, not about the candidate's correctness.
5. **Report path.** The seat spec names `w1/ExecMutVerify.md`. The hard bounds limit writes to `w1/ExecMutVerify/`, so the report lives at `w1/ExecMutVerify/ExecMutVerify.md`.

## Receipts (under `w1/ExecMutVerify/`)

| File | sha256 | Contents |
|---|---|---|
| `mutants-v3.json` | `57e949a1…a836` | 40 rows: id, killed, first_failure |
| `scan.txt` | `18f6cf35…0558b` | header with all digests and pins, per-mutant lines, verdict and freeze comparison |
| `selftest.txt` | `7649eead…2746` | frozen counter `--selftest`, rc=0 |
| `crosscheck-main-stdout.txt` | `dd5d9878…4a73d` | counter `main()` at freeze revision: 2 lines (verdict and JSON detail), rc=1 |
| `crosscheck-main-stderr.txt` | `e3b0c442…b855` | empty |
| `battery_driver.py` | `24cb63e7…a801` | the driver used for `scan.txt` and `mutants-v3.json`. Its scratch paths are not valid in the lane; it reads the frozen bytes from a scratch repo layout. |

Scratch tree `/fast/scratch/hyaku/kake-r95/ExecMutVerify/` removed after the receipts were copied here.

## Suggested checks for the L1

- Re-run `python3 -B .ufo/waves/round-95/c95_conditional.py --selftest` at the landed tip (already green at freeze bytes).
- Only if the candidate changes: re-run `c95_conditional.py --root . --revision <tip> --work <scratch>`. The mutant battery does not depend on the candidate.

VERDICT: MUT-VERIFY killed=40/40 survivors=none
