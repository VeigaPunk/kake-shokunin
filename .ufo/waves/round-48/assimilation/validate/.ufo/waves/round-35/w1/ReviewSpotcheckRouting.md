# Round 35 W1 — ReviewSpotcheckRouting: how round 35 routes each round-34 routed defect

Method: `corpus/lessons/round-34-verifier-spotcheck.md` "Routed defects" 1-6 read at
`318561e` via `git show` (lane working tree never used as landed evidence). Wave items
read from `.ufo/waves/round-35/w1-spec.json` (wave context). No sealed-path access. No
tools installed. Revision `318561e` = `318561efa67206699fdaf259ffb86e39f2d916a8`.

## Rows

1. **"Declare a target a do-nothing control cannot reach."**
   Artifact: declaration `81d9fd7` (SCORECARD.md:1356 "Round 35 — declared claims"),
   sealed counter `.ufo/waves/round-35/sealed_count.py` (keys sha-pinned, exit 2 if a key
   is visible at the measured revision), controls scored before build at `318561e`: 10
   receipts `verification/control-*.{json,exit}` + 4 bundles `retained/r35-control-*.bundle`.
   Disposition: **fix shown able to fail** — all 10 control runs exit 1 below target
   (SCORECARD:1430 table): C1 base 14/24, lookup `dcef39b5` 7/24, constant 7/24 (<22);
   C2 base/declaration/hollow/junk 0 probes, keyword 3, transcript 8 with `copiedShare`
   0.9951 (<9 probes, >0.25). GAP: the defect's third bullet — "re-run
   `criteria/lookup_control_check.py` against the new counter with both retained
   controls" — is routed to **no wave-1 item**; the spec's only mention of that script is
   `ScribeControlCorrection` reading its misdescribed line 6, not re-running it. The
   criterion also expects `total` in the counter JSON (`.ufo/waves/round-34/criteria/
   lookup_control_check.py` main()) while `sealed_count.py` prints `cases`, so an
   unmodified re-run exits 2. The committed control scores give the same guarantee, but
   the named bullet is unexecuted.

2. **"The lookup control is misdescribed" (keys on content, not the directory name) — "correct by append".**
   Artifacts: wave items `ScribeControlCorrection` (append-only correction paragraphs
   quoting `dcef39b5:scripts/link_preview_audit.py` lines: hashes argv + every relative
   path and file content; one-comment HTML perturbation defeats it, 7/28) and
   `ExecControlDescriptionCheck` (`control_description_check.py`: exit 1 when the
   document paragraph does not quote a whole line of the control and name the line
   number; acceptance demands a failing receipt on `corpus/lessons/round-34.md` mistake
   row 4 at `318561e`). Disposition: **correction by append, drafted + a check shown able
   to fail**. Nothing landed yet: round-34.md:68, `lookup_control_check.py:6` and
   SCORECARD:1256-1258 still say "case directory name" at `318561e`.

3. **"No gate registry row for the link-preview audit" (SKILL.md).**
   Artifact: wave item `ScribeSkillRegistryRow` (drafts the `link-preview-audit |
   gate|probe` row into `w1/ScribeSkillRegistryRow/registry.md`). Disposition: **carried
   → drafted, not landed**. SKILL.md at `318561e` has no registry row (`link-preview`
   hits only :993, :1024, :1031); PROTOCOL conformity still pending integration.

4. **"The C2 census numbers were published by the counter's own declaration receipt."**
   Artifacts: the round-35 C2 counter drops the census condition entirely
   (`sealed_count.py` c2 conditions: entry, size, copied, cites, probes;
   `census-before.txt` is committed pre-build but no condition consumes it); wave item
   `ExecPrebuildLeakCheck` builds `prebuild_leak_check.py` — exit 1 when a pre-build
   receipt publishes a target value; acceptance = receipts showing exit 1 and exit 0.
   Disposition: **design fix (leak channel removed) + criterion check able to fail**;
   the discriminating conditions fire on controls (transcript `copiedShare` 0.9951).

5. **"S074 reason overclaims" ("no og: occurrence").**
   Artifact: wave item `ReviewS074Head` (recount og: metas in S074.html.gz head/body via
   pasted commands; draft a one-paragraph correction note for the SOURCES.md notes area;
   changes no status/recheck/used-by cell). Disposition: **correction by append,
   drafted**; Gate reason and SOURCES.md row unchanged at `318561e`, landing pending.

6. **"Carried, unchanged" bundle.**
   - Fixed this round: first-og:url-only comparison → contract (a) `og_url_multiple`
     (SCORECARD:1380); canonical inside `<template>/<svg>/<math>` → (b) (:1383);
     unreadable page stopping the manifest → (c) `page_unreadable` (:1388). Disposition:
     **fix shown able to fail** — the 24 sealed cases test exactly these; base tool fails
     10/24 (`control-c1-base-tool.json` perCase false: case-01,02,06,11,12,14,15,19,23,24)
     and the disclosed reference patch scored 24/24.
   - Old C2 counter defects D1–D4: **carried by supersession, undocumented** — round-35
     C2 is measured by `sealed_count.py c2`, not `c2_source_census.py` (D1–D4 defined in
     `.ufo/waves/round-34/w1/ReviewC2CounterCode.md`), but no round-35 artifact says the
     old counter is retired.
   - Git-pin mutants (m3d/m3f), option tables, NUL-byte runner crash, freshness-pins
     re-pin, round-31 F1–F3: **carried, no round-35 artifact or wave item** (spec scan:
     zero hits for m3d/m3f/NUL/option-table; the single freshness-pins hit is the
     boilerplate bounds text). This matches the lesson's own "Carried, unchanged" routing.

## Flags

- Only orphaned routed instruction: defect 1 bullet 3 (lookup-criterion re-run) — no
  owner, and the criterion's JSON contract (`total`) does not fit the new counter.
- Defects 2, 3, 5 exist only as sandbox drafts/checks at wave-1 time; lane bytes at
  `318561e` are unchanged for them — landing depends on later-wave integration.
- No defect is wholly without a disposition: 1, 4 and 6(a-c) are fixes with committed
  able-to-fail evidence; 2, 3, 5 are drafted appends/checks; the 6-remainder is carried
  by name per the lesson.

## Commands and verification

`git show/log/diff/ls-tree` (all exit 0) at `318561e`/`81d9fd7`/base `16a6b8b`;
`grep` SKILL.md and SCORECARD (exit 0); `jq` over w1-spec.json and receipts (exit 0);
`cat` of the 10 `control-*.exit` files (all `exit=1`). One wrong-path guess
(`criteria/` at lane root) exited 128; correct path is
`.ufo/waves/round-34/criteria/lookup_control_check.py`. Not verified: control bundle
contents re-run (scores taken from committed receipts + SCORECARD:1430 table); the four
w1 seats' sandbox receipts (not yet written / not mine to run); no counter re-executed.
