author: hyaku closure (non-author integrator, @m_zfl)
round: kake 88
date: 2026-11-04
report: .ufo/reports/round-88/kake.md
lane_base: f4479c14813037ad993a49a3dee4028763470f7a
lane_carrier_head: 55d67f15f7a58fb49ca32a31b5c63ae716e1c38a
lane_head_before_this_section: 741fb728b2e22c7a35288d9c645e0dd71d9a0e6b

# Round 88 verifier spot-check — kake (hyaku closure, non-author)

Re-measurements below were run by this integrator on committed bytes and, for the
two shipped tools only, through stdin on payloads this integrator wrote. Lane-owned
counters and gates (`c88_defect_queue.py`, `c88_vary.py`) were **not executed**;
their committed receipts were read and their revision bindings checked
(`PROTOCOL.md` §Gate standard, "Two evidences", Closure consequence). No evidence
pointer here depends on `/fast/scratch` or any other ephemeral directory. I am not
the author of this round and edited no lane-authored file.

## Conformance results

- Report commit: `fe3e14d7168ae71b0a92f6ec8edb405c0ee277ce`, author
  `kake-shokunin <kake@shokunin.local>`, `2026-11-04 16:38:01 -0300`, path
  `.ufo/reports/round-88/kake.md`. The lane tip it cites, `741fb728`, is
  `16:37:27 -0300`, so the report lands after the cited lane commit and before
  the driver completion line (`16:39:23`). ✓
- Driver digest (copied from the dispatched prompt; `.ufo/watchdog.log`
  lines 2432/2448 agree, mutable log not relied on further):
  `2026-11-04T15:39:05-03:00 launch kake round=88 pgid=537599 driver=hyaku-inline attempt=1`;
  `2026-11-04T16:39:23-03:00 complete kake round=88; hyaku-inline attempt=1`. ✓
- `SHONEN` heading present with one line per box (`SHONEN.md` at `741fb728`
  carries 4 boxes; the report carries 4 lines, `[~]`, `[ ]`, `[~]`, `[~]`; the
  lane wrote no `[x]`). ✓
- Cited lane commits, each tested with
  `git -C kake-shokunin merge-base --is-ancestor <hash> refs/heads/master`
  (branch ref, never `@{u}`): `4f8945ea` ✓, `80637397` ✓, `52e41d2d` ✓,
  `add7e49b` ✓, `f60a852a` ✓, `55d67f15` ✓, `edcb2980` ✓, `741fb728` ✓. All
  exist and are ancestors of `master`. ✓
- Push state: `scripts/hyaku/jj-lane.sh state …/kake-shokunin` →
  `branch=master local=741fb728… remote=741fb728… ahead=0 behind=0 head=detached
  tracked=0 untracked=0`; `git status --porcelain` in the lane → empty;
  `git ls-remote origin refs/heads/master` → `741fb728b2e22c7a35288d9c645e0dd71d9a0e6b`. ✓
- Prompt `.ufo/prompts/kake-round-88.md` (tracked, commit `a281f037`, author
  `kake-shokunin`) renders `templates/round-prompt.md`: substituting
  `{{LANE}}=kake`, `{{ROUND}}=88`, `{{FLEET_ROOT}}=/home/vgpnk/Projects/shokunin`
  leaves **138 of the template's 140 lines byte-identical**; the two differing
  lines are exactly the `{{LANE}}-repo` and `{{AXES}}` substitutions
  (`Working dir: …/kake-shokunin`, `operability + freshness (web properties and
  publishing)`). §6 addendum follows. The five child-lane items are present:
  report path and filename (`§4`), commit-before-report ordering (`§5` + addendum
  pre-report gate), `SHONEN` heading (`§4`), commit-hash citation rule (`§4`,
  `§5`), lane write scope (addendum item 3, `…/kake-shokunin`). ✓
- Wave shape: `w1-spec.json`/`w1-results.json` both name 14 seats; results carry
  14 non-empty outputs; roles scout 2, executor 4, scribe 3, reviewer 2, critic 1,
  mutation-tester 1, connector 1; attack 4/14 = 28.6 % (≥25 %); `w1.ready` and
  `w1.ready.dispatched` (`2026-11-04T15:52:15`) present, `validator.err` empty,
  `wave-done-receipt.txt` records WAVE-DONE before integration. ✓
- Misroot sweep: fleet-root `git status --porcelain` shows only orchestrator
  `.scratch/` state, a sibling's `round-84/kama.md` edit, a pre-existing `after`
  file and `tsukuroi`'s census temp file — none attributable to this lane; the
  lane repo itself is clean. ✓
- Status-neutral defects (never marker predicates; detailed under **Routed
  defects**): (a) report/SCORECARD/lesson say the integrated selftest is `22/22`
  while the cited receipt prints `35/35` (plus 61 cache fixtures); (b) the
  report's Gate summary says "one admit and three rejects" while the cited
  lesson carries two admits and two rejects; (c) the "re-run at `edcb2980`"
  sentence has no committed receipt and its command writes under `/fast/scratch`;
  (d) the `1,577` controls count names no revision (it is exact only at
  `f60a852a`; at filing HEAD it is 1590); (e) freeze v3 landed after dispatch
  (15:52:15 → 15:58:05) while the wave was live, disclosed in the contract
  errata and lesson; (f) the round's four mistakes live under `## L1 mistakes`,
  while `CORPUS.md` names `## Mistakes` for a round's mined mistakes.

## Per-claim re-check

### C1 — calibration (lowest owned non-retired axis, 2 HOLD): three routed r87 defects

Plain measurement, base `f4479c14813037ad993a49a3dee4028763470f7a` vs HEAD
`741fb728b2e22c7a35288d9c645e0dd71d9a0e6b`:

- **R1 ledger companion.** Base `git ls-tree -r --name-only f4479c14 corpus/knowledge/ | grep -i gate`
  → `gate-agreement-ledger.json`, `gate-status-ledger.md` (no companion). HEAD adds
  `gate-agreement-metadata.md`, which opens with the full trio
  (`source:`, `verified-at:`, `recheck:`) and quotes
  `sha256 ef58f9092c32179de6e680ab782cfb29900d9b5b34cfbfcb76b316a144c3d506`.
  `git show f4479c14:corpus/knowledge/gate-agreement-ledger.json | sha256sum`
  → the same digest; the frozen copy re-hashes to it. The ledger bytes are
  unchanged. ✓
- **R2 diagnostic type.** Base `git show f4479c14:scripts/cache_current_age.py |
  grep -n 'must be an integer'` → `34: raise ValueError(f"{key} must be an
  integer, not boolean")` (the word *boolean* for every type). HEAD line 34 maps
  the JSON type. Independent stdin probes (this integrator, not the lane's
  counter): `{"date_value":7.0,…}` → exit 1,
  `invalid_input: date_value must be an integer, not float`; `date_value: true`
  → `… not boolean`; the valid payload → exit 0 with the six integer terms
  `current_age:30`, identical to the frozen base tool on the same three payloads
  (byte-identical stdout, exit 0/0/0). ✓
- **R3 recheck path.** Base `git show f4479c14:corpus/knowledge/cache-current-age.md | grep -n recheck:`
  → names `/fast/scratch/hyaku/kake-r87/L1` and `TMPDIR=`. HEAD's single
  `recheck:` line names checklist item 6 instead; item 6 is
  `TMPDIR=$(mktemp -d) python3 -B scripts/cache_current_age.py --selftest`.
  `git diff f4479c14 741fb728 -- corpus/knowledge/cache-current-age.md` is exactly
  one replaced metadata line plus one appended checklist item. ✓

Evidence-verified, not executed: `controls/base-c1.txt` →
`C1v1 revision=f4479c14… items=3 open=3 closed=0 met=false`, exit 1;
`controls/after-c1-carrier.txt` →
`C1v1 revision=55d67f15… items=3 open=0 closed=3 met=true`, exit 0;
`controls/c1-selftest.txt` → `selftest: 11/11 passed`, exit 0. Frozen instrument
`c88_defect_queue.py` unchanged from v2 to carrier (MutReader §1).

Result: **met, re-measured 3→0**. Score held at 2; no decision-accuracy credit.

### C2 — freshness (10 HOLD): conservative Vary-match reader (capability)

Plain measurement on committed bytes:

- Before `f4479c14`: `git cat-file -e f4479c14:scripts/vary_match.py` → fatal,
  path absent. Base counter receipt `controls/base-c2.txt`:
  `frozen=0/20 random=0/200 met=false`, exit 1.
- After `55d67f15`/`741fb728`: `git show 741fb728:scripts/vary_match.py | sha256sum`
  → `fdceef474e618d6664c15333cba6a1fa136fbc44f2791bbbdbf92d234fb287d6` (294
  lines), equal to the claimed candidate hash and to
  `tool_sha256` in `controls/after-c2-carrier.txt`
  (`frozen=20/20 random=200/200 met=true`, exit 0,
  `cases_sha256 c461cbd8…`, `random_sha256 52714a5f…`).
- Frozen case set: `git show 741fb728:.ufo/waves/round-88/vary-cases.json | jq length`
  → **20**. Seeded population: 200 generated cases inside `c88_vary.py`
  (`RANDOM_N = 200`, seed `88_088`), digest `52714a5f…` in both the base and
  after receipts. `controls/frozen-identity-carrier.txt` is empty (v3 → carrier
  unchanged). ✓
- Constants: `controls/ctl-c2-constant-{match,mismatch,invalid}.txt` carry the
  committed `cases_sha256` and the disclosed scores 7/20+67/200, 9/20+109/200,
  4/20+24/200; `controls/c2-selftest.txt` prints `selftest: 17/17 passed`, exit 0.
- Independent behavioral probes (this integrator's own payloads, not the lane's
  case file): 7/7 agree with the declared profile — `Vary: *` → `mismatch`;
  case-insensitive field names → `match`; one-sided absence → `mismatch`;
  both-absent → `match`; value case-fold → `mismatch`; empty `Vary` and trailing
  comma → exit 1 `invalid_input`. Trailing-LF members `accept-encoding\n` and
  `*\n` are refused with exit 1, matching `controls/diagnostic-lf-probe.txt`.
- Second implementation (evidence verified, not executed): `w1/ReviewReader/indep.py`
  scores 19/20 + 187/200 spec-faithful and 20/20 + 200/200 with the declared
  adapter profile (`receipts/c88-score-indep-default.json`,
  `…-profile-mode.json`) — the 1 + 13 differences are the adapter labels the
  round discloses (R88-3). Mutation battery: 21 single-point mutants,
  **15 killed / 6 survived** (`w1/MutReader.md` §3).
- Domain trial: `w1/ExecTrial/capture.json` records one public `GET
  https://ds4cc.com/` → HTTP 200, 78,897 B, `vary: Accept-Encoding`,
  `credentials_or_cookies_sent: false`; the four retained payloads replay
  `match`/`mismatch`/`match`/`invalid_input`, exits 0/0/0/1
  (`controls/integrated-trial.txt`). One identical-side observation is not
  claimed as discriminating, and neither does this file claim it.

Result: **met, bounded capability acquired**. The counter's false-green paths are
disclosed and routed (R88-1…R88-7), not repaired after scoring; the shipped
reader's arithmetic was not in scope. No whole-corpus no-harm claim.

Lane-owned gates (C1 counter, C2 counter) were **evidence-verified, never
executed**; their receipts name the revisions measured (`f4479c14` base,
`55d67f15` carrier) and the frozen bytes are confirmed unchanged
(`controls/frozen-identity-carrier.txt`).

## Sources & frontier re-check

- `git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`:
  `f4479c14` = **200**, `741fb728` = **201**; `git diff` adds exactly one row and
  edits none. ✓
- `git ls-tree -r --name-only <rev> -- corpus/knowledge | grep -c '\.md$'`:
  `f4479c14` = **74**, `741fb728` = **76** (two new `.md`: `vary-matching.md`,
  `gate-agreement-metadata.md`). Only the former is claimed as domain expansion. ✓
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin kake` → exit **0**, 25 × `W04`
  (S033…S463), last line `kake ok …/corpus/SOURCES.md`; `controls/census-before.txt`
  carries 24 × `W04`, `controls/census-final.txt` 25. The S463 increment is the
  disclosed third scoped row for the shared `httpwg.org/specs/rfc9111.html` URL. ✓
- New row S463: 11 columns, tier `A`, kind `spec`, status `mined`, `opened
  2026-11-04`, `recheck 180d`, `used-by corpus/knowledge/vary-matching.md`
  (exists), anchor `RFC 9111 June 2022 section 4.1`. ✓
- Live source re-open (this integrator, 2026-11-04):
  `GET https://www.rfc-editor.org/rfc/rfc9111.txt` → 84,477 B, sha256
  `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`, byte-identical
  to `w1/ScribeLesson/receipts/rfc9111.txt`. The MUST NOT sentence sits at txt
  lines 528–534; the wildcard sentence ("A stored response with a Vary header
  field value containing a member `"*"` always fails to match.") at 555–557;
  `§4.1` also carries the absence rule and the three permitted transformations.
  `GET https://www.rfc-editor.org/rfc/rfc9110.txt` → 502,941 B, sha256
  `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`;
  `Vary = #( "*" / field-name )` at line 5675; §5.6.1.2 at 1695–1697. ✓
- `corpus/knowledge/vary-matching.md` opens with the provenance trio and cites
  S463; its blockquoted spans are raw substrings of the retained
  `w1/ScribeVary/rfc9111.html` (sha256 `999f4013…`) at line 269, re-checked with
  Python `in` over the committed body. ✓

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | **improved (bounded)** | C1 re-measured 3→0 from base bytes; the three r87 routed defects close; score held 2, no decision-accuracy credit. Bounded to the four defect conjuncts the counter can read. |
| freshness | **improved (bounded)** | C2 capability absent→present; committed predicate 20/20 + 200/200 reuse-verified, 15/21 mutants killed, second implementation and one live capture; score held 10 (saturation). Axis-fit is a bounded capability move, as in r86/r87. |
| operability | **unchanged** | Under `scripts/` only one diagnostic line in `scripts/cache_current_age.py` changed and `scripts/vary_match.py` was added; the tool's 61-fixture selftest receipt stays green and its arithmetic is byte-identical to the frozen base on three payloads. No other script or the round-87 instrument is touched. |

No owned axis harmed. `git diff --name-only f4479c14 741fb728` outside
`.ufo/waves/round-88/` is exactly: `LOG.md`, `SCORECARD.md`, `SKILL.md`,
`corpus/README.md`, `corpus/SOURCES.md`,
`corpus/knowledge/{cache-current-age.md,gate-agreement-metadata.md,vary-matching.md}`,
`corpus/lessons/round-88.md`,
`scripts/{cache_current_age.py,vary_match.py}` — all declared, all additive except
the one replaced metadata line and the one diagnostic line.

## Spot-check table (LEARNING.md discernment, from `corpus/lessons/round-88.md` `## Gate`)

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| RFC 9111 §4.1 match rule as the ground of the new Vary-match row (S463) | admit, tier A, scope-limited | live `GET https://www.rfc-editor.org/rfc/rfc9111.txt` (84,477 B, sha256 `aeb52adb…`) and retained `w1/ScribeVary/rfc9111.html` (`999f4013…`) | **agree** | The Gate's 24-word quote ("the cache MUST NOT use that stored response without revalidation unless all the presented request header fields nominated by that Vary field value match") is byte-exact at txt 528–534, and §4.1 defines the match rule and the three transformations. Tier A (IETF spec) is right for this scope; the entry claims only field-match semantics, not reuse. |
| RFC 9110 §12.5.5 `Vary` grammar as the member-shape ground | admit, tier A | live `GET https://www.rfc-editor.org/rfc/rfc9110.txt` (502,941 B, sha256 `21c1cdce…`) | **agree** | `Vary = #( "*" / field-name )` is byte-exact at line 5675; it grounds the member alphabet only, which is all the row claims. |
| "the C2 counter's 220-case pass shows the reader implements RFC 9111 §4.1" | reject (proposition) | same §4.1 sentence plus the round's own `w1/CriticClaims.md` §2.1/2.2 and `w1/ReviewReader.md` §4b | **agree** | The sentence is a precondition on reuse, not a conformance procedure; the counter scores a published oracle and a table keyed on the committed seed or an oracle-import stub also reaches `met=true`. The entry's scope is correctly narrower. |
| "an empty `Vary` value must be refused" as an RFC requirement | reject (proposition) | live `GET https://www.rfc-editor.org/rfc/rfc9110.txt`, §5.6.1.2, lines 1695–1697 | **agree** | The text says "A recipient MUST parse and ignore a reasonable number of empty list elements"; refusal is this lane's adapter convention (frozen case 14), and the entry now declares it as adapter, not RFC. |
| New `corpus/SOURCES.md` row S463 (≤25-word quote check) | registry write | row at `741fb728`; live RFC 9111 text above | **agree** | 11 columns; tier `A`, kind `spec`, `mined`, `opened 2026-11-04`, `recheck 180d`; `used-by corpus/knowledge/vary-matching.md` exists; its `teaches` sentence is grounded in §4.1 (reuse only when every nominated field matches; wildcard never matches; one-sided absence fails). |

Gate sample coverage: **2 admits and 2 rejects, all four agree**. The report's
`Sources & frontier` paragraph describes this table as "one admit … three
rejects"; that summary is stale against the committed lesson (the third reject
exists only in `w1/L1/round-88-draft.md`) — the decisions themselves are sound.

## Trend verdicts (closure)

- **expansion: improved** — one admitted knowledge entry on ground the coverage
  map did not hold (`corpus/knowledge/vary-matching.md`, §4.1 match semantics)
  citing mined A-row S463; SOURCES 200→201 and knowledge `.md` 74→76 re-derived;
  the SCORECARD capability row enters in the same round. The provenance
  companion earns no expansion credit and the round does not claim it.
- **quality: improved (bounded)** — the reader is verified, not asserted: the
  committed counter is 20/20 + 200/200 (`frozen-identity-carrier.txt` empty), a
  21-mutant battery kills 15, a second implementation agrees 19/20 + 187/200
  spec-faithful (20/20 + 200/200 under the declared profile), one real capture
  replays, and this integrator's own 7/7 probes agree. The three r87 defects
  close with a behavioural check and a minimal diff. Nothing admitted this round
  fails its re-check. Bounded by the disclosed counter limits R88-1…R88-7.
- **discernment: improved** — this outside spot-check agrees with the gate on
  both sampled admits and both sampled rejects; the lane's own attack seats
  falsified its instruments in-round (seed table and oracle import both reach
  `met=true`; the counter accepts a trailing LF the shipped reader refuses; a
  §5.6.1.2-faithful reader fails the frozen set) and the round routed the limits
  instead of hiding them. The report's stale Gate summary is a bookkeeping slip,
  not a wrong decision, and is routed below.

## Routed defects (lane fixes next round; status-neutral)

- **R88-A (report accuracy, numeric).** The report, `SCORECARD.md` and the lesson
  say the integrated `vary_match` selftest is **22/22**; the cited
  `controls/integrated-selftests.txt` prints `selftest: 35/35 passed` (plus
  `61 isolated CLI fixtures` for `cache_current_age`). The receipt is the
  authority; correct the number in a new entry, never by rewriting filed bytes.
- **R88-B (report accuracy, Gate).** The report's `Sources & frontier` summary
  says "one admit and three rejects"; the cited `corpus/lessons/round-88.md`
  `## Gate` carries two admits (RFC 9111 §4.1; RFC 9110 §12.5.5) and two rejects
  (counter-pass proposition; empty-`Vary` proposition). The cited third reject
  appears only in `w1/L1/round-88-draft.md`. Re-point or append a correction.
- **R88-C (evidence pointer).** "Re-run at `edcb2980` with identical results"
  has no committed receipt under `controls/` and no lesson mention; the counting
  command's `--work` path is ephemeral `/fast/scratch`. Commit the re-run receipt
  with its revision or drop the claim.
- **R88-D (numeric pin).** The `considerthese` measurement "1,577 tracked files
  under `.ufo/waves/round-*/controls/`" names no revision. The count is exact at
  `f60a852a` (1577), but at filing HEAD `741fb728` it is 1590
  (`git ls-tree -r --name-only <rev> | grep -c '/controls/'`). Pin the revision
  in the next filing; the "36 multi-commit files" and "four this round's own
  re-runs" both re-derive (36; four round-88 control files with 3 commits each).
- **R88-E (freeze discipline).** v3 `52e41d2d` landed at 15:58:05, six minutes
  after the 15:52:15 dispatch, while the wave was live; it moved validation
  ahead of the wildcard rule and flipped three seeded labels (`r53`, `r150`,
  `r193`, `mismatch` → `invalid`) and the population digest `004a8eb7…` →
  `52714a5f…`. Disclosed in the contract errata and lesson; keep the
  freeze-then-dispatch order next round.
- **R88-F (lesson shape).** The round's four mistakes sit under `## L1 mistakes`;
  `CORPUS.md` names `## Mistakes` as the section that carries a round's mined
  mistakes, and that section here carries one earlier-round row. Fold or
  cross-reference them in the next lesson.
- **Carried, not new:** R88-1 (seed/oracle table false green), R88-2 (counter
  `is_token` accepts trailing LF), R88-3 (frozen case 14 and 13 seeded labels
  are adapter conventions), R88-4 (6/21 mutants survive), R88-5/6 (D2 accepts a
  hardcoded or float table; D1/D3 match text), D84-2/3 and operator-owned
  literal-planner D84-4 remain open by design.

## Operator notes (not lane defects)

- **SHONEN.** The report keeps `[~]`/`[ ]`/`[~]`/`[~]`; this non-author writes no
  `[x]`. Boxes 1, 3 and 4 look checkable from committed bytes: box 1 has the
  Round-88 registry table in `SKILL.md`; box 3's script/counter paths resolve at
  the carrier; box 4's sweep finds no sibling lane repository path in the 76
  knowledge entries (my `[A-Za-z0-9_./-]*-shokunin` sweep matches only this
  lane's own `kake-shokunin` mentions). Box 2 remains `[ ]` for the historical
  round-47 named-receipt gap. Promotion is operator-owned.
- **Axis ownership.** `MISSION.md`/`shokunin.conf` list `operability + freshness`;
  `SCORECARD.md` scores `calibration` as a round-54 evidence-backed sub-axis.
  C1 works that sub-axis as the lowest non-retired one; the lane scores it 2 and
  holds it. Operator may reflect the sub-axis in MISSION.
- **Prompt routing drift.** §6 pins the run-15 map (reviewer/critic/executor/
  mutation-tester/sentinel `@m_zfl`, scout `@m_antigravity`), while the live
  `~/.omp/agent/config.yml` `agentModelOverrides` now routes reviewer, critic,
  mutation-tester and sentinel `@m_flash`, executor `@m_zfl`, scout `@m_mim`.
  The lane's report lists a third map; the spawn-time table is not committed and
  cannot be re-derived, so this is unprovable here and operator-side. No claim
  depends on a model.

## Closure ruling

Status **ok** (substantive, non-marker report; real committed work; pushed
carrier). Both claims verify on re-measurement; no owned axis is harmed; the
outside spot-check agrees on both sampled admits and both sampled rejects.
**admitted = true**, verdict `admitted` — bounded by the disclosed instrument
limits and with the report defects routed, not rewritten.
