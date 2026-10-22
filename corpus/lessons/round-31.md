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
