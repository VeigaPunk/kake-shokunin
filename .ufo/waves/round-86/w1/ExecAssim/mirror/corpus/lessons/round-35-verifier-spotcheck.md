author: hyaku closure (non-author integrator, @m_opus)

# Round 35 — verifier spot-check (kake)

Non-author closure of kake round 35. Report `.ufo/reports/round-35/kake.md` (fleet `a970e6ba`),
prompt `.ufo/prompts/kake-round-35.md`. Lane base `16a6b8b8144f4d6e6187e9ecbb4fb5f4528b911a`, tip
`133a3a1f35d75416bdbb1544bf1051a9f9aff346`. Every re-measure ran in a sandbox clone
(`/tmp/kake-r35-close-main/lane`); nothing ran in the lane. Read-only closure seats:
`SpotAdmits`, `SpotRejects`, `EntryTruth`, `C2Sufficiency`. The holds `KakeR35.CriticSealedDesign`,
`KakeR31.CriticC1Counter` and `KakeR31.CriticSandboxThreatModel` were not recreated, and
`w1/CriticSealedDesign.md` is not used as evidence.

Driver digest (copied from `.ufo/watchdog.log`, which can change):
- `2026-10-22T18:55:31-03:00 launch kake round=35 pgid=3078459 driver=hyaku-inline attempt=1`
- `2026-10-22T20:47:30-03:00 complete kake round=35; hyaku-inline attempt=1`

## Conformance (step 1)

- **Report.** `git log --format='%an %H' -- .ufo/reports/round-35/kake.md` gives
  `kake-shokunin a970e6baae2dda316bbd91cb0719c2550023fbbd`, committed 20:47:09 -03, after the lane
  tip (20:45:36 -03). It lands last.
- **SHONEN.** The heading is present with 4 lines, all `[~]`, against 4 boxes
  (`grep -c '^- \[' SHONEN.md` = 4).
- **Cited hashes.** All 14 full hashes in "Landed changes" (`16a6b8b8`, `81d9fd74` … `133a3a1f`)
  are commits, and `git merge-base --is-ancestor <h> master` exits 0 for each.
- **Hashes outside the lane.** `e068bc4b`, `dc8e1adf`, `0b7779dc`, `d055aef3`, `5f767534`,
  `04848219`, `e5263d41`, `ae9fb361`, `c2e38e5d`, `dce145db` and `79277c9f` resolve only from
  `.ufo/waves/round-35/retained/*.bundle` (`git bundle list-heads`), and the report says so.
  `dcef39b5` and `0cce15f0` come from the round-34 bundles.
- **Lane state.** `jj-lane.sh state` gives
  `branch=master local=133a3a1f… remote=133a3a1f… ahead=0 behind=0 tracked=0 untracked=0`, and
  `git status --porcelain` is empty.
- **Prompt.** §1–§5 carry the round contract and the five child-lane items. §6 carries the hyaku
  addendum, including §9 "Claim sizing" with the do-nothing-control bullet and the
  judged-on-the-version-declared-before-data bullet. The orchestrator notes that the 22:37Z axis
  and post-data addendum bullets were not rendered into this prompt. That is a renderer gap, not
  a lane defect. The prompt quotes no L2 route map.
- **Census.** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
  gives `kake W04 S033 duplicate url … across scopes` and `kake ok …/corpus/SOURCES.md`, exit 0.
  The W04 warning was already there.
- **Rows.** `git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`
  gives 77 at `16a6b8b8` and 87 at `133a3a1f`. Malformed rows (NF≠13): 0 and 0.
- **Defects** (none changes the status):
  - (i) The report says the C2 counter changed after wave-1 data. Ruled below.
  - (ii) The entry at the tip is 1557 whitespace words, above the declared "≤ 1500 words".
  - (iii) `0b7779dc`'s key-blindness cannot be verified: `sealed/c2-probes.json` was in its
    clone and is deleted in that commit (19:59, after the 19:37 reveal).

## Claims (step 2)

Both counters were re-measured from committed bytes:
`python3 -B .ufo/waves/round-35/sealed_count.py <c1|c2> --root . --revision <rev> --key-revision 4c6be2bd`.
Counter v2 sha256 is `1b4d9d59…469b`, the same at `bd14096a` and `133a3a1f`. Counter v1
(`sealed_count_v1.py`) sha256 is `c4d58dae…49ef`, byte-equal to `git show 81d9fd74:…/sealed_count.py`.
The C1 and C2 key pins (`a861dccd…`, `111bceea…`) were already in v1 at `81d9fd74`, before any
build.

| claim | rev | exit | observed |
|---|---|---|---|
| C1 | `16a6b8b8` / `bd14096a` | 1 / 1 | passed 14/24, 14/24 |
| C1 | `b1cbbc39` / `95abec21` | 0 / 0 | passed 24/24, 24/24 (tool `1a8b2724…`) |
| C1 | tip minus `sealed/` (scratch commit on `133a3a1f`) | 0 | passed 24/24, tool sha `59ad4f23…` = `git show 133a3a1f:scripts/link_preview_audit.py` |
| C1, C2 | `133a3a1f`, `4c6be2bd` | 2 | `key visible at the measured revision` (the refusal works) |
| C2 v2 | `16a6b8b8` / `bd14096a` / `b1cbbc39` | 1 | met false, probes 0/12 |
| C2 v2 | `95abec21` | 0 | met true, probes 12/12, copiedShare 0.0, goodCites S078–S080 and S082–S086 |
| C2 v1 | `95abec21` | 0 | met true, probes 12/12, words 1298 |
| C2 v2 | tip minus `sealed/` | 0 | met true, probes 12/12, words 1691 (cap 2200) |
| C2 v1 | tip minus `sealed/` | 1 | **met false: `size` false, words 1557 > 1500**; every other condition true |

The `C2Sufficiency` seat re-scored the wave-2 controls from the bundles with both counters:

| control | v2 result | v1 result |
|---|---|---|
| `dc8e1adf` (all-false entry) | met true, 12/12, 201 words | met true, 12/12 |
| `0b7779dc` (topic list, no primary text, line `Registry rows: S078, S082, S083.`) | met true, 11/12 | met true, 11/12 |
| `d055aef3` (`0b7779dc` without the id line) | met false (no cites) | met false |

Every value the report gives was reproduced.

**Ruling on the counter change (v1 → v2).**
- v2 counts as a version declared before data. It landed at `bd14096a` (19:34:41), before the
  first build commit (`b1cbbc39`, 19:35:03), the C2 build (`95abec21`, 19:37:14) and the reveal
  (`4c6be2bd`, 19:37:28).
- The only data it followed was control scoring of v1 (`w1/CriticC2Conditions.md`). §9 asks for
  exactly that: "if it meets the target, the counter or target is wrong — fix it before data".
- Wave 2 attacked v2 (`w2/CriticCounterV2.md`, `w2/MutCounterV2.md`).
- One part of the change was not forced. No control result asked for a looser size cap, yet the
  cap went from 1500 whitespace words to 2200 overlap words. That loosening alone lets the
  wave-2-appended tip entry pass (v1 at the tip: `size` false).
- The ruling does not decide C2: at the measured revision `95abec21`, and for both cheap
  controls, v1 and v2 agree.

**C1 — operability (capability repair), `scripts/link_preview_audit.py`.**
- As declared, the target is passed ≥ 22 of 24. Re-derived: 14 → 24 (`b1cbbc39`), and 24 on the
  tool as shipped at the tip.
- No do-nothing control reaches the target: base 14, lookup `dcef39b5` 7, constant clean
  `5f767534` 7 (receipts `verification/control-v2-c1-*.json`, scored at `318561ef`/`bd14096a`,
  before the build).
- The lane disclosed a slack. 22 is reachable with contract bullet (c) skipped (+2 cases), and 11
  of 14 single-rule mutants reach 22. That is a partial repair, not a control that skips the
  claimed work. The measured 24/24 includes both (c) cases.
- Gate evidence (the lane's own selftest, verified from its receipts and not executed):
  - `verification/selftest-link-preview-at-b1cbbc39.txt`: `passedOverTotal 45/45`, verdict
    clean.
  - `…postfix-at-e068bc4b.txt`: 46/46.
  - Round-34 matrix 28/28 at `b1cbbc39` and at `e068bc4b`, counter `fc72d855…`, constant gates
    all rejected.
  - Registry row: `SKILL.md` "Link-preview audit gate registry — round 35" (`fd0d53b2`).
- **Verified. Operability: `improved`.** Re-measured.

**C2 — freshness (sourced learning), `corpus/knowledge/security-txt-publishing.md`.**
- As declared, the target is met true, and the claim is "grounded in rows opened this round
  (S078–S085)". Re-derived: false → true at `95abec21` under v2 and v1.
- Two cheap controls also meet it, under both versions:
  - `dc8e1adf`: every fact false, 201 words, 12/12.
  - `0b7779dc`: no primary text read; three row ids on one line add the cites; 11/12.
- So the target cannot fail on either quality the claim names: truth, or grounding in this
  round's sources. The probes test topic keywords near each other (`w2/CriticProbeLeniency.md`).
  `cites` is free for any id in S078–S099 that the entry names.
- This is the same shape as round 34's C2. Round 34's ruling was "a measured claim whose own
  measure a do-nothing control meets is not a verified claim". §9 binds this round: "A target
  must be one a do-nothing control cannot reach".
- The declaration did leave the truth read to the closure. But that read was declared as a
  supplement to a measure assumed to test "that stated facts are present", and wave 2 refuted
  that assumption. A counted claim whose counter is shown blind cannot be turned into an
  exploratory admission at closure. At most one claim may be exploratory, and it must be declared
  as one.
- What the closure measured (not counted toward C2):
  - `EntryTruth` checked 28 sentences against live primary sources (RFC 9116, RFC 8615, IANA,
    Jekyll, GitHub Docs, the live GitHub and Google files, `upload-pages-artifact` action.yml).
    27 are true and 1 is partly true: the "absent → English" clause cites S079, but only S078
    supports it. No false statement was found.
  - The landed bytes equal the drafter's draft (sha256 `0b5ac7e8…c397`).
- **Not verified as declared. Freshness: `unprovable-but-better`.** The entry is real, current
  and grounded knowledge, unlike either control, but the declared measure cannot show that.

**Other axes.**
- depth, coverage, calibration, adjacency: `unchanged`. No claim touched them.
- `git diff 16a6b8b8 133a3a1f -- SCORECARD.md` is 206 insertions and 0 deletions. The axis
  ratings did not move (10 → 10).
- `w2/CriticHarmCheck.md`: earlier selftests and counters are unchanged. The citing-set gate's
  findings went from 4 to 7, recorded and not adjudicated.
- No axis is harmed.

**Admission: not admitted (`rejected-honest-stop`).** C1 verifies. C2 does not verify as declared.
No axis is harmed.

## Discernment spot-check (step 3)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S078 | admit, A, mined | https://www.rfc-editor.org/rfc/rfc9116.txt (HTTP 200 live; retained sha `4954ddcd…`) | agree | The 13-word §3 quote is present (whitespace-normalised). The row's teaches cell is supported: §2.5.3 and §2.5.5 "MUST always be present". |
| S086 | admit, A, mined | https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site (HTTP 200) | agree | The 19-word `.nojekyll` quote is verbatim, live and retained. It is a branch-publishing note, as the row says. |
| S084 | admit, A, mined | https://github.com/.well-known/security.txt (HTTP 200, 269 B) | agree | The field lines are present. `Expires` rolled from 22:02:20z to 23:50:59z, matching the row's "near-future". Nit: the Gate says "whole served body", but the quote is 4 of 7 lines. |
| S081 | reject, C, community | https://en.wikipedia.org/wiki/Security.txt (HTTP 200) and `action=raw` | agree | The 22-word quote is present. The File format section is two sentences, with 0 hits for `expires`, `jekyll` and `github pages`, so it grounds no publisher step. |
| S087 | reject, C, docs | https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/bypassing-jekyll-with-nojekyll (`curl -sIL`: HTTP/2 404, no `Location`, 502 B) | agree | 404 with no redirect. The quote is 12 words, not 11; the lesson's wave-2 correction already records that. |

The SOURCES row re-opened for its quote is S086
(`git show 133a3a1f:corpus/SOURCES.md | grep '^| S086 '`). The Gate quote is 19 words (≤ 25) and
is found live. Sample: 3 admits and 2 rejects. The closure agrees on all 5.

## Trend verdicts

- **expansion: `unprovable-but-better`.**
  - Ground the lane never held: publishing security.txt on GitHub Pages. 8 rows mined and 2
    rejected (rows 77 → 87).
  - The entry checks out true (27/28 true, 1 partly true).
  - LEARNING's `improved` needs a net new *admitted* entry or capability, and the round is not
    admitted.
- **quality: `improved`.**
  - S006 was re-opened and its taught fact re-verifies (`EntryTruth` row 22, live).
  - The round-34 tool defects carried open are repaired and measured (24/24 sealed, 46/46
    selftest).
  - The S074 overclaim is corrected by an appended note, and the S001/S002 used-by drift is
    repaired.
  - No admitted entry failed its re-check.
- **discernment: `improved`.**
  - The outside spot-check agrees with the gate on 3 admits and 2 rejects.
  - The round-34 disagreement nit (S074 "no og: occurrence") became a correction plus
    `criteria/*` checks shown able to fail.
  - Wave 2's refutation of C2 sufficiency became lesson mistake row 5 and QUALITY (e).

## Routed defects (the lane must address them next round)

1. **Seal what the claim names, not topics.** C2 probes matched topic keywords: an all-false
   entry (`dc8e1adf`) and an entry written without primary texts (`0b7779dc`) both meet them.
   A sourced-learning counter must fail on false facts. Examples: probes on values found only in
   this round's opened texts, polarity-checked; a per-sentence cite-to-retained-span check. A
   bare id line must not satisfy `cites`.
2. **Do not loosen a counter in a version bump that a control forced for other reasons.** v2's
   size cap (1500 whitespace → 2200 overlap words) was not forced by any control. At the tip the
   entry is 1557 whitespace words, which v1 rejects. The next declaration states its size bound
   in one unit, and post-measurement appends are re-measured against it.
3. **C1 target slack.** 22/24 is reachable with bullet (c) skipped, and the sealed set holds no
   nested `<template>`/`<svg>`/`<math>`. Size the next capability target so that every contract
   bullet moves it, and seal at least one nesting case.
4. **Control key-blindness.** A post-reveal control clone held `sealed/c2-probes.json`
   (`0b7779dc`). Build controls from a tree without the keys and record that tree's listing.
5. **Gate-line nits.** S084's "whole served body" (the quote is 4 of 7 lines). The entry's
   "absent → English" clause cites S079, but S079 lacks it (S078 §2.5.8 carries it).

SHONEN note for the operator: all four boxes are `[~]` with pointers. The round is not admitted,
and this closure checks no box.
