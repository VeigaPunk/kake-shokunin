# G1 long-port grammar class

Axes: operability and freshness; this move targets operability.

## Change

Wrote `.ufo/waves/round-44/classes/g1_longport_grammar.py`. `cases(rng, h)` emits 298 distinct malformed-percent values alternating `loc` and `sitemapUrl`, each with a six-to-eight-digit in-range port. Exactly 149 defects are after a long first path segment (past the 64-code-point prefix window); the others are in the first path segment or query. It adds one two-value cache-key witness pair, so the run has 299 units and 300 values. The pair is intentionally isolated from the malformed corpus: it distinguishes V4's cache key dropping port digits while keeping digit length.

## Probe commands and retained JSON

Setup command: `mkdir -p /fast/scratch/hyaku/kake-r44/ExecG1LongPort /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/w1` (no output).

Working directory for all commands: `/home/vgpnk/Projects/shokunin/kake-shokunin`.

Required port-length controls: each probe returned exit 1 (witness) for both seeds.

`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G1 --tool-file .ufo/waves/round-44/controls-r43/portlen-v1-skip-grammar-6plus.py --seed 44001`

`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G1 --tool-file .ufo/waves/round-44/controls-r43/portlen-v1-skip-grammar-6plus.py --seed 44002`

`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G1 --tool-file .ufo/waves/round-44/controls-r43/portlen-v5-abbrev-window-6plus.py --seed 44001`

`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G1 --tool-file .ufo/waves/round-44/controls-r43/portlen-v5-abbrev-window-6plus.py --seed 44002`

`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G1 --tool-file .ufo/waves/round-44/controls-r43/portlen-v4-cache-portlen.py --seed 44001`

`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G1 --tool-file .ufo/waves/round-44/controls-r43/portlen-v4-cache-portlen.py --seed 44002`

Decisive JSON fields, copied from the probe output:

```json
{
 "probe": "G1",
 "seed": 44001,
 "units": 299,
 "values": 300,
 "ref41Exit": 2,
 "candExit": 1,
 "ref41OutSha256": "0002484a4b4deb14185086d3106119bba5b109621e6d82ac324d20559b36a787",
 "candOutSha256": "b33422606cdadef5d1ed904e7d10e27fa42ab0fd03de3b4334cc155e105d4cde",
 "equal": false
}
{
 "probe": "G1",
 "seed": 44002,
 "units": 299,
 "values": 300,
 "ref41Exit": 2,
 "candExit": 1,
 "ref41OutSha256": "618a370f5255c01184d0ed57a31ca56705b4a6d7c8adfdd6907ff7a31c3fd342",
 "candOutSha256": "83240a3ef3c3e43dbed6e3f9ca69828d568be85b7dc1839ebf5f8b94ec29e935",
 "equal": false
}
{
 "probe": "G1",
 "seed": 44001,
 "units": 299,
 "values": 300,
 "ref41Exit": 2,
 "candExit": 2,
 "ref41OutSha256": "0002484a4b4deb14185086d3106119bba5b109621e6d82ac324d20559b36a787",
 "candOutSha256": "f521b0bf4113871d3d3c0984a7ab3c587d3940f6d885db26d32d15e3d55c1fed",
 "equal": false
}
{
 "probe": "G1",
 "seed": 44002,
 "units": 299,
 "values": 300,
 "ref41Exit": 2,
 "candExit": 2,
 "ref41OutSha256": "618a370f5255c01184d0ed57a31ca56705b4a6d7c8adfdd6907ff7a31c3fd342",
 "candOutSha256": "92352458dc7062439dd2929e6c426a7398660bbf2e7e5ea8fd2f2fab0cbecc0c7",
 "equal": false
}
{
 "probe": "G1",
 "seed": 44001,
 "units": 299,
 "values": 300,
 "ref41Exit": 2,
 "candExit": 2,
 "ref41OutSha256": "0002484a4b4deb14185086d3106119bba5b109621e6d82ac324d20559b36a787",
 "candOutSha256": "55ae4631601fa812cf53cbfe5ac4b83f7a4dcd857ea2101857a740494476d4d4",
 "equal": false
}
{
 "probe": "G1",
 "seed": 44002,
 "units": 299,
 "values": 300,
 "ref41Exit": 2,
 "candExit": 2,
 "ref41OutSha256": "618a370f5255c01184d0ed57a31ca56705b4a6d7c8adfdd6907ff7a31c3fd342",
 "candOutSha256": "399c4ef45cc0f80af71dc24cbfb6e3fe3bf846cf984083c3b6e432b2642e00c7",
 "equal": false
}
```

The first two objects are V1, the next two V5, and the final two V4, in the command order above. Probe return code 1 means the candidate differs; in the V4 case the intentionally clean same-tail pair exposes the port-digit cache collision.

Benchmark control `buildport-m6-default-branch.py` was also probed twice; both returned exit 0 (no witness):

`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G1 --tool-file .ufo/waves/round-44/controls-r43/buildport-m6-default-branch.py --seed 44001`

`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G1 --tool-file .ufo/waves/round-44/controls-r43/buildport-m6-default-branch.py --seed 44002`

```json
{
 "probe": "G1",
 "seed": 44001,
 "units": 299,
 "values": 300,
 "ref41Exit": 2,
 "candExit": 2,
 "ref41OutSha256": "0002484a4b4deb14185086d3106119bba5b109621e6d82ac324d20559b36a787",
 "candOutSha256": "0002484a4b4deb14185086d3106119bba5b109621e6d82ac324d20559b36a787",
 "equal": true
}
{
 "probe": "G1",
 "seed": 44002,
 "units": 299,
 "values": 300,
 "ref41Exit": 2,
 "candExit": 2,
 "ref41OutSha256": "618a370f5255c01184d0ed57a31ca56705b4a6d7c8adfdd6907ff7a31c3fd342",
 "candOutSha256": "618a370f5255c01184d0ed57a31ca56705b4a6d7c8adfdd6907ff7a31c3fd342",
 "equal": true
}
```

## Files, risks, blockers

- Wrote: `.ufo/waves/round-44/classes/g1_longport_grammar.py` and this report.
- Created scratch directory `/fast/scratch/hyaku/kake-r44/ExecG1LongPort`; no persistent scratch artifacts or tool installs.
- Risk/limitation: the benchmark control did not witness on either tested seed; it was optional. Its probe output matched the reference.
- LSP was unavailable in this tool session (no LSP tool exposed); no symbol/refactor query was performed.
- No other checks were run.
