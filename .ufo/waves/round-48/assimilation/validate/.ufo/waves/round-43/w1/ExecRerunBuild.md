REPRODUCED — the C1 build scoring reproduces on three fresh seeds.

Item: re-run the frozen round-43 counter v4 against the round-42 build
`020bc4574729ed674299f6cab02faac1582d9464` with fresh (os.urandom) seeds; compare
`toolSha256` / `counterSha256` against the L1 freeze receipt `build-1.json`.

## Verdict

REPRODUCED. All three reruns exited 0, `met: true`, `equalRuns 11/11`, all five timing
ratios <= 2.0 (max observed 1.302). `toolSha256` and `counterSha256` are byte-identical to
the freeze receipt in all three runs. No conformance defect observed.

## Commands (exit codes)

```
mkdir -p /fast/scratch/hyaku/kake-r43/ExecRerunBuild
for n in 1 2 3; do
  timeout 900 prlimit --as=8000000000 -- python3 -B \
    /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-43/c43_count_v4.py \
    --root /home/vgpnk/Projects/shokunin/kake-shokunin \
    --revision 020bc4574729ed674299f6cab02faac1582d9464 \
    --out /fast/scratch/hyaku/kake-r43/ExecRerunBuild/build-rerun-$n.json
done
```
Exit codes: run1=0, run2=0, run3=0 (`exits.txt`). 3 concurrent processes, each under
`timeout 900` + `prlimit --as=8000000000`; wall ~45 s; all process trees exited on their own
(no strays from this seat).

## Receipts

| run | seed | met | equalRuns | equalValues | T1 | T2 | T3 | T4 | T5 | max |
|---|---|---|---|---|---|---|---|---|---|---|
| build-rerun-1 | 189649668521355 | true | 11/11 | 11889 | 1.025 | 1.179 | 1.302 | 1.227 | 1.086 | 1.302 |
| build-rerun-2 | 32054820857497  | true | 11/11 | 11889 | 1.022 | 1.205 | 1.297 | 1.252 | 1.184 | 1.297 |
| build-rerun-3 | 242882779121200 | true | 11/11 | 11889 | 1.043 | 1.190 | 1.288 | 1.275 | 1.123 | 1.288 |

Exact ratios (`ratiosExact`): run1 T1 1.0245289323078715 / T2 1.1792337928361845 /
T3 1.302087954841748 / T4 1.2266172853427677 / T5 1.0861380939879233; run2 T1 1.022370767309032 /
T2 1.2054573249877414 / T3 1.29715045863465 / T4 1.2523477455634058 / T5 1.1841072153783674;
run3 T1 1.0425284043505303 / T2 1.1898727031527845 / T3 1.288390536925989 /
T4 1.2753782279801755 / T5 1.122610660640702.

All three seeds differ from the freeze seeds (9325990526163 / 265206435053987 /
269853680553917): independent draw, not a replay.

## sha256 vs freeze/build-1.json (identical in all 3 reruns)

| field | value | equal to freeze |
|---|---|---|
| toolSha256 | 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021 | yes |
| counterSha256 | 1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab | yes |
| ref41Sha256 | 50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d | yes |
| base40Sha256 | 4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e | yes |
| revision | 020bc4574729ed674299f6cab02faac1582d9464 | yes |

Independent re-hash of the counter on disk: `sha256sum .ufo/waves/round-43/c43_count_v4.py` ->
`1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab`, matching
`.ufo/waves/round-43/verification/freeze/counter-v4.sha256` and the `counterSha256` in all
three freeze receipts (build-1/2/3). The counter was not modified between freeze and rerun.

## Per checked statement

- "exit code and output equal the round-41 tool's on every generated run" — holds: A,B,C,D,
  E,F,T1,T2,T3,T4,T5 all `equal: true` (11/11) in every receipt; equalValues 11889 identical
  to the freeze receipt.
- "median CPU time on each of the five timing shapes at most 2.0x the round-40 tool's" —
  holds: max ratio over 15 shape/rerun cells is 1.302 (run1 T3), 40% of the limit.
- "met" — holds for all three; `note: null` everywhere (no "tool absent", no cannot-evaluate).
- "target: round-42 build 020bc457... , tool sha256 914ebdee..." — holds: revision resolved to
  the full commit, toolSha256 matches.
- "compare toolSha256/counterSha256 to freeze/build-1.json" — holds (table above).
- Freeze receipts build-1/2/3 internally consistent (met, 11/11, distinct seeds, same shas).
- No pre-freeze seat score found: `.ufo/waves/round-43/w1/` held only `swarm-registry.json`
  and `ScoutReopen.md` before this report; no C1 score artifacts predating the freeze tip.

## Artifacts / scope

`/fast/scratch/hyaku/kake-r43/ExecRerunBuild/build-rerun-{1,2,3}.json|.log` + `exits.txt`
(40 KB total). Only file written in the lane repo: this report. No git/jj mutation, no
network access, no tooling installs needed (python3, sha256sum, coreutils only).

## Risks / blockers

None blocking. The three reruns overlapped another seat's `--tool-file` control runs, so
absolute CPU medians carry mild contention noise; the ratio compares against the base40 tool
measured in the same process, so the comparison stays internally fair and every ratio stayed
far under 2.0.
