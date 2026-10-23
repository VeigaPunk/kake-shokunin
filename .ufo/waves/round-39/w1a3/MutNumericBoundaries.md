# MutNumericBoundaries — r39-controls-a3
Axes: operability; numeric-boundary discrimination; single-point isolation/restoration; key-blindness.
Built 12 complete reference-derived mutants, each changing exactly one line at one behavior-bearing point. No equivalent mutants shipped.
Local detector: exact contract exit code, JSON verdict, check status/error and finding comparison; not the sealed counter.
Observed: 13 pristine witnesses accepted, 13 mutated witnesses rejected, 13 restored witnesses accepted (39 tool runs). All 12 mutants locally killed; sealed-key survival is UNRUN, for L1 only.
## Exact commands and exits
`timeout 10s sha256sum /fast/scratch/hyaku/kake-r39a3w1/shared/reference.py` → exit 0; 663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8.
`timeout --signal=TERM --kill-after=2s 60s prlimit --as=4000000000 -- python3 -I -B /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/probe_numeric.py prepare` → exit 0; 13 bounded witnesses; total seat bytes at preparation 54,509,889.
`timeout --signal=TERM --kill-after=2s 180s prlimit --as=4000000000 -- python3 -I -B /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/probe_numeric.py phase pristine` → exit 0; 13/13 match contract; 13/13 pristine hashes match.
`timeout --signal=TERM --kill-after=2s 180s prlimit --as=4000000000 -- python3 -I -B /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/probe_numeric.py phase mutated` → exit 0; 0/13 match contract; 13/13 match predicted mutant outputs/hashes.
`timeout --signal=TERM --kill-after=2s 180s prlimit --as=4000000000 -- python3 -I -B /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/probe_numeric.py phase restored` → exit 0; 13/13 match contract and restored hashes.
`timeout --signal=TERM --kill-after=2s 30s prlimit --as=4000000000 -- python3 -I -B /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/probe_numeric.py summarize` → exit 0; 12 killed, 12 exact restorations; sealed_counter_run=false.
Each child command is recorded verbatim with its actual exit/stdout/stderr in mutants.json and receipts/*.json: timeout 30s, kill-after 2s, prlimit 4,000,000,000 bytes, Python -I -B; maximum four children. All children joined; no process tree retained.
## Findings (reference → mutant output, with exit)
Every clean result is verdict=clean, status=clean, error=null, findings=[]; every finding result is verdict=failed-policy, status=findings, error=null, with only the named finding. All stderr empty. Full actual JSON outputs and manifest/XML inputs are in mutants.json.
| File:line | Sentence | Witness; actual reference → mutant | SHA-256 |
|---|---|---|---|
| /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/mutants/M01.py:119 | 19 | bytes-exactly-52428800: clean (exit 0) → too_large@None (exit 1) | 7f701182469b7fb2751f193013d75d811a50e6fab3611ceb4eac9ff9dc2ea52c |
| /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/mutants/M02.py:146 | 20 | entries-exactly-50000: clean (exit 0) → too_many_entries@None (exit 1) | d80fa6870df2e36decfdf6e9e489e00e31d3f613924b054f7d419e81e9edda7e |
| /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/mutants/M03.py:167 | 23 | loc-exactly-2048-codepoints: loc_too_long@1 (exit 1) → clean (exit 0) | bba96d107517f9835958d4654de51042c195eefd9e1f72509b6b3e520a80d601 |
| /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/mutants/M04.py:70 | 32 | priority-negative-zero: clean (exit 0) → priority_invalid@1 (exit 1) | 7c1ca756dc73010eb0c509e4c7239ce4fae2387cb467faf0e61dabdf3042a828 |
| /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/mutants/M05.py:70 | 32 | priority-positive-one: clean (exit 0) → priority_invalid@1 (exit 1) | ec4d2819baaab9a36b9c2206ad980d061c9ea611b7e58000503c63794b925132 |
| /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/mutants/M06.py:67 | 32 | priority-just-above-one: priority_invalid@1 (exit 1) → clean (exit 0) | 4deee24e0df7762beda36692aecdd553f0b378dd0d4345fd73cefab1d415df6a |
| /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/mutants/M07.py:54 | 29 | hour-24: lastmod_invalid@1 (exit 1) → clean (exit 0) | 3b1928a2314a71339b52dabb2cd566f14833e408fb764335d67cd304a20790b8 |
| /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/mutants/M08.py:54 | 29 | minute-60: lastmod_invalid@1 (exit 1) → clean (exit 0) | 7dd4f3886843c39d4cb4e7da2dfacf9839fd0d32a224301db443abd16278c230 |
| /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/mutants/M09.py:56 | 29 | second-60: lastmod_invalid@1 (exit 1) → clean (exit 0) | df04012d355d673c20954a62669501ae0ca30f09b84aea50fc52cf7b3016d768 |
| /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/mutants/M10.py:40 | 29 | leap-day-2000: clean (exit 0) → lastmod_invalid@1 (exit 1) | 7870b5b166da695d6ff4634f6fecb8f988c8fc8f21b33a57c205d67e9d5a914b |
| /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/mutants/M11.py:40 | 29 | leap-day-2024: clean (exit 0) → lastmod_invalid@1 (exit 1) | 0b25d6e0d73c734e57cdd0f7965946e1937ac18d7f8a28e44a538d0a240de5c7 |
| /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/mutants/M12.py:51 | 29 | nonleap-century-1900: lastmod_invalid@1 (exit 1) → clean (exit 0); april-31: lastmod_invalid@1 (exit 1) → clean (exit 0) | 414c77629db743a02d4849f87884c616e5a71f9a6310d662b553fead36f0c938 |
## Deliverables and restoration
/fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/mutants.json — sha256 ced049fa5aa5a2ffa9ac66393bf74253aa066d05614b3085aa7226be49940df3; per-mutant absolute file/hash/sentence, minimal witness paths and contents (large XML uses an exact recipe), predicted detector, all three actual outputs and local verdict.
/fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/artifacts.sha256 — sha256 7eb2586db6bfdf0fd8fc907014cc7695767319f1fe22b208382a53543f2e173e; all 47 witness/executable/evidence artifact hashes (including the per-witness manifest and XML files).
/fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/probe_numeric.py — sha256 cd28f695ba1688089d030327ece40083802181f94a721ae35e53e2f472f345b9; bounded detector; replay requires reconstructing pristine probe files from the explicitly authorized shared reference.
/fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/restoration.json — sha256 f1194ce09ea327736f5b7b2ec16c2ac8a388c06e50caaf4f5db08ad445d59547; each pristine/restored hash is 663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8; mutated hashes are listed above.
/fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/cleanup.json — sha256 99dd3a372e0ab7ef5640f85e06639e66b7921ed78e95a3574ec12775d6b52d08; after successful exact-byte restoration, functions.edit REM deleted the local reference.py and all 12 pristine probe copies; mutant executables retained.
No counter/key access, no network, no lane mutations except this report, no tool installation/update, no runtime dispatch. No sealed-key or round verdict asserted.
