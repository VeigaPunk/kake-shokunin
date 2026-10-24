# Review — PROVINCE.md and corpus/README.md round-31 sections (overclaim check)

Seat: KakeR31a2.ReviewProvinceReadme (leaf). Axes: operability, freshness.
Attacked: the round-31 sections at PROVINCE.md:111-123 and corpus/README.md:288-296
at fde133a (content unchanged through 92235a0 per diff --stat), against the entry
`corpus/knowledge/render-web-services.md`, the C1/C2 receipts, the registry rows,
and the pinned ds4cc-marketplace render.yaml. Sandbox clone:
/fast/scratch/hyaku/kake-r31/a2-w2/ReviewProvinceReadme/clone @ fde133a. No installs.

## Commands run (all exit 0)

- `git clone -q <lane> <sandbox>/clone && git -C <clone> checkout -q fde133a…` → HEAD fde133a.
- `git -C /home/vgpnk/Projects/ds4cc-marketplace show 1fbdb8ed:render.yaml | sha256sum`
  → 83e0ead9…437920b (sha256 of bytes); `git rev-parse 1fbdb8ed:render.yaml`
  → d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252 — the "blob d17ab7e5" cite in both
  sections is the Git object id and matches. File is 20 lines, keys exactly as the
  entry lists (type, runtime, dockerfilePath, dockerContext, healthCheckPath,
  envVars incl. `sync: false`, no domains/plan/region/autoDeployTrigger).
- `cat` of .ufo/waves/round-31/verification/c1-before-f1ffb81.json,
  c1-after-fde133a.json, c1-a2-at-92235a0.json → before 0/5 (P1 canary ran,
  P4 timed out on the FIFO, P2/P3 victims mutated), after 5/5 with control K1
  holding (45 cases, exit 0) at both revisions; hostile selftest present, exit 0,
  five cases true. Supports the C1 sentence's substance.
- greps for line cites in PROVINCE.md, corpus/README.md, SOURCES.md, runner.

## Findings

### F1 — HIGH (freshness, live vs offline) — PROVINCE.md:118-119

Sentence: "It is knowledge only, with no gate; nothing live was fetched and no
deploy was made."
False as written: the round's C2 ground is five live public GETs — S057–S060 at
2026-10-22T15:41:23Z–15:41:28Z and S061 at 15:41:29Z (SOURCES.md:65-69 "fetched
…15:41:2…"; entry verified-at line 2; retained bodies under .ufo/waves/round-31/sources/).
The true offline boundary is about operator-owned properties, exactly as the entry
scopes it ("No live request to any operator-owned property; nothing about the live
service is asserted."). As written, PROVINCE also hides the round's own freshness
work from the province statement.
Narrower wording: "It is knowledge only, with no gate; no operator-owned property
was fetched or measured, no deploy was made, and the only live fetches were the
Render Docs pages (S057–S061)."

### F2 — MEDIUM (operability, attribution) — PROVINCE.md:121-122

Sentence: "The citing-set fixture runner gained containment for five hostile
fixture shapes (`scripts/citing_set_hostile_selftest.py`);"
The parenthetical names the checker, not the runner or the containment. The five
refusals live in the runner `scripts/citing_set_selftest.py` (argv refusal line
331; git_commit-without-init line 352; expected.json symlink/type/size guards
lines 391-403; symlinked case line 522; fixture .git line 526);
`scripts/citing_set_hostile_selftest.py` only replays the shapes and checks for
harm (receipts: exit 1 at base, exit 0 at fde133a/92235a0). A reader following the
parenthetical lands on the wrong file when repairing or re-checking.
Narrower wording: "The citing-set fixture runner (`scripts/citing_set_selftest.py`)
gained refusals for five hostile fixture shapes, each with a committed hostile spec
checked by `scripts/citing_set_hostile_selftest.py` (5/5, control holding);"

### F3 — LOW (precision) — corpus/README.md:292 (coverage row, health checks)

Phrase: "routing stop at 15 seconds and restart at 60 seconds". The retained S060
text conditions both on sustained failure: "fails consecutive health checks for 15
seconds" / "for 60 seconds" (entry quotes; SOURCES.md:68 carries the accurate
"after 15 seconds of failures"). The row's compression can be read as fixed timers.
Narrower wording: "a failing instance leaves routing after failing checks for 15
seconds and restarts after 60 seconds of failures".
Also in the same row, "nothing live measured" is defensible but looser than the
entry's scope line; prefer "no live request to any operator-owned property (the
source pages themselves were fetched live)" so PROVINCE cannot regress to F1.

### F4 — NOTE (completeness, not overclaim) — PROVINCE.md:113-118

The section presents round 31's knowledge delta as S057–S060 only; the S061
root-domain DNS correction to `render-static-sites.md` (README.md:294-296,
SOURCES.md:69, render-static-sites.md:141-162) is part of the same round and is
unmentioned in PROVINCE. Not an overclaim of held ground; one clause would align
the two files: "Round 31 also added root-domain DNS records to
`render-static-sites.md` (S061)."

### F5 — NOTE (open-list consistency) — corpus/README.md:296

"Accessibility conformance and crawl or JS-rendered canonical signals stay open."
omits the round-27 citing-set families (identity-path, retention, unit-override)
that PROVINCE.md:122-123 carries and the Jekyll real-Pages-build item from the
r29 section. Nothing claims them closed, so this is not overclaim; if the sentence
is meant as the section's open list, add: "…and the round-27 citing-set fixture
families stay open."

## Checked and not at issue

- "offline key-by-key check of the lane's own render.yaml at … 1fbdb8ed" — true
  (entry's per-key section; blob OID verified).
- "The live service's plan, region, domains and deploy trigger stay unknown from
  the file" — true and correctly hedged; render.yaml at 1fbdb8ed sets none of them.
- "no deploy was made" — supported by entry scope and receipts.
- Core vs Frontier: no section claims Core; "knowledge only, with no gate" matches
  the Frontier rule "Ground moves to Core only with source-backed entries and a
  gate" (PROVINCE.md Frontier bullet).
- Coverage row numbers (0.0.0.0, 10000, five seconds, 15 minutes, Host header,
  sync: false, values an existing service keeps) each match a retained S057–S060
  quote in the entry.
- C1 "five hostile fixture shapes" — matches probes P1–P5 = N1,N2,N3,N5,N6.

## Residual risk / not verified

- I read the committed C1/C2 receipts; I did not re-run any counter or the hostile
  selftest (RerunC2Counters / RerunHostileSelftest own re-runs).
- I did not re-open any URL (not assigned; owned-property fetch ban respected);
  ReopenS057S058 / ReopenS059S060 own source re-opening.
- render.yaml verified only at pinned commit 1fbdb8ed; no live service observed.
- SKILL/QUALITY/LOG round-31 sections and wave-1 reports are other seats' scope.
- No tool installs or upgrades were needed or made.
