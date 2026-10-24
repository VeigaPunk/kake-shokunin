KILLED: the loc-only control scores 1170/1434, not met (seed 41001); no target-reaching control.
Axes: operability (counter discrimination); freshness (unchanged).
Mutant: gate the reference URI validator by field, retaining the base guard and urlsplit judgment for sitemapUrl only; Python 3 standard library only.
Expected detector: identical c1_count.py bytes and seed must pass pristine/restored reference bytes and reject this partial repair.

Paths and SHA-256:
- S = /fast/scratch/hyaku/kake-r41w1/CtlLocOnly
- Control S/loc_only.py: 7be091ff9f177b470ce26079eb136f603b64b3492d4eb52497c956b3cdea620f
- Pristine/restored S/probe.py: 6d7c2dd445fc7d3b2df7c3307d18f05c7f2cf6154830430dbc15dd372509010a
- Counter /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py: 2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4

Exact detector commands and counter exit codes:
```sh
# exit 0
timeout 900 prlimit --as=4000000000 -- python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlLocOnly/probe.py --label CtlLocOnly-pristine --seed 41001 --out /fast/scratch/hyaku/kake-r41w1/CtlLocOnly/pristine.json
# exit 1
timeout 900 prlimit --as=4000000000 -- python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlLocOnly/loc_only.py --label CtlLocOnly-mutant --seed 41001 --out /fast/scratch/hyaku/kake-r41w1/CtlLocOnly/mutant.json
# exit 0
timeout 900 prlimit --as=4000000000 -- python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlLocOnly/probe.py --label CtlLocOnly-restored --seed 41001 --out /fast/scratch/hyaku/kake-r41w1/CtlLocOnly/restored.json
# exit 0
timeout 20 prlimit --as=4000000000 -- sha256sum /fast/scratch/hyaku/kake-r41w1/CtlLocOnly/probe.py /fast/scratch/hyaku/kake-r41w1/CtlLocOnly/loc_only.py /fast/scratch/hyaku/kake-r41/shared/ref_fix.py /fast/scratch/hyaku/kake-r41/shared/base.py
```

Actual receipts (paths relative to S; component order: fragment, host, path, port, query, userinfo):
| Receipt | Passed | byField (loc; sitemapUrl) | byComponent | met |
|---|---|---|---|---|
| pristine.json | 1434/1434 | 630/630; 804/804 | 239/239, 239/239, 239/239, 239/239, 239/239, 239/239 | true |
| mutant.json | 1170/1434 | 630/630; 540/804 | 182/239, 188/239, 189/239, 239/239, 183/239, 189/239 | false |
| restored.json | 1434/1434 | 630/630; 804/804 | 239/239, 239/239, 239/239, 239/239, 239/239, 239/239 | true |
All receipts: toolExit=2 (the audited tool's own exit, distinct from counter exits above), note=null.

Findings and checked statements:
- holds: S/loc_only.py:110-116,405 skips RFC URI validation for sitemapUrl while retaining its base judgment; loc keeps the complete reference repair (630/630).
- wrong for this mutant: full URL agreement. The detector catches 264 sitemapUrl cases: fragment 57, host 51, path 50, query 56, userinfo 50; port 0. Examples in mutant.json: host U+0002, path '[', userinfo '|', query space and malformed percent sequences. The receipt retains only the first 200 misses.
- holds: S/probe.py (pristine and restored reference, not controls) skips neither field; no cases caught either reference run.
- holds: counter separates this specific loc-only control on seed 41001; no round-level verdict or claim about untested seeds.
- [INFERENCE] With sitemapUrl judgment required to remain base, its 540/804 score is fixed on these cases; loc already reaches 630/630, exhausting the compliant control's headroom.
Restoration evidence: saved pristine bytes were restored to S/probe.py; actual sha256sum equals the pristine receipt hash and read-only shared/ref_fix.py hash (6d7c2dd4…9010a). The retained mutant hash is 7be091ff…620f; shared/base.py hashes to 4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e.
No installs/updates; no network requests; all bounded detector/hash processes exited. Only this sandbox and report were written.
