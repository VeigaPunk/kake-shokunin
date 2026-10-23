MET
Axes: operability measured; freshness not exercised. One control, one fixed-seed mutation probe; no lane source changes.
The control meets at its baked seed 4204201, but the identical bytes do NOT meet at fresh seed 4204202.

Artifacts (S=/fast/scratch/hyaku/kake-r42w1/CtlIdKeyed):
- Control: $S/manifest_keyed.py; sha256 54f7edf721f7995c72cf9f41973a6cdf7dfd05150b90b2df868ba52715d226de.
- Pristine/restored: $S/pristine.py and $S/probe.py; sha256 50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d.
- Counter: .ufo/waves/round-42/c42_count.py; sha256 7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6.
- Trace builder: $S/build_plans.py; sha256 a884aee03f160e97f351c42da0d15ae8a7ab7a337af39ca379715445386536df.
- Witness detector: $S/check_witness.py; sha256 9b9b806e07287959ff70e1f31e0fb04efa5b71b0b6acec2bbbc5e8d07e6719ca.
- Embedded-plan source: $S/plans.json; sha256 0f0351a1cfe2b48a2e7814cd2daec62bb3996d4aea75acd979b62b229e70a30a.

Mutation: tip41 plus a matcher wrapper, selected by manifest basename, that substitutes prerecorded match truth by call order (manifest_keyed.py:89; activation :480). Unrecognized names retain tip41 behavior; mapped names never inspect URL characters in the wrapper. Existing urlsplit still runs on accepted calls.
Skipped work: T1's 20,001, T2's 20,001 and T5's 57 URI-regex calls. The trace uses only tip41's own judgments, replaying the counter RNG to learn the three names. No outside-case reads, runtime label/seed lookup, CPU hiding, or new character-level URL rules.
Expected detector: reject the non-equivalent control as not met. Observed: SURVIVED at baked seed, no run caught it; all timing repetitions equal 5/5. Fresh seed rejects it on T1/T2/T5 cost, not equality, because its skips no longer activate.

Receipts, ratios ordered T1,T2,T3,T4,T5 (every receipt under $S):
- pristine.json: seed 4204201, exit 1, equalRuns 8/8, ratios [5.408,2.766,1.367,1.225,10.157], met false. No skip; timing failed T1/T2/T5.
- mutant.json: seed 4204201, exit 0, equalRuns 8/8, ratios [0.834,1.020,1.339,1.241,1.038], met true. Tool was mutant bytes at probe.py, preserved unchanged as manifest_keyed.py.
- fresh.json: seed 4204202, exit 1, equalRuns 8/8, ratios [5.254,2.782,1.435,1.255,12.491], met false. Same control bytes; T1/T2/T5 caught cost only.
- restored.json: seed 4204201, exit 1, equalRuns 8/8, ratios [5.250,2.772,1.353,1.220,9.750], met false. Exact pristine bytes; timing failed T1/T2/T5.
All four receipts have every run equal and every timing candRepsEqual 5/5. Baseline already fails speed: kill-style mutation sensitivity is inconclusive, NOT a killed mutant. The passing non-equivalent control is the positive finding.

Witness: $S/witness/586c61c3a2e24a6.json names sitemap.xml, with sitemapUrl https://example.test/sitemap.xml and one loc https://example.test/bad|value.
Actual stdout: pristine and restored = failed-policy, loc_not_absolute at entry 1, exit 1; control = clean, findings [], exit 0; all stderr empty. Exact outputs and hashes: $S/witness.json.

Exact bounded commands (variable expansion only; cwd $S):
```sh
S=/fast/scratch/hyaku/kake-r42w1/CtlIdKeyed
R=/home/vgpnk/Projects/shokunin/kake-shokunin
C=$R/.ufo/waves/round-42/c42_count.py
timeout 900 prlimit --as=8000000000 -- python3 -B "$S/build_plans.py" # exit 0
timeout 900 prlimit --as=8000000000 -- env TMPDIR="$S" python3 -B "$C" --root "$R" --tool-file "$S/probe.py" --label CtlIdKeyed-pristine --seed 4204201 --out "$S/pristine.json" # exit 1, before mutation
timeout 900 prlimit --as=8000000000 -- env TMPDIR="$S" python3 -B "$C" --root "$R" --tool-file "$S/probe.py" --label CtlIdKeyed-mutant --seed 4204201 --out "$S/mutant.json" # exit 0, mutated bytes
timeout 900 prlimit --as=8000000000 -- env TMPDIR="$S" python3 -B "$C" --root "$R" --tool-file "$S/manifest_keyed.py" --label CtlIdKeyed-fresh --seed 4204202 --out "$S/fresh.json" # exit 1
timeout 10 prlimit --as=8000000000 -- cp "$S/pristine.py" "$S/probe.py" && timeout 10 prlimit --as=8000000000 -- cmp -s "$S/pristine.py" "$S/probe.py" && timeout 10 prlimit --as=8000000000 -- sha256sum "$S/pristine.py" "$S/probe.py" "$S/manifest_keyed.py" # exit 0
timeout 900 prlimit --as=8000000000 -- env TMPDIR="$S" python3 -B "$C" --root "$R" --tool-file "$S/probe.py" --label CtlIdKeyed-restored --seed 4204201 --out "$S/restored.json" # exit 1
timeout 30 prlimit --as=8000000000 -- python3 -B "$S/pristine.py" --manifest "$S/witness/586c61c3a2e24a6.json" # exit 1
timeout 30 prlimit --as=8000000000 -- python3 -B "$S/manifest_keyed.py" --manifest "$S/witness/586c61c3a2e24a6.json" # exit 0
timeout 60 prlimit --as=8000000000 -- python3 -B "$S/check_witness.py" # exit 0, after restoration
```
Restoration: before 50287ac6…; mutated 54f7edf7…; after 50287ac6… (full hashes above); cmp exit 0, and the same counter/seed was run on pristine, mutated and restored bytes. Retained mutant is a separate artifact.
Per checked statement: fixed-seed counter rejects this identity-keyed control — WRONG; control keeps every tip41 judgment — WRONG (witness); names carry no case identity (c42_count.py:38) — OVERSTATED for known replayable seed (:539); unchanged control meets a fresh seed — WRONG; exact restoration — HOLDS.
Limit: finite-seed overfitting, not an unseen-seed bypass; no round/admission verdict. Only two counters ran concurrently; all started processes exited. No tools installed. Initial async builder launch was refused at the harness job cap; the bounded foreground retry succeeded.
