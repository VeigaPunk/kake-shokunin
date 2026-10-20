# TrendDiscernment — round 21 critic report

Seat: `KakeR21.TrendDiscernment`, critic, leaf. I wrote only this report. I made no corpus edits. I sent peer notes to three Lesson seats, and all three applied the fixes themselves (see §3).
Axes: freshness and operability (lane-owned), plus the discernment learning trend.
Evidence state: working tree on base `5009eca`, uncommitted wave edits read at about 06:00 local on 2026-10-20.

## 1. Rule applied

Canonical rule: `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md:35,42-46`.
- Discernment counts as `improved` only when a **non-author** spot-check agrees with the gate on at least one admit and one reject. The other route is a spot-check *disagreement* that becomes a lesson and then a grounded `QUALITY.md` criterion.
- "A subagent the lane dispatched is still the lane."

The lane's own form of this rule is `corpus/QUALITY.md:12` (Admission authority). It rejects "a self-dispatched reviewer treated as independent promotion authority."

## 2. Prior round-20 outside agreement vs round-21 author-only work

**Round 20 has real outside agreement, and it belongs to round 20 only.**
- `corpus/lessons/round-20-verifier-spotcheck.md`, commit `7e17c66`, git identity `protocol-shokunin`, written by the integrator.
- Its full report is `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/kake-review.md`. Reviewer `W3ReviewKake` was "fresh orchestrator-dispatched; not the lane's L1/L2 seats" (line 3).
- §5 of that report, lines 113-122, re-opened 1 admit and 2 rejects (`ghp-custom-domain`, S017, S018), plus 2 extra admits and 1 held-back set. All agree.
- The integrator recorded "discernment improved" for round 20 (spot-check line 17). Round 20 has used up that credit.

Caveats on that prior agreement. These do not reverse it, but they must not be overstated:
- **Reviewed commit.** The review targets lane commit `02b6dd0` (kake-review.md:4). The spot-check file says the review ran "after the round landed at `9639ec7a7`" (lines 4-5), but `9639ec7` was committed 44 s before `7e17c66`.
  - The sampled decisions survive `9639ec7` unchanged: `round-20.md:312` says "No SOURCES cells changed".
  - The post-review restoration and the 728-anchor proof (`round-20.md:284-322`) are the lane's own evidence plus the orchestrator's ruling. A non-author did not re-verify them.
- **Admit sample.** The spot-check file names `crawl-scope-per-host` as the admit sample (line 12). The reviewer's core 3/3 sample used `ghp-custom-domain`; crawl-scope was extra #4. Both agree, so this is only a labelling imprecision.
- **Stale lane text.** These lines still say the spot-check is owed or unavailable: `round-20.md:58-60`, `round-20.md:194-196`, M11 at `round-20.md:259`, and `SCORECARD.md:185`. They are historical and must stay byte-identical. L1 may append a pointer in SCORECARD or LOG saying M11 for round 20 was closed by `7e17c66`. That closes round-20 debt; it is **not** round-21 discernment credit.
- **Git identity is not authorship evidence.** `Joao Pedro Veiga` authored both lane lessons and aggregator audits. `protocol-shokunin` authored both the outside spot-check and the `5009eca` docs merge. Non-author status must rest on the dispatch chain stated in the file. `round-8-aggregator-box3-coldrun.md:3-4,68` is a good example of doing this.

**Round 21 so far is entirely author-side.**
- The swarm registry `.ufo/waves/round-21/w1/swarm-registry.json` lists 64 members. Every one is `kind: spawn` with `agentId: KakeR21.*`. The critic and reviewer seats are included: GateTruth, PriorGates, TrendQuality, TrendDiscernment, NoTrade, and the others.
- Each is a lane subagent under `LEARNING.md:45-46`. None of their agreement may be recorded as an outside spot-check.
- `corpus/lessons/round-21.md:46-47` gets this right: "All seats dispatched by this L1 are author-side evidence."

## 3. Counterexamples found, and their status

| # | Counterexample | Evidence | Axes | Status |
|---|---|---|---|---|
| X1 | The round-5 retrospective Gate listed `round-10.md` ("planner, labrat, reviewer, and L1 raw-row agreement") and `keeper-timer-inert.md` (r12) under **"Outside spot-check: existing independent evidence"**. | `round-10.md:3-5` calls these "delegated read-only L2 probes … + L1 self-runs", i.e. the lane's own seats. r12 is a later round in the same lane. This breaks `QUALITY.md:12` and C2's own "no fabricated … independent review" rule. | operability (C2 content), discernment (would be harmed: false provenance) | **Fixed by Lesson11** at `round-5.md:134-146`. Only the two aggregator audits stay as non-author evidence, followed by "Admit/reject spot-check: not recorded". The round-10 and r12 items moved to a paragraph labelled "the lane's own seats and later rounds, not independent review". Change was EOF-only. |
| X2 | The round-10 Gate opened "Outside spot-check: **partial**". The aggregator audit sampled no admit/reject pair. A later tally of "partial" lessons could be counted as outside-check coverage. | `round-10.md:91` | discernment (overcount risk) | **Fixed by Lesson02.** It now reads "Admit/reject spot-check: **not recorded.** Other non-author evidence: …". |
| X3 | The round-7 Gate cited `round-20.md:58-60` ("unavailable") as round 20's spot-check state without noting that a later file supersedes it. | `round-7.md:86` vs `7e17c66` | freshness (stale state cited as current) | **Fixed by Lesson13.** The line now marks it as superseded by `round-20-verifier-spotcheck.md` (`7e17c66`, 2026-10-19). |
| X4 | `round-21.md:46-47`: the spot-check is "owed to the separately dispatched non-author closure reviewer". The dispatcher is not named, and none of the wave artifacts plan one. If KakeR21 spawns this reviewer, it is still the lane. | `round-21.md:46-47`. `wave1-spec.json`, `wave1-validation.json` and `wave1-dispatch-result.json` contain no closure or non-author seat. | discernment | **Open (L1).** Name the dispatcher: the orchestrator, integrator, or operator, never KakeR21. Require the result to land as a separate non-lane file, following the `round-20-verifier-spotcheck.md` pattern. |
| X5 | The round-21 Gate's "Rejected" list is made of policy refusals (no header-as-freshness, no invented rejects, no self-seat as verifier, no weakened gate). An outside reviewer agreeing that "inventing rejects is wrong" tests no material taste, so the reject half of the sample would be empty. | `round-21.md:31-34` | discernment | **Open (L1).** Add at least one *concrete*, file-pointed rejected candidate so the spot-check can sample it. Examples: an entry where `verified-at: <today>` was refused for the historical evidence date, or a lesson where a missing reject log was recorded as "not recorded" rather than inferred. |

**Checked clean.** The Gate wording in these lessons correctly separates in-lane seats from non-author audits, and none claims an admit/reject spot-check: round-1 (`:62`), round-3, round-4 (`:64`), round-6, round-8, round-9, round-12, round-16, round-17, round-18 and round-19-recensus. Round-1 and round-4 cite aggregator audits as non-author evidence of a different kind, which is correct, and round-4 also states "Admit/reject spot-check: not recorded".

## 4. Recommended honest trend for round 21

**discernment: `unchanged` (provisional, author-only).** Grounds:
- No non-author has sampled any round-21 admit or reject.
- All 64 seats are KakeR21-dispatched.
- The round-20 agreement is already credited to round 20 and cannot carry forward.
- Do not write "improved locally". Round 20's pre-review SCORECARD (`SCORECARD.md:183-185`) did that, and it is the self-assessed taste that `LEARNING.md:42` excludes.

**Not `harmed`, provided** two conditions hold:
- The X1-X3 fixes stay as landed.
- No Gate or summary counts lane seats or later in-lane rounds as outside review.

A `QUALITY.md` criterion that L1 grounds in an internal critic finding, with a round-21 lesson row behind it, is allowed. It does not earn `improved`, because the LEARNING route needs a disagreement from a *spot-check*.

**Upgrade path, after landing only:**
1. A reviewer dispatched by the orchestrator or operator, not `KakeR21.*`, samples at least 1 concrete round-21 admit (e.g. one knowledge provenance prefix) and at least 1 concrete reject (see X5).
2. The reviewer records agree/disagree with reasons in a separate file.
3. The integrator may then record `improved` (on agreement), or `improved` via a lesson-backed criterion (on disagreement).

**Smallest corrections still owed (both L1):**
- X4: name the non-author dispatcher.
- X5: give the Gate one concrete, pointed reject.

## 5. Checks for Main to run once

- `git diff 5009eca -- corpus/lessons | grep -nE '^\+.*(independent|non-author|Outside spot-check)'`. Every hit must either cite a non-lane dispatch chain or say "not recorded / author-side".
- Byte-preservation check on `round-5.md`, `round-7.md` and `round-10.md`: the prefix up to the original EOF must equal `git show 5009eca:<f>`.

## Tools / installs

None installed or updated.

## Limitations

- Static reads only. I did not re-run the kaika-w3 commands.
- I did not open `kake-critic.md` beyond its header.
- I did not open history or transcripts to learn who dispatched KakeR21 itself.
