NOT MET

Axes: operability (assigned target); freshness (named lane axis, not scored by this probe).
Paths below: `S=/fast/scratch/hyaku/kake-r42w1/CtlLengthGate`; `R=/home/vgpnk/Projects/shokunin/kake-shokunin`; `C=$R/.ufo/waves/round-42/c42_count.py`.
Built the six requested controls from tip41; each changes only `_parse_url` line 92. Python 3 standard library only.
Counter SHA256: `7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6`. All seeds: 42043.

| Tool path (mutation point) | Work skipped | SHA256 | Receipt | equalRuns | ratios T1,T2,T3,T4,T5 | met / exit | Runs catching wrong judgments |
|---|---|---|---|---|---|---|---|
| `S/skip_256.py:92` | No `_URI_RE` above 256 code points; urlsplit only | `4042be73c11037c7e811a75d90585d706e1bd6f4c7f0bff743e61c266d16a9eb` | `S/skip_256.json` | 5/8 | 1.078, 1.02, 1.368, 1.218, 1.188 | false / 1 | C, T1, T5 |
| `S/skip_1024.py:92` | No `_URI_RE` above 1024 code points; urlsplit only | `d4dd1d58b845c442374c7fb0c798acb7cad4365d9c500356f38da31272b19a49` | `S/skip_1024.json` | 5/8 | 1.039, 0.982, 1.396, 1.23, 1.258 | false / 1 | C, T1, T5 |
| `S/skip_2048.py:92` | No `_URI_RE` above 2048 code points; urlsplit only | `9e3657b0c391cf8e1956b4d85939c03982a8e0c9d988b6d93be8c10f0cf9ab9e` | `S/skip_2048.json` | 6/8 | 5.513, 2.768, 1.317, 1.252, 1.25 | false / 1 | C, T5 |
| `S/skip_10000.py:92` | No `_URI_RE` above 10000 code points; urlsplit only | `2ae7fdc03fe4049ce79990a3b8e640ca137780dc3998db57b5797dadcd97777a` | `S/skip_10000.json` | 6/8 | 5.65, 2.798, 1.307, 1.247, 1.199 | false / 1 | C, T5 |
| `S/skip_100000.py:92` | No `_URI_RE` above 100000 code points; urlsplit only | `da2feb2494278658153759da6e9bb8920ea69090922813bf34b97bf177bcd52a` | `S/skip_100000.json` | 6/8 | 5.381, 2.707, 1.422, 1.161, 1.201 | false / 1 | C, T5 |
| `S/prefix_1024.py:92` | `_URI_RE` sees first 1024 code points only | `952937de12d146a4046be5210dde7d55583cb213a7ffd886c23511f2e102b6f6` | `S/prefix_1024.json` | 4/8 | 2.032, 1.989, 1.303, 1.244, 1.224 | false / 1 | C, T1, T2, T5 |

Exact scoring commands (shell variables are the path constants above; each exited 1):
```sh
R=/home/vgpnk/Projects/shokunin/kake-shokunin; S=/fast/scratch/hyaku/kake-r42w1/CtlLengthGate; C="$R/.ufo/waves/round-42/c42_count.py"
timeout 900 prlimit --as=8000000000 -- env TMPDIR="$S/tmp" python3 -B "$C" --root "$R" --tool-file "$S/skip_256.py" --label CtlLengthGate-skip_256 --seed 42043 --out "$S/skip_256.json"
timeout 900 prlimit --as=8000000000 -- env TMPDIR="$S/tmp" python3 -B "$C" --root "$R" --tool-file "$S/skip_1024.py" --label CtlLengthGate-skip_1024 --seed 42043 --out "$S/skip_1024.json"
timeout 900 prlimit --as=8000000000 -- env TMPDIR="$S/tmp" python3 -B "$C" --root "$R" --tool-file "$S/skip_2048.py" --label CtlLengthGate-skip_2048 --seed 42043 --out "$S/skip_2048.json"
timeout 900 prlimit --as=8000000000 -- env TMPDIR="$S/tmp" python3 -B "$C" --root "$R" --tool-file "$S/skip_10000.py" --label CtlLengthGate-skip_10000 --seed 42043 --out "$S/skip_10000.json"
timeout 900 prlimit --as=8000000000 -- env TMPDIR="$S/tmp" python3 -B "$C" --root "$R" --tool-file "$S/skip_100000.py" --label CtlLengthGate-skip_100000 --seed 42043 --out "$S/skip_100000.json"
timeout 900 prlimit --as=8000000000 -- env TMPDIR="$S/tmp" python3 -B "$C" --root "$R" --tool-file "$S/prefix_1024.py" --label CtlLengthGate-prefix_1024 --seed 42043 --out "$S/prefix_1024.json"
```
At most two counters ran concurrently to stay within the 300 MB seat bound. All six processes finished; no timeout or cannot-evaluate receipt.
Initial asynchronous launch requests for skip_256/skip_1024 were rejected by the tool-wide 100-background-job limit before starting; the same commands then ran synchronously.

Checked statements:
- holds — this counter rejects all six requested abbreviated-check controls on seed 42043; C and T5 catch every control.
- holds — skip_256 and skip_1024 meet every timing bound but fail equality (5/8): the detector distinguishes these cheaper tools from preservation.
- holds — skip_2048, skip_10000 and skip_100000 additionally exceed the T1 and T2 timing bounds; prefix_1024 exceeds T1 (2.032) and changes T2 judgments.
- holds — on each unequal timing shape, all five candidate repetitions differed (0/5); all other timing shapes were 5/5 equal. Receipts contain the actual CPU samples and output hashes.
No tool met, so no meeting-tool witness applies. This is a finding about these six controls and this seed, not a round verdict or proof of universal counter completeness.

Mutation probe and restoration:
- Expected detector: compare each scratch tool’s CLI exit and stdout with tip41 on fixed manifests containing `https://a.example/` + `a` repeated N + `|`, N=256,1024,2048,10000,100000.
- Same command on pristine, mutated, restored bytes: `timeout 60 prlimit --as=8000000000 -- python3 -B "$S/equality_detector.py"`.
- Actual detector exits / mismatched tools: pristine 0 / 0, mutated 1 / 6, restored 0 / 0. All six mutants killed, none survived or inconclusive.
- Actual full-output records: `S/probe-pristine.json`, `S/probe-mutated.json`, `S/probe-restored.json`; per-tool before/mutant/after hashes: `S/restoration-evidence.json`.
- Before and restored SHA256 of every `S/work/*.py`: `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`; mutated hashes are the six tool hashes above.
- Pristine and restored CLI exit 1 / stdout SHA256 `03cf385537ad482b7da0eca841f93000325b15cc842e36713fcb7aeacf874c7d` for every tool. Mutated stdout hashes and differing check IDs are retained in `probe-mutated.json`.
- Exact work-copy bytes restored; requested mutant artifacts retained separately for L1 rescoring. Shared sources and lane code were never written.
Tool installs/updates: none. No network use. No integration, scoring of the round, or shipping performed.
