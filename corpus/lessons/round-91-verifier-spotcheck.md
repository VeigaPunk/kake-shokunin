author: hyaku closure (non-author integrator, @m_zfl)
round: kake 91
date: 2026-11-04
report: .ufo/reports/round-91/kake.md
lane_base: 5b20af16661040f383e9e84f85b838619857cb14
lane_head: 5c46767019051ee042bc15febb2665f801ba4abd
freeze: f4fff130a52ae6de49af5de7d568d2ee320ebfb0

# Round 91 verifier spot-check — kake (hyaku closure, non-author)

I did not author this round and edited no lane-authored file. Every measurement
below was re-run on committed bytes with plain `git`/`grep`/`awk`/`wc`/`sha256sum`.
The lane's counters (`.ufo/waves/round-91/c91_defects.py`, `c91_reuse.py`) and the
shipped tool were **not executed**: their committed receipts were read, and each
receipt's printed revision was checked against the commit it names
(`PROTOCOL.md` §Gate standard, Closure consequence).

## Conformance results

- Report commits `7b65096d4e131a98a73d64324426ee9655caa13d` (`20:44:36 -0300`) and
  `962fdd8a387be6cdb83654e5778a896b2db2a0cc` (`20:49:47 -0300`), author
  `kake-shokunin` in both (`git log --format='%an %H' -- .ufo/reports/round-91/kake.md`).
  Both land before the driver completion line `20:52:50`. ✓
- Driver digest (copied from the closure prompt; `.ufo/watchdog.log` re-read and
  equal): `2026-11-04T19:53:22-03:00 launch kake round=91 pgid=29350
  driver=hyaku-inline attempt=1`; `2026-11-04T20:52:50-03:00 complete kake round=91;
  hyaku-inline attempt=1`. One attempt, no `lane-dead` line. ✓
- `## SHONEN` appears once with exactly four box lines (`[~]`, `[ ]`, `[~]`, `[~]`,
  no `[x]`), matching `SHONEN.md`'s four boxes; `git diff 5b20af16 5c467670 --
  SHONEN.md` is empty. ✓
- Every cited lane hash resolves and is an ancestor of `master`
  (`git merge-base --is-ancestor <full> master`): `f4fff130`, `cdc6c1df`, `5c467670`
  — 3/3 ok. ✓
- `jj-lane.sh state` → `branch=master local=5c467670 remote=5c467670 ahead=0
  behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` prints
  nothing; `ls-remote origin refs/heads/master` → `5c467670…`. No uncommitted round
  work, pushed. ✓
- Prompt `.ufo/prompts/kake-round-91.md`: `diff` of lines 1–140 against
  `templates/round-prompt.md` shows only `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/
  `{{AXES}}` substitutions; the round contract and all five child-lane items are
  carried verbatim, then addendum §6 and scratch-discipline §7. ✓
- Wave: `w1-spec.json` `maxLanes=13`, 13 items — scout 2, executor 5, scribe 1,
  reviewer 2, mutation-tester 1, critic 1, connector 1; attack seats 4/13 = 31 %,
  connector 1. Nine seat `.md` files exist; `ScoutGround`, `ExecReuseStubs`,
  `ConnectorScope` have no directory content and `ScoutSources` holds only
  `quote-check.py`. ✓
- **Defects (status-neutral, routed below).** (1) `c91_defects.py` — the C1
  counter this round's calibration claim rests on — has **no registry row** in
  `SKILL.md` (`grep -c c91_defects SKILL.md` → `0`), while rounds 89 and 90
  registered `c89_defect_queue` and `c90 defects`; `PROTOCOL.md` §Gate standard
  Delivery grades no gate conformant without one. (2) The report's and `LOG.md`'s
  `controls ok 18/18` has **no committed receipt**: `grep -rn "controls ok 18/18"
  .ufo/waves/round-91/` prints nothing; the only tallies on disk are `9/9`,
  `11/14` and `14/14`. (3) The Tooling lines say "network limited to the two RFC
  GETs" while `corpus/lessons/round-91.md` states **no live GET completed** this
  round. (4) S469 records `opened 2026-11-04`, but `CORPUS.md` rule 1 writes a row
  only after the source is opened in the round that writes it; the lesson's honest
  limit says the body is the round-90 retained copy re-hashed.

## Per-claim re-check

| Claim | Reported | Re-check (mine) | Mode |
|---|---|---|---|
| C1 calibration — R90-A, R90-B, R90-C close | `open=3 closed=0 met=false` exit 1 at base → `open=0 closed=3 met=true` exit 0 at `cdc6c1df` | Receipts match line for line (`controls/base-c1.txt` `revision=5b20af16…`, `exit=1`; `controls/after-c1-carrier.txt` `revision=cdc6c1df…`, `exit=0`; `controls/freeze-state-c1.txt` `open=1 closed=2`, only B). Counter byte-identical freeze→carrier (`git diff --stat` empty). **R90-B and R90-C verify; R90-A does not** — one of the three classes it names remains admitted (below). | evidence-verified (B, C) + falsified (A) |
| C2 operability — stored-response reuse decision instrument | `candidate=absent … met=false` exit 1 at base → `hand=45/45 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok met=true` exit 0 at `cdc6c1df` | Receipts match; tool 433 lines, stdlib only (`json`, `re`, `sys`), `--selftest` 45/45; absent at base; `candidate_sha256 5004657d…ba9ad299` equals `git show cdc6c1df:scripts/stored_reuse.py \| sha256sum`; the pins digest `033b6103…95084c8` is enforced inside `met`; contract 21 numbered clauses; counter frozen freeze→carrier. Independent seat evidence: ReviewReuse 53/0, MutReuse 17/17 shipped mutants killed, ExecReuseTrial 18 surfaces / 36-0 agreement / seeds 1–3 `met=true`. | evidence-verified + re-measured |
| Counts | rows 205→206 (A 180→181), knowledge `.md` 78→79, census exit 0, 29→30 × W04 | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 205, 206; tier-A `awk` filter → 180, 181; `git ls-tree -r --name-only <rev> -- corpus/knowledge \| grep -c '\.md$'` → 78, 79; `sources-census.sh validate --root … kake` → exit 0, `kake ok`, 30 × W04 (S469 is the third rfc9111.txt scope). | re-measured, matches |

**C1, re-derived without the counter.**

- *R90-B closes.* `.ufo/waves/round-91/integration/mutation-tip.txt` line 1 reads
  `gate_sha256=d7bca38ec146727087a2d2e37a64c5154214e2dd069553fb5594372d2064b65e
  mutants=34 killed=20 survivors=14 met=true`; the file holds 34 `M<nn>` lines, 20
  `-> killed`, 14 `-> survived`, and
  `git show cdc6c1df:scripts/cache_key_conformance.py | sha256sum` is exactly
  `d7bca38e…64b65e`. The seat's run log (`w1/ExecMutationTip/run.log`, 35 lines,
  per-mutant `killed/survived rc=… 38s`) shows a real execution.
- *R90-C closes.* `.ufo/waves/round-90/controls/run_controls.sh` at the carrier:
  line 14 `LANE=${LANE:-/home/…/kake-shokunin}`, line 42
  `INHERITED=.ufo/waves/round-90/inherited/baseclean.out`, line 74
  `cp "$LANE/$INHERITED" "$D/baseclean.out"`; no lane-root copy. Replay receipt
  `controls/replay-tip.txt` line 1 `revision=f4fff130… exit=0 controls ok 9/9`,
  `git diff --name-only f4fff130 cdc6c1df -- .ufo/waves/round-90/` empty.
- *R90-A does not close.* The freeze names R90-A as three admitted classes — "a
  stale receipted revision, a case-variant token and a receipt with no execution".
  Item A's frozen battery (`c91_defects.py` line 128,
  `want = {"FA": ["B"], "FB": ["B"], "FC": ["C"], "FD": []}`) tests the first two
  plus a print-success script, which is R90-C's class; **no fixture carries a
  correctly digested receipt with no execution**. The round's own committed
  forgery shows the class is still admitted: `w1/ReviewC1/fixtures/forge-a2.txt`
  prints `C1v91 revision=11cb9a91… items=3 open=0 closed=3 met=true` and
  `exit=0` for "correct digest, fabricated lines, no execution", and item B
  (lines 196–213) checks only the first-line form, the digest against the gate
  blob, the `N≥20 / K≥18 / S==N−K` floors and the count of distinct `M<nn>`
  tokens — nothing ties those lines to a run. The report's C1 cell discloses this
  ("ReviewC1 reached `met=true` with a fabricated receipt"), and the round states
  both claims are measured on frozen predicates and **not admitted**; the claim
  sentence itself is what does not verify.

**C2, re-derived without the gate.** `c91_reuse.py` lines 48–49 pin
`PINS_SHA = 033b6103…95084c8` and line 581 folds `pins_ok`, the five refusals,
`hand_ok == len(cases)` and `gen_ok == a.generated` into `met`; the receipt's
`pins_digest` equals that constant. Contract clause count
(`grep -nE '^[0-9]+\.' c2-contract.md` under "## Field reading") = 21; hand cases
`c.append(H(` 36 + `c.append(R(` 9 = 45. ReviewReuse's committed
`w1/ReviewReuse/subject-run.txt` last line `SUMMARY subject agree=53 disagree=0
protocol_notes=0 of 53`; `w1/ExecReuseTrial/compare.json` = `{"agree": 36,
"disagree": 0, "rows": []}` over 18 surfaces; `seed-1/2/3.out` each read
`met=true`. Wording caveat: the cases are named semantically, not clause-tagged —
"clause-tagged hand cases" is loose, and clause 3 has no case (disclosed in
`w1/ReviewReuse.md` F2).

## No-harm check

`git diff --diff-filter=D --name-only 5b20af16 5c467670` prints nothing: 0 files
deleted. `git diff 5b20af16 5c467670 -- corpus/SOURCES.md` is one added row, no
content line removed. `SCORECARD.md` gains only the round-91 sections; no axis
score moved (operability 10, freshness 10, calibration 2 — all HOLD, as the round
states). `SHONEN.md` untouched. No owned axis is harmed.

## Spot-check (`corpus/lessons/round-91.md` `## Gate`; 4 admits, 2 rejects)

The retained body was re-opened at the tip: `.ufo/waves/round-91/L1/src/rfc9111.txt`
84 477 B, sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`
— equal to the row's anchor, the lesson table and the knowledge entry.

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| RFC 9111 §5.2.1 request directives (S469) | admit, A, scope-limited | `rfc9111.txt` heading line 1111 `5.2.1.  Request Directives`; lines 1113–1114 "This section defines cache request directives.  They are advisory; caches MAY implement them, but are not required to." | agree | Verbatim at the cited lines, 17 words ≤25; "advisory" is the right ground for a contract that treats `no-cache` as a client preference rather than a MUST. |
| §5.2.1.2 `max-stale` | admit, A | lines 1137–1138 "The max-stale request directive indicates that the client will accept a response that has exceeded its freshness lifetime." | agree | Verbatim (20 words); grounds `serve-stale` and the `max-stale=N` bound the contract implements. |
| §4.2.4 serving stale | admit, A | lines 790–791 "A cache MUST NOT generate a stale response if it is prohibited by an explicit in-protocol directive" | agree | Verbatim (18 words); the MUST is what `must-revalidate-fail` implements, and the lesson keeps it on the forbidden side, not the permitted one. |
| §4.2.1 first-match lifetime | admit, A | line 656 "and using the first match:"; lines 658–659 "If the cache is shared and the s-maxage response directive (Section 5.2.2.10) is present, use its value" | agree | Verbatim; the quote spans 658–659 (the lesson cites 658, one line short of the sentence end — harmless). The order s-maxage → max-age → Expires−Date → null is what clause 9 implements. |
| "a second row for §4.2.3 age arithmetic" | reject (row candidate) | `corpus/SOURCES.md:209` S462 — `httpwg.org/specs/rfc9111.html#age.calculations`, scope "Conservative current-age arithmetic on supplied timestamps only", status `mined`, `used-by corpus/knowledge/cache-current-age.md`, reopened 2026-11-04 | agree | S462 already owns §4.2.3 on the same RFC; the new contract delegates the arithmetic to it, so a second row would be a within-scope duplicate (CORPUS rule 2 append-only, no row quota). The stated flip — a contract that re-specifies the age equation — is the right condition. |
| "the contract's `Date`/`Expires` integer convention is RFC 9111's own form" | reject (proposition) | `rfc9111.txt` lines 664–667: "use its value minus the value of the Date response header field (using the time the message was received if it is not present, as per Section 6.6.1 of [HTTP])" | agree | The RFC requires an HTTP-date and tolerates a missing `Date`; the contract requires epoch integers and refuses a missing `Date`. That is an adapter convention, and the knowledge entry says so (§"Everything here is arithmetic on integers"). |

New `corpus/SOURCES.md` row re-opened: **S469**. The lesson's `## Gate` quote is
17 words (≤25) with location `§5.2.1 line 1113–1114`; every anchor cell resolves
at the stated plain-text lines (1111 heading / 1113–1201, 652 / 654–684, 784 /
786–799, 214–217); the row is tier A `spec`, `status=mined`, `used-by` names the
new knowledge entry, `recheck 180d`. No tier inflation. I also re-checked nine
quotes from the knowledge entry as raw substrings at their cited lines — 1113,
1128, 1142, 1201, 214, 656, 669, 786, 795 — 9/9 present.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
exited 0 with `kake ok …/corpus/SOURCES.md` and 30 × W04; the base had 29 and
S469 is the third scope on `www.rfc-editor.org/rfc/rfc9111.txt`.

## Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| calibration (C1, lowest owned non-retired axis) | **unchanged** | R90-B and R90-C close on committed bytes (mutation score 34/20/14 against the real gate blob; replay re-pointed and `9/9`), but R90-A does not: the third class the claim names — a receipt with no execution — is still admitted, proven by the round's own `forge-a2.txt` (`met=true`, `exit=0`), and the frozen item-A battery has no fixture for it. Score stays 2 HOLD, as the lane records. |
| operability (C2, capability acquisition) | **improved** | A new instrument exists and runs: `scripts/stored_reuse.py` 433 lines, stdlib only, `--selftest 45/45`, absent at base, `candidate_sha256` equal to the committed blob; the frozen counter reads `45/45 120/120 5/5 anti_table=ok population=ok met=true` at the carrier with the pins digest enforced; an independent 53-case review computed from the contract alone agrees 0 disagreements; the 18-surface recorded trial agrees 36/36 and flips reuse→revalidate at +30 d. The capability row is in `SCORECARD.md` and both registry rows are in `SKILL.md`. Score stays 10 HOLD. |
| freshness (not claimed this round) | unchanged | No drift claim was made; S469 carries `recheck 180d` and the knowledge entry a dated `recheck`; no admitted row was rewritten (`SOURCES.md` diff is one added line). The `opened 2026-11-04` provenance gap on S469 is routed, not scored. |

## Trend verdicts

- **expansion: improved.** `corpus/knowledge/` 78 → 79 `.md` files with
  `stored-response-reuse.md` (289 lines) on ground the coverage map did not hold;
  `corpus/README.md` gains the r91 map row and a Round-91 frontier section;
  registry 205 → 206 (tier A 180 → 181) with S469 `mined` and cited; census clean
  at both ends.
- **quality: improved.** Depth and freshness: a 289-line entry whose 20 located
  quotes are raw substrings (9 re-verified here), an append-only registry row, and
  a tool with a 45/45 selftest. Operability: the tip gate finally carries a
  mutation score (34 mutants, 20 killed), the control harness was corrected five
  times (Mistakes 1–4 before the freeze, `w1/ExecReplayC.md` F1–F3/F5 after), and
  an independent reviewer found 0 disagreements in 53 contract cases. Offsets, for
  the record: the `controls ok 18/18` tally has no committed receipt, the report's
  "every finding is routed" overstates (four of ReviewC1's routed findings —
  battery membership vs exact set, FC never reaching the replay, the literal
  `selftest 6/6` denominator, `K==N` without label assertions — are not in
  `corpus/lessons/round-91.md` §Routed), and clause 3 has no hand case.
- **discernment: improved.** The round's own attack seats falsified both frozen
  counters and the lane published the falsifications, declared both claims
  measured-but-not-admitted, and disclosed the no-live-GET limit instead of
  dressing the retained body as a fresh fetch. The outside spot-check agrees on
  all six sampled gate decisions and on the new row's quote and anchor. Offset:
  the C1 claim sentence claims a closure its own frozen battery does not cover —
  the disclosure sits in the same cell, so this is a claim-wording defect, not a
  suppressed finding.

## Routed defects (lane fixes next round)

- **K91-1.** R90-A's "receipt with no execution" class is still admitted
  (`w1/ReviewC1/fixtures/forge-a2.txt` → `met=true`). Bind item B to a committed
  execution artifact (per-mutant log bound by digest, re-hashed at the measured
  revision) and add that fixture to item A's battery. Until then the C1 claim
  sentence must not say R90-A closes.
- **K91-2.** `c91_defects.py` has no registry row at the lane's registry home
  (`SKILL.md`), which §Gate standard Delivery requires; rounds 89–90 registered
  their counters.
- **K91-3.** `controls ok 18/18` is prose only — commit the harness's final tally
  line (a numeric claim needs its observed output, not a re-runnable command
  alone).
- **K91-4.** Item A's battery asserts membership, not the exact open set or the
  reason string (`want[name][0] not in got`), and FC is refused by the static
  line-count pre-check so the replay never runs for it; the selftest denominator
  is the literal `6` while eight checks run (`c91_defects.py:276`).
- **K91-5.** Item C's replay counts the checks it runs (`K == N >= 9`) without
  asserting the nine expected labels, so any nine checks pass.
- **K91-6.** C2 counter: a candidate reaches `met=true` by importing the counter's
  reference through an absolute path (`anti_table` has no frozen subject), 9 of 10
  counter mutants survive, and five clause variants have no case; add the five
  variants MutReuse names and a frozen anti-table subject.
- **K91-7.** S469's `opened 2026-11-04` rests on the round-90 retained body
  (CORPUS rule 1 asks for the source opened in the writing round). Next round:
  re-fetch, record status/bytes/sha256, or state the provenance in that round's
  lesson.
- **K91-8.** Report and `LOG.md` Tooling lines say "network limited to the two RFC
  GETs"; the lesson says no live GET completed. Correct the wording in the next
  round's LOG (append-only).
- **K91-9.** `scripts/stored_reuse.py` re-implements the Cache-Control directive
  grammar `scripts/cache_control_effective.py` (r86) already reads — compose it
  (the round's own R91-4).
- **K91-10.** Carried: `.ufo/waves/round-90/controls/run_controls.sh` is still red
  under `ONLY=all` (`controls ok 11/14`, reader defect) — R91-3 remains open; the
  round-91 harness fix lives only in the round-91 file.

Operator note (promotion is operator-owned): `SHONEN` boxes 1, 3 and 4 carry
resolvable pointers a non-author can check; box 2 stays `[ ]` on the round-47
receipt gap the ledger records, so the checklist is not yet fully checkable by a
non-author.
