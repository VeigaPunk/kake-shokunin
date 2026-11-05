author: hyaku closure (non-author integrator, @m_zfl)

# Round 93 — verifier spot-check (non-author)

Integrator of record for kake lane round 93; author of no round-93 change. Verified against lane
HEAD `75effe7bbc1b77fbfcf80c09119c0680d9e224c9` (= `git ls-remote origin refs/heads/master`). The
lane's frozen counters were **executed by this closure as plain re-measurements over committed
bytes** (read-only, scratch-only output); the lane-owned freshness-sweep **gate was not executed**
— its committed before/after receipt was read (§Gate standard, Closure consequence). External
sources were re-opened live (one public GET each).

## 1. Conformance (step 1)

| check | command | observed |
|---|---|---|
| report attribution | `git log --format='%an %ae %H' -- .ufo/reports/round-93/kake.md` | `kake-shokunin <kake@shokunin.local> 2345a1bf2a96f8e21835f56bdc0f7b7bd249cbb1`, 2026-11-05 11:05:11 -0300 — before the driver completion line 11:11:14 |
| report substance | `grep -c '^## SHONEN' .ufo/reports/round-93/kake.md`; `wc -c` | heading ×1; four `- […]` box lines matching `SHONEN.md`'s four boxes (three `[~]` with pointers, one `[ ]`); no `[x]`; 16 942 B — a real report, not a marker |
| cited lane commits exist and are ancestors of the branch ref | `git cat-file -e <h>^{commit}`; `git merge-base --is-ancestor <h> 75effe7b` | `191ef8dd`, `bb8012fe`, `5272c727`, `d838e744`, `4f5846fe`, `75effe7b` (and base `10ecbd1a`, freeze `bb8012fe`) — all exist, all ancestors; ancestry tested against the `master` ref, not `@{u}` (jj-colocated, git HEAD detached) |
| lane pushed and clean | `scripts/hyaku/jj-lane.sh state kake-shokunin`; `git status --porcelain` | `branch=master local=75effe7bbc1b7… remote=75effe7bbc1b7… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty |
| dispatch prompt carries the template contract | diff of `.ufo/prompts/kake-round-93.md` §1–§5 vs `templates/round-prompt.md` | faithful render — only `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` placeholders substituted; hyaku addendum §6 present (run-15 round-size 8–16, ≥25 % attack share, WAVE-DONE rule) |
| dispatch digest | `.ufo/watchdog.log` (copied verbatim, mutable file) | see §5 notes block |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` | exit 0, final line `kake ok …/corpus/SOURCES.md`; 37 W04 duplicate-URL advisories (31 → 37: the six new rows re-scope `rfc9110.txt`/`rfc9111.txt`, already held — matches the report) |
| misroot | report §Pre-report checks; fleet `git status --porcelain` | `.scratch/run15-state.json` (M) and `.ufo/closure-kaidoku-r92.json` (??) pre-existing, carry no kake round-93 content; untouched |

Conformance defects (status-neutral, named in §6): no `w1-results.json` / no `WAVE-DONE`
(settlement rests on committed artifacts; L0 question filed at `.ufo/l0-questions.md:357`); four
seats filed no report (ScoutGround empty dir; CriticClaims, MutConditional, SentinelScope partial
receipts recovered to `w1/recovered-partial/`); seat-count drift (freeze text 12, dispatch 13);
the L1's first Gate block carries three wrong line spans and one 26-word quote (corrected by the
source-seat block, both kept, routed by the lane — corrections verified accurate in §3).

## 2. Per-claim re-check

### C1 — calibration (HOLD 2): self-assessment conformance, mismatches 20 → 0

Re-measured by this closure with the frozen counter over committed bytes:

```
python3 -B .ufo/waves/round-93/c93_selfassess.py --root . --revision 75effe7bbc1b77fbfcf80c09119c0680d9e224c9
→ C1v93 revision=75effe7bbc1b77fbfcf80c09119c0680d9e224c9 lessons=88 entries=81 rows=255
  criteria=39 mismatches=0 E1=0 E2=0 E3=0 E4=0 E5=0 pins=ok met=true   exit=0
python3 -B .ufo/waves/round-93/c93_selfassess.py --root . --revision 10ecbd1ade91d0721e87a9942a66a2b61d5ce8d5
→ C1v93 revision=10ecbd1a… lessons=87 entries=80 rows=255 criteria=39 mismatches=20
  E1=1 E2=8 E3=1 E4=4 E5=6 pins=ok met=false   exit=1
```

Both runs match the report and `controls/base-c1.txt` line-for-line. Self-test receipt is
committed evidence (not re-executed): `controls/ctl-c1-selftest.txt` — "selftest 5/5 planted
findings, exit 1 on planted, exit 0 on repaired", `selftest_exit=0`. Verdict: **calibration
improved** on the measured repo state (the E1–E5 repairs are real and enumerable); the instrument
is falsified as a calibration *proof* by the round's own ReviewC1 (R93-1…R93-6), which the lane
discloses and routes; the axis score stays 2 (HOLD) and no score move is claimed.

### C2 — freshness (HOLD 10), capability: conditional request evaluation (contract v1)

Re-measured by this closure:

```
python3 -B .ufo/waves/round-93/c93_conditional.py --root . --revision 75effe7bbc1b7… --work <scratch>
→ C2v93 revision=75effe7b… candidate=present hand=44/44 generated=120/120
  forgeries_refused=6/6 positive=admitted anti_table=ok population=ok seed=93 met=true   exit=0
  candidate_sha256=d3bac7de1c2d04fc355db795aebdf6012030ea5c5793d9362bc9cd8e0b8cac5e
python3 -B .ufo/waves/round-93/c93_conditional.py --root . --revision bb8012fe… --work <scratch>
→ C2v93 revision=bb8012fe… candidate=absent hand=0/44 generated=0/120
  forgeries_refused=0/6 positive=refused … met=false   exit=1
python3 -B scripts/conditional_eval.py --selftest
→ selftest 90/90   exit=0
```

All three match the report exactly; the candidate digest equals the report's `d3bac7de…` and the
SCORECARD capability row. Committed fixture-control evidence (not re-executed):
`controls/ctl-c2-fixtures.txt` — "selftest 7/7 fixtures scored as declared; drifted-reference
cases=4". Verdict: **freshness improved** (capability acquisition verified end-to-end by this
closure's own runs); the frozen population's gaps (9/40 reference mutants survive, two legal
input classes missed — R93-7/R93-8) are lane-recorded and routed; score stays 10 (HOLD).

### Axis harm

`git diff d838e744462c… 75effe7bbc1b7… -- SCORECARD.md` is purely additive: one Capabilities row,
two move-log rows (93), a round-93 claims section, a planned section. Axis cells at tip:
operability 10, freshness 10, calibration 2 — unchanged; depth/coverage/adjacency evidence
surfaces untouched. No owned axis harmed.

### Re-measured vs evidence-verified

- **Re-measured by this closure:** C1 counter (tip + base), C2 counter (tip + base),
  `conditional_eval.py --selftest`, SOURCES row count 207 → 213 (`grep -cE` over both revisions),
  SCORECARD diff, live RFC fetches + sha256 digests, quote substring checks, errata listings,
  census validate.
- **Evidence-verified (sibling gate/artifacts not executed, §Gate standard):** freshness-sweep
  gate — committed receipt `w1/ScribeC1Prose/sweep-sidecar-before-after.txt` records BEFORE
  re-pin exit 2 (`paths sidecar binding invalid: corpus/lessons/round-29.md:200`) and AFTER
  re-pin exit 1 with the pre-existing baseline miss (`~/projects` at `corpus/lessons/round-90.md:82`),
  matching the report; counter self-tests (receipts above); mutation battery (40 mutants, 31
  killed / 9 survived, `w1/recovered-partial/MutConditional/`); ReviewC1/ReviewC2 attack reports
  (committed files read; R93-1…R93-10 accepted as the round's own falsification record, not
  independently re-run).

## 3. Discernment spot-check (LEARNING.md, non-author)

Live re-open: `https://www.rfc-editor.org/rfc/rfc9110.txt` and `…/rfc9111.txt`, HTTP 200, 502 941
and 84 477 B, sha256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` and
`aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` — byte-identical to the
digests recorded in the lesson Gate and in S471–S476, so every cited line number was re-checked
in the same bytes the lane read.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| Admit §13.2.2 evaluation order (S471) | admit | live rfc9110.txt; quote exact substring of lines 6233–6234 (whitespace-normalized), 19 words ≤ 25 | agree | the MUST-evaluate-in-order sentence directly grounds the instrument's decision order (contract clauses 7–12); tier A spec is the right ground |
| Admit RFC 9111 §4.3.2 cache skip (S476) | admit | live rfc9111.txt lines 887–891; quote exact at 889–890, 13 words; §4.3.2 heading at line 866 | agree | grounds the `role: "cache"` skip verbatim |
| Admit §13.1.1 strong comparison (S472) | admit | live lines 5794–5795; quote exact, 15 words | agree | If-Match strong-comparison requirement verbatim |
| Admit §13.1.2 304-vs-412 by method (S473) | admit | live lines 5930–5931; seat's shortened 22-word quote exact | agree | the Gate's original 23-word rendering was 26 words (> rule) and the seat's shortening is faithful; correction verified |
| Admit §13.1.3 If-None-Match precedence (S474) | admit | live lines 5956–5957; quote exact, 13 words | agree | grounds the INM-over-IMS precedence rule |
| Reject: RFC-Editor errata pages as grounding row | reject | live fetch of both errata listings — bytes identical to the seat's recorded digests (`cec32fd1…`, `1df394f9…`) | agree | 9110 listing: 14 records (6 Verified / 2 Reported / 6 Rejected), none targeting §13.x or §8.8.3.x (sweep over all "Section X" mentions). 9111 listing: 4 records — 2 Reported (§3.5, §4.3.4), 1 Held for Document Update (§5.2.3), 1 **Rejected** quoting §4.3.2 (rejected 2024-01-16). Nuance: the Gate text mentions only the two Reported records; the fourth (Rejected) record does quote §4.3.2, but a rejected erratum carries no normative force, so the page still grounds nothing for this contract — verdict stands, nuance routed |
| Reject: secondary precedence explainer (tier inflation) | reject | not re-opened — reasoned reject with a defined flip | agree | the RFC text grounds the order directly at tier A; a secondary row would add no scoped ground the lane lacks |

Span corrections verified against live bytes: the Gate's original §13.2.2 span 6229–6231 does not
contain its quote (it carries the "lost update preconditions" rationale); the sentence sits at
6233–6234 — the source-seat correction is accurate, as are the §13.1.3 (5963–5966) and
§8.8.3.2-hyphenation corrections.

New-row re-open (SOURCES.md): **S471** — anchor verified (`§13.2.2 heading plain-text line 6222`
= "13.2.2.  Precedence of Preconditions"), fetch metadata (date/time, HTTP 200, 502 941 B, sha)
matches this closure's live fetch; its Gate quote is the 19-word admit verified above. S476's
anchor and quote likewise verified. Census over the registry: exit 0.

## 4. Trend verdicts (evidence)

- **expansion: improved.** `corpus/SOURCES.md` 207 → 213 rows (my grep over `10ecbd1a` and
  `75effe7b`); six new A-tier `spec` rows S471–S476; `corpus/knowledge/conditional-request-evaluation.md`
  present with provenance trio (E3 = 0 re-measured); capability row entered in SCORECARD;
  `corpus/README.md` §Round-93 frontier step present.
- **quality: improved.** C1 mismatches 20 → 0 re-measured by this closure; the sidecar re-pin
  restored the freshness sweep's line bindings (committed before/after receipt: exit 2 → exit 1);
  the new entry carries the source/verified-at/recheck trio. Limit recorded by the lane and
  endorsed here: the C1 counter is falsified as an instrument, so the quality gain is the
  measured repo state, not a verified counter.
- **discernment: unchanged.** No non-author spot-check existed at report time (owed to closure;
  supplied by this file and agreeing with every sampled decision). The lane's own discernment
  instruments did not improve: the C1 instrument is falsified (R93-1…R93-6), the C2 frozen
  population misses nine reference mutants and two legal classes (R93-7, R93-8), and the lesson's
  first Gate block carried the span/quote defects corrected by the source seat. The round records
  all of this honestly; grade unchanged.

## 5. Dispatch/complete digest (copied from `.ufo/watchdog.log`, mutable file)

```
2026-11-05T00:52:37-03:00 launch kake round=93 pgid=1825962 driver=hyaku-inline attempt=3
2026-11-05T00:53:14-03:00 lane-dead-no-report kake round=93; retry same round (hyaku-inline attempt=3: L1 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-93/kake.md)
2026-11-05T02:17:42-03:00 launch kake round=93 pgid=1991511 driver=hyaku-inline attempt=1
2026-11-05T02:18:16-03:00 lane-dead-no-report kake round=93; retry same round (hyaku-inline attempt=1: L1 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-93/kake.md)
2026-11-05T02:18:18-03:00 launch kake round=93 pgid=1995250 driver=hyaku-inline attempt=2
2026-11-05T02:18:51-03:00 lane-dead-no-report kake round=93; retry same round (hyaku-inline attempt=2: L1 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-93/kake.md)
2026-11-05T02:18:53-03:00 launch kake round=93 pgid=1996878 driver=hyaku-inline attempt=3
2026-11-05T02:19:33-03:00 lane-dead-no-report kake round=93; retry same round (hyaku-inline attempt=3: L1 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-93/kake.md)
2026-11-05T10:33:26-03:00 launch kake round=93 pgid=3763409 driver=hyaku-inline attempt=1
2026-11-05T11:11:14-03:00 complete kake round=93; hyaku-inline attempt=1
```

The resumed attempt inherited the earlier attempts' outputs, which the report discloses
item-by-item (wave files re-verified by re-running both counters at the current tip; ScribeC1Prose
late output committed `d838e744`; ScribeSources rows mirror-gated before append). Discarded: nothing.

## 6. Routed defects (the lane must fix next round)

1. **R93-1…R93-15** — the round's own routed list in `corpus/lessons/round-93.md` §Wave review and
   Routed; endorsed unchanged. Highest-weight: successor C1 counter (R93-1…R93-6) and C2 frozen
   population gaps (R93-7, R93-8).
2. **WAVE-DONE handoff gap** — no `w1-results.json`, no WAVE-DONE; settlement rests on committed
   artifacts; four seats (ScoutGround, CriticClaims, MutConditional, SentinelScope) filed no
   report and survive only as partial receipts under `w1/recovered-partial/`. Operator ruling
   requested at `.ufo/l0-questions.md:357` — status-neutral, operator-owned.
3. **Seat-count drift** — freeze text says 12 seats, dispatch carries 13 (disclosed; no predicate
   changed). Fix the freeze-vs-dispatch reconciliation next round.
4. **L1 Gate quote-span defects** — three spans wrong, one quote 26 words, in the lesson's first
   Gate block; the source-seat block beside it carries the corrections and this closure verified
   the corrections against live bytes. The defective block stays as written (append-only
   discipline); next round's Gate must run the quote verifier before commit.
5. **Freshness sweep baseline miss** — sweep exit 1 at tip with the pre-existing unannotated miss
   (`~/projects` at `corpus/lessons/round-90.md:82`); baseline drift owned by the lane,
   status-neutral; annotate or pin next round.

Operator note: SHONEN boxes 1, 3, 4 carry `[~]` with resolvable pointers and were re-checkable by
this non-author (box 1 via the E5 class re-measurement, box 3 via `conditional_eval.py --selftest`
90/90 re-run, box 4 via `w1/ConnectorScope.md`); box 2 stays `[ ]`. No `[x]` was written by anyone;
promotion remains operator-owned.
