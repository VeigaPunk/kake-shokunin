author: hyaku closure (non-author integrator, @m_zfl)
round: kake 94 (hyaku run 15, attempt 1)
date: 2026-11-05
lane-head-verified: `99a88dea1f4fade18af18de12b4d57d86a0224f5` (= `origin/master`)
base: `0f7d9bbcdd6a9ed36f5bc62b2116ddd040e871a8`; freeze: `ba667b245f26125c13885958498b3b4999756d04`
report: `.ufo/reports/round-94/kake.md` (fleet repo commit `dd7049206dce41033c41eeb9916d93e007734ef3`, author `kake-shokunin <kake@shokunin.local>`)

# Round 94 — non-author closure spot-check

Verdict: **honest stop confirmed; not admitted** (`rejected-honest-stop`). Both claims are unmet
exactly as frozen; the report's account checks out against committed bytes and a live re-opened
source. No owned axis is harmed. This file was written by the closure role only; no lane-authored
file was edited.

## 1. Step-1 conformance

| Check | Result |
|---|---|
| Report committed in fleet repo by lane identity | ok — `git log --format='%an %H' -- .ufo/reports/round-94/kake.md` → `kake-shokunin kake@shokunin.local dd7049206dce41033c41eeb9916d93e007734ef3` ("round-94: kake report") |
| `## SHONEN` heading, one line per box | ok — `grep -c '^## SHONEN'` = 1; four `[~]`/`[ ]` lines matching SHONEN.md's four boxes; no `[x]` written anywhere |
| Cited lane commits exist and are ancestors | ok — `git merge-base --is-ancestor` rc 0 for `0f7d9bbc`, `ba667b24`, `99a88dea` against `master` |
| No uncommitted round work; pushed | ok — `jj-lane.sh state` → `branch=master local=99a88dea remote=99a88dea ahead=0 behind=0 … untracked=0`; `git status --porcelain` empty; `ls-remote origin refs/heads/master` = `99a88dea` |
| Dispatch/completion evidence | ok — `.ufo/watchdog.log` lines 2857/2870 match the digest in the closure order verbatim (launch 11:24:29-03:00 pgid=3839554 attempt=1; complete 12:31:21-03:00 attempt=1) |
| Prompt carries the template contract | ok — sections 1 MISSION/AXES, 2 claims, 2b frontier, 3 L2 floor, 4 report contract, 5 commit/push/L0, 6 hyaku addendum all present; route map delegates to `task.agentModelOverrides` (no model hardcoded in the lane) |
| Marker rule | real committed work with evidence pointers — not a marker; status `ok` available |
| Wave shape | ok — `w1-results.json` `seats=11`, `results` lists 11 named agents (ScoutRFC, ExecC1Repair, ExecC2Mutants, ExecSourceRows, ScribeEntry, ReviewC1, ReviewC2, CriticClaims, MutC1, SentinelScope, ConnectorScope); attack seats 5/11 = 45 % ≥ 25 %; connectors 1 ≤ 2; `w1.ready` + `w1.ready.dispatched` committed |
| Misroot sweep | ok — no kake round-94 file at the fleet root; the report's two named pre-existing items are still the only kake-adjacent ones, plus an unrelated untracked `cases_A.json` (llm-inference-batching content, not kake's; operator awareness only) |
| Freeze before scoring | ok — freeze commit `ba667b24` (11:58:20-03:00) precedes the completion line (12:31:21-03:00) and carries the controls, instrument digests and both claim predicates |

Conformance defects found: none that bar admission; routed items in §5.

## 2. Claim re-checks

Both claims rest on lane-owned gates/counters, so per PROTOCOL §Gate standard (Closure
consequence) I verified their **committed evidence** and did not execute either counter. Plain
re-derivations over committed bytes are mine.

### C1 — calibration (score 2, HOLD): strict self-assessment conformance — **unmet, verified**

- Self-test tally (committed): `controls/ctl-c1-selftest.txt` = `selftest 9/9 planted findings, exit 1 on planted, exit 0 on repaired`, `c1-selftest-exit=0`.
- Frozen-run verdict + revision (committed): `controls/base-c1.txt` line 1 = `C1v94 revision=0f7d9bbc… counter=58028584… lessons=88 entries=81 rows=255 criteria=39 mismatches=15 E1=0 E2=0 E3=0 E4=0 E5=15 pins=ok battery=8/8 predecessor_admits=7/7 floor=2 self_pin=ok met=false`. Independent critic receipts agree: `w1/CriticClaims/c1-base-0f7d9bbc.out` and `c1-head-ba667b24.out` both read `mismatches=15`.
- Instrument digests (committed, re-hashed): `controls/instrument-sha256.txt` values match `git show ba667b24:` bytes of both counters and `frozen/c1-surfaces.json`.
- My plain checks over committed bytes: `git ls-tree` corpus lessons `round-*.md` 87 → 88 and `corpus/knowledge/*.md` 81 → 82 (matches the counter's `lessons=88→89 entries=81→82` populations); `git diff 0f7d9bbc 99a88dea -- SKILL.md` is empty, and likewise base→freeze — so the E5 inputs are byte-identical across the round and the 15 E5 findings cannot have changed. The only route to `met=true` (removing the directory backticks) was rejected and reverted; the landed tip therefore cannot read met.
- The rejected repair is kept as evidence (`w1/ExecC1Repair/skill.diff`) and the critic's falsification grid is committed (`w1/CriticClaims/e5-routes-X0-X3.json`, `e5-routes-X4-X5.json`: X4 de-backtick and X5 fabricated-absence both read `mismatches=0 … met=true` — the counter cannot distinguish gaming from repair; `--skip-battery` variant returns `met=true` with `battery=0/8`, receipt `c1-skip-battery-on-X4-variant.out`).
- Verdict: claim unmet exactly as reported; axis **unchanged** (score stays 2 per the freeze's kill rule). The finding that round 93's `met=true` overstated (its `read()` accepted trees) is recorded, not repaired.

### C2 — freshness (score 10, HOLD), instrument capability — **unmet (39/40), verified**

- Self-test tally (committed): `controls/ctl-c2-selftest.txt` = `selftest 7/7 fixtures scored as declared; drifted-reference cases=4`, `c2-selftest-exit=0`.
- Frozen-run verdicts (committed): `controls/base-c2-v1.txt` `hand=44/44 … met=true` and `controls/base-c2-v2.txt` `hand=53/53 … met=true`, both at revision `0f7d9bbc…`, candidate sha256 `d3bac7de…` recorded in both.
- Population unchanged (my plain check): `git ls-tree` blob of `.ufo/waves/round-93/w1/recovered-partial/MutConditional/mutants-posgood.json` = `f15c99f42ef250baaa21f2e3114b3b634de2734e` at both base and tip.
- Kill counts re-derived by me with jq over the committed scoring artifacts (not a gate execution):
  `git show 99a88dea:.ufo/waves/round-94/w1/ExecC2Mutants/mutants-v1.json` → 31 of 40 with `v1.killed==true`; survivors `M11 M18 M19 M24 M28 M29 M32 M37 M40` — matches `summary.txt` (`v1 killed=31/40`) and the round-93 survivor list.
  `…/mutants-v2.json` → 39 of 40 with `v2.killed==true`; exactly one non-killed: `M11 killed=false`.
- M11 equivalence (committed): `w1/ExecC2Mutants.md` §Equivalence — exhaustive product 115 200 inputs, `differing=0` (`receipts/equiv_m11.py`); independent critic grid `w1/CriticClaims/c2-m11-equivalence.out` = `grid inputs 28512 differences 0`. 40/40 was unattainable as frozen; the report says so honestly.
- Verdict: claim unmet (39/40 < 40/40 target) exactly as reported; axis **unchanged** (score stays 10). The instrument move 31→39 is real but instrument-only (the lane's own CriticClaims §4 wording, which I adopt: not "freshness improved").

### No owned axis harmed

`git diff 0f7d9bbc 99a88dea --name-only` contains only `.ufo/waves/round-94/`, `corpus/`, `SCORECARD.md`, `LOG.md`. The SCORECARD diff is an append-only round-94 section (no axis score row changed); SKILL.md, SHONEN.md, PROVINCE.md, QUALITY.md untouched; SOURCES.md +2 rows, 0 rows modified. No trade anywhere.

### Re-measured vs evidence-verified

- C1: **evidence-verified** (committed self-test tally, frozen-run verdicts at named revisions, committed critic receipts) + plain byte-identity/count checks by me. Neither counter executed by the closure.
- C2: **evidence-verified** plus my own jq re-derivation of the kill counts, survivor set and population/digest identity over committed scoring artifacts.

## 3. Discernment spot-check (LEARNING.md)

Method: sampled 2 admits and 2 rejects from `corpus/lessons/round-94.md` `## Gate`; re-opened the
live source (`https://www.rfc-editor.org/rfc/rfc9110.txt` fetched fresh by the closure: 502 941
bytes, sha256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` — byte-identical
to the lane's retained body, so every line anchor below resolves) and re-read the committed
falsification evidence for the reject that is not source-based.

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| Knowledge entry `corpus/knowledge/http-list-and-method-grammar.md` | admit (Gate) | live RFC 9110 lines 3748–3749, 5928–5932, 1762–1764, 1774 | **agree** | every quoted fragment is an exact substring of the body at the cited lines (whitespace-normalized across the RFC's line wraps); frontmatter carries `source: S477, S478`, `verified-at: 2026-11-05`, `recheck: 180d` |
| Row S477 (RFC 9110 §9.1) | admit (Gate) | live lines 3748–3749; §9.1 heading line 3728 | **agree** | located quote is exact at the recorded lines; ≤ 25 words; digest recorded in the row matches the live fetch |
| S477's first drafted `teaches` clause (all-uppercase convention sentence) | reject (ScoutRFC D1) | live lines 3750–3751 | **agree** | the body breaks `US-` / `ASCII` across the lines, so that sentence is not an exact substring; the reject reason is verified verbatim in the body |
| C1 repair route (de-backtick 13 directory paths) | reject + revert (CriticClaims X4/X5) | committed `e5-routes-X4-X5.json`, `skill.diff`, freeze repair rule | **agree** | the route zeroes the counter while naming no blob — gaming, not calibration; the freeze's repair rule requires naming a concrete non-empty blob; revert restored byte-identity (verified by diff) |
| C2 target 40/40 | not admitted (unreachable) | committed equivalence receipts (115 200 + 28 512 inputs, zero differences) | **agree** | M11 is semantically equivalent to the base candidate; no counter can kill it on this population |

New SOURCES rows re-opened: S477 and S478 (`corpus/SOURCES.md` lines 223–224). S477's quote is
exact at lines 3748–3749. S478's quote (`"a recipient MUST accept lists that satisfy the following
syntax: #element => [ element ] *( OWS "," OWS [ element ] )"`, 22 tokens) is exact after
whitespace normalization across lines 1701–1703; the row's §5.6.3 anchors (heading line 1745,
lines 1762–1764, production line 1774) all resolve, including the empty-element sentences at
1695–1697 that the first draft omitted (D2/D3 correction verified against the live body).

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0,
final line `kake ok …/corpus/SOURCES.md`; W04 duplicate-URL warnings only (existing RFC class,
now including S477/S478 — as the report stated). My row counts: 213 at base → 215 at tip
(`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`), malformed rows 0.

Discernment verdict: the round's gate calls, as finally recorded, agree with the outside check on
every sampled admit and reject; the round's own instruments and targets were falsified by its
attack seats and each landed as a lesson mistake. **Discernment: improved** (LEARNING.md improved
condition met by agreement on admits and rejects, with the agreement grounded in a live re-opened
source).

## 4. Per-axis verdicts and trends

| Axis / trend | Verdict | Evidence |
|---|---|---|
| calibration | unchanged | C1 unmet as frozen; score stays 2; the 15 E5 findings are recorded, not repaired; SKILL.md byte-identical across the round |
| freshness | unchanged | C2 unmet (39/40, M11 equivalent); score stays 10; instrument-only move labeled instrument sensitivity by the lane and adopted by the closure |
| depth / coverage / operability / adjacency | unchanged | no tree change outside wave evidence and corpus additions; PROVINCE.md untouched; ConnectorScope reports overlap in principle only |
| expansion (trend) | improved | 2 tier-A rows (S477, S478; census exit 0) + 1 admitted knowledge entry on method-token and list-member ground not held before, quotes live-verified |
| quality (trend) | unchanged | no admitted entry changed; no entry failed a re-check; SKILL.md no better or worse than at round open |
| discernment (trend) | improved | closure spot-check agrees with the gate on all sampled admits and rejects; disagreements were self-caught by attack seats and mined as Mistakes 5, 7–10 |

Admission: **false** — no claim verifies (both honest unmet), so nothing is admitted even though
no axis is harmed and the landed corpus work is real and verified.

## 5. Routed defects (status-neutral; lane must fix next round)

1. **R94-9 (new, closure): gate registry rows missing.** `c94_selfassess.py`, `c94_conditional.py` and predecessor `c93_conditional.py` have no rows in SKILL.md's `### Owned freshness gate registry` (grep count 0). PROTOCOL §Gate standard: closure grades no gate conformant until its registry row exists at the registry home. Register all three with entry command, verdict map, self-test spelling and pinned-value paths.
2. **Landed-tip receipts uncommitted.** The report's "final run at `99a88dea`" C1/C2 outputs have no committed receipt (scratch `/fast/scratch/hyaku/kake-r94/` removed after landing); `grep` for `revision=99a88dea` and `lessons=89` over the committed tree returns nothing. The quoted outputs in the committed report and the earlier-revision critic receipts carry the evidence, but next round a landed-run receipt belongs in the wave dir (evidence must resolve at closure without the report's own prose).
3. `--skip-battery` returns `met=true` while bypassing the battery and predecessor clauses (CriticClaims D5, receipt committed) — the freeze's met sentence and the flag disagree; fold into R94-1/R94-7.
4. Counter stdout label still `C2v93` on the v2 instrument (lane-recorded D3; frozen file, correctly left unrepaired mid-round).
5. Population base mismatch (D1): the 40 mutants patch the round-93 pos-good bytes, not the scored candidate; accurate under the freeze's "instrument sensitivity" wording but the population base should be pinned explicitly next round.
6. Battery F1 benign shadow (SentinelScope; lane-recorded; R94-2). Already routed by the lane; restated here for the queue.
7. Nit, wording drift: dispatch prompt says axes "operability + freshness (web properties and publishing)"; MISSION.md bucket reads "operability + freshness (web properties)". Mission files win; substance identical.
8. SHONEN note for the operator (promotion is operator-owned): boxes 1, 3, 4 carry resolvable committed evidence pointers and box 2 is an honestly named open gap; every box is checkable by a non-author as filed. No `[x]` was written by the closure.

Open L0 question stands (`kake | round-94 | Ruling wanted on two honest unmet claims`); the closure
does not answer it — R94-1…R94-8 plus R94-9 route to round 95.
