# CriticC2Repair — C2 pre-landing falsification

Axes: **freshness** (receipt-derived ledger accuracy and provenance), **operability** (the checker's last-match/rounding behavior). Scope: review only; no judgment, admission, production edit, integration, or other evaluation runtime.

## Result

- **(a) PASS:** master has 14 direct-child JSON rescore receipts and **14 distinct `toolSha256` values**, with no duplicate SHA groups.
- **(b) PASS:** `ref41-base.json` ratios are T1 **4.207** and T5 **7.047**, hence **4.21 / 7.05** at two decimals.
- **(c) PASS:** build receipt extrema are T1 **1.004–1.009**, T5 **1.105–1.215**, hence **1.00–1.01 / 1.11–1.22** at two decimals using `Decimal`/`ROUND_HALF_UP`. Those displayed endpoints are rounded values, not the exact unrounded extrema. T5's .005 ties make the rounding rule material.
- **(d) PASS at the inspected appended worktree:** the final matching repair phrases are `SCORECARD.md:3575–3576`, `LOG.md:1703`, and `LOG.md:1706`. No matching phrase occurs later in either file. Historical wrong figures precede the corrections; the subsequent parenthetical old-number reminders omit the matching labels/phrase and do not supersede them.
- **Fixable provenance defect found in the repair prose:** the numerical repairs survive all four named attacks, but the explanation of the earlier errors overstates what its evidence establishes. Details below. This is not a numeric counterexample or a round verdict.

## Work and exact commands

Read `.ufo/waves/round-44/verification/ledger-before.txt`, `scripts/ledger_latest_check.py:1-298`, its fixed `.ufo/waves/round-44/ledger-quotes.json`, the C2 declaration/amendments, and the relevant ledger append sections. The checker fixes all three figures in code; reads receipts through `git show master:<path>`; selects the final `re.finditer` match using `re.S`; and rounds with `ROUND_HALF_UP` to the quoted precision. I did not import or execute the checker in my independent derivation.

Shell commands (cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`):

```sh
mkdir -p /fast/scratch/hyaku/kake-r44/CriticC2Repair
git ls-tree -r --name-only master -- .ufo/waves/round-43/verification/l1-rescores .ufo/waves/round-43/verification/freeze
python3 -B /fast/scratch/hyaku/kake-r44/CriticC2Repair/derive_receipts.py
```

The scratch script independently parses `git show` JSON with `parse_float=Decimal`, enumerates direct-child `.json` names from `git ls-tree`, forms the set of `toolSha256` values, derives the ratios and extrema, and rounds to two decimals. Every Git subprocess it actually executed appears verbatim below. `master` remained `18cb2c28f47c3ec3732ffa06c456e61b3444b1a2` throughout.

### Baseline evidence (read, not rerun)

Verbatim `.ufo/waves/round-44/verification/ledger-before.txt`:

```text
rescore-tally MISMATCH quoted=18 derived=14 SCORECARD.md:3393
donothing-ratios MISMATCH quoted=T1 4.27, T5 8.68 derived=T1 4.21, T5 7.05 LOG.md:1661
build-ratio-range MISMATCH quoted=T1 1.00–1.02, T5 1.13–1.18 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:1660
ledger-quotes: 3 figures, 3 mismatches
```

### (a)–(c): verbatim independent derivation output

```text
$ git rev-parse master
master_before=18cb2c28f47c3ec3732ffa06c456e61b3444b1a2
$ git ls-tree -r --name-only master -- .ufo/waves/round-43/verification/l1-rescores
direct_json_receipts=14
$ git show master:.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V1c.json
.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V1c.json toolSha256=00ece64886137a23b1b6a8e7f7795885d2e23ae3c1c2a0dfdb8f05f085503238
$ git show master:.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V2b.json
.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V2b.json toolSha256=012527ff78763caf8e20bc244cf5c7d899436e026c06fb4e9e43809f700c10bf
$ git show master:.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V4b.json
.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V4b.json toolSha256=52fb29a7f74b5898d3eaf82933f0d530ea2d09862c46511b6ed5ded5faeee7c6
$ git show master:.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V7c.json
.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V7c.json toolSha256=56eda048b6bfcc4d569e23ddf4bf02261c960ceff110971357e0a93d52f615ea
$ git show master:.ufo/waves/round-43/verification/l1-rescores/CtlHostTable-A_expanded46_fixed.json
.ufo/waves/round-43/verification/l1-rescores/CtlHostTable-A_expanded46_fixed.json toolSha256=25e84d0d56f7acaef33f331f73e6c0ff21ac2466e31ae786fc4a26114b3087a9
$ git show master:.ufo/waves/round-43/verification/l1-rescores/CtlHostTable-B_expanded46_nogrammar.json
.ufo/waves/round-43/verification/l1-rescores/CtlHostTable-B_expanded46_nogrammar.json toolSha256=f852dff164f7dd94a13c43c38906457c5e9724af391a7079f5673263420ac4d7
$ git show master:.ufo/waves/round-43/verification/l1-rescores/CtlHostTable-F_provable_hosttable.json
.ufo/waves/round-43/verification/l1-rescores/CtlHostTable-F_provable_hosttable.json toolSha256=ac3f0009fd2d1894c6bda1a15e16fab1d035aaee5f2c5a0fd87a0d40df3799bf
$ git show master:.ufo/waves/round-43/verification/l1-rescores/p48_noreval.json
.ufo/waves/round-43/verification/l1-rescores/p48_noreval.json toolSha256=4e5064fccdac11262107d2005a6c88923a621e64b9d3c37787f7f78e66d2234b
$ git show master:.ufo/waves/round-43/verification/l1-rescores/v3_memo_validity_lower.json
.ufo/waves/round-43/verification/l1-rescores/v3_memo_validity_lower.json toolSha256=bec3fd0cc443ca914a14a0b450737ef8e1e9539691f929f66a913db776969df3
$ git show master:.ufo/waves/round-43/verification/l1-rescores/v4_cache_portlen_with_path.json
.ufo/waves/round-43/verification/l1-rescores/v4_cache_portlen_with_path.json toolSha256=1b34f83d4b45346dd22628064ffb5cda451ea9922b1168933b781648262df58b
$ git show master:.ufo/waves/round-43/verification/l1-rescores/v4_memo_validity_lower_short.json
.ufo/waves/round-43/verification/l1-rescores/v4_memo_validity_lower_short.json toolSha256=5c9158fb9ca98b783768fda314fbba1ae481f04ef0e0017964a4d07ae9992063
$ git show master:.ufo/waves/round-43/verification/l1-rescores/v5_abbrev_window_6plus.json
.ufo/waves/round-43/verification/l1-rescores/v5_abbrev_window_6plus.json toolSha256=e55e3bfb9a6e9f3523a9c1393e14a2defdadd2ae7c2b4104e12cd717a51e76f5
$ git show master:.ufo/waves/round-43/verification/l1-rescores/v7_memo_value_lower_nonascii.json
.ufo/waves/round-43/verification/l1-rescores/v7_memo_value_lower_nonascii.json toolSha256=d41f0f1b06315604b03eb44e1b0a4609ac7340d8a566d9e6216a5f6fd52659f8
$ git show master:.ufo/waves/round-43/verification/l1-rescores/v8_memo_value_casefold_nonascii.json
.ufo/waves/round-43/verification/l1-rescores/v8_memo_value_casefold_nonascii.json toolSha256=29070eed5a2c54ffe1619973057a2383d4e671c4235a408af7db66f5016126fa
A distinct_toolSha256=14 expected=14 PASS
duplicate_sha_groups=0
$ git show master:.ufo/waves/round-43/verification/freeze/ref41-base.json
B ref41-base T1 raw=4.207 rounded_2dp=4.21
B ref41-base T5 raw=7.047 rounded_2dp=7.05
B expected=T1 4.21, T5 7.05 PASS
$ git show master:.ufo/waves/round-43/verification/freeze/build-1.json
C build-1 T1 raw=1.005 rounded_2dp=1.01
C build-1 T5 raw=1.105 rounded_2dp=1.11
$ git show master:.ufo/waves/round-43/verification/freeze/build-2.json
C build-2 T1 raw=1.009 rounded_2dp=1.01
C build-2 T5 raw=1.144 rounded_2dp=1.14
$ git show master:.ufo/waves/round-43/verification/freeze/build-3.json
C build-3 T1 raw=1.004 rounded_2dp=1.00
C build-3 T5 raw=1.215 rounded_2dp=1.22
C extrema T1 raw_min=1.004 raw_max=1.009 rounded_2dp=1.00–1.01
C extrema T5 raw_min=1.105 raw_max=1.215 rounded_2dp=1.11–1.22
C expected=T1 1.00–1.01, T5 1.11–1.22 PASS
$ git rev-parse master
master_after=18cb2c28f47c3ec3732ffa06c456e61b3444b1a2
master_stable=True
```

### (d): matching-phrase and later-suffix sweeps

Used the specialized `grep` tool, not a shell search. The following exact pattern adds redundant `|\n` alternatives to `\s`, enabling the tool's multiline search without changing the checker's matching language:

```text
re-scored(?:\s|\n)+(\d+)(?:\s|\n)+of(?:\s|\n)+the(?:\s|\n)+27|not met \(T1(?:\s|\n)+([\d.]+),(?:\s|\n)*T5(?:\s|\n)+([\d.]+)\)|T1(?:\s|\n)+([\d.]+)–([\d.]+), T5(?:\s|\n)+([\d.]+)–([\d.]+)
```

Full-file arguments: `path=/home/vgpnk/Projects/shokunin/kake-shokunin/LOG.md;/home/vgpnk/Projects/shokunin/kake-shokunin/SCORECARD.md`, `case=true`, `gitignore=false`, `skip=0`.

Decisive excerpts copied verbatim from that post-append tool output (ellipsis separates excerpts, not omitted matches after the repair):

```text
## LOG.md#2741
 1702:  naming its receipt and derived value): (1) the do-nothing (round-41 tool at base) remains
*1703:  not met (T1 4.21, T5 7.05) per `.ufo/waves/round-43/verification/freeze/ref41-base.json`
 1704:  (the "4.27, 8.68" two entries above counted pre-freeze timings; the receipt-derived
 1705:  ratios are 4.21 and 7.05). (2) The held build `020bc457` met ×3 with ratio range
*1706:  T1 1.00–1.01, T5 1.11–1.22 over
 1707:  `.ufo/waves/round-43/verification/freeze/build-{1,2,3}.json` (the "1.00–1.02, 1.13–1.18"
 1708:  entry above quoted the settle-prose rounding, not the receipt extrema). (3) The rescore
 1709:  tally repair is recorded in SCORECARD.md under "Round 44 — C2 repair and measurement".
```

```text
## SCORECARD.md#2DBB
 3574:Routed repair for the round-43 verifier spot-check §8.1 (receipt-derived, value re-derived by
*3575:`scripts/ledger_latest_check.py` from the committed receipts at `master`): the L1 re-scored
14 of the 27 live-seat controls — the committed receipts
...
 3577:`.ufo/waves/round-43/verification/l1-rescores/*.json` at master carry 14 distinct
 3578:`toolSha256` values; the "18" in the round-43 correction above counted seat reports, not
 3579:receipts. This line is the last statement of the rescore-tally figure.
```

Same pattern/flags, exact suffix arguments:

```text
path=/home/vgpnk/Projects/shokunin/kake-shokunin/LOG.md:1707-;/home/vgpnk/Projects/shokunin/kake-shokunin/SCORECARD.md:3577-
```

Verbatim decisive suffix output:

```text
No matches found
```

The full-file sweep also finds only historical matches at LOG 1631, 1660–1662 and SCORECARD 3393 before these repairs. The rescore correction spans a newline; the multiline sweep finds it, as `latest_match(..., re.S)` with `\s+` does.

## Counterexample: repair provenance, not the corrected figures

At the inspected append, `LOG.md:1708` attributes the old build range to “settle-prose rounding.” Existing local evidence attributes it to different, discarded measurements, not rounding of the committed receipts. Verbatim `SCORECARD.md:3335–3339` read output:

```text
3335:1. Stale prose numbers (found by `RevengerFreeze` + `CriticC1Sizing`): the freeze section's quoted
3336:   ratios came from discarded pre-T2-fix receipts. True committed values: ref41-base (seed 43001)
3337:   T1 4.207, T2 1.917, T3 1.152, T4 1.228, T5 7.047; build-1..3 (seeds 9325990526163,
3338:   265206435053987, 269853680553917) T1 1.004–1.009, T2 1.201–1.250, T3 1.318–1.334,
3339:   T4 1.211–1.266, T5 1.105–1.215. Verdicts unchanged. Per-source numbers stay distinct hereafter.
```

`corpus/lessons/round-43-verifier-spotcheck.md:59–61` and `.ufo/waves/round-43/w1/CriticC1Sizing.md:17` corroborate the discarded pre-T2-fix provenance. The historical frozen values at SCORECARD 3222–3223 are T1 1.002–1.020 and T5 1.129–1.179, which round to the old LOG ranges; they are not rounding variants of the actual committed extrema derived above.

The appended tally explanation, `SCORECARD.md:3578`, says the old 18 “counted seat reports.” The independent receipt derivation does not establish that cause. Verbatim existing verifier finding:

```text
197:1. **Re-score tally overstates its receipts.** Report Before → after and `SCORECARD.md:3393` say
198:   "L1 re-scored 18 of 27"; `verification/l1-rescores/` holds **14** re-score receipts (11 in
199:   `exits.txt` + 3 in `exits2.txt`, 14 distinct `toolSha256`), and no other committed set carries
200:   the remaining four. The 27 tally itself verifies. Third instance this round of the
201:   stale-numbers class mined as Mistakes 7/9. Route to r44.
```

Additional exact specialized search: pattern `pre-freeze timings|settle-prose rounding|counted seat reports|4\.27|8\.68|18 of the 27`, paths `.ufo/waves/round-43;corpus/lessons/round-43*` under the lane root, `case=false`, `gitignore=false`, `skip=0`. It found the stale numerical brief copies and the discarded-receipt findings cited above, not evidence establishing a seat-report-count origin for 18. That causal attribution is **unestablished in this bounded sweep**, not disproven globally.

**Smallest safe correction:** retain the three derived repair values and receipt pointers, but replace the range's explanatory clause with the supported “supersedes the earlier discarded pre-T2-fix values,” or simply “supersedes the earlier quoted values.” Replace the tally's causal explanation with “the earlier 18 is unsupported by the committed receipts,” unless a specific additional source establishes why it was written. This changes no receipt, contract, axis, or frozen instrument. It is a fixable freshness/provenance defect, not a necessary axis tradeoff. I sent these findings to `kake-r44.ScribeC2Repairs`; I did not edit their files.

## Files written, checks, blockers

Every file I wrote:

1. `/fast/scratch/hyaku/kake-r44/CriticC2Repair/derive_receipts.py`
2. `.ufo/waves/round-44/w2/CriticC2Repair.md` (this report)

Created directory: `/fast/scratch/hyaku/kake-r44/CriticC2Repair/`.

No production files, frozen receipts, class modules, LOG, SCORECARD, or lane history were written by me. No tool installs or updates. No blocker to the assigned derivations/sweep.

**Unrun by this seat:** `python3 -B scripts/ledger_latest_check.py --root .`, its `--selftest`, all C1 counters/audits, tests/builds/linters, and the canonical Rust judge. No exit-0 C2 measurement is claimed here. Main should run the fixed C2 counting command after the final ledger writers finish. The appended prose contained an exit-0 pointer while my review had not exercised that command; that pointer is not my verification evidence.

## Addendum — append-ready scribe draft reviewed

After the initial review, `kake-r44.ScribeC2Repairs` supplied `/fast/scratch/hyaku/kake-r44/c2-repairs.md` (snapshot `7E33`). That seat wrote a **draft only**, not the existing ledger appends. The provenance defect above concerns the already-present worktree prose, **not** the scribe's draft.

I read draft lines 1–115. Its three fenced `text` blocks are to be appended as P1 to SCORECARD EOF and P2 then P3 to LOG EOF. They use neutral supersession wording: the tally says the old 18 lacks the remaining four committed receipts; the ratio blocks do not assert causes for the old figures. **These draft blocks survive the four assigned arithmetic/last-match attacks and avoid the reported provenance defect.** No canonical checker execution or claim judgment is implied.

Exact specialized sweep: same multiline pattern/flags as §(d), with `path=/fast/scratch/hyaku/kake-r44/c2-repairs.md:32-73`. Verbatim decisive output:

```text
[/fast/scratch/hyaku/kake-r44/c2-repairs.md#7E33]
 35:Routed repair for the round-43 verifier spot-check §8.1 "Re-score tally overstates its
*36:receipts" (`corpus/lessons/round-43-verifier-spotcheck.md:197-201`): the L1 re-scored 14 of the 27
 37:live-seat controls. The committed receipts
 38:`.ufo/waves/round-43/verification/l1-rescores/*.json` at `master` are 14 JSON receipts — 11
 39:named in `exits.txt` and 3 in `exits2.txt`, all exit 0 — and they carry 14 distinct
...
 55:  `equalRuns 11/11`) gives `ratios.T1` 4.207 and `ratios.T5` 7.047, so the receipt-derived
*56:  figures are not met (T1 4.21, T5 7.05). This supersedes the T1 4.27 / T5 8.68 values
 57:  quoted in the round-43 entry above.
 58:```
 59:
...
 70:  1.005 / 1.009 / 1.004 and T5 ratios 1.105 / 1.144 / 1.215, so the receipt-derived extrema are
*71:  T1 1.00–1.01, T5 1.11–1.22 (build-1/build-2/build-3 at `master`). This supersedes the T1
 72:  1.00–1.02 and T5 1.13–1.18 range quoted in the round-43 entry above.
 73:```
```

Same pattern/flags on exact post-match block suffixes:

```text
path=/fast/scratch/hyaku/kake-r44/c2-repairs.md:37-43;/fast/scratch/hyaku/kake-r44/c2-repairs.md:57-58;/fast/scratch/hyaku/kake-r44/c2-repairs.md:72-73
```

Verbatim output:

```text
No matches found
```

I also checked the draft's added exit-status statement with this exact command (lane cwd):

```sh
git show master:.ufo/waves/round-43/verification/l1-rescores/exits.txt master:.ufo/waves/round-43/verification/l1-rescores/exits2.txt
```

Verbatim output:

```text
v4_cache_portlen_with_path exit=0
CtlHeadTail-V7c exit=0
v5_abbrev_window_6plus exit=0
CtlHeadTail-V1c exit=0
p48_noreval exit=0
v4_memo_validity_lower_short exit=0
CtlHeadTail-V2b exit=0
v7_memo_value_lower_nonascii exit=0
v8_memo_value_casefold_nonascii exit=0
v3_memo_validity_lower exit=0
CtlHeadTail-V4b exit=0
A_expanded46_fixed exit=0
B_expanded46_nogrammar exit=0
F_provable_hosttable exit=0
```

Smallest safe integration correction remains neutral supersession wording, as the draft already uses. Keep only the intended fenced ledger blocks, in their named files and order; the surrounding draft table/notes are not ledger append text. I relayed the scoped review to the scribe. This addendum changes only my report; the complete file-write inventory and unrun-check list above remain unchanged.
