# Round 31 — citing-set runner containment; Render web services and the Blueprint file

## Claims

Declared before implementation in `SCORECARD.md` section "Round 31 — declared
claims" (commit `a16602a961da5d6e75cfa09a1118a416ad01225b`), with a C2 strict
supplement declared before any C2 after-measurement at
`b801ac808834aaa8a4cc772fee23b0b80b1287e3`.

- **C1, operability, repair.** The citing-set fixture runner refuses the five
  hostile fixture shapes the round-30 closure routed (N1, N2, N3, N5, N6), and
  each refusal has a committed hostile spec checked by a committed hostile
  selftest. Counter `.ufo/waves/round-31/c1_sandbox_probes.py` (sha256
  `4707cebf…6d1a`); before 0/5 at `f1ffb81`, declared after 5/5 with control
  K1 holding.
- **C2, freshness, frontier.** Render web-service and Blueprint semantics
  enter held knowledge as `corpus/knowledge/render-web-services.md`, grounded
  in S057–S060 opened this round, with an offline key-by-key check of the
  lane's own `render.yaml`. Counter `.ufo/waves/round-31/c2_quote_truth.py`
  (sha256 `de48d460…31b8`); before 0/4, declared after 4/4. Strict
  supplement `.ufo/waves/round-31/c2_strict_checks.py` (sha256
  `5111264f…46ad`); before 0/5. This is the round's learning claim and its
  sourced claim.

## Gate

### Source openings

The L1 opened each Render Docs page with one public GET (HTTP 200,
2026-10-22T15:41:23Z–15:41:29Z) through `.ufo/waves/round-31/fetch_sources.py`
(sha256 `bc66ceb0…42c9`, named in every receipt). Received bodies, visible
text (HTML minus script, style and comments, tags removed, entities decoded,
whitespace collapsed) and sha256 receipts are in `.ufo/waves/round-31/sources/`.
Wave-1 seat `ReopenSources` re-opened all five at 15:55:44Z–15:55:47Z: the
bodies differ only in per-request trace values and build asset ids, and the
visible text is byte-identical to the retained text for all five
(`.ufo/waves/round-31/w1/ReopenSources.md`). Quotes below are exact
substrings of the retained text after whitespace collapse, spacing included
(the text rule leaves a space before some punctuation where an inline tag
stood).

- S057 — https://render.com/docs/blueprint-spec — accessed 2026-10-22, HTTP 200 — mined: the Blueprint file's location and fields, Docker fields relative to the repository root, the health check path, and that secrets declared with sync: false are asked for once and then ignored; quote “When you update an existing Blueprint, Render ignores any environment variables with sync: false .”
- S058 — https://render.com/docs/web-services — accessed 2026-10-22, HTTP 200 — mined: a Render web service deploys on each push, must bind host 0.0.0.0 and is expected on port 10000 by default; quote “Your web service must bind to a port on host 0.0.0.0 to receive HTTP requests from the public internet.”
- S059 — https://render.com/docs/docker — accessed 2026-10-22, HTTP 200 — mined: Render builds the image from the repository Dockerfile, turns service variables into build arguments, filters the context with .dockerignore and copies secret files into it; quote “Render copies your service's secret files into the root of your build context.”
- S060 — https://render.com/docs/health-checks — accessed 2026-10-22, HTTP 200 — mined: HTTP check success, deploy acceptance and cancel, routing stop and restart times, and the Host header of checks; quote “If this condition is not met within 15 minutes, Render cancels the deploy and continues routing traffic to your service's existing instances.”
- S061 — https://render.com/docs/configure-other-dns — accessed 2026-10-22, HTTP 200 — mined (round-30 routed defect 4, not a C2 id): root-domain records for other DNS providers, ANAME or ALIAS first and an A record otherwise; quote “A records point to IP addresses, and you can use 216.24.57.1 to point your root domain to Render's load balancer IP.”

### Screened candidates

None this round. The wave-1 seat assigned to screen non-primary Render
web-service material (`ScreenWebServiceCandidates`, scribe) died at spawn
(`.ufo/waves/round-31/w1/dead-seats.json`), and the L1 did not open
third-party pages in its place. The discernment evidence of this round is the
S053/S054 resolution below and the wave-1 attacks on the C2 counter.

### Registry changes (old → new)

- S057, S058, S059, S060: no row → new rows, tier A, status `mined`, used-by `corpus/knowledge/render-web-services.md`.
- S061: no row → new row, tier A, status `mined`, used-by `corpus/knowledge/render-static-sites.md` (its round-31 corrections section).
- S053: status `rejected` → `rejected` (unchanged); recheck and used-by unchanged. Its flip condition is met: S061 names ANAME and ALIAS records for a root domain, so the tutorial's ALIAS step matches a Render primary. By the row's own flip wording the tutorial "then still adds nothing beyond S050 and S052", and S061 now carries the record types itself, so the row stays rejected. Resolution note appended below the registry in `corpus/SOURCES.md`.
- S054: status `rejected` → `rejected` (unchanged); recheck and used-by unchanged. Its flip condition is met: S061 states the apex address 216.24.57.1, matching the post. The address now enters the corpus from the Render primary S061, so the registrar post is not needed and stays rejected. Resolution note appended below the registry.
- S056 (sibling tameshi MTE ledger shape): unchanged, `queued`. Wave-1 connector `ConnectSiblingOverlap` found the pin still matches (`b173e3e5…0fac`); no round-31 output cites it.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| repair-claim wider than its guards | Round-30 commit `f80bd8f` was described as making the runner's fixture setup safe, but the closure found five gaps it left (`corpus/lessons/round-30-verifier-spotcheck.md:145-170`, N1–N6); at `f1ffb81` the round-31 counter showed each harm: a planted script ran, two victim repositories gained commits, a FIFO hung the runner, a symlinked case vanished (`.ufo/waves/round-31/verification/c1-before-f1ffb81.json`). | none: no criterion asked that a containment repair be backed by a probe per hostile shape. | Each refusal now has a hostile spec and a selftest (`scripts/citing_set_hostile_selftest.py`) that runs the shape against the runner and checks for harm; it was shown able to fail: against the base runner it exits 1 with 5/5 specs failing (`.ufo/waves/round-31/verification/hostile-selftest-base-runner.json`). New QUALITY criterion (round-31 section). |
| closure command that cannot pass as written | Round-30 C2 declared `git diff --quiet 4580c78 <commit> -- .ufo/waves/round-30/sources/ …`, which exits 1 because `sources/screened/` was added later (`round-30-verifier-spotcheck.md:101-106`). | `corpus/QUALITY.md` had no rule that a declared command be run once before declaring it. | The round-31 declaration names exact files and keeps screened material outside them; the L1 ran the declared command with both revisions equal to the declaration commit before wave 1 (wave-1 `CriticRoutedDispositions` re-ran it: exit 0). Shown able to fail: the same command with `.ufo/waves/round-31/sources/` as a directory and a file added under it exits 1 (`.ufo/waves/round-31/verification/closure-command-check.txt`). |
| partial reports not marked | Round 30 wave 2 committed 20 reports for 15 returned seats; nothing said which 5 were partial (`round-30-verifier-spotcheck.md:176-187`). | none. | Wave-1 scout `ScoutR30PartialReports` classified all 20 from the seat transcripts (15 complete, 5 partial); the list is committed as `.ufo/waves/round-30/w2/partial-reports.json`. This round records every seat's end state (returned, dead at spawn, refused, cancelled) in `.ufo/waves/round-31/<wave>/seat-status.json`, and a seat that stops early starts its report with `PARTIAL:` (wave contexts). |
| dead route not planned for | Wave 1 put every build item (3 executors, 13 scribes) and both mutation-testers on roles whose route was announced as degraded; all 18 died at spawn, 55% of the wave (`.ufo/waves/round-31/w1/dead-seats.json`). | the session route notice warned of it; no lane criterion turned the notice into a plan. | The L1 did the build work itself and sized wave 2 on reviewer, critic and scout roles only. A seat's route is decided by its role, so a round under a degraded-route notice plans builds that it can do itself. Shown able to fail: wave 2 dead-seat count is recorded in its `seat-status.json`. |
| doc claim wider than its probe | The runner docstring (`c88b97e:scripts/citing_set_selftest.py:77-78`) and SKILL said a symlinked case is "never a silent skip"; a dot-named symlink was still skipped (wave-2 `CriticSymlinkCases`, `CriticC1Wording`), and spec P5 used one name shape only. | the round-31 QUALITY criterion "one hostile probe per shape" passed: it asks for a spec per shape, not per name class the runner filters on. | Runner filter repaired; P5 gained `.h5b`; QUALITY "Round-31 wave-2 corrections" adds the per-name-class check. Shown able to fail: the extended P5 fails against the `fde133a` runner (`verification/a2-fixes/hostile-selftest-fde133a-runner.json`, exit 1, P5 false). |
| inference mark on a stated fact | `render-web-services.md:22` marked the PORT mechanism `[INFERENCE]` "not stated from a source here"; the retained S058 text states it (“The default value of PORT is 10000 for all Render web services.”), found by wave-2 `CriticLearningClaimAfter`, `ReviewEntryWebDocker`, `CriticEntryInferences`. Line 61's secret-file inference was contradicted by S059 the same way. | none: the C2 counters check quotes, never `[INFERENCE]` marks; QUALITY criterion 4 checked unmarked words only. | Appended "Round-31 wave-2 corrections" to the entry; QUALITY criterion 4 extended to wrongly placed marks. Shown able to fail: `grep -c 'PORT is 10000' .ufo/waves/round-31/sources/S058.txt` prints 1, so the mark at line 22 fails the extended check; the same grep on S059.txt prints 0. |
| attempt lost with an unlanded placeholder report | Attempt 1 died in an omp restart at 17:26Z (`.ufo/watchdog.log` `lane-dead-no-report kake round=31`) leaving an untracked fleet report with four placeholders (LANE_TIP, WAVE2_COMMITS, ROUND_SHAPE, MISROOT) and two untracked lane paths (`census-after.txt`, `w2/swarm-registry.json`). | none: no step checked a report for placeholder tokens before landing. | Before `fleet-commit.sh` the L1 runs `grep -cE 'LANE_TIP\|WAVE2_COMMITS\|ROUND_SHAPE\|MISROOT' <report>` and lands only on 0. Shown able to fail: on the attempt-1 draft it prints 4. |
| selftest trusts the reported names | Wave-2 `ReviewHostileSelftestCode` F1: a runner that refuses every case named `h*` without running it passed the `c88b97e` hostile selftest 5/5 and the frozen C1 counter 5/5 (sandbox rev `72c9bae1`). | none: the selftest checked harm and names, never that a benign case with a hostile-like name still passes. | `h0-control` benign copy in every spec run must pass. Shown able to fail: the name sham passes the `c88b97e` selftest (exit 0) and fails the repaired one (exit 1), `verification/a2-fixes/hostile-selftest-*-name-sham.json`. The C1 counter is frozen and keeps this hole; named in SKILL. |

## Carried open (attempt 2)

Named so the next round does not drop them (wave-2 `CriticOpenItemsCarried`):
the round-27 IDENTITY-PATHS, RETENTION-FRAGMENT, RETENTION-TRUST-BOUNDARY and
C1-UNIT-OVERRIDE families; the socket `document_unreadable` label; 12 of 25
reason codes without a fixture; deep corpus and `O_NOCTTY` guarded by round
counters only; the four round-30 strict-checker holes; runner mutants m2, m4,
m5; a setup `fifo` on `.gitattributes` or `.gitignore` blocking `git add`;
gate Git calls with no timeout and a Git child that may outlive the gate
[INFERENCE]; the Git pins not probed by any spec (`CriticC1Wording`); the
advisory, unverified bare-repository route from the held
`KakeR31.CriticSandboxThreatModel` seat.
