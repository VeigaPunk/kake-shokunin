# G8 host-table witness

Axes: **operability** improved by a class that exercises all three static host tables; **freshness** unchanged and out of scope.

## Change

Wrote `.ufo/waves/round-44/classes/g8_host_tables.py`. `cases(rng, h)` returns 126 `value`/`loc` units: one malformed URL for each host in each source table (46 from A, 46 from B, 34 from F). Every path contains exactly one selected defect from `%`, `|`, space, `<`, `>`; the host remains unchanged for the layout-derived `sitemapUrl`. Hosts are copied data; the module imports no controls and performs no I/O. The A and B host tuples read from their controls are identical; F is a subset.
Scope is limited to this fixed copied host population: A/B each contain the same 46 hosts, and F contains 34 hosts (a subset). This is targeted regression coverage for these known controls, not general host-table-family closure or fresh-host coverage; seeds rotate the path defect selection, not the host population.

## Probe evidence

Working directory for each command: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Each probe emitted the JSON below (trimmed to decisive fields) and exited **1**, the expected witness result.

Command:
```text
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G8 --tool-file .ufo/waves/round-44/controls-r43/hosttable-A-expanded46-fixed.py --seed 44
```
Output:
```json
{"probe":"G8","seed":44,"units":126,"values":126,"ref41Exit":1,"candExit":0,"ref41OutSha256":"02b8d787a72094f240bf90c2b1b93c1f2d7fba696034f61a2e1e56c0dc2f1fbc","candOutSha256":"6e7b401567b4c26099a24e2a4a3099f91aee2914b43147b5a8a455d30ada1049","equal":false}
```

Command:
```text
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G8 --tool-file .ufo/waves/round-44/controls-r43/hosttable-A-expanded46-fixed.py --seed 45
```
Output:
```json
{"probe":"G8","seed":45,"units":126,"values":126,"ref41Exit":1,"candExit":0,"ref41OutSha256":"f1fa063ee9e46bcb32ea4c18ebae6ade08e8ab29a200ac3a98a2cf685ff3eb58","candOutSha256":"c68840f0cb03e47520393e4abb36f2a59903a5ec46b088eb84e5436a2731f728","equal":false}
```

Command:
```text
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G8 --tool-file .ufo/waves/round-44/controls-r43/hosttable-B-expanded46-nogrammar.py --seed 44
```
Output:
```json
{"probe":"G8","seed":44,"units":126,"values":126,"ref41Exit":1,"candExit":0,"ref41OutSha256":"02b8d787a72094f240bf90c2b1b93c1f2d7fba696034f61a2e1e56c0dc2f1fbc","candOutSha256":"6e7b401567b4c26099a24e2a4a3099f91aee2914b43147b5a8a455d30ada1049","equal":false}
```

Command:
```text
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G8 --tool-file .ufo/waves/round-44/controls-r43/hosttable-B-expanded46-nogrammar.py --seed 45
```
Output:
```json
{"probe":"G8","seed":45,"units":126,"values":126,"ref41Exit":1,"candExit":0,"ref41OutSha256":"f1fa063ee9e46bcb32ea4c18ebae6ade08e8ab29a200ac3a98a2cf685ff3eb58","candOutSha256":"c68840f0cb03e47520393e4abb36f2a59903a5ec46b088eb84e5436a2731f728","equal":false}
```

Command:
```text
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G8 --tool-file .ufo/waves/round-44/controls-r43/hosttable-F-provable.py --seed 44
```
Output:
```json
{"probe":"G8","seed":44,"units":126,"values":126,"ref41Exit":1,"candExit":1,"ref41OutSha256":"02b8d787a72094f240bf90c2b1b93c1f2d7fba696034f61a2e1e56c0dc2f1fbc","candOutSha256":"2ba1bacf19f0f1e9d863eed0a3f6971d63c419a7e90e900e33b9b1950ba960bb","equal":false}
```

Command:
```text
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G8 --tool-file .ufo/waves/round-44/controls-r43/hosttable-F-provable.py --seed 45
```
Output:
```json
{"probe":"G8","seed":45,"units":126,"values":126,"ref41Exit":1,"candExit":1,"ref41OutSha256":"f1fa063ee9e46bcb32ea4c18ebae6ade08e8ab29a200ac3a98a2cf685ff3eb58","candOutSha256":"731acd6c4fa4d126c749227faa0ecb158476537898cdc16638c4d4d74ebf2bbf","equal":false}
```

For F, the exit codes match because its table is narrower than A/B; output bytes still differ (`equal:false`) as F answers cleanly for its table hosts while the round-41 reference flags the malformed `loc` values. All six runs establish a semantic witness on both seeds.

## Files and blockers

- Wrote: `.ufo/waves/round-44/classes/g8_host_tables.py`
- Wrote: `.ufo/waves/round-44/w1/ExecG8Hosts.md`
- Created empty scratch directory: `/fast/scratch/hyaku/kake-r44/ExecG8Hosts`
- No tool installs. No LSP interface was exposed in the available tool inventory. No blocker.
- Full counter/build/lint/test suites were not run; the six explicitly requested probe commands were run.
