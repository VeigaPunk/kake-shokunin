# RerunHostileSelftest — C1 hostile selftest re-run against both runners (attempt 2, wave 2)

Axes: operability (judged), freshness. Seat: leaf falsifier, no subagents used. No tool installs (none needed).

## What I attacked
The C1 claim's hostile-selftest receipts: `verification/hostile-selftest-c88b97e.json` (repaired runner, expected 5/5 pass)
and `verification/hostile-selftest-base-runner.json` (base runner, expected 0/5, exit 1). I reproduced both runs from
fresh exports instead of trusting the receipts, and looked for receipts that overstate (pass values that don't reproduce,
per-spec fields that differ materially).

## Exact commands and exits
Sandbox: `/fast/scratch/hyaku/kake-r31/a2-w2/RerunHostileSelftest/` (all writes below are inside it).

1. Export scripts/ at fde133a: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin archive fde133ab48086bb9a06911b4ab045e2ad9086347 scripts/ | tar -x -C <sandbox>/export` — exit 0; all five spec dirs present under `export/scripts/fixtures/citing-set-hostile/` (P1-selftest-argv, P2-fixture-dot-git, P3-commit-without-init, P4-expected-json-guard, P5-symlinked-case).
2. Base runner export: `git archive f1ffb81738c92c0537b99b30970143ab9419f990 scripts/citing_set_selftest.py | tar -x -C <sandbox>/base` — exit 0. Byte-identity check: `git show f1ffb81:scripts/citing_set_selftest.py | sha256sum` = `9f2d1ecb280b7dc314886c79264fb5461c400d8f7c762ea62bb4018fc49e14d3` = sha256 of the extracted file. Identical.
3. Repaired runner: `TMPDIR=<sandbox>/tmp python3 -B <sandbox>/export/scripts/citing_set_hostile_selftest.py --root <sandbox>/export --tmpdir <sandbox>/t1` — **EXIT=0**.
4. Base runner: same command with `--tmpdir <sandbox>/t2 --runner <sandbox>/base/scripts/citing_set_selftest.py` — **EXIT=1** (wall 90.7s; P4 hang is the base runner's own behavior, selftest completes normally).

## Observed per-spec results vs receipts

### Run A — repaired runner (mine) vs `hostile-selftest-c88b97e.json`
Top level: passed=true both. Every case passed=true, exit=1, timedOut=false, canary=false, victimUnchanged=true, hostile sets h1a-h1c / h2a-h2b / h3 / h4a-h4c / h5 — all identical to the receipt. Reasons strings identical except:
- h4a reason embeds a scratch path: receipt `/fast/scratch/hyaku/kake-r31/l1/hn/P4-.../fixtures/h4a/expected.json`; mine `<sandbox>/t1/P4-.../fixtures/h4a/expected.json`. Path-only difference, same errno text (Too many levels of symbolic links).
- `runner` field: receipt `/fast/scratch/hyaku/kake-r31/l1/exp/scripts/citing_set_selftest.py`; mine `<sandbox>/export/scripts/citing_set_selftest.py`. Path-only.

### Run B — base runner (mine) vs `hostile-selftest-base-runner.json`
Top level: passed=false both, error=null both. Every case passed=false, hostile sets identical. Per-case fields identical in every dimension:
- P1: exit 1, canary **true** (hostile fixture script executed — the N1 gap), reasons all "gate report carries no 'findings' array" — identical.
- P2: exit 0, victimUnchanged=false — identical.
- P3: exit 0, victimUnchanged=false — identical.
- P4: exit null, timedOut=true — identical.
- P5: exit 0, victimUnchanged=true — identical.
- `runner` field path-only difference (receipt `/fast/scratch/hyaku/kake-r31/l1/base-runner.py`; mine `<sandbox>/base/scripts/citing_set_selftest.py`).

## Verdict on this seat
Both receipts reproduce exactly; no overstatement found. The repaired runner refuses all five hostile shapes with
canary untouched and victim unchanged; the base runner fails all five with the canary breached on P1 — matching the
declared C1 counter expectations (0/5 before, K1-style control not in scope of this seat's command set).

## Provenance (sha256)
- receipts: hostile-selftest-c88b97e.json `a646ca418ff22bca476a51bf383b7ed9497f66ee210699af15dfcda7d00a0833`; hostile-selftest-base-runner.json `de764961822f9eca24c915ddf6e6f4f5bdce84a424b492e7bc54bd527757ac48`
- export at fde133a: citing_set_hostile_selftest.py `275d4144053e9216059c7836e31ccf4c8ce0220c12bee5a58b031c08d7bc3198`; citing_set_selftest.py `5371530d93ecb218b4607fb37de810fe7b7b2db869c65c8b65988b2f04c0ce6c`; citing_set.py `dbfade45e59351fb5edc010dfc45a4e15e1213fdb6fad9ec1668ffd3b77b7f02`
- base runner (f1ffb81): `9f2d1ecb280b7dc314886c79264fb5461c400d8f7c762ea62bb4018fc49e14d3`
- Receipt-vs-export comparability: `git diff --stat c88b97e fde133a -- scripts/` is empty — scripts/ unchanged between the receipt commit and my export commit, so the comparison is apples-to-apples.

## Not verified / residual risk
- I did not re-derive the receipt JSONs' own integrity beyond content comparison (hashes above pin what I compared).
- I did not attack the hostile selftest's own harness logic (e.g. whether `passed` could be true while a gap slips) — that is the held CriticC1Counter territory; not repeated here per bounds.
- P4 base-runner run took ~90s of the 300s job window; no truncation, full JSON captured.
- Lane repo untouched except this report file; no refs, index or jj state mutated; no pacman/partial upgrades; no installs.
