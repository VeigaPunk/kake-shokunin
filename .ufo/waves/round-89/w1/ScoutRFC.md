# ScoutRFC — round 89 report (lane-internal)

Full evidence: `.ufo/waves/round-89/w1/ScoutRFC/findings.md`; receipts in `w1/ScoutRFC/receipts/`.

## Registry-row facts (RFC 9111 and RFC 9110)

- RFC 9111 `https://www.rfc-editor.org/rfc/rfc9111.txt`: HTTP 200, 84477 bytes, sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`, UTC 2026-11-04T21:13:39Z.
- RFC 9110 `https://www.rfc-editor.org/rfc/rfc9110.txt`: HTTP 200, 502941 bytes, sha256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`, UTC 2026-11-04T21:13:41Z.
- RFC 9111 §4.1 nominated-field sentence: lines 530–532 (sentence 528–534). RFC 9110 §5.6.1.2 empty-element sentence: lines 1695–1697. `Vary` production: RFC 9110 §12.5.5, line 5675, `Vary = #( "*" / field-name )`.
- Highest S id at base: S463. At HEAD `acc69ba5`: S465. Both URLs already appear in the registry (rfc9111.txt in S456; rfc9110.txt in S028, S033, S453–S455).
- Registry shape: 11 columns (NF 13); template row S463 at base line 210.
- Round-88 `## Gate`: admit 2 (lines 33, 34), reject 2 (lines 35, 36). Agrees with item B.

## Defects found (exact commands and exits in findings.md §5–6)

1. **C2 guard bypass (blocks C2).** A candidate that reads the reference from `.ufo/waves/round-89` at run time scores frozen 16/16, props 200/200, refuse 9/9, guard `None`, so met would be true. The v1 guard refused it; v2 relaxed the tokens. The contract's "no read under .ufo/waves" rule is not enforced.
2. **C2 URI escaping has no killing property.** Mutant `key = uri +` scores 16/16, 200/200, 9/9 (met=true). A collision is demonstrated: `uri="x"`+header `a=v` equals `uri="x\x1fa\x1ev"` with no headers.
3. **C1 item E not revision-pinned.** At base `76225160` the counter now prints open=5, not the committed control's open=6 (exit 1 unchanged).
4. **C1 item E misses post-dispatch freeze amendment (R88-E repeat).** `46a43e94` (freeze v2) postdates dispatch `2e700b9a`; item E returns [] at HEAD.
5. **C1 at HEAD: item A open.** `open=1`: SCORECARD.md:5469, :5488 and round-88.md:265 keep `22/22` untagged (exit 1).
6. **Round-88 lesson factually wrong.** It says S463 is absent (lines 37–40, 191–196); base and `55d67f15` show S463 present.

Equivalent (not a defect): mutant `names-not-escaped` (token-restricted names).

## Limits

Response headers not retained. The C2 counter's selftest was run with inherited TMPDIR. Live tree changed during my run, so simulations used `git archive` snapshots. One 1-line file was written to `/tmp` and removed (disclosed).

## Tooling

No installs. Used `curl 8.23.0`, `git` (read-only), `python3`, `awk`, `sha256sum`. Pacman untouched.

## Scratch

`/fast/scratch/hyaku/kake-r89/ScoutRFC/` created and deleted before yield.
