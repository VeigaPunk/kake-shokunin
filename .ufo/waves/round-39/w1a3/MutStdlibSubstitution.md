# MutStdlibSubstitution — nine lexical-convenience mutants
Axes: operability, contract-sentence isolation, lexical-edge coverage (lane freshness context).
Built nine full-reference copies, each changing one behavioral point. No sealed counter, key, network, build, or other runtime invoked.
All final witnesses distinguish reference/mutant; all pristine and restored detectors pass. Local verdict: 9 killed, 0 survived, 0 inconclusive. These are witness results, NOT sealed-key scores.
Reference SHA256 before and after every probe: 663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8.
Detector compares expected exit, complete parsed JSON, and empty stderr, using identical bounded commands on pristine, mutated, restored bytes; two tool processes maximum.

## Findings (reference / mutant / restored exit codes)
M01, sentence 21, str.strip: U+2007 FIGURE SPACE around priority → priority_invalid / clean / priority_invalid (1/0/1).
M02, sentence 24, raw urlsplit().port: implicit HTTPS port versus explicit :443 → clean / loc_out_of_scope / clean (0/1/0).
M03, sentence 28, datetime.fromisoformat: U+2028 instead of T → lastmod_invalid / clean / lastmod_invalid (1/0/1); explicit timezone/date-only guard retained.
M04, sentence 32, float value conversion with lexical gate retained: 1.0000000000000001 → priority_invalid / clean / priority_invalid (1/0/1).
M05, sentence 32, float lexical/range validator: 1e-1 → priority_invalid / clean / priority_invalid (1/0/1).
M06, sentence 31, str.lower: Daily → changefreq_invalid / clean / changefreq_invalid (1/0/1).
M07, sentence 26, loc-only normpath: /d/../x under /d/s.xml → clean / loc_out_of_scope / clean (0/1/0).
M08, sentence 26, both-path normpath: /x under /d/../s.xml → loc_out_of_scope / clean / loc_out_of_scope (1/0/1).
M09, sentence 24, truthy urlsplit().port fallback: explicit :0 versus missing HTTP port → loc_out_of_scope / clean / loc_out_of_scope (1/0/1).
Initial M03 fractional-minute witness survived: both implementations rejected it on Python 3.14.8. Preserved actual outputs and original input in probe_receipts.initial.json; unchanged mutant then killed by U+2028 witness. No reference-equivalent mutant shipped.

## Exact commands and exits
`timeout 10s mkdir -p /fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/mutants && timeout 10s cp /fast/scratch/hyaku/kake-r39a3w1/shared/reference.py /fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/reference.py && timeout 10s sha256sum /fast/scratch/hyaku/kake-r39a3w1/shared/reference.py /fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/reference.py` → 0; matching hashes above.
`timeout 120s prlimit --as=4000000000 python3 -I -B /fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/run_probes.py` → 1; 8 killed, M03 survived; all restorations exact.
`timeout 5s prlimit --as=4000000000 python3 -I -B -c 'import datetime,sys; print(sys.version); print(datetime.datetime.fromisoformat("2000-01-01T00:00.1Z")); print(datetime.datetime.fromisoformat("2000-01-01 00:00Z")); print(datetime.datetime.fromisoformat("2000-01-01\u202800:00Z"))'` → 1; ValueError at fractional-minute parse; later expressions not reached.
`timeout 5s prlimit --as=4000000000 python3 -I -B -c 'import datetime; print(datetime.datetime.fromisoformat("2000-01-01 00:00Z")); print(datetime.datetime.fromisoformat("2000-01-01\u202800:00Z"))'` → 0; both printed 2000-01-01 00:00:00+00:00.
`timeout 120s prlimit --as=4000000000 python3 -I -B /fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/run_probes.py M03` → 0; revised M03 witness killed; exact restoration.
Each recorded child command: timeout 5s prlimit --as=4000000000 python3 -I -B <isolated-probe.py> --manifest <witness-manifest>; full argv, exits, stdout/stderr and before/mutated/after hashes are in mutants.json.

## Deliverables (absolute path:changed line; SHA256)
/fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/mutants/M01.py:159 — 91974fd11b42bf233bac1aebec517ac1154f871324214935974ccd951b00518f
/fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/mutants/M02.py:36 — 291602005eb5f97d89a062a7cf56edd3595bca546af5429ac56b38dc5ce2348c
/fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/mutants/M03.py:43 — 92d9c18c5b525b2945559bdcf057d87067892ca9cf36f0aa014755a1239df59c
/fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/mutants/M04.py:67 — 4deee24e0df7762beda36692aecdd553f0b378dd0d4345fd73cefab1d415df6a
/fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/mutants/M05.py:63 — a9a2289a92d144980c3d5d001617765daf0ca85521d4a5331104ce67958ceec6
/fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/mutants/M06.py:178 — 20101975a866f8c02c202c5a7b2960741abb7ea6c9c197bf8c6b54c1d6f137b0
/fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/mutants/M07.py:175 — 95c1f5e7a69f257b175ed72fec0fe14df3c84546911c878cb69a4f6852291108
/fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/mutants/M08.py:36 — fcec2fe94b65425ae3fa6c45819f17fd99ec765ceed83dec86228520fce742c6
/fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/mutants/M09.py:36 — 2e78066920f6bb2889cb65bb6e01ab6d2b6402584878f68df80d0035e0907785
/fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/mutants.json — a74148e77cd7b0a25df30e4d7d973ea4af3d299c54d7c926b2cef330acb00471
/fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/probe_receipts.json — 2ba3e9723e06d4641c695589dc14d6eacee089a1cf37dda1f9317fa133c61501
/fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/run_probes.py — b30a7285bfe215c989ff96f276db243c705d0023a6cdffa5b2e6a542f06433c7
mutants.json embeds each minimal manifest+sitemap, source replacement, expected detector, and both actual outputs; witness files live under its absolute witnesses/M01–M09 paths.
Restoration: all 10 probe triplets restored the exact reference hash before temporary probe copies were unlinked. The sandbox/reference.py copy was deleted via edit REM (tool confirmed deletion); only mutants retain full source. No processes remain from synchronous bounded runs. Tool installs/updates: none.
