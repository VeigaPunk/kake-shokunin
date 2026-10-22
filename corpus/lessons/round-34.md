# Round 34 — link-preview metadata: an offline Open Graph audit and a sourced entry

## Claims

Declared before implementation in `SCORECARD.md` section "Round 34 — declared
claims" (commit `d08d8de26c9a4290c44282b0eee2b860e8ea4ecc`, which also carries
the frozen matrix, both counters and the retained sources). Base
`1e54c89515b0b1f7c9d7d10e6232d15e43320713`. Neither claim touches the
citing-set gate: rounds 31 to 33 aimed their operability claim at it, and the
hyaku goal file's drift rule (three rounds on one axis and surface force a
different frontier area; `.scratch/goal-20261022-hyaku-12h.md`, cited by
wave-1 `CriticFrontierNovelty` finding 6) moves this round to a new area.

- C1 (operability, capability): `scripts/link_preview_audit.py`, an offline
  Open Graph audit over a version-1 manifest of local HTML pages. Counter
  `.ufo/waves/round-34/c1_matrix_count.py` (28 frozen cases, four constant
  gates): 0/28 at base, 28/28 with all constants rejected at `5613071`.
- C2 (freshness, sourced learning claim on S067–S070):
  `corpus/knowledge/link-preview-metadata.md` plus a ds4cc Open Graph census
  line equal to the counter's recount. Counter
  `.ufo/waves/round-34/c2_source_census.py`: met 0/5 at base.

Both counters are necessary, not sufficient: see `## Mistakes` row 4.

## Gate

### Source openings

Opened with `.ufo/waves/round-34/fetch_sources.py` (one public GET each;
receipts and retained text in `.ufo/waves/round-34/sources/`). S067–S072 were
opened at 20:57Z before the declaration; S073–S077 at 21:08–21:09Z after
wave-1 `ScoutMoreSourceLeads` screened them.

- S067 — https://ogp.me/ — accessed 2026-10-22T20:57:39Z, HTTP 200 — admit, tier A, kind spec, status mined: the four required Open Graph properties; quote “The four required properties for every page are” (Basic Metadata section; 8 words; the list continues with og:title, og:type, og:image, og:url and the og:url definition).
- S068 — https://developers.facebook.com/docs/sharing/webmasters/ (redirects to …/documentation/sharing/webmasters) — accessed 2026-10-22T20:57:39Z, HTTP 200 — admit, tier A, kind docs, status mined: the Facebook crawler's use of Open Graph tags and its heuristic fallback; quote “Without these Open Graph tags, the Facebook Crawler uses internal heuristics to make a best guess about the title, description, and preview image” (Open Graph Markup section; 23 words).
- S069 — https://api.slack.com/robots — accessed 2026-10-22T20:57:41Z, HTTP 200 — admit, tier A, kind docs, status mined: Slack's link robot extracts oEmbed and Twitter Card / Open Graph tags; quote “Specifically, we are looking for oEmbed and Twitter Card / Open Graph tags.” (Meet the Robots, Slackbot-LinkExpanding entry; 13 words).
- S070 — https://docs.joinmastodon.org/entities/PreviewCard/ — accessed 2026-10-22T20:57:41Z, HTTP 200 — admit, tier A, kind docs, status mined: a PreviewCard is generated from a URL's OpenGraph tags; quote “Represents a rich preview card that is generated using OpenGraph tags from a URL.” (PreviewCard entity opening definition; 14 words).
- S071 — https://developer.x.com/en/docs/x-for-websites/cards/overview/markup (final https://docs.x.com/overview) — accessed 2026-10-22T20:57:41Z, HTTP 200 — reject, tier C, kind docs, status rejected: the URL now serves the generic documentation index with no cards markup; quote “Fetch the complete documentation index at: /llms.txt Use this file to discover all available pages” (page head, documentation index; 15 words).
- S072 — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview — accessed 2026-10-22T20:57:42Z, HTTP 200 — reject, tier A for the repository setting but out of scope, kind docs, status rejected: a repository Settings > Social preview image upload, not page metadata; quote “You can customize the image displayed on social media platforms when someone links to your repository.” (page opening; 16 words).
- S073 — https://docs.discord.com/developers/link-previews/overview — accessed 2026-10-22T21:08:44Z, HTTP 200 — admit, tier A, kind docs, status mined (opened after wave-1 ScoutMoreSourceLeads named it; not one of the declared C2 ids, so it counts toward no claim): Discord reads only server-sent HTML and takes a tag's key from name before property; quote “No code is executed, so tags added by a client-side script after load are never seen.” (Requirements list; 16 words).
- S074 — https://core.telegram.org/bots/api — accessed 2026-10-22T21:08:44Z, HTTP 200 — reject, tier A for the Bot API but out of scope, kind docs, status rejected: the LinkPreviewOptions object holds only a bot's switches (disable, URL, media size, position) and the 73,876-word page has no og: occurrence, so it grounds no publisher-side tag rule; quote “Options used for link preview generation for the message, if it is a text message and link preview options were changed” (link_preview_options field; 21 words).
- S075 — https://www.linkedin.com/post-inspector/ — accessed 2026-10-22T21:09:47Z, HTTP 200, 3,577-byte body — reject, tier C, kind tool, status rejected: a JavaScript shell whose whole visible text is its title, so no preview rule is obtainable by ordinary means (no browser, no login); quote “Post Inspector” (entire visible text; 2 words).
- S076 — https://oembed.com/ — accessed 2026-10-22T21:09:47Z, HTTP 200 — queue, tier A, kind spec, status queued: oEmbed is a separate preview mechanism that S069 names beside Open Graph; no kake entry needs it yet; quote “oEmbed is a format for allowing an embedded representation of a URL on third party sites.” (opening; 16 words).
- S077 — https://github.com/jekyll/jekyll-seo-tag — accessed 2026-10-22T21:09:47Z, HTTP 200 — queue, tier B, kind code, status queued: the Jekyll SEO plugin emits Open Graph title, description, site title and URL; ds4cc's audited pages are hand-authored, so no lane property is shown to use it; quote “Open Graph title, description, site title, and URL (for Facebook, LinkedIn, etc.)” (README What it does list; 12 words).

Row changes logged old→new (all new rows; no existing row's status, recheck
or used-by cell changed):
- S067, S068, S069, S070, S073: `—` → `mined`, opened `2026-10-22`, recheck
  `90d`, used-by `corpus/knowledge/link-preview-metadata.md`.
- S071, S072, S074, S075: `—` → `rejected`, opened `2026-10-22`, recheck
  `90d`, used-by `—`.
- S076, S077: `—` → `queued`, opened `2026-10-22`, recheck `90d`, used-by `—`.

Screened and not given a row (opened by wave-1 seats only, recorded in their
reports): two LinkedIn help URLs (404), Discord message and channel resource
pages (they only link S073), `raw.githubusercontent.com` README paths of
jekyll-seo-tag (404), the docs.x.com cards paths (404; S071's rejection is
confirmed by `ScoutXCardsLocation`, which found no current cards markup page in
the docs.x.com index, sitemap or full text).

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| committed text cited evidence that existed only in sandbox scratch, so the pointer does not resolve from committed bytes | `.ufo/waves/round-33/verification/c1-strict-at-critic-489714b.json` names commit `489714be`, which lived only in `/fast/scratch/hyaku/kake-r33/w1/CriticC1RepairScope/clone` (lane tree lacks the object: `w2/RerunC1Strict.md:24-29`); the option-table `patch.diff` cited by `w2/CriticOptionTableRejection.md` was likewise sandbox-only | routed defect 2 of `corpus/lessons/round-33-verifier-spotcheck.md`; found in-round by `w2/RerunC1Strict.md:24` | Retained in the lane: `.ufo/waves/round-34/retained/r33-c1-counterexample-489714be.bundle` (sha256 `6ff6c403c4df5b2a…77c00`), `r33-option-table-dedup-patch.diff` (`28fd9adf5f30…7d6e`), `r33-option-table-alt-patch.diff` (`daeaa738525e…ce6e`). Resolution check, shown able to fail: into a clone at `a2fe31b2`, `git fetch <bundle> 'refs/tags/*:refs/tags/*'` exits 0 and `git cat-file -p 489714be` shows `parent bc6c4a8d…` with a 2-file diff (raise line + `reason_contains`); the same fetch against a nonexistent path exits 128. Limit: the bundle is thin (header `-bc6c4a8d…`), so `git clone --bare <bundle>` alone exits 128 `Repository lacks these prerequisite commits` — it resolves only where `bc6c4a8` is already present |
| a Gate that records admits only, so no reject can be sampled from it | `corpus/lessons/round-33.md` at `a2fe31b2` `## Gate` holds two rows (`:31` S065, `:32` S066), both decision `admit`; `grep -cE '\| (admit\|reject)'` over the section is 2 and the tally is `2 admit`; the closure had to fall back on a code patch for its admit+reject sample | routed defect 3 of `corpus/lessons/round-33-verifier-spotcheck.md` ("the round-33 `## Gate` records no reject") | `python3 -B .ufo/waves/round-34/criteria/gate_reject_check.py --repo . --rev <commit> --lesson <path>`: exit 1 on `corpus/lessons/round-33.md` at `93359ff` (`verification/criterion-gate-reject-r33-at-93359ff.txt`), exit 0 on `corpus/lessons/round-29.md` (`verification/criterion-gate-reject-r29-at-a2fe31b.txt`); this round's Gate records four rejects (S071, S072, S074, S075). QUALITY "Round-34 criteria" (b). |
| the report cited a run with no receipt | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kake.md:62` states "`93359ff`: 4/4 (run, not committed)"; `.ufo/waves/round-33/verification/` holds receipts only for `5777d5a`, `bc6c4a8`, `b1752a2`, `e490381`, `1cf452e`, `3abfc44` — `ls | grep -c 93359ff` is 0 | routed defect 4 of `corpus/lessons/round-33-verifier-spotcheck.md` | `python3 -B .ufo/waves/round-34/criteria/receipt_presence_check.py --report <md> --repo . --rev <commit> --round <N>`: exit 1 naming `93359ff` on the round-33 report (`verification/criterion-receipt-presence-r33-report.txt`), exit 0 on a copy without that run (wave-1 `ExecReceiptPresenceCheck.md`). QUALITY "Round-34 criteria" (c). |
| a declared counter gives its full score to a control that does none of the claimed work | Wave-1 `CriticDeclarationFit`: sandbox commit `dcef39b5` holds a C1 tool that parses no HTML, keys on the case directory name the C1 counter chooses (`c1_matrix_count.py` materializes each case at `<scratch>/<stem>/<case id>`) and replays the matrix's expected output: 28/28 with all constant gates rejected; also found by `ReviewC1CounterDiff` (stub `83f53357`). Sandbox commit `0cce15f0` (junk rows, census copied from the published receipt, first-six-word quotes) scores C2 5/5. Both retained: `.ufo/waves/round-34/retained/r34-c1-lookup-dcef39b5.bundle`, `r34-c2-hollow-0cce15f0.bundle`; receipts `verification/criterion-lookup-control-c1-dcef39b.txt`, `verification/c2-at-critic-hollow-0cce15f.json`. | QUALITY round-33 criterion 2 (hollow control) should have: the L1 crash-checked both counters at base before freezing but ran no hollow or lookup control against them. | New check `python3 -B .ufo/waves/round-34/criteria/lookup_control_check.py --counter <counter> --repo <repo> --control <rev>`, shown able to fail: exit 1 on the frozen C1 counter with control `dcef39b5` (28 of 28). The frozen counters are not changed (a supplement after a finding would not count); the claims are disclosed as necessary-not-sufficient and the non-author read of the landed tool and entry carries admission. QUALITY "Round-34 criteria" (d). |

Sweep for other round-33 author mistakes: wave-1 `ScribeMistakeMine.md`
(commands and output in that report) also found two candidate rows — wave-1
reports cited before they were committed, and an undercounted network-read
sentence (both corrected by append in round 33). They are recorded there, not
promoted here, because round 33 already corrected each by append.

## Round-33 routed defects — disposition

| # | Item | Disposition |
|---|---|---|
| 1 | C2 counter hollow shapes missing from the carried-open list | Carried by name below ("Carried open — round-33 C2 counter shapes"), with the round-34 counter marked against each shape. `c2_pin_count.py` is not reused as a gate. |
| 2 | Evidence only in sandbox scratch | Retained: `.ufo/waves/round-34/retained/r33-c1-counterexample-489714be.bundle`, `r33-option-table-dedup-patch.diff`, `r33-option-table-alt-patch.diff` (commit `a2fe31b`); wave-1 `ReviewRetainedEvidence`: bundle verifies against the lane, 489714be has parent bc6c4a8 and the described two-line diff, both patch hashes match. Mistake row 1; QUALITY round-34 (a). |
| 3 | Gate recorded no reject | This Gate records four rejects with located reasons; `gate_reject_check.py`; mistake row 2; QUALITY round-34 (b). |
| 4 | Report cited an unreceipted run | `receipt_presence_check.py`; mistake row 3; QUALITY round-34 (c). This round's report cites only committed receipts. |
| 5 | Still open (NUL-byte crash, null codes, freshness-pins re-pin, Git-pin mutants, option tables, round-31 F1–F3) | Carried; see "Carried open" below for what wave 1 learned on the Git-pin mutants and the option-table patch. |

## Carried open — round-33 C2 counter shapes

**Carried open — round-33 C2 counter shapes.** The round-34 C2 counter
(`.ufo/waves/round-34/c2_source_census.py`) inherits six round-33 hollow shapes and regresses three that
round 33 had closed; all sit in the registry/entry layer, not the retained-bytes layer.

- **junk-row** (C34:215-218): a row passes on cell 0, a source-cell substring, `mined`, and the date; the
  round-33 used-by check (C33:126) is gone, and kind/tier/scope/anchor/taught-fact are never read.
- **duplicate-row** (C34:215 `next()`) and **duplicate-heading** (C34:95-96): two matching rows or two
  `## Registry` sections resolve silently instead of failing as they did at C33:73-75,120-123.
- **fence-blind sections** (C34:95-101): a fenced literal `## Registry` opens the window (P3) and a fenced
  `## x` closes it (P2); round 33 failed closed on the duplicate case.
- **escaped-pipe** (C34:216): naive `.split("|")` plus `len(cells) >= 11` (C34:217) means checked indices need
  not be rendered columns; C33:119's `(?<!\\)\|` parity handling is gone (P4).
- **mode-blind bytes** (C34:152): the tree regex captures six mode digits but never compares them, so a
  100755 blob passes; C33:107 required `100644` (P5).
- **anywhere-cite** (C34:208,219): source ids have no required section, only a position after the entry's
  first 8 lines; the intro cite C33 rejected is excluded, but any later mention counts.
- **bigint-crash** (C34:235 over C34:66): an oversized census integer raises ValueError uncaught — no JSON,
  exit 1, the same shape as round-33 N2.
- **self-consistent-pair** (C34:148-173,226-227): the archive is exact against `tree.txt`, whose first line is
  only a string match on the pinned commit, and the retained text is checked against a receipt committed in the
  same revision. This is round 33's full-score-hollow shape (M:5,16) at a new site, so `met=5/5` certifies
  internal consistency, not that anyone read the pages.

Avoided, keep: exact path-set and per-path blob equality (C34:168-173), `errors="replace"` reads
(C34:199-201), whitespace-tolerant heading match (C34:96), word-boundary id cite (C34:219), archive exception
handling (C34:158-166). Source-URL matching remains a substring check (C34:217-218).

Probe evidence: `/fast/scratch/hyaku/kake-r34/w1/ScribeCarriedOpenNames/probe_shapes.py` (exit 0; P1-P7 in
`.ufo/waves/round-34/w1/ScribeCarriedOpenNames.md`). Counter probed at sha256
`ee7461b9e3a33949174591c527ccbf2854ca178c41638f71b5128cbd57e5f892`.

## Carried open

- Git-pin mutants: wave-1 `ExecPinMutantsGateCode` prototyped runner codes
  for gate-run refusals plus a P7 spec; m3f and m3g are killed by the P7
  `reason_code` check, m3d survives (equivalent under the current setup
  vocabulary). The patch stays in the seat's sandbox
  (`/fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/patch.diff`); it is
  citing-set work outside this round's claims and is not landed.
- Duplicated option tables: see wave-1 `ExecOptionTableAltPatch.md`.
- NUL-byte runner crash; `code` null on run-level failure entries;
  `freshness-pins.json` re-pin (three values); round-31 QUALITY F1–F3.
- C1 counter: case identity leaks through the case directory name (mistake
  row 4); non-UTF-8 tool stdout raises in the counter; `page`, `id` and
  `pagesChecked` are not compared (`ReviewC1CounterDiff`). Matrix gaps: no
  case for a non-UTF-8 page, a second canonical link, a protocol-relative
  og:url, or policy findings co-present with an input fault
  (`ReviewC1Matrix`).
- C2 counter (`ReviewC2CounterCode`, sandbox commits in that report): fence
  tracking starts after the entry's 8-line header, so a fence opened there
  hides nothing (D1, 5/5 with cites and census inside a fence); the Registry
  row search is fence-blind (D2); a naive `|` split lets `x\|mined` pass a
  row whose rendered status cell differs (D3); a non-string receipt URL, a
  5000-digit census number and an unparsable canonical href crash with exit 1
  instead of 2 (D4). The landed `9ef758c` entry, rows and lesson use none of
  these shapes (the census line and every cite sit in unfenced body text; no
  row carries an escaped pipe), which the non-author read can confirm.
