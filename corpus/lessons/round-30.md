# Round 30 — citing-set reason fixtures and round-27 families; Render static-site knowledge

## Claims

Declared before implementation in `SCORECARD.md` section "Round 30 — declared
claims" (commit `4580c78cca1185d059efa6970722bbcf2f9c1b0f`), with declaration
notes added before any after-measurement at
`04637bdd1ac1c76517b764f48bdc83279edd7266`.

- **C1, operability, repair.** The citing-set gate's reason codes are asserted
  by committed fixtures that its runner compares, and the round-27 failure
  families that round 28 left open are repaired. Counter
  `.ufo/waves/round-30/c1_reason_count.py` (sha256 `be2a1287…c53e`); before
  0/14 at `0356681`, declared after 14/14. Strict closure supplement
  `.ufo/waves/round-30/c1_strict_checks.py`; before 0/6.
- **C2, freshness, frontier.** Render static-site deploy semantics enter held
  knowledge as `corpus/knowledge/render-static-sites.md`, grounded in S049–S052
  opened this round. Counter `.ufo/waves/round-30/c2_quote_truth.py` (sha256
  `a2cd3164…5e7a`); before 0/4, declared after 4/4. This is the round's
  learning claim and its sourced claim.

The citing-set fixture runner now compares findings at this granularity: the
exit code exactly, and either the sorted multiset of finding ids (legacy string
entries) or the sorted multiset of (finding id, reason) pairs (object entries),
one form per case. Rows, files and counts are not compared by the runner.

## Gate

### Source openings

The L1 opened each Render Docs page with one public GET (HTTP 200,
2026-10-22T11:49:44Z–11:49:45Z) through `.ufo/waves/round-30/fetch_sources.py`
(sha256 `b9431a5f…90b4`, named in every receipt). Received bodies, visible
text (HTML minus script, style and comments, tags removed, entities decoded,
whitespace collapsed) and sha256 receipts are in `.ufo/waves/round-30/sources/`.
Wave-1 seat `ReviewRenderPrimary` re-opened all four at 12:05Z: bodies differ
(a Render redeploy changed asset names and trace ids), and the visible text is
byte-identical to the retained text for all four. The text rule leaves a space
before some punctuation where an inline tag stood (for example
“static sites . Services”); quotes below are exact substrings of the retained
text after whitespace collapse, spacing included.

- S049 — https://render.com/docs/static-sites — accessed 2026-10-22, HTTP 200 — mined: Render rebuilds and atomically deploys a static site on every push to the deployed branch, then invalidates its CDN caches ; quote “We build your site with every push to your deployed branch, and each build is fully atomic.”
- S050 — https://render.com/docs/redirects-rewrites — accessed 2026-10-22, HTTP 200 — mined: Render's own documentation fixes how a static site resolves a path that already has a resource against a redirect or rewrite rule; quote “Render does not apply redirect or rewrite rules to a path if a resource exists at that path.”
- S051 — https://render.com/docs/static-site-headers — accessed 2026-10-22, HTTP 200 — mined: a Render static site has no server-side component to inject custom response headers, so headers are defined in the Render Dashboard and the header path is matched against every custom domain attached to the site ; quote “The header path must be a relative path without the domain. It will be matched with all custom domains attached to your site.”
- S052 — https://render.com/docs/custom-domains — accessed 2026-10-22, HTTP 200 — mined: Render attaches a custom domain to a web service or a static site, issues and renews TLS for it automatically, redirects HTTP on it to HTTPS, and keeps the onrender.com subdomain unless that subdomain is disabled ; quote “You can apply your own custom domains to Render web services and static sites . Services with a custom domain also keep their onrender.com subdomain.”

### Screened candidates (round-28 routed defect 4)

Wave-1 seat `ScreenRenderCandidates` searched for non-primary or weaker Render
static-site material and requested each candidate once (12:06:47Z–12:23:26Z).
Bodies, text and receipts are in `.ufo/waves/round-30/sources/screened/`
(C1–C3). Each quote is an exact substring of that retained text.

- S053 (C1) — https://dev.to/stephengade/how-to-deploy-static-website-for-free-on-render-with-custom-domain-4efo — accessed 2026-10-22, HTTP 200 — **rejected**: its one durable point, the catch-all rewrite to /index.html, is already carried by S050, and its custom-domain step names an ALIAS record that S052 does not; quote “Grab your CNAME and ALIAS to add to your domain name”.
- S054 (C2) — https://www.namesilo.com/blog/en/dns/how-to-connect-a-custom-domain-to-rendercom — accessed 2026-10-22, HTTP 200 — **rejected**: it pins an apex A-record address, 216.24.57.1, that no opened Render primary states; quote “Add an A record: Type: A Host: @ Value: 216.24.57.1 TTL: 3600”.
- S055 (C3) — https://docs.astro.build/en/guides/deploy/render/ — accessed 2026-10-22, HTTP 200 — queued, tier A scoped to Astro's own recipe, so the flip condition is that a current tier-A Render page states the same build and publish values for an Astro site; quote “Build Command: npm run build Publish Directory: dist , for static sites”.
- Not opened — https://stackoverflow.com/questions/74223164/i-cant-go-directly-to-a-url-on-my-site-after-deploying-to-render — returned HTTP 403 with a bot-challenge page; it was not opened by any other means and has no row.

### Sibling source

- S056 — tameshi-shokunin/corpus/knowledge/mte-report-interop.md at commit `f4e8f7d835a8e33c64a87ff93e79da32264f031c` (read-only `git show`; file sha256 `b173e3e5…0fac`) — opened 2026-10-22, section "What the interop does", line 21 — queued: wave-1 seat `MutBaseRunnerLedger` used its ledger shape for `.ufo/waves/round-30/mutant-ledger/base-0356681-ledger.mte.json`, but no kake knowledge entry cites it; quote “`score` is a sanity check that holds by construction.”

### Registry changes (old → new)

- S049, S050, S051, S052: no row → new rows, tier A, status `mined`, used-by `corpus/knowledge/render-static-sites.md`.
- S053, S054: no row → new rows, tier C, status `rejected`, each with a flip condition.
- S055: no row → new row, tier A scoped to Astro's own recipe, status `queued`.
- S056: no row → new row, kind `docs`, tier B, status `queued`, used-by `-`.
- No pre-existing row's status, recheck or used-by cell changed.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| boundary | A falsify seat ran `node scripts/freshness-sweep.mjs` with no section flag at base and at tip, so the `§armed` section sent live GET requests to the lane's pinned owned sites and `git ls-remote` to the pinned repositories. The seat disclosed it in its own report, and the non-author closure ruled it a boundary breach whose live results were declared unverified and on which no claim evidence rests. Evidence: `.ufo/waves/round-29/w2/NoHarmExistingGates.md:30` (finding 1, HIGH, process); `corpus/lessons/round-29-verifier-spotcheck.md:177-182` (ruling) and `:235-237` (routed defect 2); `corpus/lessons/round-29.md` "Seat process notes" (the `NoHarmExistingGates` paragraph). The tool's own argument handling is what makes the default live: `scripts/freshness-sweep.mjs:152-158` (only `--section=paths\|history\|armed\|plazir` is accepted; no flag means all sections), `:160-177` (usage text: `--offline` "skip every fetch/ls-remote" at `:168`, `(default) run all three sections` at `:166`), `:802-820` (`sectionArmed` returns live verdicts unless `offline`, which short-circuits at `:812`), `:724-726` (`fetchBody`), `:744` and `:897` (`git ls-remote origin main`). | `corpus/QUALITY.md:10` "Replayable claim" (reject column: "a partial/offline run presented as a complete publishing check") and, new for round 30, the bullet drafted in the "Proposed QUALITY.md additions" section below: "A seat names its offline mode before it runs a lane tool that reaches a live surface." | The round-30 wave context bars the three owned-surface tools in every mode and names the allowed offline flags, so the breach cannot recur through a default: `scripts/freshness-sweep.mjs --section=paths --json --offline` and `--help` only (corrected by wave-1 seat `ReviewSeatBoundsSweep`: `--section=history` spawns `probe-delta.mjs` and `systemctl` even under `--offline`, and `--selftest` writes to `/tmp` and `$HOME`; round-30 wave contexts barred the script entirely). **Shown able to fail:** `python3 -B .ufo/waves/round-30/witness/witness_sweep_live_mode.py --root <lane> --round round-29 --revision 234524c` exits 1 and names `NoHarmExistingGates.md:30`; the same command with `--round round-30 --revision 04637bd` exits 0. The check reads only committed bytes and never runs the sweep. |
| unattributed-evidence | Two committed evidence receipts named no revision and no tool digest, so a reader could not tell which bytes were measured. `selftest-lane-final.json` carries only `selftest`, `tool`, `fixtures`, `verdict`, `cases`, `passed`, `failed`, `failures`, `caseNames`; `real-input/out/summary.json` carries only `contractProblems`, `outRoot`, `sites`, `sitesRoot`, `tool`, `totals`. The round-29 wave-2 seat noted the receipt was taken over the repaired tool, and the non-author closure recorded the same gap as routed defect 3. Evidence: `.ufo/waves/round-29/verification/selftest-lane-final.json`; `.ufo/waves/round-29/real-input/out/summary.json`; `corpus/lessons/round-29-verifier-spotcheck.md:238-241`; `corpus/lessons/round-29.md` "Open after wave 2 (not repaired)". Both files name the tool by **absolute path**, which is a pointer to where a file was, not a statement of what it contained. | `corpus/QUALITY.md:10` "Replayable claim" (admit column: "The report names the source revision or script digest"), `corpus/QUALITY.md:128-131` (round-22 bullet: a receipt naming a disposable runner path must carry the command that recreates the runner from Git), and the new bullet drafted below: "A measurement receipt names the revision it measured and the digest of the bytes it measured." | Round-30 receipts carry the revision and the digests of every byte they depend on. The two round-30 before-receipts do: `.ufo/waves/round-30/verification/c1-before-0356681.json` names `revision`, `counterSha256`, `gateSha256`, `runnerSha256`; `.ufo/waves/round-30/verification/c2-before-0356681.json` names `revision` and `counterSha256`. **Shown able to fail:** `python3 -B .ufo/waves/round-30/witness/witness_receipt_identity.py --root <lane> --wave round-29 --revision 234524c` exits 1 and lists 7 receipts that do not name both a revision and a digest — 3 anonymous (`selftest-lane-final.json`, `selftest-lane.json`, `real-input/out/summary.json`: no revision and no digest) and 4 partial (the `c1-*.json` receipts, which name a revision but no digest). The same command with `--wave round-30 --revision 04637bd` exits 0. |
| unbacked-claim | The round-29 report and SCORECARD said C1 and C2 were "re-measured at `7697990`" (the report adds `234524c`), but no committed receipt names either revision, so two of the four named measurements had no committed evidence. Evidence: `.ufo/reports/round-29/kake.md:90-91` (claim table, "Measured at" column) against the committed receipt set, which names only `fe1805cf`, `98dbab2`, `f8675e5`, `d8cd2e4` (`corpus/lessons/round-29-verifier-spotcheck.md:242-245`, routed defect 4). The report's own "Receipts" line at `kake.md:94` points at `c1-after-*.json` and `c2-after-*.json`, which is a glob, not a claim that those revisions are covered. | `corpus/QUALITY.md:10` "Replayable claim" and `corpus/QUALITY.md:11` "Missing substrate stays visible", plus the new bullet drafted below: "A named measurement revision has a committed receipt that names it." | Round 30 re-measured the two round-29 revisions and prepared the receipts under `.ufo/waves/round-30/verification/r29-remeasure/`, each naming its revision, the counter path, the counter blob it came from, the counter sha256, the exit code and the counter output: `r29-c1_quote_truth-at-7697990.json`, `r29-c1_quote_truth-at-234524c.json`, `r29-c2_matrix_count-at-7697990.json`, `r29-c2_matrix_count-at-234524c.json`. **These four files are present in the lane working tree but are still untracked at `04637bd`; the L1 must commit them for the fix to land.** **Shown able to fail:** `python3 -B .ufo/waves/round-30/witness/witness_claim_receipt_backing.py --root <lane> --report .ufo/reports/round-29/kake.md --wave all --revision <tip>` exits 1 and names `234524c` and `7697990` as unbacked at `04637bd`; at a sandbox commit that adds those four files to the tree it exits 0. |
| vacuous | The round-29 C2 counter compared no `id`, no `page`, no `resolved` and no counts, so a tool that returned the right exit code, verdict and reason codes while reporting a wrong finding id, a wrong page, a wrong resolved URL and wrong counts scored a full pass; the usage case was judged on the exit code alone. The counter projects the **expected** finding's keys onto the observed finding (`.ufo/waves/round-29/c2_matrix_count.py:62-72`), and the frozen matrix expectations name only `attribute`, `element`, `reason`, `value` (`.ufo/waves/round-29/c2-matrix.json`, 30 cases; the expectation key set is `['attribute','element','reason','value']`), so `id`, `page` and `resolved` were never read; the report-level counts `pagesChecked` and `referencesChecked` were never read; and the usage branch returns "ok" on the exit code before stdout is parsed (`:79-82`). Evidence: `corpus/lessons/round-29-verifier-spotcheck.md:246-248` (routed defect 5) and `corpus/lessons/round-29.md` "Open after wave 2 (not repaired)". The wave-2 seat `FieldsAndCounts` repaired the **fixture runner** (`scripts/base_path_selftest.py:52-53` compares `page` and `resolved`; `:214` compares a count when the fixture names one), but the **counter** was left as it was, so the repair did not reach the counter that grades the claim. | `corpus/QUALITY.md:362-374` "A counter compares the reason code, not only the id" and `corpus/QUALITY.md:317-322` "Conformance exceptions stay named" (the round-27 runner compared only exit code and the finding-id multiset, so finer differences were outside what a passing run showed), plus the new bullet drafted below: "A counter compares every field its expectation names, and its usage case is judged on the usage object, not the exit code alone." | A counter whose expectations name `id`, `page`, `resolved` and the counts compares them, and its usage case parses stdout as one JSON object. The extended matrix and the strict counter are committed at `.ufo/waves/round-30/witness/` (`build_extended_matrix.py`, `strict_c2_counter.py`, `extended-matrix.json`). **Shown able to fail:** the shipped counter accepts a mutant whose finding `id` is `WRONG-ID`, whose `page` and `resolved` are `https://wrong.example/...`, whose counts are `999999` and `888888`, and whose usage path prints `not json at all` while still exiting 64 — the shipped counter scores it 30/30, exit 0. The strict counter against the extended matrix scores the same mutants 9/30 and 29/30 (exit 1), and scores the real tool 30/30 with all three constant gates rejected. |
| counter-hole | The round-30 declared C1 counter, written by the L1 before the round, could be satisfied without the property: wave-1 critic `CriticC1Counter` built a gate that lists every code in one refusal and a reason-blind runner with a separate source check, each scoring 14/14 (`.ufo/waves/round-30/w1/CriticC1Counter.md`); `ReviewC1Before` and `CriticFamilyOutcomes` showed F04 missed `--name=value` and prefix-abbreviated repeats and F02 missed NaN outside the population and `1e999`. | `corpus/QUALITY.md` "A counter must be able to reject a constant" (round 28) catches constant gates only; near-miss stubs were not covered. | The declared counter stayed frozen; a strict supplement `.ufo/waves/round-30/c1_strict_checks.py` was declared before any after-measurement (`04637bd`) and must also pass. **Shown able to fail:** 0/6 at base (`verification/c1-strict-before-0356681.json`); the critic's stubs are the near-miss cases it targets (S1 exact refusal, S2 rename precision, S3 every spelling). |

## Round-29 routed defects (spot-check items 1 to 5)

1. Citing-set fixtures for reason codes and the round-27 families: repaired
   as C1 (14/14 declared counter, 6/6 strict supplement at `71c6bfa`).
   Reason codes still without a fixture are listed in `SKILL.md`,
   "Citing-set reason-code registry — round 30" (12 of 25).
2. Live `freshness-sweep.mjs` runs by seats: both wave contexts barred
   `freshness-sweep.mjs`, `probe-delta.mjs` and `live_snapshot.py` in every
   mode; the allowed offline invocation is now a `QUALITY.md` criterion
   (round-30 section, first bullet) with a witness that fails on round 29.
3. Receipts without revision or tool digest: the round-29 selftest and
   real-input demonstration were re-run at `4580c78` with digests recorded
   (`.ufo/waves/round-30/r29-rerun/receipt.json`; numbers equal round 29's).
   Every round-30 counter output names the counter sha256 and the measured
   revision; C1 outputs also name the gate and runner sha256.
4. Unreceipted re-measurements at `7697990` and `234524c`: receipts committed
   at `.ufo/waves/round-30/verification/r29-remeasure/` (each names the
   revision, the counter blob from `234524c` and its sha256): C1 4/4 and C2
   30/30 at both revisions.
5. Round-29 C2 counter compares no `id`, `page`, `resolved` or counts:
   explained, not re-scored. The round-29 matrix names no expected values for
   those fields, so the frozen counter cannot compare them. A regression pin
   `.ufo/waves/round-30/witness/extended-matrix.json` plus
   `strict_c2_counter.py` compares them (a mutant with all of them wrong:
   9/30, exit 1); the pin records the tool's own output at `234524c`, so it
   guards against change, not against an error the tool already had.

## Wave-2 falsification and the repairs it caused

- Runner harms repaired: mixed-reason expectations crashed the runner, an
  unwritable case copy crashed it (`w2/ScoutNoHarmDiff.md`, fixed at
  `1c7773e`); `case.json` setup could escape `--tmpdir`, run fixture Git
  hooks, read outside the case and accept 100,000 steps
  (`w2/SentinelRunnerSetup.md`, fixed at `f80bd8f`: contained relative paths,
  no fixture `.git`, `core.hooksPath=/dev/null`, symlinked cases skipped,
  at most 64 steps and 64 KiB).
- Fixture gap narrowed: repeated options gained fixtures 42–45 (exit 64);
  deep corpus and `O_NOCTTY` stay guarded by the counters only
  (`w2/MutGateRepeatsWalkTty.md`).
- Entry corrected: four contrasts with GitHub Pages (`w2/CriticEntryContrast.md`),
  four wording overreaches (`w2/ReviewEntryBuildRules.md`), the recheck line
  (`w2/CriticMeasurementLimits.md`).
- Rows corrected: S053 and S054 reasons and flips, S055 flip and dynamic-site
  caveat (`w2/CriticRejects.md`); README, PROVINCE and SKILL scope wording
  (`w2/CriticFrontierWording.md`, `w2/CriticC1Scope.md`); QUALITY round-30
  bullets rewritten with witness limits (`w2/CriticQualityCriteria.md`).
- Not repaired, recorded: strict-checker holes (`w2/CriticStrictChecker.md`),
  runner survivors m2, m4, m5 (`w2/MutRunnerCompare.md`), the round-30
  receipt-identity witness miss on `r29-rerun/real-input/summary.json`.
- Seat process: `ScreenRenderCandidates` sent 15 GETs to third-party hosts
  (3 retained); `ScoutRenderChangelog` sent 77 GETs to render.com; no seat
  contacted an owned site. Nineteen wave-2 seats were cancelled at wrap-up;
  their partial reports, where present, are unverified.
