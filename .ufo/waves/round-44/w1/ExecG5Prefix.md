# Kake R44 W1 — ExecG5Prefix

## Axes and implementation

Axes: **operability** and **freshness**. This item targets operability by making the G5 generator reliably exercise parse-cache key collisions; it does not change freshness behavior.

Updated `.ufo/waves/round-44/classes/g5_prefix_cut_45plus.py` only. It returns 100 `prefixpair` units / 200 values: ten clean-first pairs at each cut 44, 45, 48, 64, 65, and 80, plus forty clean-first pairs with identical first and last 48 code points and a one-character defect in the middle. Each prefix pair shares the first `cut` code points and differs at the cut; the head/tail pairs are over 96 code points and preserve both cache windows. Defects are selected only from the existing case-invariant defect set's one-character members, so they cannot shift the shared window. Pair order puts the clean value first, making the cached parse reusable for the invalid second value.

Unit/control attribution:

- `prefixpair` cut 45 pairs exercise `headtail-V7-prefix-cache45.py`.
- `prefixpair` cut 48 pairs exercise `prefixcache-p48-noreval.py`.
- `prefixpair` cut 64 pairs exercise `headtail-V1-prefix-cache64.py`.
- The `prefixpair` head/tail-middle subgroup exercises `headtail-V2-headtail-key48.py` (same first 48 and last 48; defect strictly between them).
- Cuts 44, 65, and 80 retain the neighboring-cut coverage; cuts 65 and 80 also collide with the first-64 cache window.

## Probe commands and final evidence

All commands ran from `/home/vgpnk/Projects/shokunin/kake-shokunin`. Probe exit 1 is the required witness result. Each output excerpt below preserves the probe JSON fields requested (the longer output tails are omitted).

```text
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G5 --tool-file .ufo/waves/round-44/controls-r43/headtail-V1-prefix-cache64.py --seed 4401
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G5 --tool-file .ufo/waves/round-44/controls-r43/headtail-V1-prefix-cache64.py --seed 4402
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G5 --tool-file .ufo/waves/round-44/controls-r43/headtail-V2-headtail-key48.py --seed 4401
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G5 --tool-file .ufo/waves/round-44/controls-r43/headtail-V2-headtail-key48.py --seed 4402
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G5 --tool-file .ufo/waves/round-44/controls-r43/headtail-V7-prefix-cache45.py --seed 4401
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G5 --tool-file .ufo/waves/round-44/controls-r43/headtail-V7-prefix-cache45.py --seed 4402
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G5 --tool-file .ufo/waves/round-44/controls-r43/prefixcache-p48-noreval.py --seed 4401
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G5 --tool-file .ufo/waves/round-44/controls-r43/prefixcache-p48-noreval.py --seed 4402
```

```json
{
 "probe": "G5", "seed": 4401, "units": 100, "values": 200,
 "ref41Exit": 1, "candExit": 1,
 "ref41OutSha256": "c16ebc3c1df63110c87818bd0ad80f93eb836b026c8a54249b1ba384ddf457ef",
 "candOutSha256": "b168b2f9c4de958a171e3abb806f246c07b6ab40b8af9ef35c65b926df9ce9ae", "equal": false
}
{
 "probe": "G5", "seed": 4402, "units": 100, "values": 200,
 "ref41Exit": 1, "candExit": 1,
 "ref41OutSha256": "14f73a097dbfa4c49f02cc9481205712e78ecdc91c901cc760ada7055afb70f1",
 "candOutSha256": "a15f9d74575b90dd189647120c025fb0b463e1724e9926cbf29196486501c629", "equal": false
}
{
 "probe": "G5", "seed": 4401, "units": 100, "values": 200,
 "ref41Exit": 1, "candExit": 1,
 "ref41OutSha256": "c16ebc3c1df63110c87818bd0ad80f93eb836b026c8a54249b1ba384ddf457ef",
 "candOutSha256": "5e1fb64561324f13260af7dd723a788974b1a721c26bf07ec8e5831be74fd208", "equal": false
}
{
 "probe": "G5", "seed": 4402, "units": 100, "values": 200,
 "ref41Exit": 1, "candExit": 1,
 "ref41OutSha256": "14f73a097dbfa4c49f02cc9481205712e78ecdc91c901cc760ada7055afb70f1",
 "candOutSha256": "baa4f55bdc29c9d09dc486223b8b869ff73cd5cb3f27d262e2b9ecc58347c54b", "equal": false
}
{
 "probe": "G5", "seed": 4401, "units": 100, "values": 200,
 "ref41Exit": 1, "candExit": 1,
 "ref41OutSha256": "c16ebc3c1df63110c87818bd0ad80f93eb836b026c8a54249b1ba384ddf457ef",
 "candOutSha256": "ebee0ba7ffcd05c91a6eab9bbaaf739c7c4b0d727de63e70ee15346a59770a61", "equal": false
}
{
 "probe": "G5", "seed": 4402, "units": 100, "values": 200,
 "ref41Exit": 1, "candExit": 1,
 "ref41OutSha256": "14f73a097dbfa4c49f02cc9481205712e78ecdc91c901cc760ada7055afb70f1",
 "candOutSha256": "5474134fd857779598a91563982216c841894072f98c6460db2445a8c81e2939", "equal": false
}
{
 "probe": "G5", "seed": 4401, "units": 100, "values": 200,
 "ref41Exit": 1, "candExit": 1,
 "ref41OutSha256": "c16ebc3c1df63110c87818bd0ad80f93eb836b026c8a54249b1ba384ddf457ef",
 "candOutSha256": "5ec81ea3eb73407522ba597a3b3ed140852bd047c075526e1771debcf73e5978", "equal": false
}
{
 "probe": "G5", "seed": 4402, "units": 100, "values": 200,
 "ref41Exit": 1, "candExit": 1,
 "ref41OutSha256": "14f73a097dbfa4c49f02cc9481205712e78ecdc91c901cc760ada7055afb70f1",
 "candOutSha256": "a0234cb553fe70d3fde785b3b39efb6fd0cca8f03da19f2593d7be05470902d5", "equal": false
}
```


Before editing, the same eight probe commands were also run against the supplied class. All eight returned `units: 100`, `values: 200`, `ref41Exit: 1`, `candExit: 1`, and `equal: false`; final acceptance evidence above is post-edit.

## Files and other commands

- Wrote `.ufo/waves/round-44/classes/g5_prefix_cut_45plus.py`.
- Wrote `.ufo/waves/round-44/w1/ExecG5Prefix.md` (this report).
- Created the empty scratch directory `/fast/scratch/hyaku/kake-r44/ExecG5Prefix` with `mkdir -p /fast/scratch/hyaku/kake-r44/ExecG5Prefix` (no output; no scratch files).
- No tools installed. No other checks run. Blocker: none.
