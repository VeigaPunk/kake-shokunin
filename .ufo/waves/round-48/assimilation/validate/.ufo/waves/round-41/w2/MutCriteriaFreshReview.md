# MutCriteriaFreshReview — r41-falsify
Axes: operability (judged), freshness. Scope: QUALITY (t) checker only; no round verdict or integration.
Artifacts: `/fast/scratch/hyaku/kake-r41w2/MutCriteriaFreshReview/` contains five retained `mutants/*.py`, five restored `active/*.py`, own `fixtures/`, `detector.py`, and actual command/stdout/stderr/exit/hash records in `results/*.json`.

## Commands and actual outputs
Command abbreviations below expand to these exact paths/digests:
`L=/home/vgpnk/Projects/shokunin/kake-shokunin`; `S=/fast/scratch/hyaku/kake-r41w2/MutCriteriaFreshReview`; `F=.ufo/waves/round-41/criteria/fresh_review_check.py`.
`H40=4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e`; `H41=0b485431d96268d46c8dc9052eec92520248a03989896bd83f4521f15f13edbf`.
From L: `timeout 60s prlimit --as=4000000000 -- python3 "$F" --tool-sha "$H40" --reports "$L/.ufo/waves/round-40/w1" "$L/.ufo/waves/round-40/resid"` → exit 1; `final tool 4de35f8c9d3e7849…: seat reports naming it: 0`.
From L, same command with H41 and round-41/w1, round-41/w2 → initially exit 1, zero hits, while this concurrent wave was still returning.
From S: `timeout 180s prlimit --as=4000000000 -- python3 -B detector.py pristine` → exit 0; all five pristine copies pass 9/9 literal-matcher cases (45/45).
From S: `timeout 180s prlimit --as=4000000000 -- python3 -B detector.py semantic` → exit 1; seven advertised/semantic expectations fail on pristine bytes (not mutant kills).
From S: `timeout 180s prlimit --as=4000000000 -- python3 -B detector.py mutated` → exit 1; all five mutants killed as below.
From S: `timeout 180s prlimit --as=4000000000 -- python3 -B detector.py restored` → exit 0; 45/45 again.
From S: `timeout 180s prlimit --as=4000000000 -- python3 -B detector.py real` → wrapper exit 0; child exits 1 (round 40), 0 (round 41).
Each real child: `timeout 8s prlimit --as=4000000000 -- /usr/bin/python3 -B "$L/$F" --tool-sha "$H40" --reports "$L/.ufo/waves/round-40/w1" "$L/.ufo/waves/round-40/resid"` (or H41 and round-41/w1, round-41/w2); exact expanded argv in `results/real.json`.
Latest round-41 output: `final tool 0b485431d96268d4…: seat reports naming it: 6`; hits: w2/CriticExploratoryBetter.md, RerunBuildV1Seeded.md, RerunBuildV2.md, ReviewHarmRealRun.md, ReviewHarmScope.md, ReviewHarmSelftest.md (all under w2).
The later green is a live-directory snapshot before writing this report, not proof of the reports' substantive content. Round-40-red statement: **holds**. Round-41 six-hit snapshot: **holds**.

## Five single-point checker mutants
Same nine-case detector runs on pristine, mutated, and restored bytes; baseline/restored each 9/9 per mutant. No surviving or inconclusive mutants in this literal-matcher battery.
| Mutant (source line) | Defect; expected detector | Actual mutated output / exit | Verdict; mutated SHA256 |
|---|---|---|---|
| M01_force_success (31) | unconditional exit 0; empty directory must exit 1 | `seat reports naming it: 0`, exit 0; also fails unrelated/txt cases | killed; `06298943b986757cac8efb5f4a046d81ba25cba621281a8c69b733d8ee81b161` |
| M02_ignore_sha (23) | drop digest predicate; unrelated .md must exit 1 | `seat reports naming it: 1`, `unrelated/Unrelated.md`, exit 0 | killed; `10c5ccdef081d5463659d059927286ee911ec570d8d7f1d237ecf118050a6205` |
| M03_case_sensitive (23) | remove report lowercasing; uppercase digest must exit 0 | `seat reports naming it: 0`, exit 1 | killed; `882bbbad8d343cb12d58d3599ef02cd9031919bfc9045a2c3d2062eeb2602447` |
| M04_first_dir_only (21) | scan only first directory; second-directory hit must exit 0 | `seat reports naming it: 0`, exit 1 | killed; `91823b23acd567da1bae9b1a5a1c10a450487cbbdb5982d3b439b841f213de7e` |
| M05_accept_txt (23) | admit .txt reports; txt-only digest must exit 1 | `seat reports naming it: 1`, `txt_only/Receipt.txt`, exit 0 | killed; `afda86f4d0a8af6258665905ab463af5f010da1be5474b46fbd2a68a60a01f68` |
All five active copies before AND after: `eba334a57448ddbe067adba499391c6206bcea752b8772fd4c2c72809dd651e2`, identical to the lane checker hash; retained mutant artifacts match their tested mutated hashes. Restoration is exact; lane checker/tool never edited.

## Weaknesses on pristine checker bytes
- **HIGH — overstated:** `.ufo/waves/round-41/criteria/fresh_review_check.py:2,23-24` does not establish a review occurred. Own `quote_only/Quote.md` contains only a quoted full H41 digest: exit 0, one hit. `not_reviewed/Declined.md` explicitly denies reviewing/running the build: also exit 0, one hit. Thus merely quoting a SHA **does pass**.
- **HIGH — wrong:** `.ufo/waves/round-41/criteria/fresh_review_check.py:4-5,21-24` promises exclusion of L1 files but implements none. Separate directories containing only `KakeR41.verdict.md` or only `KakeR41.md` each return exit 0, one hit. No identity/freshness check exists in the scanned predicate.
- **MEDIUM — wrong:** `.ufo/waves/round-41/criteria/fresh_review_check.py:3,11-14` documents `--l1` but does not register it. Positive fixture plus `--l1 KakeR41` exits 2: `error: unrecognized arguments: --l1 KakeR41`.
- **LOW — overstated as full-build attribution; holds as documented prefix matching:** `.ufo/waves/round-41/criteria/fresh_review_check.py:15,23` accepts a different full digest sharing only H41's first 16 characters (`prefix_collision/Stale.md`): exit 0, one hit. This is an explicit prefix rule, not an accidental-collision claim.
- **LOW — wrong if --tool-sha is claimed to require a SHA256:** `.ufo/waves/round-41/criteria/fresh_review_check.py:15-18` checks only prefix length. `--tool-sha not-a-real-sha256-value` with the matching nonhex fixture exits 0 and prints `final tool not-a-real-sha25…: seat reports naming it: 1`.
Literal .md substring matching, case normalization, both-directory scanning, short-input exit 2 and missing-directory exit 2: **hold** in the exercised detector. These kills do not rescue the failed freshness/review semantics.
All runs bounded by timeout and 4 GB address-space limits; detector concurrency two workers; all synchronous child processes exited. No network, package installs, services, or changes outside this sandbox and this report.
