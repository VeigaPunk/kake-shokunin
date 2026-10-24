NOT MET

Axes: operability (judgment separation and measured CPU); freshness unchanged and not evaluated.
Sandbox S = `/fast/scratch/hyaku/kake-r42w1/CtlHeadTail`; lane R = `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Built nine Python-standard-library controls from shared `tip41.py`: original full judgment below 2,000 code points; above it, an ASCII per-character translation table checks only the named window(s), with sampled percent-triplet checks, followed by the unchanged `urlsplit` checks. Head+tail means N code points at each end.
Behavior-bearing locations: each `S/<name>.py:89-90` selects the windows; `:100-101` retains the short-value regex; `:105-110` skips unsampled characters; `:132` replaces the regex guard.
Counter C = `R/.ufo/waves/round-42/c42_count.py`, sha256 `7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6`.

Executed batch: `timeout 900 prlimit --as=8000000000 -- python3 -B /fast/scratch/hyaku/kake-r42w1/CtlHeadTail/run_counters.py` — exit 0; nine counter children each exited 1; two counters concurrently; completed in 557.45 s.
Exact child argv and outputs are retained in `S/runs.json`. Each command was `timeout 900 prlimit --as=8000000000 -- python3 -B C --root R --tool-file S/<name>.py --label CtlHeadTail-<name> --seed <seed> --out S/<name>.json`, with C/R/S expanded to the absolute paths above and TMPDIR=`S/tmp`.
An initial async launch was rejected by the host's 100-background-job cap; no counter started from that attempt. The synchronous batch above completed normally.
Ratios below are ordered T1, T2, T3, T4, T5. Every listed `.py` tool and `.json` receipt is under S; full source hashes follow.

| Tool | SHA256 | Seed | Receipt | equalRuns | Ratios | met / exit | Work skipped; unequal runs |
|---|---|---:|---|---|---|---|---|
| tail64.py | 7a74b1f7a6901709633cb9ae9b7bd2a53ee463f2392df8b1c83d2d22082faa9a | 42640 | tail64.json | 5/8 | 0.901,1.064,1.387,1.268,1.075 | false / 1 | All but last 64; C,T1,T5 caught it |
| tail128.py | a332ae0f414628c5ac71a241217586422e73446d9bbed4d182eecaaf08b46a5c | 42641 | tail128.json | 7/8 | 0.887,1.155,1.357,1.216,1.125 | false / 1 | All but last 128; C caught it |
| tail512.py | 00369d25299cb2202dbc9837e2773641e9c3ceff32590d73e97babac643f4ec9 | 42642 | tail512.json | 7/8 | 0.979,1.288,1.340,1.210,1.032 | false / 1 | All but last 512; C caught it |
| head64.py | 68f43a1f4ce1fa45917231d36a89438fd8e6d32afe81fc45f59e1ee8477ba146 | 42643 | head64.json | 5/8 | 1.057,1.048,1.351,1.250,1.182 | false / 1 | All but first 64; C,T1,T5 caught it |
| head128.py | fe640c9e5ec03fcf11a96d453b4e14157242b5efb2904e2634eb359c18054f51 | 42644 | head128.json | 5/8 | 1.106,1.115,1.372,1.248,1.239 | false / 1 | All but first 128; C,T1,T5 caught it |
| head512.py | 1e50b5c806ac245dc4a8a7f3f1a2b70eac4d3250323c4518e75ebf6390e38879 | 42645 | head512.json | 5/8 | 1.249,1.220,1.364,1.276,1.207 | false / 1 | All but first 512; C,T1,T5 caught it |
| headtail64.py | 1e290ec3be3fc176f42ca1fc853bcb7abf8a497990e68a327a90161c7b50705c | 42646 | headtail64.json | 5/8 | 0.934,1.108,1.388,1.246,1.032 | false / 1 | Middle outside first/last 64; C,T1,T5 caught it |
| headtail128.py | 6d9fc03d85c951f8986861e39ad8b731b5fa50598aaf034eb37684acbafe7c63 | 42647 | headtail128.json | 7/8 | 1.000,1.221,1.454,1.230,1.070 | false / 1 | Middle outside first/last 128; C caught it |
| headtail512.py | 32c2f4e59851817172fdbef7555a2b77fa2d9ebc24085ba727e8c3acc229e838 | 42648 | headtail512.json | 7/8 | 1.138,1.486,1.363,1.265,1.023 | false / 1 | Middle outside first/last 512; C caught it |

All timing repetitions were equal 5/5 except T1/T5 of the five 5/8 tools, which were equal 0/5; A,B,T2,T3,T4 matched for every tool. No cannot-evaluate receipts.
Finding — holds: the counter rejects all nine assigned skips, on behavior rather than cost: every ratio is below 2.0. C is the sole separating run for tail128, tail512, headtail128 and headtail512 (`C:275-289` generates defects anywhere in long values).
Finding — wrong for every control: “keeps every round-41 judgment.” Shared witness: `'https://a.example/' + 'a'*1000 + '|' + 'a'*1100` (2,119 code points; sha256 `65a7d74159bf79420a58b32b025f025434fd2a0757e26d99d3a749777b20945e`): tip41 rejects; all nine controls accept. No tool met; no meeting-tool witness is applicable.
Finding — overstated if generalized: rejection of these nine controls does not establish detection of every possible partial-value control or decide the round claim.

Mutation detector and restoration — holds:
Executed `timeout 120 prlimit --as=8000000000 -- python3 -B /fast/scratch/hyaku/kake-r42w1/CtlHeadTail/run_probe.py` — exit 0.
Its identical bounded behavioral detector command for pristine, each mutation and each restoration was `timeout 30 prlimit --as=8000000000 -- python3 -B /fast/scratch/hyaku/kake-r42w1/CtlHeadTail/detector.py /fast/scratch/hyaku/kake-r42w1/CtlHeadTail/probe.py`.
Actual output: pristine 5/5, exit 0; each of nine mutants 3/5, exit 1 (middle-bar and middle-percent accepted incorrectly); each of nine restorations 5/5, exit 0. Mutation verdict: killed for every variant by this local behavioral detector, with no failing baseline. This local detector is separate from the full counter predicate.
Before and all nine after hashes: `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`; mutant hashes are the tool hashes in the table. `S/probe-results.json` records each command, actual output, verdict, and final `exactBytes: true`.
The probe target was restored in `finally`; the nine explicitly requested control artifacts remain for reproduction. Batch children were waited and their process groups killed in `finally`; no seat-started background services remain. Shared/lane source bytes were never changed.
Tools installed or updated: none. No network requests, build, lint, or unrelated checks were run.
