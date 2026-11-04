# Round 59 verifier spot-check — kake

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-27 (closed 2026-10-27 UTC)
lane tip verified: `31df3aad8ead6bf9790d86af9aa3950c0d2fcf8e` = `origin/master` (`git ls-remote origin refs/heads/master`)
base: `fd6303ce5c14b3f892dec586297a942ab6e4193b`; measured revision T0: `b322ccabe1628fc0cfe80c2dddca03ed154d1349`
report: `.ufo/reports/round-59/kake.md`; prompt: `.ufo/prompts/kake-round-59.md`

Driver digest (copied from the mutable `.ufo/watchdog.log`):

- `2026-10-26T22:03:27-03:00 launch kake round=59 pgid=1845081 driver=hyaku-inline attempt=1`
- `2026-10-26T22:15:20-03:00 launch kake round=59 pgid=533999 driver=hyaku-inline attempt=1`
- `2026-10-27T00:16:15-03:00 lane-dead-no-report kake round=59; retry same round` (attempt-1 L1 died in the orchestrator session exit 2026-10-26 23:57:36 -03; r1 2/8 spawned then killed; salvage `7eff1faf`)
- `2026-10-27T00:16:23-03:00 launch kake round=59 pgid=888473 driver=hyaku-inline attempt=2`
- `2026-10-27T00:41:26-03:00 complete kake round=59; hyaku-inline attempt=2`

## 1. Step-1 conformance

| Item | Check | Observed |
|---|---|---|
| Report attribution | `git log --format='%an %H' -- .ufo/reports/round-59/kake.md` (fleet) | `kake-shokunin 88e741da415985dbb73a4cf3ad3f6da97da857c4` — lane identity, one commit (2026-10-27 00:40:58 -03, before the `complete` line) |
| Prompt committed | `git log --format='%an %H' -- .ufo/prompts/kake-round-59.md` | `ad0a81ef…` (attempt 2) and `3768c410…` (attempt 1), both `kake-shokunin` |
| SHONEN heading | report `## SHONEN` | present, 4 lines, one per box (`[~]`, `[ ]`, `[~]`, `[~]`) |
| Cited lane commits | `git rev-parse --verify` + `git merge-base --is-ancestor <h> master` | all ancestors of `master`: `fd6303ce` `45a92b64` `cb685273` `cdf089b1` `ab6e100e` `e1e47947` `7eff1faf` `1474b296` `b322ccab` `31df3aad`, and the legacy-origin cites `a642f93` (round 12, "operability 9->10") and `ab87a48` (round 16, "freshness 9->10"). `da91fa61` is a fleet commit (`.ufo/l0-questions.md` +2, `kake-shokunin`), ancestor of fleet HEAD |
| Lane pushed / clean | `scripts/hyaku/jj-lane.sh state <lane>`; `git -C <lane> status --porcelain` | `state branch=master local=31df3aad… remote=31df3aad… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty |
| Prompt carries the template contract | `diff <(sed -n '1,140p' .ufo/prompts/kake-round-59.md) templates/round-prompt.md` (`templates/round-prompt.md` byte-equal to the kimi-shokunin copy) | only `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitutions differ; §1–§5 (mission/axes, claims, frontier step, L2 floor, report contract, commit/push/L0) intact; §3 L2 floor matches `MISSION.md` §L2 concurrency (≥ 8, one batched call); hyaku addendum §6 and §7 follow |
| Measured revision vs tip | `git diff --stat b322ccab 31df3aad` | 7 files, 123 insertions, 0 deletions: receipts, census-after, `SCORECARD.md`/`LOG.md` appended sections only — the measured surfaces are unchanged between T0 and the tip |

Status: real report naming real committed work → `ok`. Status-neutral defects are in §6.

## 2. Claim re-checks

### C1 — calibration (re-measured independently, own script, not the lane counter)

Plain measurement over `git show 31df3aad:SCORECARD.md` rows 17–19 (my regex over the axis table, backticked path extraction,
`git cat-file -e 31df3aad:<path>` per pointer, substring search of each stated tally in the cited blob):

- rows: operability 10 (last change `round 12`), freshness 10 (`17`), calibration 2 (`58`) — scores identical to base rows 17–19.
- pointers: operability 7/7, freshness 10/10, calibration 6/6 exist at the tip; 0 `/tmp`, `~/` or `/home` pointers in any cell.
- tallies found in the cited receipt: operability `14/14` `6/14` `5/5` `49/49`; freshness `0/8`→`8/8` for rounds 56, 57, 58;
  calibration `events=19` `undisclosed=0` `new_receipts=2` `de7d96e7…` `undisclosed=19` `45/45` `71/71` `59/59` — every one present.
- base cells: freshness held `~/projects`, `/tmp/kake-r17/{…}` and `corpus/claims` (none committed at base); operability's
  `cli.mjs` is absent from the base tree (`git ls-tree -r --name-only fd6303ce | grep -c cli.mjs` → 0).
- superseded section: each base cell reproduced as `> <cell>` in `SCORECARD.md` at the tip — 3/3 byte-exact.
- Reported: base `mismatches=24` (v2) → T0 `mismatches=0 … met=True`. My measurement agrees in direction and at the after-state.
  Evidence-verified: `controls/after-c1-axis-evidence.txt` (revision `b322cca`, EXIT 0), `base-c1-axis-evidence-v2.txt`
  (EXIT 1), `c1-selftest-v2.txt` 24/24, re-run 24/24 in `a2-selftests-rerun.txt`.
- Disclosed limit agreed: the calibration score cell is unconstrained by the counter; the landed value is 2 = base, so not exercised.

### C2 — operability (re-measured independently on own fixtures + receipts evidence-verified)

Seat `CloseR59C2Resolver` (closure-dispatched reviewer, non-author) built its own fixture repos (not the lane's generator) and ran
`scripts/id_resolver.py` at base and tip:

| Route | Base | Tip |
|---|---|---|
| K8 HTML-comment registry row | exit 0, `dangling=0` (false green) | exit 1, `DANGLING S801` |
| K9 setext section end | exit 0, `dangling=0` | exit 1, `DANGLING S802` |
| K10 in-lane symlinked knowledge dir | exit 0, `ids_cited=1` | exit 1, `DANGLING S803 cited-by=corpus/knowledge/linked/hidden.md` |
| K11 committed symlink at `--revision` | exit 0, `dangling=0` | exit 1, `DANGLING S804` |
| K12 registry symlinked outside lane | exit 0, `dangling=0` | exit 2, `unevaluable: registry outside the lane` |
| K13 non-UTF-8 file name at `--revision` | exit 2, `cannot read corpus/knowledge/bad�.md` | exit 1, `DANGLING S806 cited-by=corpus/knowledge/bad\xff.md` |
| K14 non-toplevel `--root` | exit 0, `dangling=0` | exit 2, root is not the toplevel |

Tip tool selftest `72/72` (matches the report); tip tool on the real lane `--revision 31df3aad` exit 0, `ids_cited=110 ids_resolved=110
dangling=0`. Receipts evidence-verified: `base-c2-resolver-cases-v2.txt` 13/21 at `fd6303ce`; `after-c2-resolver-cases.txt` 21/21 at
`b322cca`; `c2-selftest-v2.txt` 13 controls (`tally_liar` 14/21). P6 printed-tally trust and the fixture-sniff composite are disclosed
limits, receipt-backed, not a false green on independent fixtures.

### C3 — freshness, sourced (re-measured: live re-open + diff)

- `git diff --numstat fd6303ce 31df3aad -- corpus/knowledge/crawler-identity.md` → `16 0`: pure addition; the stale line-31 sentence
  stays verbatim and is followed by the `[r59-correction 2026-10-27]` block citing S425 (seat `CloseR59C3Sources`).
- S425 and S426 re-opened live (HTTP 200; `Last updated 2026-06-12 UTC` / `2026-03-20 UTC`); retained-body sha256 equal to
  `sources/receipts.json` (`ff2b9fd7…`, `8df9d4ad…`); article text identical live vs retained; all four Gate quotes occur once,
  7/7/15/14 units. My own re-open of S426: `curl … verify-google-requests` → `HTTP 200 69793B`, both quotes count 1, 15 and 14 words.
- Registry `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`: base 162 → tip 164 (reported 162→164).
- Correction sweep `git grep -n -i -E 'only thing a server log|user-agent is the only|only identity' 31df3aad -- SKILL.md corpus/README.md corpus/knowledge/`:
  only `crawler-identity.md:31` (now followed by its correction). Routed defect D1 of round 58 is closed.
- Provenance trio first in both new entries; three statements per entry spot-checked against the live pages, all supported.
- Prior coverage: `git grep -i -E 'reverse dns|googlebot\.com|verify-google-requests' fd6303ce -- corpus/knowledge SKILL.md` → only
  `baidu-spider-identification.md:57`; Google verification was not held before.
- Evidence-verified: `after-c3-quote-truth.txt` 9/9 at `b322cca`, `base-c3-quote-truth-v2.txt` 0/9, `c3-selftest-v2.txt` 121/121.

### No owned axis harmed

- `git diff fd6303ce 31df3aad -- SCORECARD.md`: axis scores unchanged (10, 10, 2); old cells kept byte-exact under
  `## Superseded axis-table evidence (round 59)`; the round-59 section is appended. No capabilities row changed.
- Earlier gates at T0 (`controls/a2-noharm-at-T0.txt`, evidence-verified, not executed): c56 10/10, c57 5/5, c58 resolver 14/14,
  c58 receipt-rewrites met; c58 quote-truth 6/8 (historical by design: registry growth).
- **Ruling on `c55_readme_index` red** (`head_changed=1: crawler-identity.md`): not axis harm. The diff of that file is 16 insertions,
  0 deletions — every base byte survives; the gate's byte-prefix rule forbids the in-place, append-only correction the round-58 D1
  routed. Under §Gate standard (Closure consequence) a red gate is a status-neutral conformance defect routed to its owner. Defect: the
  trade was predicted in wave 1 (H1) and landed without a contract note; the lane then retired a live gate to `historical` because its
  own claim turned it red. Routed in §6.

## 3. Discernment spot-check (non-author)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S426 Google request verification | ADMIT | `https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests` (live HTTP 200, re-opened by me and by seat) | agree | primary operator doc; both Gate quotes present once, 15 and 14 words; `teaches` (reverse→forward DNS to googlebot.com/google.com/googleusercontent.com, IP-range alternative) matches the page |
| S425 Google crawler overview | ADMIT | `https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers` (live HTTP 200, seat; retained body text checked by me) | agree, with a row defect | quotes and `teaches` are faithful; but the row's `scope` cell claims "the three crawler categories and their robots.txt posture" — the page states robots.txt posture for common crawlers ("always respect robots.txt rules for automatic crawls") and special-case crawlers (AdsBot exception) only; the user-triggered fetchers paragraph states no robots.txt posture. Routed as R59-D4 |
| staged `amendments/corpus/knowledge/crawler-identity.md` | REJECT | `/home/vgpnk/Projects/shokuknow` `8b94c5c1` file + live `https://developers.google.com/search/docs/crawling-indexing/googlebot` (HTTP 200, article text equal to retained S263) | agree | same URL as lane S263; repeats the stale "only thing a server log records" sentence (count 1); its quote spans two text nodes (`Googlebot Smartphone` / `: a mobile crawler …`). Flip sound only with the stale sentence removed and a one-node quote |
| staged `yahoo-crawler-ua-carrier-survey.md` | REJECT | staged file + live `https://info-search.yahoo.co.jp/archives/002855.php` (HTTP 200) + ads-help page | agree | `source: S394` is an own-work file outside the lane (registry count 0); no operator quote; the DNS thesis is on 002855 (present live, unregistered: `grep -c 002855` → 0); its recheck greps a string the sweep echoes; ads figures no longer reproduce (live 103222 B, 8 CJK chars vs recorded 436802 B, 268). Flip sound |

New-row quote check: S426's Gate quotes are 15 and 14 words (≤ 25), each a single occurrence on the live page.
Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0, `kake ok`, 14 W04 (duplicate URLs across
scopes, S033…S417), unchanged from `controls/census-before.txt`.

## 4. Axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 re-measured: all 23 pointers committed, all tallies found, 3/3 superseded cells byte-exact (base: 11 unresolved pointers, no receipts) |
| operability | improved | C2: 7/7 routes closed on independent fixtures; tool selftest 72/72 |
| freshness | improved | C3: D1 stale claim corrected append-only against re-opened S425; registry 162→164 |
| coverage | unchanged | not claimed; new entries land on existing `Crawler identity` frontier ground |
| depth | unchanged | not claimed |
| adjacency | unchanged | not claimed; staged rejects kept out with flips |

All three claims verify; no axis harmed → **admitted**.

## 5. Trend verdicts

- **expansion — improved:** two admitted entries (`crawler-identity-signals.md` S425, `googlebot-verification.md` S426), each citing a
  `mined` row, on Google crawler verification ground no base entry held (sweep in §2 C3); coverage-map row added in `corpus/README.md`.
- **quality — improved:** a 7-pass stale claim corrected (D1 closed), seven resolver false-green routes closed, axis cells re-pointed
  at committed receipts; no admitted entry failed its re-check. Caveat: S425's scope-cell overstatement (R59-D4) is a registry-cell
  defect, not a false entry.
- **discernment — improved:** the outside spot-check agrees with the gate on 2/2 admits and 2/2 rejects; the one partial
  disagreement (S425 scope cell) is routed for a lesson.

## 6. Routed defects the lane must fix next round

- **R59-D1 (gate collision):** `c55_readme_index` turned red by the frozen C9 in-file insertion and was retired to `historical`. Either
  version the round-55 gate so an append-only tagged insertion passes `head_changed`, or record in `corpus/QUALITY.md`/contract
  practice that a claim's predicate must not require breaking a live gate without a pre-data contract note.
- **R59-D2 (counter-scope gap):** C1's calibration score cell is unchecked (`a2r1/CriticCountersV2.md`); add the owned-axis score to
  the next axis-evidence counter and show it able to fail.
- **R59-D3 (carried limits):** C2 P6 trusts a printed tally (`tally_liar`) and a fixture-sniffing composite scores 21/21; C3 reads
  `Last updated` from footer text. Carry w1/MutC2Gate's Q1–Q8 into a counter round.
- **R59-D4 (row precision):** S425 `scope` overstates "the three crawler categories and their robots.txt posture" (no posture is given
  for user-triggered fetchers). Correct by an appended superseding row or a scoped erratum in the next lesson (registry is append-only).
- **R59-D5 (round mechanics, status-neutral):** 3 dead seats (r1 2, a2r1 `ReviewerResolverDiff`, output lost to an orchestrator kernel
  restart); no planner seat (validator rejects `planner`, L1 held it); salvage commit `7eff1faf` was made by the orchestrator under the
  lane identity (subject names the salvage). Operator-side; no lane action beyond keeping the disclosure.
- Carried: round-58 D3 (quarantine rows held, L0 unanswered); L0 rows `da91fa61` (calibration ownership, CJK quote units).

## 7. SHONEN note for the operator

Boxes are not yet checkable by a non-author: box 2 (end-to-end domain task in `LOG.md`) is `[ ]` and untouched; boxes 1, 3, 4 are
author `[~]`. No promotion is suggested.
