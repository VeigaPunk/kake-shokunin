# MutTool — round 36 wave 2 mutation probe
Axes: operability (rule detection) and freshness (recorded-quote correctness).
Attacked the tool bytes from build `4d5b3d550748e5b52af31646b74c1aa435942bde`: 32 independent single-point mutants across (a)-(g), not cumulative edits.
Result: sealed counter killed 23/32; selftest killed 27/32; M07, M08 and M24 survived both. No inconclusive probes. These are coverage findings, not a round/admission verdict or a claim that pristine has these defects.
Expected detectors: sealed score below 25/28 and selftest below 101/101. “Survived” uses each requested acceptance threshold, not merely whether some case failed.

## Commands and controls
`R=/fast/scratch/hyaku/kake-r36w2/MutTool; C=$R/clone; L=/home/vgpnk/Projects/shokunin/kake-shokunin`; commands below expand these paths. Environment: `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` unset; `TMPDIR=$R/tmp`, `PYTHONDONTWRITEBYTECODE=1`.
Setup: `mkdir -p "$R/tmp" && timeout 300 git clone -q "$L" "$C" && timeout 300 git -C "$C" checkout -q f3a38bf8e68f6cee386125d34b5e95ac9b2df66e` — exit 0.
`timeout --kill-after=5s 290s /usr/bin/python3 -B "$R/probe.py" prepare` — exit 0; extracts with `timeout --kill-after=2s 60s git -C "$C" show 4d5b3d550748e5b52af31646b74c1aa435942bde:scripts/source_recheck.py` (exit 0), and confirms landed bytes equal that extraction.
`timeout --kill-after=5s 290s /usr/bin/python3 -B "$R/probe.py" probe --shard s --shards 4` — s=0,1,2,3, all exit 0; four concurrent bounded shards, no subagents.
Every pristine/mutated/restored phase ran `timeout --kill-after=2s 120s /usr/bin/python3 -B "$C/.ufo/waves/round-36/sealed_count.py" --root "$C" --tool-file "$R/shard-s/source_recheck.py" --key-file "$C/.ufo/waves/round-36/sealed/cases.json"`.
Every phase also ran `timeout --kill-after=2s 120s /usr/bin/python3 -B "$C/scripts/source_recheck_selftest.py" --tool "$R/shard-s/source_recheck.py"`; exits are below, and full expanded argv/stdout/stderr are retained per phase.
Four initial pristine plus 32 restored detector pairs all returned sealed 28/28 (exit 0), selftest 101/101 (exit 0). Each restored pair is the next mutation's pristine control on the same pathname. Restoration runs even on detector failure via `finally`.
Before/restored SHA-256 for every active tool: `577b2d7d028964e06152f5a7b792141e586045eaa8ec9262ee7f416ba5510d48`; all 32 exact-byte comparisons true. Changed hashes are recorded individually in `manifest.json` and each `result.json`.
`timeout --kill-after=2s 30s /usr/bin/python3 -B "$R/summarize.py"` — exit 0, 32 results, 36 passing control pairs, zero missing; longest mutated detector 5.764 s.

## Mutant table
| Mutant (bullet) / skipped rule | Sealed /28 (exit; verdict) | Selftest /101 (exit; verdict) |
|---|---|---|
| M01 (a) 410 is not gone | 22 (1; killed) | 100 (1; killed) |
| M02 (a) first hop decides final status | 24 (1; killed) | 90 (1; killed) |
| M03 (a) all 2xx enter quote processing | 24 (1; killed) | 100 (1; killed) |
| M04 (a) 404 is not gone | 18 (1; killed) | 99 (1; killed) |
| M05 (b) 302 permanent instead of 301 | 24 (1; killed) | 94 (1; killed) |
| M06 (b) only first leading permanent hop | 24 (1; killed) | 100 (1; killed) |
| M07 (b) each redirect resolved from original URL | 26 (0; survived) | 101 (0; survived) |
| M08 (b) relative redirects retain dot segments | 26 (0; survived) | 101 (0; survived) |
| M09 (c) retain HTML comments | 24 (1; killed) | 101 (0; survived) |
| M10 (c) retain all raw-element contents | 20 (1; killed) | 96 (1; killed) |
| M11 (c) retain ordinary HTML tags | 16 (1; killed) | 101 (0; survived) |
| M12 (c) do not decode HTML references | 19 (1; killed) | 99 (1; killed) |
| M13 (c) raw start tags case-sensitive | 28 (0; survived) | 100 (1; killed) |
| M14 (c) retain style contents | 24 (1; killed) | 100 (1; killed) |
| M15 (d) NFC instead of NFKC | 24 (1; killed) | 99 (1; killed) |
| M16 (d) do not delete whitespace | 23 (1; killed) | 99 (1; killed) |
| M17 (d) case-insensitive quote match | 24 (1; killed) | 100 (1; killed) |
| M18 (d) whole-text equality instead of substring | 2 (1; killed) | 98 (1; killed) |
| M19 (e) media type case-sensitive | 17 (1; killed) | 100 (1; killed) |
| M20 (e) parameter names case-sensitive | 28 (0; survived) | 100 (1; killed) |
| M21 (e) apply HTML processing to text/plain | 24 (1; killed) | 98 (1; killed) |
| M22 (e) xhtml not a supported HTML type | 22 (1; killed) | 100 (1; killed) |
| M23 (f) ignore all BOM encoding overrides | 24 (1; killed) | 98 (1; killed) |
| M24 (f) decode BOM but do not drop its mark | 28 (0; survived) | 101 (0; survived) |
| M25 (f) do not remove charset double quotes | 17 (1; killed) | 100 (1; killed) |
| M26 (f) ascii label means ASCII not windows-1252 | 28 (0; survived) | 100 (1; killed) |
| M27 (f) default encoding windows-1252 not UTF-8 | 22 (1; killed) | 97 (1; killed) |
| M28 (f) discard invalid bytes instead of replacement | 28 (0; survived) | 100 (1; killed) |
| M29 (g) stop after first check_invalid | 24 (1; killed) | 99 (1; killed) |
| M30 (g) do not reject relative path escape | 24 (1; killed) | 100 (1; killed) |
| M31 (g) accept empty check id | 28 (0; survived) | 100 (1; killed) |
| M32 (g) do not validate manifest version | 28 (0; survived) | 100 (1; killed) |

## Findings and evidence
Sealed survivors: M07, M08, M13, M20, M24, M26, M28, M31, M32. Selftest survivors: M07, M08, M09, M11, M24. Their skipped rules are named above; M07/M08 are detected by two sealed cases each but still meet 25/28.
M24 is not an equivalent mutant: UTF-8 BOM body `EF BB BF` + `BOM-witness`, with quote U+FEFF + `BOM-witness`, gives pristine `quote_missing`/failed-policy (exit 1), mutant clean (exit 0), restored `quote_missing` (exit 1).
Witness command: `timeout --kill-after=2s 90s /usr/bin/python3 -B "$R/bom-witness/witness.py"` — exit 0; its three identical detector commands each have a 20 s timeout. Evidence: `/fast/scratch/hyaku/kake-r36w2/MutTool/bom-witness/result.json:18-68`; mutant hash `eaac16cc0962169df4b24fbf634784d551873e09bbada475c45f79f0e498eef2`, before/after hash as above.
All artifacts: `/fast/scratch/hyaku/kake-r36w2/MutTool/`. `manifest.json:1-11` pins build/tool/counter/selftest/key; subsequent entries record each exact replacement, original source line, and mutant hash. Immutable variants are `mutants/M01.py` through `mutants/M32.py`.
Detailed receipts: `/fast/scratch/hyaku/kake-r36w2/MutTool/shard-s/Mxx/result.json` and sibling `mutated/`/`restored/` directories. For mutant number n, s=(n-1) mod 4. Example `/fast/scratch/hyaku/kake-r36w2/MutTool/shard-0/M13/result.json:198-204` records exact restoration and separate detector verdicts.
Aggregate evidence: `/fast/scratch/hyaku/kake-r36w2/MutTool/summary.json:7018-7045` lists survivors, four final active-file hashes and all-restorations/all-controls true; SHA-256 `1cfa9ce1eab7fde16f331d804dd0080d1d1e670d2b61b6728be822f5bb5a0af9`.
Counter SHA-256 `88ec59140258ce759107b7472fdd07a005b7c1bb8b3ba5218347e4518342ff8e`; revealed key `44c94838f31af6740a3f1bb4123abe6cbb8df0bbdd3414de7acbb3838863ef1d`; selftest `0ad5623b9bbfafccd0f9f558c927d90651fabb5da4fd003e9fa2e73c96d5e419`.
Harness `/fast/scratch/hyaku/kake-r36w2/MutTool/probe.py` SHA-256 `79ab4c2de47de333971b3273fc3349a6e9a57ad62bf1d14ae4e5a92578d73f87`. Its regex-spec string literals emit Python SyntaxWarnings about `\s`; all 32 variants parse and all requested detectors completed.
Tool versions observed: Python 3.14.8, bubblewrap 0.13.1; no installs/upgrades. All finite jobs completed; no services started. No network requests, lane source/index/jj changes, integration or shipped fix. Live freshness and other mutations were not verified.
