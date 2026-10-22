# ReviewLogScorecard — LOG/SCORECARD round-31 record audit (wave 2, falsify)

Scope: LOG.md `### Round 31 — attempt 1` and SCORECARD.md `## Round 31 — declared claims` + `Declaration notes` + `## Round 31 — measured results` at `92235a0578b04458c5eb96c966f82fa03593130e` (92235a0). Method: sandbox clone `/fast/scratch/hyaku/kake-r31/a2-w2/ReviewLogScorecard/clone`; all checks read-only `git show`/`ls-tree`/`merge-base`/`cat-file`, plus `git -C /home/vgpnk/Projects/ds4cc-marketplace show 1fbdb8ed:render.yaml | git hash-object --stdin`. No counters re-run; this is a record audit, not a re-measurement.

## Commit pointers — all resolve, all ancestors verified

| Ref in text | Resolves | Ancestor of fde133a | Ancestor of 92235a0 | Commit time (UTC-3) |
|---|---|---|---|---|
| `f1ffb81` (base) | f1ffb81738c92c05... | yes | yes | 10:57:08 |
| `a16602a` (declaration) | a16602a961da5d6e... | yes | yes | 12:45:50 |
| `c88b97e` (C1 impl) | c88b97e6b02d8535... | yes | yes | 12:59:15 |
| `b801ac8` (strict supplement) | b801ac808834aaa8... | yes | yes | 13:00:26 |
| `fde133a` (C2 landed) | fde133ab48086bb9... | self | yes | 13:05:29 |

Ordering (merge-base + %ct): a16602a < c88b97e < b801ac8 < fde133a < 92235a0, linear.
- Declaration `a16602a` precedes C1 implementation `c88b97e`: confirmed.
- Strict supplement `b801ac8` precedes any C2 after-receipt: the only C2 after-receipt is `c2-after-fde133a.json` (revision fde133a, committed 13:05:29); b801ac8 (13:00:26) is its ancestor and earlier. Receipts carry no wall-clock run timestamp; precedence rests on commit times and the receipt's `revision` field.
- LOG claim "C1 after ... at c88b97e" is consistent: `c1-after-c88b97e.json` names revision c88b97e6..., and b801ac8's message records that the after receipt was already taken at c88b97e.
- Two hex refs in Declaration notes are sandbox commits, not lane history: `b6580c79` (full `b6580c798108b263fe4898178c4d7cedbdf30e56`, "sandbox clone commit ... parent a16602a" in `w1/CriticC2Sizing.md`) and `5eabd69c`. `git cat-file -t` fails for both — they are explicitly labeled sandbox artifacts, so not a defect against "ancestor of fde133a", but they cannot be inspected from lane history; only the report documents them.
- `d17ab7e5` (render.yaml blob): verified — `git -C /home/vgpnk/Projects/ds4cc-marketplace show 1fbdb8ed:render.yaml | git hash-object --stdin` → `d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252`. Content is a docker web service with `healthCheckPath: /health` and envVars, matching SCORECARD/context descriptions.

## Receipt paths — all exist at 92235a0

`verification/c1-before-f1ffb81.json`, `c1-after-c88b97e.json`, `c1-after-fde133a.json`, `c2-before-f1ffb81.json`, `c2-after-fde133a.json`, `c2-strict-before-f1ffb81.json`, `c2-strict-before-c88b97e.json`, `c2-strict-after-fde133a.json`, `hostile-selftest-base-runner.json`, `hostile-selftest-c88b97e.json`, `closure-command-check.txt`, `w1/dead-seats.json`, `w1/seat-status.json`, `sources/S057..S061.txt`, `sources/S057..S061.html.gz`, `sources/receipts.json`, `.ufo/waves/round-30/w2/partial-reports.json`, counters `c1_sandbox_probes.py`, `c2_quote_truth.py`, `c2_strict_checks.py`, `fetch_sources.py`.

## Numbers vs receipts — all match

- C1 before: receipt passed 0/5, controlK1 true, k1 {exit 0, cases 45} → SCORECARD "0/5, K1 holds with 45 cases": match. LOG harm narrative confirmed by receipt detail: P1 `canary: true` (canary written), P2+P3 `victimUnchanged: false` (victim repos changed), P4 `timedOut: true` (FIFO hang), P5 exit 0 with no failed cases (silently skipped).
- C1 after at c88b97e and re-measured at fde133a: both receipts passed 5/5, controlK1 true, 45 cases, runnerSha256 `5371530d…ce6c`, counterSha256 `4707cebf…6d1a` → "5/5, K1 holds (45 cases)": match. `git diff --stat c88b97e fde133a -- scripts/` empty → "(no scripts/ change between them)" verified.
- Hostile selftest: `hostile-selftest-c88b97e.json` passed true, all 5 cases pass, repaired runner exits 1 per case → "exit 0"; `hostile-selftest-base-runner.json` passed false, 0/5 → "exit 1, 0/5". Receipts record no top-level exit code, but `citing_set_hostile_selftest.py` lines 237–243 return `0 if passed else 1`, so `passed` fields encode the claimed exits.
- C2 before: 0/4, controlBroken false → match. C2 after: 4/4, controlBroken false, all checks true per id → "4/4, control not broken": match.
- C2 strict before: 0/5 at f1ffb81; 1/5 at c88b97e (S5 only true) → match. Strict after: 5/5 at fde133a → match.
- Sources receipts: S057–S061 `accessedUtc` 15:41:23Z–15:41:29Z, status 200, `fetcherSha256 bc66ceb0…42c9` → matches declared fetch window and fetcher hash.
- Counter identity: `git show a16602a:c1_sandbox_probes.py | sha256sum` = `4707cebf…6d1a`; `c2_quote_truth.py` = `de48d460…31b8`; `b801ac8:c2_strict_checks.py` = `5111264f…46ad`; `fetch_sources.py` = `bc66ceb0…42c9` → all equal declared prefixes/suffixes and receipt `counterSha256`/`checkerSha256`.
- partial-reports.json: statuses complete 15, partial 5 → "15 complete, 5 partial": match.
- seat-status.json: seats 33, dead-at-spawn 18 (all executor/scribe/mutation-tester, "No model selected"), refused 1, returned-after-safety-filter 1 → LOG claims match. dead-seats.json note confirms roles and error text.
- closure-command-check.txt: exists; records pass-as-written and able-to-fail outcomes consistent with LOG/SCORECARD wording.
- PROVINCE.md at f1ffb81 round-30 section: "Render web service deploys ... and the Blueprint file stay open" → matches LOG/SCORECARD motivating claim.
- render-static-sites.md `## Round-31 corrections`, SKILL.md `## Citing-set runner containment — round 31`, lesson round-31.md S053/S054 → `rejected`→`rejected` with flip conditions met (S061 names ANAME/ALIAS and 216.24.57.1): match "both stay rejected".
- SOURCES.md rows S057–S061 exist at fde133a, status `mined`, fetched timestamps match receipts.json.

## Observations (low severity; none flip a declared number)

1. `b6580c79` and `5eabd69c` do not resolve in lane history. They are correctly labeled sandbox commits (CriticC2Sizing report documents their construction), but the Declaration-notes sentence "The two sandbox commits of CriticC2Sizing score 1/5 and 2/5" has no lane-committed verification receipt; only `c2-strict-before-{f1ffb81,c88b97e}.json` exist. The claim is plausible (hollow commit fails S1–S3 while S5 holds → 1/5) but not receipt-backed.
2. "Strict supplement precedes any C2 after-receipt" is provable only via commit times: receipts record `revision`, not measurement wall-clock. A receipt generated at b801ac8-time then relabeled would be undetectable from the record; nothing suggests this.
3. LOG says hostile selftest "exits 1 against the base runner"; the receipt stores `passed: false` rather than the literal exit code. The mapping `passed → exit` is verified from `scripts/citing_set_hostile_selftest.py:237-243`, so the claim holds, but the receipt itself does not name the integer.

## Not verified
Counter behavior itself (no re-run of c1_sandbox_probes/c2_quote_truth/c2_strict_checks — out of this seat's scope); truth of entry sentences vs quotes (explicitly excluded by the declaration); lane-freshness of PROVINCE beyond the round-30 lines cited.

No defects found in the round-31 LOG/SCORECARD records: every commit pointer resolves and is an ancestor as required, every receipt path exists, ordering constraints hold, and every printed number matches its receipt.
