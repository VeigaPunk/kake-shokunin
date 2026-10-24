# SentinelBuild — round 38 wave 2

Axis: operability. Target: `scripts/robots_audit.py` at `adab4c7e9ec2178657395f49346f18800ff4796f`; source SHA-256 `f4d057c4afac885b998de404da8c19f2d5d0a4d754a9d539e49b07d3f36baace`.
Severity: no operational defect reproduced on the attacked manifests.
Exploit path: untrusted local JSON manifest passed as `--manifest`, including deep nesting, numeric tokens, URL/check volume, and malformed fields.
Impact: no crash, traceback, timeout (>20 s), or memory error observed; all runs completed within the 4,000,000,000-byte address-space cap.
Smallest remediation: none indicated by these results; this is bounded evidence, not a general resource-safety proof.

## Commands and results

Wave-1 corpus command (runner exit 0): `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && export TMPDIR=/fast/scratch/hyaku/kake-r38w2/SentinelBuild/tmp && timeout 900s sh /fast/scratch/hyaku/kake-r38w2/SentinelBuild/wave1/run.sh /fast/scratch/hyaku/kake-r38w2/SentinelBuild/clone/scripts/robots_audit.py`.
Added-input command (runner exit 0): `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && export TMPDIR=/fast/scratch/hyaku/kake-r38w2/SentinelBuild/tmp && timeout 900s sh /fast/scratch/hyaku/kake-r38w2/SentinelBuild/attacks/run.sh /fast/scratch/hyaku/kake-r38w2/SentinelBuild/clone/scripts/robots_audit.py`.
Both are the supplied `run.sh`; it invokes each manifest under `prlimit --as=4000000000 timeout 60s python3 "$tool" --manifest "$input"`.
A first wave-1 launch exited 1 before invoking the tool because its private `wave1/tmp` parent did not exist; after creating that sandbox-local directory, the command above completed. No lane/sibling input was modified.

## Verdicts per attacked statement

- Wave-1 inputs remain operational on the build — **holds**. Results: `deep-nesting` 0/15 ms clean; `digits-64m` 2/28 ms `input_invalid`; `huge-exponent` 0/16 ms clean; `long-status-integer` 2/15 ms `check_invalid`; `many-checks-long-urls` 0/67 ms, 2,048 evaluated; `many-long-numbers` 0/26 ms clean; `nonjson-number-literals` 2/15 ms `input_invalid`; `unused-long-integer` 0/16 ms clean; `url-ascii-pipe` 2/16 ms `check_invalid`. Evidence: `/fast/scratch/hyaku/kake-r38w2/SentinelBuild/wave1-results.txt:1-18`.
- 100,000 nested `[` tokens — **holds**: exit 2, 19 ms, structured `input_invalid`, no traceback. Evidence: `attack-results.txt:3-4`; size at `attacks/manifest-stats.json:4`.
- Exactly 64 MiB of mixed long integers/decimals/exponents — **holds**: exit 0, 383 ms, clean, 0 checks; no resource error. Evidence: `attack-results.txt:7-8`; exact size at `manifest-stats.json:6`.
- 100,000 checks with 43-character URLs — **holds**: exit 0, 178 ms, clean, all 100,000 evaluated. Evidence: `attack-results.txt:1-2`; count and URL length at `manifest-stats.json:2-3`.
- Huge exponents, NaN nested in arrays, and NUL robots path — **holds**: exponent exit 0/16 ms clean (`attack-results.txt:5-6`); NaN exit 2/48 ms `input_invalid` (`:9-10`); NUL path exit 2/17 ms `check_invalid` (`:11-12`). No traceback or process failure.

The only exit-2 results were structured manifest/check-invalid reports. Slowest of all 15 cases was 383 ms; no case exceeded 20 s. Relevant code: build `scripts/robots_audit.py:114-154,421-477` (64 MiB gate, bounded integer conversion, JSON parse fault handling), `:484-531` (path/URL validation), `:542-629` (check processing); hash above.

## Evidence artifacts (sandbox paths and SHA-256)

Runner: `/fast/scratch/hyaku/kake-r38w2/SentinelBuild/wave1/run.sh`, `b80d23e77e89794310602b68e7dbf973e4fa11c00d08bcf8fbf447d177836e4f`.
Wave-1 results: `/fast/scratch/hyaku/kake-r38w2/SentinelBuild/wave1-results.txt`, `5332c9ae694a45dda8164fd8686530ee07e51efe94ca7ac60a14e29793264eec`.
Added results: `/fast/scratch/hyaku/kake-r38w2/SentinelBuild/attack-results.txt`, `b7eb02ff142a03ca8d20fa5c0ea6a76e1bbad317b1d4e6c7feb2c367a23484d1`.
Generated manifest statistics: `/fast/scratch/hyaku/kake-r38w2/SentinelBuild/attacks/manifest-stats.json`, `eb57dddd6128e6ccd3c2c407c152a7f596f26447d0bf32490510d8589e344181`.
Generator: `/fast/scratch/hyaku/kake-r38w2/SentinelBuild/generate_attacks.py`, `8d8b17eed3e411d59ec2dfe226143f13af737717adde243c863041372ead0bd3`.
Added input SHA-256s:
- `checks-100k-urls-43.json` `54af228421c3b8a1d82d4bbe799c657251c3ff1da7042ece770fc3493427fd36`
- `deep-nesting-100k.json` `43600bc2bd04a9e13cbaa13ece57c2d9bd15e2f3917c8c219b5d9ab1bbaa6d77`
- `huge-exponents.json` `d2aa34fdef79797bd77f1fc888ce2257be018392e36bbe7510dd1dd88f9f50f0`
- `mixed-long-numbers-64m.json` `9d7df3c36a6dac6cd8c8966a6433b35686ff44d03afd79dec6731e72dd52d7fd`
- `nan-nested-arrays.json` `c81a5ef7829d6beec9d74091f8bc59645e2b0cadbeaa02cfabce5d89dd5e7858`
- `nul-robots-path.json` `e3c93b394b88708c9f3eea08eb34887c9f1639ba3476c8dd35676deffee990fa`
Wave-1 inputs (same names under `/fast/scratch/hyaku/kake-r38w2/SentinelBuild/wave1/inputs/`):
- `deep-nesting.json` `edd03feaeef9965bdeb9ae26f12510b06f03f76c18a36e0aae2ae031021cf398`; `digits-64m.json` `4dcf7dba36eb4b1ada7e42911fd045cf1b359e144c245ff4fc2b0d3d7a2ed081`
- `huge-exponent.json` `fff094ce9e7ebb70ca208c0bc106f084187c3cce560d58421b0641bb09e92869`; `long-status-integer.json` `8e89c52b8afb9fba0c354f62224fa11a6417578a548d98d8825a5ccf4eb828c9`
- `many-checks-long-urls.json` `26077f711f8826bf6193b64e0189bc63477e1221fdc36ed78dc5bc59c90cd2ce`; `many-long-numbers.json` `bb81587a6bea82bc606781f9775f37de7989c608100aca8a598ca5f8feb8da01`
- `nonjson-number-literals.json` `c0757233c49bc385f7430186cbacf1eed0b59ca00acd8ee0d233e62669f81626`; `unused-long-integer.json` `e972994748ed6e2aac6a7837e17d5e3053064d903526736186a62b986bd0f84c`
- `url-ascii-pipe.json` `83cff1355514af97e50f2eb7c054d61d29a1cfc4dcb7af6bbfd6782b49fd26e5`
No tools installed.