CONFORMANT — counter v4 reruns are semantically deterministic; every non-timing receipt key reproduces byte-for-byte under the same seed, and ref41-base is not met again. Receipts are not fully byte-identical because they intentionally embed measured CPU samples.

Commands (each under `timeout 900 prlimit --as=8000000000`):
- `python3 -B .ufo/waves/round-43/c43_count_v4.py --root <repo> --revision 020bc45...64 --seed 9325990526163 --label freeze-build-1 --out .../rerun-build1.json` -> exit 0 (met, 11/11)
- `python3 -B c43_count_v4.py --root <repo> --revision 020bc45...64 --seed 151761938919664 --label ReviewCounterDet-seedtypo --out .../rerun-seedtypo.json` -> exit 0 (met, 11/11)
- `python3 -B c43_count_v4.py --root <repo> --revision 1ef7a0e...ddd --seed 43001 --label freeze-ref41-base --out .../rerun-ref41.json` -> exit 1 (not met, 11/11)
- `cmp -s rerun-build1.json freeze/build-1.json` -> 1; `cmp -s rerun-ref41.json freeze/ref41-base.json` -> 1
Tool sha256: c43_count_v4.py = 1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab (matches freeze/counter-v4.sha256). Artifacts: /fast/scratch/hyaku/kake-r43/ReviewCounterDet/ (rerun-*.json, keydiff.py).

Diff summary (recursive leaf diff):
- build-1 rerun vs freeze/build-1.json: 60 differing leaves, ALL under `runs.T*.{base40Cpu,candCpu}[i]`, `ratiosExact.T*`, `ratios.T*`. Every semantic key identical: seed 9325990526163, all 11 runs' {ref41Exit, ref41OutSha256, candExit, candOutSha256, equal, values}, equalRuns 11/11, equalValues 11889, counterSha256/ref41Sha256/base40Sha256/toolSha256 (914ebdee...), met=true. Reproduction of all 11 output SHAs under a rerolled `random.Random(seed)` proves corpus generation deterministic (seed flow: c43_count_v4.py:953 urandom fallback, :991 `random.Random(seed)`).
- ref41-base rerun vs freeze/ref41-base.json: 59 differing leaves, same timing-only classes. Verdict reproduced: met=false, exit 1, T1 4.011 (frozen 4.207) and T5 7.419 (frozen 7.047) both >> 2.0. Not met for the same stated reason.
- Literal-command run (seed 151761938919664) vs build-1: 84 differing leaves = timing keys + `seed`, `label` (my label differed) + all `runs.*.OutSha256` — expected: different seed draws a different corpus.

Findings:
1. Dispatch seed mismatch (not a counter defect): build-1.json records seed 9325990526163; the assigned command's 151761938919664 matches NO freeze receipt (all 9 seeds listed above; ref41-base uses 43001). Literal `byte-identical` acceptance is unattainable under that seed by construction.
2. Timing keys are machine-time samples (5 reps each); `ratios`/`ratiosExact` shift ~±20% run-to-run — measured nondeterminism, not generation nondeterminism. Byte-identity holds for all non-timing content; verdicts stable.
3. Receipt soundness holds: no absolute paths/hostnames/env strings embedded (grep for /home, vgpnk, fast/scratch -> 0 hits); self-hash field equals file hash; freeze exits.txt codes reproduced (build 0, ref41-base 1).

Per checked statement: "receipts must be byte-identical" — overstated (timing leaves differ by design); "counter is deterministic" — holds for seed->corpus->output-chain and verdicts; "ref41-base not met" — holds (T1 4.01x, T5 7.42x vs limit 2.0). Residual risk: none found in scope; string-hash ordering could theoretically perturb output bytes but both seeds produced identical hashes across separate processes.
