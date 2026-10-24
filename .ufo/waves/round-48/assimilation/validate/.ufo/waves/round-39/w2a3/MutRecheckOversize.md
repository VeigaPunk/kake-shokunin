# MutRecheckOversize — eight single-point probes
Axes: freshness, operability. Only sandbox bytes and this report were written; no integration or round verdict.
`S=/fast/scratch/hyaku/kake-r39a3w2/MutRecheckOversize`; paths below are relative to S unless stated otherwise.
`P=/fast/scratch/hyaku/kake-r39a3w1/ExecRecheckOversize/recheck-oversize.patch`; SHA256 `12da427097a264ad70a0f7ff5e6644bcefea23581cb58f31b4d092cc95b46c37`.
Clone HEAD observed: `bb4a1e1e4ffa4757bde8275764a8526659a9ed8c` (lane advanced beyond dispatch tip); supplied patch applied successfully.
Patched `clone/scripts/source_recheck.py` and `pristine.py` SHA256: `2ce8c0d9a43bd18bf0b718299eab91ce5839556f006382194c8bd5f418687e1a` (matches wave-1 fixed bytes).
Patched `clone/scripts/source_recheck_hardening_selftest.py` SHA256: `3982837841992b4b682b4b0c94578296e57601d39fd58da0b015e94f00d13178` (matches wave-1 fixture bytes).
Detector: reuse that module's unchanged `run_case` comparator (:351-431), selecting only public `g36-body-over-cap-with-moved` (:248-258). `probe.py:38-48` captures actual commands/stdout/stderr without changing comparisons.
Expected g36: tool exit 2, could-not-evaluate, checksEvaluated 1, exactly kbad/check_invalid; kgood remains evaluated. Detector exit 0 means match; 1 means mismatch.

## Commands and actual exits (cwd S unless stated)
- `timeout 90s prlimit --as=4000000000 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r39a3w2/MutRecheckOversize/clone` — 0.
- In S/clone: `timeout 30s prlimit --as=4000000000 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git apply -p1 /fast/scratch/hyaku/kake-r39a3w1/ExecRecheckOversize/recheck-oversize.patch` — 0.
- `timeout --kill-after=2s 240s prlimit --as=4000000000 python3 -B probe.py pristine` — 0; g36 8/8 plus boundary witnesses 2/2 pass.
- `timeout --kill-after=2s 240s prlimit --as=4000000000 python3 -B probe.py mutated` — 1; g36 kills 6/8, survives 2/8; both supplementary boundary witnesses fail as expected.
- All eight paths restored from the pristine snapshot via whole-file write, then `timeout --kill-after=2s 240s prlimit --as=4000000000 python3 -B probe.py restored` — 0; g36 8/8 plus boundary witnesses 2/2 pass.
- Every tool child used `timeout --kill-after=1s 45s prlimit --as=4000000000 /usr/bin/python3 -B <source> --manifest <manifest>`; all 30 exact argv arrays, outputs and exits are in the three JSON logs. Three concurrent children maximum.
- `timeout 20s prlimit --as=4000000000 sha256sum probe.py pristine.py pristine.json mutated.json restored.json clone/scripts/source_recheck_hardening_selftest.py mutants/*.py mutations/*.patch` — 0.
- In S/clone: `timeout 15s prlimit --as=4000000000 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD` — 0; commit above.

## Mutated g36 outputs and verdicts
Sites below identify the single changed point before restoration; `mutations/<name>.patch` retains each exact delta. All findings below belong to kbad; all stderr was empty.
| Name / source site | Single defect | Tool exit / verdict / evaluated / reasons | Detector exit | Verdict |
|---|---|---|---|---|
| M1_drop_guard.py:619 | replace size predicate with False | 1 / failed-policy / 2 / moved, quote_missing | 1 | killed |
| M2_both_findings.py:620 | return moved findings plus check_invalid instead of None | 2 / could-not-evaluate / 2 / moved, check_invalid | 1 | killed |
| M3_count_invalid.py:766 | increment evaluated in the input-fault branch | 2 / could-not-evaluate / 2 / check_invalid | 1 | killed |
| M4_ge_cap.py:619 | change `>` to `>=` | 2 / could-not-evaluate / 1 / check_invalid | 0 | survived |
| M5_guard_plus_one.py:619 | compare with MAX_BODY_BYTES + 1 | 1 / failed-policy / 2 / moved, quote_missing | 1 | killed |
| M6_read_cap_only.py:616 | read MAX_BODY_BYTES rather than cap + 1 | 1 / failed-policy / 2 / moved, quote_missing | 1 | killed |
| M7_stop_after_invalid.py:766 | break rather than continue after input fault | 2 / could-not-evaluate / 0 / check_invalid | 1 | killed |
| M8_cap_plus_one.py:53 | increase MAX_BODY_BYTES constant by 1 | 2 / could-not-evaluate / 1 / check_invalid | 0 | survived |
Source-site prefix: `S/mutants/`. Mutated SHA256 values, same order M1–M8:
- M1 `3100c0ea013afdc541e5f85f1c81dc2de28b88a4f8f9696e88db81ef8acd6af5`
- M2 `cd3972fee4e820f63a45b82e254fbfe46baea97c8f4cc3f727d0c2bbf764131e`
- M3 `404361c17bcb74cc33fdd373f6f929293afe1132b336218fc8a70f8945c564f1`
- M4 `0ed60cd9a5972651671f921d42cf8fd9534c2fa7025be8ed84d02a17d44711ef`
- M5 `cdc93fe1aed8e2c13b9ff8be5cd2d6ff6243c8e2374c60a5eb315943225fa7c2`
- M6 `454a82b59c089608124401185ec0ff43cb5decddcfa299e08ed712141c958878`
- M7 `de80933e5c94690b60aa5bc891a000f32d45096f9b60a5a01adca1769313cef3`
- M8 `d5723f5158e7089b53adb8f1c07dd440be44b298d256b7940f7498925265f9e7`

## Attacked statements / coverage findings
- **holds** — exclusive check_invalid at `clone/scripts/source_recheck.py:619-620,762-766`: g36 kills M2; counts and subsequent healthy-check processing at :765-768 are pinned independently by M3 and M7.
- **holds** — g36 detects omitted size rejection, oversized-read truncation, and an overly permissive guard expression: M1/M5/M6 killed. No baseline failure; none inconclusive.
- **overstated if read as strict cap-boundary coverage** — g36 does not pin the exact 16 MiB boundary: M4 and M8 survive. These are coverage findings, not contract changes or equivalent mutants.
- Non-equivalence witnesses (`probe.py:60-64`), run on pristine/mutated/restored with the same comparator: exact-cap body for M4 yields exits 1/2/1, evaluated 2/1/2, moved/check_invalid/moved; cap+1 body for M8 yields exits 2/1/2, evaluated 1/2/1, check_invalid/moved/check_invalid. Both witness detector exits are 0/1/0; they are supplementary, not credited as g36 kills.
- **wrong, narrowly** — wave-1 report `.ufo/waves/round-39/w1a3/ExecRecheckOversize.md:9` calls the body “16 MiB+1”; fixture `clone/scripts/source_recheck_hardening_selftest.py:255` adds seven tag bytes, making 16,777,224 bytes (cap+8), not 16,777,217.

## Restoration / artifacts
All eight `mutants/*.py` hashes before and after are exactly `2ce8c0d9a43bd18bf0b718299eab91ce5839556f006382194c8bd5f418687e1a`; restored detector passes on every path. Fixed source and fixture hashes remained unchanged across all stages. Mutant deltas remain in `mutations/*.patch`; no mutant source is left active.
- `pristine.json` SHA256 `f6033b73eadae2d6834974bbf3202400d8e5d9862e8fe8c957c3d35c7b601f7e`.
- `mutated.json` SHA256 `a9a1be4a0578c641948dcf0a8cb6d8910a69abe393c1e7d975bb671f27201137`.
- `restored.json` SHA256 `4f7d95abfda88d8e0d6bf5a42c7cf6d10bae7fa953a4a6640e4b402629186c8a`.
- `probe.py` SHA256 `97be864e4f2fad0f20dea7697f709778ae6c6904a1a86d0dc688d3bb27fbe3f4`.
No full selftest suite, sealed counter, sealed data, network, installations, or upgrades used. Temporary fixture directories were removed by the detector; all synchronous process trees exited. Only this assigned mutation probe was performed.
