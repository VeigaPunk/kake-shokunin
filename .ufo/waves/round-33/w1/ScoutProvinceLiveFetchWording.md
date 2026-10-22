# Scout — round-31 F1/F2 vs PROVINCE's appended narrowing paragraph

Seat: KakeR33.ScoutProvinceLiveFetchWording (leaf), axis freshness. Target
`.ufo/waves/round-31/a2-w2/ReviewProvinceReadme.md` F1 (HIGH), F2 (MEDIUM), against PROVINCE.md
at bc6c4a8d435473f3c30903210be30d9d6e3ef750. Sandbox clone
`/fast/scratch/hyaku/kake-r33/w1/ScoutProvinceLiveFetchWording/clone`, clean. No installs, no
live requests; this report is the only lane file I wrote.

## Revision facts
- PROVINCE.md at bc6c4a8: blob `645511709371befff2c7fdd22c98b55d677cd2ff`, sha256 `0baeba82…1988b5`.
- Paragraph at PROVINCE.md:125-131, inside `## Round-31 Render web-service frontier step` (:111),
  below the attacked sentences (:119; :121-122). Landed in `9a7f5be`, byte-unchanged to bc6c4a8.
- `corpus/lessons/round-32.md:56-62` lists F1/F2 as "Carried open (wave-1 sweep, not mined this
  round)" — a `ReviewMistakeSweep` pointer, explicitly "not judged this round".

## F1 — RESOLVED (substance) at bc6c4a8
The append (:125-128) reproduces F1's own demanded wording: "'nothing live was fetched' above
means no operator-owned property was fetched or measured and no deploy was made; the round's only
live fetches were the public Render Docs pages S057–S061 (one GET each, 15:41:23–29Z)."
- Five GETs: `.ufo/waves/round-31/sources/receipts.json` has exactly S057–S061, each `status` 200,
  `finalUrl` == `url`, `accessedUtc` 15:41:23Z / :26Z / :26Z / :28Z / :29Z; all are
  `https://render.com/docs/*` (`fetch_sources.py:25-31`; S061 = `configure-other-dns`).
- "one GET each": one `urlopen` per source, no retry (`fetch_sources.py:51-59`); UA at :32 says
  "one GET per page"; same phrase as the entry's `verified-at` (`render-web-services.md:2`).
  Scope limit: receipts record the scripted run, not every seat's keyboard.
- "only live fetches": URL audit of all round-31 wave artifacts finds source URLs only for those
  five docs pages; chatgpt.com / app.ds4cc.com / rfc-editor / support.claude.com occur as Blueprint
  env values, census W04 text, or no-fetch scope lines (`w1/ScoutDs4ccRenderSurface.md:5`).
- F4 clause accurate: S061 used-by is `render-static-sites.md` (SOURCES.md:69); its
  `## Round-31 corrections` is at :141-160.
- Residual, not an open finding: :119 still reads false if quoted alone. Append-only scoping is
  this file's convention (PROVINCE:112 "historical for its date"; README:298-301 for F3). Future
  text must not restate :119 without :125-131.

## F2 — RESOLVED at bc6c4a8
The append (:129-130): "The refusals live in the runner `scripts/citing_set_selftest.py`;
`scripts/citing_set_hostile_selftest.py` is the committed check of them" — F2's harm (reader sent
to the checker instead of the runner) is fixed in the same section.
- Refusals in the runner (blob `200030d9…`): argv 340-345, predicate 370-387; `git_commit` without
  `git_init` 365-366 and 491-493; `.git` entry 390-396, 488-489, 540-543; `expected.json`
  symlink/regular/1 MiB guards 399-423; symlinked case 537-539.
- Checker, not containment: `citing_set_hostile_selftest.py` (blob `069d460c…`) builds each shape
  from `scripts/fixtures/citing-set-hostile/*/hostile.json` (:237) and passes only when the runner
  exits 1 with every hostile case in the runner's `failures`, benign and `h0-control` not failed,
  no canary, victim unchanged (:220-222).
- Ran it: `TMPDIR=<sandbox>/tmp python3 -B scripts/citing_set_hostile_selftest.py --root .
  --tmpdir $TMPDIR/hostile` → exit 0, `passed: true`, P1–P6 true, refusals runner-reported
  (`case.json argv refused: --selftest`; `case.json setup op 'git_commit' needs an earlier
  'git_init'`; `symlinked case directory refused`).
- Residual (optional): the append omits "one committed spec per shape" and "5/5, control holding".
  PROVINCE carries no run counts (`grep -nE "[0-9]+/[0-9]+|exit [0-9]|receipt"` → no hit), so this
  is house style. F2's line cites (331/352/391-403/522/526) drifted after 9a7f5be; the append cites
  no lines, so nothing in it is stale on that account.

## Residual outside F1/F2 (the append does not close it)
PROVINCE.md:122 "five hostile fixture shapes" undercounts at bc6c4a8: six specs P1–P6 exist (P6,
round 32) and the run above is 6/6. Already round-32 routed defect 5
(`round-32-verifier-spotcheck.md` "Routed defects" 5); the paragraph neither claims nor worsens it.
If wanted, append after :131: "The committed hostile-spec set now has six shapes (P6, round 32);
'five' above is the round-31 count."

## Commands (sandbox clone unless noted; all exit 0)
- `git clone -q <lane> clone; git checkout -q bc6c4a8…` → HEAD bc6c4a8…, status 0 lines.
- `grep -n "^## \|wave-2 narrowing\|refusals live" PROVINCE.md` → headings end :111; append :125-131.
- `git log -S"wave-2 narrowing" -- PROVINCE.md` → `9a7f5be`; `git diff 9a7f5be bc6c4a8 -- PROVINCE.md | wc -l` → `0`.
- `python3 -B -c` dump of `receipts.json` → five keys, timestamps/statuses as quoted.
- `grep -rhoE "https?://..." .ufo/waves/round-31 --include=*.md --include=*.json | sort | uniq -c`
  → only the five docs pages as source URLs.
- `python3 -B scripts/citing_set_hostile_selftest.py --root . --tmpdir $TMPDIR/hostile` → exit 0,
  6/6 (summary at sandbox `../hostile.json`).
- `sed`/`grep` reads of runner, hostile selftest, `SOURCES.md:65-69`, `render-static-sites.md:141-160`.

## Confidence / not verified
- F1 resolved: high; depends on the receipts being the round's complete fetch record — no committed
  artifact shows another live fetch. F2 resolved: high for attribution; containment is code read
  plus a live sandbox run at bc6c4a8.
- Not verified: no URL re-opened (owned-property ban; S057–S061 content freshness not re-measured);
  benign 45-case suite not re-run; no C1/C2 counter work.
