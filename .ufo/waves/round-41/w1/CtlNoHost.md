# CtlNoHost — KILLED: host-skipping control scores 1360/1434, not met
Axes: operability (measured); freshness (unchanged by this probe, not independently checked).
One reference-derived mutation removes the host character repertoire, percent-triplet and extra IP-literal validation; all other component checks remain. Existing urlsplit, hostname/nonempty-host, port and TAB/CR/LF behavior is retained. No alternative runtime or dependency was added.

## Artifacts and detector
- Retained control: `/fast/scratch/hyaku/kake-r41w1/CtlNoHost/no_host.py`, SHA256 `c5a11b39cc464100dacda51adeba910df871fcea4973b2307e7bb8fac6e8aa0b`.
- Restored probe: `/fast/scratch/hyaku/kake-r41w1/CtlNoHost/probe.py`, before/after SHA256 `6d7c2dd445fc7d3b2df7c3307d18f05c7f2cf6154830430dbc15dd372509010a` (identical to shared reference).
- Counter SHA256 `2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4`; all runs used seed 41001 and the same bounded detector.
- Expected detector: pristine/restored 1434/1434; mutation below 1434 because invalid hosts retain the base tool's acceptance.

## Exact scoring commands and observed exits
```sh
timeout 900 prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlNoHost/probe.py --label CtlNoHost-pristine --seed 41001 --out /fast/scratch/hyaku/kake-r41w1/CtlNoHost/pristine.json
# exit 0
timeout 900 prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlNoHost/probe.py --label CtlNoHost-mutated --seed 41001 --out /fast/scratch/hyaku/kake-r41w1/CtlNoHost/mutated.json
# exit 1
timeout 900 prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlNoHost/probe.py --label CtlNoHost-restored --seed 41001 --out /fast/scratch/hyaku/kake-r41w1/CtlNoHost/restored.json
# exit 0
timeout 900 prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlNoHost/no_host.py --label CtlNoHost-control --seed 41001 --out /fast/scratch/hyaku/kake-r41w1/CtlNoHost/control.json
# exit 1
```
Actual JSON stdout summaries and complete misses are retained in those receipts. All four report `note: null`, `toolExit: 2` (the audited manifests contain invalid checks; counter exits above are distinct).

| Receipt in `/fast/scratch/hyaku/kake-r41w1/CtlNoHost/` | passed | byField loc / sitemapUrl | byComponent fragment,host,path,port,query,userinfo | met |
|---|---|---|---|---|
| pristine.json | 1434/1434 | 630/630; 804/804 | 239/239;239/239;239/239;239/239;239/239;239/239 | true |
| mutated.json | 1360/1434 | 607/630; 753/804 | 239/239;165/239;239/239;239/239;239/239;239/239 | false |
| restored.json | 1434/1434 | 630/630; 804/804 | 239/239;239/239;239/239;239/239;239/239;239/239 | true |
| control.json | 1360/1434 | 607/630; 753/804 | 239/239;165/239;239/239;239/239;239/239;239/239 | false |

## Findings and checked statements
- **holds:** `no_host.py:77` skips host repertoire/percent validation; `no_host.py:85-88` no longer validates literal contents. The counter catches 74 host-only false acceptances: 23 loc, 51 sitemapUrl; zero false rejections. No other component bucket loses a case.
- **holds:** examples in `control.json:30-48` are host U+0002, DEL and `%4G`; `mutated.json:93-97` shows ordinary `t` splitting an existing percent triplet (`%t78`). These remain accepted by the control but are oracle-invalid.
- **holds:** this control is below 1434 on the exercised seed; the mutant is killed because both pristine and restored bytes meet the predicate. This is not an exhaustive host-grammar or round-admission verdict.
- **holds:** exact restoration used `timeout 30 prlimit --as=4000000000 cp /fast/scratch/hyaku/kake-r41/shared/ref_fix.py /fast/scratch/hyaku/kake-r41w1/CtlNoHost/probe.py` (exit 0), then `timeout 30 prlimit --as=4000000000 chmod a-w /fast/scratch/hyaku/kake-r41w1/CtlNoHost/probe.py` (exit 0).
- **holds:** `timeout 30 prlimit --as=4000000000 cmp -s /fast/scratch/hyaku/kake-r41w1/CtlNoHost/probe.py /fast/scratch/hyaku/kake-r41/shared/ref_fix.py` exited 0; sha256sum before/after matched the reference hash above; restored detector returned 1434/1434.
Initial scratch copy inherited mode 0444; one edit returned EACCES without changing bytes, resolved with sandbox-only `chmod u+w`. Shared source was never changed. The scored mutant is retained separately; probe bytes and read-only mode are restored. All counter processes finished synchronously, with no background jobs/services started. No tools installed or upgraded; no unrelated tests, network requests or lane edits.
