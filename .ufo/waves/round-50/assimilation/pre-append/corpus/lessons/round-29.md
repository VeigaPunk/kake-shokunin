# Round 29 — project-site base paths: sourced knowledge and an offline audit

## Claims

Declared before implementation in `SCORECARD.md` section "Round 29 — declared
claims" (commit `d18bbf3055f33a992fc9adc4b757172554ec9981`), with declaration
notes added before any after-measurement at `9e541a1d138158cd957c0e7b1a32050478c02dd0`.

- **C1, freshness, frontier.** Project-site base paths enter held knowledge as
  `corpus/knowledge/pages-base-path.md`, grounded in S040–S043 opened this
  round. Counter `.ufo/waves/round-29/c1_quote_truth.py`; before 0/4 at
  `fe1805cf`, declared after 4/4. It checks quote truth against retained
  source text (round-28 routed defect 3), not only quote shape.
- **C2, operability, capability.** `scripts/base_path_audit.py` audits built
  HTML of a project site against its declared base path. Counter
  `.ufo/waves/round-29/c2_matrix_count.py`; before 0/30 at `fe1805cf`,
  declared after 30/30 with all three constant gates rejected. It compares
  reason codes, not only ids (round-28 routed defect 3).

This round deliberately leaves the citing-set gate alone: rounds 27 and 28
both worked it, and a third round on that surface trips the session drift
sentinel.

## Gate

### Source openings

The L1 opened each primary page with one public GET (HTTP 200,
2026-10-22T10:29:37Z) through `.ufo/waves/round-29/fetch_sources.py`.
Received bodies, visible text (HTML minus script, style and comments, tags
removed, entities decoded, whitespace collapsed) and sha256 receipts are in
`.ufo/waves/round-29/sources/`. Wave-1 seat `ReviewSourcesReopen` re-opened all
four at 10:33:42Z: bodies and texts byte-identical to the receipts. Each quote
below is an exact substring of the retained text.

- S040 — https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages (redirects to …/what-is-github-pages) — accessed 2026-10-22, section Types of GitHub Pages sites, Default site location row: “Default site location http(s):/ / <owner>.github.io http(s):/ / <owner>.github.io/ <repositoryname>”
- S041 — https://jekyllrb.com/docs/github-pages/ — accessed 2026-10-22, section Project Pages: “will become available under a subpath of your user pages subdomain, such as username.github.io/project (unless a custom domain is specified)”
- S042 — https://jekyllrb.com/docs/liquid/filters/ — accessed 2026-10-22, Liquid Filters table, Relative URL row (#relative-url): “Prepend baseurl config value to the input to convert a URL path into a relative URL.”
- S043 — https://vite.dev/guide/static-deploy.html — accessed 2026-10-22, section GitHub Pages, Update Vite Config: “If you are deploying to https://<USERNAME>.github.io/<REPO>/ (eg. your repository is at https://github.com/<USERNAME>/<REPO> ), then set base to '/<REPO>/' .”

The S040 table cell keeps the spacing that tag removal leaves (`http(s):/ /`);
the live table reads `http(s)://<owner>.github.io/<repositoryname>`.
The S043 quote has the same artifact (`<REPO> ),` and `'/<REPO>/' .` where
the page has `</code>),` and `</code>.`). The receipts' `textRule` says tags
are removed; `fetch_sources.py` actually replaces each tag with one space
before collapsing whitespace, and the retained texts re-derive exactly under
that rule (wave-2 `GateQuotesTruth`, `RerunC1Counter`).

### Screened candidates (round-28 routed defect 4)

Wave-1 seat `ScreenRejectCandidates` ran an ordinary web search and requested
six secondary or community pages once each (10:34:12Z–10:35:40Z). Bodies, text
and receipts are in `.ufo/waves/round-29/sources/screened/` (C1–C6). Each quote
is an exact substring of that retained text.

- S044 (C1) — https://mademistakes.com/mastering-jekyll/site-url-baseurl/ — accessed 2026-10-22, HTTP 200 — **rejected**: stale version claim and raw baseurl concatenation advice; quote “GitHub Pages does not use the latest version of Jekyll to build sites. It is currently locked at 3.9.0” (S016 lists Jekyll 3.10.0).
- S045 (C3) — https://github.com/jekyll/jekyll/issues/332 — accessed 2026-10-22, HTTP 200 — **rejected**: the issue body uses a `user-name.github.com` host that no current primary source uses (S040 lists `<owner>.github.io`) and a `base-url` key; quote “If you're not using a CNAME and hosting your Project Page on GitHub Pages it's served out of a "project-name" subfolder”, followed in the issue by “http://user-name.github.com/project-name”.
- S046 (C5) — https://talk.jekyllrb.com/t/relative-url-and-baseurl/2051 — accessed 2026-10-22, HTTP 200 — **rejected**: scoped to GitLab Pages, Netlify and localhost, 2018–2020, and its durable point is already in S041/S042; quote “relative_url ensures proper links by: ensuring the url to have a single leading slash always”.
- S047 (C4) — https://michaelcurrin.github.io/dev-cheatsheets/cheatsheets/jekyll/templating/links.html — accessed 2026-10-22, HTTP 200 — queued, tier C: “Use the relative_url filter to ensure you get a GitHub Pages project prefix added.”
- S048 (C6) — https://gohugo.io/host-and-deploy/deploy-to-github-pages/ — accessed 2026-10-22, HTTP 200 — queued: “Project sites are connected to a specific project hosted on GitHub.”
- Not opened (C2) — https://stackoverflow.com/questions/30209076/ returned HTTP 403 with a bot-challenge page. It was not opened by any other means and has no row. Its receipt in `screened/receipts.json` carries `"opened": true` because the seat's script set that field for every request; read it as "requested", since the body is the 403 challenge page.

### Registry changes (old → new)

- S040–S043: no row → new rows, tier A, status `mined`, opened `2026-10-22`,
  recheck `90d`, used-by `corpus/knowledge/pages-base-path.md,
  corpus/lessons/round-29.md`.
- S044–S046: no row → new rows, tier C, status `rejected`, teaches starting
  `REJECTED:` with a flip condition.
- S047: no row → tier C, `queued`. S048: no row → `queued`; the screening seat
  drafted tier C, and the L1 set tier A because the row's stated scope is
  Hugo's own recipe and the page is Hugo's official documentation.
- Wave-2 corrections to rows added this round (old teaches cells kept in
  `.ufo/waves/round-29/verification/reject-rows-old-teaches.json`): S044 now
  names its served config keys `website`/`basewebsite` and a checkable flip
  (`AttackRejectS044`); S045 says "a host no current primary source uses"
  instead of "retired host" and names the 2013 maintainer reply
  (`AttackRejectS045`); S046 drops two reasons the thread does not support
  (pre-4.0 advice, SCSS advice), adds ijv to the anchor, and gets a flip not
  already met (`AttackRejectS046`). Status stays `rejected` for all three.
- No pre-existing row's status, recheck or used-by cell changed. One Paths
  line (Project-site base paths) and one Search log paragraph (Round 29) were
  appended.

## Mistakes

Drafted by wave-1 seat `DraftLessonMistakes` (`.ufo/waves/round-29/w1/DraftLessonMistakes.md`).
Each fix was shown able to fail: the round-29 C1 counter drops to 3/4 when one
letter of a Gate quote changes (sandbox commit `609e6777` in the wave-1 seat
clone, not in the lane; reproduced by wave-2 seats `ReopenS042` and
`MistakesRowsCheck`), while the round-28 C2 counter still scored 4/4 on the
same kind of change (sandbox commit `1f9ffdc`, likewise reproduced by
`MistakesRowsCheck`); the reject-path witness
`.ufo/waves/round-29/verification/reject-path/reject_path_check.py` passes on
the landed rows and fails on each named mutation (for example
`--registry mut/M2-no-flip.md` exits 1).

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| vacuous | The round-28 C2 counter graded quote shape, not quote truth: `.ufo/waves/round-28/c2_source_count.py:126-127` counted one curly-quoted span of 1–25 words per Gate line and never opened a source, so a quote that is worded correctly but is not in the source scored the same as a true one. `corpus/lessons/round-28.md:107-110` and `corpus/lessons/round-28-verifier-spotcheck.md:225-227` (routed defect 3) record the defect; quote truth was checked outside the counter by `residual/ReviewGateQuotes.md`. | none — the round-28 `QUALITY.md` section "Counters and field evidence — round 28" (`corpus/QUALITY.md:298-332`) requires a counter to reject a constant and to keep its scope named, but no criterion required a quote to be found in retained text, so a shape-only check passed review. | The round-29 C1 counter `.ufo/waves/round-29/c1_quote_truth.py` checks check `d_quote_in_retained_text`: the Gate quote must be an exact substring of the retained visible text `.ufo/waves/round-29/sources/S0NN.txt`, whose sha256 must equal the committed receipt (`receipts.json`) before the comparison. Shown able to fail: at the landed commit `f8675e5` the counter scores 4/4, exit 0; at the sandbox commit `609e6777fe3836ec813f499186248ff1992c6e99`, which changes exactly one letter of the S042 Gate quote and nothing else, it scores 3/4, exit 1, with `d_quote_in_retained_text` false on S042 alone. The round-28 counter cannot see that state: at the sandbox commit `1f9ffdcffcad9fa78a41aad60c00b6576d0dcfbc`, which changes exactly one letter of the round-28 S036 Gate quote, `.ufo/waves/round-28/c2_source_count.py` still scores 4/4, exit 0, although the flipped quote is not an exact substring of the retained `.ufo/waves/round-28/sources/S036.txt`. |
| vacuous | The round-28 source gate screened only the four sources it then admitted and rejected none, so no outside reviewer could draw a reject sample from the gate itself: `corpus/SOURCES.md` search log for round 28 records "Identified 4, screened 4, included 4 (S036–S039, scoped tier A), excluded 0", and `corpus/lessons/round-28-verifier-spotcheck.md:228-231` (routed defect 4) records that the reject sample had to come from outside the source gate. | none — `corpus/QUALITY.md` had no criterion requiring a screened source step to produce a checkable rejection, and the round-28 `## Gate` section had no rejected line to point at. | The round-29 lesson `## Gate` section carries a "Screened candidates (round-28 routed defect 4)" block with three rejected candidates (S044, S045, S046) and two queued ones (S047, S048), each with a quote, a one-line reason and a flip condition, and the registry rows S044–S046 read `REJECTED: … ; flip: …` with status `rejected`. Shown able to fail: the check `reject_path_check.py` reads the committed registry, lesson and entry and fails when a rejected candidate's quote is not an exact substring of that candidate's own retained text (`.ufo/waves/round-29/sources/screened/C*.txt`), when the teaches cell loses its `flip:` clause, when the row's status is not `rejected`, when a cited primary id is not tier A mined with retained text, when a rejected candidate URL appears in the entry body or in an admitting Gate line, or when no candidate is rejected at all. It scores 5/5, exit 0 on the landed bytes at `f8675e5`, and exit 1 on each of five sandbox mutations: one letter changed in the S044 quote, the S044 flip clause removed, the S044 status changed to `mined`, all three rejections relabelled as queued, and the S044 URL appended to the entry body. |
| misroot (landing) | Wave-2 seat `FieldsAndCounts` wrote its report once through a relative path, which landed at the fleet root as `/home/vgpnk/Projects/shokunin/.ufo/waves/round-29/w2/FieldsAndCounts.md` (`.ufo/waves/round-29/w2/FieldsAndCounts.md`, "Process incident"). | the wave context rule "every `Report:` trailer path is relative to the lane" (stated, not enforced) | The seat removed the fleet copy and the `w2` directory its write created and kept the lane copy; the L1's own sweep (`git -C /home/vgpnk/Projects/shokunin status --porcelain`, before the report) found no round-29 kake file at the fleet root. Not shown able to fail beyond that sweep. |

| absent-path annotation (r43 re-census 2026-10-23) | `/home/vgpnk/Projects/shokunin/.ufo/waves/round-29/w2/FieldsAndCounts.md` is absent — the fleet-root copy was removed by the round-29 misroot sweep; the byte-exact lane copy survives at `.ufo/waves/round-29/w2/FieldsAndCounts.md`. Historical incident record, not an executable path. | freshness sweep §paths gate (unannotated miss + newMissing) | This annotation row: the citation above carries its own absence wording within ±2 lines, and the token is entered in `corpus/knowledge/freshness-pins.json` `pathsMissSet` in round 43. |

## Not repaired this round (routed defects 1 and 2)

Round 28 routed two defects on the citing-set surface. Round 29 repaired
neither and says so plainly.

Routed defect 1 — committed fixtures for the round-28 reason codes — stays
open. All 29 committed fixtures under `scripts/fixtures/citing-set/` still
assert only an exit code and a finding-id list; `grep -rl reason
scripts/fixtures/citing-set` returns 0 files, and in code and fixtures the
eight round-28 reason codes exist only in `scripts/citing_set.py`. The regression coverage for
those codes still lives only in the round-scoped counter
`.ufo/waves/round-28/c1_interface_count.py`, which is not a committed
fixture and is not run by the gate's own self-test.

Routed defect 2 — the round-27 failure families outside the declared C1 set
— stays open on the terms round 28 recorded: the `JSON-PROTOCOL`
duplicate-key and nonfinite cases; `S01`-style ids that measure clean;
repeated CLI options resolved by last value wins; the deep-corpus traceback;
and the missing `O_NOCTTY`.

Why this round did not repair them: the session drift sentinel for "same
axis+surface claim or same routed defect class in a lane 3 rounds running"
(`/home/vgpnk/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md:173`)
requires the lane's next round to work a different frontier area. The
citing-set surface was worked in round 27 (the round-27 C1 citing-set
completeness claim, its counter and its fixture tree) and again in round 28
(the C1 interface repair of `scripts/citing_set.py`); repairing it a third
round running is the case that sentinel names. Round 29 therefore took a
different frontier area, project-site base paths for GitHub Pages, and
carried both defects forward as named debt.

Consequence for the record: the first half of routed defect 3, that the
round-28 C1 counter checks finding ids and not reason codes, is unchanged for
the citing-set surface; this round's own C2 counter does compare reason codes. The round-29
C1 counter measures the new base-path source rows S040 to S043, not the
citing-set surface. Nothing in this round changes the citing-set gate, its
fixture set or its counters. The next round that works the citing-set
surface inherits both defects, and the round-29 criteria in `corpus/QUALITY.md` apply to it.

## Wave-2 falsification and the repairs it caused

Wave 2 (39 attack seats, `.ufo/waves/round-29/w2/`) attacked commit
`7697990`. Both counters re-derived their values (C1 4/4, C2 30/30; 0/4 and
0/30 at `fe1805cf`; counter and matrix blobs unchanged since `d18bbf3`). The
real-input run reproduced byte for byte. Repairs landed after `7697990`:

- Entry: six bullets were overstated or misattributed (`AttackEntryJekyll`,
  `AttackEntryVite`, `AttackEntryBreaks`, `AttackEntryCustomDomain`,
  `AttackEntrySiteKinds`, `ReopenS041`): `absolute_url` was credited to S041,
  "Pages does not run Vite" overreached S043, the `../` and root-relative
  claims had no source, and the custom-domain and sibling-link wording was
  too broad. Each is now narrowed, re-sourced or marked `[INFERENCE]`.
- Registry: S044–S046 reasons corrected (above); S040 anchor widened and its
  teaches consequence marked as lane inference (`ReopenS040`); S042 anchor
  label corrected (`ReopenS042`, `GateQuotesTruth`).
- SKILL table: an S043 citation removed from the base-element row, the Vite
  preview claim withdrawn, the `--baseurl=""` command corrected, a gate
  registry row added (`SkillTableCheck`, `CalibrationScorecard`).
- Tool: help text states the same-site rule (`CrossSchemeDecision`); a
  same-scheme reference without `//` (`https:/../x`) is now resolved relative
  to the base as WHATWG does (`WhatwgDiffLandedTool`); remaining known misses
  and tokenizer differences are listed in the docstring (`ToolSourceGaming`,
  `HtmlParsingEdges`, `SrcsetLandedTool`).
- Selftest: 15 regression fixtures `X01`–`X15` were added for families the
  frozen matrix cannot see (JSON and CLI refusals, cross-scheme, template,
  audio and embed, port and host case, backslash and encoded dots, traversal
  with the target present, the `resolved` field, the counts, same-scheme
  single slash); the runner now compares `page` and `resolved` when a fixture
  names them, checks the counts when given, and refuses to pass with fewer
  than 45 default fixtures (`JsonFamilies`, `MutateToolVsCounter`,
  `MutateToolVsSelftest`, `SelftestFixtureDrift`). The frozen 30-case matrix
  and the C2 counter are unchanged.
- Reject-path witness: it now fails when no screened candidate is rejected
  (`MistakesRowsCheck`).
- QUALITY: wrong PROTOCOL line range, a misattributed observation and a
  dangling pointer corrected; the first criterion's current failure on the
  citing-set fixtures is stated (`QualityCriteriaCheck`).

Open after wave 2 (not repaired): the C2 counter does not compare `id`,
`page`, `resolved` or the counts, and passes the usage case on exit code
alone; the C1 counter checks presence of a quote, not that the entry's claim
follows from it, and binds the opened date; the tool misses `http:host/path`
on an https page, percent-encoded or non-ASCII hosts and an unparseable base;
srcset density grammar is narrower than the HTML parser; html.parser
tokenizer differences listed in the tool docstring.

Seat process notes: `NoHarmExistingGates` ran `freshness-sweep.mjs` without a
section flag once at base and once at tip, which sends GET requests to pinned
owned sites and `git ls-remote` to pinned repositories; that was outside its
bounds, it did not repeat it, and its live results are treated as unverified.
`HtmlParsingEdges` used a locally installed Chromium in headless mode against
local files only (no remote resources, proxy blackholed) as a parsing oracle,
and installed parse5 8.0.1 with npm in its sandbox. `PerfPathological` built
GNU time 1.9 from https://ftp.gnu.org/gnu/time/time-1.9.tar.gz into
`~/.local/bin/time`.
