# Round 33 W2 — runner code propagation mutation probe

Axis: operability. Question: are runner refusal codes propagated into hostile-selftest failure entries and pinned by the committed checks?

## Results

Baseline (rev `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`, pristine runner SHA-256 `88b47f6b957d0ebff0f715fa7b2081c69cc4160d087587f71997038ce8170721`): hostile exit 0, all six specs passed; C1 probe exit 0, `met=4`, `guard_ok=true`; strict supplement exit 0, `met=4`.

| Mutant (runner point) | Mutant rev / runner SHA-256 | Hostile exit / failing specs | C1 probe exit / met | Strict exit / met | Combined verdict |
|---|---|---|---:|---:|---|
| A. Drop `row["code"] = getattr(setup, "code", None)` (line 604) | `b57d58d11fd93bcf25925a508b85bfde4fb00158` / `67ad5db407e1d00ea8a08c869aaa51c81dfede6fe90b5042f426b32e89bb5de8` | 1 / P6 only | 0 / 0 (`guard_ok=false`) | 0 / 1 (`s1` only) | Killed: hostile P6 code check |
| B. Drop failure-entry `"code": row["code"]` (line 774) | `cc4b814858d404334d7c8a69b408a316a1aebce2` / `45edfb0841164d2cd012528bf70217ada32697622533371a73c54e9361b57714` | 1 / P6 only | 0 / 0 (`guard_ok=false`) | 0 / 1 (`s1` only) | Killed: hostile P6 code check |
| C. Apply-time refusal uses `setup_commit_before_init` (line 529) | `6c85296f8f9f6457c40e2dc008942f304520d961` / `0e4e0e748524bba59dc8d32e31ccce18bcbf7c905aa796e64138565ef157eeb4` | 0 / none | 0 / 3 (`m3_killed=false`) | 0 / 3 (`s4_layer=false`) | Killed by strict supplement |
| D. `prepare_case` wraps apply errors with code `None` (line 556) | `dc0c77efeaea4e54f8944c88d3e2f4c8a622054c` / `469380c89038d6ae2083756dd2dcc5d52b4c15f2d07c04c24e3298b1f6b2084f` | 0 / none | 0 / 4 (`guard_ok=true`) | 0 / 3 (`s4_layer=false`) | Killed by strict supplement; survives frozen C1 probe |
| E. Swap load-time/apply-time code literals (lines 402, 529) | `cc0c4f9642948c21295e05871c952059ac734fab` / `7e534d70dd1ada93c80f0dcd33923424839182d5308dfceecc830ddb7a0e3ace` | 1 / P6 only | 0 / 0 (`guard_ok=false`) | 0 / 1 (`s1` only) | Killed: hostile P6 code check |

`met` is the script's internal score; the recorded detector exit is shown separately. All probe/strict script exits were 0 even where their `met` scores fell. C and D pass the ordinary hostile suite because P6 reaches the load-time guard; the strict supplement's `s4_layer` m3 check is what detects their incorrect apply-time code. In particular, D demonstrates that the frozen C1 probe alone does not pin all code propagation (`met=4`). The combined hostile + C1 + strict committed checks killed all five mutants.

## Commands and evidence

All runs used `env TMPDIR=/fast/scratch/hyaku/kake-r33/w2/MutRunnerCodePropagation/tmp`; the host selftest output was JSON-summarized to `passed` and per-spec booleans. Mutant revs above were passed to these commands (with `<M>` = clone letter and `<REV>` = its mutant rev):

- `python3 -B scripts/citing_set_hostile_selftest.py --root /fast/scratch/hyaku/kake-r33/w2/MutRunnerCodePropagation/<M> --tmpdir /fast/scratch/hyaku/kake-r33/w2/MutRunnerCodePropagation/tmp/<M>-hostile --runner /fast/scratch/hyaku/kake-r33/w2/MutRunnerCodePropagation/<M>/scripts/citing_set_selftest.py`
- `python3 -B .ufo/waves/round-33/c1_code_probe.py --rev <REV> --repo /fast/scratch/hyaku/kake-r33/w2/MutRunnerCodePropagation/<M>`
- `python3 -B .ufo/waves/round-33/c1_strict_supplement.py --rev <REV> --repo /fast/scratch/hyaku/kake-r33/w2/MutRunnerCodePropagation/<M>`

The same three detectors were run on the pristine primary clone and after restoration. A restored at `60d4e10caeca759bcbd3a2978606ea0c572788f5`; B at `2eec1db21c1a1d98ed6dec1192f29a8b1a2fc4d8`; C at `13b7c9e4354844fa3a6eb2fe06861bf1e6e94d96`; D at `58a437760945ed0c5393c61f958b1afd76bb4bf7`; E at `70605c126ed2b7fe03d513f6781a9553b537ec01`. Every restored hostile run exited 0 with all six specs true; each restored C1 probe and strict supplement exited 0 with `met=4` and all checks true. Every restored runner SHA-256 was the pristine `88b47f6b957d0ebff0f715fa7b2081c69cc4160d087587f71997038ce8170721`.

Evidence is in the isolated clones under `/fast/scratch/hyaku/kake-r33/w2/MutRunnerCodePropagation/{clone,b,c,d,e}/scripts/citing_set_selftest.py`; source mutation points are lines 402, 529, 556, 604, and 774. All code and Git changes stayed in that sandbox; no tools were installed. No owned web properties were accessed.
