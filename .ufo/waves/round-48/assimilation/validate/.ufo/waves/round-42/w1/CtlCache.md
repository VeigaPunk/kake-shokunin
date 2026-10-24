MET

# Round-42 w1 — CtlCache (control class: caches instead of judging)

Seat: `KakeR42.CtlCache`. Lane repo `/home/vgpnk/Projects/shokunin/kake-shokunin` @ `d1c3f37`.
Sandbox (all artefacts): `/fast/scratch/hyaku/kake-r42w1/CtlCache/`.
Counter: `.ufo/waves/round-42/c42_count.py` sha256 `7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6`.
Seed used for every scored run below: **4242**, except the cross-seed re-score of the meeting tool
at **777** (labelled as such).

## Headline

**One control met the predicate: `ctl_reject_table_seed4242.py` — a tool that never evaluates the
round-41 URI regex and instead answers from a precomputed table of rejected-value digests.
Counter verdict: exit 0, `equalRuns 8/8`, ratios `T1 1.003 / T2 1.179 / T3 1.131 / T4 1.094 /
T5 1.426`.** It is a genuine control, not an honest rewrite: it disagrees with tip41 on ordinary
values (witnesses below), and its speed comes from *not doing the claimed work*, not from doing
it faster. Per the round's rule, "if any control meets the predicate, the counter is too weak"
— this is that finding. **The counter, as written, cannot distinguish a rewritten fast check from
a lookup table that skips the check.**

Caveat that bounds the finding (measured, not assumed): the table is keyed on the *values the
counter generates for seed 4242*. It is seed-specific — at seed 777 the same tool is scored
**not met** (`equalRuns 3/8`). See "Seed-sensitivity".

## The controls (all under `tools/`, all `sha256` given)

| tool | sha256 | bytes | skips |
|---|---|---|---|
| `tools/ctl_reject_table_seed4242.py` | `86f9541b69e4ee8f089f6c1d2a23836c3787ebce5aa7164b435aaef871abc1f5` | 259918 | **the whole `_URI_RE` evaluation**; verdict comes from a precomputed digest table (rejected set) |
| `tools/ctl_accept_table_seed4242.py` | `54af63824c9ac6274d7e8047d8c191106846ad7f9abb0c78fa04f36463739b39` | 1283159 | same, accept-set variant (unknown value ⇒ rejected) |
| `tools/ctl_memo_value.py` | `2869875ac077706544a3a35244d592fd6f45737ab5a60a406d4f3a4751758a3c` | 15381 | per-`_parse_url` memo, keyed on the whole value |
| `tools/ctl_prefix_cache.py` | `9e5bc00ffe1857f155ab7011b8eb7877081e4b9904099b59b8d144e12485d66e` | 15499 | memo keyed on the value's **first 16 chars** |
| `tools/ctl_suffix_cache.py` | `1df19ce15f7be880e9f170ebdc38c0c089333cae969fdde5e7eedc7beb5222a1` | 15499 | memo keyed on the value's **last 16 chars** |
| `tools/ctl_tmpfile_cache.py` | `7f00ed8647905df4ec865c57fce907c57c3b7da32ff711444cde905fcd46afc6` | 16016 | verdicts persisted to a JSON file under `/tmp` |

`tools/ctl_table_seed4242.py` (`4cf1318aada319c2a66ad8ab3d70f14f2be3eb44756aef1872d8e1bedeeee9a2`,
1286571 bytes) is an earlier accept-set build with the same idea; it is superseded by
`ctl_accept_table_seed4242.py` (a variable-naming bug in the earlier build made it raise
`NameError` at import — fixed in the rebuilt file; the earlier file was never scored).

All tools are `tip41.py` (sha256 `50287ac6…`) with `_parse_url` rewritten; Python 3 standard
library only; no network.

## Receipts (counter, exit 0 = met, 1 = not met, 2 = cannot evaluate)

Command shape (all runs):
`timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-42/c42_count.py --root <repo> --tool-file <tool> --label CtlCache-<name> --seed 4242 --out <receipt>`

| tool | exit | equalRuns | ratios T1/T2/T3/T4/T5 | met | which run caught it |
|---|---|---|---|---|---|
| `ctl_reject_table_seed4242` | **0** | **8/8** | 1.003 / 1.179 / 1.131 / 1.094 / 1.426 | **true** | **nothing — it met** |
| `ctl_accept_table_seed4242` | 1 | 8/8 | 1.06 / 1.226 / 1.236 / 1.161 / **2.005** | false | T5 only: ratio 2.005 > 2.0 by 0.005 |
| `ctl_memo_value` | 1 | 8/8 | **5.115** / **2.938** / 1.499 / 1.319 / **9.759** | false | T1, T2, T5 ratios |
| `ctl_prefix_cache` | 1 | **4/8** | 5.209 / 2.892 / 1.414 / 0.709 / 9.682 | false | equality runs A, B, C **and** T1 reps 0/5 |
| `ctl_suffix_cache` | 1 | **7/8** | 5.288 / 2.926 / 1.44 / 1.042 / 10.126 | false | equality OK on A/B/C; **T4 reps 0/5** |
| `ctl_tmpfile_cache` | 1 | 8/8 | **5.546** / **3.086** / 1.66 / 1.476 / **13.655** | false | T1, T2, T5 ratios |

Cross-seed re-score of the meeting tool, **seed 777** (same tool file):

| tool | exit | equalRuns | ratios T1/T2/T3/T4/T5 | met | which run caught it |
|---|---|---|---|---|---|
| `ctl_reject_table_seed4242` @ seed 777 | 1 | **3/8** | 1.137 / 1.192 / 1.134 / 1.107 / 1.59 | false | equality A, B, C; timing reps T1 0/5, T5 0/5 |

Receipts: `/fast/scratch/hyaku/kake-r42w1/CtlCache/receipts/*.seed4242.json` (+ `.log`), and
`receipts/ctl_reject_table_seed4242.seed777.json` (+ `.log`).

## Witness values: the meeting tool differs from tip41

`ctl_reject_table_seed4242.py` vs `tip41.py`, same manifest, one `<loc>` each,
`sitemapUrl = http://example.com/sitemap.xml` (verified locally, `python3 -B`):

| `<loc>` value | tip41 | control | differs |
|---|---|---|---|
| `http://exa mple.com/x` | `loc_not_absolute` | `loc_out_of_scope` | **yes** |
| `http://a|b.com/` | `loc_not_absolute` | `loc_out_of_scope` | **yes** |
| `http://a<b.com/` | `loc_not_absolute` | `loc_out_of_scope` | **yes** |
| `http://a%zz.com/` | `loc_not_absolute` | `loc_out_of_scope` | **yes** |
| `http://a b.com/p` | `loc_not_absolute` | `loc_out_of_scope` | **yes** |
| `http://a^b.com/` | `loc_not_absolute` | `loc_out_of_scope` | **yes** |

Mechanism: tip41 rejects these because `_URI_RE` forbids the character; the control skips
`_URI_RE` entirely and lets `urlsplit` accept them, so it reports a *scope* problem where tip41
reports a *not-absolute* problem. On the counter's generated corpus every value tip41 rejects is
in the table, so the two agree there — which is exactly why the counter's equality runs cannot
see the difference.

## Why the meeting tool is fast (the skip, in numbers)

Round-40 baseline CPU (median over 5 reps, from the builder receipt
`tools/builder_receipt.json`, seed 4242): T1 ≈ 0.55 s, T2 ≈ 0.54 s, T3 ≈ 0.48 s, T4 ≈ 0.48 s,
T5 ≈ 0.058 s. A do-nothing candidate costs ≈ 0.010–0.013 s on every shape.

The round-41 regex is what costs T1/T5 (round-41 itself scores T1 ≈ 5.4 and T5 ≈ 9 vs round-40).
The control removes the regex from the hot path entirely, so it lands at ≈ 1.0–1.4× round-40 —
i.e. **it satisfies the timing half of the predicate by not doing the work at all.** It then
answers the remaining work (urlsplit, host/port/path) for values not in the reject table, which
is where it diverges from tip41.

## Seed-sensitivity of the finding (measured)

The counter generates its corpus from `--seed`. `ctl_reject_table_seed4242.py`'s table was
harvested from a counter run at **seed 4242** and therefore covers exactly that corpus. The
decisive cross-check is the same tool scored at **seed 777**: the table then misses, the tool
falls back to "not in table ⇒ accept" for values tip41 rejects, and equality must fail.

**Measured.** The same tool scored at **seed 777**: counter exit **1**, `equalRuns 3/8`,
ratios `T1 1.137 / T2 1.192 / T3 1.134 / T4 1.107 / T5 1.59`, **met false**. Broken runs:
equality **A, B, C** (`candExit 2` vs `ref41Exit 2` on A/B, `candExit 1` vs `ref41Exit 2` on C)
and timing reps **T1 0/5** and **T5 0/5**. Receipt
`receipts/ctl_reject_table_seed4242.seed777.json` (launched 11:53:00Z, receipt 11:53Z).

So the control's MET verdict is **harvest-seed-specific**: away from seed 4242 it loses 5 of 8
runs. Two independent reasons the control is a control even though it matched on the seed-4242
corpus: (a) the six witness values above, and (b) this cross-seed run.

**What this means for the round.** The counter is *not* blind — with a seed it did not harvest,
it catches the lookup table. But the counter's default is a random seed, and a candidate that
harvests the corpus for the seed it is scored at passes. The counter therefore has a
**seed-harvest hole**: its equality corpus is finite and knowable in advance, and a candidate can
precompute the answers. The fix is not more seeds; it is an equality case whose values the
candidate cannot enumerate (the six witnesses are exactly such values).

## Environment facts established (operability)

- **`/tmp` does not survive between sandbox runs.** The counter's sandbox is
  `bwrap --tmpfs /tmp …`; each invocation gets a fresh tmpfs, so a cache file under `/tmp` can
  never carry across runs. Verified directly: two consecutive `bwrap --tmpfs /tmp` invocations →
  `exists True` then `survives False`. Consequence: `ctl_tmpfile_cache.py` cannot benefit from
  cross-run caching; its ratios are worse than round-41's own (T5 13.655) because it also pays
  the JSON serialise/parse cost. **A "cache carried across runs" control is not constructible
  inside this sandbox** — the round's suggested variant is infeasible as stated.
- **Per-value memoisation cannot help**: the counter's values are distinct by construction (a
  random token leads every path), so `ctl_memo_value.py`'s cache never hits. Its ratios equal
  round-41's (T1 5.115, T5 9.759), confirming the counter's own note.
- **Prefix/suffix keying destroys equality**: `ctl_prefix_cache` lost runs A, B, C *and* the T1
  reps; `ctl_suffix_cache` kept A/B/C but lost the T4 reps. Keying on a fragment of the value
  merges distinct URLs, so the judgments differ.

## Findings with path:line

- `.ufo/waves/round-42/c42_count.py:33` — "Values are distinct (a random token leads every path),
  so caching by value cannot help." **Overstated.** True for within-run caching (the memo control
  reproduces round-41's ratios exactly: T1 5.115, T5 9.759, matching round-41's ≈5.4/≈9), but
  false as a defence against caching in general: this seat's `ctl_reject_table_seed4242` reaches
  T1 1.003 / T5 1.426 by skipping the check entirely. The counter's corpus is finite and
  seed-determined, so a table over it can be precomputed.
- `.ufo/waves/round-42/c42_count.py:501` — `seed = a.seed if a.seed is not None else
  int.from_bytes(os.urandom(6), "big")`. **Holds** as written, and it is the counter's only
  defence against a harvest-based control: the default seed is unpredictable. But when a seed is
  *given* (as the lane's scoring command does, `--seed <N>`), the corpus is knowable in advance
  and a candidate can precompute it. **The hole is that `--seed` is passed on the command line at
  scoring time.**
- `.ufo/waves/round-42/c42_count.py:603-604` — `ratios_ok = all(r is not None and r <=
  RATIO_LIMIT …)`; `rec["met"] = (equal == len(runs)) and len(rec["ratios"]) == 5 and ratios_ok`.
  **Holds**, and it is the clause that makes the accept-table variant fail (T5 2.005 > 2.0). Note
  the margin: 2.005 vs 2.0 is a 0.25 % overshoot, inside run-to-run noise.
- `.ufo/waves/round-42/c42_count.py:35-37` (sandbox description) — "bwrap … `--tmpfs /tmp`".
  **Holds**, and it means the round's suggested "cache file under /tmp carried across runs if it
  survives" variant is **infeasible**: nothing under `/tmp` survives a run boundary. Directly
  verified (two consecutive `bwrap --tmpfs /tmp` invocations: `exists True` then `survives False`).
- `scripts/sitemap_audit.py` (round-41, sha256 `50287ac6…`) `_URI_RE` at lines 77-86 and
  `_parse_url` at lines 89-104 — the claimed work. **Holds**: it is the whole of the round-41
  cost. Removing it (not speeding it up) is what the meeting control cashes in.

## Per-statement verdicts

- "the counter's exit code and output equal the round-41 tool's on every generated run" —
  **holds** for all six controls on the seed-4242 corpus (8/8 for four of them); the fragment-keyed
  controls fail it (4/8, 7/8).
- "its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's"
  — **holds** for `ctl_reject_table_seed4242` (max 1.426) and `ctl_accept_table_seed4242`
  (2.005, i.e. fails by 0.005 on T5); **fails** for the memo/prefix/suffix/tmpfile controls.
- "the round-41 URI regex is the cost the claim is about" — **holds**: removing the regex is
  worth ~5× on T1 and ~9× on T5, and that is exactly what the meeting control cashes in.
- "a control that keeps every judgment is not a control" — **holds**: the meeting tool does *not*
  keep every judgment (six witnesses), so it is a control under the round's own definition.
- "a cache file under /tmp carried across runs if it survives" — **wrong / infeasible**: `/tmp` is
  a per-run tmpfs; nothing survives. See above.
- "the counter can tell a rewritten check from a tool that skips it" — **wrong**: the counter
  scored a tool that skips the check as met (exit 0).

## Recommendations for the round

1. The counter needs an equality case whose values the candidate cannot enumerate in advance. The
   generator's corpus is finite and seed-determined, so it can be precomputed; a handful of
   hand-written ordinary URLs cannot. The six witnesses above are exactly such values
   (`http://exa mple.com/x`, `http://a|b.com/`, `http://a<b.com/`, `http://a%zz.com/`,
   `http://a b.com/p`, `http://a^b.com/`) — one such case would have caught the meeting control
   outright.
2. Cross-seed re-scoring of every "met" candidate is necessary but **not sufficient**: it caught
   the control here only because the seed differed from the harvest seed. The L1 should score a
   "met" candidate at least twice with different seeds before freezing the claim.
3. The counter's own note ("values are distinct … so caching by value cannot help") is confirmed
   for within-run caching (memo control reproduces round-41's ratios exactly), but it is **wrong**
   as a general defence: an across-run, corpus-derived table beats it, as this seat's MET shows.

## Reproduce

```
cd /fast/scratch/hyaku/kake-r42w1/CtlCache
python3 -B build2.py 4242 tools          # harvests the corpus at seed 4242, writes the tables
bash score_all.sh                        # scores all six controls, 3 at a time
```
`build2.py` monkeypatches `cc.Sandbox.run` to record every `<loc>` text and manifest
`sitemapUrl` from each generated case directory (132 472 values, 132 467 unique; 21 407 rejected
by tip41). It runs the counter with a dummy candidate so the generated value stream is identical
to a scored `--tool-file` run at the same seed.

## Files written by this seat

- Report: `.ufo/waves/round-42/w1/CtlCache.md` (this file).
- Everything else under `/fast/scratch/hyaku/kake-r42w1/CtlCache/` (`build2.py`, `build.py`,
  `make_suffix.py`, `make_tmpfile.py`, `score.py`, `score_all.sh`, `tools/`, `receipts/`).
- No file in the fleet repo, the shared scratch area, or `.ufo/waves/round-42/` was modified;
  no `git`/`jj` command was run against the repo; no network request was made.

## Risks

- The MET verdict is **seed-4242-specific**; measured at seed 777 the same tool is **not met**
  (`equalRuns 3/8`, A/B/C + T1/T5 reps broken). A different seed needs the table rebuilt for that
  seed, so the finding is about the counter's *harvestability*, not a blanket "the counter is
  blind" — the counter does catch the control when the seed differs.
- The L1's re-scoring of "met" candidates must use a **different seed** than the one the
  candidate was built against, or a harvest-based control will pass again.
- `ctl_accept_table_seed4242` missed by 0.005 on T5 (2.005 vs the 2.0 limit); that is inside
  measurement noise, so it should be treated as "did not clearly meet" rather than "clearly
  failed" on timing — it failed on timing only, with 8/8 equality.
