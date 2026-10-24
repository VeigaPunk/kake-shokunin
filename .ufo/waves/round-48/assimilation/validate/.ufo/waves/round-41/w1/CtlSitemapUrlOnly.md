# CtlSitemapUrlOnly — killed field-skip control
Axes: operability (measured); freshness (no source changes or network requests).
Scope: one control variant, Python standard library only; no integration or round verdict.
Sandbox S: `/fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/`.

Mutant: reference repair applied to manifest `sitemapUrl` only; `loc` retains the base parser judgment.
`S/control.py:110-116` gates the RFC check and restores the base whitespace guard when disabled; `S/control.py:331` disables it for every loc. The manifest call remains enabled at `S/control.py:405`.
Reference: `/fast/scratch/hyaku/kake-r41/shared/ref_fix.py`; base behavior: `/fast/scratch/hyaku/kake-r41/shared/base.py:67-86`.
Expected detector: pristine/restored meet 1434/1434; removing the loc repair must score below 1434.

Tool SHA256 identities:
- Pristine and restored `S/probe.py`: `6d7c2dd445fc7d3b2df7c3307d18f05c7f2cf6154830430dbc15dd372509010a` (identical to read-only reference).
- Mutated `S/probe.py`, retained as `S/control.py`: `e9333ba02e4758e92c07c9bf99cbef45793d86321f37020facd597f902d8f0dc`.
- Counter: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py`, `2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4`.

Actual receipts (component order: fragment, host, path, port, query, userinfo; each denominator 239):
| Receipt in S | Seed | Passed | byField loc; sitemapUrl | byComponent numerators | met | Counter exit |
|---|---:|---:|---|---|---|---:|
| pristine.json | 41001 | 1434/1434 | 630/630; 804/804 | 239,239,239,239,239,239 | true | 0 |
| mutated.json | 41001 | 1313/1434 | 509/630; 804/804 | 214,216,216,239,209,219 | false | 1 |
| control.json | 24255836550377 | 1316/1434 | 512/630; 804/804 | 217,214,216,238,216,215 | false | 1 |
| restored.json | 41001 | 1434/1434 | 630/630; 804/804 | 239,239,239,239,239,239 | true | 0 |
All receipts: note=null, toolExit=2 (the generated manifest contains invalid checks; this is not a detector failure).

Per-tool findings:
- `S/control.py` (and identical mutated probe) skips all loc RFC validation; caught by 121 loc cases at seed 41001 and 118 at the fresh seed. No sitemapUrl misses. Examples include malformed percent triplets, interior spaces/DEL, forbidden printable characters and misplaced delimiters.
- `S/probe.py` pristine/restored skips nothing; no cases caught either state.
- Fixed-seed misses by component: fragment 25, host 23, path 23, port 0, query 30, userinfo 20. Fresh-seed: 22,25,23,1,23,24 respectively.
- `S/mutated.json` records examples `http://zwld_%4GvbsS.org/ykug6y` and `Https://cz8T.example/j3%EFZ/5nZxNn#rynL%c`, oracleValid=false, both loc false accepts.
- With loc behavior fixed to the base and sitemapUrl already 804/804, no additional score gain is possible on these generated cases without violating the assigned skip.

Exact scoring commands and exits (all bounded and synchronous):
`timeout 900 prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/probe.py --label CtlSitemapUrlOnly-pristine --seed 41001 --out /fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/pristine.json` → 0.
`timeout 900 prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/probe.py --label CtlSitemapUrlOnly-mutated --seed 41001 --out /fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/mutated.json` → 1.
`timeout 30 prlimit --as=4000000000 cp /fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/probe.py /fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/control.py` → 0.
`timeout 900 prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/control.py --label CtlSitemapUrlOnly-control --out /fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/control.json` → 1.
`timeout 30 prlimit --as=4000000000 cp /fast/scratch/hyaku/kake-r41/shared/ref_fix.py /fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/probe.py` → 0.
`timeout 30 prlimit --as=4000000000 chmod a-w /fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/probe.py` → 0.
`timeout 30 prlimit --as=4000000000 sha256sum /fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/probe.py /fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/control.py` → 0; hashes above.
`timeout 900 prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/probe.py --label CtlSitemapUrlOnly-restored --seed 41001 --out /fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/restored.json` → 0.
`timeout 30 prlimit --as=4000000000 cmp -s /fast/scratch/hyaku/kake-r41/shared/ref_fix.py /fast/scratch/hyaku/kake-r41w1/CtlSitemapUrlOnly/probe.py` → 0.

Restoration evidence: before hash 6d7c2dd4…010a → mutated e9333ba0…f0dc → restored 6d7c2dd4…010a; cmp exit 0 proves exact bytes. Original read-only mode restored. Initial edit hit EACCES on copied mode 444; only the sandbox copy was made writable before retrying.
Checked statements: field-skip control stays below target — holds on both scored seeds; sitemapUrl repair alone covers all 804 cases — holds; detector kills the omitted loc repair — holds; pristine/restored score equivalence and exact restoration — holds.
Verdict: KILLED, not inconclusive. Retained control is available for L1 re-scoring; no baseline failure, surviving control or round judgment claimed.
No installs/updates, no live background jobs, no external requests; all writes confined to sandbox and this report.
