# Lesson03 — round-12 historical Gate (round-21 retrospective reconstruction)

## Scope
- Target: `corpus/lessons/round-12.md` only.
- Base: `5009ecaa1cce10b895617a585ddd3f7c7c923a84` (HEAD `5009eca`; working tree was clean for this file before edit).
- Pre-existing `## Gate` heading: none (grep `^## Gate` = 0). Gate therefore appended, not left unchanged.

## Change
- Old line count: **62** (`wc -l`; `git show 5009ecaa…:corpus/lessons/round-12.md` also 62 lines). Old sha256 `935485d29b23804fdf008ef22cf608f813fc93efbaf932ed3df79160a40f5c67`.
- Appended: blank line 63, `## Gate` at line 64, body through line 95. New line count **95**; `git diff --stat`: 33 insertions, 0 deletions.
- Prefix check: `cmp` of `git show 5009ecaa…` against `head -n 62` of the working file = identical. No metadata prefix added (C1 scope, not this seat).
- Gate label: "Retrospective round-21 reconstruction, not the original round-12 admission."

## Gate content (what the appended section records)
- Candidates C1–C7: §1 free-read verbs write-free (exits 0/1/0/1); §2 "fleet already instrumented" myth; §3 "keeper re-pins marker" myth; §4 roster 21/20/18 and `lucario`; §5 r11 F1 guard proposal wrong; Lesson bullets 1–2 (runtime verification; refutation pass for handoff patches).
- Outcomes: C1 admitted with qualification; C2 admitted with qualification; C3 admitted for classification, negative sub-claim ("no webzites code writes `fleet.config.json`") unverified; C4 counts admitted with qualification, line anchors unverified; C5 admitted with qualification (patch not shipped, replica unverified here); C6/C7 process guidance, no separate admission recorded.
- Rejected: only the documented ones (two myths framed in §2/§3; r11 F1 guard; two wrong citations and two count errors fixed pre-landing per `SCORECARD.md:95`). Any other rejected candidate: not recorded.
- Outside spot-check: **not recorded**. Round-12 re-runs were same-round L2 seats (executor, critic, reviewer, labrat); none is a non-author outside check. `corpus/lessons/round-20-verifier-spotcheck.md` covers round 20 only.

## Evidence basis (read-only file reads; no live-state re-verification)
- Original lesson sections: `## What the round proved` (lines 6–46), `## Lesson` (48–58), evidence line (60–62).
- In-tree records cited in the gate: `corpus/knowledge/free-read-verbs.md:338-348,362-434`; `corpus/knowledge/keeper-timer-inert.md:3-16,83-109`; `corpus/knowledge/ops-automation.md:14,111-114`; `corpus/knowledge/publish-queue.md:32`; `corpus/handoffs/cmdProbe-merge-fix.md:24-73`; `corpus/README.md:34`; `SCORECARD.md:95`; `SKILL.md:30`.
- S019: registered at `corpus/SOURCES.md:27` (own-work, A tier; "Provenance metadata and recorded lesson gates … not verification of historical platform claims"; target `corpus/lessons/round-21.md`). Gate cites it as metadata authority only.
- Round-21 lesson `corpus/lessons/round-21.md`: **not present** at read time; cited by planned path only.
- Unavailable at read time: `/tmp/kake-r12/` (and its `live/`, `revenger-replica/` subtrees) absent; `~/Projects/webzites` paths recorded absent by `SKILL.md:30` and `keeper-timer-inert.md:14`. Those cited replica and source-line claims are therefore recorded as unverified in round 21.

## Out of scope / not touched
- No other file edited. No commits. No subagents. No tool installs or upgrades (none needed).
- Not touched: SCORECARD, LOG, QUALITY, SOURCES, README, SKILL, other lessons, metadata prefix.

## Checks for main agent
- `git diff -- corpus/lessons/round-12.md` should show 33 pure insertions at EOF.
- `grep -c '^## Gate' corpus/lessons/round-12.md` should be 1.
- Counting command from SCORECARD (lesson gate coverage): `ls corpus/lessons/round-*.md | grep -v aggregator | xargs grep -l '^## Gate' | wc -l` — this file now contributes one.

## Findings / limits
- Gate records historical outcomes only; it does not upgrade any round-12 claim to live-verified.
- Qualification for C3 and C4 line anchors depends on the webzites tree, which the in-tree notes record as partly absent since the 2026-10-12 prune; not tested here.
